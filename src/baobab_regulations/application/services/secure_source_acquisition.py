"""Rights-before-network, quarantine-before-processing REG-INGEST-02 orchestrator."""

from datetime import UTC, datetime
from uuid import uuid4

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAuthorityPort,
)
from baobab_regulations.application.ports.secure_acquisition import (
    AcquisitionAuthorityPort,
    AcquisitionEvidencePort,
    AcquisitionRightsPort,
    QuarantinePort,
    RegisteredEndpointPort,
    SourceFetcherPort,
    SourceSecurityPort,
)
from baobab_regulations.application.ports.sources import SourceRegistryPort
from baobab_regulations.domain.ingestion.models import (
    AcquisitionCommand,
    AcquisitionResult,
    AcquisitionStatus,
    RightsOutcome,
    SourceEvidenceRecord,
)
from baobab_regulations.domain.shared.ids import RegulatoryId


class AcquisitionIntegrityError(ValueError):
    """A destination, source, payload or rights invariant was violated."""


class SecureSourceAcquisitionService:
    """An offline/worker application service; deliberately not an unauthenticated API.

    All production authorities are mandatory injected ports. A caller-controlled
    tenant, destination URL, rights class or approval flag cannot reach execute().
    """

    def __init__(
        self, *,
        context_authority: ContextAuthorityPort,
        acquisition_authority: AcquisitionAuthorityPort,
        source_registry: SourceRegistryPort,
        endpoints: RegisteredEndpointPort,
        rights: AcquisitionRightsPort,
        fetcher: SourceFetcherPort,
        quarantine: QuarantinePort,
        security: SourceSecurityPort,
        evidence: AcquisitionEvidencePort,
    ) -> None:
        self._context_authority = context_authority
        self._acquisition_authority = acquisition_authority
        self._source_registry = source_registry
        self._endpoints = endpoints
        self._rights = rights
        self._fetcher = fetcher
        self._quarantine = quarantine
        self._security = security
        self._evidence = evidence

    async def execute(
        self, *, command: AcquisitionCommand, caller: AuthenticatedCaller
    ) -> AcquisitionResult:
        # CP redemption binds a verified IAM principal to a canonical tenant.
        if caller.access_token is None:
            raise PermissionError("actual authenticated workload evidence is required")
        context = await self._context_authority.redeem(
            context_id=command.context_id, caller=caller
        )
        tenant = context.tenant_id
        if not tenant:
            raise PermissionError("resolved tenant is missing")
        await self._acquisition_authority.require_acquisition_grant(
            caller=caller, tenant_id=tenant, source_id=command.source_id
        )
        source = await self._source_registry.get_source(RegulatoryId(command.source_id))
        if source is None:
            raise AcquisitionIntegrityError("source must exist in authoritative registry")
        endpoint = await self._endpoints.resolve(
            tenant_id=tenant, source_id=command.source_id,
            endpoint_ref=command.endpoint_ref
        )
        if (endpoint is None or endpoint.source_id != command.source_id
                or endpoint.endpoint_ref != command.endpoint_ref or not endpoint.approved):
            raise AcquisitionIntegrityError("source endpoint has no governed approval")
        acquisition_id = uuid4()
        await self._evidence.start(
            acquisition_id=acquisition_id, tenant_id=tenant,
            source_id=command.source_id, endpoint_ref=command.endpoint_ref,
            actor_ref=caller.subject, requested_at=datetime.now(UTC).isoformat()
        )
        await self._record(acquisition_id, tenant, AcquisitionStatus.RIGHTS_CHECK_PENDING, {})
        try:
            rights = await self._rights.decide(
                tenant_id=tenant, source_id=command.source_id, scope="ACQUIRE_AND_STORE"
            )
            if rights.scope != "ACQUIRE_AND_STORE":
                raise AcquisitionIntegrityError("rights decision scope mismatch")
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.RIGHTS_CHECK_PENDING,
                self._rights_metadata(rights)
            )
            if rights.outcome is not RightsOutcome.ALLOW:
                status = (AcquisitionStatus.CANCELLED
                          if rights.outcome is RightsOutcome.DENY
                          else AcquisitionStatus.RIGHTS_CHECK_PENDING)
                await self._record(acquisition_id, tenant, status, {"reason": "RIGHTS_NOT_ALLOWED"})
                return AcquisitionResult(acquisition_id, tenant, status)

            await self._record(acquisition_id, tenant, AcquisitionStatus.AUTHORIZED, {})
            fetched = await self._fetcher.fetch(endpoint)
            await self._record(acquisition_id, tenant, AcquisitionStatus.FETCHING, {})
            if fetched.media_type not in endpoint.permitted_media_types:
                raise AcquisitionIntegrityError("response media type not permitted")
            if fetched.content_length is not None and (
                fetched.content_length < 0 or fetched.content_length > endpoint.max_bytes
            ):
                raise AcquisitionIntegrityError("Content-Length exceeds permitted size")
            artefact_id = uuid4()
            stored = await self._quarantine.store(
                artefact_id=artefact_id, chunks=fetched.body, max_bytes=endpoint.max_bytes
            )
            if stored.size_bytes == 0:
                raise AcquisitionIntegrityError("empty source response")
            artefact = SourceEvidenceRecord(
                artefact_id=artefact_id, acquisition_id=acquisition_id,
                tenant_id=tenant, source_id=command.source_id,
                endpoint_ref=command.endpoint_ref, storage_ref=stored.storage_ref,
                sha256=stored.content_hash, size_bytes=stored.size_bytes,
                declared_media_type=fetched.media_type, retrieved_at=datetime.now(UTC),
                etag=fetched.etag, last_modified=fetched.last_modified
            )
            # Record immutable evidence before any security or processing decision.
            await self._evidence.artefact(artefact)
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.QUARANTINED,
                {"artefact_id": str(artefact_id), "sha256": stored.content_hash}
            )
            assessment = await self._security.assess(
                artefact=artefact, signature=stored.prefix
            )
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.QUARANTINED,
                {"security_ref": assessment.evidence_ref,
                 "scanner": assessment.scanner_ref,
                 "scanner_version": assessment.scanner_version,
                 "security_result": assessment.reason_code}
            )
            if not assessment.permitted:
                return AcquisitionResult(
                    acquisition_id, tenant, AcquisitionStatus.QUARANTINED, artefact
                )

            processing = await self._rights.decide(
                tenant_id=tenant, source_id=command.source_id, scope="TRANSFORM_AND_PROCESS"
            )
            if processing.scope != "TRANSFORM_AND_PROCESS":
                raise AcquisitionIntegrityError("processing rights scope mismatch")
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.QUARANTINED,
                self._rights_metadata(processing)
            )
            permitted = processing.outcome is RightsOutcome.ALLOW
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.ACQUIRED,
                {"processing_permitted": str(permitted).lower()}
            )
            return AcquisitionResult(
                acquisition_id, tenant, AcquisitionStatus.ACQUIRED,
                artefact, processing_permitted=permitted
            )
        except Exception as exc:
            # No secret-bearing exception text or URL may enter evidence.
            await self._record(
                acquisition_id, tenant, AcquisitionStatus.FAILED,
                {"error_type": type(exc).__name__}
            )
            raise

    async def _record(
        self, acquisition_id: object, tenant: str,
        status: AcquisitionStatus, details: dict[str, str]
    ) -> None:
        from uuid import UUID

        assert isinstance(acquisition_id, UUID)
        await self._evidence.event(
            acquisition_id=acquisition_id, tenant_id=tenant,
            status=status.value, details=details
        )

    @staticmethod
    def _rights_metadata(rights: object) -> dict[str, str]:
        from baobab_regulations.domain.ingestion.models import RightsDecision

        assert isinstance(rights, RightsDecision)
        return {
            "rights_scope": rights.scope,
            "rights_outcome": rights.outcome.value,
            "rights_profile": rights.profile_ref,
            "rights_revision": rights.revision,
            "rights_decision_id": rights.decision_id,
            "rights_evidence_refs": ",".join(rights.evidence_refs),
        }

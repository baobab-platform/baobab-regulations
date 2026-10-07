"""R-CAP-02 application adapter for regulations.evidence.assess."""

import hashlib
import json
import re

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityPort,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
)
from baobab_regulations.application.ports.evidence_assessment import (
    DocumentaryEvidenceAssessorPort,
    DocumentaryEvidenceAssessorUnavailableError,
    EvidenceAssessmentIdentity,
)
from baobab_regulations.application.ports.idempotency import (
    EvidenceAssessmentIdempotencyPort,
    IdempotencyAuthorityUnavailableError,
    IdempotencyConflictError,
    IdempotencyIntegrityError,
)
from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityUnavailableError,
    RequirementLookupStatus,
    RequirementRepositoryPort,
)
from baobab_regulations.contracts.rtd06 import (
    CrossEngineObjectReference,
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    PinnedRegulationsReference,
    RegulatoryDocumentRequirementProjection,
)

_IDEMPOTENCY_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


class EvidenceAssessmentAuthenticationError(PermissionError):
    """The caller token could not be independently verified for the context."""

    code = "REGULATIONS_EVIDENCE_AUTHENTICATION_FAILED"


class EvidenceAssessmentContextNotFoundError(LookupError):
    """Context is unavailable to this caller without revealing why."""

    code = "REGULATIONS_CONTEXT_NOT_FOUND"


class EvidenceAssessmentAccessDeniedError(PermissionError):
    """Caller/context/reference authority mismatch."""

    code = "REGULATIONS_EVIDENCE_ASSESSMENT_ACCESS_DENIED"


class EvidenceAssessmentNotFoundError(LookupError):
    """The exact requirement identity is not known to Regulations."""

    code = "REGULATIONS_EVIDENCE_REQUIREMENT_NOT_FOUND"


class EvidenceAssessmentConflictError(RuntimeError):
    """Request references or idempotency semantics conflict with governed state."""

    code = "REGULATIONS_EVIDENCE_ASSESSMENT_CONFLICT"


class EvidenceAssessmentUnavailableError(RuntimeError):
    """A required authority or assessment runtime is unavailable."""

    code = "REGULATIONS_EVIDENCE_ASSESSMENT_AUTHORITY_UNAVAILABLE"


class EvidenceAssessmentIntegrityError(RuntimeError):
    """A dependency returned a result inconsistent with the trusted request."""

    code = "REGULATIONS_EVIDENCE_ASSESSMENT_INTEGRITY_FAILURE"


class EvidenceAssessmentInvalidIdempotencyKeyError(ValueError):
    """Idempotency-Key does not satisfy the exact RTD-06 OpenAPI contract."""

    code = "REGULATIONS_EVIDENCE_ASSESSMENT_INVALID_IDEMPOTENCY_KEY"


class EvidenceAssessmentService:
    """Assess bounded Trade Docs facts against one exact Regulations requirement.

    The service owns orchestration and authority checks only. The assessor owns
    legal-sufficiency evaluation; Trade Docs facts remain immutable inputs.
    """

    def __init__(
        self,
        *,
        contexts: ContextAuthorityPort,
        requirements: RequirementRepositoryPort,
        assessor: DocumentaryEvidenceAssessorPort,
        idempotency: EvidenceAssessmentIdempotencyPort,
    ) -> None:
        self._contexts = contexts
        self._requirements = requirements
        self._assessor = assessor
        self._idempotency = idempotency

    async def assess(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        caller: AuthenticatedCaller,
        idempotency_key: str,
    ) -> DocumentEvidenceAssessmentResult:
        key = self._validate_idempotency_key(idempotency_key)

        try:
            trusted_context = await self._contexts.redeem(
                context_id=request.context_id,
                caller=caller,
            )
        except ContextAuthenticationError as exc:
            raise EvidenceAssessmentAuthenticationError(
                "caller token could not be verified for the supplied context_id"
            ) from exc
        except ContextNotFoundError as exc:
            raise EvidenceAssessmentContextNotFoundError(
                "supplied context_id is unavailable to this caller"
            ) from exc
        except ContextAccessDeniedError as exc:
            raise EvidenceAssessmentAccessDeniedError(
                "caller is not authorised for the supplied context_id"
            ) from exc
        except ContextAuthorityUnavailableError as exc:
            raise EvidenceAssessmentUnavailableError(
                "Control Plane context authority is unavailable"
            ) from exc

        tenant_id = trusted_context.tenant_id
        self._enforce_request_tenant(request=request, trusted_tenant_id=tenant_id)

        try:
            lookup = await self._requirements.resolve_exact(request.requirement_reference)
        except RequirementAuthorityUnavailableError as exc:
            raise EvidenceAssessmentUnavailableError(
                "Regulations requirement authority is unavailable"
            ) from exc

        if lookup.status is RequirementLookupStatus.NOT_FOUND:
            raise EvidenceAssessmentNotFoundError(
                "exact Regulations requirement was not found"
            )
        if lookup.status is RequirementLookupStatus.CONFLICT:
            raise EvidenceAssessmentConflictError(
                "requirement reference is stale, superseded, or conflicts with governed state"
            )

        requirement = lookup.requirement
        if requirement is None:
            raise EvidenceAssessmentIntegrityError(
                "requirement repository returned FOUND without a projection"
            )

        self._validate_requirement_consistency(
            request=request,
            requirement=requirement,
            trusted_tenant_id=tenant_id,
        )

        request_fingerprint = self._request_fingerprint(request)
        try:
            replay = await self._idempotency.replay(
                tenant_id=tenant_id,
                idempotency_key=key,
                request_fingerprint=request_fingerprint,
            )
        except IdempotencyConflictError as exc:
            raise EvidenceAssessmentConflictError(
                "Idempotency-Key was already used for a different assessment request"
            ) from exc
        except IdempotencyIntegrityError as exc:
            raise EvidenceAssessmentIntegrityError(
                "persisted assessment state failed integrity validation"
            ) from exc
        except IdempotencyAuthorityUnavailableError as exc:
            raise EvidenceAssessmentUnavailableError(
                "assessment idempotency authority is unavailable"
            ) from exc

        if replay is not None:
            self._validate_result_integrity(
                request=request,
                result=replay.result,
                trusted_tenant_id=tenant_id,
            )
            return replay.result

        identity = EvidenceAssessmentIdentity(
            assessment_id=self._assessment_id(tenant_id=tenant_id, idempotency_key=key),
            tenant_id=tenant_id,
        )
        try:
            result = await self._assessor.assess(
                request=request,
                requirement=requirement,
                identity=identity,
            )
        except DocumentaryEvidenceAssessorUnavailableError as exc:
            raise EvidenceAssessmentUnavailableError(
                "Regulations documentary assessment runtime is unavailable"
            ) from exc

        self._validate_result_integrity(
            request=request,
            result=result,
            trusted_tenant_id=tenant_id,
        )

        try:
            committed = await self._idempotency.commit(
                tenant_id=tenant_id,
                idempotency_key=key,
                request_fingerprint=request_fingerprint,
                request=request,
                result=result,
            )
        except IdempotencyConflictError as exc:
            raise EvidenceAssessmentConflictError(
                "Idempotency-Key was concurrently committed for a different request"
            ) from exc
        except IdempotencyIntegrityError as exc:
            raise EvidenceAssessmentIntegrityError(
                "persisted assessment state failed integrity validation"
            ) from exc
        except IdempotencyAuthorityUnavailableError as exc:
            raise EvidenceAssessmentUnavailableError(
                "assessment idempotency authority is unavailable"
            ) from exc

        # The durable store owns the authoritative result under concurrency.
        # A simultaneous caller may have committed first with the same
        # fingerprint; in that case every caller returns that one stored result.
        self._validate_result_integrity(
            request=request,
            result=committed.result,
            trusted_tenant_id=tenant_id,
        )
        return committed.result

    @staticmethod
    def _validate_idempotency_key(value: str) -> str:
        key = value.strip()
        if not 16 <= len(key) <= 128 or _IDEMPOTENCY_KEY.fullmatch(key) is None:
            raise EvidenceAssessmentInvalidIdempotencyKeyError(
                "Idempotency-Key must be 16-128 characters and match "
                "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
            )
        return key

    @staticmethod
    def _request_fingerprint(request: DocumentEvidenceAssessmentRequest) -> str:
        encoded = json.dumps(
            request.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _assessment_id(*, tenant_id: str, idempotency_key: str) -> str:
        digest = hashlib.sha256(f"{tenant_id}\n{idempotency_key}".encode()).hexdigest()
        return f"regassess_{digest[:24]}"

    def _enforce_request_tenant(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        trusted_tenant_id: str,
    ) -> None:
        self._enforce_reference_tenant(
            reference=request.regulatory_decision_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        self._enforce_reference_tenant(
            reference=request.requirement_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        for evidence in request.evidence:
            self._enforce_reference_tenant(
                reference=evidence.document_version_reference,
                trusted_tenant_id=trusted_tenant_id,
            )
            for reference in evidence.subject_references:
                self._enforce_reference_tenant(
                    reference=reference,
                    trusted_tenant_id=trusted_tenant_id,
                )
            for reference in evidence.content_artifact_references:
                self._enforce_reference_tenant(
                    reference=reference,
                    trusted_tenant_id=trusted_tenant_id,
                )
            for assertion in evidence.documentary_assertions:
                if assertion.source_artifact_reference is not None:
                    self._enforce_reference_tenant(
                        reference=assertion.source_artifact_reference,
                        trusted_tenant_id=trusted_tenant_id,
                    )

    def _validate_requirement_consistency(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        requirement: RegulatoryDocumentRequirementProjection,
        trusted_tenant_id: str,
    ) -> None:
        if requirement.requirement_reference != request.requirement_reference:
            raise EvidenceAssessmentIntegrityError(
                "resolved requirement reference does not equal the exact requested pin"
            )
        if requirement.regulatory_decision_reference != request.regulatory_decision_reference:
            raise EvidenceAssessmentConflictError(
                "requirement is not valid for the supplied pinned RegulatoryDecision"
            )
        self._enforce_reference_tenant(
            reference=requirement.requirement_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        self._enforce_reference_tenant(
            reference=requirement.regulatory_decision_reference,
            trusted_tenant_id=trusted_tenant_id,
        )

    def _validate_result_integrity(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        result: DocumentEvidenceAssessmentResult,
        trusted_tenant_id: str,
    ) -> None:
        if result.regulatory_decision_reference != request.regulatory_decision_reference:
            raise EvidenceAssessmentIntegrityError(
                "assessment result changed the requested RegulatoryDecision reference"
            )
        if result.requirement_reference != request.requirement_reference:
            raise EvidenceAssessmentIntegrityError(
                "assessment result changed the requested requirement reference"
            )

        self._enforce_reference_tenant(
            reference=result.assessment_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        self._enforce_reference_tenant(
            reference=result.regulatory_decision_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        self._enforce_reference_tenant(
            reference=result.requirement_reference,
            trusted_tenant_id=trusted_tenant_id,
        )
        if result.resulting_regulatory_decision_reference is not None:
            self._enforce_reference_tenant(
                reference=result.resulting_regulatory_decision_reference,
                trusted_tenant_id=trusted_tenant_id,
            )

        supplied = {
            evidence.document_version_reference.model_dump_json()
            for evidence in request.evidence
        }
        accepted = {
            reference.model_dump_json()
            for reference in result.accepted_document_version_references
        }
        rejected = {
            item.document_version_reference.model_dump_json()
            for item in result.rejected_evidence
        }
        if not accepted.issubset(supplied) or not rejected.issubset(supplied):
            raise EvidenceAssessmentIntegrityError(
                "assessment result referenced documentary evidence not supplied by the request"
            )
        if accepted & rejected:
            raise EvidenceAssessmentIntegrityError(
                "the same DocumentVersion cannot be both accepted and rejected"
            )

    @staticmethod
    def _enforce_reference_tenant(
        *,
        reference: PinnedRegulationsReference | CrossEngineObjectReference,
        trusted_tenant_id: str,
    ) -> None:
        if reference.scope != "tenant":
            return
        if reference.tenant_id != trusted_tenant_id:
            raise EvidenceAssessmentAccessDeniedError(
                "tenant-scoped reference does not match trusted context tenant"
            )


__all__ = [
    "EvidenceAssessmentAccessDeniedError",
    "EvidenceAssessmentAuthenticationError",
    "EvidenceAssessmentContextNotFoundError",
    "EvidenceAssessmentConflictError",
    "EvidenceAssessmentIntegrityError",
    "EvidenceAssessmentInvalidIdempotencyKeyError",
    "EvidenceAssessmentNotFoundError",
    "EvidenceAssessmentService",
    "EvidenceAssessmentUnavailableError",
]

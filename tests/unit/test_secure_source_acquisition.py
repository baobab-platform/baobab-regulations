"""REG-INGEST-02 positive/negative acquisition and evidence ordering."""

import hashlib
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    TrustedPlatformContext,
)
from baobab_regulations.application.services.secure_source_acquisition import (
    AcquisitionIntegrityError,
    SecureSourceAcquisitionService,
)
from baobab_regulations.domain.ingestion.models import (
    AcquisitionCommand,
    AcquisitionStatus,
    FetchedSource,
    RegisteredEndpoint,
    RightsDecision,
    RightsOutcome,
    SecurityAssessment,
)
from baobab_regulations.domain.shared.ids import RegulatoryId
from baobab_regulations.domain.sources.models import AuthoritativeSource
from baobab_regulations.infrastructure.acquisition.quarantine_memory import (
    InMemoryQuarantine,
    QuarantineLimitExceeded,
)
from baobab_regulations.infrastructure.acquisition.security import (
    QuarantineOnlySecurity,
    signature_matches,
)
from baobab_regulations.infrastructure.persistence.acquisition_memory import (
    InMemoryAcquisitionEvidence,
)
from baobab_regulations.infrastructure.persistence.sources_memory import (
    InMemorySourceRegistry,
)

TENANT = "tn_01k4m7x9q2v6c8r3d5f1h0j4"


async def stream(*chunks: bytes) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk


class FakeContext:
    def __init__(self, tenant: str = TENANT) -> None:
        self.tenant = tenant

    async def redeem(self, *, context_id, caller):
        return TrustedPlatformContext(context_id, self.tenant)


class FakeGrant:
    def __init__(self, deny: bool = False) -> None:
        self.deny = deny

    async def require_acquisition_grant(self, *, caller, tenant_id, source_id):
        if self.deny:
            raise PermissionError("CP capability grant denied")


class FakeEndpointRegistry:
    def __init__(self, endpoint: RegisteredEndpoint | None) -> None:
        self.endpoint = endpoint

    async def resolve(self, *, tenant_id, source_id, endpoint_ref):
        return self.endpoint


class FakeRights:
    def __init__(
        self, acquire: RightsOutcome = RightsOutcome.ALLOW,
        process: RightsOutcome = RightsOutcome.ALLOW,
    ) -> None:
        self.acquire = acquire
        self.process = process
        self.calls: list[str] = []

    async def decide(self, *, tenant_id, source_id, scope):
        self.calls.append(scope)
        outcome = self.acquire if scope == "ACQUIRE_AND_STORE" else self.process
        return RightsDecision(
            scope=scope,
            outcome=outcome,
            profile_ref="rights_governed_official",
            revision="rev_1",
            evidence_refs=("licence_fixture_1",) if outcome is RightsOutcome.ALLOW else (),
            decision_id="rights_decision_" + str(len(self.calls)),
        )


class FakeFetcher:
    def __init__(self, data: bytes = b"%PDF-1.7\nfixture", *, reported_size=None):
        self.data = data
        self.reported_size = reported_size
        self.calls = 0

    async def fetch(self, endpoint):
        self.calls += 1
        return FetchedSource(
            body=stream(self.data[:3], self.data[3:]),
            media_type="application/pdf",
            content_length=self.reported_size,
            etag='"revision-2026"',
            last_modified="Tue, 27 Oct 2026 10:00:00 GMT",
        )


class FakeSecurity:
    def __init__(self, *, permitted: bool = True):
        self.permitted = permitted
        self.calls = 0

    async def assess(self, *, artefact, signature):
        self.calls += 1
        return SecurityAssessment(
            permitted=self.permitted,
            scanner_ref="mock-qualified-test-scanner",
            scanner_version="v1",
            evidence_ref="test-scan-1",
            reason_code="TEST_PASSED" if self.permitted else "MALWARE_BLOCKED",
        )


def endpoint(**overrides):
    kwargs = {
        "source_id": "reg_official_1",
        "endpoint_ref": "official_pdf",
        "uri": "https://gazette.example.org/regulation.pdf",
        "allowed_hosts": frozenset({"gazette.example.org"}),
        "permitted_media_types": frozenset({"application/pdf"}),
        "max_bytes": 1024,
        "adapter_id": "pinned-https",
        "adapter_version": "1",
        "approved": True,
    }
    kwargs.update(overrides)
    return RegisteredEndpoint(**kwargs)


async def make_service(
    *, rights=None, fetcher=None, security=None, ep=None, grant=None,
    context=None, include_source=True
):
    sources = InMemorySourceRegistry()
    if include_source:
        await sources.save_source(
            AuthoritativeSource(
                source_id=RegulatoryId("reg_official_1"),
                name="Synthetic Gazette",
                publisher="Synthetic Official Registry",
            )
        )
    evidence = InMemoryAcquisitionEvidence()
    quarantine = InMemoryQuarantine()
    fetcher = fetcher or FakeFetcher()
    rights = rights or FakeRights()
    security = security or FakeSecurity()
    service = SecureSourceAcquisitionService(
        context_authority=context or FakeContext(),
        acquisition_authority=grant or FakeGrant(),
        source_registry=sources,
        endpoints=FakeEndpointRegistry(endpoint() if ep is None else ep),
        rights=rights,
        fetcher=fetcher,
        quarantine=quarantine,
        security=security,
        evidence=evidence,
    )
    return service, evidence, quarantine, rights, fetcher, security


def command():
    return AcquisitionCommand(
        source_id="reg_official_1",
        endpoint_ref="official_pdf",
        context_id=uuid4(),
    )


def caller():
    return AuthenticatedCaller(
        subject="issuer:principal-fixture", access_token="synthetic-test-token-with-context"
    )


@pytest.mark.asyncio
async def test_success_is_source_evidence_not_canonical_publication():
    service, journal, quarantine, rights, fetcher, security = await make_service()
    result = await service.execute(command=command(), caller=caller())
    assert result.status is AcquisitionStatus.ACQUIRED
    assert result.processing_permitted
    assert fetcher.calls == security.calls == 1
    assert rights.calls == ["ACQUIRE_AND_STORE", "TRANSFORM_AND_PROCESS"]
    assert result.artefact is not None
    assert result.artefact.authenticity == "UNVERIFIED"
    assert result.artefact.sha256 == hashlib.sha256(fetcher.data).hexdigest()
    assert await quarantine.verify(
        artefact_id=result.artefact.artefact_id,
        expected_sha256=result.artefact.sha256,
    )
    statuses = [e.status for e in journal.events]
    assert statuses.index("QUARANTINED") < statuses.index("ACQUIRED")
    assert not hasattr(service, "publish_rule")


@pytest.mark.parametrize("outcome", [RightsOutcome.DENY, RightsOutcome.HOLD])
@pytest.mark.asyncio
async def test_unapproved_rights_never_call_network(outcome):
    rights = FakeRights(acquire=outcome)
    service, journal, _, _, fetcher, _ = await make_service(rights=rights)
    result = await service.execute(command=command(), caller=caller())
    assert result.status is (
        AcquisitionStatus.CANCELLED if outcome is RightsOutcome.DENY
        else AcquisitionStatus.RIGHTS_CHECK_PENDING
    )
    assert fetcher.calls == 0
    assert not journal.artefacts


@pytest.mark.asyncio
async def test_unverified_or_missing_canonical_context_denies_before_any_io():
    service, journal, _, rights, fetcher, _ = await make_service(
        grant=FakeGrant(deny=True)
    )
    with pytest.raises(PermissionError):
        await service.execute(command=command(), caller=caller())
    assert not journal.starts and not rights.calls and not fetcher.calls
    with pytest.raises(PermissionError):
        await service.execute(
            command=command(), caller=AuthenticatedCaller(subject="unbound")
        )


@pytest.mark.asyncio
async def test_unregistered_source_or_mismatched_endpoint_denies():
    service, journal, _, rights, fetcher, _ = await make_service(
        include_source=False
    )
    with pytest.raises(AcquisitionIntegrityError):
        await service.execute(command=command(), caller=caller())
    assert not journal.starts and not rights.calls and not fetcher.calls
    service, journal, _, rights, fetcher, _ = await make_service(
        ep=endpoint(source_id="wrong_source")
    )
    with pytest.raises(AcquisitionIntegrityError):
        await service.execute(command=command(), caller=caller())
    assert not journal.starts and not rights.calls and not fetcher.calls


@pytest.mark.asyncio
async def test_unapproved_endpoint_construction_fails_closed():
    with pytest.raises(ValueError, match="not approved"):
        endpoint(approved=False)


@pytest.mark.asyncio
async def test_security_failure_quarantines_and_never_checks_processing_rights():
    security = FakeSecurity(permitted=False)
    service, journal, _, rights, _, _ = await make_service(security=security)
    result = await service.execute(command=command(), caller=caller())
    assert result.status is AcquisitionStatus.QUARANTINED
    assert not result.processing_permitted
    assert result.artefact is not None
    assert rights.calls == ["ACQUIRE_AND_STORE"]
    assert [e.status for e in journal.events][-1] == "QUARANTINED"


@pytest.mark.asyncio
async def test_default_signature_gate_never_certifies_malware_clean():
    service, _, _, rights, _, _ = await make_service(
        security=QuarantineOnlySecurity()
    )
    result = await service.execute(command=command(), caller=caller())
    assert result.status is AcquisitionStatus.QUARANTINED
    assert rights.calls == ["ACQUIRE_AND_STORE"]


@pytest.mark.asyncio
async def test_processing_rights_hold_keeps_evidence_without_permission():
    service, journal, _, rights, _, _ = await make_service(
        rights=FakeRights(process=RightsOutcome.HOLD)
    )
    result = await service.execute(command=command(), caller=caller())
    assert result.status is AcquisitionStatus.ACQUIRED
    assert result.artefact is not None
    assert not result.processing_permitted
    assert len(journal.artefacts) == 1
    assert rights.calls == ["ACQUIRE_AND_STORE", "TRANSFORM_AND_PROCESS"]


@pytest.mark.asyncio
async def test_hard_stream_limit_denies_and_does_not_leave_partial_quarantine():
    fetcher = FakeFetcher(b"%PDF-" + b"X" * 4096)
    service, journal, quarantine, _, _, _ = await make_service(fetcher=fetcher)
    with pytest.raises(QuarantineLimitExceeded):
        await service.execute(command=command(), caller=caller())
    assert journal.events[-1].status == "FAILED"
    assert not journal.artefacts
    assert not quarantine._objects  # internal synthetic store only


@pytest.mark.asyncio
async def test_false_content_length_fails_before_quarantine():
    fetcher = FakeFetcher(reported_size=999999)
    service, journal, _, _, _, _ = await make_service(fetcher=fetcher)
    with pytest.raises(AcquisitionIntegrityError, match="Content-Length"):
        await service.execute(command=command(), caller=caller())
    assert not journal.artefacts
    assert journal.events[-1].details == {"error_type": "AcquisitionIntegrityError"}


@pytest.mark.asyncio
async def test_same_bytes_have_distinct_evidentiary_identity():
    service, journal, _, _, _, _ = await make_service()
    first = await service.execute(command=command(), caller=caller())
    second = await service.execute(command=command(), caller=caller())
    assert first.artefact is not None
    assert second.artefact is not None
    assert first.artefact.sha256 == second.artefact.sha256
    assert first.artefact.artefact_id != second.artefact.artefact_id
    assert first.acquisition_id != second.acquisition_id
    assert len(journal.artefacts) == 2


def test_untrusted_formats_and_archives_stay_quarantined():
    assert signature_matches("application/pdf", b"%PDF-1.7\n")
    assert not signature_matches("application/pdf", b"<script>spoofed</script>")
    assert not signature_matches("application/pdf", b"PK\x03\x04archive")
    assert not signature_matches("text/plain", b"\x00binary")
    assert not signature_matches("application/zip", b"PK\x03\x04archive")
    assert not signature_matches("application/xml", b"<!ENTITY external>")
    assert not signature_matches("application/x-tar", b"hello")
    assert not signature_matches("unknown/type", b"payload")


def test_rights_allow_must_have_evidence():
    with pytest.raises(ValueError, match="rights evidence"):
        RightsDecision(
            scope="ACQUIRE_AND_STORE",
            outcome=RightsOutcome.ALLOW,
            profile_ref="r",
            revision="v1",
            evidence_refs=(),
            decision_id="d",
        )

"""R-CAP-04 authenticated/context-bound RTD-06 HTTP routes."""

import asyncio
from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient

from baobab_regulations.api.app import create_app
from baobab_regulations.api.runtime import CapabilityApiRuntime
from baobab_regulations.application.ports.authentication import (
    WorkloadAuthenticationError,
    WorkloadAuthenticationUnavailableError,
)
from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
    TrustedPlatformContext,
)
from baobab_regulations.application.services.evidence_assessment import EvidenceAssessmentService
from baobab_regulations.application.services.requirement_resolution import (
    RequirementResolutionService,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    RegulatoryDecisionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
)
from baobab_regulations.infrastructure.evaluation.documentary import (
    ProjectionDocumentaryEvidenceAssessor,
)
from baobab_regulations.infrastructure.persistence.idempotency_memory import (
    InMemoryEvidenceAssessmentIdempotency,
)
from baobab_regulations.infrastructure.persistence.requirements_memory import (
    InMemoryRequirementRepository,
)

CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
OTHER_TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
VALID_TOKEN = "valid-workload-token-r-cap-04"
IDEMPOTENCY_KEY = "r-cap-04-assessment-0001"
EVALUATED_AT = datetime(2026, 10, 6, 9, 30, tzinfo=UTC)


class FakeAuthenticator:
    def __init__(self, *, unavailable: bool = False) -> None:
        self.unavailable = unavailable

    async def authenticate(self, access_token: str) -> AuthenticatedCaller:
        if self.unavailable:
            raise WorkloadAuthenticationUnavailableError("auth unavailable")
        if access_token != VALID_TOKEN:
            raise WorkloadAuthenticationError("invalid token")
        return AuthenticatedCaller(
            subject="workload:trade-docs",
            client_id="baobab-trade-docs-workload",
            scopes=frozenset(),
        )


class FakeContextAuthority:
    def __init__(self, *, mode: str = "allow") -> None:
        self.mode = mode

    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        assert caller.access_token == VALID_TOKEN
        if self.mode == "auth":
            raise ContextAuthenticationError("subject invalid")
        if self.mode == "not-found":
            raise ContextNotFoundError("context hidden")
        if self.mode == "denied":
            raise ContextAccessDeniedError("tenant denied")
        if self.mode == "unavailable":
            raise ContextAuthorityUnavailableError("cp unavailable")
        assert context_id == CONTEXT_ID
        return TrustedPlatformContext(context_id=context_id, tenant_id=TENANT_ID)


def _requirement_reference(*, tenant_id: str = TENANT_ID) -> RegulatoryRequirementReference:
    return RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_01k7rtd6phyto01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _decision_reference() -> RegulatoryDecisionReference:
    return RegulatoryDecisionReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_DECISION",
        object_id="regdec_01k7rtd6decision01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_ID,
    )


def _projection() -> RegulatoryDocumentRequirementProjection:
    return RegulatoryDocumentRequirementProjection(
        requirement_reference=_requirement_reference(),
        regulatory_decision_reference=_decision_reference(),
        requirement_kind="DOCUMENT",
        requirement_code="PHYTOSANITARY_CERTIFICATE_REQUIRED",
        purpose_code="SPS",
        acceptable_document_types=["PHYTOSANITARY_CERTIFICATE"],
        required_issuer_roles=[],
        required_data_elements=[],
        unsatisfied_effect_code="SPS_HOLD_REQUIRED",
        effective_from=datetime(2026, 10, 5, tzinfo=UTC),
        effective_to=None,
        determined_at=datetime(2026, 10, 5, 20, 30, tzinfo=UTC),
    )


def _runtime(
    *,
    context_mode: str = "allow",
    auth_unavailable: bool = False,
    idempotency: InMemoryEvidenceAssessmentIdempotency | None = None,
) -> CapabilityApiRuntime:
    contexts = FakeContextAuthority(mode=context_mode)
    requirements = InMemoryRequirementRepository([_projection()])
    return CapabilityApiRuntime(
        authenticator=FakeAuthenticator(unavailable=auth_unavailable),
        requirement_resolution=RequirementResolutionService(
            contexts=contexts,
            requirements=requirements,
        ),
        evidence_assessment=EvidenceAssessmentService(
            contexts=contexts,
            requirements=requirements,
            assessor=ProjectionDocumentaryEvidenceAssessor(clock=lambda: EVALUATED_AT),
            idempotency=idempotency or InMemoryEvidenceAssessmentIdempotency(),
        ),
    )


def _requirement_body(*, tenant_id: str = TENANT_ID) -> dict[str, object]:
    return {
        "context_id": str(CONTEXT_ID),
        "requirement_reference": _requirement_reference(
            tenant_id=tenant_id
        ).model_dump(mode="json"),
    }


def _evidence_body() -> dict[str, object]:
    return {
        "context_id": str(CONTEXT_ID),
        "regulatory_decision_reference": _decision_reference().model_dump(mode="json"),
        "requirement_reference": _requirement_reference().model_dump(mode="json"),
        "assessment_reason": "INITIAL_EVIDENCE",
        "evidence": [
            {
                "document_version_reference": {
                    "owner_engine_id": "baobab-trade-docs",
                    "object_type": "DOCUMENT_VERSION",
                    "object_id": "tdocv_01k7rtd4001v1",
                    "reference_mode": "IDENTITY_PINNED",
                    "scope": "tenant",
                    "tenant_id": TENANT_ID,
                },
                "document_type": "PHYTOSANITARY_CERTIFICATE",
                "document_family": "REGULATORY",
                "issuer_claim": {
                    "party_reference": "org_ug_nppo",
                    "issuer_role": "COMPETENT_AUTHORITY",
                },
                "verification": {
                    "verification_state": "VERIFIED",
                    "reason_code": "ISSUER_AND_SIGNATURE_VERIFIED",
                    "observed_at": "2026-10-05T20:31:00Z",
                },
                "temporal_validity": {
                    "temporal_validity_state": "CURRENTLY_VALID",
                    "observed_at": "2026-10-05T20:31:00Z",
                },
                "subject_references": [],
                "documentary_assertions": [],
                "content_artifact_references": [],
                "facts_observed_at": "2026-10-05T20:31:00Z",
            }
        ],
    }


def _headers(**extra: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {VALID_TOKEN}", **extra}


def test_requirement_route_requires_workload_bearer() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post("/documentary-requirements/resolve", json=_requirement_body())

    assert response.status_code == 401
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "AUTH_TOKEN_REQUIRED"


def test_invalid_workload_bearer_is_unauthorized() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers={"Authorization": "Bearer invalid-workload-token-value"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "AUTH_TOKEN_INVALID"


def test_unconfigured_capability_runtime_fails_closed() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 503
    assert response.json()["code"] == "CAPABILITY_RUNTIME_UNAVAILABLE"
    assert response.json()["retryable"] is True


def test_requirement_route_resolves_exact_pinned_requirement() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 200
    assert response.json()["requirement"]["requirement_code"] == (
        "PHYTOSANITARY_CERTIFICATE_REQUIRED"
    )


def test_legacy_tenant_header_cannot_override_caller_bound_context() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(**{"X-Baobab-Tenant-ID": OTHER_TENANT_ID}),
    )

    assert response.status_code == 200


def test_nested_tenant_mismatch_is_forbidden() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(tenant_id=OTHER_TENANT_ID),
        headers=_headers(),
    )

    assert response.status_code == 403
    assert response.json()["code"] == "REGULATIONS_REQUIREMENT_ACCESS_DENIED"


def test_not_owned_context_is_indistinguishable_not_found() -> None:
    client = TestClient(create_app(_runtime(context_mode="not-found")))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 404
    assert response.json()["code"] == "REGULATIONS_CONTEXT_NOT_FOUND"


def test_independent_subject_verification_failure_is_unauthorized() -> None:
    client = TestClient(create_app(_runtime(context_mode="auth")))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 401
    assert response.json()["code"] == "REGULATIONS_REQUIREMENT_AUTHENTICATION_FAILED"


def test_canonical_body_validation_returns_400_not_422() -> None:
    client = TestClient(create_app(_runtime()))
    body = _requirement_body()
    body["tenant_id"] = TENANT_ID

    response = client.post(
        "/documentary-requirements/resolve",
        json=body,
        headers=_headers(),
    )

    assert response.status_code == 400
    assert response.json()["code"] == "VALIDATION_FAILED"


def test_invalid_correlation_id_returns_problem_details() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(**{"X-Correlation-ID": "not-a-uuid"}),
    )

    assert response.status_code == 400
    assert response.json()["code"] == "CORRELATION_ID_INVALID"
    UUID(response.json()["correlation_id"])


def test_valid_correlation_id_is_preserved() -> None:
    client = TestClient(create_app(_runtime()))
    correlation_id = "7d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f11"

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(**{"X-Correlation-ID": correlation_id}),
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id


def test_invalid_traceparent_returns_400() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(traceparent="00-deadbeef-deadbeef-01"),
    )

    assert response.status_code == 400
    assert response.json()["code"] == "TRACEPARENT_INVALID"


def test_evidence_route_requires_idempotency_key() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-evidence/assessments",
        json=_evidence_body(),
        headers=_headers(),
    )

    assert response.status_code == 400
    assert response.json()["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_evidence_route_assesses_documentary_facts() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/documentary-evidence/assessments",
        json=_evidence_body(),
        headers=_headers(**{"Idempotency-Key": IDEMPOTENCY_KEY}),
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "SATISFIED"
    assert response.json()["resulting_regulatory_decision_reference"] is None


def test_evidence_route_preserves_correlation_and_trace_in_canonical_event() -> None:
    store = InMemoryEvidenceAssessmentIdempotency()
    client = TestClient(create_app(_runtime(idempotency=store)))
    correlation_id = "7d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f11"
    traceparent = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    body = _evidence_body()

    response = client.post(
        "/documentary-evidence/assessments",
        json=body,
        headers=_headers(
            **{
                "Idempotency-Key": IDEMPOTENCY_KEY,
                "X-Correlation-ID": correlation_id,
                "traceparent": traceparent,
            }
        ),
    )

    assert response.status_code == 200
    request = DocumentEvidenceAssessmentRequest.model_validate(body)
    replay = asyncio.run(
        store.replay(
            tenant_id=TENANT_ID,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=EvidenceAssessmentService._request_fingerprint(request),
        )
    )
    assert replay is not None
    assert str(replay.event.correlationid) == correlation_id
    assert replay.event.traceparent == traceparent
    assert replay.event.idempotencykey == IDEMPOTENCY_KEY


def test_evidence_route_idempotently_replays_same_result() -> None:
    client = TestClient(create_app(_runtime()))
    headers = _headers(**{"Idempotency-Key": IDEMPOTENCY_KEY})

    first = client.post(
        "/documentary-evidence/assessments",
        json=_evidence_body(),
        headers=headers,
    )
    second = client.post(
        "/documentary-evidence/assessments",
        json=_evidence_body(),
        headers=headers,
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["assessment_reference"] == first.json()["assessment_reference"]


def test_authentication_authority_unavailable_is_retryable_503() -> None:
    client = TestClient(create_app(_runtime(auth_unavailable=True)))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 503
    assert response.json()["code"] == "AUTHENTICATION_UNAVAILABLE"
    assert response.json()["retryable"] is True


def test_control_plane_unavailable_is_retryable_503() -> None:
    client = TestClient(create_app(_runtime(context_mode="unavailable")))

    response = client.post(
        "/documentary-requirements/resolve",
        json=_requirement_body(),
        headers=_headers(),
    )

    assert response.status_code == 503
    assert response.json()["retryable"] is True

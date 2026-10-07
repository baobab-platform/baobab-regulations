"""R-CAP-02 documentary evidence assessment behavior."""

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.evidence_assessment import (
    EvidenceAssessmentIdentity,
)
from baobab_regulations.application.services.evidence_assessment import (
    EvidenceAssessmentAccessDeniedError,
    EvidenceAssessmentConflictError,
    EvidenceAssessmentInvalidIdempotencyKeyError,
    EvidenceAssessmentService,
)
from baobab_regulations.contracts.rtd06 import (
    ContentArtifactReference,
    CrossEngineObjectReference,
    DocumentaryAssertion,
    DocumentaryValiditySnapshot,
    DocumentaryVerificationSnapshot,
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    DocumentEvidenceFactBundle,
    DocumentVersionReference,
    IssuerClaim,
    RegulatoryDecisionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryEvidenceAssessmentReference,
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
IDEMPOTENCY_KEY = "r-cap-02-assessment-0001"
EVALUATED_AT = datetime(2026, 10, 6, 8, 30, tzinfo=UTC)


class FakeContextAuthority:
    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        if context_id != CONTEXT_ID or caller.subject != "workload:trade-docs":
            raise ContextAccessDeniedError("context denied")
        return TrustedPlatformContext(context_id=context_id, tenant_id=TENANT_ID)


def _requirement_reference(
    *,
    tenant_id: str = TENANT_ID,
) -> RegulatoryRequirementReference:
    return RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_01k7rtd6phyto01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _decision_reference(
    *,
    object_id: str = "regdec_01k7rtd6decision01",
    tenant_id: str = TENANT_ID,
) -> RegulatoryDecisionReference:
    return RegulatoryDecisionReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_DECISION",
        object_id=object_id,
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _requirement(
    *,
    decision_reference: RegulatoryDecisionReference | None = None,
) -> RegulatoryDocumentRequirementProjection:
    return RegulatoryDocumentRequirementProjection(
        requirement_reference=_requirement_reference(),
        regulatory_decision_reference=decision_reference or _decision_reference(),
        requirement_kind="DOCUMENT",
        requirement_code="PHYTOSANITARY_CERTIFICATE_REQUIRED",
        purpose_code="SPS",
        acceptable_document_types=["PHYTOSANITARY_CERTIFICATE"],
        required_issuer_roles=["COMPETENT_AUTHORITY"],
        required_data_elements=[
            "CONSIGNMENT_REFERENCE",
            "ORIGIN_COUNTRY",
            "COMMODITY_DESCRIPTION",
        ],
        unsatisfied_effect_code="SPS_HOLD_REQUIRED",
        effective_from=datetime(2026, 10, 5, tzinfo=UTC),
        effective_to=None,
        determined_at=datetime(2026, 10, 5, 20, 30, tzinfo=UTC),
    )


def _document_reference(
    *,
    tenant_id: str = TENANT_ID,
) -> DocumentVersionReference:
    return DocumentVersionReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_01k7rtd4001v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _content_reference(
    *,
    tenant_id: str = TENANT_ID,
) -> ContentArtifactReference:
    return ContentArtifactReference(
        owner_engine_id="baobab-trade-docs",
        object_type="CONTENT_ARTIFACT",
        object_id="tdoca_01k7rtd4001pdf",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _assertions(
    *,
    include_commodity: bool = True,
) -> list[DocumentaryAssertion]:
    values = [
        ("CONSIGNMENT_REFERENCE", "SHIP-UG-ZA-2026-0001", "ISSUER_ASSERTED"),
        ("ORIGIN_COUNTRY", "UG", "ISSUER_ASSERTED"),
    ]
    if include_commodity:
        values.append(("COMMODITY_DESCRIPTION", "Green coffee beans", "BAOBAB_EXTRACTED"))
    return [
        DocumentaryAssertion(
            element_code=code,
            origin=origin,
            value=value,
            unit=None,
            currency=None,
            source_artifact_reference=_content_reference(),
            field_verification_state="VERIFIED",
            observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
        )
        for code, value, origin in values
    ]


def _evidence(
    *,
    tenant_id: str = TENANT_ID,
    document_type: str = "PHYTOSANITARY_CERTIFICATE",
    issuer_role: str = "COMPETENT_AUTHORITY",
    verification_state: str = "VERIFIED",
    validity_state: str = "CURRENTLY_VALID",
    include_commodity: bool = True,
) -> DocumentEvidenceFactBundle:
    return DocumentEvidenceFactBundle.model_validate(
        {
            "document_version_reference": _document_reference(
                tenant_id=tenant_id
            ).model_dump(mode="json"),
            "document_type": document_type,
            "document_family": "REGULATORY",
            "issuer_claim": IssuerClaim(
                party_reference="org_ug_nppo",
                issuer_role=issuer_role,
                source_identity="Uganda NPPO",
                authority_context="UG",
            ).model_dump(mode="json"),
            "issued_at": "2026-10-05T18:04:00Z",
            "effective_from": "2026-10-05T18:04:00Z",
            "effective_to": "2026-11-05T23:59:59Z",
            "verification": DocumentaryVerificationSnapshot(
                verification_state=verification_state,
                reason_code="ISSUER_AND_SIGNATURE_VERIFIED",
                observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
            ).model_dump(mode="json"),
            "temporal_validity": DocumentaryValiditySnapshot(
                temporal_validity_state=validity_state,
                observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
            ).model_dump(mode="json"),
            "subject_references": [
                CrossEngineObjectReference(
                    owner_engine_id="baobab-trade",
                    object_type="SHIPMENT",
                    object_id="ship_01k4zsh001",
                    reference_mode="CURRENT",
                    scope="tenant",
                    tenant_id=tenant_id,
                ).model_dump(mode="json")
            ],
            "content_artifact_references": [
                _content_reference(tenant_id=tenant_id).model_dump(mode="json")
            ],
            "facts_observed_at": "2026-10-05T20:31:00Z",
            "documentary_assertions": [
                assertion.model_dump(mode="json")
                for assertion in _assertions(include_commodity=include_commodity)
            ],
        }
    )


def _request(
    *,
    evidence: DocumentEvidenceFactBundle | None = None,
    decision_reference: RegulatoryDecisionReference | None = None,
    assessment_reason: str = "INITIAL_EVIDENCE",
) -> DocumentEvidenceAssessmentRequest:
    return DocumentEvidenceAssessmentRequest.model_validate(
        {
            "context_id": str(CONTEXT_ID),
            "regulatory_decision_reference": (
                decision_reference or _decision_reference()
            ).model_dump(mode="json"),
            "requirement_reference": _requirement_reference().model_dump(mode="json"),
            "assessment_reason": assessment_reason,
            "evidence": [(evidence or _evidence()).model_dump(mode="json")],
        }
    )


def _service(
    *,
    requirement: RegulatoryDocumentRequirementProjection | None = None,
) -> EvidenceAssessmentService:
    return EvidenceAssessmentService(
        contexts=FakeContextAuthority(),
        requirements=InMemoryRequirementRepository([requirement or _requirement()]),
        assessor=ProjectionDocumentaryEvidenceAssessor(clock=lambda: EVALUATED_AT),
        idempotency=InMemoryEvidenceAssessmentIdempotency(),
    )


@pytest.mark.asyncio
async def test_satisfied_exact_documentary_evidence() -> None:
    result = await _service().assess(
        request=_request(),
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert result.outcome == "SATISFIED"
    assert result.accepted_document_version_references == [_document_reference()]
    assert result.rejected_evidence == []
    assert result.resulting_regulatory_decision_reference is None
    assert result.evaluated_at == EVALUATED_AT


@pytest.mark.asyncio
async def test_verified_document_can_still_be_unsatisfied() -> None:
    request = _request(evidence=_evidence(include_commodity=False))

    result = await _service().assess(
        request=request,
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert result.outcome == "UNSATISFIED"
    assert result.accepted_document_version_references == []
    assert "REQUIRED_DATA_ELEMENT_MISSING" in result.reason_codes


@pytest.mark.asyncio
async def test_pending_verification_is_indeterminate() -> None:
    result = await _service().assess(
        request=_request(evidence=_evidence(verification_state="PENDING")),
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert result.outcome == "INDETERMINATE"
    assert "DOCUMENT_VERIFICATION_INDETERMINATE" in result.reason_codes


@pytest.mark.asyncio
async def test_disputed_verification_requires_review() -> None:
    result = await _service().assess(
        request=_request(evidence=_evidence(verification_state="DISPUTED")),
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert result.outcome == "REVIEW_REQUIRED"
    assert "DOCUMENT_VERIFICATION_DISPUTED" in result.reason_codes


@pytest.mark.asyncio
async def test_expired_document_is_unsatisfied() -> None:
    result = await _service().assess(
        request=_request(evidence=_evidence(validity_state="EXPIRED")),
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert result.outcome == "UNSATISFIED"
    assert "DOCUMENT_EXPIRED" in result.reason_codes


@pytest.mark.asyncio
async def test_wrong_tenant_document_reference_is_denied() -> None:
    request = _request(evidence=_evidence(tenant_id=OTHER_TENANT_ID))

    with pytest.raises(EvidenceAssessmentAccessDeniedError):
        await _service().assess(
            request=request,
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
            idempotency_key=IDEMPOTENCY_KEY,
        )


@pytest.mark.asyncio
async def test_requirement_decision_mismatch_is_conflict() -> None:
    request = _request()
    mismatched_requirement = _requirement(
        decision_reference=_decision_reference(object_id="regdec_other_decision")
    )

    with pytest.raises(EvidenceAssessmentConflictError):
        await _service(requirement=mismatched_requirement).assess(
            request=request,
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
            idempotency_key=IDEMPOTENCY_KEY,
        )


@pytest.mark.asyncio
async def test_same_idempotency_key_replays_same_assessment() -> None:
    service = _service()
    request = _request()

    first = await service.assess(
        request=request,
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )
    second = await service.assess(
        request=request,
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    assert second == first
    assert second.assessment_reference == first.assessment_reference


@pytest.mark.asyncio
async def test_same_idempotency_key_with_changed_request_conflicts() -> None:
    service = _service()
    first_request = _request()
    second_request = _request(assessment_reason="EVIDENCE_CHANGED")

    await service.assess(
        request=first_request,
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
        idempotency_key=IDEMPOTENCY_KEY,
    )

    with pytest.raises(EvidenceAssessmentConflictError):
        await service.assess(
            request=second_request,
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
            idempotency_key=IDEMPOTENCY_KEY,
        )


@pytest.mark.asyncio
async def test_invalid_idempotency_key_is_rejected() -> None:
    with pytest.raises(EvidenceAssessmentInvalidIdempotencyKeyError):
        await _service().assess(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
            idempotency_key="short",
        )


def test_current_document_version_reference_is_rejected() -> None:
    payload = _document_reference().model_dump(mode="json")
    payload["reference_mode"] = "CURRENT"

    with pytest.raises(ValidationError):
        DocumentVersionReference.model_validate(payload)


def test_caller_cannot_supply_legal_or_knowledge_time() -> None:
    payload = _request().model_dump(mode="json")
    payload["legal_time"] = "2026-10-05T12:00:00Z"
    payload["knowledge_time"] = "2026-10-05T20:30:00Z"

    with pytest.raises(ValidationError):
        DocumentEvidenceAssessmentRequest.model_validate(payload)


@pytest.mark.asyncio
async def test_result_cannot_reference_unsupplied_document_version() -> None:
    class BrokenAssessor:
        async def assess(
            self,
            *,
            request: DocumentEvidenceAssessmentRequest,
            requirement: RegulatoryDocumentRequirementProjection,
            identity: EvidenceAssessmentIdentity,
        ) -> DocumentEvidenceAssessmentResult:
            del requirement
            foreign = DocumentVersionReference(
                owner_engine_id="baobab-trade-docs",
                object_type="DOCUMENT_VERSION",
                object_id="tdocv_not_supplied",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=TENANT_ID,
            )
            return DocumentEvidenceAssessmentResult(
                assessment_reference=RegulatoryEvidenceAssessmentReference(
                    owner_engine_id="baobab-regulations",
                    object_type="REGULATORY_EVIDENCE_ASSESSMENT",
                    object_id=identity.assessment_id,
                    reference_mode="IDENTITY_PINNED",
                    scope="tenant",
                    tenant_id=TENANT_ID,
                ),
                regulatory_decision_reference=request.regulatory_decision_reference,
                requirement_reference=request.requirement_reference,
                outcome="SATISFIED",
                accepted_document_version_references=[foreign],
                rejected_evidence=[],
                reason_codes=["DOCUMENT_TYPE_ACCEPTED"],
                resulting_regulatory_decision_reference=None,
                evaluated_at=EVALUATED_AT,
            )

    from baobab_regulations.application.services.evidence_assessment import (
        EvidenceAssessmentIntegrityError,
    )

    service = EvidenceAssessmentService(
        contexts=FakeContextAuthority(),
        requirements=InMemoryRequirementRepository([_requirement()]),
        assessor=BrokenAssessor(),
        idempotency=InMemoryEvidenceAssessmentIdempotency(),
    )

    with pytest.raises(EvidenceAssessmentIntegrityError):
        await service.assess(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
            idempotency_key=IDEMPOTENCY_KEY,
        )

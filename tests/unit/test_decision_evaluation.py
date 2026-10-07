"""R-CAP-09 canonical decision orchestration and differential tests."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID

import httpx
import pytest

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.evaluator import (
    EvaluatorNotReadyError,
    RegulatoryEvaluationInput,
    RegulatoryEvaluationResult,
    ResolvedRuleSet,
)
from baobab_regulations.application.services.decision_evaluation import (
    DecisionEvaluationAccessDeniedError,
    DecisionEvaluationIntegrityError,
    DecisionEvaluationInvalidRequestError,
    DecisionEvaluationService,
    DecisionEvaluatorNotReadyError,
)
from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
)
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState
from baobab_regulations.infrastructure.evaluation.reference_canonical import (
    ReferenceEvaluatorCanonicalAdapter,
)
from baobab_regulations.infrastructure.opa.client import OpaRegulatoryPolicyEvaluator
from baobab_regulations.infrastructure.persistence.decision_idempotency_memory import (
    InMemoryDecisionEvaluationIdempotency,
)
from baobab_regulations.infrastructure.persistence.memory import InMemoryRuleSetRepository
from baobab_regulations.infrastructure.rule_sets import RepositoryRuleSetAuthority

TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
OTHER_TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
NOW = datetime(2026, 10, 6, 10, tzinfo=UTC)
BRIR_FIXTURE = Path("tests/fixtures/brir/r_cap_09_rule_set.json")
BRIR = BrirRuleSet.model_validate(
    json.loads(BRIR_FIXTURE.read_text(encoding="utf-8"))
)
ARTIFACT = RegoV1Compiler().compile(BRIR)
RULE_FP = ARTIFACT.rule_set_fingerprint
COMMAND_ID = "r-cap-09-decision-0001"\nSECOND_COMMAND_ID = "r-cap-09-decision-0002"


class FakeContextAuthority:
    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        assert context_id == CONTEXT_ID
        assert caller.subject == "workload:test"
        return TrustedPlatformContext(context_id=context_id, tenant_id=TENANT_ID)


class RecordingEvaluator:
    def __init__(
        self,
        *,
        result: RegulatoryEvaluationResult | None = None,
        error: Exception | None = None,
    ) -> None:
        self.calls = 0
        self.result = result or _result()
        self.error = error

    async def evaluate(
        self,
        evaluation: RegulatoryEvaluationInput,
    ) -> RegulatoryEvaluationResult:
        self.calls += 1
        assert evaluation.tenant_id == TENANT_ID
        assert evaluation.rule_set.fingerprint == RULE_FP
        if self.error is not None:
            raise self.error
        return self.result


def _evidence(*, tenant_id: str = TENANT_ID) -> PinnedCrossEngineReference:
    return PinnedCrossEngineReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_r_cap_09_phyto_v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _request(
    *,
    tenant_id: str = TENANT_ID,
    replay_key: str = "replay-r-cap-09-0001",
    profile: str = "STANDARD",
    purpose: str = "TRANSACTION_DECISION",
    ceiling: str = "E2",
) -> DecisionEvaluateRequest:
    return DecisionEvaluateRequest.model_validate(
        {
            "context_id": str(CONTEXT_ID),
            "question": "MAY_TRANSACTION_PROCEED",
            "assessment_purpose": purpose,
            "decision_stage": "PRE_SHIPMENT",
            "subject_references": [
                {
                    "owner_engine_id": "baobab-trade",
                    "object_type": "SHIPMENT",
                    "object_id": "ship_r_cap_09_0001",
                    "reference_mode": "IDENTITY_PINNED",
                    "scope": "tenant",
                    "tenant_id": tenant_id,
                }
            ],
            "regulated_activities": [
                "CROSS_BORDER_EXPORT",
                "CROSS_BORDER_IMPORT",
            ],
            "facts": [
                {
                    "fact_code": "ORIGIN_COUNTRY",
                    "value": "UG",
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": None,
                },
                {
                    "fact_code": "IMPORT_COUNTRY",
                    "value": "ZA",
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": None,
                },
                {
                    "fact_code": "ORIGIN_REGIME",
                    "value": "AfCFTA",
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": None,
                },
                {
                    "fact_code": "HS_CODE",
                    "value": "0901.11.10",
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": None,
                },
                {
                    "fact_code": "PHYTOSANITARY_CERTIFICATE_PRESENT",
                    "value": True,
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": _evidence(tenant_id=tenant_id).model_dump(
                        mode="json"
                    ),
                },
                {
                    "fact_code": "ORIGIN_CERTIFICATE_PRESENT",
                    "value": True,
                    "unit": None,
                    "currency": None,
                    "observed_at": NOW.isoformat(),
                    "source_reference": None,
                },
            ],
            "evidence_references": [
                _evidence(tenant_id=tenant_id).model_dump(mode="json")
            ],
            "rule_set_reference": {
                "owner_engine_id": "baobab-regulations",
                "object_type": "REGULATORY_RULE_SET",
                "object_id": "ruleset_ug_za_coffee_2026_10",
                "reference_mode": "IDENTITY_PINNED",
                "scope": "platform",
            },
            "legal_time": NOW.isoformat(),
            "knowledge_time": NOW.isoformat(),
            "evaluation_profile": profile,
            "requested_assurance": "STANDARD",
            "requested_enforcement_class_ceiling": ceiling,
            "replay_key": replay_key,
        }
    )


def _result(
    *,
    enforcement_class: str = "E1",
) -> RegulatoryEvaluationResult:
    legal_basis = PinnedCrossEngineReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_PROVISION_VERSION",
        object_id="regprov_r_cap_09_sps",
        reference_mode="IDENTITY_PINNED",
        scope="platform",
    )
    evidence = _evidence()
    reason = DecisionReason(
        code="REFERENCE_PROFILE_SATISFIED",
        message="All checked requirements are satisfied.",
        legal_basis_references=[legal_basis],
        rule_version_references=[],
        evidence_references=[evidence],
    )
    return RegulatoryEvaluationResult(
        outcome="SATISFIED",
        enforcement_class=enforcement_class,
        reasons=(reason,),
        legal_basis_references=(legal_basis,),
        evidence_references=(evidence,),
        recommended_disposition=RecommendedDisposition(
            disposition_code="ALLOW",
            rationale="No blocking regulatory condition was found.",
            missing_requirement_references=[],
        ),
    )


async def _service(
    evaluator: RecordingEvaluator,
) -> DecisionEvaluationService:
    repository = InMemoryRuleSetRepository()
    await repository.save(
        RuleSetRecord(
            rule_set_id="ruleset_ug_za_coffee_2026_10",
            corridor_profile="UG-ZA-COFFEE",
            assurance_state=AssuranceState.VERIFIED,
            fingerprint=RULE_FP,
            legal_valid_from=NOW - timedelta(days=30),
            legal_valid_to=NOW + timedelta(days=30),
            knowledge_from=NOW - timedelta(days=10),
            knowledge_to=None,
            brir_payload=BRIR.model_dump(mode="json"),
            compiler_id=ARTIFACT.compiler_id,
            compiler_version=ARTIFACT.compiler_version,
            compiled_target=ARTIFACT.target,
            compiled_entrypoint=ARTIFACT.entrypoint,
            compiled_artifact_fingerprint=ARTIFACT.artifact_fingerprint,
        )
    )
    return DecisionEvaluationService(
        contexts=FakeContextAuthority(),
        rule_sets=RepositoryRuleSetAuthority(repository),
        evaluator=evaluator,
        idempotency=InMemoryDecisionEvaluationIdempotency(),
        clock=lambda: NOW + timedelta(seconds=1),
    )


@pytest.mark.asyncio
async def test_service_assembles_exact_canonical_decision() -> None:
    evaluator = RecordingEvaluator()
    service = await _service(evaluator)

    response = await service.evaluate(
        request=_request(),
        caller=AuthenticatedCaller(subject="workload:test", access_token="token-value"),
        idempotency_key=COMMAND_ID,
    )

    assert response.outcome == "SATISFIED"
    assert response.enforcement_class == "E1"
    assert response.rule_set_fingerprint == RULE_FP
    assert response.legal_time == NOW
    assert response.knowledge_time == NOW
    assert response.replay_identity.replay_key == "replay-r-cap-09-0001"
    assert response.decision_reference.tenant_id == TENANT_ID
    assert evaluator.calls == 1


@pytest.mark.asyncio
async def test_same_command_replays_without_second_evaluator_call() -> None:
    evaluator = RecordingEvaluator()
    service = await _service(evaluator)
    request = _request()
    caller = AuthenticatedCaller(subject="workload:test", access_token="token-value")

    first = await service.evaluate(
        request=request,
        caller=caller,
        idempotency_key=COMMAND_ID,
    )
    second = await service.evaluate(
        request=request,
        caller=caller,
        idempotency_key=COMMAND_ID,
    )

    assert second == first
    assert evaluator.calls == 1


@pytest.mark.asyncio
async def test_same_replay_identity_with_new_command_key_avoids_live_reevaluation() -> None:
    evaluator = RecordingEvaluator()
    service = await _service(evaluator)
    request = _request()
    caller = AuthenticatedCaller(subject="workload:test", access_token="token-value")

    first = await service.evaluate(
        request=request,
        caller=caller,
        idempotency_key=COMMAND_ID,
    )
    second = await service.evaluate(
        request=request,
        caller=caller,
        idempotency_key=SECOND_COMMAND_ID,
    )

    assert second == first
    assert evaluator.calls == 1


@pytest.mark.asyncio
async def test_nested_tenant_mismatch_fails_before_evaluator() -> None:
    evaluator = RecordingEvaluator()
    service = await _service(evaluator)

    with pytest.raises(DecisionEvaluationAccessDeniedError):
        await service.evaluate(
            request=_request(tenant_id=OTHER_TENANT_ID),
            caller=AuthenticatedCaller(
                subject="workload:test",
                access_token="token-value",
            ),
            idempotency_key=COMMAND_ID,
        )

    assert evaluator.calls == 0


@pytest.mark.asyncio
async def test_evaluator_cannot_exceed_enforcement_ceiling() -> None:
    evaluator = RecordingEvaluator(result=_result(enforcement_class="E3"))
    service = await _service(evaluator)

    with pytest.raises(DecisionEvaluationIntegrityError, match="ceiling"):
        await service.evaluate(
            request=_request(ceiling="E2"),
            caller=AuthenticatedCaller(
                subject="workload:test",
                access_token="token-value",
            ),
            idempotency_key=COMMAND_ID,
        )


@pytest.mark.asyncio
async def test_historical_profile_and_purpose_must_match() -> None:
    evaluator = RecordingEvaluator()
    service = await _service(evaluator)

    with pytest.raises(DecisionEvaluationInvalidRequestError):
        await service.evaluate(
            request=_request(profile="HISTORICAL_REPLAY"),
            caller=AuthenticatedCaller(
                subject="workload:test",
                access_token="token-value",
            ),
            idempotency_key=COMMAND_ID,
        )


@pytest.mark.asyncio
async def test_evaluator_not_ready_remains_technical_failure() -> None:
    evaluator = RecordingEvaluator(error=EvaluatorNotReadyError("bundle missing"))
    service = await _service(evaluator)

    with pytest.raises(DecisionEvaluatorNotReadyError):
        await service.evaluate(
            request=_request(),
            caller=AuthenticatedCaller(
                subject="workload:test",
                access_token="token-value",
            ),
            idempotency_key=COMMAND_ID,
        )


@pytest.mark.asyncio
async def test_opa_and_reference_evaluator_match_supported_golden_semantics() -> None:
    request = _request()
    evaluation = RegulatoryEvaluationInput(
        request=request,
        tenant_id=TENANT_ID,
        rule_set=ResolvedRuleSet(
            reference=request.rule_set_reference,
            fingerprint=RULE_FP,
            assurance_state="VERIFIED",
            compiler_id=ARTIFACT.compiler_id,
            compiler_version=ARTIFACT.compiler_version,
            target=ARTIFACT.target,
            entrypoint=ARTIFACT.entrypoint,
            artifact_fingerprint=ARTIFACT.artifact_fingerprint,
        ),
        input_fingerprint="b" * 64,
    )
    reference = ReferenceEvaluatorCanonicalAdapter()
    reference_result = await reference.evaluate(evaluation)

    async def handler(http_request: httpx.Request) -> httpx.Response:
        if http_request.url.path == "/health":
            return httpx.Response(200, json={})
        if http_request.url.path == "/v1/data/baobab/regulations/decision":
            return httpx.Response(
                200,
                json={
                    "result": {
                        "input_fingerprint": evaluation.input_fingerprint,
                        "rule_set_fingerprint": RULE_FP,
                        "outcome": reference_result.outcome,
                        "enforcement_class": reference_result.enforcement_class,
                        "reasons": [
                            item.model_dump(mode="json")
                            for item in reference_result.reasons
                        ],
                        "legal_basis_references": [
                            item.model_dump(mode="json")
                            for item in reference_result.legal_basis_references
                        ],
                        "evidence_references": [
                            item.model_dump(mode="json")
                            for item in reference_result.evidence_references
                        ],
                        "recommended_disposition": (
                            reference_result.recommended_disposition.model_dump(
                                mode="json"
                            )
                            if reference_result.recommended_disposition
                            else None
                        ),
                    }
                },
            )
        return httpx.Response(404)

    async with httpx.AsyncClient(
        base_url="http://opa.test",
        transport=httpx.MockTransport(handler),
    ) as client:
        opa = OpaRegulatoryPolicyEvaluator(client=client)
        opa_result = await opa.evaluate(evaluation)

    assert opa_result.outcome == reference_result.outcome
    assert opa_result.enforcement_class == reference_result.enforcement_class
    assert [item.code for item in opa_result.reasons] == [
        item.code for item in reference_result.reasons
    ]
    assert opa_result.recommended_disposition == reference_result.recommended_disposition

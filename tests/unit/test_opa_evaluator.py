"""R-CAP-09 OPA adapter protocol and readiness tests."""

from datetime import UTC, datetime
from uuid import UUID

import httpx
import pytest

from baobab_regulations.application.ports.evaluator import (
    EvaluatorNotReadyError,
    EvaluatorProtocolError,
    EvaluatorRuntimeError,
    EvaluatorUndefinedError,
    RegulatoryEvaluationInput,
    ResolvedRuleSet,
)
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    PinnedCrossEngineReference,
    RegulatoryFact,
    RuleSetReference,
)
from baobab_regulations.infrastructure.opa.client import OpaRegulatoryPolicyEvaluator

TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
RULE_FP = "a" * 64
INPUT_FP = "b" * 64
ARTIFACT_FP = "c" * 64


def _request() -> DecisionEvaluateRequest:
    evidence = PinnedCrossEngineReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_r_cap_09_phyto_v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_ID,
    )
    return DecisionEvaluateRequest(
        context_id=UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10"),
        question="MAY_TRANSACTION_PROCEED",
        assessment_purpose="TRANSACTION_DECISION",
        decision_stage="PRE_SHIPMENT",
        subject_references=[
            PinnedCrossEngineReference(
                owner_engine_id="baobab-trade",
                object_type="SHIPMENT",
                object_id="ship_r_cap_09_0001",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=TENANT_ID,
            )
        ],
        regulated_activities=["CROSS_BORDER_EXPORT", "CROSS_BORDER_IMPORT"],
        facts=[
            RegulatoryFact(
                fact_code="HS_CODE",
                value="0901.11.10",
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            )
        ],
        evidence_references=[evidence],
        rule_set_reference=RuleSetReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_RULE_SET",
            object_id="ruleset_ug_za_coffee_2026_10",
            reference_mode="IDENTITY_PINNED",
            scope="platform",
        ),
        legal_time=datetime(2026, 10, 6, 10, tzinfo=UTC),
        knowledge_time=datetime(2026, 10, 6, 10, tzinfo=UTC),
        evaluation_profile="STANDARD",
        requested_assurance="STANDARD",
        requested_enforcement_class_ceiling="E2",
        replay_key="replay-r-cap-09-0001",
    )


def _evaluation(
    *,
    entrypoint: str = "baobab/regulations/decision",
    target: str = "rego/v1",
) -> RegulatoryEvaluationInput:
    request = _request()
    return RegulatoryEvaluationInput(
        request=request,
        tenant_id=TENANT_ID,
        rule_set=ResolvedRuleSet(
            reference=request.rule_set_reference,
            fingerprint=RULE_FP,
            assurance_state="VERIFIED",
            compiler_id="baobab-regulations-rego",
            compiler_version="1",
            target=target,
            entrypoint=entrypoint,
            artifact_fingerprint=ARTIFACT_FP,
        ),
        input_fingerprint=INPUT_FP,
    )


def _result() -> dict[str, object]:
    evidence = _request().evidence_references[0].model_dump(mode="json")
    legal_basis = {
        "owner_engine_id": "baobab-regulations",
        "object_type": "REGULATORY_PROVISION_VERSION",
        "object_id": "regprov_r_cap_09_sps",
        "reference_mode": "IDENTITY_PINNED",
        "scope": "platform",
    }
    return {
        "input_fingerprint": INPUT_FP,
        "rule_set_fingerprint": RULE_FP,
        "outcome": "SATISFIED",
        "enforcement_class": "E1",
        "reasons": [
            {
                "code": "REFERENCE_PROFILE_SATISFIED",
                "message": "All checked requirements are satisfied.",
                "legal_basis_references": [legal_basis],
                "rule_version_references": [],
                "evidence_references": [evidence],
            }
        ],
        "legal_basis_references": [legal_basis],
        "evidence_references": [evidence],
        "recommended_disposition": {
            "disposition_code": "ALLOW",
            "rationale": "No blocking regulatory condition was found.",
            "missing_requirement_references": [],
        },
    }


def _client(
    *,
    health_status: int = 200,
    evaluation_status: int = 200,
    evaluation_document: object | None = None,
) -> httpx.AsyncClient:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/health":
            assert request.url.params.get("bundles") == "true"
            return httpx.Response(health_status, json={})
        if request.url.path == "/v1/data/baobab/regulations/decision":
            assert request.method == "POST"
            return httpx.Response(
                evaluation_status,
                json=(
                    evaluation_document
                    if evaluation_document is not None
                    else {"result": _result()}
                ),
            )
        return httpx.Response(404, json={})

    return httpx.AsyncClient(
        base_url="http://opa.test",
        transport=httpx.MockTransport(handler),
    )


@pytest.mark.asyncio
async def test_opa_adapter_returns_governed_decision_fragment() -> None:
    async with _client() as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        result = await evaluator.evaluate(_evaluation())

    assert result.outcome == "SATISFIED"
    assert result.enforcement_class == "E1"
    assert result.recommended_disposition is not None
    assert result.recommended_disposition.disposition_code == "ALLOW"


@pytest.mark.asyncio
async def test_opa_bundle_readiness_failure_is_not_ready() -> None:
    async with _client(health_status=500) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorNotReadyError):
            await evaluator.evaluate(_evaluation())


@pytest.mark.asyncio
async def test_missing_governed_entrypoint_is_not_ready() -> None:
    async with _client() as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorNotReadyError, match="entrypoint"):
            await evaluator.evaluate(_evaluation(entrypoint=""))


@pytest.mark.asyncio
async def test_non_rego_target_is_not_ready() -> None:
    async with _client() as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorNotReadyError, match="Rego v1"):
            await evaluator.evaluate(_evaluation(target="cel/v1"))


@pytest.mark.asyncio
async def test_opa_200_without_result_is_undefined() -> None:
    async with _client(evaluation_document={}) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorUndefinedError):
            await evaluator.evaluate(_evaluation())


@pytest.mark.asyncio
async def test_opa_wrong_rule_set_fingerprint_is_protocol_failure() -> None:
    result = _result()
    result["rule_set_fingerprint"] = "d" * 64
    async with _client(evaluation_document={"result": result}) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorProtocolError, match="rule-set fingerprint"):
            await evaluator.evaluate(_evaluation())


@pytest.mark.asyncio
async def test_opa_wrong_input_fingerprint_is_protocol_failure() -> None:
    result = _result()
    result["input_fingerprint"] = "d" * 64
    async with _client(evaluation_document={"result": result}) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorProtocolError, match="input fingerprint"):
            await evaluator.evaluate(_evaluation())


@pytest.mark.asyncio
async def test_opa_invalid_result_shape_is_protocol_failure() -> None:
    async with _client(
        evaluation_document={"result": {"outcome": "SATISFIED"}}
    ) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorProtocolError):
            await evaluator.evaluate(_evaluation())


@pytest.mark.asyncio
async def test_opa_server_error_is_runtime_failure() -> None:
    async with _client(evaluation_status=500) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        with pytest.raises(EvaluatorRuntimeError):
            await evaluator.evaluate(_evaluation())

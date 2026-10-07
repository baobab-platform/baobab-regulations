"""Live OPA Data API conformance proof for R-CAP-09."""

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import httpx
import pytest

from baobab_regulations.application.ports.evaluator import (
    RegulatoryEvaluationInput,
    ResolvedRuleSet,
)
from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    PinnedCrossEngineReference,
    RegulatoryFact,
    RuleSetReference,
)
from baobab_regulations.infrastructure.opa.client import OpaRegulatoryPolicyEvaluator

TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
BRIR_FIXTURE = Path("tests/fixtures/brir/r_cap_09_rule_set.json")
BRIR = BrirRuleSet.model_validate(
    json.loads(BRIR_FIXTURE.read_text(encoding="utf-8"))
)
ARTIFACT = RegoV1Compiler().compile(BRIR)
RULE_FP = ARTIFACT.rule_set_fingerprint
INPUT_FP = "b" * 64


@pytest.mark.live_opa
@pytest.mark.asyncio
async def test_live_opa_executes_governed_decision_envelope() -> None:
    opa_url = os.getenv("R_CAP_09_OPA_URL")
    if not opa_url:
        pytest.skip("R_CAP_09_OPA_URL is not configured")

    rule_set = RuleSetReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_RULE_SET",
        object_id="ruleset_ug_za_coffee_2026_10",
        reference_mode="IDENTITY_PINNED",
        scope="platform",
    )
    request = DecisionEvaluateRequest(
        context_id=UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10"),
        question="MAY_TRANSACTION_PROCEED",
        assessment_purpose="TRANSACTION_DECISION",
        decision_stage="PRE_SHIPMENT",
        subject_references=[
            PinnedCrossEngineReference(
                owner_engine_id="baobab-trade",
                object_type="SHIPMENT",
                object_id="ship_r_cap_09_live",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=TENANT_ID,
            )
        ],
        regulated_activities=["CROSS_BORDER_EXPORT", "CROSS_BORDER_IMPORT"],
        facts=[
            RegulatoryFact(
                fact_code="ORIGIN_COUNTRY",
                value="UG",
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
            RegulatoryFact(
                fact_code="IMPORT_COUNTRY",
                value="ZA",
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
            RegulatoryFact(
                fact_code="ORIGIN_REGIME",
                value="AfCFTA",
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
            RegulatoryFact(
                fact_code="HS_CODE",
                value="0901.11.10",
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
            RegulatoryFact(
                fact_code="PHYTOSANITARY_CERTIFICATE_PRESENT",
                value=True,
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
            RegulatoryFact(
                fact_code="ORIGIN_CERTIFICATE_PRESENT",
                value=True,
                observed_at=datetime(2026, 10, 6, 10, tzinfo=UTC),
            ),
        ],
        evidence_references=[
            PinnedCrossEngineReference(
                owner_engine_id="baobab-trade-docs",
                object_type="DOCUMENT_VERSION",
                object_id="tdocv_r_cap_09_live",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=TENANT_ID,
            )
        ],
        rule_set_reference=rule_set,
        legal_time=datetime(2026, 10, 6, 10, tzinfo=UTC),
        knowledge_time=datetime(2026, 10, 6, 10, tzinfo=UTC),
        evaluation_profile="STANDARD",
        requested_assurance="STANDARD",
        requested_enforcement_class_ceiling="E2",
        replay_key="replay-r-cap-09-live-0001",
    )
    evaluation = RegulatoryEvaluationInput(
        request=request,
        tenant_id=TENANT_ID,
        rule_set=ResolvedRuleSet(
            reference=rule_set,
            fingerprint=RULE_FP,
            assurance_state="VERIFIED",
            compiler_id=ARTIFACT.compiler_id,
            compiler_version=ARTIFACT.compiler_version,
            target=ARTIFACT.target,
            entrypoint=ARTIFACT.entrypoint,
            artifact_fingerprint=ARTIFACT.artifact_fingerprint,
        ),
        input_fingerprint=INPUT_FP,
    )

    async with httpx.AsyncClient(base_url=opa_url, timeout=5.0) as client:
        evaluator = OpaRegulatoryPolicyEvaluator(client=client)
        result = await evaluator.evaluate(evaluation)

    assert result.outcome == "SATISFIED"
    assert result.enforcement_class == "E1"
    assert result.recommended_disposition is not None
    assert result.recommended_disposition.disposition_code == "ALLOW"
    assert [reason.code for reason in result.reasons] == [
        "REFERENCE_PROFILE_SATISFIED"
    ]

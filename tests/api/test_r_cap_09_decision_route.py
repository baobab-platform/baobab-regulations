"""R-CAP-09 authenticated/context-bound canonical decision route tests."""

import asyncio
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from uuid import UUID

from fastapi.testclient import TestClient

from baobab_regulations.api.app import create_app
from baobab_regulations.api.runtime import CapabilityApiRuntime
from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.evaluator import (
    EvaluatorUndefinedError,
    RegulatoryEvaluationInput,
    RegulatoryEvaluationResult,
)
from baobab_regulations.application.services.decision_evaluation import DecisionEvaluationService
from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet
from baobab_regulations.contracts.decision import (
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
)
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState
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
TOKEN = "valid-r-cap-09-workload-token"
IDEMPOTENCY_KEY = "r-cap-09-route-0001"


class FakeAuthenticator:
    async def authenticate(self, access_token: str) -> AuthenticatedCaller:
        assert access_token == TOKEN
        return AuthenticatedCaller(
            subject="workload:test",
            access_token=access_token,
            client_id="r-cap-09-test",
        )


class FakeContextAuthority:
    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        assert context_id == CONTEXT_ID
        assert caller.access_token == TOKEN
        return TrustedPlatformContext(context_id=context_id, tenant_id=TENANT_ID)


class StaticEvaluator:
    def __init__(self, *, undefined: bool = False) -> None:
        self.undefined = undefined

    async def evaluate(
        self,
        evaluation: RegulatoryEvaluationInput,
    ) -> RegulatoryEvaluationResult:
        if self.undefined:
            raise EvaluatorUndefinedError("policy query undefined")
        evidence = evaluation.request.evidence_references[0]
        legal_basis = PinnedCrossEngineReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_PROVISION_VERSION",
            object_id="regprov_r_cap_09_sps",
            reference_mode="IDENTITY_PINNED",
            scope="platform",
        )
        return RegulatoryEvaluationResult(
            outcome="SATISFIED",
            enforcement_class="E1",
            reasons=(
                DecisionReason(
                    code="REFERENCE_PROFILE_SATISFIED",
                    message="All checked requirements are satisfied.",
                    legal_basis_references=[legal_basis],
                    rule_version_references=[],
                    evidence_references=[evidence],
                ),
            ),
            legal_basis_references=(legal_basis,),
            evidence_references=(evidence,),
            recommended_disposition=RecommendedDisposition(
                disposition_code="ALLOW",
                rationale="No blocking regulatory condition was found.",
                missing_requirement_references=[],
            ),
        )


async def _decision_service(*, undefined: bool = False) -> DecisionEvaluationService:
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
        evaluator=StaticEvaluator(undefined=undefined),
        idempotency=InMemoryDecisionEvaluationIdempotency(),
        clock=lambda: NOW + timedelta(seconds=1),
    )


def _runtime(*, undefined: bool = False, configured: bool = True) -> CapabilityApiRuntime:
    return CapabilityApiRuntime(
        authenticator=FakeAuthenticator(),
        requirement_resolution=cast(Any, object()),
        evidence_assessment=cast(Any, object()),
        decision_evaluation=(
            asyncio.run(_decision_service(undefined=undefined))
            if configured
            else None
        ),
    )


def _body(*, tenant_id: str = TENANT_ID) -> dict[str, object]:
    return {
        "context_id": str(CONTEXT_ID),
        "question": "MAY_TRANSACTION_PROCEED",
        "assessment_purpose": "TRANSACTION_DECISION",
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
        "regulated_activities": ["CROSS_BORDER_EXPORT", "CROSS_BORDER_IMPORT"],
        "facts": [
            {
                "fact_code": "HS_CODE",
                "value": "0901.11.10",
                "unit": None,
                "currency": None,
                "observed_at": NOW.isoformat(),
                "source_reference": None,
            }
        ],
        "evidence_references": [
            {
                "owner_engine_id": "baobab-trade-docs",
                "object_type": "DOCUMENT_VERSION",
                "object_id": "tdocv_r_cap_09_phyto_v1",
                "reference_mode": "IDENTITY_PINNED",
                "scope": "tenant",
                "tenant_id": tenant_id,
            }
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
        "evaluation_profile": "STANDARD",
        "requested_assurance": "STANDARD",
        "requested_enforcement_class_ceiling": "E2",
        "replay_key": "replay-r-cap-09-route-0001",
    }


def _headers(**extra: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Idempotency-Key": IDEMPOTENCY_KEY,
        **extra,
    }


def test_decision_route_returns_canonical_decision() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/decisions/evaluate",
        json=_body(),
        headers=_headers(),
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "SATISFIED"
    assert response.json()["rule_set_fingerprint"] == RULE_FP
    assert response.json()["replay_identity"]["replay_key"] == (
        "replay-r-cap-09-route-0001"
    )


def test_decision_route_requires_idempotency_key() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/decisions/evaluate",
        json=_body(),
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    assert response.status_code == 400
    assert response.json()["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_decision_route_rejects_nested_tenant_mismatch() -> None:
    client = TestClient(create_app(_runtime()))

    response = client.post(
        "/decisions/evaluate",
        json=_body(tenant_id=OTHER_TENANT_ID),
        headers=_headers(),
    )

    assert response.status_code == 403
    assert response.json()["code"] == "REGULATIONS_DECISION_ACCESS_DENIED"


def test_undefined_policy_result_is_technical_503_not_indeterminate() -> None:
    client = TestClient(create_app(_runtime(undefined=True)))

    response = client.post(
        "/decisions/evaluate",
        json=_body(),
        headers=_headers(),
    )

    assert response.status_code == 503
    assert response.json()["code"] == "EVALUATOR_UNDEFINED"
    assert "outcome" not in response.json()


def test_unconfigured_decision_runtime_fails_closed() -> None:
    client = TestClient(create_app(_runtime(configured=False)))

    response = client.post(
        "/decisions/evaluate",
        json=_body(),
        headers=_headers(),
    )

    assert response.status_code == 503
    assert response.json()["code"] == "REGULATIONS_DECISION_RUNTIME_UNAVAILABLE"
    assert response.json()["retryable"] is True


def test_generated_openapi_exposes_exact_decision_operation_and_problem_media() -> None:
    schema = create_app(_runtime()).openapi()
    operation = schema["paths"]["/decisions/evaluate"]["post"]

    assert operation["operationId"] == "evaluateRegulatoryDecision"
    assert "422" not in operation["responses"]
    assert operation["security"] == [{"workloadOidc": []}]
    idempotency = next(
        item
        for item in operation["parameters"]
        if item["name"] == "Idempotency-Key"
    )
    assert idempotency["required"] is True
    assert "application/problem+json" in operation["responses"]["503"]["content"]

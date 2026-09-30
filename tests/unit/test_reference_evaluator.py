"""Golden-path tests for the offline reference evaluator (UG→ZA profile)."""

from datetime import UTC, datetime

import pytest

from baobab_regulations.domain.context.models import (
    JurisdictionRole,
    JurisdictionRoleKind,
    PlatformContextRef,
    RegulatoryContext,
)
from baobab_regulations.domain.shared.enums import DecisionOutcome
from baobab_regulations.domain.shared.ids import HSCode, JurisdictionCode, RegimeCode
from baobab_regulations.infrastructure.evaluation.reference import ReferenceEvaluator
from baobab_regulations.tenancy.context import TenantContextError


def _ctx(**overrides: object) -> RegulatoryContext:
    base = dict(
        platform=PlatformContextRef(tenant_id="tenant-zuribeans"),
        jurisdiction_roles=[
            JurisdictionRole(
                role=JurisdictionRoleKind.ORIGIN,
                jurisdiction=JurisdictionCode("UG"),
            ),
            JurisdictionRole(
                role=JurisdictionRoleKind.IMPORT_JURISDICTION,
                jurisdiction=JurisdictionCode("ZA"),
            ),
        ],
        # AfCFTA is a regulatory regime, not a jurisdiction (ADR-REG-0017 / 0026).
        regulatory_regimes=[RegimeCode("AfCFTA")],
        hs_classification=HSCode("0901.11.10"),
        origin_claimed_country=JurisdictionCode("UG"),
        origin_regime=RegimeCode("AfCFTA"),
        legal_time=datetime(2026, 9, 30, tzinfo=UTC),
        knowledge_time=datetime(2026, 9, 30, tzinfo=UTC),
    )
    base.update(overrides)
    return RegulatoryContext(**base)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_unsatisfied_when_documents_missing() -> None:
    evaluator = ReferenceEvaluator()
    decision = await evaluator.evaluate(
        context=_ctx(),
        facts={},
        rule_set_id="ug-za-coffee-v0",
    )
    assert decision.outcome == DecisionOutcome.UNSATISFIED
    assert decision.recommended_disposition is not None
    assert decision.recommended_disposition.disposition == "HOLD"
    codes = {r.code for r in decision.reasons}
    assert "REQUIRED_PHYTOSANITARY_CERTIFICATE_MISSING" in codes
    assert "ORIGIN_PROOF_MISSING_FOR_PREFERENCE" in codes


@pytest.mark.asyncio
async def test_satisfied_when_documents_present() -> None:
    evaluator = ReferenceEvaluator()
    decision = await evaluator.evaluate(
        context=_ctx(),
        facts={
            "phytosanitary_certificate_present": True,
            "origin_certificate_present": True,
            "hs_code": "0901.11.10",
        },
        rule_set_id="ug-za-coffee-v0",
    )
    assert decision.outcome == DecisionOutcome.SATISFIED
    assert decision.recommended_disposition is not None
    assert decision.recommended_disposition.disposition == "ALLOW"


@pytest.mark.asyncio
async def test_evaluation_service_requires_tenant() -> None:
    from baobab_regulations.application.services.evaluation import EvaluationService
    from baobab_regulations.infrastructure.persistence.memory import InMemoryDecisionRepository

    service = EvaluationService(ReferenceEvaluator(), InMemoryDecisionRepository())
    # Bypass model validator to exercise service-level resolve_platform_context.
    bare = PlatformContextRef.model_construct(tenant_id="")
    ctx = _ctx(platform=bare)
    with pytest.raises(TenantContextError):
        await service.evaluate(context=ctx, facts={}, rule_set_id="ug-za-coffee-v0")

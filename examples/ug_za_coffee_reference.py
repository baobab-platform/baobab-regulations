"""Offline reference evaluation for the Uganda → South Africa coffee pilot (ADR-REG-0027)."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from baobab_regulations.application.services.evaluation import EvaluationService
from baobab_regulations.domain.context.models import (
    JurisdictionRole,
    JurisdictionRoleKind,
    PlatformContextRef,
    RegulatoryContext,
)
from baobab_regulations.domain.shared.ids import HSCode, JurisdictionCode, RegimeCode
from baobab_regulations.infrastructure.opa.reference_evaluator import ReferenceEvaluator
from baobab_regulations.infrastructure.persistence.memory import InMemoryDecisionRepository


async def main() -> None:
    service = EvaluationService(ReferenceEvaluator(), InMemoryDecisionRepository())
    context = RegulatoryContext(
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
        hs_classification=HSCode("0901.11.10"),
        origin_claimed_country=JurisdictionCode("UG"),
        origin_regime=RegimeCode("AfCFTA"),
        legal_time=datetime.now(UTC),
        knowledge_time=datetime.now(UTC),
    )
    decision = await service.evaluate(
        context=context,
        facts={
            "phytosanitary_certificate_present": False,
            "origin_certificate_present": False,
        },
        rule_set_id="ug-za-coffee-v0-reference",
    )
    print(f"outcome={decision.outcome}")
    print(f"disposition={decision.recommended_disposition}")
    for reason in decision.reasons:
        print(f"  - {reason.code}: {reason.message}")


if __name__ == "__main__":
    asyncio.run(main())

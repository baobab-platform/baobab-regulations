"""REG-2 domain aggregates and in-memory rule-set repository."""

from datetime import UTC, datetime, timedelta

import pytest

from baobab_regulations.domain.instruments.models import (
    InstrumentKind,
    Jurisdiction,
    Provision,
    RegulatoryAuthority,
    RegulatoryInstrument,
    RegulatoryRegime,
)
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState
from baobab_regulations.domain.shared.ids import JurisdictionCode, RegimeCode, RegulatoryId
from baobab_regulations.domain.shared.temporal import BitemporalInterval
from baobab_regulations.infrastructure.persistence.memory import (
    InMemoryDecisionRepository,
    InMemoryRuleSetRepository,
)


def _interval() -> BitemporalInterval:
    now = datetime(2026, 9, 30, tzinfo=UTC)
    return BitemporalInterval(valid_from=now, knowledge_from=now)


def test_jurisdiction_is_not_regime() -> None:
    j = Jurisdiction(code=JurisdictionCode("UG"), display_name="Uganda", iso_3166_1_alpha2="UG")
    r = RegulatoryRegime(code=RegimeCode("AfCFTA"), display_name="African Continental Free Trade Area")
    assert j.code != r.code
    assert str(r.code) == "AfCFTA"


def test_instrument_and_provision() -> None:
    auth = RegulatoryAuthority(
        authority_id=RegulatoryId("auth-ug-maf"),
        name="Ministry of Agriculture",
        jurisdiction=JurisdictionCode("UG"),
    )
    inst = RegulatoryInstrument(
        instrument_id=RegulatoryId("inst-1"),
        title="Plant Health Notice",
        kind=InstrumentKind.NOTICE,
        issuing_authority_id=auth.authority_id,
        jurisdiction=JurisdictionCode("UG"),
        temporal=_interval(),
    )
    prov = Provision(
        provision_id=RegulatoryId("prov-1"),
        instrument_id=inst.instrument_id,
        locator="art.3",
        text_hash="abc",
        temporal=_interval(),
    )
    assert prov.instrument_id == inst.instrument_id


@pytest.mark.asyncio
async def test_rule_set_active_only_when_verified() -> None:
    repo = InMemoryRuleSetRepository()
    now = datetime(2026, 9, 30, tzinfo=UTC)
    await repo.save(
        RuleSetRecord(
            rule_set_id="ug-za-coffee-candidate",
            corridor_profile="ug-za-coffee",
            assurance_state=AssuranceState.CANDIDATE,
            fingerprint="fp-c",
            legal_valid_from=now,
            knowledge_from=now,
        )
    )
    await repo.save(
        RuleSetRecord(
            rule_set_id="ug-za-coffee-v0",
            corridor_profile="ug-za-coffee",
            assurance_state=AssuranceState.VERIFIED,
            fingerprint="fp-v",
            legal_valid_from=now,
            knowledge_from=now,
        )
    )
    active = await repo.get_active_rule_set_id(
        corridor_profile="ug-za-coffee",
        knowledge_time=now + timedelta(seconds=1),
    )
    assert active == "ug-za-coffee-v0"


@pytest.mark.asyncio
async def test_decisions_are_append_only() -> None:
    from baobab_regulations.domain.decisions.models import RegulatoryDecision
    from baobab_regulations.domain.shared.enums import DecisionOutcome, EnforcementClass

    repo = InMemoryDecisionRepository()
    now = datetime(2026, 9, 30, tzinfo=UTC)
    decision = RegulatoryDecision(
        decision_id=RegulatoryId("d1"),
        assessment_id=RegulatoryId("a1"),
        outcome=DecisionOutcome.SATISFIED,
        enforcement_class=EnforcementClass.E1_ADVISORY,
        evaluated_at=now,
        legal_time=now,
        knowledge_time=now,
    )
    await repo.save(decision)
    with pytest.raises(ValueError, match="append-only"):
        await repo.save(decision)

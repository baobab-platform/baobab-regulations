"""REG-3 source registry, rights policy, and derived-rule gate."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from baobab_regulations.domain.shared.ids import RegulatoryId
from baobab_regulations.domain.shared.temporal import BitemporalInterval
from baobab_regulations.domain.sources.models import (
    AuthoritativeSource,
    DerivedRuleRegistration,
    RightsClass,
    SourceArtefact,
    SourceTrustTier,
)
from baobab_regulations.infrastructure.persistence.sources_memory import (
    InMemorySourceRegistry,
    SourceRegistryError,
)


def _now() -> datetime:
    return datetime(2026, 9, 30, tzinfo=UTC)


def _interval() -> BitemporalInterval:
    return BitemporalInterval(valid_from=_now(), knowledge_from=_now())


def test_hash_only_rejects_stored_text() -> None:
    with pytest.raises(ValidationError):
        SourceArtefact(
            artefact_id=RegulatoryId("art-1"),
            source_id=RegulatoryId("src-1"),
            uri="https://example.official/notice.pdf",
            retrieved_at=_now(),
            content_hash="sha256:abc",
            rights_class=RightsClass.HASH_ONLY,
            text="secret body",
        )


def test_allow_store_text_accepts_body() -> None:
    art = SourceArtefact(
        artefact_id=RegulatoryId("art-2"),
        source_id=RegulatoryId("src-1"),
        uri="https://example.official/notice.pdf",
        retrieved_at=_now(),
        content_hash="sha256:def",
        rights_class=RightsClass.ALLOW_STORE_TEXT,
        text="public notice text",
    )
    assert art.text is not None


@pytest.mark.asyncio
async def test_cannot_register_rule_without_source_artefact() -> None:
    registry = InMemorySourceRegistry()
    reg = DerivedRuleRegistration(
        rule_id=RegulatoryId("rule-1"),
        instrument_id=RegulatoryId("inst-1"),
        source_id=RegulatoryId("src-missing"),
        artefact_id=RegulatoryId("art-missing"),
        rights_class=RightsClass.CITATION_ONLY,
        assurance_state="CANDIDATE",
        legal_basis_refs=["ADR-REG-0027 §SPS"],
        temporal=_interval(),
        created_at=_now(),
    )
    with pytest.raises(SourceRegistryError, match="unknown source"):
        await registry.register_derived_rule(reg)


@pytest.mark.asyncio
async def test_register_rule_with_source_and_rights() -> None:
    registry = InMemorySourceRegistry()
    await registry.save_source(
        AuthoritativeSource(
            source_id=RegulatoryId("src-ug-maf"),
            name="UG MAF notices",
            publisher="Ministry of Agriculture",
            trust_tier=SourceTrustTier.PRIMARY_OFFICIAL,
        )
    )
    await registry.save_artefact(
        SourceArtefact(
            artefact_id=RegulatoryId("art-phyto"),
            source_id=RegulatoryId("src-ug-maf"),
            uri="https://example.official/phyto",
            retrieved_at=_now(),
            content_hash="sha256:phyto",
            rights_class=RightsClass.CITATION_ONLY,
        )
    )
    reg = DerivedRuleRegistration(
        rule_id=RegulatoryId("rule-phyto"),
        instrument_id=RegulatoryId("inst-1"),
        source_id=RegulatoryId("src-ug-maf"),
        artefact_id=RegulatoryId("art-phyto"),
        rights_class=RightsClass.CITATION_ONLY,
        assurance_state="VERIFIED",
        legal_basis_refs=["UG-MAF-phyto-notice"],
        temporal=_interval(),
        created_at=_now(),
    )
    await registry.register_derived_rule(reg)
    links = await registry.list_provenance_for(RegulatoryId("rule-phyto"))
    assert len(links) == 1
    assert links[0].artefact_id == RegulatoryId("art-phyto")


def test_derived_rule_registration_requires_legal_basis() -> None:
    with pytest.raises(ValidationError):
        DerivedRuleRegistration(
            rule_id=RegulatoryId("rule-x"),
            instrument_id=RegulatoryId("inst-1"),
            source_id=RegulatoryId("src-1"),
            artefact_id=RegulatoryId("art-1"),
            rights_class=RightsClass.HASH_ONLY,
            assurance_state="CANDIDATE",
            legal_basis_refs=[],
            temporal=_interval(),
            created_at=_now(),
        )

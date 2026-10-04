"""Regulatory instruments, authorities, and jurisdictions (ADR-REG-0006, 0007, 0008).

Platform organisations and legal entities are *not* modelled here — only
regulatory authorities and instruments (ADR-REG-0026).
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from baobab_regulations.domain.shared.ids import JurisdictionCode, RegimeCode, RegulatoryId
from baobab_regulations.domain.shared.temporal import BitemporalInterval


class InstrumentKind(StrEnum):
    STATUTE = "statute"
    REGULATION = "regulation"
    NOTICE = "notice"
    GUIDELINE = "guideline"
    TREATY = "treaty"
    ADMINISTRATIVE_ACT = "administrative_act"
    OTHER = "other"


class RegulatoryAuthority(BaseModel):
    """Issuing / interpreting authority — not a platform Organisation."""

    authority_id: RegulatoryId
    name: str
    jurisdiction: JurisdictionCode | None = None
    regime: RegimeCode | None = None
    official_code: str | None = None


class Jurisdiction(BaseModel):
    """A legal jurisdiction (country, sub-national, or designated legal territory).

    Never holds regime codes such as AfCFTA (ADR-REG-0007, 0017).
    """

    code: JurisdictionCode
    display_name: str
    iso_3166_1_alpha2: str | None = None
    parent_code: JurisdictionCode | None = None


class RegulatoryRegime(BaseModel):
    """Preferential or other regulatory regime (e.g. AfCFTA)."""

    code: RegimeCode
    display_name: str
    description: str | None = None


class RegulatoryInstrument(BaseModel):
    """Canonical instrument aggregate root (ADR-REG-0006)."""

    instrument_id: RegulatoryId
    title: str
    kind: InstrumentKind
    issuing_authority_id: RegulatoryId
    jurisdiction: JurisdictionCode | None = None
    regime: RegimeCode | None = None
    official_citation: str | None = None
    temporal: BitemporalInterval
    source_artefact_ids: list[RegulatoryId] = Field(default_factory=list)


class Provision(BaseModel):
    """Locator within an instrument — text may be omitted under rights policy."""

    provision_id: RegulatoryId
    instrument_id: RegulatoryId
    locator: str
    heading: str | None = None
    text_hash: str | None = None
    text: str | None = None
    temporal: BitemporalInterval


class DerivedRule(BaseModel):
    """Machine-actionable rule derived from provisions (not the provision itself)."""

    rule_id: RegulatoryId
    instrument_id: RegulatoryId
    provision_ids: list[RegulatoryId] = Field(default_factory=list)
    rule_set_id: str | None = None
    assurance_state: str
    enforcement_class_ceiling: str | None = None
    temporal: BitemporalInterval
    legal_basis_refs: list[str] = Field(default_factory=list)
    created_at: datetime

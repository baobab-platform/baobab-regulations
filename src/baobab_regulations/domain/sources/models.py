"""Authoritative sources, artefacts, rights, and provenance (ADR-REG-0003, 0011, 0012, 0014).

Separation (machine-enforced by type):

    AUTHORITATIVE SOURCE → SOURCE ARTEFACT → BAOBAB REPRESENTATION
        → INTERPRETATION → DERIVED RULE

Vendor SDK payloads never appear in this package.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from baobab_regulations.domain.shared.ids import JurisdictionCode, RegimeCode, RegulatoryId
from baobab_regulations.domain.shared.temporal import BitemporalInterval


class RightsClass(StrEnum):
    """What Baobab may lawfully do with an artefact (ADR-REG-0012)."""

    ALLOW_STORE_TEXT = "allow_store_text"
    HASH_ONLY = "hash_only"
    CITATION_ONLY = "citation_only"
    NO_AI_TRAIN = "no_ai_train"


class SourceTrustTier(StrEnum):
    """Multidimensional trust label (ADR-REG-0011) — simplified v0."""

    PRIMARY_OFFICIAL = "primary_official"
    OFFICIAL_REPUBLICATION = "official_republication"
    SECONDARY_COMMENTARY = "secondary_commentary"
    UNKNOWN = "unknown"


class AuthoritativeSource(BaseModel):
    """Registry entry for a publisher / official source (not an artefact body)."""

    source_id: RegulatoryId
    name: str
    publisher: str
    home_uri: str | None = None
    jurisdiction: JurisdictionCode | None = None
    regime: RegimeCode | None = None
    trust_tier: SourceTrustTier = SourceTrustTier.UNKNOWN
    notes: str | None = None


class SourceArtefact(BaseModel):
    """A retrieved artefact under a known rights class (ADR-REG-0003, 0012)."""

    artefact_id: RegulatoryId
    source_id: RegulatoryId
    uri: str
    retrieved_at: datetime
    content_hash: str
    rights_class: RightsClass
    media_type: str | None = None
    title: str | None = None
    temporal: BitemporalInterval | None = None
    text: str | None = None

    @model_validator(mode="after")
    def enforce_rights_on_text(self) -> "SourceArtefact":
        if self.text is not None and self.rights_class != RightsClass.ALLOW_STORE_TEXT:
            msg = (
                f"text storage forbidden for rights_class={self.rights_class.value}; "
                "store content_hash only"
            )
            raise ValueError(msg)
        if not self.content_hash or not str(self.content_hash).strip():
            raise ValueError("content_hash is required for every source artefact")
        return self


class ProvenanceLink(BaseModel):
    """Evidentiary chain edge: derived knowledge → artefact / source (ADR-REG-0014)."""

    link_id: RegulatoryId
    subject_id: RegulatoryId
    subject_kind: str
    artefact_id: RegulatoryId | None = None
    source_id: RegulatoryId | None = None
    citation: str | None = None
    created_at: datetime

    @model_validator(mode="after")
    def require_artefact_or_source(self) -> "ProvenanceLink":
        if not self.artefact_id and not self.source_id and not self.citation:
            raise ValueError("provenance link requires artefact_id, source_id, or citation")
        return self


class DerivedRuleRegistration(BaseModel):
    """Gate: a derived rule may only be registered with source + rights evidence."""

    rule_id: RegulatoryId
    instrument_id: RegulatoryId
    provision_ids: list[RegulatoryId] = Field(default_factory=list)
    source_id: RegulatoryId
    artefact_id: RegulatoryId
    rights_class: RightsClass
    assurance_state: str
    legal_basis_refs: list[str] = Field(default_factory=list)
    temporal: BitemporalInterval
    created_at: datetime

    @model_validator(mode="after")
    def require_source_and_rights(self) -> "DerivedRuleRegistration":
        if not self.source_id or not str(self.source_id).strip():
            raise ValueError("DerivedRule requires source_id")
        if not self.artefact_id or not str(self.artefact_id).strip():
            raise ValueError("DerivedRule requires artefact_id")
        if not self.rights_class:
            raise ValueError("DerivedRule requires rights_class")
        if not self.legal_basis_refs:
            raise ValueError("DerivedRule requires at least one legal_basis_ref")
        return self

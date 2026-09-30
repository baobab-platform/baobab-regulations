"""Regulatory vs platform context (ADR-REG-0017, ADR-REG-0026).

PlatformContext (tenant, organisation, legal entity, market, trade lane)
is owned by baobab-cp. Regulations only holds opaque references and enriches
them with regulatory dimensions.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from baobab_regulations.domain.shared.ids import HSCode, JurisdictionCode, RegimeCode


class JurisdictionRoleKind(StrEnum):
    EXPORTER_ESTABLISHMENT = "exporter_establishment"
    IMPORTER_ESTABLISHMENT = "importer_establishment"
    ORIGIN = "origin"
    EXPORT_JURISDICTION = "export_jurisdiction"
    IMPORT_JURISDICTION = "import_jurisdiction"
    DESTINATION = "destination"
    TRANSIT = "transit"
    PREFERENTIAL_REGIME = "preferential_regime"


class JurisdictionRole(BaseModel):
    role: JurisdictionRoleKind
    jurisdiction: JurisdictionCode
    regime: RegimeCode | None = None


class PlatformContextRef(BaseModel):
    """Opaque references into Control Plane — never redefined here."""

    tenant_id: str
    organisation_id: str | None = None
    legal_entity_id: str | None = None
    market_id: str | None = None
    trade_lane_id: str | None = None
    capability_grant_ids: list[str] = Field(default_factory=list)


class RegulatoryContext(BaseModel):
    """Enriched regulatory evaluation context for one assessment."""

    platform: PlatformContextRef
    jurisdiction_roles: list[JurisdictionRole] = Field(default_factory=list)
    regulated_activity: str | None = None
    commodity_description: str | None = None
    hs_classification: HSCode | None = None
    hs_nomenclature_version: str | None = None
    origin_claimed_country: JurisdictionCode | None = None
    origin_regime: RegimeCode | None = None
    legal_time: datetime
    knowledge_time: datetime
    evidence_state: dict[str, str] = Field(default_factory=dict)

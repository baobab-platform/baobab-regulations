"""Opaque regulatory identifiers — never platform tenant/org IDs."""

from typing import NewType

# Opaque string identifiers owned by the Regulations bounded context.
# Platform identities (tenant, organisation, legal entity) remain references
# resolved by baobab-cp and are never redefined here (ADR-REG-0026).

RegulatoryId = NewType("RegulatoryId", str)
JurisdictionCode = NewType("JurisdictionCode", str)
RegimeCode = NewType("RegimeCode", str)
HSCode = NewType("HSCode", str)

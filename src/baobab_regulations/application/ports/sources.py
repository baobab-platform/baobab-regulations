"""Ports for the authoritative source registry (ADR-REG-0011, 0014)."""

from typing import Protocol

from baobab_regulations.domain.shared.ids import RegulatoryId
from baobab_regulations.domain.sources.models import (
    AuthoritativeSource,
    DerivedRuleRegistration,
    ProvenanceLink,
    SourceArtefact,
)


class SourceRegistryPort(Protocol):
    async def save_source(self, source: AuthoritativeSource) -> None: ...

    async def get_source(self, source_id: RegulatoryId) -> AuthoritativeSource | None: ...

    async def save_artefact(self, artefact: SourceArtefact) -> None: ...

    async def get_artefact(self, artefact_id: RegulatoryId) -> SourceArtefact | None: ...

    async def save_provenance(self, link: ProvenanceLink) -> None: ...

    async def list_provenance_for(self, subject_id: RegulatoryId) -> list[ProvenanceLink]: ...

    async def register_derived_rule(self, registration: DerivedRuleRegistration) -> None: ...

"""In-memory source registry (REG-3 offline path)."""

from baobab_regulations.domain.shared.ids import RegulatoryId
from baobab_regulations.domain.sources.models import (
    AuthoritativeSource,
    DerivedRuleRegistration,
    ProvenanceLink,
    SourceArtefact,
)


class SourceRegistryError(ValueError):
    """Raised when registration violates source/rights gates."""


class InMemorySourceRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, AuthoritativeSource] = {}
        self._artefacts: dict[str, SourceArtefact] = {}
        self._provenance: list[ProvenanceLink] = []
        self._registrations: dict[str, DerivedRuleRegistration] = {}

    async def save_source(self, source: AuthoritativeSource) -> None:
        self._sources[str(source.source_id)] = source

    async def get_source(self, source_id: RegulatoryId) -> AuthoritativeSource | None:
        return self._sources.get(str(source_id))

    async def save_artefact(self, artefact: SourceArtefact) -> None:
        if str(artefact.source_id) not in self._sources:
            raise SourceRegistryError(
                f"unknown source_id={artefact.source_id}; register AuthoritativeSource first"
            )
        self._artefacts[str(artefact.artefact_id)] = artefact

    async def get_artefact(self, artefact_id: RegulatoryId) -> SourceArtefact | None:
        return self._artefacts.get(str(artefact_id))

    async def save_provenance(self, link: ProvenanceLink) -> None:
        self._provenance.append(link)

    async def list_provenance_for(self, subject_id: RegulatoryId) -> list[ProvenanceLink]:
        sid = str(subject_id)
        return [p for p in self._provenance if str(p.subject_id) == sid]

    async def register_derived_rule(self, registration: DerivedRuleRegistration) -> None:
        """Refuse rules that lack a known source artefact with rights class."""
        source = self._sources.get(str(registration.source_id))
        if source is None:
            raise SourceRegistryError(
                f"cannot register derived rule {registration.rule_id}: unknown source"
            )
        artefact = self._artefacts.get(str(registration.artefact_id))
        if artefact is None:
            raise SourceRegistryError(
                f"cannot register derived rule {registration.rule_id}: unknown artefact"
            )
        if artefact.source_id != registration.source_id:
            raise SourceRegistryError("artefact.source_id does not match registration.source_id")
        if artefact.rights_class != registration.rights_class:
            raise SourceRegistryError(
                "registration.rights_class must match artefact.rights_class"
            )
        self._registrations[str(registration.rule_id)] = registration
        self._provenance.append(
            ProvenanceLink(
                link_id=RegulatoryId(f"prov-{registration.rule_id}"),
                subject_id=registration.rule_id,
                subject_kind="derived_rule",
                artefact_id=registration.artefact_id,
                source_id=registration.source_id,
                citation=registration.legal_basis_refs[0] if registration.legal_basis_refs else None,
                created_at=registration.created_at,
            )
        )

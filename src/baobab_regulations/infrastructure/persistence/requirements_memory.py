"""In-memory exact requirement projection store for R-CAP-01 tests/local use."""

from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityUnavailableError,
    RequirementLookup,
    RequirementLookupStatus,
)
from baobab_regulations.contracts.rtd06 import (
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
)


def _exact_key(reference: RegulatoryRequirementReference) -> tuple[str, ...]:
    version = reference.object_version
    version_kind = version.kind if version is not None else ""
    version_value = version.value if version is not None else ""
    return (
        reference.owner_engine_id,
        reference.object_type,
        reference.object_id,
        reference.reference_mode,
        version_kind,
        version_value,
        reference.scope,
        reference.tenant_id or "",
    )


def _identity_key(reference: RegulatoryRequirementReference) -> tuple[str, ...]:
    return (
        reference.owner_engine_id,
        reference.object_type,
        reference.object_id,
        reference.scope,
        reference.tenant_id or "",
    )


class InMemoryRequirementRepository:
    """Read adapter preserving exact historical pin semantics.

    A different pin for the same owner/type/id/scope is reported as CONFLICT,
    never silently redirected to the stored state.
    """

    def __init__(
        self,
        projections: list[RegulatoryDocumentRequirementProjection] | None = None,
    ) -> None:
        self._store: dict[tuple[str, ...], RegulatoryDocumentRequirementProjection] = {}
        self._available = True
        for projection in projections or []:
            self.add(projection)

    def add(self, projection: RegulatoryDocumentRequirementProjection) -> None:
        self._store[_exact_key(projection.requirement_reference)] = projection

    def set_available(self, available: bool) -> None:
        self._available = available

    async def resolve_exact(
        self,
        reference: RegulatoryRequirementReference,
    ) -> RequirementLookup:
        if not self._available:
            raise RequirementAuthorityUnavailableError(
                "in-memory Regulations requirement authority is unavailable"
            )

        exact = self._store.get(_exact_key(reference))
        if exact is not None:
            return RequirementLookup(
                status=RequirementLookupStatus.FOUND,
                requirement=exact,
            )

        requested_identity = _identity_key(reference)
        if any(
            _identity_key(projection.requirement_reference) == requested_identity
            for projection in self._store.values()
        ):
            return RequirementLookup(status=RequirementLookupStatus.CONFLICT)

        return RequirementLookup(status=RequirementLookupStatus.NOT_FOUND)


__all__ = ["InMemoryRequirementRepository"]

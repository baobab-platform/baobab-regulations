"""Exact pinned requirement resolution port for R-CAP-01."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from baobab_regulations.contracts.rtd06 import (
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
)


class RequirementLookupStatus(StrEnum):
    """Owner-side result for one exact pinned reference."""

    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True, slots=True)
class RequirementLookup:
    """Repository lookup result without collapsing absence and staleness."""

    status: RequirementLookupStatus
    requirement: RegulatoryDocumentRequirementProjection | None = None

    def __post_init__(self) -> None:
        if self.status is RequirementLookupStatus.FOUND and self.requirement is None:
            raise ValueError("FOUND lookup requires a requirement projection")
        if self.status is not RequirementLookupStatus.FOUND and self.requirement is not None:
            raise ValueError("non-FOUND lookup must not carry a requirement projection")


class RequirementAuthorityIntegrityError(RuntimeError):
    """Owner-side persisted requirement content failed an integrity check."""


class RequirementAuthorityUnavailableError(RuntimeError):
    """Regulations requirement authority/store is unavailable."""


class RequirementRepositoryPort(Protocol):
    """Resolve an exact historical requirement reference owned by Regulations."""

    async def resolve_exact(
        self,
        reference: RegulatoryRequirementReference,
    ) -> RequirementLookup:
        pass


__all__ = [
    "RequirementAuthorityIntegrityError",
    "RequirementAuthorityUnavailableError",
    "RequirementLookup",
    "RequirementLookupStatus",
    "RequirementRepositoryPort",
]

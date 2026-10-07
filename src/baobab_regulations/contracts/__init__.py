"""Runtime adapters for canonical Shared contracts.

The canonical wire schemas remain owned by baobab-platform/shared.
"""

from baobab_regulations.contracts.rtd06 import (
    ObjectVersion,
    PinnedRegulationsReference,
    RegulatoryDecisionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
    RequirementResolveRequest,
    RequirementResolveResponse,
)

__all__ = [
    "ObjectVersion",
    "PinnedRegulationsReference",
    "RegulatoryDecisionReference",
    "RegulatoryDocumentRequirementProjection",
    "RegulatoryRequirementReference",
    "RequirementResolveRequest",
    "RequirementResolveResponse",
]

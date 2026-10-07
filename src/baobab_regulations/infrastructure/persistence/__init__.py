"""Persistence adapters."""

from baobab_regulations.infrastructure.persistence.idempotency_memory import (
    InMemoryEvidenceAssessmentIdempotency,
)
from baobab_regulations.infrastructure.persistence.idempotency_postgres import (
    PostgresEvidenceAssessmentIdempotency,
)
from baobab_regulations.infrastructure.persistence.memory import (
    InMemoryDecisionRepository,
    InMemoryRuleSetRepository,
)
from baobab_regulations.infrastructure.persistence.requirements_memory import (
    InMemoryRequirementRepository,
)
from baobab_regulations.infrastructure.persistence.sources_memory import (
    InMemorySourceRegistry,
    SourceRegistryError,
)

__all__ = [
    "InMemoryDecisionRepository",
    "InMemoryEvidenceAssessmentIdempotency",
    "PostgresEvidenceAssessmentIdempotency",
    "InMemoryRequirementRepository",
    "InMemoryRuleSetRepository",
    "InMemorySourceRegistry",
    "SourceRegistryError",
]

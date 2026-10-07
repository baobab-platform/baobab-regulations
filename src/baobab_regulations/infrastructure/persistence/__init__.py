"""Persistence adapters."""

from baobab_regulations.infrastructure.persistence.decision_idempotency_memory import (
    InMemoryDecisionEvaluationIdempotency,
)
from baobab_regulations.infrastructure.persistence.decision_idempotency_postgres import (
    PostgresDecisionEvaluationIdempotency,
)
from baobab_regulations.infrastructure.persistence.requirements_postgres import (
    GovernedRequirementProjectionWriter,
    PostgresRequirementRepository,
)
from baobab_regulations.infrastructure.persistence.event_outbox_postgres import (
    PostgresEventOutboxRepository,
)
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
    "InMemoryDecisionEvaluationIdempotency",
    "InMemoryDecisionRepository",
    "InMemoryEvidenceAssessmentIdempotency",
    "GovernedRequirementProjectionWriter",
    "PostgresRequirementRepository",
    "PostgresDecisionEvaluationIdempotency",
    "PostgresEvidenceAssessmentIdempotency",
    "PostgresEventOutboxRepository",
    "InMemoryRequirementRepository",
    "InMemoryRuleSetRepository",
    "InMemorySourceRegistry",
    "SourceRegistryError",
]

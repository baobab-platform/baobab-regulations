"""Protocol interfaces — provider-neutral boundaries (ADR-REG-0005, 0016, 0018)."""

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthorityPort,
    ContextAuthorityUnavailableError,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.evaluator import RegulatoryPolicyEvaluatorPort
from baobab_regulations.application.ports.evidence_assessment import (
    DocumentaryEvidenceAssessorPort,
    DocumentaryEvidenceAssessorUnavailableError,
    EvidenceAssessmentIdentity,
)
from baobab_regulations.application.ports.idempotency import (
    EvidenceAssessmentIdempotencyPort,
    IdempotencyAuthorityUnavailableError,
    IdempotencyConflictError,
    IdempotencyReplay,
)
from baobab_regulations.application.ports.repository import (
    DecisionRepositoryPort,
    RuleSetRepositoryPort,
)
from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityUnavailableError,
    RequirementLookup,
    RequirementLookupStatus,
    RequirementRepositoryPort,
)

__all__ = [
    "AuthenticatedCaller",
    "ContextAccessDeniedError",
    "ContextAuthorityPort",
    "ContextAuthorityUnavailableError",
    "DecisionRepositoryPort",
    "DocumentaryEvidenceAssessorPort",
    "DocumentaryEvidenceAssessorUnavailableError",
    "EvidenceAssessmentIdentity",
    "EvidenceAssessmentIdempotencyPort",
    "IdempotencyAuthorityUnavailableError",
    "IdempotencyConflictError",
    "IdempotencyReplay",
    "RegulatoryPolicyEvaluatorPort",
    "RequirementAuthorityUnavailableError",
    "RequirementLookup",
    "RequirementLookupStatus",
    "RequirementRepositoryPort",
    "RuleSetRepositoryPort",
    "TrustedPlatformContext",
]

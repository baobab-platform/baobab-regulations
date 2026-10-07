"""Protocol interfaces — provider-neutral boundaries (ADR-REG-0005, 0016, 0018)."""

from baobab_regulations.application.ports.authentication import (
    WorkloadAuthenticationError,
    WorkloadAuthenticationUnavailableError,
    WorkloadAuthenticatorPort,
)
from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityPort,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.control_plane import (
    ValidatorCredentialUnavailableError,
    ValidatorTokenProviderPort,
)
from baobab_regulations.application.ports.evaluator import RegulatoryPolicyEvaluatorPort
from baobab_regulations.application.ports.events import EventPublicationMetadata
from baobab_regulations.application.ports.evidence_assessment import (
    DocumentaryEvidenceAssessorPort,
    DocumentaryEvidenceAssessorUnavailableError,
    EvidenceAssessmentIdentity,
)
from baobab_regulations.application.ports.idempotency import (
    EvidenceAssessmentIdempotencyPort,
    IdempotencyAuthorityUnavailableError,
    IdempotencyCommit,
    IdempotencyConflictError,
    IdempotencyIntegrityError,
    IdempotencyReplay,
)
from baobab_regulations.application.ports.outbox import (
    CanonicalEventPublisherPort,
    EventOutboxAuthorityUnavailableError,
    EventOutboxIntegrityError,
    EventOutboxRecord,
    EventOutboxRepositoryPort,
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
    "ContextAuthenticationError",
    "ContextAuthorityPort",
    "ContextAuthorityUnavailableError",
    "ContextNotFoundError",
    "CanonicalEventPublisherPort",
    "DecisionRepositoryPort",
    "DocumentaryEvidenceAssessorPort",
    "DocumentaryEvidenceAssessorUnavailableError",
    "EventOutboxAuthorityUnavailableError",
    "EventOutboxIntegrityError",
    "EventOutboxRecord",
    "EventOutboxRepositoryPort",
    "EventPublicationMetadata",
    "EvidenceAssessmentIdentity",
    "EvidenceAssessmentIdempotencyPort",
    "IdempotencyAuthorityUnavailableError",
    "IdempotencyCommit",
    "IdempotencyConflictError",
    "IdempotencyIntegrityError",
    "IdempotencyReplay",
    "RegulatoryPolicyEvaluatorPort",
    "RequirementAuthorityUnavailableError",
    "RequirementLookup",
    "RequirementLookupStatus",
    "RequirementRepositoryPort",
    "RuleSetRepositoryPort",
    "TrustedPlatformContext",
    "ValidatorCredentialUnavailableError",
    "ValidatorTokenProviderPort",
    "WorkloadAuthenticationError",
    "WorkloadAuthenticationUnavailableError",
    "WorkloadAuthenticatorPort",
]

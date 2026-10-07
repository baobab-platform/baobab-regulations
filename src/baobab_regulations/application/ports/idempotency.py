"""Durable idempotency boundary for RTD-06 evidence-assessment commands."""

from dataclasses import dataclass
from typing import Protocol

from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
)


@dataclass(frozen=True, slots=True)
class IdempotencyReplay:
    """Previously committed result for the same tenant/key/fingerprint."""

    result: DocumentEvidenceAssessmentResult


@dataclass(frozen=True, slots=True)
class IdempotencyCommit:
    """Authoritative result after an atomic store-if-absent commit.

    created is true only for the caller that inserted the durable record.
    Concurrent callers for the same tenant/key/fingerprint receive the already
    committed result with created=False.
    """

    result: DocumentEvidenceAssessmentResult
    created: bool


class IdempotencyConflictError(RuntimeError):
    """The same tenant/key was already committed for a different request."""


class IdempotencyIntegrityError(RuntimeError):
    """Persisted assessment state is internally inconsistent or corrupted."""


class IdempotencyAuthorityUnavailableError(RuntimeError):
    """The idempotency/assessment authority is unavailable."""


class EvidenceAssessmentIdempotencyPort(Protocol):
    """Durably replay or commit one assessment by tenant + idempotency key."""

    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
    ) -> IdempotencyReplay | None: ...

    async def commit(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        request: DocumentEvidenceAssessmentRequest,
        result: DocumentEvidenceAssessmentResult,
    ) -> IdempotencyCommit: ...


__all__ = [
    "EvidenceAssessmentIdempotencyPort",
    "IdempotencyAuthorityUnavailableError",
    "IdempotencyCommit",
    "IdempotencyConflictError",
    "IdempotencyIntegrityError",
    "IdempotencyReplay",
]

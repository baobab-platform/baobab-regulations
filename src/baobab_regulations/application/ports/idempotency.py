"""Idempotency boundary for RTD-06 mutating assessment commands."""

from dataclasses import dataclass
from typing import Protocol

from baobab_regulations.contracts.rtd06 import DocumentEvidenceAssessmentResult


@dataclass(frozen=True, slots=True)
class IdempotencyReplay:
    """Previously committed result for the same idempotency key/fingerprint."""

    result: DocumentEvidenceAssessmentResult


class IdempotencyConflictError(RuntimeError):
    """The same key was already committed for a different request fingerprint."""


class IdempotencyAuthorityUnavailableError(RuntimeError):
    """The idempotency authority/store is unavailable."""


class EvidenceAssessmentIdempotencyPort(Protocol):
    """Replay or commit one assessment result by tenant + idempotency key."""

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
        result: DocumentEvidenceAssessmentResult,
    ) -> None: ...


__all__ = [
    "EvidenceAssessmentIdempotencyPort",
    "IdempotencyAuthorityUnavailableError",
    "IdempotencyConflictError",
    "IdempotencyReplay",
]

"""In-memory R-CAP-02 idempotency adapter.

This provides deterministic command semantics for tests/local execution only.
R-CAP-05 remains responsible for durable assessment persistence/idempotency.
"""

from dataclasses import dataclass

from baobab_regulations.application.ports.idempotency import (
    IdempotencyConflictError,
    IdempotencyReplay,
)
from baobab_regulations.contracts.rtd06 import DocumentEvidenceAssessmentResult


@dataclass(frozen=True, slots=True)
class _StoredAssessment:
    request_fingerprint: str
    result: DocumentEvidenceAssessmentResult


class InMemoryEvidenceAssessmentIdempotency:
    def __init__(self) -> None:
        self._store: dict[tuple[str, str], _StoredAssessment] = {}

    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
    ) -> IdempotencyReplay | None:
        stored = self._store.get((tenant_id, idempotency_key))
        if stored is None:
            return None
        if stored.request_fingerprint != request_fingerprint:
            raise IdempotencyConflictError(
                "idempotency key already belongs to a different request"
            )
        return IdempotencyReplay(result=stored.result)

    async def commit(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        result: DocumentEvidenceAssessmentResult,
    ) -> None:
        key = (tenant_id, idempotency_key)
        stored = self._store.get(key)
        if stored is not None:
            if stored.request_fingerprint != request_fingerprint:
                raise IdempotencyConflictError(
                    "idempotency key already belongs to a different request"
                )
            return
        self._store[key] = _StoredAssessment(
            request_fingerprint=request_fingerprint,
            result=result,
        )


__all__ = ["InMemoryEvidenceAssessmentIdempotency"]

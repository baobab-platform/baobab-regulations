"""In-memory implementation of the R-CAP-05 idempotency contract.

Kept for unit tests and local deterministic execution. Production uses the
PostgreSQL adapter; both implementations share atomic store-if-absent semantics.
"""

from dataclasses import dataclass

from baobab_regulations.application.ports.idempotency import (
    IdempotencyCommit,
    IdempotencyConflictError,
    IdempotencyReplay,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
)


@dataclass(frozen=True, slots=True)
class _StoredAssessment:
    request_fingerprint: str
    request: DocumentEvidenceAssessmentRequest
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
        request: DocumentEvidenceAssessmentRequest,
        result: DocumentEvidenceAssessmentResult,
    ) -> IdempotencyCommit:
        key = (tenant_id, idempotency_key)
        stored = self._store.get(key)
        if stored is not None:
            if stored.request_fingerprint != request_fingerprint:
                raise IdempotencyConflictError(
                    "idempotency key already belongs to a different request"
                )
            return IdempotencyCommit(result=stored.result, created=False)
        self._store[key] = _StoredAssessment(
            request_fingerprint=request_fingerprint,
            request=request,
            result=result,
        )
        return IdempotencyCommit(result=result, created=True)


__all__ = ["InMemoryEvidenceAssessmentIdempotency"]

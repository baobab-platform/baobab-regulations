"""Durable command/replay boundary for regulations.decision.evaluate."""

from dataclasses import dataclass
from typing import Protocol

from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
)


@dataclass(frozen=True, slots=True)
class DecisionReplay:
    response: DecisionEvaluateResponse


@dataclass(frozen=True, slots=True)
class DecisionCommit:
    response: DecisionEvaluateResponse
    created: bool


class DecisionIdempotencyConflictError(RuntimeError):
    """Tenant/key or replay identity already belongs to another semantic input."""


class DecisionIdempotencyIntegrityError(RuntimeError):
    """Persisted decision command state is corrupt or internally inconsistent."""


class DecisionIdempotencyUnavailableError(RuntimeError):
    """Durable decision/idempotency authority is unavailable."""


class DecisionEvaluationIdempotencyPort(Protocol):
    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        replay_key: str,
        input_fingerprint: str,
    ) -> DecisionReplay | None:
        pass

    async def commit(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        input_fingerprint: str,
        request: DecisionEvaluateRequest,
        response: DecisionEvaluateResponse,
    ) -> DecisionCommit:
        pass


__all__ = [
    "DecisionCommit",
    "DecisionEvaluationIdempotencyPort",
    "DecisionIdempotencyConflictError",
    "DecisionIdempotencyIntegrityError",
    "DecisionIdempotencyUnavailableError",
    "DecisionReplay",
]

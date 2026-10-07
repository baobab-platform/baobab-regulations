"""In-memory decision command/replay store for deterministic tests."""

from baobab_regulations.application.ports.decision_idempotency import (
    DecisionCommit,
    DecisionIdempotencyConflictError,
    DecisionReplay,
)
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
)


class InMemoryDecisionEvaluationIdempotency:
    def __init__(self) -> None:
        self._by_key: dict[tuple[str, str], tuple[str, str, DecisionEvaluateResponse]] = {}
        self._by_replay: dict[tuple[str, str], tuple[str, DecisionEvaluateResponse]] = {}

    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        replay_key: str,
        input_fingerprint: str,
    ) -> DecisionReplay | None:
        item = self._by_key.get((tenant_id, idempotency_key))
        if item is not None:
            stored_request_fingerprint, stored_input_fingerprint, response = item
            if stored_request_fingerprint != request_fingerprint:
                raise DecisionIdempotencyConflictError(
                    "idempotency key already belongs to a different request"
                )
            if stored_input_fingerprint != input_fingerprint:
                raise DecisionIdempotencyConflictError(
                    "idempotency record does not match semantic input fingerprint"
                )
            return DecisionReplay(response=response)

        replay_item = self._by_replay.get((tenant_id, replay_key))
        if replay_item is None:
            return None
        stored_input_fingerprint, response = replay_item
        if stored_input_fingerprint != input_fingerprint:
            raise DecisionIdempotencyConflictError(
                "replay_key already belongs to a different semantic input"
            )
        return DecisionReplay(response=response)

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
        existing = await self.replay(
            tenant_id=tenant_id,
            idempotency_key=idempotency_key,
            request_fingerprint=request_fingerprint,
            replay_key=request.replay_key,
            input_fingerprint=input_fingerprint,
        )
        if existing is not None:
            return DecisionCommit(response=existing.response, created=False)

        replay_key = request.replay_key
        replay_item = self._by_replay.get((tenant_id, replay_key))
        if replay_item is not None:
            stored_input_fingerprint, stored_response = replay_item
            if stored_input_fingerprint != input_fingerprint:
                raise DecisionIdempotencyConflictError(
                    "replay_key already belongs to a different semantic input"
                )
            self._by_key[(tenant_id, idempotency_key)] = (
                request_fingerprint,
                input_fingerprint,
                stored_response,
            )
            return DecisionCommit(response=stored_response, created=False)

        self._by_key[(tenant_id, idempotency_key)] = (
            request_fingerprint,
            input_fingerprint,
            response,
        )
        self._by_replay[(tenant_id, replay_key)] = (input_fingerprint, response)
        return DecisionCommit(response=response, created=True)


__all__ = ["InMemoryDecisionEvaluationIdempotency"]

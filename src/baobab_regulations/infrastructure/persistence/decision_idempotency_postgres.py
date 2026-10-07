"""PostgreSQL durable decision command/idempotency store for R-CAP-09."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

import asyncpg
from pydantic import ValidationError

from baobab_regulations.application.ports.decision_idempotency import (
    DecisionCommit,
    DecisionIdempotencyConflictError,
    DecisionIdempotencyIntegrityError,
    DecisionIdempotencyUnavailableError,
    DecisionReplay,
)
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
)


class PostgresDecisionEvaluationIdempotency:
    """Tenant-scoped durable command and semantic replay authority."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        replay_key: str,
        input_fingerprint: str,
    ) -> DecisionReplay | None:
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await self._fetch_by_key(
                    conn,
                    tenant_id=tenant_id,
                    idempotency_key=idempotency_key,
                )
                if row is None:
                    row = await self._fetch_by_replay(
                        conn,
                        tenant_id=tenant_id,
                        replay_key=replay_key,
                    )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise DecisionIdempotencyUnavailableError(
                "durable regulatory decision store is unavailable"
            ) from exc

        if row is None:
            return None
        response = self._validate_row(
            row,
            expected_tenant_id=tenant_id,
            expected_idempotency_key=idempotency_key,
            expected_request_fingerprint=request_fingerprint,
            expected_replay_key=replay_key,
            expected_input_fingerprint=input_fingerprint,
            allow_idempotency_alias=True,
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
        request_json = self._canonical_json(request)
        response_json = self._canonical_json(response)
        result_fingerprint = self._sha256(response_json)

        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await conn.fetchrow(
                    """
                    INSERT INTO regulatory_decision_evaluations (
                        decision_id,
                        assessment_id,
                        tenant_id,
                        idempotency_key,
                        replay_key,
                        request_fingerprint,
                        input_fingerprint,
                        result_fingerprint,
                        contract_major,
                        rule_set_object_id,
                        rule_set_fingerprint,
                        outcome,
                        enforcement_class,
                        request_payload,
                        response_payload,
                        legal_time,
                        knowledge_time,
                        evaluated_at
                    ) VALUES (
                        $1, $2, $3, $4, $5,
                        $6, $7, $8, 1,
                        $9, $10, $11, $12,
                        $13::jsonb, $14::jsonb,
                        $15, $16, $17
                    )
                    ON CONFLICT DO NOTHING
                    RETURNING *
                    """,
                    response.decision_reference.object_id,
                    response.assessment_reference.object_id,
                    tenant_id,
                    idempotency_key,
                    request.replay_key,
                    request_fingerprint,
                    input_fingerprint,
                    result_fingerprint,
                    response.rule_set_reference.object_id,
                    response.rule_set_fingerprint,
                    response.outcome,
                    response.enforcement_class,
                    request_json,
                    response_json,
                    response.legal_time,
                    response.knowledge_time,
                    response.evaluated_at,
                )
                created = row is not None
                if row is None:
                    row = await self._fetch_by_key(
                        conn,
                        tenant_id=tenant_id,
                        idempotency_key=idempotency_key,
                    )
                if row is None:
                    row = await self._fetch_by_replay(
                        conn,
                        tenant_id=tenant_id,
                        replay_key=request.replay_key,
                    )
        except (
            asyncpg.UniqueViolationError,
            asyncpg.CheckViolationError,
            asyncpg.DataError,
        ) as exc:
            raise DecisionIdempotencyIntegrityError(
                "regulatory decision record violates durable-store invariants"
            ) from exc
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise DecisionIdempotencyUnavailableError(
                "durable regulatory decision store is unavailable"
            ) from exc

        if row is None:
            raise DecisionIdempotencyIntegrityError(
                "decision identity collided without a recoverable durable record"
            )

        committed = self._validate_row(
            row,
            expected_tenant_id=tenant_id,
            expected_idempotency_key=idempotency_key,
            expected_request_fingerprint=request_fingerprint,
            expected_replay_key=request.replay_key,
            expected_input_fingerprint=input_fingerprint,
            allow_idempotency_alias=True,
        )
        return DecisionCommit(response=committed, created=created)

    @staticmethod
    async def _fetch_by_key(
        conn: Any,
        *,
        tenant_id: str,
        idempotency_key: str,
    ) -> Any:
        return await conn.fetchrow(
            """
            SELECT *
            FROM regulatory_decision_evaluations
            WHERE tenant_id = $1 AND idempotency_key = $2
            """,
            tenant_id,
            idempotency_key,
        )

    @staticmethod
    async def _fetch_by_replay(
        conn: Any,
        *,
        tenant_id: str,
        replay_key: str,
    ) -> Any:
        return await conn.fetchrow(
            """
            SELECT *
            FROM regulatory_decision_evaluations
            WHERE tenant_id = $1 AND replay_key = $2
            """,
            tenant_id,
            replay_key,
        )

    @staticmethod
    async def _bind_tenant(conn: Any, tenant_id: str) -> None:
        await conn.execute(
            "SELECT set_config('baobab.tenant_id', $1, true)",
            tenant_id,
        )

    def _validate_row(
        self,
        row: Mapping[str, Any],
        *,
        expected_tenant_id: str,
        expected_idempotency_key: str,
        expected_request_fingerprint: str,
        expected_replay_key: str,
        expected_input_fingerprint: str,
        allow_idempotency_alias: bool,
    ) -> DecisionEvaluateResponse:
        if str(row["tenant_id"]) != expected_tenant_id:
            raise DecisionIdempotencyIntegrityError(
                "persisted decision tenant does not match query scope"
            )

        stored_key = str(row["idempotency_key"])
        stored_replay_key = str(row["replay_key"])
        if stored_replay_key != expected_replay_key:
            raise DecisionIdempotencyConflictError(
                "replay_key already belongs to another durable decision"
            )
        if (
            stored_key == expected_idempotency_key
            and str(row["request_fingerprint"]) != expected_request_fingerprint
        ):
            raise DecisionIdempotencyConflictError(
                "idempotency key already belongs to a different request"
            )
        if stored_key != expected_idempotency_key and not allow_idempotency_alias:
            raise DecisionIdempotencyConflictError(
                "durable decision belongs to another idempotency key"
            )
        if str(row["input_fingerprint"]) != expected_input_fingerprint:
            raise DecisionIdempotencyConflictError(
                "replay_key already belongs to a different semantic input"
            )

        try:
            request = DecisionEvaluateRequest.model_validate(
                self._json_object(row["request_payload"])
            )
            response = DecisionEvaluateResponse.model_validate(
                self._json_object(row["response_payload"])
            )
        except (TypeError, ValueError, ValidationError) as exc:
            raise DecisionIdempotencyIntegrityError(
                "persisted R-CAP-09 decision payload is invalid"
            ) from exc

        stored_request_fingerprint = str(row["request_fingerprint"])
        if self._sha256(self._canonical_json(request)) != stored_request_fingerprint:
            raise DecisionIdempotencyIntegrityError(
                "persisted request does not match its fingerprint"
            )
        if self._sha256(self._canonical_json(response)) != str(row["result_fingerprint"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted decision response does not match its fingerprint"
            )
        if request.replay_key != expected_replay_key:
            raise DecisionIdempotencyIntegrityError(
                "persisted request replay identity does not match row"
            )
        if response.replay_identity.replay_key != expected_replay_key:
            raise DecisionIdempotencyIntegrityError(
                "persisted response replay identity does not match row"
            )
        if response.replay_identity.input_fingerprint != expected_input_fingerprint:
            raise DecisionIdempotencyIntegrityError(
                "persisted response input fingerprint does not match row"
            )
        if response.decision_reference.object_id != str(row["decision_id"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted decision identity does not match response"
            )
        if response.assessment_reference.object_id != str(row["assessment_id"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted assessment identity does not match response"
            )
        if response.rule_set_reference.object_id != str(row["rule_set_object_id"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted rule-set identity does not match response"
            )
        if response.rule_set_fingerprint != str(row["rule_set_fingerprint"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted rule-set fingerprint does not match response"
            )
        if response.outcome != str(row["outcome"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted outcome does not match response"
            )
        if response.enforcement_class != str(row["enforcement_class"]):
            raise DecisionIdempotencyIntegrityError(
                "persisted enforcement class does not match response"
            )
        if response.legal_time != row["legal_time"]:
            raise DecisionIdempotencyIntegrityError(
                "persisted legal_time does not match response"
            )
        if response.knowledge_time != row["knowledge_time"]:
            raise DecisionIdempotencyIntegrityError(
                "persisted knowledge_time does not match response"
            )
        if response.evaluated_at != row["evaluated_at"]:
            raise DecisionIdempotencyIntegrityError(
                "persisted evaluated_at does not match response"
            )
        return response

    @staticmethod
    def _canonical_json(
        value: DecisionEvaluateRequest | DecisionEvaluateResponse,
    ) -> str:
        return json.dumps(
            value.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _sha256(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _json_object(value: Any) -> dict[str, Any]:
        if isinstance(value, str):
            parsed = json.loads(value)
        elif isinstance(value, bytes):
            parsed = json.loads(value.decode("utf-8"))
        elif isinstance(value, Mapping):
            parsed = dict(value)
        else:
            raise TypeError("persisted JSONB value is not an object")
        if not isinstance(parsed, dict):
            raise TypeError("persisted JSONB value is not an object")
        return parsed


__all__ = ["PostgresDecisionEvaluationIdempotency"]

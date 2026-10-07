"""PostgreSQL durable store for RTD-06 evidence assessments and idempotency."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

import asyncpg
from pydantic import ValidationError

from baobab_regulations.application.ports.idempotency import (
    IdempotencyAuthorityUnavailableError,
    IdempotencyCommit,
    IdempotencyConflictError,
    IdempotencyIntegrityError,
    IdempotencyReplay,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
)


class PostgresEvidenceAssessmentIdempotency:
    """Append-oriented tenant-scoped assessment store.

    Every operation binds the trusted tenant through a transaction-local
    PostgreSQL setting used by RLS. Application predicates remain present as
    defence in depth. Commit is atomic store-if-absent: concurrent callers for
    one tenant/key/fingerprint converge on one persisted result.
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def replay(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
    ) -> IdempotencyReplay | None:
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await conn.fetchrow(
                        """
                        SELECT
                            assessment_id, tenant_id, idempotency_key,
                            request_fingerprint, result_fingerprint,
                            regulatory_decision_object_id, requirement_object_id,
                            assessment_reason, outcome, request_payload, result_payload,
                            evaluated_at
                        FROM regulatory_evidence_assessments
                        WHERE tenant_id = $1 AND idempotency_key = $2
                        """,
                    tenant_id,
                    idempotency_key,
                )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise IdempotencyAuthorityUnavailableError(
                "durable assessment store is unavailable"
            ) from exc

        if row is None:
            return None
        result = self._validate_row(
            row,
            expected_tenant_id=tenant_id,
            expected_idempotency_key=idempotency_key,
            expected_request_fingerprint=request_fingerprint,
        )
        return IdempotencyReplay(result=result)

    async def commit(
        self,
        *,
        tenant_id: str,
        idempotency_key: str,
        request_fingerprint: str,
        request: DocumentEvidenceAssessmentRequest,
        result: DocumentEvidenceAssessmentResult,
    ) -> IdempotencyCommit:
        request_json = self._canonical_json(request)
        result_json = self._canonical_json(result)
        result_fingerprint = self._sha256(result_json)
        assessment_id = result.assessment_reference.object_id

        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await conn.fetchrow(
                        """
                        INSERT INTO regulatory_evidence_assessments (
                            assessment_id,
                            tenant_id,
                            idempotency_key,
                            request_fingerprint,
                            result_fingerprint,
                            contract_major,
                            regulatory_decision_object_id,
                            requirement_object_id,
                            assessment_reason,
                            outcome,
                            request_payload,
                            result_payload,
                            evaluated_at
                        ) VALUES (
                            $1, $2, $3, $4, $5, 1,
                            $6, $7, $8, $9,
                            $10::jsonb, $11::jsonb, $12
                        )
                        ON CONFLICT DO NOTHING
                        RETURNING
                            assessment_id, tenant_id, idempotency_key,
                            request_fingerprint, result_fingerprint,
                            regulatory_decision_object_id, requirement_object_id,
                            assessment_reason, outcome, request_payload, result_payload,
                            evaluated_at
                        """,
                    assessment_id,
                    tenant_id,
                    idempotency_key,
                    request_fingerprint,
                    result_fingerprint,
                    result.regulatory_decision_reference.object_id,
                    result.requirement_reference.object_id,
                    request.assessment_reason,
                    result.outcome,
                    request_json,
                    result_json,
                    result.evaluated_at,
                )
                created = row is not None
                if row is None:
                    row = await conn.fetchrow(
                            """
                            SELECT
                                assessment_id, tenant_id, idempotency_key,
                                request_fingerprint, result_fingerprint,
                                regulatory_decision_object_id, requirement_object_id,
                                assessment_reason, outcome, request_payload, result_payload,
                                evaluated_at
                            FROM regulatory_evidence_assessments
                            WHERE tenant_id = $1 AND idempotency_key = $2
                            """,
                        tenant_id,
                        idempotency_key,
                    )
        except (asyncpg.UniqueViolationError, asyncpg.CheckViolationError, asyncpg.DataError) as exc:
            raise IdempotencyIntegrityError(
                "assessment record violates durable-store invariants"
            ) from exc
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise IdempotencyAuthorityUnavailableError(
                "durable assessment store is unavailable"
            ) from exc

        if row is None:
            raise IdempotencyIntegrityError(
                "assessment identity collided with a different idempotency record"
            )

        committed_result = self._validate_row(
            row,
            expected_tenant_id=tenant_id,
            expected_idempotency_key=idempotency_key,
            expected_request_fingerprint=request_fingerprint,
        )
        return IdempotencyCommit(result=committed_result, created=created)

    @staticmethod
    async def _bind_tenant(conn: Any, tenant_id: str) -> None:
        """Bind RLS tenant context only for the current transaction."""
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
    ) -> DocumentEvidenceAssessmentResult:
        if str(row["tenant_id"]) != expected_tenant_id:
            raise IdempotencyIntegrityError("persisted tenant_id does not match query scope")
        if str(row["idempotency_key"]) != expected_idempotency_key:
            raise IdempotencyIntegrityError("persisted idempotency_key does not match query")

        stored_request_fingerprint = str(row["request_fingerprint"])
        if stored_request_fingerprint != expected_request_fingerprint:
            raise IdempotencyConflictError(
                "idempotency key already belongs to a different request"
            )

        try:
            request = DocumentEvidenceAssessmentRequest.model_validate(
                self._json_object(row["request_payload"])
            )
            result = DocumentEvidenceAssessmentResult.model_validate(
                self._json_object(row["result_payload"])
            )
        except (TypeError, ValueError, ValidationError) as exc:
            raise IdempotencyIntegrityError(
                "persisted RTD-06 assessment payload is invalid"
            ) from exc

        if self._sha256(self._canonical_json(request)) != stored_request_fingerprint:
            raise IdempotencyIntegrityError(
                "persisted request payload does not match its fingerprint"
            )
        if self._sha256(self._canonical_json(result)) != str(row["result_fingerprint"]):
            raise IdempotencyIntegrityError(
                "persisted result payload does not match its fingerprint"
            )

        if result.assessment_reference.object_id != str(row["assessment_id"]):
            raise IdempotencyIntegrityError(
                "persisted assessment identity does not match result payload"
            )
        if result.regulatory_decision_reference.object_id != str(
            row["regulatory_decision_object_id"]
        ):
            raise IdempotencyIntegrityError(
                "persisted RegulatoryDecision identity does not match result payload"
            )
        if result.requirement_reference.object_id != str(row["requirement_object_id"]):
            raise IdempotencyIntegrityError(
                "persisted requirement identity does not match result payload"
            )
        if request.assessment_reason != str(row["assessment_reason"]):
            raise IdempotencyIntegrityError(
                "persisted assessment reason does not match request payload"
            )
        if result.outcome != str(row["outcome"]):
            raise IdempotencyIntegrityError(
                "persisted outcome does not match result payload"
            )
        if result.evaluated_at != row["evaluated_at"]:
            raise IdempotencyIntegrityError(
                "persisted evaluated_at does not match result payload"
            )
        if request.regulatory_decision_reference != result.regulatory_decision_reference:
            raise IdempotencyIntegrityError(
                "persisted request/result RegulatoryDecision references diverge"
            )
        if request.requirement_reference != result.requirement_reference:
            raise IdempotencyIntegrityError(
                "persisted request/result requirement references diverge"
            )
        assessment_ref = result.assessment_reference
        if assessment_ref.scope == "tenant" and assessment_ref.tenant_id != expected_tenant_id:
            raise IdempotencyIntegrityError(
                "persisted assessment reference does not match tenant scope"
            )
        return result

    @staticmethod
    def _canonical_json(
        value: DocumentEvidenceAssessmentRequest | DocumentEvidenceAssessmentResult,
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


__all__ = ["PostgresEvidenceAssessmentIdempotency"]

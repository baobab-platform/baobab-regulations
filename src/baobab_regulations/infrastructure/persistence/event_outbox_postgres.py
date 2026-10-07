"""PostgreSQL tenant-scoped canonical event outbox repository."""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime
from typing import Any, cast
from uuid import UUID

import asyncpg
from pydantic import ValidationError

from baobab_regulations.application.ports.outbox import (
    EventOutboxAuthorityUnavailableError,
    EventOutboxIntegrityError,
    EventOutboxRecord,
    OutboxStatus,
)
from baobab_regulations.contracts.events import (
    RequirementSatisfactionEvaluatedEvent,
    canonical_event_fingerprint,
)

_OUTBOX_COLUMNS = """
    outbox_id,
    event_id,
    assessment_id,
    tenant_id,
    event_type,
    source,
    subject,
    correlation_id,
    idempotency_key,
    envelope_fingerprint,
    envelope,
    status,
    attempt_count,
    next_attempt_at,
    lease_expires_at,
    published_at,
    last_error_code
"""


class PostgresEventOutboxRepository:
    """RLS-bound outbox repository with lease-based at-least-once delivery."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def get_by_assessment(
        self,
        *,
        tenant_id: str,
        assessment_id: str,
    ) -> EventOutboxRecord | None:
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await conn.fetchrow(
                    f"""
                    SELECT {_OUTBOX_COLUMNS}
                    FROM regulatory_event_outbox
                    WHERE tenant_id = $1 AND assessment_id = $2
                    """,
                    tenant_id,
                    assessment_id,
                )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise EventOutboxAuthorityUnavailableError(
                "canonical event outbox is unavailable"
            ) from exc
        return None if row is None else outbox_record_from_row(row)

    async def claim_due(
        self,
        *,
        tenant_id: str,
        now: datetime,
        limit: int,
        lease_expires_at: datetime,
    ) -> list[EventOutboxRecord]:
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                rows = await conn.fetch(
                    f"""
                    WITH due AS (
                        SELECT outbox_id AS candidate_id
                        FROM regulatory_event_outbox
                        WHERE tenant_id = $1
                          AND (
                              (
                                  status IN ('PENDING', 'RETRY')
                                  AND next_attempt_at <= $2
                              )
                              OR (
                                  status = 'PUBLISHING'
                                  AND lease_expires_at IS NOT NULL
                                  AND lease_expires_at <= $2
                              )
                          )
                        ORDER BY created_at, outbox_id
                        FOR UPDATE SKIP LOCKED
                        LIMIT $3
                    )
                    UPDATE regulatory_event_outbox AS outbox
                    SET
                        status = 'PUBLISHING',
                        attempt_count = outbox.attempt_count + 1,
                        lease_expires_at = $4,
                        updated_at = $2
                    FROM due
                    WHERE outbox.outbox_id = due.candidate_id
                    RETURNING {_OUTBOX_COLUMNS}
                    """,
                    tenant_id,
                    now,
                    limit,
                    lease_expires_at,
                )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise EventOutboxAuthorityUnavailableError(
                "canonical event outbox is unavailable"
            ) from exc
        return [outbox_record_from_row(row) for row in rows]

    async def mark_published(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        published_at: datetime,
    ) -> EventOutboxRecord:
        return await self._transition(
            tenant_id=tenant_id,
            outbox_id=outbox_id,
            sql="""
                status = 'PUBLISHED',
                published_at = $3,
                lease_expires_at = NULL,
                last_error_code = NULL,
                updated_at = $3
            """,
            values=(published_at,),
        )

    async def mark_retry(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        next_attempt_at: datetime,
        error_code: str,
    ) -> EventOutboxRecord:
        return await self._transition(
            tenant_id=tenant_id,
            outbox_id=outbox_id,
            sql="""
                status = 'RETRY',
                next_attempt_at = $3,
                lease_expires_at = NULL,
                last_error_code = $4,
                updated_at = now()
            """,
            values=(next_attempt_at, error_code[:100]),
        )

    async def mark_dead_letter(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        error_code: str,
    ) -> EventOutboxRecord:
        return await self._transition(
            tenant_id=tenant_id,
            outbox_id=outbox_id,
            sql="""
                status = 'DEAD_LETTER',
                lease_expires_at = NULL,
                last_error_code = $3,
                updated_at = now()
            """,
            values=(error_code[:100],),
        )

    async def _transition(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        sql: str,
        values: tuple[object, ...],
    ) -> EventOutboxRecord:
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                await self._bind_tenant(conn, tenant_id)
                row = await conn.fetchrow(
                    f"""
                    UPDATE regulatory_event_outbox
                    SET {sql}
                    WHERE tenant_id = $1
                      AND outbox_id = $2
                      AND status = 'PUBLISHING'
                    RETURNING {_OUTBOX_COLUMNS}
                    """,
                    tenant_id,
                    outbox_id,
                    *values,
                )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise EventOutboxAuthorityUnavailableError(
                "canonical event outbox is unavailable"
            ) from exc

        if row is None:
            raise EventOutboxIntegrityError(
                "outbox transition requires an actively leased PUBLISHING record"
            )
        return outbox_record_from_row(row)

    @staticmethod
    async def _bind_tenant(conn: Any, tenant_id: str) -> None:
        await conn.execute(
            "SELECT set_config('baobab.tenant_id', $1, true)",
            tenant_id,
        )


def outbox_record_from_row(row: Mapping[str, Any]) -> EventOutboxRecord:
    """Validate persisted envelope and redundant columns before dispatch."""
    try:
        event = RequirementSatisfactionEvaluatedEvent.model_validate(
            _json_object(row["envelope"])
        )
    except (TypeError, ValueError, ValidationError) as exc:
        raise EventOutboxIntegrityError("persisted canonical event envelope is invalid") from exc

    fingerprint = str(row["envelope_fingerprint"])
    if canonical_event_fingerprint(event) != fingerprint:
        raise EventOutboxIntegrityError(
            "persisted canonical event envelope does not match its fingerprint"
        )

    assessment_id = str(row["assessment_id"])
    if event.id != row["event_id"]:
        raise EventOutboxIntegrityError("persisted event id column diverges from envelope")
    if event.type != str(row["event_type"]):
        raise EventOutboxIntegrityError("persisted event type column diverges from envelope")
    if event.source != str(row["source"]):
        raise EventOutboxIntegrityError("persisted event source column diverges from envelope")
    if event.subject != str(row["subject"]):
        raise EventOutboxIntegrityError("persisted event subject column diverges from envelope")
    if event.tenantid != str(row["tenant_id"]):
        raise EventOutboxIntegrityError("persisted tenant column diverges from envelope")
    if event.correlationid != row["correlation_id"]:
        raise EventOutboxIntegrityError(
            "persisted correlation id column diverges from envelope"
        )
    if event.idempotencykey != str(row["idempotency_key"]):
        raise EventOutboxIntegrityError(
            "persisted idempotency key column diverges from envelope"
        )
    if event.data.result.assessment_reference.object_id != assessment_id:
        raise EventOutboxIntegrityError(
            "persisted assessment identity diverges from envelope"
        )

    status = str(row["status"])
    if status not in {"PENDING", "PUBLISHING", "PUBLISHED", "RETRY", "DEAD_LETTER"}:
        raise EventOutboxIntegrityError("persisted outbox status is invalid")
    attempt_count = int(row["attempt_count"])
    if attempt_count < 0:
        raise EventOutboxIntegrityError("persisted outbox attempt_count is invalid")

    return EventOutboxRecord(
        outbox_id=row["outbox_id"],
        event=event,
        assessment_id=assessment_id,
        tenant_id=str(row["tenant_id"]),
        envelope_fingerprint=fingerprint,
        status=cast(OutboxStatus, status),
        attempt_count=attempt_count,
        next_attempt_at=row["next_attempt_at"],
        lease_expires_at=row["lease_expires_at"],
        published_at=row["published_at"],
        last_error_code=(
            str(row["last_error_code"]) if row["last_error_code"] is not None else None
        ),
    )


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


__all__ = ["PostgresEventOutboxRepository", "outbox_record_from_row"]

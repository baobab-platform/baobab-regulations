"""Canonical event outbox and publication boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol
from uuid import UUID

from baobab_regulations.contracts.events import RequirementSatisfactionEvaluatedEvent

OutboxStatus = Literal["PENDING", "PUBLISHING", "PUBLISHED", "RETRY", "DEAD_LETTER"]


@dataclass(frozen=True, slots=True)
class EventOutboxRecord:
    outbox_id: UUID
    event: RequirementSatisfactionEvaluatedEvent
    assessment_id: str
    tenant_id: str
    envelope_fingerprint: str
    status: OutboxStatus
    attempt_count: int
    next_attempt_at: datetime
    lease_expires_at: datetime | None
    published_at: datetime | None
    last_error_code: str | None


class EventOutboxAuthorityUnavailableError(RuntimeError):
    """The durable outbox authority is unavailable."""


class EventOutboxIntegrityError(RuntimeError):
    """Persisted outbox state violates canonical event invariants."""


class CanonicalEventPublisherPort(Protocol):
    """Transport-neutral publisher for complete canonical event envelopes."""

    async def publish(self, event: RequirementSatisfactionEvaluatedEvent) -> None: ...


class EventOutboxRepositoryPort(Protocol):
    """Tenant-scoped leasing and delivery-state persistence."""

    async def claim_due(
        self,
        *,
        tenant_id: str,
        now: datetime,
        limit: int,
        lease_expires_at: datetime,
    ) -> list[EventOutboxRecord]: ...

    async def mark_published(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        published_at: datetime,
    ) -> EventOutboxRecord: ...

    async def mark_retry(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        next_attempt_at: datetime,
        error_code: str,
    ) -> EventOutboxRecord: ...

    async def mark_dead_letter(
        self,
        *,
        tenant_id: str,
        outbox_id: UUID,
        error_code: str,
    ) -> EventOutboxRecord: ...


__all__ = [
    "CanonicalEventPublisherPort",
    "EventOutboxAuthorityUnavailableError",
    "EventOutboxIntegrityError",
    "EventOutboxRecord",
    "EventOutboxRepositoryPort",
    "OutboxStatus",
]

"""At-least-once dispatcher for canonical Regulations outbox events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from baobab_regulations.application.ports.outbox import (
    CanonicalEventPublisherPort,
    EventOutboxRecord,
    EventOutboxRepositoryPort,
)


@dataclass(frozen=True, slots=True)
class OutboxRetryPolicy:
    max_attempts: int = 8
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 300.0
    lease_seconds: float = 60.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.initial_delay_seconds <= 0:
            raise ValueError("initial_delay_seconds must be positive")
        if self.max_delay_seconds < self.initial_delay_seconds:
            raise ValueError("max_delay_seconds must not be less than initial delay")
        if self.lease_seconds <= 0:
            raise ValueError("lease_seconds must be positive")


DEFAULT_OUTBOX_RETRY_POLICY = OutboxRetryPolicy()


class AtLeastOnceEventOutboxDispatcher:
    """Publish complete canonical envelopes with bounded retry and leases."""

    def __init__(
        self,
        *,
        repository: EventOutboxRepositoryPort,
        publisher: CanonicalEventPublisherPort,
        retry: OutboxRetryPolicy = DEFAULT_OUTBOX_RETRY_POLICY,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._retry = retry

    async def dispatch_due(
        self,
        *,
        tenant_id: str,
        now: datetime | None = None,
        limit: int = 100,
    ) -> list[EventOutboxRecord]:
        if not 1 <= limit <= 500:
            raise ValueError("outbox dispatch limit must be between 1 and 500")
        observed_at = now or datetime.now(UTC)
        if observed_at.utcoffset() is None:
            raise ValueError("outbox dispatch clock must be offset-aware")

        claimed = await self._repository.claim_due(
            tenant_id=tenant_id,
            now=observed_at,
            limit=limit,
            lease_expires_at=observed_at + timedelta(seconds=self._retry.lease_seconds),
        )

        completed: list[EventOutboxRecord] = []
        for record in claimed:
            try:
                await self._publisher.publish(record.event)
            except Exception as exc:
                error_code = self._error_code(exc)
                if record.attempt_count >= self._retry.max_attempts:
                    completed.append(
                        await self._repository.mark_dead_letter(
                            tenant_id=tenant_id,
                            outbox_id=record.outbox_id,
                            error_code=error_code,
                        )
                    )
                    continue

                delay = min(
                    self._retry.initial_delay_seconds
                    * (2 ** max(0, record.attempt_count - 1)),
                    self._retry.max_delay_seconds,
                )
                completed.append(
                    await self._repository.mark_retry(
                        tenant_id=tenant_id,
                        outbox_id=record.outbox_id,
                        next_attempt_at=observed_at + timedelta(seconds=delay),
                        error_code=error_code,
                    )
                )
                continue

            completed.append(
                await self._repository.mark_published(
                    tenant_id=tenant_id,
                    outbox_id=record.outbox_id,
                    published_at=observed_at,
                )
            )

        return completed

    @staticmethod
    def _error_code(exc: Exception) -> str:
        name = type(exc).__name__.upper()
        cleaned = "".join(char if char.isalnum() or char == "_" else "_" for char in name)
        return (cleaned or "PUBLISH_FAILED")[:100]


__all__ = [
    "AtLeastOnceEventOutboxDispatcher",
    "DEFAULT_OUTBOX_RETRY_POLICY",
    "OutboxRetryPolicy",
]

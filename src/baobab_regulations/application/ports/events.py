"""Invocation metadata carried into canonical event publication."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class EventPublicationMetadata:
    """Metadata that survives the synchronous command into the event envelope."""

    correlation_id: UUID
    causation_id: UUID | None = None
    traceparent: str | None = None
    tracestate: str | None = None


__all__ = ["EventPublicationMetadata"]

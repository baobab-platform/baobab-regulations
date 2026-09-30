"""Bitemporal intervals (ADR-REG-0015).

LEGAL / VALID TIME  — when the regulatory fact was legally effective.
KNOWLEDGE / SYSTEM TIME — when Baobab knew or recorded the fact.
"""

from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, model_validator


class BitemporalInterval(BaseModel):
    """Closed-open interval pair for valid time and knowledge time."""

    valid_from: datetime
    valid_to: datetime | None = None
    knowledge_from: datetime
    knowledge_to: datetime | None = None

    @model_validator(mode="after")
    def _check_order(self) -> Self:
        if self.valid_to is not None and self.valid_to <= self.valid_from:
            raise ValueError("valid_to must be after valid_from")
        if self.knowledge_to is not None and self.knowledge_to <= self.knowledge_from:
            raise ValueError("knowledge_to must be after knowledge_from")
        return self

    def is_valid_at(self, instant: datetime) -> bool:
        if instant < self.valid_from:
            return False
        if self.valid_to is not None and instant >= self.valid_to:
            return False
        return True

    def is_known_at(self, instant: datetime) -> bool:
        if instant < self.knowledge_from:
            return False
        if self.knowledge_to is not None and instant >= self.knowledge_to:
            return False
        return True


class LegalTimeContext(BaseModel):
    """Point-in-time evaluation axes for a regulatory assessment."""

    legal_time: datetime = Field(description="When the regulated activity is/was effective")
    knowledge_time: datetime = Field(description="As-of knowledge cut for Baobab's rule set")

"""Verified rule-set metadata for evaluation (ADR-REG-0016, 0018, 0022)."""

from datetime import datetime

from pydantic import BaseModel, Field

from baobab_regulations.domain.shared.enums import AssuranceState
from baobab_regulations.domain.shared.ids import RegulatoryId


class RuleSetRecord(BaseModel):
    """Resolved, versioned rule set ready for evaluation (not raw law text)."""

    rule_set_id: str
    corridor_profile: str
    assurance_state: AssuranceState = AssuranceState.CANDIDATE
    fingerprint: str
    legal_valid_from: datetime
    legal_valid_to: datetime | None = None
    knowledge_from: datetime
    knowledge_to: datetime | None = None
    derived_rule_ids: list[RegulatoryId] = Field(default_factory=list)
    notes: str | None = None

    def is_active_at(self, *, knowledge_time: datetime) -> bool:
        if self.assurance_state not in {
            AssuranceState.VERIFIED,
            AssuranceState.CERTIFIED,
        }:
            return False
        if knowledge_time < self.knowledge_from:
            return False
        if self.knowledge_to is not None and knowledge_time >= self.knowledge_to:
            return False
        return True

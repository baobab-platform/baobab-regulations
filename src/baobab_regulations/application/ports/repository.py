"""Persistence ports for regulatory knowledge and decisions."""

from datetime import datetime
from typing import Protocol

from baobab_regulations.domain.decisions.models import RegulatoryDecision
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.ids import RegulatoryId


class DecisionRepositoryPort(Protocol):
    async def save(self, decision: RegulatoryDecision) -> None:
        pass

    async def get(self, decision_id: RegulatoryId) -> RegulatoryDecision | None:
        pass


class RuleSetRepositoryPort(Protocol):
    """Resolved, verified rule sets ready for evaluation (not raw law text)."""

    async def get_active_rule_set_id(
        self,
        *,
        corridor_profile: str,
        knowledge_time: datetime,
    ) -> str | None:
        pass

    async def get(
        self,
        rule_set_id: str,
        *,
        tenant_id: str | None = None,
    ) -> RuleSetRecord | None:
        pass

    async def save(self, record: RuleSetRecord) -> None:
        pass

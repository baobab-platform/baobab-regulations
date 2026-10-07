"""In-memory repositories for offline tests and local scaffold runs."""

from datetime import datetime

from baobab_regulations.domain.decisions.models import RegulatoryDecision
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.ids import RegulatoryId


class InMemoryDecisionRepository:
    def __init__(self) -> None:
        self._store: dict[str, RegulatoryDecision] = {}

    async def save(self, decision: RegulatoryDecision) -> None:
        key = str(decision.decision_id)
        if key in self._store:
            raise ValueError(f"decisions are append-only; {key} already exists")
        self._store[key] = decision

    async def get(self, decision_id: RegulatoryId) -> RegulatoryDecision | None:
        return self._store.get(str(decision_id))


class InMemoryRuleSetRepository:
    def __init__(self) -> None:
        self._store: dict[str, RuleSetRecord] = {}

    async def save(self, record: RuleSetRecord) -> None:
        self._store[record.rule_set_id] = record

    async def get(
        self,
        rule_set_id: str,
        *,
        tenant_id: str | None = None,
    ) -> RuleSetRecord | None:
        record = self._store.get(rule_set_id)
        if record is None:
            return None
        if record.scope == "tenant" and record.tenant_id != tenant_id:
            return None
        return record

    async def get_active_rule_set_id(
        self,
        *,
        corridor_profile: str,
        knowledge_time: datetime,
    ) -> str | None:
        candidates = [
            r
            for r in self._store.values()
            if r.corridor_profile == corridor_profile and r.is_active_at(knowledge_time=knowledge_time)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda r: r.knowledge_from, reverse=True)
        return candidates[0].rule_set_id

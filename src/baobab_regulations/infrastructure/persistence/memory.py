"""In-memory repositories for offline tests and local scaffold runs."""

from baobab_regulations.domain.decisions.models import RegulatoryDecision
from baobab_regulations.domain.shared.ids import RegulatoryId


class InMemoryDecisionRepository:
    def __init__(self) -> None:
        self._store: dict[str, RegulatoryDecision] = {}

    async def save(self, decision: RegulatoryDecision) -> None:
        self._store[str(decision.decision_id)] = decision

    async def get(self, decision_id: RegulatoryId) -> RegulatoryDecision | None:
        return self._store.get(str(decision_id))

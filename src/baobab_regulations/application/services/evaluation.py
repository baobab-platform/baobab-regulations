"""Orchestrates regulatory evaluation (execution plane)."""

from typing import Any

from baobab_regulations.application.ports.evaluator import RegulatoryPolicyEvaluatorPort
from baobab_regulations.application.ports.repository import DecisionRepositoryPort
from baobab_regulations.domain.context.models import RegulatoryContext
from baobab_regulations.domain.decisions.models import RegulatoryDecision
from baobab_regulations.tenancy.context import require_tenant_context


class EvaluationService:
    """Thin application service over the evaluator port.

    Does not interpret law itself — delegates to a deterministic evaluator
    bound to a verified rule set.
    """

    def __init__(
        self,
        evaluator: RegulatoryPolicyEvaluatorPort,
        decisions: DecisionRepositoryPort,
    ) -> None:
        self._evaluator = evaluator
        self._decisions = decisions

    async def evaluate(
        self,
        *,
        context: RegulatoryContext,
        facts: dict[str, Any],
        rule_set_id: str,
    ) -> RegulatoryDecision:
        require_tenant_context(context.platform.tenant_id)
        decision = await self._evaluator.evaluate(
            context=context,
            facts=facts,
            rule_set_id=rule_set_id,
        )
        await self._decisions.save(decision)
        return decision

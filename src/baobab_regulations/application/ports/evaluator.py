"""Policy evaluator port — OPA is one implementation behind this interface."""

from typing import Any, Protocol

from baobab_regulations.domain.context.models import RegulatoryContext
from baobab_regulations.domain.decisions.models import RegulatoryDecision


class RegulatoryPolicyEvaluatorPort(Protocol):
    """Deterministic evaluation of a verified rule set against context + facts.

    Implementations must be side-effect free with respect to business state.
    OPA/Rego is the planned first runtime; BRIR remains the canonical IR
    (ADR-REG-0016).
    """

    async def evaluate(
        self,
        *,
        context: RegulatoryContext,
        facts: dict[str, Any],
        rule_set_id: str,
        enforcement_class_ceiling: str | None = None,
    ) -> RegulatoryDecision:
        """Return an explainable RegulatoryDecision for the given inputs."""
        ...

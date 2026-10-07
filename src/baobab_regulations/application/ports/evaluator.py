"""Provider-neutral deterministic regulatory policy evaluator boundary.

R-CAP-09 deliberately keeps OPA/Rego outside this port. Implementations receive
one canonical semantic input and return one canonical decision fragment or a
typed technical failure.
"""

from dataclasses import dataclass
from typing import Any, Protocol

from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
    RuleSetReference,
)
from baobab_regulations.domain.context.models import RegulatoryContext
from baobab_regulations.domain.decisions.models import RegulatoryDecision


@dataclass(frozen=True, slots=True)
class ResolvedRuleSet:
    """Exact verified rule-set and compiled execution binding."""

    reference: RuleSetReference
    fingerprint: str
    assurance_state: str
    compiler_id: str
    compiler_version: str
    target: str
    entrypoint: str
    artifact_fingerprint: str


@dataclass(frozen=True, slots=True)
class RegulatoryEvaluationInput:
    """Provider-neutral semantic input presented to an evaluator implementation."""

    request: DecisionEvaluateRequest
    tenant_id: str
    rule_set: ResolvedRuleSet
    input_fingerprint: str


@dataclass(frozen=True, slots=True)
class RegulatoryEvaluationResult:
    """Evaluator result before Regulations mints canonical decision identity."""

    outcome: str
    enforcement_class: str
    reasons: tuple[DecisionReason, ...]
    legal_basis_references: tuple[PinnedCrossEngineReference, ...]
    evidence_references: tuple[PinnedCrossEngineReference, ...]
    recommended_disposition: RecommendedDisposition | None


class EvaluatorUndefinedError(RuntimeError):
    """Evaluator query completed without a semantic result."""


class EvaluatorProtocolError(RuntimeError):
    """Evaluator response did not satisfy the expected deterministic protocol."""


class EvaluatorRuntimeError(RuntimeError):
    """Evaluator transport/runtime failed while executing the query."""


class EvaluatorNotReadyError(RuntimeError):
    """Evaluator is reachable but its configured policy/bundles are not ready."""


class LegacyRegulatoryPolicyEvaluatorPort(Protocol):
    """Pre-R-CAP-08 scaffold protocol retained only for the reference oracle."""

    async def evaluate(
        self,
        *,
        context: RegulatoryContext,
        facts: dict[str, Any],
        rule_set_id: str,
        enforcement_class_ceiling: str | None = None,
    ) -> RegulatoryDecision: ...


class RegulatoryPolicyEvaluatorPort(Protocol):
    """Side-effect-free evaluator for one resolved, verified rule set."""

    async def evaluate(
        self,
        evaluation: RegulatoryEvaluationInput,
    ) -> RegulatoryEvaluationResult: ...


__all__ = [
    "EvaluatorNotReadyError",
    "EvaluatorProtocolError",
    "EvaluatorRuntimeError",
    "EvaluatorUndefinedError",
    "LegacyRegulatoryPolicyEvaluatorPort",
    "RegulatoryEvaluationInput",
    "RegulatoryEvaluationResult",
    "RegulatoryPolicyEvaluatorPort",
    "ResolvedRuleSet",
]

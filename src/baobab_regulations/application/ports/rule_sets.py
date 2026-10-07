"""Exact Regulations rule-set authority boundary for R-CAP-09."""

from datetime import datetime
from typing import Protocol

from baobab_regulations.application.ports.evaluator import ResolvedRuleSet
from baobab_regulations.contracts.decision import RuleSetReference


class RuleSetNotFoundError(LookupError):
    """The exact pinned rule set is not known to Regulations."""


class RuleSetConflictError(RuntimeError):
    """The supplied pin/time/assurance conflicts with the governed rule set."""


class RuleSetAuthorityUnavailableError(RuntimeError):
    """The authoritative rule-set store is unavailable."""


class RuleSetIntegrityError(RuntimeError):
    """Persisted rule-set metadata violates production invariants."""


class RuleSetAuthorityPort(Protocol):
    async def resolve_exact(
        self,
        *,
        reference: RuleSetReference,
        legal_time: datetime,
        knowledge_time: datetime,
        requested_assurance: str,
        trusted_tenant_id: str,
    ) -> ResolvedRuleSet:
        pass


__all__ = [
    "RuleSetAuthorityPort",
    "RuleSetAuthorityUnavailableError",
    "RuleSetConflictError",
    "RuleSetIntegrityError",
    "RuleSetNotFoundError",
]

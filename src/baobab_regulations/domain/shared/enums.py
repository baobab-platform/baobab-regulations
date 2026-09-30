"""Normative enums for regulatory decisions and assurance (ADR-REG-0004, 0018)."""

from enum import StrEnum


class DecisionOutcome(StrEnum):
    """Canonical regulatory decision family (ADR-REG-0018).

    Richer than true/false; deliberately separated from operational enforcement.
    """

    SATISFIED = "SATISFIED"
    SATISFIED_WITH_REQUIREMENTS = "SATISFIED_WITH_REQUIREMENTS"
    UNSATISFIED = "UNSATISFIED"
    PROHIBITED = "PROHIBITED"
    INDETERMINATE = "INDETERMINATE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EnforcementClass(StrEnum):
    """Progressively stronger decision classes (ADR-REG-0004).

    Higher consequence requires stronger evidence, verification, and governance.
    Generative AI output does not independently qualify a rule for E3/E4.
    """

    E0_INFORMATIONAL = "E0"
    E1_ADVISORY = "E1"
    E2_REVIEW_GATE = "E2"
    E3_CONDITIONAL_DETERMINISTIC = "E3"
    E4_HIGH_ASSURANCE = "E4"


class AssuranceState(StrEnum):
    """How far regulatory knowledge has progressed through governance."""

    CANDIDATE = "CANDIDATE"
    UNDER_REVIEW = "UNDER_REVIEW"
    VERIFIED = "VERIFIED"
    CERTIFIED = "CERTIFIED"
    DEPRECATED = "DEPRECATED"
    REJECTED = "REJECTED"

"""Explainable regulatory decisions (ADR-REG-0018, ADR-REG-0020)."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from baobab_regulations.domain.shared.enums import DecisionOutcome, EnforcementClass
from baobab_regulations.domain.shared.ids import RegulatoryId


class DecisionReason(BaseModel):
    """One cited reason supporting or explaining a decision."""

    code: str
    message: str
    legal_basis_refs: list[str] = Field(default_factory=list)
    rule_version_ids: list[RegulatoryId] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class RecommendedDisposition(BaseModel):
    """Suggested operational action — enforcement remains with the owning PEP."""

    disposition: str  # e.g. HOLD, ALLOW, REQUIRE_DOCUMENT, ESCALATE
    rationale: str
    missing_requirements: list[str] = Field(default_factory=list)


class RegulatoryDecision(BaseModel):
    """Canonical regulatory decision produced by the evaluation engine.

    Outcome is deliberately separated from operational enforcement
    (ADR-REG-0019). Domain PEPs (e.g. baobab-trade) own state transitions.
    """

    decision_id: RegulatoryId
    assessment_id: RegulatoryId
    outcome: DecisionOutcome
    enforcement_class: EnforcementClass
    reasons: list[DecisionReason] = Field(default_factory=list)
    recommended_disposition: RecommendedDisposition | None = None
    explanation: str = ""
    rule_set_fingerprint: str = ""
    evaluated_at: datetime
    legal_time: datetime
    knowledge_time: datetime
    provenance: dict[str, Any] = Field(default_factory=dict)
    replay_key: str = ""

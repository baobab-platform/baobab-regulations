"""Verified rule-set metadata for evaluation (ADR-REG-0016, 0018, 0022)."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

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
    scope: Literal["platform", "tenant"] = "platform"
    tenant_id: str | None = None
    brir_payload: dict[str, Any] | None = None
    compiler_id: str | None = None
    compiler_version: str | None = None
    compiled_target: str | None = None
    compiled_entrypoint: str | None = None
    compiled_artifact_fingerprint: str | None = None
    derived_rule_ids: list[RegulatoryId] = Field(default_factory=list)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_scope(self) -> RuleSetRecord:
        if self.scope == "tenant":
            if self.tenant_id is None:
                raise ValueError("tenant-scoped rule sets require tenant_id")
        elif self.tenant_id is not None:
            raise ValueError("platform rule sets must not carry tenant_id")
        return self

    def is_active_at(self, *, knowledge_time: datetime) -> bool:
        """Compatibility helper for knowledge-only lookups."""
        if self.assurance_state not in {
            AssuranceState.VERIFIED,
            AssuranceState.CERTIFIED,
        }:
            return False
        if knowledge_time < self.knowledge_from:
            return False
        return self.knowledge_to is None or knowledge_time < self.knowledge_to

    def is_valid_for(
        self,
        *,
        legal_time: datetime,
        knowledge_time: datetime,
    ) -> bool:
        """Exact bitemporal validity required by R-CAP-09."""
        if not self.is_active_at(knowledge_time=knowledge_time):
            return False
        if legal_time < self.legal_valid_from:
            return False
        return self.legal_valid_to is None or legal_time < self.legal_valid_to

"""R-CAP-08 runtime adapters for the canonical Shared decision contract.

Shared remains the wire-contract authority. These models execute
contracts/regulatory-decision/v1 without introducing evaluator implementation
semantics. R-CAP-09 owns production evaluation.
"""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from baobab_regulations.contracts.rtd06 import (
    CrossEngineObjectReference,
    PinnedRegulationsReference,
)

HashSha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
ReasonCode = Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$")]
FactCode = Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_.-]{1,127}$")]
ActivityCode = Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_.-]{1,127}$")]
ReplayKey = Annotated[
    str,
    Field(
        min_length=16,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    ),
]


class PinnedCrossEngineReference(CrossEngineObjectReference):
    """Generic pinned ADR-SHARED-021 reference used for subjects/evidence."""

    reference_mode: Literal["IDENTITY_PINNED", "VERSION_PINNED"]


class RegulatoryDecisionReference(PinnedRegulationsReference):
    object_type: Literal["REGULATORY_DECISION"]


class RegulatoryAssessmentReference(PinnedRegulationsReference):
    object_type: Literal["REGULATORY_ASSESSMENT"]


class RuleSetReference(PinnedRegulationsReference):
    object_type: Literal["REGULATORY_RULE_SET"]


class RuleVersionReference(PinnedRegulationsReference):
    object_type: Literal["REGULATORY_RULE_VERSION"]


class RegulatoryFact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fact_code: FactCode
    value: str | float | bool
    unit: Annotated[str | None, Field(max_length=64)] = None
    currency: Annotated[str | None, Field(pattern=r"^[A-Z]{3}$")] = None
    observed_at: datetime
    source_reference: PinnedCrossEngineReference | None = None

    @field_validator("value")
    @classmethod
    def constrain_string_value(cls, value: str | float | bool) -> str | float | bool:
        if isinstance(value, str) and len(value) > 2048:
            raise ValueError("regulatory fact string values are limited to 2048 characters")
        return value

    @field_validator("observed_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("decision contract date-time values must include a UTC offset")
        return value


class DecisionReason(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: ReasonCode
    message: Annotated[str, Field(min_length=1, max_length=2048)]
    legal_basis_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(max_length=64),
    ]
    rule_version_references: Annotated[list[RuleVersionReference], Field(max_length=128)]
    evidence_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(max_length=128),
    ]

    @field_validator(
        "legal_basis_references",
        "rule_version_references",
        "evidence_references",
    )
    @classmethod
    def require_unique_references(
        cls,
        value: list[PinnedCrossEngineReference],
    ) -> list[PinnedCrossEngineReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("decision reference arrays declared uniqueItems must be unique")
        return value


class RecommendedDisposition(BaseModel):
    """Non-enforcing recommendation to the owning operational PEP."""

    model_config = ConfigDict(extra="forbid")

    disposition_code: Annotated[
        str,
        Field(pattern=r"^[A-Z][A-Z0-9_]{1,63}$"),
    ]
    rationale: Annotated[str, Field(min_length=1, max_length=2048)]
    missing_requirement_references: Annotated[
        list[PinnedRegulationsReference],
        Field(max_length=128),
    ]

    @field_validator("missing_requirement_references")
    @classmethod
    def require_unique_references(
        cls,
        value: list[PinnedRegulationsReference],
    ) -> list[PinnedRegulationsReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("missing requirement references must be unique")
        allowed = {
            "DOCUMENT_REQUIREMENT",
            "PERMIT_REQUIREMENT",
            "EVIDENCE_REQUIREMENT",
        }
        if any(item.object_type not in allowed for item in value):
            raise ValueError("missing requirement references must name canonical requirements")
        return value


class DecisionProvenance(BaseModel):
    """Provider-neutral decision reproducibility metadata."""

    model_config = ConfigDict(extra="forbid")

    contract_major: Literal[1]
    input_fingerprint: HashSha256
    rule_set_reference: RuleSetReference
    rule_set_fingerprint: HashSha256
    evaluation_profile: Literal[
        "ADVISORY",
        "STANDARD",
        "HIGH_ASSURANCE",
        "HISTORICAL_REPLAY",
        "FUTURE_SIMULATION",
        "SHADOW",
    ]


class ReplayIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    replay_key: ReplayKey
    input_fingerprint: HashSha256
    rule_set_fingerprint: HashSha256


class DecisionEvaluateRequest(BaseModel):
    """Shared R-CAP-08 decisionEvaluateRequest."""

    model_config = ConfigDict(extra="forbid")

    context_id: UUID
    question: Literal[
        "MAY_TRANSACTION_PROCEED",
        "WHAT_OBLIGATIONS_APPLY",
        "WHAT_REQUIREMENTS_REMAIN",
        "WHAT_DOCUMENTS_ARE_REQUIRED",
        "IS_REQUIREMENT_SATISFIED",
        "IS_ACTION_PROHIBITED",
        "IS_EXPLICIT_PERMISSION_AVAILABLE",
        "WHAT_DUTY_OR_AMOUNT_APPLIES",
        "WHAT_REGULATORY_GAPS_EXIST",
        "WHAT_CHANGED",
        "WHAT_WOULD_APPLY_AT_FUTURE_TIME",
    ]
    assessment_purpose: Literal[
        "TRANSACTION_DECISION",
        "COMPLIANCE_REVIEW",
        "LEGAL_REVIEW",
        "AUDIT",
        "HISTORICAL_REPLAY",
        "FUTURE_SIMULATION",
    ]
    decision_stage: Literal[
        "PLANNING",
        "QUOTATION",
        "ORDER",
        "PRE_SHIPMENT",
        "EXPORT",
        "TRANSIT",
        "IMPORT",
        "CLEARANCE",
        "DELIVERY",
        "POST_TRANSACTION",
        "PERIODIC_COMPLIANCE",
    ] | None = None
    subject_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(min_length=1, max_length=64),
    ]
    regulated_activities: Annotated[
        list[ActivityCode],
        Field(min_length=1, max_length=32),
    ]
    facts: Annotated[list[RegulatoryFact], Field(max_length=512)]
    evidence_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(max_length=128),
    ]
    rule_set_reference: RuleSetReference
    legal_time: datetime
    knowledge_time: datetime
    evaluation_profile: Literal[
        "ADVISORY",
        "STANDARD",
        "HIGH_ASSURANCE",
        "HISTORICAL_REPLAY",
        "FUTURE_SIMULATION",
        "SHADOW",
    ]
    requested_assurance: Literal["STANDARD", "HIGH_ASSURANCE"]
    requested_enforcement_class_ceiling: Literal["E0", "E1", "E2", "E3", "E4"]
    replay_key: ReplayKey

    @field_validator("legal_time", "knowledge_time")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("decision contract date-time values must include a UTC offset")
        return value

    @field_validator(
        "subject_references",
        "evidence_references",
    )
    @classmethod
    def require_unique_references(
        cls,
        value: list[PinnedCrossEngineReference],
    ) -> list[PinnedCrossEngineReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("decision reference arrays declared uniqueItems must be unique")
        return value

    @field_validator("regulated_activities")
    @classmethod
    def require_unique_activities(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("regulated_activities must be unique")
        return value


class DecisionEvaluateResponse(BaseModel):
    """Shared R-CAP-08 Regulations-owned decision response."""

    model_config = ConfigDict(extra="forbid")

    decision_reference: RegulatoryDecisionReference
    assessment_reference: RegulatoryAssessmentReference
    outcome: Literal[
        "SATISFIED",
        "SATISFIED_WITH_REQUIREMENTS",
        "UNSATISFIED",
        "PROHIBITED",
        "INDETERMINATE",
        "NOT_APPLICABLE",
    ]
    enforcement_class: Literal["E0", "E1", "E2", "E3", "E4"]
    reasons: Annotated[list[DecisionReason], Field(max_length=256)]
    legal_basis_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(max_length=256),
    ]
    evidence_references: Annotated[
        list[PinnedCrossEngineReference],
        Field(max_length=256),
    ]
    recommended_disposition: RecommendedDisposition | None
    rule_set_reference: RuleSetReference
    rule_set_fingerprint: HashSha256
    evaluated_at: datetime
    legal_time: datetime
    knowledge_time: datetime
    provenance: DecisionProvenance
    replay_identity: ReplayIdentity

    @field_validator("evaluated_at", "legal_time", "knowledge_time")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("decision contract date-time values must include a UTC offset")
        return value

    @field_validator("legal_basis_references", "evidence_references")
    @classmethod
    def require_unique_references(
        cls,
        value: list[PinnedCrossEngineReference],
    ) -> list[PinnedCrossEngineReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("decision reference arrays declared uniqueItems must be unique")
        return value


__all__ = [
    "DecisionEvaluateRequest",
    "DecisionEvaluateResponse",
    "DecisionProvenance",
    "DecisionReason",
    "PinnedCrossEngineReference",
    "RecommendedDisposition",
    "RegulatoryAssessmentReference",
    "RegulatoryDecisionReference",
    "RegulatoryFact",
    "ReplayIdentity",
    "RuleSetReference",
    "RuleVersionReference",
]

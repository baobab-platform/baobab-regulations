"""Untrusted regulatory knowledge candidates (ADR-REG-0013, -0022).

A candidate is a proposed interpretation of a source artefact, not a law,
verified requirement, published RuleVersion, or RegulatoryDecision. In
particular, APPROVED_FOR_PROMOTION never changes runtime rule-set authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from baobab_regulations.domain.shared.ids import RegulatoryId


class CandidateKind(StrEnum):
    RULE = "RULE"
    REQUIREMENT = "REQUIREMENT"
    INTERPRETATION = "INTERPRETATION"
    PROVISION = "PROVISION"


class ExtractionMethod(StrEnum):
    DETERMINISTIC = "DETERMINISTIC"
    AI_ASSISTED = "AI_ASSISTED"
    MANUAL = "MANUAL"


class CandidateState(StrEnum):
    NEEDS_REVIEW = "NEEDS_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED_FOR_PROMOTION = "APPROVED_FOR_PROMOTION"
    REJECTED = "REJECTED"


class ReviewAction(StrEnum):
    APPROVE = "APPROVE"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    REJECT = "REJECT"
    ABSTAIN = "ABSTAIN"


class RegulatoryCandidate(BaseModel):
    """Immutable submission envelope, independent of later review status.

    Identity, source pin, extraction lineage and proposed meaning are pinned by
    one deterministic fingerprint. The repository additionally deep-copies the
    nested JSON payload to protect this envelope from caller mutation.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    candidate_id: RegulatoryId
    candidate_version: Annotated[int, Field(ge=1)]
    kind: CandidateKind
    source_id: RegulatoryId
    artefact_id: RegulatoryId
    artefact_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    source_locator: Annotated[str, Field(min_length=1, max_length=512)]
    proposed_payload: dict[str, JsonValue]
    extraction_method: ExtractionMethod
    producer_principal_id: Annotated[str, Field(min_length=1, max_length=160)]
    proposed_at: datetime
    scope: Literal["platform", "tenant"]
    tenant_id: str | None = None
    model_ref: str | None = None
    prompt_version: str | None = None

    @field_validator("proposed_at")
    @classmethod
    def require_offset(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("candidate timestamp must have a timezone offset")
        return value

    @model_validator(mode="after")
    def validate_candidate(self) -> Self:
        if not self.proposed_payload:
            raise ValueError("candidate meaning cannot be empty")
        if not all(str(value).strip() for value in (
            self.candidate_id, self.source_id, self.artefact_id,
            self.producer_principal_id, self.source_locator,
        )):
            raise ValueError("candidate identity and source provenance cannot be blank")
        if self.scope == "platform" and self.tenant_id is not None:
            raise ValueError("platform candidate must not carry tenant identity")
        if self.scope == "tenant" and (
            not self.tenant_id or re.fullmatch(r"tn_[a-z0-9]+", self.tenant_id) is None
        ):
            raise ValueError("tenant candidate requires a tenant reference")
        if self.extraction_method is ExtractionMethod.AI_ASSISTED and not (
            self.model_ref and self.prompt_version
        ):
            raise ValueError("AI candidates require model and prompt lineage")
        if self.extraction_method is not ExtractionMethod.AI_ASSISTED and (
            self.model_ref is not None or self.prompt_version is not None
        ):
            raise ValueError("non-AI candidates must not impersonate AI lineage")
        return self

    def fingerprint(self) -> str:
        body = json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


class CandidateReviewDecision(BaseModel):
    """Attributable, pin-bound checker decision; never an IAM grant."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    candidate_id: RegulatoryId
    candidate_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    reviewer_principal_id: Annotated[str, Field(min_length=1, max_length=160)]
    competence_profile_ref: Annotated[str, Field(min_length=1, max_length=160)]
    action: ReviewAction
    reason_codes: tuple[str, ...]
    supporting_evidence_refs: tuple[str, ...] = ()
    decided_at: datetime

    @field_validator("decided_at")
    @classmethod
    def require_offset(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("review timestamp must have a timezone offset")
        return value

    @model_validator(mode="after")
    def require_rationale(self) -> Self:
        if not self.reason_codes or any(not s.strip() for s in self.reason_codes):
            raise ValueError("review requires nonempty reason codes")
        if self.action is ReviewAction.APPROVE and (
            not self.supporting_evidence_refs
            or any(not s.strip() for s in self.supporting_evidence_refs)
        ):
            raise ValueError("approval requires independent supporting evidence")
        return self


class CandidateReviewRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    candidate: RegulatoryCandidate
    candidate_fingerprint: str
    state: CandidateState = CandidateState.NEEDS_REVIEW
    revision: Annotated[int, Field(ge=1)] = 1
    decisions: tuple[CandidateReviewDecision, ...] = ()


__all__ = [
    "CandidateKind", "CandidateReviewDecision", "CandidateReviewRecord",
    "CandidateState", "ExtractionMethod", "RegulatoryCandidate", "ReviewAction",
]

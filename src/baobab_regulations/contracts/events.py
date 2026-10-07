"""Canonical Shared RTD-08 Regulations event adapters.

Shared remains the wire-contract authority. These models mirror only the active
requirement-satisfaction event surface needed by R-CAP-06.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from typing import Annotated, Final, Literal
from uuid import NAMESPACE_URL, UUID, uuid5

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from baobab_regulations.contracts.rtd06 import (
    CrossEngineObjectReference,
    DocumentEvidenceAssessmentResult,
    PinnedRegulationsReference,
)

EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED: Final = (
    "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1"
)
REGULATIONS_EVENT_SOURCE: Final = "urn:baobab-platform:service:baobab-regulations"
REQUIREMENT_SATISFACTION_DATASCHEMA: Final = (
    "https://contracts.baobab-platform.com/regulatory-document-exchange/v1/"
    "events.schema.json#/$defs/requirementSatisfactionEvaluatedEventData"
)

_TRACEPARENT_RE = re.compile(
    r"^00-(?!00000000000000000000000000000000)[0-9a-f]{32}-"
    r"(?!0000000000000000)[0-9a-f]{16}-[0-9a-f]{2}$"
)
_IDEMPOTENCY_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


class RequirementSatisfactionEvaluatedData(BaseModel):
    """Exact RTD-08 payload owned by Regulations."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: Annotated[
        str,
        Field(min_length=6, max_length=63, pattern=r"^tn_[a-z0-9]+$"),
    ]
    result: DocumentEvidenceAssessmentResult

    @model_validator(mode="after")
    def require_tenant_consistency(self) -> RequirementSatisfactionEvaluatedData:
        tenant_id = self.tenant_id
        references: list[
            PinnedRegulationsReference | CrossEngineObjectReference
        ] = [
            self.result.assessment_reference,
            self.result.regulatory_decision_reference,
            self.result.requirement_reference,
            *self.result.accepted_document_version_references,
            *(item.document_version_reference for item in self.result.rejected_evidence),
        ]
        if self.result.resulting_regulatory_decision_reference is not None:
            references.append(self.result.resulting_regulatory_decision_reference)
        for reference in references:
            if reference.scope == "tenant" and reference.tenant_id != tenant_id:
                raise ValueError("nested tenant-scoped event references must match tenant_id")
        return self


class RequirementSatisfactionEvaluatedEvent(BaseModel):
    """Canonical Shared CloudEvents envelope for the active RTD-08 event."""

    model_config = ConfigDict(extra="forbid")

    specversion: Literal["1.0"] = "1.0"
    id: UUID
    type: Literal[
        "com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1"
    ] = EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED
    source: Literal["urn:baobab-platform:service:baobab-regulations"] = (
        REGULATIONS_EVENT_SOURCE
    )
    subject: Annotated[str, Field(min_length=1, max_length=255)]
    time: datetime
    datacontenttype: Literal["application/json"] = "application/json"
    dataschema: Literal[
        "https://contracts.baobab-platform.com/regulatory-document-exchange/v1/"
        "events.schema.json#/$defs/requirementSatisfactionEvaluatedEventData"
    ] = REQUIREMENT_SATISFACTION_DATASCHEMA
    baobabscope: Literal["tenant"] = "tenant"
    correlationid: UUID
    causationid: UUID | None = None
    tenantid: Annotated[
        str,
        Field(min_length=6, max_length=63, pattern=r"^tn_[a-z0-9]+$"),
    ]
    idempotencykey: Annotated[str, Field(min_length=16, max_length=128)]
    traceparent: str | None = None
    tracestate: Annotated[str | None, Field(min_length=1, max_length=512)] = None
    data: RequirementSatisfactionEvaluatedData

    @field_validator("time")
    @classmethod
    def require_offset_aware_time(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("CloudEvent time must include a UTC offset")
        return value

    @field_validator("idempotencykey")
    @classmethod
    def require_idempotency_key_grammar(cls, value: str) -> str:
        if _IDEMPOTENCY_KEY_RE.fullmatch(value) is None:
            raise ValueError("event idempotencykey violates the Shared event envelope")
        return value

    @field_validator("traceparent")
    @classmethod
    def require_traceparent(cls, value: str | None) -> str | None:
        if value is not None and _TRACEPARENT_RE.fullmatch(value) is None:
            raise ValueError("traceparent violates the Shared event envelope")
        return value

    @field_validator("tracestate")
    @classmethod
    def require_ascii_tracestate(cls, value: str | None) -> str | None:
        if value is not None and any(ord(char) < 32 or ord(char) > 126 for char in value):
            raise ValueError("tracestate must contain printable ASCII only")
        return value

    @model_validator(mode="after")
    def require_envelope_consistency(self) -> RequirementSatisfactionEvaluatedEvent:
        result = self.data.result
        if self.tenantid != self.data.tenant_id:
            raise ValueError("CloudEvent tenantid must equal payload tenant_id")
        if result.assessment_reference.tenant_id != self.tenantid:
            raise ValueError("assessment tenant must equal CloudEvent tenantid")
        expected_subject = (
            f"regulatory-evidence-assessment:{result.assessment_reference.object_id}"
        )
        if self.subject != expected_subject:
            raise ValueError("CloudEvent subject must identify the assessment")
        if self.time != result.evaluated_at:
            raise ValueError("CloudEvent time must equal the assessment business occurrence")
        expected_id = requirement_satisfaction_event_id(
            assessment_id=result.assessment_reference.object_id
        )
        if self.id != expected_id:
            raise ValueError("CloudEvent id must be stable for the assessment occurrence")
        return self


def requirement_satisfaction_event_id(*, assessment_id: str) -> UUID:
    """Stable occurrence ID; delivery retries retain the same (source, id)."""
    return uuid5(
        NAMESPACE_URL,
        (
            f"{REGULATIONS_EVENT_SOURCE}|"
            f"{EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED}|{assessment_id}"
        ),
    )


def build_requirement_satisfaction_evaluated_event(
    *,
    tenant_id: str,
    idempotency_key: str,
    result: DocumentEvidenceAssessmentResult,
    correlation_id: UUID,
    causation_id: UUID | None = None,
    traceparent: str | None = None,
    tracestate: str | None = None,
) -> RequirementSatisfactionEvaluatedEvent:
    """Build one canonical event occurrence from committed assessment semantics."""
    assessment_id = result.assessment_reference.object_id
    return RequirementSatisfactionEvaluatedEvent(
        id=requirement_satisfaction_event_id(assessment_id=assessment_id),
        subject=f"regulatory-evidence-assessment:{assessment_id}",
        time=result.evaluated_at,
        correlationid=correlation_id,
        causationid=causation_id,
        tenantid=tenant_id,
        idempotencykey=idempotency_key,
        traceparent=traceparent,
        tracestate=tracestate,
        data=RequirementSatisfactionEvaluatedData(
            tenant_id=tenant_id,
            result=result,
        ),
    )


def canonical_event_json(event: RequirementSatisfactionEvaluatedEvent) -> str:
    """Canonical JSON representation used for durable envelope integrity."""
    return json.dumps(
        event.model_dump(mode="json", exclude_none=True),
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_event_fingerprint(event: RequirementSatisfactionEvaluatedEvent) -> str:
    return hashlib.sha256(canonical_event_json(event).encode("utf-8")).hexdigest()


__all__ = [
    "EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED",
    "REGULATIONS_EVENT_SOURCE",
    "REQUIREMENT_SATISFACTION_DATASCHEMA",
    "RequirementSatisfactionEvaluatedData",
    "RequirementSatisfactionEvaluatedEvent",
    "build_requirement_satisfaction_evaluated_event",
    "canonical_event_fingerprint",
    "canonical_event_json",
    "requirement_satisfaction_event_id",
]

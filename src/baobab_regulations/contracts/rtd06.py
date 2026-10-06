"""RTD-06 wire models for regulations.requirement.resolve.

Shared remains the canonical schema authority.  These Pydantic models are a
runtime adapter for the exact fields and constraints used by:

    baobab-platform/shared
    contracts/regulatory-document-exchange/v1/domain.schema.json

They deliberately model only the R-CAP-01 request/response surface.  They are
not a second canonical contract and they do not broaden Regulations authority.
"""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ObjectId = Annotated[
    str,
    Field(
        min_length=1,
        max_length=160,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    ),
]
TenantId = Annotated[
    str,
    Field(
        min_length=6,
        max_length=63,
        pattern=r"^tn_[a-z0-9]+$",
    ),
]
RequirementCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$"),
]
PurposeCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$"),
]
EffectCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$"),
]
DocumentTypeCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_]{1,63}$"),
]
IssuerRoleCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_]{1,63}$"),
]
DataElementCode = Annotated[
    str,
    Field(pattern=r"^[A-Z][A-Z0-9_.-]{1,127}$"),
]


class ObjectVersion(BaseModel):
    """Opaque owner-defined historical version from RTD-05."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["VERSION", "REVISION", "SEQUENCE", "ETAG", "CONTENT_HASH", "OTHER"]
    value: Annotated[str, Field(min_length=1, max_length=256)]


class PinnedRegulationsReference(BaseModel):
    """Common RTD-05 fields for a pinned Regulations-owned reference."""

    model_config = ConfigDict(extra="forbid")

    owner_engine_id: Literal["baobab-regulations"]
    object_type: str
    object_id: ObjectId
    reference_mode: Literal["IDENTITY_PINNED", "VERSION_PINNED"]
    object_version: ObjectVersion | None = None
    scope: Literal["platform", "tenant"]
    tenant_id: TenantId | None = None

    @model_validator(mode="after")
    def validate_scope_and_pinning(self) -> PinnedRegulationsReference:
        if self.scope == "tenant":
            if self.tenant_id is None:
                raise ValueError("tenant-scoped references require tenant_id")
        elif self.tenant_id is not None:
            raise ValueError("platform-scoped references must not carry tenant_id")

        if self.reference_mode == "VERSION_PINNED":
            if self.object_version is None:
                raise ValueError("VERSION_PINNED references require object_version")
        elif self.object_version is not None:
            raise ValueError("IDENTITY_PINNED references must not carry object_version")
        return self


class RegulatoryRequirementReference(PinnedRegulationsReference):
    """Pinned DOCUMENT/PERMIT/EVIDENCE requirement owned by Regulations."""

    object_type: Literal[
        "DOCUMENT_REQUIREMENT",
        "PERMIT_REQUIREMENT",
        "EVIDENCE_REQUIREMENT",
    ]


class RegulatoryDecisionReference(PinnedRegulationsReference):
    """Pinned Regulations-owned RegulatoryDecision reference."""

    object_type: Literal["REGULATORY_DECISION"]


class RegulatoryDocumentRequirementProjection(BaseModel):
    """Exact RTD-06 executable read projection of one requirement."""

    model_config = ConfigDict(extra="forbid")

    requirement_reference: RegulatoryRequirementReference
    regulatory_decision_reference: RegulatoryDecisionReference
    requirement_kind: Literal["DOCUMENT", "PERMIT", "EVIDENCE"]
    requirement_code: RequirementCode
    purpose_code: PurposeCode
    acceptable_document_types: Annotated[list[DocumentTypeCode], Field(max_length=64)]
    required_issuer_roles: Annotated[list[IssuerRoleCode], Field(max_length=32)]
    required_data_elements: Annotated[list[DataElementCode], Field(max_length=128)]
    unsatisfied_effect_code: EffectCode
    effective_from: datetime
    effective_to: datetime | None = None
    determined_at: datetime

    @field_validator(
        "acceptable_document_types",
        "required_issuer_roles",
        "required_data_elements",
    )
    @classmethod
    def require_unique_items(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("RTD-06 arrays declared uniqueItems must not contain duplicates")
        return value

    @field_validator("effective_from", "effective_to", "determined_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value

    @model_validator(mode="after")
    def require_kind_reference_consistency(self) -> RegulatoryDocumentRequirementProjection:
        expected_object_type = {
            "DOCUMENT": "DOCUMENT_REQUIREMENT",
            "PERMIT": "PERMIT_REQUIREMENT",
            "EVIDENCE": "EVIDENCE_REQUIREMENT",
        }[self.requirement_kind]
        if self.requirement_reference.object_type != expected_object_type:
            raise ValueError(
                "requirement_kind must match the requirement_reference object_type"
            )
        return self


class RequirementResolveRequest(BaseModel):
    """Shared RTD-06 requirementResolveRequest."""

    model_config = ConfigDict(extra="forbid")

    context_id: UUID
    requirement_reference: RegulatoryRequirementReference


class RequirementResolveResponse(BaseModel):
    """Shared RTD-06 requirementResolveResponse."""

    model_config = ConfigDict(extra="forbid")

    requirement: RegulatoryDocumentRequirementProjection


__all__ = [
    "ObjectVersion",
    "PinnedRegulationsReference",
    "RegulatoryDecisionReference",
    "RegulatoryDocumentRequirementProjection",
    "RegulatoryRequirementReference",
    "RequirementResolveRequest",
    "RequirementResolveResponse",
]

"""RTD-06 runtime adapters for the first Regulations capability tranche.

Shared remains the canonical schema authority. These Pydantic models mirror the
bounded request/response projections used by R-CAP-01 requirement.resolve and
R-CAP-02 evidence.assess. They are runtime adapters, not a fork of the Shared
JSON Schemas and not a broader regulatory decision contract.
"""

from datetime import datetime
from typing import Annotated, Any, Literal, cast
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer,
    model_validator,
)

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

    @model_serializer(mode="wrap")
    def serialize_reference(
        self,
        handler: SerializerFunctionWrapHandler,
    ) -> dict[str, object]:
        """Honor RTD-05 conditional field presence on the wire."""
        raw: Any = handler(self)
        if not isinstance(raw, dict):
            raise TypeError("reference serializer must produce an object")
        data = cast(dict[str, object], raw)
        if self.object_version is None:
            data.pop("object_version", None)
        if self.tenant_id is None:
            data.pop("tenant_id", None)
        return data


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


class CrossEngineObjectReference(BaseModel):
    """RTD-05 portable reference used inside Trade Docs fact bundles."""

    model_config = ConfigDict(extra="forbid")

    owner_engine_id: Annotated[
        str,
        Field(
            min_length=3,
            max_length=63,
            pattern=r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$",
        ),
    ]
    object_type: Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_]{1,95}$")]
    object_id: ObjectId
    reference_mode: Literal["CURRENT", "IDENTITY_PINNED", "VERSION_PINNED"]
    object_version: ObjectVersion | None = None
    scope: Literal["platform", "tenant"]
    tenant_id: TenantId | None = None

    @model_validator(mode="after")
    def validate_scope_and_pinning(self) -> CrossEngineObjectReference:
        if self.scope == "tenant":
            if self.tenant_id is None:
                raise ValueError("tenant-scoped references require tenant_id")
        elif self.tenant_id is not None:
            raise ValueError("platform-scoped references must not carry tenant_id")

        if self.reference_mode == "VERSION_PINNED":
            if self.object_version is None:
                raise ValueError("VERSION_PINNED references require object_version")
        elif self.object_version is not None:
            raise ValueError(
                "CURRENT/IDENTITY_PINNED references must not carry object_version"
            )
        return self

    @model_serializer(mode="wrap")
    def serialize_reference(
        self,
        handler: SerializerFunctionWrapHandler,
    ) -> dict[str, object]:
        raw: Any = handler(self)
        if not isinstance(raw, dict):
            raise TypeError("reference serializer must produce an object")
        data = cast(dict[str, object], raw)
        if self.object_version is None:
            data.pop("object_version", None)
        if self.tenant_id is None:
            data.pop("tenant_id", None)
        return data


class DocumentVersionReference(CrossEngineObjectReference):
    """Exact immutable Trade Docs DocumentVersion identity required by RTD-06."""

    owner_engine_id: Literal["baobab-trade-docs"]
    object_type: Literal["DOCUMENT_VERSION"]
    reference_mode: Literal["IDENTITY_PINNED"]


class ContentArtifactReference(CrossEngineObjectReference):
    """Exact Trade Docs content artifact identity."""

    owner_engine_id: Literal["baobab-trade-docs"]
    object_type: Literal["CONTENT_ARTIFACT"]
    reference_mode: Literal["IDENTITY_PINNED"]


class RegulatoryEvidenceAssessmentReference(PinnedRegulationsReference):
    """Pinned Regulations-owned evidence-assessment identity."""

    object_type: Literal["REGULATORY_EVIDENCE_ASSESSMENT"]


class IssuerClaim(BaseModel):
    """Trade Docs issuer claim; it is a fact, not a Regulations conclusion."""

    model_config = ConfigDict(extra="forbid")

    party_reference: Annotated[str, Field(min_length=1, max_length=256)]
    issuer_role: IssuerRoleCode
    source_identity: Annotated[str | None, Field(max_length=256)] = None
    authority_context: Annotated[str | None, Field(max_length=256)] = None


class DocumentaryVerificationSnapshot(BaseModel):
    """Point-in-time Trade Docs verification fact."""

    model_config = ConfigDict(extra="forbid")

    verification_state: Literal[
        "UNVERIFIED",
        "PENDING",
        "VERIFIED",
        "FAILED",
        "DISPUTED",
        "UNKNOWN",
    ]
    reason_code: RequirementCode | None = None
    observed_at: datetime

    @field_validator("observed_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value


class DocumentaryValiditySnapshot(BaseModel):
    """Point-in-time issuer/authority-relative temporal-validity fact."""

    model_config = ConfigDict(extra="forbid")

    temporal_validity_state: Literal[
        "NOT_YET_EFFECTIVE",
        "CURRENTLY_VALID",
        "EXPIRED",
        "REVOKED",
        "UNKNOWN",
    ]
    observed_at: datetime

    @field_validator("observed_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value


class DocumentaryAssertion(BaseModel):
    """Bounded documentary assertion retaining Trade Docs provenance."""

    model_config = ConfigDict(extra="forbid")

    element_code: DataElementCode
    origin: Literal[
        "ISSUER_ASSERTED",
        "BAOBAB_EXTRACTED",
        "BAOBAB_GENERATED",
        "EXTERNAL_NORMALIZED",
    ]
    value: str | float | bool
    unit: Annotated[str | None, Field(max_length=64)] = None
    currency: Annotated[str | None, Field(pattern=r"^[A-Z]{3}$")] = None
    source_artifact_reference: ContentArtifactReference | None = None
    field_verification_state: Literal[
        "UNVERIFIED",
        "PENDING",
        "VERIFIED",
        "FAILED",
        "DISPUTED",
        "UNKNOWN",
    ] | None = None
    observed_at: datetime

    @field_validator("value")
    @classmethod
    def constrain_string_value(cls, value: str | float | bool) -> str | float | bool:
        if isinstance(value, str) and len(value) > 2048:
            raise ValueError("documentary assertion string values are limited to 2048 characters")
        return value

    @field_validator("observed_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value


class DocumentEvidenceFactBundle(BaseModel):
    """Exact bounded Trade Docs facts supplied for legal sufficiency assessment."""

    model_config = ConfigDict(extra="forbid")

    document_version_reference: DocumentVersionReference
    document_type: DocumentTypeCode
    document_family: Literal[
        "TRADE",
        "TRANSPORT",
        "CUSTOMS",
        "REGULATORY",
        "PROCUREMENT",
        "FINANCIAL",
        "INSURANCE",
        "QUALITY",
        "WAREHOUSE",
        "PAYMENT",
        "CONTRACT",
        "IDENTITY_SUPPORTING",
        "OTHER",
    ]
    issuer_claim: IssuerClaim
    issued_at: datetime | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    verification: DocumentaryVerificationSnapshot
    temporal_validity: DocumentaryValiditySnapshot
    subject_references: Annotated[list[CrossEngineObjectReference], Field(max_length=64)]
    documentary_assertions: Annotated[list[DocumentaryAssertion], Field(max_length=256)]
    content_artifact_references: Annotated[list[ContentArtifactReference], Field(max_length=64)]
    facts_observed_at: datetime

    @field_validator(
        "issued_at",
        "effective_from",
        "effective_to",
        "facts_observed_at",
    )
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value

    @field_validator("subject_references", "content_artifact_references")
    @classmethod
    def require_unique_references(cls, value: list[CrossEngineObjectReference]) -> list[CrossEngineObjectReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("RTD-06 arrays declared uniqueItems must not contain duplicates")
        return value


class DocumentEvidenceAssessmentRequest(BaseModel):
    """Shared RTD-06 documentEvidenceAssessmentRequest."""

    model_config = ConfigDict(extra="forbid")

    context_id: UUID
    regulatory_decision_reference: RegulatoryDecisionReference
    requirement_reference: RegulatoryRequirementReference
    assessment_reason: Literal[
        "INITIAL_EVIDENCE",
        "EVIDENCE_CHANGED",
        "VERIFICATION_CHANGED",
        "VALIDITY_CHANGED",
        "MANUAL_REVIEW",
        "REGULATORY_REASSESSMENT",
    ]
    evidence: Annotated[list[DocumentEvidenceFactBundle], Field(min_length=1, max_length=50)]


class RejectedEvidence(BaseModel):
    """Evidence rejected for this Regulations-owned legal sufficiency assessment."""

    model_config = ConfigDict(extra="forbid")

    document_version_reference: DocumentVersionReference
    reason_codes: Annotated[list[RequirementCode], Field(min_length=1, max_length=32)]

    @field_validator("reason_codes")
    @classmethod
    def require_unique_reason_codes(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("RTD-06 reason_codes must be unique")
        return value


class DocumentEvidenceAssessmentResult(BaseModel):
    """Shared RTD-06 Regulations-owned legal sufficiency result."""

    model_config = ConfigDict(extra="forbid")

    assessment_reference: RegulatoryEvidenceAssessmentReference
    regulatory_decision_reference: RegulatoryDecisionReference
    requirement_reference: RegulatoryRequirementReference
    outcome: Literal[
        "SATISFIED",
        "UNSATISFIED",
        "INDETERMINATE",
        "NOT_APPLICABLE",
        "REVIEW_REQUIRED",
    ]
    accepted_document_version_references: Annotated[
        list[DocumentVersionReference],
        Field(max_length=50),
    ]
    rejected_evidence: Annotated[list[RejectedEvidence], Field(max_length=50)]
    reason_codes: Annotated[list[RequirementCode], Field(max_length=64)]
    resulting_regulatory_decision_reference: RegulatoryDecisionReference | None = None
    evaluated_at: datetime

    @field_validator("accepted_document_version_references")
    @classmethod
    def require_unique_accepted_references(
        cls,
        value: list[DocumentVersionReference],
    ) -> list[DocumentVersionReference]:
        canonical = [item.model_dump_json() for item in value]
        if len(canonical) != len(set(canonical)):
            raise ValueError("accepted DocumentVersion references must be unique")
        return value

    @field_validator("reason_codes")
    @classmethod
    def require_unique_reason_codes(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("RTD-06 reason_codes must be unique")
        return value

    @field_validator("evaluated_at")
    @classmethod
    def require_offset_aware_datetime(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("RTD-06 date-time values must include a UTC offset")
        return value


__all__ = [
    "ContentArtifactReference",
    "CrossEngineObjectReference",
    "DocumentEvidenceAssessmentRequest",
    "DocumentEvidenceAssessmentResult",
    "DocumentEvidenceFactBundle",
    "DocumentVersionReference",
    "DocumentaryAssertion",
    "DocumentaryValiditySnapshot",
    "DocumentaryVerificationSnapshot",
    "IssuerClaim",
    "ObjectVersion",
    "PinnedRegulationsReference",
    "RegulatoryDecisionReference",
    "RegulatoryDocumentRequirementProjection",
    "RegulatoryEvidenceAssessmentReference",
    "RegulatoryRequirementReference",
    "RejectedEvidence",
    "RequirementResolveRequest",
    "RequirementResolveResponse",
]

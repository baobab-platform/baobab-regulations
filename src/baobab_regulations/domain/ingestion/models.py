"""REG-INGEST-02 contracts. Retrieval evidence never confers legal authority."""

from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID


class RightsOutcome(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    HOLD = "HOLD"


class AcquisitionStatus(StrEnum):
    REQUESTED = "REQUESTED"
    RIGHTS_CHECK_PENDING = "RIGHTS_CHECK_PENDING"
    AUTHORIZED = "AUTHORIZED"
    FETCHING = "FETCHING"
    ACQUIRED = "ACQUIRED"
    QUARANTINED = "QUARANTINED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, slots=True)
class AcquisitionCommand:
    source_id: str
    endpoint_ref: str
    context_id: UUID

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.endpoint_ref.strip():
            raise ValueError("source_id and endpoint_ref are required")


@dataclass(frozen=True, slots=True)
class RegisteredEndpoint:
    """Only the governed endpoint registry supplies this configuration."""

    source_id: str
    endpoint_ref: str
    uri: str
    allowed_hosts: frozenset[str]
    permitted_media_types: frozenset[str]
    max_bytes: int
    adapter_id: str
    adapter_version: str
    approved: bool = False

    def __post_init__(self) -> None:
        if not self.approved:
            raise ValueError("source endpoint is not approved")
        if not 1 <= self.max_bytes <= 33554432:
            raise ValueError("source size bound must be 1..33554432 bytes")
        if not self.allowed_hosts or not self.permitted_media_types:
            raise ValueError("endpoint requires explicit host and media allow-lists")
        if not self.adapter_id or not self.adapter_version:
            raise ValueError("adapter identity and version are required")


@dataclass(frozen=True, slots=True)
class RightsDecision:
    scope: Literal["ACQUIRE_AND_STORE", "TRANSFORM_AND_PROCESS"]
    outcome: RightsOutcome
    profile_ref: str
    revision: str
    evidence_refs: tuple[str, ...]
    decision_id: str

    def __post_init__(self) -> None:
        if not self.profile_ref.strip() or not self.revision.strip() or not self.decision_id.strip():
            raise ValueError("rights decision must have a profile, revision and decision ID")
        if self.outcome is RightsOutcome.ALLOW and not self.evidence_refs:
            raise ValueError("ALLOW requires governed rights evidence")


@dataclass(frozen=True, slots=True)
class FetchedSource:
    """Headers are deliberately projected; never expose raw response headers."""

    body: AsyncIterator[bytes]
    media_type: str
    content_length: int | None
    etag: str | None
    last_modified: str | None
    on_close: Callable[[], Awaitable[None]] | None = None


@dataclass(frozen=True, slots=True)
class StoredEvidence:
    storage_ref: str
    content_hash: str
    size_bytes: int
    prefix: bytes
    hash_algorithm: Literal["SHA-256"] = "SHA-256"


@dataclass(frozen=True, slots=True)
class SourceEvidenceRecord:
    artefact_id: UUID
    acquisition_id: UUID
    tenant_id: str
    source_id: str
    endpoint_ref: str
    storage_ref: str
    sha256: str
    size_bytes: int
    declared_media_type: str
    retrieved_at: datetime
    etag: str | None = None
    last_modified: str | None = None
    authenticity: Literal["UNVERIFIED"] = "UNVERIFIED"


@dataclass(frozen=True, slots=True)
class SecurityAssessment:
    permitted: bool
    scanner_ref: str
    scanner_version: str
    evidence_ref: str
    reason_code: str

    def __post_init__(self) -> None:
        if not all((self.scanner_ref, self.scanner_version, self.evidence_ref, self.reason_code)):
            raise ValueError("security decisions must be attributable and evidenced")


@dataclass(frozen=True, slots=True)
class AcquisitionResult:
    acquisition_id: UUID
    tenant_id: str
    status: AcquisitionStatus
    artefact: SourceEvidenceRecord | None = None
    processing_permitted: bool = False

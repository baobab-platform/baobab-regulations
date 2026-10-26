"""Narrow provider-neutral ports for governed regulatory retrieval."""

from collections.abc import AsyncIterator
from datetime import datetime
from typing import Protocol
from uuid import UUID

from baobab_regulations.application.ports.context_authority import AuthenticatedCaller
from baobab_regulations.domain.ingestion.models import (
    FetchedSource,
    RegisteredEndpoint,
    RightsDecision,
    SecurityAssessment,
    SourceEvidenceRecord,
    StoredEvidence,
)


class RegisteredEndpointPort(Protocol):
    async def resolve(
        self, *, tenant_id: str, source_id: str, endpoint_ref: str
    ) -> RegisteredEndpoint | None: ...


class AcquisitionAuthorityPort(Protocol):
    async def require_acquisition_grant(
        self, *, caller: AuthenticatedCaller, tenant_id: str, source_id: str
    ) -> None: ...


class AcquisitionRightsPort(Protocol):
    async def decide(
        self, *, tenant_id: str, source_id: str, scope: str
    ) -> RightsDecision: ...


class SourceFetcherPort(Protocol):
    async def fetch(self, endpoint: RegisteredEndpoint) -> FetchedSource: ...


class QuarantinePort(Protocol):
    async def store(
        self, *, artefact_id: UUID, chunks: AsyncIterator[bytes], max_bytes: int
    ) -> StoredEvidence: ...


class SourceSecurityPort(Protocol):
    async def assess(
        self, *, artefact: SourceEvidenceRecord, signature: bytes
    ) -> SecurityAssessment: ...


class AcquisitionEvidencePort(Protocol):
    async def start(
        self, *, acquisition_id: UUID, tenant_id: str, source_id: str, endpoint_ref: str,
        actor_ref: str, requested_at: datetime
    ) -> None: ...

    async def event(
        self, *, acquisition_id: UUID, tenant_id: str, status: str,
        details: dict[str, str]
    ) -> None: ...

    async def artefact(self, artefact: SourceEvidenceRecord) -> None: ...

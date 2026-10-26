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
    ) -> RegisteredEndpoint | None:
        raise NotImplementedError


class AcquisitionAuthorityPort(Protocol):
    async def require_acquisition_grant(
        self, *, caller: AuthenticatedCaller, tenant_id: str, source_id: str
    ) -> None:
        raise NotImplementedError


class AcquisitionRightsPort(Protocol):
    async def decide(
        self, *, tenant_id: str, source_id: str, scope: str
    ) -> RightsDecision:
        raise NotImplementedError


class SourceFetcherPort(Protocol):
    async def fetch(self, endpoint: RegisteredEndpoint) -> FetchedSource:
        raise NotImplementedError


class QuarantinePort(Protocol):
    async def store(
        self, *, artefact_id: UUID, chunks: AsyncIterator[bytes], max_bytes: int
    ) -> StoredEvidence:
        raise NotImplementedError


class SourceSecurityPort(Protocol):
    async def assess(
        self, *, artefact: SourceEvidenceRecord, signature: bytes
    ) -> SecurityAssessment:
        raise NotImplementedError


class AcquisitionEvidencePort(Protocol):
    async def start(
        self, *, acquisition_id: UUID, tenant_id: str, source_id: str, endpoint_ref: str,
        actor_ref: str, requested_at: datetime
    ) -> None:
        raise NotImplementedError

    async def event(
        self, *, acquisition_id: UUID, tenant_id: str, status: str,
        details: dict[str, str]
    ) -> None:
        raise NotImplementedError

    async def artefact(self, artefact: SourceEvidenceRecord) -> None:
        raise NotImplementedError

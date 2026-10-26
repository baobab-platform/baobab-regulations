"""Offline append-only acquisition journal; never a production evidence custodian."""

from dataclasses import dataclass
from uuid import UUID

from baobab_regulations.domain.ingestion.models import SourceEvidenceRecord


@dataclass(frozen=True, slots=True)
class JournalEvent:
    tenant_id: str
    acquisition_id: UUID
    status: str
    details: dict[str, str]


class InMemoryAcquisitionEvidence:
    def __init__(self) -> None:
        self.starts: dict[UUID, tuple[str, str, str, str, str]] = {}
        self.events: list[JournalEvent] = []
        self.artefacts: dict[UUID, SourceEvidenceRecord] = {}

    async def start(
        self, *, acquisition_id: UUID, tenant_id: str, source_id: str,
        endpoint_ref: str, actor_ref: str, requested_at: str
    ) -> None:
        if acquisition_id in self.starts:
            raise ValueError("acquisition exists")
        self.starts[acquisition_id] = (
            tenant_id, source_id, endpoint_ref, actor_ref, requested_at
        )

    async def event(
        self, *, acquisition_id: UUID, tenant_id: str,
        status: str, details: dict[str, str]
    ) -> None:
        if acquisition_id not in self.starts or self.starts[acquisition_id][0] != tenant_id:
            raise PermissionError("tenant-bound acquisition required")
        self.events.append(
            JournalEvent(tenant_id, acquisition_id, status, dict(details))
        )

    async def artefact(self, artefact: SourceEvidenceRecord) -> None:
        if artefact.acquisition_id not in self.starts:
            raise ValueError("unknown acquisition")
        if self.starts[artefact.acquisition_id][0] != artefact.tenant_id:
            raise PermissionError("cross-tenant artefact")
        if artefact.artefact_id in self.artefacts:
            raise ValueError("artefact already exists")
        self.artefacts[artefact.artefact_id] = artefact

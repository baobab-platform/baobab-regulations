"""Tenant-scoped PostgreSQL 17 evidentiary append-only acquisition journal.

Use a dedicated non-BYPASSRLS runtime DB role, with INSERT/SELECT only;
connection settings are transaction-local to prevent pooled context leakage.
The migration implements matching FORCE RLS on each table.
"""

import json
from datetime import datetime
from typing import Any
from uuid import UUID

from baobab_regulations.domain.ingestion.models import SourceEvidenceRecord


class PostgresAcquisitionEvidence:
    def __init__(self, pool: Any) -> None:
        self._pool = pool

    @staticmethod
    async def _tenant(conn: Any, tenant_id: str) -> None:
        if not tenant_id.startswith("tn_"):
            raise ValueError("canonical tenant ID required")
        await conn.execute("SELECT set_config('baobab.tenant_id', $1, true)", tenant_id)

    async def start(
        self, *, acquisition_id: UUID, tenant_id: str, source_id: str,
        endpoint_ref: str, actor_ref: str, requested_at: datetime
    ) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await self._tenant(conn, tenant_id)
            await conn.execute(
                """
                INSERT INTO reg_source_acquisitions (
                    acquisition_id, tenant_id, source_id, endpoint_ref,
                    actor_ref, requested_at
                ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                acquisition_id, tenant_id, source_id, endpoint_ref,
                actor_ref, requested_at
            )

    async def event(
        self, *, acquisition_id: UUID, tenant_id: str,
        status: str, details: dict[str, str]
    ) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await self._tenant(conn, tenant_id)
            await conn.execute(
                """
                INSERT INTO reg_source_acquisition_events (
                    acquisition_id, tenant_id, status, details
                ) VALUES ($1, $2, $3, $4::jsonb)
                """,
                acquisition_id, tenant_id, status, json.dumps(details, sort_keys=True)
            )

    async def artefact(self, artefact: SourceEvidenceRecord) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await self._tenant(conn, artefact.tenant_id)
            result = await conn.fetchval(
                """
                INSERT INTO reg_source_acquisition_artefacts (
                    artefact_id, acquisition_id, tenant_id, source_id, endpoint_ref,
                    storage_ref, sha256, size_bytes, declared_media_type, retrieved_at,
                    etag, last_modified, authenticity_state
                )
                SELECT $1, a.acquisition_id, a.tenant_id, a.source_id,
                       a.endpoint_ref, $2, $3, $4, $5, $6, $7, $8, $9
                FROM reg_source_acquisitions a
                WHERE a.acquisition_id = $10 AND a.tenant_id = $11
                  AND a.source_id = $12 AND a.endpoint_ref = $13
                RETURNING artefact_id
                """,
                artefact.artefact_id, artefact.storage_ref, artefact.sha256,
                artefact.size_bytes, artefact.declared_media_type,
                artefact.retrieved_at, artefact.etag, artefact.last_modified,
                artefact.authenticity, artefact.acquisition_id,
                artefact.tenant_id, artefact.source_id, artefact.endpoint_ref
            )
            if result is None:
                raise PermissionError("unknown or cross-tenant acquisition source")

    async def read_artefact(
        self, *, tenant_id: str, artefact_id: UUID
    ) -> SourceEvidenceRecord | None:
        async with self._pool.acquire() as conn, conn.transaction():
            await self._tenant(conn, tenant_id)
            row = await conn.fetchrow(
                """
                SELECT artefact_id, acquisition_id, tenant_id, source_id,
                       endpoint_ref, storage_ref, sha256, size_bytes,
                       declared_media_type, retrieved_at, etag, last_modified
                FROM reg_source_acquisition_artefacts WHERE artefact_id = $1
                """,
                artefact_id
            )
            if row is None:
                return None
            return SourceEvidenceRecord(**dict(row))

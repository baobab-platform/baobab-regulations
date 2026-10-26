"""Live PostgreSQL 17 migration, append-only journal and tenant RLS qualification."""

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

import asyncpg
import pytest
import pytest_asyncio

from baobab_regulations.domain.ingestion.models import SourceEvidenceRecord
from baobab_regulations.infrastructure.persistence.acquisition_postgres import (
    PostgresAcquisitionEvidence,
)

TENANT_A = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
TENANT_B = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
ROLE = "reg_ingest_02_test_writer"
ROLE_PASSWORD = "reg_ingest_synthetic_ci_only"


@pytest_asyncio.fixture
async def live() -> AsyncIterator[tuple[asyncpg.Connection, PostgresAcquisitionEvidence, asyncpg.Pool]]:
    url = os.getenv("REG_INGEST_DATABASE_URL")
    if not url:
        pytest.skip("REG_INGEST_DATABASE_URL is not configured")
    admin = await asyncpg.connect(url)
    for path in (
        "migrations/000002_source_registry.sql",
        "migrations/000007_secure_source_acquisition.sql",
    ):
        await admin.execute(Path(path).read_text(encoding="utf-8"))
    await admin.execute(
        """
        INSERT INTO authoritative_sources (source_id, name, publisher)
        VALUES ('reg_ingest_synthetic_source', 'Synthetic source', 'Test publisher')
        ON CONFLICT (source_id) DO NOTHING
        """
    )
    await admin.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{ROLE}') THEN
                CREATE ROLE {ROLE} LOGIN PASSWORD '{ROLE_PASSWORD}'
                    NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
            END IF;
        END $$;
        """
    )
    await admin.execute(f"GRANT USAGE ON SCHEMA public TO {ROLE}")
    for table in (
        "reg_source_acquisitions",
        "reg_source_acquisition_events",
        "reg_source_acquisition_artefacts",
    ):
        await admin.execute(f"GRANT SELECT, INSERT ON {table} TO {ROLE}")
    await admin.execute(
        f"GRANT USAGE ON SEQUENCE reg_source_acquisition_events_event_id_seq TO {ROLE}"
    )
    split = urlsplit(url)
    pool = await asyncpg.create_pool(
        host=split.hostname, port=split.port or 5432,
        user=ROLE, password=ROLE_PASSWORD,
        database=split.path.removeprefix("/"),
        min_size=1, max_size=2,
    )
    assert pool is not None
    try:
        yield admin, PostgresAcquisitionEvidence(pool), pool
    finally:
        await pool.close()
        await admin.close()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_append_only_and_cross_tenant_read_denial(live):
    admin, journal, pool = live
    acquisition = uuid4()
    artefact = SourceEvidenceRecord(
        artefact_id=uuid4(), acquisition_id=acquisition, tenant_id=TENANT_A,
        source_id="reg_ingest_synthetic_source", endpoint_ref="official",
        storage_ref="private-quarantine:a", sha256="a" * 64,
        size_bytes=16, declared_media_type="application/pdf",
        retrieved_at=datetime.now(UTC), etag='"v1"',
    )
    await journal.start(
        acquisition_id=acquisition, tenant_id=TENANT_A,
        source_id="reg_ingest_synthetic_source",
        endpoint_ref="official", actor_ref="synthetic:issuer",
        requested_at=datetime.now(UTC),
    )
    await journal.event(
        acquisition_id=acquisition, tenant_id=TENANT_A,
        status="RIGHTS_CHECK_PENDING", details={"rights_outcome": "ALLOW"},
    )
    await journal.artefact(artefact)
    assert await journal.read_artefact(tenant_id=TENANT_A, artefact_id=artefact.artefact_id) == artefact
    assert await journal.read_artefact(tenant_id=TENANT_B, artefact_id=artefact.artefact_id) is None
    async with pool.acquire() as conn:
        assert await conn.fetchval("SELECT count(*) FROM reg_source_acquisitions") == 0
        assert await conn.fetchval("SELECT count(*) FROM reg_source_acquisition_events") == 0
        assert await conn.fetchval("SELECT count(*) FROM reg_source_acquisition_artefacts") == 0
        assert await conn.fetchval(
            "SELECT has_table_privilege(current_user, 'reg_source_acquisitions', 'DELETE')"
        ) is False
    with pytest.raises(asyncpg.exceptions.InsufficientPrivilegeError):
        async with pool.acquire() as conn, conn.transaction():
            await conn.execute("SELECT set_config('baobab.tenant_id', $1, true)", TENANT_A)
            await conn.execute(
                "DELETE FROM reg_source_acquisition_artefacts WHERE artefact_id=$1",
                artefact.artefact_id
            )
    # Admin may inspect independent evidence; no application path can rewrite it.
    assert await admin.fetchval(
        "SELECT count(*) FROM reg_source_acquisition_artefacts WHERE artefact_id=$1",
        artefact.artefact_id
    ) == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_cross_tenant_insert_and_source_spoof_denied(live):
    _, journal, _ = live
    acquisition = uuid4()
    await journal.start(
        acquisition_id=acquisition, tenant_id=TENANT_A,
        source_id="reg_ingest_synthetic_source", endpoint_ref="official",
        actor_ref="fixture", requested_at=datetime.now(UTC),
    )
    with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
        await journal.event(
            acquisition_id=acquisition, tenant_id=TENANT_B,
            status="AUTHORIZED", details={},
        )
    with pytest.raises(PermissionError):
        await journal.artefact(
            SourceEvidenceRecord(
                artefact_id=uuid4(), acquisition_id=acquisition, tenant_id=TENANT_A,
                source_id="spoofed_source", endpoint_ref="official",
                storage_ref="private-quarantine:b", sha256="b" * 64,
                size_bytes=1, declared_media_type="text/plain",
                retrieved_at=datetime.now(UTC),
            )
        )

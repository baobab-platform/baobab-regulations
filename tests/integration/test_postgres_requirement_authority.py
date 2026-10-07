"""R-CAP-10 live PostgreSQL governed requirement authority conformance."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import asyncpg
import pytest
import pytest_asyncio

from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityIntegrityError,
    RequirementLookupStatus,
)
from baobab_regulations.contracts.rtd06 import (
    ObjectVersion,
    RegulatoryDecisionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
)
from baobab_regulations.infrastructure.persistence.requirements_postgres import (
    GovernedRequirementProjectionWriter,
    PostgresRequirementRepository,
)

TENANT_A = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
TENANT_B = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
ROLE = "r_cap_10_requirement_reader"
PASSWORD = "r_cap_10_reader_test"


def reference(
    *,
    tenant: str = TENANT_A,
    version: str | None = None,
) -> RegulatoryRequirementReference:
    return RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_r_cap_10_phyto",
        reference_mode="VERSION_PINNED" if version else "IDENTITY_PINNED",
        object_version=ObjectVersion(kind="REVISION", value=version) if version else None,
        scope="tenant",
        tenant_id=tenant,
    )


def projection(
    *,
    ref: RegulatoryRequirementReference | None = None,
    code: str = "PHYTOSANITARY_CERTIFICATE_REQUIRED",
    decision_tenant: str = TENANT_A,
) -> RegulatoryDocumentRequirementProjection:
    return RegulatoryDocumentRequirementProjection(
        requirement_reference=ref or reference(),
        regulatory_decision_reference=RegulatoryDecisionReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_DECISION",
            object_id="regdec_r_cap_10",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=decision_tenant,
        ),
        requirement_kind="DOCUMENT",
        requirement_code=code,
        purpose_code="SPS",
        acceptable_document_types=["PHYTOSANITARY_CERTIFICATE"],
        required_issuer_roles=["COMPETENT_AUTHORITY"],
        required_data_elements=["CONSIGNMENT_REFERENCE", "ORIGIN_COUNTRY"],
        unsatisfied_effect_code="SPS_HOLD_REQUIRED",
        effective_from=datetime(2026, 10, 1, tzinfo=UTC),
        determined_at=datetime(2026, 10, 1, 8, tzinfo=UTC),
    )


def reader_url(admin_url: str) -> str:
    scheme_and_user, host = admin_url.split("@", 1)
    scheme = scheme_and_user.split("://", 1)[0]
    return f"{scheme}://{ROLE}:{PASSWORD}@{host}"


@pytest_asyncio.fixture
async def database() -> AsyncIterator[tuple[asyncpg.Connection, PostgresRequirementRepository, GovernedRequirementProjectionWriter, asyncpg.Pool]]:
    url = os.getenv("R_CAP_10_DATABASE_URL")
    if not url:
        pytest.skip("R_CAP_10_DATABASE_URL not provided")
    admin = await asyncpg.connect(url)
    await admin.execute(
        """
        CREATE TABLE IF NOT EXISTS regulatory_rule_sets (
            rule_set_id TEXT PRIMARY KEY
        )
        """
    )
    # The requirement migration is independently runnable.
    from pathlib import Path
    await admin.execute(
        Path("migrations/000006_regulatory_requirement_projections.sql")
        .read_text(encoding="utf-8")
    )
    await admin.execute("TRUNCATE regulatory_requirement_projections")
    await admin.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{ROLE}') THEN
                CREATE ROLE {ROLE}
                    LOGIN PASSWORD '{PASSWORD}'
                    NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
            END IF;
        END $$;
        """
    )
    await admin.execute(f"GRANT USAGE ON SCHEMA public TO {ROLE}")
    await admin.execute(
        f"GRANT SELECT ON regulatory_requirement_projections TO {ROLE}"
    )
    pool = await asyncpg.create_pool(reader_url(url), min_size=1, max_size=3)
    assert pool is not None
    admin_pool = await asyncpg.create_pool(url, min_size=1, max_size=2)
    assert admin_pool is not None
    try:
        yield (
            admin,
            PostgresRequirementRepository(pool),
            GovernedRequirementProjectionWriter(admin_pool),
            pool,
        )
    finally:
        await pool.close()
        await admin_pool.close()
        await admin.close()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_exact_historical_pin_and_repeat_append(database: tuple) -> None:
    admin, reader, writer, _ = database
    fact = projection(ref=reference(version="v1"))
    await writer.append_reviewed(fact)
    await writer.append_reviewed(fact)
    lookup = await reader.resolve_exact(fact.requirement_reference)
    assert lookup.status is RequirementLookupStatus.FOUND
    assert lookup.requirement == fact
    assert await admin.fetchval(
        "SELECT count(*) FROM regulatory_requirement_projections"
    ) == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_different_pin_conflicts_without_silent_substitution(database: tuple) -> None:
    _, reader, writer, _ = database
    await writer.append_reviewed(projection(ref=reference(version="v2")))
    lookup = await reader.resolve_exact(reference(version="v1"))
    assert lookup.status is RequirementLookupStatus.CONFLICT
    absent = await reader.resolve_exact(
        reference(version="v1").model_copy(update={"object_id": "regreq_absent"})
    )
    assert absent.status is RequirementLookupStatus.NOT_FOUND


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_historical_pins_coexist_without_rewriting(database: tuple) -> None:
    admin, reader, writer, _ = database
    first = projection(ref=reference(version="v1"))
    second = projection(ref=reference(version="v2"), code="ORIGIN_CERTIFICATE_REQUIRED")
    await writer.append_reviewed(first)
    await writer.append_reviewed(second)
    assert (await reader.resolve_exact(first.requirement_reference)).requirement == first
    assert (await reader.resolve_exact(second.requirement_reference)).requirement == second
    assert await admin.fetchval(
        "SELECT count(*) FROM regulatory_requirement_projections"
    ) == 2


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_immutable_pin_rejects_changed_content(database: tuple) -> None:
    _, _, writer, _ = database
    await writer.append_reviewed(projection())
    with pytest.raises(RequirementAuthorityIntegrityError, match="immutable"):
        await writer.append_reviewed(
            projection(code="ORIGIN_CERTIFICATE_REQUIRED")
        )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_reader_rls_denies_unbound_and_cross_tenant(database: tuple) -> None:
    _, reader, writer, pool = database
    await writer.append_reviewed(projection())
    async with pool.acquire() as conn:
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_requirement_projections"
        ) == 0
        assert await conn.fetchval(
            "SELECT has_table_privilege(current_user, "
            "'regulatory_requirement_projections', 'INSERT')"
        ) is False
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute("SELECT set_config('baobab.tenant_id', $1, true)", TENANT_B)
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_requirement_projections"
        ) == 0
    assert (await reader.resolve_exact(reference(tenant=TENANT_B))).status is RequirementLookupStatus.NOT_FOUND


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_corrupted_projection_fails_integrity(database: tuple) -> None:
    admin, reader, writer, _ = database
    await writer.append_reviewed(projection())
    await admin.execute(
        """
        UPDATE regulatory_requirement_projections
        SET requirement_payload = jsonb_set(
            requirement_payload, '{requirement_code}', '"TAMPERED"'
        )
        """
    )
    with pytest.raises(RequirementAuthorityIntegrityError):
        await reader.resolve_exact(reference())

"""R-CAP-05 PostgreSQL durability, idempotency and RLS integration tests."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID

import asyncpg
import pytest
import pytest_asyncio

from baobab_regulations.application.ports.idempotency import (
    IdempotencyConflictError,
    IdempotencyIntegrityError,
)
from baobab_regulations.contracts.events import (
    RequirementSatisfactionEvaluatedEvent,
    build_requirement_satisfaction_evaluated_event,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentaryValiditySnapshot,
    DocumentaryVerificationSnapshot,
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    DocumentEvidenceFactBundle,
    DocumentVersionReference,
    IssuerClaim,
    RegulatoryDecisionReference,
    RegulatoryEvidenceAssessmentReference,
    RegulatoryRequirementReference,
)
from baobab_regulations.infrastructure.persistence.idempotency_postgres import (
    PostgresEvidenceAssessmentIdempotency,
)

TENANT_A = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
TENANT_B = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
IDEMPOTENCY_KEY = "r-cap-05-assessment-0001"
EVALUATED_AT = datetime(2026, 10, 6, 10, 30, tzinfo=UTC)
CORRELATION_ID = UUID("7d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f11")
RUNTIME_ROLE = "regulations_runtime_test"
RUNTIME_PASSWORD = "r_cap_05_runtime_test"


def _decision_reference(tenant_id: str = TENANT_A) -> RegulatoryDecisionReference:
    return RegulatoryDecisionReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_DECISION",
        object_id="regdec_01k7rtd6decision01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _requirement_reference(tenant_id: str = TENANT_A) -> RegulatoryRequirementReference:
    return RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_01k7rtd6phyto01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _document_reference(tenant_id: str = TENANT_A) -> DocumentVersionReference:
    return DocumentVersionReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_01k7rtd4001v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=tenant_id,
    )


def _request(
    *,
    tenant_id: str = TENANT_A,
    reason: str = "INITIAL_EVIDENCE",
) -> DocumentEvidenceAssessmentRequest:
    evidence = DocumentEvidenceFactBundle(
        document_version_reference=_document_reference(tenant_id),
        document_type="PHYTOSANITARY_CERTIFICATE",
        document_family="REGULATORY",
        issuer_claim=IssuerClaim(
            party_reference="org_ug_nppo",
            issuer_role="COMPETENT_AUTHORITY",
        ),
        verification=DocumentaryVerificationSnapshot(
            verification_state="VERIFIED",
            reason_code="ISSUER_AND_SIGNATURE_VERIFIED",
            observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
        ),
        temporal_validity=DocumentaryValiditySnapshot(
            temporal_validity_state="CURRENTLY_VALID",
            observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
        ),
        subject_references=[],
        documentary_assertions=[],
        content_artifact_references=[],
        facts_observed_at=datetime(2026, 10, 5, 20, 31, tzinfo=UTC),
    )
    return DocumentEvidenceAssessmentRequest.model_validate(
        {
            "context_id": str(CONTEXT_ID),
            "regulatory_decision_reference": _decision_reference(tenant_id).model_dump(
                mode="json"
            ),
            "requirement_reference": _requirement_reference(tenant_id).model_dump(
                mode="json"
            ),
            "assessment_reason": reason,
            "evidence": [evidence.model_dump(mode="json")],
        }
    )


def _result(
    *,
    tenant_id: str = TENANT_A,
    evaluated_at: datetime = EVALUATED_AT,
) -> DocumentEvidenceAssessmentResult:
    return DocumentEvidenceAssessmentResult(
        assessment_reference=RegulatoryEvidenceAssessmentReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_EVIDENCE_ASSESSMENT",
            object_id="regassess_0123456789abcdef01234567",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=tenant_id,
        ),
        regulatory_decision_reference=_decision_reference(tenant_id),
        requirement_reference=_requirement_reference(tenant_id),
        outcome="SATISFIED",
        accepted_document_version_references=[_document_reference(tenant_id)],
        rejected_evidence=[],
        reason_codes=[
            "DOCUMENT_TYPE_ACCEPTED",
            "ISSUER_ROLE_ACCEPTED",
            "DOCUMENT_VERIFIED",
            "DOCUMENT_CURRENTLY_VALID",
        ],
        resulting_regulatory_decision_reference=None,
        evaluated_at=evaluated_at,
    )



def _event(
    result: DocumentEvidenceAssessmentResult,
    *,
    tenant_id: str | None = None,
    idempotency_key: str = IDEMPOTENCY_KEY,
) -> RequirementSatisfactionEvaluatedEvent:
    resolved_tenant = tenant_id or result.assessment_reference.tenant_id
    assert resolved_tenant is not None
    return build_requirement_satisfaction_evaluated_event(
        tenant_id=resolved_tenant,
        idempotency_key=idempotency_key,
        result=result,
        correlation_id=CORRELATION_ID,
    )

def _fingerprint(request: DocumentEvidenceAssessmentRequest) -> str:
    encoded = json.dumps(
        request.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _runtime_url(admin_url: str) -> str:
    # CI uses the standard PostgreSQL URL. Keep construction deliberately
    # narrow rather than adding another URL-parsing dependency.
    prefix, host_and_db = admin_url.split("@", 1)
    scheme = prefix.split("://", 1)[0]
    return f"{scheme}://{RUNTIME_ROLE}:{RUNTIME_PASSWORD}@{host_and_db}"


@pytest_asyncio.fixture(scope="session")
async def postgres_urls() -> AsyncIterator[tuple[str, str]]:
    admin_url = os.getenv("R_CAP_05_DATABASE_URL")
    if not admin_url:
        pytest.skip("R_CAP_05_DATABASE_URL is not configured")

    admin = await asyncpg.connect(admin_url)
    for migration_path in (
        "migrations/000003_regulatory_evidence_assessments.sql",
        "migrations/000004_regulatory_event_outbox.sql",
    ):
        migration = Path(migration_path).read_text(encoding="utf-8")
        await admin.execute(migration)
    await admin.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_roles WHERE rolname = '{RUNTIME_ROLE}'
            ) THEN
                CREATE ROLE {RUNTIME_ROLE}
                    LOGIN
                    PASSWORD '{RUNTIME_PASSWORD}'
                    NOSUPERUSER
                    NOCREATEDB
                    NOCREATEROLE
                    NOINHERIT
                    NOBYPASSRLS;
            END IF;
        END
        $$;
        """
    )
    await admin.execute(f"GRANT USAGE ON SCHEMA public TO {RUNTIME_ROLE}")
    await admin.execute(
        f"""
        GRANT SELECT, INSERT
        ON regulatory_evidence_assessments, regulatory_event_outbox
        TO {RUNTIME_ROLE}
        """
    )
    await admin.close()

    yield admin_url, _runtime_url(admin_url)


@pytest_asyncio.fixture
async def stores(
    postgres_urls: tuple[str, str],
) -> AsyncIterator[tuple[Any, Any, PostgresEvidenceAssessmentIdempotency]]:
    admin_url, runtime_url = postgres_urls
    admin = await asyncpg.connect(admin_url)
    await admin.execute(
        "TRUNCATE TABLE regulatory_event_outbox, regulatory_evidence_assessments"
    )
    pool = await asyncpg.create_pool(runtime_url, min_size=1, max_size=4)
    assert pool is not None
    store = PostgresEvidenceAssessmentIdempotency(pool)
    try:
        yield admin, pool, store
    finally:
        await pool.close()
        await admin.close()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_migration_enables_and_forces_rls(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    admin, _, _ = stores
    row = await admin.fetchrow(
        """
        SELECT relrowsecurity, relforcerowsecurity
        FROM pg_class
        WHERE relname = 'regulatory_evidence_assessments'
        """
    )

    assert row is not None
    assert row["relrowsecurity"] is True
    assert row["relforcerowsecurity"] is True


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_commit_survives_adapter_recreation_and_replays_exact_result(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, pool, store = stores
    request = _request()
    result = _result()
    fingerprint = _fingerprint(request)

    committed = await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
        request=request,
        result=result,
        event=_event(result),
    )

    assert committed.created is True
    assert committed.result == result

    recreated = PostgresEvidenceAssessmentIdempotency(pool)
    replay = await recreated.replay(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
    )

    assert replay is not None
    assert replay.result == result


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_same_key_changed_request_conflicts_durably(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, _, store = stores
    original = _request()
    changed = _request(reason="EVIDENCE_CHANGED")

    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(original),
        request=original,
        result=_result(),
        event=_event(_result()),
    )

    with pytest.raises(IdempotencyConflictError):
        await store.replay(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=_fingerprint(changed),
        )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_same_key_is_isolated_by_tenant(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, _, store = stores
    request_a = _request(tenant_id=TENANT_A)
    request_b = _request(tenant_id=TENANT_B)
    result_a = _result(tenant_id=TENANT_A)
    result_b = _result(tenant_id=TENANT_B)
    result_b = result_b.model_copy(
        update={
            "assessment_reference": result_b.assessment_reference.model_copy(
                update={"object_id": "regassess_89abcdef0123456701234567"}
            )
        }
    )

    first = await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request_a),
        request=request_a,
        result=result_a,
        event=_event(result_a),
    )
    second = await store.commit(
        tenant_id=TENANT_B,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request_b),
        request=request_b,
        result=result_b,
        event=_event(result_b),
    )

    assert first.created is True
    assert second.created is True
    assert first.result.assessment_reference.tenant_id == TENANT_A
    assert second.result.assessment_reference.tenant_id == TENANT_B


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_concurrent_duplicate_commits_converge_on_one_result(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, _, store = stores
    request = _request()
    fingerprint = _fingerprint(request)
    first_candidate = _result(evaluated_at=EVALUATED_AT)
    second_candidate = _result(evaluated_at=EVALUATED_AT + timedelta(seconds=1))

    commits = await asyncio.gather(
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            request=request,
            result=first_candidate,
            event=_event(first_candidate),
        ),
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            request=request,
            result=second_candidate,
            event=_event(second_candidate),
        ),
    )

    assert sum(1 for item in commits if item.created) == 1
    assert commits[0].result == commits[1].result

    replay = await store.replay(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
    )
    assert replay is not None
    assert replay.result == commits[0].result


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_runtime_role_is_default_deny_without_transaction_tenant(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, pool, store = stores
    request = _request()
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request),
        request=request,
        result=_result(),
        event=_event(_result()),
    )

    async with pool.acquire() as conn:
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_evidence_assessments"
        ) == 0


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_rls_prevents_cross_tenant_reads_and_pool_context_leakage(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, pool, store = stores
    request = _request()
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request),
        request=request,
        result=_result(),
        event=_event(_result()),
    )

    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(
            "SELECT set_config('baobab.tenant_id', $1, true)",
            TENANT_A,
        )
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_evidence_assessments"
        ) == 1

    # The transaction-local setting must not survive reuse of the pooled connection.
    async with pool.acquire() as conn:
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_evidence_assessments"
        ) == 0
        async with conn.transaction():
            await conn.execute(
                "SELECT set_config('baobab.tenant_id', $1, true)",
                TENANT_B,
            )
            assert await conn.fetchval(
                "SELECT count(*) FROM regulatory_evidence_assessments"
            ) == 0


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_runtime_role_cannot_update_or_delete_assessment_history(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, pool, store = stores
    request = _request()
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request),
        request=request,
        result=_result(),
        event=_event(_result()),
    )

    async with pool.acquire() as conn:
        with pytest.raises(asyncpg.InsufficientPrivilegeError):
            async with conn.transaction():
                await conn.execute(
                    "SELECT set_config('baobab.tenant_id', $1, true)",
                    TENANT_A,
                )
                await conn.execute(
                    """
                    UPDATE regulatory_evidence_assessments
                    SET outcome = 'UNSATISFIED'
                    WHERE tenant_id = $1
                    """,
                    TENANT_A,
                )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_corrupted_result_payload_is_detected_on_replay(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    admin, _, store = stores
    request = _request()
    fingerprint = _fingerprint(request)
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
        request=request,
        result=_result(),
        event=_event(_result()),
    )

    await admin.execute(
        """
        UPDATE regulatory_evidence_assessments
        SET result_payload = '{"outcome":"SATISFIED"}'::jsonb
        WHERE tenant_id = $1 AND idempotency_key = $2
        """,
        TENANT_A,
        IDEMPOTENCY_KEY,
    )

    with pytest.raises(IdempotencyIntegrityError):
        await store.replay(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
        )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_assessment_identity_collision_is_integrity_failure(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency],
) -> None:
    _, _, store = stores
    first_request = _request()
    second_request = _request(reason="MANUAL_REVIEW")
    assessment = _result()

    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(first_request),
        request=first_request,
        result=assessment,
        event=_event(assessment),
    )

    with pytest.raises(IdempotencyIntegrityError):
        await store.commit(
            tenant_id=TENANT_A,
            idempotency_key="r-cap-05-assessment-0002",
            request_fingerprint=_fingerprint(second_request),
            request=second_request,
            result=assessment,
            event=_event(
                assessment,
                idempotency_key="r-cap-05-assessment-0002",
            ),
        )

"""R-CAP-06 PostgreSQL transactional outbox and relay integration tests."""

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
    IdempotencyAuthorityUnavailableError,
)
from baobab_regulations.application.ports.outbox import EventOutboxIntegrityError
from baobab_regulations.application.services.outbox_dispatch import (
    AtLeastOnceEventOutboxDispatcher,
    OutboxRetryPolicy,
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
from baobab_regulations.infrastructure.persistence.event_outbox_postgres import (
    PostgresEventOutboxRepository,
)
from baobab_regulations.infrastructure.persistence.idempotency_postgres import (
    PostgresEvidenceAssessmentIdempotency,
)

TENANT_A = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
TENANT_B = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
CORRELATION_A = UUID("7d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f11")
CORRELATION_B = UUID("8d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f12")
IDEMPOTENCY_KEY = "r-cap-06-assessment-0001"
EVALUATED_AT = datetime(2026, 10, 6, 11, 30, tzinfo=UTC)
RUNTIME_ROLE = "regulations_outbox_runtime_test"
RUNTIME_PASSWORD = "r_cap_06_runtime_test"


def _decision_reference() -> RegulatoryDecisionReference:
    return RegulatoryDecisionReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_DECISION",
        object_id="regdec_01k7rtd6decision01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_A,
    )


def _requirement_reference() -> RegulatoryRequirementReference:
    return RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_01k7rtd6phyto01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_A,
    )


def _document_reference() -> DocumentVersionReference:
    return DocumentVersionReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_01k7rtd4001v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_A,
    )


def _request() -> DocumentEvidenceAssessmentRequest:
    evidence = DocumentEvidenceFactBundle(
        document_version_reference=_document_reference(),
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
    return DocumentEvidenceAssessmentRequest(
        context_id=CONTEXT_ID,
        regulatory_decision_reference=_decision_reference(),
        requirement_reference=_requirement_reference(),
        assessment_reason="INITIAL_EVIDENCE",
        evidence=[evidence],
    )


def _result(*, evaluated_at: datetime = EVALUATED_AT) -> DocumentEvidenceAssessmentResult:
    return DocumentEvidenceAssessmentResult(
        assessment_reference=RegulatoryEvidenceAssessmentReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_EVIDENCE_ASSESSMENT",
            object_id="regassess_0123456789abcdef01234567",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=TENANT_A,
        ),
        regulatory_decision_reference=_decision_reference(),
        requirement_reference=_requirement_reference(),
        outcome="SATISFIED",
        accepted_document_version_references=[_document_reference()],
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
    correlation_id: UUID = CORRELATION_A,
) -> RequirementSatisfactionEvaluatedEvent:
    return build_requirement_satisfaction_evaluated_event(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        result=result,
        correlation_id=correlation_id,
        traceparent="00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    )


def _fingerprint(request: DocumentEvidenceAssessmentRequest) -> str:
    encoded = json.dumps(
        request.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _runtime_url(admin_url: str) -> str:
    prefix, host_and_db = admin_url.split("@", 1)
    scheme = prefix.split("://", 1)[0]
    return f"{scheme}://{RUNTIME_ROLE}:{RUNTIME_PASSWORD}@{host_and_db}"


@pytest_asyncio.fixture(scope="session")
async def postgres_urls() -> AsyncIterator[tuple[str, str]]:
    admin_url = os.getenv("R_CAP_06_DATABASE_URL")
    if not admin_url:
        pytest.skip("R_CAP_06_DATABASE_URL is not configured")

    admin = await asyncpg.connect(admin_url)
    for migration_path in (
        "migrations/000003_regulatory_evidence_assessments.sql",
        "migrations/000004_regulatory_event_outbox.sql",
    ):
        await admin.execute(Path(migration_path).read_text(encoding="utf-8"))

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
    await admin.execute(
        f"""
        GRANT UPDATE (
            status,
            attempt_count,
            next_attempt_at,
            lease_expires_at,
            published_at,
            last_error_code,
            updated_at
        )
        ON regulatory_event_outbox
        TO {RUNTIME_ROLE}
        """
    )
    await admin.close()
    yield admin_url, _runtime_url(admin_url)


@pytest_asyncio.fixture
async def stores(
    postgres_urls: tuple[str, str],
) -> AsyncIterator[
    tuple[
        Any,
        Any,
        PostgresEvidenceAssessmentIdempotency,
        PostgresEventOutboxRepository,
    ]
]:
    admin_url, runtime_url = postgres_urls
    admin = await asyncpg.connect(admin_url)
    await admin.execute(
        "TRUNCATE TABLE regulatory_event_outbox, regulatory_evidence_assessments"
    )
    pool = await asyncpg.create_pool(runtime_url, min_size=1, max_size=6)
    assert pool is not None
    assessment_store = PostgresEvidenceAssessmentIdempotency(pool)
    outbox = PostgresEventOutboxRepository(pool)
    try:
        yield admin, pool, assessment_store, outbox
    finally:
        await pool.close()
        await admin.close()


async def _commit(
    store: PostgresEvidenceAssessmentIdempotency,
    *,
    result: DocumentEvidenceAssessmentResult | None = None,
    correlation_id: UUID = CORRELATION_A,
) -> RequirementSatisfactionEvaluatedEvent:
    request = _request()
    resolved_result = result or _result()
    event = _event(resolved_result, correlation_id=correlation_id)
    committed = await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_fingerprint(request),
        request=request,
        result=resolved_result,
        event=event,
    )
    return committed.event


class RecordingPublisher:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.events: list[RequirementSatisfactionEvaluatedEvent] = []

    async def publish(self, event: RequirementSatisfactionEvaluatedEvent) -> None:
        self.events.append(event)
        if self.fail:
            raise RuntimeError("simulated broker failure")


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_atomic_commit_persists_one_canonical_outbox_event(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    admin, _, assessment_store, outbox = stores
    event = await _commit(assessment_store)

    record = await outbox.get_by_assessment(
        tenant_id=TENANT_A,
        assessment_id=event.data.result.assessment_reference.object_id,
    )
    assert record is not None
    assert record.event == event
    assert record.status == "PENDING"
    assert record.attempt_count == 0

    assert await admin.fetchval("SELECT count(*) FROM regulatory_evidence_assessments") == 1
    assert await admin.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_outbox_insert_failure_rolls_back_assessment_atomically(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    admin, _, assessment_store, _ = stores
    await admin.execute(f"REVOKE INSERT ON regulatory_event_outbox FROM {RUNTIME_ROLE}")
    try:
        with pytest.raises(IdempotencyAuthorityUnavailableError):
            await _commit(assessment_store)
    finally:
        await admin.execute(
            f"GRANT INSERT ON regulatory_event_outbox TO {RUNTIME_ROLE}"
        )

    assert await admin.fetchval("SELECT count(*) FROM regulatory_evidence_assessments") == 0
    assert await admin.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 0


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_concurrent_duplicate_command_creates_one_assessment_and_one_event(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    admin, _, store, _ = stores
    request = _request()
    fingerprint = _fingerprint(request)
    first_result = _result(evaluated_at=EVALUATED_AT)
    second_result = _result(evaluated_at=EVALUATED_AT + timedelta(seconds=1))

    first, second = await asyncio.gather(
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            request=request,
            result=first_result,
            event=_event(first_result, correlation_id=CORRELATION_A),
        ),
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            request=request,
            result=second_result,
            event=_event(second_result, correlation_id=CORRELATION_B),
        ),
    )

    assert sum(1 for item in (first, second) if item.created) == 1
    assert first.result == second.result
    assert first.event == second.event
    assert await admin.fetchval("SELECT count(*) FROM regulatory_evidence_assessments") == 1
    assert await admin.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_outbox_rls_defaults_deny_and_does_not_leak_tenants(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, pool, assessment_store, _ = stores
    await _commit(assessment_store)

    async with pool.acquire() as conn:
        assert await conn.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 0

    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(
            "SELECT set_config('baobab.tenant_id', $1, true)",
            TENANT_A,
        )
        assert await conn.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 1

    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(
            "SELECT set_config('baobab.tenant_id', $1, true)",
            TENANT_B,
        )
        assert await conn.fetchval("SELECT count(*) FROM regulatory_event_outbox") == 0


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_dispatcher_publishes_complete_envelope_and_marks_published(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, _, assessment_store, outbox = stores
    event = await _commit(assessment_store)
    publisher = RecordingPublisher()
    dispatcher = AtLeastOnceEventOutboxDispatcher(
        repository=outbox,
        publisher=publisher,
    )
    now = datetime.now(UTC) + timedelta(seconds=2)

    completed = await dispatcher.dispatch_due(
        tenant_id=TENANT_A,
        now=now,
    )

    assert [item.status for item in completed] == ["PUBLISHED"]
    assert publisher.events == [event]
    assert publisher.events[0].model_dump(mode="json", exclude_none=True)["data"] == (
        event.model_dump(mode="json", exclude_none=True)["data"]
    )
    assert completed[0].published_at == now


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_publish_failure_retries_then_dead_letters_same_event(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, _, assessment_store, outbox = stores
    event = await _commit(assessment_store)
    publisher = RecordingPublisher(fail=True)
    dispatcher = AtLeastOnceEventOutboxDispatcher(
        repository=outbox,
        publisher=publisher,
        retry=OutboxRetryPolicy(
            max_attempts=2,
            initial_delay_seconds=1,
            max_delay_seconds=1,
            lease_seconds=1,
        ),
    )
    first_now = datetime.now(UTC) + timedelta(seconds=2)

    first = await dispatcher.dispatch_due(tenant_id=TENANT_A, now=first_now)
    assert first[0].status == "RETRY"
    assert first[0].attempt_count == 1
    assert first[0].next_attempt_at == first_now + timedelta(seconds=1)

    second = await dispatcher.dispatch_due(
        tenant_id=TENANT_A,
        now=first_now + timedelta(seconds=2),
    )
    assert second[0].status == "DEAD_LETTER"
    assert second[0].attempt_count == 2
    assert [published.id for published in publisher.events] == [event.id, event.id]


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_expired_publish_lease_redelivers_original_event_id(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, _, assessment_store, outbox = stores
    event = await _commit(assessment_store)
    claimed_at = datetime.now(UTC) + timedelta(seconds=2)
    lease_expires = claimed_at + timedelta(seconds=10)

    claimed = await outbox.claim_due(
        tenant_id=TENANT_A,
        now=claimed_at,
        limit=1,
        lease_expires_at=lease_expires,
    )
    assert len(claimed) == 1
    assert claimed[0].event.id == event.id
    assert claimed[0].attempt_count == 1

    publisher = RecordingPublisher()
    dispatcher = AtLeastOnceEventOutboxDispatcher(
        repository=outbox,
        publisher=publisher,
    )
    assert await dispatcher.dispatch_due(
        tenant_id=TENANT_A,
        now=lease_expires - timedelta(seconds=1),
    ) == []

    completed = await dispatcher.dispatch_due(
        tenant_id=TENANT_A,
        now=lease_expires + timedelta(seconds=1),
    )
    assert completed[0].status == "PUBLISHED"
    assert completed[0].attempt_count == 2
    assert [published.id for published in publisher.events] == [event.id]


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_dispatcher_is_explicitly_tenant_scoped(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, _, assessment_store, outbox = stores
    await _commit(assessment_store)
    publisher = RecordingPublisher()
    dispatcher = AtLeastOnceEventOutboxDispatcher(
        repository=outbox,
        publisher=publisher,
    )

    completed = await dispatcher.dispatch_due(
        tenant_id=TENANT_B,
        now=datetime.now(UTC) + timedelta(seconds=2),
    )

    assert completed == []
    assert publisher.events == []


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_corrupted_envelope_fingerprint_fails_closed_before_publish(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    admin, _, assessment_store, outbox = stores
    event = await _commit(assessment_store)
    await admin.execute(
        """
        UPDATE regulatory_event_outbox
        SET envelope = jsonb_set(
            envelope,
            '{data,result,outcome}',
            '"UNSATISFIED"'::jsonb
        )
        WHERE event_id = $1
        """,
        event.id,
    )

    with pytest.raises(EventOutboxIntegrityError, match="fingerprint"):
        await outbox.get_by_assessment(
            tenant_id=TENANT_A,
            assessment_id=event.data.result.assessment_reference.object_id,
        )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_runtime_role_cannot_rewrite_committed_envelope(
    stores: tuple[Any, Any, PostgresEvidenceAssessmentIdempotency, PostgresEventOutboxRepository],
) -> None:
    _, pool, assessment_store, _ = stores
    await _commit(assessment_store)

    async with pool.acquire() as conn:
        with pytest.raises(asyncpg.InsufficientPrivilegeError):
            async with conn.transaction():
                await conn.execute(
                    "SELECT set_config('baobab.tenant_id', $1, true)",
                    TENANT_A,
                )
                await conn.execute(
                    """
                    UPDATE regulatory_event_outbox
                    SET envelope = '{}'::jsonb
                    WHERE tenant_id = $1
                    """,
                    TENANT_A,
                )

"""R-CAP-09 PostgreSQL decision durability, replay and RLS tests."""

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

from baobab_regulations.application.ports.decision_idempotency import (
    DecisionIdempotencyConflictError,
)
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
    DecisionProvenance,
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
    RegulatoryAssessmentReference,
    RegulatoryDecisionReference,
    RegulatoryFact,
    ReplayIdentity,
    RuleSetReference,
)
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState
from baobab_regulations.infrastructure.persistence.decision_idempotency_postgres import (
    PostgresDecisionEvaluationIdempotency,
)
from baobab_regulations.infrastructure.persistence.postgres import PostgresRuleSetRepository

TENANT_A = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
TENANT_B = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
NOW = datetime(2026, 10, 6, 10, tzinfo=UTC)
RULE_FP = "a" * 64
INPUT_FP = "b" * 64
IDEMPOTENCY_KEY = "r-cap-09-postgres-0001"
REPLAY_KEY = "replay-r-cap-09-postgres-0001"
RUNTIME_ROLE = "regulations_decision_runtime_test"
RUNTIME_PASSWORD = "r_cap_09_runtime_test"


def _rule_set_reference() -> RuleSetReference:
    return RuleSetReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_RULE_SET",
        object_id="ruleset_ug_za_coffee_2026_10",
        reference_mode="IDENTITY_PINNED",
        scope="platform",
    )


def _evidence() -> PinnedCrossEngineReference:
    return PinnedCrossEngineReference(
        owner_engine_id="baobab-trade-docs",
        object_type="DOCUMENT_VERSION",
        object_id="tdocv_r_cap_09_phyto_v1",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_A,
    )


def _request(*, replay_key: str = REPLAY_KEY, hs: str = "0901.11.10") -> DecisionEvaluateRequest:
    return DecisionEvaluateRequest(
        context_id=CONTEXT_ID,
        question="MAY_TRANSACTION_PROCEED",
        assessment_purpose="TRANSACTION_DECISION",
        decision_stage="PRE_SHIPMENT",
        subject_references=[
            PinnedCrossEngineReference(
                owner_engine_id="baobab-trade",
                object_type="SHIPMENT",
                object_id="ship_r_cap_09_pg_0001",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=TENANT_A,
            )
        ],
        regulated_activities=["CROSS_BORDER_EXPORT", "CROSS_BORDER_IMPORT"],
        facts=[
            RegulatoryFact(
                fact_code="HS_CODE",
                value=hs,
                observed_at=NOW,
            )
        ],
        evidence_references=[_evidence()],
        rule_set_reference=_rule_set_reference(),
        legal_time=NOW,
        knowledge_time=NOW,
        evaluation_profile="STANDARD",
        requested_assurance="STANDARD",
        requested_enforcement_class_ceiling="E2",
        replay_key=replay_key,
    )


def _response(
    *,
    evaluated_at: datetime = NOW + timedelta(seconds=1),
    input_fingerprint: str = INPUT_FP,
    replay_key: str = REPLAY_KEY,
) -> DecisionEvaluateResponse:
    legal_basis = PinnedCrossEngineReference(
        owner_engine_id="baobab-regulations",
        object_type="REGULATORY_PROVISION_VERSION",
        object_id="regprov_r_cap_09_sps",
        reference_mode="IDENTITY_PINNED",
        scope="platform",
    )
    return DecisionEvaluateResponse(
        decision_reference=RegulatoryDecisionReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_DECISION",
            object_id="regdec_0123456789abcdef01234567",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=TENANT_A,
        ),
        assessment_reference=RegulatoryAssessmentReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_ASSESSMENT",
            object_id="regassess_0123456789abcdef01234567",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=TENANT_A,
        ),
        outcome="SATISFIED",
        enforcement_class="E1",
        reasons=[
            DecisionReason(
                code="REFERENCE_PROFILE_SATISFIED",
                message="All checked requirements are satisfied.",
                legal_basis_references=[legal_basis],
                rule_version_references=[],
                evidence_references=[_evidence()],
            )
        ],
        legal_basis_references=[legal_basis],
        evidence_references=[_evidence()],
        recommended_disposition=RecommendedDisposition(
            disposition_code="ALLOW",
            rationale="No blocking condition found.",
            missing_requirement_references=[],
        ),
        rule_set_reference=_rule_set_reference(),
        rule_set_fingerprint=RULE_FP,
        evaluated_at=evaluated_at,
        legal_time=NOW,
        knowledge_time=NOW,
        provenance=DecisionProvenance(
            contract_major=1,
            input_fingerprint=input_fingerprint,
            rule_set_reference=_rule_set_reference(),
            rule_set_fingerprint=RULE_FP,
            evaluation_profile="STANDARD",
        ),
        replay_identity=ReplayIdentity(
            replay_key=replay_key,
            input_fingerprint=input_fingerprint,
            rule_set_fingerprint=RULE_FP,
        ),
    )


def _request_fingerprint(request: DecisionEvaluateRequest) -> str:
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
    admin_url = os.getenv("R_CAP_09_DATABASE_URL")
    if not admin_url:
        pytest.skip("R_CAP_09_DATABASE_URL is not configured")

    admin = await asyncpg.connect(admin_url)
    for migration_path in (
        "migrations/000001_regulatory_decisions.sql",
        "migrations/000005_regulatory_decision_evaluations.sql",
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
        ON regulatory_decision_evaluations
        TO {RUNTIME_ROLE}
        """
    )
    await admin.execute(
        f"""
        GRANT SELECT, INSERT, UPDATE
        ON regulatory_rule_sets
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
        PostgresDecisionEvaluationIdempotency,
        PostgresRuleSetRepository,
    ]
]:
    admin_url, runtime_url = postgres_urls
    admin = await asyncpg.connect(admin_url)
    await admin.execute(
        "TRUNCATE TABLE regulatory_decision_evaluations, regulatory_rule_sets"
    )
    pool = await asyncpg.create_pool(runtime_url, min_size=1, max_size=6)
    assert pool is not None
    try:
        yield (
            admin,
            pool,
            PostgresDecisionEvaluationIdempotency(pool),
            PostgresRuleSetRepository(pool),
        )
    finally:
        await pool.close()
        await admin.close()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_commit_and_idempotent_replay_preserve_exact_response(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    admin, _, store, _ = stores
    request = _request()
    response = _response()
    fingerprint = _request_fingerprint(request)

    committed = await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
        input_fingerprint=INPUT_FP,
        request=request,
        response=response,
    )
    replay = await store.replay(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
        replay_key=REPLAY_KEY,
        input_fingerprint=INPUT_FP,
    )

    assert committed.created is True
    assert replay is not None
    assert replay.response == response
    assert await admin.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_new_command_key_replays_same_semantic_decision_without_duplicate(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    admin, _, store, _ = stores
    request = _request()
    response = _response()
    fingerprint = _request_fingerprint(request)

    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=fingerprint,
        input_fingerprint=INPUT_FP,
        request=request,
        response=response,
    )
    replay = await store.replay(
        tenant_id=TENANT_A,
        idempotency_key="r-cap-09-postgres-0002",
        request_fingerprint=fingerprint,
        replay_key=REPLAY_KEY,
        input_fingerprint=INPUT_FP,
    )

    assert replay is not None
    assert replay.response == response
    assert await admin.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_replay_key_cannot_be_reused_for_different_semantic_input(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    _, _, store, _ = stores
    request = _request()
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_request_fingerprint(request),
        input_fingerprint=INPUT_FP,
        request=request,
        response=_response(),
    )

    changed = _request(hs="0901.12.00")
    with pytest.raises(DecisionIdempotencyConflictError, match="semantic input"):
        await store.replay(
            tenant_id=TENANT_A,
            idempotency_key="r-cap-09-postgres-0002",
            request_fingerprint=_request_fingerprint(changed),
            replay_key=REPLAY_KEY,
            input_fingerprint="c" * 64,
        )


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_concurrent_duplicate_commit_converges_on_one_durable_decision(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    admin, _, store, _ = stores
    request = _request()
    fingerprint = _request_fingerprint(request)

    first, second = await asyncio.gather(
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            input_fingerprint=INPUT_FP,
            request=request,
            response=_response(evaluated_at=NOW + timedelta(seconds=1)),
        ),
        store.commit(
            tenant_id=TENANT_A,
            idempotency_key=IDEMPOTENCY_KEY,
            request_fingerprint=fingerprint,
            input_fingerprint=INPUT_FP,
            request=request,
            response=_response(evaluated_at=NOW + timedelta(seconds=2)),
        ),
    )

    assert sum(1 for item in (first, second) if item.created) == 1
    assert first.response == second.response
    assert await admin.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_decision_rls_defaults_deny_and_isolates_tenants(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    _, pool, store, _ = stores
    request = _request()
    await store.commit(
        tenant_id=TENANT_A,
        idempotency_key=IDEMPOTENCY_KEY,
        request_fingerprint=_request_fingerprint(request),
        input_fingerprint=INPUT_FP,
        request=request,
        response=_response(),
    )

    async with pool.acquire() as conn:
        assert await conn.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 0

    async with pool.acquire() as conn, conn.transaction():
        await conn.execute("SELECT set_config('baobab.tenant_id', $1, true)", TENANT_A)
        assert await conn.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 1

    async with pool.acquire() as conn, conn.transaction():
        await conn.execute("SELECT set_config('baobab.tenant_id', $1, true)", TENANT_B)
        assert await conn.fetchval("SELECT count(*) FROM regulatory_decision_evaluations") == 0


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_tenant_rule_set_repository_is_rls_scoped(
    stores: tuple[Any, Any, PostgresDecisionEvaluationIdempotency, PostgresRuleSetRepository],
) -> None:
    _, pool, _, rules = stores
    record = RuleSetRecord(
        rule_set_id="ruleset_tenant_a_001",
        corridor_profile="UG-ZA-COFFEE",
        assurance_state=AssuranceState.VERIFIED,
        fingerprint="d" * 64,
        legal_valid_from=NOW - timedelta(days=10),
        legal_valid_to=None,
        knowledge_from=NOW - timedelta(days=5),
        knowledge_to=None,
        scope="tenant",
        tenant_id=TENANT_A,
    )
    await rules.save(record)

    assert await rules.get(record.rule_set_id, tenant_id=TENANT_A) == record
    assert await rules.get(record.rule_set_id, tenant_id=TENANT_B) is None

    async with pool.acquire() as conn:
        assert await conn.fetchval(
            "SELECT count(*) FROM regulatory_rule_sets WHERE rule_set_id = $1",
            record.rule_set_id,
        ) == 0

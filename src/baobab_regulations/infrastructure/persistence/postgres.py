"""PostgreSQL repository skeleton (REG-2).

Requires asyncpg and a live database. Unit tests use in-memory repos;
this module is the production path once migrations are applied.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from baobab_regulations.domain.decisions.models import RegulatoryDecision
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState, DecisionOutcome, EnforcementClass
from baobab_regulations.domain.shared.ids import RegulatoryId


class PostgresDecisionRepository:
    """Append-only decision store backed by ``regulatory_decisions``."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def save(self, decision: RegulatoryDecision) -> None:
        sql = """
            INSERT INTO regulatory_decisions (
                decision_id, assessment_id, outcome, enforcement_class,
                reasons, recommended_disposition, explanation,
                rule_set_fingerprint, evaluated_at, legal_time, knowledge_time,
                provenance, replay_key, tenant_id
            ) VALUES (
                $1, $2, $3, $4,
                $5::jsonb, $6::jsonb, $7,
                $8, $9, $10, $11,
                $12::jsonb, $13, $14
            )
        """
        tenant_id = None
        if isinstance(decision.provenance, dict):
            tenant_id = decision.provenance.get("tenant_id")
        async with self._pool.acquire() as conn:
            await conn.execute(
                sql,
                str(decision.decision_id),
                str(decision.assessment_id),
                decision.outcome.value,
                decision.enforcement_class.value,
                [r.model_dump(mode="json") for r in decision.reasons],
                (
                    decision.recommended_disposition.model_dump(mode="json")
                    if decision.recommended_disposition
                    else None
                ),
                decision.explanation,
                decision.rule_set_fingerprint,
                decision.evaluated_at,
                decision.legal_time,
                decision.knowledge_time,
                decision.provenance,
                decision.replay_key,
                tenant_id,
            )

    async def get(self, decision_id: RegulatoryId) -> RegulatoryDecision | None:
        sql = "SELECT * FROM regulatory_decisions WHERE decision_id = $1"
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql, str(decision_id))
        if row is None:
            return None
        return _row_to_decision(dict(row))


class PostgresRuleSetRepository:
    """Rule-set metadata backed by ``regulatory_rule_sets``."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def save(self, record: RuleSetRecord) -> None:
        sql = """
            INSERT INTO regulatory_rule_sets (
                rule_set_id, corridor_profile, assurance_state, fingerprint,
                legal_valid_from, legal_valid_to, knowledge_from, knowledge_to,
                scope, tenant_id, brir_payload,
                compiler_id, compiler_version, compiled_target,
                compiled_entrypoint, compiled_artifact_fingerprint,
                derived_rule_ids, notes
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, $8,
                $9, $10, $11::jsonb,
                $12, $13, $14,
                $15, $16,
                $17::jsonb, $18
            )
            ON CONFLICT (rule_set_id) DO UPDATE SET
                corridor_profile = EXCLUDED.corridor_profile,
                assurance_state = EXCLUDED.assurance_state,
                fingerprint = EXCLUDED.fingerprint,
                legal_valid_from = EXCLUDED.legal_valid_from,
                legal_valid_to = EXCLUDED.legal_valid_to,
                knowledge_from = EXCLUDED.knowledge_from,
                knowledge_to = EXCLUDED.knowledge_to,
                scope = EXCLUDED.scope,
                tenant_id = EXCLUDED.tenant_id,
                brir_payload = EXCLUDED.brir_payload,
                compiler_id = EXCLUDED.compiler_id,
                compiler_version = EXCLUDED.compiler_version,
                compiled_target = EXCLUDED.compiled_target,
                compiled_entrypoint = EXCLUDED.compiled_entrypoint,
                compiled_artifact_fingerprint = EXCLUDED.compiled_artifact_fingerprint,
                derived_rule_ids = EXCLUDED.derived_rule_ids,
                notes = EXCLUDED.notes
        """
        async with self._pool.acquire() as conn, conn.transaction():
            if record.scope == "tenant" and record.tenant_id is not None:
                await conn.execute(
                    "SELECT set_config('baobab.tenant_id', $1, true)",
                    record.tenant_id,
                )
            await conn.execute(
                sql,
                record.rule_set_id,
                record.corridor_profile,
                record.assurance_state.value,
                record.fingerprint,
                record.legal_valid_from,
                record.legal_valid_to,
                record.knowledge_from,
                record.knowledge_to,
                record.scope,
                record.tenant_id,
                (
                    json.dumps(
                        record.brir_payload,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    if record.brir_payload is not None
                    else None
                ),
                record.compiler_id,
                record.compiler_version,
                record.compiled_target,
                record.compiled_entrypoint,
                record.compiled_artifact_fingerprint,
                json.dumps([str(x) for x in record.derived_rule_ids]),
                record.notes,
            )

    async def get(
        self,
        rule_set_id: str,
        *,
        tenant_id: str | None = None,
    ) -> RuleSetRecord | None:
        sql = "SELECT * FROM regulatory_rule_sets WHERE rule_set_id = $1"
        async with self._pool.acquire() as conn, conn.transaction():
            if tenant_id is not None:
                await conn.execute(
                    "SELECT set_config('baobab.tenant_id', $1, true)",
                    tenant_id,
                )
            row = await conn.fetchrow(sql, rule_set_id)
        if row is None:
            return None
        return _row_to_rule_set(dict(row))

    async def get_active_rule_set_id(
        self,
        *,
        corridor_profile: str,
        knowledge_time: datetime,
    ) -> str | None:
        sql = """
            SELECT rule_set_id
            FROM regulatory_rule_sets
            WHERE corridor_profile = $1
              AND assurance_state IN ('VERIFIED', 'CERTIFIED')
              AND knowledge_from <= $2
              AND (knowledge_to IS NULL OR knowledge_to > $2)
            ORDER BY knowledge_from DESC
            LIMIT 1
        """
        async with self._pool.acquire() as conn:
            value = await conn.fetchval(sql, corridor_profile, knowledge_time)
        return str(value) if value is not None else None


def _row_to_decision(row: dict[str, Any]) -> RegulatoryDecision:
    from baobab_regulations.domain.decisions.models import DecisionReason, RecommendedDisposition

    reasons = [DecisionReason.model_validate(r) for r in (row.get("reasons") or [])]
    disposition = row.get("recommended_disposition")
    return RegulatoryDecision(
        decision_id=RegulatoryId(row["decision_id"]),
        assessment_id=RegulatoryId(row["assessment_id"]),
        outcome=DecisionOutcome(row["outcome"]),
        enforcement_class=EnforcementClass(row["enforcement_class"]),
        reasons=reasons,
        recommended_disposition=(
            RecommendedDisposition.model_validate(disposition) if disposition else None
        ),
        explanation=row.get("explanation") or "",
        rule_set_fingerprint=row.get("rule_set_fingerprint") or "",
        evaluated_at=row["evaluated_at"],
        legal_time=row["legal_time"],
        knowledge_time=row["knowledge_time"],
        provenance=row.get("provenance") or {},
        replay_key=row.get("replay_key") or "",
    )


def _decode_jsonb(value: Any) -> Any:
    if isinstance(value, (str, bytes, bytearray)):
        return json.loads(value)
    return value


def _row_to_rule_set(row: dict[str, Any]) -> RuleSetRecord:
    brir_payload = _decode_jsonb(row.get("brir_payload"))
    derived_rule_ids = _decode_jsonb(row.get("derived_rule_ids")) or []
    if brir_payload is not None and not isinstance(brir_payload, dict):
        raise TypeError("regulatory_rule_sets.brir_payload must decode to an object")
    if not isinstance(derived_rule_ids, list):
        raise TypeError("regulatory_rule_sets.derived_rule_ids must decode to an array")

    return RuleSetRecord(
        rule_set_id=row["rule_set_id"],
        corridor_profile=row["corridor_profile"],
        assurance_state=AssuranceState(row["assurance_state"]),
        fingerprint=row["fingerprint"],
        legal_valid_from=row["legal_valid_from"],
        legal_valid_to=row.get("legal_valid_to"),
        knowledge_from=row["knowledge_from"],
        knowledge_to=row.get("knowledge_to"),
        brir_payload=brir_payload,
        compiler_id=row.get("compiler_id"),
        compiler_version=row.get("compiler_version"),
        compiled_target=row.get("compiled_target"),
        compiled_entrypoint=row.get("compiled_entrypoint"),
        compiled_artifact_fingerprint=row.get("compiled_artifact_fingerprint"),
        derived_rule_ids=[RegulatoryId(str(x)) for x in derived_rule_ids],
        scope=row.get("scope") or "platform",
        tenant_id=row.get("tenant_id"),
        notes=row.get("notes"),
    )

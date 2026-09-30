"""PostgreSQL repository skeleton (REG-2).

Requires asyncpg and a live database. Unit tests use in-memory repos;
this module is the production path once migrations are applied.
"""

from __future__ import annotations

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
                derived_rule_ids, notes
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, $8,
                $9::jsonb, $10
            )
            ON CONFLICT (rule_set_id) DO UPDATE SET
                corridor_profile = EXCLUDED.corridor_profile,
                assurance_state = EXCLUDED.assurance_state,
                fingerprint = EXCLUDED.fingerprint,
                legal_valid_from = EXCLUDED.legal_valid_from,
                legal_valid_to = EXCLUDED.legal_valid_to,
                knowledge_from = EXCLUDED.knowledge_from,
                knowledge_to = EXCLUDED.knowledge_to,
                derived_rule_ids = EXCLUDED.derived_rule_ids,
                notes = EXCLUDED.notes
        """
        async with self._pool.acquire() as conn:
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
                [str(x) for x in record.derived_rule_ids],
                record.notes,
            )

    async def get(self, rule_set_id: str) -> RuleSetRecord | None:
        sql = "SELECT * FROM regulatory_rule_sets WHERE rule_set_id = $1"
        async with self._pool.acquire() as conn:
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
            return await conn.fetchval(sql, corridor_profile, knowledge_time)


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


def _row_to_rule_set(row: dict[str, Any]) -> RuleSetRecord:
    return RuleSetRecord(
        rule_set_id=row["rule_set_id"],
        corridor_profile=row["corridor_profile"],
        assurance_state=AssuranceState(row["assurance_state"]),
        fingerprint=row["fingerprint"],
        legal_valid_from=row["legal_valid_from"],
        legal_valid_to=row.get("legal_valid_to"),
        knowledge_from=row["knowledge_from"],
        knowledge_to=row.get("knowledge_to"),
        derived_rule_ids=[RegulatoryId(x) for x in (row.get("derived_rule_ids") or [])],
        notes=row.get("notes"),
    )

-- REG-2: minimal durable stores for decisions and verified rule sets.
-- Append-only decisions; rule sets are metadata only (not BRIR bodies).
-- ADR-REG-0006, ADR-REG-0015, ADR-REG-0020, ADR-REG-0028.

BEGIN;

CREATE TABLE IF NOT EXISTS regulatory_decisions (
    decision_id            TEXT PRIMARY KEY,
    assessment_id          TEXT NOT NULL,
    outcome                TEXT NOT NULL,
    enforcement_class      TEXT NOT NULL,
    reasons                JSONB NOT NULL DEFAULT '[]'::jsonb,
    recommended_disposition JSONB,
    explanation            TEXT NOT NULL DEFAULT '',
    rule_set_fingerprint   TEXT NOT NULL DEFAULT '',
    evaluated_at           TIMESTAMPTZ NOT NULL,
    legal_time             TIMESTAMPTZ NOT NULL,
    knowledge_time         TIMESTAMPTZ NOT NULL,
    provenance             JSONB NOT NULL DEFAULT '{}'::jsonb,
    replay_key             TEXT NOT NULL DEFAULT '',
    tenant_id              TEXT,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_regulatory_decisions_tenant
    ON regulatory_decisions (tenant_id);
CREATE INDEX IF NOT EXISTS idx_regulatory_decisions_replay
    ON regulatory_decisions (replay_key);
CREATE INDEX IF NOT EXISTS idx_regulatory_decisions_knowledge
    ON regulatory_decisions (knowledge_time);

CREATE TABLE IF NOT EXISTS regulatory_rule_sets (
    rule_set_id        TEXT PRIMARY KEY,
    corridor_profile   TEXT NOT NULL,
    assurance_state    TEXT NOT NULL,
    fingerprint        TEXT NOT NULL,
    legal_valid_from   TIMESTAMPTZ NOT NULL,
    legal_valid_to     TIMESTAMPTZ,
    knowledge_from     TIMESTAMPTZ NOT NULL,
    knowledge_to       TIMESTAMPTZ,
    derived_rule_ids   JSONB NOT NULL DEFAULT '[]'::jsonb,
    notes              TEXT,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_regulatory_rule_sets_corridor_knowledge
    ON regulatory_rule_sets (corridor_profile, knowledge_from DESC);

COMMENT ON TABLE regulatory_decisions IS
    'Append-only regulatory decisions (PDP output). Operational enforcement is owned by domain PEPs.';
COMMENT ON TABLE regulatory_rule_sets IS
    'Verified/certified rule-set metadata for evaluation; bodies live in BRIR artefacts.';

COMMIT;

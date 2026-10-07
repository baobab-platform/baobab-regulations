-- R-CAP-09: production regulatory decision evaluation durability.
-- Adds governed BRIR/compiled-artifact metadata to rule sets and durable
-- canonical decision command/replay state. Operational enforcement remains
-- outside Regulations.

BEGIN;

ALTER TABLE regulatory_rule_sets
    ADD COLUMN IF NOT EXISTS scope TEXT NOT NULL DEFAULT 'platform',
    ADD COLUMN IF NOT EXISTS tenant_id TEXT,
    ADD COLUMN IF NOT EXISTS brir_payload JSONB,
    ADD COLUMN IF NOT EXISTS compiler_id TEXT,
    ADD COLUMN IF NOT EXISTS compiler_version TEXT,
    ADD COLUMN IF NOT EXISTS compiled_target TEXT,
    ADD COLUMN IF NOT EXISTS compiled_entrypoint TEXT,
    ADD COLUMN IF NOT EXISTS compiled_artifact_fingerprint TEXT;

ALTER TABLE regulatory_rule_sets
    DROP CONSTRAINT IF EXISTS ck_regulatory_rule_sets_scope,
    DROP CONSTRAINT IF EXISTS ck_regulatory_rule_sets_compiled_binding;

ALTER TABLE regulatory_rule_sets
    ADD CONSTRAINT ck_regulatory_rule_sets_scope
    CHECK (
        (scope = 'platform' AND tenant_id IS NULL)
        OR
        (scope = 'tenant' AND tenant_id ~ '^tn_[a-z0-9]+$')
    ),
    ADD CONSTRAINT ck_regulatory_rule_sets_compiled_binding
    CHECK (
        (
            brir_payload IS NULL
            AND compiler_id IS NULL
            AND compiler_version IS NULL
            AND compiled_target IS NULL
            AND compiled_entrypoint IS NULL
            AND compiled_artifact_fingerprint IS NULL
        )
        OR
        (
            jsonb_typeof(brir_payload) = 'object'
            AND char_length(compiler_id) > 0
            AND char_length(compiler_version) > 0
            AND char_length(compiled_target) > 0
            AND char_length(compiled_entrypoint) > 0
            AND compiled_artifact_fingerprint ~ '^[0-9a-f]{64}$'
        )
    );

CREATE INDEX IF NOT EXISTS idx_regulatory_rule_sets_scope_tenant
    ON regulatory_rule_sets (scope, tenant_id, rule_set_id);

ALTER TABLE regulatory_rule_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE regulatory_rule_sets FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS regulatory_rule_sets_scope_isolation
    ON regulatory_rule_sets;

CREATE POLICY regulatory_rule_sets_scope_isolation
    ON regulatory_rule_sets
    USING (
        scope = 'platform'
        OR tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    )
    WITH CHECK (
        scope = 'platform'
        OR tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

CREATE TABLE IF NOT EXISTS regulatory_decision_evaluations (
    decision_id            TEXT PRIMARY KEY,
    assessment_id          TEXT NOT NULL UNIQUE,
    tenant_id              TEXT NOT NULL,
    idempotency_key        TEXT NOT NULL,
    replay_key             TEXT NOT NULL,
    request_fingerprint    TEXT NOT NULL,
    input_fingerprint      TEXT NOT NULL,
    result_fingerprint     TEXT NOT NULL,
    contract_major         SMALLINT NOT NULL DEFAULT 1,
    rule_set_object_id     TEXT NOT NULL,
    rule_set_fingerprint   TEXT NOT NULL,
    outcome                TEXT NOT NULL,
    enforcement_class      TEXT NOT NULL,
    request_payload        JSONB NOT NULL,
    response_payload       JSONB NOT NULL,
    legal_time             TIMESTAMPTZ NOT NULL,
    knowledge_time         TIMESTAMPTZ NOT NULL,
    evaluated_at           TIMESTAMPTZ NOT NULL,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_regulatory_decision_evaluations_idempotency
        UNIQUE (tenant_id, idempotency_key),

    CONSTRAINT uq_regulatory_decision_evaluations_replay
        UNIQUE (tenant_id, replay_key),

    CONSTRAINT ck_regulatory_decision_evaluations_tenant
        CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),

    CONSTRAINT ck_regulatory_decision_evaluations_idempotency_key
        CHECK (
            char_length(idempotency_key) BETWEEN 16 AND 128
            AND idempotency_key ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'
        ),

    CONSTRAINT ck_regulatory_decision_evaluations_replay_key
        CHECK (
            char_length(replay_key) BETWEEN 16 AND 128
            AND replay_key ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'
        ),

    CONSTRAINT ck_regulatory_decision_evaluations_request_fingerprint
        CHECK (request_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_decision_evaluations_input_fingerprint
        CHECK (input_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_decision_evaluations_result_fingerprint
        CHECK (result_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_decision_evaluations_rule_set_fingerprint
        CHECK (rule_set_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_decision_evaluations_contract_major
        CHECK (contract_major = 1),

    CONSTRAINT ck_regulatory_decision_evaluations_outcome
        CHECK (
            outcome IN (
                'SATISFIED',
                'SATISFIED_WITH_REQUIREMENTS',
                'UNSATISFIED',
                'PROHIBITED',
                'INDETERMINATE',
                'NOT_APPLICABLE'
            )
        ),

    CONSTRAINT ck_regulatory_decision_evaluations_enforcement_class
        CHECK (enforcement_class IN ('E0', 'E1', 'E2', 'E3', 'E4')),

    CONSTRAINT ck_regulatory_decision_evaluations_request_object
        CHECK (jsonb_typeof(request_payload) = 'object'),

    CONSTRAINT ck_regulatory_decision_evaluations_response_object
        CHECK (jsonb_typeof(response_payload) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_regulatory_decision_evaluations_tenant_evaluated
    ON regulatory_decision_evaluations (tenant_id, evaluated_at DESC);

CREATE INDEX IF NOT EXISTS idx_regulatory_decision_evaluations_rule_set
    ON regulatory_decision_evaluations (
        tenant_id,
        rule_set_object_id,
        rule_set_fingerprint,
        evaluated_at DESC
    );

CREATE INDEX IF NOT EXISTS idx_regulatory_decision_evaluations_temporal
    ON regulatory_decision_evaluations (
        tenant_id,
        legal_time,
        knowledge_time,
        evaluated_at DESC
    );

ALTER TABLE regulatory_decision_evaluations ENABLE ROW LEVEL SECURITY;
ALTER TABLE regulatory_decision_evaluations FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS regulatory_decision_evaluations_tenant_isolation
    ON regulatory_decision_evaluations;

CREATE POLICY regulatory_decision_evaluations_tenant_isolation
    ON regulatory_decision_evaluations
    USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    )
    WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

COMMENT ON COLUMN regulatory_rule_sets.brir_payload IS
    'Typed BRIR semantic document used to reproduce the governed rule-set fingerprint and compiled policy artifact.';

COMMENT ON COLUMN regulatory_rule_sets.compiled_artifact_fingerprint IS
    'SHA-256 of the deterministic target artifact produced from brir_payload by the recorded compiler id/version.';

COMMENT ON TABLE regulatory_decision_evaluations IS
    'Append-oriented canonical R-CAP-09 decision command/replay records. Stores exact Shared request/response snapshots for deterministic replay; no operational domain state is mutated.';

COMMENT ON COLUMN regulatory_decision_evaluations.request_fingerprint IS
    'SHA-256 of the complete canonical request, including replay_key, for Idempotency-Key conflict detection.';

COMMENT ON COLUMN regulatory_decision_evaluations.input_fingerprint IS
    'SHA-256 of provider-neutral semantic input excluding replay_key and including trusted tenant context.';

COMMENT ON COLUMN regulatory_decision_evaluations.result_fingerprint IS
    'SHA-256 of the exact canonical decision response retained for integrity validation.';

COMMIT;

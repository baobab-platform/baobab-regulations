-- R-CAP-05: durable RTD-06 documentary evidence assessments and idempotency.
-- ADR-REG-0020 replay/reproducibility; ADR-REG-0028 tenant isolation.
--
-- This table is append-oriented. One tenant + Idempotency-Key owns exactly one
-- canonical request fingerprint and one canonical assessment result. The full
-- RTD-06 request/result payloads are retained so replay does not depend on
-- today's mutable Trade Docs or other domain state.

BEGIN;

CREATE TABLE IF NOT EXISTS regulatory_evidence_assessments (
    assessment_id                 TEXT PRIMARY KEY,
    tenant_id                     TEXT NOT NULL,
    idempotency_key               TEXT NOT NULL,
    request_fingerprint           TEXT NOT NULL,
    result_fingerprint            TEXT NOT NULL,
    contract_major                SMALLINT NOT NULL DEFAULT 1,
    regulatory_decision_object_id TEXT NOT NULL,
    requirement_object_id         TEXT NOT NULL,
    assessment_reason             TEXT NOT NULL,
    outcome                       TEXT NOT NULL,
    request_payload               JSONB NOT NULL,
    result_payload                JSONB NOT NULL,
    evaluated_at                  TIMESTAMPTZ NOT NULL,
    created_at                    TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_regulatory_evidence_assessment_idempotency
        UNIQUE (tenant_id, idempotency_key),

    CONSTRAINT ck_regulatory_evidence_assessment_tenant
        CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),

    CONSTRAINT ck_regulatory_evidence_assessment_idempotency_key
        CHECK (
            char_length(idempotency_key) BETWEEN 16 AND 128
            AND idempotency_key ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'
        ),

    CONSTRAINT ck_regulatory_evidence_assessment_request_fingerprint
        CHECK (request_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_evidence_assessment_result_fingerprint
        CHECK (result_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_evidence_assessment_contract_major
        CHECK (contract_major = 1),

    CONSTRAINT ck_regulatory_evidence_assessment_reason
        CHECK (
            assessment_reason IN (
                'INITIAL_EVIDENCE',
                'EVIDENCE_CHANGED',
                'VERIFICATION_CHANGED',
                'VALIDITY_CHANGED',
                'MANUAL_REVIEW',
                'REGULATORY_REASSESSMENT'
            )
        ),

    CONSTRAINT ck_regulatory_evidence_assessment_outcome
        CHECK (
            outcome IN (
                'SATISFIED',
                'UNSATISFIED',
                'INDETERMINATE',
                'NOT_APPLICABLE',
                'REVIEW_REQUIRED'
            )
        ),

    CONSTRAINT ck_regulatory_evidence_assessment_request_object
        CHECK (jsonb_typeof(request_payload) = 'object'),

    CONSTRAINT ck_regulatory_evidence_assessment_result_object
        CHECK (jsonb_typeof(result_payload) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_regulatory_evidence_assessments_tenant_evaluated
    ON regulatory_evidence_assessments (tenant_id, evaluated_at DESC);

CREATE INDEX IF NOT EXISTS idx_regulatory_evidence_assessments_requirement
    ON regulatory_evidence_assessments (tenant_id, requirement_object_id, evaluated_at DESC);

CREATE INDEX IF NOT EXISTS idx_regulatory_evidence_assessments_decision
    ON regulatory_evidence_assessments (
        tenant_id,
        regulatory_decision_object_id,
        evaluated_at DESC
    );

ALTER TABLE regulatory_evidence_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE regulatory_evidence_assessments FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS regulatory_evidence_assessments_tenant_isolation
    ON regulatory_evidence_assessments;

CREATE POLICY regulatory_evidence_assessments_tenant_isolation
    ON regulatory_evidence_assessments
    USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    )
    WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

COMMENT ON TABLE regulatory_evidence_assessments IS
    'Append-oriented Regulations-owned RTD-06 evidence assessments. Full request/result snapshots support durable idempotent replay; operational domain state remains outside Regulations.';

COMMENT ON COLUMN regulatory_evidence_assessments.request_fingerprint IS
    'SHA-256 of the canonical RTD-06 assessment request JSON used for tenant-scoped Idempotency-Key conflict detection.';

COMMENT ON COLUMN regulatory_evidence_assessments.result_fingerprint IS
    'SHA-256 of the canonical RTD-06 assessment result JSON used for persisted-state integrity checks.';

COMMENT ON COLUMN regulatory_evidence_assessments.request_payload IS
    'Historical RTD-06 request snapshot; retained so replay does not re-fetch mutable evidence facts.';

COMMENT ON COLUMN regulatory_evidence_assessments.result_payload IS
    'Historical RTD-06 Regulations-owned assessment result returned on idempotent replay.';

COMMIT;

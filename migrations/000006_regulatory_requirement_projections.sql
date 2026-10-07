-- R-CAP-10: authoritative pinned documentary requirement projections.
-- This table holds Regulations-owned RTD-06 facts, not TradeDocument state.
-- Only the separately governed ingestion path may append source-backed facts.
-- No UPDATE/DELETE permissions are granted to the capability runtime.
BEGIN;

CREATE TABLE IF NOT EXISTS regulatory_requirement_projections (
    reference_fingerprint CHAR(64) PRIMARY KEY,
    projection_fingerprint CHAR(64) NOT NULL,
    object_type TEXT NOT NULL,
    object_id TEXT NOT NULL,
    scope TEXT NOT NULL,
    tenant_id TEXT,
    reference_mode TEXT NOT NULL,
    version_kind TEXT,
    version_value TEXT,
    requirement_payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_reg_requirement_owner_type
        CHECK (object_type IN (
            'DOCUMENT_REQUIREMENT', 'PERMIT_REQUIREMENT', 'EVIDENCE_REQUIREMENT'
        )),
    CONSTRAINT ck_reg_requirement_scope
        CHECK (
            (scope = 'platform' AND tenant_id IS NULL)
            OR (scope = 'tenant' AND tenant_id ~ '^tn_[a-z0-9]+$')
        ),
    CONSTRAINT ck_reg_requirement_pinning
        CHECK (
            (reference_mode = 'IDENTITY_PINNED'
                AND version_kind IS NULL AND version_value IS NULL)
            OR (reference_mode = 'VERSION_PINNED'
                AND version_kind IN ('VERSION','REVISION','SEQUENCE','ETAG','CONTENT_HASH','OTHER')
                AND char_length(version_value) BETWEEN 1 AND 256)
        ),
    CONSTRAINT ck_reg_requirement_reference_fingerprint
        CHECK (reference_fingerprint ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_reg_requirement_projection_fingerprint
        CHECK (projection_fingerprint ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_reg_requirement_payload
        CHECK (jsonb_typeof(requirement_payload) = 'object')
);

CREATE INDEX IF NOT EXISTS idx_regulatory_requirement_identity
    ON regulatory_requirement_projections (
        object_type, object_id, scope, tenant_id
    );

ALTER TABLE regulatory_requirement_projections ENABLE ROW LEVEL SECURITY;
ALTER TABLE regulatory_requirement_projections FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS reg_requirement_read_isolation
    ON regulatory_requirement_projections;
CREATE POLICY reg_requirement_read_isolation
    ON regulatory_requirement_projections
    FOR SELECT
    USING (
        scope = 'platform'
        OR tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

-- Runtime roles must never write cross-tenant or platform-global requirements.
-- A separately governed privileged ingestion role is needed for public law.
DROP POLICY IF EXISTS reg_requirement_governed_insert
    ON regulatory_requirement_projections;
CREATE POLICY reg_requirement_governed_insert
    ON regulatory_requirement_projections
    FOR INSERT
    WITH CHECK (
        scope = 'tenant'
        AND tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

COMMENT ON TABLE regulatory_requirement_projections IS
    'Immutable RTD-06 Regulations documentary requirement projections; exact historical pins, no TradeDocument ownership.';

COMMIT;

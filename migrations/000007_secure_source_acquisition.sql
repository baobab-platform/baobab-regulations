-- REG-INGEST-02: evidence-only, tenant-bound, append-only acquisition records.
-- Rights and security decisions remain evidence, not publication authority.
-- Apply after 000002_source_registry.sql. PostgreSQL 17; ADR-REG-0013/0028.
BEGIN;

CREATE TABLE IF NOT EXISTS reg_source_acquisitions (
    acquisition_id UUID PRIMARY KEY,
    tenant_id TEXT NOT NULL CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),
    source_id TEXT NOT NULL REFERENCES authoritative_sources(source_id) ON DELETE RESTRICT,
    endpoint_ref TEXT NOT NULL,
    actor_ref TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL,
    UNIQUE (tenant_id, acquisition_id)
);

CREATE TABLE IF NOT EXISTS reg_source_acquisition_events (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    acquisition_id UUID NOT NULL,
    tenant_id TEXT NOT NULL CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),
    status TEXT NOT NULL CHECK (status IN (
        'REQUESTED','RIGHTS_CHECK_PENDING','AUTHORIZED','FETCHING',
        'ACQUIRED','QUARANTINED','FAILED','CANCELLED'
    )),
    details JSONB NOT NULL DEFAULT '{}'::jsonb
        CHECK (jsonb_typeof(details) = 'object'),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    FOREIGN KEY (tenant_id, acquisition_id)
        REFERENCES reg_source_acquisitions(tenant_id, acquisition_id)
        ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_reg_acq_events
    ON reg_source_acquisition_events (tenant_id, acquisition_id, event_id);

CREATE TABLE IF NOT EXISTS reg_source_acquisition_artefacts (
    artefact_id UUID PRIMARY KEY,
    acquisition_id UUID NOT NULL UNIQUE,
    tenant_id TEXT NOT NULL CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),
    source_id TEXT NOT NULL,
    endpoint_ref TEXT NOT NULL,
    storage_ref TEXT NOT NULL,
    content_hash_algorithm TEXT NOT NULL DEFAULT 'SHA-256'
        CHECK (content_hash_algorithm = 'SHA-256'),
    sha256 CHAR(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    size_bytes BIGINT NOT NULL CHECK (size_bytes > 0 AND size_bytes <= 33554432),
    declared_media_type TEXT NOT NULL,
    retrieved_at TIMESTAMPTZ NOT NULL,
    etag TEXT,
    last_modified TEXT,
    authenticity_state TEXT NOT NULL DEFAULT 'UNVERIFIED'
        CHECK (authenticity_state = 'UNVERIFIED'),
    FOREIGN KEY (tenant_id, acquisition_id)
        REFERENCES reg_source_acquisitions(tenant_id, acquisition_id)
        ON DELETE RESTRICT
);
-- Intentionally non-unique: equal hashes are NOT equal evidentiary identities.
CREATE INDEX IF NOT EXISTS idx_reg_acq_artefact_digest
    ON reg_source_acquisition_artefacts (tenant_id, sha256);

-- Follow the established PostgreSQL tenant GUC used by migration 000006.
-- Runtime roles must be non-superuser, non-BYPASSRLS, and have only INSERT/SELECT.
ALTER TABLE reg_source_acquisitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE reg_source_acquisitions FORCE ROW LEVEL SECURITY;
CREATE POLICY reg_source_acquisitions_read ON reg_source_acquisitions
    FOR SELECT USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );
CREATE POLICY reg_source_acquisitions_append ON reg_source_acquisitions
    FOR INSERT WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

ALTER TABLE reg_source_acquisition_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE reg_source_acquisition_events FORCE ROW LEVEL SECURITY;
CREATE POLICY reg_source_events_read ON reg_source_acquisition_events
    FOR SELECT USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );
CREATE POLICY reg_source_events_append ON reg_source_acquisition_events
    FOR INSERT WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

ALTER TABLE reg_source_acquisition_artefacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE reg_source_acquisition_artefacts FORCE ROW LEVEL SECURITY;
CREATE POLICY reg_source_artefacts_read ON reg_source_acquisition_artefacts
    FOR SELECT USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );
CREATE POLICY reg_source_artefacts_append ON reg_source_acquisition_artefacts
    FOR INSERT WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

COMMENT ON TABLE reg_source_acquisitions IS
    'Tenant-scoped governed source-acquisition requests, not regulatory truth.';
COMMENT ON TABLE reg_source_acquisition_events IS
    'Append-only status, rights and security evidence. No untrusted headers or signed URLs.';
COMMENT ON TABLE reg_source_acquisition_artefacts IS
    'Immutable metadata referencing private quarantine; no source bytes or extracted text.';

COMMIT;

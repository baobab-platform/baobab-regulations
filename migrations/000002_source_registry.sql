-- REG-3: authoritative source registry, artefacts, provenance links.
-- ADR-REG-0003, ADR-REG-0011, ADR-REG-0012, ADR-REG-0014.

BEGIN;

CREATE TABLE IF NOT EXISTS authoritative_sources (
    source_id      TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    publisher      TEXT NOT NULL,
    home_uri       TEXT,
    jurisdiction   TEXT,
    regime         TEXT,
    trust_tier     TEXT NOT NULL DEFAULT 'unknown',
    notes          TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS source_artefacts (
    artefact_id    TEXT PRIMARY KEY,
    source_id      TEXT NOT NULL REFERENCES authoritative_sources (source_id),
    uri            TEXT NOT NULL,
    retrieved_at   TIMESTAMPTZ NOT NULL,
    content_hash   TEXT NOT NULL,
    rights_class   TEXT NOT NULL,
    media_type     TEXT,
    title          TEXT,
    text_body      TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_source_artefacts_source
    ON source_artefacts (source_id);
CREATE INDEX IF NOT EXISTS idx_source_artefacts_hash
    ON source_artefacts (content_hash);

CREATE TABLE IF NOT EXISTS provenance_links (
    link_id        TEXT PRIMARY KEY,
    subject_id     TEXT NOT NULL,
    subject_kind   TEXT NOT NULL,
    artefact_id    TEXT REFERENCES source_artefacts (artefact_id),
    source_id      TEXT REFERENCES authoritative_sources (source_id),
    citation       TEXT,
    created_at     TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_provenance_subject
    ON provenance_links (subject_id);

CREATE TABLE IF NOT EXISTS derived_rule_registrations (
    rule_id        TEXT PRIMARY KEY,
    instrument_id  TEXT NOT NULL,
    provision_ids  JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_id      TEXT NOT NULL REFERENCES authoritative_sources (source_id),
    artefact_id    TEXT NOT NULL REFERENCES source_artefacts (artefact_id),
    rights_class   TEXT NOT NULL,
    assurance_state TEXT NOT NULL,
    legal_basis_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at     TIMESTAMPTZ NOT NULL
);

COMMENT ON TABLE authoritative_sources IS
    'Publisher/source registry — not artefact bodies (ADR-REG-0011).';
COMMENT ON TABLE source_artefacts IS
    'Retrieved artefacts with mandatory content_hash and rights_class (ADR-REG-0012).';
COMMENT ON TABLE provenance_links IS
    'Evidentiary chain edges for decisions and derived rules (ADR-REG-0014).';

COMMIT;

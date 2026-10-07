-- R-CAP-06: canonical RTD-08 transactional event outbox.
-- ADR-SHARED-024 requires the active Regulations event surface and recommends
-- state/event-intent atomicity. ADR-REG-0028 governs tenant isolation.

BEGIN;

-- No provider was active before R-CAP-06, so no production assessment should
-- exist without its canonical event intent. Refuse a first-time migration over
-- unexplained pre-existing rows rather than silently creating an event gap.
DO $rcap06$
BEGIN
    IF to_regclass('public.regulatory_event_outbox') IS NULL
       AND EXISTS (SELECT 1 FROM regulatory_evidence_assessments)
    THEN
        RAISE EXCEPTION
            'R-CAP-06 requires explicit assessment outbox backfill before migration';
    END IF;
END
$rcap06$;

CREATE TABLE IF NOT EXISTS regulatory_event_outbox (
    outbox_id             UUID PRIMARY KEY,
    event_id              UUID NOT NULL UNIQUE,
    assessment_id         TEXT NOT NULL UNIQUE
                          REFERENCES regulatory_evidence_assessments (assessment_id)
                          ON DELETE RESTRICT,
    tenant_id             TEXT NOT NULL,
    event_type            TEXT NOT NULL,
    source                TEXT NOT NULL,
    subject               TEXT NOT NULL,
    correlation_id        UUID NOT NULL,
    idempotency_key       TEXT NOT NULL,
    envelope_fingerprint  TEXT NOT NULL,
    envelope              JSONB NOT NULL,
    status                TEXT NOT NULL DEFAULT 'PENDING',
    attempt_count         INTEGER NOT NULL DEFAULT 0,
    next_attempt_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    lease_expires_at      TIMESTAMPTZ,
    published_at          TIMESTAMPTZ,
    last_error_code       TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_regulatory_event_outbox_command
        UNIQUE (tenant_id, idempotency_key, event_type),

    CONSTRAINT ck_regulatory_event_outbox_tenant
        CHECK (tenant_id ~ '^tn_[a-z0-9]+$'),

    CONSTRAINT ck_regulatory_event_outbox_type
        CHECK (
            event_type =
            'com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1'
        ),

    CONSTRAINT ck_regulatory_event_outbox_source
        CHECK (source = 'urn:baobab-platform:service:baobab-regulations'),

    CONSTRAINT ck_regulatory_event_outbox_subject
        CHECK (
            subject =
            'regulatory-evidence-assessment:' || assessment_id
        ),

    CONSTRAINT ck_regulatory_event_outbox_idempotency_key
        CHECK (
            char_length(idempotency_key) BETWEEN 16 AND 128
            AND idempotency_key ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'
        ),

    CONSTRAINT ck_regulatory_event_outbox_fingerprint
        CHECK (envelope_fingerprint ~ '^[0-9a-f]{64}$'),

    CONSTRAINT ck_regulatory_event_outbox_status
        CHECK (
            status IN (
                'PENDING',
                'PUBLISHING',
                'PUBLISHED',
                'RETRY',
                'DEAD_LETTER'
            )
        ),

    CONSTRAINT ck_regulatory_event_outbox_attempt_count
        CHECK (attempt_count >= 0),

    CONSTRAINT ck_regulatory_event_outbox_error_code
        CHECK (last_error_code IS NULL OR char_length(last_error_code) <= 100),

    CONSTRAINT ck_regulatory_event_outbox_publish_state
        CHECK (
            (status = 'PUBLISHED' AND published_at IS NOT NULL)
            OR (status <> 'PUBLISHED' AND published_at IS NULL)
        ),

    CONSTRAINT ck_regulatory_event_outbox_lease_state
        CHECK (
            status <> 'PUBLISHING'
            OR lease_expires_at IS NOT NULL
        ),

    CONSTRAINT ck_regulatory_event_outbox_envelope_object
        CHECK (jsonb_typeof(envelope) = 'object'),

    CONSTRAINT ck_regulatory_event_outbox_envelope_identity
        CHECK (
            envelope->>'specversion' = '1.0'
            AND envelope->>'id' = event_id::text
            AND envelope->>'type' = event_type
            AND envelope->>'source' = source
            AND envelope->>'subject' = subject
            AND envelope->>'tenantid' = tenant_id
            AND envelope->>'idempotencykey' = idempotency_key
            AND envelope->>'correlationid' = correlation_id::text
            AND envelope->>'baobabscope' = 'tenant'
            AND envelope->>'datacontenttype' = 'application/json'
            AND envelope->>'dataschema' =
                'https://contracts.baobab-platform.com/regulatory-document-exchange/v1/events.schema.json#/$defs/requirementSatisfactionEvaluatedEventData'
            AND envelope#>>'{data,tenant_id}' = tenant_id
            AND envelope#>>'{data,result,assessment_reference,object_id}' = assessment_id
        )
);

CREATE INDEX IF NOT EXISTS idx_regulatory_event_outbox_dispatch
    ON regulatory_event_outbox (tenant_id, status, next_attempt_at, created_at);

CREATE INDEX IF NOT EXISTS idx_regulatory_event_outbox_lease
    ON regulatory_event_outbox (tenant_id, lease_expires_at)
    WHERE status = 'PUBLISHING';

ALTER TABLE regulatory_event_outbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE regulatory_event_outbox FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS regulatory_event_outbox_tenant_isolation
    ON regulatory_event_outbox;

CREATE POLICY regulatory_event_outbox_tenant_isolation
    ON regulatory_event_outbox
    USING (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    )
    WITH CHECK (
        tenant_id = NULLIF(current_setting('baobab.tenant_id', true), '')
    );

COMMENT ON TABLE regulatory_event_outbox IS
    'Tenant-scoped transactional outbox for canonical Shared RTD-08 Regulations events. Delivery is at least once; retries retain the original CloudEvent id.';

COMMENT ON COLUMN regulatory_event_outbox.envelope IS
    'Complete canonical Shared CloudEvents envelope. Relays publish this object unchanged, not data alone.';

COMMENT ON COLUMN regulatory_event_outbox.envelope_fingerprint IS
    'SHA-256 of canonical envelope JSON. Status changes must never alter event identity or payload.';

COMMIT;

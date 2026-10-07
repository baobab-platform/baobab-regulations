# Migrations

PostgreSQL is the planned canonical store for regulatory state, temporal data,
governance, and audit (ADR-REG-0006, ADR-REG-0015).

## Applied (REG-2 / REG-3 / R-CAP-05 / R-CAP-06)

| File | Purpose |
|------|---------|
| `000001_regulatory_decisions.sql` | Append-only `regulatory_decisions` + `regulatory_rule_sets` metadata |
| `000002_source_registry.sql` | `authoritative_sources`, `source_artefacts`, `provenance_links`, derived-rule registrations |
| `000003_regulatory_evidence_assessments.sql` | Durable RTD-06 assessment snapshots, tenant-scoped idempotency and PostgreSQL RLS |
| `000004_regulatory_event_outbox.sql` | Transactional RTD-08 canonical event outbox with tenant RLS, leases, retry and dead-letter state |

Apply against the compose database:

```bash
docker compose up -d postgres
psql "postgres://baobab:baobab@localhost:5432/baobab_regulations" \
  -f migrations/000001_regulatory_decisions.sql \
  -f migrations/000002_source_registry.sql \
  -f migrations/000003_regulatory_evidence_assessments.sql \
  -f migrations/000004_regulatory_event_outbox.sql
```

Unit tests keep in-memory adapters for deterministic isolation. R-CAP-05 adds a
real PostgreSQL adapter for documentary evidence assessments. Every assessment
operation binds the trusted tenant through a transaction-local
`baobab.tenant_id` setting; the table has ENABLE + FORCE ROW LEVEL SECURITY and
defaults to no tenant-private rows when that context is absent. Production still
requires the infrastructure-owned separation between migrator/table-owner and
non-superuser runtime roles described by ADR-REG-0028.

R-CAP-06 writes the canonical
`com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1`
event intent in the same PostgreSQL transaction as a newly committed evidence
assessment. The relay uses tenant-scoped lease/retry state and publishes the
complete Shared CloudEvents envelope unchanged. A live broker adapter remains a
deployment integration concern behind the provider-neutral publisher port.

The other active RTD-08 event,
`com.baobab-platform.regulations.document-requirements.determined.v1`, is not
emitted from `regulations.requirement.resolve`: that capability is an exact
read of an already-established requirement, not the write operation that
determined the requirement set.

## Not yet

- Instrument / provision body tables
- Pack activation metadata

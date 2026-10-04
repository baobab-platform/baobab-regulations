# Migrations

PostgreSQL is the planned canonical store for regulatory state, temporal data,
governance, and audit (ADR-REG-0006, ADR-REG-0015).

## Applied (REG-2 / REG-3)

| File | Purpose |
|------|---------|
| `000001_regulatory_decisions.sql` | Append-only `regulatory_decisions` + `regulatory_rule_sets` metadata |
| `000002_source_registry.sql` | `authoritative_sources`, `source_artefacts`, `provenance_links`, derived-rule registrations |

Apply against the compose database:

```bash
docker compose up -d postgres
psql "postgres://baobab:baobab@localhost:5432/baobab_regulations" \
  -f migrations/000001_regulatory_decisions.sql \
  -f migrations/000002_source_registry.sql
```

Unit tests use in-memory repositories. Postgres skeletons are the production path.

## Not yet

- Outbox for regulatory events
- Instrument / provision body tables
- Pack activation metadata

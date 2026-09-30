# Migrations

PostgreSQL is the planned canonical store for regulatory state, temporal data,
governance, and audit (ADR-REG-0006, ADR-REG-0015).

## Applied (REG-2)

| File | Purpose |
|------|---------|
| `000001_regulatory_decisions.sql` | Append-only `regulatory_decisions` + `regulatory_rule_sets` metadata |

Apply against the compose database:

```bash
docker compose up -d postgres
psql "postgres://baobab:baobab@localhost:5432/baobab_regulations" \
  -f migrations/000001_regulatory_decisions.sql
```

Unit tests continue to use `InMemoryDecisionRepository` /
`InMemoryRuleSetRepository`. `PostgresDecisionRepository` /
`PostgresRuleSetRepository` are the production skeleton (asyncpg pool).

## Not yet

- Outbox for regulatory events
- Instrument / provision / source artefact tables
- Pack activation metadata

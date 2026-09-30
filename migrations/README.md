# Migrations

PostgreSQL is the planned canonical store for regulatory state, temporal data,
governance, and audit (ADR-REG-0006, ADR-REG-0015).

No production migrations are activated in the scaffold. The first candidate
tables will cover:

- `regulatory_decisions` (immutable decision records + replay keys)
- outbox for regulatory events
- rule-set / pack activation metadata

Until then, the offline `InMemoryDecisionRepository` is used by tests and the
reference example.

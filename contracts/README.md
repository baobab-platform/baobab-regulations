# Contracts

This directory holds **pinned** contract dependencies consumed or published by
`baobab-regulations`.

## Consumed (from `baobab-platform/shared`)

- Platform context / organisation / legal-entity / market / trade-lane identity
  shapes (Control Plane owns the truth; Regulations only holds references —
  ADR-REG-0026).
- Capability grant / binding vocabulary used to authorise Regulations access
  (ADR-REG-0002, ADR-REG-0030).
- Shared CloudEvents envelope and RFC 9457 problem-details profiles (when
  event emission is activated).

## Published (planned)

- `regulations.decision.v1` — wire shape for `RegulatoryDecision`
- `regulations.assessment.requested.v1` / `regulations.assessment.completed.v1`

## Draft (REG-1, local only)

Under `contracts/events/`:

- `regulations.evaluation.requested.v0.json`
- `regulations.evaluation.completed.v0.json`

These are **draft** schemas for audit emission. They are not catalogued in Shared
and must not be treated as stable public API until promoted.

Until shared contracts are pinned, domain models under
`src/baobab_regulations/domain/` remain the source of truth for regulatory types.
Do not redefine Control Plane or IAM identities here.

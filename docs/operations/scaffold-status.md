# Scaffold status — baobab-regulations

**Date:** 2026-09-30  
**Stage:** Implementation scaffold activated (Foundation + execution-plane skeleton)  
**Audit remediation:** repository.yaml convention, jurisdiction≠regime, evaluator namespace, temporal typing, import order, CONTRIBUTING

## Activated in this scaffold

| Area | Status |
|------|--------|
| Python package `baobab_regulations` (src layout, uv/hatch) | Done |
| Domain: shared enums, bitemporal interval, context, decision models | Done |
| Domain: instruments, provisions, regimes, rule-set records (REG-2) | Done |
| Application: evaluator + repository ports, `EvaluationService` | Done |
| Infrastructure: in-memory + Postgres decision/rule-set repos | Done |
| Tenancy: fail-closed `require_tenant_context` | Done |
| API: FastAPI `/healthz`, `/readyz` | Done |
| Migrations: `000001_regulatory_decisions.sql` | Done |
| Tests: unit (reference evaluator, platform context, aggregates) | Done |
| Example: UG→ZA coffee reference evaluation (ADR-REG-0027) | Done |
| Local compose: PostgreSQL 17 + OPA | Done |
| `.baobab` + capability-provider planned keys | Done |
| ADR programme ADR-REG-0001 … 0030 | Already on upstream `main` |

## Explicitly not activated yet

- Live OPA/Rego compilation from BRIR
- Knowledge plane (Haystack, Docling, Qdrant, LangGraph)
- Source ingestion adapters and rights policy (REG-3)
- BRIR v0 + applicability (REG-4)
- Jurisdiction packs / marketplace (ADR-REG-0029)
- Production evaluation HTTP routes and authn/z
- Application-specific Foundation CI workflows beyond template leftovers
- Signed pack distribution and commercial metering (ADR-REG-0030)

## Guiding constraints carried into code

1. **PDP only** — Regulations decides; domain PEPs enforce (ADR-REG-0019).
2. **Platform context is referenced, never owned** (ADR-REG-0026).
3. **Commercial packaging must not alter regulatory truth** (ADR-REG-0030).
4. **AI is subordinate** — reference evaluator is deterministic and offline.
5. **Domain must not import infrastructure** — enforced by architecture tests.
6. **Jurisdiction ≠ regime** — regimes (e.g. AfCFTA) are `RegimeCode` / `regulatory_regimes`, never `JurisdictionRoleKind` or `JurisdictionCode` (ADR-REG-0017, ADR-REG-0026).

## Next recommended gates

Follow **[implementation-plan.md](./implementation-plan.md)**.

**REG-1 + REG-2 done on branch.** Next: **REG-3** (source registry) or **REG-4** (BRIR v0). Do not start live OPA, ingestion, AI, packs, or commercial work before REG-5 coffee goldens are green against BRIR.

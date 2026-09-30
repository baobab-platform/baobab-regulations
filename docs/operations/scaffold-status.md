# Scaffold status — baobab-regulations

**Date:** 2026-09-30  
**Stage:** Implementation scaffold activated (Foundation + execution-plane skeleton)  
**Audit remediation:** repository.yaml convention, jurisdiction≠regime, evaluator namespace, temporal typing, import order, CONTRIBUTING

## Activated in this scaffold

| Area | Status |
|------|--------|
| Python package `baobab_regulations` (src layout, uv/hatch) | Done |
| Domain: shared enums, bitemporal interval, context, decision models | Done |
| Application: evaluator + repository ports, `EvaluationService` | Done |
| Infrastructure: in-memory decision repo, offline `ReferenceEvaluator` under `infrastructure.evaluation` | Done |
| Tenancy: fail-closed `require_tenant_context` | Done |
| API: FastAPI `/healthz`, `/readyz` | Done |
| Tests: unit (reference evaluator), architecture boundary, API health | Done |
| Example: UG→ZA coffee reference evaluation (ADR-REG-0027) | Done |
| Local compose: PostgreSQL 17 + OPA | Done |
| `.baobab` + `.devcontainer` activation files (platform `repository.yaml` shape) | Done |
| ADR programme ADR-REG-0001 … 0030 | Already on upstream `main` |

## Explicitly not activated yet

- PostgreSQL migrations for canonical regulatory aggregates
- Live OPA/Rego compilation from BRIR (`infrastructure.opa` reserved, empty)
- Knowledge plane (Haystack, Docling, Qdrant, LangGraph)
- Source ingestion adapters and rights policy
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

## Audit fixes applied (pre-merge)

| Issue | Resolution |
|-------|------------|
| `.baobab/repository.yaml` non-platform dialect | Replaced with `schema_version: 1` shape (lifecycle, capabilities, package_managers, environment.baobab_dev, artifacts, security.sast_provider) matching baobab-cp / baobab-pulse / shared |
| `JurisdictionRoleKind.PREFERENTIAL_REGIME` + `JurisdictionCode("AfCFTA")` | Removed; AfCFTA modelled as `RegimeCode` on `origin_regime` / `regulatory_regimes` |
| Ruff I import order in `domain/shared` and `tenancy` | Alphabetical isort order |
| `ReferenceEvaluator` under `infrastructure.opa` | Moved to `infrastructure.evaluation.reference`; `opa` package reserved for live OPA |
| `RuleSetRepositoryPort.knowledge_time: str` | Typed as `datetime` |
| CONTRIBUTING nabhold / `.nabhold` paths | Updated to baobab-platform / `.baobab` |

## Next recommended gates

1. Accept / stabilise ADR-REG-0001…0030 status on `main`.
2. Open PR for this scaffold from `feat/regulations-scaffold`.
3. Introduce `migrations/` for minimal `regulatory_decisions` table.
4. Wire OPA HTTP evaluator behind `RegulatoryPolicyEvaluatorPort` in `infrastructure.opa`.
5. Land first verified BRIR fragment for UG→ZA green coffee.
6. Activate knowledge-plane dependency group only when source ingestion begins.

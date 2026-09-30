# Gate REG — Implementation Plan from ADR-REG-0001…0030

**Status:** Active working plan  
**Date:** 2026-09-30  
**Repo:** `baobab-platform/baobab-regulations`  
**Branch / PR:** `feat/regulations-scaffold` → [PR #4](https://github.com/baobab-platform/baobab-regulations/pull/4)

## Gate sequence

```text
REG-0  Scaffold + invariants          DONE
REG-1  Platform contracts + tenancy   DONE
REG-2  Canonical aggregates + schema  DONE
REG-3  Source registry + provenance   NEXT (or REG-4)
REG-4  BRIR v0 + applicability
REG-5  Evaluation engine + UG→ZA coffee golden
REG-6  Persistence + replay store
REG-7  Live OPA adapter (optional path)
REG-8–12  Ingestion, AI, events, packs, commercial
```

## REG-2 (done)

Domain: `RegulatoryInstrument`, `Provision`, `DerivedRule`, `RegulatoryAuthority`, `Jurisdiction`, `RegulatoryRegime`, `RuleSetRecord`.

Persistence: `migrations/000001_regulatory_decisions.sql`; in-memory append-only decisions + VERIFIED/CERTIFIED rule sets; Postgres skeletons via asyncpg.

## Follow-now

1. REG-3 source registry / rights, **or** REG-4 BRIR v0 + coffee fragment from `ReferenceEvaluator`
2. REG-5 golden cases against BRIR before OPA / packs / commercial

Full matrix: `artifacts/gate-reg-implementation-plan.md` (local project).

# Gate REG — Implementation Plan from ADR-REG-0001…0030

**Status:** Active working plan  
**Date:** 2026-09-30  
**Repo:** `baobab-platform/baobab-regulations`  
**Branch / PR:** `feat/regulations-scaffold` → [PR #4](https://github.com/baobab-platform/baobab-regulations/pull/4)  
**ADR status on main:** Proposed (not Accepted). Treat as normative *target* unless an ADR is superseded.  
**Rule:** Follow this document in order. Do not skip a gate because a later ADR is more interesting. Do not let commercial, AI, or pack-marketplace work alter regulatory truth.

---

## 0. How to use this plan

1. Complete the current gate’s **exit criteria** before starting the next.
2. Every change must cite the ADR(s) it implements.
3. If an ADR conflicts with code, stop and record the conflict — do not silently invent a third model.
4. Keep `docs/operations/scaffold-status.md` in sync after each gate.
5. Prefer small PRs on `feat/regulations-scaffold` (or successor `feat/reg-N-*` branches) over one mega-merge.

### Invariants (never violate)

| ID | Invariant | ADR |
|----|-----------|-----|
| INV-1 | Regulations is a **PDP**. Domain engines (Trade, ERP, Pulse) are **PEPs**. | 0001, 0018, 0019 |
| INV-2 | Platform context (tenant, org, legal entity, market, trade lane) is **referenced, never owned**. | 0026 |
| INV-3 | **Jurisdiction ≠ country ≠ market ≠ legal entity ≠ regime**. AfCFTA is a regime. | 0007, 0017, 0026, 0027 |
| INV-4 | Authoritative source ≠ artefact ≠ representation ≠ interpretation ≠ derived rule. | 0003 |
| INV-5 | Decision **outcome** ≠ **enforcement class** ≠ operational disposition. | 0004, 0018 |
| INV-6 | Commercial entitlement must not change regulatory truth. | 0030 |
| INV-7 | AI may propose; only verified knowledge may execute at E3/E4. | 0004, 0021, 0022 |
| INV-8 | Domain must not import infrastructure. | scaffold + 0006 |
| INV-9 | Evaluation is bitemporal: `legal_time` and `knowledge_time` are `datetime`. | 0015, 0020 |
| INV-10 | Tenant isolation is defence-in-depth; `tenant_id` alone is not enough. | 0028 |

### Capability namespace (planned; not catalogued)

- `regulations.context.resolve`
- `regulations.decision.evaluate`
- `regulations.change.subscribe`
- `regulations.pack.compose`

Do not invent additional `regulations.*` keys without Shared / EA-02 census.

---

## 1. ADR → implementation mapping

See local `artifacts/gate-reg-implementation-plan.md` for the full ADR→gate matrix (0001–0030).

---

## 2. Current baseline

REG-0 done on PR #4. REG-1 implemented on this branch (capability-provider, context redemption, request scope, draft audit events).

---

## 3. Gate sequence (normative order)

```text
REG-0  Scaffold + invariants          DONE (PR #4)
REG-1  Platform contracts + tenancy   DONE (this branch)
REG-2  Canonical aggregates + schema  NEXT
REG-3  Source registry + provenance
REG-4  BRIR v0 + applicability
REG-5  Evaluation engine + UG→ZA coffee golden
REG-6  Persistence + replay store
REG-7  Live OPA adapter (optional path)
REG-8  Ingestion adapters (provider-neutral)
REG-9  AI-assist behind verification
REG-10 Change events + subscriptions
REG-11 Packs / coverage manifests
REG-12 Commercial entitlements (truth-preserving)
```

---

## REG-1 — Platform contracts, capabilities, tenancy

**Status:** IMPLEMENTED on `feat/regulations-scaffold` (2026-09-30)

Deliverables: capability-provider planned keys; draft audit events; PlatformContextRef + context_id; request-scope hooks; resolve_platform_context; unit tests.

---

## REG-2 — Canonical regulatory aggregates + first migration

**ADRs:** 0006, 0007, 0008, 0015  
**Status:** NEXT

Domain types: RegulatoryInstrument, Provision, DerivedRule, RegulatoryAuthority, Jurisdiction, RegulatoryRegime.  
First SQL: regulatory_decisions (append-only), regulatory_rule_sets.

---

## Follow-now backlog

1. REG-2.1 domain types for instrument / provision / derived rule / regime
2. REG-2.2 migrations/000001_regulatory_decisions.sql + postgres repo skeleton
3. REG-4.1 BRIR v0 schema + coffee fragment from ReferenceEvaluator

Do not start REG-7–12 until REG-5 coffee goldens are green against BRIR.

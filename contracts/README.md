# Contracts

This directory documents contract dependencies consumed or published by
`baobab-regulations`.

Canonical cross-repository contracts are governed in
`baobab-platform/shared`. This repository must pin and consume those
contracts at runtime; it must not fork their wire schemas locally.

## Consumed from Shared

- Control Plane context / organisation / legal-entity / market identity.
- Capability grant / binding vocabulary.
- Canonical CloudEvents envelope, idempotency and RFC 9457 problem-details.
- `contracts/cross-engine-reference/v1` — ADR-SHARED-021 / RTD-05.
- `contracts/regulatory-document-exchange/v1` — ADR-SHARED-022 / RTD-06.
- `contracts/regulatory-document-assessment/v1` — ADR-SHARED-024 / RTD-08 Regulations-owned AsyncAPI publication surface.

RTD-06 gives Regulations the canonical wire surfaces for:

```text
RegulatoryDocumentRequirementProjection
RegulatoryDocumentRequirementSet
DocumentEvidenceAssessmentRequest
DocumentEvidenceAssessmentResult
CrossEngineObjectReference
```

and the Regulations-owned synchronous operations:

```text
POST /v1/documentary-requirements/resolve
POST /v1/documentary-evidence/assessments
```

## Trade Docs boundary

Regulations consumes Trade Docs documentary facts through pinned
`DOCUMENT_VERSION` references and bounded `DocumentEvidenceFactBundle`
projections.

It does not consume Trade Docs tables and it does not create a competing
TradeDocument aggregate.

The key invariants are:

```text
DocumentRequirement != TradeDocument
DocumentVerification != RequirementSatisfaction
EvidenceOffered != EvidenceAccepted
RequirementSatisfaction != operational enforcement
```

## Active RTD-08 event authority

ADR-SHARED-024 / RTD-08 activates `baobab-regulations` as the canonical
`regulations` event-context steward/producer for:

```text
com.baobab-platform.regulations.document-requirements.determined.v1
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
```

Their AsyncAPI surface is canonical in Shared:

```text
contracts/regulatory-document-assessment/v1/asyncapi.yaml
```

Regulations may consume the RTD-07 Trade Docs fact:

```text
com.baobab-platform.documents.regulatory-evidence.offered.v1
```

without acquiring `documents` producer authority.

ACTIVE contract authority does not claim that this repository already has a
production outbox, relay or broker deployment.

## Local draft events

Under `contracts/events/`:

- `regulations.evaluation.requested.v0.json`
- `regulations.evaluation.completed.v0.json`

These are local REG-1 draft audit schemas.

They are **not** canonical Shared events and RTD-06 does not promote them.

New cross-engine implementation must not treat their event names or envelope
shape as the production platform contract.

## Runtime adoption status

R-CAP-01 and R-CAP-02 provide runtime adapters for the pinned Shared RTD-06
`requirementResolveRequest/Response` and `documentEvidenceAssessmentRequest/Result`
surfaces. R-CAP-04 exposes the canonical authenticated HTTP operations and
implements caller-bound Control Plane `context_id` validation. Shared remains
the wire-contract authority; the local Pydantic/FastAPI models only execute it.

R-CAP-05 now durably stores the exact RTD-06 assessment request/result snapshot,
tenant-scoped idempotency key, request/result SHA-256 fingerprints and indexed
assessment identities in PostgreSQL. Concurrent duplicates converge on one
committed result, and replay reads the historical snapshot rather than
re-fetching mutable evidence. Tenant-private rows use transaction-scoped
PostgreSQL RLS in addition to explicit tenant predicates.

R-CAP-06 now persists the active Shared RTD-08
`com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1`
envelope in the same PostgreSQL transaction as a newly committed evidence
assessment. The tenant-scoped relay publishes the full canonical envelope with
lease-based at-least-once retry semantics. It does not emit the separate
`document-requirements.determined` fact from the read-only requirement
resolution capability.

R-CAP-07 now declares `baobab-regulations.core` with PARTIAL support for both
canonical RTD-06 capabilities. This is repository implementation evidence only:
Shared deliberately excludes PARTIAL support from generated EngineRegistration.

Live route activation remains separate from route/event implementation.
Regulations still needs its governed workload authentication adapter, a durable
requirement-authority adapter, and a registered `baobab-regulations-workload`
permitted to call Control Plane `context:validate` for the
`baobab-regulations` audience. Proving consumers must separately be authorised
to obtain subject tokens addressed to `aud=baobab-regulations`. Deployment
must also bind the provider-neutral event publisher port to the selected
transport. EA-09 certification and Control Plane activation remain later gates.

Domain models under `src/baobab_regulations/domain/` remain the local source of
truth for Regulations-owned internal semantics. Do not redefine Control Plane,
IAM or Trade Docs canonical identities here.


## R-CAP-08 — regulatory decision evaluation

Shared ADR-SHARED-028 now owns the canonical contract for
`regulations.decision.evaluate` under
`contracts/regulatory-decision/v1`.

This repository adopts that contract through
`src/baobab_regulations/contracts/decision.py` and exact round-trip contract
tests. The capability is **CONTRACTED**, not provider support.

The canonical boundary explicitly keeps:

```text
Idempotency-Key != replay_key
INDETERMINATE != evaluator failure
RegulatoryDecision != operational enforcement
rule-set identity != OPA/Rego implementation
```

R-CAP-09 must implement the production evaluator behind the provider-neutral
port and may not alter the Shared wire contract merely to fit evaluator output.

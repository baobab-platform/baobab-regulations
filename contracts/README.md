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

Live route activation remains separate from route implementation: Regulations
still needs its governed workload authentication adapter and a registered
`baobab-regulations` validator workload permitted to call Control Plane
`context:validate` for the `baobab-regulations` audience. Until that
cross-repository identity allocation, durable R-CAP-05 command persistence and
R-CAP-06 publication evidence exist, provider support remains undeclared.

Domain models under `src/baobab_regulations/domain/` remain the local source of
truth for Regulations-owned internal semantics. Do not redefine Control Plane,
IAM or Trade Docs canonical identities here.

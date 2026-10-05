# Contracts

This directory documents contract dependencies consumed or published by
`baobab-regulations`.

Canonical cross-repository contracts are governed in
`baobab-platform/shared`. This repository must pin and consume those
contracts when runtime implementation begins; it must not fork their wire
schemas locally.

## Consumed from Shared

- Control Plane context / organisation / legal-entity / market identity.
- Capability grant / binding vocabulary.
- Canonical CloudEvents envelope, idempotency and RFC 9457 problem-details.
- `contracts/cross-engine-reference/v1` — ADR-SHARED-021 / RTD-05.
- `contracts/regulatory-document-exchange/v1` — ADR-SHARED-022 / RTD-06.

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

## Planned RTD-06 events

Shared ADR-SHARED-022 defines, but does not yet activate:

```text
com.baobab-platform.regulations.document-requirements.determined.v1
com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
```

Their activation remains RTD-08.

Regulations may later consume the Trade Docs event:

```text
com.baobab-platform.documents.regulatory-evidence.offered.v1
```

after the documents producer path is activated by RTD-07.

## Local draft events

Under `contracts/events/`:

- `regulations.evaluation.requested.v0.json`
- `regulations.evaluation.completed.v0.json`

These are local REG-1 draft audit schemas.

They are **not** canonical Shared events and RTD-06 does not promote them.

New cross-engine implementation must not treat their event names or envelope
shape as the production platform contract.

## Current source of domain truth

Until the runtime implements/pins the Shared contracts, domain models under
`src/baobab_regulations/domain/` remain the local source of truth for
Regulations-owned semantics.

Do not redefine Control Plane, IAM or Trade Docs canonical identities here.

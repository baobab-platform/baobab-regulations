# ADR-REG-0031 — Regulations Capability Census, Contracted Surface and Provider-Implementation Boundary

**Status:** Accepted — Engine Capability Census and Provider-Readiness Decision  
**Decision ID:** ADR-REG-0031  
**Engine:** Baobab Regulations  
**Repository:** baobab-platform/baobab-regulations  
**Date:** 2026-10-06  
**Platform Authority:** ADR-SHARED-017, ADR-SHARED-027  
**Cross-Engine Authority:** ADR-SHARED-019, ADR-SHARED-022, ADR-SHARED-026  
**Decision Type:** Capability Census / Contract Adoption / Provider Readiness / Implementation Sequencing

---

## 1. Decision

Baobab Regulations adopts the first Shared capability census without overstating
runtime maturity.

The engine now recognizes two canonical Shared capability contracts:

~~~text
regulations.requirement.resolve
regulations.evidence.assess
~~~

They are declared locally as:

~~~text
planned_capabilities
proposal_status: CONTRACTED
~~~

They are **not** declared under providers[].support.

The following broader engine proposals remain non-canonical and PROPOSED:

~~~text
regulations.context.resolve
regulations.decision.evaluate
regulations.change.subscribe
regulations.pack.compose
~~~

---

## 2. Executive Rationale

The repository already contains more implementation than its old README implied,
but less than a production capability provider.

The correct maturity picture is:

~~~text
architecture
    ✅ extensive

domain model
    ✅ real code

application orchestration
    ✅ partial

reference evaluator
    ✅ deterministic scaffold

canonical Shared RTD-06 contracts
    ✅ two narrow capabilities

public Regulations capability routes
    ❌ not implemented

production OPA evaluator
    ❌ not implemented

provider support declaration
    ❌ intentionally absent

Control Plane activation
    ❌ not applicable yet
~~~

The capability census must preserve that distinction.

---

## 3. Capability State Model

~~~text
CANDIDATE
    ↓
PROPOSED
    ↓
CONTRACTING
    ↓
CONTRACTED
    ↓
PARTIAL provider implementation
    ↓
IMPLEMENTED provider implementation
    ↓
EA-09 certification
    ↓
Control Plane activation / binding / grant / resolution
~~~

The current Regulations repository spans several points in this chain, depending
on the capability.

A single engine-wide label is therefore insufficient.

---

## 4. Census Matrix

| Capability | Shared canonical? | Current code evidence | Current runtime evidence | Local declaration |
|---|---:|---|---|---|
| regulations.requirement.resolve | Yes | domain references and RTD boundary exist | no route/handler | CONTRACTED |
| regulations.evidence.assess | Yes | RegulatoryDecision/EvaluationService/reference evaluator overlap partially | no RTD-06 handler | CONTRACTED |
| regulations.context.resolve | No | PlatformContextRef + fail-closed helpers | context-ID redemption not implemented | PROPOSED |
| regulations.decision.evaluate | No | strongest implementation: EvaluationService + ReferenceEvaluator + decision repository + tests | no canonical HTTP contract; no production OPA | PROPOSED |
| regulations.change.subscribe | No | ADR architecture only | no subscription runtime | PROPOSED |
| regulations.pack.compose | No | ADR architecture / domain location only | no pack composer | PROPOSED |

---

## 5. Canonical Capability: regulations.requirement.resolve

### 5.1 Meaning

This capability resolves an **exact already-established Regulations requirement**
through the canonical RTD-06 contract.

It answers a question shaped like:

~~~text
Given:
  trusted context
  pinned RegulatoryDecision reference
  pinned requirement reference

Return:
  exact Regulations-owned requirement projection
~~~

### 5.2 It does not mean

~~~text
resolve the whole regulatory context
determine every applicable rule
evaluate an entire transaction
create a TradeDocument
verify a TradeDocument
enforce a shipment state
~~~

Therefore:

~~~text
regulations.requirement.resolve
    !=
regulations.context.resolve
~~~

### 5.3 Current implementation state

No FastAPI route currently implements the Shared operation:

~~~text
POST /documentary-requirements/resolve
~~~

Current app routes remain health/readiness only.

Verdict:

~~~text
CONTRACTED
not implemented
no provider support
~~~

---

## 6. Canonical Capability: regulations.evidence.assess

### 6.1 Meaning

This capability evaluates bounded documentary evidence against one exact
Regulations requirement.

Conceptually:

~~~text
Regulations Requirement
        +
Trade Docs DocumentVersion references
        +
bounded documentary assertions
        +
trusted tenant context
        ↓
Regulatory Evidence Assessment
        ↓
SATISFIED / UNSATISFIED / INDETERMINATE /
NOT_APPLICABLE / REVIEW_REQUIRED
~~~

### 6.2 Authority boundary

Trade Docs supplies documentary facts.

Regulations decides legal/regulatory sufficiency.

~~~text
Trade Docs VERIFIED
        !=
Regulations SATISFIED
~~~

The capability does not mutate:

~~~text
TradeDocument
DocumentVersion
CustomsCase
Shipment
Order
ERP state
~~~

### 6.3 Current implementation state

The repository has related implementation primitives:

- RegulatoryDecision;
- DecisionReason;
- RecommendedDisposition;
- EvaluationService;
- ReferenceEvaluator;
- decision persistence port/repository;
- deterministic golden-path tests.

But those do not yet implement the exact Shared RTD-06
documentEvidenceAssessmentRequest / Result contract.

Verdict:

~~~text
CONTRACTED
not yet provider support
~~~

---

## 7. Proposed Capability: regulations.context.resolve

ADR-REG-0017 defines a broad Regulatory Applicability Resolution Pipeline.

Target behavior includes:

~~~text
Control Plane context redemption
actor roles
legal entities
jurisdiction roles
trade regimes
regulated activity
transaction geography
classification
legal time
knowledge time
conditions
exceptions
exemptions
rule-set applicability
~~~

The live implementation currently supports only a bounded subset.

Evidence:

~~~text
PlatformContextRef
resolve_platform_context()
tenant fail-closed checks
header/request-scope helpers
~~~

Critical gap:

~~~text
context_id only
    ↓
ContextRedemptionNotImplementedError
    code = CONTEXT_REDEMPTION_NOT_IMPLEMENTED
~~~

Therefore this proposal is not canonicalized by the census.

Verdict:

~~~text
PROPOSED
implementation scaffold only
~~~

---

## 8. Proposed Capability: regulations.decision.evaluate

This is the most mature uncontracted proposal.

### Existing evidence

~~~text
RegulatoryDecision domain model
EvaluationService
RegulatoryPolicyEvaluatorPort
DecisionRepositoryPort
ReferenceEvaluator
InMemoryDecisionRepository
golden reference tests
legal_time
knowledge_time
rule_set_id
reason codes
recommended disposition
PDP / PEP separation
~~~

### Existing execution flow

~~~mermaid
flowchart LR
    C[RegulatoryContext] --> S[EvaluationService]
    F[Facts] --> S
    RS[Rule Set ID] --> S
    S --> R[resolve_platform_context]
    R --> E[RegulatoryPolicyEvaluatorPort]
    E --> D[RegulatoryDecision]
    D --> P[DecisionRepositoryPort]
~~~

### Why it is not yet canonical capability support

The current ReferenceEvaluator explicitly identifies itself as:

~~~text
offline scaffold
not production OPA
~~~

The current FastAPI surface does not expose a general decision-evaluation route.

No provider-neutral Shared request/response schema currently defines:

~~~text
RegulatoryDecisionEvaluationRequest
RegulatoryDecisionEvaluationResult
~~~

The implementation also does not yet prove:

- production OPA execution;
- BRIR-to-policy compilation;
- canonical rule-set version semantics;
- cross-engine context redemption;
- stable idempotency/replay contract;
- Problem Details mapping;
- contract-level provenance references;
- production event/outbox behavior.

Verdict:

~~~text
PROPOSED
next capability-contract priority
~~~

---

## 9. Proposed Capability: regulations.change.subscribe

ADR-REG-0023 and ADR-REG-0024 establish regulatory change architecture.

However:

~~~text
RTD-08 event producer authority
    !=
general change subscription capability
~~~

The current Shared Regulations events:

~~~text
document-requirements.determined
requirement-satisfaction.evaluated
~~~

are documentary exchange facts, not a generic regulatory-change subscription
API.

No source, broker subscription manager, change-query API or consumer contract is
implemented locally.

Verdict:

~~~text
PROPOSED
not implemented
~~~

---

## 10. Proposed Capability: regulations.pack.compose

ADR-REG-0029 defines reusable:

~~~text
RegulatoryModule
JurisdictionPack
RegulatoryRegimePack
CommodityProfile
CorridorProfile
CoverageManifest
~~~

But the repository has no executable pack-composition service and no Shared
request/response contract for pack composition.

Verdict:

~~~text
PROPOSED
not implemented
~~~

---

## 11. Why No providers Block Exists

The provider declaration answers:

> Which canonical capability contracts does a concrete provider actually
> implement?

At census time, the truthful answer is:

~~~text
none yet
~~~

That does not mean the repository has no useful code.

It means no current code path satisfies a complete canonical capability
contract strongly enough to become ProviderCapabilitySupport.

This distinction is mandatory.

---

## 12. ReferenceEvaluator Classification

ReferenceEvaluator is retained as an implementation and assurance asset.

It is not promoted to a provider.

Its current role is:

~~~text
golden-case execution
offline deterministic behavior
domain model exercise
future OPA differential oracle
development feedback
~~~

It SHALL NOT be described as:

~~~text
production regulatory evaluator
certified provider
active Control Plane provider
E3/E4 enforcement evaluator
~~~

---

## 13. Current API Surface

The live FastAPI application currently exposes:

~~~text
GET /healthz
GET /readyz
~~~

It does not yet expose:

~~~text
POST /documentary-requirements/resolve
POST /documentary-evidence/assessments
POST /regulatory-decisions/evaluate
~~~

This fact is a decisive part of the provider-readiness assessment.

---

## 14. Capability Contract vs API Route

A Shared canonical capability contract may exist before the engine implements a
route.

Therefore:

~~~text
Shared capability = DRAFT
        +
Regulations planned capability = CONTRACTED
        +
no provider support
~~~

is valid.

The next implementation increment may add a provider adapter, but the provider
claim must follow the implementation rather than precede it.

---

## 15. Recommended Implementation Order

The census establishes the following implementation order:

~~~text
R-CAP-01
Implement regulations.requirement.resolve adapter
        ↓
R-CAP-02
Implement regulations.evidence.assess adapter
        ↓
R-CAP-03
Add exact Shared contract tests
        ↓
R-CAP-04
Add authenticated/context-bound API routes
        ↓
R-CAP-05
Add durable assessment persistence / idempotency
        ↓
R-CAP-06
Add canonical event outbox publication
        ↓
R-CAP-07
Declare PARTIAL provider support if all canonical contract paths are covered
        ↓
R-CAP-08
Contract regulations.decision.evaluate in Shared
        ↓
R-CAP-09
Implement production policy evaluator path
        ↓
R-CAP-10
Promote provider support only with full implementation evidence
~~~

The order deliberately begins with the two contracts already stabilized by
RTD-06.

---

## 16. R-CAP-01 — requirement.resolve Exit Criteria

Before provider support may be claimed:

1. exact RTD-06 request schema is accepted;
2. authenticated tenant/context is validated;
3. decision and requirement references are owner-preserving;
4. exact pinned requirement is resolved;
5. stale/superseded references fail correctly;
6. not-found and authority-unavailable are distinct;
7. response validates against requirementResolveResponse;
8. no TradeDocument ownership is introduced;
9. contract tests execute in CI;
10. invocation remains provider-neutral.

---

## 17. R-CAP-02 — evidence.assess Exit Criteria

Before provider support may be claimed:

1. documentEvidenceAssessmentRequest is accepted exactly;
2. Trade Docs DocumentVersion references are owner-preserving and pinned;
3. envelope/context tenant mismatches fail closed;
4. documentary verification is not treated as automatic satisfaction;
5. SATISFIED/UNSATISFIED/INDETERMINATE semantics are preserved;
6. resulting RegulatoryDecision remains Regulations-owned;
7. assessment is idempotent/replayable;
8. result validates against Shared schema;
9. canonical satisfaction event can be published through an outbox;
10. operational shipment/order state is not mutated.

---

## 18. R-CAP-08 — decision.evaluate Contracting Scope

The broader decision capability should be contracted only after its semantics are
written in Shared.

Minimum request concepts:

~~~text
context reference
regulatory subject references
regulated activities
facts
rule-set/version reference
legal time
knowledge time
assessment purpose
requested assurance/enforcement ceiling
idempotency/replay key
~~~

Minimum response concepts:

~~~text
RegulatoryDecision reference
outcome
enforcement class
reasons
legal basis references
evidence references
recommended disposition
rule-set fingerprint
evaluated_at
legal_time
knowledge_time
provenance
replay identity
~~~

Technical errors must remain separate from regulatory outcomes.

---

## 19. Capability Non-Duplication Rules

The following shall remain distinct:

~~~text
regulations.requirement.resolve
    exact requirement lookup

regulations.context.resolve
    broad applicability/context derivation

regulations.evidence.assess
    documentary sufficiency evaluation

regulations.decision.evaluate
    full regulatory decision evaluation

regulations.change.subscribe
    regulatory change consumption/subscription

regulations.pack.compose
    regulatory pack composition
~~~

Convenience must not collapse these into one generic:

~~~text
regulations.regulation.process
~~~

or similar monolithic capability.

---

## 20. Control Plane Boundary

Nothing in this census changes Control Plane authority.

Control Plane still owns:

~~~text
Capability
CapabilityProvider
ProviderCapabilitySupport registration
CapabilityBinding
CapabilityGrant
health
EngineInstance
provider routing
tenant entitlement
resolution
activation
~~~

The Regulations repository only declares implementation intent/evidence.

---

## 21. RTD-10 Relationship

The repository pins the post-census Shared conformance revision.

RTD-10 now permits:

~~~text
planned_capabilities:
  capability_key: <catalogued regulations key>
  proposal_status: CONTRACTED
~~~

and still rejects:

~~~text
non-catalogued capability_key
CONTRACTED + proposed_key
provider support without later implementation evidence
foreign bounded-context ownership
~~~

---

## 22. Evidence Snapshot

| Evidence | What it proves | What it does not prove |
|---|---|---|
| RegulatoryDecision model | Regulations owns decision semantics | production decision API |
| EvaluationService | orchestration boundary exists | production policy runtime |
| ReferenceEvaluator | deterministic reference behavior | OPA/provider readiness |
| platform context tests | fail-closed tenant/context behavior | Control Plane redemption |
| RTD-06 Shared contracts | two narrow capability contracts exist | Regulations implements them |
| RTD-08 active event contracts | canonical producer authority exists | deployed outbox/broker |
| RTD-10 conformance | engine boundaries remain correct | production certification |

---

## 23. Capability Census Diagram

~~~mermaid
flowchart TD
    A[Proposed Regulations capability] --> B{Shared request/response contract?}
    B -- No --> C[Remain PROPOSED]
    B -- Yes --> D{Semantics bounded and owner clear?}
    D -- No --> C
    D -- Yes --> E[Canonical DRAFT capability]
    E --> F[Local planned capability = CONTRACTED]
    F --> G{Exact runtime contract implemented?}
    G -- No --> H[No provider support]
    G -- Partial --> I[Provider support PARTIAL]
    G -- Complete --> J[Provider support IMPLEMENTED]
    J --> K[EA-09 certification]
    K --> L[Control Plane activation]
~~~

---

## 24. Non-Goals

This ADR does not:

- implement the two contracted capabilities;
- promote any provider;
- activate a capability;
- certify Regulations;
- enable production OPA;
- claim Foundation production readiness;
- redefine Trade Docs;
- redefine Pulse;
- add a general regulatory decision contract;
- add pack or change-subscription contracts.

---

## 25. Invariants

~~~text
REG-CENSUS-001
A canonical Shared capability can exist without a provider implementation.

REG-CENSUS-002
No providers block exists until exact canonical contract implementation is evidenced.

REG-CENSUS-003
ReferenceEvaluator is scaffold/reference evidence, not production provider support.

REG-CENSUS-004
regulations.requirement.resolve is not regulations.context.resolve.

REG-CENSUS-005
regulations.evidence.assess is not regulations.decision.evaluate.

REG-CENSUS-006
RTD-08 event activation is not regulations.change.subscribe.

REG-CENSUS-007
A packs domain model/location is not regulations.pack.compose.

REG-CENSUS-008
Control Plane owns activation, binding, grants and resolution.

REG-CENSUS-009
Trade Docs VERIFIED never automatically means Regulations SATISFIED.

REG-CENSUS-010
Operational enforcement remains outside Regulations.
~~~

---

## 26. Final Decision

> **Baobab Regulations now has two canonical contracted capability surfaces but zero implemented provider-support claims. The next work should implement the narrow contracts already standardized by RTD-06 before expanding the capability catalogue to the broader decision, context, change or pack surfaces.**

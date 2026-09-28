# ADR-REG-0019 — Policy Decision Point and Enforcement Point Separation

**Subtitle:** Distributed Regulatory Execution, Signed Policy Distribution, Delegated Decision Runtime and Enforcement Boundary

**Status:** Proposed — Foundational Distributed Runtime Architecture  
**Decision ID:** `ADR-REG-0019`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** PDP / PEP / Distributed Policy Execution / Bundle Distribution / Runtime Delegation / Enforcement  
**Strategic Classification:** Core Regulatory Execution Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL maintain a strict separation between:

```text
REGULATORY AUTHORITY
        │
        ▼
REGULATORY KNOWLEDGE
        │
        ▼
REGULATORY DECISION AUTHORITY
        │
        ▼
POLICY EVALUATION
        │
        ▼
REGULATORY DECISION
        │
        ▼
POLICY ENFORCEMENT
        │
        ▼
BUSINESS STATE CHANGE
```

The initial topology SHALL be:

```text
Consumer / Domain Engine
          │
          ▼
   Baobab Regulations API
          │
          ▼
Regulatory Decision Engine
          │
          ▼
     Internal OPA PDP
          │
          ▼
   RegulatoryDecision
          │
          ▼
Domain Engine PEP
          │
          ▼
Operational Enforcement
```

Baobab MAY later distribute regulatory execution closer to selected Policy Enforcement Points.

However:

> **Distributed execution SHALL distribute verified decision capability—not distribute regulatory authority.**

---

# 2. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine`
- `ADR-REG-0003 — Regulatory Authority and Interpretation Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence Architecture`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0017 — Regulatory Context and Applicability Resolution`
- `ADR-REG-0018 — Regulatory Decision and Evaluation Engine`

It SHALL also remain consistent with accepted Control Plane decisions governing:

```text
capabilities

providers

bindings

engine instances

readiness

resolution assertions

failover

service-to-service invocation

controlled mutation.
```

---

# 3. Fundamental Doctrine

The architecture SHALL distinguish:

```text
LAW
≠
REGULATORY RULE
≠
BRIR
≠
COMPILED POLICY
≠
OPA PDP
≠
REGULATORY DECISION
≠
PEP
≠
ENFORCEMENT ACTION.
```

---

# 4. Three Different Authorities

The system SHALL distinguish:

```text
LEGAL AUTHORITY

REGULATORY DECISION AUTHORITY

OPERATIONAL ENFORCEMENT AUTHORITY.
```

---

# 5. Legal Authority

Legal authority originates outside Baobab from:

```text
legislature

regulator

customs authority

tax authority

court

treaty body

other competent authority.
```

Baobab does not manufacture it.

---

# 6. Regulatory Decision Authority

`baobab-regulations` is the Baobab platform authority for:

```text
verified regulatory rules

applicability

assessment semantics

decision policies

regulatory outcomes.
```

---

# 7. Operational Enforcement Authority

The domain engine that owns the business object owns its operational mutation.

Examples:

```text
Trade
    shipment hold
    order hold
    fulfilment restriction

ERP
    accounting / filing workflow

Digital Estate
    UI gate

future Ledger
    posting restriction.
```

---

# 8. Regulations SHALL Not Own Domain Mutations

Rejected:

```text
Regulations directly updates
Trade shipment table.
```

---

# 9. Domain Engines SHALL Not Own Regulatory Semantics

Rejected:

```text
Trade decides independently
which statute prohibits shipment.
```

---

# 10. PDP / PEP Model

OPA defines itself as a Policy Decision Point and the calling application as the Policy Enforcement Point. Its deployment guidance specifically recommends placing OPA close to PEPs where low latency and resilience justify doing so.

Baobab adopts this separation while adding a higher-level regulatory domain boundary.

---

# 11. Baobab Terminology

Baobab SHALL distinguish:

```text
Regulatory Decision Authority
    baobab-regulations

Policy Evaluation PDP
    OPA or future execution provider

Policy Enforcement Point
    Trade / ERP / estate / other engine.
```

---

# 12. Why the Additional Distinction

OPA answers:

```text
"What does this compiled policy
return for this input?"
```

Baobab Regulations answers:

```text
"What regulatory conclusion follows
from applicable verified law,
facts, evidence and decision policy?"
```

These are not identical.

---

# 13. Central Decision Architecture

The default production topology SHALL initially be:

```text
                         CONTROL PLANE
                      capability/context
                              │
                              ▼
DOMAIN ENGINE ───────► REGULATIONS API
                              │
                              ▼
                    DECISION ENGINE
                              │
                              ▼
                         LOCAL OPA
                              │
                              ▼
                    RuleEvaluationResult
                              │
                              ▼
                  RegulatoryDecision
                              │
                              ▼
DOMAIN ENGINE ◄──────── decision
      │
      ▼
     PEP
      │
      ▼
BUSINESS STATE
```

---

# 14. Why Central First

Central execution provides:

```text
simpler semantics

single decision implementation

simpler rollout

easier provenance

simpler bundle management

simpler initial observability

lower distributed-state risk.
```

---

# 15. Central Does Not Mean Control Plane Proxy

Consistent with accepted Control Plane architecture:

```text
Control Plane
```

resolves:

```text
capability
provider
context
authorization.
```

The consumer then invokes:

```text
baobab-regulations
```

directly.

---

# 16. OPA Remains Behind Regulations

Initially:

```text
Trade
  ↓
Regulations
  ↓
OPA
```

not:

```text
Trade
  ↓
OPA.
```

---

# 17. Direct PEP-to-OPA Is Initially Forbidden

A domain PEP SHALL NOT directly call a Regulations OPA endpoint and independently interpret the output.

---

# 18. Why

Doing so would bypass:

```text
context resolution

coverage checks

evidence assessment

normative aggregation

AssessmentOutcome

effect-class gating

provenance

decision lifecycle.
```

---

# 19. Distributed Execution Is Still Valuable

OPA's architecture explicitly supports distributed deployments and recommends co-location with applications where low latency and higher availability are important. Its management APIs support central distribution of policy and collection of status and decision telemetry.

Baobab therefore SHALL design for future distributed execution.

---

# 20. Distributed Architecture

Future approved topology:

```text
                  BAOBAB REGULATIONS
                     AUTHORITATIVE
                        PUBLISHER
                            │
                            ▼
                Regulatory Execution
                     Package
                            │
                      distribution
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
           Trade           ERP          Other PEP
             │              │              │
             ▼              ▼              ▼
      Regulatory      Regulatory      Regulatory
      Runtime          Runtime          Runtime
             │              │              │
             ▼              ▼              ▼
         local OPA       local OPA       local OPA
             │              │              │
             ▼              ▼              ▼
       local decision   local decision  local decision
             │              │              │
             ▼              ▼              ▼
            PEP            PEP            PEP
```

---

# 21. Critical Restriction

The distributed component SHALL NOT be:

```text
"an OPA sidecar the service
can query however it wants."
```

It SHALL be a governed:

# **Baobab Regulatory Runtime**

---

# 22. Regulatory Runtime

The `Baobab Regulatory Runtime` SHALL provide the local execution contract.

Conceptually:

```text
Baobab Regulatory Runtime
├── package validator
├── context/input validator
├── RuleSet selector
├── OPA adapter
├── result validator
├── DecisionPolicy evaluator
├── effect-class gate
├── DecisionTrace builder
├── decision receipt producer
└── telemetry client
```

---

# 23. PEP Shall Call Runtime, Not Raw OPA

Correct:

```text
Trade
  ↓
Baobab Regulatory Runtime
  ↓
OPA
```

Rejected:

```text
Trade custom code
  ↓
data.some.package.allow
```

---

# 24. Provider Neutrality

The Regulatory Runtime SHALL expose Baobab contracts.

OPA SHALL remain hidden behind:

```text
DeterministicPolicyEvaluator.
```

---

# 25. Future Replacement

The runtime may later use:

```text
OPA

CEL

native BRIR evaluator

Wasm

another deterministic engine.
```

The PEP contract SHALL remain unchanged.

---

# 26. Regulatory Execution Package

Distributed execution SHALL consume a Baobab-owned:

# `RegulatoryExecutionPackage`

abbreviated:

```text
REP
```

---

# 27. REP Is Above the OPA Bundle

Conceptually:

```text
RegulatoryExecutionPackage
           │
           ├── manifest
           ├── RuleSet identity
           ├── DecisionPolicy
           ├── schemas
           ├── effect ceiling
           ├── temporal metadata
           ├── provenance
           ├── signatures
           │
           └── target artifacts
                  └── OPA Bundle
```

---

# 28. OPA Bundle Is an Artifact

Therefore:

```text
REP
≠
OPA Bundle.
```

The OPA bundle is one compiled implementation artifact contained or referenced by the REP.

---

# 29. REP Manifest

Conceptually:

```text
RegulatoryExecutionPackageManifest
├── package_id
├── package_revision
├── ruleset_ref
├── ruleset_fingerprint
├── brir_version
├── decision_policy_version
├── compiler_version
├── evaluator_target
├── evaluator_version_range
├── regulatory_profile
├── jurisdiction_scope[]
├── regime_scope[]
├── tenant_scope?
├── legal_validity_metadata
├── knowledge_cutoff
├── activation_state
├── effect_class_ceiling
├── offline_execution_policy
├── freshness_policy
├── supersedes?
├── revoked?
├── required_runtime_version
├── artifact_refs[]
├── artifact_hashes[]
├── issued_at
├── signature_metadata
└── provenance
```

---

# 30. Package Identity

Each REP SHALL be immutable once published.

---

# 31. Package Revision

New content requires:

```text
new package revision.
```

---

# 32. No Mutable `latest` as Decision Identity

Distribution MAY expose:

```text
latest
```

for discovery.

Actual decisions SHALL record:

```text
package revision
+
ruleset fingerprint.
```

---

# 33. Package Promotion States

Initial states SHOULD include:

```text
BUILT

VALIDATED

SHADOW

CANARY

ACTIVE

DEPRECATED

REVOKED

RETIRED.
```

---

# 34. Build Does Not Mean Active

A successfully compiled bundle does not mean:

```text
legally approved

operationally approved

active.
```

---

# 35. SHADOW

A SHADOW package MAY execute real inputs but SHALL NOT determine production enforcement.

---

# 36. CANARY

A CANARY package MAY become authoritative only for explicitly assigned bounded execution targets.

---

# 37. ACTIVE

ACTIVE means the package is authorised for its declared:

```text
scope

runtime targets

effect ceiling.
```

---

# 38. REVOKED

A revoked package SHALL no longer be eligible for new consequential decisions.

---

# 39. RETIRED

A retired package remains available for:

```text
historical replay

audit.
```

---

# 40. OPA Bundles

OPA bundles are designed to distribute policy/data and allow policy updates without restarting OPA. The distribution mechanism is eventually consistent and can use revision metadata and HTTP caching through ETags.

Baobab SHALL use OPA bundles as the initial policy-artifact distribution mechanism.

---

# 41. Snapshot Bundles

For consequential regulatory policy, the initial default SHALL be:

```text
signed snapshot bundles.
```

---

# 42. Delta Bundles

OPA delta bundles update data only and currently do not support bundle signing or persisted recovery.

Therefore:

> **OPA delta bundles SHALL NOT initially be used for E3/E4 regulatory policy distribution.**

---

# 43. Why

High-assurance regulatory execution requires:

```text
signed

immutable

reconstructable

version-identifiable
```

policy artifacts.

---

# 44. Delta Bundles May Be Reconsidered

They MAY later be used for:

```text
low-risk derived data

E0/E1 scenarios
```

after separate threat and assurance analysis.

---

# 45. Bundle Signing

OPA supports signed bundles and verifies their file hashes/signature before activation. If verification fails, OPA keeps the currently active bundle rather than activating the invalid replacement.

E3/E4 OPA artifacts SHALL be signed.

---

# 46. Baobab Package Signing

Baobab SHOULD additionally sign the REP envelope.

Thus:

```text
REP signature
    proves Baobab package integrity

OPA bundle signature
    proves target artifact integrity.
```

---

# 47. Signature Does Not Prove Legal Correctness

Again:

```text
SIGNED
≠
LEGALLY CORRECT.
```

It proves integrity and publisher identity.

---

# 48. Signing Keys

Signing keys SHALL be managed through platform infrastructure/key-management controls.

They SHALL NOT be stored in:

```text
Git repository

OPA bundle

Regulations source code.
```

---

# 49. Trust Root

Distributed runtimes SHALL receive trusted verification keys through a secure bootstrap path independent of the regulatory bundle itself.

---

# 50. OPA Discovery

OPA's Discovery mechanism can centrally configure which bundles, status services and decision-log services agents use. OPA recommends signing discovery bundles because they can themselves distribute the verification keys used for other bundles.

---

# 51. Discovery Initial Decision

OPA Discovery SHALL be:

```text
OPTIONAL
```

in the first implementation.

---

# 52. Initial Simpler Bootstrap

The first distributed deployment SHOULD favour:

```text
static trusted boot configuration

+
signed regulatory bundle configuration.
```

---

# 53. Future Discovery Use

Discovery MAY later help select bundles by:

```text
region

environment

engine

regulatory profile

jurisdiction.
```

---

# 54. Discovery Trust Root

If OPA Discovery is enabled:

```text
discovery verification key
```

SHALL be bootstrapped independently.

OPA specifically prevents that trust key from being changed through the discovery bundle itself.

---

# 55. Regulatory Distribution Controller

`baobab-regulations` SHALL operate or own the domain semantics of a:

# `RegulatoryDistributionController`

---

# 56. Distribution Controller Responsibilities

It SHALL track:

```text
published REP revisions

target runtimes

expected package revision

actual package revision

activation state

download state

runtime readiness

staleness

revocation

decision telemetry.
```

---

# 57. It Is Not Baobab Control Plane

The Baobab Control Plane remains responsible for:

```text
capability/provider topology

engine instances

context

isolation

bindings.
```

Regulations owns:

```text
regulatory execution package semantics

regulatory rule distribution state.
```

---

# 58. Integration With Control Plane

Control Plane MAY know that:

```text
EngineInstance T
provides/consumes
regulations.evaluate
```

and may know its readiness.

Regulations SHALL know:

```text
which REP revision
that runtime must execute.
```

---

# 59. OPA Does Not Provide a Full Management Control Plane

OPA's own documentation describes management APIs for bundle distribution, decision logs, status and discovery, but explicitly notes that OPA does not provide a control-plane service itself.

Therefore Baobab must implement the governance and desired-state layer above these APIs.

---

# 60. Desired Execution State

Conceptually:

```text
RegulatoryRuntimeDesiredState
├── runtime_ref
├── expected_package_revision
├── expected_ruleset_fingerprint
├── expected_opa_bundle_revision
├── effect_class_ceiling
├── activation_mode
└── required_by
```

---

# 61. Observed Execution State

```text
RegulatoryRuntimeObservedState
├── runtime_ref
├── active_package_revision
├── active_bundle_revision
├── opa_version
├── last_successful_download
├── last_successful_activation
├── decision_log_status
├── plugin_status
├── runtime_health
├── last_seen
└── errors[]
```

---

# 62. Reconciliation

Regulations SHALL compare:

```text
desired state
```

against:

```text
observed state.
```

---

# 63. Drift

Potential:

```text
PACKAGE_DRIFT

BUNDLE_DRIFT

RUNTIME_VERSION_DRIFT

CONFIGURATION_DRIFT

TELEMETRY_DRIFT.
```

---

# 64. Drift Is Operational State

It SHALL not alter canonical law.

---

# 65. OPA Status API

OPA can report:

```text
active bundle revision

download timestamps

activation timestamps

activation errors

plugin states

OPA instance identity/version.
```


Baobab SHOULD consume this telemetry for distributed runtime reconciliation.

---

# 66. OPA Health API Limitation

OPA's `/health?bundles` can verify initial bundle activation, but subsequent bundle download/activation failures do not make that initial health check sufficient; OPA recommends using status reporting for fine-grained bundle monitoring.

---

# 67. Therefore

Baobab SHALL NOT define regulatory readiness as:

```text
GET /health == 200.
```

---

# 68. Regulatory Runtime Readiness

Readiness SHALL require:

```text
runtime process healthy

expected REP known

expected bundle activated

bundle signature accepted

expected RuleSet fingerprint

supported runtime version

effect ceiling valid

freshness state valid

required plugins healthy

no revocation

no material drift.
```

---

# 69. RuntimeReadiness

Potential:

```text
READY

DEGRADED

STALE

NOT_READY

REVOKED.
```

---

# 70. READY

Expected package is active and all consequential requirements are satisfied.

---

# 71. DEGRADED

Package remains usable for declared lower-risk modes but some non-critical management/telemetry dependency is unavailable.

---

# 72. STALE

Package exceeded its approved freshness/lease policy.

---

# 73. NOT_READY

No suitable executable package is available.

---

# 74. REVOKED

Package or runtime has explicitly lost execution authority.

---

# 75. Freshness Is Not Merely Download Age

Regulatory freshness SHALL consider:

```text
expected revision

known regulatory changes

activation deadline

knowledge cutoff

legal effective boundaries

revocation status.
```

---

# 76. Regulatory Freshness Policy

Conceptually:

```text
RegulatoryFreshnessPolicy
├── profile
├── effect_class
├── maximum_package_age?
├── maximum_distribution_lag?
├── required_revision?
├── hard_expiry?
├── offline_allowed
├── offline_until?
└── stale_disposition
```

---

# 77. No Universal TTL

A single:

```text
bundle_ttl = 24h
```

SHALL NOT govern every regulatory domain.

---

# 78. Why

Change velocity differs between:

```text
tariffs

sanctions

tax

company-registration requirements

record-retention rules.
```

---

# 79. Effect-Class Freshness

More consequential execution SHALL require stronger freshness.

---

# 80. E0/E1 Offline

Informational/advisory evaluation MAY tolerate a wider bounded staleness window where clearly disclosed.

---

# 81. E2 Offline

Review-gate evaluation MAY be allowed with a valid package if:

```text
no hard revocation

freshness still acceptable.
```

---

# 82. E3 Offline

Conditional enforcement MAY be allowed only where:

```text
package is signed

within explicit execution lease

expected legal-time boundaries known

runtime state verified

offline execution is approved for profile.
```

---

# 83. E4 Offline Default

The initial default SHALL be:

> **E4 SHALL NOT be permitted during an unbounded or unverified offline condition.**

---

# 84. E4 Exception

A regulatory profile MAY explicitly permit bounded offline E4 only after demonstrating:

```text
signed immutable execution package

strict freshness lease

revocation strategy

clock integrity

complete deterministic rules

safe failure mode

reconciliation

decision replay.
```

---

# 85. Why Conservative

Autonomous enforcement on stale legal state is materially more dangerous than advisory use.

---

# 86. Execution Lease

Distributed consequential execution SHOULD use an explicit:

```text
ExecutionLease
```

or equivalent package policy.

---

# 87. ExecutionLease

Conceptually:

```text
ExecutionLease
├── package_revision
├── runtime_scope
├── effect_class_ceiling
├── valid_from
├── valid_until
├── offline_allowed
├── revocation_epoch?
└── signature
```

---

# 88. Lease Is Operational

It does not define:

```text
legal validity of the rules.
```

---

# 89. Package Expiry ≠ Law Expiry

This distinction SHALL be explicit.

---

# 90. Future Effective Rules

A REP MAY include verified future-effective rules.

Therefore:

```text
midnight legal change
```

SHOULD NOT necessarily require:

```text
midnight bundle download.
```

---

# 91. Preferred Future Activation

```text
bundle deployed beforehand
        │
        ▼
legal_time changes
        │
        ▼
precompiled rule becomes applicable.
```

---

# 92. This Reduces Deployment Risk

It avoids relying on:

```text
network

scheduler

artifact publication
```

exactly at commencement time.

---

# 93. Bundle Activation Time ≠ Legal Effective Time

Again:

```text
OPA activation
≠
law commencement.
```

---

# 94. Emergency Regulatory Change

Where a newly verified change requires immediate runtime update:

```text
new REP
   ↓
expedited governed promotion
   ↓
distribution
   ↓
activation deadline.
```

---

# 95. Activation Deadline

A regulatory package MAY include:

```text
must_activate_by.
```

This is operational readiness metadata.

---

# 96. Old Bundle After Failed Update

OPA deliberately keeps an existing bundle if signature/activation of a new bundle fails.

This is good availability behaviour.

But Baobab SHALL NOT assume:

```text
old bundle still active
⇒
old bundle still safe.
```

---

# 97. Example

```text
Old RuleSet:
valid yesterday.

New law:
effective today.

New bundle:
activation failed.

OPA:
continues old bundle.
```

Baobab runtime state SHALL become:

```text
STALE / NOT_READY
```

for consequential evaluation.

---

# 98. This Is Critical

OPA runtime availability and regulatory decision readiness are distinct.

---

# 99. Persisted Bundles

OPA can persist the last successfully activated bundle and restore it on startup if the bundle server is unavailable.

Baobab MAY enable this for distributed runtime resilience.

---

# 100. Persisted Bundle Safety

A restored persisted bundle SHALL still undergo Baobab checks for:

```text
lease

freshness

revocation

expected revision

effect ceiling.
```

---

# 101. Persistence Does Not Grant Indefinite Authority

Rejected:

```text
OPA found old disk bundle
⇒
enforce forever.
```

---

# 102. Bundle Polling

OPA supports periodic polling, long polling and ETag-based efficient updates.

Baobab MAY use these mechanisms.

---

# 103. Polling Interval Is Operational

It SHALL be configured according to:

```text
regulatory freshness SLO

runtime count

network cost

change velocity.
```

---

# 104. Urgent Revocation

Polling alone MAY be insufficient for urgent revocation.

Baobab SHOULD support an additional:

```text
revocation / invalidation event
```

path.

---

# 105. Revocation Model

Conceptually:

```text
PackageRevision P5
    ↓
REVOKED
    ↓
runtime invalidation event
    ↓
runtime marks P5 unusable
    ↓
new consequential evaluation blocked
```

---

# 106. Revocation Must Be Auditable

Record:

```text
who

why

when

affected runtimes

replacement revision.
```

---

# 107. Network Partition

If revocation channel cannot be contacted:

```text
offline execution policy
```

governs continued use.

---

# 108. No Invisible Network Assumption

Distributed regulatory evaluation SHALL explicitly define behaviour under:

```text
Regulations unavailable

bundle server unavailable

status collector unavailable

decision log collector unavailable

Control Plane unavailable

OPA unavailable.
```

---

# 109. Bundle Server Unavailable

If a currently approved package remains within lease:

```text
local evaluation MAY continue
```

according to effect-class policy.

---

# 110. Regulations API Unavailable

A delegated runtime MAY continue only if:

```text
delegated execution is approved

package valid

lease valid

context can still be authoritatively resolved.
```

---

# 111. Control Plane Unavailable

If the PEP lacks a valid cached context assertion and cannot resolve canonical context:

```text
consequential evaluation SHALL NOT guess context.
```

---

# 112. OPA Unavailable Locally

Result:

```text
EVALUATOR_UNAVAILABLE.
```

Regulatory decision:

```text
INDETERMINATE
```

for material evaluation.

Operational policy may:

```text
HOLD.
```

---

# 113. Status Collector Unavailable

Decision execution MAY continue within policy if:

```text
local runtime knows its package state
```

but central visibility becomes:

```text
DEGRADED.
```

---

# 114. Decision Log Collector Unavailable

OPA decision-log upload failure SHALL not necessarily halt low-risk evaluation.

For E3/E4, Baobab SHALL require durable local regulatory decision receipts so audit evidence is not lost.

---

# 115. OPA Decision Logs Are Supplemental

OPA decision logs contain inputs/results, decision IDs, trace IDs and bundle revisions.

They SHALL complement—not replace—the Baobab:

```text
RegulatoryDecisionReceipt.
```

---

# 116. RegulatoryDecisionReceipt

A distributed runtime SHALL produce a durable:

```text
RegulatoryDecisionReceipt
```

for every consequential decision.

---

# 117. DecisionReceipt

Conceptually:

```text
RegulatoryDecisionReceipt
├── decision_id
├── runtime_id
├── package_revision
├── ruleset_fingerprint
├── decision_policy_version
├── context_snapshot_ref
├── context_fingerprint
├── evidence_snapshot_ref?
├── question
├── outcome
├── effect_class
├── disposition
├── OPA_decision_id?
├── OPA_bundle_revision?
├── input_fingerprint
├── result_fingerprint
├── decided_at
├── offline_state
├── signature/attestation?
└── provenance
```

---

# 118. Local Decision IDs

Distributed runtimes SHALL generate globally unique Baobab decision IDs or obtain them through a compatible ID scheme.

---

# 119. Central Reconciliation

Decision receipts SHALL eventually be reconciled back into the Regulations canonical decision ledger/store.

---

# 120. Offline Queue

Where bounded offline execution is supported:

```text
DecisionReceipt
   ↓
durable local outbox
   ↓
later upload/reconciliation.
```

---

# 121. No Audit Loss on Reconnect

A runtime SHALL NOT discard offline decision history after reconnecting.

---

# 122. Duplicate Receipt

Central ingestion SHALL be idempotent by:

```text
decision_id.
```

---

# 123. Decision Receipt Rejection

Central Regulations MAY flag a receipt:

```text
INVALID_PACKAGE

EXPIRED_LEASE

REVOKED_PACKAGE

UNKNOWN_RUNTIME

CONTEXT_MISMATCH

DUPLICATE_CONFLICT

CLOCK_ANOMALY.
```

---

# 124. Invalid Receipt Does Not Rewrite Operational History

If Trade already enforced the decision:

```text
enforcement occurred.
```

The system must record and remediate it.

Do not pretend it did not happen.

---

# 125. EnforcementReceipt

The PEP SHALL produce:

```text
EnforcementReceipt
```

after performing a consequential operational action.

---

# 126. EnforcementReceipt Chain

```text
RegulatoryDecision
      │
      ▼
PEP Enforcement
      │
      ▼
EnforcementReceipt
```

---

# 127. EnforcementReceipt Fields

Conceptually:

```text
decision_ref

domain_object_ref

domain_object_version

requested_disposition

actual_action

result

executed_at

PEP_identity

correlation_id

failure_reason?
```

---

# 128. PEP SHALL Validate Decision

Before enforcement:

```text
decision authentic

decision not stale

subject/context matches

effect class permits action

domain object version still matches

decision not revoked/superseded.
```

---

# 129. Time-of-Check / Time-of-Use

This is critical.

A decision may be valid for:

```text
Shipment version 12
```

while enforcement attempts to mutate:

```text
Shipment version 14.
```

---

# 130. PEP Must Detect This

Correct:

```text
RESOURCE_VERSION_MISMATCH
→ re-evaluate.
```

Rejected:

```text
use old decision anyway.
```

---

# 131. Domain Object Version

Consequential decisions SHOULD bind to:

```text
subject version

ETag

canonical state fingerprint

or equivalent optimistic-concurrency token.
```

---

# 132. Context Mutation

Changes such as:

```text
destination

importer

classification

quantity

shipment date
```

may invalidate regulatory decision.

---

# 133. PEP Re-evaluation

If material domain state changed:

```text
request new decision.
```

---

# 134. PEP Cannot Reinterpret Outcome

If Regulations returns:

```text
INDETERMINATE
```

the PEP SHALL NOT record:

```text
REGULATION_PROHIBITS.
```

---

# 135. PEP May Be More Operationally Conservative

Trade MAY decide:

```text
INDETERMINATE
→ HOLD
```

through an internal risk policy.

---

# 136. But It Must Say Why

Correct:

```text
Regulatory outcome:
INDETERMINATE

Trade internal disposition:
HOLD.
```

---

# 137. Internal Policy SHALL Remain Distinct

This is essential for audit and legal explainability.

---

# 138. PEP Cannot Weaken E4

If valid E4 says:

```text
BLOCK
```

a consumer SHALL not silently:

```text
PROCEED.
```

Any authorised override must follow governed override architecture.

---

# 139. PEP Cannot Escalate Effect Class

If decision is:

```text
E1 Advisory
```

Trade cannot treat it as:

```text
E4 legal block.
```

---

# 140. Local Runtime Delegation

Distributed regulatory execution SHALL require explicit:

```text
DelegatedExecutionAuthority.
```

---

# 141. DelegatedExecutionAuthority

Conceptually:

```text
DelegatedExecutionAuthority
├── runtime_ref
├── regulatory_profile
├── jurisdiction_scope[]
├── tenant_scope?
├── question_types[]
├── maximum_effect_class
├── offline_policy
├── effective_period
├── allowed_PEPs[]
└── provenance
```

---

# 142. Delegation Is Not Legal Delegation

This is internal software execution authority.

It SHALL not be confused with:

```text
statutory delegation of regulatory power.
```

---

# 143. Local Runtime Cannot Expand Scope

A runtime authorised for:

```text
CrossBorderGoods / ZA import / E3
```

cannot execute:

```text
employment law / Kenya / E4.
```

---

# 144. Package Scope Must Fit Delegation

Effective execution scope SHALL be the intersection of:

```text
runtime delegation

REP scope

decision policy

consumer capability

effect ceiling.
```

---

# 145. Tenant Scope

Shared public regulatory rules MAY be distributed broadly.

Tenant-private overlays SHALL remain tenant-isolated.

---

# 146. Avoid Per-Tenant Bundle Explosion

Baobab SHOULD separate:

```text
shared regulatory packages

tenant overlays
```

where practical.

---

# 147. But Isolation Comes First

Optimisation SHALL not risk:

```text
tenant private interpretation
```

leaking into another tenant's execution package.

---

# 148. Package Composition

Potential:

```text
Base Jurisdiction Package
        +
Regulatory Profile Package
        +
Tenant Overlay
        ↓
Resolved Runtime Execution Package
```

---

# 149. Composition SHALL Be Deterministic

Every effective package must have:

```text
one identifiable fingerprint.
```

---

# 150. OPA Bundle Roots

OPA bundle manifests support explicit data/policy ownership roots.

Baobab MAY use non-overlapping roots where multiple bundles are loaded.

---

# 151. Root Collisions

Bundle composition SHALL fail rather than silently create conflicting ownership.

---

# 152. Static Regulatory Data

OPA bundle `data` MAY contain:

```text
verified threshold tables

country/regime membership

classification support data

regulatory constants.
```

---

# 153. Transaction Facts Do Not Belong in Bundle

Per-request facts SHALL normally enter via:

```text
input.
```

---

# 154. Why

Embedding transaction state in policy bundle would cause:

```text
staleness

privacy risk

bundle explosion

replay ambiguity.
```

---

# 155. PEP Data Ownership

Trade remains authoritative for:

```text
shipment/order state.
```

ERP remains authoritative for its facts.

Regulations package contains:

```text
regulatory semantics.
```

---

# 156. Decision Telemetry Privacy

Decision logs may contain sensitive inputs.

OPA provides decision-log masking facilities for removing or modifying sensitive fields before upload.

Baobab SHALL use masking or equivalent filtering.

---

# 157. Data Residency

Decision telemetry SHALL comply with:

```text
tenant isolation

regional residency

privacy classification.
```

---

# 158. Full Input Need Not Be Centralized

Where residency requires:

```text
DecisionReceipt
```

MAY contain:

```text
canonical IDs

hashes

reason codes

bounded facts
```

instead of complete transaction payload.

---

# 159. Provenance Must Still Be Sufficient

Privacy minimisation SHALL not destroy decision reproducibility.

---

# 160. OPA Network Exposure

Local OPA endpoints SHOULD be:

```text
loopback/private network only

not publicly exposed.
```

---

# 161. Sidecar Architecture

OPA's Kubernetes guidance identifies application sidecars as appropriate where low-latency local policy decisions are needed; sidecar and application share the pod/network namespace and communicate locally.

This is the preferred future distributed OPA topology for containerized Baobab domain engines.

---

# 162. But Runtime Sidecar May Contain More Than OPA

Preferred:

```text
PEP Pod
├── domain engine
├── baobab-regulatory-runtime
└── OPA
```

or a combined bounded runtime where operationally appropriate.

---

# 163. Why Separate Baobab Runtime Layer

It enforces:

```text
REP validation

effect ceilings

context schema

freshness

result schema

receipt generation.
```

Raw OPA does not know these Baobab domain requirements.

---

# 164. Embedded OPA

OPA also supports Go embedding and other integration options.

A future Go-based Regulations runtime MAY use embedded OPA where deployment simplicity justifies it.

---

# 165. Wasm

OPA supports compiling policies to WebAssembly for embedded policy evaluation.

Wasm SHALL remain a future execution option.

---

# 166. Wasm High-Assurance Gate

Consistent with ADR-REG-0016:

```text
Wasm E3/E4
```

requires semantic-conformance testing against the authoritative evaluator profile.

---

# 167. Browser Execution

Regulatory E3/E4 policy SHALL NOT initially execute authoritatively inside untrusted end-user browsers.

---

# 168. Why

Browser runtime cannot be assumed to provide:

```text
trusted context

trusted clock

secret keys

tamper-resistant enforcement

reliable telemetry.
```

---

# 169. Browser May Simulate

E0/E1 planning tools MAY eventually use bounded local policy projections for:

```text
estimates

explanations

previews.
```

They SHALL not create authoritative enforcement decisions.

---

# 170. Central PDP Availability

Central Regulations API has:

```text
simpler governance
```

but adds:

```text
network latency

network dependency.
```

---

# 171. Distributed PDP Availability

Near-PEP execution improves:

```text
latency

network-failure tolerance

horizontal scaling.
```

But introduces:

```text
policy distribution

version skew

revocation

telemetry

reconciliation complexity.
```

---

# 172. Therefore Distribution Is Selective

Baobab SHALL not distribute execution merely because OPA supports it.

---

# 173. Distribution Eligibility

A capability is a good candidate where:

```text
high request volume

tight latency budget

offline resilience needed

rules deterministic

inputs local

package reasonably bounded

decision semantics stable.
```

---

# 174. Central Execution Remains Appropriate Where

```text
complex multi-engine facts

heavy evidence retrieval

frequent human review

dynamic authority decisions

low request rate

high sensitivity to package freshness.
```

---

# 175. Example — Trade Shipment Gate

Potentially suitable for local execution after maturity:

```text
precompiled shipment prerequisites

document requirements

hard prohibitions

permit validity facts.
```

---

# 176. Example — Complex Regulatory Interpretation

Not suitable:

```text
unresolved hierarchy

legal discretion

newly ingested regulation

human review.
```

This remains central/slow-path.

---

# 177. Local Runtime Is Fast Path Only

It SHALL not run:

```text
Docling

Haystack research

Qdrant legal discovery

LLM interpretation

LangGraph legal review.
```

---

# 178. Distributed Package Origin

Only canonical published Regulations state may produce distributed execution packages.

---

# 179. No Local Rule Authoring

Domain teams SHALL NOT patch local Rego to:

```text
"fix"
```

a regulation.

---

# 180. No Local Emergency Rego Patch

Even emergencies SHALL use:

```text
governed Regulations change
→ new REP
→ expedited distribution.
```

---

# 181. Local PEP-Specific Operational Policy

The PEP may maintain its own:

```text
internal risk policy

workflow policy.
```

That policy SHALL be separately identified from regulatory bundles.

---

# 182. Example

```text
Regulatory package:
missing permit → UNSATISFIED / E3

Trade internal policy:
E3 unsatisfied → shipment HOLD.
```

---

# 183. Separate OPA Namespaces/Bundles

If both use OPA:

```text
regulatory policy
```

and:

```text
Trade operational policy
```

SHOULD use separate packages/bundles/namespaces and provenance.

---

# 184. IAM OPA Remains Separate Too

IAM/security authorization OPA policy SHALL remain distinct from regulatory OPA policy.

---

# 185. Same Engine Technology ≠ Same Authority

```text
OPA
```

is merely a common runtime technology.

---

# 186. Decision Request Contract

PEP SHALL submit a canonical:

```text
RegulatoryEvaluationRequest
```

rather than arbitrary OPA input.

---

# 187. Evaluation Request

Conceptually:

```text
RegulatoryEvaluationRequest
├── request_id
├── question
├── regulatory_profile
├── context_assertion/snapshot
├── subject_ref
├── subject_version
├── legal_time
├── evidence refs/state
├── decision stage
└── trace context
```

---

# 188. Runtime Builds OPA Input

The Baobab runtime adapter translates this into:

```text
OPA input.
```

---

# 189. PEP Does Not Build Rego-Specific Input

This preserves provider neutrality.

---

# 190. Decision Output Contract

Runtime returns:

```text
RegulatoryDecision
```

or a compatible delegated decision envelope.

---

# 191. PEP Validates Output Contract

It SHALL not directly inspect internal:

```text
OPA AST

Rego package internals.
```

---

# 192. Split-Brain Risk

Distributed runtimes may temporarily have different revisions.

Example:

```text
Trade runtime A → Package 12

Trade runtime B → Package 13.
```

---

# 193. Split-Brain SHALL Be Observable

Distribution controller must know:

```text
active revision per runtime.
```

---

# 194. E4 Split-Brain Default

During E4 production rollout:

> **Two materially different policy revisions SHALL NOT simultaneously make independent authoritative enforcement decisions for the same declared execution cohort unless the rollout explicitly permits it.**

---

# 195. Canary Isolation

CANARY revision SHALL apply only to:

```text
explicit cohort

tenant

runtime

traffic partition.
```

---

# 196. Shadow Is Safer

Preferred validation:

```text
old ACTIVE evaluates
+
new SHADOW evaluates
+
compare
```

before new revision becomes authoritative.

---

# 197. Decision Diff

Shadow evaluation SHOULD compare:

```text
outcome

requirements

prohibitions

unknowns

effect class

reason codes.
```

---

# 198. Expected Difference

A regulatory change may intentionally alter outcomes.

Such difference requires:

```text
approved impact analysis.
```

---

# 199. Unexpected Difference

Blocks rollout.

---

# 200. Rollout Sequence

Preferred:

```text
BUILD
  ↓
VALIDATE
  ↓
GOLDEN TEST
  ↓
SHADOW
  ↓
COMPARE
  ↓
CANARY
  ↓
VERIFY
  ↓
ACTIVE
  ↓
RECONCILE.
```

---

# 201. Changeset Governance

Material E3/E4 rollout SHALL follow platform controlled-change principles:

```text
plan

impact

approval

execution

desired state

reconciliation

readiness

verification.
```

---

# 202. Rollback

Operational package rollback SHALL be possible.

---

# 203. Rollback Does Not Change Law

If Package 14 implementation is faulty but RuleSet 14 is legally correct:

```text
runtime rollback
```

does not mean:

```text
law reverted.
```

---

# 204. Important Consequence

If old package no longer represents current law:

```text
rollback to old enforcement
```

may be unsafe.

---

# 205. Safe Rollback Options

May include:

```text
central Regulations fallback

E2 review mode

temporary hold

corrected package.
```

---

# 206. Never Blindly Roll Back Legal Semantics

Rollback strategy SHALL distinguish:

```text
implementation regression
```

from:

```text
regulatory-version change.
```

---

# 207. Central Fallback

Distributed runtime MAY fall back to central Regulations where:

```text
network available

central provider healthy

context valid.
```

---

# 208. Fallback Must Be Governed

It SHALL not happen silently where the central and local revisions differ.

---

# 209. Fallback Validation

Before fallback:

```text
expected RuleSet compatibility
```

SHOULD be established.

---

# 210. Local-to-Central Fallback Result

Decision provenance SHALL identify:

```text
execution_topology = CENTRAL_FALLBACK.
```

---

# 211. Multi-Region

Distributed runtimes MAY support regional placement for:

```text
latency

residency

availability.
```

---

# 212. Regulatory Package Replication

Signed immutable packages are well suited to cross-region replication.

---

# 213. Canonical Authoring Remains Singular

Regional copies SHALL not create:

```text
regional independent legal interpretations
```

unless they are separately governed canonical overlays.

---

# 214. Data Residency

Business facts may remain in-region while:

```text
regulatory package
```

is globally replicated where rights permit.

---

# 215. Decision Receipt Residency

Receipt transmission MAY be regionalised or redacted as appropriate.

---

# 216. Regional Outage

A region MAY continue within execution lease when approved.

---

# 217. Clock Integrity

Distributed lease and temporal checks depend on reliable time.

Runtime SHALL monitor:

```text
clock skew

timezone configuration

synchronisation health.
```

---

# 218. Clock Used for Two Different Purposes

```text
legal event time
```

comes from regulatory/business context.

```text
runtime current time
```

is used for:

```text
lease

expiry

operational freshness.
```

---

# 219. Runtime Clock Does Not Define Legal Event Time

Hard invariant.

---

# 220. Clock Anomaly

Excessive clock skew SHALL reduce or remove high-assurance delegated execution authority.

---

# 221. Security Boundary

Distributed policy artifacts are consequential code.

They SHALL be treated as software-supply-chain artifacts.

---

# 222. Required Controls

High-assurance deployment SHOULD include:

```text
artifact signing

hash verification

authenticated transport

least privilege

immutable artifacts

version pinning

runtime admission controls

audit.
```

---

# 223. Package Source

Runtime SHALL accept regulatory packages only from configured trusted distribution sources.

---

# 224. No Arbitrary Bundle URL

PEP SHALL not choose:

```text
bundle_url=https://random.example
```

per request.

---

# 225. No Runtime Policy Mutation API for Consumers

OPA mutation endpoints SHALL not be exposed to ordinary domain services for regulatory policy.

---

# 226. Bundle-Owned Roots

OPA protects bundle-owned policy/data from ordinary REST mutation by default.

Baobab SHALL retain that protection.

---

# 227. Runtime Identity

Each distributed runtime SHALL have canonical:

```text
runtime_id / engine_instance_id
```

and authenticated service identity.

---

# 228. Runtime Labels

Useful labels include:

```text
environment

region

engine

instance

deployment

regulatory profile.
```

OPA status itself reports a globally unique agent ID and OPA version among its labels.

---

# 229. Runtime Registration

Control Plane may register engine topology.

Regulations registers its execution/package state against that canonical runtime identity.

---

# 230. Runtime Upgrade

OPA/runtime version upgrades SHALL follow compatibility testing.

---

# 231. Package Runtime Compatibility

REP SHALL declare:

```text
minimum runtime version

supported evaluator version range.
```

---

# 232. Unsupported Runtime

Result:

```text
RUNTIME_INCOMPATIBLE.
```

No consequential execution.

---

# 233. Observability

The distributed execution architecture SHALL expose:

```text
decision latency

OPA evaluation latency

runtime availability

active revision

expected revision

bundle age

activation lag

bundle failures

decision volume

decision outcome counts

effect-class counts

offline decision counts

reconciliation backlog.
```

---

# 234. OPA Monitoring

OPA exposes Prometheus metrics including bundle load success/failure and last successful bundle activation/download.

Baobab SHOULD ingest these into platform observability.

---

# 235. Regulatory Metrics Above OPA

OPA metrics are insufficient by themselves.

Baobab also needs:

```text
regulatory package freshness

RuleSet alignment

decision receipt reconciliation

effect-class readiness

staleness exposure.
```

---

# 236. Alert Examples

```text
E4 runtime on stale package

expected revision not activated

bundle signature failure

runtime not reporting

offline lease nearing expiry

decision receipts not reconciling

different revisions in same enforcement cohort.
```

---

# 237. Decision Correlation

Across:

```text
PEP
Regulatory Runtime
OPA
Regulations
```

propagate:

```text
trace_id

request_id

decision_id

package_revision.
```

---

# 238. OpenTelemetry

Platform distributed traces SHOULD correlate these boundaries.

---

# 239. Observability Is Not Canonical Provenance

Logs/traces may expire.

Decision receipts and canonical decision state remain durable.

---

# 240. Performance

The purpose of distributed evaluation is primarily:

```text
lower latency

higher local availability

scalability.
```

---

# 241. But Premature Distribution Is Rejected

The first production version SHOULD prove central Regulations decision quality before distributing authority.

---

# 242. Distribution Promotion Gate

A regulatory profile SHOULD become locally executable only after:

```text
central production maturity

stable BRIR

stable DecisionPolicy

golden-case coverage

shadow equivalence

runtime package support

reconciliation tested

failure-mode testing.
```

---

# 243. Initial Production Recommendation

Initial go-live:

```text
Regulations API
    │
    ▼
internal co-located OPA
```

with:

```text
Trade / ERP as remote PEPs.
```

---

# 244. Phase 2

Introduce:

```text
Trade Regulatory Runtime
```

in SHADOW mode.

---

# 245. Phase 3

Allow bounded:

```text
E0/E1 local decisions.
```

---

# 246. Phase 4

Allow selected:

```text
E2/E3 local decisions
```

after reconciliation/freshness controls prove reliable.

---

# 247. Phase 5

Consider:

```text
E4 local autonomous enforcement
```

only for sufficiently deterministic and mature profiles.

---

# 248. No Requirement to Reach Phase 5 Everywhere

Some regulatory domains SHOULD remain central permanently.

---

# 249. Example — Central ZuriBeans Decision

```text
Trade
  │
  │ shipment S
  ▼
Regulations
  │
  ├── resolve context
  ├── select ruleset
  ├── evaluate OPA
  └── issue D123
  │
  ▼
Trade
  │
  └── HOLD shipment
      because D123 = UNSATISFIED / E3
```

---

# 250. Example — Future Local ZuriBeans Decision

```text
Trade
  │
  ▼
Regulatory Runtime
  │
  ├── validates REP-57
  ├── confirms lease
  ├── validates context
  ├── invokes local OPA
  ├── assembles Decision D400
  └── writes durable receipt
  │
  ▼
Trade PEP
  │
  ▼
HOLD
```

Later:

```text
D400 receipt
    ↓
Regulations reconciliation
```

---

# 251. Example — Stale Local Package

```text
Local:
REP-57

Expected:
REP-58

REP-58 contains
currently effective rule change.

Effect:
E3.
```

Result:

```text
Runtime:
STALE

Regulatory outcome:
INDETERMINATE

Disposition:
HOLD / central fallback.
```

Not:

```text
evaluate stale package anyway.
```

---

# 252. Example — Advisory Staleness

```text
E1 regulatory guidance
package slightly beyond preferred refresh
but within approved advisory window.
```

Possible:

```text
DEGRADED advisory result
+
staleness warning.
```

---

# 253. Example — Invalid Bundle Signature

OPA rejects new bundle and preserves previous bundle.

Baobab records:

```text
BUNDLE_SIGNATURE_FAILURE

expected revision unavailable.
```

If old package no longer satisfies freshness:

```text
NOT_READY.
```

---

# 254. Example — Network Partition

```text
Trade runtime:
online

Regulations:
unreachable

bundle server:
unreachable

current package:
signed
lease valid

effect:
E1
```

Evaluation MAY continue.

---

# 255. Same Partition, E4

Initial default:

```text
no fresh revocation/freshness assurance
    ↓
E4 disabled
    ↓
INDETERMINATE / HOLD
```

unless profile has explicit bounded offline E4 approval.

---

# 256. Example — Object Changed After Decision

```text
D100 evaluated shipment version 8.

Before enforcement:
destination changed.

Shipment now version 9.
```

PEP:

```text
rejects D100 as stale
and requests reassessment.
```

---

# 257. Example — Internal Risk Policy

Regulations:

```text
SATISFIED_WITH_REQUIREMENTS
E1
```

Trade policy:

```text
requires manager approval.
```

Trade may hold operationally.

Audit must show:

```text
LEGAL RESULT:
SATISFIED_WITH_REQUIREMENTS

INTERNAL CONTROL:
MANAGER_APPROVAL_REQUIRED.
```

---

# 258. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-PDP-I01` | Regulations SHALL remain canonical regulatory decision authority |
| `REG-PDP-I02` | OPA SHALL remain an execution provider |
| `REG-PDP-I03` | PEPs SHALL remain owners of domain-state mutation |
| `REG-PDP-I04` | Domain engines SHALL not reinterpret regulatory policy independently |
| `REG-PDP-I05` | Initial PEPs SHALL invoke Regulations rather than raw Regulations OPA |
| `REG-PDP-I06` | Distributed execution SHALL use a Baobab Regulatory Runtime |
| `REG-PDP-I07` | Local PEPs SHALL not call raw Rego entrypoints as the business contract |
| `REG-PDP-I08` | REP SHALL remain distinct from an OPA bundle |
| `REG-PDP-I09` | Every distributed execution package SHALL be immutable and versioned |
| `REG-PDP-I10` | High-assurance OPA bundles SHALL be signed |
| `REG-PDP-I11` | OPA bundle activation time SHALL not define legal-effective time |
| `REG-PDP-I12` | Runtime health SHALL remain distinct from regulatory readiness |
| `REG-PDP-I13` | Existing active bundle SHALL not automatically be considered safe after failed update |
| `REG-PDP-I14` | Package freshness SHALL be policy/profile specific |
| `REG-PDP-I15` | Unbounded offline E4 SHALL be prohibited by default |
| `REG-PDP-I16` | Distributed execution SHALL carry an explicit effect-class ceiling |
| `REG-PDP-I17` | Local runtimes SHALL not expand delegated scope |
| `REG-PDP-I18` | Tenant-private regulatory overlays SHALL remain isolated |
| `REG-PDP-I19` | Transaction facts SHALL normally remain runtime input, not bundle data |
| `REG-PDP-I20` | Local policy mutation by consumers SHALL be prohibited |
| `REG-PDP-I21` | Decision receipts SHALL identify exact package and RuleSet revision |
| `REG-PDP-I22` | Offline consequential decisions SHALL be durably queued for reconciliation |
| `REG-PDP-I23` | OPA decision logs SHALL not replace canonical decision receipts |
| `REG-PDP-I24` | PEPs SHALL validate domain-object version before enforcement |
| `REG-PDP-I25` | PEPs SHALL not transform INDETERMINATE into legal PROHIBITED |
| `REG-PDP-I26` | PEP internal risk policy SHALL remain distinguishable from regulation |
| `REG-PDP-I27` | PEPs SHALL not escalate regulatory effect class |
| `REG-PDP-I28` | Split-brain package revisions SHALL be observable and governed |
| `REG-PDP-I29` | Rollback SHALL distinguish runtime failure from legal-state change |
| `REG-PDP-I30` | Replacing OPA SHALL not require changing PEP business contracts |

---

# 259. Rejected Alternative — PEP Calls Raw OPA

Rejected.

It bypasses the Baobab decision domain.

---

# 260. Rejected Alternative — Central OPA Shared by Every Engine Directly

Rejected as the primary regulatory contract.

This creates:

```text
tight Rego coupling

semantic leakage

weak decision lifecycle

weak effect-class governance.
```

---

# 261. Rejected Alternative — Copy Rego into Trade

Rejected.

---

# 262. Rejected Alternative — Trade Authors Regulatory Rego

Rejected.

---

# 263. Rejected Alternative — OPA Bundle Is Canonical Rule Package

Rejected.

REP remains the Baobab-level package.

---

# 264. Rejected Alternative — Unsigned E4 Bundles

Rejected.

---

# 265. Rejected Alternative — Delta Bundles for Initial E4 Policy

Rejected because current OPA delta bundles do not support signing and have additional persistence limitations.

---

# 266. Rejected Alternative — Health 200 Means Ready

Rejected.

OPA's own health semantics require additional status monitoring after initial activation.

---

# 267. Rejected Alternative — Last Good Bundle Always Safe

Rejected.

The law may have changed.

---

# 268. Rejected Alternative — Infinite Offline Execution

Rejected for consequential policy.

---

# 269. Rejected Alternative — Network Failure Means Legal Prohibition

Rejected.

Correct:

```text
INDETERMINATE
+
conservative operational disposition.
```

---

# 270. Rejected Alternative — Bundle Expiry Means Law Expired

Rejected.

---

# 271. Rejected Alternative — Bundle Activation Means Law Became Effective

Rejected.

---

# 272. Rejected Alternative — Scheduler Is Legal Authority

Rejected.

---

# 273. Rejected Alternative — PEP May Ignore Subject Version

Rejected.

Creates TOCTOU enforcement errors.

---

# 274. Rejected Alternative — Internal Risk Policy Re-labelled as Regulation

Rejected.

---

# 275. Rejected Alternative — Browser as Authoritative E4 PDP

Rejected initially.

---

# 276. Rejected Alternative — Every Regulatory Domain Must Become Distributed

Rejected.

Distribution is a profile-specific optimisation.

---

# 277. Rejected Alternative — Control Plane Owns Regulatory Bundles

Rejected.

Control Plane owns platform topology/capability resolution.

Regulations owns regulatory semantics and execution packages.

---

# 278. Minimum Implementation Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text
1. Central Regulations PDP topology.

2. Trade as PEP.

3. ERP as separate PEP seam.

4. OPA hidden behind Regulations contract.

5. Raw OPA access unavailable to consumers.

6. RegulatoryExecutionPackage schema.

7. REP manifest.

8. Immutable package revision.

9. RuleSet fingerprint.

10. BRIR/compiler provenance.

11. OPA bundle nested/referenced by REP.

12. Rego v1 bundle.

13. Signed OPA snapshot bundle.

14. Signed REP envelope.

15. Signature-failure test.

16. Old bundle remains active after failed OPA activation.

17. Baobab detects old bundle as stale when required.

18. Desired runtime state.

19. Observed runtime state.

20. OPA Status API ingestion.

21. OPA runtime ID/version capture.

22. Expected vs active revision reconciliation.

23. `/health` initial activation test.

24. Proof that health alone is insufficient after later bundle failure.

25. Bundle download failure.

26. Bundle activation failure.

27. Bundle persistence/restart test.

28. Persisted bundle lease validation.

29. Regulatory runtime READY state.

30. DEGRADED state.

31. STALE state.

32. NOT_READY state.

33. REVOKED state.

34. Profile-specific freshness policy.

35. Effect-class-specific offline policy.

36. E1 bounded offline decision.

37. E3 lease-expired denial.

38. Default E4 offline rejection.

39. Revocation event.

40. Revoked package cannot issue new decisions.

41. Future-effective rule pre-deployed.

42. Legal-time activation without bundle download.

43. Emergency package rollout.

44. SHADOW package.

45. Current-vs-shadow decision diff.

46. CANARY package.

47. Controlled ACTIVE promotion.

48. Package rollback.

49. Rollback blocked where old package represents obsolete law.

50. Central fallback.

51. Fallback revision compatibility test.

52. Baobab Regulatory Runtime abstraction.

53. Local OPA sidecar prototype.

54. PEP calls Runtime, not raw OPA.

55. DelegatedExecutionAuthority.

56. Jurisdiction scope enforcement.

57. Regulatory profile scope enforcement.

58. Effect-class ceiling enforcement.

59. Tenant overlay isolation.

60. Shared package + tenant overlay composition.

61. Composition fingerprint.

62. No transaction facts embedded in static bundle.

63. RegulatoryEvaluationRequest contract.

64. Provider-neutral runtime input adapter.

65. RegulatoryDecision output.

66. RegulatoryDecisionReceipt.

67. Globally unique local decision ID.

68. Durable offline receipt outbox.

69. Central receipt reconciliation.

70. Duplicate receipt idempotency.

71. Invalid receipt detection.

72. OPA decision ID correlation.

73. OPA bundle revision correlation.

74. Decision-log masking.

75. Decision log upload failure.

76. Consequential decision still durably receipted locally.

77. EnforcementReceipt.

78. Subject object-version binding.

79. TOCTOU stale-decision rejection.

80. Context mutation forces reevaluation.

81. PEP cannot escalate E1 to E4.

82. PEP cannot rewrite INDETERMINATE as PROHIBITED.

83. Internal Trade hold recorded separately from legal outcome.

84. Split-brain revision detection.

85. E4 enforcement cohort revision consistency.

86. Runtime clock-skew detection.

87. Excessive clock skew disables high-assurance offline execution.

88. Runtime version incompatibility.

89. OPA upgrade compatibility test.

90. Signed package verification keys bootstrapped outside package.

91. Optional signed OPA Discovery proof.

92. Discovery-key trust-root test.

93. Multi-region package replication.

94. Region-aware decision receipt.

95. Data-residency-safe telemetry.

96. Prometheus OPA bundle metrics.

97. Regulatory freshness metrics.

98. Distribution lag alert.

99. Reconciliation backlog alert.

100. End-to-end decision → enforcement → receipt → canonical reconciliation.
```

---

# 279. Initial Rollout Recommendation

The initial implementation SHALL use:

```text
                      baobab-regulations
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Decision Engine               OPA
                 │
                 ▼
         RegulatoryDecision
                 │
         ┌───────┴─────────┐
         ▼                 ▼
   baobab-trade         baobab-erp
       PEP                  PEP
```

No distributed OPA in Trade for the first production gate.

---

# 280. Why

This gives Baobab time to validate:

```text
rule correctness

decision semantics

coverage

effect classes

decision trace

enforcement contracts
```

before adding distributed consistency problems.

---

# 281. Second Rollout Stage

Introduce:

```text
Trade Regulatory Runtime
```

in:

```text
SHADOW
```

mode.

---

# 282. Shadow Architecture

```text
                     Trade Request
                          │
                 ┌────────┴─────────┐
                 ▼                  ▼
           Regulations          Local Runtime
             ACTIVE               SHADOW
                 │                  │
                 ▼                  ▼
             Decision A         Decision B
                 │                  │
                 └────────┬─────────┘
                          ▼
                      Comparator
```

Only Decision A is enforced.

---

# 283. Promotion Criteria

Local runtime proceeds beyond SHADOW only after:

```text
semantic equivalence demonstrated

known expected regulatory deltas understood

failure cases validated

receipt reconciliation proven

staleness/revocation proven.
```

---

# 284. Strategic Architecture

The resulting architecture becomes:

```text
                         LEGAL AUTHORITY
                              │
                              ▼
                      REGULATORY SOURCES
                              │
                              ▼
                    BAOBAB REGULATIONS
                       CANONICAL TRUTH
                              │
                              ▼
                         RULE VERSION
                              │
                              ▼
                            BRIR
                              │
                              ▼
                        RULESET SNAPSHOT
                              │
                              ▼
                  REGULATORY DECISION POLICY
                              │
                              ▼
                REGULATORY EXECUTION PACKAGE
                              │
                 signed / versioned / scoped
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Central Runtime   Trade Runtime    ERP Runtime
             │                │                │
             ▼                ▼                ▼
            OPA              OPA              OPA
             │                │                │
             ▼                ▼                ▼
       Regulatory         Regulatory       Regulatory
        Decision            Decision         Decision
             │                │                │
             ▼                ▼                ▼
            PEP              PEP              PEP
             │                │                │
             ▼                ▼                ▼
        ENFORCEMENT       ENFORCEMENT      ENFORCEMENT
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                         RECEIPTS
                              │
                              ▼
                        REGULATIONS
                       RECONCILIATION
```

---

# 285. The Most Important Boundary

Even when evaluation is fully distributed:

```text
Legal Source
      ↓
Interpretation
      ↓
RuleVersion
      ↓
BRIR
      ↓
DecisionPolicy
      ↓
REP
```

remains controlled by:

```text
baobab-regulations.
```

---

# 286. The PEP Never Becomes Regulatory Authority

It receives:

```text
a signed executable projection
```

of canonical regulatory semantics.

---

# 287. The Local OPA Never Becomes Regulatory Authority

It evaluates:

```text
a compiled executable projection.
```

---

# 288. The Bundle Server Never Becomes Regulatory Authority

It distributes:

```text
artifacts.
```

---

# 289. The Control Plane Never Becomes Regulatory Authority

It resolves:

```text
provider

context

capability

topology.
```

---

# 290. Source of Truth Remains Clear

```text
Regulatory semantic truth
    → baobab-regulations / PostgreSQL

Compiled runtime artifact
    → REP / OPA bundle

Runtime evaluation
    → OPA / evaluator

Canonical regulatory decision
    → Regulations decision contract

Domain mutation
    → PEP/domain engine.
```

---

# 291. Research Foundation Summary

OPA formally separates Policy Decision Points from Policy Enforcement Points and recommends locating policy engines close to enforcement points where latency and network resilience matter. This validates Baobab's future near-PEP execution option while not requiring distributed execution initially.

OPA's management architecture is explicitly designed for distributed policy enforcement and provides bundle distribution, decision logs, status and discovery mechanisms. OPA does not itself provide the higher-level policy control plane, which means Baobab Regulations must own desired-state, regulatory package governance, readiness, reconciliation and legal-semantic versioning above OPA.

OPA bundles support live policy/data updates, revisions, ETags, persistence of successfully activated bundles and signature verification. On failed signature or activation, the previous bundle remains active, making Baobab-level expected-revision and freshness checks essential whenever regulatory law has changed.

OPA's Status API reports active bundle revision, download/activation timestamps and failures, runtime labels/version and plugin state. This provides the lower-level telemetry needed for Baobab's distributed regulatory-runtime reconciliation.

OPA's health endpoint can include initial bundle/plugin readiness but does not detect all subsequent bundle-update failures; the Status API is required for ongoing bundle-state monitoring. Baobab therefore separates process health from regulatory readiness.

OPA decision logs provide decision IDs, trace IDs, bundle revisions and policy paths, and support sensitive-data masking. These facilities become execution provenance beneath Baobab's canonical RegulatoryDecision and DecisionReceipt rather than replacing them.

OPA Discovery can centralise runtime configuration and can itself be signed. Because a discovery bundle may distribute keys for ordinary policy bundles, OPA recommends signing discovery and bootstrapping its verification key independently.

OPA supports WebAssembly and embedded execution in addition to server-based REST evaluation, preserving future options for even tighter local decision execution. Baobab nevertheless requires semantic-equivalence testing before consequential Wasm deployment.

---

# 292. Final Decision

Baobab Regulations SHALL establish a strict:

# **Regulatory PDP / PEP Separation**

with the following authority chain:

```text
                    EXTERNAL LEGAL AUTHORITY
                              │
                              ▼
                    BAOBAB REGULATIONS
                    CANONICAL KNOWLEDGE
                              │
                              ▼
                           BRIR
                              │
                              ▼
                     DECISION POLICY
                              │
                              ▼
                  REGULATORY EXECUTION
                         PACKAGE
                              │
               ┌──────────────┴───────────────┐
               ▼                              ▼
          CENTRAL PDP                 DELEGATED RUNTIME
               │                              │
               ▼                              ▼
              OPA                            OPA
               │                              │
               └──────────────┬───────────────┘
                              ▼
                   REGULATORY DECISION
                              │
                              ▼
                   POLICY ENFORCEMENT
                         POINT
                              │
                              ▼
                    BUSINESS MUTATION
                              │
                              ▼
                   ENFORCEMENT RECEIPT
```

The authority rule is:

> **Baobab Regulations owns regulatory meaning and decision semantics; OPA evaluates compiled policy; the domain PEP owns operational enforcement.**

The distribution rule is:

> **Only signed, versioned, scoped and governed Regulatory Execution Packages may delegate consequential regulatory evaluation away from the central Regulations service.**

The local-runtime rule is:

> **A PEP SHALL consume a Baobab Regulatory Runtime contract—not raw Rego or an arbitrary OPA package.**

The freshness rule is:

> **The fact that a policy bundle is loaded does not mean it is sufficiently current to make a regulatory decision.**

The offline rule is:

> **Offline execution authority is bounded by explicit freshness, effect-class and revocation policy; unbounded offline E4 enforcement is prohibited by default.**

The failure rule is:

> **Infrastructure failure produces uncertainty or degraded readiness—it does not manufacture a legal prohibition.**

The enforcement rule is:

> **A PEP may be operationally more conservative than a regulatory decision, but it must preserve the distinction between its internal policy and the regulatory conclusion.**

The consistency rule is:

> **A regulatory decision applies to the exact domain state it evaluated; if that state changes before enforcement, the PEP must re-evaluate rather than enforce a stale decision.**

The rollout rule is:

> **Distributed regulatory execution shall progress from central → shadow → canary → bounded enforcement, with equivalence, freshness, reconciliation and failure semantics proven at every stage.**

And the strategic principle is:

> **Baobab can move the decision engine closer to the transaction without moving ownership of regulatory truth away from Baobab Regulations.**

That is the architecture established by `ADR-REG-0019`.

---

## Decision Summary

```text
ADR-REG-0019
────────────────────────────────────────────

AUTHORITY

Law
 ↓
Regulations
 ↓
BRIR
 ↓
Decision Policy
 ↓
Execution Package
 ↓
OPA
 ↓
RegulatoryDecision
 ↓
PEP
 ↓
Business Action


INITIAL TOPOLOGY

PEP
 ↓
Regulations API
 ↓
OPA


FUTURE TOPOLOGY

PEP
 ↓
Baobab Regulatory Runtime
 ↓
local OPA


NEVER

PEP
 ↓
raw OPA
 ↓
custom interpretation


DISTRIBUTION UNIT

RegulatoryExecutionPackage

NOT merely OPA bundle.


REP CONTAINS

RuleSet identity
BRIR/compiler provenance
DecisionPolicy
schemas
effect ceiling
freshness policy
target artifact
signature


OPA BUNDLES

Signed snapshot bundles
for high assurance.


OPA DELTA BUNDLES

Not initial E3/E4 path.


READINESS

Process healthy
≠
Regulatory ready.


READY REQUIRES

Expected revision
Correct RuleSet
Valid signature
Compatible runtime
Valid lease
No revocation


OFFLINE

E0/E1:
bounded tolerance possible

E2/E3:
explicit policy

E4:
no unbounded offline
execution by default


FRESHNESS

Loaded
≠
Current.


FAILED NEW BUNDLE

OPA may retain old bundle.

Baobab must determine
whether old bundle remains
regulatorily safe.


PEP

Owns operational mutation.

Does not own legal semantics.


TOCTOU

Decision for object V8
cannot enforce object V9
without reassessment.


INTERNAL POLICY

Trade HOLD
≠
law PROHIBITS.


DECISION RECEIPT

Exact package
Exact RuleSet
Exact context
Exact result
Exact runtime


ENFORCEMENT RECEIPT

Decision
 ↓
business mutation
 ↓
receipt


ROLLOUT

Central
 ↓
Shadow
 ↓
Canary
 ↓
Bounded distributed
 ↓
Selective autonomous


STRATEGIC RESULT

Move execution
closer to the transaction

without moving
regulatory authority.
```
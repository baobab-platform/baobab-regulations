# ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider

**Status:** Proposed — Normative Target Architecture  
**Decision ID:** `ADR-REG-0002`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Decision Type:** Foundational Runtime and Integration Architecture  
**Date:** 2026-09-27  
**Strategic Classification:** Platform Differentiator / Regulatory Infrastructure  
**Parent Decision:** `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`  
**Contract Authority:** `baobab-platform/shared`  
**Capability Resolution Authority:** `baobab-platform/baobab-cp`  
**Identity Authority:** Baobab IAM  
**Operational Enforcement Authorities:** Domain-owning Baobab engines  
**Primary Capability Namespace:** `regulations.*` — registered in Shared by ADR-SHARED-024 / RTD-08; individual capability keys remain subject to catalogue/contract/provider gates  
**Architecture Style:** Headless, capability-centric, provider-neutral, contract-first, context-resolved, event-enabled, independently deployable, multi-tenant  
**Initial Consumption Profile:** Service-to-service regulatory assessment for cross-border trade  
**Initial Proving Consumer:** ZuriBeans / Baobab Trade  
**Strategic Peer Engine:** Baobab Pulse

---

# 1. Executive Decision

Baobab Regulations SHALL be implemented as an **independently deployable headless Baobab capability provider**.

It SHALL expose regulatory capabilities through stable, implementation-neutral contracts defined by `baobab-platform/shared`.

It SHALL NOT require Digital Estates or other Baobab engines to understand:

```text
which framework Regulations uses
which database Regulations uses
which rule engine Regulations uses
which AI provider Regulations uses
which graph technology Regulations uses
which regulatory-content vendor Regulations uses
where a particular Regulations instance is deployed
```

The canonical relationship SHALL be:

```text
Regulatory Capability
        │
        ▼
Capability Provider
        │
        ▼
Baobab Regulations
        │
        ▼
Engine Instance
```

The runtime interaction SHALL follow the established Baobab capability architecture:

```text
Consumer
    │
    │ request capability
    ▼
Baobab Control Plane
    │
    │ resolve entitlement + context + provider
    ▼
Capability Resolution
    │
    ▼
Consumer
    │
    │ invoke authorised provider
    ▼
Baobab Regulations
    │
    ▼
Regulatory Assessment / Decision
```

The Control Plane SHALL determine:

```text
WHO
FOR WHICH TENANT
FOR WHICH LEGAL ENTITY
THROUGH WHICH DIGITAL ESTATE
IN WHICH MARKET / GEOGRAPHY
IS ENTITLED TO WHICH REGULATORY CAPABILITY
USING WHICH PROVIDER
ON WHICH AUTHORISED ENGINE INSTANCE
UNDER WHICH ISOLATION / RESIDENCY CONDITIONS.
```

Baobab Regulations SHALL determine:

```text
WHICH REGULATORY RULES APPLY
TO THE SUPPLIED REGULATORY CONTEXT
AT THE RELEVANT TIME
AND WHAT REGULATORY CONSEQUENCE FOLLOWS.
```

These responsibilities SHALL remain separate.

The governing rule is:

> **Control Plane determines whether and where Baobab Regulations may be consumed. Baobab Regulations determines regulatory meaning. The operational engine determines how an authorised regulatory decision is enforced.**

---

# 2. Context

`ADR-REG-0001` establishes Baobab Regulations as the platform's **Regulatory Context and Execution Engine**.

That ADR deliberately defers implementation technology.

The next architectural problem is therefore:

> How does this regulatory capability participate in Baobab without becoming a special-case service, a universal middleware layer, or a tightly coupled dependency of Trade?

The existing Baobab platform architecture already provides the answer.

`ADR-BCP-002` defines Baobab as capability-centric:

```text
Digital Estates consume capabilities.
Products compose capabilities.
Control Plane grants and resolves capabilities.
Engines provide capabilities.
Shared defines contracts.
```

`ADR-BCP-003` further distinguishes:

```text
Capability
CapabilityGrant
CapabilityScope
CapabilityProvider
CapabilityBinding
CapabilityResolution
```

`ADR-BCP-006` distinguishes:

```text
Capability
     ≠
Provider
     ≠
Engine
     ≠
EngineInstance
```

And `ADR-BCP-007` establishes the key runtime principle:

> **The Control Plane decides whether and where a capability may execute; the data plane executes it.**

Baobab Regulations SHALL conform to this architecture.

It SHALL NOT invent an alternative integration model merely because regulatory decisions are consequential.

---

# 3. Why "Headless" Is an Architectural Decision

The term **headless** SHALL have a precise meaning.

It does not merely mean:

```text
"there is no frontend yet"
```

It means the engine's authoritative functionality is exposed through:

```text
stable APIs
events
contracts
machine-readable decisions
```

rather than being trapped inside a user interface.

The canonical model SHALL therefore be:

```text
                    BAOBAB REGULATIONS

                    ┌────────────────┐
                    │ Domain Engine  │
                    │                │
                    │ Sources        │
                    │ Rules          │
                    │ Context        │
                    │ Assessments    │
                    │ Decisions      │
                    │ Change Impact  │
                    └───────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
           APIs           Events      Admin Contract
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                      Consumers
```

A future console MAY exist.

A Digital Estate MAY present regulatory functionality.

A Baobab administrative experience MAY allow rule verification.

None of those interfaces SHALL define the regulatory domain.

---

# 4. Headless Does Not Mean Browser-Callable

The engine being headless SHALL NOT imply that browsers directly invoke internal engine instances.

The preferred public-facing pattern remains:

```text
Browser / Digital Estate
          │
          ▼
      Estate BFF
          │
          ├──────────► Control Plane
          │               capability resolution
          │
          ▼
Baobab Regulations
```

Browsers SHALL NOT be trusted to supply authoritative:

```text
tenant_id
legal_entity_id
capability_binding
provider_id
engine_instance_id
isolation_profile
residency_profile
```

The same browser trust boundary already established by the Control Plane architecture SHALL apply.

---

# 5. Architectural Position

Baobab Regulations SHALL be one provider family within the Baobab data plane.

```text
                         BAOBAB CONTROL PLANE
                                │
                      Capability Resolution
                                │
        ┌───────────────────────┼──────────────────────┐
        │                       │                      │
        ▼                       ▼                      ▼
      Trade                    Pulse              Regulations
        │                       │                      │
        ▼                       ▼                      ▼
     Commerce               Intelligence           Regulatory
    Capabilities            Capabilities           Capabilities
```

No direct architectural hierarchy SHALL imply:

```text
Regulations > Trade
```

or:

```text
Regulations > ERP
```

or:

```text
Pulse > Regulations
```

These engines own different domains.

---

# 6. Engine Identity

The platform SHALL register Baobab Regulations as an Engine family.

Conceptually:

```text
Engine
├── engine_key: baobab-regulations
├── engine_type: DOMAIN_ENGINE
├── ownership: BAOBAB_PLATFORM
├── domain: REGULATORY
├── lifecycle_status
└── metadata
```

The exact persisted contract belongs to Control Plane.

The regulatory repository SHALL NOT redefine `Engine`.

---

# 7. Capability Provider Identity

Baobab Regulations SHALL declare one or more Capability Providers.

An initial provider identity MAY resemble:

```text
baobab-regulations.core
```

Provider identity SHALL remain separate from engine identity.

This permits future topology such as:

```text
Baobab Regulations Engine
          │
          ├── regulations.core
          ├── regulations.crossborder
          ├── regulations.tax
          └── regulations.enterprise-private
```

if deployment or commercial requirements eventually justify separate providers.

The initial implementation SHOULD remain simpler unless operational evidence requires such separation.

---

# 8. Engine Instance Identity

Each deployable runtime SHALL be represented by a Control Plane `EngineInstance`.

Conceptually:

```text
baobab-regulations-prod-africa-south-01

baobab-regulations-prod-africa-east-01

baobab-regulations-dedicated-client-x-01
```

The Control Plane SHALL determine which instance is eligible under:

```text
environment
region
residency
isolation
health
contract version
tenant
legal entity
capability binding
```

Consumers SHALL NOT select an instance directly.

---

# 9. Initial Capability Vocabulary

The initial canonical capability family SHOULD include:

```text
regulations.rule.query

regulations.applicability.evaluate

regulations.obligation.resolve

regulations.assessment.evaluate

regulations.decision.read

regulations.decision.explain

regulations.history.resolve

regulations.change.query

regulations.change.subscribe

regulations.impact.evaluate

regulations.evidence.bundle

regulations.crossborder.evaluate
```

These are conceptual candidate keys.

ADR-SHARED-024 / RTD-08 has registered the top-level `regulations` namespace in Shared, but it has **not** catalogued these individual keys. Final capability registration SHALL still occur through `baobab-platform/shared` after contract and implementation evidence gates are satisfied.

---

# 10. Capability Names Describe What, Not How

Valid:

```text
regulations.assessment.evaluate
```

Invalid:

```text
regulations.opa.evaluate
```

Invalid:

```text
regulations.postgres.query
```

Invalid:

```text
regulations.openai.assess
```

Invalid:

```text
regulations.reggenome.lookup
```

Invalid:

```text
regulations.zuribeans.validate
```

The capability must survive replacement of implementation technology.

---

# 11. Domain Capability versus Regulatory Profile

Capability identity SHALL NOT be overloaded with every jurisdiction.

Avoid:

```text
regulations.south-africa.coffee.import.evaluate
```

as the canonical capability architecture.

Prefer:

```text
capability:
regulations.crossborder.evaluate
```

plus context:

```text
origin = UG
destination = ZA
product = ...
effective_at = ...
```

plus regulatory profile:

```text
cross-border-goods
```

The engine should evaluate context, not multiply capability keys indefinitely.

---

# 12. Regulatory Profiles

Profiles SHALL represent regulatory knowledge and evaluation composition rather than provider identity.

Conceptually:

```text
CrossBorderGoodsProfile
      │
      ├── classification
      ├── customs
      ├── tariffs
      ├── origin
      ├── permits
      ├── SPS
      ├── restrictions
      └── documentation
```

Future profiles MAY include:

```text
DataProtectionProfile

ProductSafetyProfile

FinancialServicesProfile

EmploymentProfile

EnvironmentalProfile
```

Profiles SHALL NOT require separate engines.

---

# 13. Control Plane Remains Capability Authority

Baobab Regulations SHALL NOT independently determine:

```text
whether tenant X subscribed
whether capability Y was granted
whether provider Z is bound
which deployment region applies
which isolation profile applies
which Digital Estate is entitled
```

These remain Control Plane concerns.

Regulations SHALL receive validated context and capability resolution.

---

# 14. Regulations Is Not a Second Control Plane

The following architecture is rejected:

```text
Consumer
   │
   ▼
Control Plane
   │
   ▼
Regulations
   │
   ▼
Regulations decides:
 tenant
 subscription
 provider
 routing
 isolation
```

Regulations SHALL trust authorised platform assertions while validating that required regulatory context exists.

It SHALL NOT duplicate platform topology.

---

# 15. Preferred Runtime Invocation

The preferred runtime pattern SHALL be:

```text
1. Consumer authenticates.

2. Consumer resolves canonical Baobab Context.

3. Consumer requests regulations capability resolution.

4. Control Plane verifies:
      entitlement
      scope
      provider
      contract
      health
      topology
      isolation
      residency

5. Control Plane returns authorised resolution.

6. Consumer invokes Regulations.

7. Regulations validates:
      workload identity
      resolution/context assertion
      domain request
      regulatory context

8. Regulations evaluates regulatory state.

9. Regulations persists consequential state.

10. Regulations returns canonical result.

11. Owning engine enforces if authorised.
```

---

# 16. Control Plane SHALL NOT Proxy Every Regulatory Request

The architecture SHALL reject:

```text
Consumer
   │
   ▼
Control Plane
   │
   ▼
Regulations
   │
   ▼
Control Plane
   │
   ▼
Consumer
```

for ordinary domain traffic.

That would make Control Plane:

```text
regulatory API gateway
traffic bottleneck
latency multiplier
failure multiplier
data-plane intermediary
```

The existing Baobab architecture explicitly separates control plane resolution from data-plane execution.

Regulations SHALL follow that model.

---

# 17. Resolution Assertions

Where Baobab adopts signed or otherwise verifiable capability-resolution assertions, Regulations SHOULD consume them.

A resolution assertion MAY convey:

```text
resolution_id
context_id
tenant_id
legal_entity_id
digital_estate_id
capability
contract_version
provider
engine_instance
isolation constraints
residency constraints
expiry
correlation_id
```

Such an assertion SHALL NOT carry provider secrets.

The detailed canonical assertion remains owned by Shared and Control Plane.

---

# 18. Context Immutability

Regulations SHALL treat resolved platform context as immutable for a regulatory evaluation.

A caller SHALL NOT begin with:

```text
context:
tenant A
legal entity B
market ZA
```

and mutate the request mid-evaluation to:

```text
market UG
```

without initiating a new assessment context.

This is essential for replayability.

---

# 19. Regulatory Context Extends Platform Context

Control Plane Context does not contain every fact required for regulatory reasoning.

Regulations therefore SHALL distinguish:

```text
PlatformContext
```

from:

```text
RegulatoryOperationContext
```

Conceptually:

```text
RegulatoryOperationContext
├── resolved_platform_context
├── actor / workload
├── effective_time
├── operation_type
├── product / commodity
├── origin
├── destination
├── transit locations
├── counterparty refs
├── classification
├── value
├── quantity
├── licences
├── documentary evidence
└── domain-specific facts
```

Control Plane remains authoritative for platform identity.

The relevant business engine remains authoritative for business facts.

Regulations evaluates those facts.

---

# 20. Context References over Data Duplication

Where practical, requests SHOULD carry canonical references rather than full duplicated domain objects.

Example:

```text
product_ref
shipment_ref
counterparty_ref
legal_entity_ref
```

Regulations MAY receive an evaluation snapshot necessary for deterministic assessment.

It SHALL NOT permanently create competing product, shipment or counterparty master records.

---

# 21. Snapshot Requirement

A consequential assessment SHALL preserve enough evaluated context to explain the decision later.

Therefore:

```text
reference only
```

may be insufficient for historical replay if the external object changes.

The architecture SHOULD eventually preserve:

```text
canonical reference
+
relevant evaluated snapshot
+
snapshot provenance
```

for consequential assessments.

Detailed snapshot semantics belong in later ADRs.

---

# 22. Workload Identity

Every service-to-service invocation SHALL use authenticated workload identity.

The exact IAM technology is outside this ADR.

The contract SHALL support:

```text
caller workload identity
audience
issuer
expiry
coarse scope
delegated human identity where applicable
```

Long-lived shared API secrets SHOULD NOT be the normal Baobab internal pattern.

---

# 23. User Delegation

Some regulatory assessments occur on behalf of a human user.

The engine SHALL distinguish:

```text
CALLING WORKLOAD
```

from:

```text
DELEGATED USER
```

Example:

```text
ZuriBeans BFF
     │
     │ acts for
     ▼
procurement officer
```

Both identities may matter for audit.

---

# 24. Trust No Arbitrary Tenant Headers

Headers such as:

```text
X-Tenant-ID
X-Legal-Entity-ID
X-Market
X-Country
```

SHALL NOT become authoritative merely because a caller supplied them.

Canonical context must derive from trusted platform mechanisms.

---

# 25. Runtime API Families

Baobab Regulations SHOULD expose distinct logical API families:

```text
Regulatory Query
Regulatory Applicability
Obligation Resolution
Assessment
Decision
History
Change
Impact
Evidence
Administration
Diagnostics
Readiness
```

Runtime and administrative contracts SHALL remain separated.

---

# 26. Query APIs

Query APIs answer informational questions about canonical regulatory state.

Examples:

```text
GET /v1/rules/{id}

GET /v1/instruments/{id}

GET /v1/decisions/{id}

GET /v1/changes/{id}
```

Exact endpoint structure is not normative in this ADR.

The logical separation is normative.

---

# 27. Assessment APIs

Assessment operations SHOULD ordinarily use `POST`.

For example:

```text
POST /v1/assessments
```

because an assessment commonly contains structured contextual input unsuitable for a query string and may create an auditable regulatory artefact.

Conceptually:

```text
RegulatoryAssessmentRequest
├── capability_contract_version
├── context_reference
├── regulatory_operation_context
├── effective_at
├── requested_profile
├── evidence_references
├── correlation_id
├── idempotency_key
└── metadata
```

---

# 28. Assessment Response

Conceptually:

```text
RegulatoryAssessmentResponse
├── assessment_id
├── decision_id
├── status
├── outcome
├── applicable_rules
├── obligations
├── prohibitions
├── requirements
├── missing_evidence
├── uncertainty
├── assurance
├── effective_at
├── rule_set_version
├── explanation_reference
├── evidence_bundle_reference
├── evaluated_at
└── correlation_id
```

The precise schema belongs in Shared.

---

# 29. Synchronous Evaluation

A regulatory evaluation MAY complete synchronously where:

```text
rule set is locally available
context is complete
evaluation is bounded
no expensive external acquisition is required
```

Example:

```text
Trade
  │
  │ "Can shipment proceed?"
  ▼
Regulations
  │
  │ 120 ms
  ▼
ALLOW_WITH_REQUIREMENTS
```

The architecture SHOULD optimise common transactional checks for synchronous operation.

---

# 30. Long-Running Evaluation

Some work is inherently asynchronous.

Examples:

```text
large portfolio impact analysis
cross-jurisdiction historical reconstruction
fresh external evidence acquisition
bulk re-evaluation after regulatory change
mass product classification review
```

Such operations SHALL support a long-running pattern.

Conceptually:

```text
POST
   │
   ▼
202 Accepted
   │
   ├── operation_id
   └── status_reference
```

followed by:

```text
operation.completed
```

or polling through an operation resource.

---

# 31. Synchronous and Asynchronous Semantics Must Match

A result SHALL mean the same thing regardless of whether computation completed:

```text
synchronously
```

or:

```text
asynchronously
```

Transport mechanics SHALL NOT alter regulatory semantics.

---

# 32. Idempotency

Consequential assessment creation SHALL support idempotent retry semantics.

Network retries must not accidentally create:

```text
five independent assessments
```

for a single business decision.

The contract SHOULD support:

```text
idempotency_key
```

and/or a stable request identifier.

HTTP itself defines idempotent methods by whether repeated identical requests have the same intended server effect, and warns against blindly retrying non-idempotent operations. Baobab SHOULD therefore make retry behaviour explicit rather than depend on network assumptions.

---

# 33. Duplicate Requests

Where two requests have the same valid idempotency key and materially identical content, Regulations SHOULD return the prior result or durable operation reference.

Where the same idempotency key is reused with incompatible content:

```text
409 Conflict
```

or an equivalent canonical domain error SHOULD result.

---

# 34. Contract-First HTTP APIs

All externally consumable HTTP APIs SHALL have machine-readable contracts.

`baobab-platform/shared` remains the contract authority.

OpenAPI is the industry standard Baobab SHOULD use for synchronous HTTP API description unless a future platform ADR supersedes it. The current OpenAPI specification family includes versions through 3.2.1.

The exact repository tooling SHALL remain standardised through Shared.

---

# 35. API Contract versus Implementation

The following SHALL be independently versionable:

```text
API contract version
engine software version
rule-set version
regulatory source version
AI model version
```

These SHALL NOT collapse into:

```text
version = 4.2
```

because they represent different change dimensions.

---

# 36. Domain Contract Version

Example:

```text
regulations.assessment.evaluate
contract = 1.0
```

may be served by:

```text
baobab-regulations
software = 3.8.4
```

using:

```text
regulatory_rule_set = 2027.04.18-r3
```

There is no architectural reason these versions must match.

---

# 37. Contract Compatibility

The provider SHALL declare supported canonical contract versions.

Example:

```text
CapabilityProvider:
  regulations.assessment.evaluate

Supports:
  1.x
  2.x
```

Control Plane SHALL participate in provider compatibility resolution according to existing capability architecture.

A consumer SHALL NOT discover contract incompatibility only after sending production business data.

---

# 38. Breaking Changes

A breaking canonical contract change SHALL require a major contract version.

Provider implementation upgrades that preserve semantic compatibility SHALL NOT force Digital Estates to change.

This is one of the principal benefits of the capability model.

---

# 39. Standard Error Contract

Regulations SHALL use the canonical Baobab error model.

For HTTP transport, that error model SHOULD be compatible with RFC 9457 Problem Details unless Shared establishes an equivalent standard.

RFC 9457 defines a machine-readable structure specifically so HTTP APIs need not invent a unique error format for every service.

Regulatory domain errors SHALL add machine-readable reason codes rather than rely on free-text messages.

---

# 40. Regulatory Error Categories

Expected categories include:

```text
INVALID_CONTEXT

INSUFFICIENT_CONTEXT

CAPABILITY_NOT_SUPPORTED

JURISDICTION_NOT_SUPPORTED

PROFILE_NOT_AVAILABLE

REGULATORY_DATA_UNAVAILABLE

REGULATORY_DATA_STALE

RULE_SET_UNAVAILABLE

RULE_CONFLICT

INTERPRETATION_UNRESOLVED

EVIDENCE_REQUIRED

SOURCE_RIGHTS_RESTRICTED

ASSESSMENT_INDETERMINATE

PROVIDER_DEGRADED

DEPENDENCY_UNAVAILABLE
```

These are conceptually distinct from normal infrastructure errors.

---

# 41. Events Are First-Class

Baobab Regulations SHALL publish domain events for important state changes.

Likely examples include:

```text
regulation.source.acquired

regulation.source.failed

regulation.instrument.changed

regulation.rule.created

regulation.rule.verified

regulation.rule.effective

regulation.rule.superseded

regulation.assessment.completed

regulation.decision.issued

regulation.impact.detected

regulation.coverage.degraded
```

Final names and schemas belong in Shared.

---

# 42. Event Contracts

Event-driven contracts SHOULD be described using AsyncAPI where compatible with Baobab Shared tooling.

AsyncAPI explicitly defines machine-readable contracts between senders and receivers in event-driven systems and is protocol-agnostic; version 3.1.0 was released in January 2026.

This supports Baobab's provider-neutral event architecture.

---

# 43. Event Envelope

Baobab event contracts SHALL continue to use the canonical Shared event envelope.

That envelope SHOULD preserve compatibility with widely adopted CloudEvents concepts where useful.

CloudEvents exists specifically to provide a common, vendor-neutral event format for interoperability between independently developed systems and transports.

Regulations SHALL NOT invent a proprietary event envelope merely because its events concern law.

---

# 44. Transport Independence

The domain event SHALL NOT depend semantically upon:

```text
Kafka
NATS
RabbitMQ
Redis Streams
HTTP webhook
cloud event bus
```

The platform may change transport later.

The event remains:

```text
regulation.rule.effective
```

not:

```text
kafka.regulation.rule.effective
```

---

# 45. No Premature Kafka Requirement

This ADR SHALL NOT require Kafka, Redpanda or another distributed log.

Baobab's existing architecture intentionally begins with simpler integration where practical.

Initial event delivery MAY use:

```text
outbox
HTTP/webhook delivery
existing Baobab event infrastructure
```

The domain contract must survive transport evolution.

---

# 46. Transactional Outbox

Where a domain event corresponds to persisted authoritative Regulations state, the event SHALL NOT normally be published before that state is durably committed.

Preferred:

```text
Database Transaction
        │
        ├── persist regulatory state
        └── persist outbox record
                 │
                 ▼
            event publisher
```

Not:

```text
publish event
     │
     X
database commit fails
```

---

# 47. Delivery Semantics

Consumers SHALL assume events MAY be delivered:

```text
more than once
out of instantaneous order across partitions
after temporary delay
```

Regulations SHALL therefore provide stable event identity.

Consumers SHALL be idempotent.

The architecture SHALL NOT pretend that "exactly once" magically exists across independent engines.

---

# 48. Event Causation

Events SHOULD preserve:

```text
event_id
correlation_id
causation_id
tenant/context reference
source engine
occurred_at
schema version
```

This is particularly important for chains such as:

```text
SARS source change
       │
       ▼
rule changed
       │
       ▼
impact detected
       │
       ▼
Trade shipment placed on hold
       │
       ▼
Pulse risk generated
```

---

# 49. Observability

Baobab Regulations SHALL participate in standard platform observability.

At minimum:

```text
distributed traces
structured logs
metrics
health
readiness
domain diagnostics
```

OpenTelemetry provides a standard context mechanism for propagating execution-scoped values across API boundaries and correlating traces, logs and other telemetry.

Baobab SHOULD use platform-standard OpenTelemetry instrumentation unless superseded.

---

# 50. Correlation

Every material regulatory evaluation SHOULD be traceable across:

```text
Digital Estate
BFF
Control Plane
Regulations
Trade
ERP
Pulse
```

through a shared correlation identifier and distributed trace context.

Regulatory decision identifiers are domain identities.

Trace identifiers are operational identities.

They SHALL remain distinct.

---

# 51. Sensitive Observability Data

The following SHOULD NOT be placed casually into trace tags or logs:

```text
full contracts
private legal opinions
customer secrets
supplier banking information
personal data
complete regulatory evidence documents
commercial transaction payloads
```

Observability SHALL favour references and safe metadata.

---

# 52. Internal Engine Architecture

The initial implementation SHOULD be architected as a **modular headless engine**, not a constellation of microservices.

Conceptually:

```text
BAOBAB REGULATIONS
│
├── API / Invocation
│
├── Regulatory Context
│
├── Source Registry
│
├── Source Acquisition
│
├── Regulatory Knowledge
│
├── Interpretation
│
├── Applicability
│
├── Rule Evaluation
│
├── Assessment
│
├── Decision
│
├── Provenance
│
├── Change Detection
│
├── Impact Analysis
│
├── Evidence
│
├── Administration
│
├── Event Outbox
│
└── Observability
```

These are logical modules.

They do not imply separate network services.

---

# 53. Modular Monolith First

The initial preference SHOULD be:

```text
strong module boundaries
+
one primary deployable runtime
+
background workers where necessary
```

rather than:

```text
15 networked microservices
```

The regulatory domain is already complex.

Distribution should not multiply that complexity without a workload justification.

---

# 54. Independent Workers Are Allowed

Some responsibilities naturally require worker processes.

Examples:

```text
source acquisition
document extraction
change detection
bulk impact re-evaluation
event publication
scheduled verification
```

These MAY run as independent processes or containers while remaining part of the same logical Baobab Regulations engine.

---

# 55. Worker Does Not Mean New Domain Owner

Example:

```text
regulations-ingestion-worker
```

remains part of Baobab Regulations.

It does not become:

```text
Baobab Ingestion Engine
```

unless future architecture explicitly establishes such a domain.

---

# 56. Internal Module Boundary — Source Registry

The Source Registry module SHALL ultimately own Regulations' representation of:

```text
source identity
authority
retrieval method
trust classification
licensing
reuse rights
verification policy
refresh expectations
```

Detailed decisions belong in later ADRs.

---

# 57. Internal Module Boundary — Acquisition

Acquisition SHALL fetch or receive external regulatory artefacts.

It SHALL NOT make those artefacts automatically authoritative regulatory rules.

```text
acquired
     ≠
interpreted
     ≠
verified
     ≠
enforceable
```

---

# 58. Internal Module Boundary — Regulatory Knowledge

Regulatory Knowledge SHALL own canonical representations of the domain established in later ADRs.

It SHALL NOT own business transactions.

---

# 59. Internal Module Boundary — Applicability

Applicability SHALL answer:

```text
Given:
rule
+
context
+
time

Does the rule apply?
```

It SHALL NOT determine platform entitlement.

That remains Control Plane.

---

# 60. Internal Module Boundary — Evaluation

The evaluation layer SHALL execute applicable machine-evaluable regulatory semantics.

The specific rule-engine technology is intentionally deferred.

---

# 61. Internal Module Boundary — Assessment

Assessment SHALL combine:

```text
context
applicable rules
evidence
obligations
exceptions
uncertainty
```

into a durable regulatory assessment where required.

---

# 62. Internal Module Boundary — Decision

Decision SHALL derive the canonical regulatory outcome:

```text
ALLOW
ALLOW_WITH_REQUIREMENTS
REVIEW_REQUIRED
BLOCK
INDETERMINATE
NOT_APPLICABLE
```

subject to later ADR refinement.

Decision SHALL remain distinct from enforcement.

---

# 63. Internal Module Boundary — Change

Change detection SHALL identify material differences in:

```text
sources
instruments
provisions
rules
effective dates
interpretations
```

It SHALL not itself decide commercial strategy.

---

# 64. Internal Module Boundary — Impact

Impact Analysis SHALL determine:

> Which Baobab regulatory contexts may be affected by this regulatory change?

It MAY consume canonical references to:

```text
products
trade lanes
jurisdictions
tenants
legal entities
transactions
```

but SHALL NOT take ownership of those objects.

---

# 65. Internal Module Boundary — Evidence

Evidence SHALL maintain the regulatory decision evidence chain.

It SHALL support eventual:

```text
audit
replay
dispute investigation
human review
external assurance
```

without turning Regulations into general-purpose document management.

---

# 66. Internal Module Boundary — Administration

Administrative functions SHALL cover regulatory-domain governance only.

Examples:

```text
verify source
approve interpretation
promote rule assurance
resolve source conflict
retire regulatory profile
approve override authority
```

They SHALL NOT become generic tenant administration.

---

# 67. State Ownership

Baobab Regulations MAY own persistence required for:

```text
regulatory sources
acquired artefacts
canonical instruments
provisions
rules
interpretations
regulatory profiles
verification state
assessments
decisions
regulatory change
impact state
regulatory evidence
event outbox
internal audit
```

It SHALL NOT own canonical Control Plane entities.

---

# 68. Separate Databases by Ownership

Baobab Regulations SHALL own its own persistence.

It SHALL NOT read or write another engine's tables directly.

Rejected:

```text
Regulations
   │
   ├── SELECT FROM trade.shipment
   ├── SELECT FROM erp.invoice
   └── SELECT FROM cp.tenant
```

Preferred:

```text
canonical API
event
authorised snapshot
canonical reference
```

This preserves independent deployability.

---

# 69. Shared Database Is Rejected

The following is explicitly rejected:

```text
one Baobab database
│
├── Trade tables
├── ERP tables
├── Pulse tables
├── Regulations tables
└── Control Plane tables
```

Database convenience SHALL NOT destroy domain ownership.

---

# 70. Search Indexes Are Non-Authoritative

Any:

```text
full-text index
vector index
graph projection
search cache
```

SHALL be treated as derived unless a future ADR explicitly establishes otherwise.

A search index SHALL NOT become the only copy of a regulatory rule.

---

# 71. Vector Stores Are Non-Authoritative

If vector retrieval is used:

```text
embedding
+
vector record
```

is a retrieval aid.

It is not legal authority.

It SHALL remain reconstructable from authoritative domain state.

---

# 72. Rule Engine Is an Implementation Component

The eventual rules evaluator MAY use:

```text
custom deterministic evaluator
OPA
Datalog
DMN
LegalRuleML-derived representation
another rules engine
a combination
```

This ADR selects none.

The canonical regulatory semantics must survive replacement of the evaluator.

---

# 73. AI Orchestrator Is an Implementation Component

Likewise:

```text
Haystack
LangGraph
direct LLM APIs
future agent framework
```

MAY assist the engine.

No AI framework SHALL define the canonical Regulations domain.

---

# 74. Storage Technology Is Deferred

This ADR SHALL NOT decide:

```text
PostgreSQL-only
graph database
document database
object storage topology
vector database
```

The regulatory data model must be decided before storage fashion dictates architecture.

---

# 75. Primary Runtime Store

The engine SHALL require an authoritative transactional persistence mechanism capable of supporting:

```text
versioning
consistency
audit
temporal state
idempotency
outbox semantics
```

The exact technology will be selected separately.

---

# 76. Large Artefacts

Large source artefacts MAY be stored outside the transactional database in approved object storage.

Example:

```text
gazette PDF
legal XML
tariff dataset
source snapshot
```

The domain store SHALL retain:

```text
content identity
hash
provenance
storage reference
rights state
```

---

# 77. API Tier Should Be Stateless Where Practical

The request-serving API tier SHOULD avoid storing session-local regulatory truth in memory.

This improves:

```text
horizontal scaling
failover
deployment
instance replacement
```

Authoritative state belongs in persistent stores.

---

# 78. Evaluation Must Not Depend on Sticky Sessions

A request SHOULD be processable by any eligible engine instance able to access the same authorised regulatory state.

Sticky routing MAY exist for infrastructure reasons.

It SHALL NOT become a regulatory correctness requirement.

---

# 79. Health Is Multi-Dimensional

A process returning HTTP 200 is not sufficient to say:

```text
Baobab Regulations is healthy.
```

The engine SHALL distinguish:

```text
process health
dependency health
source freshness
rule coverage
evaluation readiness
jurisdiction readiness
profile readiness
event publication health
```

---

# 80. Liveness

Liveness answers:

> Is this process alive and able to continue execution?

It SHALL NOT perform expensive external regulatory checks.

---

# 81. Readiness

Readiness answers:

> Can this engine instance currently accept the class of work it declares itself able to perform?

Examples of blockers:

```text
authoritative datastore unavailable
mandatory rule set unavailable
critical migration incomplete
required cryptographic material unavailable
```

---

# 82. Regulatory Readiness

The regulatory domain requires a richer concept than generic infrastructure readiness.

Example:

```text
Process:
HEALTHY

ZA cross-border regulatory profile:
READY

UG cross-border profile:
DEGRADED

Kenya:
NOT_COVERED
```

One global:

```text
healthy = true
```

is insufficient.

---

# 83. Capability-Specific Readiness

Where feasible, Regulations SHOULD report readiness per capability/profile combination.

Example:

```text
regulations.rule.query
    READY

regulations.crossborder.evaluate
    DEGRADED

regulations.impact.evaluate
    READY
```

Control Plane may use this information in provider eligibility.

---

# 84. Freshness Is Not Availability

An engine can be technically available while regulatory content is stale.

Therefore:

```text
ENGINE_UP
```

and:

```text
REGULATORY_STATE_CURRENT
```

are different facts.

The system SHALL expose both where material.

---

# 85. Coverage State

A requested jurisdiction/profile SHOULD be able to return:

```text
SUPPORTED
PARTIAL
NOT_SUPPORTED
TEMPORARILY_DEGRADED
```

rather than silently evaluating an incomplete rule set as if it were complete.

---

# 86. Provider Health Integration

Baobab Regulations SHALL integrate with the Control Plane provider-health model.

Control Plane SHALL NOT need Regulations-specific routing logic.

Regulations exposes provider health.

Control Plane applies generic capability-provider rules.

---

# 87. Deployment Topology

The architecture SHALL support multiple engine instances.

Conceptually:

```text
                    baobab-regulations
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       Africa South                  Africa East
         Instance                      Instance
```

The reason may be:

```text
latency
residency
availability
jurisdiction coverage
customer isolation
scale
```

---

# 88. Multi-Region Is Supported, Not Required Initially

The engine architecture SHALL not prevent regional deployment.

However, initial implementation SHALL NOT require full active-active multi-region infrastructure before business need exists.

Architecture must permit growth without forcing premature cost.

---

# 89. Shared and Dedicated Isolation

The provider model SHALL permit:

```text
shared multi-tenant instance
```

and where commercial or regulatory policy requires:

```text
dedicated tenant instance
```

without changing capability semantics.

---

# 90. Dedicated Deployment Is Not a New Product Semantics

If Customer X requires a dedicated Regulations deployment:

```text
regulations.assessment.evaluate
```

SHALL remain the same capability.

Deployment topology is not business capability identity.

---

# 91. Residency

Regulatory evaluation may include private business context.

EngineInstance selection SHALL therefore honour Control Plane residency and isolation policies.

Regulations SHALL NOT implement an independent competing residency resolver.

---

# 92. Provider Replacement

The architecture SHALL allow a future replacement such as:

```text
Baobab Regulations v1
        ↓
Baobab Regulations v2
```

or potentially:

```text
Baobab Regulations implementation A
        ↓
implementation B
```

without changing Digital Estate capability identity.

---

# 93. Shadow Execution

The platform SHOULD eventually support provider shadowing for high-risk upgrades.

Example:

```text
Production request
      │
      ├────► Provider A
      │       authoritative response
      │
      └────► Provider B
              shadow response
```

Responses can be compared without Provider B affecting the transaction.

This is particularly useful for rule-engine migrations.

---

# 94. Canary Migration

Control Plane's provider lifecycle SHOULD support controlled migration.

Conceptually:

```text
5% contexts → new provider
95% contexts → old provider
```

where regulatory governance permits.

Migration SHALL be explicit and auditable.

---

# 95. Decision Equivalence Testing

Before migration between Regulations implementations, a defined set of regulatory golden cases SHOULD demonstrate acceptable semantic equivalence.

This becomes especially important when changing:

```text
rule engine
ontology
source provider
AI extraction pipeline
```

Detailed golden-case architecture belongs in `ADR-REG-0025`.

---

# 96. Caching

Caching MAY be used.

But regulatory caching is dangerous if context or rule versions are omitted from the cache key.

A decision cache SHOULD conceptually consider:

```text
tenant / scope
regulatory context
effective time
profile
rule-set version
relevant evidence version
contract version
```

where appropriate.

---

# 97. Never Cache "Allow" Indefinitely

The following is explicitly prohibited:

```text
coffee → South Africa
ALLOW
TTL = 30 days
```

without consideration of:

```text
effective date
rule changes
source changes
product state
document state
permit state
```

Regulatory cache invalidation is a domain problem, not only a performance problem.

---

# 98. Change-Driven Invalidation

Where rules change:

```text
rule superseded
```

SHOULD invalidate or mark affected cached assessments according to impact policy.

The engine SHOULD prefer version-addressed caches that naturally prevent stale-rule reuse.

---

# 99. Read Models

Regulations MAY maintain read-optimised projections for:

```text
search
explanation
history
impact
reporting
```

These SHALL remain reconstructable where practical.

A projection SHALL not quietly become the only regulatory truth.

---

# 100. Eventual Consistency

Not every cross-engine state will be instantaneously consistent.

Example:

```text
regulatory change published
        │
        ▼
impact analysis begins
        │
        ▼
1.2 million business objects evaluated
```

Impact state may become available progressively.

The API SHALL represent:

```text
PENDING
RUNNING
PARTIAL
COMPLETE
FAILED
```

rather than pretending instantaneous global consistency.

---

# 101. Transaction Boundary

One Regulations transaction SHALL NOT span another engine's database.

Distributed workflows SHALL rely on:

```text
APIs
events
idempotency
outbox
compensation
reconciliation
```

not distributed SQL transactions.

---

# 102. Consequential Decision Persistence

Where a regulatory decision may:

```text
block shipment
affect financial posting
prevent publication
deny market entry
trigger legal review
```

the engine SHOULD durably persist the assessment before or atomically with publication of its authoritative decision.

---

# 103. Decision Immutability

An issued regulatory decision SHALL NOT normally be overwritten.

If new information produces a different conclusion:

```text
Decision v1
     │
     ▼
superseded by
     │
     ▼
Decision v2
```

The history remains.

---

# 104. Current View versus Historical Record

The engine MAY maintain a convenient:

```text
current decision
```

projection.

But historical decision records SHALL remain independently addressable where audit requirements demand it.

---

# 105. Simulation Mode

The engine SHOULD eventually support explicitly non-authoritative simulation.

Example:

```text
"What would the assessment be
if the destination changed to Kenya?"
```

Simulation SHALL be clearly distinguished from:

```text
transaction-bound regulatory decision
```

It SHALL NOT accidentally enter enforcement workflows.

---

# 106. Preview Rule Sets

A future capability MAY allow assessment against:

```text
proposed regulation
future-effective regulation
draft interpretation
```

This MUST be explicit.

Example:

```text
rule_set_mode = FUTURE_EFFECTIVE
```

A proposed or future rule SHALL never silently contaminate the current enforceable rule set.

---

# 107. Administrative APIs

Administrative APIs SHALL be separately protected.

Examples:

```text
source registration
source trust update
interpretation review
rule verification
regulatory profile publication
coverage lifecycle
override review
```

They SHALL require stronger privileges than runtime evaluation.

---

# 108. Runtime Caller Cannot Promote Rules

A workload authorised to call:

```text
regulations.assessment.evaluate
```

SHALL NOT thereby gain permission to:

```text
verify rule
change source trust
promote interpretation
publish jurisdiction pack
```

Runtime and governance authority are distinct.

---

# 109. No Admin UI Requirement in Core Engine

The existence of administrative workflows SHALL NOT require the core engine to ship a monolithic web application.

A future:

```text
Regulations Governance Console
```

MAY consume the administrative APIs.

The headless engine remains authoritative.

---

# 110. Digital Estate UI Ownership

A Digital Estate owns presentation.

Example ZuriBeans may render:

```text
Regulatory status:
Review required

Missing:
Phytosanitary certificate

Source:
...
```

The regulatory semantics remain owned by Regulations.

UI styling remains owned by ZuriBeans.

---

# 111. External Enterprise Consumption

Baobab Regulations SHALL be capable of eventually serving external systems that are not Baobab Digital Estates.

The pattern SHOULD remain:

```text
External Enterprise
       │
       ▼
Baobab Edge / API Boundary
       │
       ▼
IAM
       │
       ▼
Control Plane
       │
       ▼
Regulations
```

External customers SHALL not be coupled to physical engine instances.

---

# 112. API Gateway Is Not Regulations

An edge gateway MAY provide:

```text
TLS termination
rate limiting
API routing
developer keys
WAF
metering
```

That infrastructure SHALL not own regulatory semantics.

---

# 113. Metering Hooks

The engine SHOULD emit enough usage telemetry to support future commercial metering.

Potential units include:

```text
assessment
impact evaluation
historical reconstruction
evidence bundle
rule query
jurisdiction profile
bulk evaluation
```

Commercial charging logic belongs elsewhere.

Regulations reports usage.

---

# 114. Metering Must Not Affect Decision Correctness

A failed billing-event publication SHALL NOT transform:

```text
BLOCK
```

into:

```text
ALLOW
```

Commercial control and regulatory truth are separate.

---

# 115. Rate Limiting

Rate limits MAY vary by:

```text
product entitlement
capability
tenant
workload
bulk versus transactional use
```

Rate limiting SHALL return explicit operational failure.

It SHALL NOT return a fabricated regulatory result.

---

# 116. Degraded Dependencies

If an optional explanatory LLM is unavailable but deterministic assessment succeeds:

```text
decision:
ALLOW_WITH_REQUIREMENTS

explanation:
DEGRADED
```

may be legitimate.

If the authoritative applicable rule set is unavailable:

```text
decision:
INDETERMINATE
```

may be required.

Dependency failure handling SHALL understand domain criticality.

---

# 117. No Global "AI Down = Regulations Down"

The engine SHALL be designed so deterministic regulatory capabilities remain operational when AI services are unavailable where possible.

AI is subordinate to the regulatory domain.

---

# 118. No Global "Search Down = Regulations Down"

Likewise, a semantic-search outage SHOULD NOT automatically prevent evaluation of locally available verified rules.

Capabilities SHALL degrade independently where architecture permits.

---

# 119. Failure Isolation

The following source failure:

```text
Kenya environmental regulator unavailable
```

SHALL NOT automatically prevent:

```text
ZA customs assessment
```

unless the requested context depends on that source.

---

# 120. Fail-Closed Means No Fabricated Permission

At minimum:

```text
unknown
```

SHALL NOT silently become:

```text
allowed
```

The engine's regulatory output should represent uncertainty honestly.

Actual operational fail-open/fail-closed enforcement remains policy of the consuming engine and later ADRs.

---

# 121. Domain Failure versus Infrastructure Failure

Distinguish:

```text
ASSESSMENT_INDETERMINATE
```

from:

```text
HTTP_SERVICE_UNAVAILABLE
```

One means the regulatory reasoning reached uncertainty.

The other means the engine could not perform the computation.

They are not interchangeable.

---

# 122. Timeout Semantics

A regulatory evaluation timeout SHALL NOT be interpreted as:

```text
no applicable regulation
```

Timeout is operational failure.

The caller may:

```text
retry
route to review
apply authorised hold policy
```

depending upon capability policy.

---

# 123. Security Architecture

The engine SHALL follow platform security standards for:

```text
authentication
authorisation
network policy
secret management
encryption
audit
data classification
residency
tenant isolation
```

This ADR adds regulatory-specific constraints, not a replacement security architecture.

---

# 124. Source Network Isolation

External source acquisition SHOULD be separable from high-trust evaluation workloads.

Conceptually:

```text
Internet
   │
   ▼
Acquisition Boundary
   │
   ▼
Validation / Sanitisation
   │
   ▼
Regulatory Evidence Store
   │
   ▼
Interpretation / Evaluation
```

Untrusted regulatory websites SHALL NOT have direct execution influence over the trusted runtime.

---

# 125. Ingestion Does Not Share Execution Authority

The process that downloads:

```text
government-gazette.pdf
```

SHOULD NOT automatically possess authority to:

```text
promote rule to ENFORCEABLE
```

Separation of duties SHOULD be supported.

---

# 126. Prompt Injection Isolation

If AI processes external regulatory content, embedded instructions are source data, not trusted prompts.

Acquisition and AI pipelines SHALL enforce this boundary.

---

# 127. Secrets

Source credentials, commercial data-provider keys and service credentials SHALL use approved secret-management infrastructure.

They SHALL NOT appear in:

```text
capability resolutions
events
regulatory decisions
logs
source records
```

---

# 128. Data Classification

Regulatory data is not uniformly public.

The engine may hold:

```text
PUBLIC
INTERNAL
TENANT_CONFIDENTIAL
RESTRICTED
```

information.

Classification SHALL propagate appropriately through decisions and evidence bundles.

---

# 129. Audit

Regulations SHALL maintain domain-level audit for changes to:

```text
source configuration
source trust
interpretation
rule verification
profile publication
assessment override
decision supersession
administrative policy
```

Platform security audit and regulatory-domain audit are complementary.

---

# 130. Observability Is Not Regulatory Audit

A log line:

```text
POST /assessments 200
```

does not prove why a transaction was permitted.

Regulatory audit requires domain evidence.

Operational logs are not a substitute.

---

# 131. Performance Principle

Transactional regulatory checks SHOULD be engineered for use inside live business workflows.

The architecture SHALL therefore distinguish:

```text
fast-path evaluation
```

from:

```text
research / acquisition / heavy impact processing
```

A simple verified rule evaluation should not need to crawl the internet.

---

# 132. Fast Path

The fast path SHOULD use:

```text
locally available verified rules
canonical context
cached deterministic supporting state where safe
```

and avoid:

```text
live web searches
unbounded LLM research
long external-source dependency chains
```

---

# 133. Slow Path

The slow path MAY perform:

```text
source acquisition
deep interpretation
portfolio impact analysis
bulk classification
human review
```

and complete asynchronously.

---

# 134. Research and Execution Are Different Workloads

The engine SHALL distinguish:

```text
"What does this new regulation appear to mean?"
```

from:

```text
"May shipment SHP-123 proceed?"
```

The first may tolerate research latency.

The second requires bounded, governed evaluation.

---

# 135. Rule Promotion Protects the Fast Path

The long-term preferred workflow is:

```text
Research
   │
   ▼
Interpret
   │
   ▼
Verify
   │
   ▼
Publish Rule
   │
   ▼
Fast Transaction Evaluation
```

not:

```text
Every transaction
    │
    ▼
LLM reads entire legislation again
```

---

# 136. Scalability Model

Regulations SHOULD scale independently from:

```text
Trade
ERP
Pulse
CMS
Control Plane
```

Heavy regulatory-change processing SHALL not require scaling Trade.

Likewise, Black Friday commerce traffic SHALL not require scaling source ingestion equally.

---

# 137. Workload Classes

The engine SHOULD permit independent capacity planning for:

```text
runtime assessments
source acquisition
AI extraction
change detection
impact analysis
search/query
administrative review
event publication
```

Even when these remain modules of one logical engine.

---

# 138. Background Backpressure

Bulk work SHALL not starve transactional evaluation.

For example:

```text
re-evaluate 5 million historical objects
```

must not consume every worker needed for live transaction checks.

Queue and worker design SHALL support workload isolation.

---

# 139. Availability Classes

Future commercial products MAY offer different availability or response-time objectives.

The canonical regulatory semantics SHALL remain the same.

Enterprise SLA is commercial configuration, not a different regulatory model.

---

# 140. Provider Availability

Control Plane MAY bind different tenants to different provider instances based upon:

```text
availability tier
isolation
residency
region
commercial entitlement
```

This is precisely why capability/provider separation exists.

---

# 141. Pulse Integration

Pulse SHALL consume regulatory state through stable APIs/events.

Preferred:

```text
Regulations
    │
    │ regulation.impact.detected
    ▼
Pulse
```

Pulse SHALL NOT poll Regulations' database.

---

# 142. Pulse Does Not Need Regulations Internals

Pulse should not know whether Regulations uses:

```text
OPA
Datalog
PostgreSQL
Neo4j
OpenAI
RegGenome
```

It consumes:

```text
regulatory change
regulatory impact
regulatory decision
regulatory evidence reference
```

---

# 143. Trade Integration

Trade SHALL consume:

```text
assessment
decision
obligations
missing evidence
```

through canonical contracts.

Trade SHALL retain ownership of:

```text
order
shipment
hold
release
commercial state
```

---

# 144. ERP Integration

ERP SHALL consume regulatory facts and decisions relevant to its domain.

ERP retains accounting authority.

Regulations SHALL never directly post entries.

---

# 145. CMS Integration

CMS MAY request regulatory publication constraints.

CMS retains content and publication workflow authority.

---

# 146. IAM Integration

IAM authenticates and establishes identity security.

Regulations SHALL not replace IAM's general authorisation model.

---

# 147. Digital Estate Integration

Digital Estates SHALL consume regulatory capability through their BFF/API boundary rather than embed legal interpretation.

This supports:

```text
one regulatory truth
many experiences
```

---

# 148. Contract Generation

Where practical, Shared SHOULD generate:

```text
TypeScript types
Go types
Python models
Java models
validation fixtures
SDK clients
```

from canonical schema artefacts.

Hand-reimplementing the same request contract in every repository SHOULD be avoided.

---

# 149. Contract Tests

Baobab Regulations SHALL participate in contract compatibility tests.

CI SHOULD verify:

```text
provider contract matches Shared
events validate against canonical schemas
breaking changes are detected
registered capability versions remain accurate
```

---

# 150. Consumer-Driven Tests

Critical consumers such as Trade SHOULD maintain integration scenarios demonstrating that Regulations' current supported contract behaves as expected.

Contract tests do not replace domain correctness tests.

---

# 151. Golden Regulatory Tests

Domain regression SHALL ultimately include verified regulatory scenarios.

Example:

```text
UG → ZA green coffee
effective date = X

Expected:
rules A/B/C apply
documents D/E required
outcome = ALLOW_WITH_REQUIREMENTS
```

These tests belong in the wider ADR programme but are fundamental to safe provider evolution.

---

# 152. Sandbox Capability

A sandbox or non-production regulatory capability SHOULD exist for:

```text
developer integration
customer testing
simulation
contract validation
```

Sandbox results SHALL be unmistakably distinguished from production regulatory decisions.

---

# 153. Sandbox Rule Sets

Sandbox MAY use:

```text
synthetic data
reduced coverage
test rules
future rules
```

provided the result identifies its environment and authority clearly.

---

# 154. Development Environment

`baobab-regulations` SHOULD integrate with the standard Baobab development environment and DevContainer/Codespaces approach.

Its development tooling SHALL not require every other engine to be embedded in the same runtime container.

Provider integration can use:

```text
Compose
test doubles
contract fixtures
local service instances
```

---

# 155. Polyrepo Discipline

The Regulations repository SHALL own:

```text
implementation
domain internals
migrations
internal tests
runtime packaging
engine-specific docs
engine-specific ADRs
```

Shared SHALL own:

```text
cross-engine contracts
canonical events
capability definitions
portable schemas
```

Control Plane SHALL own:

```text
provider registration state
bindings
grants
resolutions
topology
```

---

# 156. No Copy-Pasted Shared Schemas

The engine SHALL depend on versioned canonical contracts rather than copying them into its repository and independently editing them.

Generated artefacts MAY be vendored only through governed tooling and version metadata.

---

# 157. Provider Registration Lifecycle

A new Regulations provider/version SHOULD follow:

```text
Implement contract
      │
      ▼
Validate capability compatibility
      │
      ▼
Register provider support
      │
      ▼
Register EngineInstance
      │
      ▼
Health/readiness validation
      │
      ▼
Create governed binding
      │
      ▼
Resolve in non-production
      │
      ▼
Promote
```

---

# 158. Engine Startup Does Not Grant Capability

Starting a Regulations container SHALL NOT mean:

```text
all tenants may use it
```

Capability entitlement still requires:

```text
grant
scope
binding
provider eligibility
```

---

# 159. Subscription Does Not Equal Provider

A customer subscribing to a regulatory product SHALL NOT imply:

```text
use physical instance X
```

Subscription creates commercial intent and eventually grants.

Control Plane resolves the actual provider.

---

# 160. Product Packaging Is Separate

Future products might include:

```text
Baobab Regulatory Essentials

Baobab Cross-Border Assurance

Baobab Regulatory Impact

Baobab Enterprise Regulatory Execution
```

These products compose capabilities.

They do not define engine architecture.

---

# 161. Commercial Portability

Because product identity, capability identity and provider identity remain separate, Baobab can:

```text
change implementation
change regulatory data vendor
introduce dedicated deployment
introduce new rule engine
```

without renegotiating every customer's API semantics.

That is an architectural asset.

---

# 162. OpenAPI / AsyncAPI Posture

Baobab SHOULD maintain:

```text
OpenAPI
    for synchronous HTTP contracts

AsyncAPI
    for event-driven contracts

JSON Schema
    for reusable canonical payload definitions
```

where compatible with Shared.

OpenAPI's current specification line extends through 3.2.1, while AsyncAPI 3.1.0 provides protocol-independent event API description.

Specification patch versions MAY evolve without an ADR where semantic compatibility is preserved.

---

# 163. CloudEvents Compatibility

Shared MAY retain its own canonical event semantics, but SHOULD preserve compatibility with the useful CloudEvents model of:

```text
id
source
type
specversion
time
subject
data
```

where practical.

CloudEvents was specifically designed to reduce proprietary event-description differences across platforms and transports.

---

# 164. OpenTelemetry Posture

Instrumentation SHOULD use the Baobab standard OpenTelemetry implementation.

OpenTelemetry's Context model is explicitly designed to propagate execution-scoped information between associated units and API boundaries, which aligns with Baobab's cross-engine correlation requirements.

Regulatory domain context SHALL NOT be indiscriminately placed in telemetry baggage.

---

# 165. Architecture Shall Remain Protocol-Evolvable

Initial runtime communication will likely favour HTTP/JSON.

This ADR SHALL NOT permanently prohibit:

```text
gRPC
message-based invocation
batch interfaces
streaming
```

where future scale requires them.

The canonical capability contract remains the stable abstraction.

---

# 166. Technology Decisions Explicitly Deferred

This ADR intentionally does not select:

```text
Python
Go
Java
TypeScript

FastAPI
Django
Spring
another framework

PostgreSQL
graph database
document database

OPA
Drools
Datalog
DMN engine

Haystack
LangGraph
another AI orchestrator

Qdrant
pgvector
another vector engine

Kafka
NATS
Redis Streams

OpenAI
Anthropic
open-source LLM
```

These choices must follow domain needs.

---

# 167. Why Runtime Language Is Deferred

The strategic contract is:

```text
regulations.assessment.evaluate
```

not:

```text
python.assessment.evaluate
```

Runtime language selection deserves a separate implementation decision informed by:

```text
rule-engine ecosystem
legal-language processing
performance
team capability
AI ecosystem
operability
long-term maintenance
```

---

# 168. Why Graph Technology Is Deferred

A regulatory model is highly connected.

That does not automatically mean:

```text
graph domain
=
graph database
```

A relational database can represent graphs.

A graph database may later prove useful.

The canonical domain model must be settled first.

---

# 169. Why OPA Is Deferred

OPA is a mature general-purpose policy engine and demonstrates useful PDP/PEP separation.

But Baobab Regulations requires additional legal semantics:

```text
authority
jurisdiction
temporal validity
legal hierarchy
source provenance
interpretation
uncertainty
obligation
exemption
```

OPA MAY become an evaluator.

It SHALL NOT automatically become the regulatory domain model.

---

# 170. Why AI Platform Choice Is Deferred

The Regulations moat SHALL not depend upon one LLM vendor.

Any AI layer must sit behind Baobab-owned domain interfaces.

---

# 171. Rejected Architecture — Regulations as Trade Module

Rejected:

```text
baobab-trade/
   modules/
      regulations/
```

Reason:

Regulatory capability must serve:

```text
Trade
ERP
CMS
IAM
Pulse
external enterprises
```

Trade is the first consumer, not the owner.

---

# 172. Rejected Architecture — Regulations Inside Pulse

Rejected:

```text
Pulse
  └── regulatory execution
```

Pulse and Regulations carry materially different authority semantics.

Intelligence may be probabilistic.

Regulatory enforcement needs explicit source, temporal and assurance semantics.

---

# 173. Rejected Architecture — Regulations as Control Plane Module

Rejected:

```text
Control Plane
   └── regulatory rules
```

Control Plane resolves platform context and capability.

It must not become a universal business-domain engine.

---

# 174. Rejected Architecture — Regulations as API Gateway

Rejected:

```text
Every business call
      │
      ▼
Regulations
      │
      ▼
Owning engine
```

Only regulatory operations should invoke Regulations.

It is not service-mesh middleware.

---

# 175. Rejected Architecture — Regulations as Shared Library

Rejected:

```text
shared/regulatory-engine
```

A shared library cannot independently provide:

```text
central rule lifecycle
temporal reconstruction
source governance
change detection
cross-engine impact
provider replacement
central audit
```

Regulations requires an independent engine.

---

# 176. Rejected Architecture — Regulations as Vendor Wrapper

Rejected:

```text
Baobab Regulations
        =
Vendor X API proxy
```

A vendor may supply content or services.

Baobab owns canonical context, semantics and execution contracts.

---

# 177. Rejected Architecture — Regulations as LLM Endpoint

Rejected:

```text
POST /ask-lawyer-ai
```

as the core engine architecture.

Natural-language interfaces may exist later.

The authoritative architecture is structured regulatory computation.

---

# 178. Rejected Architecture — Direct Database Integration

Rejected:

```text
Trade DB ───────┐
ERP DB ─────────┼── Regulations
CP DB ──────────┘
```

This destroys independent ownership and makes deployment changes dangerous.

---

# 179. Rejected Architecture — Browser Direct to Physical Instance

Rejected:

```text
Browser
  │
  ▼
https://regulations-prod-za-01.internal...
```

Digital Estates consume logical Baobab capability, not physical topology.

---

# 180. Consequences — Positive

This decision provides:

```text
independent deployability
provider replacement
clean domain ownership
multi-consumer reuse
contract stability
commercial productisation
regional deployment
dedicated isolation
cross-engine interoperability
controlled migration
testable regulatory semantics
```

It prevents ZuriBeans implementation details from becoming platform architecture.

---

# 181. Consequences — Positive for Commercial Strategy

The same capability can serve:

```text
ZuriBeans
Thamani
future Nabhold businesses
external Baobab customers
partner software
customer ERP systems
customer trade systems
```

without building a different regulatory engine for each.

That is essential if Regulations is to become a profitable Baobab differentiator.

---

# 182. Consequences — Positive for Trust

Because:

```text
capability contract
provider
engine instance
rule set
assessment
decision
```

remain distinguishable, a customer can understand:

```text
what was requested
which engine evaluated it
which version performed it
which rules were used
what decision resulted
```

This improves auditability.

---

# 183. Consequences — Negative

The architecture introduces additional discipline:

```text
provider registration
contract governance
context resolution
version compatibility
workload identity
event contracts
distributed tracing
separate domain persistence
```

A quick monolithic application would initially be simpler.

That simplicity would not survive platform growth.

---

# 184. Consequences — Operational Complexity

Independent deployment means the platform must manage:

```text
health
service discovery
credentials
networking
versioning
migrations
observability
provider readiness
```

These are accepted costs of making Regulations a reusable platform engine.

---

# 185. Consequences — Consistency

Cross-engine operations become distributed.

Baobab must accept:

```text
eventual consistency
idempotency
reconciliation
outbox patterns
```

rather than rely on one ACID transaction across the platform.

This is consistent with the existing engine architecture.

---

# 186. Architectural Invariants

The following are normative.

| ID | Invariant |
|---|---|
| `REG-E-I01` | Baobab Regulations is an independent headless engine |
| `REG-E-I02` | Digital Estates consume regulatory capabilities, not physical engine instances |
| `REG-E-I03` | Shared owns canonical cross-engine contracts |
| `REG-E-I04` | Control Plane owns entitlement and provider resolution |
| `REG-E-I05` | Regulations owns regulatory domain behaviour |
| `REG-E-I06` | Operational engines own enforcement actions |
| `REG-E-I07` | Regulations does not read/write other engine databases |
| `REG-E-I08` | Provider identity is separate from capability identity |
| `REG-E-I09` | Engine identity is separate from EngineInstance identity |
| `REG-E-I10` | Regulatory profiles do not become engine identities |
| `REG-E-I11` | Runtime and administrative APIs remain distinct |
| `REG-E-I12` | Consequential assessment creation supports safe retry/idempotency |
| `REG-E-I13` | Events are contract-first and transport-neutral |
| `REG-E-I14` | Search/vector indexes are not canonical regulatory truth |
| `REG-E-I15` | AI infrastructure is replaceable |
| `REG-E-I16` | Rule-engine infrastructure is replaceable |
| `REG-E-I17` | Regulatory readiness is richer than process liveness |
| `REG-E-I18` | Unsupported or stale regulatory state cannot silently produce permission |
| `REG-E-I19` | Deployment topology shall not alter capability semantics |
| `REG-E-I20` | Every consequential cross-engine invocation must be correlatable |
| `REG-E-I21` | Contract version and software version remain separate |
| `REG-E-I22` | External regulatory providers enter through anti-corruption adapters |
| `REG-E-I23` | Control Plane does not proxy ordinary Regulations business traffic |
| `REG-E-I24` | Browser-supplied tenant/context identifiers are not inherently trusted |
| `REG-E-I25` | Headless architecture remains valid even if all UI implementations are replaced |

---

# 187. Target Runtime Topology

The initial production model SHOULD conceptually resemble:

```text
                            Internet
                               │
                          Digital Estate
                               │
                              BFF
                               │
                   ┌───────────┴───────────┐
                   │                       │
                   ▼                       ▼
             Baobab IAM              Baobab CP
                                           │
                                   capability resolution
                                           │
                                           ▼
                               Baobab Regulations
                              ┌─────────────┼─────────────┐
                              │             │             │
                              ▼             ▼             ▼
                           Runtime       Workers       Persistence
                              │             │             │
                        assessments      ingest        rules
                        queries          impact        evidence
                        decisions        events        decisions
```

No specific container count is mandated here.

---

# 188. Target Cross-Engine Flow

```text
                     ZuriBeans
                         │
                         ▼
                    Estate BFF
                         │
                 resolve capability
                         │
                         ▼
                  CONTROL PLANE
                         │
        regulations.crossborder.evaluate
                         │
                         ▼
               BAOBAB REGULATIONS
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
       rule set       context       evidence
           │             │             │
           └─────────────┼─────────────┘
                         │
                         ▼
                    Assessment
                         │
                         ▼
                      Decision
                         │
                         ▼
                  BAOBAB TRADE
                         │
                         ▼
                Hold / Proceed /
                  Require Evidence
```

---

# 189. Target Regulations–Pulse Flow

```text
                REGULATORY SOURCE
                       │
                       ▼
               Baobab Regulations
                       │
             rule/change verified
                       │
                       ▼
         regulation.impact.detected
                       │
                       ▼
                  Baobab Pulse
                       │
                       ▼
             strategic analysis
```

Pulse does not need privileged database access.

---

# 190. Target Direct Enterprise Flow

Future external consumption MAY follow:

```text
Customer System
      │
      ▼
Baobab API Edge
      │
      ▼
IAM
      │
      ▼
Control Plane
      │
      ▼
Baobab Regulations
      │
      ▼
Regulatory Decision
```

Thus Baobab Regulations can become independently monetisable without abandoning platform architecture.

---

# 191. Implementation Phases

The architecture SHOULD be proven incrementally.

```text
PHASE REG-E0
Contracts and provider registration

PHASE REG-E1
Headless runtime skeleton

PHASE REG-E2
Context validation

PHASE REG-E3
Source / rule persistence

PHASE REG-E4
Deterministic assessment endpoint

PHASE REG-E5
Decision + evidence persistence

PHASE REG-E6
Trade integration

PHASE REG-E7
Events and Pulse integration

PHASE REG-E8
Change impact

PHASE REG-E9
Multi-instance / production hardening

PHASE REG-E10
External enterprise consumption
```

---

# 192. Minimum Architecture Proof

Before claiming the engine architecture proven, Baobab SHOULD demonstrate:

```text
1.
Register a canonical regulatory capability in Shared.

2.
Register Baobab Regulations as an approved provider.

3.
Register at least one EngineInstance in Control Plane.

4.
Grant the capability to a test tenant.

5.
Resolve it through CP.

6.
Invoke Regulations using authenticated workload identity.

7.
Evaluate a contextual regulatory assessment.

8.
Persist the resulting assessment and decision.

9.
Return a canonical contract.

10.
Publish a canonical event.

11.
Allow Trade to consume the decision.

12.
Allow Pulse to consume a regulatory-change event.

13.
Replace the engine instance without changing the consumer contract.
```

If this cannot be accomplished without vendor-specific knowledge leaking into Digital Estates, the architecture is not complete.

---

# 193. Production Readiness Gates

Before production enforcement, the engine SHALL demonstrate:

```text
contract validation
tenant isolation
workload authentication
provider registration
capability resolution
idempotency
source provenance
rule-set versioning
decision persistence
event outbox
audit
observability
health/readiness
dependency degradation
backup/restore
migration safety
security testing
regulatory golden tests
```

Specific operational SLOs belong in later technical specifications.

---

# 194. Follow-On Decisions

This ADR enables the next decisions in the sequence.

Most immediately:

```text
ADR-REG-0003
Regulatory Authority versus
Baobab Interpretation Boundary
```

will formalise the authority chain that the headless engine must carry through its APIs.

Then:

```text
ADR-REG-0004
Advisory, Review and Enforcement Decision Classes
```

will determine which output classes may influence operations.

And:

```text
ADR-REG-0005
Provider-Neutral Regulatory Intelligence Architecture
```

will define how government, commercial and partner regulatory sources enter this engine without any provider becoming Baobab's ontology.

---

# 195. Research and Standards Foundation

This architecture deliberately uses established open standards at its interfaces rather than inventing unnecessary Baobab protocols.

The OpenAPI Specification provides a machine-readable contract for HTTP APIs and currently publishes specifications through version 3.2.1.

AsyncAPI provides protocol-independent machine-readable contracts for event-driven APIs; its current 3.1.0 release reinforces the use of sender/receiver contracts independently of the underlying broker.

CloudEvents addresses interoperability by defining common event metadata independently of producer, consumer and transport. Its design explicitly targets loosely coupled services that may be developed and deployed independently.

RFC 9457 provides a standard structure for machine-readable HTTP API problem details and avoids every service creating a unique error format.

OpenTelemetry provides standard cross-process context propagation and correlation across traces, logs and metrics, which is particularly important when a regulatory decision moves through Control Plane, Regulations, Trade and Pulse.

These standards influence the boundary.

They do not define the regulatory domain.

---

# 196. Final Decision

Baobab Regulations SHALL be built as:

> **A contract-first, independently deployable, headless Baobab capability provider that receives trusted canonical context, evaluates regulatory state, persists explainable regulatory assessments and decisions, and exposes those results through stable APIs and events without owning platform routing or downstream operational enforcement.**

The canonical architecture is:

```text
              BAOBAB SHARED
             Canonical Contracts
                    │
                    ▼
            BAOBAB CONTROL PLANE
         Entitlement / Resolution
                    │
                    ▼
            BAOBAB REGULATIONS
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
    Sources        Rules      Context
       │            │            │
       └────────────┼────────────┘
                    │
                    ▼
              Applicability
                    │
                    ▼
                Assessment
                    │
                    ▼
                 Decision
                    │
             APIs / Events
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
     Trade         ERP         Pulse
       │            │            │
       ▼            ▼            ▼
   enforce       enforce       analyse
```

The engine SHALL remain:

```text
headless
provider-neutral
multi-tenant
context-aware
temporally aware
independently deployable
replaceable behind capability contracts
observable
auditable
event-enabled
```

It SHALL NOT become:

```text
a special Control Plane subsystem

a Trade module

a Pulse submodule

a universal API gateway

a shared library

a regulatory vendor proxy

a browser application

a database integration layer

a general-purpose policy engine

an LLM endpoint masquerading as regulatory infrastructure
```

The deepest architectural consequence is this:

```text
Digital Estate
     does not know Regulations topology.

Trade
     does not know Regulations implementation.

Pulse
     does not know Regulations storage.

Control Plane
     does not know Regulations legal semantics.

Regulations
     does not know how Trade enforces its decision.
```

They know only the contracts they are authorised to know.

That separation is what allows Baobab Regulations to become both **deeply embedded** and **replaceable internally**.

And that is exactly where a durable platform advantage lies:

> **Regulatory capability becomes part of Baobab's platform fabric without turning Baobab into one inseparable monolith.**

---

## Decision Summary

```text
ADR-REG-0002
──────────────────────────────────────────────

DECISION

Baobab Regulations is an independent,
headless Baobab capability provider.

Shared:
    defines canonical contracts.

Control Plane:
    resolves entitlement, context and provider.

IAM:
    authenticates callers and workloads.

Regulations:
    evaluates regulatory meaning.

Operational engines:
    enforce authorised decisions.

Pulse:
    interprets regulatory changes commercially.

Digital Estates:
    present regulatory capability.

PRIMARY INTERFACES

    HTTP APIs
    Canonical events
    Long-running operations where necessary

ARCHITECTURAL STYLE

    contract-first
    capability-centric
    provider-neutral
    modular
    event-enabled
    independently deployable

DO NOT COUPLE TO

    rule engine
    LLM vendor
    database
    graph technology
    regulatory content vendor
    event transport
    deployment topology

FIRST PROOF

    ZuriBeans
    Uganda → South Africa
    Coffee / Vanilla
        ↓
    capability resolution
        ↓
    Regulations assessment
        ↓
    Trade enforcement
        ↓
    Pulse impact consumption
```
# ADR-REG-0024 — Regulatory Events, Subscriptions and Notifications

**Subtitle:** Canonical Event Contracts, Durable Publication, Subscription Filtering, Delivery Guarantees, Webhook Security, Replay and Human Notification

**Status:** Proposed — Foundational Event-Driven Integration Architecture  
**Decision ID:** `ADR-REG-0024`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Cross-Repository Contract Target:** `baobab-platform/shared`  
**Date:** 2026-09-29  
**Amended:** 2026-10-06 — RTD-06/RTD-08 under ADR-SHARED-022/024; canonical cross-engine naming, Regulations ↔ Trade Docs exchange, `regulations` namespace, event-context stewardship and producer activation reconciled  
**Cross-Engine Authority:** ADR-SHARED-019, ADR-SHARED-021, ADR-SHARED-022, ADR-SHARED-024  
**Decision Type:** Events / Messaging / Subscriptions / Notifications / Integration / Delivery / Replay  
**Strategic Classification:** Core Platform Integration Infrastructure

---

# RTD-06 Normative Amendment — Regulations ↔ Trade Docs Exchange

This amendment is normative for cross-engine documentary integration.

ADR-SHARED-022 now governs the executable Regulations ↔ Trade Docs wire boundary.

The local event architecture in this ADR remains valid for Regulations-owned publication mechanics, but the following cross-engine rules now apply.

## A. Canonical event naming

Earlier examples in this ADR used:

~~~text
io.baobab.regulations.*
~~~

Those examples are superseded for platform wire contracts.

Canonical Shared naming is:

~~~text
com.baobab-platform.<context>.<fact>.vN
~~~

under ADR-SHARED-008 and ADR-SHARED-018.

For RTD-06 the canonical Regulations facts are:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

The Trade Docs fact relevant to Regulations is:

~~~text
com.baobab-platform.documents.regulatory-evidence.offered.v1
~~~

## B. RTD-08 activation state

ADR-SHARED-024 / RTD-08 now activates the Shared `regulations` event context
with `baobab-regulations` as steward/producer for:

~~~text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
~~~

Their canonical AsyncAPI publication surface is:

~~~text
baobab-platform/shared/contracts/regulatory-document-assessment/v1/asyncapi.yaml
~~~

This activation is narrow. The wider illustrative event taxonomy in this ADR
remains non-canonical until each event has an explicit Shared payload contract
and registration.

## C. Assessment is a command, not an event

The canonical assessment request is:

~~~text
POST /v1/documentary-evidence/assessments
~~~

It SHALL NOT be disguised as:

~~~text
PleaseAssessDocumentEvidence event
~~~

The eventual:

~~~text
requirement-satisfaction.evaluated
~~~

event records the committed Regulations fact after assessment.

## D. Requirements are Regulations-owned

Regulations publishes/serves pinned:

~~~text
DocumentRequirement
PermitRequirement
EvidenceRequirement
RegulatoryDecision
~~~

through RTD-05 references and RTD-06 projections.

Trade Docs SHALL NOT reinterpret or mutate those requirements.

## E. Documentary facts are Trade Docs-owned

Trade Docs supplies:

~~~text
DocumentVersion reference
document type/family
issuer claim
verification snapshot
temporal-validity snapshot
subject references
documentary assertions
content-artifact references
~~~

Regulations consumes those facts and decides legal sufficiency.

## F. Verification is not satisfaction

~~~text
Trade Docs:
VERIFIED + CURRENTLY_VALID

does not imply

Regulations:
SATISFIED
~~~

Wrong consignment, commodity, issuer, jurisdiction, regime or required data can still make evidence insufficient.

## G. Assertion provenance must survive

Documentary values SHALL retain whether they were:

~~~text
ISSUER_ASSERTED
BAOBAB_EXTRACTED
BAOBAB_GENERATED
EXTERNAL_NORMALIZED
~~~

An extracted/OCR value does not silently become an issuer assertion.

## H. Legal time is owner-controlled

Trade Docs does not supply legal_time or knowledge_time in the evidence-assessment command.

Those remain Regulations-owned and are derived from the pinned requirement/decision context.

## I. Local v0 events remain local draft

The repository-local:

~~~text
regulations.evaluation.requested.v0
regulations.evaluation.completed.v0
~~~

remain draft audit schemas.

They SHALL NOT be promoted as canonical cross-engine contracts merely by copying them into Shared.

## J. Existing document events are triggers, not decisions

Once Trade Docs events are activated, Regulations may consume:

~~~text
document-version.verification-changed.v2
document-version.validity-changed.v2
~~~

to detect material evidence changes.

Regulations still decides whether reassessment is required and what legal result follows.

## K. Historical replay

Consequential documentary assessment SHALL preserve exact pinned requirement, decision and DocumentVersion references.

A missing historical version SHALL NOT be replaced by the current version.

## L. Tenant/context consistency

All tenant-scoped references in RTD-06 operations SHALL match the tenant obtained from trusted Control Plane context.

Reference possession does not grant access.


# 1. Executive Decision

Baobab Regulations SHALL expose material regulatory state transitions through a provider-neutral event architecture based upon:

```text
Canonical Regulations State
          │
          ▼
     Domain Transaction
          │
     ┌────┴─────┐
     ▼          ▼
 State Change   Transactional Outbox
                    │
                    ▼
                Event Relay
                    │
                    ▼
          Canonical CloudEvent
                    │
              ┌─────┼─────┐
              ▼     ▼     ▼
            Trade  Pulse  CMS
              │
              ▼
          Other Consumers
```

The architecture SHALL provide:

```text
canonical event contracts

durable publication

subscriptions

tenant-aware filtering

idempotent consumption

bounded ordering

replay

webhooks

human notifications

delivery monitoring

dead-letter handling

traceability.
```

However:

> **Events SHALL describe canonical state transitions; they SHALL NOT become an alternative source of regulatory truth.**

---

# 2. Governing Principles

The primary rules are:

```text
CANONICAL STATE
≠
EVENT

EVENT
≠
COMMAND

EVENT
≠
NOTIFICATION

SUBSCRIPTION
≠
AUTHORIZATION

DELIVERY
≠
PROCESSING

DELIVERY ACKNOWLEDGEMENT
≠
BUSINESS EFFECT

EVENT REPLAY
≠
REGULATORY DECISION REPLAY

BROKER ORDER
≠
LEGAL CHRONOLOGY.
```

---

# 3. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0018 — Regulatory Decision and Evaluation Engine`
- `ADR-REG-0019 — Policy Decision Point and Enforcement Point Separation`
- `ADR-REG-0020 — Decision Explainability, Replay and Reproducibility`
- `ADR-REG-0023 — Regulatory Change Detection and Impact Analysis`

It SHALL also conform to canonical contracts maintained through `baobab-platform/shared`.

---

# 4. Research Finding — CloudEvents Is Appropriate for the Envelope

CloudEvents defines a vendor-neutral event format and requires the core attributes:

```text
id
source
specversion
type.
```

Its specification also defines optional attributes such as:

```text
subject
time
dataschema
datacontenttype.
```

Importantly, CloudEvents specifies that the combination of `source + id` uniquely identifies a distinct event and may therefore be used by consumers to identify duplicate deliveries.

Baobab SHALL adopt CloudEvents **1.0 envelope semantics**.

---

# 5. CloudEvents Specification Version

Baobab SHALL initially emit:

```text
specversion = "1.0"
```

even though ongoing CloudEvents specification work may subsequently publish patch revisions.

Application event schema versioning remains a separate concern.

---

# 6. Research Finding — AsyncAPI Fits Baobab's Contract Model

AsyncAPI 3.0 is protocol-neutral and explicitly separates:

```text
channels

messages

operations.
```

This allows Baobab to document one logical event contract while binding it later to technologies such as:

```text
Kafka

AMQP

MQTT

HTTP

WebSocket

other brokers/transports.
```

without embedding infrastructure topology into canonical domain contracts.

Baobab SHALL use **AsyncAPI 3.x-compatible descriptions** for asynchronous cross-repository contracts.

---

# 7. CloudEvents Subscription Specification

The CloudEvents project is developing a Subscription API, but the currently surfaced specification is explicitly marked:

```text
Version 0.1-wip.
```


Therefore:

> **Baobab SHALL NOT make its canonical subscription domain dependent upon the current CloudEvents Subscription API.**

Baobab MAY map to that specification later if it matures appropriately.

---

# 8. Event Transport Is Provider-Neutral

This ADR SHALL NOT mandate:

```text
Kafka

NATS

RabbitMQ

AWS EventBridge

Google Pub/Sub

Azure Event Grid

Pulsar.
```

The canonical architecture is:

```text
Regulations
   │
   ▼
Baobab Event Contract
   │
   ▼
Transport Adapter
   │
   ▼
Selected Infrastructure.
```

---

# 9. Broker Choice Is Deployment Architecture

It SHALL NOT change:

```text
event meaning

event identity

tenant semantics

subscription semantics

schema versioning.
```

---

# 10. Canonical Truth

The source of regulatory truth remains:

```text
Baobab Regulations
+
PostgreSQL canonical state.
```

---

# 11. Events Are Immutable Projections

An event states:

> **A particular domain occurrence happened.**

It does not own the current regulatory state.

---

# 12. Example

Canonical state:

```text
RuleVersion R17
status = PUBLISHED.
```

Event:

```text
regulation.rule.published.
```

If the event broker disappears, RuleVersion R17 remains published.

---

# 13. Conversely

If an event exists saying:

```text
Rule R17 published
```

but canonical state does not contain valid R17:

```text
event cannot manufacture R17.
```

This is an integrity incident.

---

# 14. Event versus Command

A domain event SHALL describe something that has happened.

Good:

```text
RegulatoryChangeVerified

ReassessmentRequired

RegulatoryDecisionIssued

RequirementChanged.
```

A command expresses requested intent.

Examples:

```text
ReassessRegulatorySubject

PublishRegulatoryRule

AcknowledgeNotification.
```

---

# 15. Commands SHALL Not Be Disguised as Events

Rejected:

```text
event:
PleaseReassessShipment.
```

---

# 16. Message Infrastructure May Carry Both

AsyncAPI can describe event-driven commands and events.

Their semantic distinction SHALL remain explicit.

---

# 17. Event versus Notification

Event:

```text
RegulatoryDecisionChanged.
```

Notification:

```text
Email compliance officer:
"Shipment S now requires Permit P."
```

---

# 18. Notification Is a Projection

Notification presentation does not become canonical regulatory state.

---

# 19. Human Notification Failure

If email delivery fails:

```text
RegulatoryDecision
```

remains valid.

---

# 20. Event Naming

> **RTD-06 amendment:** canonical platform wire names use ADR-SHARED-018's
> `com.baobab-platform.<context>.<fact>.vN` convention. The older
> `io.baobab.regulations.*` examples are superseded.

Examples of the canonical form include:

```text
com.baobab-platform.regulations.change.verified.v1

com.baobab-platform.regulations.reassessment.required.v1

com.baobab-platform.regulations.decision.issued.v1

com.baobab-platform.regulations.requirement.changed.v1
```

RTD-06 defines and ADR-SHARED-024 / RTD-08 now activates:

```text
com.baobab-platform.regulations.document-requirements.determined.v1

com.baobab-platform.regulations.requirement-satisfaction.evaluated.v1
```

Both are ACTIVE in Shared with `baobab-regulations` as producer.

Other examples in this section remain illustrative until canonical Shared
schemas and registrations are approved.

---

# 21. Event Type Version

A new major event type version SHALL be introduced where:

```text
semantic meaning changes incompatibly

required fields change incompatibly

field meaning changes.
```

---

# 22. Additive Evolution

Compatible optional additions SHOULD preserve the current event major version.

---

# 23. `dataschema`

Every canonical production event SHOULD identify its payload schema using:

```text
dataschema.
```

Example conceptually:

```text
urn:baobab:schema:regulations:
change-verified:v1
```

Exact URI scheme belongs in `shared`.

---

# 24. Critical CloudEvents Terminology Distinction

CloudEvents:

```text
source
```

means:

> event producer/context.

It SHALL NOT mean:

```text
legal source of regulation.
```

---

# 25. Example

Correct:

```text
source =
/engines/baobab-regulations
```

Payload:

```text
regulatorySourceRefs = [...]
```

---

# 26. Never Overload `source`

This prevents confusion between:

```text
event provenance
```

and:

```text
legal provenance.
```

---

# 27. Canonical Event Envelope

Conceptually:

```text
CloudEvent
├── specversion
├── id
├── source
├── type
├── subject?
├── time
├── datacontenttype
├── dataschema
│
├── tenantref?
├── contextref?
├── correlationid?
├── causationid?
├── aggregateid?
├── aggregateversion?
├── classification?
├── legalvalidfrom?
├── knowledgeat?
│
└── data
```

---

# 28. Required CloudEvents Attributes

At minimum:

```text
specversion

id

source

type.
```

This follows CloudEvents core.

---

# 29. Baobab SHOULD Also Require `time`

For canonical Regulations events:

```text
time
```

SHOULD normally identify when the domain occurrence occurred.

---

# 30. Event Time Is Not Legal Time

Hard invariant:

```text
event.time
≠
regulatory legal_valid_from.
```

---

# 31. Example

```text
change verified:
29 September

law effective:
1 October.
```

Event:

```text
time = 29 September
legalvalidfrom = 1 October.
```

---

# 32. `subject`

CloudEvents `subject` SHOULD identify the primary canonical entity/resource affected where practical.

Example:

```text
subject =
regulatory-change/chg_123
```

---

# 33. `id`

Event ID SHALL be generated before durable publication.

Retries SHALL retain the same event ID.

---

# 34. Stable Retry Identity

If publishing fails:

```text
Event E123
```

is retried.

Do NOT generate:

```text
E124
E125
E126
```

for each delivery attempt.

---

# 35. Delivery Attempt Has Separate Identity

Conceptually:

```text
Event
  E123

DeliveryAttempt
  DA1
  DA2
  DA3.
```

---

# 36. Duplicate Handling

Consumers SHALL treat identical:

```text
source + id
```

as the same event.

This aligns directly with CloudEvents duplicate semantics.

---

# 37. Event IDs Are Not Aggregate IDs

```text
event.id
≠
decision_id

change_id

rule_id

transaction_id.
```

---

# 38. Causality

Baobab SHALL preserve domain causality separately from event identity.

---

# 39. `correlationid`

Groups related activity.

Example:

```text
regulatory change
→ reassessment campaign
→ 30 decisions.
```

All MAY share:

```text
correlationid.
```

---

# 40. `causationid`

Identifies the immediately preceding causal event/command where meaningful.

Example:

```text
ChangeVerified event
        ↓
ReassessmentRequired event

causationid =
ChangeVerified.event_id.
```

---

# 41. Correlation Is Not Causation

Hard invariant.

---

# 42. Distributed Tracing

Baobab SHOULD propagate W3C Trace Context where event transport supports it.

W3C Trace Context standardises `traceparent` and `tracestate` propagation across distributed systems so otherwise independent tracing implementations can correlate requests into one distributed trace.

---

# 43. Trace ID Is Not Business Correlation ID

```text
trace_id
≠
correlationid.
```

Trace IDs may be short-lived operational data.

Business causality may need years of retention.

---

# 44. Aggregate Identity

Events associated with versioned domain aggregates SHOULD expose:

```text
aggregateid

aggregateversion.
```

---

# 45. Example

```text
aggregateid =
decision/D123

aggregateversion =
4.
```

---

# 46. Ordering

Baobab SHALL NOT promise:

```text
global event ordering.
```

---

# 47. Why

A distributed platform spanning:

```text
regions

repositories

brokers

retries
```

cannot safely rely upon one universal total order.

---

# 48. Aggregate Ordering

Where order matters, producers SHALL provide monotonic:

```text
aggregateversion
```

or equivalent sequence within the domain aggregate.

---

# 49. Example

Consumer receives:

```text
Rule R version event:
aggregateversion = 8
```

before:

```text
aggregateversion = 7.
```

Consumer can detect out-of-order delivery.

---

# 50. Missing Sequence

Consumer may:

```text
wait

retry

fetch canonical state

request replay.
```

It SHALL NOT invent missing state.

---

# 51. Event Ordering Is Not Legal Chronology

A later-delivered event might describe:

```text
retroactive law.
```

Legal ordering uses ADR-REG-0015 temporal semantics.

---

# 52. Transactional Publication

Baobab Regulations SHALL use the:

# **Transactional Outbox Pattern**

for canonical state changes that must emit events.

---

# 53. Required Atomicity

Conceptually:

```text
BEGIN TRANSACTION

UPDATE canonical regulatory state

INSERT event into outbox

COMMIT
```

Either both commit:

```text
state + publication intent
```

or neither commits.

---

# 54. Rejected Architecture

```text
commit database

then publish event

hope network works.
```

This can lose events.

---

# 55. Also Rejected

```text
publish event

then commit database.
```

This can publish events for transactions that later roll back.

---

# 56. Outbox Record

Conceptually:

```text
RegulatoryOutboxRecord
├── event_id
├── event_type
├── aggregate_ref
├── aggregate_version
├── tenant_ref?
├── payload
├── schema_ref
├── created_at
├── publish_status
├── attempt_count
└── published_at?
```

---

# 57. Event Relay

A separate relay/worker SHALL publish committed outbox records.

---

# 58. Relay Retries

Publishing SHALL be retryable.

Retry SHALL preserve:

```text
event identity.
```

---

# 59. Relay Failure

Canonical transaction remains committed.

Outbox remains:

```text
PENDING / RETRYING.
```

---

# 60. Publication Lag Is Observable

Metrics SHALL track:

```text
transaction commit
→ event publish
```

latency.

---

# 61. Event Archive

Baobab SHOULD retain a durable archive of published canonical events according to policy.

---

# 62. Archive Is Not Source of Truth

It enables:

```text
audit

delivery replay

forensics.
```

Canonical state remains PostgreSQL domain state.

---

# 63. Not Full Event Sourcing

This ADR does NOT require rebuilding the entire Regulations domain solely from events.

---

# 64. Consumer Idempotency

Because transport delivery is inherently retryable:

> **Consumers SHALL be idempotent.**

---

# 65. Delivery Semantics

The default guarantee SHALL be:

# **At-least-once delivery**

for durable integrations.

---

# 66. No Generic Exactly-Once Claim

Baobab SHALL NOT claim:

```text
exactly-once transport delivery.
```

---

# 67. Exactly-Once Effect

Where important, a consumer MAY achieve an effectively once-applied business transition through:

```text
deduplication

idempotency

transactional inbox

domain constraints.
```

---

# 68. Consumer Inbox

Each durable consumer SHOULD maintain:

```text
ConsumedEvent
├── source
├── event_id
├── received_at
├── processed_at?
├── processing_status
└── result_ref?
```

---

# 69. Unique Constraint

Consumer storage SHOULD enforce uniqueness on:

```text
source + event_id.
```

---

# 70. Consumer Transaction

Where possible:

```text
BEGIN

record event as consumed

apply business mutation

COMMIT
```

should occur atomically in the consumer's own database.

---

# 71. No Shared Consumer Database

Each Baobab engine remains owner of its persistence.

---

# 72. `shared` May Provide Helpers

`baobab-platform/shared` MAY define reusable:

```text
event schemas

inbox interfaces

idempotency helpers

test fixtures.
```

It SHALL not become a shared runtime database.

---

# 73. Event Schema Ownership

The producing bounded context owns semantic meaning.

For Regulations events:

```text
baobab-regulations
```

owns event semantics.

---

# 74. Cross-Repository Contract Location

Stable shared schemas and AsyncAPI descriptions SHOULD be published through:

```text
baobab-platform/shared.
```

---

# 75. `shared` Does Not Own Meaning

It distributes contracts.

---

# 76. AsyncAPI Contract

Each canonical event SHOULD document:

```text
event/message

payload schema

publisher

expected consumers where known

channel/address abstraction

correlation ID

security requirements

examples

compatibility notes.
```

AsyncAPI 3.0 explicitly supports message schemas and correlation IDs independently of channel and operation topology.

---

# 77. Schema Compatibility

Event consumers SHALL:

```text
ignore unknown optional fields

validate required known fields

reject incompatible major versions.
```

---

# 78. Breaking Change

Breaking event semantics require:

```text
new major event type/schema.
```

---

# 79. Dual Publishing

During migration Baobab MAY publish:

```text
v1
+
v2
```

temporarily.

---

# 80. Dual-Publish Window Must Be Governed

Consumers SHALL migrate before v1 retirement.

---

# 81. Event Retirement

Event schema status SHOULD include:

```text
ACTIVE

DEPRECATED

RETIRED.
```

---

# 82. Thin Events

Cross-domain Regulations events SHOULD generally be:

```text
thin events.
```

---

# 83. Thin Event Means

Payload contains:

```text
canonical references

material changed fields

reason codes

bounded summaries.
```

It does not duplicate full regulatory aggregates.

---

# 84. Example

Good:

```text
changeId

changeType

jurisdictionRefs

affectedRuleRefs

legalValidFrom

impactStatus.
```

---

# 85. Avoid Full Source Text

Do not routinely emit:

```text
entire Gazette

entire statute

private legal opinion

raw evidence.
```

---

# 86. Why

Thin events reduce:

```text
privacy exposure

rights exposure

schema coupling

payload size

stale duplicated state.
```

---

# 87. Consumer Needs Rich State

Consumer may call the canonical Regulations API subject to authorization.

---

# 88. Event Payload Is a Snapshot

Even thin event fields describe the event occurrence.

They SHALL not be assumed to remain current forever.

---

# 89. Data Classification

Each event SHOULD carry or derive:

```text
classification.
```

Possible classes:

```text
PUBLIC

PLATFORM_INTERNAL

TENANT_PRIVATE

RESTRICTED

PRIVILEGED.
```

---

# 90. Classification Affects Routing

A broker subscription SHALL never override data classification.

---

# 91. Tenant Isolation

Tenant-private events SHALL be delivered only to authorised consumers within the relevant tenant scope.

---

# 92. Subscription Is Not Authorization

A subscription saying:

```text
eventTypes = "*"
```

does not grant:

```text
access to every tenant.
```

---

# 93. Authorization Intersection

Effective delivery scope SHALL be:

```text
requested subscription scope
∩
subscriber authorization
∩
data classification
∩
tenant isolation.
```

---

# 94. Authorization Must Be Revalidated

Subscriber authorization SHOULD be checked:

```text
at creation

and where necessary at delivery/runtime.
```

---

# 95. Why

A subscriber's access can later be:

```text
revoked

reduced

expired.
```

---

# 96. Revoked Consumer

It SHALL stop receiving newly protected events.

---

# 97. Previously Delivered Data

Revocation does not magically erase information already delivered.

Retention/privacy policy applies.

---

# 98. Subscription Domain

Baobab Regulations SHALL implement a provider-neutral:

# `RegulatorySubscription`

for Regulations-specific events.

---

# 99. RegulatorySubscription

Conceptually:

```text
RegulatorySubscription
├── subscription_id
├── subscriber_ref
├── tenant_scope
├── event_types[]
├── filter
├── delivery_profile
├── accepted_schema_versions[]
├── replay_policy?
├── status
├── created_at
├── valid_from?
├── valid_until?
└── provenance
```

---

# 100. Subscriber Types

Potential:

```text
BAOBAB_ENGINE

TENANT_APPLICATION

EXTERNAL_INTEGRATION

INTERNAL_SERVICE.
```

Human users SHALL normally use notification preferences rather than raw system subscriptions.

---

# 101. Subscription Filters

Initial regulatory filters SHOULD support:

```text
event type

jurisdiction

regulatory profile

change type

RuleVersion / rule family

regulatory domain

product / commodity

HS classification

market

trade lane

legal entity

transaction

decision outcome

effect class

urgency

source authority.
```

---

# 102. Filtering Is Typed

Rejected:

```text
arbitrary SQL WHERE clause.
```

---

# 103. Why

Typed filtering enables:

```text
authorization analysis

indexing

contract stability

security validation.
```

---

# 104. SubscriptionFilter

Conceptually:

```text
RegulatorySubscriptionFilter
├── jurisdictions[]
├── profiles[]
├── change_types[]
├── rule_refs[]
├── domains[]
├── product_refs[]
├── classification_patterns[]
├── market_refs[]
├── trade_lane_refs[]
├── legal_entity_refs[]
├── transaction_refs[]
├── outcomes[]
├── effect_classes[]
└── urgencies[]
```

---

# 105. Subscription Filter Does Not Evaluate Law

It determines:

```text
which events interest subscriber.
```

It does not determine regulatory applicability.

---

# 106. Example

Subscription:

```text
jurisdiction = ZA
product = coffee
```

means:

> Send matching change events.

It does NOT mean:

> All South African coffee laws apply to this tenant.

---

# 107. Subscription Lifecycle

Potential:

```text
PENDING

ACTIVE

PAUSED

DEGRADED

SUSPENDED

EXPIRED

REVOKED

DELETED.
```

---

# 108. Subscription Validation

Before activation verify:

```text
subscriber exists

subscriber authorised

delivery destination valid

filters valid

schema version supported

security configuration valid.
```

---

# 109. Delivery Profiles

Potential:

```text
INTERNAL_BROKER

WEBHOOK

PULL_FEED

INTERNAL_CALLBACK.
```

Exact transports remain provider-neutral.

---

# 110. External Webhooks

Webhook delivery SHALL use:

```text
HTTPS.
```

---

# 111. HTTPS Alone Is Not Sufficient

For consequential external integrations Baobab SHOULD additionally support cryptographic message authentication.

---

# 112. HTTP Message Signatures

RFC 9421 defines HTTP Message Signatures, including:

```text
keyid

created

expires

nonce
```

and allows applications to require particular covered components and replay protections.

Baobab SHOULD use RFC 9421-compatible signatures or an equivalently strong controlled mechanism for external webhook signing.

---

# 113. Signed Components

A webhook security profile SHOULD cover material components such as:

```text
HTTP method

target URI

content type

Content-Digest

event identity

signature metadata.
```

Exact profile SHALL be versioned.

---

# 114. Content Integrity

RFC 9530 defines the `Content-Digest` field for HTTP message content integrity and explicitly notes it can be combined with HTTP Message Signatures.

Baobab SHOULD include and sign a `Content-Digest` for consequential webhook deliveries.

---

# 115. TLS Still Required

RFC 9421 explicitly notes message signatures do not provide confidentiality and do not replace TLS.

---

# 116. Replay Attack Protection

Webhook verification SHOULD use:

```text
signature created time

maximum signature age

expiration

nonce where applicable

event deduplication.
```

RFC 9421 specifically discusses timestamps, expiry and nonces as replay mitigations.

---

# 117. Webhook Key Rotation

Support:

```text
keyid

multiple simultaneously valid verification keys

graceful rotation

revocation.
```

---

# 118. Secrets Do Not Belong in Subscription Payload

Credentials SHALL reside in:

```text
secret-management infrastructure.
```

---

# 119. Endpoint Security

Webhook registration SHALL protect against:

```text
SSRF

loopback targeting

cloud metadata endpoints

private-address abuse

DNS rebinding

unapproved schemes.
```

---

# 120. External Endpoint

Only approved:

```text
https://
```

destinations SHALL be permitted by default.

---

# 121. Internal Endpoints

Private-network delivery may be permitted through separately governed internal profiles.

---

# 122. Delivery Response

A webhook SHOULD treat appropriate HTTP:

```text
2xx
```

as successful transport acknowledgement.

---

# 123. Transport ACK Means Only

> **The endpoint accepted delivery at the HTTP layer.**

It does not prove that subscriber business logic completed correctly.

---

# 124. Retryable Failures

Examples:

```text
network timeout

5xx

429

temporary connection failure.
```

---

# 125. Retry-After

HTTP defines `Retry-After`, including use with `503`, while HTTP 429 can indicate rate limiting and may also carry `Retry-After`.

Baobab webhook delivery SHOULD respect valid bounded `Retry-After` values.

---

# 126. Retry Strategy

Default:

```text
exponential backoff

jitter

upper bound

maximum attempt window.
```

---

# 127. No Retry Storm

A failed subscriber SHALL not overload itself or the platform.

---

# 128. DeliveryAttempt

Conceptually:

```text
DeliveryAttempt
├── delivery_attempt_id
├── subscription_ref
├── event_ref
├── attempt_number
├── started_at
├── completed_at?
├── result
├── http_status?
├── retry_after?
├── next_attempt_at?
└── failure_reason?
```

---

# 129. Delivery Failure Does Not Delete Event

After retry exhaustion:

```text
delivery = PARKED / DEAD_LETTERED
```

not:

```text
event deleted.
```

---

# 130. Dead-Letter State

The platform SHALL preserve:

```text
event

subscriber

failure reason

delivery attempts.
```

---

# 131. Dead Letter Is Not Garbage

Operators can:

```text
inspect

repair destination

replay delivery.
```

---

# 132. Subscription Suspension

Repeated failures MAY automatically transition:

```text
ACTIVE
→
DEGRADED
→
SUSPENDED.
```

---

# 133. High-Consequence Subscriber Failure

If failure prevents material regulatory workflow:

```text
operational alert
```

SHOULD be raised.

---

# 134. But Regulations Decision Remains Valid

Event subscriber availability does not redefine law.

---

# 135. Event Replay

Baobab SHALL distinguish:

```text
DELIVERY RETRY

DELIVERY REPLAY

EVENT REPROJECTION

DECISION REPLAY.
```

---

# 136. Delivery Retry

Same event:

```text
same source

same id
```

sent again because earlier delivery failed.

---

# 137. Delivery Replay

Historical event is intentionally resent to a subscriber.

It SHOULD retain original event identity where exact event redelivery is intended.

---

# 138. New Delivery Attempt

Replay delivery gets a new:

```text
DeliveryAttempt ID
```

not a new event ID.

---

# 139. Event Reprojection

If Baobab deliberately creates a new event representation from current canonical state:

```text
new event.
```

---

# 140. Reprojection Must Reference Origin

Potential:

```text
replayof

derivedfrom
```

or payload provenance relation.

---

# 141. Reprojection Is Not Historical Event Replay

Important.

---

# 142. Decision Replay

ADR-REG-0020:

```text
re-runs regulatory decision semantics.
```

That is completely separate from event redelivery.

---

# 143. Replay Authorization

Historical event replay SHALL reapply current authorization.

---

# 144. Old Permission Is Not Current Permission

A subscriber once authorised to see an event does not necessarily remain authorised years later.

---

# 145. Replay Range

Subscriptions MAY request replay by:

```text
timestamp

cursor

event range

change set

aggregate.
```

subject to retention and authorization.

---

# 146. Replay Limits

Large replay requests SHOULD be:

```text
asynchronous

rate-limited

observable.
```

---

# 147. Retention

Event retention depends on:

```text
event type

effect class

tenant requirements

regulatory audit needs

privacy

contractual requirements.
```

---

# 148. Event Retention ≠ Canonical Retention

Canonical decisions/rules may require longer retention than delivery events or vice versa.

---

# 149. Event Taxonomy — Source and Change

Initial event family SHOULD include:

```text
source.change-detected

source.monitoring-degraded

change.candidate-created

change.verified

change.rejected

change.future-effective

change.became-effective

change.superseded.
```

---

# 150. Event Taxonomy — Impact

```text
impact.analysis-started

impact.candidate-identified

impact.confirmed

impact.not-material

reassessment.required

reassessment.campaign-started

reassessment.campaign-completed.
```

---

# 151. Event Taxonomy — Regulatory Knowledge

```text
rule.published

rule.superseded

rule.suspended

rule.revalidation-required

jurisdiction-pack.degraded

jurisdiction-pack.ready.
```

---

# 152. Event Taxonomy — Decisions

```text
decision.issued

decision.superseded

decision.stale

decision.restatement-issued

decision.outcome-changed.
```

---

# 153. Event Taxonomy — Requirements

```text
requirement.created

requirement.changed

requirement.satisfied

requirement.unsatisfied

requirement.expiring

requirement.violated.
```

---

# 154. Event Taxonomy — Runtime

```text
runtime.package-published

runtime.package-activated

runtime.stale

runtime.reconciled

runtime.revoked.
```

---

# 155. Internal Workflow Events

Not every internal state transition must become a cross-platform event.

---

# 156. Avoid Event Noise

Examples that may remain internal:

```text
parser page 17 completed

vector embedding batch 43 finished

LangGraph node entered.
```

---

# 157. Publish Domain-Relevant Facts

Cross-boundary events SHOULD represent facts meaningful outside the implementation.

---

# 158. Reassessment Required Event

Example payload:

```text
changeRef

subjectRef

reasonCodes

affectedRuleRefs

reassessmentMode

urgency

legalValidFrom.
```

---

# 159. It Is a State Fact

Meaning:

> Regulations has established that this subject requires reassessment.

---

# 160. Actual Reassessment Command

Consumer or orchestration may issue:

```text
ReassessRegulatorySubject.
```

---

# 161. Decision Issued Event

Payload SHOULD be intentionally bounded.

Potential:

```text
decisionRef

subjectRef

question

outcome

effectClass

recommendedDisposition

reasonCodes

rulesetRef

decidedAt.
```

---

# 162. Decision Event Should Not Contain Full Evidence

Consumers needing evidence access it through authorised APIs.

---

# 163. Requirement Changed

Useful for Trade/ERP/customer portals.

Potential:

```text
requirementRef

subjectRef

previousStatus

currentStatus

dueAt

reasonCode.
```

---

# 164. Change Verified Event

Potential:

```text
changeRef

changeType

jurisdictionRefs

affectedInstrumentRefs

legalValidFrom

verificationState

urgency.
```

---

# 165. Shared Public Change Event

May be:

```text
PLATFORM_INTERNAL
```

or public-facing where appropriate.

---

# 166. Tenant Impact Event

Contains:

```text
tenantref
```

and must remain tenant-scoped.

---

# 167. Public Change and Private Impact Are Different Events

Preferred:

```text
Regulation changed
```

shared event,

followed by:

```text
Tenant T has 7 impacted transactions
```

private event.

---

# 168. This Reduces Data Leakage

A shared legal update need not reveal:

```text
which customers trade that product.
```

---

# 169. Subscription Examples

### Trade

```text
event types:
reassessment.required
decision.outcome-changed
requirement.changed

filters:
tenant = own tenant
domain = cross-border trade.
```

---

# 170. Pulse

```text
event types:
change.verified
change.future-effective
impact.confirmed

filters:
jurisdictions = subscribed markets.
```

---

# 171. CMS

```text
event types:
change.verified
rule.published
rule.superseded

purpose:
content staleness / update candidate.
```

---

# 172. ERP

```text
event types:
requirement.changed
change.verified

filters:
tax
filing
reporting
financial obligations.
```

---

# 173. Digital Estate

Should usually consume through backend/BFF integration rather than directly subscribing browser clients to privileged regulatory events.

---

# 174. Browser Event Security

Do not expose internal event streams directly to arbitrary frontends.

---

# 175. Human Notifications

Baobab SHALL model notification separately from system event subscription.

---

# 176. NotificationPreference

Conceptually:

```text
NotificationPreference
├── principal_ref
├── tenant_ref
├── regulatory_interests
├── channels[]
├── urgency_threshold
├── digest_policy
├── quiet_hours?
├── language?
└── status
```

---

# 177. Notifications Are Derived from Events

```text
Canonical Event
       │
       ▼
NotificationPolicy
       │
       ▼
Recipient Resolution
       │
       ▼
Notification
       │
       ▼
Channel Adapter.
```

---

# 178. Notification Channels

Potential:

```text
IN_APP

EMAIL

PUSH

SMS

CHAT / collaboration provider.
```

Actual providers remain adapters.

---

# 179. Notification Provider Is Replaceable

Canonical Regulations state SHALL NOT depend upon:

```text
SendGrid

Twilio

specific push provider

specific chat platform.
```

---

# 180. NotificationPolicy

Determines:

```text
who

what

when

urgency

channel

digest/escalation.
```

---

# 181. Event Urgency and Notification Urgency Are Related but Distinct

A regulatory event may be critical but certain recipients may receive:

```text
immediate alert.
```

Others may receive:

```text
daily digest.
```

---

# 182. Immediate Notifications

Appropriate for:

```text
new prohibition

E3/E4 decision change

imminent permit requirement

runtime stale during consequential enforcement.
```

---

# 183. Digest Notifications

Appropriate for:

```text
routine guidance changes

low-impact regulatory updates

weekly market summaries.
```

---

# 184. Notification Aggregation

Avoid sending:

```text
47 emails
```

for one regulatory ChangeSet affecting 47 rules.

---

# 185. Digest Grouping

Possible by:

```text
RegulatoryChangeSet

jurisdiction

profile

transaction group

time window.
```

---

# 186. Alert Fatigue Is a Governance Risk

Notifications SHOULD prioritise:

```text
material

actionable

time-sensitive
```

information.

---

# 187. Notification ≠ Audit Evidence

Canonical decision/change records remain audit evidence.

---

# 188. Notification Read Status

May track:

```text
DELIVERED

READ

ACKNOWLEDGED.
```

---

# 189. Acknowledgement Does Not Change Regulatory Truth

It records human workflow state.

---

# 190. Critical Acknowledgement

For certain events:

```text
acknowledgement_required = true
```

MAY trigger escalation if overdue.

---

# 191. Escalation

Example:

```text
critical prohibition change
        ↓
compliance officer notified
        ↓
not acknowledged
        ↓
escalate to designated alternate.
```

---

# 192. Escalation Policy Is Operational

It does not change regulatory effect.

---

# 193. Notification Templates

CMS MAY own or assist with reusable content templates where appropriate.

---

# 194. But Notification Facts Come from Regulations

CMS SHALL NOT invent:

```text
new requirements

new outcomes

new effective dates.
```

---

# 195. Notification Localisation

Canonical:

```text
reason codes

dates

rule references
```

remain stable.

Presentation may vary by language.

---

# 196. Event Security Model

Every publisher and subscriber SHALL authenticate through platform-authorised service identity mechanisms.

---

# 197. Producer Identity

The event's CloudEvents `source` identifies logical producer context.

It does not replace service authentication.

---

# 198. Broker ACL

Transport adapters SHALL enforce:

```text
publish permissions

consume permissions

tenant isolation
```

where supported.

---

# 199. Topic Names Are Not Security Boundaries by Themselves

Authorization remains explicit.

---

# 200. Sensitive Event Filtering

For tenant-private data:

> **Filtering SHALL occur before unauthorised delivery.**

Rejected:

```text
broadcast everything
and trust consumer to discard it.
```

---

# 201. Payload Minimisation

Events SHALL contain the minimum data required for the integration purpose.

---

# 202. Personal Information

Where event data contains personal information:

```text
POPIA/privacy policy

retention

data residency
```

must apply.

---

# 203. Legal Privilege

Privileged legal interpretations SHALL not enter broad event channels.

---

# 204. Rights

Content-rights restrictions from ADR-REG-0012 also apply.

---

# 205. Event Does Not Launder Licensed Content

If source text may not be redistributed:

```text
putting it into an event payload
```

does not make redistribution lawful.

---

# 206. Event Encryption

Transport SHALL be encrypted in transit.

At-rest encryption follows platform security architecture.

---

# 207. Webhook Delivery Logs

SHALL NOT indiscriminately log complete sensitive payloads.

Prefer:

```text
event ID

subscription ID

status

latency

payload hash.
```

---

# 208. Delivery Observability

Track:

```text
events created

outbox backlog

publication lag

broker publish failures

consumer lag

webhook attempts

webhook failures

dead-letter count

subscription health

replay backlog.
```

---

# 209. Event SLOs

Potential SLO dimensions:

```text
publication latency

delivery latency

durability

subscription availability

replay completion time.
```

---

# 210. Event SLO ≠ Regulatory Freshness SLO

A fast event about stale legal knowledge is still stale knowledge.

---

# 211. Distributed Trace

Events SHOULD carry sufficient trace linkage to correlate:

```text
source change
→ verification
→ impact
→ reassessment
→ decision
→ enforcement.
```

---

# 212. Causality Chain Example

```text
E1 change.verified
    │
    ▼
E2 impact.confirmed
    │
    ▼
E3 reassessment.required
    │
    ▼
D44 decision issued
    │
    ▼
E4 decision.issued
    │
    ▼
Trade enforcement.
```

---

# 213. Correlation Does Not Require Same Trace

The chain may span:

```text
hours

days

human review.
```

Therefore persistent causation IDs are required beyond ordinary distributed tracing.

---

# 214. Event Processing Errors

Consumer-side failures SHOULD distinguish:

```text
TRANSIENT

PERMANENT_SCHEMA

AUTHORIZATION

DOMAIN_CONFLICT

DUPLICATE

STALE_EVENT.
```

---

# 215. Stale Event

Example:

Consumer currently knows:

```text
aggregateversion = 12
```

then receives:

```text
aggregateversion = 10.
```

It may safely recognise the event as older.

---

# 216. But Older Events May Still Have Audit Value

Do not necessarily discard from archive.

---

# 217. Consumer Recovery

If consumer falls far behind:

```text
canonical snapshot
+
event cursor
```

MAY be preferable to replaying millions of stale events.

---

# 218. Snapshot Bootstrap

Potential pattern:

```text
1. Fetch authorised current snapshot.

2. Record snapshot sequence/watermark.

3. Begin event consumption after watermark.
```

---

# 219. Eventual Consistency

Cross-engine projections are inherently eventually consistent.

---

# 220. Consequential Enforcement

Where synchronous regulatory correctness is required:

```text
Trade SHALL request current Regulations decision
```

rather than rely solely upon eventually delivered events.

---

# 221. Critical Boundary

Events are excellent for:

```text
change propagation

workflow triggers

cache invalidation

reassessment notification.
```

They SHALL NOT replace synchronous decision evaluation where a transaction requires immediate authoritative confirmation.

---

# 222. Example

Shipment clearance request:

Wrong:

```text
Trade checks whether it remembers
a prohibition event.
```

Correct:

```text
Trade obtains current RegulatoryDecision.
```

---

# 223. Event Can Invalidate Cached Decision

Example:

```text
change.verified
```

causes Trade to mark cached decision:

```text
potentially stale
```

and request reassessment.

---

# 224. Pulse Integration

Pulse SHOULD consume:

```text
change.verified

change.future-effective

impact.confirmed

requirement.changed.
```

---

# 225. Pulse May Emit Intelligence

Example:

```text
HighCommercialImpactSignal.
```

This remains Pulse intelligence.

---

# 226. No Event Authority Loop

Pulse's event SHALL not be consumed by Regulations as verified legal change without normal source/change verification.

---

# 227. CMS Integration

CMS SHOULD consume:

```text
rule.published

rule.superseded

change.verified.
```

---

# 228. CMS Response

Potential:

```text
mark Article A
REGULATORY_REVIEW_REQUIRED.
```

---

# 229. Trade Integration

Trade SHOULD consume:

```text
reassessment.required

decision.outcome-changed

requirement.changed.
```

---

# 230. ERP Integration

ERP SHOULD consume selected:

```text
tax

reporting

filing

financial regulatory events.
```

---

# 231. Control Plane Integration

Control Plane MAY consume Regulations readiness/capability events where required.

But it SHALL not consume events to reconstruct legal truth.

---

# 232. Runtime Events

`ADR-REG-0019` execution package state MAY emit:

```text
package.published

package.activated

runtime.stale

runtime.reconciled.
```

---

# 233. Runtime Stale Event

Can trigger:

```text
operator alert

effect-class reduction

decision reassessment.
```

---

# 234. Event Storm Control

Large regulatory changes may produce:

```text
millions
```

of candidate impacts.

---

# 235. Avoid Naive Per-Entity Event Explosion

Use hierarchy where appropriate:

```text
ChangeVerified
    ↓
ReassessmentCampaignStarted
    ↓
bounded batch processing
    ↓
only material per-subject events.
```

---

# 236. Campaign Events

Useful:

```text
campaign.started

campaign.progressed

campaign.completed.
```

Detailed item state can remain queryable.

---

# 237. Backpressure

Transport adapters SHALL support:

```text
bounded queues

consumer lag monitoring

flow control

rate limiting.
```

---

# 238. Backpressure Cannot Lose Events

Durable outbox/archive preserves publication intent.

---

# 239. Subscriber Rate Limits

External webhook consumers MAY define bounded delivery capacity.

Baobab may adapt within configured policy.

---

# 240. Subscription Quotas

Commercial entitlements MAY later limit:

```text
number of subscriptions

event volume

retention

webhooks

replay horizon.
```

Detailed commercial policy belongs to ADR-REG-0030.

---

# 241. Entitlement Does Not Alter Regulatory Truth

A lower plan may receive fewer notifications.

It cannot receive different law.

---

# 242. Notification Entitlements

Similarly:

```text
premium alerting
```

may affect delivery features.

Not decision semantics.

---

# 243. Contract Testing

Every event producer SHALL have:

```text
schema tests

CloudEvents envelope tests

AsyncAPI contract tests

compatibility tests.
```

---

# 244. Consumer Contract Tests

Critical consumers SHOULD test:

```text
duplicate event

missing optional field

new optional field

out-of-order event

replay

unknown newer event type.
```

---

# 245. Outbox Tests

Must cover:

```text
database commit succeeds / broker down

transaction rollback

relay retry

duplicate publish

relay restart.
```

---

# 246. Inbox Tests

Must cover:

```text
duplicate delivery

consumer crash after processing

consumer crash before commit

redelivery.
```

---

# 247. Webhook Security Tests

Must cover:

```text
valid signature

invalid signature

expired signature

reused nonce

wrong Content-Digest

wrong key

rotated key

tampered payload.
```

RFC 9421 explicitly allows verifier policy around signature age, expiry and nonce uniqueness; RFC 9530 provides `Content-Digest` integrity semantics.

---

# 248. SSRF Tests

Cover:

```text
localhost

127.0.0.1

link-local

cloud metadata address

DNS rebinding

redirect to private target.
```

---

# 249. Tenant Isolation Tests

Subscription for Tenant A SHALL never receive:

```text
Tenant B impact event.
```

---

# 250. Replay Authorization Test

User who lost access SHALL not regain protected data through replay.

---

# 251. Event Schema Golden Tests

Stable canonical example events SHALL be stored as contract fixtures.

---

# 252. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-EVT-I01` | Events SHALL remain projections of canonical state |
| `REG-EVT-I02` | Event stream SHALL NOT become a second regulatory source of truth |
| `REG-EVT-I03` | Events SHALL remain distinct from commands |
| `REG-EVT-I04` | Events SHALL remain distinct from human notifications |
| `REG-EVT-I05` | CloudEvents `source` SHALL mean event producer, not legal source |
| `REG-EVT-I06` | Event identity SHALL remain stable across delivery retries |
| `REG-EVT-I07` | Consumers SHALL deduplicate by stable event identity |
| `REG-EVT-I08` | Baobab SHALL not promise generic exactly-once delivery |
| `REG-EVT-I09` | Durable integrations SHALL support at-least-once delivery |
| `REG-EVT-I10` | Canonical mutation and outbox insertion SHALL be atomic |
| `REG-EVT-I11` | Subscriber failure SHALL not roll back canonical Regulations state |
| `REG-EVT-I12` | No global event ordering SHALL be assumed |
| `REG-EVT-I13` | Aggregate ordering SHALL be explicit where required |
| `REG-EVT-I14` | Event time SHALL remain distinct from legal-effective time |
| `REG-EVT-I15` | Event delivery order SHALL not determine legal chronology |
| `REG-EVT-I16` | Subscription SHALL not grant authorization |
| `REG-EVT-I17` | Tenant-private filtering SHALL occur before unauthorised delivery |
| `REG-EVT-I18` | Thin events SHOULD be preferred across bounded contexts |
| `REG-EVT-I19` | Restricted source material SHALL not be laundered through events |
| `REG-EVT-I20` | Webhook delivery SHALL use secure authenticated transport |
| `REG-EVT-I21` | Webhook retries SHALL preserve original event identity |
| `REG-EVT-I22` | Dead-lettering SHALL preserve event and failure history |
| `REG-EVT-I23` | Event replay SHALL remain distinct from regulatory decision replay |
| `REG-EVT-I24` | Replay SHALL reapply authorization |
| `REG-EVT-I25` | Event schema contracts SHALL be versioned |
| `REG-EVT-I26` | Breaking semantic change SHALL require an explicit event contract version change |
| `REG-EVT-I27` | Broker technology SHALL not leak into canonical event semantics |
| `REG-EVT-I28` | AsyncAPI SHALL describe contracts independently of deployment topology |
| `REG-EVT-I29` | Human notification delivery SHALL not alter regulatory outcome |
| `REG-EVT-I30` | Critical transactional decisions SHALL not rely only on eventually consistent event state |
| `REG-EVT-I31` | Pulse events SHALL not become regulatory truth without verification |
| `REG-EVT-I32` | CMS events SHALL not establish legal semantics |
| `REG-EVT-I33` | Consumer processing SHALL be idempotent |
| `REG-EVT-I34` | Event publication and delivery health SHALL be observable |
| `REG-EVT-I35` | Event replay and subscription facilities SHALL respect tenant isolation, rights and privacy |

---

# 253. Rejected Alternative — Events Are the Regulatory Database

Rejected.

---

# 254. Rejected Alternative — Full Event Sourcing as Mandatory Architecture

Rejected.

---

# 255. Rejected Alternative — Database Commit Then Best-Effort Publish

Rejected.

---

# 256. Rejected Alternative — Broker Publish Before Database Commit

Rejected.

---

# 257. Rejected Alternative — Generate New Event ID on Every Retry

Rejected.

---

# 258. Rejected Alternative — Exactly-Once Transport Marketing Claim

Rejected.

---

# 259. Rejected Alternative — Global Event Order

Rejected.

---

# 260. Rejected Alternative — Event Arrival Order Determines Which Law Applied

Rejected.

---

# 261. Rejected Alternative — One Global Topic With Every Tenant Payload

Rejected unless the transport can prove strict server-side isolation appropriate to the classification.

---

# 262. Rejected Alternative — Consumer Filters Private Events After Receiving Them

Rejected.

---

# 263. Rejected Alternative — Subscription Grants Access

Rejected.

---

# 264. Rejected Alternative — Raw Legal Source Text in Every Event

Rejected.

---

# 265. Rejected Alternative — CloudEvents `source` Stores Gazette URL

Rejected.

That field identifies the event source, not the legal source.

---

# 266. Rejected Alternative — Broker Technology in Shared Domain Schema

Rejected.

---

# 267. Rejected Alternative — Event = Email Notification

Rejected.

---

# 268. Rejected Alternative — Notification Failure Means Decision Failed

Rejected.

---

# 269. Rejected Alternative — Email Read Receipt Means Compliance Action Completed

Rejected.

---

# 270. Rejected Alternative — Webhook Shared Secret Embedded in Subscription Record/Event

Rejected.

---

# 271. Rejected Alternative — TLS Without Payload Authentication for High-Consequence External Webhooks

Rejected as the preferred high-assurance configuration.

---

# 272. Rejected Alternative — Ignore Webhook Replay Attacks

Rejected.

---

# 273. Rejected Alternative — Infinite Immediate Retry

Rejected.

---

# 274. Rejected Alternative — Drop Event After Retry Exhaustion

Rejected.

---

# 275. Rejected Alternative — Replay Bypasses Current Authorization

Rejected.

---

# 276. Rejected Alternative — Event Archive Replaces Canonical State

Rejected.

---

# 277. Rejected Alternative — Trade Determines Current Regulatory State from Event History Alone

Rejected.

---

# 278. Rejected Alternative — Browser Directly Consumes Privileged Regulatory Broker

Rejected.

---

# 279. Rejected Alternative — CloudEvents Subscription 0.1-WIP as Mandatory Canonical Subscription Model

Rejected for now because the surfaced CloudEvents subscription specification remains work in progress.

---

# 280. Minimum Implementation Proof

Before `ADR-REG-0024` is considered implemented, Baobab SHOULD demonstrate:

```text
1. CloudEvents 1.0 envelope.

2. stable event ID.

3. canonical event source.

4. event type versioning.

5. subject.

6. event time.

7. dataschema.

8. datacontenttype.

9. tenant reference extension.

10. context reference extension.

11. correlation ID.

12. causation ID.

13. aggregate ID.

14. aggregate version.

15. classification metadata.

16. legal-valid-from metadata.

17. knowledge-time metadata.

18. distinction between legal source and CloudEvents source.

19. AsyncAPI 3.x contract.

20. event schema in shared.

21. compatible additive schema evolution.

22. breaking-event v2 evolution.

23. deprecated event contract.

24. transactional outbox table.

25. canonical mutation + outbox atomic commit.

26. transaction rollback produces no event.

27. relay publishes committed event.

28. relay retry keeps same event ID.

29. relay restart recovery.

30. broker outage recovery.

31. publication latency metric.

32. published-event archive.

33. consumer inbox pattern.

34. duplicate delivery.

35. duplicate deduplication.

36. consumer crash before commit.

37. consumer crash after commit.

38. redelivery after crash.

39. effectively-once domain mutation.

40. at-least-once delivery contract.

41. no exactly-once assertion.

42. no global ordering assumption.

43. aggregate ordering.

44. out-of-order event handling.

45. missing aggregate version handling.

46. canonical state refresh after gap.

47. EventSubscription aggregate.

48. subscriber identity.

49. tenant scope.

50. event-type filter.

51. jurisdiction filter.

52. regulatory-profile filter.

53. change-type filter.

54. rule filter.

55. product filter.

56. HS/classification filter.

57. market filter.

58. trade-lane filter.

59. legal-entity filter.

60. transaction filter.

61. decision-outcome filter.

62. effect-class filter.

63. urgency filter.

64. typed filtering.

65. subscription authorization.

66. authorization intersection.

67. authorization revocation.

68. subscription pause.

69. subscription suspension.

70. subscription expiry.

71. INTERNAL_BROKER delivery profile.

72. WEBHOOK delivery profile.

73. webhook HTTPS enforcement.

74. HTTP Message Signature verification.

75. Content-Digest verification.

76. key ID.

77. signing-key rotation.

78. signature creation-time validation.

79. signature-expiration validation.

80. nonce replay prevention.

81. tampered-payload rejection.

82. invalid-signature rejection.

83. webhook SSRF protection.

84. redirect SSRF protection.

85. DNS-rebinding protection.

86. webhook delivery attempts.

87. exponential backoff.

88. jitter.

89. HTTP 429 handling.

90. Retry-After handling.

91. HTTP 503 handling.

92. retry exhaustion.

93. dead-letter/parking state.

94. manual delivery replay.

95. delivery retry same event ID.

96. replay new delivery-attempt ID.

97. historical subscription replay.

98. replay authorization.

99. replay by time.

100. replay by cursor.

101. replay rate limit.

102. distinction between event replay and decision replay.

103. thin event.

104. authorised canonical-resource fetch.

105. public regulatory-change event.

106. tenant-private impact event.

107. source text excluded from ordinary event.

108. privileged counsel excluded from public stream.

109. rights-restricted source protected.

110. tenant A cannot receive tenant B event.

111. NotificationPreference.

112. in-app notification.

113. email adapter seam.

114. push adapter seam.

115. notification localisation.

116. notification templates.

117. immediate notification.

118. digest notification.

119. ChangeSet aggregation.

120. quiet-hours policy.

121. critical escalation.

122. acknowledgement-required workflow.

123. unacknowledged escalation.

124. notification failure does not alter decision.

125. source.change-detected event.

126. source.monitoring-degraded event.

127. change.verified event.

128. change.future-effective event.

129. change.became-effective event.

130. impact.confirmed event.

131. reassessment.required event.

132. campaign.started event.

133. campaign.completed event.

134. rule.published event.

135. rule.superseded event.

136. rule.revalidation-required event.

137. decision.issued event.

138. decision.superseded event.

139. decision.stale event.

140. decision.outcome-changed event.

141. requirement.changed event.

142. requirement.satisfied event.

143. requirement.unsatisfied event.

144. runtime.package-activated event.

145. runtime.stale event.

146. Pulse change subscription.

147. Pulse verified-change consumption.

148. CMS regulatory-content invalidation.

149. Trade reassessment subscription.

150. Trade decision-change subscription.

151. ERP regulatory-obligation subscription.

152. browser excluded from private broker.

153. W3C Trace Context propagation.

154. trace/correlation distinction.

155. causal chain across multi-day workflow.

156. domain-event/command distinction.

157. event/notification distinction.

158. broker-provider adapter.

159. event transport can be replaced without event-contract change.

160. consumer lag metric.

161. subscription-health metric.

162. webhook-delivery latency metric.

163. dead-letter metric.

164. outbox backlog alert.

165. event-storm batch handling.

166. reassessment campaign prevents millions of naive notifications.

167. backpressure handling.

168. subscriber quota seam.

169. event entitlement seam.

170. end-to-end verified change → event → subscriber → idempotent reaction.
```

---

# 281. Initial Cross-Border Proof

The initial end-to-end proof SHOULD use:

```text
verified South African
import-rule change
```

affecting:

```text
ZuriBeans
coffee
ZA import
future shipment.
```

---

# 282. Example Flow

```text
Official regulatory change
          │
          ▼
Regulations verifies change
          │
          ▼
PostgreSQL transaction
          │
          ├── RegulatoryChange saved
          │
          └── Outbox E101 saved
          │
          ▼
COMMIT
          │
          ▼
Event Relay
          │
          ▼
com.baobab-platform.regulations.change.verified.v1
          │
      ┌───┼─────────────┐
      ▼   ▼             ▼
    Pulse CMS        Impact Engine
                         │
                         ▼
                affected shipment found
                         │
                         ▼
com.baobab-platform.regulations.reassessment.required.v1
                         │
                         ▼
                    Trade
                         │
                         ▼
                asks Regulations
                for new decision
                         │
                         ▼
                  UNSATISFIED
                         │
                         ▼
             decision.issued event
                         │
                         ▼
                     Trade PEP
                         │
                         ▼
               REGULATORY_HOLD
```

---

# 283. Notice What the Event Did Not Do

The `change.verified` event did NOT itself:

```text
block shipment

calculate legal outcome

change Trade state.
```

It caused interested systems to react.

---

# 284. Decision Authority Remained in Regulations

Trade ultimately enforced:

```text
a RegulatoryDecision
```

not:

```text
an event assumption.
```

---

# 285. Example — Duplicate

Broker sends:

```text
E101
E101
```

Trade inbox:

```text
source + id already processed.
```

Second delivery:

```text
DUPLICATE
→ no second hold.
```

---

# 286. Example — Out-of-Order

CMS receives:

```text
rule aggregate version 7
```

then:

```text
version 6.
```

CMS sees version 6 is older and does not overwrite its newer projection.

---

# 287. Example — Subscriber Down

Pulse unavailable.

Regulations:

```text
change remains verified.
```

Event:

```text
remains deliverable/replayable.
```

Pulse later recovers and catches up.

---

# 288. Example — Webhook Replay Attack

Attacker captures:

```text
signed event webhook.
```

Later resends it.

Receiver validates:

```text
signature age

expiration

nonce

event ID.
```

Replay is rejected or deduplicated according to the security profile. RFC 9421 explicitly provides the relevant signature metadata mechanisms.

---

# 289. Example — Tenant Leakage Attempt

External tenant subscribes:

```text
eventTypes = decision.*
filters = *
```

Control Plane/IAM authorisation restricts:

```text
tenant = T1.
```

Effective subscription:

```text
T1 only.
```

No T2 event enters the subscriber delivery path.

---

# 290. Example — Regulatory Change Digest

Twenty routine rule corrections occur in one week.

Rather than:

```text
20 emails,
```

NotificationPolicy creates:

```text
Weekly Regulatory Digest
```

while urgent E3-impacting change still sends immediate notification.

---

# 291. Research Foundation Summary

CloudEvents provides Baobab with a vendor-neutral event envelope and explicitly defines event identity through the combination of `source` and `id`, allowing duplicate deliveries to remain distinguishable from distinct domain occurrences. This is the foundation for Baobab's stable event identity and idempotent-consumer strategy.

AsyncAPI 3.0 separates messages, channels and operations and remains protocol-neutral, allowing the canonical event contract to remain independent of whether a future Baobab deployment uses Kafka, AMQP, HTTP webhooks or another transport.

The current CloudEvents Subscription API is still presented as a `0.1-wip` specification. Baobab therefore defines its own canonical subscription domain while remaining structurally compatible with future standard mapping rather than making an immature subscription specification foundational.

W3C Trace Context supplies interoperable `traceparent` and `tracestate` propagation for distributed operational tracing, while Baobab separately retains durable correlation and causation identifiers because regulatory workflows can span hours or days and must remain reconstructable beyond ordinary trace retention.

RFC 9421 provides a standards-based model for signing HTTP messages and includes creation times, expiration, key identifiers and nonce mechanisms useful for securing external webhook delivery and limiting replay attacks. It explicitly does not replace TLS.

RFC 9530 defines `Content-Digest` for HTTP content integrity and describes its combination with HTTP Message Signatures, making it appropriate for detecting payload modification before an external subscriber processes a signed regulatory event.

HTTP semantics also provide established retry signals: `503 Service Unavailable` can carry `Retry-After`, while `429 Too Many Requests` represents rate limiting and may likewise communicate retry timing. These support standards-aware webhook retry behaviour rather than hard-coded immediate retry loops.

---

# 292. Final Decision

Baobab Regulations SHALL implement a **durable, provider-neutral, tenant-aware regulatory event architecture**.

The architecture is:

```text
                    REGULATIONS
                   CANONICAL STATE
                         │
                         ▼
                 DOMAIN TRANSACTION
                         │
                  ┌──────┴──────┐
                  ▼             ▼
             State Change      Outbox
                                 │
                                 ▼
                           Event Publisher
                                 │
                                 ▼
                            CloudEvent
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                  Trade        Pulse          CMS
                    │            │            │
                    ▼            ▼            ▼
               Idempotent    Intelligence   Content
               Consumer       Projection    Projection
                    │
                    ▼
                Domain Action
```

The canonical-state principle is:

> **The database records what is true; events communicate that something happened.**

The event principle is:

> **Events are immutable domain facts, not commands, notifications or mutable records.**

The identity principle is:

> **Every event has a stable identity that survives retries, enabling idempotent consumption.**

The delivery principle is:

> **Baobab guarantees durable publication intent and at-least-once delivery for durable integrations; consumers provide idempotent effects rather than relying on mythical global exactly-once transport.**

The atomicity principle is:

> **A consequential domain change and the intent to publish its event SHALL commit together through a transactional outbox.**

The ordering principle is:

> **There is no global event order; bounded aggregate versions provide ordering only where domain semantics require it.**

The temporal principle is:

> **Event occurrence time, legal-valid time and regulatory knowledge time remain separate.**

The subscription principle is:

> **A subscription expresses interest, not authority; effective delivery scope is always constrained by current authorization and tenant isolation.**

The payload principle is:

> **Cross-domain events should carry stable canonical references and material summaries rather than duplicating entire regulatory records or restricted source material.**

The security principle is:

> **External webhook delivery uses authenticated encrypted transport, integrity verification and replay protection; the webhook endpoint itself is treated as an untrusted network destination during registration.**

The replay principle is:

> **Event redelivery replays communication; regulatory replay reconstructs a decision. Those are distinct operations.**

The notification principle is:

> **Human notifications are derived communication artefacts whose delivery, acknowledgement or failure does not alter the regulatory decision that generated them.**

The synchronous-decision principle is:

> **A domain engine making a consequential transaction decision SHALL ask Regulations for the current regulatory decision rather than infer current law from whatever events it happens to have consumed.**

The provider-neutrality principle is:

> **CloudEvents and AsyncAPI define Baobab's logical integration contracts; the broker remains replaceable infrastructure.**

The platform principle is:

> **Shared owns reusable contract distribution, Regulations owns regulatory event meaning, Control Plane/IAM constrain who may receive events, and each consumer owns its processing state.**

And the strategic principle is:

> **Baobab Regulations should be capable not merely of knowing that regulation changed, but of reliably and securely propagating that fact to every authorised system and person that needs to react—without losing events, duplicating business effects, leaking tenant information, or allowing the messaging layer to become the law.**

That is the architecture established by `ADR-REG-0024`.

---

## Decision Summary

```text
ADR-REG-0024
────────────────────────────────────────

STANDARD ENVELOPE

CloudEvents 1.0


CONTRACT DESCRIPTION

AsyncAPI 3.x


CANONICAL TRUTH

PostgreSQL
Regulations domain


PUBLICATION

Domain transaction
+
Transactional Outbox


DELIVERY

At least once


CONSUMPTION

Idempotent


DUPLICATE IDENTITY

CloudEvents
source + id


ORDERING

No global order.

Aggregate version
where required.


EVENT

Fact that happened.


COMMAND

Requested action.


NOTIFICATION

Human presentation.


SUBSCRIPTION

Interest
not authorization.


TENANT SECURITY

Filter before delivery.


PAYLOAD

Thin
referential
rights-safe.


WEBHOOK SECURITY

TLS

HTTP Message Signatures

Content-Digest

created / expires

nonce

key rotation


RETRY

Backoff
Jitter
Retry-After


FAILURE

Dead-letter / parked

Never silently drop.


REPLAY

Event delivery replay
≠
Decision replay.


TRACEABILITY

Correlation
Causation
W3C trace context


PULSE

Consumes verified change.

Does not establish law.


CMS

Consumes verified content change.

Does not establish law.


TRADE

Consumes reassessment signals.

Requests current decision
before consequential action.


BROKER

Replaceable infrastructure.


STRATEGIC RESULT

Reliable propagation
without creating
a second source
of regulatory truth.
```
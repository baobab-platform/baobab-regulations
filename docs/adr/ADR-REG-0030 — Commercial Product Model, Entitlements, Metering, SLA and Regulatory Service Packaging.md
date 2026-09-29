# ADR-REG-0030 — Commercial Product Model, Entitlements, Metering, SLA and Regulatory Service Packaging

**Subtitle:** Commercial Offerings, Product Composition, Tenant Entitlements, Usage Metering, Rating Boundaries, Service Levels, Marketplace Economics and Enterprise Regulatory Services

**Status:** Proposed — Foundational Commercial Architecture  
**Decision ID:** `ADR-REG-0030`  
**Engine:** `baobab-platform/baobab-regulations`  
**Cross-Repository Dependencies:** `baobab-platform/baobab-cp`, `baobab-platform/shared`, `baobab-platform/baobab-erp`, future Ledger/Billing capabilities, `baobab-platform/infrastructure`  
**Date:** 2026-09-29  
**Decision Type:** Product / Monetisation / Entitlements / Metering / SLA / Billing Integration / Marketplace Economics  
**Strategic Classification:** Commercialisation Boundary and Product Architecture

---

# 1. Executive Decision

Baobab Regulations SHALL implement a commercial architecture in which:

```text id="ao7x9n"
REGULATORY TRUTH
        │
        ▼
Regulatory Capability
        │
        ▼
Regulatory Coverage/Profile
        │
        ▼
Baobab Product Composition
        │
        ▼
Subscription
        │
        ▼
Entitlement / CapabilityGrant
        │
        ▼
CapabilityBinding
        │
        ▼
Regulations Access
        │
        ▼
Logical Customer Usage
        │
        ▼
Usage Meter
        │
        ▼
Rating / Commercial Terms
        │
        ▼
Billing / ERP / Ledger
```

The architecture SHALL preserve a hard boundary between:

```text id="kba5oe"
WHAT THE LAW REQUIRES

and

WHAT THE CUSTOMER PURCHASED.
```

A customer paying more SHALL NOT receive:

```text id="be09s6"
different law

different tariff

different prohibition

different legal hierarchy

different factual truth.
```

A higher commercial tier MAY receive:

```text id="qg33ej"
additional jurisdictions

additional profiles

higher usage allowances

change intelligence

bulk reassessment

automation features

dedicated infrastructure

higher service levels

premium evidence/export capabilities.
```

The governing rule is:

> **Commercial packaging determines access, capacity and service characteristics. It SHALL NOT determine regulatory truth.**

---

# 2. Baobab Platform Alignment

The accepted Control Plane architecture already separates:

```text id="5dvv3q"
Product

CapabilityComposition

Subscription

Entitlement / CapabilityGrant

CapabilityBinding

Provider

EngineInstance.
```

`ADR-BCP-005` specifically establishes the Product, Capability Composition, Subscription, Entitlement and Digital Estate Provisioning model.

Baobab Regulations SHALL consume that architecture rather than build a competing commercial-account system.

---

# 3. Provider-Neutral Product Architecture

The existing Baobab desired-state architecture deliberately records customer intent such as:

```text id="fd51v4"
tenant

legal entities

products / profiles

market participation

digital estates

isolation requirements

residency requirements
```

while forbidding provider and engine topology from becoming customer-authored desired state.

Commercial Regulations products SHALL follow the same rule.

---

# 4. Customer Buys a Capability, Not Technology

Correct:

```text id="ifqgv6"
Southern Africa
Cross-Border Regulatory Decision Service
```

Incorrect:

```text id="5s3yuc"
OPA Enterprise Plan

Qdrant Premium Search

Haystack Gold Package.
```

---

# 5. Framework Choices Are Baobab Internals

A pricing page SHALL NOT expose infrastructure architecture such as:

```text id="vydouw"
OPA

Haystack

LangGraph

Qdrant

PostgreSQL.
```

unless infrastructure is specifically being sold as an enterprise deployment characteristic.

---

# 6. Product ≠ Regulatory Pack

Hard invariant:

```text id="x2z00p"
Commercial Product
≠
JurisdictionPack.
```

---

# 7. Product ≠ Capability

```text id="98leyd"
Product
```

is a commercial composition.

```text id="51v6rn"
Capability
```

is a platform-consumable function.

---

# 8. Product ≠ Subscription

A product is an offer.

A subscription is a customer's contractual participation in a product/version.

---

# 9. Subscription ≠ CapabilityGrant

A subscription may cause capability grants to be created.

The subscription itself SHALL NOT become runtime authorization.

---

# 10. CapabilityGrant ≠ CapabilityBinding

The grant answers:

> **May this tenant use the capability?**

The binding answers:

> **Which provider/EngineInstance satisfies it?**

---

# 11. Entitlement ≠ Regulatory Applicability

A tenant entitled to:

```text id="i4gd93"
South Africa customs regulation
```

does not make South African customs law applicable to every transaction.

Applicability remains determined by RegulatoryContext.

---

# 12. Commercial Availability ≠ Legal Applicability

Hard invariant.

---

# 13. Regulatory Coverage ≠ Commercial Entitlement

A jurisdiction pack can exist and be fully certified while a tenant is not commercially entitled to it.

---

# 14. Product Model

Baobab SHOULD expose Regulations through reusable commercial compositions rather than one monolithic plan.

Initial product families MAY include:

```text id="3k50r8"
Regulatory Foundation

Jurisdiction Coverage

Cross-Border Corridor Profiles

Regulatory Decision API

Regulatory Change Intelligence

Regulatory Evidence & Explanation

Bulk Reassessment

Developer/API Access

Enterprise Dedicated Deployment

Marketplace Add-Ons.
```

These are architectural product families, not final pricing names.

---

# 15. Regulatory Foundation

Potential capabilities:

```text id="b4v22l"
Regulatory rule query

basic applicability

decision explanation

basic evidence trace

jurisdiction-pack access.
```

---

# 16. Jurisdiction Coverage

Potential commercial dimension:

```text id="01ihw5"
Uganda

South Africa

Kenya

Tanzania

Rwanda

regional regimes.
```

---

# 17. Cross-Border Corridor Profile

Example:

```text id="kpbeoe"
UG → ZA

Coffee / Vanilla
```

may commercially compose:

```text id="432ych"
UG jurisdiction coverage

AfCFTA regime coverage

ZA jurisdiction coverage

cross-border regulatory decision

change monitoring.
```

---

# 18. Decision API Product

Could provide:

```text id="w5h1de"
synchronous applicability

regulatory assessment

decision

explanation.
```

---

# 19. Change Intelligence Product

Could include:

```text id="3o5lza"
verified regulatory change feeds

future-effective changes

impact analysis

reassessment triggers

notifications

webhooks.
```

---

# 20. Evidence and Explanation Product

Potential:

```text id="2wt0y2"
source chains

decision evidence bundle

historical reconstruction

auditor export

legal-source citations.
```

---

# 21. Bulk Reassessment Product

Potential:

```text id="7ihs13"
portfolio reassessment

bulk shipment reassessment

post-regulatory-change impact campaign.
```

---

# 22. Dedicated Enterprise Product

Potential:

```text id="kmoe9r"
dedicated database

dedicated Qdrant

dedicated OPA runtime

private registry mirror

region-specific processing

custom retention

private packs

enterprise SLA.
```

The implementation remains governed by Control Plane isolation and residency.

---

# 23. Regulatory Marketplace Add-Ons

`ADR-REG-0029` marketplace packs MAY become commercially purchasable add-ons.

The commercial layer controls:

```text id="dgk8r2"
access
```

not:

```text id="8as506"
legal authority.
```

---

# 24. Commercial Composition

Conceptually:

```text id="y1znl6"
Product
   │
   ▼
CapabilityComposition
   │
   ├── REGULATORY_DECISION
   ├── REGULATORY_EXPLANATION
   ├── CHANGE_INTELLIGENCE
   ├── BULK_REASSESSMENT
   └── REGULATORY_EVIDENCE_EXPORT
   │
   ▼
Regulatory Profile Entitlements
   │
   ├── UG
   ├── ZA
   ├── AfCFTA
   └── UG→ZA Coffee
```

---

# 25. Commercial Product Versions

Commercial products SHALL be versioned.

A price/package change creates:

```text id="usjxuf"
ProductVersion v2
```

rather than mutating the commercial history of:

```text id="v4pa1q"
v1.
```

Modern product-catalog systems similarly model versioned plans so pricing/package evolution does not require rewriting existing subscriptions.

---

# 26. Commercial Version ≠ Regulatory Version

Hard invariant:

```text id="cva09q"
ProductVersion
≠
PackRelease

≠
RuleVersion

≠
legal effective date.
```

---

# 27. Law Change Does Not Automatically Create New Commercial Product

Example:

```text id="gxf1xd"
South African tariff changes.
```

Normally:

```text id="jyyml2"
ZA Tariff pack updates.
```

The customer remains subscribed to the existing:

```text id="ok0cu2"
ZA regulatory coverage product.
```

---

# 28. Pricing Change Does Not Change Law

Likewise:

```text id="7mbp0y"
price increases
```

must not create new legal semantics.

---

# 29. Subscription Ownership

Consistent with the Control Plane architecture, a product subscription SHALL primarily attach to:

```text id="rlsqg1"
Tenant.
```

---

# 30. Consolidated Billing Is Separate

A corporate group may want:

```text id="mc6257"
one invoice
```

for multiple tenant subscriptions.

That SHALL NOT collapse tenant isolation or entitlements.

---

# 31. BillableAccount

Conceptually:

```text id="adcuif"
BillableAccount
├── platform_account_ref
├── billing_customer_ref?
├── invoice_account_ref?
├── currency
├── payment_terms
└── tax_profile_ref?
```

The canonical ownership belongs in the appropriate platform/billing/ERP domain, not Regulations.

---

# 32. Tenant Subscription Can Roll Up to Billable Account

```text id="20wjdo"
PlatformAccount
       │
       ├── Tenant A Subscription
       ├── Tenant B Subscription
       └── Tenant C Subscription
       │
       ▼
Consolidated Billing
```

Entitlements remain tenant-specific.

---

# 33. Entitlement Model

Baobab SHALL support commercial entitlements with semantics equivalent to:

```text id="ftksyh"
BOOLEAN

STATIC / CONFIGURATION

METERED.
```

Current entitlement platforms use the same broad separation: Boolean entitlements for feature access, static entitlements for customer-specific configuration and metered entitlements for usage allowances.

---

# 34. Boolean Entitlement

Examples:

```text id="51luai"
change intelligence enabled

evidence export enabled

webhooks enabled

private pack support enabled.
```

---

# 35. Static Entitlement

Examples:

```text id="ae5a7s"
allowed jurisdiction profiles

allowed corridor profiles

retention configuration

maximum monitored entities

support class.
```

---

# 36. Metered Entitlement

Examples:

```text id="2ch5eu"
10,000 regulatory decisions/month

500 bulk reassessments/month

100 monitored trade relationships

N evidence-bundle exports.
```

---

# 37. Entitlement Provider Remains Replaceable

Baobab MAY integrate an external metering/entitlement implementation.

However:

> **Control Plane remains canonical for Baobab Product → Composition → Subscription → CapabilityGrant semantics.**

---

# 38. OpenMeter/Konnect as Reference Implementation

Current OpenMeter/Konnect architecture supports:

```text id="p2jx03"
features

meters

boolean entitlements

static entitlements

metered entitlements

plans

rate cards

usage limits.
```


It is therefore a plausible implementation provider.

---

# 39. But External Product Catalog Is a Projection

If OpenMeter or another commercial platform is used:

```text id="7sgbu0"
its customer

plan

subscription

entitlement
```

records SHALL be projections/mappings of Baobab canonical commercial state where those concepts overlap.

---

# 40. No Second Product Authority

Rejected:

```text id="oq7hck"
Control Plane says plan A

OpenMeter says plan B

Regulations guesses.
```

---

# 41. Metering Provider Port

Baobab SHOULD define:

```text id="n55bva"
UsageMeteringProvider
```

with operations conceptually supporting:

```text id="lzoy0z"
ingest_usage

query_usage

resolve_balance

record_adjustment

usage_statement.
```

---

# 42. Provider Implementations

Potential:

```text id="gqpn83"
OpenMeter

future billing platform

native Baobab provider.
```

---

# 43. Regulations Does Not Become Billing Engine

`baobab-regulations` SHALL NOT own:

```text id="y74xo9"
invoice creation

accounts receivable

payment collection

general ledger posting

revenue recognition.
```

---

# 44. Commercial Boundary

Preferred:

```text id="h8ks5m"
Regulations
     │
     ▼
Usage Events
     │
     ▼
Metering
     │
     ▼
Rating / Billing
     │
     ▼
ERP / Ledger
```

---

# 45. Metering ≠ Rating

A meter answers:

> **How much occurred?**

A rate card answers:

> **How is that quantity priced?**

---

# 46. Rating ≠ Invoice

Rating produces:

```text id="u6brmg"
commercial charge calculation.
```

Billing produces:

```text id="7m7ok4"
customer-facing financial obligation.
```

---

# 47. Invoice ≠ Ledger

Financial posting remains ERP/Ledger responsibility.

---

# 48. Usage Metering Principle

Baobab SHALL meter:

# **logical customer consumption**

rather than raw implementation operations.

---

# 49. Correct Meter

```text id="fhzc06"
one completed regulatory decision
```

---

# 50. Bad Meter

```text id="uv7rfb"
7 OPA queries

4 Qdrant calls

2 PostgreSQL queries

1 Haystack retrieval.
```

---

# 51. Why

Internal implementation can change without changing customer value.

Provider neutrality requires pricing to survive such implementation changes.

---

# 52. Internal Cost Telemetry Is Separate

Baobab SHOULD still observe:

```text id="kiiz7v"
LLM tokens

vector searches

CPU

OPA evaluations

storage

egress.
```

But those MAY be:

```text id="1pa7kj"
internal cost-attribution metrics
```

rather than customer billable units.

---

# 53. Billable Unit Examples

Potential:

```text id="7lvdz1"
REGULATORY_DECISION

BULK_REASSESSMENT_SUBJECT

EVIDENCE_EXPORT

MONITORED_ENTITY_PERIOD

PREMIUM_CHANGE_FEED

DEDICATED_ENVIRONMENT_PERIOD.
```

---

# 54. API Call Is Not Necessarily Billable Decision

One logical decision might use:

```text id="a4dbmx"
multiple HTTP requests
```

or retries.

Those SHALL not automatically multiply billing.

---

# 55. Retry Is Not New Usage

Hard invariant:

```text id="18pa7k"
system retry
≠
new billable consumption.
```

---

# 56. Idempotent Request Is Not New Usage

If the same logical decision is replayed due to network retry:

```text id="fdmrxs"
same decision operation
→ one billable event.
```

---

# 57. CloudEvents Metering

Usage events SHOULD use the same stable CloudEvents principles established by ADR-REG-0024.

Modern usage-metering systems such as OpenMeter use CloudEvents and deduplicate repeated events using the combination of `source + id`.

---

# 58. RegulatoryUsageEvent

Conceptually:

```text id="7ibq50"
RegulatoryUsageEvent
├── event_id
├── event_type
├── source
├── occurred_at
├── ingested_at
├── tenant_ref
├── billable_account_ref?
├── subscription_ref
├── capability_ref
├── meter_key
├── quantity
├── unit
├── logical_operation_ref
├── profile_ref?
├── pack_refs[]?
├── commercial_dimensions
├── billability_policy_version
└── correlation_id
```

---

# 59. Usage Event Does Not Contain Price

Hard invariant.

---

# 60. Price Can Change Independently

Meter event:

```text id="3p1re5"
1 regulatory decision
```

remains historically true regardless of the price then assigned to that unit.

---

# 61. Usage Event Does Not Contain Regulatory Outcome Detail Unless Needed

Billing generally does not need:

```text id="ow7ejg"
PROHIBITED

permit number

source text

legal opinion.
```

---

# 62. Data Minimisation

Metering SHOULD receive only dimensions required for:

```text id="2gpt9o"
aggregation

entitlement

rating

audit.
```

---

# 63. Commercial Metadata ≠ Legal Evidence

Usage events SHALL NOT become part of regulatory provenance merely because they reference a Decision.

---

# 64. Meter Definition Is Versioned

A meter definition SHALL include:

```text id="o2as1j"
meter_key

event_type

aggregation

value selector

grouping dimensions

unit

billability policy

effective period.
```

---

# 65. Meter Meaning Is Immutable

Current metering systems deliberately make core meter semantics such as event type, aggregation and value property immutable because changing them would redefine the meaning of previously collected usage.

Baobab SHALL follow the same principle.

---

# 66. Changing Meter Semantics Creates New Meter Version

Rejected:

```text id="9d7qxz"
yesterday:
decision_count = successful decisions

today:
decision_count = all attempts.
```

---

# 67. MeterVersion

Example:

```text id="4ssgm5"
regulatory_decision.v1

regulatory_decision.v2.
```

---

# 68. Usage Aggregation

Possible meter aggregations:

```text id="1bl1a9"
COUNT

SUM

UNIQUE_COUNT

LATEST/MAX
```

depending on commercial unit.

Current usage-metering platforms support analogous aggregation approaches.

---

# 69. Decision Meter

Likely:

```text id="4y4u33"
COUNT
```

of logical completed billable decision operations.

---

# 70. Monitored Entity Meter

Could use:

```text id="4nziwt"
UNIQUE_COUNT
```

or a periodic snapshot entitlement model.

---

# 71. Storage Meter

Could use:

```text id="5ricip"
LATEST/MAX
```

where contractually appropriate.

---

# 72. Billability Policy

Baobab SHALL define:

# `BillabilityPolicy`

---

# 73. Conceptually

```text id="ojwz9u"
BillabilityPolicy
├── policy_id
├── operation_type
├── bill_on_success?
├── bill_on_customer_error?
├── bill_on_platform_error?
├── retry_handling
├── cache_hit_handling
├── shadow_handling
├── replay_handling
├── reassessment_handling
├── effective_from
└── version
```

---

# 74. Default Customer-Fairness Rule

Baobab SHOULD generally avoid billing for:

```text id="6u7l9k"
platform failures

internal retries

provider failover attempts

shadow evaluations

canary duplicates

regression tests

internal reconciliation.
```

---

# 75. Cache Hit

If pricing is:

```text id="oopam2"
per logical regulatory decision
```

a cache hit MAY remain billable because the customer received the contracted decision service.

That choice must be explicit in the BillabilityPolicy.

---

# 76. Internal Recalculation Is Not Customer Usage

Example:

```text id="1yczjl"
Baobab detects compiler defect

recalculates 100,000 decisions.
```

Those corrective internal operations SHALL NOT create 100,000 customer charges.

---

# 77. Automatic Regulatory Reassessment

A verified law change may cause Baobab to reassess customer subjects.

Commercial treatment SHALL be product-defined.

Potential models:

```text id="eqkrx7"
included in change-monitoring subscription

included up to allowance

metered per affected subject

enterprise committed volume.
```

---

# 78. No Surprise Billing

Automatic system-triggered reassessment SHALL NOT create unlimited unforeseen charges unless the subscribed commercial terms clearly establish that model.

---

# 79. Customer-Initiated Historical Replay

May be separately billable if contractually defined.

---

# 80. System-Initiated Historical Replay

Performed for:

```text id="8ur0b9"
audit

regression

correctness validation
```

SHALL normally be non-billable.

---

# 81. Usage Deduplication

Every logical billable event SHALL have stable identity.

The combination:

```text id="rd8hgy"
source + event_id
```

SHALL uniquely identify a logical usage event.

Current event-based metering systems use this exact mechanism to make retries deduplicatable.

---

# 82. Usage Event Retry

If metering provider is unavailable:

```text id="u9n287"
same event ID
```

is retried.

Do not create a new billable event.

---

# 83. Transactional Outbox

Billable usage emitted from a successful logical operation SHOULD use the transactional-outbox architecture from ADR-REG-0024.

---

# 84. Example

```text id="wk0e1y"
BEGIN

persist Decision D

persist UsageEvent U(D)

COMMIT
```

The usage event then publishes asynchronously.

---

# 85. Decision and Meter Event Need Not Commit in Different Systems Atomically

Baobab avoids distributed transactions.

The durable outbox preserves publication intent.

---

# 86. Failed Decision Persistence

If Decision D never commits:

```text id="7cbn97"
no billable Decision-completed event.
```

---

# 87. Late Usage Events

Usage systems SHALL distinguish:

```text id="lmuvol"
occurred_at

received_at.
```

---

# 88. Billing Period

Usage should generally be attributed to the commercial period defined by the meter/rating policy.

Late-arriving events require explicit:

```text id="4y2m04"
late-event policy.
```

---

# 89. Closed Billing Period

Do not silently mutate a finalized invoice.

Potential:

```text id="jjwocn"
next-period adjustment

credit/debit adjustment

reissued invoice
```

belongs to billing policy.

---

# 90. Usage Events Are Immutable

Corrections SHALL use:

```text id="xil6m9"
UsageAdjustment
```

rather than changing an historical usage fact invisibly.

---

# 91. UsageAdjustment

Conceptually:

```text id="4peo44"
UsageAdjustment
├── adjustment_id
├── original_usage_event_ref
├── adjustment_type
├── quantity_delta
├── reason_code
├── authorised_by?
├── created_at
└── audit_ref
```

---

# 92. Metering Reconciliation

Baobab SHALL reconcile:

```text id="qnr03r"
logical Regulations operations
```

against:

```text id="smu1ps"
accepted metering events.
```

---

# 93. Metering Provider Outage Does Not Block Regulatory Truth

Preferred:

```text id="0x66li"
Regulatory decision succeeds

usage outbox accumulates

metering catches up later.
```

---

# 94. Billing Plane Shall Not Sit in Decision Hot Path

Unless an explicit real-time entitlement check is necessary.

---

# 95. Real-Time Entitlement Check

Where a quota is hard:

```text id="gntijq"
Request
   │
   ▼
Entitlement Check
   │
   ├── permitted → Regulations
   └── denied → Commercial Access Error
```

---

# 96. Commercial Denial ≠ Regulatory Outcome

If quota is exhausted:

```text id="hxm5ur"
ENTITLEMENT_LIMIT_EXCEEDED
```

is a commercial/platform result.

It SHALL NOT produce:

```text id="vv69j9"
PROHIBITED

INDETERMINATE.
```

---

# 97. No Mid-Decision Commercial Cutoff

Once a consequential decision request has been accepted for processing, crossing a quota threshold during execution SHOULD NOT terminate that decision halfway through.

---

# 98. Soft Limits

For safety-critical or workflow-critical regulatory decision services:

```text id="k3ipte"
soft quota + overage
```

may be preferable to a hard cutoff.

---

# 99. Why

A payment/quota boundary should not cause a shipment system to suddenly operate without regulatory assessment.

---

# 100. Hard Limit Appropriate Use

Hard limits are more appropriate for:

```text id="p2cwv6"
bulk exports

optional analytics

non-critical evidence exports

developer sandbox.
```

---

# 101. Grace Policy

Commercial suspension MAY support:

```text id="l7rdw0"
ACTIVE

GRACE

SUSPENDED

TERMINATED.
```

---

# 102. Grace Is Commercial

It SHALL not change:

```text id="2uq3o2"
RuleSet

RegulatoryDecision semantics.
```

---

# 103. Subscription Suspension

Control Plane should revoke/suspend relevant CapabilityGrants.

Regulations should not query:

```text id="wz3hcn"
invoice overdue?
```

to infer entitlement.

---

# 104. Billing Status Does Not Belong in Legal Evaluation

Hard invariant.

---

# 105. Suspended Customer

Correct:

```text id="fxxmww"
access denied:
subscription suspended.
```

Incorrect:

```text id="8tatbe"
transaction allowed because no regulatory decision available.
```

---

# 106. PEP Safe Behaviour

Domain engines SHALL follow their safety/failure policy when Regulations access is commercially or operationally unavailable.

Commercial suspension is never an implicit legal permission.

---

# 107. Regulatory Effect Class and Commercial Plan

Commercial products MAY expose different automation capabilities.

Example:

```text id="czq9fc"
Advisory
→ human-facing recommendations

Automation
→ PEP integration.
```

---

# 108. But Commercial Tier Cannot Increase Regulatory Assurance

Hard invariant:

```text id="0jpw4k"
paid E4 plan
+
pack certified only to E2
=
maximum E2.
```

---

# 109. Effective Automation Ceiling

Conceptually:

```text id="p4nhd3"
EffectiveEffectCeiling
=
minimum(
    PackCertificationCeiling,
    ContractAutomationCeiling,
    RuntimeReadinessCeiling,
    GovernanceCeiling
)
```

---

# 110. Money Cannot Buy Higher Legal Confidence

The customer can buy:

```text id="l78j4p"
automation capability
```

but the pack still has to earn the corresponding regulatory assurance independently.

---

# 111. Lower Tier Should Not Receive Incorrect Law

A limited/free tier MAY provide:

```text id="2rp1w1"
less coverage

fewer calls

less automation

less evidence detail.
```

It SHALL NOT intentionally provide:

```text id="tc8e6z"
lower-quality legal truth
```

within a supported query.

---

# 112. Unsupported Feature Response

Prefer:

```text id="srrptr"
NOT_ENTITLED
```

over an incomplete answer presented as complete.

---

# 113. Trials

Trials MAY provide:

```text id="c8i1r1"
limited jurisdictions

limited decisions

limited duration

sandbox data.
```

---

# 114. Trial Law Is Still Law

If the trial answers:

```text id="cc5528"
ZA tariff rule
```

the regulatory semantics SHALL be the same verified semantics used by paid customers.

---

# 115. Commercial Service Packaging

Baobab SHOULD support four orthogonal packaging axes.

---

# 116. Axis 1 — Regulatory Coverage

```text id="xggrti"
jurisdictions

regimes

corridors

commodities

regulatory domains.
```

---

# 117. Axis 2 — Functional Capability

```text id="dgjh2c"
query

decision

explanation

evidence

change intelligence

reassessment

webhooks

audit export.
```

---

# 118. Axis 3 — Capacity

```text id="1i7g9n"
decision volume

monitored subjects

bulk reassessments

storage

API throughput.
```

---

# 119. Axis 4 — Operational Service

```text id="vv2ab2"
shared versus dedicated

region

availability objective

support response

RTO/RPO

retention.
```

---

# 120. Avoid “Bronze/Silver/Gold” in Canonical Contracts

Marketing names may vary.

Canonical product state SHOULD express actual capabilities and limits.

---

# 121. Commercial Profile Example

```yaml id="4gv99k"
coverage:
  jurisdictions:
    - UG
    - ZA
  corridors:
    - UG-ZA
  commodities:
    - coffee
    - vanilla

capabilities:
  decision: true
  explanation: true
  change_intelligence: true
  bulk_reassessment: true

capacity:
  decisions_per_month: 10000
  monitored_subjects: 500

service:
  isolation: shared
  sla_profile: business
```

Illustrative only.

---

# 122. Price Is Not Canonical Regulations Data

Prices SHOULD live in the commercial/billing catalog.

Regulations needs:

```text id="2gnbrv"
entitlement

metering dimensions

commercial policy references.
```

---

# 123. Multi-Currency

Commercial pricing MAY support:

```text id="m4e404"
ZAR

USD

UGX

other currencies.
```

Regulatory decision semantics remain currency-neutral except where underlying legal rules require currency.

---

# 124. Pricing Currency ≠ Transaction Currency

---

# 125. Marketplace Economics

Third-party packs create a second commercial relationship:

```text id="xe0ki3"
Customer
    │
    ▼
Baobab
    │
    ▼
Marketplace Publisher.
```

---

# 126. Marketplace Revenue Models

Possible:

```text id="ccnybq"
fixed pack subscription

tenant licence

usage-based pack fee

revenue share

enterprise negotiated licence.
```

---

# 127. Initial Recommendation

Prefer:

```text id="u8beug"
clear pack subscription/add-on pricing
```

before attempting fine-grained per-rule royalties.

---

# 128. Why

A single regulatory decision may compose:

```text id="4v2us5"
six packs

thirty rules

multiple sources.
```

Per-rule economic attribution would create unnecessary complexity.

---

# 129. Publisher Compensation ≠ Legal Precedence

Hard invariant.

---

# 130. Marketplace Ranking ≠ Revenue Share

A high-margin pack SHALL not receive higher legal ranking.

---

# 131. Marketplace Usage Attribution

If usage-based publisher settlement is later required, Baobab MAY derive:

```text id="mdt10q"
PublisherUsageAllocation
```

from:

```text id="aiqlas"
RegulatoryPackLock

+

billable logical operation.
```

---

# 132. But Attribution Policy Must Be Stable

Do not invent publisher allocation after an invoice period closes.

---

# 133. Marketplace Payout Is Financial Domain

Regulations may emit attribution evidence.

ERP/Ledger/Billing owns financial settlement.

---

# 134. Service Levels

Baobab SHALL distinguish:

```text id="2sh9qd"
SLI

SLO

SLA.
```

---

# 135. Service Level Indicator

An SLI is:

```text id="5pazav"
measured service behaviour.
```

Examples:

```text id="yxe452"
availability

decision latency

change-detection latency.
```

---

# 136. Service Level Objective

An SLO is:

```text id="s2qei7"
internal/declared target
for an SLI.
```

---

# 137. Service Level Agreement

An SLA is:

```text id="b7w2x5"
contractual commitment
and consequence/remedy.
```

Google's SRE guidance similarly separates SLIs, SLOs and SLAs and recommends selecting objectives based on service behaviour meaningful to users rather than merely adopting current observed performance.

---

# 138. No Universal SLA

Different Regulations workloads have fundamentally different behaviour.

---

# 139. Interactive Decision Workload

Cares about:

```text id="drsbd8"
availability

latency

correct runtime readiness.
```

---

# 140. Bulk Reassessment

Cares more about:

```text id="0asjk6"
throughput

campaign completion time.
```

---

# 141. Regulatory Change Monitoring

Cares about:

```text id="en7lln"
source monitoring availability

change-detection lag

verification workflow latency.
```

---

# 142. Notification Delivery

Cares about:

```text id="c6fitj"
delivery latency

delivery success

webhook availability.
```

---

# 143. Pack Distribution

Cares about:

```text id="0up2dm"
registry availability

freshness

activation propagation.
```

---

# 144. Different Workloads Need Different SLOs

Google SRE explicitly recommends separate objectives where workloads have heterogeneous latency/throughput requirements.

Baobab SHALL follow that principle.

---

# 145. SLA Dimensions

Commercial service plans MAY specify:

```text id="1o7vce"
decision API availability

decision latency

bulk reassessment completion

change-monitoring freshness

notification delivery

support response

RTO

RPO.
```

---

# 146. Legal Correctness Is Not an Uptime SLA

Rejected:

```text id="1telpx"
99.99% legally correct.
```

---

# 147. Why

Legal correctness is not meaningfully represented as:

```text id="c2xeh8"
uptime percentage.
```

Baobab instead provides:

```text id="gwm1rh"
source provenance

coverage declarations

assurance certification

golden testing

decision replay

incident correction.
```

---

# 148. Regulatory Assurance Commitment

Commercial contracts MAY commit to:

```text id="y15z26"
declared coverage

source monitoring

verification processes

incident remediation

audit retention.
```

These are not equivalent to guaranteeing legal outcomes.

---

# 149. Source Availability Is External

Baobab cannot guarantee:

```text id="b8g2lh"
a regulator will publish on time

a government website will remain online

law will be unambiguous.
```

---

# 150. Freshness SLA Must Define Measurement Point

For example:

```text id="lhpzm3"
time authoritative monitored source
made change observable

→

time Baobab detected candidate.
```

---

# 151. Detection SLA ≠ Verified Interpretation SLA

A change can be detected quickly but require:

```text id="fe3dsf"
human legal review.
```

---

# 152. Therefore Separate

```text id="xj14xy"
SOURCE_MONITORING_SLO

CHANGE_DETECTION_SLO

VERIFICATION_WORKFLOW_SLO

PACK_PUBLICATION_SLO.
```

---

# 153. Example SLA Profile

Conceptually:

```text id="i5e3em"
RegulatoryServiceLevelProfile
├── profile_id
├── API_availability_objective
├── interactive_latency_objective
├── bulk_completion_objective?
├── change_detection_objective?
├── notification_objective?
├── support_response_objective?
├── RTO?
├── RPO?
├── measurement_policy
├── exclusions
└── version
```

---

# 154. Numbers Are Product Configuration

This ADR SHALL NOT hard-code one universal:

```text id="xdo7kh"
99.9%

99.95%

99.99%.
```

Those belong in versioned service-level profiles and contracts.

---

# 155. Internal SLO May Be Stricter Than SLA

Recommended.

---

# 156. Error Budgets

Baobab SHOULD use error-budget operating practice for services with explicit SLOs.

Google SRE defines the error budget as the complement of the SLO and uses its consumption to guide reliability versus release decisions.

---

# 157. Example

If:

```text id="k8q1qt"
SLO = 99.9%
```

then:

```text id="29e2jc"
error budget = 0.1%.
```

---

# 158. Error Budget Is Operational

It SHALL NOT influence:

```text id="8i6jjk"
regulatory rule interpretation.
```

---

# 159. SLA Measurement Policy

Each SLA SHALL define:

```text id="f5ph61"
measurement point

eligible requests

success criteria

window

maintenance handling

customer-caused failures

force majeure/external dependency handling

remedies.
```

---

# 160. Valid Entitlement Denial Is Not Availability Failure

If a customer legitimately exceeds a hard commercial quota:

```text id="qt85m0"
ENTITLEMENT_LIMIT_EXCEEDED
```

should not normally count as Regulations service downtime.

---

# 161. Platform Failure Is Different

If the entitlement service cannot determine whether access is valid:

```text id="a5wgl5"
ENTITLEMENT_SERVICE_UNAVAILABLE
```

that may be a service failure.

---

# 162. Regulatory Outcome Is Not SLA Success Indicator

A correct:

```text id="f11j73"
PROHIBITED
```

decision is a successful service request.

---

# 163. Successful API Response ≠ Business Approval

---

# 164. Decision Latency

Measure:

```text id="3si3x1"
accepted decision request
→
RegulatoryDecision available.
```

---

# 165. Client Network Latency

SHOULD normally be outside server-side SLI unless contract explicitly includes it.

---

# 166. Bulk Reassessment SLI

Potential:

```text id="j9f0uf"
percentage of eligible reassessment subjects
completed within target window.
```

---

# 167. Change Detection SLI

Potential:

```text id="51mg0w"
verified monitoring candidates detected
within specified time
after source publication becomes observable.
```

---

# 168. Coverage Is Not Availability

If pack coverage says:

```text id="0stqti"
SPS = NOT_COVERED
```

that is not:

```text id="wtbum2"
API downtime.
```

---

# 169. Coverage Commitments Are Separate Contract Terms

---

# 170. SLA Cannot Promote Coverage

A premium SLA cannot convert:

```text id="gtrpvq"
PARTIAL coverage
```

into:

```text id="w0p72i"
COVERED.
```

---

# 171. SLA Cannot Promote Effect Class

---

# 172. Dedicated Deployment SLA

A dedicated customer MAY receive differentiated:

```text id="v7eslg"
availability

capacity

RTO/RPO

region

maintenance windows.
```

But the same regulatory semantics should execute for the same pinned RuleSet.

---

# 173. Shared versus Dedicated Is Operational Packaging

Not legal packaging.

---

# 174. Multi-Region Enterprise

Could purchase:

```text id="ykmqn9"
multiple Regulations EngineInstances

regional failover

private registry mirrors.
```

Control Plane owns provider/topology resolution.

---

# 175. Commercial Entitlement Does Not Pick Engine Instance Directly

Correct:

```text id="ykq7xw"
product:
dedicated high-isolation service.
```

CP derives compliant:

```text id="iwhnhe"
provider

EngineInstance

region.
```

---

# 176. Rate Limits

Technical rate limits SHALL remain distinct from commercial quotas.

---

# 177. Technical Rate Limit

Protects:

```text id="nboc9n"
service availability

abuse

noisy-neighbour isolation.
```

---

# 178. Commercial Quota

Represents:

```text id="k51cyz"
contracted usage allowance.
```

---

# 179. Customer Can Have Usage Remaining But Be Rate-Limited Temporarily

---

# 180. Customer Can Be Within Technical Rate Limit But Commercially Out of Quota

---

# 181. Error Types Must Distinguish Them

Potential:

```text id="ecaj0d"
RATE_LIMITED

ENTITLEMENT_LIMIT_EXCEEDED.
```

---

# 182. Overage

Commercial products MAY permit:

```text id="jlln33"
usage allowance
+
billable overage.
```

---

# 183. Overage Is Preferable for Critical Runtime Paths

Where abrupt cutoff could create operational risk.

---

# 184. Prepaid Credits

MAY be supported.

Current metering/entitlement architectures support recurring or one-time usage grants and balance-based entitlements.

---

# 185. Credit ≠ Currency

A commercial credit may represent:

```text id="y3p8xc"
decision allowance.
```

It SHALL not be confused with:

```text id="ixbcut"
money

customs duty

tax credit.
```

---

# 186. Commitment Pricing

Enterprise contracts MAY include:

```text id="mfq70l"
committed annual decision volume

minimum marketplace spend

reserved dedicated capacity.
```

---

# 187. Commitment Is Commercial Only

Unused commitment does not affect regulatory data.

---

# 188. Seats

Human-seat pricing MAY be used for:

```text id="ftunl6"
reviewer portal

compliance team

administrative access.
```

---

# 189. Machine-to-Machine Decision Volume Should Not Be Artificially Seat-Based

The product model should support both.

---

# 190. Meter Subject

Usage aggregation SHALL normally identify:

```text id="9xa3im"
Tenant
```

as the primary consuming subject.

---

# 191. Additional Attribution

Usage MAY additionally group by:

```text id="t3kh5z"
LegalEntity

DigitalEstate

API client

profile

jurisdiction

commercial product

marketplace pack.
```

---

# 192. Grouping Dimension Does Not Grant Access

---

# 193. Group Usage Must Sum Correctly

If consolidated billing spans tenants:

```text id="5arskj"
invoice aggregation
```

can happen after tenant-specific usage accounting.

---

# 194. Metering Privacy

Usage events SHALL follow ADR-REG-0028.

---

# 195. Billing System Does Not Need Regulatory Secrets

It generally needs:

```text id="xbcdpo"
tenant

meter

quantity

time

commercial dimensions.
```

Not:

```text id="mvx67d"
shipment contents

permit scans

counsel opinion.
```

---

# 196. External Metering Provider Is Data Processor

Its:

```text id="bhpej4"
region

retention

security

subprocessors
```

must satisfy applicable Baobab policy.

---

# 197. Usage Residency

A tenant may require:

```text id="csxlfg"
usage telemetry
```

to remain in an approved region even if it contains no legal evidence.

---

# 198. Metering Access

Billing support staff SHALL NOT automatically receive:

```text id="s4qo96"
regulatory evidence access.
```

---

# 199. Revenue Operations Separation

Commercial administrators may change:

```text id="pkw24s"
price

allowance

subscription.
```

They SHALL NOT be able to change:

```text id="siift6"
RuleVersion

legal hierarchy

RegulatoryDecision.
```

---

# 200. Regulatory Administrators

May publish rules according to governance.

They SHALL NOT automatically change:

```text id="8qq424"
customer pricing.
```

---

# 201. Separation of Duties

```text id="xsm5k3"
REGULATORY GOVERNANCE
≠
REVENUE OPERATIONS
≠
FINANCE
≠
PLATFORM ADMINISTRATION.
```

---

# 202. Commercial Audit

Baobab SHOULD preserve:

```text id="fdh4xl"
subscription changes

entitlement changes

quota changes

manual usage adjustments

rate-card changes

billing-account mappings

SLA-profile changes.
```

---

# 203. Commercial Audit Is Separate from Regulatory Audit

But correlation MAY connect them.

---

# 204. Example

```text id="ufkc2i"
Regulatory Decision D
        │
        └── produced Usage Event U

Usage Event U
        │
        └── contributed to Invoice I.
```

This does not make Invoice I part of D's legal provenance.

---

# 205. Product Downgrade

A customer moving from:

```text id="6og4o5"
Enterprise
→
Basic
```

may lose:

```text id="atz0w3"
dedicated deployment

bulk reassessment

certain jurisdiction entitlements

premium SLA.
```

---

# 206. Historical Decisions Remain Historical

Downgrade SHALL NOT rewrite:

```text id="nskps6"
past Decisions

past usage

past audit.
```

---

# 207. Pack Access After Downgrade

Historical regulatory decisions may remain inspectable according to:

```text id="e0atob"
contract

retention

audit policy.
```

This is distinct from rights to make new decisions using the pack.

---

# 208. Product Cancellation

Should trigger:

```text id="vb6507"
new-request access revocation

metering closure

retention/offboarding policy

final usage reconciliation

final billing.
```

---

# 209. Cancellation Does Not Delete Public Law

ADR-REG-0028 applies.

---

# 210. Service Suspension and Events

Customers SHOULD receive:

```text id="kc0uvu"
subscription expiring

quota threshold

grace entering

suspension scheduled
```

commercial notifications where appropriate.

---

# 211. Commercial Notifications ≠ Regulatory Notifications

Hard invariant.

---

# 212. Do Not Mix

```text id="nhvsx4"
“new import prohibition”
```

with:

```text id="8n3svs"
“80% of API allowance consumed.”
```

as one semantic event family.

---

# 213. Threshold Notifications

Modern metered-entitlement systems support threshold events as usage balances approach defined limits.

Baobab MAY implement equivalent threshold notifications.

---

# 214. Threshold Example

```text id="312uey"
50%

80%

100%
```

of monthly decision allowance.

Exact thresholds are product configuration.

---

# 215. Commercial Metrics

Track at least:

```text id="chh4y6"
subscriptions

active entitled tenants

usage

overage

pack adoption

corridor adoption

change-monitoring adoption

metering lag

metering reconciliation errors

entitlement-check failures.
```

---

# 216. Internal Unit Economics

Baobab SHOULD separately understand:

```text id="kumh9p"
cost per decision

cost per monitored source

cost per reassessment

LLM cost

vector/storage cost

dedicated infrastructure cost.
```

---

# 217. Internal Cost ≠ Customer Price

Pricing may include:

```text id="9tzlmo"
value

market

support

risk

coverage cost

margin
```

in addition to infrastructure cost.

---

# 218. Regulatory Source Provider Costs

Commercial source licences may introduce:

```text id="w5txky"
pass-through cost

per-tenant licence

per-jurisdiction fee.
```

---

# 219. Pack Economics Must Respect Source Rights

A customer entitlement cannot exceed the source licence under ADR-REG-0012.

---

# 220. Premium Source Licence

Potential flow:

```text id="9kdk96"
Customer buys premium jurisdiction profile
       │
       ▼
Baobab entitlement
       │
       ▼
Provider licence entitlement checked
       │
       ▼
Regulations access.
```

---

# 221. Provider Licence Failure

If Baobab loses commercial source rights:

```text id="cvv3ef"
commercial entitlement
```

does not manufacture those rights.

Coverage/readiness must degrade explicitly.

---

# 222. Source Cost Shall Not Alter Legal Hierarchy

A more expensive source is not more authoritative merely because it costs more.

---

# 223. SLA and Third-Party Sources

Contract SHALL define dependency treatment.

For example:

```text id="89rjev"
Baobab API available

government source unavailable.
```

These are separate service conditions.

---

# 224. Source Monitoring Redundancy

Premium service MAY fund:

```text id="dyb7p0"
multiple source channels

commercial backup providers

higher monitoring frequency.
```

---

# 225. But Redundancy Does Not Create Legal Authority

---

# 226. Support Packaging

Enterprise service MAY include:

```text id="oubkxh"
24×7 incident response

named technical support

regulatory operations escalation

integration support.
```

---

# 227. Support ≠ Legal Counsel

Unless separately contracted and delivered by appropriately qualified providers.

---

# 228. Legal Review Marketplace

Future specialist human review MAY itself become a marketplace service.

That SHALL remain separate from automated Regulations entitlement.

---

# 229. Human Review Meter

If commercialised, a human-review request may be:

```text id="m5grtd"
per case

per hour

retainer

included allowance.
```

It SHALL not be disguised as a deterministic API decision.

---

# 230. Outcome-Based Pricing Caution

Baobab SHOULD avoid pricing directly on:

```text id="fkeq6k"
whether transaction is allowed

amount of duty saved

regulatory outcome.
```

unless deliberately governed.

---

# 231. Why

Commercial incentives must not appear to influence:

```text id="hpk3sc"
legal interpretation

classification

preference eligibility.
```

---

# 232. Safer Billing Units

Prefer neutral units such as:

```text id="a868gq"
decision

monitored subject

coverage subscription

dedicated capacity.
```

---

# 233. No “Pay for Favourable Decision”

Explicitly prohibited.

---

# 234. Regulatory Decision Independence

The evaluator SHALL have no access to:

```text id="d51llk"
customer price tier

invoice value

publisher commission
```

unless a strictly non-legal operational parameter genuinely requires it.

---

# 235. Commercial Fields Must Not Enter BRIR Input

Examples prohibited from legal rule evaluation:

```text id="27z0n7"
monthly_recurring_revenue

pricing_tier

discount_percentage

publisher_commission.
```

---

# 236. Subscription Tier May Gate Invocation Before BRIR

But once evaluation occurs:

```text id="373ecd"
same context
+
same RuleSet
+
same evidence
+
same DecisionPolicy
=
same regulatory semantics.
```

---

# 237. Commercial Neutrality Golden Test

ADR-REG-0025 SHALL include:

```text id="l2c9iq"
same RegulatoryContext

tenant plan A
versus
tenant plan B

same certified RuleSet
```

Expected:

```text id="79zovz"
same regulatory outcome.
```

---

# 238. Allowable Difference

One plan may receive:

```text id="8me372"
full evidence export
```

while another receives:

```text id="8r5q32"
summary explanation.
```

The underlying decision remains the same.

---

# 239. Commercial Isolation Test

Tenant A usage SHALL never contribute to:

```text id="6xzvi6"
Tenant B quota

Tenant B invoice

Tenant B marketplace settlement.
```

---

# 240. Reconciliation

Baobab SHALL regularly reconcile:

```text id="xu494x"
subscriptions

CapabilityGrants

entitlements

meter balances

usage aggregates

billing statements.
```

---

# 241. Entitlement Drift

Example:

```text id="4cnc1o"
CP says:
REGULATORY_DECISION not granted

metering provider says:
active.
```

Result:

```text id="zt6baz"
ENTITLEMENT_DRIFT.
```

---

# 242. Control Plane Wins for Runtime Capability Authority

External metering state must reconcile toward canonical CP state.

---

# 243. Usage Drift

Example:

```text id="nr5g7u"
10,001 Decisions exist

meter reports 10,000.
```

Requires reconciliation.

---

# 244. Invoice Shall Not Be Silently Corrected by Regulations

Financial adjustment flows through billing/ERP governance.

---

# 245. Subscription Change Lifecycle

Conceptually:

```text id="uv17a0"
Product Selection
      │
      ▼
Commercial Agreement
      │
      ▼
ProductSubscription
      │
      ▼
Capability Grants
      │
      ▼
Profile Entitlements
      │
      ▼
Provisioning
      │
      ▼
Readiness
      │
      ▼
ACTIVE.
```

---

# 246. Upsell Lifecycle

```text id="0bleae"
Add ZA SPS coverage
      │
      ▼
Product change
      │
      ▼
Entitlement change
      │
      ▼
Pack/profile availability
      │
      ▼
Capability readiness
      │
      ▼
Active.
```

---

# 247. Commercial Change Must Use CP Controlled Mutation Where Appropriate

Do not mutate:

```text id="wmezty"
grants

isolation

provider binding
```

behind Control Plane's back.

---

# 248. Usage-Based Feature Gate

Conceptually:

```text id="57c3ye"
Request
   │
   ▼
CapabilityGrant
   │
   ▼
Metered Entitlement
   │
   ├── allowance available
   │       ↓
   │   Regulations
   │
   └── no allowance
           ↓
       overage/grace/
       commercial deny
```

---

# 249. Regulatory Decision Execution

```text id="cxyck2"
Entitlement Admission
       │
       ▼
Regulatory Decision
       │
       ▼
Usage Event
```

Do not charge first and then discover the request was not authorised.

---

# 250. Metering Provider Failures

Possible state:

```text id="3lwfay"
METERING_DEGRADED.
```

---

# 251. Entitlement Provider Failure

Possible:

```text id="gqbdn1"
ENTITLEMENT_RESOLUTION_DEGRADED.
```

---

# 252. Safety Policy

For high-consequence operations, outage policy SHOULD specify whether to:

```text id="cqv4aq"
use bounded cached entitlement

allow temporary grace

fail closed.
```

This is a commercial/platform availability policy, not a legal rule.

---

# 253. Cached Entitlement

If used, must include:

```text id="i1yzfg"
tenant

capability

allowance state

validity

issued_at

expires_at

source version.
```

---

# 254. Cached Entitlement Must Expire

No indefinite access because billing service is unavailable.

---

# 255. Metering Security

Usage events SHALL be:

```text id="t2wy85"
authenticated

tenant-scoped

idempotent

auditable.
```

---

# 256. Customer Cannot Self-Report Arbitrary Billable Usage

Unless an explicit trusted ingestion API exists with validation.

---

# 257. Server-Side Meter Generation Preferred

For Regulations service usage:

```text id="fd2tfb"
Regulations
```

or a trusted Baobab gateway SHOULD emit authoritative usage.

---

# 258. Frontend Meter Events Are Not Billing Authority

---

# 259. Meter Replay

Replaying the same canonical usage event SHALL not duplicate charge.

---

# 260. Usage Statement

Customers SHOULD eventually be able to inspect:

```text id="kz3r41"
meter

period

usage

allowance

overage

adjustments.
```

---

# 261. Explainable Billing

The customer should be able to answer:

> Why was I charged for this quantity?

without exposing sensitive regulatory content.

---

# 262. Usage-to-Operation Trace

```text id="e3jwp3"
Invoice Line
    │
    ▼
Usage Aggregate
    │
    ▼
Usage Events
    │
    ▼
Logical Operation References.
```

---

# 263. Financial Privacy

Billing users MAY inspect:

```text id="vn6hlx"
decision IDs/counts
```

without necessarily seeing:

```text id="6tm8xc"
decision evidence.
```

---

# 264. Marketplace Publisher Statement

Likewise a publisher should be able to inspect:

```text id="hqz6ie"
licensed usage / revenue allocation
```

without receiving tenant transaction secrets.

---

# 265. Commercial Analytics

Pulse MAY later analyse aggregated commercial metrics if appropriately authorised.

---

# 266. Pulse Shall Not Become Billing Source of Truth

---

# 267. Commercial Events

Potential separate event family:

```text id="z93k01"
subscription.activated

subscription.changed

subscription.suspended

entitlement.changed

usage.threshold-reached

usage.adjusted

sla.budget-exhausted.
```

---

# 268. These Are Not Regulatory Events

They may share CloudEvents transport but have distinct semantic namespaces.

---

# 269. SLA Error Budget Event

Potential:

```text id="lgl5yj"
service.error-budget.threshold-reached.
```

---

# 270. Error Budget Automation

May trigger:

```text id="nu9v48"
release freeze

capacity intervention

incident review.
```

---

# 271. It SHALL NOT Change Regulatory Rule Evaluation

---

# 272. Service-Level Transparency

Customer-facing product metadata SHOULD state:

```text id="dtruzr"
coverage

usage allowances

rate limits

SLA

support

isolation

residency options.
```

---

# 273. Avoid Ambiguous “Unlimited”

Any “unlimited” product SHOULD still state:

```text id="9kbq97"
fair-use

abuse

technical rate limits

service constraints.
```

---

# 274. Coverage Transparency

A customer buying:

```text id="5o7q41"
UG→ZA Cross-Border
```

should be able to inspect machine-readable:

```text id="y81mbj"
coverage manifest

known gaps

assurance ceiling.
```

---

# 275. Commercial UI Must Not Hide Coverage Gaps

---

# 276. SLA UI Must Not Imply Legal Guarantee

---

# 277. Marketplace UI Must Not Equate Price with Authority

---

# 278. Commercial Model Evolution

Baobab SHOULD begin with simple, comprehensible packaging.

Recommended initial commercial primitives:

```text id="injod3"
base subscription

jurisdiction/profile add-ons

included decision allowance

overage

change-intelligence add-on

enterprise dedicated add-on

marketplace pack add-ons.
```

---

# 279. Avoid Premature Pricing Complexity

Do not begin with:

```text id="e033ki"
different price per rule

different price per source

different price per legal effect

micro-royalty per provision

dynamic legal-complexity pricing.
```

---

# 280. Complexity Can Evolve Later

The architecture supports richer models without requiring them initially.

---

# 281. Initial ZuriBeans Internal Consumption

ZuriBeans may initially consume Regulations through:

```text id="at27wl"
INTERNAL / group subscription
```

according to Control Plane subscription classification.

---

# 282. Internal Does Not Mean Unmetered Operationally

Baobab SHOULD still meter internal usage for:

```text id="fnvlrn"
capacity

cost attribution

product learning

forecasting.
```

---

# 283. Internal Metering May Be Non-Billable

```text id="1m0hvr"
usage exists
≠
invoice exists.
```

---

# 284. This Is Important for Product Economics

ZuriBeans can reveal:

```text id="w8vhnm"
cost per regulatory decision

source monitoring cost

profile maintenance cost
```

before external pricing is finalised.

---

# 285. External Customer Model

A future external B2B tenant might purchase:

```text id="9mqgmc"
Base Regulations
+
ZA
+
UG
+
UG→ZA Trade Profile
+
10,000 decisions/month
+
Change Intelligence
+
Business SLA.
```

---

# 286. Thamani Example

Thamani may independently purchase:

```text id="sagfyl"
different regulatory profiles
```

based on its logistics/shipping activities.

ZuriBeans entitlement SHALL never confer Thamani entitlement.

---

# 287. Corporate Ownership Does Not Collapse Subscription

Hard invariant.

---

# 288. External Group Customer

A third-party client with several subsidiaries may have:

```text id="12gf5o"
PlatformAccount
      │
      ├── Tenant A
      ├── Tenant B
      └── Tenant C
```

with consolidated commercial contract but isolated entitlements and usage.

---

# 289. Regulatory Product Does Not Care Who Owns Subsidiary for Billing Alone

Legal entity relationships affect RegulatoryContext only when legally relevant.

---

# 290. Commercial Product Registry

Control Plane should remain canonical for:

```text id="y4zmmc"
Product

ProductVersion

CapabilityComposition

Subscription.
```

---

# 291. Regulations Commercial Descriptor

Regulations MAY publish provider metadata such as:

```text id="262lcv"
capabilities offered

regulatory profiles offered

meter keys

SLA dimensions supported

commercial add-on compatibility.
```

This is descriptive capability metadata.

---

# 292. Billing Integration Contract

`shared` SHOULD eventually define provider-neutral schemas for:

```text id="t77dvs"
UsageEvent

UsageAdjustment

MeterDefinition

EntitlementProjection

UsageStatementRef

CommercialCorrelation.
```

---

# 293. It SHALL Not Define Prices Globally

Prices are product/commercial configuration.

---

# 294. Currency/Tax Billing Logic

Customer-subscription tax/VAT on Baobab's own service belongs to:

```text id="k5vj9v"
billing/ERP/finance.
```

It is NOT the same as:

```text id="ozzi3q"
import VAT
```

computed by Regulations for a shipment.

---

# 295. Critical Naming Separation

```text id="0525ej"
REGULATORY IMPORT VAT
```

and:

```text id="8g84gb"
VAT ON BAOBAB'S CUSTOMER INVOICE
```

are unrelated business domains.

---

# 296. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-COM-I01` | Commercial product SHALL remain distinct from regulatory truth |
| `REG-COM-I02` | Product SHALL remain distinct from Capability |
| `REG-COM-I03` | Product SHALL remain distinct from RegulatoryPack |
| `REG-COM-I04` | Subscription SHALL remain distinct from CapabilityGrant |
| `REG-COM-I05` | CapabilityGrant SHALL remain distinct from CapabilityBinding |
| `REG-COM-I06` | Entitlement SHALL remain distinct from regulatory applicability |
| `REG-COM-I07` | Higher price SHALL NOT produce different law for identical regulatory context |
| `REG-COM-I08` | Commercial product versions SHALL remain distinct from RuleVersions and PackReleases |
| `REG-COM-I09` | Law changes SHALL NOT automatically create commercial product versions |
| `REG-COM-I10` | Pricing changes SHALL NOT alter historical regulatory decisions |
| `REG-COM-I11` | Control Plane SHALL remain canonical for Product/Composition/Subscription/CapabilityGrant |
| `REG-COM-I12` | External entitlement platforms SHALL be projections/providers, not competing Baobab product authorities |
| `REG-COM-I13` | Regulations SHALL not issue customer invoices |
| `REG-COM-I14` | Metering SHALL remain distinct from rating |
| `REG-COM-I15` | Rating SHALL remain distinct from invoicing/accounting |
| `REG-COM-I16` | Customer meters SHOULD measure logical customer value rather than internal implementation operations |
| `REG-COM-I17` | Internal retries SHALL NOT create duplicate billable usage |
| `REG-COM-I18` | Idempotent decision retries SHALL NOT double-charge |
| `REG-COM-I19` | Meter semantics SHALL be versioned and historically stable |
| `REG-COM-I20` | Usage corrections SHALL use auditable adjustments rather than silent mutation |
| `REG-COM-I21` | Metering provider outage SHOULD NOT normally invalidate committed regulatory decisions |
| `REG-COM-I22` | Commercial denial SHALL remain distinct from RegulatoryDecision outcome |
| `REG-COM-I23` | Quota exhaustion SHALL NOT be interpreted as regulatory permission or prohibition |
| `REG-COM-I24` | Commercial plan SHALL NOT elevate regulatory effect above certification/readiness ceiling |
| `REG-COM-I25` | Lower-priced access SHALL NOT intentionally substitute incorrect regulatory semantics |
| `REG-COM-I26` | Technical rate limits SHALL remain distinct from commercial quotas |
| `REG-COM-I27` | SLA availability SHALL remain distinct from regulatory coverage |
| `REG-COM-I28` | Legal correctness SHALL NOT be represented as an uptime percentage |
| `REG-COM-I29` | Different workload classes SHALL have independently meaningful SLOs |
| `REG-COM-I30` | SLA profile SHALL not elevate pack assurance or legal coverage |
| `REG-COM-I31` | Marketplace publisher revenue SHALL never affect legal precedence |
| `REG-COM-I32` | Regulatory evaluator SHALL not consume customer price/commission fields as legal inputs |
| `REG-COM-I33` | Tenant usage SHALL remain tenant-isolated even under consolidated billing |
| `REG-COM-I34` | Internal/group use MAY be metered without generating an invoice |
| `REG-COM-I35` | Regulatory usage telemetry SHALL obey ADR-REG-0028 security/residency requirements |
| `REG-COM-I36` | Commercial notifications SHALL remain distinct from regulatory notifications |
| `REG-COM-I37` | Commercial audit SHALL remain distinct from regulatory audit |
| `REG-COM-I38` | Cancellation/downgrade SHALL NOT rewrite historical Decisions or UsageEvents |
| `REG-COM-I39` | Marketplace/source licensing constraints SHALL bound what can commercially be sold |
| `REG-COM-I40` | Same certified RuleSet + same context + same evidence SHALL yield same regulatory semantics regardless of price tier |

---

# 297. Rejected Alternatives

The following designs are explicitly rejected:

```text id="kzrl0e"
premium customers get different law

free tier gets intentionally less accurate law

billing status inside BRIR

invoice overdue → transaction permitted

invoice overdue → transaction prohibited

one giant Regulations plan

product hard-coded to OPA infrastructure

Product = JurisdictionPack

Pack = subscription

subscription = authorization

API HTTP request count as only billing model

billing every OPA query

billing every Qdrant search

billing internal retries

billing shadow decisions

billing canary duplicates

meter semantics mutated historically

prices stored in RuleVersion

usage event contains unit price

Regulations creates invoices

Regulations posts general ledger entries

marketplace commission affects legal ranking

publisher revenue affects pack precedence

“99.99% legally correct” SLA

SLA availability used as regulatory confidence

higher SLA increases effect class

hard quota silently disabling critical regulatory safety

one billing account collapsing tenant isolation

OpenMeter product catalog becoming the canonical Baobab product registry

metering provider outage deleting usage

product cancellation deleting public regulatory knowledge

commercial rate card used in customs-duty calculation.
```

---

# 298. Minimum Implementation Proof

Before `ADR-REG-0030` is considered implemented, Baobab SHOULD demonstrate:

```text id="4emznk"
1. CP Product integration.

2. ProductVersion.

3. CapabilityComposition.

4. ProductSubscription.

5. CapabilityGrant.

6. CapabilityBinding separation.

7. tenant-owned subscription.

8. consolidated billing-account mapping.

9. product/profile distinction.

10. RegulatoryPack/product distinction.

11. commercial version/regulatory version distinction.

12. base Regulations product composition.

13. jurisdiction add-on composition.

14. corridor-profile composition.

15. Decision API capability.

16. Explanation capability.

17. Evidence-export capability.

18. Change-intelligence capability.

19. Bulk-reassessment capability.

20. dedicated-deployment add-on.

21. marketplace-pack add-on.

22. Boolean entitlement.

23. static entitlement.

24. metered entitlement.

25. quota allowance.

26. overage allowance.

27. trial entitlement.

28. grace state.

29. suspension state.

30. termination state.

31. entitlement reconciliation.

32. CP remains entitlement authority.

33. external entitlement-provider adapter.

34. OpenMeter-compatible provider seam.

35. no duplicate product catalog authority.

36. UsageMeteringProvider interface.

37. Regulations usage producer.

38. logical billable-operation model.

39. RegulatoryUsageEvent schema.

40. CloudEvents usage envelope.

41. stable event ID.

42. tenant subject.

43. subscription reference.

44. capability reference.

45. logical operation reference.

46. meter key.

47. quantity/unit.

48. occurred_at.

49. ingested_at.

50. usage event contains no price.

51. usage-event data minimisation.

52. decision-count meter.

53. bulk-reassessment meter.

54. evidence-export meter.

55. monitored-subject meter.

56. MeterDefinition.

57. immutable meter semantics.

58. meter versioning.

59. COUNT aggregation.

60. SUM aggregation where applicable.

61. UNIQUE_COUNT where applicable.

62. BillabilityPolicy.

63. successful-operation billing policy.

64. platform-failure non-billing.

65. internal-retry non-billing.

66. provider-failover non-billing.

67. shadow-evaluation non-billing.

68. canary-evaluation non-billing.

69. internal replay non-billing.

70. customer replay policy.

71. automatic reassessment policy.

72. cache-hit billing policy.

73. usage-event deduplication.

74. same source+id counted once.

75. usage transactional outbox.

76. metering-provider outage retry.

77. late-event policy.

78. billing-period attribution.

79. UsageAdjustment.

80. manual adjustment audit.

81. usage reconciliation.

82. decision-count reconciliation.

83. meter-balance reconciliation.

84. real-time entitlement check.

85. cached entitlement.

86. cached-entitlement expiry.

87. commercial access error.

88. regulatory outcome distinct from commercial denial.

89. hard-quota test.

90. soft-quota test.

91. overage test.

92. no mid-decision cutoff.

93. effect-class commercial ceiling.

94. pack-certification ceiling.

95. runtime-readiness ceiling.

96. effective effect ceiling.

97. paid tier cannot promote E2 pack to E3/E4.

98. same-law-across-tiers golden test.

99. evidence-output differentiation test.

100. product downgrade.

101. downgrade preserves historical decisions.

102. cancellation.

103. cancellation preserves audit history.

104. final usage reconciliation.

105. BillableAccount.

106. consolidated group billing.

107. tenant usage isolation under consolidation.

108. multi-currency price seam.

109. RateCard provider seam.

110. rating separated from meter.

111. billing separated from rating.

112. ERP/Ledger financial handoff.

113. Regulations cannot post invoice.

114. Regulations cannot post journal.

115. import-VAT/customer-invoice-VAT naming separation.

116. marketplace fixed-subscription add-on.

117. marketplace publisher entitlement.

118. publisher settlement evidence.

119. publisher compensation does not affect precedence.

120. publisher usage attribution seam.

121. ServiceLevelIndicator.

122. ServiceLevelObjective.

123. ServiceLevelAgreementProfile.

124. decision API availability SLI.

125. decision latency SLI.

126. bulk reassessment SLI.

127. source-monitoring SLI.

128. change-detection SLI.

129. notification-delivery SLI.

130. pack-distribution SLI.

131. support-response target seam.

132. RTO seam.

133. RPO seam.

134. measurement window.

135. SLA exclusions.

136. scheduled-maintenance policy.

137. entitlement denial excluded appropriately from availability SLI.

138. valid PROHIBITED decision counted as successful service response.

139. coverage gap not counted as infrastructure outage.

140. error-budget calculation.

141. error-budget alert.

142. reliability release policy.

143. workload-specific SLOs.

144. dedicated-deployment SLA profile.

145. shared-deployment SLA profile.

146. technical rate limiting.

147. commercial quota.

148. technical/commercial limit distinction.

149. usage threshold notifications.

150. threshold events distinct from regulatory events.

151. commercial audit trail.

152. subscription-change audit.

153. entitlement-change audit.

154. quota-adjustment audit.

155. rate-card-change audit.

156. usage-adjustment audit.

157. SLA-profile-change audit.

158. metering privacy controls.

159. metering residency controls.

160. external-metering provider policy.

161. no legal evidence in billing events.

162. revenue-operations role.

163. regulatory-governance role.

164. finance role.

165. separation of duties.

166. internal cost telemetry.

167. LLM-token internal cost metric.

168. Qdrant internal cost metric.

169. OPA internal cost metric.

170. storage internal cost metric.

171. customer meter remains provider-neutral.

172. source-licensing commercial constraint.

173. premium-source entitlement.

174. source-rights loss degradation.

175. source cost does not affect authority.

176. ZuriBeans INTERNAL subscription.

177. ZuriBeans metering without invoice.

178. Thamani independent subscription.

179. external customer tenant subscription.

180. external group consolidated invoice.

181. individual tenant entitlements under group invoice.

182. customer usage statement.

183. usage-to-operation trace.

184. invoice-line-to-usage aggregation seam.

185. publisher statement with no tenant-secret leakage.

186. commercial events.

187. subscription activated event.

188. entitlement changed event.

189. quota threshold event.

190. suspension event.

191. SLA error-budget event.

192. commercial events separated from Regulations domain events.

193. product-profile coverage display.

194. known-gap visibility.

195. SLA display.

196. coverage/SLA separation.

197. machine-readable entitlement inspection.

198. machine-readable usage inspection.

199. machine-readable service-level profile.

200. end-to-end Product → Subscription → Grant → Binding → Decision → Usage → Meter → Rating → Billing/ERP flow.
```

---

# 299. Initial Commercial Product Shape

Baobab SHOULD initially resist an elaborate pricing matrix.

A practical first commercial composition could be:

```text id="hcgppu"
BAOBAB REGULATIONS
        │
        ├── BASE
        │     ├── API access
        │     ├── regulatory query
        │     ├── decisions
        │     └── explanations
        │
        ├── COVERAGE ADD-ONS
        │     ├── Uganda
        │     ├── South Africa
        │     ├── AfCFTA
        │     └── UG→ZA Cross-Border
        │
        ├── INTELLIGENCE ADD-ON
        │     ├── regulatory change monitoring
        │     ├── impact analysis
        │     └── reassessment
        │
        ├── CAPACITY
        │     ├── included decisions
        │     └── overage
        │
        ├── MARKETPLACE ADD-ONS
        │     └── specialist regulatory packs
        │
        └── ENTERPRISE
              ├── dedicated infrastructure
              ├── private packs
              ├── residency options
              ├── custom retention
              └── enhanced SLA/support
```

---

# 300. Initial ZuriBeans Model

During internal launch:

```text id="3tg2pq"
Tenant:
ZuriBeans

Subscription type:
INTERNAL

Coverage:
UG
ZA
AfCFTA
UG→ZA coffee
UG→ZA vanilla

Capabilities:
Decision
Explanation
Change Intelligence
Reassessment

Metering:
enabled

Billing:
non-cash/internal initially

Purpose:
measure real usage
and unit economics.
```

---

# 301. Why Meter ZuriBeans Now

It lets Baobab learn:

```text id="454w1k"
decisions per shipment

reassessments per regulatory change

change-notification volume

source-processing cost

AI cost

infrastructure cost

support burden.
```

before external pricing assumptions become contracts.

---

# 302. External Customer Example

Future customer:

```text id="5urmxn"
Product:
Cross-Border Regulatory Business

Coverage:
UG + ZA + AfCFTA

Profile:
UG→ZA agricultural trade

Allowance:
25,000 decisions / month

Change Intelligence:
enabled

Overage:
enabled

Deployment:
shared

SLA:
business profile.
```

---

# 303. Enterprise Example

```text id="bb2r2n"
Product:
Enterprise Regulatory Execution

Coverage:
custom

Allowance:
annual committed volume

Deployment:
dedicated

Region:
contractually approved

Private Packs:
enabled

Bulk Reassessment:
enabled

SLA:
enterprise profile

RTO/RPO:
contract-defined.
```

---

# 304. Same Law Test

Suppose both customers evaluate:

```text id="xeoomj"
same shipment facts

same legal time

same RuleSet

same evidence.
```

One has:

```text id="s1hvxk"
Business
```

and the other:

```text id="2acekw"
Enterprise.
```

Expected:

```text id="efz80q"
same classification

same applicable rules

same requirements

same regulatory outcome.
```

Differences may include:

```text id="4x3wq8"
response latency objective

support

dedicated infrastructure

evidence export format

commercial quota.
```

---

# 305. Research Foundation

Current entitlement-platform architecture supports an important distinction Baobab adopts here: feature access may be Boolean, static/configurational or usage-metered. Metered entitlements can maintain balances, allowances and overages, while product catalogs can separately version plans, rate cards and pricing. This supports Baobab's decision to represent coverage, capability and capacity as different commercial dimensions rather than one undifferentiated subscription tier.

Current usage-metering systems also use event-driven metering with explicit event identity, occurrence time, subject and data attributes. OpenMeter, for example, uses CloudEvents and deduplicates repeated usage on `source + id`, which aligns directly with Baobab's ADR-REG-0024 event semantics and prevents ordinary network retries from creating duplicate consumption.

Meter definitions themselves require historical semantic stability. OpenMeter makes core fields such as aggregation, event type and value property immutable because changing them would reinterpret previously recorded usage. Baobab adopts the same principle: when the meaning of a meter changes, the meter version changes rather than silently re-rating history under a new definition.

Google SRE's established service-level model distinguishes SLIs, SLOs and SLAs, recommends choosing objectives around user-relevant service behaviour, and recognises that heterogeneous workloads may require different objectives. This directly supports Baobab defining separate objectives for interactive regulatory decisions, bulk reassessment, source/change monitoring and event delivery rather than publishing one meaningless global “Regulations SLA.”

Google's error-budget model additionally treats reliability as an explicit operating budget—the complement of the SLO—which can guide release and reliability decisions. Baobab adopts this operational pattern while keeping error-budget state completely outside regulatory interpretation and Decision semantics.

The existing Baobab architecture is equally important. Control Plane already models Product, Capability Composition, Subscription, Entitlement/CapabilityGrant and CapabilityBinding as separate concepts, while its desired-state architecture explicitly keeps provider and EngineInstance topology out of customer intent. Regulations therefore adds usage semantics, coverage packaging and service-level descriptors without becoming another product/subscription authority.

---

# 306. Final Decision

Baobab Regulations SHALL be commercialised as a **coverage-aware, capability-composed, entitlement-controlled and usage-observable regulatory service**, while preserving complete independence between commercial state and regulatory truth.

The final architecture is:

```text id="m0k7ai"
                  REGULATORY KNOWLEDGE
                         │
                         ▼
              Certified Regulatory Packs
                         │
                         ▼
                 Regulatory Profiles
                         │
                         ▼
                    Capabilities
                         │
                         ▼
                Product Composition
                         │
                         ▼
                    Subscription
                         │
                         ▼
                     Entitlement
                         │
                         ▼
                 CapabilityGrant
                         │
                         ▼
                CapabilityBinding
                         │
                         ▼
              Regulatory Decision API
                         │
                  ┌──────┴──────┐
                  ▼             ▼
        RegulatoryDecision    UsageEvent
                  │             │
                  ▼             ▼
             Domain PEP       Meter
                                │
                                ▼
                              Rating
                                │
                                ▼
                             Billing
                                │
                                ▼
                         ERP / Ledger
```

The truth principle is:

> **The commercial tier SHALL never determine what the law means.**

The product principle is:

> **Customers purchase compositions of regulatory coverage, capabilities, capacity and operational service—not implementation technologies.**

The platform principle is:

> **Control Plane remains canonical for Product, Composition, Subscription, Grant and Binding; Regulations contributes domain capabilities, regulatory profiles and usage facts.**

The entitlement principle is:

> **Entitlements determine whether and how much of a capability may be consumed; they do not determine whether a regulation applies.**

The metering principle is:

> **Meter the logical customer service delivered, not the incidental number of OPA calls, SQL queries, vectors retrieved or model tokens consumed internally.**

The idempotency principle is:

> **One logical billable operation creates one billable usage fact; retries, failovers, shadow evaluations and infrastructure implementation details do not create artificial customer consumption.**

The historical principle is:

> **Meter definitions, usage events, adjustments and commercial product versions are historically stable and auditable.**

The billing principle is:

> **Regulations emits usage; a metering/rating layer prices it; billing/ERP/Ledger creates and accounts for financial obligations. Regulations itself is not the invoicing system.**

The safety principle is:

> **Commercial quota exhaustion or subscription suspension produces an explicit commercial-access state; it SHALL never masquerade as `PERMITTED`, `PROHIBITED` or another RegulatoryDecision outcome.**

The automation principle is:

> **A customer may purchase access to greater automation, but money cannot elevate an E2-certified regulatory profile into E3 or E4.**

The fairness principle is:

> **A lower-priced customer may receive less coverage, capacity or automation—but whenever Baobab answers the same supported legal question from the same evidence and RuleSet, the regulatory semantics must remain the same.**

The SLA principle is:

> **Baobab measures availability, latency, freshness, throughput, recovery and notification service levels; it does not convert legal correctness into a fictitious uptime percentage.**

The workload principle is:

> **Interactive decisions, bulk reassessment, change monitoring and notifications each receive service objectives appropriate to their actual workload.**

The error-budget principle is:

> **Reliability objectives may govern release velocity and operational remediation, never regulatory interpretation.**

The marketplace principle is:

> **Publishers may earn revenue from verified regulatory knowledge, but price, commission, popularity and commercial ranking SHALL never establish legal authority or rule precedence.**

The enterprise principle is:

> **Dedicated infrastructure, stronger isolation, residency commitments and enhanced SLA are commercial service characteristics—not different law.**

The internal-launch principle is:

> **ZuriBeans should be metered from the beginning even where the initial subscription is internal and non-cash, because real consumption is necessary to understand Baobab Regulations' unit economics before external pricing is finalised.**

And the strategic principle is:

> **Baobab Regulations becomes commercially valuable not by selling access to legal text, but by selling reusable regulatory coverage, executable contextual decisions, verified change intelligence, explainability, automation and operational assurance—while ensuring that the customer's ability to pay never alters the regulatory truth the platform is entrusted to determine.**

That is the architecture established by **`ADR-REG-0030`**.

---

# Decision Summary

```text id="u2lfkl"
ADR-REG-0030
────────────────────────────────────

LAW

≠ product tier


PRODUCT

Coverage
+
Capability
+
Capacity
+
Service


CONTROL PLANE OWNS

Product

Composition

Subscription

CapabilityGrant

CapabilityBinding


REGULATIONS CONTRIBUTES

Profiles

Coverage

Capabilities

Usage facts


ENTITLEMENT

Access

Configuration

Allowance


ENTITLEMENT

≠ applicability


METER

Logical customer value

not internal compute.


BILLABLE UNITS

Decision

Reassessment subject

Evidence export

Monitored subject

Dedicated capacity


DO NOT BILL

Retries

Failover

Shadow

Canary

Regression

Internal correction


USAGE EVENT

Immutable

Idempotent

Tenant-scoped

No price


METER DEFINITION

Versioned

Historically stable


METERING

≠ rating


RATING

≠ invoice


REGULATIONS

does not invoice.


ERP / LEDGER

own financial posting.


QUOTA

Commercial state

not legal outcome.


HIGHER TIER

may buy

more coverage

more capacity

more automation

better SLA

dedicated infrastructure


HIGHER TIER

cannot buy
different law.


EFFECT CEILING

Certification

∩ Contract automation

∩ Runtime readiness

∩ Governance


SLA

Availability

Latency

Freshness

Throughput

RTO / RPO

Support


SLA

≠ legal correctness


MARKETPLACE

Publisher revenue

≠ legal authority


INTERNAL LAUNCH

Meter ZuriBeans now

even if not invoiced.


COMMERCIAL MOAT

Coverage

+
Contextual Decisions

+
Change Intelligence

+
Evidence

+
Automation

+
Operational Assurance


FINAL PRINCIPLE

Monetise access
to regulatory capability.

Never monetise
regulatory truth itself.
```
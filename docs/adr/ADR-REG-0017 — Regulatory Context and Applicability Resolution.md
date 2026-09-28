# ADR-REG-0017 — Regulatory Context and Applicability Resolution

**Status:** Proposed — Foundational Runtime Architecture  
**Decision ID:** `ADR-REG-0017`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Regulatory Context / Jurisdiction Resolution / Applicability / RuleSet Selection / Cross-Border Context  
**Strategic Classification:** Core Regulatory Execution Infrastructure

---

# 1. Decision Context

Baobab Regulations now has architectural decisions covering:

```text
authority
sources
provenance
temporal truth
regulatory ontology
normative effects
machine-executable BRIR
```

The next problem is:

> **Which of those rules apply to this particular legal entity, activity, product, transaction, jurisdiction and time?**

That question is the purpose of this ADR.

---

# 2. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine`
- `ADR-REG-0003 — Regulatory Authority and Interpretation Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics and Defeasible Reasoning`
- `ADR-REG-0010 — Regulatory Knowledge Graph`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`

It also SHALL conform to accepted Control Plane decisions including:

- `ADR-BCP-003 — Capability Registry, Grants, Scopes, Bindings and Deterministic Resolution`
- `ADR-BCP-004 — Context, Market, Geography, Legal-Entity and Digital Estate Resolution`
- `ADR-BCP-007 — Capability Resolution and Service-to-Service Consumption`
- `ADR-BCP-009 — Security, Isolation, Residency, Revocation and Failure Semantics`
- `ADR-BCP-011 — Market Participation, Trade Lanes and Cross-Market Trading`
- `ADR-BCP-014 — Canonical Counterparty Identity, Roles and Relationships`
- `ADR-BCP-018 — Organisation, Corporate Group, Platform Account and Tenant Relationship Model`

---

# 3. Executive Decision

Baobab Regulations SHALL implement a deterministic:

# **Regulatory Applicability Resolution Pipeline**

which resolves:

```text
VERIFIED REGULATORY RULES
              ×
RESOLVED PLATFORM CONTEXT
              ×
REGULATED ACTIVITY
              ×
LEGAL ACTOR ROLES
              ×
TRANSACTION GEOGRAPHY
              ×
JURISDICTION / REGIME
              ×
PRODUCT / SUBJECT
              ×
CLASSIFICATION
              ×
REGULATED EVENT TIME
              ×
RELEVANT FACTS
              ↓
     APPLICABLE RULESET
```

The canonical principle is:

> **Applicability SHALL be resolved from authoritative context and explicit rule semantics. It SHALL NOT be guessed from market, tenant, IP address, storefront, source-document location or semantic similarity.**

---

# 4. Fundamental Equation

Conceptually:

```text
Applicability =
    f(
      RuleScope,
      PlatformContext,
      ActorRoles,
      RegulatedActivity,
      JurisdictionRoles,
      RegulatoryRegimes,
      TransactionGeography,
      SubjectMatter,
      ProductClassification,
      LegalTime,
      Conditions,
      Exceptions,
      Exemptions,
      LegalHierarchy
    )
```

---

# 5. Applicability Is Not Rule Retrieval

These are different questions:

```text
RETRIEVAL

"Which rules might be relevant?"
```

versus:

```text
APPLICABILITY

"Which rules legally apply?"
```

Qdrant/Haystack MAY assist with retrieval during research or authoring.

They SHALL NOT establish transactional applicability.

---

# 6. Applicability Is Not Entitlement

These are also different:

```text
ENTITLEMENT

"May Tenant T invoke
Baobab Regulations?"
```

and:

```text
APPLICABILITY

"Does Regulation R apply
to Transaction X?"
```

The first belongs primarily to:

```text
Control Plane
+
IAM
+
subscription/capability policy.
```

The second belongs to:

```text
Baobab Regulations.
```

---

# 7. Subscription Cannot Change Law

A tenant not subscribing to a premium Regulations product does not cause:

```text
a legal obligation to disappear.
```

It merely means Baobab may not provide that capability to the tenant.

---

# 8. Capability Grant Cannot Create Applicability

Likewise:

```text
CapabilityGrant
```

does not imply:

```text
Regulation R applies.
```

---

# 9. Market Is Not Jurisdiction

This accepted Control Plane principle remains foundational:

```text
Market
≠
Country
≠
Jurisdiction
≠
LegalEntity
≠
TransactionGeography.
```

---

# 10. Why This Matters

A ZuriBeans transaction may involve:

```text
commercial market:
South Africa

seller:
Ugandan legal entity

origin:
Uganda

export jurisdiction:
Uganda

transit:
Kenya / Tanzania
depending on route

import jurisdiction:
South Africa

destination:
Cape Town

trade regime:
AfCFTA / other qualifying regimes

currency:
USD

customer:
South African company.
```

No single:

```text
market = ZA
```

field can determine the complete regulatory rule set.

---

# 11. WCO Alignment

The WCO Data Model is designed around standardized cross-border regulatory data for import, export and transit processes and explicitly distinguishes transaction roles, countries, locations and data supplied by traders versus government authorities.

This reinforces Baobab's decision that cross-border regulatory context must be multi-dimensional.

---

# 12. LegalRuleML Alignment

LegalRuleML defines jurisdiction as an area or subject matter over which an authority applies legal power and explicitly supports context and factual statements as part of legal rule representation.

Baobab SHALL preserve equivalent expressive power while using its own canonical contracts.

---

# 13. ELI Alignment

ELI defines a common model for legislation metadata and provides explicit jurisdictional/legal-resource metadata rather than treating document location as legal applicability.

---

# 14. Context Ownership Principle

Baobab Regulations SHALL NOT duplicate or redefine canonical platform context entities already owned by Control Plane.

Control Plane owns canonical resolution of, among other things:

```text
Tenant

Platform Account

Organisation

Legal Entity

Business Unit

Digital Estate

Digital Property

Channel

Market

Jurisdiction

Operating Geography

Capability Context

Isolation Context.
```

---

# 15. Regulations Enriches Context

Regulations SHALL create a:

# `RegulatoryContextSnapshot`

which references resolved Control Plane context and enriches it with:

```text
regulated activities

legal actor roles

transaction facts

product classifications

jurisdiction roles

regulatory regimes

relevant event times

regulatory evidence state.
```

---

# 16. Context Resolution Direction

Correct:

```text
Consumer
   │
   ▼
Control Plane
   │
   ▼
resolved PlatformContext
   │
   ▼
Regulations
   │
   ▼
RegulatoryContextSnapshot
```

Rejected:

```text
Browser
   │
   ▼
"tenant=foo&jurisdiction=ZA"
   │
   ▼
Regulations trusts it.
```

---

# 17. Authoritative Context Principle

Caller-provided values MAY be:

```text
claims

hints

references

requested targets.
```

They SHALL NOT automatically become canonical context.

---

# 18. Context Resolver SHALL Fail Closed

If:

```text
tenant ambiguous

legal entity unresolved

market invalid

jurisdiction conflicting

counterparty mapping ambiguous

canonical object belongs to another tenant
```

then context resolution SHALL fail.

The Control Plane's existing architecture already adopts fail-closed behavior for unresolved and ambiguous context.

---

# 19. Canonical Regulatory Context

Conceptually:

```text
RegulatoryContextSnapshot
├── context_snapshot_id
├── platform_context_ref
├── tenant_ref
├── platform_account_ref?
├── organisation_ref?
├── legal_entity_ref
├── business_unit_ref?
├── digital_estate_ref?
├── market_refs[]
├── channel_ref?
├── principal_ref?
├── transaction_ref?
├── subject_refs[]
├── actor_bindings[]
├── regulated_activities[]
├── geography[]
├── jurisdiction_bindings[]
├── regime_bindings[]
├── classifications[]
├── temporal_context
├── facts[]
├── evidence_state_refs[]
├── context_version
├── resolved_at
└── provenance
```

---

# 20. Snapshot, Not Master Data

`RegulatoryContextSnapshot` SHALL be:

```text
an immutable evaluation envelope
```

not:

```text
the master customer record

shipment master

product catalogue

organisation registry.
```

---

# 21. Source Engines Retain Ownership

Examples:

```text
Legal Entity
    Control Plane

Shipment
    Trade

Invoice
    ERP / Trade

Editorial content
    CMS

Identity
    IAM

Market intelligence
    Pulse

Regulatory decision
    Regulations.
```

---

# 22. Context Snapshot Purpose

The snapshot records:

> **What facts and canonical references did Regulations actually evaluate?**

This supports replay under ADR-REG-0014 and 0015.

---

# 23. Tenant

Tenant primarily determines:

```text
isolation

subscription

private regulatory overlays

tenant counsel interpretations

tenant-specific configuration.
```

Tenant SHALL NOT automatically determine jurisdiction.

---

# 24. Platform Account

A platform customer/account may contain:

```text
multiple organisations

multiple legal entities

subsidiaries.
```

ADR-BCP-018 explicitly supports this organisational complexity.

Regulations SHALL therefore never assume:

```text
Tenant = Legal Entity.
```

---

# 25. Organisation

Organisation expresses organisational structure.

It may help establish:

```text
group relationship

corporate ownership

business relationship.
```

It does not by itself determine:

```text
which legal entity bears an obligation.
```

---

# 26. Legal Entity

The legal entity is critical because regulatory obligations usually attach to legally recognised actors.

Examples:

```text
importer

exporter

employer

licence holder

taxpayer

data controller.
```

---

# 27. Legal Entity SHALL Be Explicit

A consequential assessment SHOULD ordinarily have a resolved:

```text
legal_entity_ref
```

for every material regulated actor whose identity is known.

---

# 28. No Tenant-as-Legal-Entity Shortcut

Rejected:

```text
regulated_actor = tenant_id.
```

---

# 29. Business Unit

Business unit MAY affect:

```text
operating activity

location

internal responsibility.
```

It SHALL not be treated as a legal person unless external law explicitly recognises it in the relevant context.

---

# 30. Digital Estate

Digital Estate identifies the consuming experience.

Examples:

```text
ZuriBeans buyer portal

supplier portal

Nabhold corporate estate.
```

This is useful for:

```text
capability resolution

user experience

entitlements.
```

It generally does not determine legal applicability.

---

# 31. Channel

Channel MAY matter where law differentiates:

```text
online sale

physical retail

marketplace

direct B2B

distance selling.
```

Where relevant, it SHALL be represented as an explicit fact or activity characteristic.

---

# 32. Market

Market describes Baobab commercial operating context.

It MAY help select:

```text
commercial configuration

catalogue

pricing

language

currency.
```

It SHALL NOT stand in for regulatory jurisdiction.

---

# 33. Market Participation

Control Plane's accepted model explicitly tracks capabilities such as:

```text
SOURCING

PROCUREMENT

SELLING

IMPORTING

EXPORTING

WAREHOUSING

DISTRIBUTION

FULFILMENT

LEGAL_PRESENCE

PROCESSING

TRANSIT.
```

Regulations SHALL consume these as context where useful.

---

# 34. Market Participation Is Not Proof of Transaction Activity

A legal entity configured for:

```text
IMPORTING
```

in South Africa does not mean every transaction is an import.

Transaction activity still needs resolution.

---

# 35. Trade Lane

Control Plane models directional Trade Lanes independently from Market Participation.

Regulations SHALL use Trade Lane references where available for cross-border context.

---

# 36. Trade Lane Is Not Legal Regime

This remains a hard distinction:

```text
TradeLane
≠
Treaty
≠
Customs Union
≠
Trade Agreement
≠
Legal Jurisdiction.
```

---

# 37. Trade Lane Does Not Guarantee Preferential Treatment

Example:

```text
UG → ZA
```

does not mean:

```text
AfCFTA preferential origin automatically applies.
```

Qualification must be evaluated.

---

# 38. Regulated Activity

Applicability SHALL be activity-aware.

Canonical activity vocabulary SHOULD support at least:

```text
IMPORT

EXPORT

TRANSIT

SALE

PURCHASE

SUPPLY

MANUFACTURE

PROCESS

STORE

WAREHOUSE

TRANSPORT

DISTRIBUTE

ADVERTISE

LABEL

REGISTER

FILE

PAY

EMPLOY

COLLECT_DATA

PROCESS_DATA

TRANSFER_DATA.
```

The vocabulary SHALL remain extensible.

---

# 39. Activity Is Not Market Participation

```text
MarketParticipationCapability
```

describes authorised/configured operating footprint.

```text
RegulatedActivity
```

describes the activity being legally assessed.

---

# 40. Multiple Activities

One transaction may create several regulated activities:

```text
SELL

EXPORT

TRANSPORT

IMPORT

STORE

DISTRIBUTE.
```

Each can trigger different regulation.

---

# 41. Activity Chain

Conceptually:

```text
Supplier
   │
   ▼
SELL
   │
   ▼
EXPORT
   │
   ▼
CARRIAGE
   │
   ▼
IMPORT
   │
   ▼
WAREHOUSE
   │
   ▼
DISTRIBUTE.
```

---

# 42. Applicability May Differ by Activity

Example:

```text
export permit
```

applies to:

```text
EXPORT
```

while:

```text
import permit
```

applies to:

```text
IMPORT.
```

They SHALL not be conflated into one generic:

```text
CROSS_BORDER_TRADE.
```

---

# 43. Actor Role

Regulatory rules SHALL primarily refer to legal roles, not arbitrary platform personas.

Examples:

```text
IMPORTER

EXPORTER

SUPPLIER

BUYER

SELLER

CARRIER

CUSTOMS_BROKER

WAREHOUSE_OPERATOR

MANUFACTURER

PRODUCER

LICENSEE

EMPLOYER

DATA_CONTROLLER.
```

---

# 44. ActorRoleBinding

Conceptually:

```text
ActorRoleBinding
├── role
├── canonical_actor_ref
├── legal_entity_ref?
├── counterparty_ref?
├── source
├── verification_state
├── valid_period?
└── provenance
```

---

# 45. Same Entity, Multiple Roles

One legal entity MAY be:

```text
seller
+
exporter
+
producer.
```

---

# 46. Different Entities, Different Roles

A transaction MAY involve:

```text
seller ≠ exporter

buyer ≠ importer

carrier ≠ customs broker.
```

Applicability SHALL support this explicitly.

---

# 47. Counterparty Context

Control Plane's canonical counterparty model SHALL be referenced rather than duplicated.

Regulations MAY need:

```text
counterparty role

legal identity

residence/incorporation

licence status

relationship.
```

---

# 48. Counterparty Role Is Transactional

A counterparty may be:

```text
buyer in transaction A

supplier in transaction B.
```

Role SHALL therefore be contextual.

---

# 49. Transaction Geography

Regulations SHALL model geography by role.

Not:

```text
countries = [UG, ZA]
```

alone.

---

# 50. Jurisdiction / Geography Roles

Initial vocabulary SHOULD include:

```text
INCORPORATION

ESTABLISHMENT

LEGAL_PRESENCE

ORIGIN

PRODUCTION

PROCESSING

EXPORT

IMPORT

DESTINATION

TRANSIT

WAREHOUSING

PLACE_OF_SUPPLY

PLACE_OF_PERFORMANCE

DATA_SUBJECT

DATA_PROCESSING

EMPLOYMENT

ASSET_LOCATION

DISPUTE_FORUM

REGULATORY_AUTHORITY.
```

---

# 51. Role-Qualified Geography

Correct:

```text
EXPORT_JURISDICTION = UG

IMPORT_JURISDICTION = ZA
```

rather than:

```text
jurisdiction = ZA.
```

---

# 52. Country Is Not Always Jurisdiction

A country may contain:

```text
national jurisdictions

provincial/state jurisdictions

municipal rules

special economic zones

free zones.
```

---

# 53. Non-State Jurisdiction

Regulatory context MAY also include:

```text
supranational regime

regional integration regime

customs union

treaty regime

special regulatory zone.
```

---

# 54. RegulatoryJurisdictionBinding

Conceptually:

```text
RegulatoryJurisdictionBinding
├── jurisdiction_ref
├── jurisdiction_role
├── basis
├── fact_refs[]
├── valid_at
├── verification_state
└── provenance
```

---

# 55. Multiple Jurisdictions Are Normal

Cross-border assessment SHOULD expect:

```text
N ≥ 2 jurisdictions
```

rather than treating multi-jurisdiction as exceptional.

---

# 56. Transit Jurisdiction

Transit MAY activate:

```text
customs

transport

SPS

dangerous goods

security

documentation
```

requirements.

Transit SHALL be captured when known/material.

---

# 57. Unknown Transit Route

Where route is not yet known:

```text
transit jurisdiction = UNKNOWN
```

may result in:

```text
partial / planning assessment
```

rather than invented routing.

---

# 58. Destination Is Not Import Jurisdiction Automatically

Goods may:

```text
enter country A
```

and ultimately:

```text
be delivered in country B.
```

These roles SHALL remain separate.

---

# 59. Origin Is a Legal Concept

Country of origin is not always:

```text
shipping origin

seller country

manufacturing location.
```

WCO material explicitly defines country of origin according to criteria used for tariffs, quantitative restrictions and trade measures.

---

# 60. Origin SHALL Be Evaluated

Where preferential/non-preferential origin matters:

```text
origin determination
```

SHALL be a regulatory fact, potentially derived through constitutive rules.

---

# 61. Regime Context

Regulations SHALL evaluate relevant `RegulatoryRegime` memberships.

Examples:

```text
national customs regime

EAC

SACU

SADC

AfCFTA

bilateral agreement.
```

---

# 62. Regime Membership Is Temporal

As established in ADR-REG-0015:

```text
membership today
```

does not imply:

```text
membership at historical transaction date.
```

---

# 63. Requested Regime

A caller MAY request consideration of:

```text
AfCFTA preference.
```

This is:

```text
requested_regime
```

not:

```text
verified qualification.
```

---

# 64. Regime Eligibility

Baobab SHALL evaluate:

```text
party membership

effective dates

product coverage

origin rules

transaction criteria

exceptions

documentation.
```

before determining a preferential regime applies.

---

# 65. Higher Integration

ADR-REG-0007 established that some regional arrangements may preserve higher levels of integration.

Regime selection SHALL therefore not use:

```text
choose one agreement
```

as a universal model.

---

# 66. Multiple Regimes May Coexist

Possible:

```text
national law

customs union

regional treaty

continental agreement
```

all relevant simultaneously.

---

# 67. Product / Subject

Rules MAY apply based upon:

```text
goods

service

legal entity

facility

employment relationship

financial transaction

data processing operation.
```

Applicability SHALL therefore use generic:

```text
RegulatorySubject
```

rather than assume all Regulations concerns physical goods.

---

# 68. Initial Goods Subject

Initial cross-border scope SHALL support:

```text
product_ref

commodity identity

classification

origin

quantity

value

composition

processing state

intended use

packaging

transport mode.
```

---

# 69. Product Identity Is Not Classification

```text
Coffee Beans SKU 101
```

is a product identity.

```text
HS 0901...
```

is a regulatory classification.

---

# 70. Classification Is Versioned

The assessment SHALL identify:

```text
scheme

scheme edition/version

classification code

classification validity

determination provenance.
```

---

# 71. Classification Unknown

If rule applicability depends on classification and classification is unresolved:

```text
INDETERMINATE
```

or:

```text
REVIEW_REQUIRED.
```

---

# 72. No Similarity-Based Classification as Legal Fact

AI/Qdrant MAY suggest candidate classifications.

They SHALL not silently become authoritative applicability facts.

---

# 73. Product Attributes

Rules may require:

```text
species

variety

processing method

ingredients

weight

packaging

intended use

hazard class

value.
```

These SHALL be explicit facts when material.

---

# 74. Legal Entity Attributes

Rules may depend on:

```text
incorporation jurisdiction

business form

registration

licences

revenue/size

regulated status

economic operator status.
```

---

# 75. Facts Have Provenance

Every material fact used in applicability SHALL follow ADR-REG-0014.

---

# 76. Facts May Be Derived

Example:

```text
raw:
product composition

constitutive rule:
composition satisfies definition X

derived fact:
regulated_product_type = X.
```

---

# 77. Derived Facts SHALL Be Traceable

They SHALL identify:

```text
source facts

constitutive rule

RuleVersion.
```

---

# 78. Legal Time

Applicability SHALL use explicit legal time according to ADR-REG-0015.

---

# 79. Regulated Event Time

The relevant time may be:

```text
export date

customs entry date

contract date

import date

sale date

filing date.
```

Rule semantics determine which event controls.

---

# 80. Evaluation Date Is Not Automatically Legal Date

A transaction assessed today for shipment next month may require:

```text
future legal state.
```

---

# 81. Knowledge Perspective

Applicability also binds to:

```text
knowledge_time
```

for:

```text
historical-as-known

historical-restated

current

future-effective
```

queries.

---

# 82. Rule Scope

Every executable RuleVersion SHOULD expose a coarse `RuleScope`.

---

# 83. RuleScope

Conceptually:

```text
RuleScope
├── jurisdiction_scope[]
├── regime_scope[]
├── subject_domains[]
├── activities[]
├── actor_roles[]
├── instrument_scope?
├── classification_scope?
├── geographic_scope?
├── legal_valid_period
├── applicability_profile
└── provenance
```

---

# 84. RuleScope Is Indexable

RuleScope exists partly to reduce the executable candidate universe efficiently.

---

# 85. RuleScope SHALL Remain Semantic

It SHALL not be generated merely from:

```text
document keywords.
```

---

# 86. Scope versus Condition

Example:

```text
scope:
South African customs import rules

condition:
shipment value > threshold.
```

Scope filters the rule universe.

Condition evaluates the specific transaction.

---

# 87. Scope versus Exception

Example:

```text
scope:
imports of product class X

exception:
personal-use goods below Y.
```

---

# 88. Applicability Criterion

BRIR SHOULD support explicit:

```text
ApplicabilityCriterion
```

nodes separate from general conditions where useful.

---

# 89. Applicability Resolution Stages

Baobab SHALL resolve applicability through defined stages.

```text
Stage 0  Request validation
Stage 1  Platform context resolution
Stage 2  Subject/transaction resolution
Stage 3  Actor-role resolution
Stage 4  Regulated-activity resolution
Stage 5  Geography/jurisdiction resolution
Stage 6  Regime resolution
Stage 7  Classification/subject resolution
Stage 8  Temporal resolution
Stage 9  Candidate rule selection
Stage 10 BRIR applicability evaluation
Stage 11 Exceptions/exemptions
Stage 12 Hierarchy/conflict resolution
Stage 13 Applicable RuleSet snapshot
```

---

# 90. Stage 0 — Request Validation

Validate:

```text
caller identity

requested capability

request schema

canonical references

assessment purpose.
```

---

# 91. Stage 1 — Platform Context Resolution

Regulations SHALL consume an authoritative:

```text
PlatformContext
```

or verifiable Control Plane context assertion.

---

# 92. Context Assertion

A service-to-service context assertion SHOULD include enough material to identify:

```text
tenant

legal entity

organisation

market

jurisdiction where already resolved

digital estate

principal

capability

context version

expiry.
```

Exact Control Plane contract remains CP-owned.

---

# 93. Context Assertion Validation

Regulations SHALL verify:

```text
issuer

signature/authentication

expiry

tenant consistency

legal entity consistency.
```

---

# 94. Stage 2 — Subject Resolution

Resolve relevant domain objects:

```text
shipment

order

product

counterparty

facility

employment relationship

data-processing activity.
```

---

# 95. Domain Resolver Ports

Regulations SHOULD depend on Baobab-owned ports such as:

```text
TradeFactProvider

ERPFactProvider

CounterpartyFactProvider

ClassificationProvider.
```

Not internal database coupling.

---

# 96. No Cross-Engine Database Joins

Rejected:

```text
Regulations SQL JOIN Trade database.
```

---

# 97. Stage 3 — Actor-Role Resolution

Determine:

```text
who is importer?

who is exporter?

who is seller?

who is licence holder?
```

from canonical relationships and transaction facts.

---

# 98. Role Ambiguity

If:

```text
importer cannot be established
```

and import law depends on importer identity:

```text
context incomplete.
```

---

# 99. Stage 4 — Activity Resolution

Resolve the actual regulated activities.

Do not infer merely from UI route.

---

# 100. Example

A buyer portal user creating an order does not necessarily mean:

```text
the buyer is importer of record.
```

---

# 101. Stage 5 — Geography Resolution

Resolve role-qualified geography from:

```text
trade lane

shipment route

origin determination

destination

entity establishment

locations

event location.
```

---

# 102. Geography Candidate versus Verified Geography

Planning scenarios MAY contain:

```text
proposed route.
```

The snapshot SHALL distinguish:

```text
ACTUAL

PLANNED

CLAIMED

VERIFIED.
```

---

# 103. Stage 5 — Jurisdiction Resolution

Regulations maps relevant geography/activity/actor relationships into:

```text
RegulatoryJurisdictionBinding[]
```

using the legal topology from ADR-REG-0007.

---

# 104. Jurisdiction Resolution Is Domain Logic

Control Plane provides canonical jurisdiction references/context.

Regulations determines:

```text
which jurisdiction role matters
for the legal rule.
```

---

# 105. Example

Control Plane knows:

```text
UG

ZA.
```

Regulations determines:

```text
UG = export jurisdiction

ZA = import jurisdiction.
```

---

# 106. Stage 6 — Regulatory Regime Resolution

Determine candidate regimes based on:

```text
jurisdictions

effective membership

activity

product

trade-lane facts

requested treatment.
```

---

# 107. Regime Resolution Outcome

Potential:

```text
APPLICABLE

POTENTIALLY_APPLICABLE

NOT_APPLICABLE

QUALIFICATION_REQUIRED

INDETERMINATE.
```

---

# 108. Stage 7 — Classification Resolution

Resolve required classification dimensions.

Possible:

```text
HS

tax classification

SPS category

hazard classification

data category

industry classification.
```

---

# 109. Multiple Classifications

A rule MAY depend on more than one taxonomy.

BRIR SHALL not assume one universal:

```text
classification_code.
```

---

# 110. Stage 8 — Temporal Resolution

Determine:

```text
legal_time

knowledge_time

rule-specific regulated-event times.
```

---

# 111. Stage 9 — Candidate Rule Selection

Candidate rules SHALL be selected through deterministic indexed scope matching.

Examples:

```text
jurisdiction

regime

domain

activity

actor role

classification

time.
```

---

# 112. Candidate Selection Is Not Applicability

A candidate rule still needs BRIR evaluation.

---

# 113. Qdrant SHALL NOT Select Transactional RuleSet

For high-assurance runtime:

```text
vector similarity
```

SHALL NOT determine candidate legal rules.

---

# 114. Why

Vector retrieval is:

```text
probabilistic
```

while rule candidate selection must be:

```text
complete for the declared regulatory scope.
```

---

# 115. PostgreSQL Rule Indexes

Candidate RuleSet selection SHOULD initially use canonical structured data and PostgreSQL indexes over:

```text
jurisdiction

regime

activity

classification

legal time

status.
```

---

# 116. Search Has a Different Purpose

Haystack/Qdrant remain valuable for:

```text
regulatory research

authoring

interpretation support

explanation

change investigation.
```

---

# 117. Stage 10 — Applicability Evaluation

For each candidate RuleVersion, evaluate BRIR applicability predicates.

---

# 118. Applicability Input

Input SHOULD use a typed:

```text
RegulatoryEvaluationContext
```

derived from the immutable ContextSnapshot.

---

# 119. Applicability Result

Per rule:

```text
APPLIES

DOES_NOT_APPLY

POTENTIALLY_APPLIES

INDETERMINATE

ERROR.
```

---

# 120. POTENTIALLY_APPLIES

Useful when:

```text
known facts suggest relevance
but required qualifying fact
is unresolved.
```

---

# 121. UNKNOWN Does Not Mean Does Not Apply

If:

```text
classification unknown
```

then:

```text
DOES_NOT_APPLY
```

is often unsafe.

---

# 122. Stage 11 — Exceptions

Explicit exceptions SHALL be evaluated after the base applicability/condition path appropriate to BRIR semantics.

---

# 123. Exception Result

Potential:

```text
NOT_TRIGGERED

TRIGGERED

INDETERMINATE.
```

---

# 124. Exemption Fact

A verified exemption MAY cause:

```text
EXEMPTED.
```

---

# 125. Claimed Exemption

A customer claim:

```text
"We are exempt"
```

without verified legal basis/evidence SHALL NOT create `EXEMPTED`.

---

# 126. Stage 12 — Legal Hierarchy

Applicable rules may:

```text
coexist

overlap

conflict

override.
```

ADR-REG-0007 governs resolution.

---

# 127. Cumulative Rules

If:

```text
export licence required
```

and:

```text
SPS certificate required
```

both apply:

```text
both obligations survive.
```

---

# 128. No Winner Needed for Non-Conflict

Do not force every set of rules into:

```text
one winning rule.
```

---

# 129. Conflict

Example:

```text
Rule A:
prohibits action X

Rule B:
expressly permits X under Condition C.
```

Conflict/override resolution follows verified legal topology.

---

# 130. Unresolved Conflict

Result:

```text
APPLICABILITY_CONFLICT
+
REVIEW_REQUIRED.
```

---

# 131. Stage 13 — Applicable RuleSet Snapshot

Final resolution produces an immutable:

# `ApplicableRuleSetSnapshot`

---

# 132. ApplicableRuleSetSnapshot

Conceptually:

```text
ApplicableRuleSetSnapshot
├── ruleset_snapshot_id
├── regulatory_context_snapshot_ref
├── legal_time
├── knowledge_time
├── considered_rule_versions[]
├── applicable_rule_versions[]
├── non_applicable_rule_versions[]
├── defeated_rule_versions[]
├── exempted_rule_versions[]
├── indeterminate_rule_versions[]
├── unresolved_conflicts[]
├── resolution_policy_version
├── fingerprint
├── resolved_at
└── provenance
```

---

# 133. Considered Rules Matter

Historical replay SHOULD know:

```text
what was considered
```

not only:

```text
what applied.
```

---

# 134. Why

A future audit may ask:

> Why was Rule R not applied?

Answer:

```text
considered

scope matched

exception triggered.
```

is much stronger than:

```text
not present.
```

---

# 135. Rule Exclusion Reasons

Examples:

```text
WRONG_JURISDICTION

WRONG_ACTIVITY

OUTSIDE_VALID_TIME

ACTOR_ROLE_MISMATCH

CLASSIFICATION_MISMATCH

REGIME_NOT_APPLICABLE

EXCEPTION_TRIGGERED

SUPERSEDED

OVERRIDDEN.
```

---

# 136. RuleSet Fingerprint

The ApplicableRuleSetSnapshot SHALL have a deterministic fingerprint used by:

```text
assessment

decision

historical replay.
```

---

# 137. RuleSet Snapshot Is Immutable

Once used for a consequential assessment:

```text
do not mutate it.
```

---

# 138. Context Snapshot Is Immutable

Same rule.

If the transaction changes:

```text
create new context snapshot
+
new assessment.
```

---

# 139. ApplicabilityResolution

The process itself SHOULD produce:

```text
ApplicabilityResolution
```

with detailed outcomes.

---

# 140. ApplicabilityResolution Object

Conceptually:

```text
ApplicabilityResolution
├── resolution_id
├── context_snapshot_ref
├── candidate_ruleset_ref
├── applicable_ruleset_ref
├── jurisdiction_resolution
├── regime_resolution
├── classification_resolution
├── activity_resolution
├── actor_resolution
├── temporal_resolution
├── conflicts[]
├── unknowns[]
├── warnings[]
├── result
├── resolver_version
└── provenance
```

---

# 141. Overall Resolution Result

Possible:

```text
RESOLVED

RESOLVED_WITH_GAPS

REVIEW_REQUIRED

INDETERMINATE

FAILED.
```

---

# 142. RESOLVED_WITH_GAPS

May be appropriate for advisory assessments where:

```text
non-material facts
```

remain unresolved.

---

# 143. Materiality

ADR-REG-0018 SHALL determine whether unresolved applicability gaps are material to the final decision.

---

# 144. Context Completeness

`RegulatoryContextSnapshot` SHOULD expose:

```text
COMPLETE_FOR_PURPOSE

PARTIAL

INSUFFICIENT

CONFLICTING.
```

---

# 145. Purpose-Specific Completeness

A context may be complete for:

```text
basic product prohibition screening
```

but insufficient for:

```text
landed-duty calculation.
```

---

# 146. Assessment Purpose

The request SHALL identify a regulatory purpose/profile.

Examples:

```text
CROSS_BORDER_IMPORT_READINESS

EXPORT_READINESS

PRODUCT_MARKET_ACCESS

DOCUMENT_REQUIREMENTS

TARIFF_ASSESSMENT

SUPPLIER_REGULATORY_READINESS.
```

---

# 147. RegulatoryProfile

From ADR-REG-0006:

```text
RegulatoryProfile
```

is a compositional set of regulatory domains/capabilities.

---

# 148. Profile Is Not Jurisdiction

Example:

```text
CrossBorderGoodsProfile
```

may operate over:

```text
UG → ZA

KE → ZA

ZA → UG.
```

---

# 149. Profile Drives Required Context

Example:

```text
TariffAssessment
```

may require:

```text
classification

origin

customs value

import date.
```

---

# 150. Context Requirement Contract

Each RegulatoryProfile SHOULD declare:

```text
required facts

optional facts

conditional facts.
```

---

# 151. Example

```text
CrossBorderGoodsProfile
├── seller
├── exporter
├── importer
├── origin
├── export jurisdiction
├── import jurisdiction
├── product classification
├── transaction value
├── regulated event date
└── route if transit-sensitive.
```

---

# 152. Missing Required Context

Result:

```text
CONTEXT_INCOMPLETE.
```

---

# 153. No Guessing

The resolver SHALL not guess:

```text
importer

jurisdiction

classification

origin

legal entity.
```

---

# 154. Default Values

Defaults MAY be used only where they are:

```text
architectural defaults

jurisdiction policy defaults

or source-backed legal defaults.
```

They SHALL be explicit.

---

# 155. User Preference Is Not Legal Default

A tenant configuration cannot redefine:

```text
country of origin
```

or:

```text
applicable law
```

arbitrarily.

---

# 156. Tenant Regulatory Overlay

Tenants MAY have:

```text
counsel interpretations

risk policies

additional internal controls.
```

These SHALL be overlay layers, not mutations of public law.

---

# 157. Overlay Resolution

Conceptually:

```text
Shared Regulatory RuleSet
          +
Tenant Legal Overlay
          +
Tenant Internal Control Policy
```

but these categories SHALL remain distinguishable.

---

# 158. Internal Policy Is Not Regulation

Example:

```text
company policy requires
two approvals for shipments
over X.
```

That is not:

```text
external regulatory obligation.
```

---

# 159. OPA Boundary

OPA may ultimately evaluate:

```text
applicability predicates

conditions

exceptions
```

compiled from BRIR.

---

# 160. OPA SHALL Consume Resolved Context

OPA SHALL NOT be responsible for discovering:

```text
which legal entity?

which jurisdiction?

which shipment?

which market?
```

from arbitrary request data.

---

# 161. Correct OPA Input

```text
RegulatoryEvaluationInput
      │
      ├── canonical context
      ├── resolved actors
      ├── resolved jurisdictions
      ├── typed facts
      └── temporal parameters
```

---

# 162. Wrong OPA Input

Rejected:

```json
{
  "country": "South Africa",
  "company": "Zuribeans",
  "stuff": {}
}
```

with Rego expected to reconstruct all platform semantics.

---

# 163. Context Version

The context contract SHALL be explicitly versioned.

---

# 164. Resolver Version

`ApplicabilityResolution` SHOULD record:

```text
resolver_version.
```

---

# 165. Platform Context Version

It SHOULD also preserve:

```text
platform_context_version
```

or equivalent assertion identity.

---

# 166. Historical Replay

Historical applicability requires:

```text
historical context snapshot

historical ruleset

historical legal time

historical knowledge time.
```

---

# 167. Do Not Re-Resolve Old Context Blindly

Current Control Plane state may differ from historical state.

Therefore historical replay SHOULD ordinarily use the persisted historical ContextSnapshot.

---

# 168. Example

Today:

```text
LegalEntity A is inactive.
```

Two years ago:

```text
LegalEntity A was active
and was importer.
```

Historical decision replay needs the old context.

---

# 169. Future Planning Context

Future assessments MAY use:

```text
planned shipment

planned route

future effective law.
```

The snapshot SHALL explicitly classify planning facts.

---

# 170. Planning Assessment

Result SHOULD identify:

```text
BASED_ON_PLANNED_CONTEXT.
```

It SHALL not imply:

```text
final regulatory clearance.
```

---

# 171. Context Confidence

Baobab SHALL NOT use a single opaque:

```text
context_confidence = 82%.
```

---

# 172. Fact-Level Assurance

Instead track:

```text
importer = VERIFIED

origin = PROVISIONAL

classification = REVIEWED

transit route = PLANNED.
```

---

# 173. Context Conflict

If two authoritative providers disagree:

```text
CONTEXT_CONFLICT.
```

---

# 174. Example

Trade says:

```text
Importer = Entity A.
```

Customs declaration says:

```text
Importer = Entity B.
```

Do not silently prefer one unless governed precedence establishes which is authoritative for that fact.

---

# 175. Fact Authority Registry

Regulations SHOULD know which engine/source is authoritative for which fact category.

Example:

```text
tenant/legal entity
    Control Plane

order/shipment state
    Trade

accounting document
    ERP

identity
    IAM

regulatory source
    Regulations.
```

---

# 176. Domain Authority ≠ Legal Authority

Trade being authoritative for:

```text
shipment destination
```

does not make Trade:

```text
legal authority for customs law.
```

---

# 177. Canonical References

Regulations SHALL use canonical identifiers rather than free-text entity names where possible.

---

# 178. ExternalReference

External provider identifiers SHALL follow Shared mapping semantics rather than becoming context identity.

---

# 179. Cross-Tenant Isolation

A canonical object belonging to Tenant A SHALL never be admitted into Tenant B's RegulatoryContextSnapshot unless an explicitly governed cross-tenant relationship permits it.

---

# 180. Subsidiaries

An external customer may contain:

```text
ParentCo

Subsidiary A

Subsidiary B.
```

Regulations SHALL assess the actual legal entity and transaction roles rather than applying regulation at customer-account level.

---

# 181. Group Relationship

Corporate-group membership MAY matter where laws include:

```text
related-party

group turnover

affiliate

beneficial ownership
```

rules.

These SHALL be explicit legal facts.

---

# 182. Group Does Not Merge Legal Persons

Rejected:

```text
same corporate group
⇒
same legal entity.
```

---

# 183. Legal Presence

A legal entity may operate commercially in a market without:

```text
incorporated subsidiary
```

there.

Control Plane MarketParticipation already distinguishes activities such as:

```text
LEGAL_PRESENCE
```

from other market capabilities.

Regulations SHALL preserve this distinction.

---

# 184. Market Presence ≠ Legal Presence

A digital estate serving South Africa does not prove:

```text
legal establishment in South Africa.
```

---

# 185. Establishment Facts

Rules may depend on:

```text
incorporation

branch

permanent establishment

registered office

local representative.
```

These SHALL be explicit.

---

# 186. Jurisdiction Candidate Resolver

The resolver SHOULD construct candidates from:

```text
actor establishment

transaction geography

regulated activity

asset/location

trade lane

regime membership

legal source scope.
```

---

# 187. Candidate Jurisdiction Does Not Mean Applies

Example:

```text
ZA candidate
```

still requires rule-level applicability evaluation.

---

# 188. Subject-Matter Jurisdiction

Authority may have competence over:

```text
customs

tax

food safety

employment

privacy.
```

even within the same geography.

ADR-REG-0007 competence semantics SHALL participate in candidate-rule validation.

---

# 189. Rule Issued Outside Authority Competence

If source/rule mapping conflicts with authority competence:

```text
REGULATORY_KNOWLEDGE_ERROR
```

or review is required.

Applicability shall not make an invalid authority relationship valid.

---

# 190. Rule Status Gate

Only governed rule states SHOULD enter production candidate RuleSets:

```text
PUBLISHED
```

and relevant future-effective verified states.

---

# 191. Suspended Rule

A suspended RuleVersion SHALL not ordinarily produce current effects.

---

# 192. Superseded Rule

A superseded RuleVersion may still be relevant to:

```text
historical transactions

grandfathering

savings provisions.
```

---

# 193. Draft Rule

A draft SHALL not enter binding production applicability.

---

# 194. Scenario Mode

Scenario evaluation MAY deliberately include:

```text
DRAFT
```

or:

```text
PROPOSED
```

RuleVersions.

The output SHALL clearly state:

```text
NON_BINDING_SCENARIO.
```

---

# 195. Applicability Index

Regulations SHOULD maintain structured indexes for:

```text
jurisdiction

regime

activity

actor role

subject

classification

valid time

rule status.
```

---

# 196. Index Is Derived

An applicability index can be rebuilt from canonical RuleVersion/BRIR metadata.

---

# 197. Qdrant Separation Again

Qdrant may index:

```text
rule text

explanation

concepts.
```

It SHALL not be the applicability index for E3/E4 decisions.

---

# 198. RuleSet Resolution Cache

Applicable/candidate RuleSet resolution MAY be cached.

---

# 199. Cache Key

A safe key may include:

```text
tenant scope if overlay relevant

legal entity

regulated activities

jurisdiction set

regime set

classification set

legal time

knowledge version

regulatory profile

ruleset generation/version.
```

---

# 200. Context Facts May Make Cache Unsafe

Transaction-specific:

```text
quantity

value

permit status
```

may affect applicability.

Therefore candidate-rule caching and complete applicability-result caching SHOULD be distinguished.

---

# 201. Candidate Rule Cache

Broad candidate RuleSet selection may be highly reusable.

---

# 202. Applicability Result Cache

Specific applicability result is tied much more closely to:

```text
context snapshot fingerprint.
```

---

# 203. No Stale Rule Cache Across Legal Boundary

ADR-REG-0015 applies.

Crossing:

```text
effective date
```

must not leave stale applicability results active.

---

# 204. Resolution Readiness

Applicability resolution SHALL depend on regulatory capability readiness.

Examples:

```text
rule corpus current

required jurisdiction pack active

classification service available

compiled rules ready.
```

---

# 205. Missing Jurisdiction Pack

If a requested regulatory domain/jurisdiction is not covered:

```text
COVERAGE_UNAVAILABLE
```

not:

```text
NO_REGULATION_APPLIES.
```

---

# 206. This Distinction Is Critical

No rule found can mean:

```text
no applicable law
```

or:

```text
Baobab lacks coverage.
```

These SHALL never be confused.

---

# 207. Coverage Assertion

Each resolution SHOULD know:

```text
coverage status
```

for the requested profile/jurisdiction/time.

---

# 208. Coverage Outcomes

Potential:

```text
COMPLETE_FOR_DECLARED_SCOPE

PARTIAL

UNAVAILABLE

UNKNOWN.
```

---

# 209. No-Rules Outcome

`NO_APPLICABLE_RULES` MAY only be returned where:

```text
coverage sufficient
+
candidate universe checked
+
rules evaluated
```

supports that result.

---

# 210. Otherwise

Use:

```text
INDETERMINATE

COVERAGE_INCOMPLETE.
```

---

# 211. Completeness Before E4

E4 decisions SHALL require sufficient coverage of the relevant regulatory profile.

---

# 212. Applicable RuleSet Cannot Be More Trustworthy Than Coverage

A beautifully evaluated rule set is insufficient if half the applicable legal domain is missing.

---

# 213. Rule Materiality

Not every applicable rule is material to every decision question.

Example:

```text
record-retention requirement
```

may apply generally but not determine:

```text
may shipment depart now?
```

---

# 214. Decision Question

The assessment SHALL therefore carry a:

```text
RegulatoryQuestion
```

or purpose.

---

# 215. Example Questions

```text
MAY_TRANSACTION_PROCEED?

WHAT_REQUIREMENTS_APPLY?

WHAT_DOCUMENTS_ARE_REQUIRED?

WHAT_DUTY_IS_DUE?

WHAT_REGULATORY_RISKS_REMAIN?
```

---

# 216. Same Context, Different RuleSet Projection

The underlying applicable regulatory universe may be the same.

The material subset can differ by question.

---

# 217. No Premature Rule Exclusion

Materiality filtering must not remove a rule needed to establish:

```text
an exception

definition

dependency

hierarchy relationship.
```

---

# 218. Dependency Closure

Candidate RuleSet SHALL include required transitive dependencies.

---

# 219. Example

```text
Rule R:
permit required for "regulated agricultural product."

Definition Rule D:
defines regulated agricultural product.
```

Selecting R requires D.

---

# 220. Dependency Closure Algorithm

Conceptually:

```text
candidate primary rules
      ↓
follow DEPENDS_ON /
DEFINES_TERM_FOR /
EXCEPTED_BY /
override relationships
      ↓
closed executable RuleSet.
```

---

# 221. Dependency Cycle

Unexpected cycle:

```text
RULESET_INVALID
```

unless BRIR explicitly supports the semantics.

---

# 222. Cross-Domain Dependencies

A customs rule may depend on:

```text
SPS classification

origin determination

licence status.
```

Profiles SHALL permit cross-domain dependency resolution.

---

# 223. No Monolithic Compliance RuleSet

Baobab SHOULD compose:

```text
Customs

SPS

Tax

Trade Controls

Documentation
```

profiles rather than create one universal:

```text
all laws everywhere
```

RuleSet.

---

# 224. Evaluation Cost

Scope filtering before OPA protects:

```text
latency

memory

audit clarity.
```

---

# 225. But Scope Filtering Must Be Complete

Performance optimisation SHALL not create false negatives.

---

# 226. Applicability Resolution API

Potential:

```text
POST /regulatory-applicability/resolve
```

Input:

```text
regulatory profile

canonical context reference

subject reference

assessment purpose

legal time

knowledge time.
```

---

# 227. Output

```text
context snapshot ID

applicable ruleset snapshot ID

jurisdictions

regimes

coverage

unknowns

conflicts

resolution result.
```

---

# 228. Consumer API Should Not Expose Internal OPA

External consumers SHALL not be required to know:

```text
OPA package

Rego entrypoint

bundle revision
```

to request applicability.

---

# 229. Decision Architecture

The full runtime becomes:

```text
Consumer
   │
   ▼
Control Plane
   │
   ▼
Capability + Context Resolution
   │
   ▼
Regulations
   │
   ▼
RegulatoryContextSnapshot
   │
   ▼
Applicability Resolver
   │
   ▼
ApplicableRuleSetSnapshot
   │
   ▼
OPA / deterministic evaluator
   │
   ▼
RuleEvaluationResults
   │
   ▼
ADR-REG-0018 Decision Engine
```

---

# 230. Control Plane SHALL NOT Proxy Every Business Request

Consistent with BCP-007:

```text
consumer resolves provider/context
```

and invokes Regulations.

The Control Plane need not sit in the business data path for every rule evaluation.

---

# 231. Context Assertion Caching

Validated CP context assertions MAY be cached within bounded validity.

---

# 232. Revocation

If Control Plane context or entitlement is revoked:

```text
cached context must not live indefinitely.
```

---

# 233. Applicability and Authorization Ordering

A typical call:

```text
1 Authenticate principal.

2 Resolve capability/provider/context.

3 Authorize service request.

4 Resolve regulatory applicability.

5 Evaluate regulation.
```

---

# 234. Authorization Is Not Applicability Again

A user authorized to ask:

```text
"What rules apply?"
```

does not control the answer.

---

# 235. User Cannot Select Provider Internals

Caller SHALL NOT specify:

```text
OPA instance

Rego package

regulatory source provider
```

for ordinary evaluation.

---

# 236. User May Select Legitimate Assessment Parameters

Examples:

```text
planned shipment date

requested trade regime

scenario mode

assessment profile.
```

Those remain facts/request semantics, not infrastructure selection.

---

# 237. Cross-Border Example — ZuriBeans

Synthetic context:

```text
Tenant:
ZuriBeans

Legal entity:
ZuriBeans Uganda Ltd

Activity:
EXPORT + SALE

Product:
green coffee

Origin:
Uganda

Destination:
South Africa

Exporter:
ZuriBeans Uganda Ltd

Importer:
South African buyer

Regulated event:
planned customs entry 2027-01-05.
```

---

# 238. Candidate Jurisdictions

Potential:

```text
Uganda
    export/control jurisdiction

South Africa
    import/destination jurisdiction

regional regimes
    where qualifying.
```

---

# 239. Candidate Regulatory Domains

Potential:

```text
customs

export controls

SPS

plant health

rules of origin

import controls

tax/VAT

trade documentation.
```

---

# 240. Candidate Rule Scope Filtering

Using:

```text
UG export

ZA import

coffee classification

activity

future legal time.
```

---

# 241. Rule Applicability

Each candidate is then deterministically evaluated.

---

# 242. Requirements Produced

Potential synthetic output:

```text
export requirement A

certificate B

import declaration C

origin requirement D

tariff calculation E.
```

Actual production requirements SHALL be sourced from verified law.

---

# 243. Domestic B2B Example

Baobab customer sells goods entirely inside one country.

Context may contain:

```text
origin market = ZA

destination market = ZA

no cross-border import/export.
```

Cross-border rules SHALL not activate merely because the tenant also operates internationally.

---

# 244. External Customer With Subsidiaries

```text
Client X

Subsidiary Kenya

Subsidiary Tanzania
```

Transaction:

```text
Kenya subsidiary sells to external customer.
```

Rules attach to:

```text
actual legal actors/activities
```

not parent platform account.

---

# 245. Thamani Example

Because Thamani operates logistics/shipping across B2B and B2C contexts, Regulations may see roles such as:

```text
carrier

freight operator

seller

fulfilment provider

possibly importer/exporter depending transaction.
```

These roles must be resolved per transaction rather than hard-coded from business model.

---

# 246. Marketplace / Platform Example

A future platform client MAY facilitate transactions without becoming:

```text
seller

importer

exporter.
```

Applicability resolution SHALL distinguish:

```text
platform operator

merchant

customer

carrier.
```

---

# 247. Physical Location versus Legal Role

A warehouse in country X may create:

```text
storage obligations
```

without making the warehouse operator:

```text
importer.
```

---

# 248. Digital Context

For privacy/data regulation:

```text
data subject jurisdiction

controller establishment

processor location

processing location

transfer destination
```

may replace trade geography.

The same architecture SHALL generalise.

---

# 249. Context Model Must Therefore Be Extensible

Do not design RegulatoryContext exclusively around:

```text
shipment.
```

---

# 250. Regulated Activity Families

Potential domain families:

```text
TRADE

TAX

EMPLOYMENT

DATA

FINANCIAL

ENVIRONMENT

PRODUCT

LICENSING.
```

---

# 251. Domain-Specific Context Extensions

A profile MAY attach a typed extension such as:

```text
CrossBorderGoodsContext

EmploymentContext

DataProcessingContext.
```

---

# 252. Extension SHALL Not Replace Core Context

All extensions still retain:

```text
tenant

legal entity

jurisdiction

time

actors

provenance.
```

---

# 253. No Generic JSON Dump

Rejected:

```text
context: {
  "whatever": "anything"
}
```

for canonical applicability.

---

# 254. Extension Registration

Context extensions SHOULD be:

```text
schema-versioned

named

validated.
```

---

# 255. Fact Namespace

Facts SHOULD use controlled namespaces.

Example:

```text
trade.shipment.destination

trade.product.hs_code

organisation.entity.incorporation_jurisdiction

regulatory.permit.status.
```

Exact naming belongs to technical specification.

---

# 256. Fact Collisions

Do not allow:

```text
country
```

to mean:

```text
origin
```

in one rule and:

```text
destination
```

in another.

---

# 257. Strong Typing

Applicability facts SHOULD have typed definitions.

---

# 258. Fact Source

Fact schema SHOULD identify authoritative fact-provider capability.

---

# 259. Derived Fact

Derived facts SHOULD identify their producing BRIR rule.

---

# 260. Circular Fact Derivation

A circular fact dependency SHALL fail ruleset validation unless supported formally.

---

# 261. Context Provenance

Each context component SHOULD state:

```text
resolved from

provided by

derived by

verified by.
```

---

# 262. Caller-Claimed Fact

A caller-supplied value SHOULD be marked:

```text
CLAIMED
```

until verified if the fact requires assurance.

---

# 263. Planning Fact

Future transaction parameters MAY be marked:

```text
PLANNED.
```

---

# 264. Verified Fact

A fact established from authoritative platform/master data MAY be:

```text
CANONICAL
```

or equivalent.

---

# 265. Regulatory Fact

A legal conclusion derived by Regulations may be:

```text
REGULATORY_DERIVED.
```

---

# 266. No Universal Confidence Score

Again:

```text
context_score = 95
```

is rejected.

---

# 267. Applicability Trace

Every resolution SHOULD support:

```text
Rule R considered.

Jurisdiction matched.

Activity matched.

Actor role matched.

Classification matched.

Temporal scope matched.

Exception not triggered.

Therefore APPLIES.
```

---

# 268. Non-Applicability Trace

Likewise:

```text
Rule R considered.

Export jurisdiction required ZA.

Resolved export jurisdiction UG.

Therefore DOES_NOT_APPLY.
```

---

# 269. Unknown Trace

```text
Rule R considered.

Requires HS classification.

Classification unresolved.

Therefore INDETERMINATE.
```

---

# 270. Explanation Shall Use Structured Trace

Do not depend on LLM reasoning to explain applicability.

---

# 271. AI Explanation

AI MAY transform structured trace into clearer prose.

The underlying trace remains authoritative.

---

# 272. Applicability Error Taxonomy

Initial reason codes SHOULD include:

```text
CONTEXT_UNRESOLVED

TENANT_MISMATCH

LEGAL_ENTITY_UNRESOLVED

ACTOR_ROLE_UNKNOWN

ACTIVITY_UNKNOWN

JURISDICTION_UNKNOWN

JURISDICTION_CONFLICT

REGIME_QUALIFICATION_UNKNOWN

CLASSIFICATION_UNKNOWN

SUBJECT_SCOPE_UNKNOWN

LEGAL_TIME_UNKNOWN

COVERAGE_INCOMPLETE

RULE_CONFLICT

DEPENDENCY_UNRESOLVED

FACT_PROVIDER_UNAVAILABLE

INVALID_CONTEXT.
```

---

# 273. Missing Provider

If Trade/ERP/another source engine cannot provide a required fact:

```text
DEPENDENCY_UNAVAILABLE.
```

Not:

```text
fact = false.
```

---

# 274. Context Provider Availability

Applicability readiness may depend on upstream engine health.

---

# 275. Graceful Degradation

For advisory contexts:

```text
partial resolution
```

may still be useful.

---

# 276. High-Assurance Fail-Closed

For E3/E4:

```text
material context unresolved
```

SHALL prevent automated consequential enforcement.

---

# 277. Applicability Assurance

A resolved rule MAY carry:

```text
applicability_assurance
```

as structured dimensions, not one score.

Potential dimensions:

```text
context complete

jurisdiction verified

classification verified

temporal certainty

rule provenance

conflict resolved.
```

---

# 278. E4 Applicability Gate

Before a rule may contribute to E4:

```text
canonical tenant/legal entity resolved

actors resolved

jurisdictions resolved

activity resolved

required classification resolved

legal time determined

coverage sufficient

rule published/verified

exceptions resolved

conflicts resolved.
```

---

# 279. Applicability Does Not Determine Enforcement Alone

Rule applies:

```text
APPLIES
```

does not automatically mean:

```text
BLOCK TRANSACTION.
```

ADR-REG-0004 and ADR-REG-0018 determine outcome and operational disposition.

---

# 280. Example

Applicable rule produces:

```text
certificate required.
```

Certificate missing.

Possible assessment:

```text
UNSATISFIED
```

with disposition:

```text
REMEDIATE / REVIEW / HOLD
```

rather than generic:

```text
PROHIBITED.
```

---

# 281. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-APP-I01` | Market SHALL remain distinct from jurisdiction |
| `REG-APP-I02` | Tenant SHALL remain distinct from legal entity |
| `REG-APP-I03` | Organisation SHALL remain distinct from regulated legal actor |
| `REG-APP-I04` | Trade Lane SHALL remain distinct from regulatory regime |
| `REG-APP-I05` | Capability entitlement SHALL remain distinct from regulatory applicability |
| `REG-APP-I06` | Platform context SHALL be resolved, not trusted from caller claims |
| `REG-APP-I07` | RegulatoryContextSnapshot SHALL not duplicate master data ownership |
| `REG-APP-I08` | Transaction geography SHALL be role-qualified |
| `REG-APP-I09` | Multi-jurisdiction context SHALL be first-class |
| `REG-APP-I10` | Market participation SHALL not prove transaction activity |
| `REG-APP-I11` | Requested trade regime SHALL not prove regime qualification |
| `REG-APP-I12` | Product identity SHALL remain distinct from regulatory classification |
| `REG-APP-I13` | Unknown classification SHALL not become non-applicability |
| `REG-APP-I14` | Qdrant semantic similarity SHALL not determine transactional applicability |
| `REG-APP-I15` | Candidate rule selection SHALL use deterministic canonical scope |
| `REG-APP-I16` | Scope matching SHALL remain distinct from BRIR applicability evaluation |
| `REG-APP-I17` | Exceptions and exemptions SHALL remain explicit |
| `REG-APP-I18` | Missing facts SHALL not automatically become negative facts |
| `REG-APP-I19` | Legal hierarchy SHALL resolve conflicts, not arbitrary rule order |
| `REG-APP-I20` | Applicable RuleSet snapshots SHALL be immutable |
| `REG-APP-I21` | Historical replay SHALL use historical context snapshots |
| `REG-APP-I22` | Future planning facts SHALL be visibly distinguishable from actual facts |
| `REG-APP-I23` | Coverage gaps SHALL not be interpreted as absence of regulation |
| `REG-APP-I24` | No-applicable-rule result SHALL require adequate declared coverage |
| `REG-APP-I25` | Tenant overlays SHALL not mutate public-law rules |
| `REG-APP-I26` | OPA SHALL consume resolved context rather than reconstruct platform context |
| `REG-APP-I27` | Cross-tenant canonical references SHALL fail closed |
| `REG-APP-I28` | Applicable rule explanations SHALL derive from structured resolution traces |
| `REG-APP-I29` | High-assurance enforcement SHALL require materially complete applicability context |
| `REG-APP-I30` | Applicability shall remain provider-neutral and reproducible |

---

# 282. Rejected Alternative — Market Determines Regulation

Rejected.

---

# 283. Rejected Alternative — Country Field Determines Jurisdiction

Rejected.

Cross-border regulation is role- and activity-dependent.

---

# 284. Rejected Alternative — Tenant Determines Legal Entity

Rejected.

---

# 285. Rejected Alternative — Digital Estate Determines Law

Rejected.

The estate is a consumer context, not sovereign jurisdiction.

---

# 286. Rejected Alternative — Vector Search Determines Applicable Rules

Rejected.

---

# 287. Rejected Alternative — Ask LLM Which Laws Apply at Runtime

Rejected for consequential deterministic assessments.

---

# 288. Rejected Alternative — Apply Every Rule in Database

Rejected for:

```text
performance

explainability

correctness.
```

---

# 289. Rejected Alternative — One Country per Assessment

Rejected.

---

# 290. Rejected Alternative — One Trade Agreement per Assessment

Rejected.

Multiple regimes may coexist.

---

# 291. Rejected Alternative — "No Rule Found" Means Permitted

Rejected.

---

# 292. Rejected Alternative — Unknown Fact Means Rule Does Not Apply

Rejected.

---

# 293. Rejected Alternative — User Supplies Applicable Jurisdiction

Rejected as authoritative input.

The user MAY supply a claim/request.

Resolution remains governed.

---

# 294. Rejected Alternative — OPA Resolves Baobab Tenancy

Rejected.

---

# 295. Rejected Alternative — Regulations Copies Trade/ERP Data

Rejected.

Use canonical references and fact-provider contracts.

---

# 296. Rejected Alternative — Current Master Data for Historical Replay

Rejected.

Historical snapshots are required.

---

# 297. Minimum Implementation Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text
1. Control Plane context consumption.

2. Context assertion validation.

3. Tenant/legal-entity separation.

4. Organisation/legal-entity separation.

5. External customer with subsidiaries.

6. Cross-tenant negative case.

7. Digital Estate context without legal conflation.

8. Market/jurisdiction separation.

9. Market Participation consumption.

10. Trade Lane consumption.

11. Regulated activity resolution.

12. Multiple activities in one transaction.

13. Actor-role resolution.

14. Seller ≠ exporter.

15. Buyer ≠ importer.

16. Counterparty canonical reference.

17. Export jurisdiction.

18. Import jurisdiction.

19. Destination jurisdiction.

20. Transit jurisdiction.

21. Unknown transit.

22. Multiple simultaneous jurisdictions.

23. Regime candidate resolution.

24. Regime qualification required.

25. Temporal regime membership.

26. Product identity.

27. HS classification.

28. Classification version.

29. Unknown classification.

30. Derived classification fact.

31. Current legal-time evaluation.

32. Future legal-time evaluation.

33. Historical-as-known applicability.

34. Historical-restated applicability.

35. RuleScope filtering.

36. Candidate RuleSet.

37. Dependency closure.

38. Constitutive dependency.

39. BRIR applicability evaluation.

40. Explicit exception.

41. Verified exemption.

42. Claimed but unverified exemption.

43. Cumulative rules.

44. Explicit override.

45. Unresolved conflict.

46. ApplicableRuleSetSnapshot.

47. RuleSet fingerprint.

48. Non-applicable rule reason.

49. Indeterminate rule reason.

50. ContextSnapshot fingerprint.

51. Planning context.

52. Context conflict.

53. Coverage-complete no-rule result.

54. Coverage-incomplete no-rule case rejected.

55. Tenant counsel overlay.

56. Internal policy kept distinct from law.

57. Qdrant excluded from transactional rule selection.

58. OPA receives resolved context.

59. No OPA platform-context reconstruction.

60. E4 fails when material applicability fact unresolved.

61. Full applicability trace.

62. Historical replay with old legal-entity state.

63. Domestic single-jurisdiction transaction.

64. Cross-border multi-jurisdiction transaction.

65. External customer with corporate group.

66. Non-goods domain extension proof.
```

---

# 298. Initial Uganda → South Africa Profile

The first production-grade applicability profile SHOULD cover:

```text
LEGAL ACTORS
seller
exporter
importer
buyer
carrier where material

ACTIVITIES
sale
export
carriage
import

GEOGRAPHY
origin
export
transit
import
destination

SUBJECT
coffee / vanilla product

CLASSIFICATION
HS and other required classifications

REGIMES
verified applicable national/regional regimes

TIME
planned / actual customs event

REGULATORY DOMAINS
customs
trade controls
origin
SPS
documentation
tax where relevant.
```

---

# 299. Synthetic End-to-End Example

```text
CONTROL PLANE
──────────────────────────────
Tenant:
ZuriBeans

Legal entity:
UG Legal Entity A

Markets:
UG + ZA

Trade Lane:
UG → ZA


TRADE
──────────────────────────────
Seller:
A

Exporter:
A

Buyer:
B

Importer:
B

Product:
P

Shipment:
S

Origin:
UG

Destination:
ZA

Planned import:
2027-01-15


REGULATIONS
──────────────────────────────
Resolve activities:
SALE
EXPORT
IMPORT

Resolve jurisdictions:
UG(EXPORT)
ZA(IMPORT)

Resolve classification:
HS:X

Resolve regimes:
national + candidate regional

Resolve legal time:
2027-01-15

Select candidate rules.

Evaluate BRIR.

Resolve exceptions.

Resolve hierarchy.

Produce:
ApplicableRuleSetSnapshot.
```

---

# 300. Runtime Architecture

```text
                     DIGITAL ESTATE / ENGINE
                              │
                              ▼
                         BAOBAB CP
                  Capability + Context
                              │
                              ▼
                     REGULATIONS API
                              │
                              ▼
                  PlatformContextAssertion
                              │
                              ▼
              Regulatory Context Assembler
          ┌───────────────────┼────────────────────┐
          ▼                   ▼                    ▼
        Trade                ERP          Other Fact Providers
          │                   │                    │
          └───────────────────┼────────────────────┘
                              ▼
                 RegulatoryContextSnapshot
                              │
                              ▼
                Jurisdiction / Regime Resolver
                              │
                              ▼
                   Rule Scope Resolver
                              │
                              ▼
                   Candidate RuleSet
                              │
                              ▼
                      BRIR / OPA
                              │
                              ▼
                  Applicability Results
                              │
                              ▼
                Legal Hierarchy Resolver
                              │
                              ▼
                ApplicableRuleSetSnapshot
                              │
                              ▼
                   ADR-REG-0018
                     Decision Engine
```

---

# 301. Interaction With Pulse

Pulse MAY identify:

```text
emerging risk

new market

potential regulatory change.
```

It MAY then ask Regulations questions such as:

```text
Would this opportunity
be legally feasible?
```

Regulations resolves:

```text
actual applicability.
```

---

# 302. Pulse SHALL Not Supply Legal Applicability

Pulse findings can populate:

```text
business context

scenario assumptions

discovery signals.
```

They SHALL not dictate:

```text
applicable law.
```

---

# 303. Interaction With CMS

CMS MAY request a context-aware publishable projection such as:

```text
"What requirements currently apply
to importing Product X into ZA?"
```

Regulations SHALL produce the applicable regulatory projection.

CMS remains responsible for editorial presentation.

---

# 304. CMS Shall Not Compute Applicability

Payload content rules SHALL not become an alternative jurisdiction engine.

---

# 305. Interaction With Trade

Trade is likely to be the most frequent operational consumer.

Trade supplies:

```text
transaction facts.
```

Regulations supplies:

```text
regulatory applicability
+
requirements
+
decision.
```

---

# 306. Interaction With ERP

ERP MAY supply:

```text
legal entity/accounting references

registration facts

tax facts

invoice values
```

where authoritative.

Regulations does not own those records.

---

# 307. Interaction With IAM

IAM establishes:

```text
principal identity.
```

Control Plane establishes:

```text
principal authorization and context.
```

Regulations determines:

```text
external regulatory applicability.
```

---

# 308. Strategic Consequence

Without this ADR, Baobab Regulations would be:

```text
a sophisticated legal-rule library.
```

With this ADR, it becomes:

```text
a contextual regulatory execution engine.
```

---

# 309. Why This Is Differentiating

A database can answer:

> What regulations exist in South Africa?

A search engine can answer:

> Which documents mention coffee imports?

An LLM can attempt:

> What rules might apply?

Baobab's target is more precise:

> **For this legal entity, acting as exporter in Uganda, with this counterparty acting as importer in South Africa, for this product/classification, moving along this transaction geography on this legally relevant date, which verified regulatory rules actually apply?**

That is a fundamentally different capability.

---

# 310. Research Foundation Summary

The WCO Data Model provides a globally oriented, harmonised data framework for import, export and transit processes and explicitly models multiple actors, locations, countries, declarations and regulatory-agency data. This supports Baobab's use of role-qualified cross-border context rather than a single-country field.

WCO guidance also distinguishes concepts such as country of origin, exportation country, delivery location and other transaction locations, illustrating why origin, export, import, destination and transit must not be collapsed into one geography field.

LegalRuleML models jurisdiction as geographic or subject-matter authority and incorporates contexts and factual statements alongside legal norms, validating the separation between legal rules and the factual context against which they are evaluated.

ELI provides a structured metadata model for legislation and jurisdictional/legal-resource identification, further supporting the use of explicit legal-resource and jurisdiction metadata rather than document-location inference.

Baobab Control Plane's accepted architecture already distinguishes Tenant, Legal Entity, Organisation, Market, Jurisdiction, transaction geography, Market Participation and Trade Lane, and adopts fail-closed context and entitlement resolution. `ADR-REG-0017` intentionally consumes those boundaries rather than redefining them.

---

# 311. Final Decision

Baobab Regulations SHALL implement regulatory applicability as a **deterministic, contextual and auditable resolution process**.

The governing architecture is:

```text
                VERIFIED REGULATORY KNOWLEDGE
                            │
                            ▼
                      RuleVersion / BRIR
                            │
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
         RULE SCOPE             PLATFORM CONTEXT
                                      │
                                      ▼
                             REGULATORY CONTEXT
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
                 ACTORS           GEOGRAPHY          SUBJECT
                    │                 │                 │
                    ▼                 ▼                 ▼
                 ROLES          JURISDICTIONS    CLASSIFICATION
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      ▼
                                   REGIMES
                                      │
                                      ▼
                                  LEGAL TIME
                                      │
                                      ▼
                              CANDIDATE RULESET
                                      │
                                      ▼
                               BRIR EVALUATION
                                      │
                                      ▼
                          EXCEPTIONS / EXEMPTIONS
                                      │
                                      ▼
                           HIERARCHY / CONFLICT
                                      │
                                      ▼
                        APPLICABLE RULESET SNAPSHOT
                                      │
                                      ▼
                               DECISION ENGINE
```

The core distinctions are:

```text
Tenant
≠
Legal Entity

Market
≠
Jurisdiction

Trade Lane
≠
Trade Regime

Market Participation
≠
Actual Regulated Activity

Product
≠
Classification

Destination
≠
Import Jurisdiction

Seller
≠
Exporter

Buyer
≠
Importer

Requested Regime
≠
Qualified Regime

Rule Retrieval
≠
Rule Applicability

Capability Entitlement
≠
Regulatory Applicability

No Rule Found
≠
No Regulation Applies.
```

The context principle is:

> **Regulatory context SHALL be resolved, evidenced and snapshotted—not guessed.**

The jurisdiction principle is:

> **Applicability is role-qualified and multi-jurisdictional by design.**

The execution principle is:

> **Structured scope narrows the candidate rule universe; BRIR evaluates applicability; legal hierarchy resolves genuine conflicts.**

The uncertainty principle is:

> **Missing context produces explicit uncertainty, not invented non-applicability.**

The coverage principle is:

> **Baobab may conclude that no rule applies only when it has sufficient declared coverage to support that conclusion.**

The platform principle is:

> **Control Plane owns canonical platform context; domain engines own their business facts; Regulations owns the legal determination of what rules apply to those facts.**

And the strategic principle is:

> **Baobab does not ask only “what regulations exist?” It resolves “what law applies to this exact business situation?”**

That is the architecture established by `ADR-REG-0017`.

---

## Decision Summary

```text
ADR-REG-0017
────────────────────────────────────────────

CORE FUNCTION

Verified Rule
      ×
Resolved Context
      ×
Legal Time
      =
Applicable RuleSet


CONTEXT SOURCE

Control Plane
+
domain fact providers


REGULATIONS ADDS

Actor roles
Regulated activities
Jurisdiction roles
Regimes
Classification
Legal time


HARD DISTINCTIONS

Market ≠ Jurisdiction

Tenant ≠ Legal Entity

Trade Lane ≠ Regime

Product ≠ Classification

Seller ≠ Exporter

Buyer ≠ Importer

Retrieval ≠ Applicability

Entitlement ≠ Applicability


RULE SELECTION

Structured deterministic scope.

NOT:

vector similarity.


APPLICABILITY

BRIR / deterministic evaluator.


UNKNOWN

Does not become
DOES_NOT_APPLY.


COVERAGE

No rule found
does not mean
no regulation.


OUTPUT

Immutable
ApplicableRuleSetSnapshot.


OPA

Consumes resolved context.

Does not reconstruct
Baobab context.


HISTORICAL

Uses persisted
historical ContextSnapshot.


FUTURE

Supports planned context
+
known future-effective law.


PLATFORM OWNERSHIP

Control Plane:
context identity

Trade / ERP:
business facts

Regulations:
legal applicability


STRATEGIC RESULT

"For this actor,
activity,
product,
transaction,
jurisdiction,
regime,
and time—

what verified law
actually applies?"
```
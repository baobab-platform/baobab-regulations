# ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary

**Status:** Proposed  
**Decision ID:** `ADR-REG-0001`  
**Engine:** Baobab Regulations  
**Repository:** `baobab-platform/baobab-regulations`  
**Organisation:** `baobab-platform`  
**Decision Type:** Foundational Architecture Decision  
**Date:** 2026-09-27  
**Strategic Classification:** Platform Differentiator / Regulatory Infrastructure  
**Primary Capability Domain:** `regulations.*`  
**Initial Regulatory Profile:** Cross-Border Goods Regulation  
**Initial Markets/Jurisdictions:** Uganda and South Africa, with regional and supranational regimes resolved independently  
**Related Engines:** Baobab Control Plane, Baobab Pulse, Baobab Trade, Baobab ERP, Baobab IAM, Baobab CMS  
**Canonical Contract Repository:** `baobab-platform/shared`

**Relevant existing architecture**

| Existing decision / architecture | Relevance |
|---|---|
| `ADR-BCP-002` | Capability-centric platform and Digital Estate consumption |
| `ADR-BCP-003` | Capability registry, grants, bindings and resolution |
| `ADR-BCP-004` | Context, market, geography, legal-entity and Digital Estate resolution |
| `ADR-BCP-005` | Product composition, subscription and entitlement |
| `ADR-BCP-006` | Capability-provider lifecycle and engine topology |
| `ADR-BCP-007` | Capability-resolution and service-to-service contracts |
| `ADR-BCP-009` | Security, isolation, residency, revocation and failure semantics |
| `ADR-BCP-011` | Market participation and trade lanes |
| `ADR-BCP-018` | Organisation, corporate group, tenant and platform-account relationships |
| `ADR-BCP-021` | Changeset, impact analysis and controlled mutation |
| `ADR-BCP-023` | Organisation evidence, verification and trust |
| `ADR-PULSE-001` | Pulse mission, authority and system boundary |
| `ADR-PULSE-006` | Provenance, lineage and evidence architecture |
| `ADR-PULSE-007` | Temporal and bitemporal semantics |
| `ADR-PULSE-009` | Evidence reliability and intelligence confidence |
| `ADR-SHARED-007` | Canonical capability contracts and provider model |
| `ADR-SHARED-012` | Topology identifiers and external system registry |
| `ADR-SHARED-013/014` | External references and trusted mapping resolution |

---

# 1. Executive Decision

Baobab SHALL introduce **Baobab Regulations** as a first-class, independently deployable, headless platform engine responsible for **regulatory context, machine-actionable regulatory knowledge, applicability assessment, obligation determination, regulatory decision support, regulatory change impact and evidence-backed regulatory execution contracts**.

Baobab Regulations SHALL be defined as:

> **The Baobab Platform Regulatory Context and Execution Engine.**

Its purpose is not merely to answer questions about regulations.

Its purpose is to transform authoritative regulatory material into **traceable, temporally correct, context-sensitive and operationally consumable regulatory decisions** that other Baobab engines and Digital Estates can act upon.

The governing model SHALL be:

```text
AUTHORITATIVE REGULATORY SOURCE
            │
            ▼
     Source Acquisition
            │
            ▼
   Structured Representation
            │
            ▼
 Regulatory Interpretation
            │
            ▼
  Applicability Resolution
            │
            ▼
       Obligations
            │
            ▼
 Regulatory Assessment
            │
            ▼
 Explainable Decision
            │
            ▼
 Operational Enforcement
   by the owning engine
```

The architectural separation is deliberate:

```text
Law / Regulation
       ≠
Baobab representation
       ≠
Baobab interpretation
       ≠
Regulatory assessment
       ≠
Operational enforcement
```

No implementation SHALL collapse these concepts.

Baobab Regulations SHALL own the middle of this chain.

It SHALL NOT claim authority that belongs to governments, regulators, courts, treaty bodies, standards authorities or other legally competent institutions.

It SHALL NOT silently take operational ownership away from Trade, ERP, IAM, CMS, Control Plane or any other Baobab engine.

---

# 2. Strategic Context

Baobab is evolving as a platform of independently deployable engines connected by canonical contracts rather than as a single application. The established platform direction is to standardise identity, tenancy, organisation, APIs, events, audit, security and observability while allowing each specialised engine to own its internal implementation.

This ADR extends that principle to regulatory capability.

Baobab Regulations is intended to sit alongside Baobab Pulse as one of the platform's principal differentiating capabilities.

The distinction is fundamental:

```text
BAOBAB PULSE
System of Intelligence
"What is happening, what may happen,
and what should the business consider?"

BAOBAB REGULATIONS
System of Regulatory Context and Execution
"What is required, permitted, prohibited,
conditional or uncertain in this context?"
```

Pulse interprets evidence to produce intelligence.

Regulations interprets authoritative normative sources to determine regulatory consequences.

Neither replaces operational systems of record.

The platform therefore evolves toward:

```text
                         BAOBAB PLATFORM

                               │
                     BAOBAB CONTROL PLANE
                               │
                      Canonical Context
                               │
         ┌─────────────────────┼──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
     Operational           Intelligence          Regulatory
       Engines                Engine               Engine
         │                     │                      │
    ┌────┼─────┐               │                      │
    │    │     │               │                      │
 Trade ERP   CMS/IAM         Pulse               Regulations
    │    │     │               │                      │
    └────┴─────┴───────────────┼──────────────────────┘
                               │
                        Digital Estates
```

The platform's previously established architecture explicitly treats specialised systems as engines and shared contracts as the integration foundation rather than forcing them into a common implementation.

Baobab Regulations SHALL preserve that principle.

---

# 3. Why a Separate Regulatory Engine Is Necessary

Regulatory requirements affect commerce, accounting, identity, content, logistics, product eligibility, taxation, documentation, market entry and data handling.

Without a dedicated regulatory boundary, regulatory logic inevitably becomes scattered:

```text
Trade
 ├── customs conditions
 ├── origin logic
 └── permit checks

ERP
 ├── tax rules
 └── reporting obligations

CMS
 └── labelling / claims restrictions

IAM
 └── privacy / residency decisions

Pulse
 └── regulatory-change analysis

Frontend
 └── miscellaneous hard-coded market conditions
```

That produces five structural problems.

| Problem | Consequence |
|---|---|
| Duplicate interpretations | Different engines may implement the same rule differently |
| Lost provenance | Nobody can reliably explain why a rule exists |
| Temporal inconsistency | Historical transactions may be evaluated against today's rules |
| Provider lock-in | Regulatory behaviour becomes tied to whichever engine implemented it first |
| Change propagation failure | A changed regulation cannot reliably identify affected transactions, products or tenants |

The correct model is therefore:

```text
                    REGULATORY AUTHORITY
                            │
                            ▼
                  BAOBAB REGULATIONS
                            │
                     canonical decision
                            │
        ┌───────────┬───────┼──────────┬───────────┐
        ▼           ▼       ▼          ▼           ▼
      Trade        ERP     IAM        CMS         Pulse
        │           │       │          │           │
        ▼           ▼       ▼          ▼           ▼
     enforce      enforce enforce    enforce      analyse
```

---

# 4. External Research and Market Evidence

## 4.1 The underlying problem is real

The World Trade Organization's Trade Facilitation Agreement requires members to publish import, export and transit procedures, required forms, taxes and duties, classification rules, origin rules, restrictions, penalties and related information. It also encourages Single Windows and the use of information technology and international standards.

Publication, however, does not mean operational usability.

The WCO reported from the 2024 PAFTRAC Africa CEO Trade Survey that **70% of participating African business leaders reported no or low access to relevant AfCFTA information for business purposes**.

That is a strategic signal.

The African trade problem is not merely:

```text
information does not exist
```

It is frequently:

```text
information exists
+
information is fragmented
+
legal effects depend on context
+
requirements change
+
business systems cannot consume them directly
```

---

# 5. The African Cross-Border Reality

The initial Uganda–South Africa focus provides an appropriate proving ground.

Uganda's official Trade Portal shows that a first-time exporter moving an unprocessed coffee consignment worth more than USD 2,000 through Malaba may encounter a procedure containing **25 steps**, including electronic Single Window registration, exporter registration, a performance bond, coffee export licensing, sales-contract registration, coffee quality certification, certificate of origin, customs declaration, inspection and border release.

Uganda's official portal also states that coffee exporters require consignment-specific quality and origin documentation, illustrating that product, shipment and documentary requirements cannot be reduced to a single tariff lookup.

South Africa presents similar complexity on the destination side.

SARS maintains customs schedules containing duties and levies and updated Schedule 1 tariff material as recently as August 2026.

Its prohibited and restricted goods framework links tariff headings to conditions imposed by multiple government bodies and distinguishes absolute prohibitions from conditional restrictions requiring permits, certificates or other authority. SARS was publishing changes to individual tariff-heading restrictions repeatedly during July 2026.

ITAC separately administers import and export controls arising from health, environmental, safety, security, technical and international-agreement requirements.

The practical regulatory graph therefore resembles:

```text
Product
   │
   ├── HS classification
   │
   ├── country of origin
   │
   ├── export jurisdiction
   │
   ├── destination jurisdiction
   │
   ├── transit jurisdiction(s)
   │
   ├── customs regime
   │
   ├── trade agreement
   │
   ├── rules of origin
   │
   ├── SPS controls
   │
   ├── product controls
   │
   ├── permit authorities
   │
   ├── tax treatment
   │
   ├── required documents
   │
   ├── quantity/value thresholds
   │
   └── effective date
```

This is precisely the class of contextual complexity Baobab Regulations exists to resolve.

---

# 6. The Opportunity Is Not "Regulatory Search"

Baobab SHALL NOT assume that regulatory information alone is a differentiated proposition.

The market already contains capable regulatory and trade-compliance systems.

SAP Global Trade Services can perform transaction-level compliance checks, sanctioned-party screening, customs management and import/export controls; SAP explicitly supports blocking transactions that fail compliance checks.

Thomson Reuters ONESOURCE provides continuously updated global trade content across more than 220 countries and territories and offers AI-powered research with cited answers, import/export controls, rules-of-origin information and commercial-documentation requirements.

RegGenome provides machine-readable regulatory infrastructure, source-linked regulatory requirements and tools for applying structured regulatory content to compliance questions.

Originvia is already pursuing provenance, corridor-specific compliance and workflow orchestration for regulated Africa–Europe trade corridors.

Therefore the following propositions are explicitly rejected as sufficient Baobab differentiation:

```text
"We provide regulations."

"We use AI to search regulation."

"We classify regulations."

"We provide African compliance information."

"We monitor regulatory change."

"We calculate tariffs."

"We provide rules-of-origin information."
```

Each of these is useful.

None by itself is strategically sufficient.

---

# 7. Baobab's Intended Differentiation

The differentiated proposition SHALL instead be:

> **Baobab converts authoritative regulation into contextual, explainable and executable regulatory decisions inside live business operations.**

The architecture SHALL optimise for:

```text
Regulation
      +
Canonical Baobab Context
      +
Transaction Context
      +
Temporal Validity
      +
Provenance
      +
Applicability Logic
      +
Obligations
      +
Decision
      +
Operational Integration
```

The commercial concept is therefore:

> **Regulation-aware operations.**

And the engineering concept is:

> **Regulatory context and execution.**

The intended progression is:

```text
SEARCH
"What does regulation X say?"

        ↓

RELEVANCE
"Which regulations concern this activity?"

        ↓

APPLICABILITY
"Which rules apply to this exact context?"

        ↓

OBLIGATION
"What must, may or must not be done?"

        ↓

DECISION
"Can this business action proceed?"

        ↓

IMPACT
"What changes if this rule changes?"

        ↓

EXECUTION
"How should the owning engine respond?"
```

Baobab Regulations SHALL be designed primarily for the last four levels.

---

# 8. Mission

Baobab Regulations SHALL:

| Mission responsibility | Meaning |
|---|---|
| Acquire | Integrate authorised regulatory sources through controlled adapters |
| Preserve | Retain authoritative source evidence, versions and provenance |
| Structure | Represent regulatory instruments, provisions, rules and obligations canonically |
| Contextualise | Resolve rules against Baobab tenant, legal-entity, market, geography and transaction context |
| Evaluate | Determine applicability, conditions, obligations, prohibitions, exemptions and uncertainty |
| Explain | State how and why an assessment was reached |
| Reconstruct | Determine what regulatory state applied at a historical point in time |
| Detect change | Identify changed regulatory state |
| Assess impact | Determine potentially affected entities, products, transactions or capabilities |
| Publish | Expose regulatory decisions through canonical APIs and events |
| Support enforcement | Allow authorised operational engines to enforce verified decisions |
| Preserve evidence | Produce an auditable decision and evidence chain |

---

# 9. Baobab Regulations Is Not the Law

The following hierarchy SHALL be foundational:

```text
LEVEL A
Authoritative legal / regulatory source

LEVEL B
Baobab source representation

LEVEL C
Baobab structured regulatory rule

LEVEL D
Baobab interpretation

LEVEL E
Baobab applicability assessment

LEVEL F
Baobab regulatory decision

LEVEL G
Operational enforcement
```

These levels SHALL remain independently identifiable.

A Baobab rule SHALL retain links to its source.

A Baobab interpretation SHALL retain links to the rule.

A Baobab assessment SHALL retain links to all rules and context used.

A Baobab decision SHALL preserve the assessment from which it was produced.

Operational enforcement SHALL identify the decision relied upon.

The engine SHALL therefore be able to answer:

```text
Why was this action blocked?
        │
        ▼
Which assessment caused it?
        │
        ▼
Which rule was evaluated?
        │
        ▼
Which interpretation was used?
        │
        ▼
Which provision supports it?
        │
        ▼
Which authoritative source contains it?
```

---

# 10. Regulatory Authority Boundary

Baobab Regulations SHALL NOT declare itself the authoritative source of law merely because it stores or structures legal material.

Examples:

```text
SARS tariff schedule
```

Authority remains with the competent South African source.

```text
Ugandan export requirement
```

Authority remains with the competent Ugandan authority.

```text
AfCFTA rule
```

Authority remains with the relevant treaty/institutional framework and legally applicable implementation.

Baobab owns:

```text
canonical representation
source relationship
interpretation
applicability model
assessment
decision record
change-impact analysis
execution contract
```

It does not own the underlying sovereign authority.

---

# 11. Legal Advice Boundary

Baobab Regulations SHALL be designed as regulatory infrastructure and decision-support technology.

It SHALL NOT implicitly present machine interpretation as professional legal advice.

Outputs SHALL distinguish, where relevant:

```text
AUTHORITATIVE_SOURCE

VERIFIED_RULE

INTERPRETATION

AUTOMATED_ASSESSMENT

HUMAN_REVIEWED_ASSESSMENT

LEGAL_OR_REGULATORY_OPINION
```

The final category may only exist if an appropriately authorised external professional or competent authority explicitly supplies or approves it.

Product wording, APIs and user interfaces SHALL preserve this distinction.

---

# 12. System of Regulatory Context

Baobab Regulations SHALL be the Baobab system authoritative for its own regulatory domain objects.

Expected canonical entities include conceptually:

```text
RegulatorySource
RegulatoryAuthority
Jurisdiction
RegulatoryRegime
RegulatoryInstrument
RegulatoryProvision
RegulatoryRule
RegulatoryInterpretation
ApplicabilityCriterion
Obligation
Permission
Prohibition
Exemption
Condition
Requirement
RegulatoryEvidence
RegulatoryAssessment
RegulatoryDecision
RegulatoryChange
RegulatoryImpact
RegulatoryProfile
RegulatoryVerification
```

The exact canonical schema is deferred to `ADR-REG-0006` onward.

---

# 13. Regulatory Decision Does Not Mean Sovereign Decision

A canonical:

```text
RegulatoryDecision
```

means:

> the result produced by Baobab Regulations when evaluating a defined regulatory rule set against a defined context at a defined time.

It does not inherently mean:

```text
court judgment
customs ruling
tax ruling
regulator determination
binding legal opinion
```

If a competent authority provides one of these, it SHALL be represented as a distinct external authoritative artefact.

---

# 14. Normative Semantics

The architecture SHALL support, at minimum, distinction between:

```text
OBLIGATION
PERMISSION
PROHIBITION
EXEMPTION
CONDITION
REQUIREMENT
DISCRETION
DEFINITION
CLASSIFICATION
PROCEDURE
REPORTING_DUTY
DOCUMENTARY_REQUIREMENT
```

These SHALL NOT be reduced to generic Boolean rules where the source semantics are richer.

OASIS LegalRuleML already demonstrates mature modelling concepts for obligations, permissions, prohibitions, jurisdiction, temporal applicability, rule conditions and defeasibility. Baobab SHOULD learn from these semantics rather than recreate legal modelling from scratch.

This ADR does not mandate LegalRuleML as Baobab's persistence or interchange format.

The principle is:

> **Adopt mature legal semantics; do not inherit unnecessary serialization complexity.**

---

# 15. Law Is Not Always Deterministic

Baobab SHALL explicitly reject the assumption:

```text
all regulation
      =
if/then statements
```

Regulatory sources may contain:

```text
ambiguity
discretion
reasonableness tests
materiality
exceptions
cross-references
conflicting provisions
administrative interpretation
judicial interpretation
fact-specific tests
transitional provisions
undefined terms
```

The OECD's Rules-as-Code work recognises both the opportunity and limitations of machine-consumable rules, while its current 2026 Law-as-Code consultation focuses on preserving authoritative legal logic, accountability and interoperability rather than blindly translating every legal sentence into deterministic code.

Therefore:

```text
uncertainty
```

SHALL be a valid regulatory state.

The engine SHALL prefer:

```text
REVIEW_REQUIRED
```

or:

```text
INDETERMINATE
```

over invented certainty.

---

# 16. Foundational Decision Outcomes

The canonical decision vocabulary SHOULD support the following conceptual outcomes:

| Outcome | Meaning |
|---|---|
| `ALLOW` | No applicable blocking condition was identified within the evaluated rule set |
| `ALLOW_WITH_REQUIREMENTS` | Action may proceed subject to explicit obligations |
| `REVIEW_REQUIRED` | Material ambiguity, discretion or unresolved evidence requires authorised review |
| `BLOCK` | A sufficiently authoritative and enforceable prohibition prevents the proposed action |
| `INDETERMINATE` | Required context, rules or evidence are insufficient to reach a reliable result |
| `NOT_APPLICABLE` | Evaluated regulatory domain does not apply to the supplied context |

Exact decision semantics SHALL be defined in later ADRs.

---

# 17. Enforcement Boundary

Baobab Regulations SHALL ordinarily be a **Policy Decision Point**, not the operational Policy Enforcement Point.

The architectural pattern is:

```text
Operational Engine
       │
       │ regulatory context
       ▼
Baobab Regulations
       │
       │ decision
       ▼
Operational Engine
       │
       ▼
Enforcement
```

This follows the widely used PDP/PEP separation demonstrated by Open Policy Agent, where policy decision-making is decoupled from application enforcement.

Therefore:

```text
Baobab Trade
```

may block a shipment.

```text
Baobab ERP
```

may reject a posting or require additional evidence.

```text
Baobab CMS
```

may prevent publication.

```text
Baobab IAM
```

may deny an operation.

But the enforcement action belongs to the operational owner.

Baobab Regulations provides the regulatory decision and evidence supporting it.

---

# 18. No Silent Operational Mutation

Baobab Regulations SHALL NOT directly modify another engine's persistence layer.

Forbidden:

```text
Regulations
   ↓
UPDATE trade.order
```

```text
Regulations
   ↓
UPDATE erp.invoice
```

```text
Regulations
   ↓
UPDATE iam.user
```

Required:

```text
Regulations
   ↓
canonical decision / event
   ↓
owning engine
   ↓
authorised workflow
```

This preserves Baobab's existing principle that engines own their domains and integrate through contracts rather than shared databases.

---

# 19. Boundary with Baobab Control Plane

The Control Plane SHALL remain authoritative for platform context and capability resolution.

Baobab Regulations SHALL consume, not redefine:

```text
Tenant
Organisation
LegalEntity
CorporateGroup
PlatformAccount
Market
Geography
TradeLane
DigitalEstate
Engine
EngineInstance
Capability
CapabilityBinding
Context
IsolationProfile
```

Conceptually:

```text
BAOBAB CONTROL PLANE
         │
         │ resolved context
         ▼
BAOBAB REGULATIONS
         │
         │ context-specific regulatory decision
         ▼
Consuming Engine
```

The Control Plane answers:

> **Who, where, which tenant, which legal entity, which market, which capability and which provider?**

Regulations answers:

> **Given that resolved context, what regulatory rules and obligations apply?**

---

# 20. Context Is a Competitive Advantage

Standalone regulatory systems often begin with a query.

Baobab begins with platform context.

A regulatory evaluation MAY consume:

```text
tenant_id
organisation_id
legal_entity_id
market_id
digital_estate_id
origin
destination
transit_geographies
trade_lane
counterparty
product
product_classification
transaction_type
channel
currency
value
quantity
unit
effective_time
contractual_context
licence_state
evidence_state
```

Not every field will apply to every regulatory domain.

But the key architectural principle is:

```text
Regulation
      ×
Canonical Context
      =
Regulatory Applicability
```

This is one of the main reasons Baobab Regulations belongs inside Baobab rather than existing only as a standalone research product.

---

# 21. Tenant Is Not Jurisdiction

Baobab Regulations SHALL preserve the platform rule that:

```text
Tenant
≠
Legal Entity
≠
Market
≠
Jurisdiction
```

Example:

```text
Tenant:
ZuriBeans

Legal entity:
Ugandan entity

Origin:
Uganda

Customer:
South African entity

Destination:
South Africa

Transit:
potential third jurisdiction
```

The applicable regulatory graph may involve multiple regimes simultaneously.

No rule SHALL infer jurisdiction solely from tenant identity.

---

# 22. Boundary with Baobab Pulse

This boundary is strategically important.

Baobab Pulse SHALL remain the **System of Intelligence**.

Baobab Regulations SHALL become the **System of Regulatory Context and Execution**.

The separation is:

| Question | Authoritative Baobab engine |
|---|---|
| What regulation was published? | Regulations for canonical regulatory state; Pulse may observe the event |
| What does the rule require? | Regulations |
| Does the rule apply to this transaction? | Regulations |
| What regulatory obligations arise? | Regulations |
| What changed? | Regulations owns regulatory change; Pulse may analyse implications |
| Which transactions are legally affected? | Regulations determines regulatory applicability; operational systems provide transaction state |
| What commercial opportunity does the change create? | Pulse |
| What demand consequences may follow? | Pulse |
| What strategic response is recommended? | Pulse |
| Should an operational action occur? | Authorised human/policy + owning operational engine |

The intended interaction is:

```text
REGULATIONS
     │
     │ regulatory change
     ▼
PULSE
     │
     │ commercial / strategic analysis
     ▼
Opportunity / Risk / Recommendation
```

and in the other direction:

```text
PULSE
     │
     │ opportunity detected
     ▼
REGULATIONS
     │
     │ feasibility / regulatory assessment
     ▼
Business Decision Support
```

---

# 23. Existing Pulse Regulatory Data

Pulse may continue to ingest regulatory publications as external observations or intelligence evidence.

However, once a regulatory artefact is promoted into:

```text
canonical regulatory instrument
canonical regulatory provision
canonical regulatory rule
obligation
regulatory assessment
regulatory decision
```

Baobab Regulations SHALL become authoritative.

Pulse SHALL reference those objects rather than maintain a competing operational regulatory truth.

This ADR therefore clarifies, rather than invalidates, the current Pulse boundary.

---

# 24. Boundary with Baobab Trade

Trade owns operational commerce and trade execution.

Depending upon its final domain implementation, Trade may own:

```text
products
commercial offers
quotations
orders
contracts
trade executions
shipments
inventory-related trade state
commercial pricing
returns
fulfilment
trade documents
```

Regulations MAY answer:

```text
May this product be sold into this market?

May this shipment proceed?

Which permit is required?

Which certificate is required?

Which origin rule applies?

Which restriction applies?

Which customs classification rules are relevant?

What regulatory evidence is missing?
```

Trade SHALL own:

```text
shipment status
order status
commercial mutation
release workflow
document attachment workflow
operational hold
```

Example:

```text
Trade shipment
      │
      ▼
RegulatoryAssessment
      │
      ▼
REVIEW_REQUIRED
      │
      ▼
Trade places regulatory hold
```

The hold is a Trade action.

The decision is a Regulations artefact.

---

# 25. Boundary with Baobab ERP

ERP remains authoritative for accounting and operational financial records.

Regulations may determine:

```text
regulatory tax treatment
reporting requirement
documentation condition
effective statutory rate
regulatory classification
```

ERP remains responsible for:

```text
journal posting
tax posting
invoice posting
general ledger
accounts payable
accounts receivable
statutory accounting records
financial periods
```

Baobab Regulations SHALL NOT become a tax ledger or shadow ERP.

---

# 26. Boundary with IAM

IAM owns authentication, identity security, sessions, credentials, MFA, authorisation mechanisms and identity lifecycle.

Regulations MAY eventually determine regulatory requirements relevant to:

```text
data residency
privacy
identity assurance
regulated access
retention
age or eligibility restrictions
segregation requirements
```

IAM enforces authorised identity/security policy.

Regulations SHALL NOT become a replacement general-purpose authorisation engine.

---

# 27. Boundary with CMS

CMS owns:

```text
content
publication state
editorial workflow
content taxonomy
digital composition
```

Regulations may provide:

```text
market-specific label restrictions
mandatory disclosures
prohibited claims
regulated-product publication restrictions
effective-date conditions
```

CMS enforces publication workflow.

Regulations SHALL NOT become a CMS.

---

# 28. Boundary with Shared

`baobab-platform/shared` SHALL remain authoritative for cross-engine canonical contracts.

Regulations-specific internals remain within `baobab-regulations`.

Contracts promoted for organisational consumption SHALL belong in `shared`.

Expected candidates include:

```text
RegulatoryContextRef
RegulatoryAssessmentRef
RegulatoryDecisionRef
RegulatoryEvidenceRef
RegulatoryOutcome
RegulatoryAssuranceLevel
RegulatoryChangeEvent
RegulatoryImpactEvent
```

The engine SHALL conform to shared:

```text
tenant identity
organisation identity
legal-entity identity
market identity
canonical references
external references
event envelope
correlation
causation
schema version
error semantics
classification
```

---

# 29. Boundary with Digital Estates

Digital Estates MAY consume regulatory capabilities.

They SHALL NOT become authoritative rule engines.

Example:

```text
ZuriBeans frontend
       │
       ▼
"Can this product ship to ZA?"
       │
       ▼
Baobab capability resolution
       │
       ▼
Baobab Regulations
       │
       ▼
Assessment
```

Leaf UI components SHALL NOT contain hidden jurisdiction logic such as:

```text
if country === "ZA" ...
```

where that condition expresses regulatory meaning.

Presentation logic is acceptable.

Regulatory truth is not frontend logic.

---

# 30. Regulatory Sources

Baobab Regulations SHALL be provider-neutral.

Source categories MAY include:

```text
government legislation
regulator notices
gazettes
customs schedules
tax authorities
trade portals
standards bodies
treaties
regional economic communities
multilateral organisations
court decisions
official rulings
licensed commercial regulatory providers
official APIs
authoritative machine-readable rule feeds
```

No single source provider SHALL become synonymous with the engine.

---

# 31. Source Adapter Boundary

Every external regulatory source SHALL enter through an anti-corruption layer.

```text
External Source
      │
      ▼
Source Adapter
      │
      ▼
Raw Acquired Artefact
      │
      ▼
Canonical Source Representation
      │
      ▼
Regulatory Interpretation
```

Never:

```text
Vendor schema
      =
Baobab regulatory domain
```

This allows a provider to be replaced without redesigning the engine.

---

# 32. Build-vs-Buy Principle

Baobab SHALL NOT attempt to manually reconstruct every global regulatory corpus.

The engine SHALL support a hybrid model:

```text
authoritative public sources
          +
licensed regulatory providers
          +
partner datasets
          +
customer-specific regulatory artefacts
          +
Baobab-derived structured rules
```

The strategic IP lies principally in:

```text
context
applicability
decision semantics
provenance
temporal state
cross-engine integration
impact analysis
execution contracts
```

not in pretending Baobab alone can collect every law on Earth.

---

# 33. Regulatory Content Rights

Public availability SHALL NOT be assumed to imply unrestricted commercial reuse.

Cambridge's Regulatory Genome Project explicitly identifies regulator website terms and reuse restrictions as a barrier to commercial regulatory applications; some public regulatory material requires express permission for commercial representation or reuse.

Therefore every regulatory source SHALL eventually carry rights metadata such as:

```text
source_owner
source_authority
access_basis
reuse_basis
licence
redistribution_rights
derivative_rights
commercial_use
attribution_requirement
retention_requirement
```

Detailed source licensing architecture is deferred to a later ADR.

But the principle is established here:

> **No ingestion pipeline may assume that "publicly visible" means "commercially exploitable."**

---

# 34. Provenance Is Mandatory

A regulatory rule without provenance SHALL NOT qualify for high-assurance automated enforcement.

The evidence chain SHOULD resemble:

```text
Authority
   │
   ▼
Instrument
   │
   ▼
Provision
   │
   ▼
Interpretation
   │
   ▼
Rule
   │
   ▼
Assessment
   │
   ▼
Decision
```

W3C PROV provides established concepts for representing entities, activities, agents and derivations so users can assess quality, reliability and trustworthiness. Baobab SHOULD align its provenance model conceptually with such mature standards.

---

# 35. Temporal Truth Is Mandatory

Baobab Regulations SHALL be designed to answer both:

```text
What applies now?
```

and:

```text
What applied at time T?
```

Regulatory data SHALL therefore not be implemented as mutable current-state records alone.

Conceptually:

```text
Rule Version 1
effective:
2026-01-01 → 2026-08-31

Rule Version 2
effective:
2026-09-01 → ...
```

Historical transactions SHALL remain reconstructable.

A later correction to source ingestion SHALL not erase what Baobab previously knew.

The detailed temporal model is deferred, but this ADR establishes temporal reconstruction as a non-negotiable requirement.

---

# 36. Publication Time Is Not Effective Time

The engine SHALL distinguish where source material permits:

```text
publication_time
retrieval_time
valid_from
valid_to
effective_from
effective_to
repealed_at
superseded_at
verified_at
```

A regulation published today may become effective later.

A regulation repealed today may still determine yesterday's transaction.

No generic:

```text
updated_at
```

field can represent this adequately.

---

# 37. Regulatory Change Is a Domain Event

Regulatory change SHALL be modelled as first-class domain state.

Conceptually:

```text
Source changed
     │
     ▼
Change detected
     │
     ▼
Change verified
     │
     ▼
Rule set updated
     │
     ▼
Affected contexts resolved
     │
     ▼
Impact published
```

Potential impact targets include:

```text
tenants
legal entities
markets
products
HS classifications
trade lanes
counterparties
open quotations
orders
shipments
contracts
documents
policies
Digital Estates
```

The owning engines remain authoritative for actual operational state.

---

# 38. Change Impact Is a Core Differentiator

Traditional alerting:

```text
New regulation
     ↓
email
```

Baobab target:

```text
New regulation
       │
       ▼
Changed canonical rules
       │
       ▼
Applicability graph
       │
       ▼
Affected Baobab contexts
       │
       ▼
Affected operational objects
       │
       ├── active products
       ├── open orders
       ├── pending shipments
       ├── suppliers
       ├── customers
       └── markets
       │
       ▼
Actionable impact
```

This capability SHALL be treated as strategic.

---

# 39. Regulation as Event Source

Baobab Regulations MAY publish:

```text
regulation.source.acquired
regulation.instrument.changed
regulation.rule.verified
regulation.rule.effective
regulation.rule.superseded
regulation.assessment.completed
regulation.decision.issued
regulation.impact.detected
```

Final canonical event names belong in Shared.

---

# 40. AI Boundary

AI SHALL be an implementation capability, not the source of legal authority.

AI MAY assist with:

```text
source discovery
document classification
OCR where necessary
provision extraction
entity extraction
cross-reference detection
candidate rule generation
classification
translation
change summarisation
similarity analysis
explanation
research assistance
```

AI SHALL NOT, by itself, grant a regulatory rule sufficient authority to block a high-impact transaction.

---

# 41. AI Explanation versus Rule Authority

The governing rule is:

> **AI may explain; sources establish; verified rules evaluate; authorised systems enforce; humans govern.**

Conceptually:

```text
LLM explanation
      │
      │ references
      ▼
RegulatoryDecision
      │
      │ produced from
      ▼
Verified Rule
      │
      │ derived from
      ▼
Authoritative Source
```

Never:

```text
LLM response
      │
      ▼
BLOCK SHIPMENT
```

without a verified rule and approved enforcement policy.

---

# 42. Confidence Is Not Authority

The engine SHALL distinguish:

```text
model confidence
source authority
rule verification
interpretation assurance
decision assurance
```

A model may be:

```text
99.9% confident
```

and still be legally wrong.

Conversely, an authoritative rule may require no probabilistic inference at all.

These concepts SHALL not share one generic `confidence` field.

---

# 43. Human Review

The platform SHALL support meaningful human review.

A reviewer SHOULD be able to inspect:

```text
question / proposed action
context
applicable jurisdiction(s)
applicable regulatory regimes
rules evaluated
source provisions
interpretation
exceptions
missing evidence
decision
assurance level
effective time
rule version
```

High-impact enforcement SHALL be capable of requiring review.

---

# 44. Regulatory Assurance

Detailed assurance levels are deferred.

However, the engine SHALL eventually distinguish at least conceptually:

```text
UNVERIFIED
EXTRACTED
MACHINE_INTERPRETED
HUMAN_REVIEWED
VERIFIED
AUTHORITY_SUPPLIED
```

A rule's permitted operational consequences MAY depend upon its assurance state.

---

# 45. Determinism Where Possible

Where a regulatory rule is explicit and sufficiently structured:

```text
verified inputs
+
verified deterministic rule
=
reproducible decision
```

SHALL be preferred over probabilistic inference.

AI SHOULD assist where interpretation is necessary.

It SHOULD NOT replace ordinary deterministic evaluation where the law is already explicit.

---

# 46. Reproducibility

A regulatory decision SHOULD be replayable.

Given:

```text
same regulatory rule versions
same context
same evidence
same interpretation version
same evaluation implementation
```

the engine SHOULD reproduce the same deterministic decision.

When a decision depends on probabilistic processing, the relevant model/provider/version and material parameters SHALL be recorded sufficiently for auditability.

---

# 47. Cross-Border Data Standards

For the initial cross-border trade profile, Baobab SHOULD align with established international trade concepts where practical.

The WCO Data Model has served as a global interoperability foundation for cross-border regulatory exchange for more than two decades and provides standardised reusable data definitions and electronic messages for customs and other border agencies.

Therefore Baobab SHOULD map compatible concepts rather than invent incompatible equivalents for:

```text
goods
consignments
declarations
parties
transport
certificates
permits
origin
customs procedures
```

where mature international semantics exist.

Baobab canonical identity remains Baobab-owned.

Interoperability semantics SHOULD use standards where useful.

---

# 48. Rules-as-Code Strategic Direction

The OECD defines Rules as Code as the creation of official machine-consumable versions of rules so computer systems may understand and act upon them consistently.

Its 2026 Law-as-Code consultation identifies a current structural problem: legal logic is repeatedly translated independently across government agencies, providers and technology systems, creating duplication, inconsistency, transparency problems and provider dependence.

Baobab Regulations SHALL be designed to benefit from a future in which authorities increasingly publish authoritative machine-readable law.

Therefore the source architecture SHALL support:

```text
TODAY

Human-readable authority
        ↓
Baobab extraction
        ↓
Baobab verified machine rule
```

and:

```text
FUTURE

Authority-supplied machine rule
        ↓
Baobab validation/contextualisation
        ↓
Baobab applicability
        ↓
Baobab operational decision
```

Baobab's value SHALL not depend on remaining the only party capable of digitising regulation.

Its enduring value should lie in **operational contextualisation and execution**.

---

# 49. AfCFTA and Digital Trade Alignment

The African Union's AfCFTA Digital Trade Protocol seeks harmonised rules, common principles and standards that support digital trade and continental digital transformation.

Baobab Regulations SHOULD be designed so that increasing regional harmonisation improves the engine rather than makes it obsolete.

The preferred model is:

```text
national rules
       +
regional rules
       +
continental rules
       +
international rules
       │
       ▼
Regulatory applicability graph
```

The engine SHALL NOT hardcode an assumption that one geographic level permanently overrides another.

Legal hierarchy and applicability require explicit modelling.

---

# 50. Initial Regulatory Profile

The first implementation profile SHALL focus on **cross-border goods regulation**.

Initial target context:

```text
Origin:
Uganda

Destination:
South Africa

Initial product families:
Coffee
Vanilla
selected ZuriBeans commodities
```

Initial regulatory concerns SHOULD prioritise:

| Domain | Initial concern |
|---|---|
| Product classification | HS and national tariff classification |
| Customs | applicable customs requirements |
| Tariffs | duties and levies |
| Tax | import transaction tax consequences where supported |
| Rules of origin | origin qualification and evidence |
| SPS | sanitary/phytosanitary requirements |
| Product controls | restrictions and prohibitions |
| Permits | import/export permit requirements |
| Documentation | certificates and trade documentation |
| Market entry | product eligibility |
| Effective dates | historical/current regulatory applicability |
| Evidence | provenance and verification |

This is an implementation priority, not a permanent limitation of the domain model.

---

# 51. Initial Validation Use Case

A suitable canonical validation scenario is:

```text
Tenant:
ZuriBeans

Origin:
Uganda

Product:
green coffee

Destination:
South Africa

Transaction:
B2B cross-border goods sale

Shipment:
proposed

Question:
Can this transaction proceed,
what regulatory obligations apply,
and what evidence is required?
```

The engine SHOULD ultimately produce something conceptually equivalent to:

```text
assessment_id
context_hash
evaluated_at
effective_at

jurisdictions:
  - UG
  - ZA
  - applicable regional/supranational regimes

classification:
  status
  code
  evidence

obligations:
  - export licence
  - quality evidence
  - origin evidence
  - customs declaration
  - destination regulatory conditions

missing_evidence:
  ...

decision:
  ALLOW_WITH_REQUIREMENTS | REVIEW_REQUIRED | BLOCK | ...

sources:
  ...

rule_versions:
  ...

explanation:
  ...
```

This is conceptual only.

It does not pre-decide the final API schema.

---

# 52. Capability Model

Baobab Regulations SHOULD expose capabilities rather than applications.

Potential canonical capabilities include:

```text
regulations.source.read
regulations.rule.query
regulations.applicability.evaluate
regulations.obligation.resolve
regulations.assessment.evaluate
regulations.decision.explain
regulations.history.resolve
regulations.change.query
regulations.change.subscribe
regulations.impact.evaluate
regulations.evidence.bundle
regulations.crossborder.evaluate
```

Final capability vocabulary SHALL be promoted through `baobab-platform/shared`.

---

# 53. Capability Resolution

A Digital Estate or engine SHALL NOT assume a particular Regulations implementation.

The Control Plane SHOULD resolve:

```text
Capability:
regulations.assessment.evaluate

Context:
tenant / legal entity / market / jurisdiction

          │
          ▼
CapabilityBinding
          │
          ▼
Baobab Regulations EngineInstance
```

This maintains provider-neutral Baobab architecture.

---

# 54. Commercial Entitlement

Access to regulatory capabilities SHALL be capable of independent entitlement.

For example:

```text
Tenant A
    regulations.basic.research

Tenant B
    regulations.crossborder.evaluate

Tenant C
    regulations.change-impact

Tenant D
    regulations.enterprise-enforcement
```

Exact packaging belongs in later commercial architecture ADRs.

The foundational decision is:

> Regulatory capability SHALL be productisable independently of any single Digital Estate.

---

# 55. Regulations as a Platform Product

Baobab Regulations SHALL support both:

```text
embedded platform consumption
```

and:

```text
direct API / enterprise consumption
```

This allows:

```text
ZuriBeans
Baobab-native Digital Estates
future Baobab customers
third-party enterprise systems
partner applications
```

to consume the engine under controlled entitlements.

Baobab Regulations therefore SHALL NOT be architected only around ZuriBeans UI requirements.

ZuriBeans is the proving customer.

It is not the domain boundary.

---

# 56. Commercial Moat

The intended moat SHALL NOT be defined as:

```text
number of PDFs indexed
number of LLM prompts
number of chatbot answers
number of tariff tables
```

The intended defensibility is the accumulated relationship among:

```text
regulatory source
      │
regulatory rule
      │
obligation
      │
jurisdiction
      │
market
      │
product
      │
legal entity
      │
counterparty
      │
transaction
      │
evidence
      │
decision
      │
operational outcome
```

Over time this becomes a regulatory execution graph.

That graph can answer not only:

```text
What does the regulation say?
```

but:

```text
Who does it affect?

What must change?

Which transactions are exposed?

What evidence is missing?

What happened under the previous rule?

Which business opportunities became feasible?

Which risks have increased?
```

That is the strategic asset.

---

# 57. Must-Have Versus Nice-to-Have

The product SHALL aim to move from:

```text
informational utility
```

to:

```text
operational dependency
```

The path is:

```text
Research
   ↓
Applicability
   ↓
Assessment
   ↓
Transaction validation
   ↓
Regulatory gate
   ↓
Change impact
   ↓
Continuous operational assurance
```

A regulatory dashboard may be optional.

A system that tells a company whether it can legally:

```text
sell
import
export
ship
publish
process
retain
declare
```

becomes operational infrastructure.

That is the intended strategic position.

---

# 58. Public Regulatory Knowledge versus Tenant Knowledge

Regulatory source material MAY be shared platform-wide where rights permit.

Example:

```text
official tariff schedule
```

may be common.

Tenant-specific artefacts SHALL remain tenant-scoped.

Examples:

```text
private legal opinion
licence
permit
internal compliance policy
regulatory correspondence
customer-specific ruling
customs determination
```

The engine SHALL preserve the distinction between:

```text
PUBLIC REGULATORY KNOWLEDGE
```

and:

```text
TENANT REGULATORY EVIDENCE
```

---

# 59. Cross-Tenant Learning

Private regulatory evidence SHALL NOT automatically become shared training data or platform knowledge.

Any cross-tenant aggregation SHALL require explicit governance concerning:

```text
confidentiality
privacy
contractual rights
data residency
licensing
re-identification risk
model-training rights
```

No commercial advantage justifies violating tenant isolation.

---

# 60. Data Residency and Locality

Regulatory source data may be public, but assessment context may contain:

```text
customer identity
supplier identity
transaction value
product details
contracts
shipment information
employee information
private legal analysis
```

Therefore regulatory computation SHALL participate in Baobab isolation and residency controls.

Public-source status SHALL NOT cause private assessment context to lose classification.

---

# 61. Regulatory Context Minimisation

The engine SHALL consume only context required for the regulatory decision.

For example, determining an SPS requirement may need:

```text
product
origin
destination
classification
shipment state
```

It may not need:

```text
full customer accounting history
```

Context contracts SHOULD support minimal disclosure.

---

# 62. Failure Semantics

Regulatory failure SHALL not silently become regulatory approval.

The engine SHALL distinguish:

```text
NO_APPLICABLE_RULE
```

from:

```text
RULE_DATA_UNAVAILABLE
```

and:

```text
INSUFFICIENT_CONTEXT
```

and:

```text
SOURCE_STALE
```

and:

```text
INTERPRETATION_UNRESOLVED
```

and:

```text
CONFLICTING_AUTHORITY
```

and:

```text
ENGINE_UNAVAILABLE
```

These states are materially different.

---

# 63. Fail-Open versus Fail-Closed

No global fail-open/fail-closed behaviour SHALL be hardcoded.

Enforcement policy SHALL depend on:

```text
regulatory domain
decision assurance
business impact
risk classification
tenant policy
operational context
```

Example:

```text
optional catalogue advisory unavailable
```

may fail open with warning.

```text
verified prohibited-goods check unavailable
```

may require a regulatory hold.

Detailed semantics belong in later ADRs.

---

# 64. Source Freshness

Regulatory content SHALL carry freshness and verification state.

If a source expected to update daily has not been acquired for a material period, Baobab SHALL NOT continue presenting the regulatory state as unquestionably current.

The engine SHALL communicate degraded freshness explicitly.

---

# 65. Conflicting Sources

If two apparently authoritative sources conflict:

```text
Source A
  says X

Source B
  says Y
```

the engine SHALL NOT silently choose whichever was ingested last.

The conflict SHALL become explicit regulatory state requiring:

```text
hierarchy resolution
source-priority policy
human review
or authoritative clarification
```

depending on context.

---

# 66. Source Removal

If an authority removes an online source, previously acquired evidence SHALL remain governed by:

```text
licensing rights
retention policy
audit requirements
provenance policy
```

Deletion from the internet SHALL NOT automatically erase historical regulatory decision evidence.

---

# 67. Auditability

Every consequential assessment SHOULD preserve:

```text
assessment_id
tenant/context
effective time
rules evaluated
rule versions
source versions
evidence
decision
decision assurance
engine version
evaluation version
human reviewer where applicable
correlation_id
causation_id
```

An audit should not require reverse engineering application logs.

---

# 68. Decision Evidence Bundle

The engine SHOULD eventually support an immutable or tamper-evident logical evidence bundle:

```text
Regulatory Decision
       │
       ├── context snapshot / references
       ├── applicable rules
       ├── source citations
       ├── interpretation versions
       ├── evidence
       ├── exceptions
       ├── reviewer
       └── outcome
```

This SHALL be exportable for authorised audit and dispute workflows.

---

# 69. Override Governance

Operational systems MAY support authorised overrides.

An override SHALL NOT mutate the original regulatory decision.

Correct:

```text
Decision:
BLOCK

Override:
authorised reviewer
reason
timestamp
authority
```

Incorrect:

```text
Decision changed from BLOCK to ALLOW
with no trace
```

Regulatory history SHALL be additive and auditable.

---

# 70. Decision Replay

The architecture SHOULD support:

```text
Original decision
       │
       ▼
Replay using original rule set
```

and independently:

```text
Original transaction
       │
       ▼
Re-evaluate using current rule set
```

These are different operations.

They SHALL not be confused.

---

# 71. Regulatory Change Impact on Historical Decisions

A new rule does not automatically invalidate historical decisions.

The engine SHALL distinguish:

```text
prospective regulatory change
retroactive regulatory change
source correction
interpretation correction
Baobab implementation defect
```

These conditions may require different impact treatment.

---

# 72. Security Boundary

Regulatory input SHALL be treated as untrusted.

External documents, websites, APIs, attachments and datasets MAY contain:

```text
malformed content
prompt injection
embedded scripts
unexpected markup
poisoned metadata
incorrect classifications
malicious files
```

Regulatory ingestion SHALL therefore be isolated from decision authority.

No source document SHALL be capable of altering engine policy merely through embedded natural-language instructions.

---

# 73. AI Prompt-Injection Boundary

Natural-language regulatory sources are data.

They are not instructions to Baobab's AI runtime.

The architecture SHALL enforce:

```text
Source Content
      │
      ▼
Untrusted Evidence
```

not:

```text
Source Content
      │
      ▼
Agent Instruction
```

This is especially important if regulatory ingestion uses LLM-based extraction.

---

# 74. Administrative Boundary

Baobab Regulations SHALL require administrative capabilities for:

```text
source registration
source trust
rule verification
interpretation review
change approval
policy publication
decision investigation
override review
jurisdiction-pack lifecycle
```

These SHALL follow Baobab IAM and Control Plane administrative authority rather than inventing another identity system.

---

# 75. No General-Purpose Workflow Engine

Baobab Regulations SHALL NOT become another enterprise workflow product.

Regulatory workflows such as:

```text
review
verification
approval
override
```

may exist where required to govern regulatory state.

General procurement, sales, HR or operational workflows belong elsewhere.

---

# 76. No General-Purpose Rules Platform

Baobab Regulations SHALL NOT automatically become the policy engine for every Baobab rule.

Examples that do not inherently belong here:

```text
user may edit profile
order requires manager approval above R100,000
feature available to subscription tier X
employee receives 20 days leave
```

unless they are explicitly represented as regulatory-derived policy.

General platform entitlement remains with Control Plane/IAM and owning domains.

The fact that Regulations evaluates rules does not make all rules regulatory.

---

# 77. No Shadow Trade Engine

Regulations SHALL NOT own:

```text
orders
shipments
fulfilment
inventory
pricing
customers
suppliers
```

It may reference canonical identities and evaluate regulatory consequences.

---

# 78. No Shadow ERP

Regulations SHALL NOT own:

```text
general ledger
tax ledger
journal
accounts receivable
accounts payable
invoice accounting state
asset register
```

---

# 79. No Shadow Pulse

Regulations SHALL NOT own:

```text
market opportunity discovery
demand forecasting
competitive intelligence
commodity forecasting
strategic recommendation
general risk forecasting
```

unless these are directly regulatory assessments.

---

# 80. No Monolithic Global Legal Database Assumption

The architecture SHALL NOT require Baobab to ingest every law before delivering value.

Capability SHALL be composable by:

```text
jurisdiction
regulatory domain
trade corridor
product class
customer entitlement
```

This enables progressive coverage.

---

# 81. Jurisdiction Packs

The design SHALL permit future:

```text
UG regulatory pack
ZA regulatory pack
KE regulatory pack
TZ regulatory pack
RW regulatory pack
...
```

and domain packs such as:

```text
cross-border trade
food & agriculture
data protection
product safety
financial services
employment
environmental
```

Exact packaging belongs in `ADR-REG-0029`.

However, the core engine SHALL not hardcode Uganda or South Africa into the domain model.

---

# 82. Regulatory Profiles

Profiles MAY compose jurisdiction and domain knowledge.

Conceptually:

```text
CrossBorderGoodsProfile
      │
      ├── customs
      ├── origin
      ├── permits
      ├── restrictions
      ├── SPS
      └── documentation
```

and:

```text
UG
+
CrossBorderGoodsProfile
```

or:

```text
ZA
+
CrossBorderGoodsProfile
```

The same evaluation engine should consume different regulatory knowledge.

---

# 83. Architecture Must Support External Customers

Baobab Regulations SHALL NOT assume all customers belong to Nabhold Group Africa.

The engine MUST support:

```text
Baobab internal subsidiaries
external standalone organisations
external corporate groups
external subsidiaries
multi-market customers
multi-estate customers
```

Context is supplied by the Control Plane.

Regulations SHALL not embed Nabhold-specific ownership assumptions.

---

# 84. Provider-Neutrality

The following MUST remain replaceable:

```text
LLM provider
embedding provider
search engine
regulatory-content provider
OCR provider
rule-evaluation implementation
storage engine
graph implementation
notification provider
```

Canonical regulatory semantics SHALL remain Baobab-owned.

---

# 85. Technology Deferral

This ADR intentionally does **not** decide:

```text
programming language
web framework
database
graph database
vector database
rule engine
OPA adoption
LegalRuleML serialization
LLM provider
search engine
message broker
UI framework
```

Those decisions SHALL follow domain and contract decisions.

We will not choose a graph database merely because diagrams contain graphs.

We will not choose an LLM merely because regulatory text is natural language.

We will not choose OPA merely because it is a policy engine.

Architecture first.

Tooling second.

---

# 86. Standards Posture

Baobab SHOULD favour semantic compatibility with mature standards where doing so improves interoperability.

| Standard / body | Architectural relevance |
|---|---|
| OECD Rules/Law as Code | Machine-consumable regulatory logic and institutional governance |
| OASIS LegalRuleML | Legal-rule semantics |
| W3C PROV | Provenance and derivation |
| WCO Data Model | Cross-border regulatory data interoperability |
| WTO Trade Facilitation Agreement | Publication, formalities, standards and Single Window direction |
| AfCFTA frameworks | Continental/regional trade and digital-trade context |
| ISO/UN/CEFACT where relevant | Trade and information interoperability |

Baobab SHALL not adopt standards ceremonially.

Each standard must solve a real interoperability or semantic problem.

---

# 87. Alternatives Considered

## Alternative A — Put regulation inside Baobab Trade

Rejected.

This would make Trade the implicit legal engine and prevent ERP, CMS, IAM, Pulse and third-party systems from consuming regulation independently.

It would also couple regulatory logic to Medusa-oriented commerce implementation.

---

## Alternative B — Put regulation inside Pulse

Rejected.

Pulse evaluates evidence and produces intelligence.

Regulatory applicability carries different authority, provenance, temporal and enforcement requirements.

Combining them risks treating:

```text
market inference
```

and:

```text
legal obligation
```

as equivalent evidence types.

They are not.

---

## Alternative C — Buy one regulatory platform and expose it directly

Rejected as the platform architecture.

Commercial providers may be excellent source partners.

But making one vendor's ontology and APIs canonical would create provider lock-in and undermine Baobab's platform contract.

Preferred:

```text
Provider
    ↓
Adapter
    ↓
Baobab canonical regulatory model
```

---

## Alternative D — Build a giant global regulatory corpus ourselves

Rejected.

It would consume enormous resources and recreate capabilities already available from regulators, governments, commercial providers and standards organisations.

Baobab should own the differentiating execution layer.

---

## Alternative E — Build only an AI regulatory chatbot

Rejected.

Search and summarisation have low barriers to replication.

A chatbot alone does not provide:

```text
temporal reconstruction
transaction applicability
verified rule execution
operational gating
change impact
decision replay
audit evidence
```

---

## Alternative F — General-purpose policy-as-code service

Rejected as the core identity.

A generic policy engine can evaluate rules but does not inherently understand:

```text
legal authority
regulatory provenance
jurisdiction
effective dates
obligations
legal hierarchy
evidence
regulatory change
```

A policy engine may become an implementation component.

It is not the domain.

---

## Alternative G — Dedicated Baobab Regulatory Context and Execution Engine

**Accepted.**

This best preserves:

```text
domain ownership
provider neutrality
Baobab context integration
commercial productisation
auditability
cross-engine reuse
future Law-as-Code compatibility
```

---

# 88. Consequences — Positive

This decision creates a single canonical regulatory boundary.

It allows:

```text
one interpretation
one provenance chain
one temporal regulatory state
many consuming engines
```

It creates potential recurring commercial products around:

```text
jurisdiction access
transaction assessments
cross-border regulatory profiles
change monitoring
impact analysis
historical reconstruction
audit evidence
enterprise enforcement
```

It strengthens Pulse by giving intelligence access to trusted regulatory change.

It strengthens Trade by removing duplicated compliance logic.

It strengthens ERP by providing externally governed regulatory facts without making ERP collect them.

It improves provider portability.

It creates a platform capability that can be consumed outside Baobab Digital Estates.

---

# 89. Consequences — Negative

This decision introduces a difficult domain.

The engine will require:

```text
regulatory-domain expertise
source licensing discipline
strong provenance
temporal modelling
verification workflows
high-quality testing
continuous source maintenance
careful AI governance
```

Incorrect regulatory decisions may have significant financial or legal consequences.

Source coverage will initially be incomplete.

Human review will remain necessary for many cases.

Commercial regulatory datasets may be expensive.

Legal structures vary by jurisdiction.

Not every rule is machine-executable.

These are accepted costs.

Pretending otherwise would be more dangerous.

---

# 90. Key Architectural Risks

| Risk | Required architectural response |
|---|---|
| Hallucinated legal interpretation | Source grounding + verification + assurance levels |
| Stale law | freshness state + change monitoring |
| Wrong effective date | temporal model |
| Hidden source conflict | explicit conflict state |
| Vendor lock-in | adapters + canonical model |
| Over-automation | review/enforcement classes |
| Legal-content licensing violation | source rights registry |
| Regulatory drift | change detection + impact |
| Hard-coded jurisdiction logic | packs/profiles |
| Cross-tenant leakage | Control Plane isolation |
| AI prompt injection | untrusted source boundary |
| Unexplained block | decision evidence bundle |
| Rules duplicated across engines | central regulatory ownership |
| Platform bottleneck | capability-oriented deployment and caching strategies in later ADRs |

---

# 91. Architectural Invariants

The following SHALL be treated as non-negotiable unless a future ADR explicitly supersedes this decision:

| Invariant | Rule |
|---|---|
| REG-I01 | Authoritative source and Baobab interpretation are distinct |
| REG-I02 | Regulatory decisions must identify their rule/source lineage |
| REG-I03 | Regulatory state must be temporally reconstructable |
| REG-I04 | Tenant and jurisdiction are not synonyms |
| REG-I05 | Regulations does not own another engine's operational data |
| REG-I06 | Operational enforcement occurs through the owning engine |
| REG-I07 | AI output alone cannot create high-assurance enforcement authority |
| REG-I08 | Uncertainty must be representable |
| REG-I09 | External providers enter through adapters |
| REG-I10 | Public availability does not imply commercial reuse rights |
| REG-I11 | Private tenant evidence remains tenant scoped |
| REG-I12 | Regulatory change is first-class domain state |
| REG-I13 | Current and historical assessments must be distinguishable |
| REG-I14 | Regulatory context is supplied through canonical platform contracts |
| REG-I15 | UI code is not a regulatory system of record |
| REG-I16 | Pulse and Regulations retain distinct authority |
| REG-I17 | Regulatory semantics are platform-owned, not vendor-owned |
| REG-I18 | No direct cross-engine database writes |
| REG-I19 | Missing regulatory data must not silently mean permission |
| REG-I20 | Every consequential decision must be explainable at an appropriate level |

---

# 92. Success Criteria

Baobab Regulations SHOULD eventually demonstrate all of the following in a production-quality proof:

```text
1.
Acquire authoritative UG and ZA regulatory sources.

2.
Preserve immutable/source-verifiable provenance.

3.
Represent at least one cross-border regulatory domain canonically.

4.
Resolve applicable rules from canonical Baobab context.

5.
Evaluate a ZuriBeans UG → ZA commodity transaction.

6.
Identify regulatory obligations and missing evidence.

7.
Produce an explainable assessment.

8.
Replay that assessment using the same historical rule set.

9.
Detect a regulatory change.

10.
Identify at least one affected canonical context.

11.
Publish a canonical regulatory event.

12.
Allow Trade to enforce the decision without Regulations
mutating Trade state directly.

13.
Allow Pulse to consume the regulatory change and assess
commercial implications.

14.
Replace or simulate replacement of one regulatory source
provider without changing the external capability contract.
```

If we cannot demonstrate these behaviours cleanly, the architecture has not yet proved the intended differentiation.

---

# 93. Initial North-Star Scenario

The primary proof SHALL be:

```text
                      ZURIBEANS

UG Supplier / Export Operation
             │
             ▼
         Product
      Coffee / Vanilla
             │
             ▼
       Proposed Trade
             │
             ▼
   BAOBAB CONTROL PLANE
             │
       resolved context
             │
             ▼
    BAOBAB REGULATIONS
             │
       ┌─────┴──────────────┐
       │                    │
       ▼                    ▼
Uganda obligations   South Africa obligations
       │                    │
       └─────────┬──────────┘
                 │
                 ▼
        Regional / treaty rules
                 │
                 ▼
       Regulatory Assessment
                 │
      ┌──────────┼───────────┐
      ▼          ▼           ▼
    ALLOW      REVIEW      BLOCK
      │          │           │
      └──────────┼───────────┘
                 ▼
             TRADE
                 │
                 ▼
       Operational workflow
```

At every step:

```text
decision
   ↓
rule
   ↓
provision
   ↓
source
```

must remain traceable.

---

# 94. Pulse + Regulations Strategic Flywheel

The two differentiators SHOULD eventually reinforce one another.

```text
                BAOBAB PULSE
                     │
       commercial / market signals
                     │
                     ▼
          Opportunity / Risk
                     │
                     ▼
            BAOBAB REGULATIONS
                     │
        regulatory feasibility
                     │
                     ▼
            Business Decision
```

and:

```text
           BAOBAB REGULATIONS
                     │
           regulatory change
                     │
                     ▼
                BAOBAB PULSE
                     │
          strategic impact
                     │
                     ▼
       Opportunity / Risk / Forecast
```

This creates a platform proposition that is stronger than either engine alone:

> **Pulse discovers what matters. Regulations determines what is permissible and required. Operational engines execute.**

---

# 95. Long-Term Strategic Position

Baobab Regulations SHALL be designed for a future in which regulatory authorities increasingly publish digital and potentially machine-executable regulation.

The engine should therefore remain valuable even if:

```text
manual regulatory extraction
```

becomes much easier or disappears.

Future Baobab value should lie in:

```text
multi-jurisdiction composition
context resolution
legal-entity applicability
business-object impact
transaction evaluation
operational enforcement integration
historical reconstruction
cross-engine regulatory assurance
```

That remains valuable even when authoritative rules arrive already machine-readable.

---

# 96. Product Position

The target external proposition is not:

> "Search African regulations."

It is:

> **"Know what your business is allowed, required or prohibited from doing in each operating context — before you commit, ship, pay, publish or process."**

The internal platform proposition is:

> **"One source of regulatory context for every Baobab engine."**

The architectural proposition is:

> **"Make regulation executable without making software pretend to be the law."**

---

# 97. Follow-On ADR Programme

This ADR establishes the constitutional boundary.

The following decisions SHALL elaborate it:

| ADR | Subject |
|---|---|
| `ADR-REG-0002` | Baobab Regulations as a Headless Platform Engine |
| `ADR-REG-0003` | Regulatory Authority versus Baobab Interpretation Boundary |
| `ADR-REG-0004` | Advisory, Review and Enforcement Decision Classes |
| `ADR-REG-0005` | Provider-Neutral Regulatory Intelligence Architecture |
| `ADR-REG-0006` | Canonical Regulatory Domain Model |
| `ADR-REG-0007` | Jurisdiction, Regulatory Authority and Legal Hierarchy Model |
| `ADR-REG-0008` | Regulatory Instrument, Provision, Rule and Obligation Model |
| `ADR-REG-0009` | Permission, Prohibition, Obligation, Exemption and Discretion Semantics |
| `ADR-REG-0010` | Regulatory Knowledge Graph and Relationship Model |
| `ADR-REG-0011` | Authoritative Source Registry and Source Trust Model |
| `ADR-REG-0012` | Regulatory Content Acquisition, Licensing and Reuse Rights |
| `ADR-REG-0013` | Source Ingestion, Normalisation and Adapter Architecture |
| `ADR-REG-0014` | Provenance, Citation and Evidentiary Chain |
| `ADR-REG-0015` | Temporal Regulation, Versioning and Historical Reconstruction |
| `ADR-REG-0016` | Machine-Executable Regulatory Rules Representation |
| `ADR-REG-0017` | Regulatory Context and Applicability Resolution |
| `ADR-REG-0018` | Regulatory Decision and Evaluation Engine |
| `ADR-REG-0019` | Policy Decision Point and Enforcement Point Separation |
| `ADR-REG-0020` | Decision Explainability, Replay and Reproducibility |
| `ADR-REG-0021` | AI-Assisted Regulatory Extraction and Interpretation Boundary |
| `ADR-REG-0022` | Human Verification, Confidence and Regulatory Governance Workflow |
| `ADR-REG-0023` | Regulatory Change Detection and Impact Analysis |
| `ADR-REG-0024` | Regulatory Events, Subscriptions and Proactive Notifications |
| `ADR-REG-0025` | Testing, Golden Regulatory Cases and Decision Regression |
| `ADR-REG-0026` | Baobab Platform Integration and Canonical Context Contract |
| `ADR-REG-0027` | Cross-Border Trade Regulatory Profile |
| `ADR-REG-0028` | Multi-Tenancy, Isolation, Security, Audit and Data Residency |
| `ADR-REG-0029` | Jurisdiction Packs, Regulatory Modules and Extension Marketplace |
| `ADR-REG-0030` | Commercial Product Model, Entitlements, Metering and Regulatory Decision SLA |

---

# 98. Research Foundation

This ADR is informed by several external architectural and regulatory trends.

The OECD's Rules-as-Code work establishes the importance of machine-consumable rules and explicitly considers both their possibilities and limitations.

The OECD's 2026 Law-as-Code consultation identifies repeated translation of legal logic across systems as a source of duplication, inconsistency, limited transparency and provider dependency.

OASIS LegalRuleML demonstrates mature semantic treatment of obligations, permissions, prohibitions, jurisdiction, temporal rules and defeasibility.

W3C PROV provides a mature provenance model for entities, activities, agents and derivation.

OPA demonstrates the architectural value of separating policy decision from enforcement.

The WCO Data Model demonstrates that cross-border regulatory interoperability benefits from standardised reusable data definitions rather than proprietary field systems.

The WTO Trade Facilitation Agreement reinforces publication, transparency, international standards and Single Window principles for cross-border formalities.

The AfCFTA e-Tariff initiative and PAFTRAC evidence demonstrate both progress in continental trade information and continuing business-access problems.

The African Union's Digital Trade Protocol demonstrates a policy direction toward harmonised continental digital-trade rules and standards.

RegGenome demonstrates that structured, machine-readable, source-linked regulatory infrastructure is already commercially meaningful, while Cambridge's research also exposes the non-trivial content-licensing problem.

SAP GTS proves that transaction-level compliance decisions and operational blocking are commercially established requirements, meaning Baobab must compete beyond mere information retrieval.

Thomson Reuters demonstrates that comprehensive regulatory content plus cited AI research is already available at global scale, again reinforcing that Baobab's moat must exist above the corpus layer.

---

# 99. Final Decision

Baobab Regulations SHALL be established as a **provider-neutral, multi-tenant, jurisdiction-aware, temporally correct, provenance-first Regulatory Context and Execution Engine**.

It SHALL:

```text
understand authoritative regulatory sources
        │
        ▼
structure them without claiming sovereign authority
        │
        ▼
resolve them against Baobab Context
        │
        ▼
determine applicable obligations and conditions
        │
        ▼
produce explainable regulatory assessments
        │
        ▼
preserve source and temporal evidence
        │
        ▼
publish decisions through canonical contracts
        │
        ▼
allow owning engines to enforce those decisions
```

It SHALL NOT become:

```text
a regulator

a law firm

a generic chatbot

a shadow ERP

a shadow Trade engine

a shadow IAM engine

a shadow Pulse engine

a generic policy service

a proprietary regulatory data silo

an LLM whose confidence is mistaken for legal authority
```

Baobab Regulations and Baobab Pulse SHALL form complementary strategic differentiators:

```text
                     BAOBAB PLATFORM
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       BAOBAB PULSE              BAOBAB REGULATIONS
   System of Intelligence      System of Regulatory
                                Context & Execution
             │                           │
             └─────────────┬─────────────┘
                           │
                    Decision Support
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
        Trade             ERP          Digital Estates
```

The long-term strategic objective is not simply to help a user read regulation.

It is to allow Baobab to answer, with defensible evidence:

> **What rules apply to this organisation, this legal entity, this product, this market, this counterparty, this transaction and this moment in time?**

Then:

> **What must happen because of them?**

Then:

> **What changed, what is affected, and what action is required?**

If Baobab can answer those questions reliably across fragmented regulatory environments while remaining explainable, provider-neutral and deeply integrated into business operations, Baobab Regulations becomes more than a compliance feature.

It becomes **regulatory infrastructure for the business itself**.

That is the architectural intent established by `ADR-REG-0001`.

---

## Decision Summary

```text
DECISION
────────

Create Baobab Regulations as an independent
Regulatory Context & Execution Engine.

Authority:
Own canonical Baobab regulatory knowledge,
applicability assessments, regulatory decisions,
change impact and regulatory evidence.

Do not own:
Sovereign legal authority or operational
transactions belonging to other engines.

Differentiation:
Regulation + Baobab Context + Temporal Truth
+ Provenance + Applicability + Execution.

Initial proof:
Uganda → South Africa cross-border goods,
starting with ZuriBeans coffee/vanilla.

Strategic peer:
Baobab Pulse.

Long-term destination:
Regulation-aware operations across every
Baobab capability and customer.
```
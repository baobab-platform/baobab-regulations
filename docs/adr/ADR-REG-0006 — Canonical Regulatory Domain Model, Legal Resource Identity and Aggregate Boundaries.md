# ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries

**Status:** Proposed — Normative Foundational Domain Architecture  
**Decision ID:** `ADR-REG-0006`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Decision Type:** Canonical Domain Model / Aggregate Boundary / Semantic Architecture  
**Date:** 2026-09-28  
**Strategic Classification:** Core Platform IP / Regulatory Semantic Foundation

**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`

**Relevant Existing Baobab Architecture:**

- `ADR-BCP-004 — Context, Market, Geography, Legal-Entity and Digital Estate Resolution Model`
- `ADR-BCP-011 — Market Participation, Trade Lanes and Cross-Market Trading Model`
- `ADR-BCP-018 — Canonical Organisation, Corporate Group, Platform Account and Tenant Relationship Model`
- `ADR-SHARED-007 — Canonical Capability Contracts, Composition Registry and Cross-Engine Provider Model`
- `ADR-SHARED-012 — Topology Identifiers and External System Registry`
- `ADR-SHARED-013 — External References and Canonical Mapping Administration`
- `ADR-PULSE-002 — Canonical Intelligence Domain Model and Aggregate Boundaries`
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`

**Primary Principle:**

> **Baobab Regulations SHALL model regulation according to its legal and operational semantics, not according to the shape of the documents, databases, vendors or APIs from which it was acquired.**

---

# 1. Executive Decision

Baobab Regulations SHALL establish a canonical, provider-neutral **Regulatory Domain Model** separating:

```text
AUTHORITY
   │
   ▼
LEGAL / REGULATORY RESOURCE
   │
   ▼
LEGAL EXPRESSION
   │
   ▼
SOURCE ARTEFACT
```

from:

```text
PROVISION
   │
   ▼
INTERPRETATION
   │
   ▼
REGULATORY RULE
   │
   ▼
APPLICABILITY
   │
   ▼
REGULATORY EFFECT
   │
   ▼
ASSESSMENT
   │
   ▼
DECISION
```

and separately from:

```text
BAOBAB PLATFORM CONTEXT
   │
   ├── tenant
   ├── organisation
   ├── legal entity
   ├── market
   ├── jurisdiction
   ├── trade lane
   ├── Digital Estate
   └── canonical business references
```

The core model SHALL NOT collapse these concepts.

The fundamental canonical graph SHALL be:

```text
                    REGULATORY AUTHORITY
                            │
                            ▼
                   REGULATORY REGIME
                            │
                            ▼
                  REGULATORY INSTRUMENT
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
      INSTRUMENT EXPRESSION       REGULATORY PROVISION
                │                       │
                ▼                       ▼
         SOURCE ARTEFACT          PROVISION VERSION
                                        │
                                        ▼
                               REGULATORY INTERPRETATION
                                        │
                                        ▼
                                  REGULATORY RULE
                                        │
                             ┌──────────┼───────────┐
                             ▼          ▼           ▼
                         CONDITIONS  EXCEPTIONS   EFFECT
                                        │
                                        ▼
                             APPLICABILITY EVALUATION
                                        │
                                        ▼
                              REGULATORY EFFECT
                                        │
                             ┌──────────┼───────────┐
                             ▼          ▼           ▼
                         OBLIGATION  PERMISSION  PROHIBITION
                             │
                             ▼
                            etc.
                                        │
                                        ▼
                              REGULATORY ASSESSMENT
                                        │
                                        ▼
                                REGULATORY DECISION
```

This graph is a **semantic architecture**.

It SHALL NOT imply that Baobab must use a graph database.

---

# 2. Why This ADR Is Critical

Almost every future Regulations decision depends on this ADR.

If the canonical model is weak, later implementations will create divergent concepts such as:

```text
SouthAfricaRegulation

UgandaTariff

CustomsRequirement

PermitCheck

LawRecord

ComplianceRule

TradeRestriction
```

with inconsistent meanings.

Eventually:

```text
Trade
```

would interpret regulation differently from:

```text
ERP
```

which would differ from:

```text
Pulse
```

which would differ from:

```text
the ZuriBeans UI.
```

That would destroy the entire premise of Baobab Regulations.

---

# 3. Canonical Domain Goal

The domain model must support questions such as:

```text
Who issued this rule?

What legal instrument contains it?

Which provision supports it?

Which version was in force?

Which interpretation produced the executable rule?

Which jurisdiction or regime governs it?

Who or what is subject to it?

Under which conditions does it apply?

Which exceptions defeat it?

What obligation or prohibition arises?

What evidence satisfies that obligation?

What happens if it is not satisfied?

Which transaction was evaluated?

Which version of the rule was applied?

What decision resulted?

What changed later?
```

without collapsing everything into:

```text
compliance_rule JSONB
```

---

# 4. Research Foundation — Legal Resource Identity

The current ELI ontology defines a common data model for exchanging legislation metadata and is currently published as version 1.5 by the EU Publications Office.

ELI's modelling distinguishes levels corresponding conceptually to:

```text
LegalResource
      │
      ▼
LegalExpression
      │
      ▼
Format
```

allowing the same underlying legal resource to have different language or version expressions and different publication formats.

Baobab SHALL adopt the **principle** of this separation.

It SHALL NOT blindly import the ELI ontology as its internal model.

---

# 5. Research Foundation — Structured Legal Documents

OASIS Akoma Ntoso 1.0 is an international standard for structured machine-readable legislative, regulatory and judicial documents and provides a shared document and metadata model across institutions.

Akoma Ntoso explicitly separates legal-document metadata from structural content and supports lifecycle and publication information.

Baobab SHOULD therefore avoid inventing an incompatible document-structure vocabulary where mature legal-document concepts are available.

However:

> **Akoma Ntoso is an interchange/document standard; it SHALL NOT become the Baobab Regulations bounded-context model by default.**

---

# 6. Research Foundation — Normative Rules

OASIS LegalRuleML 1.0 models:

```text
constitutive rules
prescriptive rules
obligations
permissions
prohibitions
jurisdiction
temporality
defeasibility
authorial tracking
rule/provision relationships
```

and explicitly supports many-to-many relationships between machine rules and textual legal provisions.

Baobab SHALL incorporate these semantic lessons.

---

# 7. Research Foundation — Provenance

W3C PROV distinguishes:

```text
Entity
Activity
Agent
```

and models derivation and responsibility across transformations.

Baobab Regulations SHALL remain conceptually compatible with this approach for provenance.

---

# 8. Domain Bounded Contexts

The Regulations domain SHALL be organised conceptually into six bounded contexts:

```text
1. SOURCE & AUTHORITY

2. LEGAL RESOURCE

3. NORMATIVE KNOWLEDGE

4. REGULATORY EVALUATION

5. CHANGE & IMPACT

6. REGULATORY GOVERNANCE
```

These are logical bounded contexts.

They SHALL NOT automatically become six microservices.

---

# 9. Bounded Context — Source & Authority

Responsible for:

```text
RegulatoryAuthority

RegulatorySourceProvider

RegulatorySource

SourceArtefact

Acquisition provenance

Source rights

Source authenticity

Source coverage
```

---

# 10. Bounded Context — Legal Resource

Responsible for:

```text
RegulatoryRegime

RegulatoryInstrument

InstrumentExpression

RegulatoryProvision

ProvisionVersion

RegulatoryCitation

instrument lifecycle relationships
```

---

# 11. Bounded Context — Normative Knowledge

Responsible for:

```text
RegulatoryConcept

RegulatoryInterpretation

RegulatoryRule

ApplicabilityCriterion

RuleCondition

RuleException

NormativeEffectTemplate

Rule relationships
```

---

# 12. Bounded Context — Regulatory Evaluation

Responsible for:

```text
RegulatoryContext

RegulatoryFactSnapshot

ApplicabilityResult

RegulatoryEffect

RegulatoryAssessment

RegulatoryDecision

Decision Effect Class
```

---

# 13. Bounded Context — Change & Impact

Responsible for:

```text
RegulatoryChange

RegulatoryImpact

affected-rule relationships

affected-context relationships

reassessment requirements
```

---

# 14. Bounded Context — Governance

Responsible for:

```text
Verification

Review

Publication

Suspension

Override

Challenge

Decision assurance

Regulatory evidence bundles
```

---

# 15. Platform Context Is Not Regulations-Owned

Baobab Regulations SHALL consume but SHALL NOT redefine:

```text
Tenant

Organisation

CorporateGroup

PlatformAccount

LegalEntity

Market

Jurisdiction

TradeLane

DigitalEstate

Principal

Capability
```

These remain governed by Control Plane / Shared.

---

# 16. Regulatory Extension of Platform Jurisdiction

Control Plane already owns canonical:

```text
Jurisdiction
```

identity.

Regulations SHALL therefore NOT invent a parallel:

```text
regulations_country
```

table as the canonical platform identity.

Instead, Regulations MAY own:

```text
RegulatoryJurisdictionProfile
```

referencing the canonical `jurisdiction_id`.

Conceptually:

```text
RegulatoryJurisdictionProfile
├── jurisdiction_ref
├── legal_system_metadata
├── authority_relationships
├── hierarchy_profile
├── source_coverage
├── regulatory_domains
└── lifecycle
```

---

# 17. Market Is Not Jurisdiction

This existing Baobab invariant is especially important here:

```text
Market
≠
Jurisdiction
```

A South African commercial market may involve:

```text
national law

provincial requirements

municipal requirements

SACU

SADC

AfCFTA

international standards
```

depending on context.

Regulations SHALL never infer the whole legal environment from:

```text
market_id.
```

---

# 18. Jurisdiction Is Not Regulatory Regime

Likewise:

```text
Jurisdiction
≠
RegulatoryRegime.
```

A regime may span several jurisdictions.

Examples conceptually include:

```text
AfCFTA

EAC customs framework

SACU customs framework

international treaty regime

national data-protection regime
```

---

# 19. RegulatoryRegime

`RegulatoryRegime` SHALL represent a coherent body or framework of regulatory authority applicable to a subject area or legal relationship.

Conceptually:

```text
RegulatoryRegime
├── id
├── canonical_name
├── regime_type
├── jurisdiction_refs[]
├── authority_refs[]
├── regulatory_domains[]
├── valid_from
├── valid_to?
├── lifecycle_state
└── metadata
```

---

# 20. Regime Types

Initial conceptual types MAY include:

```text
NATIONAL

SUBNATIONAL

SUPRANATIONAL

REGIONAL

TREATY

CUSTOMS_UNION

REGULATOR_SPECIFIC

SECTORAL

INTERNATIONAL
```

These are classification aids.

They SHALL NOT independently determine legal hierarchy.

---

# 21. RegulatoryDomain

Baobab SHALL maintain a stable regulatory-domain taxonomy.

Initial candidates include:

```text
CUSTOMS

TARIFF

TRADE_CONTROLS

RULES_OF_ORIGIN

SPS

FOOD_SAFETY

PRODUCT_STANDARDS

LABELLING

INDIRECT_TAX

DIRECT_TAX

CORPORATE

LICENSING

DATA_PROTECTION

CYBERSECURITY

FINANCIAL_SERVICES

EMPLOYMENT

ENVIRONMENTAL

SANCTIONS

TRANSPORT

LOGISTICS

CONSUMER_PROTECTION
```

The list SHALL evolve under governance.

---

# 22. Regulatory Domain Is Not Repository Namespace

The fact that a regulation belongs to:

```text
DATA_PROTECTION
```

does not imply:

```text
baobab-iam owns it.
```

Regulations owns regulatory knowledge.

IAM may enforce relevant identity/security controls.

---

# 23. RegulatoryAuthority

`RegulatoryAuthority` SHALL be an aggregate root.

It represents a legally or institutionally relevant authority associated with issuing, administering, interpreting or adjudicating regulation.

Conceptually:

```text
RegulatoryAuthority
├── id
├── canonical_name
├── authority_type
├── jurisdiction_refs[]
├── regulatory_domain_refs[]
├── predecessor_refs[]
├── successor_refs[]
├── valid_from
├── valid_to?
├── external_refs[]
└── lifecycle_state
```

---

# 24. Authority Types

Potential types:

```text
LEGISLATURE

EXECUTIVE_AUTHORITY

MINISTRY

REGULATOR

CUSTOMS_AUTHORITY

TAX_AUTHORITY

COURT

TRIBUNAL

TREATY_BODY

REGIONAL_BODY

STANDARDS_AUTHORITY

MUNICIPAL_AUTHORITY

OTHER_COMPETENT_AUTHORITY
```

Legal rank is not implied by this taxonomy.

---

# 25. Authority Aggregate Boundary

The Authority aggregate owns:

```text
identity

classification

institutional lifecycle

authority relationships
```

It SHALL NOT transactionally own:

```text
all instruments it ever issued.
```

Instruments reference authority identities.

---

# 26. RegulatoryInstrument

`RegulatoryInstrument` SHALL represent the stable conceptual identity of a legal or regulatory instrument.

Examples:

```text
Act

Regulation

Notice

Directive

Treaty

Order

Ruling

Standard incorporated into law

Official schedule
```

Conceptually:

```text
RegulatoryInstrument
├── id
├── authority_refs[]
├── regime_refs[]
├── jurisdiction_refs[]
├── instrument_type
├── official_identifier
├── canonical_title
├── regulatory_domains[]
├── lifecycle_state
├── enacted_at?
├── published_at?
├── effective_from?
├── effective_to?
├── repealed_at?
└── external_refs[]
```

---

# 27. Instrument Identity Is Stable

The instrument identity SHOULD survive:

```text
new HTML rendering

new PDF

translation

consolidation

minor publication format change
```

unless the legal identity itself changes.

---

# 28. Instrument Is Not Document File

This invariant is mandatory:

```text
RegulatoryInstrument
≠
PDF.
```

One instrument can have:

```text
PDF

HTML

XML

official print

translation

consolidated expression
```

---

# 29. InstrumentExpression

`InstrumentExpression` SHALL represent a particular linguistic, temporal or editorial expression of an instrument.

This is influenced by the ELI distinction between legal resource and legal expression.

Conceptually:

```text
InstrumentExpression
├── id
├── instrument_id
├── language
├── expression_type
├── version_date
├── consolidation_date?
├── official_status
├── valid_from?
├── valid_to?
├── publisher_ref?
└── source_artefact_refs[]
```

---

# 30. Expression Types

Potential:

```text
ORIGINAL

AMENDED

CONSOLIDATED

OFFICIAL_TRANSLATION

UNOFFICIAL_TRANSLATION

CORRECTED

REPUBLICATION
```

---

# 31. Expression Is Not Artefact

Example:

```text
English consolidated expression
```

may exist as:

```text
HTML

PDF

XML.
```

Therefore:

```text
InstrumentExpression
≠
SourceArtefact.
```

---

# 32. SourceArtefact

`SourceArtefact` remains the acquired physical/digital representation established by ADR-REG-0005.

Examples:

```text
PDF file

HTML snapshot

XML document

JSON response

CSV schedule
```

It SHALL retain:

```text
provider

endpoint

hash

retrieval time

rights

provenance
```

---

# 33. Legal Resource Three-Level Model

Baobab SHALL therefore implement conceptually:

```text
REGULATORY INSTRUMENT
       │
       │ expressed as
       ▼
INSTRUMENT EXPRESSION
       │
       │ embodied / published as
       ▼
SOURCE ARTEFACT
```

This provides stable legal identity despite changing technical formats.

---

# 34. RegulatoryProvision

`RegulatoryProvision` SHALL represent a stable addressable structural component of an instrument.

Examples:

```text
Section

Article

Regulation

Rule

Schedule Item

Paragraph

Subsection

Table entry
```

Conceptually:

```text
RegulatoryProvision
├── id
├── instrument_id
├── provision_type
├── canonical_locator
├── parent_provision_id?
├── ordering_key
├── semantic_heading?
└── lifecycle_state
```

---

# 35. Provision Hierarchy

Provisions SHOULD support hierarchy:

```text
Section 7
   │
   ├── subsection (1)
   │
   ├── subsection (2)
   │      ├── paragraph (a)
   │      └── paragraph (b)
   └── subsection (3)
```

Baobab SHALL not flatten this into unrelated strings where source structure is available.

---

# 36. Provision Identity and Provision Text Are Distinct

A stable:

```text
Section 7
```

may have different text over time.

Therefore:

```text
RegulatoryProvision
      │
      ▼
ProvisionVersion
```

SHALL be supported.

---

# 37. ProvisionVersion

Conceptually:

```text
ProvisionVersion
├── id
├── provision_id
├── expression_id
├── text_reference
├── valid_from
├── valid_to?
├── effective_from?
├── effective_to?
├── source_artefact_refs[]
├── content_hash?
└── status
```

---

# 38. Why ProvisionVersion Matters

Without provision versions, Baobab cannot reliably answer:

> What exactly did section 7(3) say on 18 February 2027?

That is unacceptable for regulatory infrastructure.

---

# 39. Structured Legal Documents

Akoma Ntoso provides mature patterns for representing structured legislative and judicial documents, including document metadata and nested content.

Baobab SHOULD map Akoma Ntoso-compatible structures where useful.

It SHALL not require every source to be converted into full Akoma Ntoso XML before it can be useful.

---

# 40. RegulatoryCitation

A `RegulatoryCitation` SHALL represent a precise reference from one regulatory object to another legal resource or provision.

It MAY capture:

```text
instrument reference

provision locator

case reference

standard reference

authority ruling reference
```

It SHALL support:

```text
source-backed explanation

cross-reference resolution

impact analysis
```

---

# 41. Regulatory Relationships

The domain SHALL support typed relationships instead of generic:

```text
RELATED_TO.
```

---

# 42. Legislative Lifecycle Relationships

Initial relationship types SHOULD include:

```text
AMENDS

AMENDED_BY

REPEALS

REPEALED_BY

COMMENCES

COMMENCED_BY

CORRECTS

CORRECTED_BY

CONSOLIDATES

CONSOLIDATED_BY

SUPERSEDES

SUPERSEDED_BY
```

ELI currently models several of these legislative relationships explicitly, including amendments, repeal, commencement, correction and consolidation.

---

# 43. Legal Dependency Relationships

Additional relationships MAY include:

```text
BASED_ON

IMPLEMENTS

TRANSPOSES

INCORPORATES_BY_REFERENCE

CITES

APPLIES

DELEGATES_AUTHORITY_TO
```

---

# 44. Provenance Relationships

The model SHALL support:

```text
DERIVED_FROM

EXTRACTED_FROM

INTERPRETS

ENCODES

VERIFIED_BY

EXPLAINED_BY
```

---

# 45. Normative Relationships

The model SHALL eventually support:

```text
OVERRIDES

EXCEPTS

QUALIFIES

DEFEATS

REPAIRS

TRIGGERS
```

The precise semantics belong primarily in ADR-REG-0008/0009.

---

# 46. RegulatoryConcept

Baobab SHOULD support a `RegulatoryConcept` identity for legally relevant concepts whose meaning may itself be defined by law.

Examples:

```text
importer

exporter

beneficial owner

personal information

food product

originating product

resident

employee
```

---

# 47. Concept Is Not Universal Meaning

A concept's legal definition may differ by:

```text
jurisdiction

regime

instrument

effective period
```

Therefore:

```text
"importer"
```

SHALL NOT have one eternal global definition.

---

# 48. Constitutive Rules

LegalRuleML distinguishes **constitutive rules**, which define institutional concepts or facts, from **prescriptive rules**, which impose normative effects such as obligations, permissions or prohibitions.

Baobab SHALL preserve this distinction.

---

# 49. RegulatoryInterpretation

`RegulatoryInterpretation` SHALL remain a first-class aggregate root as established in ADR-REG-0003.

Conceptually:

```text
RegulatoryInterpretation
├── id
├── source_provision_refs[]
├── interpretation_kind
├── structured_meaning
├── narrative
├── assumptions[]
├── ambiguity_state
├── alternative_interpretation_refs[]
├── jurisdiction_scope
├── domain_scope
├── review_state
├── scope
├── valid_from
├── valid_to?
└── provenance
```

---

# 50. Interpretation Aggregate Boundary

An interpretation owns:

```text
meaning

assumptions

identified ambiguity

review state

interpretive provenance
```

It SHALL NOT own:

```text
the source provision

the machine rule

the final transaction assessment.
```

---

# 51. Many-to-Many Provision/Interpretation Relationships

One interpretation MAY depend on:

```text
several provisions.
```

One provision MAY support:

```text
several interpretations.
```

The model SHALL therefore support N:M relationships.

---

# 52. Many-to-Many Provision/Rule Relationships

LegalRuleML explicitly supports N:M linkage between machine rules and textual provisions: a provision may contain multiple rules, and a rule may derive from several provisions.

Baobab SHALL support this structure.

Rejected:

```text
rule.provision_id
```

as the only possible relationship.

Preferred:

```text
RegulatoryRule
   * ───────── * ProvisionVersion
```

through explicit provenance relationships.

---

# 53. RegulatoryRule

`RegulatoryRule` SHALL represent a canonical machine-evaluable formulation of regulatory meaning.

Conceptually:

```text
RegulatoryRule
├── id
├── rule_kind
├── regulatory_domain
├── interpretation_refs[]
├── provision_refs[]
├── regime_refs[]
├── jurisdiction_scope
├── subject_scope
├── applicability_expression
├── effect_template
├── exception_refs[]
├── priority_relations[]
├── assurance_state
├── max_effect_class
├── effective_from
├── effective_to?
├── rule_version
└── provenance
```

---

# 54. Rule Kind

At the highest legal-semantic level:

```text
CONSTITUTIVE

PRESCRIPTIVE
```

SHALL be supported.

LegalRuleML uses precisely this distinction.

---

# 55. Rule Function

Separate from legal rule kind, Baobab MAY classify operational function:

```text
DEFINITION

CLASSIFICATION

ELIGIBILITY

PROCEDURAL

CALCULATION

DOCUMENTARY

REPORTING

LICENSING

PROHIBITION

DEADLINE

DISCLOSURE

RETENTION
```

This taxonomy SHALL NOT replace legal semantics.

---

# 56. Rule Is General

A RegulatoryRule describes a general regulatory norm.

Example conceptually:

```text
IF
    person imports controlled commodity X
INTO
    jurisdiction Y
THEN
    importer must hold permit P
```

It does NOT mean:

```text
ZuriBeans shipment SHP-001 currently requires P.
```

That conclusion requires applicability evaluation.

---

# 57. ApplicabilityCriterion

`ApplicabilityCriterion` SHALL describe one condition relevant to whether a rule applies.

Examples:

```text
jurisdiction = ZA

activity = IMPORT

commodity_class = X

transaction_value > threshold

entity_type = importer

effective_date within interval
```

---

# 58. Criteria Are Rule Components

Applicability criteria SHOULD ordinarily be subordinate to rules rather than independent aggregate roots.

They MAY be reusable definitions where semantics justify reuse.

---

# 59. RuleCondition

`RuleCondition` SHALL capture positive preconditions.

Conceptually:

```text
WHEN fact A
AND fact B
AND fact C
```

---

# 60. RuleException

`RuleException` SHALL capture exclusions or defeaters.

Conceptually:

```text
Rule applies
UNLESS
condition X.
```

It SHALL not be represented merely by:

```text
condition = false.
```

where doing so destroys legal meaning.

---

# 61. Exception Is Not Permission

An exemption from an obligation is not always equivalent to a general permission.

The domain SHALL preserve that distinction.

---

# 62. NormativeEffectTemplate

A prescriptive rule SHALL describe the normative consequence that arises when applicability is satisfied.

Conceptually:

```text
NormativeEffectTemplate
├── effect_type
├── bearer_role
├── action
├── object_ref/type
├── beneficiary?
├── deadline_rule?
├── evidence_requirement?
├── violation_consequence?
└── parameters
```

---

# 63. Core Normative Effect Types

The canonical model SHALL support at least:

```text
OBLIGATION

PERMISSION

PROHIBITION
```

because these are fundamental LegalRuleML deontic categories.

The model SHOULD be extensible to:

```text
ENTITLEMENT

POWER / COMPETENCE

RIGHT

LIABILITY

IMMUNITY
```

where later regulatory domains require them.

---

# 64. Requirement Is Not Necessarily a Fundamental Deontic Operator

Baobab SHALL distinguish:

```text
legal normative effect
```

from:

```text
operational requirement needed to satisfy that effect.
```

Example:

```text
Obligation:
importer must demonstrate origin.

Operational Requirements:
certificate of origin
supporting supplier declaration
```

---

# 65. RegulatoryRequirement

`RegulatoryRequirement` SHALL therefore represent a concrete requirement arising from a regulatory effect.

Potential kinds:

```text
DOCUMENT

PERMIT

LICENCE

CERTIFICATE

DECLARATION

FILING

DISCLOSURE

PAYMENT

INSPECTION

TEST

REGISTRATION

RECORD_RETENTION

REPORT

APPROVAL
```

---

# 66. Rule Template versus Effect Instance

This distinction is fundamental:

```text
REGULATORY RULE
    general norm

        ↓ applied to context

REGULATORY EFFECT
    contextualised normative consequence.
```

---

# 67. RegulatoryEffect

`RegulatoryEffect` SHALL be an independently addressable derived object where persistence or workflow requires it.

Conceptually:

```text
RegulatoryEffect
├── id
├── effect_type
├── rule_ref
├── assessment_ref
├── subject_ref
├── context_ref
├── bearer_ref/role
├── object_ref?
├── requirement_refs[]
├── effective_from
├── effective_to?
├── due_at?
├── satisfaction_state?
└── provenance
```

---

# 68. RegulatoryEffect Examples

Examples include:

```text
ZuriBeans must provide Certificate X
for Shipment SHP-100.

Product P may not be imported into ZA.

Importer L is permitted to use procedure Y.

Legal entity A must file report R by date D.
```

These are contextual effects.

---

# 69. Obligation Instance

An obligation is therefore:

```text
a RegulatoryEffect
where:
effect_type = OBLIGATION
```

It is distinct from the general rule that generated it.

---

# 70. Prohibition Instance

Likewise:

```text
effect_type = PROHIBITION
```

can represent:

> this transaction is prohibited under Rule R.

---

# 71. Permission Instance

A permission can represent:

> this action is expressly permitted under Rule R.

Absence of prohibition SHALL NOT automatically create a permission object.

---

# 72. Effect Lifecycle

Potential state for obligation-type effects MAY include:

```text
PENDING

SATISFIED

WAIVED

EXEMPTED

VIOLATED

EXPIRED

SUPERSEDED

CANCELLED
```

Detailed semantics belong in ADR-REG-0008/0009.

---

# 73. Effect Does Not Own Operational Object

A RegulatoryEffect may reference:

```text
shipment_id
```

but SHALL not own the shipment.

Trade remains authoritative for shipment state.

---

# 74. RegulatoryContext

`RegulatoryContext` SHALL be the immutable evaluation input envelope.

It SHALL combine:

```text
resolved Baobab PlatformContext

+

domain facts required for regulatory evaluation.
```

---

# 75. RegulatoryContext Structure

Conceptually:

```text
RegulatoryContext
├── context_id
├── platform_context_ref
├── tenant_ref
├── legal_entity_ref?
├── organisation_ref?
├── market_refs[]
├── jurisdiction_refs[]
├── trade_lane_ref?
├── operation_type
├── subject_refs[]
├── product_refs[]
├── counterparty_refs[]
├── origin
├── destination
├── transit_geographies[]
├── classification_refs[]
├── currency?
├── value?
├── quantity?
├── effective_at
├── evidence_refs[]
└── facts[]
```

Not every domain populates every field.

---

# 76. Regulatory Context Is Not Platform Context

```text
PlatformContext
```

answers:

> Who/where/which tenant/capability?

`RegulatoryContext` answers:

> What legally relevant facts are being evaluated?

The latter may include shipment or product facts unavailable to Control Plane.

---

# 77. Context Is Immutable per Assessment

Once assessment begins:

```text
RegulatoryContext v1
```

SHALL remain stable.

Changed facts require:

```text
RegulatoryContext v2
```

or a new assessment context.

---

# 78. RegulatoryFactSnapshot

A consequential assessment SHALL preserve relevant evaluated facts.

Conceptually:

```text
RegulatoryFactSnapshot
├── fact_key
├── value
├── value_type
├── source_ref
├── canonical_object_ref?
├── observed_at?
├── effective_at?
└── provenance
```

---

# 79. Facts Are Not Master Data

A snapshot of:

```text
product origin = UG
```

does not make Regulations the product master.

It records what the assessment evaluated.

---

# 80. Source of Facts

Facts MAY originate from:

```text
Trade

ERP

Control Plane

customer input

official authority

Regulations-derived classification

human reviewer
```

Their provenance SHALL be retained.

---

# 81. ApplicabilityResult

Applicability evaluation SHALL produce explicit results.

Potential:

```text
APPLIES

DOES_NOT_APPLY

POTENTIALLY_APPLIES

INDETERMINATE
```

The exact ADR-REG-0017 semantics remain deferred.

---

# 82. Applicability Is Rule-Specific

An assessment may contain:

```text
Rule A → APPLIES

Rule B → DOES_NOT_APPLY

Rule C → INDETERMINATE
```

rather than one global applicability Boolean.

---

# 83. RegulatoryAssessment

`RegulatoryAssessment` SHALL be an aggregate root.

It represents a bounded evaluation of a specific regulatory context against a defined regulatory profile/rule set.

Conceptually:

```text
RegulatoryAssessment
├── id
├── regulatory_context_snapshot
├── profile_ref
├── rule_set_ref/version
├── effective_at
├── evaluated_at
├── applied_rule_refs[]
├── non_applicable_rule_refs[]
├── applicability_results[]
├── effect_refs[]
├── missing_facts[]
├── missing_evidence[]
├── conflicts[]
├── outcome
├── assurance
├── lifecycle_state
└── provenance
```

---

# 84. Assessment Aggregate Boundary

An Assessment owns its:

```text
evaluation input snapshot

rule-set identity

applicability findings

evaluation outcome

unresolved issues
```

It references rather than embeds full:

```text
rules

instruments

operational business objects.
```

---

# 85. Assessment Is Immutable After Issue

A completed assessment SHALL not have its meaning silently modified.

Changed context or rules produce:

```text
new assessment.
```

---

# 86. Assessment Outcome

As established in ADR-REG-0004:

```text
SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE
```

---

# 87. Assessment Is Not Decision

An assessment determines regulatory findings.

A `RegulatoryDecision` determines the operationally consumable regulatory disposition under effect policy.

---

# 88. RegulatoryDecision

`RegulatoryDecision` SHALL be a separate aggregate root.

Conceptually:

```text
RegulatoryDecision
├── id
├── assessment_ref
├── outcome
├── effect_class
├── disposition
├── reason_codes[]
├── review_requirement
├── max_authorised_action
├── effect_policy_version
├── rule_set_version
├── validity
├── status
├── issued_at
├── supersedes?
└── provenance
```

---

# 89. Why Decision Is Separate Aggregate

A decision can independently be:

```text
reviewed

overridden

suspended

superseded

challenged

enforced
```

while the assessment that produced it remains unchanged.

---

# 90. Decision State

Possible lifecycle:

```text
ISSUED

UNDER_REVIEW

CONFIRMED

OVERRIDDEN

SUSPENDED

SUPERSEDED

EXPIRED

INVALIDATED
```

---

# 91. Decision Does Not Own Enforcement

Operational enforcement remains owned by:

```text
Trade

ERP

CMS

IAM

future domain engine.
```

Regulations records decision authority.

---

# 92. RegulatoryProfile

`RegulatoryProfile` SHALL represent a governed composition of regulatory domains/rules for a business purpose.

Examples:

```text
CROSS_BORDER_GOODS

FOOD_IMPORT

DATA_PROTECTION

PRODUCT_MARKET_ENTRY

FINANCIAL_SERVICES
```

---

# 93. Profile Structure

Conceptually:

```text
RegulatoryProfile
├── id
├── key
├── name
├── purpose
├── domains[]
├── supported_context_types[]
├── rule_selection_policy
├── source_coverage_requirements
├── lifecycle_state
├── valid_from
├── valid_to?
└── version
```

---

# 94. Profile Is Not Jurisdiction

Do NOT define:

```text
SouthAfricaProfile
```

as the only modelling mechanism.

Prefer composition:

```text
CrossBorderGoodsProfile
+
ZA jurisdiction
+
UG origin
```

---

# 95. Profile Is Not Product Subscription

A regulatory profile describes regulatory evaluation semantics.

Commercial products may package profiles.

They are distinct concepts.

---

# 96. Regulatory Pack

A future `JurisdictionPack` or `DomainPack` defined by ADR-REG-0029 MAY compose:

```text
profile

rules

coverage

sources

commercial entitlement
```

without changing the canonical domain.

---

# 97. RegulatoryConcept versus Classification Scheme

Regulations SHALL distinguish:

```text
legal concepts
```

from external classification schemes such as:

```text
HS classifications

tariff nomenclature

industry codes

product standards codes.
```

---

# 98. ClassificationReference

The core model SHOULD permit:

```text
ClassificationReference
├── scheme
├── code
├── version
├── authority
└── effective_at
```

without requiring Regulations to become the product master.

Detailed trade classification belongs in ADR-REG-0027.

---

# 99. RegulatoryChange

`RegulatoryChange` SHALL be an aggregate root representing a verified material change in regulatory state.

Conceptually:

```text
RegulatoryChange
├── id
├── change_type
├── affected_object_refs[]
├── source_change_refs[]
├── detected_at
├── verified_at?
├── effective_at?
├── significance
├── lifecycle_state
└── provenance
```

---

# 100. Change Types

Potential:

```text
ENACTED

AMENDED

REPEALED

COMMENCED

CORRECTED

SOURCE_CORRECTED

INTERPRETATION_CHANGED

RULE_CHANGED

EFFECTIVE_DATE_CHANGED

AUTHORITY_CHANGED

COVERAGE_CHANGED
```

---

# 101. Source Change Is Not Necessarily Legal Change

This distinction from ADR-REG-0005 remains mandatory.

```text
PDF formatting changed
```

does not necessarily mean:

```text
regulation changed.
```

---

# 102. Interpretation Change Is Not Necessarily Legal Change

Similarly:

```text
Baobab corrected interpretation
```

must be distinguishable from:

```text
Parliament amended law.
```

---

# 103. RegulatoryImpact

`RegulatoryImpact` SHALL represent the result of analysing what may be affected by a verified regulatory change.

Conceptually:

```text
RegulatoryImpact
├── id
├── change_ref
├── impact_scope
├── affected_rule_refs[]
├── affected_profile_refs[]
├── affected_context_refs[]
├── affected_object_refs[]
├── assessment_state
├── severity
└── generated_at
```

---

# 104. Impact Is Not Commercial Intelligence

Regulations may determine:

```text
these shipments are affected.
```

Pulse may determine:

```text
this creates a strategic supply opportunity.
```

The distinction remains.

---

# 105. RegulatoryVerification

Verification SHALL be represented as explicit domain activity/state.

Potential subjects include:

```text
source

instrument

provision

interpretation

rule

classification

decision.
```

---

# 106. Verification Record

Conceptually:

```text
RegulatoryVerification
├── id
├── subject_ref
├── verification_type
├── verifier
├── method
├── result
├── performed_at
├── evidence_refs[]
└── notes/reference
```

---

# 107. Verification Is Not Generic Approval

Different verification types answer different questions:

```text
SOURCE_AUTHENTICITY

INTERPRETATION_REVIEW

RULE_IMPLEMENTATION

CLASSIFICATION_REVIEW

EFFECT_POLICY_APPROVAL
```

---

# 108. RegulatoryEvidence

The core model SHOULD use references to evidence rather than embedding arbitrary documents throughout entities.

A `RegulatoryEvidenceRef` MAY refer to:

```text
SourceArtefact

authority determination

tenant document

professional opinion

test result

permit

certificate

licence.
```

---

# 109. Evidence Is Contextual

The same document may:

```text
support one obligation

fail to satisfy another.
```

Evidence relation semantics matter.

---

# 110. RegulatoryEvidenceBundle

A decision MAY later expose a bundle containing:

```text
context snapshot

source citations

rules

interpretations

evidence

assessment

decision

review / override
```

The detailed chain belongs in ADR-REG-0014.

---

# 111. Aggregate Root Catalogue

The initial canonical aggregate roots SHALL be:

```text
1. RegulatoryAuthority

2. RegulatoryRegime

3. RegulatoryInstrument

4. RegulatoryProvision

5. RegulatoryInterpretation

6. RegulatoryRule

7. RegulatoryProfile

8. RegulatoryEffect

9. RegulatoryAssessment

10. RegulatoryDecision

11. RegulatoryChange

12. RegulatoryImpact
```

Source Fabric aggregates established by ADR-REG-0005 remain part of the engine but are separately governed.

---

# 112. Why Provision Is Independently Addressable

Although structurally contained within an instrument, a provision must support:

```text
individual citations

individual versioning

individual amendments

individual interpretations

individual rule mappings

individual impact analysis.
```

Therefore it SHALL be independently addressable.

---

# 113. Why Provision Need Not Be Separate Microservice

Independent aggregate identity does NOT imply:

```text
provision-service.
```

Baobab Regulations SHOULD initially remain a modular engine.

---

# 114. Aggregate Rules

Aggregate roots SHALL own local consistency.

Cross-aggregate relationships SHALL usually be:

```text
identity references

+

events

+

eventual consistency
```

rather than one giant transactional graph.

---

# 115. No Giant Legal Aggregate

Rejected:

```text
RegulatoryInstrument
    contains all provisions
    contains all interpretations
    contains all rules
    contains all assessments
    contains all decisions
```

This becomes unmanageable.

---

# 116. No Fully Fragmented Records

Also rejected:

```text
everything is a generic node
with arbitrary JSON and arbitrary edges.
```

That destroys local invariants.

---

# 117. Aggregate Reference Principle

Example:

```text
RegulatoryRule
```

references:

```text
interpretation_id
provision_id
```

rather than embedding the complete mutable objects.

---

# 118. Aggregate Versioning

Material aggregates SHOULD carry:

```text
revision
```

for technical optimistic concurrency where mutable governance state exists.

This technical revision SHALL remain distinct from:

```text
legal version

rule version

effective period.
```

---

# 119. Legal Version versus Technical Revision

Example:

```text
Rule legal version:
2

Database aggregate revision:
17
```

These are not the same.

---

# 120. Stable Identity

Canonical IDs SHALL be immutable.

Suggested conceptual prefixes MAY include:

```text
regauth_

regime_

reginst_

regexp_

regprov_

reginterp_

regrule_

regprofile_

regeffect_

regassess_

regdec_

regchange_

regimpact_
```

Exact grammar belongs in Shared contract design.

---

# 121. Provider IDs Are Never Canonical IDs

Example:

```text
Thomson ID 837182
```

maps to:

```text
ExternalReference
```

not:

```text
regrule_837182.
```

---

# 122. Language

Legal expression language SHALL be explicit.

The domain SHALL not assume English.

This is necessary for continental expansion.

---

# 123. Translation Relationship

Expressions SHALL support:

```text
IS_TRANSLATION_OF

HAS_TRANSLATION
```

relationships.

ELI similarly models translation relationships between legal expressions.

---

# 124. Official versus Unofficial Translation

The model SHALL distinguish:

```text
OFFICIAL_TRANSLATION

UNOFFICIAL_TRANSLATION

MACHINE_TRANSLATION.
```

---

# 125. Multilingual Rule Interpretation

Baobab may derive one canonical interpretation from:

```text
several official language expressions
```

where jurisdictional policy requires comparison.

All source expressions SHALL remain linked.

---

# 126. Temporal Requirements

The canonical model SHALL include temporal fields from day one even though ADR-REG-0015 defines detailed semantics.

At minimum objects SHOULD be capable of carrying:

```text
published_at

effective_from

effective_to

valid_from

valid_to

repealed_at

superseded_at

observed_at

recorded_at.
```

---

# 127. Effective Time versus Knowledge Time

The model SHALL be capable of later answering:

```text
What law applied?
```

and:

```text
What did Baobab know?
```

These require different timelines.

Detailed bitemporal behaviour is deferred.

---

# 128. Effective Dates Belong at Multiple Levels

An:

```text
instrument

provision

rule

interpretation
```

may each have different relevant temporal states.

The model SHALL not assume instrument dates alone are sufficient.

---

# 129. Jurisdiction Scope

A rule MAY apply to:

```text
one jurisdiction

several jurisdictions

regional regime

specific territorial subdivision

subject-matter jurisdiction.
```

Therefore jurisdiction scope SHALL be modeled as references, not one country string.

---

# 130. Subject Scope

A rule MAY apply to:

```text
importer

exporter

manufacturer

data controller

employer

financial institution

specific product class

specific transaction type.
```

Subject semantics SHALL therefore be explicit.

---

# 131. RegulatedActivity

The canonical model SHOULD support a stable controlled vocabulary for regulated activities.

Potential initial activities:

```text
IMPORT

EXPORT

SELL

BUY

MANUFACTURE

STORE

TRANSPORT

PROCESS_DATA

TRANSFER_DATA

EMPLOY

ADVERTISE

PUBLISH

REPORT

FILE

PAY

REGISTER
```

Exact taxonomy belongs in detailed domain design.

---

# 132. Activities Are Contextual

A single transaction may involve:

```text
EXPORT from UG

IMPORT into ZA

TRANSPORT through transit territory

SELL to customer
```

Several regulatory rules may therefore apply simultaneously.

---

# 133. Actor/Bearer

Normative effects SHALL identify the legal role that bears the obligation.

Example:

```text
IMPORTER

EXPORTER

EMPLOYER

CONTROLLER

MANUFACTURER.
```

This is not necessarily identical to:

```text
legal_entity_id.
```

---

# 134. Role Resolution

Assessment resolves:

```text
canonical legal entity
```

into:

```text
regulatory role
```

for the evaluated context.

Example:

```text
ZuriBeans Uganda
    acts_as
EXPORTER.
```

---

# 135. Bearer Role Is Not Permanent Entity Attribute

A legal entity may be:

```text
exporter in one transaction

importer in another

seller in another.
```

Do not persist:

```text
legal_entity.role = EXPORTER
```

globally.

---

# 136. Counterparty Context

Regulatory rules MAY depend on counterparty attributes.

Regulations SHALL reference canonical counterparty identities where available.

It SHALL not create another customer/supplier master.

---

# 137. Product Context

Regulations SHALL reference canonical product identities and classifications.

It SHALL not become:

```text
Trade catalogue.
```

---

# 138. Transaction Context

A regulatory assessment MAY reference:

```text
order

shipment

invoice

declaration

contract

payment
```

through canonical/external references.

Regulations does not own them.

---

# 139. Evidence Requirement

A RegulatoryRequirement MAY specify:

```text
evidence_type

issuer requirement

validity condition

document condition

effective period
```

without storing the operational document itself.

---

# 140. Regulatory Document versus Evidence Document

Distinguish:

```text
Government regulation PDF
```

from:

```text
Certificate of Origin submitted by trader.
```

The former is a regulatory source artefact.

The latter is evidence satisfying an obligation.

These belong to different semantic roles.

---

# 141. Authority Determination

The model SHOULD support an external:

```text
AuthorityDetermination
```

concept or typed evidence/reference for:

```text
advance ruling

customs ruling

permit decision

tax ruling

regulator decision.
```

Such determinations may affect context-specific applicability.

---

# 142. Authority Determination Is Not Generic Rule

A ruling applicable only to:

```text
Company A + Product X
```

SHALL not become:

```text
global law.
```

---

# 143. Tenant Scope

Regulatory knowledge SHALL distinguish:

```text
PLATFORM_SHARED

TENANT_PRIVATE

TENANT_OVERRIDE

CUSTOMER_COUNSEL

EXTERNAL_AUTHORITY
```

or semantically equivalent scopes.

---

# 144. Public Regulatory Knowledge

Generally applicable authoritative regulation MAY be shared across tenants where rights permit.

It SHOULD NOT be duplicated:

```text
once per tenant.
```

---

# 145. Tenant Private Knowledge

Tenant-specific:

```text
legal opinions

regulatory correspondence

rulings

permits

private interpretations

internal policies
```

SHALL remain tenant-scoped.

---

# 146. Tenant Override Does Not Mutate Shared Law

Example:

```text
Platform interpretation v3
```

remains unchanged if Tenant A adopts:

```text
Counsel Interpretation C12.
```

The tenant overlay references the shared source and records its alternative interpretation.

---

# 147. Shared Rule and Tenant Effect Policy

A single verified rule may support:

```text
Tenant A:
E2 review

Tenant B:
E4 automatic hold
```

without creating two versions of the underlying law.

---

# 148. Security Classification Is Separate from Knowledge Scope

For example:

```text
source = public law

interpretation = platform internal

tenant legal opinion = tenant confidential.
```

These classification levels SHALL remain independently modelled.

---

# 149. Source Rights Are Separate Again

A source can be:

```text
legally public
```

but have:

```text
licensed commercial annotation
```

whose redistribution is restricted.

Knowledge scope and licence rights SHALL remain separate.

---

# 150. Regulatory Graph

The canonical model forms a logical graph.

Example:

```text
Authority
   │ ISSUED
   ▼
Instrument
   │ CONTAINS
   ▼
Provision
   │ INTERPRETED_BY
   ▼
Interpretation
   │ ENCODED_AS
   ▼
Rule
   │ APPLIED_IN
   ▼
Assessment
   │ PRODUCED
   ▼
Decision
```

---

# 151. Graph Database Is Not Required

This ADR explicitly rejects:

```text
regulatory data is connected
therefore Neo4j.
```

A relational implementation may model these relationships perfectly well initially.

Technology selection remains separate.

---

# 152. Graph Projection

A future graph store MAY become a derived projection for:

```text
impact analysis

legal dependency traversal

explanation

source lineage

knowledge navigation.
```

It need not become system of record.

---

# 153. Relationship Identity

Important relationships SHOULD be independently identifiable where they carry:

```text
effective dates

provenance

verification

review

scope.
```

Simple structural relationships need not all become aggregates.

---

# 154. Typed Edges

Baobab SHOULD avoid:

```text
relationship_type = "other"
```

for legally consequential edges.

Semantics matter.

---

# 155. Rule Precedence

The core model SHALL permit explicit:

```text
OverrideRelation
```

or equivalent.

Detailed legal hierarchy and rule priority belong in ADR-REG-0007/0009.

---

# 156. Defeasibility

LegalRuleML explicitly models defeasible rules and priority/override relationships.

Baobab SHALL therefore avoid a rule representation incapable of expressing:

```text
rule applies normally
unless exception
unless stronger rule overrides it.
```

---

# 157. Violation

The core model SHOULD be extensible to represent:

```text
RegulatoryViolation
```

where an applicable obligation is not satisfied.

However detailed violation/remediation semantics are deferred.

---

# 158. Reparative Obligation

LegalRuleML recognises that violations may trigger subsequent obligations, including reparative obligations.

Baobab's model SHALL not prevent:

```text
Violation of Rule A
      ↓
triggers
      ↓
Obligation B.
```

---

# 159. Procedure

Regulation frequently prescribes processes:

```text
register

submit

inspect

approve

declare

retain.
```

Baobab MAY model these as structured requirements/effect sequences.

It SHALL not become a general workflow engine.

---

# 160. Deadline

Deadlines SHALL be explicit where legally meaningful.

A deadline MAY be:

```text
absolute date

duration from event

business-day calculation

periodic obligation.
```

Detailed temporal calculation is deferred.

---

# 161. Monetary Threshold

Rules may depend on:

```text
transaction value
currency
threshold
```

The rule SHALL identify:

```text
threshold value

currency

effective period

conversion rule where applicable.
```

---

# 162. Calculation

Statutory calculations SHOULD be expressible as versioned rule logic.

Examples:

```text
duty

tax

penalty

deadline

percentage

quota.
```

---

# 163. Calculation Result

A calculation result is derived assessment evidence.

It SHALL preserve:

```text
formula version

inputs

rounding

result.
```

---

# 164. Assessment Rule Set

Every assessment SHALL identify a stable:

```text
rule_set_version
```

or equivalent immutable collection fingerprint.

This is essential for replay.

---

# 165. RuleSet

A `RegulatoryRuleSet` MAY exist as a versioned composition artefact.

Conceptually:

```text
RegulatoryRuleSet
├── id
├── profile_ref
├── rule_versions[]
├── generated_at
├── effective_scope
└── fingerprint
```

Whether it becomes an aggregate root is deferred to ADR-REG-0016/0018.

---

# 166. Rule Set Is Not Regulatory Profile

Profile:

```text
what kinds of rules should be considered.
```

Rule set:

```text
which concrete rule versions were evaluated.
```

---

# 167. Assessment Snapshot

A completed assessment SHALL preserve enough state to replay:

```text
context snapshot

rule-set identity

evidence refs

effect-policy version

engine version.
```

---

# 168. Immutability Principle

Published:

```text
ProvisionVersion

Interpretation Version

Rule Version

Assessment

Decision
```

SHALL ordinarily be immutable in semantic content.

Corrections create new versions/records.

---

# 169. Mutable Governance State

Fields such as:

```text
review assignment

draft status

workflow status
```

may change.

That does not justify rewriting published semantics.

---

# 170. Retention

Historical regulatory knowledge SHALL remain retained according to:

```text
legal need

audit requirement

source rights

tenant retention

platform policy.
```

Detailed retention belongs later.

---

# 171. Domain Events

Aggregate changes MAY produce canonical events such as:

```text
regulation.instrument.published

regulation.provision.changed

regulation.interpretation.verified

regulation.rule.published

regulation.effect.created

regulation.assessment.completed

regulation.decision.issued

regulation.change.verified

regulation.impact.detected
```

Exact contracts belong in Shared.

---

# 172. Events Reference Aggregate IDs

Events SHOULD contain:

```text
aggregate ID

version

context

correlation

causation
```

rather than embedding complete mutable domain graphs.

---

# 173. Cross-Engine Contract Promotion

Internal Regulations domain classes SHALL NOT automatically be copied into Shared.

Shared SHOULD receive only cross-engine contracts required by consumers.

---

# 174. Likely Shared References

Potential:

```text
RegulatoryAssessmentRef

RegulatoryDecisionRef

RegulatoryEffectRef

RegulatoryOutcome

RegulatoryDisposition

RegulatoryAssuranceSummary

RegulatoryChangeEvent

RegulatoryImpactEvent
```

---

# 175. Internal Domain Richer Than Shared Contract

The Regulations internal model may contain:

```text
legal hierarchy

interpretive history

source graph

rule compiler representation.
```

Trade does not need all of it.

---

# 176. API Projection

A consumer may receive:

```text
decision

obligations

requirements

citations

assurance
```

without receiving the complete internal regulatory graph.

---

# 177. Query Model

Read APIs SHOULD support projections such as:

```text
instrument view

provision history

rule explanation

obligation list

assessment evidence

decision explanation

regulatory change timeline
```

without changing aggregate ownership.

---

# 178. Search Model

Search MAY index:

```text
instrument titles

provision text

concepts

interpretations

rules.
```

Search indexes remain derived.

---

# 179. Vector Model

Embeddings MAY support retrieval.

They SHALL never become canonical identity or authority.

---

# 180. Canonical Model Technology Neutrality

No canonical entity SHALL depend upon:

```text
PostgreSQL table name

Neo4j label

Haystack Document

OPA policy package

LLM response type

RegGenome requirement ID

Thomson Reuters DTO.
```

---

# 181. Persistence Deferral

This ADR does NOT choose:

```text
PostgreSQL

graph database

document store

vector database.
```

The domain comes first.

---

# 182. Implementation Bias

A relational authoritative store is likely to be suitable for many of these strongly versioned entities.

That is an implementation inference, not a decision of this ADR.

---

# 183. No Generic JSON Blob Model

Rejected:

```text
RegulatoryObject
├── type
└── payload JSONB
```

for the entire domain.

JSONB may support extensions.

It SHALL not substitute for core semantics.

---

# 184. No Single `ComplianceRule`

Rejected:

```text
ComplianceRule
├── country
├── condition
├── result
```

This loses:

```text
authority

instrument

provision

interpretation

legal hierarchy

temporal state

provenance.
```

---

# 185. No `CountryRule`

Rejected because:

```text
country
≠
jurisdiction
≠
regime.
```

---

# 186. No `RegulationDocument`

Rejected as the central entity.

A document file is only one representation layer.

---

# 187. No `Law = PDF`

Explicitly rejected.

---

# 188. No Generic "Compliance Item"

Rejected as primary ontology.

It conceals whether the item is:

```text
law

obligation

evidence

policy

interpretation

decision.
```

---

# 189. No Vendor Requirement as Canonical Rule

Rejected.

Vendor requirement objects enter through mapping and provenance.

---

# 190. No Tenant-Copied Law

Rejected:

```text
Tenant A regulations table

Tenant B regulations table

Tenant C regulations table.
```

Shared regulation should remain shared where permissible.

---

# 191. No Market-Copied Law

Rejected:

```text
market_za.rules
```

as canonical architecture.

Rules attach to jurisdictions/regimes and applicability contexts.

---

# 192. No Rule-Owned Operational Entity

Rejected:

```text
RegulatoryRule.shipment
```

as direct domain ownership.

Use canonical references.

---

# 193. No Mutable "Current Law" Only

Rejected.

Historical versions are foundational.

---

# 194. No Single Authority Score

Rejected consistently with ADR-REG-0003.

Authority is semantic and multidimensional.

---

# 195. No Single Compliance Boolean

Rejected:

```text
compliant = true.
```

Baobab should answer:

```text
compliant with which evaluated obligations
under which rule set
for which context
at which time?
```

---

# 196. Example — Cross-Border Goods

Conceptually:

```text
Authority
   │
   ▼
Instrument
   │
   ▼
Provision:
"Importers of category X require permit P"
   │
   ▼
Interpretation
   │
   ▼
Rule
   │
   ├── jurisdiction = ZA
   ├── activity = IMPORT
   ├── product_class = X
   └── effect = OBLIGATION
                       │
                       ▼
                  Assessment
                       │
                       ├── importer = ZuriBeans entity
                       ├── product = P123
                       ├── destination = ZA
                       └── permit missing
                       │
                       ▼
                RegulatoryEffect
                       │
                       ▼
        "Importer must provide permit P"
                       │
                       ▼
                   Decision
                       │
                       ▼
            REQUIRE_EVIDENCE / E3
```

---

# 197. Example — Exemption

```text
General Rule
   │
   ▼
Permit required

Exception Rule
   │
   ▼
unless quantity < statutory threshold
and goods satisfy category Y
```

Assessment must evaluate both.

It SHALL not simply see:

```text
permit required
```

and stop.

---

# 198. Example — Constitutive Rule

```text
Provision:
"For purposes of this regulation,
an importer means ..."
        │
        ▼
Constitutive Rule
        │
        ▼
defines RegulatoryConcept:
IMPORTER
```

That definition may determine who bears later obligations.

---

# 199. Example — Multiple Provisions

A duty rule MAY derive from:

```text
Section 3:
defines controlled goods

Section 12:
requires permit

Schedule 4:
lists products.
```

Therefore one executable rule may legitimately reference all three.

---

# 200. Example — Multiple Rules per Provision

One provision may state:

```text
importer must register

importer must keep records

importer must report annually.
```

Baobab may derive three regulatory rules.

This is why N:M mapping is required.

---

# 201. Example — Multiple Jurisdictions

A Uganda → South Africa transaction may resolve:

```text
UG export rules

regional origin regime

transit rules

ZA import rules

SPS rules

customs rules.
```

One assessment therefore operates against several applicable regulatory regimes.

---

# 202. Example — Market versus Jurisdiction

Commercial destination:

```text
South African market.
```

Regulatory context might include:

```text
South Africa national jurisdiction

specific customs regime

regional trade regime

municipal product rule
```

Market alone is insufficient.

---

# 203. Example — Tenant Counsel Overlay

```text
Shared source provision
      │
      ├── Platform Interpretation A
      │
      └── Tenant Counsel Interpretation B
```

Tenant B's assessment may use its authorised interpretation.

The source provision remains shared.

---

# 204. Example — Authority Ruling

```text
General rule:
classification ambiguous

Authority ruling:
Product P classified as code X
for Legal Entity L
        │
        ▼
Assessment uses ruling
for its valid scope.
```

The ruling SHALL not automatically classify every customer's product P equivalent.

---

# 205. Domain Integrity Rule — Authority

An Instrument MUST have identifiable provenance to its authority/source state before high-assurance use.

---

# 206. Domain Integrity Rule — Provision

A Provision MUST belong to an Instrument.

---

# 207. Domain Integrity Rule — Provision Version

A published ProvisionVersion MUST identify its:

```text
provision

effective/version state

source expression/artefact.
```

---

# 208. Domain Integrity Rule — Interpretation

A production Interpretation MUST reference at least one supporting regulatory source/provision.

---

# 209. Domain Integrity Rule — Rule

A production Rule MUST reference:

```text
interpretation/source lineage

rule version

applicability semantics

normative or constitutive effect.
```

---

# 210. Domain Integrity Rule — Effect

A RegulatoryEffect MUST identify the rule from which it derives.

---

# 211. Domain Integrity Rule — Assessment

A completed Assessment MUST identify:

```text
context

effective time

rule set.
```

---

# 212. Domain Integrity Rule — Decision

A Decision MUST identify:

```text
assessment

effect class

effect policy version.
```

---

# 213. Domain Integrity Rule — Change

A verified Change MUST identify what regulatory object/state changed.

---

# 214. Domain Integrity Rule — Impact

An Impact MUST identify the Change that produced it.

---

# 215. Domain Integrity Rule — Cross-Tenant Knowledge

Tenant-private interpretation or evidence MUST NOT silently influence another tenant.

---

# 216. Domain Integrity Rule — Historical State

Published historical objects SHALL remain reconstructable after supersession.

---

# 217. Domain Integrity Rule — Provider Independence

No aggregate ID SHALL depend on provider-native identity.

---

# 218. Domain Integrity Rule — Context Ownership

Regulations SHALL not promote temporary transaction context into new master data unless the authoritative domain explicitly supplies it.

---

# 219. Domain Integrity Rule — Unknown

Unknown values SHALL remain:

```text
UNKNOWN
```

or absent/indeterminate according to schema.

They SHALL not be invented from correlated values.

---

# 220. Null Is Not False

Example:

```text
exemption_known = null
```

SHALL not automatically equal:

```text
no exemption.
```

This matters legally.

---

# 221. Missing Is Not Not-Applicable

Likewise:

```text
missing classification
```

may make applicability:

```text
INDETERMINATE
```

not:

```text
DOES_NOT_APPLY.
```

---

# 222. Domain Model and Commercial Strategy

This canonical model directly enables commercial packaging.

Baobab can productise:

```text
rules

profiles

jurisdiction packs

corridor packs

change feeds

assessments

obligations

decision evidence
```

without redesigning the core engine.

---

# 223. Regulatory Graph as Strategic Asset

Over time Baobab accumulates:

```text
Authority
   ↓
Instrument
   ↓
Provision
   ↓
Interpretation
   ↓
Rule
   ↓
Context
   ↓
Effect
   ↓
Decision
   ↓
Operational Outcome
```

That graph is more valuable than a folder of regulations.

---

# 224. Pulse Strategic Integration

Pulse may consume:

```text
RegulatoryChange

RegulatoryImpact

RegulatoryDecision statistics

RegulatoryEffect patterns
```

to analyse strategic consequences.

It SHALL not mutate the canonical regulatory graph.

---

# 225. Operational Feedback

Trade may later publish:

```text
shipment successfully cleared
```

or:

```text
authority rejected document.
```

Regulations may link that as operational outcome/evidence.

It SHALL not allow historical outcomes to silently rewrite regulatory rules.

---

# 226. Feedback as Learning Evidence

Operational outcomes can help identify:

```text
bad interpretation

false positives

missing rules

source lag

process friction.
```

They trigger governance/research.

They do not self-modify law.

---

# 227. Canonical Model Extensibility

New regulatory domains SHOULD extend through:

```text
new rule functions

new requirement types

new regulated activities

new profiles

new relationship types
```

rather than inventing unrelated domain models.

---

# 228. Extension Discipline

Extensions SHALL be promoted to core only when:

```text
semantics are stable

reuse exists

domain meaning is clear

existing concepts are insufficient.
```

---

# 229. No Premature Universal Legal Ontology

Baobab SHALL NOT attempt to solve all jurisprudence in ADR-REG-0006.

It needs enough semantics for dependable regulatory operations.

---

# 230. Deferred Legal Semantics

The following are deliberately deferred:

```text
exact legal hierarchy

precedent

conflict-of-laws rules

defeasibility algorithm

rule-language syntax

formal logic

obligation lifecycle details

violation and remediation semantics

jurisdiction-specific hierarchy
```

These belong in later ADRs.

---

# 231. Deferred Physical Schema

This ADR does not prescribe:

```text
SQL tables

ORM classes

graph labels

Pydantic models

Go structs

Java records.
```

Implementation shall derive from this semantic architecture.

---

# 232. Migration Policy

Because `baobab-regulations` is being established new, implementations SHOULD remodel aggressively before production rather than preserve weak early schemas indefinitely.

---

# 233. Architecture Tests

Future CI SHOULD enforce boundaries such as:

```text
domain cannot import provider SDK

domain cannot import Trade models

domain cannot import Control Plane persistence models

provider-native DTOs cannot enter canonical contracts

assessment cannot exist without rule-set reference

decision cannot exist without assessment reference.
```

---

# 234. Contract Tests

Shared contracts SHOULD verify:

```text
stable identifiers

enumeration compatibility

event schemas

cross-engine references

version compatibility.
```

---

# 235. Golden Domain Fixtures

The repository SHOULD maintain representative fixtures covering:

```text
instrument with amendments

multiple expressions

multiple provision versions

one provision → many rules

many provisions → one rule

exception

obligation

prohibition

tenant-specific interpretation

multi-jurisdiction assessment

historical assessment

regulatory change.
```

---

# 236. Minimum Canonical Model Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text
1. RegulatoryAuthority created.

2. RegulatoryRegime references canonical jurisdiction.

3. RegulatoryInstrument issued by authority.

4. Two InstrumentExpressions for one instrument.

5. Two SourceArtefacts for one expression.

6. Nested RegulatoryProvision tree.

7. Two versions of one provision.

8. RegulatoryInterpretation references provision version.

9. One provision produces multiple rules.

10. One rule derives from multiple provisions.

11. Constitutive rule defines a concept.

12. Prescriptive rule creates obligation template.

13. Exception modifies applicability.

14. RegulatoryContext references CP + Trade data.

15. Applicability produces RegulatoryEffect.

16. Assessment groups rule findings.

17. Decision references assessment.

18. Tenant-specific interpretation coexists with platform interpretation.

19. RegulatoryChange identifies affected rule.

20. RegulatoryImpact identifies affected transaction reference.

21. Every path remains provenance traceable.
```

---

# 237. Initial ZuriBeans Proof Graph

The initial implementation SHOULD ultimately demonstrate conceptually:

```text
Ugandan Authority
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
Rule:
export documentation requirement
      │
      │
      ├───────── Context ──────────┐
      │                            │
      │                    ZuriBeans legal entity
      │                    Product
      │                    Origin UG
      │                    Destination ZA
      │                    Transaction date
      │                            │
      └────────────────────────────┘
                    │
                    ▼
              Applicability
                    │
                    ▼
                Obligation
                    │
                    ▼
                Assessment
                    │
                    ▼
                 Decision
                    │
                    ▼
            Baobab Trade Hold
```

---

# 238. Standards Interoperability Position

Baobab SHALL treat major legal-information standards according to purpose:

| Standard | Baobab use |
|---|---|
| ELI | legal-resource metadata and identity inspiration |
| Akoma Ntoso | structured legal-document interchange |
| LegalRuleML | normative rule semantics and rule/provision linkage |
| W3C PROV | provenance and derivation |
| WCO Data Model | cross-border business/regulatory interoperability |
| OpenAPI/AsyncAPI | service/event contracts |

No one standard SHALL become Baobab Regulations wholesale.

---

# 239. ELI Position

The latest ELI ontology is currently v1.5 and exists to provide a common data model for exchanging legislation metadata on the web.

Baobab SHALL borrow:

```text
resource identity

expression identity

version relationships

legislative lifecycle relationships
```

where appropriate.

---

# 240. Akoma Ntoso Position

Akoma Ntoso gives Baobab a mature structured-document vocabulary for legislation, regulatory and judicial documents.

Use cases may include:

```text
import/export

structured source representation

provision addressing

document interchange.
```

---

# 241. LegalRuleML Position

LegalRuleML SHALL inform:

```text
constitutive/prescriptive distinction

deontic effects

jurisdiction

temporality

exceptions/defeasibility

rule/provision isomorphism

authorial tracking.
```


---

# 242. W3C PROV Position

W3C PROV SHALL inform:

```text
entity

activity

agent

derivation

revision

responsibility.
```


---

# 243. Architectural Invariants

The following are normative.

| ID | Invariant |
|---|---|
| `REG-M-I01` | RegulatoryInstrument SHALL NOT equal SourceArtefact |
| `REG-M-I02` | InstrumentExpression SHALL remain distinct from RegulatoryInstrument |
| `REG-M-I03` | Provision identity SHALL remain distinct from ProvisionVersion |
| `REG-M-I04` | Interpretation SHALL remain distinct from Rule |
| `REG-M-I05` | General Rule SHALL remain distinct from contextual RegulatoryEffect |
| `REG-M-I06` | Assessment SHALL remain distinct from Decision |
| `REG-M-I07` | Decision SHALL remain distinct from Enforcement |
| `REG-M-I08` | Market SHALL not substitute for Jurisdiction |
| `REG-M-I09` | Jurisdiction SHALL not substitute for RegulatoryRegime |
| `REG-M-I10` | Regulations SHALL consume, not redefine, Control Plane tenant/legal-entity identities |
| `REG-M-I11` | Provider-native identity SHALL not become canonical regulatory identity |
| `REG-M-I12` | One Rule MAY derive from multiple Provisions |
| `REG-M-I13` | One Provision MAY generate multiple Rules |
| `REG-M-I14` | Constitutive and prescriptive rule semantics SHALL be distinguishable |
| `REG-M-I15` | Obligations, permissions and prohibitions SHALL remain distinguishable |
| `REG-M-I16` | Exceptions SHALL remain explicit |
| `REG-M-I17` | Unknown SHALL not be silently interpreted as false |
| `REG-M-I18` | Missing evidence SHALL not automatically imply non-applicability |
| `REG-M-I19` | Published semantic state SHALL be versioned, not overwritten |
| `REG-M-I20` | Tenant-private knowledge SHALL not mutate platform-shared regulatory knowledge |
| `REG-M-I21` | Legal authority and source licensing SHALL remain different dimensions |
| `REG-M-I22` | Regulatory relationships SHALL be typed where legally consequential |
| `REG-M-I23` | Canonical domain semantics SHALL not depend on database technology |
| `REG-M-I24` | Regulatory graph semantics SHALL not require a graph database |
| `REG-M-I25` | Operational master data SHALL remain owned by its originating engine |
| `REG-M-I26` | Every consequential effect SHALL retain rule provenance |
| `REG-M-I27` | Every consequential assessment SHALL identify the rule set evaluated |
| `REG-M-I28` | Every consequential decision SHALL identify its assessment and effect-policy version |
| `REG-M-I29` | Temporal semantics SHALL be supported from the first persistence model |
| `REG-M-I30` | Canonical concepts SHALL survive provider replacement |

---

# 244. Consequences — Positive

This model provides:

```text
stable regulatory identity

international-standard compatibility

provider independence

historical reconstruction

precise citations

machine rule traceability

multi-jurisdiction applicability

tenant-specific overlays

cross-engine regulatory contracts

decision replay

regulatory change impact

commercial pack composition
```

---

# 245. Consequences — Commercial

Because Baobab separates:

```text
knowledge

profiles

rules

effects

decisions
```

the platform can monetise different products from the same canonical regulatory foundation.

Potential products include:

```text
Regulatory Research API

Jurisdiction Pack

Trade Corridor Pack

Transaction Assessment

Obligation Monitoring

Regulatory Change Feed

Impact Analysis

Historical Evidence Bundle

Enterprise Enforcement
```

without creating separate engines.

---

# 246. Consequences — Differentiation

A competitor may provide:

```text
excellent regulatory content.
```

Baobab can integrate it.

A competitor may provide:

```text
excellent AI search.
```

Baobab can integrate or reproduce that.

The harder asset is:

```text
canonical regulatory semantics
+
Baobab operational context
+
applicability
+
obligation instantiation
+
decision effects
+
operational feedback
```

This ADR lays the foundation for that asset.

---

# 247. Consequences — Complexity

The model is intentionally richer than a generic compliance table.

It creates:

```text
more domain entities

more versioning

more provenance

more relationships

more governance.
```

That complexity is accepted because the problem itself is complex.

---

# 248. Consequences — Discipline Required

Developers will need to resist shortcuts such as:

```text
just add JSON field

just use country code

just store the PDF

just put the law text in the prompt

just copy provider DTO.
```

Architecture tests should eventually enforce these boundaries.

---

# 249. Follow-On ADRs

This ADR now allows the sequence to become increasingly precise.

Next:

```text
ADR-REG-0007
Jurisdiction, Regulatory Authority
and Legal Hierarchy Model
```

will define:

```text
jurisdiction relationships

competent authority

legal hierarchy

instrument precedence

court/regulator relationships

conflict resolution

regional and supranational regimes.
```

Then:

```text
ADR-REG-0008
Regulatory Instrument, Provision,
Rule and Obligation Model
```

will deepen the central chain defined here.

Then:

```text
ADR-REG-0009
Permission, Prohibition, Obligation,
Exemption and Discretion Semantics
```

will define normative effects rigorously.

Then:

```text
ADR-REG-0010
Regulatory Knowledge Graph
and Relationship Model
```

will formalise the graph relationships introduced here.

---

# 250. Final Decision

Baobab Regulations SHALL adopt the following canonical semantic architecture:

```text
                EXTERNAL LEGAL WORLD

                Regulatory Authority
                         │
                         ▼
                 Regulatory Regime
                         │
                         ▼
                Regulatory Instrument
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
    Instrument Expression       Provision Identity
             │                       │
             ▼                       ▼
       Source Artefact          Provision Version
                                     │
──────────────────── BAOBAB INTERPRETIVE BOUNDARY ────────────────────
                                     │
                                     ▼
                         Regulatory Interpretation
                                     │
                                     ▼
                              Regulatory Rule
                                     │
                  ┌──────────────────┼──────────────────┐
                  ▼                  ▼                  ▼
              Conditions         Exceptions       Effect Template
                                     │
                                     ▼
                              Regulatory Context
                                     │
                                     ▼
                               Applicability
                                     │
                                     ▼
                            Regulatory Effect
                              /      |      \
                             /       |       \
                            ▼        ▼        ▼
                    Obligation  Permission  Prohibition
                            │
                            ▼
                    Regulatory Assessment
                            │
                            ▼
                     Regulatory Decision
                            │
──────────────────── OPERATIONAL BOUNDARY ────────────────────────────
                            │
                            ▼
                   Domain Engine Enforcement
```

Around that chain sit:

```text
RegulatoryProfile

RegulatoryChange

RegulatoryImpact

Verification

Evidence

Provenance

Tenant overlays

Canonical Baobab Context
```

The model SHALL be:

```text
provider-neutral

jurisdiction-aware

multi-regime

temporal

versioned

provenance-first

multi-tenant

cross-engine

rule-engine-neutral

storage-neutral

AI-provider-neutral.
```

The architectural objective is not merely to model documents about law.

It is to model:

> **how authoritative regulatory material becomes a precise, contextual and auditable operational consequence.**

That distinction is the heart of Baobab Regulations.

The resulting chain:

```text
Authority
→ Instrument
→ Provision
→ Interpretation
→ Rule
→ Context
→ Effect
→ Assessment
→ Decision
→ Operational Outcome
```

should become one of the most valuable canonical graphs in the Baobab Platform.

If we preserve those semantics rigorously, we can change:

```text
data providers

AI models

rule engines

databases

Digital Estates

jurisdictions

commercial packaging
```

without losing the identity and meaning of the regulatory knowledge itself.

That is what `ADR-REG-0006` establishes.

---

## Decision Summary

```text
ADR-REG-0006
────────────────────────────────────────────

CORE CANONICAL CHAIN

Authority
  ↓
Regime
  ↓
Instrument
  ↓
Provision
  ↓
Interpretation
  ↓
Rule
  ↓
Applicability
  ↓
Regulatory Effect
  ↓
Assessment
  ↓
Decision


LEGAL RESOURCE MODEL

Instrument
  ↓
Expression
  ↓
Source Artefact


NORMATIVE MODEL

Constitutive Rule
or
Prescriptive Rule

Prescriptive effects include:
  Obligation
  Permission
  Prohibition


GENERAL RULE
        ≠
CONTEXTUAL OBLIGATION


PLATFORM CONTEXT

Tenant
Legal Entity
Market
Jurisdiction
Trade Lane
Digital Estate

are referenced,
not redefined.


AGGREGATE ROOTS

RegulatoryAuthority
RegulatoryRegime
RegulatoryInstrument
RegulatoryProvision
RegulatoryInterpretation
RegulatoryRule
RegulatoryProfile
RegulatoryEffect
RegulatoryAssessment
RegulatoryDecision
RegulatoryChange
RegulatoryImpact


STANDARDS INFLUENCE

ELI
    legal resource/expression identity

Akoma Ntoso
    legal-document structure

LegalRuleML
    normative rule semantics

W3C PROV
    provenance


NON-NEGOTIABLE

Law ≠ PDF

Provision ≠ Rule

Rule ≠ Obligation instance

Assessment ≠ Decision

Decision ≠ Enforcement

Market ≠ Jurisdiction

Jurisdiction ≠ Regulatory Regime

Provider identity ≠ Canonical identity


STRATEGIC RESULT

Baobab gains a durable regulatory
semantic layer that survives changes
in vendors, AI, rules engines,
databases and Digital Estates.
```
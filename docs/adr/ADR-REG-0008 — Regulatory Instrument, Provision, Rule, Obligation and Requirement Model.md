# ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0008`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Normative Knowledge, Executable Rule, Obligation and Requirement Architecture  
**Strategic Classification:** Core Regulatory IP / Rules-as-Code Foundation

**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`

**Related Baobab Decisions:**

- `ADR-BCP-004 — Context, Market, Geography, Legal-Entity and Digital Estate Resolution Model`
- `ADR-BCP-011 — Market Participation, Trade Lanes and Cross-Market Trading Model`
- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`
- applicable Shared canonical-reference, event, evidence and capability contracts

**Primary Principle:**

> **Regulatory text, regulatory meaning, executable rule, contextual obligation, operational requirement and evidence of satisfaction are different objects and SHALL remain different objects.**

---

# 1. Executive Decision

Baobab Regulations SHALL model the progression from authoritative legal text to operational regulatory consequence through the following canonical chain:

```text
REGULATORY INSTRUMENT
        │
        ▼
REGULATORY PROVISION
        │
        ▼
PROVISION VERSION
        │
        ▼
REGULATORY INTERPRETATION
        │
        ▼
REGULATORY RULE
        │
        ├── applicability
        ├── conditions
        ├── exceptions
        ├── temporal semantics
        ├── bearer roles
        └── normative effect template
        │
        ▼
REGULATORY CONTEXT
        │
        ▼
RULE APPLICATION
        │
        ▼
REGULATORY EFFECT
        │
        ├── obligation
        ├── permission
        └── prohibition
        │
        ▼
REGULATORY REQUIREMENT
        │
        ├── document
        ├── licence
        ├── certificate
        ├── declaration
        ├── filing
        ├── payment
        ├── inspection
        ├── registration
        ├── reporting
        ├── retention
        └── other fulfilment condition
        │
        ▼
SATISFACTION EVIDENCE
        │
        ▼
REQUIREMENT / EFFECT STATE
        │
        ▼
REGULATORY ASSESSMENT
        │
        ▼
REGULATORY DECISION
```

The following identities SHALL therefore remain distinct:

```text
Instrument
    ≠
Provision

Provision
    ≠
Interpretation

Interpretation
    ≠
Rule

Rule
    ≠
Obligation

Obligation
    ≠
Requirement

Requirement
    ≠
Evidence

Evidence
    ≠
Satisfaction

Satisfaction
    ≠
Decision

Decision
    ≠
Enforcement
```

This separation is normative.

---

# 2. Purpose

The purpose of this ADR is to establish the canonical mechanism through which Baobab can answer:

> What does this regulatory source require?

and then:

> Under which conditions?

and then:

> Of whom?

and then:

> For which transaction or regulated activity?

and then:

> By when?

and then:

> What must be done, possessed, submitted, retained, paid or avoided?

and finally:

> What evidence demonstrates that the regulatory effect has been satisfied?

The engine SHALL represent those questions explicitly rather than burying them in arbitrary code.

---

# 3. Why This ADR Matters

A weak regulatory engine often reduces regulation to:

```json
{
  "country": "ZA",
  "rule": "Certificate required",
  "required": true
}
```

That structure cannot reliably express:

```text
who must obtain the certificate

which goods are affected

which transaction triggers the requirement

which exceptions apply

who may issue the certificate

when it must exist

when it expires

whether electronic evidence is accepted

whether several documents may satisfy the requirement

whether a later rule changes it

whether missing evidence means violation or merely pending fulfilment

whether non-compliance triggers another obligation.
```

Baobab Regulations SHALL support these semantics.

---

# 4. Research Foundation — Rules as Code

The OECD's Rules-as-Code work describes the translation of human-readable rules into machine-consumable forms and argues that official machine-consumable rules can improve consistency and reduce repeated interpretation by regulated parties.

The OECD's 2026 Law-as-Code consultation goes further and explicitly identifies:

```text
conditions
exceptions
references
hierarchies
responsibilities
time limits
discretionary powers
legal consequences
```

as elements that machine-executable legal representations need to retain.

Baobab SHALL therefore avoid a rules architecture capable of representing only:

```text
IF X THEN Y.
```

---

# 5. Research Foundation — LegalRuleML

LegalRuleML distinguishes:

```text
constitutive rules
```

which establish concepts or institutional facts, from:

```text
prescriptive rules
```

which create obligations, permissions and prohibitions.

It further models:

```text
bearers
temporal characteristics
violations
penalties
reparations
defeasibility
```

and explicitly recognises that violations may activate additional reparative obligations.

Baobab SHALL preserve these semantic capabilities.

It SHALL NOT necessarily use LegalRuleML XML as its internal representation.

---

# 6. Research Foundation — Obligation Types

LegalRuleML's specification discusses distinctions such as:

```text
achievement obligations
```

which are satisfied if the required state/action occurs within the relevant period, and:

```text
maintenance obligations
```

which require the prescribed state to remain true throughout the applicable period.

Baobab SHALL therefore not model every obligation as:

```text
done = true / false.
```

---

# 7. Research Foundation — Structured Provisions

Akoma Ntoso recognises the hierarchical structure common to legislation and supports structures including:

```text
parts
chapters
sections
subsections
articles
clauses
paragraphs
subparagraphs
```

across different legal drafting traditions.

Baobab SHALL preserve legal structure where it is materially relevant to citations, amendments and derivation.

---

# 8. Research Foundation — Cross-Border Supporting Evidence

The World Customs Organization explicitly recognises supporting documents as part of customs regulatory processes and provides for electronic supporting documents where appropriate. The WCO Data Model is designed around harmonised data required by Customs and other cross-border regulatory agencies.

Recent WCO Data Model releases also include standardised treatment of Certificates of Origin and broad support for digital supporting documents such as invoices and certificates.

This validates modelling:

```text
Regulatory Requirement
```

separately from:

```text
Evidence presented to satisfy it.
```

---

# 9. Instrument Layer

`RegulatoryInstrument` remains the stable legal-resource aggregate defined in ADR-REG-0006.

It SHALL contain or reference:

```text
authority

regime

jurisdiction

instrument type

official identifier

title

lifecycle

effective dates

expressions

provisions

external references.
```

The Instrument itself SHALL NOT carry arbitrary executable rules directly as its only semantic representation.

---

# 10. Instrument Does Not Equal Rule Set

One instrument can contain:

```text
definitions

substantive obligations

powers

prohibitions

exceptions

procedures

penalties

transitional provisions

commencement provisions

schedules.
```

It may generate dozens or thousands of distinct executable regulatory rules.

Therefore:

```text
RegulatoryInstrument
≠
RegulatoryRule.
```

---

# 11. Instrument Expression

A particular published or consolidated expression of the instrument SHALL remain distinguishable from the underlying instrument.

This preserves the ADR-REG-0006 model:

```text
Instrument
   ↓
Expression
   ↓
Artefact.
```

---

# 12. Provision

`RegulatoryProvision` SHALL be the smallest stable legal structural identity normally used for:

```text
citation

versioning

amendment

interpretation

rule derivation.
```

It SHALL support hierarchical structure.

---

# 13. Provision Version

A `ProvisionVersion` SHALL represent the actual provision content applicable during a defined legal period.

Conceptually:

```text
ProvisionVersion
├── id
├── provision_ref
├── expression_ref
├── source_artefact_refs[]
├── text / content reference
├── legal_status
├── effective_from
├── effective_to?
├── valid_from
├── valid_to?
├── publication_date?
├── content_hash?
└── provenance
```

---

# 14. Rules Derive from Provision Versions

Production rules SHALL normally reference:

```text
ProvisionVersion
```

rather than merely:

```text
RegulatoryProvision.
```

Otherwise Baobab could not determine which wording generated a historical rule.

---

# 15. Provision-to-Rule Cardinality

The canonical relationship SHALL be:

```text
ProvisionVersion  * ───────── *  RegulatoryRuleVersion
```

not:

```text
ProvisionVersion 1 ───────── 1 RegulatoryRule.
```

---

# 16. One Provision May Generate Several Rules

Example:

```text
Section 8:

An importer shall:
(a) register before importation;
(b) maintain records for five years; and
(c) submit an annual declaration.
```

Baobab SHOULD derive separate regulatory semantics for:

```text
registration obligation

record-retention obligation

annual reporting obligation.
```

---

# 17. One Rule May Require Several Provisions

Example:

```text
Provision A:
defines "regulated food product"

Provision B:
specifies import requirement

Schedule C:
lists affected product classifications

Provision D:
defines exemption.
```

One executable rule may depend upon all four.

---

# 18. Provision Fragments

Where only part of a provision supports a rule, Baobab SHOULD support granular citation to:

```text
paragraph

subparagraph

sentence

table row

schedule item

defined term
```

where source structure permits.

---

# 19. Rule Derivation Record

The relationship between source law and rule SHALL be explicitly represented.

Conceptually:

```text
RuleDerivation
├── rule_version_ref
├── provision_version_refs[]
├── interpretation_refs[]
├── derivation_type
├── generated_by
├── reviewed_by
├── verification_state
└── provenance
```

---

# 20. Derivation Types

Potential:

```text
AUTHORITY_SUPPLIED

DIRECT_STRUCTURAL_ENCODING

BAOBAB_INTERPRETED

COMMERCIAL_PROVIDER_DERIVED

TENANT_COUNSEL_DERIVED

MACHINE_ASSISTED

HUMAN_AUTHORED
```

The origin SHALL remain visible.

---

# 21. Interpretation Layer

`RegulatoryInterpretation` SHALL remain between provision and Baobab-derived executable rule where substantive interpretation occurred.

Correct:

```text
Provision
   ↓
Interpretation
   ↓
Rule.
```

Not:

```text
Provision
   ↓
opaque code.
```

---

# 22. No Interpretation Needed for Every Transformation

Pure structural transformation MAY not require substantive interpretation.

Example:

```text
official machine rule
```

may be imported through a verified authority-supplied mapping.

Likewise, extracting an explicit effective date may be structural rather than interpretive.

The system SHALL still preserve provenance.

---

# 23. RegulatoryRule

`RegulatoryRule` SHALL represent stable conceptual rule identity.

A separately versioned:

```text
RegulatoryRuleVersion
```

SHOULD represent executable semantics at a defined time/version.

---

# 24. Rule Identity versus Rule Version

Example:

```text
Rule:
ZA_IMPORT_PERMIT_CONTROLLED_GOODS
```

may have:

```text
Version 1
effective until 30 June

Version 2
effective from 1 July.
```

A new legal amendment need not create a completely unrelated rule identity if the semantic regulatory concept continues.

---

# 25. Rule Version

Conceptually:

```text
RegulatoryRuleVersion
├── id
├── rule_ref
├── version
├── rule_kind
├── regulatory_domain
├── source_refs[]
├── interpretation_refs[]
├── applicability
├── conditions
├── exceptions
├── normative_effect_template
├── temporal_semantics
├── priority_relationships
├── max_effect_class
├── verification_state
├── effective_from
├── effective_to?
├── published_at
└── provenance
```

---

# 26. Constitutive Rule

A constitutive rule defines:

```text
concept

status

classification

institutional fact

legal relationship.
```

Example:

```text
IF
product satisfies conditions A/B/C

THEN
product is "originating goods"
for Regime R.
```

No obligation need arise directly.

---

# 27. Constitutive Rules Matter Operationally

The resulting institutional fact may activate another rule:

```text
Product qualifies as originating
           │
           ▼
Preferential tariff rule applies.
```

Therefore constitutive rules SHALL be first-class.

---

# 28. Prescriptive Rule

A prescriptive rule creates or alters normative effects such as:

```text
obligation

permission

prohibition.
```

---

# 29. Rule Components

A machine-evaluable rule SHALL be capable of representing:

```text
trigger

subjects / bearer roles

jurisdiction

regime

regulated activity

object / subject matter

conditions

exceptions

definitions

effective period

normative effect

deadline semantics

evidence requirements

priority relationships.
```

Not every rule will use every component.

---

# 30. Trigger

Some rules become relevant only following a triggering fact/event.

Examples:

```text
importation

shipment arrival

invoice issuance

employment

registration

licence expiry

threshold exceeded

regulatory breach.
```

---

# 31. RegulatoryTrigger

Conceptually:

```text
RegulatoryTrigger
├── trigger_type
├── fact_pattern
├── event_type?
├── temporal_anchor?
└── parameters
```

---

# 32. Trigger Is Not Workflow Event

A legal trigger such as:

```text
goods entered territory
```

may correspond operationally to several system events.

The legal semantic shall remain independent of technical implementation.

---

# 33. Condition

A rule condition describes facts that must hold.

Examples:

```text
product_class = X

origin = UG

destination = ZA

value > threshold

entity acts_as importer.
```

---

# 34. Condition Evaluation Is Three/Four-Valued

A condition SHALL not necessarily be only:

```text
TRUE
FALSE.
```

Baobab SHOULD support:

```text
TRUE

FALSE

UNKNOWN

ERROR / UNRESOLVED
```

or equivalent semantics.

---

# 35. Unknown Is Not False

This invariant from earlier ADRs remains essential.

If:

```text
HS classification unknown
```

then:

```text
condition:
classification in restricted class
```

may be:

```text
UNKNOWN
```

not:

```text
FALSE.
```

---

# 36. Exception

`RuleException` SHALL explicitly represent facts that:

```text
defeat

exclude

modify

derogate from
```

the ordinary application of a rule.

---

# 37. Exception Precedence

An applicable exception SHALL be evaluated before instantiating the general normative effect.

---

# 38. Exemption

An exemption MAY itself derive from:

```text
another provision

licence

status

threshold

authority determination

special regime.
```

It SHALL retain provenance.

---

# 39. Exemption versus Exception

The terms may have jurisdiction-specific meanings.

Baobab's canonical model SHOULD distinguish conceptually:

```text
RULE_EXCEPTION
```

as logical rule structure,

from:

```text
EXEMPTION
```

as a legal status or entitlement that may satisfy an exception condition.

---

# 40. Normative Effect Template

A prescriptive `RegulatoryRuleVersion` SHALL contain or reference a `NormativeEffectTemplate`.

Conceptually:

```text
NormativeEffectTemplate
├── effect_type
├── bearer_role
├── auxiliary_party_role?
├── action
├── object
├── required_state
├── temporal_semantics
├── requirement_templates[]
├── remedy_refs[]
└── parameters
```

---

# 41. Effect Template versus Effect Instance

Template:

```text
Importers of product X
must hold Permit P.
```

Instance:

```text
ZuriBeans Uganda,
for transaction T,
must hold Permit P.
```

These SHALL remain different.

---

# 42. RegulatoryEffect

Once rule applicability resolves, Baobab MAY instantiate:

```text
RegulatoryEffect.
```

Effect types SHALL include at minimum:

```text
OBLIGATION

PERMISSION

PROHIBITION.
```

---

# 43. Directed Normative Effects

LegalRuleML explicitly recognises obligations, permissions and prohibitions as directed specifications associated with parties/bearers.

Baobab SHALL therefore always be capable of asking:

> Who bears this obligation?

rather than merely:

> Is there an obligation?

---

# 44. Bearer

A `RegulatoryEffect` SHALL have:

```text
bearer role
```

and, once contextualised:

```text
resolved bearer reference
```

where determinable.

---

# 45. Bearer Role versus Entity

Rule:

```text
bearer_role = IMPORTER.
```

Assessment:

```text
bearer_ref = legal_entity_123.
```

Do not encode a tenant's permanent identity as:

```text
IMPORTER.
```

---

# 46. Auxiliary Parties

Some legal relations involve another party.

Example:

```text
Authority must issue decision
to Applicant.

Employer must disclose
to Employee.
```

The model SHOULD be extensible to actor relationships beyond one bearer.

---

# 47. Obligation

An obligation means the regulated bearer is required to:

```text
perform an action
```

or:

```text
maintain a state
```

under the applicable regulatory rule.

---

# 48. Obligation Is Not Task

Example:

```text
Legal obligation:
retain transaction records for five years.
```

Trade or ERP may create operational tasks.

The legal obligation remains Regulations-owned.

---

# 49. Obligation Is Not Document

Example:

```text
Obligation:
demonstrate preferential origin.
```

Potential evidence:

```text
Certificate of Origin.
```

The certificate is not the obligation.

---

# 50. Obligation Types

Baobab SHOULD support at least conceptual obligation characteristics:

```text
ACHIEVEMENT

MAINTENANCE

PERIODIC

CONTINUING

ONE_TIME

EVENT_TRIGGERED.
```

This is consistent with LegalRuleML's recognition that obligations may have different temporal fulfilment semantics.

---

# 51. Achievement Obligation

Example:

```text
Submit declaration
within 30 days.
```

The required act need occur once within the legally defined period.

---

# 52. Maintenance Obligation

Example:

```text
Maintain a valid licence
while carrying out Activity X.
```

Satisfaction at one instant does not satisfy the entire obligation.

---

# 53. Periodic Obligation

Example:

```text
Submit report annually.
```

This may instantiate recurring obligation periods.

---

# 54. Continuing Obligation

Example:

```text
Maintain records for five years.
```

The obligation remains active for a period after the triggering transaction.

---

# 55. Permission

A permission SHALL represent an explicit normative permission where the legal source provides one.

---

# 56. Strong versus Weak Permission

LegalRuleML distinguishes the idea of explicit/strong permission from mere absence of prohibition.

Baobab SHALL therefore reject:

```text
not prohibited
=
explicitly permitted
```

as a universal equivalence.

---

# 57. Prohibition

A prohibition SHALL represent a rule forbidding:

```text
action

state

transaction

activity.
```

It may instantiate:

```text
RegulatoryEffect.effect_type = PROHIBITION.
```

---

# 58. Prohibition Is Not Operational Cancellation

A prohibition can justify an E4:

```text
DENY_TRANSITION
```

under ADR-REG-0004.

It does not authorise arbitrary downstream business actions.

---

# 59. Regulatory Requirement

`RegulatoryRequirement` SHALL represent a concrete fulfilment condition arising from a contextual RegulatoryEffect.

Examples:

```text
provide permit

possess certificate

submit declaration

pay duty

complete inspection

maintain registration

retain record

provide disclosure.
```

---

# 60. Requirement Template

Rules SHOULD normally define:

```text
RegulatoryRequirementTemplate
```

from which contextual:

```text
RegulatoryRequirement
```

instances are derived.

---

# 61. Requirement Template Structure

Conceptually:

```text
RegulatoryRequirementTemplate
├── type
├── required_subject
├── issuer_role?
├── recipient_role?
├── format_constraints?
├── validity_constraints?
├── timing
├── satisfaction_criteria
├── evidence_policy
├── alternative_requirements?
└── parameters
```

---

# 62. Requirement Instance Structure

Conceptually:

```text
RegulatoryRequirement
├── id
├── regulatory_effect_ref
├── template_ref
├── bearer_ref
├── target_object_ref?
├── requirement_type
├── state
├── due_at?
├── valid_from?
├── valid_to?
├── satisfaction_policy
├── evidence_refs[]
├── satisfied_at?
├── violated_at?
└── provenance
```

---

# 63. Requirement Kinds

Initial kinds SHOULD include:

```text
DOCUMENT

LICENCE

PERMIT

CERTIFICATE

DECLARATION

REGISTRATION

FILING

DISCLOSURE

PAYMENT

INSPECTION

TEST

LABEL

MARKING

RECORD_RETENTION

REPORT

APPROVAL

NOTIFICATION

DATA_ELEMENT

CALCULATION

ACTION

STATE
```

The list SHALL remain extensible.

---

# 64. Requirement Kind Does Not Create Domain Ownership

A:

```text
PAYMENT
```

requirement does not make Regulations a payment processor.

A:

```text
DOCUMENT
```

requirement does not make Regulations a document management system.

---

# 65. Documentary Requirement

A documentary requirement SHALL describe:

```text
what evidence is legally required

for which regulatory purpose

who may issue it

when it must be valid

to whom it must be supplied

which attributes must be present.
```

---

# 66. Evidence Document

The actual:

```text
certificate

permit

invoice

declaration
```

may be owned by:

```text
Trade

ERP

document service

tenant system

external authority.
```

Regulations SHALL reference it.

---

# 67. WCO Alignment

WCO customs guidance explicitly treats supporting documents as evidence required to allow Customs to control an operation and verify compliance, including electronic submission where appropriate.

Baobab SHOULD align cross-border documentary semantics with WCO concepts where useful.

---

# 68. WCO Data Interoperability

The WCO Data Model provides reusable data definitions for Customs and other cross-border regulatory agencies and increasingly supports digitally exchanged supporting documents.

Therefore Baobab requirements SHOULD prefer:

```text
structured evidence requirements
```

over assumptions that compliance always means:

```text
upload PDF.
```

---

# 69. Data Requirement versus Document Requirement

Some regulations require:

```text
specific data
```

rather than a particular document.

Baobab SHALL distinguish:

```text
DATA_ELEMENT
```

from:

```text
DOCUMENT.
```

---

# 70. Example

Requirement:

```text
Provide commodity origin.
```

may be satisfied through:

```text
structured customs message
```

without requiring a dedicated PDF if the governing process accepts structured electronic data.

---

# 71. Issuer Constraint

A certificate requirement SHOULD be capable of expressing:

```text
issuer must be competent authority X

issuer must be recognised certification body

issuer must satisfy accreditation class Y.
```

---

# 72. Recipient Constraint

Some requirements specify the recipient:

```text
Customs

regulator

consumer

counterparty

employee.
```

The requirement model SHALL support that distinction.

---

# 73. Format Constraint

A regulatory requirement MAY specify:

```text
electronic

paper

original

certified copy

signed

digitally signed

prescribed form.
```

Baobab SHALL represent such constraints when legally material.

---

# 74. Evidence Validity

Evidence MAY require:

```text
not expired

issued after date X

applicable to specific shipment

applicable to specific product

issued to specific legal entity

valid for specified territory.
```

---

# 75. Evidence Identity

Evidence SHALL be referenced using canonical/external reference patterns.

Regulations SHALL NOT derive evidence identity solely from:

```text
filename.
```

---

# 76. Satisfaction Policy

A requirement SHALL define what constitutes satisfaction.

Examples:

```text
one valid certificate

all listed certificates

any one of several alternatives

authority-verification result

payment confirmed

inspection passed

threshold met.
```

---

# 77. Satisfaction Is More Than Presence

Rejected:

```python
if document_exists:
    satisfied = True
```

The document may be:

```text
expired

wrong issuer

wrong product

wrong shipment

altered

revoked.
```

---

# 78. Evidence Assessment

Baobab SHOULD support:

```text
EvidenceAssessment
```

or equivalent derived result.

Conceptually:

```text
EvidenceAssessment
├── requirement_ref
├── evidence_ref
├── relevance
├── authenticity_state
├── validity_state
├── scope_match
├── issuer_match
├── temporal_match
├── result
└── provenance
```

---

# 79. Evidence Assessment Is Not Global Verification

A document may be authentic but irrelevant.

Therefore:

```text
AUTHENTIC
≠
SATISFIES_REQUIREMENT.
```

---

# 80. Requirement Satisfaction States

Initial states SHOULD support:

```text
PENDING

SATISFIED

PARTIALLY_SATISFIED

UNSATISFIED

EXEMPTED

WAIVED

VIOLATED

EXPIRED

SUPERSEDED

INDETERMINATE
```

Exact lifecycle may vary by requirement type.

---

# 81. `WAIVED` Is Not Universal

A regulatory requirement may not legally be waivable.

`WAIVED` SHALL only be available where:

```text
law

authority determination

effect policy
```

permits it.

---

# 82. Exempted versus Satisfied

```text
SATISFIED
```

means the requirement was fulfilled.

```text
EXEMPTED
```

means the requirement did not need fulfilment under an applicable exemption.

These SHALL remain distinct.

---

# 83. Partial Satisfaction

A multi-part requirement MAY legitimately be:

```text
PARTIALLY_SATISFIED.
```

Example:

```text
three mandatory supporting documents;
two available.
```

---

# 84. Obligation State

An obligation MAY have state:

```text
PENDING

ACTIVE

SATISFIED

VIOLATED

EXEMPTED

SUPERSEDED

EXPIRED

INDETERMINATE
```

but obligation state SHALL be derived from legal semantics, not merely workflow status.

---

# 85. Requirement State versus Obligation State

A complex obligation may have several requirements.

Example:

```text
Obligation:
demonstrate legal import eligibility

Requirements:
  Permit A
  Certificate B
  Declaration C.
```

Two requirements being satisfied does not mean the obligation is satisfied if C remains outstanding.

---

# 86. Satisfaction Aggregation

Rule-derived satisfaction logic SHALL define how requirement states roll up.

Possible strategies include:

```text
ALL

ANY

AT_LEAST_N

CONDITIONAL

SEQUENTIAL

ALTERNATIVE_GROUPS.
```

---

# 87. Alternatives

Law may permit:

```text
Certificate A
OR
Declaration B.
```

Baobab SHALL model alternatives explicitly.

---

# 88. Requirement Group

Conceptually:

```text
RequirementGroup
├── operator
├── requirements[]
└── conditions
```

where operator might be:

```text
ALL_OF

ANY_OF

ONE_OF

AT_LEAST.
```

---

# 89. Nested Requirement Logic

The model SHOULD permit:

```text
A
AND
(B OR C)
AND
D
```

without flattening everything into independent mandatory requirements.

---

# 90. Temporal Requirement

Requirements SHALL support temporal semantics.

Examples:

```text
before shipment

at importation

within 7 days

annually

continuously

for five years after transaction

before publication.
```

---

# 91. DueDateExpression

A requirement MAY use:

```text
DueDateExpression
```

rather than fixed timestamp.

Conceptually:

```text
DueDateExpression
├── anchor
├── offset
├── unit
├── calendar
├── adjustment_rule
└── timezone / jurisdiction policy
```

---

# 92. Temporal Anchor

Examples:

```text
shipment_departure

import_entry

invoice_date

licence_issue

reporting_period_end

employment_start

authority_notice.
```

---

# 93. Relative Deadline

Example:

```text
within 30 days after importation
```

shall preserve:

```text
anchor = importation
offset = 30
unit = calendar days
```

rather than calculating once and losing the formula.

---

# 94. Calculated Deadline

An instantiated requirement MAY then carry:

```text
due_at = 2026-10-31
```

plus:

```text
calculated_from
formula_version.
```

---

# 95. Calendar Rules

Deadlines may depend on:

```text
calendar days

business days

customs working days

public holidays

end-of-month rules.
```

Baobab SHALL not assume all durations use ordinary elapsed time.

---

# 96. Deadline Service Boundary

Regulations may calculate statutory deadlines using canonical calendar information.

It SHALL not become a generic enterprise scheduling engine.

---

# 97. Grace Period

Where law provides a grace period:

```text
grace period
```

SHALL be explicitly modelled rather than hidden in arbitrary code.

---

# 98. Periodic Obligations

Recurring obligations SHALL preserve recurrence semantics.

Conceptually:

```text
every calendar year

quarterly

monthly

within N days after event.
```

---

# 99. Recurrence Does Not Require Infinite Pre-Creation

The engine SHALL NOT need to instantiate 100 years of future obligations.

Future instances may be generated as required under deterministic recurrence rules.

---

# 100. Calculation Rules

Regulations SHALL support requirements/effects whose values are calculated.

Examples:

```text
customs duty

tax

levy

penalty

minimum capital

reporting threshold

quota

percentage.
```

---

# 101. Calculation Formula

Conceptually:

```text
RegulatoryCalculation
├── calculation_type
├── formula
├── input_definitions[]
├── source_rule_refs[]
├── rounding_policy
├── currency_policy?
├── unit_policy?
├── version
└── provenance
```

---

# 102. Formula Is Regulatory Knowledge

Where the formula is derived from law, it belongs in Regulations.

The actual accounting journal remains ERP-owned.

---

# 103. Calculation Result

An assessment SHALL preserve:

```text
formula version

input values

input provenance

result

rounding

currency/unit conversions.
```

---

# 104. External Rate Inputs

Calculations may depend on:

```text
FX rate

customs valuation

published tariff

index

benchmark.
```

Those external inputs SHALL retain provenance and effective time.

---

# 105. Regulatory Value versus Accounting Value

Regulatory calculation may produce:

```text
duty due = X.
```

ERP remains authoritative for:

```text
posted payable

ledger entry

payment settlement.
```

---

# 106. Monetary Requirement

A payment obligation MAY instantiate:

```text
amount

currency

due date

payee authority.
```

Regulations does not execute payment.

---

# 107. Inspection Requirement

An obligation may require:

```text
inspection before release.
```

Regulations SHALL model:

```text
inspection requirement
```

and may consume an inspection result.

It SHALL not become inspection workflow ownership.

---

# 108. Approval Requirement

Some rules require:

```text
authority approval
```

before a regulated action.

This SHALL be distinct from:

```text
Baobab internal approval.
```

---

# 109. External Regulatory Approval

Example:

```text
Import permit approved by Authority X.
```

This is evidence of regulatory status.

---

# 110. Internal Review

Example:

```text
Baobab reviewer confirms rule application.
```

This is governance state.

The two SHALL never be conflated.

---

# 111. Registration Requirement

A rule may require:

```text
legal entity registered with regulator.
```

The requirement MAY be satisfied by authoritative registry evidence.

---

# 112. Licence Requirement

Licence semantics SHOULD support:

```text
issuer

holder

scope

activity

jurisdiction

product class

valid_from

valid_until

status

conditions.
```

---

# 113. Licence Scope

A valid licence held by one subsidiary SHALL NOT automatically satisfy another subsidiary's obligation.

Canonical legal-entity identity matters.

---

# 114. Licence Validity

A licence may be:

```text
ACTIVE

SUSPENDED

REVOKED

EXPIRED

PENDING.
```

Only statuses legally sufficient for the applicable rule satisfy the requirement.

---

# 115. Certificate Requirement

Certificates SHOULD support:

```text
issuer

subject

product/shipment scope

issuance date

expiry

reference number

digital signature/status

revocation.
```

where relevant.

---

# 116. Certificate of Origin Example

A rule may create:

```text
Obligation:
prove preferential origin.

Requirement:
valid Certificate of Origin
under Regime R.
```

The WCO's current Data Model explicitly includes standardised Certificate of Origin datasets, reinforcing the need for machine-readable certificate semantics.

---

# 117. Declaration Requirement

A declaration MAY consist primarily of structured data.

Baobab SHALL not require a document object where the regulatory process is data-native.

---

# 118. Filing Requirement

Filing SHALL distinguish:

```text
prepared

submitted

accepted

rejected

amended.
```

Submission is not necessarily acceptance.

---

# 119. Reporting Requirement

A reporting obligation may require:

```text
recipient

period

deadline

content specification

submission format.
```

---

# 120. Record-Retention Requirement

Conceptually:

```text
RecordRetentionRequirement
├── record_type
├── retention_period
├── anchor_event
├── accessibility_constraint?
├── format_constraint?
├── storage_location_constraint?
└── destruction_after?
```

---

# 121. Data Retention versus Evidence Retention

Regulations may require a business record to be retained.

Separately, Baobab must retain enough regulatory decision evidence for its own audit.

These SHALL remain different policies.

---

# 122. Action Requirement

Some obligations require an act:

```text
notify

register

label

test

inspect

disclose.
```

The engine SHALL not force all requirements into document semantics.

---

# 123. State Requirement

Some obligations require a continuing state:

```text
remain licensed

maintain minimum capital

maintain appropriate labelling

keep records accessible.
```

---

# 124. Prohibition Satisfaction

A prohibition is satisfied when the forbidden state/action does not occur during the applicable period.

It SHALL not ordinarily produce a:

```text
document required.
```

---

# 125. Permission Satisfaction

Permission is not "satisfied" in the same way as an obligation.

The domain model SHALL not force all normative effects into one lifecycle.

---

# 126. Violation

An obligation or prohibition MAY be violated.

LegalRuleML explicitly models violations separately from logical inconsistency.

Baobab SHALL adopt the same principle.

---

# 127. Violation Is a Legal/Regulatory Finding

Example:

```text
licence expired
while regulated activity continued.
```

may produce:

```text
RegulatoryViolation.
```

This SHALL not be inferred merely because an internal task was late.

---

# 128. Potential Violation

Where evidence is incomplete:

```text
POTENTIAL_VIOLATION
```

or:

```text
VIOLATION_UNDETERMINED
```

may be appropriate.

Baobab SHALL avoid unsupported definitive findings.

---

# 129. RegulatoryViolation

Conceptually:

```text
RegulatoryViolation
├── id
├── effect_ref
├── rule_ref
├── bearer_ref
├── violation_type
├── occurred_at / period
├── facts
├── evidence_refs[]
├── assurance
├── status
└── provenance
```

Whether this becomes an independent aggregate is deferred.

---

# 130. Reparative Obligation

LegalRuleML recognises that a violation may trigger a reparative obligation or sanction structure.

Baobab SHALL therefore support:

```text
Violation A
      │
      ▼
Rule B activated
      │
      ▼
Reparative Obligation B.
```

---

# 131. Example

```text
Primary obligation:
File declaration by 31 March.

Violation:
deadline missed.

Reparative rule:
late filer must submit declaration
plus prescribed penalty/notification.
```

---

# 132. Reparation Is Not Generic Workflow Compensation

This is legal reparation, not software saga compensation.

The concepts SHALL remain distinct.

---

# 133. Penalty

A penalty MAY be represented where it follows from verified regulatory law.

Examples:

```text
fixed monetary penalty

percentage penalty

licence suspension

additional reporting requirement.
```

---

# 134. Penalty Calculation

If calculable:

```text
PenaltyFormula
```

SHALL follow the same provenance/version discipline as other regulatory calculations.

---

# 135. Discretionary Consequence

Where the authority has discretion:

```text
up to R X

may suspend licence

may require additional evidence.
```

Baobab SHALL preserve the discretion.

It SHALL NOT automatically assume the maximum or a single outcome.

---

# 136. Discretion Boundary

A discretionary authority power SHALL generally produce:

```text
possible consequence

risk

review requirement
```

not an automatic deterministic action unless an authority has actually exercised the discretion.

---

# 137. Rule Dependency

Rules MAY depend on other rules.

Example:

```text
Rule A
defines importer

Rule B
determines licence requirement

Rule C
defines exception

Rule D
sets filing deadline.
```

Baobab SHALL support dependency graphs.

---

# 138. Rule Dependency Types

Potential:

```text
DEPENDS_ON

DEFINES_TERM_FOR

TRIGGERS

EXCEPTED_BY

OVERRIDDEN_BY

REPAIRS_VIOLATION_OF

CALCULATES

SATISFIES

QUALIFIES.
```

---

# 139. Circular Dependency

Rule compilation/verification SHALL detect inappropriate dependency cycles.

Not every legal recursion is invalid, but accidental executable cycles SHALL not be silently accepted.

---

# 140. Rule Compilation

Baobab SHOULD distinguish:

```text
canonical rule semantics
```

from:

```text
compiled evaluator representation.
```

---

# 141. Canonical Rule IR

Future ADR-REG-0016 SHALL define a provider-neutral rule intermediate representation.

This ADR establishes that such an IR must support:

```text
conditions

exceptions

normative effects

bearers

temporal logic

requirements

dependencies

calculations

provenance.
```

---

# 142. Evaluator Representation

The eventual engine may compile canonical rule semantics into:

```text
CEL

Rego

Datalog

DMN

custom AST

another deterministic evaluator.
```

The compiled representation SHALL be derived and replaceable.

---

# 143. Human-Readable Rendering

Every production rule SHOULD support a human-readable projection.

Example:

```text
When an entity imports regulated commodity X
into South Africa,
the importer must possess Permit P,
unless Exemption E applies.
```

This projection aids review.

It is not the canonical legal source.

---

# 144. Machine Rule versus Explanation

The evaluator shall operate on structured semantics.

Natural-language explanation SHALL be generated from:

```text
rule

assessment

provenance.
```

It SHALL not become the executable rule.

---

# 145. Rule Verification

A rule SHALL be verified at three levels:

```text
source fidelity

interpretation fidelity

executable fidelity.
```

---

# 146. Executable Fidelity

Verification asks:

> Does the machine rule produce the effects the approved interpretation requires?

It does not re-answer whether the source itself is authoritative.

---

# 147. Golden Cases

Every consequential rule SHOULD possess domain fixtures covering:

```text
positive applicability

negative applicability

exception

unknown fact

boundary value

effective-date boundary

satisfied obligation

unsatisfied obligation

alternative evidence.
```

---

# 148. Calculation Golden Cases

Calculation rules additionally SHOULD test:

```text
zero

threshold

just below threshold

just above threshold

rounding

currency/unit conversion

historical rate/version.
```

---

# 149. Deadline Golden Cases

Deadline rules SHOULD test:

```text
exact trigger instant

business-day boundary

month/year boundary

weekend/holiday

late fulfilment

effective-date transition.
```

---

# 150. Evidence Golden Cases

Evidence tests SHOULD include:

```text
valid evidence

expired evidence

wrong issuer

wrong subject

wrong shipment

revoked document

partial evidence

alternative acceptable evidence.
```

---

# 151. Rule Assurance

A rule SHALL have assurance independently from:

```text
requirement satisfaction.
```

A perfectly verified rule may evaluate against incomplete evidence.

---

# 152. Rule Assurance State

Potential:

```text
DRAFT

EXTRACTED

INTERPRETED

REVIEWED

VERIFIED

PUBLISHED

SUSPENDED

SUPERSEDED

RETIRED.
```

---

# 153. Rule Publication

Only governed published rule versions SHALL enter production regulatory profiles.

---

# 154. Rule Suspension

A published rule MAY be suspended due to:

```text
source conflict

interpretation defect

court decision

new amendment

failed regression

licensing/source problem

operational incident.
```

---

# 155. Suspended Rule

A suspended rule SHALL remain historically addressable.

It SHALL not be used for new authoritative assessments unless specifically allowed for historical replay.

---

# 156. Rule Supersession

When:

```text
Rule Version 2
```

supersedes:

```text
Rule Version 1
```

the system SHALL preserve both.

---

# 157. Rule Effective Time

Rule execution SHALL evaluate:

```text
effective_at
```

against the rule's legal period.

Current clock time SHALL not be the only supported mode.

---

# 158. Future Rules

Verified future-effective rules MAY participate in:

```text
simulation

impact analysis

planning.
```

They SHALL not enter current production enforcement before commencement.

---

# 159. Historical Rules

Repealed rules may still apply to historical assessments.

They SHALL remain available.

---

# 160. Transitional Rules

Regulatory amendments often contain:

```text
transitional provisions

grandfathering

phased applicability.
```

Baobab's rule model SHALL support these through conditions/effective periods rather than losing them during simplification.

---

# 161. Grandfathering

Example:

```text
entities licensed before date X
may continue until date Y.
```

This SHALL be representable.

---

# 162. Threshold Rules

Thresholds SHALL preserve:

```text
operator

value

unit/currency

effective period

aggregation basis.
```

---

# 163. Aggregation Basis

Example:

```text
annual turnover > threshold
```

is not equivalent to:

```text
transaction amount > threshold.
```

The aggregation semantics SHALL be explicit.

---

# 164. Unit Semantics

A quantity rule SHALL record:

```text
unit

conversion policy

measurement basis.
```

Never compare:

```text
kg
```

and:

```text
tonnes
```

without explicit conversion.

---

# 165. Classification-Dependent Rules

Regulatory rules MAY depend on:

```text
HS code

product category

regulated-substance class

entity classification.
```

Classification SHALL be referenced with:

```text
scheme

version

effective date.
```

---

# 166. Classification Uncertainty

Where classification is unresolved, dependent requirements SHALL ordinarily become:

```text
INDETERMINATE
```

or review-gated.

---

# 167. Rule Set Composition

A RegulatoryProfile will select applicable candidate rule versions.

The immutable evaluation composition SHOULD be captured as:

```text
RegulatoryRuleSet.
```

---

# 168. Rule Set Fingerprint

A rule set SHOULD carry a deterministic fingerprint or equivalent identity over the participating rule versions.

This supports:

```text
replay

cache safety

audit

provider migration testing.
```

---

# 169. Rule Set Is Immutable for Assessment

Once an assessment begins, its rule-set identity SHALL be pinned.

A source update during evaluation SHALL not mutate the evaluation underneath it.

---

# 170. Obligation Instantiation

When a rule applies:

```text
general obligation template
```

SHALL be resolved into:

```text
context-specific RegulatoryEffect
```

using the regulatory facts.

---

# 171. Example

General:

```text
Importer must possess Certificate C
for Product Class X.
```

Context:

```text
Legal entity:
ZuriBeans SA

Activity:
IMPORT

Product:
Coffee Lot 123

Class:
X
```

Instance:

```text
Bearer:
ZuriBeans SA

Effect:
OBLIGATION

Requirement:
Certificate C
for Coffee Lot 123.
```

---

# 172. Context Binding

A RegulatoryEffect SHALL preserve which contextual bindings were used.

Conceptually:

```text
role importer
    → LegalEntity ZA-001

regulated product
    → Product P-123

transaction
    → Shipment S-456.
```

---

# 173. Effect Identity

A persisted RegulatoryEffect SHALL have its own stable identifier where it drives lifecycle/evidence/enforcement.

---

# 174. Ephemeral Effects

Simple informational assessments MAY return calculated effects without persisting each effect individually.

Persistence policy SHALL depend on consequence and lifecycle needs.

---

# 175. Consequential Effects

Effects that:

```text
create review

block transition

require evidence

survive beyond transaction

create recurring obligation
```

SHOULD normally be durably addressable.

---

# 176. Obligation Deduplication

Two different rules may create apparently identical obligations.

Baobab SHALL not automatically merge them merely because their display text is the same.

Their legal provenance may differ.

---

# 177. Shared Fulfilment

One piece of evidence MAY satisfy several obligations.

Example:

```text
one Certificate of Origin
```

may support:

```text
customs preference

origin declaration requirement.
```

The evidence can be referenced by both without merging the obligations.

---

# 178. Equivalent Requirements

Where two rules genuinely impose the same legal requirement, Baobab MAY define an explicit equivalence relationship.

That decision SHALL be governed.

---

# 179. Cumulative Requirements

Where rules independently require:

```text
Permit A

Certificate B
```

both SHALL remain active.

---

# 180. Conflicting Requirements

If two controlling rules require incompatible actions:

```text
Rule A requires X

Rule B prohibits X
```

ADR-REG-0007 hierarchy/conflict resolution SHALL run before final effect instantiation where possible.

---

# 181. Requirement Conflict After Instantiation

If conflict becomes apparent only after contextualisation, it SHALL produce:

```text
REGULATORY_CONFLICT
```

and ordinarily:

```text
REVIEW_REQUIRED.
```

---

# 182. Requirement Satisfaction Is Contextual

A licence valid for:

```text
Product A
```

may not satisfy a requirement for:

```text
Product B.
```

A generic:

```text
tenant has licence
```

Boolean is insufficient.

---

# 183. Requirement Satisfaction Time

Evidence may satisfy an obligation only during:

```text
specific valid period.
```

Historical assessment must evaluate the evidence state at the relevant legal time.

---

# 184. Revocation

If evidence is later revoked:

```text
previous assessment
```

may remain historically valid or may require reassessment depending on legal effect.

The system SHALL preserve both timelines.

---

# 185. Retrospective Authority Action

A regulator may revoke or invalidate a licence retrospectively in some contexts.

Baobab SHALL support:

```text
effective revocation time
```

separately from:

```text
recorded revocation time.
```

Detailed bitemporal behaviour belongs in ADR-REG-0015.

---

# 186. Assessment Aggregation

A RegulatoryAssessment SHALL evaluate:

```text
applicable rules

effects

requirements

satisfaction states

conflicts

missing facts

missing evidence.
```

---

# 187. Outcome Derivation

Conceptually:

```text
all mandatory effects satisfied
      → SATISFIED

all satisfied but continuing requirements exist
      → SATISFIED_WITH_REQUIREMENTS

required effect not fulfilled
      → UNSATISFIED

applicable prohibition applies
      → PROHIBITED

critical determination unresolved
      → INDETERMINATE
```

Actual derivation remains governed by rule/effect semantics.

---

# 188. Requirement Unsatisfied versus Prohibited

Missing a permit may mean:

```text
UNSATISFIED
```

and therefore:

```text
do not proceed until permit obtained.
```

The underlying activity may not be absolutely prohibited.

This distinction is commercially and legally important.

---

# 189. Remediable Requirement

A requirement SHOULD be marked:

```text
remediable = true
```

only where remediation is legally meaningful.

This metadata may help ADR-REG-0004 choose E3 conditional enforcement.

---

# 190. Non-Remediable Prohibition

Some contexts may simply produce:

```text
PROHIBITED
```

with no document the customer can upload to fix it.

The UI SHALL not invent a remediation action.

---

# 191. Corrective Requirement

Some violations may be cured.

Example:

```text
late report
    → report still required
    + possible penalty.
```

The corrective requirement should derive from the legal reparation rule.

---

# 192. Operational Action Projection

Regulations MAY project:

```text
requirements requiring human/business action
```

to Trade/ERP/etc.

It SHALL not own their operational task queues.

---

# 193. Example — Trade

Regulations:

```text
Requirement:
obtain certificate of origin.
```

Trade:

```text
creates document-request workflow.
```

The workflow state may reference:

```text
reg_requirement_id.
```

---

# 194. Example — ERP

Regulations:

```text
Obligation:
pay/import duty X.
```

ERP:

```text
creates payable / financial posting.
```

Regulations owns the regulatory calculation and obligation semantics.

ERP owns accounting.

---

# 195. Example — CMS

Regulations:

```text
Requirement:
include mandatory disclosure on product publication.
```

CMS:

```text
requires disclosure field before publication.
```

---

# 196. Example — IAM

Regulations:

```text
Applicable privacy regulation requires specified assurance/control.
```

IAM may enforce identity/security control.

Regulations SHALL not own authentication.

---

# 197. Requirement API Projection

A consumer-facing requirement contract MAY resemble:

```yaml
requirement:
  id: regreq_...
  type: CERTIFICATE
  status: PENDING
  bearer_ref: ...
  object_ref: ...
  due_at: ...
  required_evidence:
    type: CERTIFICATE_OF_ORIGIN
    issuer_role: DESIGNATED_AUTHORITY
  rule_ref: regrule_...
  source_refs:
    - ...
```

Illustrative only.

---

# 198. Requirement API Must Not Leak Rule Engine Syntax

Consumers SHALL not receive:

```text
OPA AST

DMN XML

Datalog term

CEL expression
```

as their primary contract.

---

# 199. Rule Query

Administrative/research interfaces MAY expose structured rule semantics.

Operational consumers SHOULD primarily receive:

```text
effects

requirements

decisions

source references.
```

---

# 200. Rule Compiler Boundary

The future implementation SHOULD contain:

```text
Canonical Rule Model
       │
       ▼
Rule Compiler
       │
       ▼
Evaluator Representation
       │
       ▼
Evaluation Runtime
```

---

# 201. Compiler Version

Assessment/replay SHOULD be capable of identifying:

```text
compiler version

evaluator version
```

where these could materially affect results.

---

# 202. Compiler Must Not Change Legal Meaning

A compiler upgrade SHALL preserve canonical rule semantics.

Any semantic change requires new rule/version governance.

---

# 203. Deterministic Evaluation

High-assurance regulatory rules SHOULD favour deterministic evaluation.

---

# 204. AI Is Not Runtime Rule Logic by Default

Preferred:

```text
AI assists interpretation
       ↓
verified canonical rule
       ↓
deterministic evaluation.
```

Not:

```text
every transaction
       ↓
LLM reads law
       ↓
decides obligations.
```

---

# 205. AI Candidate Rule Generation

AI MAY propose:

```text
condition

exception

effect

requirement

deadline

formula.
```

These SHALL remain candidate state until verification.

---

# 206. Machine-Generated Requirement

No requirement generated solely from unverified AI interpretation SHALL acquire E3/E4 authority.

ADR-REG-0004's ceiling remains applicable.

---

# 207. Rules as Public Infrastructure Compatibility

The OECD's Law-as-Code direction anticipates authoritative machine representations linked to the underlying legal texts.

Baobab SHALL therefore be able to replace:

```text
Baobab-derived Rule
```

with:

```text
Authority-supplied machine rule
```

without changing the downstream:

```text
Effect
Requirement
Assessment
Decision
```

contracts.

---

# 208. Authority-Supplied Rules

Where a competent authority provides executable logic:

```text
authority_machine_rule
```

SHALL be preserved distinctly.

Baobab may wrap/adapt it into canonical semantics for evaluation.

---

# 209. Authority Rule Does Not Remove Context Resolution

Even authoritative machine rules still need:

```text
correct transaction facts

jurisdiction

actor roles

effective time

classification

evidence.
```

Baobab Context remains strategically important.

---

# 210. Rule Portability

The same canonical rule SHOULD be executable by another compatible evaluator without changing:

```text
rule identity

source provenance

assessment semantics.
```

---

# 211. Rule Export

Future enterprise functionality MAY allow export of:

```text
canonical rule package

source references

test fixtures
```

subject to licensing.

---

# 212. Rule Import

Baobab MAY ingest externally authored machine rules through ADR-REG-0005 adapters.

They SHALL pass canonical mapping and verification.

---

# 213. Rule Package

A future portable `RegulatoryRulePackage` MAY include:

```text
rule versions

source references

interpretations

required concepts

tests

effective dates

signature/fingerprint.
```

Detailed design is deferred.

---

# 214. Signed Rule Packages

Authority- or provider-signed rule packages MAY support integrity verification.

Cryptographic signature does not itself prove substantive legal correctness.

---

# 215. Rule Change

A `RegulatoryChange` SHALL distinguish:

```text
source text changed

interpretation changed

rule logic changed

requirement changed

deadline changed

calculation changed.
```

---

# 216. Requirement Change Impact

If:

```text
Certificate A
```

is replaced with:

```text
Certificate B,
```

Baobab should determine which:

```text
open requirements

shipments

orders

legal entities
```

are affected.

---

# 217. Deadline Change Impact

If reporting deadline moves:

```text
30 days → 15 days,
```

open obligations may require recalculation.

Historical obligations remain tied to the applicable historical rule.

---

# 218. Rule Change Does Not Mutate Existing Historical Effects

Existing issued effects SHALL retain:

```text
rule_version.
```

New rule versions generate new/reassessed effects according to policy.

---

# 219. Active Obligation Reassessment

A continuing obligation MAY need reassessment after regulatory change.

Example:

```text
retention period changes.
```

The legal transition policy determines whether existing records inherit the new period.

The engine SHALL not assume.

---

# 220. Transition Rules

Changes affecting ongoing obligations SHOULD be expressed through explicit transitional legal rules where available.

---

# 221. Obligation Satisfaction Event

Regulations MAY publish:

```text
regulation.requirement.satisfied

regulation.obligation.satisfied
```

where these are useful cross-engine facts.

Exact event contracts belong in Shared.

---

# 222. Requirement Created Event

Potential:

```text
regulation.requirement.created
```

can allow Trade or another engine to create corresponding operational workflows.

---

# 223. Requirement Expired Event

Potential:

```text
regulation.requirement.expired.
```

---

# 224. Violation Event

A verified regulatory violation MAY emit:

```text
regulation.violation.detected
```

subject to governance and confidentiality.

It SHALL NOT automatically mean external regulator notification.

---

# 225. Reparative Obligation Event

Potential:

```text
regulation.reparation.required.
```

---

# 226. Event Idempotency

Requirement/effect events SHALL carry stable identifiers so consumers can safely deduplicate.

---

# 227. Requirement Lifecycle Is Regulations-Owned

The legal requirement lifecycle belongs to Regulations.

The operational fulfilment workflow belongs to the consuming domain.

---

# 228. Example Lifecycle

```text
Regulations:
Requirement PENDING
        │
        ▼
Trade:
requests certificate
        │
        ▼
Document received
        │
        ▼
Regulations:
evaluates evidence
        │
        ▼
Requirement SATISFIED
        │
        ▼
Regulatory Decision updated/reassessed
        │
        ▼
Trade:
releases regulatory hold.
```

---

# 229. No Direct Workflow Mutation

Regulations SHALL NOT:

```text
click Trade workflow complete

close ERP task

publish CMS page.
```

It emits domain state/decision.

---

# 230. Operational Workflow Failure

If Trade fails to request evidence:

```text
RegulatoryRequirement
```

remains valid.

The failure is operational.

---

# 231. Evidence Loss

If a document repository becomes unavailable:

```text
evidence retrieval unavailable
```

does not necessarily mean:

```text
evidence legally absent.
```

The system SHALL distinguish infrastructure availability from regulatory state.

---

# 232. Evidence Revocation

Where authoritative evidence is revoked:

```text
Requirement SATISFIED
        ↓
may become
Requirement UNSATISFIED
```

according to legal semantics.

This should trigger reassessment.

---

# 233. Duplicate Evidence

One document uploaded twice SHALL not create two independent satisfactions.

Evidence identity/deduplication belongs to the evidence integration layer.

---

# 234. Evidence Reuse

Evidence MAY satisfy several transactions only where its legal scope allows it.

---

# 235. Transaction-Specific Evidence

A Certificate of Origin tied to:

```text
Shipment A
```

SHALL not satisfy:

```text
Shipment B
```

without legal basis.

---

# 236. Standing Evidence

A regulatory licence held by the entity may satisfy requirements across many transactions during its valid period.

---

# 237. Evidence Scope Type

Evidence SHOULD therefore support:

```text
ENTITY_SCOPED

PRODUCT_SCOPED

TRANSACTION_SCOPED

SHIPMENT_SCOPED

LOCATION_SCOPED

PERIOD_SCOPED

ACTIVITY_SCOPED.
```

---

# 238. Evidence Requirement Matching

Matching SHALL consider:

```text
evidence type

issuer

subject

scope

time

status

required attributes.
```

---

# 239. Rule Reasoning Trace

Every applicable rule evaluation SHOULD produce a structured trace sufficient to answer:

```text
which conditions were true?

which were false?

which were unknown?

which exception applied?

which effect was instantiated?
```

---

# 240. Trace Is Not Private Chain of Thought

The reasoning trace SHALL be a deliberately designed domain artefact:

```text
facts
rule conditions
evaluations
provenance
outcome.
```

It SHALL not depend upon storing opaque model chain-of-thought.

---

# 241. RuleEvaluationTrace

Conceptually:

```text
RuleEvaluationTrace
├── rule_version_ref
├── evaluated_conditions[]
├── evaluated_exceptions[]
├── fact_refs[]
├── result
├── effect_refs[]
└── correlation_id
```

---

# 242. Explainability

The trace supports:

```text
machine explanation

human explanation

audit

debugging

appeal/review.
```

---

# 243. Rule Evaluation Errors

Errors SHALL distinguish:

```text
UNKNOWN_FACT

INVALID_FACT

TYPE_MISMATCH

RULE_COMPILATION_FAILURE

CALCULATION_FAILURE

DEPENDENCY_UNAVAILABLE

UNRESOLVED_CLASSIFICATION

UNSUPPORTED_RULE_SEMANTIC.
```

They SHALL not become:

```text
NOT_APPLICABLE.
```

---

# 244. Unsupported Semantic

If law requires reasoning Baobab cannot yet encode safely:

```text
UNSUPPORTED_SEMANTIC
```

SHOULD trigger review.

The system SHALL not approximate silently.

---

# 245. Natural-Language Standard

A rule may involve concepts such as:

```text
reasonable

material

adequate

substantial

appropriate.
```

These may require:

```text
interpretive policy

human review

authority guidance.
```

They SHALL not be naively converted into arbitrary numeric thresholds.

---

# 246. Discretion

Where a rule explicitly grants regulator discretion, Baobab SHALL model:

```text
DISCRETIONARY
```

rather than pretend a deterministic formula exists.

---

# 247. Discretionary Effect

A discretionary rule may produce:

```text
REVIEW_REQUIRED

AUTHORITY_DETERMINATION_REQUIRED

POTENTIAL_CONSEQUENCE.
```

---

# 248. Rule Safety Classification

Rule complexity MAY be classified for operational purposes:

```text
DETERMINISTIC

DETERMINISTIC_WITH_EXTERNAL_FACTS

INTERPRETIVE

DISCRETIONARY

HUMAN_JUDGMENT_REQUIRED.
```

---

# 249. Safety Classification Influences Effect Ceiling

`DETERMINISTIC` may become E3/E4 eligible.

`HUMAN_JUDGMENT_REQUIRED` should ordinarily remain E2 maximum without further verified authority.

---

# 250. Cross-Rule Effects

The result of one rule may become a fact consumed by another.

Example:

```text
Rule A:
goods qualify as originating

resulting institutional fact:
ORIGINATING = true

Rule B:
originating goods qualify for preference.
```

---

# 251. Derived Facts

Such facts SHALL retain:

```text
derivation rule

input facts

effective time

assurance.
```

---

# 252. Derived Fact Is Not Master Data

A derived regulatory classification need not overwrite Trade's canonical product record.

It may be referenced as a regulatory fact.

---

# 253. Rule Evaluation Ordering

Ordering SHOULD derive from:

```text
dependencies

hierarchy

definitions

rule graph
```

not from file order.

---

# 254. Evaluation DAG

Where possible, deterministic rule dependencies SHOULD form a directed acyclic evaluation graph.

Defeasible/reparative semantics may require richer treatment.

---

# 255. No Arbitrary Priority Numbers

Rejected:

```text
priority = 100
```

as the canonical legal explanation of why a rule wins.

Priority relationships must be legally meaningful under ADR-REG-0007.

---

# 256. Technical Priority

A technical evaluator MAY compile legal relationships into numeric/ordered optimisation.

That is implementation detail.

---

# 257. Performance

The engine SHOULD precompile verified rules for fast transactional evaluation.

A live shipment assessment SHOULD not parse legislation from scratch.

---

# 258. Compilation Cache

Compiled rule artefacts SHOULD be keyed by:

```text
rule version

compiler version

semantic profile.
```

---

# 259. Rule Cache Invalidation

Rule amendment/suspension SHALL invalidate affected compiled artefacts.

---

# 260. Requirement Query

Consumers SHOULD be able to ask:

> What remains outstanding before this activity may proceed?

without evaluating the entire legal corpus manually.

---

# 261. Outstanding Requirement Projection

Conceptually:

```text
GET /assessments/{id}/requirements
```

may return:

```text
2 satisfied

1 pending

1 review required.
```

Exact API design remains deferred.

---

# 262. Requirement Explanation

A requirement SHOULD answer:

```text
Why is this required?

Which rule created it?

Which provisions support that rule?

Which authority issued them?

What evidence satisfies it?

When is it due?

What happens if it remains unsatisfied?
```

---

# 263. Commercial Importance

This is a major differentiator.

A conventional regulation search tool returns:

```text
documents.
```

Baobab's target output is:

```text
For this transaction,
these four obligations apply.

Two are satisfied.

One requires this certificate.

One requires filing before this date.

Here are the source provisions.

Here is why each applies.
```

---

# 264. Obligation Graph

The resulting graph may become:

```text
Provision
   ↓
Rule
   ↓
Obligation
   ↓
Requirement
   ↓
Evidence
   ↓
Satisfaction
   ↓
Decision
   ↓
Operational outcome.
```

This graph is commercially more useful than a document corpus alone.

---

# 265. Revenue Opportunities

This architecture enables future products such as:

```text
Transaction Compliance Assessment

Outstanding Regulatory Requirements API

Permit & Licence Readiness

Regulatory Document Checklist

Deadline Monitoring

Regulatory Obligation Register

Continuous Obligation Monitoring

Evidence Assurance

Audit Evidence Bundle.
```

---

# 266. Enterprise Obligation Register

Baobab MAY eventually provide:

```text
all active regulatory obligations
for Legal Entity X
```

across:

```text
transactions

licences

reporting

record retention

ongoing activities.
```

That could become a high-value enterprise capability.

---

# 267. Transactional versus Standing Obligations

The engine SHALL distinguish:

```text
TRANSACTIONAL
```

effects tied to an operation,

from:

```text
STANDING
```

effects applying to an entity/activity over time.

---

# 268. Standing Obligation Example

```text
Maintain valid importer registration.
```

This may affect thousands of transactions.

---

# 269. Standing Effect Reuse

The engine SHOULD avoid creating unnecessary duplicate obligations per transaction where one valid standing effect applies.

Transactions may reference the standing obligation.

---

# 270. Transaction-Specific Example

```text
Submit declaration for Shipment S.
```

This SHOULD be individually instantiated.

---

# 271. Rule Scope Determines Instantiation Strategy

The regulatory model, not implementation convenience, determines whether obligations are:

```text
standing

periodic

transactional

event-specific.
```

---

# 272. Requirement Ownership Boundary

Regulations owns:

```text
requirement meaning

legal origin

satisfaction semantics.
```

Domain engine owns:

```text
operational process used to fulfil it.
```

---

# 273. Customer Workflow Independence

Two customers may fulfil the same legal requirement differently.

Example:

```text
Customer A:
manual upload

Customer B:
government API verification

Customer C:
broker integration.
```

The RegulatoryRequirement remains the same.

---

# 274. Provider Independence

One provider may validate a certificate today.

Another may validate it tomorrow.

Requirement semantics do not change.

---

# 275. Document Provider Independence

Regulations SHALL not encode:

```text
Dropbox URL

S3 path

Payload CMS document ID
```

as regulatory semantics.

Use external/canonical references.

---

# 276. Failure Semantics — Evidence Provider

If certificate verification service is unavailable:

```text
VERIFICATION_UNAVAILABLE
```

not:

```text
CERTIFICATE_INVALID.
```

---

# 277. Failure Semantics — Calculation

If required exchange-rate source is unavailable:

```text
CALCULATION_INDETERMINATE.
```

Not:

```text
duty = 0.
```

---

# 278. Failure Semantics — Deadline

If statutory calendar rules cannot be resolved:

```text
DEADLINE_INDETERMINATE.
```

Not an invented date.

---

# 279. Domain Model Invariants

The following SHALL be normative.

| ID | Invariant |
|---|---|
| `REG-R-I01` | Instrument SHALL remain distinct from Provision |
| `REG-R-I02` | Provision SHALL remain distinct from ProvisionVersion |
| `REG-R-I03` | Interpretation SHALL remain distinct from Rule |
| `REG-R-I04` | Rule identity SHALL remain distinct from RuleVersion |
| `REG-R-I05` | Provision↔Rule derivation SHALL support many-to-many relationships |
| `REG-R-I06` | Production RuleVersions SHALL retain source/provision provenance |
| `REG-R-I07` | Constitutive and prescriptive rules SHALL remain distinguishable |
| `REG-R-I08` | General Rule SHALL remain distinct from contextual RegulatoryEffect |
| `REG-R-I09` | Obligation SHALL remain distinct from operational task |
| `REG-R-I10` | Obligation SHALL remain distinct from Requirement |
| `REG-R-I11` | Requirement SHALL remain distinct from Evidence |
| `REG-R-I12` | Evidence authenticity SHALL not automatically mean Requirement satisfaction |
| `REG-R-I13` | Requirement satisfaction SHALL be context- and scope-sensitive |
| `REG-R-I14` | Obligations, Permissions and Prohibitions SHALL remain distinguishable |
| `REG-R-I15` | Explicit Permission SHALL not be inferred merely from absence of prohibition |
| `REG-R-I16` | Rule exceptions SHALL remain explicit |
| `REG-R-I17` | Unknown conditions SHALL not silently evaluate as false |
| `REG-R-I18` | Requirements SHALL support alternative and composite satisfaction logic |
| `REG-R-I19` | Regulatory deadlines SHALL preserve their derivation formula |
| `REG-R-I20` | Calculations SHALL preserve formulas, inputs and versions |
| `REG-R-I21` | Violation SHALL remain distinct from missing evidence |
| `REG-R-I22` | Reparative obligations SHALL be representable |
| `REG-R-I23` | Discretionary rules SHALL not be silently converted into deterministic rules |
| `REG-R-I24` | AI-generated candidate rules SHALL require governance before production |
| `REG-R-I25` | Rule engine implementation SHALL remain replaceable |
| `REG-R-I26` | Compiled rule representation SHALL not become canonical regulatory semantics |
| `REG-R-I27` | Published rule semantics SHALL be versioned rather than overwritten |
| `REG-R-I28` | Historical effects SHALL retain the RuleVersion that created them |
| `REG-R-I29` | Operational domain engines SHALL retain ownership of business workflows |
| `REG-R-I30` | Consequential requirement/effect state SHALL be explainable to source provision level |

---

# 280. Rejected Alternative — One Rule per Provision

Rejected.

Real legal drafting does not preserve that cardinality.

---

# 281. Rejected Alternative — One Provision per Rule

Rejected.

Rules frequently require definitions, schedules, exceptions and multiple provisions.

---

# 282. Rejected Alternative — Obligation Equals Checklist Item

Rejected.

An obligation has legal bearer, scope, timing, conditions and provenance.

---

# 283. Rejected Alternative — Requirement Equals Document

Rejected.

Many requirements concern:

```text
data

actions

state

payment

inspection

registration.
```

---

# 284. Rejected Alternative — Document Presence Equals Compliance

Rejected.

Validity, issuer, scope, timing and status must be evaluated.

---

# 285. Rejected Alternative — Every Obligation Is One-Time

Rejected.

Maintenance, periodic and continuing obligations exist.

---

# 286. Rejected Alternative — Permission Means "No Prohibition Found"

Rejected.

Explicit and implicit permission semantics differ.

---

# 287. Rejected Alternative — Rule Violation Means System Error

Rejected.

A legal violation is valid domain state.

---

# 288. Rejected Alternative — Every Violation Immediately Means Penalty

Rejected.

Penalty/reparation must come from applicable legal rules.

---

# 289. Rejected Alternative — Rules Directly Own Trade Tasks

Rejected.

Regulations owns legal semantics.

Trade owns workflow.

---

# 290. Rejected Alternative — Store Rule as Natural-Language Prompt

Rejected.

Prompts are implementation artefacts, not canonical regulatory semantics.

---

# 291. Rejected Alternative — Store Rule Only as Rego/DMN/etc.

Rejected.

Evaluator technology must remain replaceable.

---

# 292. Rejected Alternative — LLM Reads Law for Every Transaction

Rejected.

Governed, compiled rule semantics shall serve runtime evaluation.

---

# 293. Rejected Alternative — Boolean Compliance

Rejected.

Baobab must understand:

```text
which effect

which requirement

which evidence

which rule

which context

which time.
```

---

# 294. Initial ZuriBeans Proving Model

The initial UG → ZA B2B proving implementation SHOULD contain at least:

```text
one constitutive classification/origin rule

one documentary obligation

one permit/licence obligation

one customs/tariff calculation rule

one deadline

one exception

one standing obligation

one transaction-specific obligation

one evidence-verification case

one reparative/violation example.
```

---

# 295. Coffee Example

Conceptually:

```text
Provision:
regulated export commodity requirements
        │
        ▼
Interpretation
        │
        ▼
Rule
        │
        ├── bearer = exporter
        ├── product = coffee class ...
        └── effect = obligation
        │
        ▼
ZuriBeans context
        │
        ▼
Obligation
        │
        ▼
Requirement:
specified export evidence
        │
        ▼
Evidence
        │
        ▼
Satisfied / Unsatisfied.
```

Actual legal requirements SHALL be determined from verified Ugandan sources during implementation.

---

# 296. Vanilla Example

The same architecture SHALL work for vanilla without creating:

```text
VanillaComplianceEngine.
```

Product/commodity facts change.

The canonical regulatory model remains.

---

# 297. Rules-of-Origin Example

Conceptually:

```text
Several provisions
    │
    ├── definition of originating product
    ├── product-specific rule
    ├── cumulation rule
    ├── direct-transport condition
    └── proof requirement
    │
    ▼
several constitutive/prescriptive rules
    │
    ▼
Origin qualification
    +
Certificate requirement
    │
    ▼
preferential treatment assessment.
```

This demonstrates why one-document/one-rule modelling would fail.

---

# 298. Tariff Example

```text
classification rule
      │
      ▼
tariff code
      │
      ▼
rate rule
      │
      ▼
customs value
      │
      ▼
calculation formula
      │
      ▼
regulatory amount
```

Each stage retains provenance.

---

# 299. Supporting Document Example

The WCO approach to cross-border regulatory data and supporting documents demonstrates that documentary requirements should be modelled as interoperable structured requirements rather than hard-coded local upload fields.

---

# 300. Initial Implementation Sequence

```text
REG-R0
Provision / ProvisionVersion persistence

REG-R1
Interpretation-to-rule derivation

REG-R2
RegulatoryRule / RuleVersion

REG-R3
Canonical condition + exception representation

REG-R4
NormativeEffectTemplate

REG-R5
RegulatoryEffect instantiation

REG-R6
RequirementTemplate

REG-R7
Requirement instance + satisfaction state

REG-R8
Evidence assessment

REG-R9
Deadline expression

REG-R10
Calculation expression

REG-R11
Standing / periodic obligations

REG-R12
Violation / reparation

REG-R13
Rule compilation boundary

REG-R14
Golden regulatory tests

REG-R15
Trade integration
```

---

# 301. Minimum Implementation Proof

Before `ADR-REG-0008` is considered implemented, Baobab SHOULD demonstrate:

```text
1.
One Instrument with nested provisions.

2.
Two versions of one Provision.

3.
One ProvisionVersion generating several rules.

4.
One Rule derived from several ProvisionVersions.

5.
One Constitutive Rule.

6.
One Prescriptive Obligation Rule.

7.
One Permission Rule.

8.
One Prohibition Rule.

9.
One explicit Exception.

10.
One unknown-condition result.

11.
One context-specific Obligation.

12.
One Standing Obligation.

13.
One Periodic Obligation.

14.
One Documentary Requirement.

15.
One Data Requirement.

16.
One Licence/Permit Requirement.

17.
One Deadline calculated from event.

18.
One Regulatory Calculation.

19.
One alternative evidence group.

20.
One invalid/expired evidence case.

21.
One partially satisfied requirement.

22.
One satisfied obligation.

23.
One violation.

24.
One reparative obligation.

25.
One rule suspension.

26.
One historical replay.

27.
One rule-engine compiled projection.

28.
Successful evaluation through a second evaluator/test implementation without changing canonical rule identity.

29.
Trade consumes a RegulatoryRequirement without importing Regulations internals.

30.
Decision traces back to ProvisionVersion.
```

---

# 302. Production Gate for E3/E4 Rules

A RuleVersion SHALL NOT support E3/E4 operational authority until:

```text
all source provisions identified

interpretation governed

N:M derivation verified

conditions tested

exceptions tested

bearer role resolved

temporal semantics tested

requirement semantics tested

evidence criteria tested

unknown handling tested

historical version tested

calculation/deadline tested if relevant

golden positive cases pass

golden negative cases pass

provider independence verified

decision explanation verified

rule suspension tested.
```

---

# 303. Relationship to ADR-REG-0009

`ADR-REG-0009` SHALL deepen normative semantics:

```text
obligation

permission

prohibition

exemption

exception

defeasibility

discretion

violation

reparation

rights

powers.
```

This ADR establishes the objects they inhabit.

---

# 304. Relationship to ADR-REG-0010

`ADR-REG-0010` SHALL formalise graph relationships including:

```text
PROVISION_DERIVES_RULE

RULE_CREATES_EFFECT

EFFECT_REQUIRES

REQUIREMENT_SATISFIED_BY

RULE_EXCEPTED_BY

VIOLATION_TRIGGERS

RULE_DEPENDS_ON.
```

---

# 305. Relationship to ADR-REG-0014

`ADR-REG-0014` SHALL establish the full evidence and citation chain from:

```text
Requirement satisfaction
      ↓
Evidence
      ↓
Rule
      ↓
Interpretation
      ↓
Provision
      ↓
Source artefact
      ↓
Authority.
```

---

# 306. Relationship to ADR-REG-0015

`ADR-REG-0015` SHALL formalise:

```text
legal valid time

knowledge time

obligation period

deadline semantics

historical replay

retroactivity.
```

---

# 307. Relationship to ADR-REG-0016

`ADR-REG-0016` SHALL define the actual provider-neutral executable rule representation / IR.

The IR MUST be capable of implementing the semantic requirements established here.

---

# 308. Relationship to ADR-REG-0017

`ADR-REG-0017` SHALL define how:

```text
context facts
```

are resolved and bound to:

```text
rule variables / roles.
```

---

# 309. Relationship to ADR-REG-0018

`ADR-REG-0018` SHALL define evaluation-engine execution:

```text
candidate selection

dependency evaluation

applicability

effect instantiation

assessment aggregation.
```

---

# 310. Research Foundation Summary

The architecture is deliberately informed by established standards while preserving Baobab ownership of its canonical domain.

Akoma Ntoso confirms that legal documents have hierarchical structural components that must remain addressable if legislation is to be represented accurately across drafting traditions.

LegalRuleML establishes a mature semantic distinction between constitutive and prescriptive rules; models obligations, permissions and prohibitions; recognises bearer roles, temporal semantics, violations and reparative obligations; and demonstrates why regulatory norms cannot be reduced to flat Boolean conditions.

The OECD's Rules-as-Code work confirms the value of machine-consumable rules linked to authoritative human-readable regulation, while its 2026 Law-as-Code work explicitly recognises conditions, exceptions, hierarchies, responsibilities, time limits, discretion and legal consequences as necessary parts of executable law.

The WCO Data Model and customs guidance validate modelling structured supporting evidence, certificates, declarations and cross-border regulatory data independently from the underlying legal obligation.

---

# 311. Final Decision

Baobab Regulations SHALL model regulatory execution through:

```text
AUTHORITY
   │
   ▼
INSTRUMENT
   │
   ▼
PROVISION
   │
   ▼
PROVISION VERSION
   │
   ▼
INTERPRETATION
   │
   ▼
RULE VERSION
   │
   ├── conditions
   ├── exceptions
   ├── bearer role
   ├── timing
   ├── normative effect
   └── requirement templates
   │
   ▼
REGULATORY CONTEXT
   │
   ▼
APPLICABILITY
   │
   ▼
REGULATORY EFFECT
   │
   ├── OBLIGATION
   ├── PERMISSION
   └── PROHIBITION
   │
   ▼
REGULATORY REQUIREMENT
   │
   ├── document
   ├── data
   ├── permit
   ├── licence
   ├── certificate
   ├── declaration
   ├── filing
   ├── payment
   ├── inspection
   ├── registration
   ├── report
   └── continuing state
   │
   ▼
EVIDENCE
   │
   ▼
SATISFACTION
   │
   ▼
ASSESSMENT
   │
   ▼
DECISION
```

Baobab SHALL be able to prove:

```text
why the obligation exists

who bears it

which legal text created it

which rule instantiated it

which context made the rule applicable

what exactly must be done

when it must be done

what evidence satisfies it

whether it has actually been satisfied

and what happens if it is violated.
```

The central strategic consequence is that Baobab will not merely know:

```text
what regulation says.
```

It will progressively know:

```text
what regulation requires
of this legal entity
for this activity
in this jurisdiction
at this time
for this transaction
and what remains to be done.
```

That is the transition from **regulatory content** to **regulatory execution infrastructure**.

And that is where `baobab-regulations` begins to become a must-have part of the Baobab Platform rather than another searchable legal database.

---

## Decision Summary

```text
ADR-REG-0008
─────────────────────────────────────────────

CORE CHAIN

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
Regulatory Effect
  ↓
Requirement
  ↓
Evidence
  ↓
Satisfaction
  ↓
Assessment
  ↓
Decision


CARDINALITY

Provision * ↔ * Rule

One provision may produce many rules.

One rule may depend on many provisions.


RULE TYPES

Constitutive
Prescriptive


NORMATIVE EFFECTS

Obligation
Permission
Prohibition


OBLIGATION TYPES

Achievement
Maintenance
Periodic
Continuing
Event-triggered


REQUIREMENTS

Document
Data
Licence
Permit
Certificate
Declaration
Registration
Filing
Disclosure
Payment
Inspection
Test
Report
Retention
Action
State


CRITICAL DISTINCTIONS

Obligation ≠ Requirement
Requirement ≠ Evidence
Evidence ≠ Satisfaction
Violation ≠ Missing evidence
Permission ≠ Absence of prohibition
Rule ≠ Workflow
Rule ≠ Rule-engine syntax


RUNTIME

Verified canonical rule
      ↓
Context binding
      ↓
Effect instance
      ↓
Requirement state
      ↓
Regulatory Decision


FAILURE PRINCIPLE

Unknown
    ≠ False

Missing document
    ≠ automatically legal violation

Provider failure
    ≠ evidence invalid


STRATEGIC RESULT

Baobab can transform authoritative
regulatory provisions into precise,
versioned, contextual obligations
that can be satisfied, monitored,
explained and safely enforced.
```
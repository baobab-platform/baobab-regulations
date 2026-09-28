# ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0003`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Decision Type:** Regulatory Authority, Provenance, Interpretation and Trust Architecture  
**Date:** 2026-09-27  
**Strategic Classification:** Platform Differentiator / Trust Foundation  
**Parent Decisions:**  
- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`

**Related Baobab Decisions:**  
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- `ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture`
- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`
- `ADR-SHARED-010 — Supplier KYB Evidence and Decision Contracts`
- applicable Control Plane context, capability and audit ADRs

**Primary Principle:**  
**Authority is inherited from authoritative sources; it is never manufactured by Baobab.**

---

# 1. Executive Decision

Baobab Regulations SHALL establish a strict, machine-enforced separation between:

```text
AUTHORITATIVE SOURCE
        │
        ▼
SOURCE ARTEFACT
        │
        ▼
BAOBAB REPRESENTATION
        │
        ▼
BAOBAB INTERPRETATION
        │
        ▼
DERIVED REGULATORY RULE
        │
        ▼
APPLICABILITY ASSESSMENT
        │
        ▼
REGULATORY DECISION
        │
        ▼
NATURAL-LANGUAGE EXPLANATION
```

These objects SHALL NOT be treated as interchangeable.

The governing rule is:

> **Baobab may acquire, structure, interpret, derive, evaluate and explain regulation. It may not elevate its own interpretation into sovereign legal authority.**

Baobab SHALL therefore distinguish at minimum:

```text
what the authority published
what Baobab acquired
what Baobab extracted
what Baobab normalised
what Baobab interpreted
what Baobab encoded
what Baobab evaluated
what Baobab decided
what Baobab explained
```

Every consequential regulatory decision SHALL be traceable backward through this chain.

No AI model, human reviewer, commercial regulatory provider, internal rule engine or Baobab administrator SHALL be permitted to collapse these stages into a generic:

```text
"LAW"
```

object.

---

# 2. Why This Decision Is Foundational

A regulatory engine can fail in a particularly dangerous way.

It may take:

```text
government text
      ↓
AI summary
      ↓
structured rule
      ↓
API response
```

and eventually expose:

```text
"THE LAW REQUIRES X"
```

without preserving which stage actually supports that assertion.

This creates **authority laundering**.

The software's confidence, polish or sophistication makes a derived interpretation appear more authoritative than its provenance allows.

This ADR prohibits that architecture.

---

# 3. The Fundamental Authority Problem

Consider:

```text
Official Gazette
       ↓
Baobab ingestion
       ↓
OCR
       ↓
LLM extraction
       ↓
Baobab interpretation
       ↓
Rule
       ↓
Decision:
BLOCK SHIPMENT
```

The legal authority does not originate at:

```text
BLOCK SHIPMENT
```

or:

```text
Baobab interpretation
```

or:

```text
LLM extraction
```

The authority chain originates outside Baobab.

Baobab's responsibility is to preserve that chain faithfully.

---

# 4. External Research Direction

The OECD's Rules-as-Code work makes a crucial distinction between rules independently translated by regulated entities and **official machine-consumable versions produced by government**. It notes that current users commonly translate human-readable rules into code for their own systems, while the stronger Rules-as-Code vision is for government itself to produce official machine-consumable forms alongside human-readable rules.

The OECD's ongoing 2026 Law-as-Code consultation goes further. It defines Law as Code as **state-authorised provision of authoritative law in force transformed into machine-executable representations**, while requiring those representations to remain explicitly linked to their underlying legal texts. It also identifies the current duplication and inconsistency caused by separate organisations independently translating legal logic.

This distinction directly informs Baobab:

```text
Authority-issued machine rule
            ≠
Baobab-created machine rule
```

even if the logical expression happens to be identical.

---

# 5. Source Text and Machine Rule Are Different Objects

Baobab SHALL preserve:

```text
Natural-Language Provision
```

separately from:

```text
Machine-Executable Rule
```

The relationship MAY be:

```text
MachineRule
    DERIVED_FROM
Provision
```

or, where supplied directly by an authority:

```text
MachineRule
    AUTHORITY_SUPPLIED_REPRESENTATION_OF
Provision
```

These relationships have materially different authority characteristics.

---

# 6. Core Authority Chain

The canonical conceptual chain SHALL be:

```text
RegulatoryAuthority
        │
        ▼
RegulatoryInstrument
        │
        ▼
RegulatoryProvision
        │
        ▼
SourceArtefact
        │
        ▼
BaobabSourceRepresentation
        │
        ▼
RegulatoryInterpretation
        │
        ▼
RegulatoryRule
        │
        ▼
RegulatoryAssessment
        │
        ▼
RegulatoryDecision
```

Each step SHALL preserve provenance.

---

# 7. Authority SHALL NOT Be a Boolean

The platform SHALL NOT model:

```text
authoritative = true
```

as the only meaningful authority concept.

Authority is multidimensional.

The engine SHALL eventually represent separate dimensions such as:

```text
source authenticity
issuing authority
jurisdictional competence
instrument status
legal force
binding effect
temporal validity
scope
publication status
interpretation origin
interpretation assurance
rule verification
decision assurance
```

These SHALL not collapse into one scalar.

---

# 8. No Universal Trust Score

The following is explicitly rejected:

```text
authority_score = 92
```

or:

```text
legal_confidence = 0.87
```

as a universal representation of authority.

Such values blur fundamentally different questions.

For example:

```text
Is the source authentic?

Is the issuing body competent?

Is the text legally binding?

Does it apply to this transaction?

Is our interpretation correct?

Is the rule current?

Is there conflicting precedent?
```

These are separate questions.

---

# 9. Authority Is Not Accuracy

Baobab SHALL preserve the same important distinction already established elsewhere in the platform:

> **Authority is not accuracy.**

An official publication may be authoritative evidence of what was officially promulgated.

That does not necessarily establish:

```text
Baobab interpreted every provision correctly
```

or:

```text
every fact recited in the document is empirically correct
```

or:

```text
the provision applies to this specific transaction.
```

---

# 10. Authority Is Not Applicability

A highly authoritative rule can still be irrelevant to a particular case.

Therefore:

```text
AUTHORITY
      ≠
APPLICABILITY
```

Example:

```text
ZA customs regulation
```

may be unquestionably authoritative within its legal scope.

It may nevertheless be:

```text
NOT_APPLICABLE
```

to a purely Ugandan domestic transaction.

---

# 11. Authority Is Not Interpretation Assurance

Likewise:

```text
AUTHENTIC SOURCE
```

does not automatically mean:

```text
HIGH-CONFIDENCE BAOBAB INTERPRETATION
```

The source may contain ambiguity.

The interpretation may require cross-referencing multiple provisions.

The legal question may involve discretion.

---

# 12. Authority Is Not Decision Assurance

A verified rule can still produce:

```text
INDETERMINATE
```

where transaction facts are incomplete.

Therefore:

```text
verified rule
+
missing evidence
=
possibly indeterminate assessment
```

This is legitimate.

---

# 13. RegulatoryAuthority

Baobab SHALL model the issuer or legally relevant authority separately from the artefact.

Conceptually:

```text
RegulatoryAuthority
├── id
├── canonical_name
├── authority_type
├── jurisdiction_ref
├── canonical_external_refs
├── valid_from
├── valid_to
├── successor?
├── predecessor?
└── metadata
```

Examples may include:

```text
legislature
ministry
customs authority
tax authority
regulator
court
treaty body
standards authority
municipal authority
regional organisation
```

Detailed authority hierarchy belongs in `ADR-REG-0007`.

---

# 14. Authority Type Is Not Legal Rank

The taxonomy:

```text
COURT
REGULATOR
MINISTRY
LEGISLATURE
CUSTOMS_AUTHORITY
```

describes what the authority is.

It SHALL NOT, by itself, determine precedence.

Legal hierarchy varies by jurisdiction and issue.

That logic is explicitly deferred to the jurisdiction and hierarchy ADR.

---

# 15. RegulatoryInstrument

A RegulatoryInstrument SHALL represent the recognised legal or regulatory instrument.

Conceptually:

```text
RegulatoryInstrument
├── id
├── authority_id
├── jurisdiction_id
├── instrument_type
├── title
├── official_identifier
├── publication_reference
├── lifecycle_status
├── enacted_at?
├── published_at?
├── effective_from?
├── effective_to?
├── repealed_at?
└── source_relationships
```

Possible instrument types MAY eventually include:

```text
CONSTITUTION
ACT
STATUTE
REGULATION
RULE
NOTICE
PROCLAMATION
TREATY
DIRECTIVE
ORDER
DECISION
RULING
STANDARD
CODE
BYLAW
GUIDANCE
PROCEDURE
```

The type SHALL NOT imply binding force without jurisdiction-specific semantics.

---

# 16. RegulatoryProvision

Baobab SHOULD address regulation at provision-level granularity where practical.

Conceptually:

```text
RegulatoryProvision
├── id
├── instrument_id
├── canonical_locator
├── heading
├── text_reference
├── effective_state
├── parent_provision?
├── supersedes?
├── amended_by?
└── provenance
```

Examples:

```text
section 12
regulation 5(3)
schedule item 0901...
article 7
paragraph 4(a)
```

A whole 200-page Act SHALL NOT be the smallest unit of regulatory reasoning if the decision depends on one subsection.

---

# 17. SourceArtefact

A SourceArtefact SHALL represent what Baobab actually acquired.

Examples:

```text
PDF
HTML page
XML document
JSON API response
gazette scan
CSV tariff file
official machine-readable rule package
```

Conceptually:

```text
SourceArtefact
├── id
├── source_id
├── retrieval_uri
├── retrieved_at
├── media_type
├── language
├── content_hash
├── byte_size
├── published_at?
├── source_version?
├── authenticity_state
├── rights_state
└── storage_reference
```

---

# 18. SourceArtefact Is Not RegulatoryInstrument

One instrument can have multiple artefacts.

Example:

```text
Regulation
   │
   ├── Official Gazette PDF
   ├── Official HTML copy
   ├── XML publication
   └── Commercial provider representation
```

These may describe the same instrument.

They SHALL not become four different regulations.

---

# 19. Artefact Authenticity

Baobab SHALL separately assess whether the acquired artefact is plausibly authentic.

Potential evidence MAY include:

```text
official publisher
official URL
digital signature
publication identifier
gazette number
authority reference
checksum
known distribution channel
cross-source corroboration
```

No one criterion SHALL automatically establish authenticity for every jurisdiction.

---

# 20. Official Domain Is Evidence, Not Proof

A URL ending in:

```text
.gov.za
```

or:

```text
.go.ug
```

is useful provenance.

It SHALL NOT be the sole architectural criterion for legal authority.

Authority comes from:

```text
issuer
publication mechanism
legal context
instrument
jurisdiction
```

not merely DNS.

---

# 21. Uganda Example — Official Gazette

Uganda provides a useful initial authority model.

The Uganda Printing and Publishing Corporation states that the **Uganda Gazette is the official Government publication**, containing notices, government declarations, Bills, statutes, statutory instruments and legal notices. UPPC also identifies itself as the official publisher, and its current electronic archive contains thousands of gazette issues.

A Baobab acquisition might therefore model:

```text
Authority:
Government of Uganda / competent issuing body

Official publication mechanism:
Uganda Gazette

Publisher:
Uganda Printing and Publishing Corporation

Artefact:
Gazette issue / supplement

Provision:
specific statutory instrument provision
```

Baobab SHALL preserve all of those distinctions.

---

# 22. South Africa Example — Government Gazette

South Africa's Government Printing Works publishes the Government Gazette, and the South African Government portal directs users to GPW as the publisher of the latest Gazette. Government portals also associate Acts, notices, regulations and proclamations with specific Gazette references.

Accordingly:

```text
Government Gazette
```

is not equivalent to:

```text
Baobab copy of Gazette PDF.
```

Baobab owns the latter artefact.

It does not own the official publication.

---

# 23. Primary Source versus Convenience Source

Baobab MAY acquire the same content through:

```text
official government source
official mirror
legal information institute
commercial provider
partner API
internal upload
```

The acquisition route SHALL be preserved separately from underlying authority.

Example:

```text
CommercialProviderRecord
     │
     │ represents
     ▼
GovernmentNotice
     │
     │ published by
     ▼
GovernmentAuthority
```

The commercial provider does not become the government authority.

---

# 24. Commercial Regulatory Providers

Commercial providers MAY be extremely valuable.

RegGenome, for example, explicitly structures regulatory requirements into machine-readable form while retaining links to original source regulation, and positions provenance and traceability as part of its regulatory infrastructure model.

Baobab SHOULD be able to consume such data.

But:

```text
Commercial structured source
       ≠
sovereign legal authority
```

unless a competent authority has explicitly delegated or adopted that status.

---

# 25. Derived Structured Data

If Vendor X produces:

```text
Requirement R123
```

derived from:

```text
Official Provision P45
```

Baobab SHALL preserve:

```text
R123
  DERIVED_FROM
P45
```

and not merely store:

```text
rule = R123
source = Vendor X
```

if the underlying source is available.

---

# 26. Authority Laundering Is Prohibited

Authority laundering occurs when:

```text
secondary source
      ↓
AI summary
      ↓
Baobab rule
      ↓
API
```

is presented as:

```text
Official requirement
```

without preserving the fact that Baobab never obtained or verified the underlying authoritative source.

This SHALL be prohibited.

---

# 27. Canonical Source Relationship Types

Baobab SHOULD eventually support explicit source relationships such as:

```text
OFFICIAL_PUBLICATION_OF

OFFICIAL_COPY_OF

MIRROR_OF

DERIVED_FROM

INTERPRETS

SUMMARISES

TRANSLATES

CITES

AMENDS

REPEALS

SUPERSEDES

CORRECTS

IMPLEMENTS

INCORPORATES_BY_REFERENCE
```

Generic:

```text
RELATED_TO
```

SHALL not be adequate for important authority relationships.

---

# 28. Source Origin

Each material source SHOULD carry an origin classification.

Conceptually:

```text
AUTHORITY_PRIMARY

AUTHORITY_SECONDARY_PUBLICATION

OFFICIAL_GUIDANCE

OFFICIAL_PROCEDURE

OFFICIAL_RULING

JUDICIAL_DECISION

AUTHORITY_MACHINE_RULE

COMMERCIAL_REGULATORY_PROVIDER

PROFESSIONAL_INTERPRETATION

ACADEMIC_COMMENTARY

INTERNAL_TENANT_DOCUMENT

BAOBAB_DERIVED

UNKNOWN
```

This vocabulary describes provenance category.

It SHALL NOT independently determine legal hierarchy.

---

# 29. Official Guidance Is Not Automatically Legislation

An authority may publish:

```text
FAQ
guidance note
procedure manual
trade portal instruction
interpretation note
```

Such material can be highly useful and may sometimes carry formal regulatory significance.

But Baobab SHALL NOT automatically treat:

```text
official website content
```

as equivalent to:

```text
binding legislation
```

Its legal status must be explicit.

---

# 30. Official Procedure Portals

Government trade portals MAY provide highly operational descriptions of:

```text
steps
documents
fees
responsible agencies
```

These are excellent sources for operational regulatory modelling.

They SHALL retain their source type.

Where the portal cites underlying legislation, Baobab SHOULD preserve those references.

---

# 31. Normative versus Informational Sources

Baobab SHALL distinguish conceptually:

```text
NORMATIVE
```

sources that create, modify or authoritatively determine legal obligations,

from:

```text
INFORMATIVE
```

sources that explain, describe or assist understanding.

A source MAY have mixed characteristics.

Therefore the classification SHALL be applied carefully.

---

# 32. Binding versus Persuasive

The architecture SHALL eventually support:

```text
BINDING
PERSUASIVE
INFORMATIVE
UNKNOWN
```

or richer jurisdiction-specific semantics.

But this ADR does NOT establish universal rules for which instrument falls into which class.

That belongs in `ADR-REG-0007`.

---

# 33. Source Authenticity versus Legal Force

These are independent.

Example:

```text
Authentic government FAQ
```

may have:

```text
authenticity = VERIFIED
```

while:

```text
legal_force = GUIDANCE
```

That is entirely legitimate.

---

# 34. BaobabSourceRepresentation

After acquisition, Baobab MAY create a structured representation.

Conceptually:

```text
BaobabSourceRepresentation
├── id
├── source_artefact_id
├── representation_type
├── representation_version
├── generated_by
├── generated_at
├── transformation_method
├── extraction_quality
├── text_alignment
└── provenance
```

Examples:

```text
OCR_TEXT
CANONICAL_XML
NORMALISED_TEXT
STRUCTURED_PROVISION_TREE
TABLE_EXTRACTION
TARIFF_DATASET_NORMALISATION
```

---

# 35. Representation Does Not Add Legal Authority

If Baobab converts:

```text
PDF
```

into:

```text
JSON
```

the JSON does not become more legally authoritative because it is easier for machines to process.

Authority remains attributable to the original source.

---

# 36. Representation Fidelity

Baobab SHOULD preserve enough mapping to determine:

```text
which structured element
came from
which source text
```

Example:

```text
RuleCondition
   ↓
SourceProvision:
section 7(3)(a)
   ↓
SourceArtefact:
pages 41–42
```

---

# 37. Isomorphic Mapping

Where practical, Baobab SHOULD pursue close correspondence between:

```text
source provision
```

and:

```text
structured representation
```

The OECD Rules-as-Code work discusses the value of an effective mapping between human and machine-consumable rules, while LegalRuleML explicitly supports linking machine rules to natural-language normative provisions.

Perfect one-to-one representation will not always be possible.

Ambiguity must remain visible.

---

# 38. RegulatoryInterpretation

A RegulatoryInterpretation SHALL be a first-class Baobab object.

It SHALL NOT be hidden inside:

```text
rule JSON
```

or:

```text
prompt template
```

Conceptually:

```text
RegulatoryInterpretation
├── id
├── provision_refs[]
├── interpretation_type
├── interpretation_text
├── structured_meaning
├── assumptions[]
├── unresolved_questions[]
├── exceptions[]
├── alternative_interpretations[]
├── method
├── generated_by
├── reviewed_by[]
├── created_at
├── effective_context
├── lifecycle_status
└── provenance
```

---

# 39. Interpretation Is Explicitly Derived

Every Baobab interpretation SHALL identify:

```text
INTERPRETS
```

one or more:

```text
RegulatoryProvision
```

or external authoritative interpretation objects.

A floating interpretation with no source lineage SHALL not qualify for production regulatory enforcement.

---

# 40. Interpretation Types

The engine SHOULD distinguish at least conceptually:

```text
TEXTUAL_EXTRACTION

BAOBAB_NORMALISATION

MACHINE_INTERPRETATION

HUMAN_REVIEWED_INTERPRETATION

EXTERNAL_PROFESSIONAL_INTERPRETATION

AUTHORITY_ISSUED_INTERPRETATION

JUDICIAL_INTERPRETATION

TENANT_ACCEPTED_INTERPRETATION
```

These are not equivalent.

---

# 41. Authority-Issued Interpretation

Where the competent authority publishes an interpretation, ruling or formal guidance:

```text
authority interpretation
```

remains an external source artefact.

Baobab may represent it.

Baobab SHALL NOT claim authorship of it.

---

# 42. Judicial Interpretation

Court decisions MAY affect the meaning or application of legal text.

Baobab SHALL therefore support judicial interpretations as first-class external legal artefacts.

The exact treatment of:

```text
precedent
court hierarchy
binding jurisdiction
ratio
obiter
```

is deferred to the legal hierarchy ADR.

---

# 43. External Professional Interpretation

A tenant MAY provide:

```text
lawyer opinion
customs adviser opinion
tax opinion
regulatory counsel memorandum
```

Such material MAY influence tenant-specific regulatory policy.

It SHALL retain:

```text
professional origin
tenant scope
issue date
subject
limitations
```

It SHALL NOT silently become global Baobab law.

---

# 44. Tenant Interpretation versus Platform Interpretation

Baobab SHALL support the possibility that:

```text
Baobab platform interpretation
```

and:

```text
Tenant-approved legal interpretation
```

differ.

These SHALL coexist explicitly.

Example:

```text
Platform interpretation:
REVIEW_REQUIRED

Tenant counsel interpretation:
ALLOW_WITH_REQUIREMENTS
```

A tenant may configure authorised policy based on its counsel.

The original Baobab interpretation SHALL remain preserved.

---

# 45. Alternative Interpretations Are Legitimate

Where regulation is genuinely ambiguous, Baobab SHALL support:

```text
Interpretation A

Interpretation B
```

with:

```text
supporting authority
assumptions
scope
review status
```

rather than forcing artificial consensus.

---

# 46. No Last-Writer-Wins Interpretation

The engine SHALL NOT resolve legal ambiguity through:

```text
most recently saved interpretation wins
```

Interpretation conflicts SHALL require governed resolution.

---

# 47. Interpretation Lifecycle

A recommended lifecycle is:

```text
DRAFT
    ↓
EXTRACTED
    ↓
INTERPRETED
    ↓
REVIEW_PENDING
    ↓
REVIEWED
    ↓
VERIFIED
    ↓
PUBLISHED

with possible:
DISPUTED
SUSPENDED
SUPERSEDED
RETIRED
```

Exact lifecycle semantics will be refined later.

---

# 48. Verification Does Not Make Baobab Sovereign

Even:

```text
VERIFIED
```

Baobab interpretation means:

> Baobab has completed the required verification workflow for this interpretation.

It does not mean:

> The competent government has officially adopted Baobab's interpretation.

This distinction SHALL remain explicit in naming and UI.

---

# 49. RegulatoryRule

A RegulatoryRule SHALL represent machine-evaluable regulatory logic derived from:

```text
authoritative source
+
interpretation
```

or supplied directly by an authority.

Conceptually:

```text
RegulatoryRule
├── id
├── interpretation_ref
├── source_refs[]
├── rule_type
├── conditions
├── consequence
├── exceptions
├── temporal_scope
├── jurisdiction_scope
├── verification_state
├── authority_origin
├── effective_from
├── effective_to
└── provenance
```

---

# 50. Two Fundamentally Different Rule Origins

Baobab SHALL distinguish:

```text
BAOBAB_DERIVED_RULE
```

from:

```text
AUTHORITY_SUPPLIED_MACHINE_RULE
```

The distinction SHALL never be erased.

---

# 51. Authority-Supplied Machine Rules

The OECD's current Law-as-Code model explicitly contemplates state-authorised authoritative machine-executable representations that remain linked to underlying legal text.

Where such a source becomes available, Baobab SHOULD model:

```text
Authority
   │
   ├── Legal Text
   │
   └── Official Machine Rule
```

rather than re-derive the same rule unnecessarily.

---

# 52. Baobab Derived Rules Remain Derived

For:

```text
BAOBAB_DERIVED_RULE
```

the system SHALL preserve:

```text
rule
  DERIVED_FROM
interpretation
  INTERPRETS
provision
  CONTAINED_IN
instrument
  ISSUED_BY
authority
```

---

# 53. Rule Verification

Rule verification SHALL assess whether the machine representation faithfully implements the approved interpretation.

This is a different check from:

```text
source authenticity
```

and:

```text
interpretation correctness.
```

---

# 54. Three Independent Checks

The engine SHALL conceptually support:

```text
SOURCE VERIFICATION
Is this the source we believe it is?

INTERPRETATION VERIFICATION
Does our interpretation adequately represent the source?

RULE VERIFICATION
Does the executable rule implement the interpretation?
```

A production rule may require all three.

---

# 55. RegulatoryAssessment

A RegulatoryAssessment SHALL evaluate verified regulatory logic against contextual facts.

Conceptually:

```text
RegulatoryAssessment
├── id
├── context_snapshot
├── effective_at
├── rule_refs[]
├── interpretation_refs[]
├── source_refs[]
├── evidence_refs[]
├── unresolved_conditions[]
├── applicable_rules[]
├── non_applicable_rules[]
├── result
└── provenance
```

---

# 56. Assessment Is a Derived Object

A regulatory assessment SHALL be labelled clearly as:

```text
BAOBAB ASSESSMENT
```

It SHALL not be presented as:

```text
REGULATOR DETERMINATION
```

unless the regulator actually issued the determination.

---

# 57. RegulatoryDecision

A RegulatoryDecision is the operationally consumable result of an assessment.

Example:

```text
ALLOW_WITH_REQUIREMENTS
```

This is:

```text
Baobab's decision under configured verified regulatory logic
```

not necessarily:

```text
a legally binding adjudication
```

---

# 58. Decision Provenance

Every consequential RegulatoryDecision SHALL retain:

```text
assessment_ref
rule_refs
interpretation_refs
provision_refs
source_refs
effective_at
decision_engine_version
rule_set_version
assurance_state
```

---

# 59. Explanation

A human-readable explanation SHALL be considered another derived layer.

```text
Decision
   │
   ▼
Explanation
```

The explanation SHALL NOT become the source of truth for the decision.

---

# 60. Explanations Cannot Change Decisions

If canonical structured decision says:

```text
REVIEW_REQUIRED
```

an AI-generated explanation SHALL NOT say:

```text
You are cleared to proceed.
```

Explanation generation SHALL be validated against structured decision state where practical.

---

# 61. Explanations Cannot Invent Sources

Natural-language explanation MAY cite only sources present in the decision's authorised provenance graph.

An LLM SHALL NOT independently invent:

```text
case citation
section number
regulation number
gazette reference
authority statement
```

and insert it into a production explanation.

---

# 62. Generative AI Risk

NIST's Generative AI Profile defines **confabulation** as confidently generated erroneous or false content and specifically notes that generative systems may fabricate logic or citations that misleadingly appear to justify their output. NIST highlights the danger of this behaviour in consequential decision contexts.

Accordingly:

> **Generated confidence is never evidence of legal authority.**

---

# 63. AI SHALL Be Downstream of Provenance

Preferred:

```text
Verified sources
      ↓
Structured rule
      ↓
Decision
      ↓
AI explanation
```

Not:

```text
User prompt
      ↓
LLM memory
      ↓
"legal decision"
```

---

# 64. AI May Assist Interpretation

AI MAY support:

```text
provision extraction
cross-reference identification
candidate interpretation
semantic classification
change comparison
candidate rule generation
translation assistance
```

But generated artefacts SHALL retain:

```text
generated_by_model
model/provider/version
timestamp
input source refs
review state
```

where material.

---

# 65. AI Cannot Self-Verify

The following SHALL not satisfy verification:

```text
LLM A produces interpretation
LLM A says interpretation is correct
```

or:

```text
LLM A generates rule
LLM B agrees
```

Model agreement MAY be useful evidence.

It is not equivalent to independent verification.

---

# 66. Human Review SHALL Be Attributable

Human regulatory review SHALL identify:

```text
reviewer identity
review role
review timestamp
review action
scope of review
comments / reason where necessary
```

Anonymous:

```text
approved = true
```

SHALL not be adequate for consequential rule promotion.

---

# 67. Reviewer Role

A reviewer may be:

```text
regulatory analyst
domain specialist
internal counsel
external counsel
customs specialist
tax specialist
authorised tenant reviewer
platform governance reviewer
```

Role SHALL be captured where material.

---

# 68. Human Review Is Not Automatically Legal Advice

An internal regulatory analyst reviewing an extraction does not transform the result into:

```text
formal legal opinion
```

The reviewer type and authority SHALL remain explicit.

---

# 69. Separation of Duties

High-impact regulatory rules SHOULD support maker-checker governance.

Conceptually:

```text
Analyst creates interpretation
          │
          ▼
Reviewer validates interpretation
          │
          ▼
Rule author creates machine rule
          │
          ▼
Verifier approves executable rule
```

The same individual MAY perform multiple roles in low-risk environments.

But the architecture SHALL support separation.

---

# 70. Promotion Authority

Only authorised governance roles SHALL be capable of promoting:

```text
DRAFT RULE
```

to a state eligible for production use.

An ingestion worker SHALL never receive this authority merely because it discovered the source.

---

# 71. Interpretation Assurance

Interpretation assurance SHALL be multidimensional.

Potential attributes include:

```text
source completeness
cross-reference completeness
review state
ambiguity state
alternative interpretation state
jurisdiction review
domain specialist review
machine/human provenance
```

It SHALL NOT merely be:

```text
confidence = 91%
```

---

# 72. Source Trust

Source trust SHALL likewise be multidimensional.

Potential dimensions include:

```text
authenticity
authority status
publication channel
currency
completeness
integrity
rights
availability
```

This aligns with Baobab's broader principle that evidence quality should not collapse into one opaque trust score.

---

# 73. Source Authority and Reliability Can Diverge

Example:

```text
Official Gazette:
very high legal authority for promulgation
```

but a poor scan could create:

```text
low extraction reliability.
```

The source remains authoritative.

The acquired representation may be unreliable.

The architecture must capture both.

---

# 74. Perfect OCR Does Not Increase Legal Force

Likewise:

```text
100% accurate OCR
```

of:

```text
private law-firm blog
```

does not elevate the blog to:

```text
primary legislation.
```

Transformation fidelity and legal authority are independent.

---

# 75. Translation

Translations SHALL be treated as derivative representations unless the relevant jurisdiction recognises the translated version as equally authoritative.

The engine SHOULD preserve:

```text
source language
translation language
translation origin
translation method
official_translation status
```

---

# 76. Machine Translation

Machine translation SHALL never silently receive the same authority classification as the source-language legal text.

Preferred:

```text
TranslatedRepresentation
    DERIVED_FROM
AuthoritativeSourceText
```

---

# 77. Official Translation

Where an authority publishes multiple official language versions:

```text
Version A
Version B
```

Baobab MAY represent both as authority-issued.

Any legal rule about which version prevails in case of divergence belongs in the jurisdiction profile.

---

# 78. Amendments

Baobab SHALL preserve amendment lineage.

Conceptually:

```text
Instrument v1
    │
    ▼
Amendment A
    │
    ▼
Instrument state v2
```

It SHALL not simply overwrite the original provision.

---

# 79. Consolidated Text

A consolidated official or unofficial text SHALL identify:

```text
consolidation origin
included amendments
consolidation date
official status
```

An unofficial consolidation can be extremely useful.

It is still not necessarily the legal publication authority.

---

# 80. Corrections

Where a source authority issues a correction:

```text
Correction
```

SHALL not silently alter history.

Instead:

```text
Original Source
      │
      ▼
Corrected / Superseded By
      │
      ▼
Corrected Source
```

---

# 81. Retractions

Retracted or withdrawn guidance SHALL remain historically discoverable where retention and licensing allow.

Current applicability shall change.

Historical evidence SHALL not disappear.

---

# 82. Temporal Authority

Every material source SHOULD distinguish, where available:

```text
published_at
effective_from
effective_to
repealed_at
superseded_at
```

The detailed temporal architecture belongs to `ADR-REG-0015`.

This ADR establishes the principle that authority is always time-sensitive.

---

# 83. Knowledge Time

Baobab SHALL also distinguish:

```text
when the law took effect
```

from:

```text
when Baobab learned about it.
```

Example:

```text
effective_from:
1 July

Baobab acquired:
3 July
```

This difference matters for audit and incident analysis.

---

# 84. Historical Interpretation

A later interpretation SHALL NOT silently rewrite an earlier decision.

If Baobab changes interpretation:

```text
Interpretation v1
        │
        ▼
SUPERSEDED_BY
        │
        ▼
Interpretation v2
```

Historical decisions should remain linked to v1.

---

# 85. Interpretation Correction

A correction differs from ordinary supersession.

The architecture SHOULD distinguish:

```text
NEW LEGAL POSITION
```

from:

```text
BAOBAB PREVIOUSLY MISINTERPRETED EXISTING LAW
```

These carry different operational consequences.

---

# 86. Source Conflict

Where two source artefacts appear to conflict, Baobab SHALL create an explicit conflict state.

Not:

```text
latest_ingested_source wins
```

but:

```text
SOURCE_CONFLICT
```

with references to both.

---

# 87. Authority Conflict

Where legally relevant authorities disagree:

```text
Regulator A interpretation
       ≠
Court decision
```

Baobab SHALL not resolve the conflict using generic source priority.

Jurisdiction-specific hierarchy SHALL determine treatment.

If unresolved:

```text
REVIEW_REQUIRED
```

is valid.

---

# 88. Commercial Provider Conflict

If:

```text
Vendor A says rule X
Vendor B says rule Y
```

Baobab SHOULD trace both back to source provisions.

Provider reputation alone SHALL not settle the legal question.

---

# 89. Secondary Commentary

Academic research, industry publications and specialist commentary MAY help Baobab:

```text
understand
identify ambiguity
locate primary sources
discover interpretations
```

But they SHALL retain secondary-source status unless their legal role is otherwise established.

---

# 90. Source Substitution

If the official source is temporarily unavailable, Baobab MAY use a trusted secondary copy.

But the assessment SHALL preserve:

```text
source substitution occurred
```

and SHALL not pretend the secondary copy is the official publisher.

---

# 91. Offline Evidence Preservation

Regulatory decisions must remain explainable even when the original web page later disappears.

Baobab SHOULD preserve authorised source snapshots or durable content hashes subject to licensing and retention policy.

W3C PROV explicitly models entities, activities, agents, derivation and responsibility so data lineage and trust can be examined even as artefacts evolve.

---

# 92. Provenance Graph

The Regulations provenance graph SHOULD conceptually support:

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
SourceArtefact
    │
    ▼
Representation
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
    │
    ▼
Explanation
```

and reverse traversal:

```text
Decision
    │
    ▼
Which rule?
    │
    ▼
Which interpretation?
    │
    ▼
Which source provision?
    │
    ▼
Which authority?
```

---

# 93. Provenance Objects Need Agents

Important derivations SHOULD identify the responsible agent.

Agents MAY include:

```text
government authority
Baobab ingestion worker
AI model
human analyst
external counsel
rule compiler
regulatory reviewer
tenant administrator
```

This closely matches W3C PROV's model of entities, activities and agents associated with derivation and responsibility.

---

# 94. Provenance of Provenance

Even provenance assertions may themselves require provenance.

Example:

```text
Baobab claims:
"This document is from Authority X."
```

Baobab SHOULD be able to explain:

```text
how that attribution was established.
```

W3C PROV supports provenance bundles and provenance of provenance, providing a useful conceptual basis.

---

# 95. Regulatory Claim

The engine MAY benefit from an explicit:

```text
RegulatoryClaim
```

object.

Example:

```text
"Import permit X is required for goods Y."
```

A claim SHALL link to:

```text
supporting provisions
interpretations
rules
contradicting evidence
status
```

This pattern mirrors Baobab's existing claim/evidence/verification discipline in organisational verification.

---

# 96. Claim Is Not Rule

A textual claim:

```text
"Export certificate required."
```

is not yet necessarily executable.

A RegulatoryRule must specify machine-evaluable semantics such as:

```text
subject
conditions
scope
consequence
exceptions
effective time
```

---

# 97. Rule Is Not Assessment

Likewise:

```text
Rule:
certificate required when condition X
```

does not imply:

```text
this shipment requires certificate.
```

That conclusion requires context.

---

# 98. Assessment Is Not Enforcement

The authority chain remains:

```text
Rule
     ↓
Assessment
     ↓
Decision
     ↓
Operational policy
     ↓
Enforcement
```

No layer may silently impersonate another.

---

# 99. Proposed Decision Evidence Contract

A consequential decision SHOULD expose references similar to:

```yaml
decision:
  id: regdec_...
  outcome: REVIEW_REQUIRED
  effective_at: 2026-09-27

  assessment:
    id: regassess_...

  authority:
    jurisdiction: ZA

  rules:
    - rule_id: regrule_...
      origin: BAOBAB_DERIVED
      verification: VERIFIED

  interpretations:
    - interpretation_id: reginterp_...
      type: HUMAN_REVIEWED_INTERPRETATION

  sources:
    - provision_id: ...
      instrument_id: ...
      authority_id: ...
      artefact_id: ...

  assurance:
    decision_state: ...

  explanation:
    reference: ...
```

This is conceptual.

Canonical schemas belong in later ADRs and Shared.

---

# 100. UI Labelling

User interfaces SHALL clearly distinguish:

```text
OFFICIAL SOURCE

BAOBAB STRUCTURED REPRESENTATION

BAOBAB INTERPRETATION

AUTOMATED REGULATORY ASSESSMENT

HUMAN-REVIEWED ASSESSMENT

EXTERNAL PROFESSIONAL OPINION

AUTHORITY RULING
```

The UI SHALL NOT visually flatten all of these into:

```text
Regulatory Answer
```

without provenance.

---

# 101. Human-Friendly Wording

Appropriate:

> "Baobab's current assessment is that this transaction requires review under the following verified rule."

Not:

> "The law definitely says you cannot do this."

unless the system is explicitly quoting and accurately representing the authoritative source and context supports that statement.

---

# 102. Source Citation

Every consequential explanation SHOULD expose a path to its source.

The minimum source reference MAY include:

```text
authority
instrument
provision
publication reference
effective date
source link where available
```

---

# 103. Citation Is Not Decoration

A citation SHALL support the specific claim it accompanies.

A long list of unrelated legal sources at the bottom of an AI answer SHALL not qualify as regulatory provenance.

---

# 104. Exact Provision Mapping

Where practical:

```text
Requirement A
```

SHOULD map to:

```text
Provision X
```

rather than merely:

```text
Act Y
```

This is essential for explainability.

---

# 105. Derived Calculations

Some regulatory outcomes involve calculations:

```text
duty
tax
threshold
percentage
deadline
```

Baobab SHALL preserve:

```text
source rule
calculation formula
input values
rounding method
calculation result
```

The calculation result itself is Baobab-derived.

---

# 106. Example

```text
Official tariff rate:
10%

Customs value:
R100,000

Baobab calculation:
R10,000
```

Baobab owns:

```text
calculation
```

not:

```text
official tariff rate
```

unless Baobab itself is the authority—which it is not.

---

# 107. External Authority Determination

Sometimes a regulator or customs authority may issue:

```text
classification ruling
advance ruling
permit decision
tax determination
licensing decision
```

Such an artefact SHALL be represented separately from Baobab's decision.

Example:

```text
AuthorityDetermination
   │
   ▼
BaobabAssessment
```

Baobab may rely upon it.

Baobab SHALL not rename it as a Baobab interpretation.

---

# 108. Authority Determination May Be Context-Specific

A ruling issued for:

```text
specific company
specific product
specific period
```

SHALL not automatically become universal regulatory law.

Its scope must be preserved.

---

# 109. Scope Is Mandatory

All material interpretations and rules SHOULD be capable of expressing:

```text
jurisdiction
entity class
product class
transaction type
market
effective period
counterparty class
regulatory domain
```

where applicable.

---

# 110. Unknown Scope

Where scope cannot reliably be determined:

```text
scope = UNKNOWN
```

is preferable to:

```text
scope = GLOBAL
```

---

# 111. Authority Status Change

The source authority itself may evolve.

Example:

```text
Agency A
      ↓
merged into
Agency B
```

Historical source relationships SHALL preserve which authority issued the rule at the time.

---

# 112. Delegated Authority

A regulator may act under authority delegated by legislation.

Baobab SHOULD eventually support:

```text
AUTHORITY_DERIVED_FROM
```

relationships.

Detailed constitutional/legal hierarchy belongs in `ADR-REG-0007`.

---

# 113. Incorporated Standards

Regulation may incorporate external standards by reference.

Example:

```text
Regulation
     │
     ▼
incorporates Standard X
```

Baobab SHALL preserve the relationship rather than copy the standard and pretend it originated with the regulator.

Licensing may also differ.

---

# 114. Source Rights and Authority Are Separate

An artefact may be:

```text
highly authoritative
```

but:

```text
commercial redistribution prohibited.
```

Conversely, an open dataset may have broad reuse rights but low normative authority.

Therefore:

```text
authority
≠
licence
```

Detailed licensing architecture belongs in `ADR-REG-0012`.

---

# 115. Internal Rule Overrides

A tenant may impose internal policy stricter than law.

Example:

```text
Law permits transaction.

Tenant policy prohibits transaction.
```

That SHALL NOT be represented as:

```text
Regulation prohibits transaction.
```

The architecture must retain:

```text
REGULATORY_RULE

TENANT_POLICY_RULE
```

as separate domains.

---

# 116. Regulatory Floor versus Internal Policy

Future consuming systems MAY evaluate:

```text
regulation
+
tenant policy
```

But Baobab Regulations SHALL clearly identify which consequence originates from which layer.

---

# 117. Customer Counsel Override

A tenant may instruct Baobab:

```text
For this jurisdiction,
follow counsel interpretation C123.
```

The resulting assessment SHALL preserve:

```text
source law
Baobab default interpretation
tenant-approved interpretation
counsel reference
decision policy
```

This protects both transparency and customer autonomy.

---

# 118. Platform Default Interpretation

Baobab MAY publish:

```text
PLATFORM_DEFAULT
```

interpretations.

These SHOULD be clearly labelled and versioned.

They SHALL NOT masquerade as official state interpretations.

---

# 119. Local Legal Expertise

Jurisdiction expansion SHALL eventually require qualified local regulatory knowledge.

The architecture SHALL support:

```text
jurisdiction reviewers
domain reviewers
partner counsel
authority-supplied content
```

without requiring that every interpretation be produced by one central Baobab team.

---

# 120. Governance versus Legal Authority

Baobab governance can authorise:

```text
this rule may be used in production
```

It cannot authorise:

```text
this Baobab rule is legally binding law
```

Those are different powers.

---

# 121. Production Eligibility

A future rule may reach:

```text
PRODUCTION_ELIGIBLE
```

after Baobab governance.

This status means:

> permitted for configured production regulatory assessments.

It SHALL not be named:

```text
LEGAL_AUTHORITY
```

---

# 122. Enforcement Eligibility

Likewise:

```text
ENFORCEMENT_ELIGIBLE
```

will mean:

> the rule's assurance and policy state allow it to participate in operational enforcement.

The exact classes belong in `ADR-REG-0004`.

---

# 123. Uncertainty

The engine SHALL preserve uncertainty explicitly.

Possible states include:

```text
AMBIGUOUS_TEXT

CONFLICTING_INTERPRETATIONS

MISSING_SOURCE

PARTIAL_SOURCE

UNRESOLVED_CROSS_REFERENCE

FACT_DEPENDENT

DISCRETIONARY

JURISDICTION_UNCERTAIN

TEMPORAL_UNCERTAIN
```

---

# 124. Ambiguity Shall Not Be "Resolved" by LLM Temperature

Changing model settings until an LLM returns one answer SHALL not qualify as legal interpretation governance.

Where ambiguity is real, it remains a domain fact.

---

# 125. Contradiction Is Information

If two authoritative artefacts appear inconsistent:

```text
CONTRADICTION
```

is meaningful regulatory state.

The system SHOULD preserve it.

This follows Baobab's wider evidence principle that contradiction is itself information rather than merely noise to eliminate.

---

# 126. Missing Evidence Is Not Permission

If Baobab has not found a prohibition, this does not necessarily prove none exists.

Therefore:

```text
NO_PROHIBITION_FOUND
```

SHALL not automatically equal:

```text
ALLOW
```

unless coverage and policy justify that conclusion.

---

# 127. Coverage Context

Decision assurance may depend upon:

```text
rule coverage
source coverage
jurisdiction coverage
domain coverage
effective-date coverage
```

This is distinct from source authority.

---

# 128. Research Mode

The engine MAY expose research results that include:

```text
unverified sources
candidate interpretations
secondary commentary
```

Research mode SHALL never be mistaken for production regulatory authority.

---

# 129. Production Mode

Production assessments SHOULD consume only rule states permitted under configured assurance policy.

Example:

```text
DRAFT interpretation
```

may appear in research.

It should not normally drive:

```text
BLOCK
```

in production.

---

# 130. Shadow Mode

New interpretations MAY run in shadow mode.

```text
Production Rule v1
      │
      ├── authoritative operational decision
      │
      └── shadow Rule v2
             │
             ▼
        comparison only
```

This supports safe evolution.

---

# 131. Interpretation Regression

When interpretation changes, Baobab SHOULD identify:

```text
which decisions would change?
```

before promotion.

This becomes part of later golden-case testing architecture.

---

# 132. Authority Regression Is Impossible

Software testing can validate:

```text
Baobab behaviour
```

It cannot test:

```text
whether Parliament had authority to enact a law
```

without a jurisdiction-specific legal model.

This reminds us to keep software assurance distinct from legal authority.

---

# 133. Data Model SHALL Resist Shortcut Fields

Avoid:

```text
is_law = true

is_valid = true

confidence = 95

source_type = official
```

as the complete domain representation.

These are too crude for production regulatory infrastructure.

---

# 134. Recommended Authority Dimensions

A future canonical model SHOULD support concepts equivalent to:

```text
source_origin

source_authenticity

issuing_authority

instrument_type

publication_status

legal_force

binding_effect

jurisdiction_scope

subject_scope

temporal_scope

interpretation_origin

interpretation_review_state

rule_verification_state

decision_assurance
```

---

# 135. No Arithmetic Authority Aggregation

The system SHALL NOT calculate:

```text
authority_score =
0.3 source +
0.2 review +
0.5 model confidence
```

and use it to decide whether law exists.

Regulatory authority is semantic, not a credit score.

---

# 136. API Contracts Must Preserve the Distinction

A regulatory API SHALL NOT simply return:

```json
{
  "answer": "Permit required",
  "confidence": 0.92
}
```

for consequential use.

It needs structured provenance.

Conceptually:

```json
{
  "outcome": "ALLOW_WITH_REQUIREMENTS",
  "requirements": [],
  "rule_refs": [],
  "interpretation_refs": [],
  "source_refs": [],
  "assurance": {},
  "effective_at": "..."
}
```

---

# 137. Natural-Language API Responses

Conversational interfaces MAY exist.

They SHALL be projections over structured regulatory objects.

The conversation itself SHALL not become regulatory truth.

---

# 138. Chat Answer Provenance

A conversational answer SHOULD be reconstructable from:

```text
assessment
decision
rules
sources
```

rather than only from:

```text
prompt + model output
```

---

# 139. Model Memory Is Not Regulatory Source

An LLM's training corpus or latent knowledge SHALL never qualify as an authoritative regulatory source.

If a model recalls:

```text
South Africa requires X
```

the claim remains unverified until linked to appropriate regulatory evidence.

---

# 140. Web Search Is Not Verification

Finding multiple websites saying the same thing SHALL not automatically create verification.

Those pages may copy one another.

Verification should examine source lineage.

---

# 141. Search Rank Is Not Authority

The top search result SHALL not be presumed the most legally authoritative result.

Search engines optimise relevance, not legal hierarchy.

---

# 142. AI Retrieval Result Is Not Source Authority

A retrieved chunk may be:

```text
high semantic similarity
```

while being:

```text
outdated
secondary
wrong jurisdiction
draft
repealed
```

Retrieval relevance and regulatory authority SHALL remain independent.

---

# 143. Proposed Authority Validation Pipeline

```text
Acquire
   │
   ▼
Identify Source
   │
   ▼
Identify Authority
   │
   ▼
Verify Artefact
   │
   ▼
Identify Instrument
   │
   ▼
Identify Provision
   │
   ▼
Determine Publication / Lifecycle State
   │
   ▼
Create Representation
   │
   ▼
Interpret
   │
   ▼
Review
   │
   ▼
Encode Rule
   │
   ▼
Verify Rule
   │
   ▼
Publish for Approved Use
```

---

# 144. Source Promotion Is Not Rule Promotion

These SHALL be separate workflows.

A source can be:

```text
AUTHENTIC
```

while its extracted rule remains:

```text
DRAFT
```

---

# 145. Rule Promotion Is Not Enforcement Promotion

A rule can be:

```text
VERIFIED
```

while policy permits only:

```text
ADVISORY
```

use.

`ADR-REG-0004` will define that boundary.

---

# 146. Decision Assurance Shall Reflect Inputs

A decision's assurance SHALL never exceed what its critical dependencies justify.

Conceptually:

```text
decision assurance
depends on
    source state
    interpretation state
    rule state
    context completeness
    evidence completeness
```

The exact propagation model remains deferred.

---

# 147. Weakest Critical Dependency Principle

For consequential rules, if an essential input is unresolved:

```text
critical interpretation unresolved
```

the system SHOULD not produce:

```text
HIGH_ASSURANCE BLOCK
```

merely because other inputs are strong.

---

# 148. Audit

The engine SHALL audit material changes to:

```text
source authority metadata
authenticity state
instrument status
interpretation
rule verification
rule publication
authority relationship
conflict resolution
review
override
```

---

# 149. Audit Cannot Rewrite Domain History

Administrative correction SHALL create:

```text
new version
correction record
supersession
```

rather than delete inconvenient history.

---

# 150. Source Tampering

If an acquired artefact changes at the same URI:

```text
hash A
     ↓
hash B
```

Baobab SHALL treat the new content as a new artefact/version unless proven otherwise.

It SHALL not overwrite the original silently.

---

# 151. Hashes

Cryptographic hashes MAY support:

```text
integrity
deduplication
change detection
evidence identification
```

A hash proves content equality relative to bytes.

It does not prove legal authority.

---

# 152. Digital Signatures

Where authorities provide cryptographically signed artefacts, Baobab SHOULD preserve and verify signatures where technically feasible.

Signature verification establishes integrity/authenticity properties.

It does not independently determine substantive applicability.

---

# 153. Source Freshness

An authentic source may become stale.

Therefore:

```text
AUTHENTIC
```

does not mean:

```text
CURRENT
```

Source freshness is an independent dimension.

---

# 154. Superseded Authority

A repealed rule may remain:

```text
authentic
historically authoritative
```

while not:

```text
currently applicable.
```

This is why temporal state must not be encoded as source trust.

---

# 155. Regulatory Change

When law changes:

```text
Source v1
     │
     ▼
Source v2
```

Baobab SHALL determine whether:

```text
legal text changed
interpretation changed
rule changed
applicability changed
```

These are different forms of change.

---

# 156. Baobab Interpretation Change Without Legal Change

It is possible for:

```text
source unchanged
```

while:

```text
Baobab interpretation corrected
```

The system SHALL represent this explicitly.

This is vital for incident analysis.

---

# 157. Legal Change Without Interpretation Change

Likewise, a legal amendment might not affect a particular Baobab rule.

Change detection SHOULD not assume every source update changes every downstream interpretation.

---

# 158. Interpretation Impact Graph

The provenance structure should eventually enable:

```text
Changed provision
      │
      ▼
Affected interpretations
      │
      ▼
Affected rules
      │
      ▼
Affected decisions
      │
      ▼
Affected transactions
```

This becomes foundational for `ADR-REG-0023`.

---

# 159. Source-Level Impact

Conversely:

```text
Source found unreliable
```

should allow Baobab to determine:

```text
which rules depended upon it?
```

This is one of the commercial advantages of first-class provenance.

---

# 160. Regulatory Evidence Bundle

A decision evidence bundle SHOULD distinguish:

```text
PRIMARY AUTHORITY

OFFICIAL SUPPORTING MATERIAL

BAOBAB INTERPRETATION

BAOBAB RULE

TENANT EVIDENCE

ASSESSMENT

DECISION
```

rather than returning an undifferentiated ZIP archive.

---

# 161. Cross-Engine Consumption

Trade, ERP, CMS, IAM and Pulse SHALL normally consume:

```text
decision
obligations
requirements
source references
assurance state
```

They SHALL not need to understand the full legal corpus.

---

# 162. Consumers Must Not Promote Authority

Trade SHALL NOT receive:

```text
Baobab interpretation
```

and then relabel it internally as:

```text
official law.
```

Canonical contracts SHOULD preserve authority metadata across engine boundaries.

---

# 163. Pulse Boundary

Pulse MAY analyse:

```text
regulatory changes
regulatory uncertainty
regulatory exposure
```

But Pulse SHALL consume Baobab Regulations' authority distinctions.

A Pulse insight SHALL not convert:

```text
proposed regulation
```

into:

```text
effective obligation.
```

---

# 164. Regulations Boundary with Pulse Evidence

Pulse may discover:

```text
news report about upcoming regulation.
```

That can trigger:

```text
Regulations source discovery
```

It SHALL NOT automatically create:

```text
effective RegulatoryRule.
```

---

# 165. Regulations Boundary with Control Plane Evidence

Control Plane may hold:

```text
organisation licence
registration
tenant evidence
```

Regulations MAY evaluate that evidence.

It SHALL not change its canonical organisational meaning.

---

# 166. Reuse of Evidence Philosophy

This ADR intentionally aligns with existing Baobab evidence architecture:

```text
claim
≠
evidence
≠
verification
≠
canonical fact
```

The regulatory equivalent is:

```text
source
≠
representation
≠
interpretation
≠
rule
≠
assessment
≠
decision.
```

This consistency across Baobab is deliberate.

---

# 167. LegalRuleML Influence

OASIS LegalRuleML explicitly models legal characteristics including:

```text
obligations
permissions
prohibitions
rights
temporality
jurisdiction
defeasibility
authorial tracking
links between rules and natural-language provisions
```

which validates the need for Baobab to preserve richer authority and provenance semantics rather than reduce regulation to anonymous Boolean expressions.

Baobab SHALL borrow semantic concepts selectively.

It is not required to use LegalRuleML XML as its internal persistence model.

---

# 168. W3C PROV Influence

W3C PROV models:

```text
Entities
Activities
Agents
Derivations
Revisions
Responsibility
```

and explicitly supports tracking derivation and responsibility across data transformations.

Baobab Regulations SHOULD remain conceptually compatible with those provenance ideas.

---

# 169. RegGenome Market Validation

RegGenome's current commercial model emphasises structured machine-readable regulatory requirements that remain linked to source text, enabling applicability analysis and audit-ready traceability.

This validates the commercial importance of provenance.

Baobab's intended differentiation remains further downstream:

```text
source-linked regulation
      +
Baobab context
      +
operational assessment
      +
cross-engine execution.
```

---

# 170. Authority-Safe AI Principle

The architecture SHALL adopt:

> **No AI output may acquire greater authority merely by being transformed, repeated, summarised or displayed by Baobab.**

This applies recursively.

---

# 171. Authority Monotonicity Rule

Transformations may preserve or reduce usable authority.

They SHALL NOT automatically increase it.

Conceptually:

```text
secondary commentary
     ↓
LLM extraction
     ↓
structured rule
```

cannot become:

```text
PRIMARY AUTHORITATIVE
```

without additional authoritative evidence.

---

# 172. Authority Enrichment

Authority can only increase when additional evidence is attached.

Example:

```text
commercial rule
      +
verified official provision
      +
review
```

may become:

```text
verified Baobab-derived rule
```

It still does not become:

```text
authority-issued rule
```

unless the authority issued it.

---

# 173. No "Official" Branding Without Basis

UI, API or documentation SHALL NOT label:

```text
OFFICIAL
```

unless the underlying source relationship supports that term.

Marketing language is not exempt from architectural truth.

---

# 174. No "Legally Approved" Status

Baobab SHALL NOT expose generic status:

```text
LEGALLY_APPROVED
```

unless that status genuinely reflects approval from an identified legally competent authority.

Preferred:

```text
BAOBAB_VERIFIED
TENANT_COUNSEL_APPROVED
AUTHORITY_ISSUED
```

as separate states.

---

# 175. No Universal "Compliant"

Likewise:

```text
transaction.compliant = true
```

is too vague.

Compliance must answer:

```text
compliant with what
under which rules
at what time
for which context
```

This follows the broader Baobab principle already established for organisation compliance.

---

# 176. Decision Language

Preferred:

```text
Regulatory assessment passed
under rule set X
for context Y
at effective time Z.
```

Rather than:

```text
This business is compliant.
```

---

# 177. Rejected Alternative — Single Source Ranking

Rejected:

```text
1. Government
2. Commercial Provider
3. News
```

Reason:

Legal authority is jurisdictional and claim-specific.

A court, customs ruling, regulator notice and statute cannot be ordered meaningfully with one universal ranking.

---

# 178. Rejected Alternative — Confidence Score

Rejected:

```text
legal_confidence = 94%
```

Reason:

It conflates authority, interpretation, applicability and evidence.

---

# 179. Rejected Alternative — LLM as Interpreter of Record

Rejected:

```text
source document
      ↓
LLM
      ↓
production legal rule
```

without explicit interpretation artefact, review and provenance.

---

# 180. Rejected Alternative — Commercial Vendor as Canonical Authority

Rejected:

```text
Vendor API says X
therefore X = law
```

Baobab SHALL preserve underlying authority where available.

---

# 181. Rejected Alternative — Human Reviewer as Authority

Rejected:

```text
Baobab analyst approved
therefore legal authority established.
```

Human review verifies Baobab interpretation.

It does not create sovereign law.

---

# 182. Rejected Alternative — Flatten Everything into a Knowledge Graph

Rejected:

```text
all nodes equally trusted
```

Graph connectivity does not imply authority equivalence.

Edges and node types must preserve provenance semantics.

---

# 183. Rejected Alternative — Mutable Canonical Rule

Rejected:

```text
update rule row
with latest interpretation.
```

This destroys historical explainability.

Rule and interpretation versions must remain traceable.

---

# 184. Rejected Alternative — Citation-Only Trust

Rejected:

```text
answer has citations
therefore answer is authoritative.
```

Citations must support the exact claim and preserve source status.

---

# 185. Consequences — Positive

This ADR enables:

```text
defensible regulatory decisions
clear source attribution
historical replay
human review
AI containment
customer counsel integration
authority-aware UI
cross-engine trust
change impact
regulatory audit
provider neutrality
```

---

# 186. Consequences — Commercial

Customers can ask Baobab:

```text
Why did you reach this result?
```

and receive:

```text
authority
instrument
provision
interpretation
rule
assessment
decision
```

rather than:

```text
"The AI says so."
```

That is a substantial enterprise trust advantage.

---

# 187. Consequences — Negative

This architecture requires more entities and governance than a simple rules database.

It adds:

```text
source modelling
authority modelling
provenance
interpretation versions
review workflows
conflict handling
decision lineage
```

That complexity is accepted.

A regulatory system that hides these distinctions would be simpler and less trustworthy.

---

# 188. Consequences — Data Volume

Preserving source versions, interpretations and decision evidence increases storage.

This is accepted.

Historical regulatory explainability is more important than saving modest storage cost.

---

# 189. Consequences — Human Expertise

Some regulatory interpretations will require domain specialists.

The platform cannot automate away genuine legal ambiguity.

This is accepted.

The engine must know when automation should stop.

---

# 190. Architectural Invariants

| ID | Invariant |
|---|---|
| `REG-A-I01` | Baobab never becomes sovereign legal authority merely by storing regulation |
| `REG-A-I02` | Source, representation, interpretation, rule, assessment and decision remain distinct |
| `REG-A-I03` | Authority SHALL NOT be represented by one universal score |
| `REG-A-I04` | Authority, accuracy, applicability and decision assurance remain separate |
| `REG-A-I05` | Every production rule SHALL retain source provenance |
| `REG-A-I06` | Baobab-derived and authority-supplied machine rules remain distinguishable |
| `REG-A-I07` | AI model output cannot self-establish legal authority |
| `REG-A-I08` | Natural-language explanations cannot override structured decisions |
| `REG-A-I09` | Generated citations cannot enter production provenance without verification |
| `REG-A-I10` | Official guidance SHALL not automatically equal binding legislation |
| `REG-A-I11` | Commercial regulatory providers SHALL not automatically become legal authorities |
| `REG-A-I12` | Authenticity and legal force are separate |
| `REG-A-I13` | Historical source and interpretation versions SHALL remain traceable |
| `REG-A-I14` | Conflicting sources and interpretations must be representable |
| `REG-A-I15` | Translation provenance must be preserved |
| `REG-A-I16` | Human review establishes review, not sovereign authority |
| `REG-A-I17` | Tenant counsel interpretations SHALL remain scoped and attributable |
| `REG-A-I18` | Source licensing and source authority are different dimensions |
| `REG-A-I19` | Missing evidence SHALL not silently imply permission |
| `REG-A-I20` | Every consequential decision must support backward provenance traversal |
| `REG-A-I21` | Source transformations SHALL not silently increase authority |
| `REG-A-I22` | Authority terminology in UI/API SHALL accurately reflect provenance |
| `REG-A-I23` | Search rank, retrieval similarity and model confidence are not authority |
| `REG-A-I24` | Current and historical authority states must remain separable |
| `REG-A-I25` | Regulatory ambiguity is valid domain state |

---

# 191. Initial Implementation Proof

The first production-quality proof SHOULD demonstrate:

```text
1.
Acquire an official Uganda Gazette artefact.

2.
Identify its issuing/publication authority.

3.
Hash and preserve the acquired artefact.

4.
Extract a specific provision.

5.
Create a Baobab structured representation.

6.
Create a distinct interpretation.

7.
Record interpretation provenance.

8.
Review the interpretation.

9.
Generate an executable rule.

10.
Verify that rule against the interpretation.

11.
Evaluate a ZuriBeans regulatory context.

12.
Produce a RegulatoryAssessment.

13.
Produce a RegulatoryDecision.

14.
Generate a human explanation.

15.
Traverse from decision back to official source.

16.
Change the interpretation.

17.
Preserve the original decision and interpretation.

18.
Re-run the transaction under the new interpretation.

19.
Show that source authority remained unchanged
while Baobab interpretation changed.
```

That would prove the essential architecture.

---

# 192. Second Proof — South Africa

A second proof SHOULD use:

```text
Government Gazette / SARS / ITAC regulatory material
```

and demonstrate that Baobab distinguishes:

```text
official instrument
official guidance
operational procedure
Baobab interpretation
derived machine rule
```

rather than labelling everything:

```text
South African law.
```

---

# 193. AI Proof

The implementation SHOULD deliberately test an LLM that:

```text
hallucinates a regulation number
```

or:

```text
creates a plausible but false citation.
```

The architecture SHALL reject that source from production provenance.

This SHOULD become a mandatory security/regression case.

---

# 194. Conflict Proof

The implementation SHOULD demonstrate:

```text
Source A
  conflicts with
Source B
```

and show:

```text
CONFLICT
→ REVIEW_REQUIRED
```

rather than silent selection.

---

# 195. Historical Proof

The implementation SHOULD demonstrate:

```text
Rule v1
produced Decision A
```

followed by:

```text
Interpretation correction
Rule v2
produces Decision B
```

while Decision A remains fully explainable against v1.

---

# 196. Follow-On ADR Dependency

This ADR enables:

```text
ADR-REG-0004
Advisory, Review and Enforcement Decision Classes
```

because the platform can now answer:

```text
How much authority and assurance
does this decision actually have?
```

before deciding whether it may:

```text
inform
warn
require review
or block.
```

It also provides essential foundations for:

```text
ADR-REG-0006
Canonical Regulatory Domain Model

ADR-REG-0007
Jurisdiction, Regulatory Authority
and Legal Hierarchy Model

ADR-REG-0011
Authoritative Source Registry
and Source Trust Model

ADR-REG-0014
Provenance, Citation and Evidentiary Chain

ADR-REG-0015
Temporal Regulation

ADR-REG-0021
AI-Assisted Regulatory Interpretation
```

---

# 197. Research Foundation

This ADR adopts principles supported by several mature external bodies and technologies.

The OECD's Rules-as-Code work distinguishes ordinary user-created machine implementations of law from official machine-consumable rules produced by government.

The OECD's 2026 Law-as-Code consultation proposes state-authorised machine-executable law that remains explicitly linked to authoritative legal text and retains conditions, exceptions, hierarchy, responsibilities, discretion and legal consequences.

OASIS LegalRuleML provides an established semantic framework covering obligations, permissions, prohibitions, temporality, jurisdiction, defeasibility, authorial tracking and mapping to natural-language legal provisions.

W3C PROV provides a mature conceptual architecture for recording entities, activities, agents, derivation, revision and responsibility in provenance chains.

NIST warns that generative AI can confidently generate false content, logic and citations, particularly creating risk when users rely on the output in consequential domains.

RegGenome provides current commercial validation for structured source-linked regulatory data and explicitly positions provenance and traceability as core regulatory infrastructure requirements.

Uganda's UPPC identifies the Uganda Gazette as the official government publication for statutory instruments, legal notices and other official legal material, providing an appropriate initial authoritative-source test case.

South Africa's Government Printing Works publishes Government Gazettes, while government portals associate legislation and regulatory notices with Gazette references, providing a second appropriate source-authority test environment.

---

# 198. Final Decision

Baobab Regulations SHALL adopt the following immutable mental model:

```text
                  OUTSIDE BAOBAB

              REGULATORY AUTHORITY
                       │
                       ▼
                LEGAL INSTRUMENT
                       │
                       ▼
                   PROVISION
                       │
                       ▼
               SOURCE ARTEFACT

──────────────── BAOBAB TRUST BOUNDARY ────────────────

                       │
                       ▼
              SOURCE REPRESENTATION
                       │
                       ▼
                 INTERPRETATION
                       │
                       ▼
               EXECUTABLE RULE
                       │
                       ▼
                  ASSESSMENT
                       │
                       ▼
                   DECISION
                       │
                       ▼
                 EXPLANATION
```

Baobab owns everything below its trust boundary.

It does **not** own the authority above it.

Where an authority itself supplies machine-executable law:

```text
Authority
    │
    ├── Human-readable law
    │
    └── Authoritative machine rule
```

Baobab SHALL preserve that distinction and consume the authority-supplied representation rather than pretending Baobab authored it.

The cardinal architectural rule established by this ADR is:

> **Baobab shall never make an interpretation look more authoritative than the source from which it derives.**

And the second is:

> **Baobab shall never hide where legal authority ends and Baobab reasoning begins.**

The entire trust proposition of `baobab-regulations` depends upon these rules.

A customer should eventually be able to open any consequential regulatory decision and see:

```text
Why?
 │
 ▼
Because Rule R applied.
 │
 ▼
Why does Rule R exist?
 │
 ▼
Because Interpretation I represents Provision P.
 │
 ▼
Who issued Provision P?
 │
 ▼
Authority A.
 │
 ▼
Where is the evidence?
 │
 ▼
Source Artefact S.
 │
 ▼
What did Baobab add?
 │
 ▼
The interpretation,
the executable rule,
the contextual assessment,
and the explanation.
```

There must never be any mystery about which part came from government and which part came from Baobab.

That transparency is not a cosmetic compliance feature.

It is foundational Baobab IP.

It gives `baobab-regulations` something substantially more durable than an AI legal assistant:

> **a verifiable chain from sovereign authority to executable business decision.**

---

## Decision Summary

```text
ADR-REG-0003
──────────────────────────────────────────

AUTHORITY

Comes from external competent authorities.

BAOBAB

Acquires
Structures
Interprets
Encodes
Evaluates
Explains

BUT DOES NOT

Create sovereign legal authority.

CHAIN

Authority
  ↓
Instrument
  ↓
Provision
  ↓
Source Artefact
  ↓
Baobab Representation
  ↓
Baobab Interpretation
  ↓
Executable Rule
  ↓
Assessment
  ↓
Decision
  ↓
Explanation

MANDATORY DISTINCTIONS

Authority ≠ Accuracy
Authority ≠ Applicability
Authority ≠ Confidence
Source ≠ Interpretation
Interpretation ≠ Rule
Rule ≠ Assessment
Assessment ≠ Enforcement
AI ≠ Authority

TRUST RULE

Every consequential decision must be
traceable backwards to authoritative
source material.

STRATEGIC RESULT

Baobab can make regulation executable
without pretending that Baobab itself
is the law.
```
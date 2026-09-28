# ADR-REG-0018 — Regulatory Decision and Evaluation Engine

**Status:** Proposed — Foundational Runtime Architecture  
**Decision ID:** `ADR-REG-0018`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Regulatory Evaluation / Assessment / Decision Aggregation / Evidence Satisfaction / Runtime Execution  
**Strategic Classification:** Core Regulatory Decision Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL implement a provider-neutral:

# **Regulatory Decision and Evaluation Engine**

which transforms:

```text
Regulatory Question
        +
RegulatoryContextSnapshot
        +
ApplicableRuleSetSnapshot
        +
Verified Facts
        +
Evidence State
        +
Compiled Rule Evaluations
        ↓
Regulatory Assessment
        ↓
AssessmentOutcome
        ↓
RegulatoryDecision
```

The engine SHALL preserve the distinctions:

```text
RULE EVALUATION
≠
NORMATIVE EFFECT

NORMATIVE EFFECT
≠
REQUIREMENT SATISFACTION

REQUIREMENT SATISFACTION
≠
ASSESSMENT OUTCOME

ASSESSMENT OUTCOME
≠
DECISION EFFECT CLASS

DECISION EFFECT CLASS
≠
OPERATIONAL DISPOSITION

OPERATIONAL DISPOSITION
≠
ENFORCEMENT ACTION.
```

---

# 2. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Permission, Prohibition, Obligation, Exemption, Discretion, Violation and Reparation Semantics`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0017 — Regulatory Context and Applicability Resolution`

---

# 3. Governing Doctrine

> **A regulatory decision is a governed conclusion over applicable law, resolved facts, evidence and uncertainty—not the raw return value of a policy engine.**

---

# 4. Decision Pipeline

The canonical runtime path SHALL be:

```text
Regulatory Question
        │
        ▼
RegulatoryContextSnapshot
        │
        ▼
ApplicableRuleSetSnapshot
        │
        ▼
Fact / Evidence Snapshot
        │
        ▼
Rule Evaluation
        │
        ▼
Normative Effects
        │
        ▼
Requirement Evaluation
        │
        ▼
Conflict / Defeasibility Resolution
        │
        ▼
Materiality Analysis
        │
        ▼
AssessmentOutcome
        │
        ▼
Decision Effect Classification
        │
        ▼
RegulatoryDecision
        │
        ▼
Consumer
        │
        ▼
Operational Disposition / Enforcement
```

---

# 5. OPA Is an Evaluator, Not the Decision Engine

The initial architecture SHALL use OPA as the preferred deterministic evaluator for the BRIR subset defined by `ADR-REG-0016`.

OPA SHALL NOT own:

```text
RegulatoryAssessment

AssessmentOutcome

RegulatoryDecision

DecisionEffectClass

OperationalDisposition.
```

---

# 6. OPA Can Return Structured Results

OPA's Data API can return arbitrary JSON values rather than only Boolean authorization decisions. Its response can also include a `decision_id` when decision logging is enabled.

Baobab SHALL therefore require OPA to return a structured:

```text
RuleEvaluationEnvelope
```

rather than:

```text
allow = true / false.
```

---

# 7. Undefined OPA Result

OPA documents that an undefined policy query can return HTTP `200` without a `result` field.

Therefore:

```text
HTTP 200
≠
VALID REGULATORY RESULT.
```

---

# 8. OPA Readiness

OPA also documents that an instance may answer queries while lacking the policies required for the requested decision, and readiness cannot be inferred merely from the query response.

Baobab SHALL therefore verify:

```text
runtime ready

expected RuleSet loaded

expected bundle revision loaded

expected entrypoint exists

result schema valid.
```

---

# 9. Evaluation Engine Boundary

Conceptually:

```text
Regulations Decision Engine
        │
        ├── Context Resolver
        ├── RuleSet Resolver
        ├── Fact Resolver
        ├── Evidence Evaluator
        ├── Deterministic Rule Evaluator
        │       └── OPA initially
        ├── Normative Aggregator
        ├── Conflict Resolver
        ├── Materiality Evaluator
        ├── Outcome Resolver
        └── Decision Assembler
```

---

# 10. Regulatory Question

Every assessment SHALL evaluate a declared:

```text
RegulatoryQuestion
```

rather than an ambiguous:

```text
"is this compliant?"
```

---

# 11. Initial Question Types

The initial vocabulary SHOULD support:

```text
MAY_TRANSACTION_PROCEED

WHAT_OBLIGATIONS_APPLY

WHAT_REQUIREMENTS_REMAIN

WHAT_DOCUMENTS_ARE_REQUIRED

IS_REQUIREMENT_SATISFIED

IS_ACTION_PROHIBITED

IS_EXPLICIT_PERMISSION_AVAILABLE

WHAT_DUTY_OR_AMOUNT_APPLIES

WHAT_REGULATORY_GAPS_EXIST

WHAT_CHANGED

WHAT_WOULD_APPLY_AT_FUTURE_TIME.
```

---

# 12. Why Question Type Matters

The same regulatory state can produce different useful answers.

Example:

```text
Applicable obligation:
retain records for five years.
```

For:

```text
WHAT_OBLIGATIONS_APPLY
```

it is material.

For:

```text
MAY_SHIPMENT_DEPART_NOW
```

it may not presently block shipment departure.

---

# 13. Assessment Purpose

Every `RegulatoryAssessment` SHALL therefore include:

```text
question

profile

purpose

decision stage.
```

---

# 14. Decision Stage

Possible lifecycle stages include:

```text
PLANNING

QUOTATION

ORDER

PRE_SHIPMENT

EXPORT

TRANSIT

IMPORT

CLEARANCE

DELIVERY

POST_TRANSACTION

PERIODIC_COMPLIANCE.
```

---

# 15. Same Rule, Different Stage

An obligation may be:

```text
applicable
```

during quotation but:

```text
not yet due.
```

It may become:

```text
blocking prerequisite
```

at pre-shipment.

---

# 16. RegulatoryAssessment

Conceptually:

```text
RegulatoryAssessment
├── assessment_id
├── tenant_ref
├── question
├── regulatory_profile
├── context_snapshot_ref
├── applicable_ruleset_snapshot_ref
├── fact_snapshot_ref
├── evidence_set_ref
├── legal_time
├── knowledge_time
├── evaluation_profile
├── rule_results[]
├── normative_effects[]
├── requirement_results[]
├── conflicts[]
├── unknowns[]
├── errors[]
├── coverage
├── assessment_outcome
├── decision_effect_class
├── materiality
├── started_at
├── completed_at
└── provenance
```

---

# 17. Assessment and Decision Remain Separate

`Assessment` determines:

```text
what the regulatory state means.
```

`Decision` determines:

```text
what conclusion Regulations communicates
for the declared question.
```

---

# 18. Why Separate Them

The same assessment may support:

```text
transaction decision

audit report

supplier dashboard

regulatory notification

CMS explanation.
```

---

# 19. Rule Evaluation

Each applicable executable RuleVersion SHALL produce a:

```text
RuleEvaluationResult.
```

---

# 20. RuleEvaluationResult

Conceptually:

```text
RuleEvaluationResult
├── rule_ref
├── rule_version_ref
├── applicability_result
├── truth_state
├── effect_templates[]
├── instantiated_effects[]
├── requirement_templates[]
├── derived_facts[]
├── condition_results[]
├── exception_results[]
├── unknown_facts[]
├── errors[]
├── reason_codes[]
├── evaluator_ref
├── compiled_artifact_ref
├── evaluator_decision_ref?
└── provenance
```

---

# 21. Rule Applicability

Possible values remain:

```text
APPLIES

DOES_NOT_APPLY

DEFEATED

EXEMPTED

INDETERMINATE

ERROR.
```

---

# 22. Rule Truth

Separately:

```text
TRUE

FALSE

UNKNOWN

ERROR.
```

---

# 23. Applicability and Truth Are Different

A rule can be:

```text
APPLIES
```

but its substantive condition may evaluate:

```text
FALSE.
```

---

# 24. Example

Rule:

```text
For imported goods above threshold X,
permit P is required.
```

Context:

```text
import activity applies.
```

Therefore rule applicability:

```text
APPLIES.
```

Transaction value:

```text
below X.
```

Condition:

```text
FALSE.
```

No permit obligation is instantiated.

---

# 25. Material OPA Result

OPA MAY evaluate:

```text
conditions

exceptions

deterministic definitions

calculations

derived facts.
```

The Decision Engine then interprets the structured result according to canonical BRIR semantics.

---

# 26. OPA Result Validation

Before accepting evaluator output, Baobab SHALL validate:

```text
evaluation ID matches

RuleSet fingerprint matches

bundle revision expected

BRIR/compiler version compatible

result schema valid

all rule references known

no unexpected result type.
```

---

# 27. Invalid Result

Unexpected OPA response:

```text
EVALUATOR_PROTOCOL_ERROR.
```

It SHALL NOT become:

```text
FALSE.
```

---

# 28. Missing Result

OPA response without expected result:

```text
EVALUATOR_UNDEFINED.
```

---

# 29. Runtime Error

OPA HTTP/runtime error:

```text
EVALUATOR_RUNTIME_ERROR.
```

---

# 30. Readiness Error

Expected bundle not loaded:

```text
EVALUATOR_NOT_READY.
```

---

# 31. All Are Distinct

```text
FALSE
≠
UNKNOWN
≠
UNDEFINED
≠
ERROR
≠
NOT_READY.
```

---

# 32. Evaluation Profile

Potential profiles:

```text
ADVISORY

STANDARD

HIGH_ASSURANCE

HISTORICAL_REPLAY

FUTURE_SIMULATION

SHADOW.
```

---

# 33. HIGH_ASSURANCE

For E3/E4-capable assessments:

```text
strict evaluator errors

verified context

coverage checks

provenance checks

no unresolved material conflicts

pinned RuleSet

pinned evaluator artifact.
```

---

# 34. SHADOW

`SHADOW` runs a candidate RuleSet without affecting operational disposition.

---

# 35. Future Simulation

Uses:

```text
currently verified future law
+
planned context.
```

It SHALL identify itself as prospective.

---

# 36. Historical Replay

Uses:

```text
historical rules

historical context

historical evidence

historical knowledge perspective.
```

---

# 37. Normative Effect Resolution

Applicable true rules MAY instantiate:

```text
RegulatoryEffect.
```

---

# 38. Effect Types

At minimum:

```text
OBLIGATION

PROHIBITION

PERMISSION.
```

Extended:

```text
RIGHT

POWER

LIABILITY

IMMUNITY

REPARATION.
```

---

# 39. Effect Instantiation

A RuleVersion contains general semantics.

The evaluation produces contextual effect:

```text
Rule:
Importer must hold permit.

Context:
Importer = LegalEntity B.

Effect:
LegalEntity B
is obliged to hold Permit P
for Shipment S.
```

---

# 40. Effect Instance

Conceptually:

```text
RegulatoryEffect
├── effect_id
├── source_rule_ref
├── effect_type
├── bearer_ref
├── auxiliary_party_ref?
├── action
├── object_ref?
├── transaction_ref?
├── temporal_scope
├── requirement_refs[]
├── status
├── materiality
└── provenance
```

---

# 41. Effects Are Addressable

Consequential contextual effects SHOULD have stable IDs.

This permits:

```text
requirement lifecycle

evidence association

notifications

auditing.
```

---

# 42. Obligation Evaluation

An obligation evaluation SHALL answer:

```text
Does the obligation arise?

Who bears it?

When does it become due?

What satisfies it?

Is it currently satisfied?

Has it been violated?
```

---

# 43. Obligation Status

Initial statuses MAY include:

```text
NOT_YET_DUE

PENDING

SATISFIED

PARTIALLY_SATISFIED

UNSATISFIED

VIOLATED

EXEMPTED

WAIVED

EXPIRED

SUPERSEDED

INDETERMINATE.
```

---

# 44. Requirement Status

From ADR-REG-0008:

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

INDETERMINATE.
```

---

# 45. Requirement Evaluation

Each requirement SHALL produce:

```text
RequirementEvaluation.
```

---

# 46. RequirementEvaluation

Conceptually:

```text
RequirementEvaluation
├── requirement_ref
├── source_effect_ref
├── status
├── due_at?
├── evidence_refs[]
├── evidence_assessment_refs[]
├── satisfaction_reason
├── missing_evidence[]
├── remediation?
├── blocking_at_stage?
└── provenance
```

---

# 47. Requirement Is Not Automatically Blocking

Example:

```text
Maintain records for 5 years.
```

This requirement may be:

```text
PENDING
```

but not prevent:

```text
current shipment departure.
```

---

# 48. Stage Materiality

Requirement SHALL therefore have a relationship to:

```text
decision stage

decision question.
```

---

# 49. Prerequisite Requirement

A requirement such as:

```text
obtain import permit before entry
```

can be:

```text
not yet overdue
```

but still:

```text
blocking prerequisite
```

for customs entry.

---

# 50. Due Status ≠ Stage Readiness

This distinction SHALL be explicit.

---

# 51. Prohibition Evaluation

An applicable prohibition SHALL produce:

```text
ProhibitionEffect.
```

---

# 52. Explicit Prohibition

If all conditions are satisfied and no exception/override defeats it:

```text
requested action prohibited
```

may support:

```text
AssessmentOutcome = PROHIBITED.
```

---

# 53. Prohibition Requires Resolved Scope

A candidate prohibition with unknown material condition SHALL produce:

```text
INDETERMINATE
```

not `PROHIBITED`.

---

# 54. Permission Evaluation

Explicit strong permission SHALL be represented where applicable.

---

# 55. Permission Does Not Automatically Mean Proceed

An explicit permission may coexist with:

```text
separate obligation

separate licence requirement

different prohibition.
```

---

# 56. Example

Rule A:

```text
Product may be imported.
```

Rule B:

```text
Importer must hold licence.
```

Permission does not satisfy Rule B.

---

# 57. No Implicit Permission

Absence of prohibition SHALL not create:

```text
PERMISSION.
```

---

# 58. Exemption Evaluation

Verified exemption may:

```text
defeat obligation

defeat prohibition

modify requirement.
```

according to legal semantics.

---

# 59. Exemption Does Not Delete Rule

Rule remains applicable in general.

The contextual effect is:

```text
EXEMPTED.
```

---

# 60. Waiver

Waiver SHALL only be used where:

```text
law permits waiver

competent actor exercised it

scope/time verified.
```

---

# 61. Internal Override Is Different

Baobab human override from ADR-REG-0004:

```text
does not change external law.
```

---

# 62. Violation

A violation is:

```text
an applicable obligation/prohibition
whose legally defined satisfaction state
has been breached.
```

---

# 63. Violation Is Not Evaluation Error

```text
VIOLATED
≠
ERROR.
```

---

# 64. LegalRuleML Alignment

LegalRuleML distinguishes obligations, permissions and prohibitions, models violations, reparations and defeasible rule relationships, and explicitly notes that violation does not itself create logical inconsistency.

Baobab SHALL preserve this distinction.

---

# 65. Reparation

A verified violation MAY activate:

```text
reparative obligation

penalty-related rule

corrective requirement.
```

---

# 66. Primary Violation Remains

A reparative obligation SHALL NOT automatically erase:

```text
the primary violation.
```

---

# 67. Example

```text
Primary:
file by 30 June.

Actual:
not filed.

Result:
VIOLATION.

Reparation:
late filing obligation activates.
```

---

# 68. Sanction Is Not Decision Outcome

A statutory sanction rule MAY be identified.

Baobab SHALL not automatically impose:

```text
maximum fine

criminal conclusion

external reporting
```

unless the relevant legal decision/execution authority belongs to Baobab and is explicitly governed.

---

# 69. Evidence Evaluation Layer

Rule execution SHALL consume:

```text
facts
```

and:

```text
evidence evaluation state.
```

It SHALL not treat a raw uploaded document as proven fact.

---

# 70. Evidence Chain

```text
Evidence
    ↓
EvidenceAssessment
    ↓
Verified / unresolved Fact
    ↓
Rule Evaluation.
```

---

# 71. Evidence Authenticity ≠ Satisfaction

A genuine permit may still:

```text
expire

cover wrong entity

cover wrong product

cover wrong jurisdiction.
```

---

# 72. Evidence Sufficiency

Requirement evaluation SHALL determine:

```text
evidence sufficient

partially sufficient

insufficient

indeterminate.
```

---

# 73. Composite Evidence

If requirement demands:

```text
A AND (B OR C)
```

the evidence evaluator SHALL preserve that structure.

---

# 74. Requirement Satisfaction

The Decision Engine SHALL not use:

```text
document_count > 0
```

as a generic satisfaction algorithm.

---

# 75. Evidence Materiality

Evidence unresolved for an irrelevant requirement SHALL not necessarily make the whole decision indeterminate.

---

# 76. Materiality Is Question-Specific

This is central.

---

# 77. Materiality Model

Each effect/requirement/rule result SHOULD be classified relative to the current decision question as:

```text
DECISIVE

MATERIAL

SUPPORTING

INFORMATIONAL

NOT_MATERIAL_TO_QUESTION.
```

---

# 78. Materiality Is Not Legal Hierarchy

It answers:

```text
Does this fact affect this decision question?
```

not:

```text
Which law outranks another?
```

---

# 79. No Single Materiality Score

Rejected:

```text
materiality = 0.82.
```

Use explicit classification and reasons.

---

# 80. Materiality Example

Question:

```text
MAY_SHIPMENT_DEPART_NOW?
```

Results:

```text
Export permit missing:
DECISIVE

Record-retention obligation:
INFORMATIONAL

Packaging reporting due in 30 days:
MATERIAL but not currently blocking.
```

---

# 81. Regulatory Conflict Resolution

The engine SHALL receive resolved conflicts where possible from the legal hierarchy model.

---

# 82. Conflict Outcomes

Possible:

```text
NO_CONFLICT

CUMULATIVE

RULE_A_CONTROLS

RULE_B_CONTROLS

PARTIAL_DISPLACEMENT

CONTEXT_SPECIFIC_EXCEPTION

UNRESOLVED.
```

---

# 83. Cumulative Effects

Multiple obligations SHALL normally be accumulated.

---

# 84. No Generic "Deny Overrides"

Security-policy systems often use:

```text
deny overrides.
```

That SHALL NOT be a universal regulatory aggregation rule.

---

# 85. Why

A strong permission might lawfully derogate from a general prohibition.

A special rule may override a general one.

A later rule may or may not supersede another.

Legal topology governs this.

---

# 86. DMN Comparison

DMN recognizes multiple hit policies such as `Unique`, `Any`, `Priority`, `First` and `Collect`, demonstrating that multi-rule decision aggregation requires explicit semantics rather than an assumed one-rule result.

Baobab SHALL take the useful lesson:

> **Aggregation semantics must be explicit.**

It SHALL NOT use DMN's generic `Priority` or `First` hit policy as legal precedence.

---

# 87. No Rule Order Semantics

The physical ordering of:

```text
BRIR rules

Rego modules

database rows
```

SHALL NOT determine legal outcomes.

---

# 88. Normative Aggregator

Baobab SHALL implement a:

```text
NormativeEffectAggregator
```

responsible for combining all resolved contextual effects.

---

# 89. Aggregator Inputs

```text
applicable effects

defeated effects

exempted effects

requirements

violations

reparations

permissions

conflict resolutions.
```

---

# 90. Aggregator Output

```text
NormativeState
```

---

# 91. NormativeState

Conceptually:

```text
NormativeState
├── obligations[]
├── prohibitions[]
├── permissions[]
├── rights[]
├── powers[]
├── requirements[]
├── violations[]
├── reparations[]
├── unresolved_effects[]
├── conflicts[]
└── provenance
```

---

# 92. Assessment Outcome Is Not Directly Produced by OPA

OPA may produce individual rule/effect results.

Baobab's Decision Engine SHALL derive:

```text
AssessmentOutcome.
```

---

# 93. Canonical AssessmentOutcome

The canonical values are:

```text
SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE.
```

---

# 94. No `COMPLIANT = TRUE/FALSE`

Rejected as canonical model.

---

# 95. `NOT_APPLICABLE`

Use only when:

```text
declared coverage is sufficient

material candidate rule universe evaluated

no material applicable normative effect exists
for the declared question.
```

---

# 96. `NOT_APPLICABLE` Is Not "We Found Nothing"

If coverage is incomplete:

```text
INDETERMINATE
```

or explicit coverage-gap result is required.

---

# 97. `SATISFIED`

Use when:

```text
material applicable obligations/requirements
relevant to the question are satisfied

no applicable material prohibition blocks the action

no material unknown/conflict/error remains.
```

---

# 98. `SATISFIED` Does Not Mean No Regulation Exists

It means:

```text
applicable requirements relevant to this assessment
are currently satisfied.
```

---

# 99. `SATISFIED_WITH_REQUIREMENTS`

Use where:

```text
the requested activity may presently proceed

BUT

applicable prospective/continuing requirements
remain outstanding or will become due

AND

those requirements do not currently make
the present decision unsatisfied.
```

---

# 100. Example

At quotation stage:

```text
Import permit must exist before customs entry.

Customs entry is 30 days away.

Permit not yet required to issue quotation.
```

Possible:

```text
SATISFIED_WITH_REQUIREMENTS
```

with:

```text
Requirement:
obtain permit before customs entry.
```

---

# 101. Another Example

Shipment is currently ready to leave export warehouse but:

```text
post-import filing due in 10 days.
```

The requirement may remain visible without blocking current stage.

---

# 102. `UNSATISFIED`

Use where:

```text
a material applicable obligation/requirement
that must currently be satisfied
is not satisfied.
```

---

# 103. UNSATISFIED Is Usually Remediable

Examples:

```text
missing certificate

expired permit

required declaration incomplete

required fee unpaid.
```

---

# 104. UNSATISFIED ≠ PROHIBITED

This distinction is fundamental.

---

# 105. `PROHIBITED`

Use where:

```text
an applicable resolved prohibition
legally bars the action/state
for the assessed context
```

and no applicable exception, permission or overriding rule defeats it.

---

# 106. Missing Permit Usually Not Automatically PROHIBITED

If law says:

```text
permit required before import
```

and permit is absent:

```text
UNSATISFIED
```

may be the more precise result.

If the law explicitly makes import without permit prohibited, a prohibition effect may also exist.

The RuleVersion determines semantics.

---

# 107. `INDETERMINATE`

Use when a reliable outcome cannot be reached because of material:

```text
unknown fact

missing evidence

context ambiguity

classification ambiguity

coverage gap

legal conflict

unresolved hierarchy

authority discretion

human judgment

evaluator error

ruleset readiness failure.
```

---

# 108. INDETERMINATE Is a First-Class Result

It SHALL NOT be treated as an error in the business sense.

Uncertainty can be legally correct.

---

# 109. `NOT_APPLICABLE` versus `INDETERMINATE`

```text
NOT_APPLICABLE:
we know the rule does not apply.

INDETERMINATE:
we cannot establish whether it applies
or what conclusion follows.
```

---

# 110. Outcome Resolution Is Not a Simple Severity Sort

Rejected:

```text
PROHIBITED > UNSATISFIED >
INDETERMINATE > SATISFIED.
```

as a universal aggregation algorithm.

---

# 111. Why

Suppose:

```text
Rule A:
clearly prohibits X.

Rule B:
unrelated record-retention fact unknown.
```

Overall:

```text
PROHIBITED
```

may still be determinate.

---

# 112. Opposite Example

```text
Potential prohibition rule:
material classification unknown.
```

Overall cannot safely become:

```text
SATISFIED.
```

Result may be:

```text
INDETERMINATE.
```

---

# 113. Outcome Resolver

The engine SHALL therefore use:

```text
question-specific

materiality-aware

normative-aware
```

resolution.

---

# 114. Conceptual Decision Logic

For `MAY_TRANSACTION_PROCEED`:

```text
1. Verify coverage sufficient.

2. Identify material applicable effects.

3. Resolve all material conflicts.

4. Determine explicit prohibitions.

5. Determine current prerequisite obligations.

6. Determine evidence satisfaction.

7. Determine material unknowns/errors.

8. Determine future/continuing requirements.

9. Produce outcome.
```

---

# 115. Illustrative Outcome Decision Tree

```text
Coverage adequate?
   │
   ├── No ─────────────► INDETERMINATE
   │
   ▼
Material conflict/error unresolved?
   │
   ├── Yes ────────────► INDETERMINATE
   │
   ▼
Material prohibition applies?
   │
   ├── Yes ────────────► PROHIBITED
   │
   ▼
Current mandatory prerequisite unsatisfied?
   │
   ├── Yes ────────────► UNSATISFIED
   │
   ▼
Material required fact/evidence unknown?
   │
   ├── Yes ────────────► INDETERMINATE
   │
   ▼
Future/continuing requirements remain?
   │
   ├── Yes ────────────► SATISFIED_WITH_REQUIREMENTS
   │
   ▼
Material rules apply?
   │
   ├── No ─────────────► NOT_APPLICABLE
   │
   ▼
SATISFIED
```

This is an architectural baseline, not a substitute for domain-specific normative semantics.

---

# 116. Prohibition Check Before Unsatisfied Requirement

This order is useful only after:

```text
legal conflict resolution
```

has determined that prohibition is actually controlling.

It is not generic precedence.

---

# 117. Unknown May Preclude Prohibition Determination

If prohibition applicability is unknown:

```text
do not claim PROHIBITED.
```

---

# 118. Question-Specific Resolvers

Different question types MAY use different outcome functions.

---

# 119. `WHAT_OBLIGATIONS_APPLY`

Should return:

```text
obligations[]
```

rather than forcing all results into one transaction-readiness status.

---

# 120. `WHAT_DOCUMENTS_ARE_REQUIRED`

Should project:

```text
document requirements
```

including:

```text
satisfied

missing

future-due

conditional.
```

---

# 121. `IS_ACTION_PROHIBITED`

Can return:

```text
PROHIBITED

NOT_PROHIBITED_BY_EVALUATED_SCOPE

INDETERMINATE

NOT_APPLICABLE
```

as a question-specific projection.

It SHALL not use `NOT_PROHIBITED` to imply positive legal permission.

---

# 122. Decision Question Contract

Each supported question SHALL define:

```text
required context

required coverage

material effect categories

aggregation semantics

allowed AssessmentOutcomes.
```

---

# 123. DecisionPolicy

Conceptually:

```text
DecisionPolicy
├── question_type
├── policy_version
├── required_profiles[]
├── material_effect_types[]
├── required_coverage
├── unknown_handling
├── conflict_handling
├── requirement_stage_rules
├── outcome_rules
└── max_effect_class
```

---

# 124. DecisionPolicy Is Baobab Governance

It SHALL not redefine the underlying law.

It governs how canonical regulatory state is projected into a requested decision.

---

# 125. Example

Law says:

```text
certificate required before import.
```

DecisionPolicy for:

```text
QUOTATION_READINESS
```

may classify missing certificate:

```text
future requirement.
```

DecisionPolicy for:

```text
CUSTOMS_ENTRY_READINESS
```

may classify it:

```text
current unsatisfied prerequisite.
```

The law has not changed.

The decision stage has.

---

# 126. Decision Policy Versioning

Every consequential assessment SHALL identify:

```text
decision_policy_version.
```

---

# 127. Material Unknown

A material unknown SHALL be represented explicitly.

---

# 128. UnknownReason

Potential:

```text
FACT_NOT_PROVIDED

FACT_NOT_VERIFIED

EVIDENCE_MISSING

EVIDENCE_CONFLICT

CLASSIFICATION_UNRESOLVED

JURISDICTION_UNRESOLVED

LEGAL_INTERPRETATION_UNRESOLVED

AUTHORITY_DECISION_PENDING

HUMAN_JUDGMENT_REQUIRED

COVERAGE_INCOMPLETE.
```

---

# 129. ErrorReason

Separately:

```text
EVALUATOR_FAILURE

INVALID_RULE

TYPE_ERROR

CALCULATION_ERROR

RULESET_MISMATCH

PROVIDER_UNAVAILABLE

PROTOCOL_ERROR.
```

---

# 130. Unknown and Error May Lead to Same Outcome

Both may produce:

```text
INDETERMINATE.
```

But remediation differs.

---

# 131. Remediation

Every non-satisfied result SHOULD identify available:

```text
RemediationAction[]
```

where appropriate.

---

# 132. Remediation Types

Possible:

```text
PROVIDE_FACT

PROVIDE_DOCUMENT

OBTAIN_PERMIT

RENEW_LICENCE

COMPLETE_FILING

PAY_REQUIRED_AMOUNT

RESOLVE_CLASSIFICATION

REQUEST_REVIEW

OBTAIN_AUTHORITY_DECISION

CORRECT_CONTEXT

WAIT_UNTIL_EFFECTIVE_DATE

CHANGE_TRANSACTION.
```

---

# 133. Remediation Is Not Legal Advice by Default

It describes:

```text
what requirement remains
```

or:

```text
what information is needed.
```

It SHALL not claim professional legal advice unless provided under an appropriate product/governance model.

---

# 134. Blocking Status

A requirement MAY expose:

```text
blocking_now

blocking_at_stage

not_blocking.
```

---

# 135. No Universal `blocking=true`

A requirement can change operational materiality as transaction stage changes.

---

# 136. AssessmentOutcome and Effect Class

After AssessmentOutcome, `ADR-REG-0004` governs:

```text
DecisionEffectClass.
```

---

# 137. Effect Classes

Existing canonical model:

```text
E0 — Informational

E1 — Advisory

E2 — Review Gate

E3 — Conditional Enforcement

E4 — Automated Enforcement.
```

---

# 138. AssessmentOutcome Does Not Automatically Determine Effect Class

Example:

```text
PROHIBITED
```

under an immature, human-reviewed RuleVersion may still have:

```text
E2
```

maximum effect.

---

# 139. Another Example

```text
UNSATISFIED
```

from a deterministic verified permit prerequisite may support:

```text
E3.
```

---

# 140. Enforcement Ceiling

Effective class SHALL be:

```text
min(
 rule assurance ceiling,
 decision policy ceiling,
 coverage/readiness ceiling,
 context/evidence assurance ceiling,
 runtime readiness ceiling
)
```

Conceptually.

This is not a numeric ranking implementation requirement; it means no layer may escalate beyond its approved capability.

---

# 141. Consumer Cannot Escalate

Trade SHALL NOT request:

```text
"treat this E1 result as E4."
```

---

# 142. OperationalDisposition

Regulations MAY recommend or return a typed:

```text
OperationalDisposition
```

separate from AssessmentOutcome.

---

# 143. Potential Dispositions

Initial vocabulary MAY include:

```text
NO_ACTION

PROCEED

PROCEED_WITH_REQUIREMENTS

REVIEW

HOLD

REMEDIATE

BLOCK

ESCALATE.
```

---

# 144. These Are Operational Semantics

They SHALL not replace:

```text
SATISFIED

UNSATISFIED

PROHIBITED

INDETERMINATE.
```

---

# 145. Example

```text
AssessmentOutcome:
UNSATISFIED

EffectClass:
E3

OperationalDisposition:
HOLD
```

Reason:

```text
required permit missing.
```

---

# 146. Another Example

```text
AssessmentOutcome:
PROHIBITED

EffectClass:
E1

OperationalDisposition:
REVIEW
```

because the underlying interpretation is not approved for enforcement.

---

# 147. Enforcement Action

Actual:

```text
cancel shipment

freeze order

reject filing

prevent checkout
```

belongs to the relevant domain PEP.

---

# 148. Regulations Is PDP

Consistent with prior ADRs:

```text
Regulations
    = regulatory PDP.

Trade / ERP / Digital Estate
    = operational PEP.
```

---

# 149. Decision Contract

Conceptually:

```text
RegulatoryDecision
├── decision_id
├── assessment_ref
├── question
├── outcome
├── effect_class
├── recommended_disposition
├── material_effects[]
├── material_requirements[]
├── violations[]
├── prohibitions[]
├── permissions[]
├── unknowns[]
├── errors[]
├── remediation[]
├── reason_codes[]
├── context_snapshot_ref
├── ruleset_snapshot_ref
├── evidence_set_ref
├── decision_policy_version
├── evaluator_metadata
├── valid_until?
├── staleness_conditions[]
├── decided_at
└── provenance
```

---

# 150. Decision Has Identity

Consequential decisions SHALL be durably addressable.

---

# 151. Decision Is Immutable

Materially revised conclusion creates:

```text
new decision
```

or:

```text
superseding decision.
```

---

# 152. Decision Supersession

```text
Decision D2
    SUPERSEDES
Decision D1.
```

---

# 153. Correction

Correction SHALL preserve:

```text
D1

reason

D2.
```

---

# 154. Decision Validity

A decision SHOULD identify conditions under which it becomes stale.

---

# 155. Staleness Triggers

Examples:

```text
transaction changed

planned date changed

classification changed

permit expired

evidence revoked

RuleSet changed

relevant future rule became effective

jurisdiction changed.
```

---

# 156. `valid_until`

Where determinable, decision MAY expose:

```text
valid_until.
```

---

# 157. But Legal Change Can Be Unscheduled

Therefore:

```text
valid_until
```

does not guarantee the decision remains valid if a material regulatory change occurs first.

---

# 158. Staleness Condition Set

Preferred:

```text
DecisionValidity
├── valid_until?
├── ruleset_change_invalidates
├── context_change_invalidates
├── evidence_change_invalidates
└── relevant_event_time_boundary?
```

---

# 159. Decision Reuse

Consumers MAY reuse a prior decision only if:

```text
context fingerprint matches

RuleSet compatible

evidence state unchanged

decision unexpired

staleness trigger absent.
```

---

# 160. Idempotency

Repeated identical evaluation SHOULD support idempotent behaviour.

---

# 161. EvaluationRequest

Conceptually:

```text
EvaluationRequest
├── idempotency_key?
├── question
├── context_ref
├── profile
├── legal_time
├── knowledge_time
└── requested_mode
```

---

# 162. Same Request, Same Snapshot

For deterministic evaluation over identical immutable inputs:

```text
semantic result SHOULD be identical.
```

---

# 163. Decision IDs May Differ

Operational requests may produce separate Decision IDs while sharing:

```text
decision_input_fingerprint.
```

Exact idempotency semantics belong to implementation specification.

---

# 164. Input Fingerprint

From ADR-REG-0014:

```text
hash(
 context_snapshot
 + ruleset_snapshot
 + evidence_set
 + decision_policy_version
 + evaluator semantic version
)
```

---

# 165. Decision Trace

Every consequential decision SHALL persist a structured:

```text
DecisionTrace.
```

---

# 166. DecisionTrace Structure

```text
DecisionTrace
├── candidate_rule_count
├── applicable_rule_results[]
├── defeated_rule_results[]
├── normative_effects[]
├── requirement_evaluations[]
├── evidence_evaluations[]
├── conflicts[]
├── materiality_results[]
├── unknowns[]
├── errors[]
├── aggregation_steps[]
├── outcome
└── provenance
```

---

# 167. Aggregation Steps Are Structured

Example:

```text
1. 12 rules considered.
2. 8 applicable.
3. 2 constitutive only.
4. 4 obligations created.
5. 1 prohibition created.
6. prohibition defeated by verified exception.
7. 3 current requirements satisfied.
8. 1 future requirement remains.
9. no material unknowns.
10. outcome SATISFIED_WITH_REQUIREMENTS.
```

---

# 168. This Is Not Hidden Chain-of-Thought

It is a deliberate domain decision trace.

---

# 169. Explanation

Human-facing explanation SHALL be derived from:

```text
DecisionTrace

Rule citations

EvidenceAssessment

Reason codes.
```

---

# 170. LLM May Rewrite Explanation

AI MAY produce clearer language.

The canonical structured explanation remains upstream.

---

# 171. Reason Codes

Stable reason codes SHOULD accompany outcomes.

Examples:

```text
EXPLICIT_PROHIBITION_APPLIES

REQUIRED_PERMIT_MISSING

REQUIRED_CERTIFICATE_EXPIRED

MATERIAL_FACT_UNKNOWN

REGULATORY_COVERAGE_INCOMPLETE

RULE_CONFLICT_UNRESOLVED

ALL_CURRENT_REQUIREMENTS_SATISFIED

FUTURE_REQUIREMENTS_REMAIN

NO_APPLICABLE_RULES_WITHIN_COVERAGE.
```

---

# 172. Reason Codes Are API-Safe

They SHOULD be more stable than prose explanations.

---

# 173. Localisation

CMS/digital estates MAY localise prose explanations while preserving:

```text
reason codes

canonical IDs

citations.
```

---

# 174. Coverage Is Part of Decision Integrity

Decision SHALL include:

```text
CoverageAssessment.
```

---

# 175. CoverageAssessment

Conceptually:

```text
CoverageAssessment
├── requested_profile
├── jurisdictions[]
├── domains[]
├── completeness
├── known_gaps[]
├── freshness
├── blocking_gap
└── provenance
```

---

# 176. Coverage Outcomes

```text
COMPLETE_FOR_DECLARED_SCOPE

PARTIAL

UNAVAILABLE

UNKNOWN.
```

---

# 177. Coverage and SATISFIED

A `SATISFIED` decision SHALL not normally be emitted when:

```text
material coverage = PARTIAL.
```

unless the declared question explicitly permits bounded assessment and communicates that limitation.

---

# 178. Bounded Assessment

Possible:

```text
"Assess customs-document requirements only."
```

Then completeness applies to:

```text
customs-document scope
```

not:

```text
all law applicable to the transaction.
```

---

# 179. Never Claim Universal Compliance

The decision SHOULD state:

```text
scope assessed.
```

---

# 180. Example

Good:

> "Within the South African import-document profile evaluated, the current prerequisites are satisfied."

Bad:

> "This transaction is fully legal."

unless the declared product genuinely covers that much broader conclusion.

---

# 181. Context Completeness

Decision integrity also includes:

```text
ContextCompleteness.
```

---

# 182. Required Context Missing

A material missing context dimension MAY force:

```text
INDETERMINATE.
```

---

# 183. Evidence Completeness

Likewise:

```text
EvidenceCompleteness.
```

---

# 184. Rule Assurance

RuleVersion verification/assurance state contributes to decision effect ceiling.

---

# 185. Runtime Readiness

A valid rule corpus can exist while evaluator runtime is unhealthy.

These SHALL remain distinct.

---

# 186. Readiness Dimensions

Decision engine SHOULD verify:

```text
RuleSet readiness

compiled artifact readiness

OPA readiness

fact-provider readiness

evidence-provider readiness

context readiness.
```

---

# 187. OPA Bundle Identity

Expected bundle revision SHALL be known before E3/E4 evaluation.

---

# 188. OPA Decision Provenance

OPA decision logs can include:

```text
decision_id

trace_id

bundle revision

policy path

input/result.
```


Baobab SHOULD correlate these with the canonical DecisionTrace.

---

# 189. Sensitive Decision Logging

OPA supports masking/erasing fields in decision logs.

Baobab SHALL use such facilities or equivalent controls where inputs contain:

```text
private customer data

privileged evidence

commercially sensitive data.
```

---

# 190. Canonical Decision Remains in PostgreSQL

OPA decision logs SHALL NOT become the source of record.

---

# 191. Rule Evaluation Batching

Applicable RuleSet SHOULD be evaluated as a coherent batch or bounded evaluation unit rather than one remote OPA call per rule.

---

# 192. Why

Benefits:

```text
consistent bundle state

lower latency

clearer trace

fewer network failures.
```

---

# 193. OPA Performance

OPA recommends indexed policy structures and supports partial evaluation/bundle optimization for lower-latency evaluation.

Baobab MAY use these optimizations after semantic equivalence testing.

---

# 194. Optimization Is Runtime Detail

Optimized bundle:

```text
≠ new RuleVersion.
```

---

# 195. Decision Engine Should Be Mostly Deterministic

The fast path SHALL not require:

```text
LLM

Haystack

Qdrant

Docling

LangGraph.
```

---

# 196. Fast Path

```text
Resolved Context
       ↓
Pinned RuleSet
       ↓
Verified Facts/Evidence State
       ↓
OPA / deterministic evaluator
       ↓
Normative Aggregator
       ↓
Decision
```

---

# 197. Slow Path

If evaluation encounters:

```text
human judgment

authority discretion

unresolved interpretation

material conflict
```

the Decision Engine MAY:

```text
create ReviewCase
```

and return:

```text
INDETERMINATE
+
E2 REVIEW.
```

---

# 198. LangGraph Boundary

LangGraph MAY orchestrate that review workflow.

It SHALL NOT replace the canonical assessment/decision state.

---

# 199. Human Review

A reviewer may:

```text
verify fact

resolve permitted interpretation issue

approve override

record authority decision

request evidence.
```

---

# 200. Human Reviewer Cannot Alter Law Casually

Review action must operate within:

```text
scope

authority

governance

provenance.
```

---

# 201. ReviewCase

Conceptually:

```text
ReviewCase
├── review_case_id
├── assessment_ref
├── unresolved_issue_refs[]
├── required_role
├── due_at?
├── status
├── decision?
└── provenance
```

---

# 202. Review Case Outcome

Possible:

```text
FACT_VERIFIED

EVIDENCE_ACCEPTED

EVIDENCE_REJECTED

INTERPRETATION_SELECTED

ESCALATED

AUTHORITY_DECISION_REQUIRED

UNRESOLVED.
```

---

# 203. Review Produces New Assessment Where Material

If a reviewer supplies a material new fact:

```text
new Context/Evidence snapshot
+
new Assessment
```

SHOULD ordinarily follow.

Do not mutate the old decision inputs invisibly.

---

# 204. Assessment Lifecycle

Potential:

```text
REQUESTED

RESOLVING

EVALUATING

REVIEW_REQUIRED

COMPLETED

FAILED

SUPERSEDED.
```

---

# 205. Decision Lifecycle

Potential:

```text
ISSUED

SUPERSEDED

WITHDRAWN

EXPIRED

STALE

CHALLENGED

CONFIRMED

VARIED

REVERSED.
```

---

# 206. Withdrawn

A decision may be withdrawn operationally.

Historical record remains.

---

# 207. Challenge

Consumers MAY challenge a decision by providing:

```text
new evidence

context correction

interpretation dispute.
```

---

# 208. Challenge Is Not Automatic Reversal

It creates:

```text
review / reassessment.
```

---

# 209. External Legal Appeal

Baobab's internal challenge workflow SHALL not be confused with:

```text
statutory appeal to regulator/court.
```

---

# 210. Historical Replay

Given Decision D:

```text
replay
```

SHALL use:

```text
same ContextSnapshot

same RuleSetSnapshot

same evidence state

same DecisionPolicy

same evaluator semantics.
```

---

# 211. Current Reevaluation

Separately:

```text
re-evaluate same transaction
under current law/current knowledge.
```

---

# 212. Difference Report

Baobab SHOULD support:

```text
Historical Decision:
SATISFIED

Current Restatement:
UNSATISFIED

Difference:
late-discovered Rule R17.
```

---

# 213. Reproducibility

The Decision Engine SHALL preserve sufficient inputs to reproduce:

```text
normative result

aggregation

outcome.
```

---

# 214. Exact OPA Instance Is Not Required Forever

Historical replay can use a compatible evaluator if semantic equivalence is proven.

Original:

```text
bundle revision

compiled artifact

decision metadata
```

remain provenance.

---

# 215. Decision Versioning

Decision schema itself SHALL be versioned.

Example:

```text
regulatory-decision/v1.
```

---

# 216. Contract Evolution

New fields SHOULD be additive where practical.

Breaking semantic changes require:

```text
new contract version.
```

---

# 217. Domain Events

Potential events:

```text
regulation.assessment.requested

regulation.assessment.review-required

regulation.assessment.completed

regulation.decision.issued

regulation.decision.superseded

regulation.decision.stale

regulation.requirement.unsatisfied

regulation.requirement.satisfied

regulation.prohibition.detected

regulation.violation.detected.
```

Exact contracts belong in Shared.

---

# 218. Transactional Outbox

Decision issue + outbox event SHALL be transactional where appropriate.

---

# 219. Duplicate Event Handling

Consumers SHALL treat decision events idempotently.

---

# 220. Pulse Integration

Pulse SHOULD consume bounded projections such as:

```text
DecisionOutcome

RegulatoryChangeImpact

RegulatoryRequirementDelta

RegulatoryRiskSignal.
```

---

# 221. Pulse Does Not Re-Decide Law

Pulse MAY conclude:

```text
commercial risk is high
```

from a Regulations decision.

It SHALL not change:

```text
UNSATISFIED → SATISFIED.
```

---

# 222. Pulse Opportunity Example

Regulations:

```text
new tariff requirement applies.
```

Pulse:

```text
margin impact

supplier alternatives

market opportunity.
```

---

# 223. CMS Integration

CMS MAY consume:

```text
publishable decision explanation

requirements summary

citations

effective dates.
```

---

# 224. CMS SHALL Not Expose Private Assessment by Default

Transactional/private decisions remain scoped to authorised consumers.

---

# 225. Trade Integration

Trade consumes:

```text
AssessmentOutcome

EffectClass

OperationalDisposition

Requirements

Decision ID.
```

---

# 226. Trade Enforces

Example:

```text
Regulations:
UNSATISFIED / E3 / HOLD

Trade:
moves shipment to REGULATORY_HOLD.
```

---

# 227. Enforcement Receipt

Trade SHOULD return:

```text
EnforcementReceipt
```

for consequential enforcement.

---

# 228. ERP Integration

ERP MAY consume decisions concerning:

```text
tax

filing

regulatory charges

accounting-related obligations.
```

ERP remains owner of accounting execution.

---

# 229. IAM / Control Plane

IAM authenticates.

Control Plane authorizes platform capability and resolves canonical context.

Regulations determines external regulatory state.

---

# 230. OPA Reuse Across Domains

IAM and Regulations MAY both use OPA.

Their:

```text
policy bundles

schemas

authority sources

decision contracts
```

SHALL remain separate.

---

# 231. Security Authorization Decision

```text
May Principal P invoke endpoint E?
```

is not:

```text
May LegalEntity L import Product X?
```

---

# 232. Decision Engine API

Potential:

```text
POST /regulatory-assessments
```

---

# 233. Request

Conceptually:

```text
{
  question,
  regulatoryProfile,
  contextReference,
  legalTime,
  knowledgeTime?,
  mode
}
```

---

# 234. Response

Conceptually:

```text
{
  assessmentId,
  decisionId,
  outcome,
  effectClass,
  disposition,
  requirements,
  prohibitions,
  permissions,
  unknowns,
  remediation,
  explanation,
  provenanceReference,
  validity
}
```

---

# 235. No Internal OPA Leakage

Consumer API SHALL not expose as primary semantics:

```text
rego_result

opa_query

package.
```

---

# 236. Developer Metadata

Privileged diagnostics MAY expose:

```text
evaluator provider

bundle revision

OPA decision ID

compiler version.
```

---

# 237. Decision SLA

Future commercial SLA may include:

```text
latency

availability

freshness

replayability

coverage.
```

Detailed commercial rules belong to `ADR-REG-0030`.

---

# 238. Latency Classes

Potential:

```text
TRANSACTIONAL

INTERACTIVE

BATCH

REVIEW_REQUIRED.
```

---

# 239. Transactional

Target:

```text
precompiled
no LLM
no document parsing
no external legal-source fetch.
```

---

# 240. Interactive

May include richer explanation but still use pinned law.

---

# 241. Batch

Useful for:

```text
portfolio reassessment

supplier base

open orders

regulatory change blast radius.
```

---

# 242. Review Required

Human workflow latency is separate from deterministic engine latency.

---

# 243. Fail-Closed Semantics

Material infrastructure failure SHALL never silently produce:

```text
SATISFIED.
```

---

# 244. But "Fail Closed" Does Not Mean "PROHIBITED"

Correct regulatory outcome may be:

```text
INDETERMINATE.
```

Operational policy may then:

```text
HOLD.
```

---

# 245. This Distinction Is Fundamental

```text
Regulatory truth:
INDETERMINATE.

Operational risk posture:
HOLD.
```

---

# 246. Example

OPA unavailable.

Correct:

```text
AssessmentOutcome:
INDETERMINATE

OperationalDisposition:
HOLD

Reason:
EVALUATOR_UNAVAILABLE.
```

Wrong:

```text
AssessmentOutcome:
PROHIBITED.
```

---

# 247. Runtime Provider Failure

A technical outage cannot manufacture:

```text
a legal prohibition.
```

---

# 248. Rule Coverage Failure

Likewise, missing regulation pack cannot create:

```text
SATISFIED
```

or:

```text
PROHIBITED.
```

---

# 249. Decision Quality Dimensions

A decision SHOULD be able to report structured assurance on:

```text
coverage

context completeness

rule verification

evidence sufficiency

conflict resolution

temporal certainty

runtime integrity.
```

---

# 250. No Global Trust Score

Rejected:

```text
decision_confidence = 92%.
```

---

# 251. AssuranceSummary

Conceptually:

```text
AssuranceSummary
├── coverage
├── context
├── legal_source
├── interpretation
├── evidence
├── temporal
├── evaluator
└── unresolved_items[]
```

---

# 252. E4 Gate

An E4-capable decision SHOULD require:

```text
coverage sufficient

context materially complete

rules verified/published

BRIR deterministic

compiled artifact validated

runtime ready

material evidence sufficient

no unresolved conflict

no material unknown

legal time resolved

golden tests passing

decision reproducible.
```

---

# 253. E3 Gate

E3 MAY allow:

```text
remediable unmet prerequisite
```

provided underlying legal determination is deterministic and sufficiently assured.

---

# 254. E2 Gate

E2 is appropriate when:

```text
material judgment

ambiguity

conflict

uncertainty

human verification
```

remains.

---

# 255. E1

Useful for:

```text
regulatory advice

warnings

future requirements

lower-assurance interpretation.
```

---

# 256. E0

Pure informational output.

---

# 257. Testing Architecture

The Decision Engine SHALL have its own test suite beyond BRIR/OPA tests.

---

# 258. Test Layers

```text
Rule evaluation tests

Normative aggregation tests

Evidence tests

Materiality tests

Outcome tests

Effect-class tests

Disposition tests

End-to-end decision tests

Historical replay tests.
```

---

# 259. Golden Case — All Satisfied

```text
Applicable obligations:
3

Satisfied:
3

Prohibitions:
0

Material unknown:
0

Outcome:
SATISFIED.
```

---

# 260. Golden Case — Future Requirement

```text
Current prerequisites:
satisfied

future filing:
due after transaction stage

Outcome:
SATISFIED_WITH_REQUIREMENTS.
```

---

# 261. Golden Case — Missing Permit

```text
Permit requirement:
currently prerequisite

Permit:
missing

Outcome:
UNSATISFIED.
```

---

# 262. Golden Case — Explicit Prohibition

```text
Prohibition:
applicable

Exception:
none

Outcome:
PROHIBITED.
```

---

# 263. Golden Case — Prohibition Defeated

```text
General prohibition:
applies

Specific verified permission/exception:
applies and overrides

Outcome:
determined from remaining effects.
```

Not automatically `PROHIBITED`.

---

# 264. Golden Case — Unknown Classification

```text
Classification material.

Unknown.

Potential prohibition depends on it.

Outcome:
INDETERMINATE.
```

---

# 265. Golden Case — Unknown Irrelevant Fact

```text
Record-retention metadata unknown.

Question:
may shipment depart?

All departure prerequisites satisfied.

Outcome need not become INDETERMINATE
if unknown is genuinely non-material.
```

---

# 266. Golden Case — Coverage Incomplete

```text
Customs rules:
covered

SPS pack:
unavailable

Question:
overall import readiness

Outcome:
INDETERMINATE.
```

---

# 267. Golden Case — Bounded Coverage

```text
Question:
customs duty only

Customs pack:
complete

SPS pack:
not requested.

Outcome:
may be determinate for customs duty.
```

---

# 268. Golden Case — Evaluator Undefined

OPA:

```text
HTTP 200
no result.
```

Expected:

```text
EVALUATOR_UNDEFINED

Assessment:
INDETERMINATE.
```

---

# 269. Golden Case — Wrong Bundle

OPA loaded bundle revision differs from expected ruleset artifact.

Expected:

```text
RULESET_RUNTIME_MISMATCH

INDETERMINATE.
```

---

# 270. Golden Case — Runtime Unready

OPA running but required bundle not loaded.

Expected:

```text
EVALUATOR_NOT_READY

not SATISFIED.
```

---

# 271. Golden Case — Multiple Obligations

All applicable requirements accumulate unless legal semantics defeat/replace them.

---

# 272. Golden Case — Conflict

Applicable:

```text
OBLIGATION X

PROHIBITION X
```

No resolved hierarchy.

Outcome:

```text
INDETERMINATE

E2 REVIEW.
```

---

# 273. Golden Case — Violation + Reparation

Primary obligation:

```text
VIOLATED.
```

Reparation:

```text
PENDING.
```

Decision trace retains both.

---

# 274. Golden Case — Historical Replay

Same decision inputs produce historical result using original:

```text
RuleSet

DecisionPolicy

facts

evidence.
```

---

# 275. Golden Case — Current Restatement

Same transaction under newly discovered historical law produces a different assessment without rewriting original Decision.

---

# 276. Golden Case — Future Change

Current transaction stage:

```text
SATISFIED
```

but planned event after future-effective rule:

```text
SATISFIED_WITH_REQUIREMENTS
```

or another prospective result as appropriate.

---

# 277. Golden Case — Tenant Internal Policy

External regulation:

```text
SATISFIED.
```

Tenant internal policy:

```text
requires additional approval.
```

Regulatory outcome remains:

```text
SATISFIED.
```

Operational platform may still:

```text
HOLD FOR INTERNAL APPROVAL.
```

Do not mislabel tenant policy as law.

---

# 278. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-DEC-I01` | OPA SHALL remain a rule evaluator, not the canonical decision owner |
| `REG-DEC-I02` | HTTP success SHALL not imply valid regulatory evaluation |
| `REG-DEC-I03` | Undefined evaluator output SHALL remain distinct from false |
| `REG-DEC-I04` | Runtime readiness SHALL be verified independently of query success |
| `REG-DEC-I05` | Rule evaluation SHALL remain distinct from assessment outcome |
| `REG-DEC-I06` | Normative effect SHALL remain distinct from requirement satisfaction |
| `REG-DEC-I07` | AssessmentOutcome SHALL remain distinct from OperationalDisposition |
| `REG-DEC-I08` | OperationalDisposition SHALL remain distinct from enforcement action |
| `REG-DEC-I09` | UNSATISFIED SHALL remain distinct from PROHIBITED |
| `REG-DEC-I10` | INDETERMINATE SHALL remain a first-class regulatory outcome |
| `REG-DEC-I11` | NOT_APPLICABLE SHALL require sufficient declared coverage |
| `REG-DEC-I12` | SATISFIED SHALL not imply universal legal compliance beyond declared scope |
| `REG-DEC-I13` | Explicit permission SHALL not automatically satisfy independent obligations |
| `REG-DEC-I14` | Absence of prohibition SHALL not create positive permission |
| `REG-DEC-I15` | Cumulative obligations SHALL not be discarded by one-rule winner logic |
| `REG-DEC-I16` | Legal conflicts SHALL not be resolved by rule order |
| `REG-DEC-I17` | Generic deny-overrides SHALL not replace legal hierarchy |
| `REG-DEC-I18` | Material unknowns SHALL prevent false certainty |
| `REG-DEC-I19` | Non-material unknowns SHALL not automatically poison unrelated questions |
| `REG-DEC-I20` | Evaluation shall be question- and stage-aware |
| `REG-DEC-I21` | Coverage, context and evidence assurance SHALL affect decision assurance |
| `REG-DEC-I22` | Technical provider failure SHALL not manufacture legal prohibition |
| `REG-DEC-I23` | Technical failure SHALL never silently produce SATISFIED |
| `REG-DEC-I24` | DecisionEffectClass SHALL never exceed the assurance ceilings established upstream |
| `REG-DEC-I25` | Consumer engines SHALL not escalate regulatory effect class |
| `REG-DEC-I26` | Consequential decisions SHALL use immutable Context and RuleSet snapshots |
| `REG-DEC-I27` | Decisions SHALL carry structured reason codes and traceability |
| `REG-DEC-I28` | Historical replay SHALL preserve historical decision inputs |
| `REG-DEC-I29` | Current reevaluation SHALL not overwrite historical decision state |
| `REG-DEC-I30` | Replacing OPA SHALL not redefine AssessmentOutcome semantics |

---

# 279. Rejected Alternative — `allow: true/false`

Rejected.

Regulation is not merely access control.

---

# 280. Rejected Alternative — OPA Result Equals Regulatory Decision

Rejected.

---

# 281. Rejected Alternative — Undefined Means False

Rejected.

OPA itself distinguishes undefined responses, and Baobab requires explicit semantics above that runtime behaviour.

---

# 282. Rejected Alternative — HTTP 200 Means Ready

Rejected.

OPA's operations guidance explicitly warns that query response alone does not prove operational readiness.

---

# 283. Rejected Alternative — Worst Outcome Wins

Rejected as a generic algorithm.

Materiality and normative relationships matter.

---

# 284. Rejected Alternative — Prohibition Always Wins

Rejected.

Verified exceptions, strong permissions and legal precedence may alter the result.

---

# 285. Rejected Alternative — Missing Requirement = Prohibited

Rejected.

Usually:

```text
UNSATISFIED
```

unless actual rule semantics establish a prohibition.

---

# 286. Rejected Alternative — Unknown = Prohibited

Rejected.

Correct regulatory state:

```text
INDETERMINATE.
```

Operational disposition may still be conservative.

---

# 287. Rejected Alternative — Unknown = Satisfied

Rejected.

---

# 288. Rejected Alternative — No Rule Found = Not Applicable

Rejected without sufficient coverage.

---

# 289. Rejected Alternative — AI Determines Final Runtime Outcome

Rejected for deterministic transactional assessments.

---

# 290. Rejected Alternative — Haystack Runs Regulatory Decisions

Rejected.

Haystack is knowledge-processing infrastructure.

---

# 291. Rejected Alternative — Qdrant Determines Outcome

Rejected.

---

# 292. Rejected Alternative — LangGraph Is the Decision Store

Rejected.

LangGraph may orchestrate review.

---

# 293. Rejected Alternative — Rule Order Aggregation

Rejected.

---

# 294. Rejected Alternative — DMN `First` or `Priority` as Legal Precedence

Rejected.

DMN's hit policies are useful decision-table mechanics, but regulatory precedence belongs to ADR-REG-0007.

---

# 295. Rejected Alternative — One Global Compliance Score

Rejected.

---

# 296. Rejected Alternative — One `compliant=true`

Rejected.

---

# 297. Rejected Alternative — Operational Hold Means Legal Prohibition

Rejected.

---

# 298. Rejected Alternative — Rule Engine Calls External Systems Live

Rejected for the high-assurance fast path.

Facts SHALL be resolved before deterministic evaluation.

---

# 299. Rejected Alternative — Current Law Used for Historical Decision Replay

Rejected.

---

# 300. Minimum Implementation Proof

Before `ADR-REG-0018` is considered implemented, Baobab SHOULD demonstrate:

```text
1. RegulatoryQuestion model.

2. Question-specific DecisionPolicy.

3. Decision-stage model.

4. RegulatoryAssessment aggregate.

5. Structured RuleEvaluationResult.

6. Structured OPA result.

7. OPA undefined-result detection.

8. OPA runtime-error detection.

9. OPA readiness verification.

10. Bundle revision verification.

11. RuleSet runtime mismatch detection.

12. Context snapshot pinning.

13. RuleSet snapshot pinning.

14. Evidence snapshot pinning.

15. Obligation instantiation.

16. Prohibition instantiation.

17. Explicit permission instantiation.

18. Requirement instantiation.

19. Evidence satisfaction.

20. Composite requirement satisfaction.

21. Pending requirement.

22. Future-due requirement.

23. Current blocking prerequisite.

24. Obligation violation.

25. Reparative obligation.

26. Exemption.

27. Waiver.

28. Defeated prohibition.

29. Cumulative obligations.

30. Resolved rule conflict.

31. Unresolved rule conflict.

32. Materiality model.

33. Material unknown.

34. Non-material unknown.

35. Coverage assessment.

36. Coverage-complete NOT_APPLICABLE.

37. Coverage-incomplete INDETERMINATE.

38. SATISFIED.

39. SATISFIED_WITH_REQUIREMENTS.

40. UNSATISFIED.

41. PROHIBITED.

42. INDETERMINATE.

43. NOT_APPLICABLE.

44. AssessmentOutcome distinct from disposition.

45. E0 decision.

46. E1 decision.

47. E2 review-gate decision.

48. E3 conditional enforcement decision.

49. E4 automated enforcement gate.

50. Consumer prevented from effect-class escalation.

51. PROCEED disposition.

52. PROCEED_WITH_REQUIREMENTS disposition.

53. HOLD disposition.

54. REVIEW disposition.

55. BLOCK disposition.

56. Remediation actions.

57. Stable reason codes.

58. Structured DecisionTrace.

59. Human-readable deterministic explanation.

60. OPA decision ID correlation.

61. OPA bundle revision correlation.

62. Sensitive decision-log redaction.

63. Decision input fingerprint.

64. Idempotent repeated evaluation.

65. Decision validity/staleness model.

66. Rule change invalidates prior decision where material.

67. Evidence expiry invalidates prior decision.

68. Context change invalidates prior decision.

69. Historical replay.

70. Historical restatement.

71. Decision supersession.

72. Challenge/reassessment.

73. ReviewCase creation.

74. LangGraph review orchestration seam.

75. Transactional outbox.

76. Decision-issued event.

77. Enforcement receipt.

78. Trade PEP integration.

79. Pulse projection.

80. CMS publishable explanation projection.

81. Batch reassessment.

82. Shadow RuleSet assessment.

83. Candidate/current decision comparison.

84. OPA outage producing INDETERMINATE rather than PROHIBITED.

85. Missing coverage producing INDETERMINATE rather than SATISFIED.

86. Tenant internal policy preserved separately from regulatory outcome.

87. Future-effective decision test.

88. Historical bitemporal decision test.

89. Performance benchmark for representative RuleSet.

90. Decision explainable without Haystack, Qdrant, LangGraph or live regulatory-source access.
```

---

# 301. Initial ZuriBeans Cross-Border Proof

The first meaningful end-to-end proof SHOULD cover a synthetic UG → ZA transaction with:

```text
exporter

importer

coffee/vanilla product

HS classification

export rules

import rules

origin rules

SPS requirement

permit requirement

certificate requirement

document requirement

tariff calculation

future obligation

explicit exception.
```

Actual legal rules SHALL be verified against authoritative sources during jurisdiction-pack implementation.

---

# 302. Example Decision — Ready

Synthetic:

```text
Question:
MAY_TRANSACTION_PROCEED?

Applicable obligations:
4

Current prerequisites:
4

Satisfied:
4

Applicable prohibition:
none

Material unknowns:
none

Future filing:
1
```

Decision:

```text
AssessmentOutcome:
SATISFIED_WITH_REQUIREMENTS

EffectClass:
E3

Disposition:
PROCEED_WITH_REQUIREMENTS
```

---

# 303. Example Decision — Missing Certificate

```text
SPS certificate:
required before export

Evidence:
none
```

Decision:

```text
AssessmentOutcome:
UNSATISFIED

Disposition:
HOLD / REMEDIATE

Reason:
REQUIRED_CERTIFICATE_MISSING.
```

---

# 304. Example Decision — Explicit Prohibition

```text
Product class:
X

Rule:
import prohibited

Exception:
none

Conflict:
none.
```

Decision:

```text
AssessmentOutcome:
PROHIBITED
```

subject to the approved effect class.

---

# 305. Example Decision — Classification Unknown

```text
Potential prohibition depends on HS classification.

Classification:
UNKNOWN.
```

Decision:

```text
AssessmentOutcome:
INDETERMINATE

Disposition:
REVIEW

Reason:
CLASSIFICATION_UNRESOLVED.
```

---

# 306. Example Decision — Platform Outage

```text
Applicable rules:
known

OPA:
not ready / expected bundle unavailable.
```

Decision:

```text
AssessmentOutcome:
INDETERMINATE

Disposition:
HOLD

Reason:
EVALUATOR_NOT_READY.
```

Crucially:

```text
not PROHIBITED.
```

---

# 307. Example Decision — Explicit Permission plus Obligation

```text
Permission:
goods may be imported.

Obligation:
import licence required.

Licence:
missing.
```

Decision:

```text
UNSATISFIED.
```

The permission does not erase the obligation.

---

# 308. Example Decision — Exemption

```text
General requirement:
permit P required.

Verified exemption:
applies to transaction.

Result:
requirement EXEMPTED.
```

Other applicable requirements continue independently.

---

# 309. Example Decision — Late Filing Reparation

```text
Primary filing:
VIOLATED.

Reparative late filing:
PENDING.

Penalty rule:
potentially applicable,
subject to authority determination.
```

Baobab records all three distinct states.

---

# 310. Example Decision — Bounded Assessment

Question:

```text
WHAT_CUSTOMS_DOCUMENTS_ARE_REQUIRED?
```

Coverage:

```text
Customs documentation:
COMPLETE

SPS:
not evaluated.
```

The result SHALL explicitly say:

```text
scope = customs documentation.
```

It SHALL not imply overall import compliance.

---

# 311. Example Decision — Future Shipment

```text
Assessment date:
28 September 2026

Planned import:
15 January 2027

Verified future rule:
effective 1 January 2027.
```

The Decision Engine uses:

```text
legal_time = 15 January 2027
```

and may return future requirements before the rule is currently operative.

---

# 312. Decision Engine Runtime Architecture

```text
                     CONSUMER
                        │
                        ▼
                   CONTROL PLANE
              authz + context/provider
                        │
                        ▼
                REGULATIONS API
                        │
                        ▼
              Regulatory Question
                        │
                        ▼
            RegulatoryContextSnapshot
                        │
                        ▼
           ApplicableRuleSetSnapshot
                        │
                        ▼
             Fact/Evidence Snapshot
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
    Deterministic Evaluator    Evidence Evaluator
           OPA                       │
            │                        │
            └───────────┬────────────┘
                        ▼
                  Rule Results
                        │
                        ▼
               Normative Aggregator
                        │
                        ▼
              Requirement Evaluator
                        │
                        ▼
              Conflict / Materiality
                        │
                        ▼
                 Outcome Resolver
                        │
                        ▼
              RegulatoryAssessment
                        │
                        ▼
                Effect-Class Gate
                        │
                        ▼
               RegulatoryDecision
            ┌───────────┼────────────┐
            ▼           ▼            ▼
          Trade        Pulse         CMS
          /ERP      projection    projection
```

---

# 313. Why OPA Does Not Need to Own Everything

OPA is strongest at:

```text
deterministic predicate evaluation

set logic

structured rule evaluation

precompiled low-latency policy.
```

The Regulations domain is stronger at:

```text
legal provenance

applicability context

evidence state

normative aggregation

decision scope

assurance

decision lifecycle.
```

The combination is deliberate.

---

# 314. OPA Optimization Boundary

OPA supports rule indexing, profiling and partial-evaluation-based bundle optimization for performance.

Baobab MAY use these techniques provided:

```text
semantic equivalence tests pass

golden regulatory cases pass

UNKNOWN/ERROR semantics remain intact.
```

---

# 315. DMN Relationship

DMN may later be useful for:

```text
decision tables

analyst-facing models

decision-policy representation.
```

DMN's explicit hit-policy model demonstrates the importance of defining what happens when multiple rules match.

However:

```text
BRIR
+
Baobab normative aggregation
```

remain authoritative.

---

# 316. LegalRuleML Relationship

LegalRuleML establishes useful formal distinctions among:

```text
prescriptive rules

obligations

permissions

prohibitions

violations

reparations

defeasibility.
```


Those distinctions SHALL survive the entire decision pipeline.

---

# 317. Strategic Capability — Transaction-Level Regulatory Decision

Baobab can answer:

> **Can this exact transaction proceed at this exact stage, under the applicable verified regulatory state, and if not, precisely what remains?**

That is substantially different from regulatory search.

---

# 318. Strategic Capability — Actionable Requirement Set

Instead of:

```text
"South Africa has import regulations."
```

Baobab can return:

```text
Transaction may proceed only after:

1. Permit P is valid.
2. Certificate C is supplied.
3. Declaration D is completed.

Rule X applies.
Rule Y is exempted.
Rule Z becomes relevant after import.

No unresolved material conflicts.
```

---

# 319. Strategic Capability — Regulatory Readiness

A business can assess:

```text
supplier

product

shipment

trade lane

market-entry plan
```

before operational commitment.

---

# 320. Strategic Capability — Machine-Readable Decision

Consumers receive:

```text
canonical decision

not prose chatbot answer.
```

That allows downstream enforcement, auditing and automation.

---

# 321. Strategic Capability — Explainability

Every consequential result can answer:

```text
What rules applied?

Which rules did not?

What obligations arose?

What was satisfied?

What was missing?

Was anything prohibited?

What was unknown?

What evidence supported the result?

What runtime evaluated it?
```

---

# 322. Strategic Capability — Reassessment

When regulation changes:

```text
new RuleSet
      ↓
batch re-evaluation
      ↓
affected decisions
      ↓
new requirements / holds / opportunities.
```

---

# 323. Strategic Capability — Pulse Feedback

Decision changes can become Pulse signals:

```text
new prohibition

new permit burden

new tariff

new market-access requirement

reduced regulatory burden.
```

Pulse can then determine business significance.

---

# 324. Strategic Capability — CMS Explanation

The same structured decision semantics can produce:

```text
customer guidance

market guide

FAQ

regulatory change notice
```

through a rights-safe CMS projection.

---

# 325. Commercial Capability

Potential product surfaces include:

```text
Transaction Regulatory Decision API

Regulatory Readiness API

Outstanding Requirements API

Regulatory Pre-Clearance

Rule Evaluation Trace

Decision Audit Bundle

Portfolio Reassessment

Future Regulatory Readiness.
```

---

# 326. Research Foundation Summary

OPA supports returning arbitrary structured policy values through its Data API rather than requiring Boolean decisions. Its API also distinguishes undefined queries by omitting the `result` field, which means Baobab must treat evaluator protocol state separately from regulatory falsehood.

OPA's operations documentation further warns that successful query responses do not by themselves prove that the policy runtime is operationally ready for the requested decision; an instance may be running without the required policy. Baobab therefore requires explicit RuleSet/bundle readiness checks.

OPA's decision logging supplies traceable decision IDs, trace IDs, policy paths and bundle revisions, making it suitable as one component of Baobab's evidentiary execution chain without replacing the canonical `RegulatoryDecision`.

OPA's performance architecture provides indexing and partial-evaluation-based optimization that can support Baobab's low-latency deterministic fast path after semantic equivalence testing.

LegalRuleML formally distinguishes prescriptive legal rules, obligations, permissions, prohibitions, violations, reparations and defeasible/override relationships. These distinctions reinforce Baobab's decision not to reduce regulatory evaluation to a simple allow/deny policy.

DMN similarly demonstrates that multi-rule decisions require explicit aggregation/hit semantics rather than an assumed single-rule winner. Baobab uses that architectural insight while keeping legal precedence under its own legal-hierarchy and normative models.

---

# 327. Final Decision

Baobab Regulations SHALL implement a **provider-neutral Regulatory Decision and Evaluation Engine** above the deterministic rule evaluator.

Its canonical flow is:

```text
                      REGULATORY QUESTION
                              │
                              ▼
                   REGULATORY CONTEXT
                              │
                              ▼
                    APPLICABLE RULESET
                              │
                              ▼
                     FACTS + EVIDENCE
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
              OPA                     EVIDENCE
        RULE EVALUATION                ENGINE
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    NORMATIVE EFFECTS
                              │
            ┌─────────────────┼──────────────────┐
            ▼                 ▼                  ▼
       OBLIGATIONS       PROHIBITIONS       PERMISSIONS
            │                 │                  │
            └─────────────────┼──────────────────┘
                              ▼
                       REQUIREMENTS
                              │
                              ▼
                     SATISFACTION STATE
                              │
                              ▼
                 CONFLICT / MATERIALITY
                              │
                              ▼
                    ASSESSMENT OUTCOME
                              │
                              ▼
                    EFFECT-CLASS GATE
                              │
                              ▼
                   REGULATORY DECISION
                              │
                              ▼
                OPERATIONAL DISPOSITION
                              │
                              ▼
                     DOMAIN ENFORCEMENT
```

The canonical outcomes are:

```text
SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE.
```

Their meanings SHALL remain distinct.

The governing semantic rule is:

> **Unsatisfied is not prohibited; unknown is not false; technical failure is not prohibition; no rule found is not proof that no law applies.**

The aggregation rule is:

> **Baobab SHALL combine regulatory effects according to their verified legal relationships and materiality to the decision question—not arbitrary rule order, generic deny-overrides or severity ranking.**

The OPA rule is:

> **OPA evaluates compiled BRIR; Baobab Regulations interprets those results within the canonical regulatory domain and issues the regulatory decision.**

The assurance rule is:

> **A decision may be no more consequential than the assurance of its rules, context, evidence, coverage and runtime allows.**

The failure rule is:

> **When Baobab cannot reliably determine the legal conclusion, the regulatory answer is `INDETERMINATE`; an operational policy may then choose a conservative hold without falsely claiming the law prohibits the action.**

The enforcement rule is:

> **Regulations decides; domain engines enforce.**

And the strategic principle is:

> **The value of Baobab Regulations is not merely knowing that a rule exists—it is turning the entire applicable regulatory state into a precise, explainable, auditable and machine-actionable decision for the business transaction in front of us.**

That is the architecture established by `ADR-REG-0018`.

---

## Decision Summary

```text
ADR-REG-0018
────────────────────────────────────────────

INPUT

Regulatory Question
+
ContextSnapshot
+
ApplicableRuleSet
+
Facts
+
Evidence


DETERMINISTIC EVALUATOR

OPA initially.


OPA OUTPUT

Structured rule results.

NOT merely:
allow / deny.


OPA IS NOT

RegulatoryDecision owner.


RULE RESULTS

APPLIES
DOES_NOT_APPLY
DEFEATED
EXEMPTED
INDETERMINATE
ERROR


NORMATIVE EFFECTS

Obligations
Prohibitions
Permissions
Rights
Powers
Reparations


REQUIREMENTS

Satisfied
Pending
Unsatisfied
Violated
Exempted
Indeterminate


ASSESSMENT OUTCOME

SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE


CRITICAL DISTINCTIONS

Unsatisfied
≠
Prohibited

Unknown
≠
False

Technical failure
≠
Legal prohibition

No rule found
≠
No law applies

Assessment outcome
≠
Operational disposition


EFFECT CLASSES

E0 Information
E1 Advisory
E2 Review Gate
E3 Conditional Enforcement
E4 Automated Enforcement


FAILURE

Regulatory result:
INDETERMINATE

Operational result may be:
HOLD


OPA READINESS

Must verify:

bundle
revision
entrypoint
runtime readiness
result schema


PROVENANCE

Decision
→ Assessment
→ Rule results
→ OPA decision ID
→ bundle revision
→ BRIR
→ RuleVersion
→ Provision
→ Source


FAST PATH

No LLM
No Haystack
No Qdrant
No Docling
No live legal-source fetch


PLATFORM

Regulations = PDP

Trade / ERP / Estate = PEP


STRATEGIC RESULT

"What may happen,
what must happen,
what cannot happen,
what remains,
and why?"
```
# ADR-REG-0009 — Normative Semantics, Defeasibility, Discretion, Rights, Violations and Reparative Rules Model

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0009`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Normative Logic / Defeasible Reasoning / Discretion / Violation Architecture  
**Strategic Classification:** Core Regulatory Reasoning IP

**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`

**Relevant Existing Baobab Architecture:**

- `ADR-BCP-020 — Administrative Authority, Delegated Administration, Privileged Access and Separation-of-Duties Model`
- `ADR-BCP-021 — Changeset, Impact Analysis, Approval and Controlled Mutation Model`
- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`
- `ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture`
- applicable Baobab IAM assurance and privileged-authority ADRs
- applicable canonical contracts in `baobab-platform/shared`

**Primary Principle:**

> **Baobab SHALL represent what the law requires, permits, forbids, empowers, exempts and leaves to judgment without silently converting legal nuance into Boolean software logic.**

---

# 1. Executive Decision

Baobab Regulations SHALL implement a canonical normative reasoning model capable of representing:

```text
OBLIGATION

PROHIBITION

EXPLICIT PERMISSION

WEAK / INFERRED PERMISSION

RIGHT

LEGAL POWER / COMPETENCE

EXCEPTION

EXEMPTION

DEROGATION

WAIVER

DEFEASIBLE RULE

DEFEATER

OVERRIDE

DISCRETION

VIOLATION

PENALTY

REPARATION

REMEDIAL OBLIGATION
```

while preserving:

```text
source authority
jurisdiction
legal hierarchy
scope
bearer
counterparty
conditions
exceptions
time
evidence
interpretation
assurance
```

The canonical reasoning model SHALL NOT reduce all regulatory semantics to:

```text
IF condition:
    allow = true
ELSE:
    allow = false
```

The normative pipeline SHALL instead be:

```text
                         FACTUAL CONTEXT
                               │
                               ▼
                         CANDIDATE RULES
                               │
                               ▼
                    CONDITIONS / DEFINITIONS
                               │
                               ▼
                        PRIMARY NORM
                               │
        ┌──────────────────────┼───────────────────────┐
        ▼                      ▼                       ▼
   OBLIGATION             PROHIBITION             PERMISSION
        │                      │                       │
        └───────────────┬──────┴─────────────┬─────────┘
                        │                    │
                        ▼                    ▼
                    EXCEPTIONS           RIGHTS /
                    EXEMPTIONS           POWERS
                        │                    │
                        ▼                    ▼
                    DEFEASIBILITY      DISCRETION
                        │                    │
                        └─────────┬──────────┘
                                  ▼
                            RULE CONFLICT
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                     RESOLVED          UNRESOLVED
                         │                 │
                         ▼                 ▼
                 NORMATIVE EFFECT    REVIEW_REQUIRED
                         │
                         ▼
                    COMPLIANCE /
                     VIOLATION
                         │
                  ┌──────┴────────┐
                  ▼               ▼
              SATISFIED        VIOLATED
                                  │
                                  ▼
                           REPARATIVE RULE
                                  │
                                  ▼
                       PENALTY / REMEDIATION
```

The central doctrine is:

> **The engine SHALL preserve legal uncertainty when the law is uncertain.**

---

# 2. Why This ADR Is Necessary

`ADR-REG-0008` establishes how:

```text
Provision
   ↓
Rule
   ↓
Regulatory Effect
   ↓
Requirement
```

works structurally.

It does not yet fully define what the normative effects **mean**.

Without a normative semantics ADR, several dangerous simplifications could emerge:

```text
no prohibition found
    =
permission

"may"
    =
optional boolean

exception
    =
condition false

rule conflict
    =
latest rule wins

missed requirement
    =
violation

violation
    =
maximum penalty

regulator discretion
    =
algorithm chooses

right
    =
permission

waiver
    =
exemption
```

Every one of these can be legally wrong.

---

# 3. External Research Foundation

LegalRuleML was designed specifically to represent legal norms and reasoning rather than generic business logic. It models obligations, permissions, prohibitions, rights, temporal characteristics, violations, reparations, defeasibility and rule-override relationships. It also distinguishes constitutive and prescriptive rules and recognises that conflicting legal rules may require defeasible rather than classical monotonic reasoning.

This directly validates a richer Baobab normative model.

---

# 4. OECD Law-as-Code Principle

The OECD's current Law-as-Code consultation states that machine-executable law must preserve elements including:

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

and explicitly warns that interpretive, discretionary and evaluative elements should remain visible rather than being silently transformed into deterministic rules.

Baobab SHALL adopt that principle as foundational.

---

# 5. Normative Rule Families

At a high level, Baobab SHALL preserve the distinction between:

```text
CONSTITUTIVE RULE
```

and:

```text
PRESCRIPTIVE RULE.
```

A constitutive rule defines:

```text
what something legally is
```

while a prescriptive rule determines:

```text
what someone must, may or must not do.
```

LegalRuleML makes the same distinction.

---

# 6. Constitutive Rule Example

```text
IF

product satisfies originating criteria

THEN

product has legal status:
ORIGINATING_GOOD
```

That status may then activate:

```text
preferential tariff rule.
```

---

# 7. Prescriptive Rule Example

```text
IF

entity acts as importer
AND
product falls in class X

THEN

importer SHALL possess Permit P.
```

This creates an obligation.

---

# 8. Core Deontic Effects

The initial canonical deontic effects SHALL be:

```text
OBLIGATION

PROHIBITION

PERMISSION
```

LegalRuleML identifies these as core deontic specifications.

Baobab SHALL extend beyond them only where the semantics are clear.

---

# 9. Obligation

An `OBLIGATION` states that its bearer is legally required to:

```text
perform an act
```

or:

```text
maintain a state.
```

Example:

```text
Exporter must submit declaration D.
```

---

# 10. Obligation Is Directed

An obligation SHALL identify its bearer.

Correct:

```text
Bearer:
ZuriBeans Uganda

Obligation:
submit export declaration.
```

Not:

```text
"Declaration required."
```

without identifying who is responsible.

LegalRuleML explicitly treats obligations as directed normative specifications with a bearer.

---

# 11. Obligation Content

Conceptually:

```text
NormativeEffect
├── modality = OBLIGATION
├── bearer_role
├── bearer_ref?
├── action_or_state
├── object?
├── counterparty?
├── temporal_scope
├── requirements[]
├── exceptions[]
└── provenance
```

---

# 12. Achievement Obligation

An achievement obligation requires the relevant act or state to occur at least once within its valid fulfilment period.

Example:

```text
Submit declaration
before 31 March.
```

LegalRuleML explicitly recognises achievement versus maintenance obligations as useful refinements.

---

# 13. Maintenance Obligation

A maintenance obligation requires a state to remain true throughout the relevant period.

Example:

```text
Maintain a valid importer licence
while conducting regulated imports.
```

---

# 14. Continuing Obligation

A continuing obligation may persist after the triggering event.

Example:

```text
Retain records
for five years following importation.
```

---

# 15. Periodic Obligation

Example:

```text
File report
every quarter.
```

The recurrence semantics SHALL remain explicit.

---

# 16. Conditional Obligation

An obligation MAY become active only when a condition is satisfied.

Example:

```text
IF turnover exceeds threshold
THEN submit audited return.
```

---

# 17. Prohibition

A `PROHIBITION` means its bearer is legally forbidden from performing or maintaining the prohibited action/state.

Example:

```text
Importer must not import Product Class X.
```

---

# 18. Prohibition Is Directed

The engine SHALL identify:

```text
who is prohibited
from doing what
under which context.
```

---

# 19. Prohibition versus Obligation of Negation

Formal deontic systems may represent:

```text
PROHIBITION(X)
```

as related to:

```text
OBLIGATION(NOT X).
```

LegalRuleML recognises this traditional relationship.

Baobab SHALL nevertheless preserve `PROHIBITION` explicitly because it carries clearer legal and operational meaning.

---

# 20. Why Explicit Prohibition Matters

These are operationally different:

```text
must not import Product X
```

and:

```text
must ensure Product X is absent from inventory.
```

Their enforcement scope may differ.

---

# 21. Permission

Permission SHALL require more nuanced treatment.

The engine SHALL distinguish:

```text
EXPLICIT / STRONG PERMISSION
```

from:

```text
WEAK / INFERRED PERMISSION.
```

---

# 22. Strong Permission

A strong permission exists where the legal framework explicitly permits an act or creates a permission as an exception or derogation from another rule.

LegalRuleML describes strong permission as explicit permission, typically operating as an exception or derogation from an otherwise applicable obligation or prohibition.

Example:

```text
General rule:
U-turn prohibited.

Specific rule:
Emergency vehicles may perform U-turn
under Condition X.
```

---

# 23. Weak Permission

Weak permission corresponds conceptually to:

```text
no applicable obligation or prohibition
to the contrary
```

rather than an affirmative statement of permission. LegalRuleML distinguishes this from strong permission.

---

# 24. Weak Permission Is Dangerous Operationally

The fact that Baobab did not find a prohibition may mean:

```text
no prohibition exists
```

or:

```text
coverage incomplete
```

or:

```text
required facts missing
```

or:

```text
relevant rule not yet acquired.
```

Therefore weak permission SHALL NOT be treated as high-assurance regulatory approval by default.

---

# 25. Permission Assurance

A permission SHOULD therefore identify:

```text
permission_type

source basis

coverage basis

rule-set completeness

applicable exceptions

assurance.
```

---

# 26. No "No Rule Found = Allowed"

This is a non-negotiable invariant:

```text
NO_RULE_FOUND
    ≠
PERMITTED.
```

---

# 27. Open-World Regulatory Semantics

For consequential regulatory assessment, Baobab SHALL generally operate under an **open-world assumption**:

> Absence of known evidence does not imply the opposite fact.

---

# 28. Example

Unknown:

```text
Does Product P contain regulated substance S?
```

Baobab knows neither:

```text
YES
```

nor:

```text
NO.
```

Therefore the fact remains:

```text
UNKNOWN.
```

---

# 29. Explicit Negation

The engine SHALL distinguish:

```text
NOT_X
```

from:

```text
X_NOT_KNOWN.
```

This is critical.

---

# 30. Closed-World Exceptions

A domain MAY use closed-world reasoning only where:

```text
the dataset is authoritative

the dataset's completeness is established

the law permits that inference

the scope is precisely defined.
```

Example:

```text
official exhaustive list
of prohibited tariff codes.
```

Even there, effective version and scope matter.

---

# 31. Negative Evidence

Baobab SHALL distinguish:

```text
evidence of absence
```

from:

```text
absence of evidence.
```

This aligns with the broader evidence philosophy already established in Pulse and Control Plane.

---

# 32. Right

Baobab SHOULD support `RIGHT` as a richer normative relation.

LegalRuleML models a right as a permission held by a bearer together with corresponding obligations or prohibitions affecting another party.

---

# 33. Right Structure

Conceptually:

```text
RegulatoryRight
├── holder_role
├── holder_ref?
├── permitted_action
├── counterparty_role?
├── correlative_effect_refs[]
├── exercise_conditions[]
├── temporal_scope
└── provenance
```

---

# 34. Right Is Not Merely Permission

Example:

```text
Person has right to receive information.
```

This may imply:

```text
Authority / business
has obligation to provide information.
```

The permission alone does not capture the complete relationship.

---

# 35. Correlative Effects

The model SHOULD therefore support:

```text
Right A
      │
      ▼
correlates_with
      │
      ▼
Obligation B.
```

---

# 36. Legal Power / Competence

The domain SHALL be extensible to represent a **legal power** or **legal competence**:

> the legally recognised ability of an actor to alter a legal or regulatory position through an authorised act.

Examples:

```text
authority may issue permit

authority may revoke licence

customs authority may classify goods

court may invalidate measure

applicant may exercise statutory election.
```

---

# 37. Legal Power Is Not Permission

A regulator being:

```text
permitted to revoke licence
```

is not necessarily the complete semantic meaning.

The act may:

```text
change another person's legal status.
```

That is a different normative function.

---

# 38. Power versus Platform Administrative Authority

Baobab SHALL distinguish:

```text
LEGAL POWER
```

derived from law,

from:

```text
BAOBAB ADMINISTRATIVE AUTHORITY
```

derived from Control Plane governance.

---

# 39. Example

```text
SARS legal power:
issue customs determination
```

is not equivalent to:

```text
Baobab reviewer permission:
approve rule interpretation.
```

---

# 40. Exercise of Legal Power

Where an external authority exercises power:

```text
Power
   ↓
Authority Act
   ↓
Legal State Change
```

Baobab SHALL model the resulting authority determination as external legal evidence/state.

---

# 41. Permission versus Power

The canonical engine SHALL therefore support:

```text
Permission:
actor may do X.

Power:
if authorised actor does X,
legal state Y changes.
```

This distinction becomes important for:

```text
licences

permits

rulings

revocations

registrations

waivers.
```

---

# 42. Exception

A `RULE_EXCEPTION` SHALL represent a condition under which a normally applicable rule does not produce its ordinary conclusion.

Example:

```text
General rule:
Permit required.

Exception:
Permit not required where
quantity < threshold T.
```

---

# 43. Exception Is Structural

An exception belongs to the normative logic of one or more rules.

It SHALL not necessarily create a persistent legal status of its own.

---

# 44. Exception Is Not False Condition

Rejected:

```text
exception exists
=
main condition false.
```

An exception may apply even though the general rule's ordinary antecedent is fully satisfied.

---

# 45. Example

```text
General antecedent:
entity imports Product X.

TRUE.

Exception:
goods are diplomatic shipment.

TRUE.

Result:
general obligation defeated.
```

The general antecedent did not become false.

---

# 46. Exemption

An `EXEMPTION` SHALL represent a legal status or legally recognised relief from an otherwise applicable requirement.

Example:

```text
Entity E
is exempt from Requirement R
under statutory exemption X.
```

---

# 47. Exemption versus Exception

Canonical distinction:

```text
EXCEPTION
=
rule logic that defeats ordinary application

EXEMPTION
=
legal status/fact that may satisfy
an exception or derogation condition.
```

---

# 48. Standing Exemption

Example:

```text
registered diplomatic mission
is exempt from specified duties.
```

This may persist across transactions.

---

# 49. Transaction-Specific Exemption

Example:

```text
Authority grants exemption
for Shipment S.
```

This SHALL remain scoped to that transaction unless the legal source says otherwise.

---

# 50. Exemption Provenance

Every consequential exemption SHALL identify:

```text
legal basis

subject

scope

issuer where applicable

effective period

conditions

revocation state.
```

---

# 51. Waiver

A `WAIVER` SHALL remain distinct from exemption.

A waiver generally represents a competent actor intentionally foregoing or suspending a requirement, right, condition or enforcement consequence where law permits that result.

---

# 52. Waiver Requires Competence

Baobab SHALL NOT permit:

```text
internal administrator
```

to create a legal waiver merely because they have application privileges.

The actor exercising the waiver must possess the relevant legal or tenant authority.

---

# 53. Tenant Waiver versus Regulatory Waiver

A tenant may waive:

```text
internal policy requirement.
```

It may not necessarily waive:

```text
statutory obligation.
```

These SHALL remain distinct.

---

# 54. Derogation

A `DEROGATION` SHALL support situations where a legal rule expressly creates a limited departure from another norm.

This may be:

```text
temporary

actor-specific

territory-specific

subject-specific

emergency-related.
```

---

# 55. Derogation versus Repeal

Derogation does not necessarily repeal the underlying rule.

It may:

```text
limit

suspend

displace
```

its effect in a defined context.

---

# 56. Defeasibility

Baobab SHALL support **defeasible legal reasoning**.

A rule may ordinarily apply while remaining capable of being defeated by:

```text
exception

stronger rule

specific override

legal hierarchy

contextual qualification.
```

LegalRuleML explicitly models defeasibility and rule superiority/override relationships.

---

# 57. Why Classical Boolean Logic Is Insufficient

Suppose:

```text
Rule A:
imports of Product X are prohibited.

Rule B:
licensed research institutions
may import Product X.
```

If both antecedents are true, a simplistic engine produces:

```text
PROHIBITED
AND
PERMITTED.
```

A legal system instead needs:

```text
override / exception semantics.
```

---

# 58. Rule Strength

The canonical rule model SHOULD support a `DefeasibilityProfile`.

Conceptually:

```text
DefeasibilityProfile
├── strength
├── override_relations[]
├── defeater_relations[]
├── exception_refs[]
├── hierarchy_basis_refs[]
└── provenance
```

---

# 59. Initial Strength Types

At minimum:

```text
STRICT

DEFEASIBLE

DEFEATER
```

SHALL be representable where legally meaningful.

LegalRuleML uses analogous concepts.

---

# 60. Strict Rule

A `STRICT` rule means that within the verified formal scope:

```text
when its antecedent holds,
its conclusion follows
```

without ordinary defeasible exceptions represented at that level.

This SHALL be used carefully.

---

# 61. Strict Does Not Mean Constitutionally Unchallengeable

A rule marked `STRICT` in the evaluator does not become legally supreme.

ADR-REG-0007 hierarchy and validity still apply.

---

# 62. Defeasible Rule

A `DEFEASIBLE` rule means:

```text
antecedent holds
    ↓
conclusion ordinarily follows

UNLESS

applicable defeating condition /
higher rule / exception exists.
```

---

# 63. Defeater

A `DEFEATER` SHALL represent a rule that can prevent another conclusion without necessarily asserting the opposite normative conclusion itself.

---

# 64. Why Defeaters Matter

Example:

```text
General rule:
permit normally required.

Defeater:
pending court injunction
prevents enforcement
of permit requirement.
```

This need not necessarily mean:

```text
permit not required forever.
```

---

# 65. Override

`OverrideRelation` SHALL represent legally supported superiority between rules.

Conceptually:

```text
OverrideRelation
├── overriding_rule_ref
├── overridden_rule_ref
├── scope
├── conditions
├── legal_basis_refs[]
├── effective_from
├── effective_to?
└── provenance
```

---

# 66. Override Comes from Legal Topology

The canonical source for override legitimacy SHALL be:

```text
ADR-REG-0007
legal hierarchy
+
source-backed interpretation.
```

No rule engine may invent precedence merely to resolve a contradiction.

---

# 67. Skeptical Conflict Resolution

Where two defeasible rules produce contradictory conclusions and no verified superiority relation exists, the engine SHALL prefer:

```text
UNRESOLVED
```

rather than arbitrarily selecting one.

This mirrors the sceptical approach described by LegalRuleML's defeasible reasoning model.

---

# 68. Unresolved Conflict Effect

A materially unresolved normative conflict SHALL ordinarily propagate:

```text
INDETERMINATE
      ↓
E2 REVIEW_GATE
```

under ADR-REG-0004.

---

# 69. No Last-Writer-Wins

Rejected:

```text
latest rule imported wins.
```

---

# 70. No Highest-ID-Wins

Rejected:

```text
rule.priority = 100.
```

unless that technical priority was deterministically compiled from legally verified relations.

---

# 71. Specificity

A more specific rule may defeat a more general rule where recognised by the applicable legal framework.

Specificity SHALL NOT be globally hard-coded as superior.

---

# 72. Temporality

A later rule may amend or supersede an earlier rule.

Publication date alone is insufficient.

The engine SHALL rely on:

```text
amendment

repeal

commencement

hierarchy

verified interpretation.
```

---

# 73. Permission as Override

A strong explicit permission MAY override:

```text
general prohibition
```

within its authorised scope.

LegalRuleML explicitly recognises strong permission as capable of operating as an exception or derogation from contrary norms.

---

# 74. Weak Permission Cannot Defeat Explicit Prohibition

An inferred lack of prohibition SHALL NEVER override:

```text
verified explicit prohibition.
```

---

# 75. Exemption as Defeating Fact

An exemption status MAY activate:

```text
RuleException
```

and defeat the general obligation.

---

# 76. Revoked Exemption

If the exemption is revoked:

```text
exception condition
```

may cease to hold, causing the general obligation to become applicable again prospectively or according to legal effect.

---

# 77. Discretion

Baobab SHALL treat legal discretion as first-class semantic state.

A rule expressing discretion means that the law permits or requires an authorised actor to exercise judgment among legally available outcomes.

---

# 78. Discretion Must Remain Visible

The OECD's current Law-as-Code framework explicitly states that discretionary and evaluative elements should remain visible rather than being silently converted into deterministic rules.

Baobab SHALL enforce this architectural principle.

---

# 79. Discretion Is Not Randomness

Discretion does not mean:

```text
random choice.
```

It generally means legally bounded judgment.

---

# 80. Discretion Is Not AI Freedom

Discretion SHALL NOT be interpreted as:

```text
LLM can decide.
```

---

# 81. DiscretionaryPower

Conceptually:

```text
DiscretionaryPower
├── holder_role
├── holder_ref?
├── authorised_actions[]
├── preconditions[]
├── relevant_factors[]
├── prohibited_factors[]
├── limits[]
├── procedural_requirements[]
├── reviewability?
├── source_refs[]
└── provenance
```

---

# 82. Examples of Discretionary Language

Potential indicators include:

```text
may

may determine

if satisfied that

where appropriate

reasonable

necessary

material

adequate

in the public interest.
```

These words alone SHALL NOT determine semantics.

They trigger interpretation.

---

# 83. The Word "May"

The parser SHALL NEVER automatically compile:

```text
"may"
```

into:

```text
PERMISSION.
```

Depending on context, "may" may indicate:

```text
permission

legal power

administrative discretion

option

procedural possibility

qualified entitlement.
```

---

# 84. The Word "Shall"

Likewise:

```text
shall
```

often indicates obligation but its actual legal function SHALL be interpreted from context and jurisdiction.

The parser may propose.

It shall not establish meaning autonomously.

---

# 85. Discretionary Decision

When a rule requires external authority discretion:

```text
Baobab cannot substitute itself
for the regulator.
```

Instead the assessment may yield:

```text
AUTHORITY_DETERMINATION_REQUIRED.
```

---

# 86. Example

```text
"The Authority may grant an exemption
if satisfied that conditions A, B and C
are appropriate."
```

Baobab MAY establish:

```text
A = true
B = true
C = true.
```

It SHALL NOT automatically conclude:

```text
exemption granted.
```

The legal power still belongs to the authority.

---

# 87. Discretionary Preconditions

Baobab MAY automate:

```text
whether objective preconditions
for exercise of discretion are met.
```

This can reduce review burden without usurping authority.

---

# 88. Discretionary Outcome

Where several outcomes are legally available:

```text
Outcome A
Outcome B
Outcome C
```

Baobab SHALL represent:

```text
AVAILABLE_OUTCOMES
```

rather than selecting one without authority.

---

# 89. Bounded Discretion

Example:

```text
Authority may impose penalty
between X and Y.
```

Baobab MAY calculate:

```text
legal range = X..Y.
```

It SHALL NOT choose:

```text
penalty = Y
```

without an applicable authority determination.

---

# 90. Human Judgment

Some rules require genuinely evaluative judgment.

Potential canonical state:

```text
HUMAN_JUDGMENT_REQUIRED.
```

This is valid.

---

# 91. Judgment Is Not Failure

A system that correctly identifies:

```text
this question requires authorised judgment
```

is functioning properly.

---

# 92. Discretion Effect Ceiling

Unless a verified authority determination resolves the discretionary question, a rule materially dependent on discretion SHALL ordinarily have maximum effect:

```text
E2 REVIEW_GATE.
```

---

# 93. Authority Determination

Once the competent external authority exercises discretion:

```text
AuthorityDetermination
```

may become a fact in future regulatory evaluation.

---

# 94. Determination Scope

The determination SHALL preserve:

```text
subject

product

entity

transaction

jurisdiction

period

conditions.
```

It SHALL not automatically become universal law.

---

# 95. Internal Business Discretion

Tenant staff may also have internal discretion.

That remains:

```text
business policy
```

not:

```text
regulatory discretion.
```

---

# 96. Violation

A `VIOLATION` SHALL mean that an applicable obligation or prohibition has been breached according to the relevant normative semantics.

LegalRuleML explicitly treats violation as distinct legal state rather than logical inconsistency.

---

# 97. Obligation Violation

Conceptually:

```text
OBLIGATION(X)
+
NOT_X during required period
=
VIOLATION
```

subject to the obligation's temporal semantics.

---

# 98. Prohibition Violation

Conceptually:

```text
PROHIBITION(X)
+
X occurs
=
VIOLATION.
```

---

# 99. Permission Cannot Ordinarily Be Violated

A permission does not command the bearer to act.

Failure to exercise it is therefore not ordinarily a violation.

This is consistent with LegalRuleML's treatment of permissions in reparation structures.

---

# 100. Missing Evidence Is Not Automatically Violation

This distinction is mandatory:

```text
cannot prove compliance
```

does not necessarily mean:

```text
non-compliance occurred.
```

---

# 101. Example

```text
Licence verification service unavailable.
```

Correct:

```text
COMPLIANCE_INDETERMINATE.
```

Not:

```text
VIOLATION.
```

---

# 102. Late Evidence

A business may submit evidence late proving that the underlying obligation was satisfied on time.

Therefore:

```text
evidence received late
```

does not automatically imply:

```text
obligation violated.
```

---

# 103. Violation Finding

Conceptually:

```text
RegulatoryViolation
├── id
├── effect_ref
├── bearer_ref
├── prohibited_or_required_content
├── violation_type
├── occurrence_period
├── fact_refs[]
├── evidence_refs[]
├── verification_state
├── assurance
├── detected_at
├── determined_at?
└── provenance
```

---

# 104. Potential Violation

Where facts are insufficient:

```text
POTENTIAL_VIOLATION
```

SHALL be representable.

---

# 105. Suspected Violation

A weak signal from AI or external report MAY produce:

```text
SUSPECTED_VIOLATION.
```

It SHALL NOT automatically become a verified regulatory breach.

---

# 106. Verified Violation

A high-assurance violation requires:

```text
applicable verified rule

correct bearer

relevant time

facts establishing breach

appropriate evidence

absence of applicable exception.
```

---

# 107. Violation Is Not Enforcement Outcome

A violation does not automatically mean:

```text
terminate

report

fine

block forever.
```

Consequences must themselves have a legal basis.

---

# 108. Penalty

A `PENALTY` SHALL represent a legal sanction potentially arising from a violation.

Examples:

```text
fine

interest

licence suspension

additional restriction

criminal penalty

administrative penalty.
```

---

# 109. Penalty Is Not Automatically Imposed

A source may state:

```text
violation is punishable by fine up to X.
```

This establishes potential legal consequence.

It does not prove:

```text
fine X has been imposed.
```

---

# 110. Penalty Stages

The engine SHALL distinguish:

```text
POTENTIAL_PENALTY

CALCULATED_PENALTY

PROPOSED_PENALTY

AUTHORITY_IMPOSED_PENALTY

PAID / SATISFIED PENALTY
```

where relevant.

---

# 111. Criminal Consequences

Baobab SHALL exercise particular caution around:

```text
criminal liability

criminal penalties

personal culpability.
```

Detection of a regulatory fact SHALL NOT automatically become a conclusion of criminal guilt.

---

# 112. Reparative Rule

A `REPARATIVE_RULE` SHALL represent a rule triggered by violation of another norm.

LegalRuleML explicitly models reparations and chains where violation of one norm activates another normative requirement.

---

# 113. Example

```text
Primary Obligation:
File return by 31 March.

Violation:
Return not filed.

Reparative Rule:
File late return
+
pay prescribed late fee.
```

---

# 114. Reparative Obligation

The resulting:

```text
file late return
```

is itself an obligation.

It SHALL have:

```text
bearer

requirements

deadline

evidence

provenance.
```

---

# 115. Reparation Chain

The engine SHALL be capable of:

```text
Primary Obligation A
       │
       ▼
Violation A
       │
       ▼
Reparative Obligation B
       │
       ▼
Violation B
       │
       ▼
Further consequence C
```

without creating infinite uncontrolled recursion.

---

# 116. Reparative Chain Limits

The evaluator SHALL protect against:

```text
cyclic reparations

accidental infinite rule chains

invalid recursive dependencies.
```

---

# 117. Reparation versus Software Compensation

A legal reparation is not a distributed-system saga compensation.

These concepts SHALL not share semantic classes.

---

# 118. Remedy

Baobab MAY distinguish:

```text
REPARATION
```

as a legally required corrective effect,

from:

```text
REMEDY
```

as broader relief available to an affected party.

Detailed civil-remedy modelling is deferred unless required by product scope.

---

# 119. Defeasible Violation

Even an apparent violation may be defeated by:

```text
exception

exemption

waiver

authority determination

higher rule.
```

Therefore violation evaluation SHALL occur after normative conflict resolution.

---

# 120. Contrary-to-Duty Structures

The rule model SHALL support situations where:

```text
primary duty
```

is violated and:

```text
secondary duty
```

comes into force.

This pattern SHALL not be treated as logical inconsistency.

---

# 121. Example

```text
Primary:
Do not import without Permit P.

If import nevertheless occurs:
Notify Authority within 24 hours.
```

Both rules can coexist.

The second does not imply that importing without permit was permitted.

---

# 122. No "Penalty Means Permission"

The fact that law specifies a penalty for prohibited conduct SHALL never be interpreted as permission to perform the conduct by paying the penalty.

---

# 123. Rights and Correlative Duties

Where useful, Baobab SHOULD represent correlative normative positions.

Example:

```text
Trader has right:
receive written reasons.

Authority has obligation:
provide written reasons.
```

---

# 124. Right Exercise

A right MAY require:

```text
request

application

election

notice
```

before the correlative obligation becomes active.

The activation condition SHALL be explicit.

---

# 125. Legal Entitlement

A legally defined entitlement MAY be represented as:

```text
RIGHT
```

or:

```text
CONSTITUTIVE STATUS + PERMISSION
```

depending on source semantics.

The domain SHALL not force all entitlements into one primitive too early.

---

# 126. Legal Power and Rights

A right to:

```text
apply for licence
```

is distinct from:

```text
authority's power to issue licence.
```

Both can participate in one legal process.

---

# 127. Immunity and Liability

The canonical model SHOULD remain extensible to richer legal positions such as:

```text
LIABILITY

IMMUNITY

POWER

DISABILITY
```

if later domains require them.

They SHALL not be prematurely used in initial cross-border trade rules unless needed.

---

# 128. NormativeEffectType

The canonical enumeration SHOULD therefore initially support:

```text
OBLIGATION

PROHIBITION

PERMISSION_STRONG

PERMISSION_WEAK

RIGHT

LEGAL_POWER
```

with extension capability.

---

# 129. Why Permission Types Are Explicit

A consumer should be able to distinguish:

```text
law explicitly permits this
```

from:

```text
Baobab found no applicable prohibition
within verified coverage.
```

That distinction is commercially important.

---

# 130. Normative Status

A contextual action MAY have an overall normative status such as:

```text
OBLIGATORY

PROHIBITED

EXPLICITLY_PERMITTED

WEAKLY_PERMITTED

CONDITIONALLY_PERMITTED

DISCRETIONARY

INDETERMINATE.
```

This is a derived assessment projection.

It SHALL not replace underlying effects.

---

# 131. Conditioned Permission

Example:

```text
Import is permitted
provided Permit P remains valid.
```

The permission is conditional.

---

# 132. Permission Does Not Cancel Independent Obligations

A transaction may be:

```text
permitted
```

while still having:

```text
reporting obligations

documentary obligations

tax obligations.
```

---

# 133. Prohibition Dominance Must Be Legal, Not Technical

If both:

```text
permission
```

and:

```text
prohibition
```

appear, Baobab SHALL invoke normative conflict resolution.

It SHALL not universally hard-code:

```text
prohibition wins.
```

---

# 134. Strong Permission Can Defeat Prohibition

Where law explicitly establishes the permission as an exception:

```text
strong permission
```

may prevail within its scope.

---

# 135. Normative Conflict

A normative conflict exists where applicable norms require incompatible legal positions.

Examples:

```text
OBLIGATION(X)
+
PROHIBITION(X)

PROHIBITION(X)
+
STRONG_PERMISSION(X)

OBLIGATION(X)
+
OBLIGATION(NOT_X).
```

---

# 136. Normative Conflict Resolution

The order SHALL be:

```text
1. Verify both rules actually apply.

2. Evaluate exceptions.

3. Evaluate exemptions / waivers.

4. Evaluate legal hierarchy.

5. Evaluate explicit overrides.

6. Evaluate temporal relations.

7. Apply verified defeasibility semantics.

8. If still unresolved:
   preserve conflict.
```

---

# 137. No Explosion

Classical logical contradiction SHALL NOT cause arbitrary conclusions.

If contradictory legal rules remain unresolved:

```text
CONFLICT
```

is the result.

---

# 138. Conflict as Evidence

This aligns with the broader Baobab principle:

> **Contradiction is information.**

---

# 139. Alternative Interpretations

The same legal text may support:

```text
Interpretation A
Interpretation B.
```

LegalRuleML explicitly recognises that legal documents may permit multiple incompatible interpretations and provides mechanisms for alternatives.

Baobab SHALL support that reality.

---

# 140. Interpretation-Specific Rules

Different interpretations SHALL generate separate:

```text
RuleVersion
```

or rule-interpretation associations.

They SHALL not overwrite one another.

---

# 141. Platform Default Interpretation

Baobab MAY designate:

```text
PLATFORM_DEFAULT
```

for operational use.

The alternatives remain visible.

---

# 142. Tenant Counsel Interpretation

A tenant MAY select:

```text
TENANT_COUNSEL_APPROVED
```

interpretation within permitted scope.

---

# 143. Interpretation Selection Is Governed

The engine SHALL record:

```text
which interpretation

why

under whose authority

for which scope.
```

---

# 144. AI Alternative Interpretation

AI MAY suggest an alternative interpretation.

It SHALL remain:

```text
CANDIDATE
```

until reviewed.

---

# 145. Normative Confidence Is Not Probability of Law

Avoid:

```text
82% prohibited.
```

unless a narrowly defined statistical meaning exists.

Prefer:

```text
rule verified

facts partial

interpretation disputed

outcome indeterminate.
```

---

# 146. Factual Uncertainty versus Normative Uncertainty

These SHALL be distinct.

```text
FACTUAL UNCERTAINTY:
We do not know product composition.

NORMATIVE UNCERTAINTY:
We know the facts,
but legal interpretation is unresolved.
```

---

# 147. Authority Uncertainty

Separate again:

```text
We know the rule text,
but issuer competence is disputed.
```

---

# 148. Hierarchy Uncertainty

Separate:

```text
Two rules conflict
and controlling precedence is unresolved.
```

---

# 149. Coverage Uncertainty

Separate:

```text
Baobab's relevant regulatory corpus
is incomplete.
```

---

# 150. Evaluation Uncertainty

Separate:

```text
rule semantics supported
but evaluator could not resolve result.
```

---

# 151. UncertaintyReason

The assessment SHOULD support reason codes such as:

```text
MISSING_FACT

MISSING_EVIDENCE

INTERPRETATION_DISPUTED

LEGAL_HIERARCHY_UNRESOLVED

DISCRETION_REQUIRED

AUTHORITY_DETERMINATION_REQUIRED

SOURCE_CONFLICT

COVERAGE_INCOMPLETE

UNSUPPORTED_NORMATIVE_SEMANTIC.
```

---

# 152. No Uncertainty Laundering

An explanation SHALL not convert:

```text
INDETERMINATE
```

into:

```text
probably allowed.
```

unless the underlying decision explicitly supports an advisory probability-style assessment.

---

# 153. Defeasibility and Rule Engine Selection

The future rule evaluator SHALL be capable of representing:

```text
exceptions

override relations

explicit negation

unknown states

conflicts

defeaters

non-monotonic conclusions
```

or Regulations SHALL provide those semantics above the evaluator.

---

# 154. Generic Boolean Rules Engine May Be Insufficient

An engine capable only of:

```text
TRUE / FALSE
```

may not be adequate as the sole normative reasoning layer.

That does not automatically require a specialised legal-logic engine.

---

# 155. Canonical Semantics Before Technology

Baobab SHALL first define:

```text
what the legal semantics mean
```

and only later decide whether those semantics compile into:

```text
Datalog

defeasible logic

Rego

CEL

DMN

custom AST

hybrid evaluation.
```

---

# 156. Hybrid Evaluation Is Permitted

Different rule classes MAY use different evaluators.

Example:

```text
numeric tariff calculation
    → deterministic expression evaluator

document requirement
    → deterministic rules

defeasible exception graph
    → normative reasoning layer

discretion
    → human/authority determination.
```

---

# 157. One Evaluator Need Not Solve All Law

This ADR explicitly rejects the assumption that one generic rule engine must implement every legal reasoning problem.

---

# 158. Deterministic Core

Where law is objectively expressible, Baobab SHOULD use deterministic rules.

---

# 159. Defeasible Layer

Where law includes:

```text
exceptions

overrides

competing norms
```

a defeasible reasoning layer SHALL resolve them where verified.

---

# 160. Judgment Layer

Where the law retains:

```text
discretion

open-textured standards

institutional judgment
```

the result SHALL route appropriately rather than force deterministic execution.

---

# 161. Normative Evaluation Pipeline

The canonical evaluation pipeline SHALL be:

```text
Canonical Facts
      │
      ▼
Constitutive Rules
      │
      ▼
Derived Legal Facts
      │
      ▼
Candidate Prescriptive Rules
      │
      ▼
Conditions
      │
      ▼
Exceptions / Exemptions
      │
      ▼
Deontic Effects
      │
      ▼
Conflicts
      │
      ▼
Hierarchy / Overrides
      │
      ▼
Discretion Check
      │
      ▼
Resolved Normative Effects
      │
      ▼
Requirements / Evidence
      │
      ▼
Compliance / Violation
      │
      ▼
Reparative Rules
```

---

# 162. Constitutive Rules Run Before Dependent Prescriptions

Example:

```text
Rule A:
classifies entity as importer.

Rule B:
importers require Permit P.
```

Rule B cannot evaluate correctly before relevant Rule A result is available.

---

# 163. Derived Legal Facts

Derived legal facts SHALL retain:

```text
rule provenance

input facts

effective time

assurance.
```

---

# 164. Default Logic

Default assumptions SHALL be extremely constrained.

Example:

```text
assume entity is NOT exempt
unless exemption proven
```

may be valid in some rules, invalid in others.

Default semantics SHALL come from the verified rule model, not developer convenience.

---

# 165. Presumption

The model SHOULD remain extensible to legal presumptions.

A presumption is not equivalent to an ordinary factual assertion.

Example:

```text
fact presumed true
unless rebutted.
```

---

# 166. Rebuttable Presumption

Potential future concept:

```text
RebuttablePresumption
├── presumed_fact
├── trigger
├── rebuttal_conditions
└── source_refs
```

This may later prove valuable in tax, customs and corporate regulation.

---

# 167. Irrebuttable / Conclusive Legal Rule

Some statutory constructs may operate conclusively.

These SHALL be modelled only where legally verified.

---

# 168. Presumption versus Default

Developer default:

```text
if null use false
```

is technical.

Legal presumption:

```text
treat fact as true unless evidence rebuts
```

is normative.

Never conflate them.

---

# 169. Burden of Proof

The domain SHOULD remain extensible to represent:

```text
who must demonstrate
a relevant regulatory fact.
```

This becomes important for:

```text
rules of origin

licensing

tax

customs valuation.
```

---

# 170. Burden Is Not Obligation to Do the Underlying Act

Example:

```text
trader bears burden of proving origin
```

is distinct from:

```text
goods actually originated in Uganda.
```

---

# 171. Evidence Standard

Some legal domains may require different evidentiary thresholds.

Baobab SHALL not invent universal standards.

The model may later support:

```text
evidence_standard
```

where required.

---

# 172. Discretion and Relevant Factors

Where an authority's discretion is legally constrained by relevant factors, those factors MAY be represented.

Example:

```text
authority shall consider:
A
B
C.
```

Baobab may verify whether factors were available.

It SHALL not substitute its weighting for the authority unless legally and contractually permitted.

---

# 173. Human Review Interface

When discretion or unresolved norm conflicts require review, the reviewer SHOULD see:

```text
rule text

source provision

facts

candidate effects

exceptions

overrides

alternative interpretations

unresolved question.
```

---

# 174. Reviewer Decision Must Be Typed

The reviewer SHOULD choose among:

```text
CONFIRM_RULE_APPLICATION

APPLY_EXCEPTION

APPLY_EXEMPTION

SELECT_INTERPRETATION

RESOLVE_CONFLICT

REQUEST_MORE_FACTS

AUTHORITY_DETERMINATION_REQUIRED

ESCALATE.
```

Not merely:

```text
Approve / Reject.
```

---

# 175. Reviewer Cannot Invent Law

A reviewer may interpret within delegated authority.

They SHALL not silently create a new platform-wide rule by resolving one transaction.

---

# 176. Reusable Review Determination

Where a review establishes reusable legal interpretation:

```text
case decision
      ↓
candidate interpretation
      ↓
governed promotion
      ↓
new RuleVersion.
```

---

# 177. One-Off Determination

A case-specific determination remains scoped to its case.

---

# 178. Tenant Review

A tenant reviewer MAY resolve:

```text
tenant-specific counsel question
```

without modifying platform global semantics.

---

# 179. NormativeEffect Lifecycle

Different modalities SHALL have different lifecycle behaviour.

Do not force:

```text
OBLIGATION

PERMISSION

PROHIBITION

RIGHT

POWER
```

into one generic `completed=true` model.

---

# 180. Obligation Lifecycle

Possible:

```text
PENDING

ACTIVE

SATISFIED

VIOLATED

EXEMPTED

SUPERSEDED

EXPIRED

INDETERMINATE.
```

---

# 181. Prohibition Lifecycle

Possible:

```text
ACTIVE

NOT_APPLICABLE

COMPLIED_WITH

VIOLATED

EXEMPTED

SUPERSEDED

EXPIRED.
```

---

# 182. Permission Lifecycle

Possible:

```text
AVAILABLE

CONDITIONALLY_AVAILABLE

EXERCISED

EXPIRED

SUSPENDED

REVOKED.
```

Not every permission needs persistence.

---

# 183. Right Lifecycle

Possible:

```text
AVAILABLE

EXERCISABLE

EXERCISED

SATISFIED

DENIED

EXPIRED

WAIVED.
```

Exact semantics will vary.

---

# 184. Power Lifecycle

Possible:

```text
AVAILABLE

EXERCISED

LAPSED

REVOKED

SUSPENDED.
```

---

# 185. Violation Does Not Rewrite Norm

The original obligation remains historically valid even after it is violated.

Correct:

```text
Obligation = VIOLATED
```

not:

```text
delete obligation.
```

---

# 186. Remediation Does Not Erase Violation

If the trader later cures the breach:

```text
violation occurred
+
remedial obligation satisfied.
```

Historical violation remains.

---

# 187. Cured Violation

Potential state:

```text
VIOLATED_AND_REMEDIATED
```

or a separate reparation state MAY be used.

Do not rewrite history to:

```text
SATISFIED.
```

---

# 188. Appeal / Challenge

A violation or regulatory determination MAY be:

```text
UNDER_CHALLENGE.
```

The platform SHALL preserve:

```text
original determination

challenge

review outcome.
```

---

# 189. Reversed Determination

If review determines:

```text
no violation occurred
```

Baobab SHALL create a reversal/correction history.

It SHALL not simply delete the old decision.

---

# 190. Penalty Appeal

A penalty may be:

```text
imposed

appealed

stayed

varied

reversed.
```

These states SHALL not alter the underlying normative rule automatically.

---

# 191. Operational Enforcement

Resolved normative semantics flow into ADR-REG-0004.

Example:

```text
verified Prohibition
       │
       ▼
Assessment PROHIBITED
       │
       ▼
E4 eligible
       │
       ▼
Trade DENY_TRANSITION.
```

---

# 192. Discretionary Enforcement

Example:

```text
possible prohibition
dependent on authority discretion
       │
       ▼
Assessment INDETERMINATE
       │
       ▼
E2 REVIEW_GATE.
```

---

# 193. Weak Permission Enforcement

A weak permission SHALL ordinarily NOT justify:

```text
high-assurance affirmative regulatory clearance
```

unless coverage/closed-world guarantees support it.

---

# 194. Strong Permission Enforcement

A verified explicit permission MAY support stronger outcomes when:

```text
conditions satisfied

no overriding rule exists

context complete.
```

---

# 195. Right Enforcement

A recognised right MAY generate obligations for platform workflows.

Example:

```text
regulated party has right to receive reasons.
```

A workflow may require:

```text
decision explanation.
```

But the right itself remains Regulations-owned.

---

# 196. Legal Power Enforcement

A platform SHALL not itself exercise an authority's statutory power unless it is legally authorised to do so through a valid external integration/mandate.

---

# 197. Authority Integration

A future government API may return:

```text
Permit Approved.
```

Baobab records:

```text
AuthorityDetermination.
```

It does not pretend:

```text
Baobab granted permit.
```

---

# 198. Normative Reasoning Trace

Every consequential evaluation SHOULD preserve a deliberate structured trace:

```text
Rule A applicable

Exception E false

Rule B applicable

Rule B overrides Rule A under relation R

Strong Permission P applies

Result:
PERMITTED_WITH_REQUIREMENTS
```

---

# 199. No Hidden Model Chain-of-Thought

The trace SHALL contain:

```text
facts

conditions

rule identities

relationships

citations

outcomes.
```

It SHALL NOT depend on storing private LLM reasoning text.

---

# 200. NormativeTrace

Conceptually:

```text
NormativeTrace
├── fact_bindings[]
├── candidate_rules[]
├── applicable_rules[]
├── exceptions[]
├── exemption_refs[]
├── conflicts[]
├── override_relations[]
├── discretion_points[]
├── resolved_effects[]
├── unresolved_issues[]
└── provenance
```

---

# 201. Explainability

From a normative trace, Baobab SHOULD be able to generate:

> Import is normally prohibited under Rule A. Rule B expressly permits qualifying research institutions to import the product. The legal entity has verified Status S, Rule B applies, and no controlling contrary rule was found within the verified regulatory profile.

This is substantially more useful than:

```text
ALLOW.
```

---

# 202. Normative Decision Reasons

Machine-readable reasons SHOULD include concepts such as:

```text
OBLIGATION_APPLIES

PROHIBITION_APPLIES

STRONG_PERMISSION_APPLIES

RULE_EXCEPTED

EXEMPTION_APPLIES

RULE_OVERRIDDEN

NORMATIVE_CONFLICT

DISCRETION_REQUIRED

VIOLATION_CONFIRMED

REPARATION_REQUIRED.
```

---

# 203. Testing Obligation Rules

Tests SHOULD include:

```text
fulfilled

unfulfilled

late fulfilment

exemption

unknown fact

wrong bearer

wrong period.
```

---

# 204. Testing Prohibition Rules

Tests SHOULD include:

```text
forbidden action absent

forbidden action present

strong permission exception

wrong jurisdiction

rule expired.
```

---

# 205. Testing Permissions

Tests MUST distinguish:

```text
explicit permission

absence of prohibition

incomplete coverage

conflicting prohibition.
```

---

# 206. Testing Defeasibility

Tests MUST include:

```text
general rule only

general + exception

general + stronger contrary rule

two conflicting rules without superiority

temporary override

expired override.
```

---

# 207. Testing Discretion

Tests MUST prove:

```text
objective preconditions can evaluate

discretion remains unresolved

system does not fabricate authority decision.
```

---

# 208. Testing Violation

Tests MUST distinguish:

```text
actual breach

missing evidence

late evidence

system outage

repaired breach

appealed determination.
```

---

# 209. Testing Reparation

Tests SHOULD include:

```text
primary norm satisfied
→ no reparation

primary norm violated
→ reparation activated

reparation satisfied

reparation violated
→ next consequence.
```

---

# 210. Normative Golden Cases

The initial repository SHOULD maintain golden examples covering:

```text
simple obligation

maintenance obligation

prohibition

explicit permission

weak permission

right + correlative obligation

legal power

exception

exemption

waiver

derogation

defeasible override

unresolved conflict

discretionary rule

violation

reparative obligation.
```

---

# 211. Initial ZuriBeans Golden Case — Obligation

```text
Applicable export rule
      ↓
Exporter obligation
      ↓
Required certificate
      ↓
Certificate valid
      ↓
SATISFIED.
```

---

# 212. Initial Golden Case — Exception

```text
General permit rule
      ↓
transaction matches general condition
      ↓
verified exception applies
      ↓
general permit obligation defeated.
```

---

# 213. Initial Golden Case — Strong Permission

```text
General restriction
      ↓
special verified permission rule
      ↓
qualifying status present
      ↓
specific activity permitted.
```

---

# 214. Initial Golden Case — Weak Permission

```text
No prohibition found
      +
coverage incomplete
      ↓
NOT affirmative permission
      ↓
INDETERMINATE / advisory.
```

---

# 215. Initial Golden Case — Discretion

```text
Rule:
Authority may approve
if criteria A/B/C satisfied.

Facts:
A/B/C satisfied.

Result:
eligible for authority determination

NOT:
approved.
```

---

# 216. Initial Golden Case — Violation

```text
Maintenance obligation:
licence must remain valid.

Licence expires.

Regulated activity continues.

Result:
violation candidate/verified finding
according to evidence.
```

---

# 217. Initial Golden Case — Reparation

```text
Report due:
30 September

Not filed.

Violation confirmed.

Rule:
late filing requires
report + prescribed consequence.

Reparative obligation created.
```

---

# 218. Initial Golden Case — Conflict

```text
Rule A:
Activity X prohibited.

Rule B:
Activity X expressly permitted
for qualifying entities.

Entity qualifies.

Verified relation:
B overrides A within scope.

Result:
STRONG_PERMISSION.
```

---

# 219. Initial Golden Case — Unresolved Conflict

```text
Rule A:
X prohibited.

Rule B:
X permitted.

Both applicable.

No verified priority.

Result:
NORMATIVE_CONFLICT

Decision:
REVIEW_REQUIRED.
```

---

# 220. Formal Semantics Boundary

This ADR establishes semantic requirements.

It does NOT select a mathematical formalism.

---

# 221. Future Rule IR

`ADR-REG-0016` SHALL define how these concepts are represented in Baobab's provider-neutral rule IR.

That IR MUST support:

```text
explicit modalities

negative facts

unknown facts

exceptions

defeaters

overrides

rule strength

rights

powers

discretion markers

violation triggers

reparative chains.
```

---

# 222. Future Applicability ADR

`ADR-REG-0017` SHALL define how real context is bound into these rules.

---

# 223. Future Evaluation ADR

`ADR-REG-0018` SHALL define the execution algorithm and evaluation ordering.

---

# 224. Future PDP/PEP ADR

`ADR-REG-0019` SHALL define how resolved normative decisions travel to enforcement points.

---

# 225. Future Replay ADR

`ADR-REG-0020` SHALL define explainability, historical replay and reproducibility.

---

# 226. Future AI Governance ADR

`ADR-REG-0021` SHALL apply particularly strict controls to AI interpretation of:

```text
exceptions

discretion

rights

conflicts

reparative consequences.
```

---

# 227. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-N-I01` | Obligation, Prohibition and Permission SHALL remain distinct |
| `REG-N-I02` | Explicit/strong permission SHALL remain distinct from weak permission |
| `REG-N-I03` | Absence of known prohibition SHALL NOT automatically mean affirmative permission |
| `REG-N-I04` | Baobab SHALL generally preserve open-world semantics for material regulatory facts |
| `REG-N-I05` | Unknown SHALL remain distinct from false |
| `REG-N-I06` | Explicit negation SHALL remain distinct from absence of evidence |
| `REG-N-I07` | Right SHALL remain distinguishable from simple permission |
| `REG-N-I08` | Legal power SHALL remain distinguishable from permission |
| `REG-N-I09` | Legal power SHALL remain distinguishable from Baobab administrative authority |
| `REG-N-I10` | Exception SHALL remain distinct from general-condition failure |
| `REG-N-I11` | Exemption SHALL remain distinguishable from exception |
| `REG-N-I12` | Waiver SHALL require legally competent authority where regulatory law is concerned |
| `REG-N-I13` | Derogation SHALL not automatically imply repeal |
| `REG-N-I14` | Defeasible rules SHALL support explicit defeat/override semantics |
| `REG-N-I15` | Unresolved defeasible conflicts SHALL remain unresolved |
| `REG-N-I16` | Rule precedence SHALL derive from verified legal relations, not technical priority alone |
| `REG-N-I17` | Discretion SHALL remain visible and SHALL NOT silently become deterministic logic |
| `REG-N-I18` | The word “may” SHALL NOT automatically compile into simple permission |
| `REG-N-I19` | AI SHALL NOT exercise legal discretion merely because a rule is discretionary |
| `REG-N-I20` | Violation SHALL remain distinct from missing evidence |
| `REG-N-I21` | Violation SHALL remain distinct from infrastructure failure |
| `REG-N-I22` | Penalty SHALL remain distinct from violation |
| `REG-N-I23` | Potential penalty SHALL remain distinct from authority-imposed penalty |
| `REG-N-I24` | Reparative obligations SHALL retain the violated norm as provenance |
| `REG-N-I25` | Remediation SHALL not erase historical violation |
| `REG-N-I26` | Conflicting applicable norms SHALL not trigger arbitrary conclusions |
| `REG-N-I27` | Alternative interpretations SHALL remain representable |
| `REG-N-I28` | Factual, normative, hierarchy and coverage uncertainty SHALL remain distinguishable |
| `REG-N-I29` | Consumer systems SHALL receive resolved normative outcomes rather than opaque rule-engine internals |
| `REG-N-I30` | Every consequential normative conclusion SHALL be explainable to rule and source level |

---

# 228. Rejected Alternative — Pure Boolean Logic

Rejected:

```text
allowed = true / false
```

as the entire normative model.

---

# 229. Rejected Alternative — No Rule Means Allowed

Rejected.

It converts incomplete regulatory knowledge into false assurance.

---

# 230. Rejected Alternative — Permission and Right Are Identical

Rejected.

Rights may create correlative duties for others.

---

# 231. Rejected Alternative — Permission and Power Are Identical

Rejected.

A legal power can alter legal relationships.

---

# 232. Rejected Alternative — "May" Means Permission

Rejected.

"May" is interpretively context-sensitive.

---

# 233. Rejected Alternative — Exception Means Condition False

Rejected.

Exceptions defeat otherwise satisfied rules.

---

# 234. Rejected Alternative — Exemption Means Rule Deleted

Rejected.

The general rule continues to exist.

---

# 235. Rejected Alternative — Tenant Admin Can Waive Law

Rejected.

Platform permissions do not create sovereign legal authority.

---

# 236. Rejected Alternative — Conflict Means Prohibition Wins

Rejected.

Controlling relation must be legally established.

---

# 237. Rejected Alternative — Latest Rule Wins

Rejected consistently with ADR-REG-0007.

---

# 238. Rejected Alternative — Most Specific Always Wins

Rejected unless supported by the jurisdiction's interpretive framework.

---

# 239. Rejected Alternative — AI Resolves Discretion

Rejected.

The system may assist authorised judgment, not usurp it.

---

# 240. Rejected Alternative — Missing Document Means Violation

Rejected.

The legal obligation may have been satisfied through evidence not yet available to Baobab.

---

# 241. Rejected Alternative — Violation Means Maximum Penalty

Rejected.

Penalty determination may itself involve separate rules or discretion.

---

# 242. Rejected Alternative — Remediation Deletes Violation

Rejected.

Auditability requires historical truth.

---

# 243. Rejected Alternative — Every Rule Must Be Fully Automated

Rejected.

Some law remains appropriately:

```text
interpretive

evaluative

discretionary

human-governed.
```

---

# 244. Rejected Alternative — One Rules Engine for Everything

Rejected as an architectural assumption.

Baobab owns semantics, not vendor/runtime ideology.

---

# 245. Commercial Consequence

This normative model materially changes what Baobab can sell.

A basic regulatory product can answer:

```text
"What rules mention my product?"
```

Baobab's intended capability can answer:

```text
"This general prohibition applies,
but your legal entity has an applicable
statutory exemption.

That exemption is valid until date X.

You remain subject to reporting obligations Y and Z.

The permission does not extend to Product B.

Here are the governing provisions,
interpretation and evidence."
```

That is a substantially higher-value enterprise capability.

---

# 246. Commercial Consequence — Regulatory Decision API

A future API can expose:

```text
OBLIGATORY

PROHIBITED

EXPLICITLY_PERMITTED

CONDITIONALLY_PERMITTED

DISCRETIONARY

INDETERMINATE
```

plus:

```text
requirements

exceptions

source basis

evidence

review path.
```

---

# 247. Commercial Consequence — Exception Intelligence

Businesses frequently lose money not only because they miss rules but because they fail to identify:

```text
exemptions

derogations

preferential treatments

rights

alternative compliance pathways.
```

Baobab's model can surface these explicitly.

---

# 248. Commercial Consequence — Avoid Over-Compliance

A simplistic compliance engine often produces:

```text
when uncertain → require everything.
```

That increases:

```text
cost

delay

paperwork

border friction.
```

Correct normative reasoning can identify when requirements genuinely do **not** apply.

---

# 249. Commercial Consequence — Avoid Under-Compliance

Conversely:

```text
not seeing a prohibition
```

does not become false clearance.

This reduces under-compliance risk.

---

# 250. Commercial Consequence — Human Review Efficiency

By isolating:

```text
objective deterministic questions
```

from:

```text
true discretion / ambiguity
```

Baobab can automate the easy 80–90% of repetitive cases while routing the difficult minority to qualified review.

The exact percentage is empirical and SHALL not be assumed in product claims.

---

# 251. Differentiation from LLM Regulatory Search

An LLM may produce:

```text
"It appears the rule allows..."
```

Baobab's target architecture instead produces:

```text
Rule A creates prohibition.

Rule B creates strong permission
for qualifying category C.

Entity qualifies under Rule D.

Rule B defeats Rule A
within this scope.

Requirements E and F remain.

Decision:
CONDITIONALLY_PERMITTED.
```

That structured reasoning is a fundamentally different product.

---

# 252. Strategic Relationship with Pulse

Pulse may answer:

```text
"What commercial opportunity does this exemption create?"
```

Regulations answers:

```text
"Does the exemption legally apply?"
```

That combination becomes strategically powerful.

---

# 253. Pulse Must Not Infer Permission from Opportunity

A Pulse recommendation that a market looks attractive SHALL not become regulatory permission.

---

# 254. Regulations Must Not Infer Commercial Wisdom from Permission

A transaction being legally permitted does not mean:

```text
commercially advisable.
```

---

# 255. Minimum Implementation Proof

Before `ADR-REG-0009` is considered implemented, Baobab SHOULD demonstrate:

```text
1. Simple Obligation.

2. Maintenance Obligation.

3. Prohibition.

4. Strong explicit Permission.

5. Weak permission / absence-of-prohibition case.

6. Right with correlative obligation.

7. Legal Power distinct from Permission.

8. Rule Exception.

9. Standing Exemption.

10. Transaction-specific Exemption.

11. Waiver requiring competent authority.

12. Derogation without repeal.

13. Defeasible general rule.

14. Defeater.

15. Explicit Override relation.

16. Conflict with verified superior rule.

17. Conflict without superior rule → unresolved.

18. Explicit negative fact distinct from unknown.

19. Closed-world rule profile for one verified exhaustive dataset.

20. Open-world result for incomplete coverage.

21. Discretionary rule.

22. Objective preconditions to discretion.

23. Authority determination resolving discretion.

24. Potential violation.

25. Verified violation.

26. Missing evidence that does not become violation.

27. Reparative obligation.

28. Potential penalty distinct from imposed penalty.

29. Remediated violation preserving history.

30. Alternative interpretations producing different candidate rule outcomes.

31. Tenant-selected counsel interpretation.

32. Normative trace exposing conditions, exceptions and override.

33. Second evaluator reproducing deterministic semantics.

34. No AI-only result acquiring E3/E4 authority.

35. Historical replay reproducing old normative outcome.
```

---

# 256. Production Gate

No normative rule SHALL become E3/E4 eligible until, where applicable:

```text
modality verified

bearer role verified

conditions verified

exceptions verified

exemptions modelled

negative/unknown semantics tested

conflict relationships tested

hierarchy links verified

defeasibility tested

discretion markers reviewed

violation semantics tested

reparative semantics tested

golden positive and negative cases pass

source lineage complete

human-readable explanation verified.
```

---

# 257. Initial Cross-Border Scope

The first implementation SHOULD prioritise normative structures common to cross-border trade:

```text
import/export obligations

licence requirements

permit requirements

documentation

rules-of-origin entitlement

preferential treatment

restricted-goods prohibitions

product-specific exemptions

reporting

record retention

customs/tax obligations.
```

---

# 258. AfCFTA-Type Example

Conceptually:

```text
General tariff treatment
       │
       ▼
Originating status rule
       │
       ▼
Strong entitlement / permission
to claim preferential treatment
       │
       ▼
subject to proof requirement.
```

The model must represent:

```text
right/permission

conditions

proof requirement

possible exception
```

rather than merely:

```text
tariff = 0.
```

---

# 259. Licence Exception Example

```text
General prohibition:
Activity X prohibited without Licence L.

Licence fact:
valid.

Specific permission:
licensed holder may perform X.

Result:
Strong permission / conditional permission.

Continuing obligation:
Licence must remain valid.
```

---

# 260. Discretion Example

```text
Authority MAY waive Requirement R
where exceptional circumstances exist.

Baobab:
detects exceptional circumstance candidate.

Result:
WAIVER_ELIGIBLE_FOR_REVIEW.

Not:
WAIVER_GRANTED.
```

---

# 261. Violation Example

```text
Obligation:
Maintain valid export licence.

Licence expired:
1 September.

Export:
4 September.

No exemption.

Result:
possible/verified violation,
depending on evidence assurance.
```

---

# 262. Reparative Example

```text
Violation:
late declaration.

Applicable secondary rule:
submit declaration immediately
+
pay prescribed late charge.

Result:
new reparative obligations.
```

---

# 263. Future ADR Dependencies

This ADR is foundational for:

```text
ADR-REG-0010
Regulatory Knowledge Graph
and Relationship Model

ADR-REG-0016
Machine-Executable Regulatory Rule
Representation and Intermediate Language

ADR-REG-0017
Regulatory Context and Applicability Resolution

ADR-REG-0018
Regulatory Decision and Evaluation Engine

ADR-REG-0019
Policy Decision Point and
Policy Enforcement Point Boundary

ADR-REG-0020
Decision Explainability,
Replay and Reproducibility

ADR-REG-0021
AI-Assisted Regulatory Interpretation
and Model Governance

ADR-REG-0022
Human Verification,
Assurance and Governance Workflow.
```

---

# 264. Research Foundation Summary

LegalRuleML provides the strongest direct semantic validation for this ADR. Its model includes obligations, permissions, prohibitions, rights, bearers, violations, reparations, strict and defeasible rules, defeaters and override relationships. It explicitly distinguishes weak permission from strong permission and recognises that legal rule conflicts may require sceptical defeasible reasoning rather than classical Boolean inference.

Its treatment of normative violations is particularly important: a violated obligation does not make the logical system inconsistent; instead, the violation can activate separate reparative normative effects. This directly supports Baobab's separation of primary obligations, violations and reparative rules.

The OECD's 2026 Law-as-Code consultation independently reinforces that machine-executable legal infrastructure must retain conditions, exceptions, hierarchy, responsibilities, time limits, discretion and legal consequences, while keeping interpretive and discretionary aspects visible rather than silently mechanising them.

These external sources do not dictate Baobab's implementation technology. They validate the semantic requirements.

---

# 265. Final Decision

Baobab Regulations SHALL adopt a **defeasible, open-world and provenance-aware normative model**.

The canonical architecture is:

```text
                      VERIFIED LEGAL RULES
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
            OBLIGATION   PROHIBITION   PERMISSION
                 │            │            │
                 │            │      ┌─────┴──────┐
                 │            │      ▼            ▼
                 │            │    STRONG        WEAK
                 │            │
                 └────────────┼────────────┐
                              │            │
                              ▼            ▼
                          EXCEPTIONS      RIGHTS
                          EXEMPTIONS        │
                          WAIVERS           ▼
                          DEROGATIONS   CORRELATIVE
                              │         OBLIGATIONS
                              ▼
                         DEFEASIBILITY
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
                   RULE A            RULE B
                     │                 │
                     └────────┬────────┘
                              ▼
                           CONFLICT
                              │
                    hierarchy / override
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
            RESOLVED                     UNRESOLVED
               │                             │
               ▼                             ▼
       NORMATIVE EFFECT                 HUMAN REVIEW
               │
         ┌─────┴─────────┐
         ▼               ▼
     SATISFIED        VIOLATED
                         │
                         ▼
                   REPARATIVE RULE
                         │
                         ▼
              PENALTY / REMEDIAL DUTY
```

Alongside that model:

```text
LEGAL POWER
       │
       ▼
AUTHORISED ACTOR
       │
       ▼
EXERCISE OF POWER
       │
       ▼
LEGAL STATE CHANGE
```

and:

```text
DISCRETION
       │
       ▼
OBJECTIVE PRECONDITIONS
       │
       ▼
LEGAL JUDGMENT REQUIRED
       │
       ▼
AUTHORITY / AUTHORISED REVIEW
```

shall remain distinct.

The engine SHALL understand that law can say:

```text
must

must not

may

may not

is entitled to

is exempt from

unless

except where

subject to

provided that

if satisfied

may determine

shall consider

notwithstanding

despite

without prejudice to.
```

and that these expressions do **not** all reduce to the same software construct.

The most important principle of `ADR-REG-0009` is:

> **Baobab SHALL automate legal certainty without manufacturing certainty where the legal system deliberately retains exceptions, ambiguity, defeasibility or discretion.**

A second principle is:

> **The absence of a known prohibition is not the same thing as an authoritative permission.**

A third is:

> **Violation is a regulatory fact; punishment is a separate regulatory consequence.**

And a fourth is:

> **A machine may establish that an authority is legally capable of choosing. It does not thereby become entitled to make that choice.**

That gives Baobab Regulations a normative foundation capable of supporting serious regulatory execution rather than simplistic compliance checklists.

---

## Decision Summary

```text
ADR-REG-0009
──────────────────────────────────────────────

CORE NORMATIVE EFFECTS

Obligation
Prohibition
Permission


PERMISSION

Strong / Explicit
    ≠
Weak / No contrary rule found


ADDITIONAL POSITIONS

Right
Legal Power
Exemption
Waiver
Derogation


CRITICAL LOGIC

Unknown ≠ False

No rule found ≠ Permitted

Exception ≠ Condition false

Exemption ≠ Rule deletion

Waiver ≠ Internal admin override

Violation ≠ Missing evidence

Penalty ≠ Violation

Remediation ≠ Erasing history


DEFEASIBILITY

General rule
    ↓
Exception / Override / Stronger Rule
    ↓
Defeated or modified conclusion


CONFLICT

If verified priority exists:
resolve.

If no verified priority exists:
UNRESOLVED → REVIEW_REQUIRED.


DISCRETION

Machine may evaluate objective preconditions.

Machine does NOT silently exercise
authority's legal discretion.


VIOLATION

Obligation violated
or
Prohibition violated

may activate:

Reparative Rule
    ↓
Corrective Obligation
    ↓
Penalty / remediation


REASONING PHILOSOPHY

Open-world by default.

Explicit negatives.

Visible uncertainty.

No arbitrary conflict resolution.

No AI-created legal certainty.


STRATEGIC RESULT

Baobab can reason about
what law must,
must not,
may,
exempts,
overrides,
leaves to discretion,
and requires after breach—

without reducing law to
a brittle Boolean rules engine.
```
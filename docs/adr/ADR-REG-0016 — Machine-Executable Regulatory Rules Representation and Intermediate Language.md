# ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language

**Status:** Proposed — Foundational Execution Architecture  
**Decision ID:** `ADR-REG-0016`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Regulatory Rule Representation / Intermediate Language / Compilation / Deterministic Policy Execution  
**Strategic Classification:** Core Regulatory Execution Infrastructure

---

# 1. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics, Defeasibility, Discretion, Rights, Violations and Reparative Rules`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`

It also follows Baobab-wide principles that:

```text
canonical semantics
≠
provider implementation

capability
≠
provider

business meaning
≠
runtime technology.
```

---

# 2. Executive Decision

Baobab Regulations SHALL define and own a versioned, provider-neutral:

# **Baobab Regulatory Rule Intermediate Representation — BRIR**

The BRIR SHALL represent verified machine-executable regulatory semantics independently of:

```text
Rego

OPA

CEL

DMN

Python

Java

Go

SQL

LLM prompts

Haystack

LangGraph.
```

The initial preferred deterministic execution path SHALL be:

```text
AUTHORITATIVE SOURCE
        │
        ▼
PROVISION VERSION
        │
        ▼
VERIFIED INTERPRETATION
        │
        ▼
REGULATORY RULE VERSION
        │
        ▼
      BRIR
        │
        ▼
STATIC + SEMANTIC VALIDATION
        │
        ▼
TARGET COMPILER
        │
        ▼
    Rego v1
        │
        ▼
SIGNED OPA BUNDLE
        │
        ▼
       OPA
        │
        ▼
TYPED RULE EVALUATION
        │
        ▼
REGULATORY ASSESSMENT
        │
        ▼
REGULATORY DECISION
```

OPA SHALL be the initial deterministic policy-execution provider.

OPA SHALL NOT be the canonical regulatory model.

---

# 3. Fundamental Doctrine

> **Law is not Rego.**

> **A verified interpretation is not Rego.**

> **A Baobab regulatory rule is not Rego.**

> **Rego is one executable rendering of a Baobab regulatory rule.**

---

# 4. Why an Intermediate Representation Is Required

If canonical rules were authored directly in Rego:

```text
Legal Source
    ↓
Rego
```

Baobab would couple:

```text
legal semantics
+
regulatory governance
+
decision logic
+
execution technology.
```

That would undermine `ADR-REG-0005`.

Instead:

```text
Legal Source
    ↓
Interpretation
    ↓
Baobab Rule Semantics
    ↓
BRIR
    ├──► Rego / OPA
    ├──► CEL
    ├──► DMN
    ├──► native evaluator
    └──► future engine.
```

---

# 5. OPA Is a Suitable Initial Target

OPA is a general-purpose policy decision engine that separates policy decision-making from enforcement and evaluates declarative Rego policies over structured data. It supports REST, Go embedding, WebAssembly and other compiled evaluation paths.

Those properties fit Baobab's:

```text
PDP / PEP separation

structured context

provider-neutral execution

bundle deployment

decision audit.
```

---

# 6. But OPA Is Domain-Agnostic

OPA intentionally knows nothing intrinsically about:

```text
legal hierarchy

regulatory authority

obligations

permissions

prohibitions

legal evidence

jurisdiction

defeasibility

grandfathering.
```

Those semantics belong to Baobab Regulations.

---

# 7. OPA's Own IR SHALL NOT Become BRIR

OPA itself has a low-level Intermediate Representation representing planned Rego evaluation paths. OPA describes that IR as a compiler/interpreter representation and publishes a versioned JSON Schema for it.

That is:

```text
OPA implementation IR
```

not:

```text
Baobab Regulatory Rule IR.
```

---

# 8. Two Different IRs

The architecture SHALL distinguish:

```text
BRIR
    regulatory semantic representation

OPA IR
    OPA execution-plan representation.
```

The latter MAY appear downstream during compilation.

It SHALL never become canonical.

---

# 9. BRIR Objective

BRIR SHALL provide enough semantics to represent:

```text
constitutive rules

prescriptive rules

applicability

conditions

exceptions

exemptions

obligations

permissions

prohibitions

requirements

deadlines

calculations

violations

reparations

explicit overrides

temporal scope

jurisdictional scope

evidence requirements

unknown facts

decision explanations.
```

---

# 10. BRIR SHALL NOT Attempt to Formalise All Law

The objective is not:

```text
encode every possible legal argument
into deterministic software.
```

The objective is:

```text
represent machine-executable regulatory semantics
where sufficiently verified and formalizable,
while explicitly identifying what remains
judgmental, discretionary or unresolved.
```

---

# 11. Standards Alignment — LegalRuleML

LegalRuleML formally addresses features peculiar to legal norms, including:

```text
obligations

permissions

prohibitions

rights

defeasibility

rule overrides

temporal characteristics

violations

reparations.
```


BRIR SHALL preserve semantic interoperability with these concepts.

---

# 12. BRIR Is Not LegalRuleML

LegalRuleML is a rich legal-rule interchange standard.

Baobab SHALL NOT require its internal execution runtime to use LegalRuleML XML directly.

Instead:

```text
BRIR
    internal canonical execution representation

LegalRuleML
    interoperability / import / export representation.
```

---

# 13. DMN Interoperability

DMN is designed for precise specification of business decisions and business rules and provides executable decision tables and FEEL expressions.

DMN MAY become a useful future:

```text
decision-table import/export target

human-readable regulatory decision model.
```

It SHALL not replace BRIR.

---

# 14. CEL Interoperability

CEL is designed as a portable, safe, non-Turing-complete expression language optimized for compile-once/evaluate-many scenarios.

CEL MAY later become an alternative target for:

```text
small predicates

edge evaluation

embedded runtime policies.
```

Again:

```text
CEL ≠ BRIR.
```

---

# 15. Canonical Representation Layers

Baobab SHALL distinguish:

```text
RegulatoryRule
        │
        ▼
RegulatoryRuleVersion
        │
        ▼
BRIRDocument
        │
        ▼
CompiledPolicyArtifact
        │
        ▼
RuntimePolicyInstance.
```

---

# 16. RegulatoryRule

Stable conceptual identity:

```text
reg_rule_123
```

---

# 17. RegulatoryRuleVersion

Immutable verified semantic version:

```text
reg_rule_123:v4
```

---

# 18. BRIRDocument

Machine-executable representation of that RuleVersion.

A materially changed rule meaning creates:

```text
new RuleVersion
+
new BRIR.
```

---

# 19. CompiledPolicyArtifact

A target-specific derivative:

```text
Rego module

OPA bundle

Wasm module

CEL expression

DMN file.
```

---

# 20. RuntimePolicyInstance

Represents the deployed executable state:

```text
OPA bundle revision

runtime instance

loaded_at

health state.
```

Deployment does not change legal meaning.

---

# 21. Serialization

The canonical portable BRIR representation SHOULD initially use:

```text
JSON
```

validated by:

```text
JSON Schema Draft 2020-12.
```

JSON Schema 2020-12 defines a standard JSON-based mechanism for expressing structure and validation constraints.

---

# 22. Serialization Is Not Domain Ownership

BRIR being serialised as JSON SHALL NOT mean:

```text
untyped JSON blob
```

is the domain model.

Implementations SHOULD expose typed domain objects.

---

# 23. BRIR Schema Identity

Example:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "brirVersion": "baobab.regulations.brir/v1"
}
```

---

# 24. BRIR Versioning

Separate:

```text
RuleVersion
```

from:

```text
BRIR schema version.
```

Example:

```text
RuleVersion = 7

BRIR specification = v2.
```

The same legal rule semantics may be migrated to a newer IR specification.

---

# 25. BRIR Schema Migration

BRIR migration SHALL preserve:

```text
semantic equivalence

provenance

source RuleVersion

migration tool/version.
```

---

# 26. Semantic Migration

If migration changes regulatory meaning:

```text
it is not merely an IR migration.
```

It requires a new:

```text
RuleVersion.
```

---

# 27. Conceptual BRIR Structure

```text
BRIRDocument
├── brir_version
├── rule_ref
├── rule_version_ref
├── semantic_kind
├── executability
├── scope
├── temporal
├── variables
├── fact_requirements
├── applicability
├── conditions
├── exceptions
├── effects
├── requirements
├── calculations
├── deadlines
├── defeasibility
├── dependencies
├── reparations
├── evidence_policy
├── enforcement_ceiling
├── explanation_metadata
└── provenance
```

---

# 28. Synthetic Example

Illustrative only:

```json
{
  "brirVersion": "baobab.regulations.brir/v1",
  "ruleRef": "reg_rule_example",
  "semanticKind": "PRESCRIPTIVE",
  "executability": "DETERMINISTIC",
  "when": {
    "all": [
      {
        "eq": [
          {"fact": "transaction.activity"},
          {"literal": "IMPORT"}
        ]
      },
      {
        "eq": [
          {"fact": "transaction.destinationJurisdiction"},
          {"literal": "ZA"}
        ]
      }
    ]
  },
  "unless": [
    {
      "fact": "regulatory.exemption.active"
    }
  ],
  "effect": {
    "type": "OBLIGATION",
    "bearerRole": "IMPORTER",
    "requirement": "VALID_IMPORT_PERMIT"
  }
}
```

This is an architecture example.

It is not a statement of South African law.

---

# 29. Rule Semantic Kind

BRIR SHALL support at least:

```text
CONSTITUTIVE

PRESCRIPTIVE.
```

---

# 30. Constitutive Rule

Defines or derives regulatory facts/concepts.

Example:

```text
IF product attributes satisfy X
THEN product is classified as Concept Y.
```

---

# 31. Prescriptive Rule

Produces normative effect:

```text
OBLIGATION

PROHIBITION

PERMISSION

RIGHT

POWER

or related normative result.
```

---

# 32. Constitutive Before Prescriptive

Rules MAY form dependencies:

```text
classification rule
      ↓
derived fact
      ↓
prescriptive rule.
```

---

# 33. Fact Model

BRIR SHALL consume typed:

```text
RegulatoryFact
```

rather than arbitrary undocumented JSON fields.

---

# 34. Fact Definition

A fact definition SHOULD include:

```text
fact_key

type

source authority

scope

cardinality

unit?

temporal semantics

nullable?

unknown semantics.
```

---

# 35. Fact Value Envelope

A consequential fact SHOULD conceptually support:

```text
KNOWN(value)

UNKNOWN(reason)

UNAVAILABLE(reason)

ERROR(error_code).
```

This avoids conflating:

```text
missing
null
false
zero
empty
unknown.
```

---

# 36. Fundamental Truth Domain

BRIR expression evaluation SHALL support:

```text
TRUE

FALSE

UNKNOWN

ERROR.
```

---

# 37. UNKNOWN Is Not FALSE

This is normative.

```text
UNKNOWN
≠
FALSE.
```

---

# 38. ERROR Is Not UNKNOWN

Example:

```text
unknown:
required classification has not been established.

error:
classification service returned malformed data.
```

Different remediation applies.

---

# 39. Null Is Not Unknown

A legitimate:

```text
null
```

value MAY mean:

```text
known absence
```

only where the fact schema explicitly defines it that way.

---

# 40. Missing Key Is Not Negative Fact

If:

```text
permit
```

is absent from runtime input:

```text
permit does not exist
```

SHALL NOT be inferred automatically.

---

# 41. Open-World Default

BRIR SHALL use an:

```text
OPEN-WORLD
```

fact model by default.

Absence of evidence does not imply evidence of absence.

---

# 42. Closed-World Exception

A closed-world interpretation MAY be allowed only where the relevant data source is explicitly verified as exhaustive for the proposition.

Example:

```text
verified complete registry
+
query finds no record.
```

Even then the rule must declare that semantic assumption.

---

# 43. ClosedWorldScope

Conceptually:

```text
ClosedWorldScope
├── fact_namespace
├── authoritative_source_ref
├── completeness_assertion_ref
├── valid_period
└── verification_state
```

---

# 44. Logical Negation

BRIR SHALL distinguish:

```text
NOT proposition
```

from:

```text
fact absent from input.
```

---

# 45. Negation-as-Failure

OPA/Rego uses undefined/negation semantics that can be very useful in ordinary policy evaluation.

BRIR compiler SHALL NOT translate legal negative assertions into Rego negation-as-failure unless the relevant completeness assumptions are verified.

---

# 46. Expression AST

BRIR conditions SHALL use a typed abstract syntax tree.

Core nodes SHOULD include:

```text
Literal

FactRef

VariableRef

All

Any

Not

Equals

NotEquals

LessThan

LessThanOrEqual

GreaterThan

GreaterThanOrEqual

In

NotIn

Contains

Exists

ForAll

RangeContains

SetIntersection

Arithmetic

FunctionCall.
```

---

# 47. No Arbitrary Code

BRIR SHALL NOT contain:

```text
eval("...")

Python expression

JavaScript expression

raw SQL

raw Rego
```

inside canonical conditions.

---

# 48. Why No Raw Target Code

Allowing:

```text
"rego": "..."
```

inside BRIR would bypass:

```text
provider neutrality

type checking

semantic validation

cross-target testing.
```

---

# 49. Literal Types

Initial literal types SHOULD support:

```text
BOOLEAN

INTEGER

DECIMAL

STRING

DATE

DATETIME

DURATION

CODE

IDENTIFIER

MONEY

QUANTITY

ENUM

LIST

SET

MAP / OBJECT.
```

---

# 50. Decimal Semantics

Money, tariffs, percentages and similar regulated calculations SHALL NOT rely on uncontrolled binary floating-point behaviour.

BRIR SHALL define exact decimal semantics.

---

# 51. Target Numeric Equivalence

A compiler SHALL prove that its target representation preserves required decimal/rounding semantics.

Where it cannot:

```text
calculation SHALL remain in
Baobab's deterministic calculation layer
rather than compiling unsafely.
```

---

# 52. Money

`Money` SHOULD include:

```text
amount

currency.
```

Operations across different currencies SHALL require an explicit conversion operation and rate provenance.

---

# 53. Quantity

`Quantity` SHOULD include:

```text
amount

unit.
```

Unit conversions SHALL be explicit.

---

# 54. Temporal Values

BRIR SHALL use the temporal semantics from ADR-REG-0015.

Types SHALL distinguish:

```text
DATE

DATETIME

DURATION

PERIOD / INTERVAL.
```

---

# 55. Temporal Comparison

Example:

```text
shipment_date >= rule.applicable_from
```

is deterministic.

But commencement determination itself may have been established upstream by interpretation.

---

# 56. Temporal Functions

Potential functions:

```text
date_add

business_days_add

within_period

overlaps

before

after

age_at.
```

They SHALL have versioned deterministic semantics.

---

# 57. Business-Day Calculations

Business-day functions SHALL reference:

```text
calendar_id

calendar_version

jurisdiction

timezone.
```

---

# 58. Function Registry

BRIR SHALL define a controlled:

```text
RegulatoryFunctionRegistry.
```

---

# 59. Function Requirements

Every executable function SHALL define:

```text
function_id

version

input types

output type

purity

determinism

error semantics

target support.
```

---

# 60. Pure Functions Preferred

Compiled deterministic rule execution SHOULD use:

```text
pure
side-effect-free
deterministic
```

functions.

---

# 61. No Network Calls from Regulatory Rules

Production regulatory rules SHALL NOT normally call:

```text
external HTTP APIs

databases

LLMs

search engines
```

from inside the deterministic evaluator.

---

# 62. Why

The decision input should already contain:

```text
resolved facts
verified evidence state
context
```

before evaluation.

This improves:

```text
reproducibility

latency

auditability

failure isolation.
```

---

# 63. OPA `http.send`

OPA supports network-related built-ins, but Baobab SHOULD prohibit network I/O from compiled regulatory policy under the high-assurance execution profile.

This is a Baobab architectural restriction, not an OPA limitation.

---

# 64. Conditions

A RuleVersion SHALL distinguish:

```text
applicability predicates

substantive conditions

exceptions.
```

---

# 65. Applicability

Applicability determines whether the rule belongs in the candidate rule set for the regulatory context.

---

# 66. Condition

Condition determines whether the normative rule's antecedent is satisfied.

---

# 67. Exception

Exception determines whether an otherwise applicable rule is defeated or excluded for the particular context.

---

# 68. Exception SHALL Be Explicit

Preferred:

```text
WHEN A AND B
UNLESS C.
```

Not:

```text
WHEN A AND B AND NOT C
```

where `C` is legally an exception.

Preserving semantic distinction improves explanations.

---

# 69. Exemption

A legal exemption MAY satisfy an exception condition.

But:

```text
Exception
≠
Exemption.
```

The exemption remains a legal status/fact with provenance.

---

# 70. Quantification

BRIR SHALL support:

```text
EXISTS

FOR_ALL

NONE

COUNT
```

where needed.

---

# 71. OPA Quantification

Rego supports existential evaluation by default and provides `every` for universal quantification.

The BRIR compiler MAY map compatible quantifiers to those constructs.

---

# 72. Quantifier Scope

Quantification SHALL operate only over explicitly typed collections.

---

# 73. Deontic Effects

BRIR SHALL retain the normative effect rather than compiling everything to:

```text
allow = true / false.
```

---

# 74. Core Effects

At minimum:

```text
OBLIGATION

PROHIBITION

PERMISSION.
```

---

# 75. Extended Effects

The model SHALL be extensible for:

```text
RIGHT

POWER

IMMUNITY

LIABILITY

DISABILITY

REPARATION.
```

as established by ADR-REG-0009.

---

# 76. Effect Template

Conceptually:

```text
NormativeEffectIR
├── effect_type
├── bearer_role
├── auxiliary_party_role?
├── action
├── object
├── timing?
├── requirement_refs[]
├── consequence_refs[]
└── provenance_ref
```

---

# 77. Bearer Role

Rules SHOULD refer first to:

```text
IMPORTER

EXPORTER

EMPLOYER

LICENSEE

SUPPLIER
```

or other regulated roles.

The runtime context resolves the actual legal entity.

---

# 78. No Tenant-Specific Legal Entity Hard-Coding

Canonical shared rules SHALL not contain:

```text
if company_id == ZURIBEANS
```

unless the rule genuinely concerns that entity specifically.

---

# 79. Permission Semantics

BRIR SHALL distinguish:

```text
EXPLICIT / STRONG PERMISSION
```

from:

```text
lack of identified prohibition.
```

LegalRuleML itself distinguishes weak and strong permission concepts.

---

# 80. Silence Is Not Permission

The evaluator SHALL NOT produce:

```text
PERMITTED
```

merely because no prohibition rule matched.

---

# 81. Prohibition Semantics

A prohibition effect SHALL identify:

```text
bearer

prohibited action/state

object

scope

time.
```

---

# 82. Obligation Semantics

An obligation SHALL identify:

```text
bearer

required action/state

trigger

deadline if any

requirements/evidence.
```

---

# 83. Obligation Lifecycle Is Downstream

BRIR defines how the obligation arises.

The contextual `RegulatoryEffect` / `Obligation` domain object manages lifecycle after instantiation.

---

# 84. Requirement Templates

Rules MAY produce:

```text
DOCUMENT

PERMIT

LICENCE

CERTIFICATE

FILING

PAYMENT

INSPECTION

DECLARATION

APPROVAL

NOTIFICATION

RECORD_RETENTION

CALCULATION
```

requirement templates.

---

# 85. Requirement IR

Conceptually:

```text
RequirementTemplateIR
├── type
├── subject
├── issuer_constraints?
├── evidence_types[]
├── timing
├── cardinality
├── satisfaction_logic
└── provenance
```

---

# 86. Composite Requirements

BRIR SHALL support:

```text
ALL_OF

ANY_OF

ONE_OF

AT_LEAST_N.
```

---

# 87. Evidence Satisfaction Is Not Boolean Shortcut

A rule MAY require:

```text
VALID_CERTIFICATE
```

but the evaluator should consume a verified fact such as:

```text
certificate_requirement_status =
SATISFIED
```

or structured evidence state.

OPA should not verify cryptographic certificates itself.

---

# 88. Calculation IR

BRIR SHALL support deterministic calculations where semantics can be represented safely.

---

# 89. Calculation Components

A calculation MAY include:

```text
inputs

formula

units

currency

rounding

minimum / maximum

threshold

effective version.
```

---

# 90. Calculation Provenance

Calculation outputs SHALL remain linked to:

```text
rule version

input facts

formula version.
```

---

# 91. Deadline IR

A deadline expression MAY include:

```text
anchor

offset

unit

calendar

adjustment convention

timezone.
```

---

# 92. Reparations

LegalRuleML explicitly models reparations linked to violations of prescriptive rules.

BRIR SHALL support:

```text
Violation
      ↓
ReparationRule
```

without interpreting the reparation as replacement of the original obligation unless the legal interpretation says so.

---

# 93. Contrary-to-Duty

Example:

```text
Primary:
file by date T

If violated:
file late declaration
+
possible penalty.
```

The reparative rule does not necessarily erase:

```text
the original violation.
```

---

# 94. Defeasibility

BRIR SHALL explicitly represent:

```text
STRICT

DEFEASIBLE

DEFEATER
```

semantics where verified.

LegalRuleML expressly models strict rules, defeasible rules, defeaters and superiority/override relationships.

---

# 95. No Arbitrary Priority Integer

Rejected:

```text
priority = 900
```

as canonical legal precedence.

---

# 96. Override Relation

Preferred:

```text
Rule B
OVERRIDES
Rule A

scope:
specific condition

basis:
Provision X.
```

---

# 97. Explicit Precedence Graph

BRIR rule sets MAY contain verified:

```text
OverrideRelationship
```

edges derived from ADR-REG-0007.

---

# 98. Compiler May Resolve Verified Overrides

Where precedence is:

```text
explicit

acyclic

fully verified
```

the compiler MAY translate it into deterministic target logic.

---

# 99. Unresolved Legal Conflict

Where competing rules lack resolved precedence:

```text
OPA SHALL NOT invent a winner.
```

Result:

```text
REVIEW_REQUIRED
```

or:

```text
INDETERMINATE.
```

---

# 100. Priority Cycle

A cycle such as:

```text
A overrides B
B overrides C
C overrides A
```

SHALL fail semantic validation.

---

# 101. Legal Hierarchy Is Not Rego Rule Order

Rego textual ordering SHALL NOT establish regulatory precedence.

---

# 102. Rule Dependencies

BRIR SHALL represent:

```text
DEPENDS_ON

DEFINES_TERM_FOR

TRIGGERS

EXCEPTED_BY

OVERRIDDEN_BY

REPAIRS_VIOLATION_OF

CALCULATES

QUALIFIES.
```

---

# 103. Dependency DAG

The deterministic compilation subset SHOULD form an acyclic dependency graph except where explicitly supported fixed-point semantics are introduced later.

---

# 104. Recursion

Arbitrary recursive regulatory rules SHALL NOT be supported in BRIR v1 unless their semantics and termination are explicitly defined.

---

# 105. Definitions

Constitutive definition rules SHOULD derive named regulatory concepts.

Example:

```text
IF A + B + C
THEN status = QUALIFYING_GOOD.
```

---

# 106. Definition Versioning

Definitions are themselves temporally versioned regulatory knowledge.

---

# 107. Discretion

A rule containing substantive external legal discretion SHALL NOT be transformed into deterministic permit/deny logic merely because its text includes:

```text
may.
```

---

# 108. Discretion Node

BRIR MAY represent:

```text
DiscretionRequired
├── holder
├── legal_basis
├── possible_outcomes
├── constraints
└── review_required
```

---

# 109. Discretion Is Usually Non-OPA

Unless an authority's discretion has already been exercised and supplied as an authoritative fact:

```text
EXTERNAL_AUTHORITY_DECISION_REQUIRED.
```

---

# 110. Open-Textured Standards

Terms such as:

```text
reasonable

adequate

material

substantial

appropriate
```

SHALL not receive arbitrary deterministic thresholds.

---

# 111. Judgment Node

BRIR SHOULD support marking:

```text
JUDGMENT_REQUIRED.
```

---

# 112. Executability Profile

Every RuleVersion SHALL carry an `ExecutabilityProfile`.

Initial values:

```text
DETERMINISTIC

DETERMINISTIC_WITH_EXTERNAL_FACTS

HUMAN_JUDGMENT_REQUIRED

AUTHORITY_DECISION_REQUIRED

REPRESENTATIONAL_ONLY.
```

---

# 113. DETERMINISTIC

All material semantics can be evaluated using:

```text
typed facts

pure deterministic functions

verified rule structure.
```

---

# 114. DETERMINISTIC_WITH_EXTERNAL_FACTS

Evaluation is deterministic after authoritative facts have been supplied.

Example:

```text
permit.status = ACTIVE.
```

---

# 115. HUMAN_JUDGMENT_REQUIRED

A human reviewer must establish one or more propositions.

---

# 116. AUTHORITY_DECISION_REQUIRED

A regulator/court/competent authority must exercise legal power/discretion.

---

# 117. REPRESENTATIONAL_ONLY

Rule can be represented for:

```text
search

explanation

impact analysis
```

but is not machine-executable.

---

# 118. Compilation Eligibility

Separately from legal executability, BRIR SHALL calculate target capability:

```text
OPA_COMPILABLE

CEL_COMPILABLE

DMN_COMPILABLE

NATIVE_ONLY

NOT_EXECUTABLE.
```

---

# 119. Legal Executability ≠ Target Compatibility

A rule can be deterministic but contain a calculation not yet supported by the OPA compiler.

That is:

```text
DETERMINISTIC
+
OPA_NOT_SUPPORTED.
```

---

# 120. BRIR Validation Layers

Publication SHALL require multiple validation passes:

```text
Schema Validation

Type Validation

Semantic Validation

Temporal Validation

Dependency Validation

Provenance Validation

Compilation Validation

Golden-Case Validation.
```

---

# 121. Schema Validation

Ensures BRIR conforms structurally to its JSON Schema.

---

# 122. Type Validation

Ensures:

```text
date compared with date

money compared with compatible money

integer expected where integer required.
```

---

# 123. Semantic Validation

Ensures things such as:

```text
prohibition has bearer/action

obligation has required state

exception references known facts

reparation references valid violation semantics.
```

---

# 124. Temporal Validation

Ensures rule's:

```text
force

applicability

transition
```

semantics align with ADR-REG-0015.

---

# 125. Provenance Validation

Production BRIR SHALL resolve to:

```text
RuleVersion
→ Interpretation
→ Provision(s)
→ Source(s).
```

---

# 126. Compilation Validation

Compiler output SHALL be parsed/checked by the target engine's tooling.

---

# 127. OPA Static Checking

OPA performs compilation-time validation including safety and type-related checks; `opa check`/strict validation can catch unsafe variables and related policy problems.

Baobab-generated Rego SHALL pass strict target validation.

---

# 128. Input Schema Validation

OPA supports JSON Schema-informed type checking for policy input/data.

Generated Rego SHOULD therefore carry or be checked against generated schemas for:

```text
RegulatoryEvaluationInput.
```

---

# 129. Runtime Input Contract

Conceptually:

```text
RegulatoryEvaluationInput
├── evaluation_id
├── legal_time
├── knowledge_time
├── context
├── facts
├── evidence_state
├── ruleset_ref
└── evaluation_profile
```

---

# 130. Facts Input Example

Preferred:

```json
{
  "product.classification": {
    "state": "KNOWN",
    "value": "0901"
  },
  "permit.status": {
    "state": "UNKNOWN",
    "reason": "NOT_VERIFIED"
  }
}
```

rather than:

```json
{
  "permit_status": null
}
```

with ambiguous meaning.

---

# 131. OPA Output SHALL NOT Be Bare Boolean

Rejected canonical target:

```json
{"allow": false}
```

---

# 132. Target Evaluation Result

Generated policy SHOULD return a structured object conceptually equivalent to:

```text
RuleEvaluationResult
├── rule_ref
├── truth_state
├── applicability
├── disposition
├── effects[]
├── requirements[]
├── unknown_facts[]
├── errors[]
├── reason_codes[]
├── trace_tokens[]
└── evaluator_metadata
```

---

# 133. Applicability Result

Potential:

```text
APPLIES

DOES_NOT_APPLY

DEFEATED

EXEMPTED

INDETERMINATE

ERROR.
```

---

# 134. Truth Result

Separately:

```text
TRUE

FALSE

UNKNOWN

ERROR.
```

---

# 135. Effect Production

Only:

```text
APPLIES
+
required condition truth
```

may instantiate the effect.

---

# 136. UNKNOWN SHALL Propagate

Required unknown input SHALL ordinarily produce:

```text
INDETERMINATE
```

rather than:

```text
DOES_NOT_APPLY.
```

---

# 137. Critical OPA Semantic Boundary

OPA documents that many runtime built-in errors ordinarily evaluate as undefined and often behave like false unless strict built-in errors are enabled.

That default is unsafe as the canonical interpretation of high-assurance regulatory evaluation.

---

# 138. Strict Runtime Profile

The high-assurance OPA integration SHALL use strict error handling where supported.

An arithmetic/type/date error must become:

```text
ERROR
```

not:

```text
FALSE.
```

---

# 139. Compiler-Supplied Guards

The BRIR compiler SHALL additionally emit explicit guards for:

```text
required facts

fact states

type expectations

unknown values.
```

This ensures regulatory semantics do not rely solely on OPA undefined behaviour.

---

# 140. Example

Wrong:

```rego
allow if input.permit.expiry >= input.shipment.date
```

if missing `permit` silently results in an undefined condition.

Preferred conceptual output:

```text
IF permit fact UNKNOWN
    → INDETERMINATE

ELSE
    evaluate permit expiry condition.
```

---

# 141. OPA Strict Built-in Limitation in Wasm

OPA documents that `strict-builtin-errors` is not available for its Wasm evaluation mode.

Therefore:

> **BRIR v1 SHALL NOT assume OPA Wasm and OPA server evaluation have identical failure semantics.**

---

# 142. Wasm Use

OPA's Wasm target is attractive for portable embedded evaluation and can compile Rego entrypoints into executable WebAssembly.

However, E3/E4 use SHALL require dedicated conformance testing before Wasm is approved as an equivalent execution profile.

---

# 143. Initial OPA Runtime Profile

The initial production high-assurance profile SHOULD favour:

```text
OPA runtime / service integration
with explicit strict-error semantics
```

rather than immediately distributing Wasm everywhere.

Exact deployment topology remains for ADR-REG-0019.

---

# 144. Rego Version

Generated policy SHALL target:

```text
Rego v1 semantics.
```

OPA 1.x makes `if`, `contains`, `in` and `every` part of the normal language semantics.

---

# 145. Generated Rego, Not Hand-Copied Legal Rules

Production canonical flow SHALL favour:

```text
BRIR
→ compiler
→ generated Rego.
```

Hand-authored Rego MAY be used for:

```text
compiler infrastructure

platform policy

test scaffolding.
```

It SHALL not silently become the source of regulatory meaning.

---

# 146. Generated Code Traceability

Every generated Rego rule SHOULD include target metadata mapping it to:

```text
rule_ref

rule_version

BRIR version

compiler version.
```

OPA supports metadata annotations on packages/rules.

---

# 147. Rego Package Naming

Generated package identity SHOULD be deterministic and collision-resistant.

Example:

```text
baobab.regulations.generated.<ruleset>
```

Exact convention is deferred.

---

# 148. No Canonical Rego Editing

Editing generated Rego directly SHALL be treated like editing compiled output.

Source changes belong upstream in:

```text
RuleVersion / BRIR.
```

---

# 149. Compiler Pipeline

```text
BRIR
  │
  ▼
schema validation
  │
  ▼
semantic validation
  │
  ▼
normalisation
  │
  ▼
target capability analysis
  │
  ▼
Rego AST generation
  │
  ▼
opa format/check
  │
  ▼
generated tests
  │
  ▼
opa test
  │
  ▼
bundle build
  │
  ▼
bundle sign
  │
  ▼
publish artifact.
```

---

# 150. No Text Templates for Complex Compilation

The compiler SHOULD construct an intermediate target AST or similarly structured representation rather than rely entirely on fragile string concatenation.

---

# 151. Deterministic Compilation

Given identical:

```text
BRIR

compiler version

target configuration
```

the compiler SHOULD produce semantically identical output.

---

# 152. Build Fingerprint

Compiled artefact SHALL record:

```text
BRIR fingerprint

compiler version

target version

target configuration

bundle revision/hash.
```

---

# 153. Compiled Artifact

Conceptually:

```text
CompiledPolicyArtifact
├── artifact_id
├── ruleset_ref
├── source_rule_refs[]
├── brir_version
├── compiler_version
├── target
├── target_version
├── artifact_hash
├── test_result_ref
├── built_at
└── provenance
```

---

# 154. RuleSet

Regulatory execution SHOULD compile immutable:

```text
RegulatoryRuleSet
```

snapshots rather than arbitrary live rule queries.

---

# 155. RuleSet Contents

A RuleSet may include:

```text
rule versions

dependencies

definition rules

verified override relationships

temporal metadata

supporting static regulatory data.
```

---

# 156. RuleSet Fingerprint

The same RuleSet fingerprint SHALL identify the same semantic rule collection.

---

# 157. Static Regulatory Data

OPA's `data` document MAY contain compiled/projected regulatory data such as:

```text
classification tables

verified thresholds

country group membership

public regulatory constants.
```

It SHALL be versioned with the ruleset.

---

# 158. Runtime Facts

OPA `input` SHOULD contain per-evaluation facts/context.

Conceptually:

```text
data
    stable ruleset data

input
    transaction/evaluation state.
```

---

# 159. No Mutable External Truth Hidden in OPA

If OPA holds cached base data, its version SHALL be identifiable.

---

# 160. Bundle Distribution

OPA bundles provide a standard mechanism for distributing policy and supporting data to OPA agents.

Baobab SHOULD use versioned bundles for the initial target architecture.

---

# 161. Signed Bundles

OPA supports cryptographically signed bundles and verifies hashes/signatures before activating new policy bundles. If verification fails, OPA retains the existing bundle rather than activating the invalid replacement.

E3/E4 deployments SHOULD use signed bundles.

---

# 162. Bundle Signature Meaning

Bundle signature establishes:

```text
integrity

trusted publisher identity.
```

It does not establish:

```text
legal correctness.
```

---

# 163. Bundle Revision

Every deployed bundle SHALL expose an immutable revision/fingerprint traceable to its source RuleSet.

---

# 164. Decision Logging

OPA decision logs can include:

```text
decision_id

trace_id

bundle revisions

policy path

input/result.
```


Baobab SHALL capture the relevant identifiers within the larger `DecisionTrace`.

---

# 165. Sensitive Inputs

OPA decision logging SHALL be configured so sensitive:

```text
tenant facts

privileged evidence

commercial secrets
```

are not indiscriminately logged.

---

# 166. OPA Decision Log Is Not Canonical Decision Store

Regulations' canonical `RegulatoryDecision` remains in PostgreSQL.

OPA logs are execution/audit evidence.

---

# 167. OPA Optimization

OPA supports build-time policy optimization and partial evaluation.

Baobab MAY use such optimization after proving semantic equivalence through regression tests.

---

# 168. Optimization SHALL Be Transparent

An optimization changing runtime implementation SHALL NOT create a new:

```text
RuleVersion
```

if semantics remain identical.

It SHALL create a different:

```text
CompiledPolicyArtifact
```

if appropriate.

---

# 169. Performance Does Not Override Semantics

No optimization MAY convert:

```text
UNKNOWN
```

into:

```text
FALSE
```

or otherwise change BRIR semantics.

---

# 170. Testing Layers

Every executable rule SHOULD participate in:

```text
BRIR unit tests

compiler tests

target tests

golden regulatory cases

cross-target equivalence tests

historical temporal tests.
```

---

# 171. OPA Tests

OPA provides native policy unit tests and coverage reporting; `opa test --fail-on-empty` can ensure CI does not pass when no tests execute.

Generated Rego SHALL have corresponding target tests.

---

# 172. Generated Tests

BRIR golden cases MAY compile into:

```text
Rego tests
```

automatically.

---

# 173. Positive Case

Rule expected:

```text
APPLIES.
```

---

# 174. Negative Case

Rule expected:

```text
DOES_NOT_APPLY.
```

---

# 175. Exception Case

Base conditions true, exception true:

```text
DEFEATED / EXEMPTED.
```

---

# 176. Unknown Case

Required fact missing:

```text
INDETERMINATE.
```

---

# 177. Error Case

Invalid calculation:

```text
ERROR.
```

Not:

```text
FALSE.
```

---

# 178. Boundary Case

Examples:

```text
threshold exactly N

date exactly effective date

permit expires same date

amount exactly statutory limit.
```

---

# 179. Temporal Case

Same transaction evaluated:

```text
before amendment

after amendment

historical-as-known

historical-restated.
```

---

# 180. Override Case

General rule applies but verified special rule overrides it.

---

# 181. Conflict Case

Two incompatible rules with unresolved precedence:

```text
INDETERMINATE / REVIEW_REQUIRED.
```

---

# 182. Reparative Case

Primary obligation violated; appropriate reparation rule activates.

---

# 183. Regression Corpus

Each jurisdiction pack SHALL contain:

```text
golden regulatory cases.
```

These become part of rule publication gates.

---

# 184. Compiler Conformance

The BRIR→Rego compiler SHALL have an independent conformance suite.

---

# 185. Cross-Evaluator Oracle

Baobab SHOULD eventually maintain a small reference BRIR interpreter for tests.

Purpose:

```text
BRIR expected semantics
        ↓ compare
OPA compiled result.
```

This prevents the compiler target from becoming the only definition of IR semantics.

---

# 186. Reference Evaluator

The reference evaluator need not initially meet production latency requirements.

Its primary role may be:

```text
semantic oracle

testing

debugging.
```

---

# 187. Cross-Target Equivalence

If later compiling BRIR to:

```text
OPA

CEL

DMN
```

the same golden case SHALL produce semantically equivalent regulatory results.

---

# 188. Target-Specific Unsupported Feature

If a target cannot preserve semantics:

```text
COMPILATION_UNSUPPORTED
```

is correct.

Do not approximate silently.

---

# 189. Target Capability Matrix

Conceptually:

| BRIR capability | OPA | CEL | DMN |
|---|---:|---:|---:|
| Boolean predicates | Yes | Yes | Yes |
| Sets / membership | Yes | Yes | Varies |
| Quantification | Yes | Some | Varies |
| Decision tables | Possible | Limited | Strong |
| Deontic effects | Compiled projection | Projection | Projection |
| Defeasible legal priority | Baobab-generated logic | Limited | Not canonical |
| Human discretion | No | No | Can model handoff |
| External authority decision | Input fact | Input fact | Input |

The matrix SHALL be tested, not assumed.

---

# 190. Decision Tables

Where a rule is naturally tabular:

```text
input combinations
→ outcome
```

BRIR MAY contain a decision-table representation.

---

# 191. Decision Table Is Still BRIR

It SHALL not require DMN internally.

---

# 192. DMN Export

A compatible BRIR decision table MAY later export to DMN for analyst/legal-review tooling.

---

# 193. Human Readability

BRIR SHOULD support deterministic generation of a controlled-language rendering such as:

```text
WHEN:
  activity is IMPORT
  AND destination is ZA

UNLESS:
  valid exemption exists

THEN:
  importer is OBLIGED TO
  provide requirement X.
```

---

# 194. Controlled Language Is a Projection

It assists:

```text
review

approval

debugging.
```

The structured BRIR remains authoritative for execution.

---

# 195. Round-Trip Caution

Natural language SHALL not be assumed to round-trip perfectly back into BRIR.

---

# 196. AI-Assisted BRIR Generation

Haystack/LLMs MAY propose candidate BRIR.

---

# 197. AI SHALL NOT Publish BRIR

Candidate pipeline:

```text
Source
   ↓
AI candidate extraction
   ↓
Candidate BRIR
   ↓
semantic validation
   ↓
human / governed review
   ↓
verified RuleVersion
   ↓
published BRIR.
```

---

# 198. AI-Generated Expressions

Every AI-produced expression SHALL be:

```text
schema validated

type checked

source traceable

golden-tested.
```

---

# 199. AI Cannot Create Unsupported Operator

Unknown operator:

```text
"probablyRequires"
```

SHALL fail validation.

---

# 200. Compiler Trust Boundary

The BRIR compiler is consequential security/regulatory infrastructure.

It SHALL be treated similarly to:

```text
critical compiler

policy compiler

rules engine.
```

---

# 201. Compiler Changes

Material compiler changes SHALL require:

```text
review

tests

cross-version regression

artifact comparison.
```

---

# 202. Compiler Version Pinning

A historical decision SHALL be able to identify:

```text
compiler version

compiled policy artifact

bundle revision.
```

---

# 203. Determinism

Compiler builds SHOULD avoid:

```text
timestamps inside semantic output

random ordering

unstable hash inputs.
```

---

# 204. Canonical Ordering

Sets/maps SHOULD use deterministic canonicalisation where fingerprints depend on them.

---

# 205. BRIR Fingerprint

A RuleVersion SHOULD have a canonical BRIR fingerprint.

---

# 206. Fingerprint Meaning

Same fingerprint means:

```text
same normalised BRIR representation
```

under the defined canonicalisation.

It does not independently prove:

```text
legal correctness.
```

---

# 207. Security — Injection

Because BRIR is structured and target code is generated, user-controlled strings SHALL never be inserted into executable Rego without safe target encoding.

---

# 208. No Raw Rego from Tenant Inputs

Tenant data SHALL not provide:

```text
rego fragments

package names

function code
```

that become executable policy.

---

# 209. Rule Authorisation

Only authorised governance processes may publish:

```text
RuleVersion

BRIR

compiled regulatory bundles.
```

---

# 210. Source Data versus Executable Policy

Regulatory source text SHALL remain:

```text
data/evidence
```

and SHALL never execute merely because it contains something resembling:

```text
Rego

JSON

prompt instructions.
```

---

# 211. Compiler Sandboxing

Compilation workers SHOULD have:

```text
minimal privileges

no production DB write authority beyond artifact workflow

bounded CPU/memory

controlled filesystem.
```

---

# 212. Artifact Signing

E3/E4 compiled-policy publication SHOULD produce signed artifacts/bundles.

---

# 213. Key Management

Signing keys SHALL NOT live in:

```text
source repository

compiler code

rule bundle.
```

Key-management architecture belongs to Infrastructure/IAM.

---

# 214. Promotion Workflow

Preferred:

```text
Verified RuleVersion
      │
      ▼
BRIR published
      │
      ▼
compiler
      │
      ▼
artifact
      │
      ▼
tests
      │
      ▼
signature
      │
      ▼
release
      │
      ▼
runtime activation
      │
      ▼
readiness verification.
```

---

# 215. Compilation Failure

If a verified RuleVersion cannot compile:

```text
RULE REMAINS VALID REGULATORY KNOWLEDGE
```

but:

```text
AUTOMATED EXECUTION NOT READY.
```

---

# 216. Readiness Separation

Track separately:

```text
semantic readiness

compilation readiness

deployment readiness

runtime readiness.
```

---

# 217. Legal Effect Before Runtime Readiness

If law becomes effective but compiled runtime is unavailable:

```text
regulatory readiness failure
```

SHALL be visible.

Do not continue with stale automation as though nothing changed.

---

# 218. Enforcement Ceiling

Every BRIR RuleVersion SHALL retain the `max_effect_class` from ADR-REG-0004.

---

# 219. Compiler Cannot Escalate

A rule approved only for:

```text
E1
```

cannot become:

```text
E4
```

because it successfully compiled to Rego.

---

# 220. Execution Success ≠ Regulatory Assurance

```text
OPA returned a result
```

does not imply:

```text
rule legally verified.
```

---

# 221. E4 Compilation Gate

A rule eligible for E4 SHOULD require:

```text
published verified RuleVersion

complete provenance

deterministic executability

supported target capability

no unresolved override conflict

temporal certainty

required fact schema

golden cases passing

compiler conformance

signed deployment artifact

runtime readiness.
```

---

# 222. OPA Undefined Result

If the target query returns undefined unexpectedly:

```text
ERROR / INDETERMINATE
```

shall be surfaced.

It SHALL NOT become default:

```text
ALLOW.
```

---

# 223. Default Deny Is Not Enough

Security systems often use:

```text
default deny.
```

Regulatory systems need richer semantics.

For example:

```text
UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE
```

are materially different.

---

# 224. Regulatory Result ≠ Authorization Result

OPA is frequently used for authorization.

Baobab Regulations SHALL return regulatory semantics, not simply:

```text
allow / deny.
```

---

# 225. Authorization Remains IAM/CP Concern

Example:

```text
May user Alice request this assessment?
```

belongs to:

```text
IAM / Control Plane authorization.
```

---

# 226. Regulatory Question

Example:

```text
Does shipment S satisfy
the regulatory requirements
for import?
```

belongs to Regulations.

Both might use OPA internally.

Their semantics remain different.

---

# 227. Separate Bundles

IAM authorization policies and regulatory-rule bundles SHALL NOT be casually combined merely because both use OPA.

---

# 228. Different Authorities

```text
IAM policy
    authority = platform security/governance.

Regulatory rule
    authority = external law/regulation.
```

The distinction is foundational.

---

# 229. PostgreSQL Ownership

Canonical:

```text
RuleVersion

BRIR metadata

RuleSet

provenance

compiled artifact metadata
```

SHALL remain persisted under Regulations ownership in PostgreSQL.

---

# 230. Compiled Policy Storage

Generated Rego/bundles MAY live in:

```text
artifact/object storage
```

with PostgreSQL metadata.

---

# 231. Qdrant

Qdrant SHALL NOT store the canonical BRIR execution model.

It MAY index:

```text
rule descriptions

citations

controlled-language rendering

explanation metadata
```

for retrieval.

---

# 232. Haystack

Haystack MAY retrieve and assist in generating/explaining BRIR candidates.

It SHALL NOT execute authoritative deterministic rules.

---

# 233. LangGraph

LangGraph MAY orchestrate:

```text
candidate review

rule verification

compiler failure remediation

maker-checker promotion.
```

It SHALL NOT define BRIR semantics.

---

# 234. Pulse

Pulse MAY consume:

```text
rule changed

obligation changed

threshold changed

future-effective rule
```

projections for commercial-impact analysis.

Pulse SHALL not compile or mutate BRIR.

---

# 235. CMS

CMS MAY consume:

```text
human-readable rule projection

effective dates

citations

requirements.
```

CMS SHALL not store an alternative executable representation.

---

# 236. Shared

Cross-engine BRIR public contracts MAY eventually be placed in `shared` where necessary.

However:

```text
shared
```

shall contain canonical schemas/contracts—not runtime Rego implementations.

---

# 237. API Boundaries

Consumers SHOULD see:

```text
RegulatoryDecision

Assessment

Requirements

Explanation
```

not:

```text
Rego query

OPA package

BRIR AST
```

unless they possess explicit administration/developer capabilities.

---

# 238. BRIR Administration API

Administrative capabilities MAY include:

```text
validate BRIR

compile BRIR

compare versions

explain target support

run golden cases.
```

---

# 239. No Public Rule Editing Initially

Direct end-user BRIR editing SHOULD NOT be exposed initially.

The governance risk is too high.

---

# 240. Future Rule Authoring UI

A future regulatory-authoring interface MAY render:

```text
decision tables

controlled natural language

visual conditions

normative effects
```

and generate BRIR.

BRIR remains the machine contract.

---

# 241. Rule Diff

Baobab SHOULD support semantic BRIR diff.

Example:

```text
threshold:
1000 → 1500

effect:
OBLIGATION unchanged

exception:
new exception added.
```

---

# 242. Avoid Text-Only Diff

Comparing generated Rego line-by-line is insufficient because compiler changes can alter code without changing semantics.

---

# 243. Semantic Change Classification

Potential:

```text
CONDITION_ADDED

CONDITION_REMOVED

THRESHOLD_CHANGED

EFFECT_CHANGED

EXCEPTION_ADDED

EXCEPTION_REMOVED

BEARER_CHANGED

TEMPORAL_SCOPE_CHANGED

REQUIREMENT_CHANGED

CALCULATION_CHANGED.
```

---

# 244. Impact Analysis

A semantic BRIR change SHALL feed ADR-REG-0023 impact analysis.

---

# 245. OPA Target Validation

Generated policy SHALL pass at minimum:

```text
opa fmt

opa check --strict

opa test --fail-on-empty

golden-case execution.
```

Exact CI commands may evolve with OPA versions.

---

# 246. Regal

Regal MAY be used as an additional Rego linter for generated or infrastructure Rego.

Its recommendations SHALL not override BRIR semantics.

---

# 247. Target Version Pinning

Production compilation SHALL pin supported:

```text
OPA version range

Rego language profile.
```

---

# 248. Upgrade Testing

OPA upgrades SHALL run:

```text
compiler suite

golden cases

historical decisions

performance benchmarks

undefined/error cases.
```

before production rollout.

---

# 249. No Automatic Major Upgrade

A new OPA major version SHALL not be accepted solely because generated Rego compiles.

Semantic equivalence must be proven.

---

# 250. OPA IR Version Independence

OPA's low-level IR itself is versioned and may introduce future incompatible versions.

Another reason Baobab SHALL not make it canonical.

---

# 251. Performance Benchmark

Performance tests SHOULD include:

```text
single-rule evaluation

large RuleSet

complex quantification

large input facts

multiple effects

historical ruleset

concurrent transaction load.
```

---

# 252. Performance Budget

Exact latency SLO belongs to ADR-REG-0018/0030.

But compilation architecture SHALL target:

```text
compile once

evaluate many.
```

This is also the design model promoted by CEL and is appropriate for Baobab's fast path.

---

# 253. Precompilation

Production transactional paths SHALL not compile RuleVersions per request.

---

# 254. Runtime Path

Preferred:

```text
request
  ↓
resolve context
  ↓
select published RuleSet
  ↓
evaluate precompiled policy
  ↓
typed results
  ↓
decision assembly.
```

---

# 255. Compilation Path

Separate:

```text
regulatory knowledge change
  ↓
BRIR
  ↓
compile
  ↓
test
  ↓
publish bundle.
```

---

# 256. Safe Bundle Rollout

Bundle rollout SHOULD support:

```text
candidate

shadow

canary

active

rollback.
```

Detailed PDP deployment belongs in ADR-REG-0019.

---

# 257. Shadow Evaluation

New compiled RuleSet MAY evaluate real inputs without affecting operational disposition.

Compare:

```text
current result
vs
candidate result.
```

---

# 258. Difference Detection

Unexpected decision differences SHALL block promotion where required.

---

# 259. Rollback

Rollback SHALL restore:

```text
previous compiled artifact
```

without rewriting canonical legal history.

---

# 260. Rollback Is Operational

If new RuleVersion is legally correct but deployment artifact is broken:

```text
operational rollback
```

does not mean:

```text
legal RuleVersion repealed.
```

---

# 261. Rule Execution Errors

Canonical error categories SHOULD include:

```text
MISSING_REQUIRED_FACT

UNKNOWN_FACT

INVALID_FACT_TYPE

UNSUPPORTED_OPERATOR

FUNCTION_ERROR

CALCULATION_ERROR

TEMPORAL_ERROR

RULESET_INCONSISTENCY

UNRESOLVED_OVERRIDE

TARGET_RUNTIME_ERROR.
```

---

# 262. Error to Decision Mapping

ADR-REG-0018 SHALL define how those errors influence overall assessment.

Default for material unresolved execution errors SHALL be conservative.

---

# 263. Error Cannot Become Not Applicable

This is a hard invariant.

---

# 264. Rule Result Explainability

Each result SHALL identify:

```text
rule

matched predicates

failed predicates

unknown predicates

exception status

effect

reason codes.
```

---

# 265. Explanation Does Not Need Source Code

Users should see:

```text
Rule R applies because...
```

not:

```text
Rego line 89 returned true.
```

---

# 266. Developer Diagnostics

Administrative diagnostics MAY include:

```text
Rego package

entrypoint

bundle revision

OPA decision ID.
```

---

# 267. Initial OPA Entrypoint

A generated ruleset SHOULD expose a stable Baobab-defined evaluation entrypoint returning structured JSON.

Exact package/path is implementation detail.

---

# 268. One Rule ≠ One Network Call

OPA SHOULD evaluate an applicable RuleSet in an efficient batch/aggregate manner rather than requiring one HTTP call per rule.

---

# 269. Overall Decision Outside Individual Rule

Individual policy evaluation produces:

```text
rule evaluations

effects

requirements.
```

ADR-REG-0018 assembles those into the canonical:

```text
AssessmentOutcome.
```

---

# 270. OPA Does Not Own Decision Aggregation by Default

Some deterministic aggregation MAY run in OPA.

But the canonical decision semantics remain Regulations-owned.

---

# 271. Conflict Aggregation

Example:

```text
Permission P
+
Prohibition Q
```

requires the resolved normative/hierarchy semantics from BRIR.

It SHALL not use:

```text
deny wins
```

as an arbitrary general algorithm.

---

# 272. Unknown Aggregation

One rule being unknown does not always make the entire transaction indeterminate.

It depends on whether that rule is material to the requested regulatory question.

ADR-REG-0018 will formalise this.

---

# 273. Rule Applicability Filtering

Some filtering MAY occur before OPA using:

```text
jurisdiction

domain

legal time

profile.
```

This improves efficiency.

---

# 274. Filtering Must Be Semantically Safe

Pre-filtering cannot remove rules whose applicability still requires execution.

---

# 275. RuleSet Resolver

The Regulations domain SHOULD select:

```text
candidate RuleSet
```

before deterministic evaluation.

---

# 276. OPA Is Not Rule Discovery

OPA should evaluate:

```text
resolved executable rule universe
```

not search the regulatory corpus.

---

# 277. Qdrant Is Not Rule Execution

Conversely, semantic similarity SHALL never determine:

```text
whether rule applies.
```

---

# 278. BRIR and Temporal Versioning

Every BRIR SHALL bind to:

```text
RuleVersion

legal-valid state

knowledge state
```

from ADR-REG-0015.

---

# 279. Future Rules

BRIR MAY exist and be compiled before:

```text
legal_valid_from.
```

Runtime legal-time checks determine applicability.

---

# 280. Historical BRIR

Old BRIR versions SHALL remain available for:

```text
historical replay

audit

decision reconstruction.
```

---

# 281. Historical Compiled Artifact

For high-assurance decisions, retain the compiled artifact or sufficient build inputs/fingerprints to reconstruct it.

---

# 282. Rule Retirement

Retiring an old runtime artifact SHALL not delete:

```text
RuleVersion

BRIR

decision provenance.
```

---

# 283. Initial Example — Deterministic Rule

Synthetic:

```text
IF:
activity = IMPORT

AND:
product_classification = X

AND:
destination jurisdiction = Y

THEN:
OBLIGATION:
bearer IMPORTER
must provide Requirement P

UNLESS:
verified Exemption E active.
```

This is OPA-compilable if all facts/semantics are deterministic.

---

# 284. Initial Example — Not Deterministically Executable

Synthetic:

```text
Authority may approve an exception
where circumstances are reasonable
and in the public interest.
```

BRIR:

```text
AUTHORITY_DECISION_REQUIRED.
```

Not:

```text
if score > 0.75:
    allow.
```

---

# 285. Initial Example — External Fact

```text
IF regulator-issued licence.status = ACTIVE
THEN requirement satisfied.
```

OPA can evaluate the status.

OPA does not determine whether the regulator validly issued the licence.

---

# 286. Initial Example — Unknown

```text
licence.status = UNKNOWN
```

Result:

```text
INDETERMINATE
```

not:

```text
UNSATISFIED
```

unless the underlying legal rule explicitly makes absence of proof sufficient for non-satisfaction.

---

# 287. Initial Example — Evidence Burden

A rule may legitimately state:

```text
failure to present required evidence
means requirement not satisfied.
```

Then:

```text
missing evidence
```

can result in:

```text
UNSATISFIED
```

because the rule explicitly defines that consequence.

This is different from generic closed-world inference.

---

# 288. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-IR-I01` | BRIR SHALL be owned by Baobab Regulations |
| `REG-IR-I02` | Rego SHALL not be the canonical regulatory representation |
| `REG-IR-I03` | OPA's internal IR SHALL not be BRIR |
| `REG-IR-I04` | RuleVersion SHALL remain distinct from BRIR schema version |
| `REG-IR-I05` | Compiled policy SHALL remain distinct from canonical rule semantics |
| `REG-IR-I06` | Runtime deployment SHALL not determine legal validity |
| `REG-IR-I07` | UNKNOWN SHALL remain distinct from FALSE |
| `REG-IR-I08` | ERROR SHALL remain distinct from UNKNOWN |
| `REG-IR-I09` | Missing input SHALL not automatically imply legal negation |
| `REG-IR-I10` | Closed-world reasoning SHALL require explicit verified scope |
| `REG-IR-I11` | Normative effects SHALL not collapse into Boolean allow/deny |
| `REG-IR-I12` | Obligation, prohibition and permission SHALL remain distinguishable |
| `REG-IR-I13` | Strong permission SHALL remain distinguishable from silence |
| `REG-IR-I14` | Exceptions SHALL remain explicitly representable |
| `REG-IR-I15` | Defeasible override relations SHALL not become arbitrary priority numbers |
| `REG-IR-I16` | Unresolved legal conflict SHALL not be silently compiled away |
| `REG-IR-I17` | Legal discretion SHALL not be converted into invented deterministic thresholds |
| `REG-IR-I18` | Rules SHALL not perform arbitrary network I/O |
| `REG-IR-I19` | AI-generated BRIR SHALL remain candidate state until governed promotion |
| `REG-IR-I20` | Compilation SHALL be deterministic and versioned |
| `REG-IR-I21` | Target-specific unsupported semantics SHALL fail explicitly |
| `REG-IR-I22` | Generated Rego SHALL be traceable to RuleVersion and BRIR |
| `REG-IR-I23` | OPA runtime errors SHALL not silently become regulatory false |
| `REG-IR-I24` | Wasm equivalence SHALL be tested before E3/E4 use |
| `REG-IR-I25` | Bundles supporting E3/E4 SHOULD be signed |
| `REG-IR-I26` | Golden regulatory tests SHALL gate consequential publication |
| `REG-IR-I27` | Historical BRIR SHALL remain available for replay |
| `REG-IR-I28` | IAM/security policy and regulatory policy SHALL remain distinct even when both use OPA |
| `REG-IR-I29` | Consumers SHALL receive Baobab regulatory contracts, not Rego/OPA internals |
| `REG-IR-I30` | Replacing OPA SHALL not require redefining canonical regulatory meaning |

---

# 289. Rejected Alternative — Direct Rego Authoring as Canonical Law

Rejected.

It binds regulatory semantics to one runtime.

---

# 290. Rejected Alternative — OPA IR as Canonical IR

Rejected.

OPA's IR represents planned Rego evaluation, not Baobab legal semantics.

---

# 291. Rejected Alternative — Generic `allow`

Rejected.

Regulatory outcomes are richer than access authorization.

---

# 292. Rejected Alternative — Missing Fact Means False

Rejected.

Dangerous in law.

---

# 293. Rejected Alternative — Everything Unknown Means Deny

Rejected as a universal semantic rule.

A conservative operational hold may be appropriate later, but:

```text
INDETERMINATE
```

must remain the regulatory conclusion.

---

# 294. Rejected Alternative — Raw Python Rules

Rejected.

It creates:

```text
security risk

provider coupling

poor static validation

poor portability.
```

---

# 295. Rejected Alternative — Raw SQL Rules

Rejected for the same reasons.

---

# 296. Rejected Alternative — Natural Language as Executable Rule

Rejected.

Natural language remains source/interpretation/explanation material.

---

# 297. Rejected Alternative — LLM Executes Law at Runtime

Rejected for deterministic transactional decisions.

---

# 298. Rejected Alternative — AI Confidence Controls Enforcement

Rejected.

A high model confidence score does not create legal verification.

---

# 299. Rejected Alternative — Priority Numbers Resolve Law

Rejected.

ADR-REG-0007 governs legal hierarchy.

---

# 300. Rejected Alternative — Rego File Order Resolves Conflicts

Rejected.

---

# 301. Rejected Alternative — Runtime Bundle Deployment Changes Legal Time

Rejected.

ADR-REG-0015 governs temporal truth.

---

# 302. Rejected Alternative — Qdrant Retrieval Decides Applicable Rule

Rejected.

Retrieval and legal applicability are separate.

---

# 303. Rejected Alternative — Haystack Pipeline as Rule Engine

Rejected.

Haystack assists knowledge processing.

---

# 304. Rejected Alternative — LangGraph as Transaction Rule Engine

Rejected.

LangGraph governs slow-path review/workflows.

---

# 305. Rejected Alternative — Wasm Everywhere Immediately

Rejected.

OPA documents meaningful differences in supported runtime behaviour, including strict built-in error handling availability.

---

# 306. Minimum Implementation Proof

Before `ADR-REG-0016` is considered implemented, Baobab SHOULD demonstrate:

```text
1. BRIR JSON Schema v1.

2. Typed BRIR domain model.

3. RuleVersion → BRIR mapping.

4. Constitutive rule.

5. Obligation rule.

6. Prohibition rule.

7. Explicit permission rule.

8. Exception.

9. Verified exemption.

10. Composite conditions.

11. ALL_OF / ANY_OF requirements.

12. EXISTS quantifier.

13. FOR_ALL quantifier.

14. Typed dates.

15. Typed decimal.

16. Money.

17. Quantity/unit handling.

18. Deadline expression.

19. Calculation.

20. Temporal applicability.

21. Future-effective rule.

22. Defeasible rule.

23. Explicit override relationship.

24. Unresolved conflict rejected from deterministic compilation.

25. Reparative rule.

26. HUMAN_JUDGMENT_REQUIRED rule.

27. AUTHORITY_DECISION_REQUIRED rule.

28. REPRESENTATIONAL_ONLY rule.

29. UNKNOWN fact.

30. ERROR fact.

31. Missing fact does not become false.

32. Closed-world scope proof.

33. BRIR schema validation.

34. BRIR type validation.

35. Semantic validation.

36. Dependency-cycle detection.

37. BRIR canonical fingerprint.

38. BRIR → Rego v1 compiler.

39. Generated Rego metadata.

40. Generated input JSON Schema.

41. `opa check --strict` success.

42. `opa test --fail-on-empty` success.

43. Golden-case compilation.

44. Positive evaluation.

45. Negative evaluation.

46. Exception evaluation.

47. Unknown evaluation.

48. Runtime error evaluation.

49. Strict OPA error handling.

50. Structured OPA result rather than bare allow/deny.

51. RuleSet compilation.

52. OPA bundle creation.

53. Signed OPA bundle.

54. Bundle revision tracking.

55. OPA decision ID tracking.

56. Compiler version tracking.

57. Historical artifact retention.

58. Shadow candidate ruleset evaluation.

59. Rollback.

60. Reference BRIR evaluator or semantic oracle.

61. BRIR↔OPA equivalence tests.

62. OPA upgrade regression suite.

63. Wasm equivalence test showing any unsupported semantic difference.

64. Synthetic DMN-compatible decision-table export.

65. Synthetic CEL-compatible predicate compilation or compatibility analysis.

66. Rule explainability generated without displaying Rego.

67. No framework-native type exposed through consumer API.

68. End-to-end Source → Provision → Interpretation → RuleVersion → BRIR → Rego → OPA Decision lineage.
```

---

# 307. Initial ZuriBeans Proof

The first corridor SHOULD contain a representative executable set covering:

```text
classification rule

trade-lane applicability

document requirement

permit requirement

certificate requirement

tariff calculation

effective-date transition

rule exception

verified exemption

unknown fact

evidence requirement

reparative consequence.
```

Actual regulatory content SHALL be sourced and verified before implementation.

---

# 308. Initial Compilation Proof

For one verified synthetic rule:

```text
RuleVersion
      ↓
BRIR
      ↓
Generated Rego
      ↓
OPA bundle
      ↓
OPA decision
```

The same test case SHALL be evaluated by:

```text
BRIR reference semantics
```

and:

```text
OPA target
```

with equivalent output.

---

# 309. Initial Unknown Proof

Input:

```text
product classification = UNKNOWN.
```

BRIR:

```text
classification required.
```

Expected:

```text
truth = UNKNOWN

applicability = INDETERMINATE

unknown_fact =
product.classification
```

No Boolean false shortcut.

---

# 310. Initial Runtime Error Proof

A malformed calculation input SHALL produce:

```text
ERROR
```

and a structured reason.

It SHALL not result in:

```text
NOT_APPLICABLE

ALLOW

FALSE
```

by accident.

---

# 311. Initial Defeasibility Proof

```text
General Rule A:
prohibition.

Specific verified Rule B:
permission under Exception X.

Verified override:
B overrides A
within X.
```

Result under X:

```text
A defeated

B applies.
```

Outside X:

```text
A applies.
```

---

# 312. Initial Unresolved Conflict Proof

```text
Rule A:
OBLIGATION X.

Rule B:
PROHIBITION X.

No verified precedence.
```

Result:

```text
RULE_CONFLICT

REVIEW_REQUIRED.
```

Not:

```text
last rule wins.
```

---

# 313. Strategic Architecture

BRIR creates a stable centre:

```text
            LEGAL SOURCES
                  │
                  ▼
             INTERPRETATION
                  │
                  ▼
              RULE VERSION
                  │
                  ▼
                 BRIR
      ┌───────────┼───────────┐
      ▼           ▼           ▼
     OPA         CEL         DMN
    Rego       future      future
      │
      ▼
REGULATORY EXECUTION
```

---

# 314. Strategic Provider Neutrality

Without BRIR:

```text
switch OPA
=
rewrite regulation.
```

With BRIR:

```text
switch OPA
=
implement new compiler target
+
prove semantic equivalence.
```

That is the correct dependency direction.

---

# 315. Strategic AI Boundary

Haystack and AI can increasingly improve:

```text
source extraction

interpretation candidate generation

BRIR candidate generation.
```

Yet transactional execution remains:

```text
verified

typed

compiled

deterministic.
```

---

# 316. Strategic Auditability

A customer can traverse:

```text
Decision
  ↓
OPA decision ID
  ↓
bundle revision
  ↓
CompiledPolicyArtifact
  ↓
BRIR
  ↓
RuleVersion
  ↓
Interpretation
  ↓
Provision
  ↓
Official Source.
```

---

# 317. Strategic Portability

This gives Baobab options.

For example:

```text
central Regulations:
OPA server

edge/low-latency:
future Wasm or CEL

analyst interchange:
DMN

legal interoperability:
LegalRuleML

canonical semantics:
BRIR.
```

---

# 318. Research Foundation Summary

OPA is explicitly designed to decouple policy decision-making from enforcement, uses declarative Rego over structured data, and supports REST, Go and WebAssembly execution models. These capabilities make it a strong initial execution target rather than an appropriate canonical legal model.

OPA itself maintains a low-level compiler IR for planned Rego evaluation paths, reinforcing why Baobab must distinguish domain-level BRIR from target-engine implementation IR.

OPA's normal runtime semantics can treat built-in runtime errors as undefined unless strict built-in errors are enabled, and strict built-in errors are not available in the Wasm profile. Baobab therefore requires explicit `TRUE / FALSE / UNKNOWN / ERROR` semantics above OPA rather than relying directly on undefined/Boolean behavior.

OPA provides native policy testing, coverage, compiler validation, bundle distribution, bundle signing and decision logging with bundle revisions and decision IDs. These capabilities support a strong compilation/deployment/audit pipeline.

LegalRuleML provides established legal-rule concepts including obligations, permissions, prohibitions, defeasibility, overrides, violations, reparations and temporal characteristics. BRIR uses these concepts as interoperability and semantic guidance without making LegalRuleML XML its operational representation.

DMN provides an industry standard for business decisions and executable decision tables, while CEL offers a safe, portable, non-Turing-complete expression model. Both therefore remain credible future BRIR compilation/interoperability targets without displacing BRIR itself.

JSON Schema Draft 2020-12 provides an appropriate standards-based mechanism for defining and validating BRIR's portable JSON representation.

---

# 319. Final Decision

Baobab Regulations SHALL establish **BRIR — Baobab Regulatory Rule Intermediate Representation** as the canonical machine-executable representation of verified regulatory rules.

The final architecture is:

```text
                     AUTHORITATIVE LAW
                            │
                            ▼
                         PROVISION
                            │
                            ▼
                     INTERPRETATION
                            │
                            ▼
                       RULE VERSION
                            │
                            ▼
                           BRIR
                            │
          ┌─────────────────┼────────────────┐
          │                 │                │
          ▼                 ▼                ▼
      VALIDATOR         EXPLAINER        COMPILER
                                             │
                                             ▼
                                           REGO
                                             │
                                             ▼
                                      SIGNED OPA BUNDLE
                                             │
                                             ▼
                                            OPA
                                             │
                                             ▼
                                   STRUCTURED RULE RESULT
                                             │
                                             ▼
                                  REGULATORY ASSESSMENT
                                             │
                                             ▼
                                   REGULATORY DECISION
```

The critical semantic model is:

```text
Fact
    KNOWN
    UNKNOWN
    ERROR

        ↓

Condition
    TRUE
    FALSE
    UNKNOWN
    ERROR

        ↓

Rule
    APPLIES
    DOES_NOT_APPLY
    DEFEATED
    EXEMPTED
    INDETERMINATE
    ERROR

        ↓

Normative Effect
    OBLIGATION
    PROHIBITION
    PERMISSION
    ...
```

Not:

```text
allow = true
allow = false
```

The provider-neutrality rule is:

> **Baobab Regulations SHALL be capable of replacing OPA without rewriting its regulatory knowledge.**

The determinism rule is:

> **Only sufficiently formalised and verified regulatory semantics SHALL enter deterministic execution.**

The uncertainty rule is:

> **Unknown is not false, absence is not prohibition, and an execution error is not legal non-applicability.**

The legal-governance rule is:

> **No compiler, policy language or runtime engine may resolve legal ambiguity that Baobab's governed regulatory model has not already resolved.**

The AI rule is:

> **AI may help produce candidate BRIR; AI does not make candidate BRIR authoritative.**

The OPA rule is:

> **OPA decides against Baobab's compiled policy; Baobab Regulations determines what the policy means.**

And the strategic principle is:

> **BRIR is the seam that lets Baobab turn verified regulation into executable software without turning a particular software language into law.**

That is the architecture established by `ADR-REG-0016`.

---

## Decision Summary

```text
ADR-REG-0016
────────────────────────────────────────────

CANONICAL MACHINE REPRESENTATION

BRIR
Baobab Regulatory Rule IR


BRIR IS

Typed
Versioned
Provider-neutral
Source-traceable
Temporal
Normative
Deterministic where possible


BRIR IS NOT

Rego
OPA IR
Python
SQL
LLM prompt
LegalRuleML XML


INITIAL TARGET

BRIR
  ↓
Rego v1
  ↓
Signed OPA Bundle
  ↓
OPA


SEMANTICS

TRUE
FALSE
UNKNOWN
ERROR

not merely Boolean.


RULE RESULTS

APPLIES
DOES_NOT_APPLY
DEFEATED
EXEMPTED
INDETERMINATE
ERROR


NORMATIVE EFFECTS

OBLIGATION
PROHIBITION
PERMISSION
RIGHT
POWER
REPARATION
...


OPEN WORLD

Missing fact
≠
False fact.


DEFEASIBILITY

Explicit override graph.

No arbitrary
priority numbers.


DISCRETION

Human / authority
decision required.

Do not invent thresholds.


OPA

Execution provider,
not canonical law.


OPA ERRORS

Must not silently
collapse into false.


OPA WASM

Allowed only after
semantic equivalence
testing for consequential use.


BUNDLES

Versioned
Tested
Signed for high assurance
Auditable


ALTERNATIVE TARGETS

CEL
DMN
future native evaluator


INTEROPERABILITY

LegalRuleML


STRATEGIC RESULT

Change execution provider
without changing
regulatory meaning.
```
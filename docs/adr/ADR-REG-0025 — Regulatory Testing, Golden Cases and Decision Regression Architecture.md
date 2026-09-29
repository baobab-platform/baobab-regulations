# ADR-REG-0025 — Regulatory Testing, Golden Cases and Decision Regression Architecture

**Subtitle:** Regulatory Test Oracles, Golden Cases, BRIR Conformance, Differential Evaluation, Property-Based Testing, Mutation Testing, Historical Replay and Jurisdiction-Pack Certification

**Status:** Proposed — Foundational Regulatory Assurance Architecture  
**Decision ID:** `ADR-REG-0025`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Cross-Repository Contract Targets:** `baobab-platform/shared` and affected consumer repositories  
**Date:** 2026-09-29  
**Decision Type:** Testing / TEVV / Golden Cases / Regression / Conformance / Certification / Quality Assurance  
**Strategic Classification:** Core Regulatory Assurance Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL implement a layered regulatory assurance architecture capable of proving that:

```text
Authoritative Source
        │
        ▼
Verified Interpretation
        │
        ▼
RegulatoryRuleVersion
        │
        ▼
BRIR
        │
        ▼
Compiled Policy
        │
        ▼
OPA / Evaluator
        │
        ▼
Assessment
        │
        ▼
RegulatoryDecision
```

preserves the intended regulatory semantics at every transformation boundary.

Testing SHALL therefore cover:

```text
source processing

normalisation

canonical domain semantics

temporal semantics

applicability

rule representation

BRIR compilation

OPA execution

DecisionPolicy

explanations

historical replay

distributed execution packages

change detection

events/contracts

tenant isolation

performance

failure behaviour.
```

The governing principle is:

> **Baobab SHALL test regulatory meaning, not merely software execution.**

---

# 2. Fundamental Assurance Doctrine

The following distinctions SHALL remain explicit:

```text
CODE COMPILES
≠
RULE IS CORRECT

TEST PASSES
≠
LEGAL INTERPRETATION IS CORRECT

LINE COVERAGE
≠
REGULATORY SEMANTIC COVERAGE

GOLDEN CASE
≠
ARBITRARY FIXTURE

MODEL BENCHMARK
≠
RULE CERTIFICATION

BRIR VALID
≠
BRIR SEMANTICALLY CORRECT

OPA TEST PASSES
≠
LAW CORRECTLY REPRESENTED

SAME RESULT
≠
SAME REASON

HISTORICAL REPLAY
≠
CURRENT REASSESSMENT

PERFORMANCE TEST
≠
CORRECTNESS TEST.
```

---

# 3. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0003 — Regulatory Authority and Interpretation Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy`
- `ADR-REG-0008 — Instrument, Provision, Rule, Obligation and Requirement`
- `ADR-REG-0009 — Normative Semantics and Defeasible Reasoning`
- `ADR-REG-0010 — Regulatory Knowledge Graph`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0017 — Regulatory Context and Applicability Resolution`
- `ADR-REG-0018 — Regulatory Decision and Evaluation Engine`
- `ADR-REG-0019 — PDP and PEP Separation`
- `ADR-REG-0020 — Decision Explainability, Replay and Reproducibility`
- `ADR-REG-0021 — AI-Assisted Regulatory Extraction and Interpretation Boundary`
- `ADR-REG-0022 — Human Verification and Regulatory Knowledge Governance`
- `ADR-REG-0023 — Regulatory Change Detection and Impact Analysis`
- `ADR-REG-0024 — Regulatory Events, Subscriptions and Notifications`

---

# 4. Research Finding — OPA Provides Useful Policy Testing Primitives

OPA provides first-class policy testing through:

```text
opa test
```

including:

```text
test discovery

input/data substitution

failure reporting

coverage

coverage thresholds

test filtering

parallel execution

benchmark execution

Rego and Wasm targets.
```

OPA also provides `--fail-on-empty`, preventing a CI pipeline from silently succeeding when no test actually ran.

Baobab SHALL use these capabilities for compiled Rego verification.

They are not sufficient alone.

---

# 5. OPA Coverage Is Useful but Limited

OPA can report policy-line coverage and can fail when coverage falls below a configured threshold. Its coverage reports can additionally distinguish code skipped because of indexing or early-exit optimisation.

This is valuable implementation evidence.

However:

> **A policy can achieve high Rego coverage while still failing to test the legally decisive scenario.**

---

# 6. Example

Tests may exercise:

```text
rule applies

rule does not apply
```

and reach nearly every Rego line.

But never test:

```text
exception triggered exactly
on threshold boundary.
```

The suite is legally incomplete despite strong code coverage.

---

# 7. Therefore Two Coverage Families Are Required

Baobab SHALL distinguish:

```text
IMPLEMENTATION COVERAGE
```

from:

```text
REGULATORY SEMANTIC COVERAGE.
```

---

# 8. Implementation Coverage

Examples:

```text
Python statement/branch coverage

Go coverage

Rego line coverage

API route coverage

compiler branch coverage.
```

---

# 9. Regulatory Semantic Coverage

Examples:

```text
obligation exercised

prohibition exercised

permission exercised

exception exercised

exemption exercised

unknown fact exercised

conflict exercised

hierarchy exercised

deadline boundary exercised

effective-date boundary exercised

retroactive case exercised

future-effective case exercised

not-applicable case exercised.
```

---

# 10. Research Finding — OPA Strict Checking Should Be Part of the Gate

OPA recommends:

```text
opa check --strict
```

as part of policy build pipelines, while the Regal tooling complements OPA compiler checks with additional policy linting.

Baobab SHALL apply both classes of checks to generated or maintained Rego.

---

# 11. Rego v1

OPA v1 syntax and associated compiler restrictions SHALL be the baseline for new Baobab-generated Rego unless a separately governed compatibility requirement exists.

OPA's v1 architecture makes many previously optional strictness rules the normal language behaviour.

---

# 12. Rego Lint/Compilation Is Not Legal Validation

A syntactically perfect policy may encode:

```text
amount < 100
```

where law actually requires:

```text
amount <= 100.
```

Compiler success cannot detect that legal-semantic defect.

---

# 13. Research Finding — Property-Based Testing Expands Input Exploration

Hypothesis supports generation of test data beyond manually selected examples and can shrink failing generated inputs into smaller reproductions. It also supports stateful testing in which sequences of operations are generated and explored automatically.

Baobab SHOULD use property-based testing for regulatory invariants where appropriate.

---

# 14. Research Finding — Metamorphic Testing Addresses Oracle Limits

NIST research describes metamorphic testing as useful when obtaining a complete expected-output oracle is difficult or impractical. Rather than asserting an exact answer for every generated input, metamorphic relations define how results should or should not change when inputs are transformed.

This technique is highly relevant to regulatory rule systems.

---

# 15. Research Finding — Mutation Testing Probes Test Adequacy

Mutation testing deliberately introduces defects such as:

```text
boundary changes

negated conditions

changed constants

changed return values
```

and observes whether the test suite detects them. Mature mutation frameworks use exactly these kinds of operators to expose weak test suites.

Baobab SHALL adopt this **principle** but implement regulatory-domain mutations appropriate to BRIR and regulatory semantics.

---

# 16. PIT Is Not the Baobab Mutation Engine

PIT is Java-oriented.

It is cited here as evidence for the testing technique.

Baobab SHOULD build BRIR-aware semantic mutation tooling rather than adopting PIT for regulatory rule representation.

---

# 17. Research Finding — TEVV Must Evaluate the System, Not Merely a Model

NIST's current TEVV-Athlon work, published as an **initial public draft** in August 2026, proposes an extensible Testing, Evaluation, Verification and Validation framework applicable across ML, generative and agentic systems and emphasises assessment in real intended-use contexts.

Because the document remains a draft as of September 2026, Baobab SHALL treat it as useful research guidance rather than a final normative standard.

---

# 18. Regulatory Testing Is a System Property

Baobab therefore tests the chain:

```text
Source
   ↓
Docling
   ↓
Normalisation
   ↓
Haystack / candidate generation
   ↓
Human verification
   ↓
RuleVersion
   ↓
BRIR
   ↓
Compiler
   ↓
OPA
   ↓
Decision Engine
   ↓
PEP
```

rather than evaluating any component in isolation.

---

# 19. Regulatory Test Taxonomy

Baobab SHALL adopt layered test classes.

Initial levels:

```text
RT0 — Source and Document Fidelity

RT1 — Canonical Domain Validation

RT2 — Regulatory Semantic Unit Tests

RT3 — BRIR Conformance Tests

RT4 — Target Evaluator Differential Tests

RT5 — Jurisdiction/Profile Golden Tests

RT6 — Historical Decision Regression

RT7 — Distributed Runtime and Integration Tests

RT8 — Shadow / Canary Production Validation

RT9 — Operational Resilience and Failure Tests.
```

---

# 20. RT0 — Source and Document Fidelity

Tests:

```text
document parsing

page structure

tables

sections

citations

OCR

normalisation

source offsets.
```

---

# 21. RT0 Example

Official tariff PDF contains:

```text
0901 | Coffee | 10%
```

Test verifies:

```text
HS = 0901

description = Coffee

rate = 10%

correct row/page provenance retained.
```

---

# 22. RT0 Does Not Decide Legal Applicability

It establishes source representation fidelity.

---

# 23. RT1 — Canonical Domain Validation

Tests:

```text
domain invariants

identifiers

versioning

temporal intervals

typed relationships

tenant isolation

provenance completeness.
```

---

# 24. Examples

Reject:

```text
RuleVersion with no interpretation provenance

legal interval with invalid bounds

tenant-private interpretation assigned globally

ProvisionVersion linked to unknown Instrument.
```

---

# 25. RT2 — Regulatory Semantic Unit Tests

Tests specific semantic functions such as:

```text
conditions

exceptions

effects

requirements

deadlines

calculations

classifications

conflict resolution

unknown propagation.
```

---

# 26. RT3 — BRIR Conformance

Verifies that:

```text
RegulatoryRuleVersion semantics
```

have been correctly represented in:

```text
BRIR.
```

---

# 27. RT4 — Evaluator Differential Testing

Verifies that:

```text
BRIR Reference Evaluator
```

and:

```text
OPA compiled target
```

produce semantically equivalent outcomes.

---

# 28. RT5 — Jurisdiction/Profile Golden Tests

Exercises complete legal profiles such as:

```text
ZA import readiness

UG export readiness

UG → ZA coffee trade

SPS

tariff

rules of origin.
```

---

# 29. RT6 — Historical Decision Regression

Replays prior validated decisions against unchanged semantics to detect regressions introduced by:

```text
compiler changes

OPA upgrades

BRIR changes

DecisionPolicy changes

context resolver changes.
```

---

# 30. RT7 — Distributed Runtime Integration

Tests:

```text
RegulatoryExecutionPackage

signature validation

bundle deployment

central/local equivalence

PEP interaction

receipts

staleness

reconciliation.
```

---

# 31. RT8 — Shadow / Canary

Executes candidate new regulatory versions against real or production-representative traffic without initially affecting authoritative enforcement.

---

# 32. RT9 — Resilience

Tests:

```text
missing bundle

stale bundle

OPA unavailable

Regulations unavailable

Control Plane unavailable

clock skew

network partition

outbox failure

model plane unavailable.
```

---

# 33. Golden Cases

Baobab SHALL make:

# `RegulatoryGoldenCase`

a first-class assurance object.

---

# 34. Golden Case Definition

A Regulatory Golden Case is:

> **A independently verified regulatory scenario with explicitly defined source basis, context, evidence, temporal perspective and expected semantic outcome.**

---

# 35. Golden Case Is More Than Fixture JSON

It SHALL include why the expected answer is considered correct.

---

# 36. RegulatoryGoldenCase

Conceptually:

```text
RegulatoryGoldenCase
├── golden_case_id
├── version
├── title
├── jurisdiction_scope[]
├── regulatory_profile
├── question
├── legal_time
├── knowledge_time
├── context
├── facts
├── evidence_state
├── source_refs[]
├── interpretation_refs[]
├── expected_applicability[]
├── expected_effects[]
├── expected_requirements[]
├── expected_unknowns[]
├── expected_conflicts[]
├── expected_outcome
├── expected_effect_class?
├── expected_reason_codes[]
├── oracle_basis
├── verification_refs[]
├── status
└── provenance
```

---

# 37. Golden Case Versioning

Golden cases SHALL be immutable once approved.

Change creates:

```text
GoldenCase v2
```

rather than rewriting:

```text
v1.
```

---

# 38. Golden Case States

Potential:

```text
DRAFT

UNDER_REVIEW

VERIFIED

APPROVED

DEPRECATED

RETIRED.
```

---

# 39. Golden Case Oracle Basis

Initial values MAY include:

```text
DIRECT_STATUTORY_TEXT

OFFICIAL_DECISION

OFFICIAL_GUIDANCE

VERIFIED_BAOBAB_INTERPRETATION

QUALIFIED_LEGAL_REVIEW

AUTHORITATIVE_DATASET

HISTORICAL_CONFIRMED_DECISION.
```

---

# 40. Independent Oracle Principle

A golden case SHALL NOT be considered independently verified merely because:

```text
the same model
```

that generated a candidate rule also generated:

```text
the expected test result.
```

---

# 41. Circular Testing Is Prohibited

Rejected:

```text
LLM writes BRIR
      ↓
same LLM writes expected result
      ↓
tests pass.
```

---

# 42. Why

That only demonstrates internal consistency between two outputs of the same potentially incorrect interpretation.

---

# 43. Independent Oracle

For consequential golden cases, expected semantics SHOULD be established through:

```text
verified source analysis

qualified reviewer

maker-checker where required.
```

---

# 44. Golden Case Categories

The corpus SHALL deliberately contain multiple categories.

---

# 45. Positive Case

Rule applies and requirement is satisfied.

---

# 46. Negative Case

Rule does not apply or requirement is not satisfied.

---

# 47. Boundary Case

Examples:

```text
amount = exactly threshold

date = exact commencement date

age = exact legal boundary

quantity = quota limit.
```

---

# 48. Exception Case

General rule applies but:

```text
exception

exemption

waiver

derogation
```

changes the outcome.

---

# 49. Unknown Case

A required fact is missing.

Expected result SHOULD often be:

```text
INDETERMINATE
```

rather than silently false or allowed.

---

# 50. Error Case

Invalid calculation or malformed context.

Expected:

```text
evaluation error / indeterminate
```

not invented legal outcome.

---

# 51. Not-Applicable Case

Demonstrates sufficient coverage but rule/profile does not apply.

---

# 52. Incomplete-Coverage Case

Demonstrates:

```text
coverage gap
→ INDETERMINATE
```

rather than false assurance.

---

# 53. Conflict Case

Two rules appear inconsistent.

Case specifies:

```text
resolved hierarchy
```

or:

```text
REVIEW_REQUIRED.
```

---

# 54. Cumulative Case

Two obligations both apply.

Tests ensure one does not incorrectly defeat the other.

---

# 55. Temporal Case

Rule applicability differs before and after:

```text
commencement

expiry

suspension

revival.
```

---

# 56. Retroactive Case

Tests law with legal effect predating publication/discovery.

---

# 57. Future-Effective Case

Tests planned future transaction.

---

# 58. Amendment Case

Tests previous and successor RuleVersions.

---

# 59. Classification Case

Different HS classification changes applicable rule.

---

# 60. Evidence Case

Same regulation/context but different evidence state changes requirement satisfaction.

---

# 61. Discretion Case

Expected:

```text
AUTHORITY_DETERMINATION_REQUIRED
```

rather than deterministic Boolean.

---

# 62. Human-Judgment Case

Expected:

```text
HUMAN_JUDGMENT_REQUIRED.
```

---

# 63. Role Case

Exporter/importer/broker or other legal role changes applicability.

---

# 64. Jurisdiction Case

Same activity under different jurisdiction context produces different applicable RuleSet.

---

# 65. Regime Case

Trade-regime membership changes result.

---

# 66. Semantic Coverage Matrix

Each jurisdiction pack SHALL maintain a:

# `RegulatorySemanticCoverageMatrix`

---

# 67. Coverage Dimensions

Potential dimensions:

```text
normative modality

conditions

exceptions

thresholds

temporal operators

jurisdiction roles

actor roles

classifications

requirements

evidence states

conflicts

outcomes

effect classes.
```

---

# 68. Example

A profile containing explicit exceptions SHALL not be certified if:

```text
exception coverage = none.
```

even if Rego line coverage is 100%.

---

# 69. Branch Coverage

Implementation branch coverage remains useful.

But it supplements, rather than replaces:

```text
semantic scenario coverage.
```

---

# 70. Expected Outcome Is Not Enough

Golden cases SHOULD verify intermediate semantics.

---

# 71. Example

Both of these may return:

```text
UNSATISFIED.
```

Case A:

```text
permit missing.
```

Case B:

```text
certificate expired.
```

A suite checking only final outcome could miss swapped or incorrect reasons.

---

# 72. Therefore Golden Cases MAY Assert

```text
applicable rules

effects

requirements

evidence assessments

reason codes

final outcome.
```

---

# 73. Do Not Over-Specify Implementation

Golden cases SHOULD NOT generally assert:

```text
exact Rego rule name

internal loop count

database query plan
```

unless those are the subject of the test.

---

# 74. Golden Case Storage

Canonical golden-case metadata SHOULD live in Regulations-owned persistence and/or version-controlled assurance artefacts with deterministic linkage.

---

# 75. Human-Readable Form

Each case SHOULD have a reviewable representation.

Potential:

```text
YAML

JSON

structured Markdown projection.
```

---

# 76. Machine-Readable Form

Tests SHALL consume a canonical structured schema.

---

# 77. Golden Cases in Git

Approved non-sensitive golden fixtures SHOULD be version-controlled.

---

# 78. Sensitive Cases

Tenant-private or privileged cases SHALL NOT be committed to public/shared fixtures.

---

# 79. Synthetic Cases

Synthetic cases are valuable.

They SHALL be marked:

```text
SYNTHETIC.
```

---

# 80. Real Source Cases

Where a case derives from actual authoritative law:

```text
source provenance
```

must remain attached.

---

# 81. Test Data Rights

ADR-REG-0012 applies.

A licence prohibiting redistribution may prevent storing full source text inside a repository fixture.

---

# 82. Rights-Safe Fixture

May use:

```text
source canonical ID

permitted excerpt

hash

structured expected semantics.
```

---

# 83. BRIR Reference Evaluator

Baobab SHALL maintain a:

# `BRIR Reference Evaluator`

for semantic conformance testing.

---

# 84. Purpose

It serves as:

```text
reference executable semantics

compiler oracle

cross-runtime comparison target

historical semantic replay mechanism.
```

---

# 85. Reference Evaluator Is Not Necessarily Production Runtime

It MAY prioritise:

```text
clarity

determinism

correctness

traceability
```

over maximum performance.

---

# 86. Compiler Pipeline

```text
RuleVersion
    │
    ▼
BRIR
    │
    ├─────────────► Reference Evaluator
    │
    ▼
Compiler
    │
    ▼
Rego
    │
    ▼
OPA
```

---

# 87. Differential Assertion

For same:

```text
BRIR

context

facts

evidence

DecisionPolicy
```

expected:

```text
Reference Evaluator
=
OPA target
```

at semantic output level.

---

# 88. Semantic Output Comparison

Compare:

```text
applicability

effects

requirements

unknowns

violations

outcome

reason codes.
```

---

# 89. Exact JSON Equality Not Required

Provider-specific metadata may differ.

---

# 90. Semantic Equivalence Required

Example:

```text
OPA trace ID
```

may differ.

Outcome semantics may not.

---

# 91. Compiler Regression

If:

```text
BRIR unchanged
```

but compiler upgrade changes outcome:

```text
COMPILER_SEMANTIC_REGRESSION.
```

---

# 92. OPA Upgrade Regression

If compiler artifact unchanged but new OPA runtime changes deterministic output unexpectedly:

```text
EVALUATOR_CONFORMANCE_FAILURE.
```

---

# 93. Multiple Execution Targets

Where ADR-REG-0016 supports:

```text
Rego

Wasm

future evaluator
```

all production-authorised targets SHALL pass equivalent conformance suites.

---

# 94. OPA Test Targets

Current OPA tooling can run tests targeting:

```text
rego

wasm.
```

This SHOULD be used when Baobab supports both targets.

---

# 95. OPA Unit Tests

Generated Rego SHALL include or accompany tests for:

```text
positive cases

negative cases

unknown handling

exceptions

boundaries.
```

---

# 96. OPA CI Minimum

Production-generated policy CI SHOULD include:

```text
opa check --strict

regal lint

opa test --fail-on-empty

opa test --coverage

configured coverage threshold.
```

OPA directly supports strict checking, coverage thresholds and failure on an empty test run.

---

# 97. Coverage Threshold Is Engineering Policy

This ADR SHALL NOT establish one universal percentage.

---

# 98. Why

A profile with:

```text
95% coverage
```

may still miss a critical exception.

A small deterministic rule may legitimately achieve:

```text
100%.
```

---

# 99. Coverage Thresholds SHALL Be Profile-Specific

But uncovered consequential rules SHALL normally block promotion.

---

# 100. Property-Based Testing

Baobab SHOULD use a property-based framework such as Hypothesis for Python-side regulatory semantic testing where technically appropriate.

---

# 101. Generated Contexts

Strategies MAY generate:

```text
dates

quantities

jurisdictions

actor roles

classification codes

permit states

evidence validity

trade lanes.
```

---

# 102. Example Property — Irrelevant Fact Invariance

Given decision:

```text
D
```

adding a context fact that no applicable rule references SHOULD NOT change regulatory outcome.

---

# 103. Example Property — Evidence Independence

Adding unrelated evidence SHOULD NOT satisfy an unrelated requirement.

---

# 104. Example Property — Temporal Monotonicity Is Not Universal

Baobab SHALL NOT assume:

```text
later time
→ stricter result.
```

Regulations can expire or relax.

Therefore properties must be domain-valid, not intuitive guesses.

---

# 105. Example Property — Pre-Commencement

If:

```text
legal_time < valid_from
```

a rule SHALL NOT be considered legally effective unless another temporal rule explicitly gives retroactive effect.

---

# 106. Example Property — Post-Expiry

If:

```text
legal_time > valid_to
```

expired rule SHALL not apply unless legal semantics preserve effect for the specific situation.

---

# 107. Example Property — Unknown Propagation

If a condition requires material fact F and F is:

```text
UNKNOWN
```

evaluation SHALL NOT silently coerce it to:

```text
FALSE
```

or:

```text
TRUE
```

unless BRIR semantics explicitly specify that treatment.

---

# 108. Example Property — Tenant Isolation

Changing:

```text
tenant T1
→ tenant T2
```

SHALL never leak T1 private regulatory overlay into T2.

---

# 109. Stateful Property Testing

Hypothesis stateful testing can generate sequences of actions rather than only static input values.

This is valuable for:

```text
publish RuleVersion

supersede

suspend

resume

reassess

distribute bundle

revoke bundle.
```

---

# 110. Example Stateful Property

Sequence:

```text
R1 published
→ R2 future published
→ legal time advances
→ R2 active
→ R1 retained historically.
```

Invariant:

```text
historical R1 decisions remain replayable.
```

---

# 111. Shrinking

Hypothesis can shrink generated failures into smaller examples.

This is particularly useful when a failure arises only under a complex combination such as:

```text
jurisdiction = ZA

quantity = threshold

permit = expired

exception = active

legal time = commencement instant.
```

---

# 112. Metamorphic Testing

Baobab SHALL define regulatory metamorphic relations where exact expected output across all generated cases would otherwise be expensive.

NIST research specifically identifies metamorphic testing as one response to the test-oracle problem.

---

# 113. Metamorphic Relation — Irrelevant Context

If context property X is irrelevant to every rule contributing to D:

```text
change X
```

SHOULD NOT change D.

---

# 114. Metamorphic Relation — Equivalent Identifier

Replacing an external source identifier with its verified canonical-equivalent identity SHOULD NOT change normative result.

---

# 115. Metamorphic Relation — Evidence Ordering

Reordering an evidence collection SHALL NOT change outcome.

---

# 116. Metamorphic Relation — Duplicate Evidence

Adding an exact duplicate evidence reference SHALL NOT double-count compliance.

---

# 117. Metamorphic Relation — Presentation Language

Changing explanation language SHALL NOT change:

```text
outcome

requirements

rule identity.
```

---

# 118. Metamorphic Relation — Retrieval Independence

Once RuleVersion is published:

```text
Qdrant index ordering
```

SHALL NOT change deterministic regulatory decision.

---

# 119. Metamorphic Relation — Model Independence

Changing configured LLM provider SHALL NOT alter existing verified RuleVersion execution.

---

# 120. Metamorphic Relation — Event Delivery Duplication

Delivering the same:

```text
source + event.id
```

twice SHALL NOT produce duplicate business effect.

---

# 121. Mutation Testing

Baobab SHOULD build:

# `RegulatorySemanticMutator`

against BRIR and related regulatory structures.

---

# 122. Purpose

To answer:

> **Would our tests actually catch a plausible regulatory implementation defect?**

---

# 123. Mutation Families

Initial mutations SHOULD include:

```text
boundary operator mutation

normative modality mutation

exception removal

condition removal

actor-role mutation

jurisdiction mutation

effective-date mutation

threshold mutation

requirement mutation

unknown-semantics mutation

hierarchy override mutation

unit/currency mutation.
```

---

# 124. Boundary Mutation

Example:

```text
<=
```

mutated to:

```text
<
```

Mutation-testing tools commonly use analogous conditional-boundary changes specifically because boundary bugs are difficult to catch with weak test suites.

---

# 125. Normative Modality Mutation

```text
OBLIGATION
→
PERMISSION
```

or:

```text
PROHIBITION
→
OBLIGATION.
```

Golden semantic cases SHOULD kill this mutant.

---

# 126. Exception Removal Mutation

Original:

```text
prohibited unless Permit P.
```

Mutant:

```text
prohibited.
```

Exception golden case MUST fail the mutant.

---

# 127. Condition Removal

Original:

```text
applies when quantity > 100.
```

Mutant:

```text
applies unconditionally.
```

---

# 128. Threshold Mutation

```text
100
→
101.
```

Boundary cases should detect.

---

# 129. Effective-Date Mutation

```text
1 Jan
→
2 Jan.
```

Temporal cases should detect.

---

# 130. Jurisdiction Mutation

```text
ZA
→
UG.
```

Jurisdiction cases should detect.

---

# 131. Role Mutation

```text
IMPORTER
→
EXPORTER.
```

Role cases should detect.

---

# 132. Unknown-Semantics Mutation

```text
UNKNOWN
→ FALSE.
```

Indeterminate tests should detect.

---

# 133. Override Mutation

Remove:

```text
specific exception overrides general rule.
```

Conflict/defeasibility golden cases should detect.

---

# 134. Requirement Satisfaction Mutation

```text
EXPIRED evidence
```

mutated to:

```text
VALID.
```

Evidence tests should detect.

---

# 135. Surviving Mutant

A mutation that passes all tests is:

```text
SURVIVED.
```

---

# 136. Surviving Mutant Means One of Several Things

Potentially:

```text
test gap

equivalent mutation

unreachable semantics

intentional irrelevance.
```

It requires analysis.

---

# 137. Mutation Score Is Not Legal Assurance

Baobab SHALL NOT state:

```text
95% mutations killed
therefore rule is 95% legally correct.
```

---

# 138. Mutation Testing Is Test-Suite Adequacy Evidence

Nothing more.

---

# 139. High-Consequence Mutation Policy

E4-capable rule sets SHOULD have no unexplained surviving **material regulatory-semantic mutations** within the defined mutation set.

---

# 140. Historical Decision Regression

Production or production-derived decisions SHALL become a powerful regression corpus where privacy, rights and governance permit.

---

# 141. HistoricalRegressionCase

Conceptually:

```text
HistoricalRegressionCase
├── source_decision_ref
├── input_snapshot_ref
├── ruleset_fingerprint
├── decision_policy_version
├── expected_semantics
├── permitted_variance?
├── data_classification
└── provenance
```

---

# 142. Expected Regression Rule

If:

```text
legal semantics unchanged
```

then after infrastructure/compiler/evaluator upgrade:

```text
historical semantic result
```

SHOULD remain equivalent.

---

# 143. Unexpected Difference

Produces:

```text
DECISION_REGRESSION.
```

---

# 144. DecisionDiff

ADR-REG-0020 SHALL be used to explain any regression.

---

# 145. Expected Legal Change

If test run intentionally uses:

```text
new RuleVersion
```

after law changed, outcome difference may be expected.

---

# 146. Baseline Must Not Be Updated Blindly

Rejected:

```text
tests failed after change
→ regenerate snapshots
→ commit.
```

---

# 147. Golden Baseline Change

Requires:

```text
identified legal/semantic cause

reviewed expected difference

updated provenance

new golden-case version.
```

---

# 148. Snapshot Testing Caution

Generic output snapshots MAY be used for convenience.

They SHALL NOT be the primary oracle for consequential regulation.

---

# 149. Why

Large JSON snapshots can hide semantic changes inside noise.

---

# 150. Structured Assertion Preferred

Assert:

```text
outcome changed from SATISFIED to UNSATISFIED
because Permit P became required.
```

rather than merely approving a 2,000-line snapshot diff.

---

# 151. Regression Corpus Selection

Historical corpus SHOULD include:

```text
common scenarios

rare outcomes

critical prohibitions

exceptions

high-value transactions

previous incidents

boundary cases.
```

---

# 152. Privacy-Safe Regression

Where production data is sensitive:

```text
pseudonymise

minimise

synthesise equivalent context
```

where this does not alter material legal semantics.

---

# 153. Jurisdiction Pack Certification

Each published jurisdiction/regulatory profile SHALL have an associated:

# `RegulatoryPackCertification`

---

# 154. RegulatoryPackCertification

Conceptually:

```text
RegulatoryPackCertification
├── certification_id
├── pack_ref
├── pack_version
├── source_manifest_ref
├── coverage_manifest_ref
├── golden_case_suite_ref
├── semantic_coverage_ref
├── brir_conformance_ref
├── evaluator_conformance_ref
├── regression_suite_ref
├── performance_evidence_ref
├── security_evidence_ref
├── governance_review_refs[]
├── maximum_effect_class
├── certification_state
├── certified_at
└── provenance
```

---

# 155. Pack Certification Is Not Legal Certification by Government

It means:

> **Baobab has verified that this pack meets Baobab's declared technical/regulatory assurance standard.**

---

# 156. Do Not Say Government Certified

Unless the actual competent authority has done so.

---

# 157. Certification States

Potential:

```text
DRAFT

TESTING

ADVISORY_READY

REVIEW_GATE_READY

CONDITIONAL_ENFORCEMENT_READY

HARD_ENFORCEMENT_READY

SUSPENDED

REVALIDATION_REQUIRED

RETIRED.
```

---

# 158. Effect Class Mapping

Conceptually:

```text
ADVISORY_READY
→ E0/E1

REVIEW_GATE_READY
→ up to E2

CONDITIONAL_ENFORCEMENT_READY
→ up to E3

HARD_ENFORCEMENT_READY
→ eligible for E4
```

subject to runtime decision controls.

---

# 159. Certification Does Not Guarantee Every Future Decision

It establishes profile readiness under current verified knowledge and test evidence.

---

# 160. Pack Coverage Manifest

SHALL state:

```text
included regulatory domains

excluded domains

jurisdictions

activities

products/classifications

legal-time coverage

known gaps.
```

---

# 161. Unknown Coverage Must Be Visible

A pack SHALL NOT become E4-ready where a material required regulatory domain is explicitly unknown.

---

# 162. Certification Requires Golden Corpus

No consequential jurisdiction pack without:

```text
verified golden cases.
```

---

# 163. E3 Pack Requirements

At minimum SHOULD include:

```text
positive

negative

exception

boundary

unknown

temporal

not-applicable

evidence-state cases.
```

---

# 164. E4 Pack Requirements

SHOULD additionally demonstrate:

```text
legal conflicts where relevant

historical replay

semantic mutation adequacy

runtime differential tests

failure behaviour

change rollout/shadow testing.
```

---

# 165. Certification Renewal

Required after material:

```text
law change

interpretation change

BRIR version change

compiler semantic change

DecisionPolicy change

critical defect.
```

---

# 166. Not Every Code Change Requires Full Pack Recertification

Impact-based testing applies.

---

# 167. Test Impact Analysis

Change graph from ADR-REG-0023 SHOULD identify which:

```text
golden cases

rule tests

jurisdiction packs

historical regression cases
```

are affected.

---

# 168. Selective Testing

PR CI MAY run:

```text
affected tests
+
mandatory foundation tests.
```

---

# 169. Release Certification Still Runs Broader Suite

Optimised developer feedback SHALL NOT eliminate comprehensive release assurance.

---

# 170. Change-to-Test Traceability

Each RuleVersion SHOULD know relevant:

```text
golden cases

unit tests

semantic properties

mutation families.
```

---

# 171. Requirement-to-Test Traceability

Consequential Requirement types SHOULD have tested states such as:

```text
present

absent

expired

revoked

wrong scope

unknown.
```

---

# 172. CI Architecture

Testing SHALL be staged.

---

# 173. PR Gate — Fast

Typical:

```text
format

lint

type/schema checks

domain unit tests

selected golden cases

BRIR compile

OPA strict check

OPA unit tests

contract tests.
```

---

# 174. Main Integration Gate

Adds:

```text
PostgreSQL integration

API tests

Haystack/Docling adapter tests

OPA server integration

event/outbox tests

cross-module golden suite.
```

---

# 175. Extended Assurance Gate

May run:

```text
full golden corpus

property-based tests

stateful tests

semantic mutations

historical replay corpus

performance regression.
```

This MAY run on scheduled or release workflows where cost makes it unsuitable for every commit.

---

# 176. Release Candidate Gate

Runs:

```text
jurisdiction-pack certification

evaluator differential matrix

historical regression

security/resilience

bundle signing

runtime compatibility

shadow preparation.
```

---

# 177. Production Promotion Gate

Uses:

```text
SHADOW

decision comparison

CANARY

runtime reconciliation.
```

---

# 178. No Test Bypass for E3/E4 Hotfix

Emergency governance MAY reduce turnaround time.

It SHALL not eliminate the minimum applicable:

```text
golden

conformance

regression
```

tests.

---

# 179. OPA Benchmarking

OPA provides:

```text
opa bench

opa test --bench
```

and profiling facilities for measuring evaluation performance.

Baobab SHALL include performance regression testing for consequential rules.

---

# 180. Why

A legally correct policy taking:

```text
15 seconds
```

per transaction may still be operationally unusable.

---

# 181. Performance Metrics

At minimum track where relevant:

```text
evaluation latency p50

p95

p99

compilation latency

bundle activation latency

memory usage

allocations

package size

startup time.
```

---

# 182. Benchmark Actual Packages

OPA documentation explicitly recommends measuring realistic policy/data sizes because evaluation and memory behaviour depend upon loaded policy and data.

---

# 183. Benchmark Modes

Tests SHOULD distinguish:

```text
warm local evaluator

central API

distributed sidecar

cold startup

bundle activation.
```

---

# 184. Performance Thresholds

SHALL be defined by deployment/profile.

No universal latency number is declared in this ADR.

---

# 185. Performance Regression

Same semantic output but substantial unexpected performance degradation:

```text
PERFORMANCE_REGRESSION.
```

---

# 186. Performance Optimisation Requires Semantic Re-Test

Changing Rego for performance may change semantics.

Full affected semantic suite reruns.

---

# 187. AI Knowledge-Plane Testing

ADR-REG-0021/0022 TEVV remains separate from deterministic rule testing.

---

# 188. AI Evaluation Corpus

Tests:

```text
provision segmentation

citation extraction

definition extraction

amendment detection

exception extraction

temporal extraction

candidate rule generation.
```

---

# 189. AI Metrics

Examples:

```text
precision

recall

critical miss rate

citation hallucination rate

exception recall

human correction rate.
```

---

# 190. Strong AI Performance Does Not Certify BRIR Automatically

The candidate still passes:

```text
human governance

canonical promotion

BRIR conformance

golden tests.
```

---

# 191. End-to-End Golden Pipeline Test

A selected fixture MAY exercise:

```text
SourceArtefact
      ↓
Docling
      ↓
normalisation
      ↓
candidate extraction
      ↓
verified fixture
      ↓
RuleVersion
      ↓
BRIR
      ↓
OPA
      ↓
Decision.
```

---

# 192. AI Nondeterminism

AI stages SHALL NOT make deterministic release tests flaky.

---

# 193. Strategy

For deterministic core CI:

```text
pin verified candidate fixtures.
```

Separate AI TEVV evaluates live model behaviour.

---

# 194. Model Call Is Not Required in Every Golden Decision Test

Once interpretation is verified:

```text
RuleVersion
```

is the test starting point for deterministic execution assurance.

---

# 195. Security Tests

Assurance SHALL include:

```text
tenant isolation

authorization

prompt injection boundaries

rule-package integrity

bundle signature

tampered artifact

privileged data exposure.
```

---

# 196. PEP Bypass Test

Attempt:

```text
consumer bypasses Regulations
and calls unapproved OPA policy.
```

Architecture must reject/prevent where governed topology requires.

---

# 197. Tenant Overlay Test

T1 private rule SHALL NOT affect T2.

---

# 198. Signed Bundle Test

Modify one byte.

Expected:

```text
bundle rejected.
```

---

# 199. Stale Bundle Test

OPA remains healthy but old RuleSet is active.

Expected:

```text
runtime STALE / NOT_READY
```

according to ADR-REG-0019.

---

# 200. Failure-Injection Tests

Simulate:

```text
PostgreSQL unavailable

OPA unavailable

Qdrant unavailable

Haystack unavailable

LLM unavailable

LangGraph unavailable

Control Plane unavailable

event broker unavailable.
```

---

# 201. Deterministic Fast Path Independence

Existing verified E3/E4 decision execution SHOULD continue appropriately when:

```text
Haystack

Qdrant

LLM
```

are unavailable.

---

# 202. This SHALL Be Tested

Not merely assumed.

---

# 203. AI Plane Failure

Expected:

```text
knowledge-production degraded.
```

Not:

```text
verified rules vanish.
```

---

# 204. Control Plane Failure

Consequential evaluation without valid current/cached context assertion:

```text
shall not guess context.
```

---

# 205. Event Testing

ADR-REG-0024 requires tests for:

```text
transactional outbox

duplicates

ordering

replay

tenant filtering

webhook integrity.
```

These become part of RT7.

---

# 206. Contract Testing

Canonical APIs/events SHALL use:

```text
OpenAPI

AsyncAPI

JSON Schema
```

or relevant contract format.

---

# 207. Consumer Compatibility

Breaking change tests SHALL prevent silent incompatibility with:

```text
Trade

ERP

Pulse

CMS

digital estates.
```

---

# 208. Database Testing

PostgreSQL integration tests SHALL cover:

```text
temporal constraints

unique identities

foreign keys

tenant isolation

transactional outbox

concurrent promotion.
```

---

# 209. Migration Tests

Database migrations SHALL be tested against:

```text
representative prior schema state

current data fixtures

rollback/forward strategy where supported.
```

---

# 210. Never Test Only Empty Database

Production migrations interact with existing history.

---

# 211. Temporal Database Tests

Test:

```text
overlapping legal intervals

non-overlapping versions

future versions

retroactive knowledge insertion

as-of queries.
```

---

# 212. Concurrency Tests

Examples:

```text
two reviewers promote same candidate

RuleVersion superseded during evaluation

reassessment races transaction update

bundle changes during decision.
```

---

# 213. Expected Behaviour Must Be Deterministic

No silent last-writer-wins on material regulatory state.

---

# 214. Clock Tests

Use explicit fixed:

```text
legal_time

knowledge_time

system_time
```

in tests.

---

# 215. Avoid Wall Clock Dependence

Rejected:

```text
if datetime.now()...
```

inside regulatory golden semantics.

---

# 216. Timezone Tests

Test:

```text
UTC

jurisdiction local midnight

DST where relevant

date-only legal commencement.
```

---

# 217. South Africa / Uganda

Both currently use time zones without daylight-saving transitions, but Baobab architecture is multi-jurisdictional and SHALL not assume that universally.

---

# 218. Numeric Semantics

Tests SHALL cover:

```text
decimal precision

rounding

currency

unit conversion

inclusive/exclusive boundaries.
```

---

# 219. Avoid Floating-Point Surprise

Regulatory monetary/rate calculations SHOULD use deterministic decimal semantics appropriate to the rule.

---

# 220. Test Oracle Integrity

Every approved golden expected value SHALL itself have provenance.

---

# 221. GoldenCaseVerification

Conceptually:

```text
GoldenCaseVerification
├── case_ref
├── oracle_basis
├── source_refs[]
├── reviewer_refs[]
├── verification_date
├── review_policy_ref
└── provenance
```

---

# 222. Golden Tests Can Be Wrong

Therefore golden corpus governance matters.

---

# 223. Golden Case Challenge

A reviewer MAY challenge an approved case.

---

# 224. Challenge Does Not Silently Edit It

Creates:

```text
revalidation case
```

and, if necessary:

```text
GoldenCase v2.
```

---

# 225. Incorrect Golden Case Incident

If a test oracle is found wrong:

```text
GOLDEN_ORACLE_DEFECT.
```

---

# 226. Blast Radius

Find:

```text
rules validated by case

certifications depending on case

historical releases affected.
```

---

# 227. Test Evidence

Every consequential release SHALL produce a:

# `RegulatoryTestEvidenceBundle`

---

# 228. RegulatoryTestEvidenceBundle

Conceptually:

```text
RegulatoryTestEvidenceBundle
├── test_run_id
├── commit/build_ref
├── RuleSet fingerprint
├── BRIR version
├── compiler version
├── evaluator version
├── package revision
├── golden_suite_version
├── test categories[]
├── pass/fail summary
├── semantic coverage
├── implementation coverage
├── mutation evidence
├── performance evidence
├── regression evidence
├── environment
├── executed_at
└── integrity metadata
```

---

# 229. Test Evidence Is Immutable

A later rerun creates:

```text
new test run.
```

---

# 230. Release Artifact Linkage

RegulatoryExecutionPackage SHOULD reference:

```text
test evidence / certification
```

used to authorise publication.

---

# 231. Reproducible Test Environment

Pin material dependencies:

```text
BRIR schema

compiler

OPA version

test fixtures

DecisionPolicy

runtime config.
```

---

# 232. Containerised Test Environment

SHOULD be reproducible through project-standard container/devcontainer/CI mechanisms.

---

# 233. Python Test Harness

Where Regulations Python components are used, pytest SHOULD provide the conventional deterministic test harness.

Pytest supports reusable fixtures and extensive parametrisation suitable for running a golden scenario across multiple evaluators/configurations.

---

# 234. Parametrised Conformance Example

Conceptually:

```text
GoldenCase X
```

runs against:

```text
BRIR reference evaluator

OPA/Rego

OPA/Wasm

future evaluator.
```

All must satisfy expected semantics where the target is certified.

---

# 235. Custom Test Markers

Tests SHOULD be classifiable:

```text
golden

e3

e4

jurisdiction_za

jurisdiction_ug

mutation

historical

slow

integration

performance.
```

Pytest supports custom markers and strict validation of marker names, preventing silent selection errors due to typos.

---

# 236. Strict Markers

Python test configuration SHOULD enable strict marker validation where custom markers are used.

---

# 237. No Hidden Skips

Consequential suites SHALL treat unexpected:

```text
SKIPPED

XFAIL
```

carefully.

---

# 238. E4 Required Tests Shall Not Be Silently XFailed

---

# 239. Test Quarantine

A flaky test MAY be quarantined only if:

```text
reason documented

effect-class impact understood

owner assigned

expiry/remediation date defined.
```

---

# 240. A Flaky Regulatory Test Is an Engineering Defect

Do not normalise repeated reruns until green.

---

# 241. Reproducibility

Given same:

```text
golden case

RuleSet

BRIR

DecisionPolicy

evaluator semantics
```

result SHALL be reproducible.

---

# 242. Randomness

Consequential deterministic test paths SHALL not depend upon uncontrolled randomness.

---

# 243. Property-Based Tests Use Reproducible Seeds/Examples Where Needed

Failed generated examples SHALL be retained so regressions remain repeatable.

Hypothesis supports reuse of previously failing examples from its example database.

---

# 244. Certification versus Testing

Testing answers:

> Did the selected cases pass?

Certification answers:

> Is the total body of assurance evidence sufficient for this regulatory profile and effect ceiling?

---

# 245. Certification Is Governed Decision

Not merely:

```text
CI green = certified.
```

---

# 246. Certification Inputs

Include:

```text
test evidence

coverage

known gaps

review state

source state

change freshness

security

runtime compatibility.
```

---

# 247. Certification Approval

For E3/E4 SHOULD require authorised governance role from ADR-REG-0022.

---

# 248. Test Failure Effect

A failing test SHALL prevent publication where it affects the intended execution scope.

---

# 249. Failure Classification

Potential:

```text
SOURCE_FIXTURE_FAILURE

DOMAIN_INVARIANT_FAILURE

SEMANTIC_FAILURE

BRIR_CONFORMANCE_FAILURE

COMPILER_FAILURE

EVALUATOR_FAILURE

GOLDEN_CASE_FAILURE

HISTORICAL_REGRESSION

PERFORMANCE_REGRESSION

SECURITY_FAILURE

CONTRACT_FAILURE

RESILIENCE_FAILURE.
```

---

# 250. Materiality

No single numeric score.

Failures are evaluated by:

```text
affected semantics

affected profile

effect class

known exposure.
```

---

# 251. Production Shadow Testing

Before consequential new RuleSet activation:

```text
Current Active RuleSet
          │
          ├──────────────┐
          ▼              ▼
    authoritative       candidate
      decision           shadow
          │              │
          └───────┬──────┘
                  ▼
             DecisionDiff
```

---

# 252. Expected Differences

For intended legal change:

```text
difference manifest
```

SHOULD identify expected changed cases.

---

# 253. Unexpected Difference

Blocks promotion until explained.

---

# 254. Shadow Data

May use:

```text
live transaction inputs
```

subject to privacy/rights and without candidate enforcement.

---

# 255. Canary

After shadow equivalence, a bounded canary MAY activate new package for:

```text
specific runtime

tenant

profile

traffic cohort.
```

---

# 256. Canary Tests Operational Correctness

Including:

```text
bundle distribution

latency

receipts

context interaction

event propagation.
```

---

# 257. Canary Does Not Replace Semantic Testing

It occurs after semantic assurance.

---

# 258. Production Monitoring as Continuing Validation

Monitor:

```text
decision outcome distribution

INDETERMINATE rate

evaluation errors

latency

runtime drift

unexpected rule path

reassessment anomalies.
```

---

# 259. Statistical Drift Does Not Automatically Mean Legal Defect

A real market behaviour change could explain output distribution changes.

Investigate.

---

# 260. Decision Anomaly

Unexpected spike:

```text
PROHIBITED
```

may indicate:

```text
new valid rule

bad context feed

compiler defect

evidence outage.
```

---

# 261. Production Incident Feeds Regression Corpus

Every material regulatory defect SHOULD produce:

```text
new regression fixture

or golden case
```

after remediation.

---

# 262. Learning Loop

```text
Production Incident
      ↓
Root Cause
      ↓
Regression Case
      ↓
Test Suite
      ↓
Future Prevention
```

---

# 263. Regulatory Change Integration

ADR-REG-0023 change events SHOULD select affected:

```text
RuleVersions

golden cases

certifications

regression corpus.
```

---

# 264. New Rule Version

Must run:

```text
its own golden cases
+
affected neighbouring semantics
+
relevant historical regressions.
```

---

# 265. Exception Change

Must run:

```text
general case

old exception cases

new exception cases

boundary cases.
```

---

# 266. Threshold Change

Must run values:

```text
below

exactly equal

above
```

old and new thresholds.

---

# 267. Effective-Date Change

Must run:

```text
immediately before

exact instant/date

immediately after.
```

---

# 268. Repeal

Must prove:

```text
rule previously applies

rule no longer applies after repeal

historical pre-repeal replay remains unchanged.
```

---

# 269. Retroactive Change

Must test:

```text
historical restatement

original historical decision preserved.
```

---

# 270. Source Correction

Must test whether:

```text
knowledge correction
```

changes historical restatement as intended.

---

# 271. Jurisdiction Expansion

A new jurisdiction SHALL NOT inherit another jurisdiction's certification.

---

# 272. Shared Semantics May Reuse Tests

But:

```text
new jurisdiction
```

requires its own source/authority/temporal/context evidence.

---

# 273. Test Reuse Is Not Certification Reuse

Hard invariant.

---

# 274. Cross-Border Profiles

Tests MUST consider interactions rather than only isolated national rules.

Example:

```text
UG export
+
trade-regime origin
+
ZA import
+
SPS
+
documents.
```

---

# 275. End-to-End Cross-Border Golden Case

Expected output SHOULD identify:

```text
origin obligations

export requirements

transit if applicable

destination/import obligations

combined decision.
```

---

# 276. Do Not Collapse Jurisdictions

Test failure should show which jurisdiction/regime caused it.

---

# 277. Initial ZuriBeans Test Matrix

Initial certification corpus SHOULD include:

```text
coffee UG → ZA

vanilla UG → ZA

permit present

permit absent

permit expired

SPS certificate valid

SPS certificate missing

different HS classification

threshold boundary

future-effective rule

retroactive correction

explicit prohibition

verified exception

unknown classification.
```

---

# 278. Example Golden Case — Permit

Context:

```text
origin = UG
destination = ZA
product = coffee
legal_time = T
```

Verified rule:

```text
Permit P required.
```

Evidence:

```text
Permit P absent.
```

Expected:

```text
applicability = APPLIES

requirement = UNSATISFIED

outcome = UNSATISFIED

effect class = policy-dependent

reason =
REQUIRED_PERMIT_MISSING.
```

---

# 279. Mutation Proof

Remove Permit requirement from BRIR.

Expected:

```text
golden case fails.
```

If it passes:

```text
critical test gap.
```

---

# 280. Example Golden Case — Exception

Rule:

```text
Product X prohibited
unless valid Permit P.
```

Case A:

```text
permit absent
→ PROHIBITED.
```

Case B:

```text
permit valid
→ prohibition defeated.
```

---

# 281. Mutation

Delete exception.

Case B MUST fail.

---

# 282. Example — Effective Date Boundary

Rule effective:

```text
2027-01-01.
```

Cases:

```text
2026-12-31
→ rule not effective

2027-01-01
→ rule effective.
```

---

# 283. Boundary Mutation

Compiler mutation changes:

```text
>= commencement
```

to:

```text
> commencement.
```

Golden case at exactly commencement kills defect.

---

# 284. Example — Unknown Classification

Context:

```text
HS classification = UNKNOWN.
```

Applicability depends on HS.

Expected:

```text
INDETERMINATE.
```

---

# 285. Mutation

Unknown treated as false.

Golden case must fail.

---

# 286. Example — Historical Regression

Decision from June:

```text
SATISFIED
```

with pinned RuleSet.

OPA upgraded.

Historical semantic replay:

```text
SATISFIED.
```

If new runtime produces:

```text
UNSATISFIED
```

release is blocked.

---

# 287. Example — Legitimate Law Change

New RuleVersion intentionally changes threshold.

Historical replay with old RuleSet:

```text
same historical result.
```

Current reassessment with new RuleSet:

```text
changed result.
```

Both tests pass.

---

# 288. Example — AI Extraction Regression

New extraction pipeline begins missing:

```text
"except where"
```

clauses.

Exception-recall benchmark fails.

Candidate-generation pipeline cannot be promoted.

Existing published rules remain unaffected.

---

# 289. Example — Qdrant Outage

Qdrant unavailable.

Expected:

```text
knowledge retrieval degraded.
```

Existing verified OPA decision:

```text
still executable.
```

---

# 290. Example — OPA Bundle Missing

Consequential decision request.

Expected:

```text
EVALUATOR_NOT_READY

INDETERMINATE / governed hold
```

not:

```text
ALLOW.
```

---

# 291. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-TST-I01` | Regulatory correctness SHALL not be inferred from compilation success |
| `REG-TST-I02` | OPA line coverage SHALL remain distinct from regulatory semantic coverage |
| `REG-TST-I03` | Consequential rules SHALL be tested against verified semantic cases |
| `REG-TST-I04` | Golden cases SHALL carry independent provenance for expected outcomes |
| `REG-TST-I05` | The same unverified AI pipeline SHALL not serve as both implementation and sole oracle |
| `REG-TST-I06` | Golden cases SHALL be versioned rather than silently rewritten |
| `REG-TST-I07` | Positive tests alone SHALL be insufficient |
| `REG-TST-I08` | Exceptions, boundaries and UNKNOWN states SHALL be explicitly tested |
| `REG-TST-I09` | Temporal rule boundaries SHALL be explicitly tested |
| `REG-TST-I10` | BRIR semantics SHALL be independently testable |
| `REG-TST-I11` | Production evaluator output SHALL conform to reference BRIR semantics |
| `REG-TST-I12` | Compiler upgrades SHALL not silently change unchanged BRIR semantics |
| `REG-TST-I13` | Evaluator upgrades SHALL pass historical differential regression |
| `REG-TST-I14` | Property-based tests SHALL use legally valid invariants rather than assumed monotonicity |
| `REG-TST-I15` | Mutation testing SHALL be used as adequacy evidence, not legal correctness scoring |
| `REG-TST-I16` | Material surviving semantic mutants SHALL require explanation |
| `REG-TST-I17` | Historical decisions SHALL remain regression-testable |
| `REG-TST-I18` | Intended legal changes SHALL not be treated as software regressions |
| `REG-TST-I19` | Golden baselines SHALL not be updated merely to make CI pass |
| `REG-TST-I20` | Jurisdiction certification SHALL remain distinct from government/legal certification |
| `REG-TST-I21` | Certification SHALL declare a maximum permitted effect class |
| `REG-TST-I22` | Jurisdiction certification SHALL not automatically transfer to another jurisdiction |
| `REG-TST-I23` | Test fixtures SHALL respect content rights and tenant isolation |
| `REG-TST-I24` | Consequential release evidence SHALL be retained and reproducible |
| `REG-TST-I25` | Performance optimisations SHALL rerun semantic conformance tests |
| `REG-TST-I26` | AI extraction TEVV SHALL remain distinct from deterministic decision certification |
| `REG-TST-I27` | Verified fast-path execution SHALL not depend upon AI-plane availability |
| `REG-TST-I28` | Production shadow/canary tests SHALL supplement, not replace, pre-production semantic testing |
| `REG-TST-I29` | Every material production defect SHOULD produce a future regression case |
| `REG-TST-I30` | Test and certification evidence SHALL be traceable to exact RuleSet/compiler/evaluator versions |
| `REG-TST-I31` | Event-contract and idempotency tests SHALL be part of integration assurance |
| `REG-TST-I32` | Test execution time SHALL not substitute for explicit legal-time inputs |
| `REG-TST-I33` | No E4-required test may silently become an expected failure |
| `REG-TST-I34` | Test coverage SHALL include reasons and requirements, not only final outcomes |
| `REG-TST-I35` | Regulatory assurance SHALL be established by converging independent evidence, not one metric |

---

# 292. Rejected Alternative — Rego Unit Tests Only

Rejected.

---

# 293. Rejected Alternative — 100% Line Coverage Means Rule Correct

Rejected.

---

# 294. Rejected Alternative — Compiler Success Means Rule Correct

Rejected.

---

# 295. Rejected Alternative — Snapshot Tests as Primary Legal Oracle

Rejected.

---

# 296. Rejected Alternative — AI Generates Rule and Its Own Golden Answer

Rejected.

---

# 297. Rejected Alternative — Only Happy-Path Tests

Rejected.

---

# 298. Rejected Alternative — Only Final Outcome Assertions

Rejected.

---

# 299. Rejected Alternative — No Boundary Tests

Rejected.

---

# 300. Rejected Alternative — Unknown Treated as False for Easier Tests

Rejected.

---

# 301. Rejected Alternative — One Global Coverage Percentage

Rejected.

---

# 302. Rejected Alternative — Mutation Score as Legal Confidence Score

Rejected.

---

# 303. Rejected Alternative — Production Traffic Is the Test Suite

Rejected.

---

# 304. Rejected Alternative — Canary Instead of Golden Tests

Rejected.

---

# 305. Rejected Alternative — Update Golden Snapshots Automatically After Rule Change

Rejected.

---

# 306. Rejected Alternative — New Jurisdiction Reuses Existing Certification Unchanged

Rejected.

---

# 307. Rejected Alternative — Model Benchmark Certifies E4 Rule

Rejected.

---

# 308. Rejected Alternative — OPA Upgrade Directly to Production

Rejected for consequential profiles without regression/conformance testing.

---

# 309. Rejected Alternative — Property Tests Using Arbitrary Business Assumptions

Rejected.

Properties must correspond to verified regulatory/domain invariants.

---

# 310. Rejected Alternative — Test With `datetime.now()`

Rejected for legal semantics.

---

# 311. Rejected Alternative — Ignore Test Data Rights

Rejected.

---

# 312. Rejected Alternative — Flaky E4 Test Rerun Until Green

Rejected.

---

# 313. Minimum Implementation Proof

Before `ADR-REG-0025` is considered implemented, Baobab SHOULD demonstrate:

```text
1. RegulatoryGoldenCase schema.

2. golden-case versioning.

3. golden-case provenance.

4. oracle basis.

5. reviewer verification.

6. synthetic-case classification.

7. source-backed case.

8. rights-safe case.

9. positive case.

10. negative case.

11. boundary case.

12. exception case.

13. exemption case.

14. unknown case.

15. indeterminate case.

16. not-applicable case.

17. coverage-gap case.

18. conflict case.

19. cumulative-obligation case.

20. temporal case.

21. retroactive case.

22. future-effective case.

23. amendment case.

24. evidence case.

25. discretion case.

26. human-judgment-required case.

27. jurisdiction case.

28. role case.

29. regime case.

30. SemanticCoverageMatrix.

31. normative-modality coverage.

32. exception coverage.

33. temporal coverage.

34. requirement-state coverage.

35. outcome coverage.

36. RT0 document fidelity suite.

37. table extraction fidelity test.

38. OCR fidelity test.

39. source-coordinate test.

40. RT1 domain invariant suite.

41. temporal-domain constraints.

42. tenant-isolation invariant.

43. RT2 semantic unit suite.

44. condition tests.

45. exception tests.

46. calculation tests.

47. deadline tests.

48. classification tests.

49. conflict-resolution tests.

50. UNKNOWN propagation tests.

51. RT3 BRIR conformance suite.

52. BRIR schema validation.

53. BRIR type validation.

54. reference BRIR evaluator.

55. RT4 OPA differential suite.

56. BRIR-reference versus OPA equivalence.

57. Rego target conformance.

58. Wasm target conformance where enabled.

59. compiler-version differential.

60. OPA-version differential.

61. `opa check --strict`.

62. `regal lint`.

63. `opa test --fail-on-empty`.

64. OPA coverage report.

65. OPA coverage threshold.

66. profile-specific coverage policy.

67. parametrised golden tests.

68. pytest strict markers.

69. property-based context generation.

70. Hypothesis failure shrinking.

71. previous-failure reuse.

72. stateful RuleVersion lifecycle test.

73. irrelevant-context metamorphic relation.

74. unrelated-evidence metamorphic relation.

75. evidence-order metamorphic relation.

76. duplicate-evidence metamorphic relation.

77. explanation-language metamorphic relation.

78. Qdrant-independence metamorphic relation.

79. LLM-independence metamorphic relation.

80. RegulatorySemanticMutator.

81. `<`/`<=` boundary mutant.

82. `>`/`>=` mutant.

83. normative-modality mutant.

84. exception-removal mutant.

85. condition-removal mutant.

86. threshold mutant.

87. effective-date mutant.

88. jurisdiction mutant.

89. actor-role mutant.

90. UNKNOWN-to-false mutant.

91. hierarchy-override mutant.

92. evidence-validity mutant.

93. survivor reporting.

94. equivalent-mutant review.

95. E4 material-mutant policy.

96. HistoricalRegressionCase.

97. production-derived rights-safe corpus.

98. historical exact replay regression.

99. historical semantic replay regression.

100. compiler upgrade regression.

101. evaluator upgrade regression.

102. DecisionPolicy regression.

103. context-resolver regression.

104. DecisionDiff on regression.

105. intended-change manifest.

106. governed golden-baseline update.

107. RegulatoryPackCertification.

108. pack source manifest.

109. pack coverage manifest.

110. pack golden-suite reference.

111. pack semantic coverage.

112. pack BRIR conformance evidence.

113. pack evaluator conformance.

114. pack historical regression evidence.

115. pack performance evidence.

116. pack security evidence.

117. ADVISORY_READY state.

118. REVIEW_GATE_READY state.

119. CONDITIONAL_ENFORCEMENT_READY state.

120. HARD_ENFORCEMENT_READY state.

121. maximum-effect-class enforcement.

122. certification suspension.

123. certification revalidation.

124. test-impact selection from RuleVersion change.

125. change-to-test traceability.

126. PR fast gate.

127. integration gate.

128. extended assurance gate.

129. release-candidate certification gate.

130. production shadow gate.

131. canary gate.

132. emergency minimum regression gate.

133. `opa bench` performance test.

134. `opa test --bench` regression benchmark.

135. p50 evaluation latency.

136. p95 evaluation latency.

137. p99 evaluation latency.

138. memory benchmark.

139. package-size benchmark.

140. bundle-activation benchmark.

141. performance-regression alert.

142. AI extraction evaluation suite.

143. citation precision/recall.

144. exception recall.

145. temporal extraction accuracy.

146. hallucinated-citation metric.

147. human-correction metric.

148. live-model TEVV separated from deterministic CI.

149. prompt-injection security test.

150. tenant-overlay isolation test.

151. tampered bundle test.

152. stale-bundle readiness test.

153. Qdrant-outage test.

154. Haystack-outage test.

155. LLM-outage test.

156. LangGraph-outage test.

157. OPA-outage test.

158. Control-Plane-outage test.

159. PostgreSQL failure test.

160. event-broker failure test.

161. fast-path independence proof.

162. API contract tests.

163. AsyncAPI event contract tests.

164. duplicate-event consumer test.

165. out-of-order event test.

166. database migration test.

167. historical-data migration test.

168. concurrency promotion test.

169. reassessment race test.

170. fixed legal-time fixture.

171. fixed knowledge-time fixture.

172. timezone test.

173. decimal precision test.

174. unit-conversion test.

175. golden-oracle challenge workflow.

176. golden-oracle defect incident.

177. RegulatoryTestEvidenceBundle.

178. test-run immutability.

179. commit/build provenance.

180. RuleSet fingerprint provenance.

181. compiler-version provenance.

182. OPA-version provenance.

183. golden-suite-version provenance.

184. release-artifact linkage.

185. shadow decision comparison.

186. expected-difference validation.

187. unexpected-difference failure.

188. canary runtime validation.

189. production outcome monitoring.

190. material production incident → regression case.

191. Uganda export golden suite.

192. South Africa import golden suite.

193. UG→ZA cross-border combined golden suite.

194. coffee scenario.

195. vanilla scenario.

196. HS-classification scenario.

197. SPS certificate scenario.

198. permit scenario.

199. rules-of-origin scenario.

200. tariff scenario.

201. explicit prohibition scenario.

202. verified exception scenario.

203. future-effective amendment scenario.

204. retroactive correction scenario.

205. complete Source→RuleVersion→BRIR→OPA→Decision golden path.

206. complete BRIR-reference→OPA differential path.

207. complete historical-decision replay path.

208. complete mutation→test-kill evidence path.

209. complete jurisdiction-pack certification path.

210. complete shadow→canary→active promotion path.
```

---

# 314. Initial Cross-Border Golden Suite

The first certification suite SHOULD focus on:

```text
UGANDA
   │
   ├── exporter
   ├── export requirements
   └── origin facts
   │
   ▼
TRADE / REGIONAL REGIME
   │
   ├── rules of origin
   └── cross-border documentation
   │
   ▼
SOUTH AFRICA
   │
   ├── importer
   ├── customs
   ├── SPS
   ├── tariff
   └── permit requirements
```

for:

```text
coffee

vanilla.
```

---

# 315. Example Cross-Border Golden Case

Context:

```text
Tenant:
ZuriBeans

Exporter:
UG legal entity

Importer:
ZA counterparty

Product:
Coffee

Classification:
verified HS code

Legal time:
T

Quantity:
Q.
```

Expected semantics:

```text
UG export Rule A applies

Regional Rule B applies

ZA import Rule C applies

ZA SPS Rule D applies

Permit P required

Certificate C required.
```

---

# 316. Evidence Scenario A

```text
Permit P valid

Certificate C valid.
```

Expected:

```text
SATISFIED
or
SATISFIED_WITH_REQUIREMENTS
```

depending on remaining obligations.

---

# 317. Scenario B

```text
Permit P absent.
```

Expected:

```text
UNSATISFIED.
```

---

# 318. Scenario C

```text
classification unknown.
```

Expected:

```text
INDETERMINATE.
```

---

# 319. Scenario D

Verified exception applies.

Expected:

```text
general prohibition defeated

exception reason visible.
```

---

# 320. Mutation Run

Mutations:

```text
remove permit requirement

remove exception

shift threshold

change ZA jurisdiction to UG

treat UNKNOWN as false.
```

The golden suite SHOULD detect every material mutation.

---

# 321. Historical Regression Proof

Save validated decisions from this corpus.

Upgrade:

```text
OPA

compiler

Decision Engine.
```

Replay same:

```text
RuleSet

context

evidence.
```

Expected:

```text
semantic equivalence.
```

---

# 322. Future Law Change Proof

Publish new future-effective tariff rule.

Tests prove:

```text
old legal time
→ old outcome

future legal time
→ new outcome

historical replay
→ unchanged historical result.
```

---

# 323. Research Foundation Summary

OPA's built-in testing framework supports unit testing, mocking/substitution, coverage reporting, configurable coverage thresholds, failing when no tests are executed, parallel test execution and both Rego and Wasm evaluation targets. Baobab uses these mechanisms as the execution-target assurance layer, while explicitly supplementing them with legal-semantic golden cases.

OPA also recommends strict compilation checks, and its associated Regal tooling supplies additional linting. This makes syntax/type/static-analysis gates straightforward, but these checks establish policy-code quality rather than correctness of the underlying legal interpretation.

OPA includes benchmarking and profiling capabilities through `opa bench`, `opa test --bench` and `opa eval --profile`, allowing Baobab to track policy latency and memory/performance behaviour independently from semantic correctness.

Hypothesis provides property-based data generation, shrinking of failing inputs, persistence/reuse of known failures and rule-based stateful testing. These capabilities make it suitable for exploring regulatory boundary conditions and lifecycle sequences beyond the manually curated golden corpus.

Pytest's parametrisation and fixtures provide a practical mechanism for executing the same verified regulatory scenario across multiple evaluators and configurations, while custom markers can partition jurisdiction, consequence, performance and integration suites.

NIST research on metamorphic testing demonstrates its value where complete test oracles are expensive or unavailable by testing expected relationships between transformed inputs and outputs. Baobab uses the same concept for invariants such as irrelevant-context independence, evidence ordering and explanation-language independence.

Mutation-testing practice deliberately changes conditions, constants and return behaviour to determine whether tests actually detect likely defects. Baobab adapts that technique at the regulatory semantic layer—mutating modalities, exceptions, thresholds, effective dates, actors and jurisdictions rather than treating generic source-code mutation alone as sufficient.

NIST's TEVV-Athlon initial public draft, released in August 2026, reinforces the need to evaluate complete AI systems in their real intended-use contexts rather than depending solely on individual model metrics. Because it remains an initial public draft as of September 2026, Baobab treats it as evolving research guidance rather than final normative requirements.

---

# 324. Final Decision

Baobab Regulations SHALL implement a **multi-layer regulatory assurance architecture** in which independently verified golden cases provide the legal-semantic oracle, BRIR provides provider-neutral executable semantics, a reference evaluator provides semantic conformance, and production evaluators such as OPA must demonstrate equivalent behaviour before consequential deployment.

The assurance architecture is:

```text
                 AUTHORITATIVE SOURCE
                         │
                         ▼
                VERIFIED INTERPRETATION
                         │
                         ▼
                    RULEVERSION
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   GOLDEN CASE                      BRIR
      ORACLE                           │
          │                ┌───────────┴───────────┐
          │                ▼                       ▼
          │        Reference Evaluator          Compiler
          │                                        │
          │                                        ▼
          │                                       OPA
          │                                        │
          └──────────────┬─────────────────────────┘
                         ▼
                    DIFFERENTIAL
                       TESTING
                         │
                         ▼
                 REGULATORY DECISION
                         │
                         ▼
                HISTORICAL REGRESSION
                         │
                         ▼
                SHADOW / CANARY
                         │
                         ▼
                  CERTIFIED RELEASE
```

The golden-case principle is:

> **A consequential regulatory test needs an independently verified expected answer, not merely another output generated by the system being tested.**

The coverage principle is:

> **Implementation coverage tells us which code executed; regulatory semantic coverage tells us whether the important legal possibilities were actually exercised. Both matter, but they answer different questions.**

The BRIR principle is:

> **BRIR semantics must be testable independently of whichever policy engine executes them.**

The evaluator principle is:

> **OPA is required to agree with the verified BRIR semantics; OPA does not define those semantics.**

The differential principle is:

> **Every supported deterministic evaluator target must demonstrate semantic equivalence against the same canonical test corpus.**

The property-testing principle is:

> **Golden cases capture known important scenarios; property-based and metamorphic testing explore invariants and combinations humans did not enumerate.**

The mutation principle is:

> **Baobab should deliberately introduce plausible regulatory defects and demonstrate that its tests detect them.**

The temporal principle is:

> **Every consequential rule must be tested around commencement, expiry and other material temporal boundaries rather than merely at convenient dates.**

The historical principle is:

> **Infrastructure upgrades must preserve unchanged historical decision semantics, while genuine legal changes must produce intentionally explainable differences.**

The baseline principle is:

> **When a golden test fails, Baobab must establish why the expected regulatory result changed before changing the test.**

The jurisdiction principle is:

> **Each jurisdiction/profile must earn its own assurance evidence; similarity to another market is not certification.**

The certification principle is:

> **CI success is an input into regulatory-pack certification, not certification itself.**

The consequence principle is:

> **The greater the permitted enforcement effect, the richer the required test corpus, conformance evidence, mutation evidence, regression history and runtime validation.**

The performance principle is:

> **Regulatory correctness and operational viability are separately tested; neither compensates for the other.**

The AI principle is:

> **AI extraction performance is evaluated independently, while published deterministic rules remain subject to their own golden, BRIR, evaluator and historical regression tests.**

The production principle is:

> **Shadow and canary testing validate deployment behaviour after semantic correctness has already been established; production traffic is not where Baobab discovers whether the law was encoded correctly.**

And the strategic principle is:

> **Baobab should be able to demonstrate not merely that a regulatory rule has tests, but that independent source-backed examples define its expected meaning, adversarial mutations challenge that meaning, multiple evaluators agree on that meaning, historical decisions preserve that meaning, and the exact body of assurance evidence that authorised the rule can be reconstructed years later.**

That is the architecture established by `ADR-REG-0025`.

---

## Decision Summary

```text
ADR-REG-0025
────────────────────────────────────────

TEST THE MEANING
not merely the code.


GOLDEN CASE

Source-backed
Independently verified
Versioned
Temporal
Contextual


DO NOT

Let the same AI
write the rule
and its sole oracle.


TEST LEVELS

RT0 Source Fidelity

RT1 Domain Invariants

RT2 Semantic Units

RT3 BRIR Conformance

RT4 Evaluator Differential

RT5 Jurisdiction Golden Suite

RT6 Historical Regression

RT7 Distributed Runtime

RT8 Shadow / Canary

RT9 Resilience


COVERAGE

Code coverage
≠
semantic coverage.


SEMANTIC COVERAGE

Obligations
Prohibitions
Permissions
Exceptions
Unknowns
Boundaries
Time
Conflicts
Evidence


OPA

opa check --strict

Regal

opa test

fail-on-empty

coverage threshold

Rego / Wasm targets


REFERENCE EVALUATOR

BRIR semantic oracle
for execution conformance.


DIFFERENTIAL TEST

BRIR reference
=
OPA


PROPERTY TESTING

Generate contexts

Explore boundaries

Shrink failures


METAMORPHIC TESTING

Test how outcomes
must behave when
inputs are transformed.


MUTATION TESTING

Flip modality

Remove exception

Shift threshold

Change date

Change jurisdiction

Change actor

UNKNOWN → false


SURVIVING MUTANT

Test weakness
or equivalent mutation.

Investigate.


HISTORICAL REGRESSION

Same law
+
same inputs
=
same semantics.


LEGAL CHANGE

May change result
intentionally.

Explain with DecisionDiff.


JURISDICTION PACK

Source manifest

Coverage manifest

Golden suite

BRIR conformance

Evaluator conformance

Regression

Performance

Security

Governance


EFFECT CEILING

Certification determines
maximum eligible
decision consequence.


AI TEVV

Separate from
deterministic rule
certification.


PRODUCTION

Shadow
→
Canary
→
Active


STRATEGIC RESULT

Source-backed oracle
+
semantic tests
+
property tests
+
mutation tests
+
differential evaluation
+
historical replay
=
defensible regulatory assurance.
```
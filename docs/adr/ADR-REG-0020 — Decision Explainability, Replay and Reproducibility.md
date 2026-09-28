# ADR-REG-0020 — Decision Explainability, Replay and Reproducibility

**Subtitle:** Historical Reconstruction, Current-Knowledge Restatement, Decision Diff, Explanation Views and Reproducibility Assurance

**Status:** Proposed — Foundational Decision Assurance Architecture  
**Decision ID:** `ADR-REG-0020`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Explainability / Replay / Reproducibility / Decision Audit / Historical Reconstruction  
**Strategic Classification:** Core Regulatory Trust Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL implement first-class, machine-verifiable capabilities for:

```text
EXPLAIN

REPLAY

RESTATE

REASSESS

COMPARE

RECONSTRUCT

AUDIT
```

regulatory decisions.

Every consequential `RegulatoryDecision` SHALL be capable of answering, subject to access rights:

```text
What did Baobab decide?

What regulatory question was asked?

What business context was evaluated?

Which jurisdictions and regimes applied?

Which RuleVersions were considered?

Which rules actually applied?

Which rules were defeated or excluded?

What obligations arose?

What prohibitions applied?

What permissions applied?

Which requirements were satisfied?

Which requirements remained outstanding?

Which facts were used?

Which evidence supported those facts?

What was unknown?

Which conflicts were resolved?

What remained unresolved?

Which decision policy was used?

Which executable package evaluated it?

What outcome was produced?

What enforcement followed?

Would the result be different today?

If so, exactly why?
```

---

# 2. Governing Principle

> **A regulatory decision that cannot be reconstructed from its material inputs and rules is not suitable for consequential automation.**

A second principle is:

> **An explanation SHALL describe the structured reasons for a decision; it SHALL NOT depend upon hidden model reasoning.**

A third principle is:

> **Historical replay and present-day reinterpretation SHALL never be conflated.**

---

# 3. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics and Defeasible Reasoning Model`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0017 — Regulatory Context and Applicability Resolution`
- `ADR-REG-0018 — Regulatory Decision and Evaluation Engine`
- `ADR-REG-0019 — Policy Decision Point and Enforcement Point Separation`

It also follows Baobab Control Plane principles that consequential history, changesets, approvals, desired state, reconciliation and verification SHALL remain auditable rather than being rewritten after the fact.

---

# 4. Core Distinctions

Baobab SHALL distinguish:

```text
EXPLANATION
≠
TRACE

TRACE
≠
PROVENANCE

PROVENANCE
≠
AUDIT LOG

REPLAY
≠
RESTATEMENT

RESTATEMENT
≠
REASSESSMENT

REASSESSMENT
≠
SIMULATION

REPRODUCIBILITY
≠
IDENTICAL RUNTIME RE-EXECUTION

DECISION DIFF
≠
TEXT DIFF.
```

---

# 5. Explanation

An explanation answers:

> **Why did Baobab reach this regulatory conclusion?**

---

# 6. Decision Trace

A `DecisionTrace` answers:

> **Which structured decision operations occurred?**

Example:

```text
12 candidate rules
        ↓
8 applicable
        ↓
2 constitutive
        ↓
4 obligations
        ↓
1 prohibition
        ↓
1 exception defeats prohibition
        ↓
3 current requirements satisfied
        ↓
1 future requirement
        ↓
SATISFIED_WITH_REQUIREMENTS
```

---

# 7. Provenance

Provenance answers:

> **Where did the information, rules, evidence and generated artifacts come from, and through what activities were they produced?**

W3C PROV explicitly models provenance using entities, activities, agents, derivation and responsibility relationships.

---

# 8. Audit Log

An audit log answers:

```text
who

did what

when

to which object.
```

It is valuable but insufficient to explain legal reasoning.

---

# 9. Replay

Replay asks:

> **Can we reconstruct the decision using the state under which that decision was originally made?**

---

# 10. Restatement

Restatement asks:

> **Knowing what Baobab knows now, what do we now conclude about the historical situation?**

---

# 11. Reassessment

Reassessment asks:

> **What regulatory conclusion follows from the transaction's current state under the currently applicable regulatory state?**

---

# 12. Simulation

Simulation asks:

> **What would happen under a declared hypothetical or future context?**

---

# 13. The Four Main Temporal Operations

Baobab SHALL support at least four explicit modes:

```text
1. HISTORICAL_EXACT_REPLAY

2. HISTORICAL_SEMANTIC_REPLAY

3. CURRENT_KNOWLEDGE_RESTATEMENT

4. CURRENT_OR_FUTURE_REASSESSMENT
```

---

# 14. Historical Exact Replay

`HISTORICAL_EXACT_REPLAY` attempts to recreate the decision using the exact material execution state originally used.

Conceptually:

```text
Original ContextSnapshot

Original RuleSetSnapshot

Original EvidenceSnapshot

Original DecisionPolicy version

Original BRIR

Original CompiledPolicyArtifact

Original evaluator compatibility profile

Original legal time

Original knowledge time.
```

---

# 15. Exact Replay Objective

The objective is:

```text
same material inputs
+
same semantic rules
+
same execution artifact
=
same regulatory result.
```

---

# 16. Exact Does Not Mean Same CPU Instructions

Baobab does not require:

```text
same physical server

same CPU

same pod

same IP address.
```

Those are not regulatory semantics.

---

# 17. Historical Semantic Replay

`HISTORICAL_SEMANTIC_REPLAY` reconstructs the original decision semantics even if the exact original execution provider/runtime is no longer available.

Example:

```text
Original:
OPA 1.x

Future:
OPA removed from platform

Still retained:
RuleVersion
BRIR
DecisionPolicy
ContextSnapshot
EvidenceSnapshot
RuleSetSnapshot.
```

A compatible BRIR evaluator can reproduce the semantic decision.

---

# 18. Why Semantic Replay Matters

Provider neutrality from `ADR-REG-0005` and `0016` requires:

> **Historical explainability SHALL survive replacement of OPA.**

---

# 19. Exact Replay versus Semantic Replay

```text
EXACT REPLAY

same historical semantics
+
same target artifact where available


SEMANTIC REPLAY

same historical semantics
+
equivalent evaluator
```

---

# 20. Replay Assurance

Replay SHALL indicate which level was achieved.

Potential:

```text
EXACT

SEMANTICALLY_EQUIVALENT

PARTIAL

NOT_REPRODUCIBLE.
```

---

# 21. Current-Knowledge Restatement

`CURRENT_KNOWLEDGE_RESTATEMENT` uses:

```text
historical regulated event

historical transaction context
```

but:

```text
current Baobab knowledge
```

about the legal state.

---

# 22. Example

Original decision:

```text
10 September:
SATISFIED
```

Baobab later discovers on 20 September that a regulation had legally become effective on 1 September.

Restatement:

```text
Historical legal time:
10 September

Knowledge time:
current

Result:
UNSATISFIED
```

---

# 23. The Original Decision Remains

Baobab SHALL NOT rewrite:

```text
Decision D1
```

into the later conclusion.

Instead:

```text
D1
ORIGINAL DECISION

D2
CURRENT-KNOWLEDGE RESTATEMENT
```

with an explicit relationship.

---

# 24. Current Reassessment

`CURRENT_REASSESSMENT` may use:

```text
current transaction state

current evidence

current law

current knowledge.
```

It answers a different question.

---

# 25. Future Reassessment

Future mode MAY use:

```text
planned transaction state

future legal time

currently verified future-effective law.
```

---

# 26. Simulation

Simulation MAY use:

```text
draft law

alternative route

different classification

different importer

different shipment date.
```

It SHALL be clearly marked:

```text
SCENARIO / NON_BINDING.
```

---

# 27. ReplayMode

Conceptually:

```text
ReplayMode
├── HISTORICAL_EXACT
├── HISTORICAL_SEMANTIC
├── HISTORICAL_RESTATED
├── CURRENT_REASSESSMENT
└── FUTURE_SIMULATION
```

---

# 28. No Generic `replay=true`

Rejected.

The temporal perspective must be explicit.

---

# 29. ReplayRequest

Conceptually:

```text
DecisionReplayRequest
├── original_decision_ref
├── replay_mode
├── target_knowledge_time?
├── target_legal_time?
├── evaluator_preference?
├── include_explanation
├── include_diff
└── trace_context
```

---

# 30. ReplayResult

Conceptually:

```text
DecisionReplayResult
├── replay_id
├── original_decision_ref
├── replay_mode
├── original_outcome
├── replayed_outcome
├── reproducibility_level
├── context_comparison
├── ruleset_comparison
├── evidence_comparison
├── decision_policy_comparison
├── runtime_comparison
├── decision_diff_ref?
├── explanation_ref
├── executed_at
└── provenance
```

---

# 31. Replay SHALL Be Read-Only

Replay SHALL NOT:

```text
update shipment

enforce hold

change order

publish regulation

mutate original decision.
```

---

# 32. Replay Side Effects

All external side effects SHALL be disabled.

---

# 33. No Event Re-Emission

Historical replay SHALL NOT re-emit original:

```text
shipment.blocked

decision.issued

invoice.created
```

business events.

---

# 34. Replay Environment

Replay SHOULD execute in an isolated execution profile.

---

# 35. Replay Evaluation Profile

Potential:

```text
evaluation_profile =
HISTORICAL_REPLAY
```

with:

```text
side_effects = prohibited

external mutations = prohibited

live fact fetch = prohibited by default.
```

---

# 36. Live Fact Fetch During Exact Replay

Rejected by default.

Historical replay SHALL use persisted historical snapshots.

---

# 37. Why

Today's external system may return different values.

That would turn replay into reassessment.

---

# 38. Snapshot Requirement

Consequential decisions SHALL preserve sufficient immutable references to:

```text
RegulatoryContextSnapshot

ApplicableRuleSetSnapshot

FactSnapshot

EvidenceSet

DecisionPolicy

CompiledPolicyArtifact

Execution metadata.
```

---

# 39. Snapshot Independence

A historical decision SHALL remain explainable even if:

```text
Trade changed the shipment

ERP archived the invoice

customer changed name

permit expired

current regulation changed.
```

---

# 40. Referential Preservation

Canonical references remain useful for navigation, but replay SHALL rely on historical snapshots rather than reconstructing old facts from today's mutable master data.

---

# 41. Decision Input Envelope

A consequential assessment SHOULD retain a canonical:

# `DecisionInputEnvelope`

---

# 42. DecisionInputEnvelope

Conceptually:

```text
DecisionInputEnvelope
├── input_envelope_id
├── regulatory_question
├── context_snapshot_ref
├── ruleset_snapshot_ref
├── fact_snapshot_ref
├── evidence_set_ref
├── decision_policy_ref
├── legal_time
├── knowledge_time
├── evaluation_profile
├── subject_version
├── input_fingerprint
└── provenance
```

---

# 43. Execution Envelope

Separate:

```text
DecisionExecutionEnvelope
├── evaluator_provider
├── evaluator_version
├── compiled_artifact_ref
├── package_revision
├── bundle_revision?
├── compiler_version
├── runtime_ref
├── runtime_mode
├── execution_started_at
├── execution_completed_at
├── evaluator_decision_id?
└── result_fingerprint
```

---

# 44. Input and Execution Are Different

This separation means:

```text
same DecisionInputEnvelope
```

can be tested against:

```text
different equivalent evaluator versions
```

without changing regulatory meaning.

---

# 45. OPA Decision Provenance

OPA decision logs can record the query input/result, `decision_id`, trace identifiers and exact bundle revisions used by an evaluation. OPA explicitly describes this information as supporting auditing and offline debugging.

Baobab SHALL use this as execution evidence.

---

# 46. OPA Decision ID Is Not Baobab Decision ID

```text
OPA decision_id
≠
RegulatoryDecision.decision_id.
```

---

# 47. OPA Trace

OPA can return query explanation traces containing events such as:

```text
Enter

Exit

Eval

Fail

Redo.
```


These are useful for:

```text
developer diagnostics

compiler debugging

evaluation verification.
```

---

# 48. OPA Trace Is Not User Explanation

OPA evaluation traces expose execution mechanics.

They SHALL NOT be presented as the canonical legal explanation.

---

# 49. Why

A customer needs:

> "The import permit requirement applies because this shipment is an import into jurisdiction X and no verified exemption applies."

Not:

```text
Eval
Redo
Fail
query_id=54.
```

---

# 50. Explanation Architecture

Baobab SHALL produce explanations from a structured:

# `DecisionReasonGraph`

---

# 51. DecisionReasonGraph

Conceptually:

```text
Decision
   │
   ├── HAS_OUTCOME
   │      └── UNSATISFIED
   │
   ├── BECAUSE_OF
   │      └── Requirement R
   │
   ├── REQUIREMENT_DERIVED_FROM
   │      └── Obligation O
   │
   ├── OBLIGATION_DERIVED_FROM
   │      └── RuleVersion V
   │
   ├── RULE_INTERPRETS
   │      └── Provision P
   │
   ├── PROVISION_FROM
   │      └── Source S
   │
   └── REQUIREMENT_NOT_SATISFIED_BECAUSE
          └── Evidence E expired
```

---

# 52. DecisionReasonGraph Is a Logical Projection

It MAY be stored as relational structures and typed edges.

It does not require a graph database.

---

# 53. Reason Node Types

Initial types SHOULD include:

```text
DECISION

ASSESSMENT_OUTCOME

RULE

CONDITION

EXCEPTION

EFFECT

OBLIGATION

PROHIBITION

PERMISSION

REQUIREMENT

FACT

EVIDENCE

EVIDENCE_ASSESSMENT

CONFLICT

OVERRIDE

UNKNOWN

ERROR

REMEDIATION

SOURCE

PROVISION

INTERPRETATION.
```

---

# 54. Reason Relationship Types

Potential:

```text
BECAUSE_OF

SUPPORTED_BY

DERIVED_FROM

SATISFIED_BY

UNSATISFIED_BECAUSE

DEFEATED_BY

EXEMPTED_BY

OVERRIDDEN_BY

CONTRADICTED_BY

DEPENDS_ON

UNKNOWN_BECAUSE

FAILED_BECAUSE

REMEDIABLE_BY.
```

---

# 55. Explanation Shall Be Deterministically Grounded

Every material explanation statement SHALL resolve to structured canonical facts.

---

# 56. Example

Human explanation:

> "The shipment is not currently ready for import because the required permit has expired."

Underlying structure:

```text
Decision:
UNSATISFIED

Requirement:
VALID_IMPORT_PERMIT

EvidenceAssessment:
EXPIRED

Evidence:
permit_123

Rule:
reg_rule_456

Provision:
s14(2)

Source:
official publication.
```

---

# 57. Explainability Layers

Baobab SHALL support several explanation layers.

```text
L0 — Outcome

L1 — Reason Summary

L2 — Requirements and Effects

L3 — Rule and Legal Basis

L4 — Evidence and Fact Basis

L5 — Technical Execution Provenance
```

---

# 58. L0 — Outcome

Example:

```text
UNSATISFIED
```

---

# 59. L1 — Reason Summary

Example:

```text
Required import permit is not currently valid.
```

---

# 60. L2 — Requirements and Effects

Example:

```text
Obligation:
Importer must hold permit P.

Requirement:
Permit valid at customs-entry date.

Current state:
Expired.
```

---

# 61. L3 — Rule and Legal Basis

Shows:

```text
RuleVersion

citation

provision

instrument

jurisdiction

legal effective period.
```

---

# 62. L4 — Evidence and Facts

Shows:

```text
permit evidence

issuer

validity dates

shipment scope

EvidenceAssessment

relevant transaction facts.
```

---

# 63. L5 — Technical Provenance

For authorised operators/developers:

```text
BRIR fingerprint

compiler version

REP revision

OPA bundle revision

OPA decision_id

runtime version

trace_id.
```

---

# 64. Explanation Audience

Explanation SHALL be audience-sensitive.

Initial audiences:

```text
BUSINESS_USER

COMPLIANCE_OFFICER

LEGAL_REVIEWER

AUDITOR

REGULATOR

DEVELOPER

SUPPORT_OPERATOR

PUBLIC_CONTENT_CONSUMER.
```

---

# 65. Same Decision, Different Views

The underlying decision SHALL remain identical.

Only presentation changes.

---

# 66. Business View

Example:

```text
This shipment cannot currently proceed to customs entry.

Outstanding:
Valid import permit.

Next step:
Provide or obtain a valid permit.
```

---

# 67. Legal Reviewer View

Adds:

```text
legal source

provision

interpretation

RuleVersion

hierarchy

exceptions.
```

---

# 68. Auditor View

Adds:

```text
decision history

evidence

review actions

package version

enforcement receipt.
```

---

# 69. Developer View

Adds:

```text
compiler

OPA runtime

bundle revision

technical errors

trace IDs.
```

---

# 70. Public View

May show:

```text
general regulatory requirement

official citation

effective date.
```

It SHALL NOT expose private tenant transaction/evidence data.

---

# 71. Explanation View

Conceptually:

```text
DecisionExplanationView
├── decision_ref
├── audience
├── outcome
├── summary
├── reason_codes[]
├── material_effects[]
├── requirements[]
├── unresolved_items[]
├── remediation[]
├── citations[]
├── evidence_summary?
├── technical_metadata?
├── limitations[]
└── generated_at
```

---

# 72. Explanation Presentation Is Not New Decision

Different explanation views SHALL all reference the same canonical `RegulatoryDecision`.

---

# 73. Explanation Accuracy

NIST's explainability work identifies four useful principles: systems should provide an explanation, make it meaningful to its intended audience, ensure the explanation accurately reflects the basis/process that produced the output, and operate within clearly recognised knowledge limits.

Baobab SHALL adopt these principles where applicable to its explanation design, including where AI assists only with presentation.

---

# 74. Explanation Must Reflect Actual Decision

Rejected:

```text
generate plausible reason
after the fact.
```

---

# 75. Reason Fidelity

The explanation generator SHALL consume the actual:

```text
DecisionTrace

DecisionReasonGraph

RuleVersions

EvidenceAssessments.
```

---

# 76. Knowledge Limits

An explanation SHALL surface:

```text
INDETERMINATE

coverage limitation

unknown fact

unverified evidence

unresolved interpretation
```

instead of inventing certainty.

---

# 77. AI Explanation Boundary

AI MAY produce:

```text
plain-language paraphrase

summary

translation

audience adaptation.
```

---

# 78. AI SHALL NOT Determine Explanation Facts

AI SHALL NOT independently decide:

```text
which rule applied

which permit failed

what law controlled

which exception was relevant.
```

Those are canonical structured inputs.

---

# 79. AI Explanation Pipeline

Preferred:

```text
DecisionReasonGraph
        │
        ▼
Structured Explanation DTO
        │
        ▼
Optional LLM Presentation
        │
        ▼
Grounding Validator
        │
        ▼
Human-Readable Explanation
```

---

# 80. Deterministic Explanation Required

Every consequential decision SHALL have a useful explanation even if:

```text
LLM unavailable

Haystack unavailable

Qdrant unavailable.
```

---

# 81. LLM-Free Baseline

Template/structured rendering SHALL always be available.

---

# 82. Hidden Chain-of-Thought Is Not Required

Baobab SHALL NOT:

```text
store

request

depend upon
```

private hidden model reasoning as regulatory evidence.

---

# 83. Structured Reasons Are Sufficient

Baobab records:

```text
facts

conditions

exceptions

rules

relationships

evidence

outputs.
```

That is the proper explanation basis.

---

# 84. AI Translation

If explanation is translated:

```text
translated explanation
```

is a presentation artifact.

Canonical reason codes and source citations remain unchanged.

---

# 85. Translation Provenance

For consequential externally distributed explanations, Baobab SHOULD preserve:

```text
translation language

translation mechanism

model/human translator

version.
```

---

# 86. Legal Citation Preservation

Translation SHALL NOT translate or alter canonical legal identifiers incorrectly.

---

# 87. LegalRuleML Alignment

LegalRuleML explicitly emphasises preservation of the connection between formal rules and legally binding textual sources, supports fine-grained N:M relationships between provisions and rules, and carries provenance/creator metadata.

Baobab's explanation chain SHALL therefore preserve:

```text
Decision
→ RuleVersion
→ Interpretation
→ Provision
→ Legal Source.
```

---

# 88. Explanation of Rule Applicability

The engine SHOULD answer:

```text
Why did this rule apply?
```

Example:

```text
Jurisdiction:
ZA import

Activity:
IMPORT

Product classification:
X

Legal time:
T

Rule scope:
matches all above

Exception:
not triggered.
```

---

# 89. Explanation of Non-Applicability

Equally important:

```text
Why did Rule R not apply?
```

Example:

```text
Rule required exporter established in jurisdiction X.

Resolved exporter established in jurisdiction Y.

Result:
DOES_NOT_APPLY.
```

---

# 90. Explanation of Defeat

```text
General prohibition matched.

Verified specific exception applied.

Rule therefore defeated for this context.
```

---

# 91. Explanation of Indeterminate

Example:

```text
Outcome:
INDETERMINATE

Reason:
Product classification required.

Current classification:
UNRESOLVED.

Rules potentially affected:
R17
R18.
```

---

# 92. Explanation of Technical Failure

Correct:

```text
Regulatory conclusion could not be completed because
the expected policy bundle was unavailable.
```

Not:

```text
Law prohibits the transaction.
```

---

# 93. Explanation of Coverage Gap

```text
Assessment covers customs and tariff requirements.

SPS coverage unavailable.

Overall import readiness cannot be determined.
```

---

# 94. Scope Shall Be Visible

Every explanation SHOULD communicate:

```text
what was assessed

what was not assessed.
```

---

# 95. No Universal Compliance Claim

A bounded assessment SHALL not be rendered as:

```text
fully compliant with all law.
```

---

# 96. Explanation Limitations

Potential:

```text
Coverage limited to declared profile.

One classification remains provisional.

Decision based on planned shipment date.

Tenant counsel interpretation applied.

External authority determination pending.
```

---

# 97. Explanation of Enforcement

A complete audit explanation MAY include:

```text
Regulatory decision:
UNSATISFIED / E3

Recommended disposition:
HOLD

Trade enforcement:
shipment transitioned to REGULATORY_HOLD

Enforcement time:
T.
```

---

# 98. Decision and Enforcement Remain Separate

Explanation SHALL clearly distinguish:

```text
what Regulations decided
```

from:

```text
what Trade/ERP actually did.
```

---

# 99. Explanation of Internal Policy

Example:

```text
Regulatory result:
SATISFIED.

Trade internal policy:
Manager approval required.

Operational state:
HOLD.
```

This prevents misrepresentation that law caused the internal hold.

---

# 100. Decision Diff

Baobab SHALL implement a first-class:

# `DecisionDiff`

---

# 101. DecisionDiff Purpose

It answers:

> **Why are these two decisions different?**

---

# 102. DecisionDiff Is Semantic

It SHALL compare regulatory meaning, not just JSON fields.

---

# 103. DecisionDiff Dimensions

At minimum:

```text
CONTEXT

LEGAL TIME

KNOWLEDGE TIME

JURISDICTIONS

REGIMES

CLASSIFICATIONS

RULESET

RULE VERSIONS

INTERPRETATIONS

FACTS

EVIDENCE

REQUIREMENTS

CONFLICT RESOLUTION

DECISION POLICY

EVALUATOR

COVERAGE

OUTCOME

EFFECT CLASS

DISPOSITION

ENFORCEMENT.
```

---

# 104. Diff Categories

Potential:

```text
CONTEXT_CHANGED

RULE_ADDED

RULE_REMOVED

RULE_VERSION_CHANGED

RULE_BECAME_EFFECTIVE

RULE_REPEALED

INTERPRETATION_CHANGED

EXCEPTION_CHANGED

FACT_CHANGED

FACT_VERIFIED

EVIDENCE_ADDED

EVIDENCE_EXPIRED

EVIDENCE_REVOKED

CLASSIFICATION_CHANGED

COVERAGE_CHANGED

DECISION_POLICY_CHANGED

RUNTIME_CHANGED

OUTCOME_CHANGED.
```

---

# 105. Rule Difference Example

```text
Decision D1:
Rule R17 v3

Decision D2:
Rule R17 v4

Semantic change:
threshold 1000 → 1500.
```

---

# 106. Evidence Difference Example

```text
D1:
Permit absent.

D2:
Permit evidence supplied and verified.

Outcome:
UNSATISFIED → SATISFIED.
```

---

# 107. Context Difference Example

```text
D1:
Importer = Entity A

D2:
Importer = Entity B.
```

Applicable obligations may change.

---

# 108. Time Difference Example

```text
D1 legal time:
30 Dec

D2 legal time:
2 Jan

Rule R:
effective 1 Jan.
```

---

# 109. Knowledge Difference Example

```text
Same historical legal time.

D1 known-at:
10 Sep

D2 known-at:
28 Sep.

Newly discovered historical regulation changes result.
```

---

# 110. Evaluator Difference

If:

```text
same BRIR

same inputs

different evaluator provider
```

and outcome changes:

```text
SEMANTIC_CONFORMANCE_FAILURE.
```

---

# 111. Compiler Difference

Similarly:

```text
same RuleVersion

same BRIR

compiler v5 versus v6

different regulatory result
```

is presumptively a compiler/regression defect unless intentionally documented semantic behaviour changed upstream.

---

# 112. Decision Policy Difference

Outcome may change while law remains unchanged because:

```text
decision stage changed

decision question changed

DecisionPolicy changed.
```

This SHALL be identifiable.

---

# 113. Causal Diff

DecisionDiff SHOULD identify the smallest material change set sufficient to explain the outcome difference.

---

# 114. Example Causal Diff

```text
Outcome:
SATISFIED → UNSATISFIED

Primary cause:
Permit expired.

No RuleVersion changed.

No jurisdiction changed.

No classification changed.
```

---

# 115. Causal Diff Is Better Than Raw Diff

Raw:

```text
42 JSON fields changed.
```

Useful:

```text
permit validity ended before new customs-entry date.
```

---

# 116. DecisionDiff

Conceptually:

```text
DecisionDiff
├── diff_id
├── left_decision_ref
├── right_decision_ref
├── outcome_change?
├── context_changes[]
├── ruleset_changes[]
├── semantic_rule_changes[]
├── fact_changes[]
├── evidence_changes[]
├── temporal_changes[]
├── coverage_changes[]
├── decision_policy_changes[]
├── runtime_changes[]
├── effect_changes[]
├── requirement_changes[]
├── enforcement_changes[]
├── causal_summary[]
└── generated_at
```

---

# 117. Diff Direction Matters

```text
D1 → D2
```

may represent:

```text
historical → current

old rule → new rule

planned → actual.
```

The direction SHALL be explicit.

---

# 118. Explain Change API

Potential:

```text
GET /decisions/{left}/diff/{right}
```

Exact route deferred.

---

# 119. Replay APIs

Potential:

```text
POST /decisions/{id}/replay

POST /decisions/{id}/restatement

POST /decisions/{id}/reassessment
```

or one typed endpoint.

Exact HTTP shape deferred.

---

# 120. Explanation API

Potential:

```text
GET /decisions/{id}/explanation
```

with:

```text
audience

detail

language

includeEvidence

includeTechnical.
```

---

# 121. Server Determines Access

A caller cannot gain privileged provenance merely by asking:

```text
detail=developer.
```

IAM/Control Plane authorisation still applies.

---

# 122. Explanation Capability Scopes

Potential:

```text
regulations.decision.explain

regulations.decision.explain.legal

regulations.decision.explain.evidence

regulations.decision.explain.technical

regulations.decision.replay

regulations.decision.restate.
```

Exact capability contracts deferred.

---

# 123. Explanation Redaction

Explanation projections SHALL apply:

```text
tenant isolation

privilege

rights restrictions

privacy policy.
```

---

# 124. Redacted Does Not Mean Invented

If information cannot be disclosed:

```text
REDACTED / RESTRICTED
```

is appropriate.

Do not substitute fabricated detail.

---

# 125. Example

Legal reviewer may see:

```text
Tenant counsel opinion C123.
```

Ordinary operator may see:

```text
Verified tenant legal interpretation applied.
```

---

# 126. Privilege Leakage

Even revealing:

```text
a counsel opinion exists
```

may be sensitive.

Graph edges themselves SHALL respect classification.

---

# 127. Source Licensing

Historical replay may be possible even when source content can no longer legally be redistributed.

Baobab MAY retain:

```text
source ID

citation

hash

RuleVersion

interpretation

rights-safe metadata.
```

---

# 128. Reproducibility Limitation

If complete source artefact cannot be retained:

```text
SOURCE_REPRODUCIBILITY = LIMITED
```

SHALL be reported.

---

# 129. Reproducibility Dimensions

Baobab SHALL evaluate reproducibility across multiple dimensions.

---

# 130. ReproducibilityProfile

Conceptually:

```text
ReproducibilityProfile
├── source_reproducibility
├── context_reproducibility
├── evidence_reproducibility
├── ruleset_reproducibility
├── decision_policy_reproducibility
├── compiled_artifact_reproducibility
├── evaluator_reproducibility
├── outcome_reproducibility
└── explanation_reproducibility
```

---

# 131. Reproducibility States

Each dimension MAY use:

```text
EXACT

SEMANTICALLY_EQUIVALENT

PARTIAL

EXTERNAL_DEPENDENCY_REQUIRED

UNAVAILABLE.
```

---

# 132. Source Reproducibility

Can Baobab reconstruct:

```text
the exact source edition

provision locator

source hash?
```

---

# 133. Context Reproducibility

Can Baobab reconstruct the exact:

```text
actors

jurisdictions

activities

product/classification

transaction geography?
```

---

# 134. Evidence Reproducibility

Can Baobab identify:

```text
evidence used

its validity

its EvidenceAssessment?
```

---

# 135. RuleSet Reproducibility

Can Baobab recreate the exact immutable set of RuleVersions?

---

# 136. DecisionPolicy Reproducibility

Can Baobab identify the exact policy that mapped normative state to the requested decision?

---

# 137. Compiled Artifact Reproducibility

Can Baobab retrieve or deterministically rebuild the original target artifact?

---

# 138. Evaluator Reproducibility

Is the same evaluator version available?

If not, can equivalent semantics be demonstrated?

---

# 139. Outcome Reproducibility

Does replay produce:

```text
same AssessmentOutcome

same requirements

same effect class
```

where exact reproduction is expected?

---

# 140. Explanation Reproducibility

Can the structured explanation be regenerated from preserved reason data?

---

# 141. Full Reproducibility

A decision MAY be classified:

```text
FULLY_REPRODUCIBLE
```

only where all material dimensions satisfy the declared assurance profile.

---

# 142. Semantic Reproducibility

A decision MAY be:

```text
SEMANTICALLY_REPRODUCIBLE
```

if original infrastructure is unavailable but regulatory result can be reproduced from canonical semantics.

---

# 143. Partial Reproducibility

Example:

```text
decision

rules

context

evidence metadata
```

preserved, but original licensed source PDF unavailable.

---

# 144. Reproducibility Failure

Material missing:

```text
RuleSetSnapshot deleted

context snapshot missing

decision policy unknown.
```

Result:

```text
NOT_REPRODUCIBLE.
```

This is a governance incident for consequential decisions.

---

# 145. Reproducibility SLO

Future commercial/operational tiers MAY define:

```text
E1:
semantic replay target

E3/E4:
stronger exact artifact retention.
```

Detailed SLA belongs to `ADR-REG-0030`.

---

# 146. E4 Replay Requirement

An E4 decision SHOULD require sufficient retention to reproduce:

```text
context

ruleset

evidence

decision policy

compiled artifact identity

result

enforcement.
```

---

# 147. Evaluation Package Retention

Execution packages used for consequential decisions SHALL be retained according to decision-retention policy.

---

# 148. OPA Bundle Retention

For E3/E4:

```text
bundle revision alone
```

may not be sufficient if the bundle can no longer be retrieved.

The artifact or reconstructable equivalent SHOULD be retained.

---

# 149. OPA Decision Logs Are Not Sufficient Alone

OPA decision logs include useful input/result and bundle information, but Baobab's replay requires domain state such as:

```text
RuleVersion provenance

DecisionPolicy

ContextSnapshot

EvidenceAssessment.
```


---

# 150. OPA Rule Labels

Current OPA decision logging can include rule annotation IDs and labels for successfully evaluated rules, which Baobab MAY use as additional target-runtime correlation data.

These labels remain secondary to Baobab RuleVersion IDs.

---

# 151. Distributed Runtime Replay

For a locally delegated decision from `ADR-REG-0019`, replay SHALL consume:

```text
RegulatoryDecisionReceipt

REP revision

RuleSet fingerprint

local context fingerprint

evidence refs

decision policy

local evaluator metadata.
```

---

# 152. Offline Decision Replay

A later central replay SHALL be able to reproduce a bounded offline decision.

---

# 153. Offline Receipt Inconsistency

If replay demonstrates the offline result could not have been produced by the claimed package/input:

```text
DECISION_RECEIPT_INTEGRITY_FAILURE.
```

---

# 154. Receipt Signature

High-assurance local decision receipts MAY be signed or attested.

---

# 155. Replay of Enforcement

Regulatory replay SHALL NOT repeat the enforcement action.

Instead it MAY replay the:

```text
decision logic
```

and compare with:

```text
historical EnforcementReceipt.
```

---

# 156. Enforcement Explainability

The audit chain becomes:

```text
RegulatoryDecision
       │
       ▼
OperationalDisposition
       │
       ▼
PEP
       │
       ▼
EnforcementReceipt
       │
       ▼
Domain state transition.
```

---

# 157. Why Was This Shipment Held?

Baobab should answer:

```text
Regulations returned UNSATISFIED.

Effect class E3.

Reason:
required certificate expired.

Trade policy maps that E3 result
to REGULATORY_HOLD.

Trade enforced the hold at T.
```

---

# 158. Why Was It Released?

Likewise:

```text
New certificate supplied.

Evidence verified.

New assessment SATISFIED.

New decision superseded old decision.

Trade released hold.
```

---

# 159. Decision Lineage

Decision versions SHALL form a lineage.

Example:

```text
D1
UNSATISFIED
      │
      │ superseded by
      ▼
D2
SATISFIED
      │
      │ later restated by
      ▼
D3
HISTORICAL_RESTATEMENT
```

---

# 160. Relationship Types

Potential:

```text
SUPERSEDES

REPLAYS

RESTATES

REASSESSES

CHALLENGES

CONFIRMS

VARIES

REVERSES

SIMULATES.
```

---

# 161. Replay Does Not Supersede

A pure historical replay confirming D1 SHALL NOT supersede D1.

---

# 162. Reassessment May Supersede Operationally

A new current decision can supersede an old stale decision for operational use.

---

# 163. Restatement Does Not Automatically Supersede Historical Fact

Historical D1 remains:

```text
what Baobab decided then.
```

D2 records:

```text
what Baobab now concludes.
```

---

# 164. Challenge Explainability

When a user challenges a decision, Baobab SHOULD show:

```text
decision basis

material facts

evidence

unknowns

available remediation

challenge/review route
```

where appropriate.

---

# 165. No Invented Appeal Rights

Internal review SHALL not be called:

```text
statutory appeal
```

unless actual law establishes one.

---

# 166. Human Review Explanation

If a human decision materially contributed:

```text
reviewer role

decision

reason code

supporting evidence

scope

timestamp
```

SHALL be visible to authorised reviewers.

---

# 167. Human Review Is Not "Because Human Said So"

The explanation SHOULD preserve structured review basis.

---

# 168. Override Explanation

If an internal override affects operation:

```text
Regulatory conclusion:
UNSATISFIED

Internal override:
temporary release approved by role X

Legal conclusion remains:
UNSATISFIED.
```

---

# 169. Legal Exemption Explanation

Different:

```text
Regulatory requirement:
EXEMPTED

Legal basis:
Exemption E

Authority:
A

Period:
T1–T2.
```

---

# 170. Override ≠ Exemption

Hard invariant.

---

# 171. Explanation Freshness

An explanation is a view of a specific decision.

If law later changes:

```text
original explanation
```

SHALL remain historically correct for that decision.

---

# 172. Current Warning

UI MAY show:

```text
This historical decision was based on a superseded RuleSet.
```

without rewriting its explanation.

---

# 173. Current-Knowledge Banner

A historical explanation MAY also state:

```text
A later restatement produced a different outcome.
```

---

# 174. Historical Explanation

Should display:

```text
Decision made:
10 Sep

Legal time:
10 Sep

Knowledge cutoff:
10 Sep

RuleSet:
R123

Outcome:
SATISFIED.
```

---

# 175. Restated Explanation

Should display:

```text
Historical legal time:
10 Sep

Restatement performed:
28 Sep

Knowledge cutoff:
28 Sep

Newly discovered Rule:
R999

Restated outcome:
UNSATISFIED.
```

---

# 176. This Prevents Revisionist Audit History

Both records remain visible.

---

# 177. Explanation of Temporal Law

A decision SHOULD be able to say:

```text
Rule R17 was selected because it was
legally applicable on 5 January 2027,
even though the assessment was performed
on 20 December 2026.
```

---

# 178. Temporal Difference Explanation

Or:

```text
Previous shipment date:
30 December

Current shipment date:
5 January

Rule R17:
effective 1 January

Therefore R17 now applies.
```

---

# 179. Explainability of Legal Hierarchy

If a rule was displaced:

```text
Rule A would otherwise apply.

Rule B prevailed for this conflict scope
under verified precedence relationship P.

Therefore A was partially displaced.
```

---

# 180. Explainability of Cumulative Rules

```text
Both Rule A and Rule B apply.

They regulate different requirements.

Neither displaces the other.
```

---

# 181. Explainability of Defeasibility

```text
General Rule A applies in principle.

Exception Rule B applies to this context.

A is therefore defeated for this transaction.
```

---

# 182. Explanation of Permission

```text
Rule P grants explicit permission.

This permission does not remove
independent obligation O.
```

---

# 183. Explainability of Unknown

The system SHALL state:

```text
what is unknown

why it matters

what decision depends upon it

how the gap may be resolved.
```

---

# 184. Example

```text
Outcome:
INDETERMINATE

Unknown:
product classification

Why it matters:
Rules R12 and R14 depend on classification.

Remediation:
obtain verified classification.
```

---

# 185. Explainability of Errors

System errors SHALL not be presented as legal conclusions.

Example:

```text
Regulatory evaluation could not complete
because the expected policy package was unavailable.
```

---

# 186. Technical Details Are Audience-Gated

Developer:

```text
REP-44 not loaded;
active REP-43.
```

Business user:

```text
Regulatory assessment temporarily unavailable.
```

The semantic state remains:

```text
INDETERMINATE.
```

---

# 187. Reproducibility and AI

An original AI-assisted extraction does not have to be regenerated token-for-token to replay a later deterministic decision.

---

# 188. Canonical Promotion Boundary

```text
AI extraction candidate
        ↓
verified interpretation
        ↓
RuleVersion
        ↓
BRIR
```

Historical decision depends on the promoted RuleVersion.

---

# 189. Why

AI APIs may be:

```text
nondeterministic

updated

retired.
```

Canonical regulatory execution must survive those changes.

---

# 190. AI Provenance Still Retained

The RuleVersion's provenance MAY still show:

```text
AI model used

prompt/template version

reviewer

promotion workflow.
```

---

# 191. Explanation Generation Reproducibility

Exact prose need not always reproduce identically if an LLM paraphrase is regenerated.

---

# 192. Semantic Explanation Must Reproduce

The underlying:

```text
reason codes

effects

requirements

citations

facts

evidence

limitations
```

must remain reproducible.

---

# 193. Rendered Explanation Version

Where exact published text matters, Baobab SHOULD persist:

```text
RenderedExplanation
```

rather than rely upon regeneration.

---

# 194. Published Explanation

Examples:

```text
customer notification

regulator submission

CMS article

formal audit report.
```

---

# 195. Published Artifact Provenance

Persist:

```text
rendered text

template/model version

language

source decision

generated_at

publisher/reviewer.
```

---

# 196. CMS Boundary

CMS MAY publish a rights-safe `DecisionExplanationView`.

CMS SHALL not regenerate legal reasoning independently.

---

# 197. CMS Historical Content

If CMS content was based on RuleVersion R1 and R2 supersedes it:

```text
stale regulatory projection
```

can be detected.

---

# 198. Pulse Boundary

Pulse MAY compare regulatory decisions over time to identify:

```text
commercial impact

new risk

new opportunity

cost changes.
```

---

# 199. Pulse Does Not Rewrite Explanation

A Pulse insight such as:

```text
"This change may reduce margins"
```

is commercial intelligence.

It does not become:

```text
the reason the regulation applies.
```

---

# 200. Explainability Export

Baobab SHOULD support a portable:

# `DecisionExplanationBundle`

---

# 201. DecisionExplanationBundle

Potential contents:

```text
Decision

Assessment

DecisionTrace

ReasonGraph

Context summary

RuleSet manifest

material RuleVersions

citations

EvidenceAssessment summaries

DecisionDiff if relevant

Execution metadata

EnforcementReceipt

reproducibility profile

integrity manifest.
```

---

# 202. Bundle Audience

Export profile MAY be:

```text
INTERNAL_AUDIT

CUSTOMER

LEGAL_REVIEW

REGULATOR

TECHNICAL_FORENSICS.
```

---

# 203. Rights-Safe Export

Restricted source text or privileged material MAY be omitted while retaining:

```text
citation

hash

canonical ID

restriction reason.
```

---

# 204. Integrity Manifest

The bundle SHOULD contain hashes for included immutable objects.

---

# 205. Bundle Signing

High-assurance exported explanation bundles MAY be cryptographically signed.

---

# 206. Signature Meaning

Signature establishes:

```text
bundle integrity

publisher identity.
```

It does not make the regulatory conclusion infallible.

---

# 207. W3C PROV Projection

Selected explanation/provenance data SHOULD be exportable as W3C PROV-compatible relationships where useful.

---

# 208. Internal Model Remains Richer

W3C PROV provides generic provenance.

Baobab's regulatory model additionally understands:

```text
RuleVersion

Obligation

EvidenceAssessment

DecisionOutcome

legal citation.
```

---

# 209. Decision Graph Traversal

Backward:

```text
Decision
  ↓
Assessment
  ↓
Rule
  ↓
Interpretation
  ↓
Provision
  ↓
Source.
```

---

# 210. Evidence Traversal

```text
Decision
  ↓
Requirement
  ↓
EvidenceAssessment
  ↓
Evidence
  ↓
Issuer / source.
```

---

# 211. Forward Impact Traversal

```text
RuleVersion
  ↓
Assessments
  ↓
Decisions
  ↓
EnforcementReceipts.
```

---

# 212. Source Correction Impact

```text
Corrected Source
   ↓
ProvisionVersion
   ↓
Interpretations
   ↓
Rules
   ↓
Decisions.
```

---

# 213. Evidence Revocation Impact

```text
Revoked Permit
   ↓
EvidenceAssessments
   ↓
RequirementSatisfaction
   ↓
Assessments
   ↓
Decisions.
```

---

# 214. These Capabilities Prepare ADR-REG-0023

Change detection and impact analysis will rely heavily on this decision/provenance graph.

---

# 215. Decision Replay Store

PostgreSQL SHALL remain the authoritative store for replay metadata and canonical decision state.

---

# 216. No Event-Sourcing Requirement

This ADR does not mandate full platform event sourcing.

---

# 217. Why

Append-oriented domain history plus immutable snapshots is sufficient initially.

---

# 218. Events Are Valuable

Domain events remain useful for:

```text
notifications

projections

reassessment triggers

Pulse integration.
```

But event logs are not the sole canonical persistence model.

---

# 219. Snapshot + History Model

Preferred:

```text
immutable snapshots
+
versioned canonical objects
+
audit/provenance events.
```

---

# 220. Storage Retention

Retention policy SHALL account for:

```text
decision effect class

contract requirements

jurisdiction requirements

transaction lifecycle

evidence retention rules

tenant policy

content rights.
```

---

# 221. High-Consequence Retention

E3/E4 decision material SHOULD ordinarily have stronger retention than E0 informational queries.

---

# 222. Right to Delete / Privacy

Where privacy law requires deletion/minimisation:

```text
decision defensibility

legal retention obligation

data minimisation
```

must be reconciled through explicit policy.

---

# 223. Pseudonymised Replay

Where identity itself is not legally relevant, replay records MAY use:

```text
canonical pseudonymous reference
```

subject to policy.

---

# 224. Identity Relevant Cases

If legal-entity identity is material to applicability:

```text
removing identity semantics
```

may destroy reproducibility.

That limitation must be explicit.

---

# 225. Data Residency

Replay/export SHALL preserve tenant/regional data-residency boundaries.

---

# 226. Cross-Border Explanation Export

A user in one region SHALL not automatically gain access to private evidence stored in another region simply because the decision spans both jurisdictions.

---

# 227. Explanation Caching

Rendered explanations MAY be cached.

---

# 228. Cache Key

SHOULD include:

```text
decision_id

explanation audience

language

detail level

explanation schema/version

redaction profile.
```

---

# 229. Decision Explanation Is Immutable for Historical Decision

If the canonical decision does not change:

```text
deterministic structured explanation
```

should not semantically drift.

---

# 230. Presentation Upgrade

A new UI/template may render the same decision differently.

Store:

```text
presentation version
```

where exact historical output matters.

---

# 231. Reason Codes

Reason codes from ADR-REG-0018 are foundational for stable explanation.

Examples:

```text
REQUIRED_PERMIT_MISSING

EXPLICIT_PROHIBITION_APPLIES

MATERIAL_CLASSIFICATION_UNKNOWN

COVERAGE_INCOMPLETE

RULE_CONFLICT_UNRESOLVED.
```

---

# 232. Reason Code Stability

Codes SHOULD remain stable across wording/localisation changes.

---

# 233. Explanation Schema Version

Canonical structured explanations SHALL carry:

```text
explanation_schema_version.
```

---

# 234. Replay Schema Migration

Old decisions SHOULD remain interpretable after decision-schema upgrades.

---

# 235. Migration Does Not Rewrite Historical Semantics

New serialization:

```text
≠
new decision.
```

---

# 236. Semantic Migration Testing

Migration tests SHALL verify:

```text
old decision semantics preserved

fingerprints/audit linkage maintained.
```

---

# 237. Historical Runtime Replacement

Suppose:

```text
OPA replaced by Engine X in 2030.
```

A 2027 decision should still be reconstructable.

---

# 238. Replay Strategy

```text
Original BRIR
     │
     ├── original OPA artifact available
     │       ↓
     │   EXACT replay
     │
     └── original runtime unavailable
             ↓
         reference BRIR evaluator
             ↓
       SEMANTIC replay
```

---

# 239. Reference Evaluator Importance

`ADR-REG-0016` proposed a BRIR reference evaluator.

This ADR makes its long-term value clearer:

```text
semantic replay oracle

cross-evaluator conformance

historical independence.
```

---

# 240. Reference Evaluator Need Not Be Production PDP

It can remain:

```text
slower

test-oriented

highly deterministic.
```

---

# 241. Conformance Test

For pinned inputs:

```text
OPA result
=
BRIR reference result.
```

A mismatch is a release/replay defect.

---

# 242. OPA Monitoring Correlation

OPA can emit OpenTelemetry spans that include the policy evaluation's `opa.decision_id` when decision logging is enabled.

Baobab SHOULD correlate:

```text
trace_id

RegulatoryDecision ID

OPA decision_id
```

for operational forensic analysis.

---

# 243. Distributed Trace Is Not Explanation

Tracing helps answer:

```text
where latency/error occurred.
```

It does not answer:

```text
why law required a permit.
```

---

# 244. Performance

Replay SHALL not compete with transactional fast-path capacity without resource controls.

---

# 245. Replay Workload Classes

Potential:

```text
INTERACTIVE_REPLAY

AUDIT_REPLAY

BATCH_REPLAY

IMPACT_REASSESSMENT.
```

---

# 246. Batch Replay

Useful for:

```text
100,000 historical decisions

after source correction

after compiler defect

after rule reinterpretation.
```

---

# 247. Replay Is Not Impact Selection

ADR-REG-0023 will determine:

```text
which decisions need reevaluation.
```

This ADR defines:

```text
how to replay them.
```

---

# 248. Batch Replay Results

SHOULD report:

```text
same result

different result

non-reproducible

requires review.
```

---

# 249. Replay Drift Detection

If exact historical replay unexpectedly yields a different result:

```text
REPLAY_DRIFT.
```

---

# 250. Potential Causes

```text
compiler defect

runtime semantic change

corrupted artifact

incorrect snapshot

nondeterministic function

data migration defect.
```

---

# 251. Replay Drift Is Serious

For E3/E4 decisions it SHALL be treated as a high-priority integrity incident.

---

# 252. Deterministic Functions

BRIR production rules from `0016` SHALL use deterministic functions where possible precisely to make replay reliable.

---

# 253. Randomness

Randomness SHALL NOT affect consequential regulatory evaluation.

---

# 254. Current Wall Clock

Historical replay SHALL not use:

```text
NOW()
```

in place of original temporal input.

---

# 255. External API Calls

Historical replay SHALL not depend on live external APIs for material facts.

---

# 256. Machine Learning Runtime

Consequential deterministic replay SHALL not depend on re-running an LLM.

---

# 257. Database Query Ordering

Replay logic SHALL not rely upon undefined relational row ordering.

---

# 258. Decimal Arithmetic

Calculation semantics SHALL remain deterministic/versioned.

---

# 259. Business Calendar

Replay of deadlines SHALL use the exact:

```text
calendar version

timezone

adjustment policy
```

originally used.

---

# 260. FX / External Rate

If a regulatory calculation used a historical exchange rate or reference value:

```text
that input snapshot
```

must be preserved.

---

# 261. Reproduction Failure Example

Wrong:

```text
replay 2026 tariff decision
using today's FX rate.
```

---

# 262. Correct

Use:

```text
historical input rate
+
its provenance.
```

---

# 263. Explainability Quality Gates

A consequential rule SHOULD not reach E3/E4 if it cannot generate a coherent structured explanation.

---

# 264. Minimum Explanation Gate

At minimum:

```text
rule identity

source basis

applicability reason

material facts

effect

requirement

outcome reason.
```

---

# 265. E4 Explainability Gate

E4 SHOULD additionally require:

```text
full DecisionTrace

evidence links

replayability

RuleSet fingerprint

runtime/package provenance

decision validity

enforcement receipt linkage.
```

---

# 266. Explanation Failure

If the rule evaluator produces a result but DecisionReasonGraph cannot be constructed consistently:

```text
EXPLANATION_INTEGRITY_FAILURE.
```

High-consequence automation SHALL fail closed operationally.

---

# 267. Explainability Must Not Be Decorative

A fluent paragraph attached to an opaque decision is insufficient.

---

# 268. Explanation Validation

Structured explanation SHOULD be validated against:

```text
DecisionOutcome

RuleEvaluationResults

EvidenceAssessment

DecisionTrace.
```

---

# 269. Contradictory Explanation

If explanation says:

```text
permit satisfied
```

but canonical requirement says:

```text
UNSATISFIED
```

publication SHALL fail.

---

# 270. AI Hallucination Guard

LLM explanation output SHALL be checked against allowed canonical reason objects before release for consequential decisions.

---

# 271. Citation Hallucination Guard

Every generated legal citation SHALL resolve to:

```text
canonical RegulatoryCitation

or explicitly marked unverified material.
```

---

# 272. Explanation Templates

Deterministic templates SHOULD be maintained for:

```text
SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE.
```

---

# 273. Example — SATISFIED

```text
The assessed transaction currently satisfies
all material requirements within the declared
Cross-Border Import profile.

4 applicable obligations were evaluated.
4 current prerequisites are satisfied.
No unresolved material prohibition or conflict remains.
```

---

# 274. Example — SATISFIED_WITH_REQUIREMENTS

```text
The transaction may proceed at the current stage.

A post-import filing remains due by Date T.

This requirement does not currently prevent
the assessed pre-shipment action.
```

---

# 275. Example — UNSATISFIED

```text
The transaction does not currently satisfy
the assessed import-readiness requirements.

A valid import permit is required before customs entry.

The submitted permit expired on Date T.
```

---

# 276. Example — PROHIBITED

```text
The requested activity is prohibited under Rule R
for the assessed product and jurisdiction.

No verified exception or controlling permission applies.
```

---

# 277. Example — INDETERMINATE

```text
Baobab cannot currently determine whether
the transaction may proceed.

Product classification remains unresolved,
and that classification determines whether
Rule R applies.
```

---

# 278. Example — NOT_APPLICABLE

```text
Within the declared and sufficiently covered profile,
no regulatory rules material to this question apply
to the assessed context.
```

---

# 279. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-EXP-I01` | Explanation SHALL be derived from canonical structured reasons |
| `REG-EXP-I02` | Hidden LLM reasoning SHALL not be required for explanation |
| `REG-EXP-I03` | OPA evaluation trace SHALL not be the canonical legal explanation |
| `REG-EXP-I04` | Replay SHALL remain distinct from restatement |
| `REG-EXP-I05` | Restatement SHALL remain distinct from current reassessment |
| `REG-EXP-I06` | Historical replay SHALL use historical snapshots |
| `REG-EXP-I07` | Historical replay SHALL not fetch mutable live facts by default |
| `REG-EXP-I08` | Replay SHALL have no operational business side effects |
| `REG-EXP-I09` | Replay SHALL not re-emit historical enforcement events |
| `REG-EXP-I10` | Original decisions SHALL never be overwritten by later restatements |
| `REG-EXP-I11` | Historical-as-known and current-knowledge views SHALL remain separately identifiable |
| `REG-EXP-I12` | Exact replay and semantic replay SHALL remain distinguishable |
| `REG-EXP-I13` | Replacing OPA SHALL not destroy historical explainability |
| `REG-EXP-I14` | Decision differences SHALL be expressed semantically, not only textually |
| `REG-EXP-I15` | Rule changes, fact changes and evidence changes SHALL remain distinguishable causes |
| `REG-EXP-I16` | Explanation views MAY vary by audience but SHALL not change the underlying decision |
| `REG-EXP-I17` | Privileged/redacted information SHALL not be fabricated in explanation |
| `REG-EXP-I18` | Regulatory conclusion and PEP operational action SHALL remain distinguishable |
| `REG-EXP-I19` | Internal policy and external regulation SHALL remain distinguishable |
| `REG-EXP-I20` | AI paraphrase SHALL not create new decision facts |
| `REG-EXP-I21` | Consequential decisions SHALL have a deterministic explanation path |
| `REG-EXP-I22` | Material legal citations in explanations SHALL resolve to canonical source records |
| `REG-EXP-I23` | Reproducibility SHALL be measured across multiple dimensions rather than one Boolean |
| `REG-EXP-I24` | Missing exact runtime SHALL not imply semantic non-reproducibility |
| `REG-EXP-I25` | An evaluator semantic mismatch SHALL be treated as a conformance failure |
| `REG-EXP-I26` | Replay drift SHALL be observable and governed |
| `REG-EXP-I27` | Historical evidence versions SHALL remain reconstructable subject to lawful retention |
| `REG-EXP-I28` | Explanation export SHALL respect licensing, privilege, tenant isolation and residency |
| `REG-EXP-I29` | High-assurance decisions SHALL retain stronger replay material |
| `REG-EXP-I30` | Every consequential decision SHALL remain defensible from decision back to source and facts |

---

# 280. Rejected Alternative — Store Only Final Outcome

Rejected.

```text
UNSATISFIED
```

without reasons is insufficient.

---

# 281. Rejected Alternative — Store Explanation Prose Only

Rejected.

Natural-language prose is not a durable canonical decision structure.

---

# 282. Rejected Alternative — OPA Trace Is the Explanation

Rejected.

OPA trace describes runtime execution, not legal meaning.

---

# 283. Rejected Alternative — LLM Generates Explanation from Scratch

Rejected.

---

# 284. Rejected Alternative — Hidden Chain-of-Thought as Evidence

Rejected.

---

# 285. Rejected Alternative — Replay Using Current Law

Rejected.

That is restatement/reassessment.

---

# 286. Rejected Alternative — Replay Using Current Master Data

Rejected.

---

# 287. Rejected Alternative — Replay Causes Business Mutations

Rejected.

---

# 288. Rejected Alternative — New Knowledge Rewrites Old Decision

Rejected.

---

# 289. Rejected Alternative — Exact Old OPA Binary Required Forever

Rejected.

Semantic replay through canonical BRIR SHALL remain possible.

---

# 290. Rejected Alternative — Same Outcome Means Same Reason

Rejected.

Two decisions may share:

```text
UNSATISFIED
```

for different causes.

---

# 291. Rejected Alternative — JSON Diff Is Decision Diff

Rejected.

---

# 292. Rejected Alternative — Same Rule ID Means Same Rule Semantics

Rejected.

RuleVersion matters.

---

# 293. Rejected Alternative — Current Citation URL Required for Replay

Rejected.

Persistent source identity/provenance must survive URL loss.

---

# 294. Rejected Alternative — Explanation Available to Everyone

Rejected.

Access control and privilege remain necessary.

---

# 295. Rejected Alternative — Redaction Means Remove All Trace

Rejected.

Rights-safe references may remain even where content cannot be disclosed.

---

# 296. Rejected Alternative — AI Explanation Confidence Score Determines Decision Assurance

Rejected.

---

# 297. Rejected Alternative — Different Evaluator Result Is Acceptable Variance

Rejected for deterministic BRIR.

---

# 298. Rejected Alternative — Re-running LLM Needed for Decision Replay

Rejected.

Canonical promotion intentionally breaks that dependency.

---

# 299. Minimum Implementation Proof

Before `ADR-REG-0020` is considered implemented, Baobab SHOULD demonstrate:

```text
1. DecisionInputEnvelope.

2. DecisionExecutionEnvelope.

3. Historical exact replay mode.

4. Historical semantic replay mode.

5. Current-knowledge restatement mode.

6. Current reassessment mode.

7. Future simulation mode.

8. Explicit replay-mode contract.

9. Side-effect-free replay.

10. No domain events emitted during replay.

11. Historical ContextSnapshot reuse.

12. Historical FactSnapshot reuse.

13. Historical EvidenceSet reuse.

14. Historical RuleSetSnapshot reuse.

15. Historical DecisionPolicy reuse.

16. Historical legal-time reuse.

17. Historical knowledge-time reuse.

18. Exact CompiledPolicyArtifact replay.

19. OPA bundle revision replay.

20. OPA decision_id correlation.

21. Semantic replay using BRIR reference evaluator.

22. OPA unavailable but semantic replay succeeds.

23. DecisionReasonGraph.

24. Structured reason relationships.

25. L0 outcome explanation.

26. L1 reason summary.

27. L2 effect/requirement explanation.

28. L3 rule/legal-source explanation.

29. L4 evidence explanation.

30. L5 technical explanation.

31. Business-user explanation view.

32. Compliance-officer explanation view.

33. Legal-reviewer view.

34. Auditor view.

35. Developer view.

36. Public rights-safe view.

37. Audience authorization.

38. Privileged evidence redaction.

39. Restricted-source redaction.

40. Deterministic LLM-free explanation.

41. Optional LLM paraphrase.

42. LLM grounding validator.

43. Citation hallucination prevention.

44. Translation projection.

45. Canonical reason-code preservation across translation.

46. Explanation limitation disclosure.

47. Explanation of APPLIES.

48. Explanation of DOES_NOT_APPLY.

49. Explanation of DEFEATED.

50. Explanation of EXEMPTED.

51. Explanation of INDETERMINATE.

52. Explanation of evaluator failure.

53. Explanation of coverage gap.

54. Explanation of legal hierarchy.

55. Explanation of cumulative obligations.

56. Explanation of strong permission.

57. Explanation of requirement satisfaction.

58. Explanation of evidence failure.

59. DecisionDiff aggregate.

60. Context diff.

61. RuleSet diff.

62. Rule semantic diff.

63. Evidence diff.

64. Classification diff.

65. temporal diff.

66. coverage diff.

67. DecisionPolicy diff.

68. evaluator/compiler diff.

69. enforcement diff.

70. causal decision-diff summary.

71. SATISFIED → UNSATISFIED diff.

72. UNSATISFIED → SATISFIED diff.

73. Original decision preserved after restatement.

74. Decision lineage relationships.

75. SUPERSEDES relation.

76. REPLAYS relation.

77. RESTATES relation.

78. REASSESSES relation.

79. SIMULATES relation.

80. ReproducibilityProfile.

81. exact source reproducibility status.

82. context reproducibility status.

83. evidence reproducibility status.

84. RuleSet reproducibility status.

85. DecisionPolicy reproducibility status.

86. compiled-artifact reproducibility status.

87. evaluator reproducibility status.

88. outcome reproducibility status.

89. explanation reproducibility status.

90. FULLY_REPRODUCIBLE state.

91. SEMANTICALLY_REPRODUCIBLE state.

92. PARTIALLY_REPRODUCIBLE state.

93. NOT_REPRODUCIBLE incident.

94. Replay drift detection.

95. compiler regression detection.

96. evaluator semantic-conformance failure.

97. batch historical replay.

98. source-correction batch replay.

99. evidence-revocation batch replay.

100. DecisionExplanationBundle.

101. bundle integrity manifest.

102. signed audit bundle.

103. W3C PROV projection.

104. OPA trace retained only as technical provenance.

105. OpenTelemetry/decision correlation.

106. EnforcementReceipt explanation.

107. decision-to-enforcement chain.

108. TOCTOU decision-version explanation.

109. internal Trade policy distinguished from regulatory decision.

110. E4 explainability gate.

111. E4 replayability gate.

112. explanation integrity-failure test.

113. exact rendered published explanation retention.

114. CMS decision projection.

115. Pulse decision-change projection.

116. decision explanation without Haystack.

117. decision explanation without Qdrant.

118. decision explanation without LangGraph.

119. decision replay without live source fetch.

120. decision replay after OPA replacement.
```

---

# 300. Initial ZuriBeans Replay Proof

The initial end-to-end demonstration SHOULD use a synthetic cross-border transaction:

```text
ZuriBeans shipment S

Uganda
    exporter jurisdiction

South Africa
    importer jurisdiction

Product
    coffee

Classification
    X

Import date
    T

Permit
    expired

Certificate
    valid.
```

Original assessment:

```text
UNSATISFIED
```

because:

```text
permit requirement
+
expired evidence.
```

---

# 301. Exact Replay Proof

Replay uses:

```text
same context

same RuleSet

same permit evidence

same DecisionPolicy

same evaluator artifact.
```

Expected:

```text
UNSATISFIED

same material reason codes.
```

---

# 302. Semantic Replay Proof

Original OPA runtime unavailable.

Use BRIR reference evaluator.

Expected:

```text
same normative effects

same requirements

same outcome.
```

---

# 303. Restatement Proof

Later source correction establishes:

```text
permit rule was not actually applicable
to Product Classification X.
```

Current-knowledge historical restatement:

```text
SATISFIED
```

while original decision remains:

```text
UNSATISFIED.
```

---

# 304. Decision Diff

Baobab reports:

```text
Original:
UNSATISFIED

Restated:
SATISFIED


CAUSE

Rule R17 applicability changed
because verified historical
classification scope was corrected.


UNCHANGED

Shipment context

Permit evidence

Import date.
```

---

# 305. Regulatory Audit Explanation

An authorised auditor should be able to traverse:

```text
Original Decision
       │
       ▼
UNSATISFIED
       │
       ▼
Requirement R
       │
       ▼
Permit evidence
       │
       ▼
Expired
```

and separately:

```text
Restatement
       │
       ▼
Rule R17 no longer applicable
       │
       ▼
SATISFIED
```

without either record rewriting the other.

---

# 306. Strategic Capability — Regulatory Time Machine

With `ADR-REG-0015` and this ADR together, Baobab can answer:

```text
WHAT APPLIED THEN?

WHAT DID WE KNOW THEN?

WHAT DID WE DECIDE THEN?

WHAT DO WE KNOW NOW?

WHAT WOULD WE DECIDE NOW?

WHY ARE THOSE ANSWERS DIFFERENT?
```

---

# 307. Strategic Capability — Decision Defence

A customer facing an audit can ask:

> **Why did we block this shipment eighteen months ago?**

Baobab can provide:

```text
exact context

exact applicable rules

exact evidence

exact decision policy

exact decision

exact enforcement receipt.
```

---

# 308. Strategic Capability — Corrective Transparency

Baobab can also say:

> **We later discovered that the historical legal position differed from the one known at the time. Here is the original decision, here is the corrected historical restatement, and here is exactly what changed.**

This is materially stronger than silently rewriting the database.

---

# 309. Strategic Capability — Regulatory Regression Testing

Historical decisions become regression fixtures.

Before releasing:

```text
new compiler

new OPA version

new BRIR evaluator

new DecisionPolicy implementation
```

Baobab can replay historical decisions.

---

# 310. Expected Regression Result

For unchanged semantics:

```text
same result.
```

Unexpected delta:

```text
release blocked.
```

---

# 311. Strategic Capability — Provider Migration

A future migration:

```text
OPA
→
another deterministic policy engine
```

can be validated against:

```text
thousands of historical decisions.
```

This provides strong evidence of semantic equivalence.

---

# 312. Strategic Capability — Customer Trust

Rather than:

```text
"The system says no."
```

Baobab can say:

```text
"The transaction is currently unsatisfied because
this requirement applies,
this evidence expired,
this is the legal source,
this is the applicable version,
and this is what would resolve it."
```

---

# 313. Strategic Capability — Explainable Automation

The more Baobab moves toward E3/E4 automation, the more this capability becomes foundational rather than optional.

---

# 314. Research Foundation Summary

W3C PROV provides a standard model for representing entities, activities, agents, derivations and responsibility chains, which supports Baobab's source-to-rule-to-decision reconstruction without constraining Baobab to a generic provenance-only domain model.

LegalRuleML explicitly treats preservation of the relationship between legal text and machine-represented rules as essential to provenance, authority, authenticity and validation, including fine-grained N:M relationships between legal provisions and formal rules and support for multiple interpretations.

OPA decision logs preserve inputs/results, decision IDs, trace identifiers and policy-bundle revisions, making them valuable runtime evidence for replay and auditing. Baobab retains these as execution provenance beneath its richer regulatory decision model.

OPA can also expose detailed query evaluation traces for debugging. Those traces are implementation-level execution evidence and therefore useful to developers, but they are intentionally not adopted as Baobab's canonical human/legal explanation.

OPA can propagate its decision IDs through OpenTelemetry spans, providing a useful bridge between distributed operational tracing and Baobab's canonical decision IDs during forensic analysis.

NIST's explainability principles emphasise that explanations should accompany outputs, be meaningful to their intended recipient, accurately reflect how outputs were produced, and respect system knowledge limits. Baobab adopts those principles for explanation presentation while grounding consequential explanations in deterministic regulatory state rather than model-generated narrative.

---

# 315. Final Decision

Baobab Regulations SHALL implement **Decision Explainability, Replay and Reproducibility as first-class domain capabilities**.

The architecture is:

```text
                      REGULATORY DECISION
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        EXPLANATION         REPLAY          COMPARISON
             │                │                │
             ▼                ▼                ▼
       Reason Graph     Input Snapshot      DecisionDiff
             │                │                │
             ▼                ▼                ▼
       Human Views      Exact/Semantic       Causal
                         Reconstruction      Differences
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                      AUDIT / DEFENCE
```

The temporal architecture is:

```text
                    ORIGINAL DECISION
                           │
              ┌────────────┼─────────────┐
              ▼            ▼             ▼
        EXACT REPLAY   SEMANTIC      RESTATEMENT
                       REPLAY
              │            │             │
              ▼            ▼             ▼
       What happened?  Same meaning?  What do we
                                     now know about
                                         then?
                                           │
                                           ▼
                                      REASSESSMENT
                                           │
                                           ▼
                                      What applies
                                          now?
```

The explanation rule is:

> **Baobab SHALL explain decisions through structured regulatory reasons, not opaque runtime traces or hidden model reasoning.**

The historical rule is:

> **The original decision SHALL remain immutable even when later knowledge demonstrates that a different historical legal conclusion would now be reached.**

The replay rule is:

> **Historical replay reconstructs what Baobab decided under the original state; current-knowledge restatement asks what Baobab now concludes about that same historical state.**

The provider-neutrality rule is:

> **A historical decision SHALL remain semantically replayable after the evaluator that originally executed it has been replaced.**

The comparison rule is:

> **Decision differences SHALL identify changes in context, law, interpretation, facts, evidence, time, coverage, policy or runtime rather than presenting an undifferentiated data diff.**

The AI rule is:

> **AI may make a verified explanation easier to understand, but it SHALL NOT invent the reasons a regulatory decision was made.**

The assurance rule is:

> **The higher the consequence of a regulatory decision, the stronger its explanation, evidence, provenance and replay guarantees must be.**

And the strategic principle is:

> **Baobab Regulations should never merely tell a business what the answer is. It should be able to show why that answer was reached, reproduce the answer later, explain why the answer changed, and trace the entire conclusion back to both the law and the facts.**

That is the architecture established by `ADR-REG-0020`.

---

## Decision Summary

```text
ADR-REG-0020
────────────────────────────────────────────

CORE CAPABILITIES

Explain
Replay
Restate
Reassess
Compare
Audit


FOUR TEMPORAL MODES

Historical Exact Replay

Historical Semantic Replay

Current-Knowledge Restatement

Current/Future Reassessment


REPLAY

Original context
+
Original RuleSet
+
Original evidence
+
Original DecisionPolicy
+
Original temporal perspective


RESTATEMENT

Historical event
+
Current knowledge


REASSESSMENT

Current state
+
Current law


EXPLANATION

DecisionReasonGraph
not hidden AI reasoning.


EXPLANATION LEVELS

L0 Outcome

L1 Reason

L2 Effects / Requirements

L3 Legal Basis

L4 Evidence

L5 Technical Provenance


AUDIENCES

Business
Compliance
Legal
Audit
Regulator
Developer
Public


AI

May paraphrase.

Cannot invent
decision reasons.


OPA

Decision ID
Bundle revision
Evaluation trace

= execution provenance

NOT canonical explanation.


DECISION DIFF

Context
Rules
Interpretations
Facts
Evidence
Time
Coverage
Policy
Runtime
Outcome
Enforcement


REPRODUCIBILITY

Exact

Semantically Equivalent

Partial

Unavailable


PROVIDER NEUTRALITY

OPA may disappear.

Historical regulatory
meaning must survive.


HISTORY

Never rewrite
what Baobab decided then.


STRATEGIC RESULT

What did we decide?

Why?

Can we reproduce it?

What do we know now?

Why did the answer change?
```
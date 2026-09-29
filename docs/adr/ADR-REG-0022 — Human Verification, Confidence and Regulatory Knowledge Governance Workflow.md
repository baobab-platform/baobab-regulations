# ADR-REG-0022 — Human Verification, Confidence and Regulatory Knowledge Governance Workflow

**Subtitle:** Competence-Based Review, Maker-Checker Separation, Multidimensional Assurance, Sampling, Escalation and Canonical Knowledge Promotion

**Status:** Proposed — Foundational Regulatory Governance Architecture  
**Decision ID:** `ADR-REG-0022`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-29  
**Decision Type:** Human Verification / Knowledge Governance / Assurance / Maker-Checker / AI Oversight / Promotion Workflow  
**Strategic Classification:** Core Regulatory Trust and Governance Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL implement a competence-based, risk-proportionate and auditable regulatory knowledge governance system governing the transition:

```text
SOURCE
   │
   ▼
EXTRACTION
   │
   ▼
AI / MACHINE CANDIDATE
   │
   ▼
VALIDATION
   │
   ▼
HUMAN / GOVERNED VERIFICATION
   │
   ▼
INDEPENDENT CHECK
   │
   ▼
APPROVAL
   │
   ▼
PROMOTION
   │
   ▼
CANONICAL REGULATORY KNOWLEDGE
   │
   ▼
RULEVERSION
   │
   ▼
BRIR
   │
   ▼
DETERMINISTIC EXECUTION
```

The architecture SHALL NOT treat:

```text
human present
```

as equivalent to:

```text
effective human oversight.
```

Nor SHALL it treat:

```text
model confidence
```

as equivalent to:

```text
regulatory assurance.
```

The governing principle is:

> **AI may generate candidates. Qualified humans may verify them. Independent governance may approve them. Only governed promotion creates canonical Baobab regulatory knowledge.**

---

# 2. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics, Defeasibility, Discretion and Reparative Rules`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0012 — Regulatory Content Acquisition, Licensing and Reuse Rights`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0020 — Decision Explainability, Replay and Reproducibility`
- `ADR-REG-0021 — AI-Assisted Regulatory Extraction and Interpretation Boundary`

It also relies upon Baobab IAM and Control Plane for:

```text
identity

authentication

authorization

role/scoped authority

tenant isolation

administrative authority.
```

---

# 3. Research Finding — Human Oversight Must Be Designed

NIST's AI RMF requires human roles and responsibilities to be clearly defined and differentiated, calls for proficiency standards and training for those carrying out oversight, and requires human-oversight processes to be defined, assessed and documented.

Therefore Baobab SHALL NOT implement governance as:

```text
AI result
   ↓
[Approve] button
   ↓
Published.
```

---

# 4. Research Finding — Humans Are Not Automatically Reliable Controls

NIST's work on AI bias expressly warns against assuming that merely placing a human in the loop makes algorithmic systems adequately governed. Humans bring cognitive biases and may lack either appropriate subject-matter expertise or AI-system understanding.

Therefore:

> **The quality, competence, independence, information and authority of the reviewer matter more than the mere existence of a reviewer.**

---

# 5. Research Finding — Automation Bias Must Be Addressed

The EU AI Act's Article 14 requires human oversight for covered high-risk systems to be commensurate with risk, autonomy and context, and expressly requires overseers to understand system capabilities and limitations, interpret outputs correctly, remain aware of automation bias, disregard or reverse outputs where appropriate, and intervene where necessary.

Baobab is not asserting that Article 14 universally governs Baobab Regulations.

However, these are valuable design principles for consequential AI-assisted regulatory knowledge production.

---

# 6. Research Finding — Competence, Training and Authority Matter

The same EU framework emphasises that human overseers should have the necessary:

```text
competence

training

authority
```

to perform their oversight function.

NIST likewise calls for documented proficiency standards and training protocols for AI actors responsible for operation and oversight.

Baobab SHALL therefore implement reviewer qualification as a first-class control.

---

# 7. Research Finding — Separation of Duties Is a Mature Control

NIST defines separation of duties as preventing any one user from having sufficient privileges to misuse a system alone, and explicitly recognises two-person operations as a form of dynamic separation of duty.

Baobab SHALL apply this principle to consequential regulatory knowledge publication.

---

# 8. Two-Person Verification Is a Baobab Governance Decision

The EU AI Act contains a specific two-natural-person verification requirement for a particular biometric high-risk use case. That provision is not a general legal requirement for all AI systems.

Baobab nevertheless adopts:

```text
maker-checker separation
```

for selected consequential regulatory artefacts as an internal governance architecture based upon:

```text
separation of duties

independent verification

regulatory consequence.
```

---

# 9. Research Finding — Governance Is Continuous

NIST structures AI risk management around:

```text
GOVERN

MAP

MEASURE

MANAGE
```

and emphasises lifecycle-wide risk management, evaluation, documentation and monitoring.

ISO/IEC 42001 similarly establishes an AI management-system model covering governance, risk management, performance evaluation and continual improvement.

Therefore human-verification policy SHALL evolve from measured system performance rather than remain a static checklist.

---

# 10. Research Finding — TEVV Must Be Systematic

NIST's AI work emphasises:

```text
Testing

Evaluation

Verification

Validation
```

as a structured discipline rather than ad hoc quality inspection.

As of September 2026, NIST has also published an initial public draft of its TEVV-Athlon framework for evaluating AI systems, intended to provide an extensible approach across machine-learning, generative and agentic systems.

Baobab SHALL use TEVV evidence when deciding how much automation a particular extraction task may safely receive.

---

# 11. Fundamental Distinctions

Baobab SHALL distinguish:

```text
MODEL CONFIDENCE
≠
CANDIDATE ASSURANCE

CANDIDATE ASSURANCE
≠
HUMAN VERIFICATION

HUMAN VERIFICATION
≠
PUBLICATION APPROVAL

PUBLICATION APPROVAL
≠
LEGAL AUTHORITY

LEGAL AUTHORITY
≠
BAOBAB INTERPRETATION

SINGLE REVIEW
≠
INDEPENDENT REVIEW

REVIEWER SENIORITY
≠
REVIEWER COMPETENCE

AI AGREEMENT
≠
LEGAL CERTAINTY

SAMPLING
≠
VERIFICATION OF EVERY ITEM.
```

---

# 12. Human Verification Does Not Create Law

A qualified human reviewer can establish:

```text
Baobab has verified
this interpretation
under this governance policy.
```

The reviewer does not thereby create:

```text
statutory authority.
```

---

# 13. Reviewer Approval Is a Baobab Governance Fact

It SHALL remain distinct from:

```text
court ruling

regulator decision

official interpretation

statutory exemption

legal opinion by licensed counsel.
```

---

# 14. Reviewer Authority Basis

Every consequential review SHOULD state its authority basis.

Initial values MAY include:

```text
INTERNAL_REGULATORY_ANALYST

INTERNAL_DOMAIN_SPECIALIST

TENANT_DESIGNATED_EXPERT

LICENSED_LEGAL_COUNSEL

EXTERNAL_PROFESSIONAL_ADVISER

COMPETENT_AUTHORITY

TECHNICAL_RULE_ENGINEER

QUALITY_ASSURANCE_REVIEWER.
```

---

# 15. Authority Basis Is Not Competence Scope

A licensed lawyer may not necessarily be competent in:

```text
Ugandan phytosanitary export rules.
```

A customs specialist may not necessarily be competent in:

```text
South African privacy law.
```

---

# 16. Reviewer Competence Is Scoped

Baobab SHALL therefore maintain:

# `RegulatoryReviewerProfile`

---

# 17. RegulatoryReviewerProfile

Conceptually:

```text
RegulatoryReviewerProfile
├── reviewer_ref
├── principal_ref
├── reviewer_type
├── jurisdiction_scopes[]
├── regulatory_domains[]
├── subject_matter_scopes[]
├── language_scopes[]
├── activity_scopes[]
├── review_permissions[]
├── effect_class_authority[]
├── tenant_scope?
├── qualification_refs[]
├── training_refs[]
├── competence_valid_from
├── competence_valid_until?
├── status
└── provenance
```

---

# 18. Identity Remains IAM-Owned

Regulations SHALL reference:

```text
principal_ref
```

rather than creating an alternative human identity system.

---

# 19. Authorization Remains Control-Plane/IAM Governed

Regulations owns:

```text
what regulatory competence
a reviewer has.
```

IAM / Control Plane owns:

```text
whether that principal
may invoke the review capability.
```

---

# 20. Reviewer Status

Potential:

```text
ACTIVE

SUSPENDED

EXPIRED

REVOKED

UNDER_REVIEW.
```

---

# 21. Expired Competence

A reviewer whose competence scope has expired SHALL NOT approve new items under that scope.

Historical approvals remain part of history.

---

# 22. Competence Evidence

`QualificationReference` MAY reference:

```text
internal certification

professional qualification

professional licence

client designation

employment role

training completion

experience assessment

external accreditation.
```

---

# 23. Baobab Shall Not Invent Qualifications

If a credential has not been verified:

```text
CLAIMED
```

SHALL remain distinct from:

```text
VERIFIED.
```

---

# 24. Review Roles

The governance workflow SHOULD support distinct roles.

Initial roles:

```text
CANDIDATE_PRODUCER

STRUCTURAL_VALIDATOR

SOURCE_VERIFIER

REGULATORY_ANALYST

JURISDICTION_SPECIALIST

LEGAL_REVIEWER

RULE_ENGINEER

CHECKER

PUBLICATION_APPROVER

EMERGENCY_APPROVER

QUALITY_AUDITOR.
```

---

# 25. Candidate Producer

May be:

```text
AI

automated extraction system

human analyst.
```

Producer identity SHALL be recorded.

---

# 26. Structural Validator

Checks:

```text
document structure

schema

tables

citations

locators

cross-reference syntax

machine extraction fidelity.
```

---

# 27. Source Verifier

Checks:

```text
source identity

authority

official status

authenticity

version

publication

rights

source provenance.
```

---

# 28. Regulatory Analyst

Evaluates:

```text
normative meaning

conditions

exceptions

actor roles

requirements

temporal effects

jurisdictional applicability.
```

---

# 29. Jurisdiction Specialist

Provides deeper competence for:

```text
jurisdiction-specific drafting

hierarchy

regulatory institutions

legal conventions

regional regimes.
```

---

# 30. Legal Reviewer

Where required by governance, a legal reviewer evaluates interpretation requiring:

```text
professional legal judgment

legal hierarchy

material ambiguity

complex statutory construction

case-law interaction.
```

---

# 31. Legal Reviewer Is Not Mandatory for Every Extraction

Baobab SHALL avoid making the architecture economically impossible by requiring legal counsel to verify:

```text
every title

every citation

every obvious effective date

every OCR correction.
```

Review SHALL be proportional to semantic risk.

---

# 32. Rule Engineer

Checks:

```text
RuleVersion

BRIR

conditions

types

unknown semantics

exception encoding

test cases

compiler behaviour.
```

---

# 33. Checker

An independent reviewer who validates the maker's substantive work.

---

# 34. Publication Approver

Authorises:

```text
promotion into published canonical state
```

subject to all required controls.

---

# 35. Quality Auditor

Samples completed work and tests whether governance controls are operating effectively.

The auditor SHOULD be independent from routine maker/checker activity where practical.

---

# 36. Reviewer Does Not Need Every Role

One individual MAY hold several permitted capabilities.

However separation-of-duty constraints govern which combinations may be exercised on the same artefact.

---

# 37. Governance Object

Baobab SHALL define:

# `RegulatoryReviewPolicy`

---

# 38. RegulatoryReviewPolicy

Conceptually:

```text
RegulatoryReviewPolicy
├── policy_id
├── policy_version
├── candidate_type
├── jurisdiction_scope?
├── domain_scope?
├── source_class?
├── AI_assistance_class
├── required_review_route
├── required_competence[]
├── independence_rules[]
├── review_sampling_policy?
├── required_tests[]
├── required_approvals[]
├── maximum_effect_class
├── emergency_policy?
├── effective_period
└── provenance
```

---

# 39. Review Route

Initial `ReviewRoute` values SHOULD include:

```text
AUTO_STRUCTURAL_VALIDATION

QUALIFIED_SINGLE_REVIEW

INDEPENDENT_MAKER_CHECKER

SPECIALIST_REVIEW

LEGAL_REVIEW

EXTERNAL_AUTHORITY_REQUIRED.
```

---

# 40. These Are Routes, Not Confidence Levels

They SHALL NOT be interpreted as:

```text
0–5 confidence scores.
```

---

# 41. AI Assistance Classes from ADR-REG-0021

Recall:

```text
AI-A0 Structural Transformation

AI-A1 Descriptive Extraction

AI-A2 Semantic Extraction

AI-A3 Interpretive Candidate

AI-A4 Executable Rule Candidate

AI-A5 Presentation.
```

---

# 42. Initial Review Matrix

| AI class | Example | Initial review policy |
|---|---|---|
| A0 | OCR/layout/table segmentation | deterministic validation + sampling |
| A1 | title, authority, publication date | validation; selective auto-promotion where directly observable |
| A2 | obligation/condition/exception extraction | qualified review initially; limited controlled automation after TEVV evidence |
| A3 | legal interpretation | mandatory qualified substantive review |
| A4 | RuleVersion / BRIR candidate | independent maker-checker + rule-engineering tests |
| A5 | explanation/summary | grounding validation; human review according to audience/consequence |

---

# 43. E3/E4 Rule Publication

A RuleVersion capable of contributing to:

```text
E3

E4
```

SHALL initially require:

```text
qualified maker

independent checker

required rule-engineering tests

publication approval.
```

---

# 44. E4 Additional Requirement

E4-capable regulatory logic SHOULD also require a reviewer with appropriate:

```text
jurisdiction

domain

legal/regulatory competence
```

where substantive interpretation is involved.

---

# 45. Same Person Cannot Be Maker and Checker

Where maker-checker is required:

```text
maker_ref
≠
checker_ref.
```

---

# 46. Dynamic Separation of Duty

The platform SHALL enforce this at approval time.

This follows the mature separation-of-duty principle that sensitive actions should not be exercisable by one actor alone.

---

# 47. Role Possession Does Not Bypass Same-Object Constraint

A person who possesses both:

```text
RULE_MAKER

RULE_CHECKER
```

roles MAY perform either role generally.

They SHALL NOT perform both on the same governed item where independence is required.

---

# 48. History-Based Separation of Duty

Baobab SHOULD support:

```text
the person who materially authored
Candidate X
cannot later independently check X.
```

---

# 49. Reviewer Independence

Independence MAY consider:

```text
different principal

different workflow role

different team where required

absence of material conflict of interest.
```

---

# 50. Blind Checker Mode

For high-consequence or calibration workflows, Baobab SHOULD support an option where the checker:

```text
reviews source and candidate
without seeing the maker's final verdict
until submitting their own assessment.
```

---

# 51. Purpose of Blind Review

This reduces:

```text
anchoring

groupthink

automation bias

deference to senior reviewer.
```

---

# 52. Model Confidence SHOULD Not Be Prominently Displayed to Reviewers

A model saying:

```text
98% confidence
```

can itself create anchoring.

The default review experience SHOULD emphasise:

```text
source

candidate

uncertainties

validation issues
```

rather than persuasive confidence labels.

---

# 53. Confidence Taxonomy

Baobab SHALL distinguish at least four concepts.

```text
MODEL_CONFIDENCE

TASK_PERFORMANCE_EVIDENCE

CANDIDATE_ASSURANCE

VERIFICATION_STATUS.
```

---

# 54. Model Confidence

Examples:

```text
log probability

provider confidence

classifier probability.
```

This is diagnostic model metadata.

---

# 55. Model Confidence Shall Not Authorise Publication

Hard invariant.

---

# 56. Task Performance Evidence

This describes historical measured performance of a pipeline.

Examples:

```text
exception recall

citation precision

critical miss rate

human correction rate.
```

---

# 57. Candidate Assurance

This describes evidence concerning one candidate.

---

# 58. Verification Status

This describes completed governance actions.

Examples:

```text
UNREVIEWED

SINGLE_VERIFIED

INDEPENDENTLY_VERIFIED

SPECIALIST_VERIFIED

EXTERNAL_CONFIRMATION_REQUIRED.
```

---

# 59. No Universal Confidence Number

Rejected:

```text
regulatory_confidence = 0.93.
```

---

# 60. Regulatory Knowledge Assurance

Baobab SHALL use a multidimensional:

# `RegulatoryKnowledgeAssurance`

---

# 61. RegulatoryKnowledgeAssurance

Conceptually:

```text
RegulatoryKnowledgeAssurance
├── source_authority_state
├── source_authenticity_state
├── source_integrity_state
├── rights_state
├── extraction_fidelity
├── source_grounding
├── citation_integrity
├── cross_reference_completeness
├── amendment_completeness
├── temporal_resolution
├── exception_completeness
├── contradiction_state
├── interpretation_state
├── reviewer_competence_state
├── reviewer_independence_state
├── verification_state
├── test_state
├── publication_state
└── unresolved_issues[]
```

---

# 62. Assurance Is Evidence, Not Arithmetic

These dimensions SHALL not be summed into:

```text
87/100.
```

---

# 63. Why No Aggregate Score

A candidate may be:

```text
perfectly extracted
```

but:

```text
from a non-authoritative source.
```

An average score could conceal this fatal defect.

---

# 64. Another Example

A rule may have:

```text
excellent authoritative source
```

but:

```text
unresolved exception.
```

Again, no average should obscure the critical weakness.

---

# 65. Hard Gates

Certain assurance dimensions SHALL act as hard gates.

Examples:

```text
fabricated citation

unknown authoritative source

material unresolved exception

unresolved legal conflict

missing required independent review.
```

---

# 66. Gate Outcome

Potential:

```text
PASS

PASS_WITH_CONDITIONS

REVIEW_REQUIRED

BLOCKED

NOT_APPLICABLE.
```

---

# 67. Candidate Lifecycle

Candidate artifacts SHOULD use a lifecycle such as:

```text
CREATED
   ↓
MACHINE_VALIDATED
   ↓
TRIAGED
   ↓
AWAITING_REVIEW
   ↓
IN_REVIEW
   ├──► CHANGES_REQUESTED
   ├──► DISPUTED
   ├──► REJECTED
   └──► VERIFIED
              ↓
          APPROVED
              ↓
          PROMOTED
```

---

# 68. Canonical Lifecycle Is Separate

Promotion creates or advances the canonical domain object.

For example:

```text
CandidateRule
       ↓
PROMOTED
       ↓
RegulatoryRuleVersion
```

---

# 69. Candidate Is Not Mutated Into Canonical Object

Maintain lineage:

```text
Candidate C123
    GENERATED
        ↓
RuleVersion R17:v4.
```

---

# 70. Review Decision

Every human review SHALL produce a:

# `ReviewDecision`

---

# 71. ReviewDecision

Conceptually:

```text
ReviewDecision
├── review_decision_id
├── candidate_ref
├── reviewer_ref
├── reviewer_role
├── competence_profile_ref
├── review_scope
├── decision
├── reason_codes[]
├── comments?
├── proposed_changes?
├── supporting_evidence_refs[]
├── reviewed_candidate_version
├── decided_at
└── provenance
```

---

# 72. Review Decisions

Possible:

```text
APPROVE

APPROVE_WITH_CHANGES

REQUEST_CHANGES

REJECT

ESCALATE

ABSTAIN

DISPUTE.
```

---

# 73. Abstention Is Valid

A reviewer SHOULD be able to say:

```text
OUTSIDE_MY_COMPETENCE.
```

This is a healthy governance outcome.

---

# 74. Reviewers SHALL NOT Be Forced to Choose Yes/No

Where evidence is insufficient:

```text
ESCALATE

ABSTAIN

REQUEST_MORE_EVIDENCE
```

must be available.

---

# 75. Automation Bias Mitigation in Review UX

The review interface SHOULD:

```text
show primary source prominently

show exact source spans

show candidate separately

show unresolved validations

show competing interpretations

allow reject/abstain easily

avoid presenting AI output as default truth.
```

---

# 76. Reviewer Must Be Able to Disregard AI Output

This aligns with contemporary human-oversight principles requiring the human overseer to be able to disregard, override or reverse AI output.

---

# 77. Human Authority Must Be Real

A reviewer who can see an AI recommendation but cannot:

```text
reject it

stop publication

request evidence

escalate
```

is not exercising meaningful oversight.

---

# 78. Rubber-Stamp Detection

Baobab SHOULD monitor patterns such as:

```text
100% approval rate

extremely short review duration

no source interaction

repeated approval despite gold-set failures.
```

These may indicate ineffective review.

---

# 79. Review Metrics Shall Not Punish Appropriate Rejection

Productivity metrics SHALL NOT create incentives to:

```text
approve quickly
```

at the expense of regulatory quality.

---

# 80. Reviewer Calibration

Qualified reviewers SHOULD periodically receive:

```text
known-answer calibration items

gold examples

controlled ambiguous cases.
```

---

# 81. Calibration Purpose

Measure:

```text
competence

consistency

automation bias susceptibility

interpretation divergence.
```

---

# 82. Calibration Is Not Secret Employee Scoring by Default

Its primary purpose is governance quality.

Employment/performance use would require separate policy.

---

# 83. Reviewer Training

Training SHOULD cover:

```text
Baobab regulatory ontology

source hierarchy

jurisdiction model

temporal model

AI limitations

automation bias

candidate review UX

BRIR where relevant

escalation procedures

data confidentiality.
```

---

# 84. Reviewer Training Is Role-Specific

A source verifier needs different training from a BRIR rule engineer.

---

# 85. Review Competence Renewal

Competence SHOULD be periodically:

```text
reviewed

renewed

restricted

expanded
```

based upon:

```text
training

experience

audit findings

domain changes.
```

---

# 86. Candidate Triage

Every candidate SHOULD pass a:

# `ReviewTriage`

---

# 87. ReviewTriage Inputs

Potential:

```text
candidate type

AI assistance class

source class

jurisdiction

regulatory domain

novelty

ambiguity

identified conflicts

materiality

potential effect class

model/pipeline maturity

task performance evidence.
```

---

# 88. Triage Output

```text
required ReviewRoute

required reviewer competence

required independence

required tests

priority

SLA

publication ceiling.
```

---

# 89. Novelty

Candidates involving:

```text
new source format

new jurisdiction

new legal concept

new model

new prompt

new extraction pipeline
```

SHOULD generally receive stricter review.

---

# 90. Novelty Is Separate From Model Confidence

A model may be highly confident on a type of document Baobab has never validated.

Novelty still requires caution.

---

# 91. Consequence Matters

Potential RuleVersion contribution to:

```text
E4
```

requires more governance than:

```text
E0 explanatory metadata.
```

---

# 92. Review Policy Function

Conceptually:

```text
ReviewRequirement =
 f(
   candidate_type,
   semantic_risk,
   consequence,
   novelty,
   measured_pipeline_performance,
   jurisdiction,
   ambiguity,
   source_assurance
 )
```

---

# 93. Mandatory Review Conditions

Initial mandatory human review SHOULD include:

```text
new legal interpretation

new RuleVersion

new BRIR semantics

material exception

legal hierarchy resolution

material ambiguity

tenant counsel interpretation

rule capable of E3/E4 consequence

new jurisdiction pack semantics.
```

---

# 94. Automated Structural Promotion

Baobab MAY permit automated promotion of directly observable low-risk metadata where:

```text
source authoritative

field directly observable

deterministic validation passes

pipeline performance proven

no contradiction

sampling controls active.
```

---

# 95. Examples

Potential automated fields:

```text
source file checksum

page count

instrument identifier from verified machine metadata

publication date from authoritative API.
```

---

# 96. Automatic Promotion Shall Be Field-Specific

Do not promote an entire document merely because some metadata fields are reliable.

---

# 97. Semantic Extraction Automation

A2 semantic extraction MAY progress toward controlled automation only after sufficient TEVV evidence.

---

# 98. Initial Conservative Policy

At first production maturity:

```text
obligation extraction

exception extraction

effective-date interpretation

legal actor identification
```

SHOULD remain human-reviewed where they contribute to executable rules.

---

# 99. Sampling

Baobab SHALL support review sampling for appropriate lower-risk automation.

---

# 100. Sampling Is a Governance Mechanism

It is not:

```text
randomly ignore most errors.
```

---

# 101. ReviewSamplingPolicy

Conceptually:

```text
ReviewSamplingPolicy
├── policy_id
├── task_profile
├── population_scope
├── minimum_sample_rate
├── sampling_method
├── strata[]
├── mandatory_review_conditions[]
├── escalation_thresholds[]
├── stop_rules[]
├── audit_frequency
└── effective_period
```

---

# 102. Sampling Methods

Potential:

```text
RANDOM

STRATIFIED

RISK_WEIGHTED

TARGETED

CONTINUOUS_AUDIT.
```

---

# 103. Stratification

Samples SHOULD include important categories such as:

```text
jurisdiction

document type

language

source quality

new source

rare clause type

exception presence

table-heavy document.
```

---

# 104. Pure Random Sampling Is Insufficient

Rare but dangerous errors such as:

```text
missed prohibition exception
```

may occur too infrequently to be reliably discovered through simple random samples.

---

# 105. Mandatory Review Overrides Sampling

Certain items are always reviewed even under automated workflows.

Examples:

```text
negative/exception clauses

new jurisdiction

novel amendment type

low OCR quality

cross-reference failure

critical source conflict.
```

---

# 106. Review Rate Can Increase Automatically

If error rates rise:

```text
10% sample
→
25%
→
50%
→
100%.
```

The exact percentages belong in operational policy.

---

# 107. Review Rate Can Decrease Only Through Governance

Reduced review SHALL require evidence.

It SHALL NOT happen because:

```text
queue is too large.
```

---

# 108. Automation Maturity

Baobab SHOULD maintain task-specific:

# `AutomationMaturityState`

---

# 109. AutomationMaturityState

Potential:

```text
EXPERIMENTAL

HUMAN_ASSISTED

SUPERVISED_AUTOMATION

CONTROLLED_AUTOMATION.
```

---

# 110. Experimental

Every output reviewed.

No automated canonical promotion.

---

# 111. Human-Assisted

AI performs much of extraction.

Human reviews every consequential item.

---

# 112. Supervised Automation

Certain low-risk results auto-promote.

Samples and mandatory-review triggers remain active.

---

# 113. Controlled Automation

A mature, narrowly defined task may operate largely automatically under:

```text
continuous monitoring

sampling

drift controls

rollback

hard exceptions.
```

---

# 114. Controlled Automation Does Not Mean Autonomous Legal Interpretation

Initial policy:

> **A3 interpretive candidates and A4 executable-rule candidates SHALL not progress to unsupervised legal publication merely because extraction metrics improve.**

---

# 115. Why

Accuracy on historical examples does not automatically establish:

```text
authority to interpret novel law.
```

---

# 116. Automation Scope Is Narrow

Example:

```text
"Extract publication date
from South African Gazette metadata"
```

may achieve controlled automation.

That does not authorise:

```text
"Interpret all South African law automatically."
```

---

# 117. Performance Evidence

Automation-maturity decisions SHOULD use multiple measures.

---

# 118. Measurement Dimensions

Potential:

```text
precision

recall

critical false-negative rate

critical false-positive rate

citation validity

exception recall

amendment recall

human edit rate

review disagreement rate

drift rate.
```

---

# 119. Average Accuracy Is Insufficient

A system with:

```text
99% average accuracy
```

but poor performance on:

```text
legal exceptions
```

may be unsuitable.

---

# 120. Critical Error Classes

Baobab SHOULD define:

```text
CRITICAL

MAJOR

MINOR

PRESENTATIONAL.
```

for governance measurement.

---

# 121. Critical Error Examples

Potential:

```text
fabricated legal citation

missed prohibition

missed exception

wrong effective date

wrong jurisdiction

wrong legal actor

reversed obligation/prohibition

published repealed rule.
```

---

# 122. Critical Error Tolerance

Some critical error classes MAY have:

```text
zero tolerated observed errors
```

within a release evaluation corpus.

---

# 123. TEVV Evidence Is Version-Specific

Performance evidence SHALL bind to:

```text
model version

prompt version

retrieval profile

pipeline version

source class

jurisdiction/domain.
```

---

# 124. Model Upgrade Resets Relevant Assurance

A materially changed model SHALL not inherit full automation maturity blindly.

---

# 125. Prompt Change Can Matter Equally

A prompt change may alter:

```text
exception extraction

citation behaviour

classification.
```

Relevant evaluations SHALL rerun.

---

# 126. Retrieval Change Can Matter

Changing:

```text
embedding

top-k

reranker

filters
```

can change candidate quality.

---

# 127. Reviewer Disagreement

Baobab SHALL treat meaningful disagreement as first-class information.

---

# 128. DISPUTED State

Where maker and checker materially disagree:

```text
Candidate = DISPUTED.
```

---

# 129. Disagreement Does Not Auto-Resolve by Seniority

Rejected:

```text
senior reviewer always wins.
```

---

# 130. Disagreement Does Not Auto-Resolve by Majority Vote

Legal interpretation may not be suitable for:

```text
2 votes versus 1.
```

---

# 131. Dispute Resolution

Potential path:

```text
Maker
  │
  ▼
Checker disagreement
  │
  ▼
DISPUTED
  │
  ▼
Specialist reviewer
  │
  ▼
Legal reviewer where required
  │
  ▼
Resolution
```

---

# 132. InterpretationResolution

Conceptually:

```text
InterpretationResolution
├── resolution_id
├── candidate_ref
├── competing_positions[]
├── supporting_sources[]
├── resolving_authority
├── selected_interpretation?
├── unresolved_questions[]
├── reason
├── resolved_at
└── provenance
```

---

# 133. Unresolved Dispute Is Valid

Outcome MAY be:

```text
UNRESOLVED.
```

---

# 134. Consequence of Unresolved Dispute

Potential:

```text
do not publish executable rule

publish representational knowledge only

effect ceiling E1/E2

mark review required.
```

---

# 135. Alternative Interpretations May Be Preserved

Especially where:

```text
law genuinely contested

tenant counsel differs

jurisdictions differ

guidance conflicts.
```

---

# 136. Baobab Need Not Pretend One Answer Exists

The canonical model from ADR-REG-0003 and `0009` supports interpretive plurality where legally appropriate.

---

# 137. Tenant Interpretation

A tenant-specific counsel interpretation MAY be approved for:

```text
tenant overlay
```

without becoming:

```text
shared global interpretation.
```

---

# 138. Global Shared Interpretation Requires Appropriate Authority

Tenant approval alone is insufficient.

---

# 139. Conflict of Interest

Reviewers SHOULD disclose and, where policy requires, be excluded from review where they have a material conflict affecting independence.

---

# 140. Conflict Example

A reviewer who authored a tenant legal opinion should not serve as the supposedly independent checker of that same opinion's canonicalisation where independence is required.

---

# 141. Review Assignment

The workflow SHOULD select reviewers based on:

```text
competence

authorization

independence

availability

tenant constraints.
```

---

# 142. Assignment Shall Not Be Random Alone

A random available user may lack required legal/regulatory competence.

---

# 143. ReviewAssignment

Conceptually:

```text
ReviewAssignment
├── review_case_ref
├── required_role
├── required_competence
├── independence_constraints
├── assignee_ref
├── assigned_at
├── accepted_at?
├── due_at?
└── status
```

---

# 144. ReviewCase

A canonical:

```text
ReviewCase
```

SHALL be persisted in Regulations.

---

# 145. ReviewCase

Conceptually:

```text
ReviewCase
├── review_case_id
├── candidate_ref
├── review_policy_ref
├── required_route
├── current_stage
├── assignments[]
├── decisions[]
├── unresolved_issues[]
├── escalation_state
├── SLA
├── created_at
├── completed_at?
└── provenance
```

---

# 146. LangGraph Orchestrates ReviewCase

LangGraph SHALL:

```text
route

pause

resume

assign

escalate

coordinate.
```

---

# 147. PostgreSQL Owns ReviewCase

Canonical state remains Regulations-owned PostgreSQL.

---

# 148. LangGraph Checkpoint Is Not Approval Evidence

Hard invariant.

---

# 149. Human Decision Must Become Canonical Domain State

An `interrupt()` response such as:

```text
approved=true
```

SHALL result in a canonical:

```text
ReviewDecision
```

being persisted.

---

# 150. LangGraph Human-in-the-Loop

Current LangGraph documentation supports persistent checkpoints and `interrupt()`-based flows that pause and later resume once human input is provided.

That mechanism is suitable for workflow orchestration.

It is not itself the regulatory governance model.

---

# 151. Workflow Resumption

A workflow may resume:

```text
hours

days

weeks
```

later.

---

# 152. Review Context Must Be Revalidated on Resume

If, while paused:

```text
candidate superseded

source corrected

reviewer's authority expired

policy changed
```

the workflow SHALL detect this before accepting the review.

---

# 153. Stale Review

Result:

```text
REVIEW_CONTEXT_STALE.
```

---

# 154. Reviewer Approval Binds to Candidate Version

ReviewDecision SHALL identify:

```text
reviewed_candidate_version.
```

---

# 155. Candidate Mutation Invalidates Prior Approval Where Material

Do not approve version 3 and publish version 4 silently.

---

# 156. Minor Presentation Changes

Policies MAY identify changes that do not invalidate substantive approval.

Such rules SHALL be explicit.

---

# 157. Maker-Checker Candidate Version

Checker SHALL review the actual version proposed for promotion.

---

# 158. Promotion Command

Canonical promotion SHOULD occur through:

```text
PromoteRegulatoryCandidate
```

or domain-specific equivalents.

---

# 159. Promotion Preconditions

Command handler SHALL independently verify:

```text
correct candidate version

required ReviewDecisions exist

reviewers distinct

reviewers competent

review authority valid

all hard gates pass

tests pass

candidate not disputed

candidate not superseded.
```

---

# 160. Workflow Cannot Bypass Domain Preconditions

Even if LangGraph has a bug:

```text
database promotion command
```

shall still reject invalid state.

---

# 161. Defence in Depth

```text
Workflow says approved
        │
        ▼
Domain promotion handler
        │
        ├── verifies approval evidence
        ├── verifies separation of duty
        ├── verifies tests
        └── promotes only if valid.
```

---

# 162. Publication Approval

Publication is distinct from substantive verification.

---

# 163. Why

A verified rule may not yet be publishable because:

```text
effective date future

jurisdiction pack incomplete

commercial release delayed

rights issue unresolved

testing incomplete.
```

---

# 164. PublicationAuthority

A separate capability SHOULD govern:

```text
PUBLISH.
```

---

# 165. Publication Is Consequential Configuration Change

For E3/E4-capable rules it SHOULD integrate with platform controlled-change principles.

---

# 166. Emergency Governance

Regulatory environments occasionally require rapid response.

Examples:

```text
emergency customs prohibition

immediate tariff change

public-health restriction

urgent regulator notice.
```

---

# 167. Emergency Does Not Mean Ungoverned

Hard invariant:

> **Emergency publication may compress process duration; it SHALL NOT erase provenance, authority or accountability.**

---

# 168. EmergencyPromotionCase

Conceptually:

```text
EmergencyPromotionCase
├── emergency_case_id
├── candidate_ref
├── emergency_basis
├── source_ref
├── urgency
├── required_activation_time
├── compressed_controls[]
├── deferred_controls[]
├── temporary_effect_ceiling
├── approvers[]
├── expires_at?
└── provenance
```

---

# 169. Controls That Emergency SHALL NOT Skip

At minimum:

```text
source identity

source authenticity/integrity

legal-effective time

candidate provenance

independent approval where required

audit trail.
```

---

# 170. Emergency Interpretive Ambiguity

If substantive interpretation remains unresolved:

```text
effect ceiling SHOULD remain E2
```

until normal verification completes.

---

# 171. Emergency E4

Emergency status SHALL NOT automatically justify E4.

E4 still requires normal high-assurance conditions.

---

# 172. Temporary Publication

A temporary emergency artefact MAY carry:

```text
expires_at

mandatory_review_by

temporary_effect_ceiling.
```

---

# 173. Deferred Controls

Any compressed/deferred control SHALL be explicitly recorded.

---

# 174. Post-Emergency Review

Emergency publication SHALL trigger:

```text
mandatory retrospective full review.
```

---

# 175. External Authority Required

Some regulatory questions cannot be resolved by Baobab reviewers.

---

# 176. Examples

```text
regulator discretion

official tariff-classification ruling

court interpretation

licensing-authority determination

binding customs ruling.
```

---

# 177. Correct State

```text
EXTERNAL_AUTHORITY_REQUIRED.
```

---

# 178. Human Review Cannot Manufacture External Authority

Even highly qualified counsel cannot transform:

```text
pending regulator determination
```

into:

```text
authority has decided.
```

---

# 179. ExternalAuthorityDecision

When received, it SHOULD be represented as:

```text
ExternalAuthorityDecision
├── authority_ref
├── decision_type
├── subject
├── decision_reference
├── legal_scope
├── valid_period
├── source/evidence_ref
└── provenance
```

---

# 180. External Decision May Then Become Fact

Subject to verification.

---

# 181. Review Escalation Triggers

Mandatory escalation SHOULD include:

```text
material reviewer disagreement

authority ambiguity

unresolved legal hierarchy

ambiguous exception

conflicting official sources

translation materially changes meaning

classification dispute

temporal ambiguity

novel precedent-sensitive issue

external discretion required.
```

---

# 182. EscalationRoute

Potential:

```text
DOMAIN_SPECIALIST

JURISDICTION_SPECIALIST

LEGAL_REVIEW

TENANT_COUNSEL

EXTERNAL_COUNSEL

COMPETENT_AUTHORITY.
```

---

# 183. Escalation Is Not Failure

In a sound regulatory system:

```text
"I cannot safely determine this"
```

is often the correct state.

---

# 184. Review SLAs

Governance SHOULD support deadlines.

However:

```text
SLA expiry
```

SHALL NOT auto-approve a regulatory candidate.

---

# 185. SLA Expiry

Possible outcome:

```text
ESCALATED

OVERDUE

COVERAGE_DELAYED.
```

Never:

```text
APPROVED_BY_TIMEOUT.
```

---

# 186. No Default Approval

Hard invariant.

---

# 187. Reviewer Absence

If qualified reviewer unavailable:

```text
publication waits
```

or:

```text
effect ceiling reduced.
```

---

# 188. Queue Prioritisation

Review priority MAY consider:

```text
legal effective date

customer exposure

number of affected transactions

potential prohibition

jurisdiction importance

regulatory-change urgency.
```

---

# 189. Pulse May Inform Priority

Pulse MAY indicate:

```text
commercial exposure
```

or:

```text
affected transaction volume.
```

---

# 190. Pulse Cannot Approve Candidate

Again, commercial impact does not determine legal truth.

---

# 191. Review Corrections as Learning Data

Reviewer changes MAY be captured as:

```text
CandidateCorrection
```

for improving pipelines.

---

# 192. CandidateCorrection

Potential:

```text
original candidate

reviewed result

error category

source support

reviewer explanation.
```

---

# 193. Corrections Do Not Automatically Train Models

Use for:

```text
training

fine tuning

prompt improvement
```

requires rights and model-governance approval.

---

# 194. Corrections Should Feed Benchmarks

Safe default:

```text
verified correction
→ regression test fixture.
```

---

# 195. Feedback Loop

```text
Candidate
   ↓
Human Review
   ↓
Correction
   ↓
Gold Fixture
   ↓
TEVV
   ↓
Pipeline Improvement
   ↓
Candidate
```

---

# 196. This Is Controlled Learning

Not:

```text
model learns automatically
from every reviewer click.
```

---

# 197. Reviewer Disagreement Also Feeds Evaluation

High disagreement may indicate:

```text
ambiguous law

poor source presentation

poor AI extraction

insufficient reviewer guidance.
```

---

# 198. Review Quality Metrics

Useful metrics include:

```text
first-pass acceptance

edit rate

rejection rate

disagreement rate

critical error escape rate

audit correction rate

review turnaround time

reviewer calibration accuracy

automation override rate.
```

---

# 199. Metrics Must Be Interpreted Carefully

High approval rate can mean:

```text
excellent model
```

or:

```text
rubber-stamping.
```

Metrics need contextual interpretation.

---

# 200. Audit Sampling

Published artefacts SHOULD be subject to independent retrospective sampling.

---

# 201. Audit Review

Auditor SHOULD compare:

```text
source

candidate

review decisions

published artefact

tests

workflow compliance.
```

---

# 202. Audit Finding

Potential:

```text
CONFORMANT

PROCESS_DEVIATION

SEMANTIC_DEFECT

COMPETENCE_GAP

SYSTEMIC_MODEL_ERROR

CONTROL_FAILURE.
```

---

# 203. Audit Defect May Trigger Reassessment

Where published regulatory knowledge is defective:

```text
ADR-REG-0023
```

will govern downstream impact analysis.

---

# 204. Reviewer Performance and Candidate Performance Remain Separate

Do not assume:

```text
human approved
therefore correct.
```

---

# 205. Independent Verification

Independent verification and validation is an established assurance concept involving review/testing by an objective party to confirm requirements and implementation.

Baobab SHALL adopt this principle selectively where consequences justify it.

---

# 206. Legal Review Independence

For particularly consequential interpretations, review policy MAY require:

```text
external legal reviewer

tenant counsel

second internal specialist.
```

---

# 207. Not Every Customer Needs Same Governance

Tenant agreements MAY define:

```text
who has authority
to approve tenant-specific interpretation.
```

---

# 208. Shared Baobab Knowledge Has Higher Governance Burden

An interpretation published to all tenants SHOULD generally require stronger governance than:

```text
one tenant's private overlay.
```

---

# 209. Shared Rule

Potential audience:

```text
all platform clients.
```

Error blast radius is larger.

---

# 210. Tenant Rule

Blast radius is bounded.

Governance may differ.

---

# 211. Effect-Class Governance

Review policy SHALL integrate with:

```text
E0

E1

E2

E3

E4
```

from ADR-REG-0004.

---

# 212. E0

May permit:

```text
automated metadata

informational interpretation
```

subject to source and disclosure policy.

---

# 213. E1

May permit qualified single review for many advisory interpretations.

---

# 214. E2

Material ambiguity is compatible with:

```text
review-required operational use.
```

Publication should clearly preserve limitations.

---

# 215. E3

Requires:

```text
stronger verification

maker-checker

deterministic rule tests

resolved material ambiguity.
```

---

# 216. E4

Requires strongest governance.

---

# 217. E4 Publication Gate

An E4-capable RuleVersion SHOULD require:

```text
verified authoritative source

resolved rights

verified interpretation

competent maker

independent checker

specialist/legal review where substantive interpretation requires it

BRIR validation

golden regulatory tests

regression tests

no material dispute

publication approval.
```

---

# 218. E4 Reviewer Identity

Review decisions SHALL be attributable to actual authorised principals.

---

# 219. Shared Credentials Prohibited

Review actions SHALL NOT occur under:

```text
regulations-admin@example
```

shared identity.

---

# 220. Auditability Requires Individual Attribution

---

# 221. Reviewer Authentication Assurance

High-consequence approvals MAY require stronger IAM assurance.

Examples:

```text
MFA

passkey

step-up authentication.
```

Exact identity policy remains under IAM architecture.

---

# 222. Approval Session Context

Approval record MAY include:

```text
authentication assurance level

session ID

client context
```

without duplicating IAM semantics.

---

# 223. Approval Cannot Be Performed by AI Agent Identity

AI service principal may:

```text
create candidate

run validation.
```

It SHALL NOT satisfy human-review requirements.

---

# 224. Machine Checker ≠ Independent Human Checker

A second model is not:

```text
maker-checker separation
```

for policies requiring two humans.

---

# 225. Machine Verification Still Valuable

Deterministic validators SHOULD operate before humans.

---

# 226. Humans Should Not Waste Time on Machine-Detectable Errors

Examples:

```text
missing citation

invalid date

unknown authority ID

BRIR type error.
```

These should fail before human review.

---

# 227. Review Funnel

Preferred:

```text
Machine candidate
      │
      ▼
Schema validation
      │
      ▼
Source/citation validation
      │
      ▼
Cross-reference validation
      │
      ▼
Temporal validation
      │
      ▼
Automated consistency checks
      │
      ▼
Human semantic review
      │
      ▼
Independent check
      │
      ▼
Tests
      │
      ▼
Promotion.
```

---

# 228. Reviewer Interface Shall Surface Validation Results

Do not require reviewer to rediscover all machine-detectable defects.

---

# 229. But Machine Pass Does Not Bias Toward Approval

UI SHOULD display:

```text
validation passed
```

as technical evidence.

Not:

```text
AI says this is correct.
```

---

# 230. Reviewer Explanation

Consequential approval SHOULD include:

```text
structured reason
```

not merely:

```text
Approved.
```

---

# 231. Reason Codes

Potential:

```text
SOURCE_DIRECTLY_SUPPORTS

INTERPRETATION_CONSISTENT_WITH_DEFINED_TERM

EXCEPTION_CORRECTLY_CAPTURED

TEMPORAL_SCOPE_VERIFIED

CROSS_REFERENCE_RESOLVED

RULE_SEMANTICS_VERIFIED

BRIR_EQUIVALENT_TO_RULE.
```

---

# 232. Rejection Reason Codes

Potential:

```text
SOURCE_UNSUPPORTED

WRONG_AUTHORITY

CITATION_INVALID

MISSED_EXCEPTION

WRONG_NORMATIVE_EFFECT

TEMPORAL_ERROR

JURISDICTION_ERROR

CROSS_REFERENCE_INCOMPLETE

INTERPRETATION_UNSUPPORTED

BRIR_SEMANTIC_MISMATCH.
```

---

# 233. Structured Reasons Enable Metrics

They also become:

```text
gold test categories

pipeline-improvement data.
```

---

# 234. Reviewer Free Text Is Supplemental

Free text may be useful.

Canonical governance should still use structured reason codes.

---

# 235. Reviewer Cannot Alter Source Evidence

A reviewer may:

```text
reject extraction

correct normalized representation

add interpretation.
```

They SHALL NOT mutate immutable raw SourceArtefact.

---

# 236. Source Correction Is Separate

If source itself is corrected/replaced:

```text
new SourceArtefact / SourceVersion
```

is created according to prior ADRs.

---

# 237. Review of Translation

Translations MAY require reviewers competent in:

```text
source language

target language

relevant legal domain.
```

---

# 238. Translation Reviewer

A general translator may not be sufficient for legally material translation.

---

# 239. Official Translation

If an official translation exists:

```text
authority status
```

must be preserved.

---

# 240. Human Translation Is Still Derived

Unless authority itself designates it official.

---

# 241. Regulatory Knowledge Governance Board

As the platform matures, Baobab SHOULD support a governance function or board responsible for:

```text
review policy

effect ceilings

reviewer competence

automation maturity

critical incidents

jurisdiction-pack approval.
```

---

# 242. This Need Not Be a Large Committee

It is an accountability function.

It may begin with a small set of authorised roles.

---

# 243. Governance Board Does Not Interpret Every Rule

It establishes:

```text
policy

authority

escalation

risk tolerance.
```

---

# 244. ReviewPolicy Change

A material policy change SHALL be versioned.

---

# 245. Historical Approvals Use Historical Policy

Do not apply today's ReviewPolicy retroactively when explaining:

```text
why Rule R was published in 2027.
```

---

# 246. New Policy May Trigger Retrospective Audit

A stricter new policy MAY trigger review of older artefacts.

That is:

```text
revalidation
```

not historical rewrite.

---

# 247. Knowledge Revalidation

Published regulatory knowledge MAY require periodic revalidation.

---

# 248. Revalidation Triggers

Examples:

```text
source updated

source trust degraded

model/pipeline incident

jurisdiction change

new conflicting authority

reviewer qualification issue

audit finding.
```

---

# 249. Revalidation Does Not Automatically Depublish

Outcome depends on severity.

---

# 250. Possible States

```text
REVALIDATION_REQUIRED

UNDER_REVIEW

SUSPENDED

DEPRECATED

SUPERSEDED.
```

---

# 251. Suspension

Material concern may temporarily prevent:

```text
E3/E4 use
```

while retaining knowledge for research/audit.

---

# 252. Confidence Degradation

Baobab SHALL not say:

```text
confidence dropped from 91 to 67.
```

Instead:

```text
source trust degraded

review now stale

new contradiction detected

revalidation required.
```

---

# 253. Review Freshness

Some approvals may remain valid indefinitely until source changes.

Others may require periodic review.

Policy-specific.

---

# 254. Legal Rule Does Not Expire Because Reviewer Training Expires

If the reviewer later loses authorization:

```text
historical verified artefact
```

does not automatically become legally false.

---

# 255. But Governance May Require Revalidation

Especially if qualification was later found invalid.

---

# 256. Review Incident

Baobab SHOULD define:

# `RegulatoryGovernanceIncident`

---

# 257. Governance Incident Examples

```text
unauthorised reviewer

same maker/checker

fabricated reviewer identity

rubber-stamping evidence

candidate version mismatch

promotion without test

AI bypassed promotion gate

critical audit defect.
```

---

# 258. Governance Incident May Reduce Effect Ceiling

Example:

```text
E4 rule
      ↓
governance defect found
      ↓
temporarily limited to E2
```

pending revalidation.

---

# 259. Incident Blast Radius

Use the knowledge/decision graph:

```text
defective review
   ↓
RuleVersions
   ↓
Decisions
   ↓
Enforcement.
```

---

# 260. ADR-REG-0023 Will Own Formal Impact Analysis

This ADR establishes the governance event.

---

# 261. Continuous TEVV

Baobab SHALL continuously evaluate:

```text
models

retrievers

parsers

workflow

reviewers

published outcomes.
```

---

# 262. System-Level TEVV

Important distinction:

```text
model benchmark
≠
system assurance.
```

---

# 263. Example

A model can have excellent extraction accuracy while:

```text
workflow allows same user
to publish without review.
```

The system remains weak.

---

# 264. Another Example

Reviewer process may be excellent while:

```text
retriever systematically omits amendments.
```

Again, system weak.

---

# 265. NIST TEVV Alignment

NIST's current TEVV direction emphasises assessment of AI systems in their actual intended context rather than model-only metrics.

Baobab SHALL therefore evaluate the complete:

```text
Docling
→ Haystack
→ Qdrant
→ model
→ LangGraph
→ reviewer
→ promotion
```

system.

---

# 266. Governance Dashboard

A future operational dashboard SHOULD surface:

```text
candidate backlog

review backlog

overdue reviews

disputed items

critical extraction errors

automation maturity

review sampling status

reviewer coverage

jurisdiction coverage

pending revalidation

governance incidents.
```

---

# 267. Dashboard Is Not Authority

Metrics support governance.

They do not publish regulatory knowledge.

---

# 268. Reviewer Capacity Is a Product Constraint

Baobab SHOULD measure:

```text
verified artefacts per reviewer hour

review latency

error reduction

automation leverage.
```

---

# 269. Commercial Importance

If every provision requires many hours of expert legal review, jurisdiction expansion will not scale economically.

---

# 270. But Cost Reduction Cannot Override Assurance

The correct objective is:

```text
automate machine-verifiable work

focus human expertise
where semantic judgment matters.
```

---

# 271. Progressive Human-Leverage Strategy

```text
Phase 1
AI assists; humans review most semantics.

Phase 2
structural/descriptive extraction largely automated.

Phase 3
mature semantic extraction uses controlled sampling.

Phase 4
humans concentrate on ambiguity, novelty,
legal interpretation and consequential rule approval.
```

---

# 272. Human Review Does Not Disappear

It becomes:

```text
targeted

specialised

high-leverage.
```

---

# 273. AI Literacy

The EU AI Act's oversight model and NIST governance both emphasise that overseers must understand AI-system capabilities and limitations.

Baobab reviewer training SHALL therefore include:

```text
how the AI pipeline can fail.
```

---

# 274. Legal Expertise Without AI Literacy Is Not Enough

A reviewer who believes:

```text
the model found all relevant provisions
```

without understanding retrieval limitations may over-trust the system.

---

# 275. AI Expertise Without Legal Expertise Is Not Enough

A model engineer may validate:

```text
JSON schema
```

but should not independently decide:

```text
whether a statutory exception defeats a prohibition.
```

---

# 276. Interdisciplinary Governance

This is a socio-technical system.

ISO and NIST both emphasise organisational/process controls alongside technical AI performance.

---

# 277. Responsibilities Must Therefore Be Explicit

```text
AI engineer
≠
regulatory analyst

regulatory analyst
≠
publication approver

publication approver
≠
legal authority.
```

---

# 278. Interaction with baobab-pulse

Pulse MAY contribute:

```text
new-source leads

change signals

impact priority.
```

---

# 279. Pulse SHALL NOT Satisfy Human Verification Requirements

Even if Pulse ranks a change:

```text
99% likely material.
```

---

# 280. Regulations → Pulse

After verification:

```text
VerifiedRegulatoryChange
```

may feed Pulse impact analysis.

---

# 281. Interaction with baobab-cms

CMS editorial reviewers MAY improve:

```text
clarity

tone

presentation.
```

---

# 282. CMS Editorial Approval ≠ Regulatory Verification

Hard invariant.

---

# 283. CMS Cannot Upgrade Unverified Regulatory Content

An excellent editor cannot transform:

```text
CandidateInterpretation
```

into:

```text
VerifiedInterpretation.
```

---

# 284. CMS May Require Its Own Editorial Maker-Checker

That remains a CMS concern and separate from regulatory knowledge governance.

---

# 285. Interaction with OPA

OPA SHALL only receive:

```text
published verified BRIR-derived policy.
```

---

# 286. OPA Success Does Not Verify Legal Interpretation

```text
opa test passes
```

means:

```text
policy behaves as encoded.
```

It does not prove:

```text
encoding correctly represents law.
```

---

# 287. Human + Test Complementarity

Correct governance:

```text
legal semantic review
          +
rule-engineering tests
          =
stronger assurance.
```

---

# 288. Neither Alone Is Sufficient for E4

---

# 289. Interaction with PostgreSQL

Canonical governance records SHALL be stored under Regulations ownership in PostgreSQL.

---

# 290. Candidate and Review History SHALL Be Append-Oriented

Material changes should preserve previous versions.

---

# 291. No Silent Review Record Editing

If a reviewer corrects an earlier approval:

```text
new ReviewDecision
```

should supersede or withdraw the old one.

---

# 292. Review Withdrawal

Potential:

```text
ReviewDecision R1
APPROVE

later:
R2 WITHDRAWS R1.
```

---

# 293. Withdrawal Does Not Delete History

---

# 294. Review Events

Potential domain events:

```text
regulation.candidate.created

regulation.candidate.validation-failed

regulation.review.requested

regulation.review.assigned

regulation.review.completed

regulation.review.disputed

regulation.review.escalated

regulation.candidate.verified

regulation.candidate.rejected

regulation.knowledge.promoted

regulation.knowledge.revalidation-required

regulation.governance.incident-detected.
```

---

# 295. Events Are Not Canonical State

PostgreSQL canonical state remains authoritative.

---

# 296. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-GOV-I01` | Human presence SHALL NOT by itself constitute effective oversight |
| `REG-GOV-I02` | Reviewers SHALL possess scoped competence appropriate to the task |
| `REG-GOV-I03` | Reviewer identity SHALL remain attributable to an IAM principal |
| `REG-GOV-I04` | Reviewer competence SHALL remain distinct from platform authorization |
| `REG-GOV-I05` | Model confidence SHALL NOT establish regulatory assurance |
| `REG-GOV-I06` | Regulatory assurance SHALL remain multidimensional |
| `REG-GOV-I07` | Critical assurance defects SHALL operate as hard gates rather than average into scores |
| `REG-GOV-I08` | Candidate creation SHALL remain distinct from verification |
| `REG-GOV-I09` | Verification SHALL remain distinct from publication approval |
| `REG-GOV-I10` | Human verification SHALL NOT manufacture external legal authority |
| `REG-GOV-I11` | Maker and checker SHALL be distinct where independent verification is required |
| `REG-GOV-I12` | Separation of duty SHALL be enforced at runtime, not only documented |
| `REG-GOV-I13` | Review approval SHALL bind to an immutable candidate version |
| `REG-GOV-I14` | Material candidate modification SHALL invalidate prior approval where policy requires |
| `REG-GOV-I15` | AI systems SHALL NOT satisfy mandatory human-review requirements |
| `REG-GOV-I16` | Multi-model agreement SHALL NOT substitute for qualified human verification |
| `REG-GOV-I17` | Reviewer disagreement SHALL be preserved and escalated rather than averaged away |
| `REG-GOV-I18` | Reviewer abstention SHALL be supported |
| `REG-GOV-I19` | SLA expiry SHALL never result in automatic approval |
| `REG-GOV-I20` | Review sampling SHALL be evidence-based and task-specific |
| `REG-GOV-I21` | Critical or novel items SHALL bypass ordinary sampling and receive mandatory review |
| `REG-GOV-I22` | Automation maturity SHALL be version-, task- and domain-specific |
| `REG-GOV-I23` | Model/prompt/retrieval changes SHALL trigger applicable TEVV regression |
| `REG-GOV-I24` | Emergency governance SHALL compress time, not eliminate accountability |
| `REG-GOV-I25` | Emergency status SHALL not by itself authorise E4 |
| `REG-GOV-I26` | External-authority questions SHALL not be resolved through internal reviewer opinion alone |
| `REG-GOV-I27` | LangGraph SHALL orchestrate review but SHALL NOT own canonical approval state |
| `REG-GOV-I28` | Human decisions SHALL be persisted as canonical Regulations domain records |
| `REG-GOV-I29` | Domain promotion handlers SHALL independently verify workflow preconditions |
| `REG-GOV-I30` | AI agents SHALL NOT possess canonical publication authority |
| `REG-GOV-I31` | CMS editorial approval SHALL remain distinct from regulatory verification |
| `REG-GOV-I32` | Pulse prioritisation SHALL remain distinct from legal verification |
| `REG-GOV-I33` | OPA policy correctness SHALL remain distinct from legal-semantic correctness |
| `REG-GOV-I34` | Published regulatory knowledge SHALL remain revalidatable |
| `REG-GOV-I35` | Governance defects affecting consequential rules SHALL be traceable to downstream decisions |

---

# 297. Rejected Alternative — Generic Human-in-the-Loop Checkbox

Rejected.

---

# 298. Rejected Alternative — Any Employee Can Approve

Rejected.

---

# 299. Rejected Alternative — Reviewer Role Without Competence Scope

Rejected.

---

# 300. Rejected Alternative — Seniority Equals Competence

Rejected.

---

# 301. Rejected Alternative — AI Confidence Determines Review Route Alone

Rejected.

---

# 302. Rejected Alternative — 90% Confidence Means Auto-Publish

Rejected.

---

# 303. Rejected Alternative — One Regulatory Confidence Score

Rejected.

---

# 304. Rejected Alternative — Human Approval Automatically Means Legal Truth

Rejected.

---

# 305. Rejected Alternative — Same Person Makes and Checks E4 Rule

Rejected.

---

# 306. Rejected Alternative — Second LLM Counts as Checker

Rejected.

---

# 307. Rejected Alternative — Majority Vote Establishes Law

Rejected.

---

# 308. Rejected Alternative — Reviewer Disagreement Resolved by Confidence Score

Rejected.

---

# 309. Rejected Alternative — Automatic Approval on Timeout

Rejected.

---

# 310. Rejected Alternative — Review Sampling Based Only on Queue Size

Rejected.

---

# 311. Rejected Alternative — Sample Only Random Items

Rejected.

Risk-weighted and mandatory-review strata are required.

---

# 312. Rejected Alternative — Low Average Error Rate Justifies Full Automation

Rejected.

Critical error distribution matters.

---

# 313. Rejected Alternative — Automation Maturity Transfers Across Jurisdictions Automatically

Rejected.

---

# 314. Rejected Alternative — Model Upgrade Inherits Previous Assurance Automatically

Rejected.

---

# 315. Rejected Alternative — Human Reviewer Sees Only AI Summary

Rejected.

Primary source/support SHALL be available.

---

# 316. Rejected Alternative — Model Confidence Shown as Dominant UX Element

Rejected due to anchoring/automation-bias risk.

---

# 317. Rejected Alternative — LangGraph `approved=true` Equals Canonical Approval

Rejected.

---

# 318. Rejected Alternative — Workflow Engine Writes Published Rule Directly

Rejected.

---

# 319. Rejected Alternative — Emergency Means Skip Second Review

Rejected where independent review is a hard gate.

---

# 320. Rejected Alternative — Every Candidate Requires Outside Counsel

Rejected.

Economically and operationally disproportionate.

---

# 321. Rejected Alternative — No Legal Specialist Ever Required

Rejected.

Some interpretations need specialised judgment.

---

# 322. Rejected Alternative — Tenant Counsel Opinion Automatically Becomes Shared Platform Rule

Rejected.

---

# 323. Rejected Alternative — CMS Editor Verifies Law

Rejected.

---

# 324. Rejected Alternative — OPA Test Success Verifies Law

Rejected.

---

# 325. Rejected Alternative — Humans Are Assumed Unbiased

Rejected.

NIST explicitly cautions that human cognitive biases are part of the socio-technical AI system.

---

# 326. Minimum Implementation Proof

Before `ADR-REG-0022` is considered implemented, Baobab SHOULD demonstrate:

```text
1. RegulatoryReviewerProfile schema.

2. IAM principal reference.

3. jurisdiction competence.

4. regulatory-domain competence.

5. language competence.

6. reviewer-type distinction.

7. training reference.

8. qualification evidence.

9. competence expiry.

10. competence suspension.

11. RegulatoryReviewPolicy.

12. policy versioning.

13. AI-A0 review route.

14. AI-A1 review route.

15. AI-A2 review route.

16. AI-A3 mandatory review.

17. AI-A4 maker-checker.

18. A5 presentation validation.

19. RegulatoryKnowledgeAssurance.

20. no aggregate confidence score.

21. hard-gate assurance defect.

22. Candidate lifecycle.

23. ReviewCase aggregate.

24. ReviewAssignment.

25. ReviewDecision.

26. structured approval reason.

27. structured rejection reason.

28. abstention.

29. escalation.

30. source verifier role.

31. regulatory analyst role.

32. jurisdiction specialist role.

33. legal reviewer role.

34. rule engineer role.

35. checker role.

36. publication approver role.

37. auditor role.

38. dynamic separation of duty.

39. maker != checker check.

40. author != checker where required.

41. candidate-version binding.

42. changed candidate invalidates approval.

43. blind-checker mode.

44. model-confidence hidden/default-deemphasised.

45. source side-by-side review.

46. exception highlighted.

47. unresolved issue display.

48. competing interpretation display.

49. reviewer can reject AI.

50. reviewer can abstain.

51. reviewer can request evidence.

52. reviewer can stop promotion.

53. LangGraph review workflow.

54. PostgreSQL-backed durable checkpoint.

55. interrupt/resume.

56. stale reviewer authority detected on resume.

57. stale candidate detected on resume.

58. canonical ReviewDecision persisted after interrupt.

59. LangGraph cannot direct-publish.

60. promotion command.

61. promotion handler revalidates controls.

62. published RuleVersion lineage back to candidate.

63. two-person publication for E3 rule.

64. two-person + specialist path for E4 rule.

65. machine validators before human review.

66. BRIR test gate.

67. golden case gate.

68. ReviewSamplingPolicy.

69. random sampling.

70. stratified sampling.

71. risk-weighted sampling.

72. mandatory-review override.

73. sample-rate increase on quality degradation.

74. return to 100% review after threshold breach.

75. AutomationMaturityState.

76. EXPERIMENTAL state.

77. HUMAN_ASSISTED state.

78. SUPERVISED_AUTOMATION state.

79. CONTROLLED_AUTOMATION state.

80. task-specific maturity.

81. source-class-specific maturity.

82. jurisdiction-specific maturity.

83. pipeline-version-specific TEVV.

84. model change triggers regression.

85. prompt change triggers regression.

86. retriever change triggers regression.

87. embedding change triggers appropriate regression.

88. precision metric.

89. recall metric.

90. critical error metric.

91. exception recall metric.

92. citation hallucination metric.

93. human correction-rate metric.

94. disagreement-rate metric.

95. review turnaround metric.

96. reviewer calibration exercise.

97. calibration failure reduces/suspends competence where policy requires.

98. rubber-stamp detection.

99. ReviewTriage.

100. novelty trigger.

101. consequence trigger.

102. unresolved ambiguity trigger.

103. DISPUTED state.

104. specialist escalation.

105. legal-review escalation.

106. external-authority escalation.

107. InterpretationResolution.

108. preservation of competing interpretations.

109. tenant-private interpretation overlay.

110. shared-rule governance stronger than tenant overlay.

111. reviewer conflict-of-interest declaration.

112. EmergencyPromotionCase.

113. emergency source verification.

114. emergency independent review.

115. temporary effect ceiling.

116. emergency expiry.

117. mandatory retrospective review.

118. emergency cannot auto-authorise E4.

119. EXTERNAL_AUTHORITY_REQUIRED state.

120. ExternalAuthorityDecision record.

121. governance incident model.

122. same-maker-checker incident detection.

123. unauthorized-reviewer incident.

124. promotion-without-test incident.

125. governance incident effect-ceiling reduction.

126. independent audit sampling.

127. audit finding model.

128. published-rule revalidation trigger.

129. source trust degradation revalidation.

130. reviewer qualification issue revalidation.

131. CandidateCorrection.

132. correction → gold fixture.

133. corrections not automatically used for training.

134. TEVV dashboard.

135. review backlog dashboard.

136. disputed-item dashboard.

137. reviewer competence coverage.

138. automation maturity dashboard.

139. critical defect alert.

140. regulatory governance events.

141. Pulse priority input without verification authority.

142. Regulations verified event to Pulse.

143. CMS editorial workflow kept separate.

144. OPA compilation test distinct from legal verification.

145. end-to-end AI candidate → maker → checker → approval → RuleVersion.

146. end-to-end disputed candidate → specialist → resolution.

147. end-to-end emergency change → bounded publication → retrospective review.

148. end-to-end sampled automated metadata → audit catches defect → automation returns to full review.

149. historical reconstruction of who reviewed what under which policy.

150. proof that no model/service principal can satisfy a human-review requirement.
```

---

# 327. Initial ZuriBeans / Uganda → South Africa Governance Proof

The first practical governance corpus SHOULD include:

```text
customs rule

SPS requirement

permit requirement

certificate requirement

tariff table

rules-of-origin clause

explicit prohibition

explicit exception

future-effective amendment.
```

---

# 328. Example — Low-Risk Metadata

Source:

```text
official gazette
```

Candidate:

```text
publication date = 2026-09-20.
```

Pipeline:

```text
authoritative metadata
+
direct extraction
+
date parser
+
cross-check
```

Potential outcome after demonstrated maturity:

```text
AUTO_STRUCTURAL_VALIDATION
+
sampling.
```

No legal interpretation involved.

---

# 329. Example — Obligation Extraction

Text:

```text
The importer shall submit Certificate C
before clearance.
```

AI candidate:

```text
OBLIGATION

bearer = importer

requirement = Certificate C

deadline = before clearance.
```

Initial route:

```text
QUALIFIED_SINGLE_REVIEW.
```

If rule may later support E3:

```text
independent checker
```

is also required before publication.

---

# 330. Example — Exception

Text:

```text
The prohibition does not apply
where Permit P has been granted.
```

Candidate omitted the exception.

Machine detector finds:

```text
"does not apply where"
```

Result:

```text
HARD_GOVERNANCE_GATE_FAILED

promotion blocked.
```

---

# 331. Example — Interpretive Ambiguity

Provision uses:

```text
"reasonable measures."
```

Model proposes:

```text
reasonable = action within 48 hours.
```

No authoritative threshold supports this.

Reviewer:

```text
REJECT

reason:
UNSUPPORTED_DETERMINISTIC_THRESHOLD.
```

Correct canonical outcome:

```text
HUMAN_JUDGMENT_REQUIRED
```

or representational interpretation.

---

# 332. Example — Maker-Checker

Maker:

```text
Regulatory Analyst A

verifies Rule R.
```

Checker:

```text
Regulatory Analyst B

independently verifies:
source
conditions
exception
temporal scope.
```

Rule Engineer:

```text
verifies BRIR equivalence.
```

Publication Approver:

```text
publishes version.
```

---

# 333. Example — Checker Disagrees

Maker:

```text
effect = OBLIGATION.
```

Checker:

```text
effect = PROHIBITION.
```

Result:

```text
DISPUTED.
```

Not:

```text
use maker's answer because maker is senior.
```

---

# 334. Example — External Authority

Classification rule depends upon:

```text
binding tariff ruling.
```

Baobab reviewers cannot determine it safely.

Result:

```text
EXTERNAL_AUTHORITY_REQUIRED.
```

Once official ruling received:

```text
verify source
→ canonical fact
→ resume rule evaluation.
```

---

# 335. Example — Controlled Automation

After extensive evidence, Baobab's:

```text
South African Gazette publication-date extractor
```

demonstrates:

```text
very high validated accuracy

no critical errors

stable source format

continuous sampling.
```

It MAY move from:

```text
HUMAN_ASSISTED
```

to:

```text
CONTROLLED_AUTOMATION.
```

That does not authorise automatic legal interpretation of the Gazette.

---

# 336. Example — Drift

Publisher changes Gazette layout.

Extraction errors rise.

Monitoring detects:

```text
publication-date parser regression.
```

Governance response:

```text
CONTROLLED_AUTOMATION
    ↓
HUMAN_ASSISTED

review rate → 100%

pipeline correction

TEVV rerun.
```

---

# 337. Example — Automation Bias

AI presents:

```text
98.7% confidence:
"This provision creates a prohibition."
```

Review UI SHOULD NOT make the confidence figure the dominant cue.

Reviewer sees:

```text
source clause

candidate

conditions

exceptions

cross-references

validation results.
```

Reviewer concludes:

```text
effect is actually an obligation.
```

The system records:

```text
AI candidate rejected

human correction

regression fixture created.
```

---

# 338. Example — Emergency Gazette

Official authority issues an immediately effective restriction.

Normal review SLA is too slow.

Emergency route:

```text
source authenticity verified

legal-effective time verified

qualified maker reviews

independent checker reviews

minimum golden tests run

rule published under bounded emergency governance.
```

If material ambiguity remains:

```text
maximum effect = E2.
```

E4 does not arise merely from urgency.

---

# 339. Governance Architecture

```text
                    CANDIDATE
                        │
                        ▼
              AUTOMATED VALIDATION
                        │
                        ▼
                     TRIAGE
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       LOW RISK      SEMANTIC      HIGH IMPACT
          │             │             │
          ▼             ▼             ▼
     Validation      Qualified      Qualified
      + Sample         Maker          Maker
                         │             │
                         ▼             ▼
                       Review       Specialist
                         │             │
                         │             ▼
                         │          Checker
                         │             │
                         └──────┬──────┘
                                ▼
                           TEST / VERIFY
                                │
                                ▼
                        PUBLICATION GATE
                                │
                                ▼
                           CANONICAL
                         REGULATORY
                           KNOWLEDGE
```

---

# 340. Assurance Architecture

```text
                 MODEL OUTPUT
                      │
                      ▼
               Model Confidence
                 diagnostic
                      │
                      ▼
                 Candidate
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
 Source Assurance  Semantic      Technical
                  Assurance      Validation
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                Human Review
                      │
                      ▼
             Independent Check
                      │
                      ▼
                 Test State
                      │
                      ▼
            Publication Approval
                      │
                      ▼
         RegulatoryKnowledgeAssurance
```

There is deliberately no:

```text
confidence = 94%.
```

---

# 341. Strategic Consequence

This architecture solves a fundamental scalability problem.

Without measured automation:

```text
every page
→ expert review
→ high cost
→ slow jurisdiction expansion.
```

Without strong governance:

```text
every page
→ AI
→ auto-publish
→ unacceptable regulatory risk.
```

Baobab instead targets:

```text
machines perform repeatable extraction

validators catch mechanical defects

AI proposes semantic structure

experts concentrate on ambiguity and consequence

TEVV progressively automates proven low-risk work

maker-checker protects consequential publication.
```

---

# 342. Research Foundation Summary

NIST's AI RMF provides the primary governance foundation for this ADR. It explicitly requires organisations to define and differentiate human oversight roles, establish proficiency and training standards, document human-AI configurations, and assess human oversight according to risk and intended context.

NIST also cautions that humans themselves carry cognitive bias and that simply inserting a human into an AI-supported process does not guarantee effective governance. This directly supports Baobab's decision to make reviewer competence, authority, interface design and independence first-class controls rather than relying on a generic human-in-the-loop label.

The EU AI Act provides a useful contemporary example of risk-proportionate human oversight. Article 14 requires appropriately empowered human overseers to understand system limits, monitor anomalies, recognise automation bias, interpret outputs, disregard or reverse them where appropriate, and intervene when necessary. Its specialised two-person verification provision also illustrates that particularly consequential contexts can justify independent human confirmation. Baobab uses these principles as governance design input rather than claiming that every Article 14 obligation necessarily applies to Baobab Regulations.

NIST's separation-of-duty guidance provides a mature security/control basis for Baobab's maker-checker model: no one actor should possess enough effective authority to complete a sensitive process alone, and two-person operations are a recognised dynamic separation-of-duty mechanism.

ISO/IEC 42001:2023 supplies an organisational management-system perspective: AI governance should include defined responsibilities, risk management, transparency, performance evaluation and continual improvement across the lifecycle rather than one-time approval.

NIST's TEVV work reinforces the decision that automation maturity must rest on measured evidence. Its current TEVV programme emphasises testing, evaluation, verification and validation of complete AI systems in their intended use context rather than relying solely on vendor model metrics.

LangGraph provides appropriate technical primitives for the workflow layer: persistent state and human interrupts can pause review workflows and later resume them. Baobab deliberately places canonical reviewer decisions in the Regulations domain rather than making LangGraph checkpoints authoritative regulatory state.

The OECD's Rules as Code work remains relevant because translating human-readable regulation into machine-consumable logic requires governance over interpretation and implementation, not simply successful compilation.

---

# 343. Final Decision

Baobab Regulations SHALL implement **human verification as a competence-based, independence-aware, measurable and auditable regulatory governance system**.

The final architecture is:

```text
                  AUTHORITATIVE SOURCE
                          │
                          ▼
                      AI / MACHINE
                       CANDIDATE
                          │
                          ▼
                 AUTOMATED VALIDATION
                          │
                          ▼
                        TRIAGE
                          │
                          ▼
                 QUALIFIED REVIEWER
                          │
                    ┌─────┴─────┐
                    │           │
               lower risk    consequential
                    │           │
                    ▼           ▼
                 verify      independent
                               checker
                                  │
                                  ▼
                           specialist/legal
                           review if required
                                  │
                                  ▼
                              TESTS
                                  │
                                  ▼
                         PUBLICATION APPROVAL
                                  │
                                  ▼
                         PROMOTION COMMAND
                                  │
                                  ▼
                          POSTGRESQL
                        CANONICAL STATE
                                  │
                                  ▼
                            RULEVERSION
                                  │
                                  ▼
                                BRIR
                                  │
                                  ▼
                                OPA
```

The human-oversight principle is:

> **A human is an effective control only when that human has the competence, information, independence and authority necessary to challenge the system.**

The confidence principle is:

> **Model confidence is diagnostic metadata; it is not regulatory assurance.**

The assurance principle is:

> **Regulatory assurance is multidimensional and shall never be reduced to one opaque percentage.**

The reviewer principle is:

> **Verification authority is scoped by jurisdiction, domain, task and consequence—not merely by job title or seniority.**

The maker-checker principle is:

> **Consequential regulatory knowledge shall not depend upon one actor being both creator and independent verifier.**

The automation principle is:

> **Human workload may decrease only when task-specific TEVV demonstrates that automation is reliable within a bounded scope.**

The sampling principle is:

> **Sampling may reduce repetitive review for proven low-risk tasks, but novelty, ambiguity and critical semantic constructs always retain mandatory-review escape hatches.**

The disagreement principle is:

> **Reviewer disagreement is regulatory information to be resolved or preserved—not noise to be averaged away.**

The emergency principle is:

> **Urgency may accelerate governance; it does not eliminate governance.**

The authority principle is:

> **No internal reviewer, however senior, may manufacture a decision that legally belongs to a regulator, court or other competent authority.**

The LangGraph principle is:

> **LangGraph coordinates people and workflow state; PostgreSQL records what Baobab canonically decided and approved.**

The improvement principle is:

> **Every verified correction should make the system easier to test, measure and improve—but not silently retrain or alter production behaviour.**

The scalability principle is:

> **Machines should absorb repeatable work; qualified humans should concentrate on judgment, ambiguity, novelty and consequence.**

And the strategic principle is:

> **Baobab Regulations becomes trustworthy not because AI is removed from regulatory work, nor because a human approves everything, but because the platform can demonstrate exactly which work was automated, which work was reviewed, who was competent to review it, which independent controls operated, what evidence supported publication, and why the resulting regulatory knowledge was allowed to become executable.**

That is the architecture established by `ADR-REG-0022`.

---

## Decision Summary

```text
ADR-REG-0022
────────────────────────────────────────────

HUMAN-IN-THE-LOOP

Not enough.


EFFECTIVE HUMAN OVERSIGHT

Competence
+
Training
+
Authority
+
Information
+
Ability to reject
+
Independence where required


CONFIDENCE

Model confidence
≠
Regulatory assurance.


ASSURANCE

Multidimensional:

Source
Grounding
Citation
Temporal
Exceptions
Cross-reference
Reviewer competence
Reviewer independence
Testing
Publication state


NO

Single 0–100
regulatory confidence score.


REVIEW ROUTES

Auto Structural Validation

Qualified Single Review

Independent Maker-Checker

Specialist Review

Legal Review

External Authority Required


E3 / E4

Stronger governance.

Maker
≠
Checker.


AI

Can create candidate.

Cannot satisfy mandatory
human-review requirement.


LANGGRAPH

Pause
Route
Resume
Escalate

NOT canonical approval store.


POSTGRESQL

Canonical ReviewCase
ReviewDecision
Promotion state.


SAMPLING

Allowed only for
bounded proven tasks.

Critical/novel cases
remain mandatory review.


AUTOMATION MATURITY

Experimental

Human Assisted

Supervised Automation

Controlled Automation


MATURITY

Task-specific
Model-version-specific
Pipeline-specific
Jurisdiction-specific


DISAGREEMENT

Preserve
Escalate
Resolve

Do not average.


EMERGENCY

Compress time.

Do not remove
authority or audit.


EXTERNAL AUTHORITY

Where law requires regulator/court:

Baobab cannot substitute
internal review.


STRATEGIC RESULT

Automate repetition.

Reserve humans for
judgment and consequence.

Make every promotion
defensible.
```
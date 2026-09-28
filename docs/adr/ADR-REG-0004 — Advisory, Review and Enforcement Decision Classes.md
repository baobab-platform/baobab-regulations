# ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0004`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Decision Type:** Regulatory Decision Authority, Human Oversight and Enforcement Governance  
**Date:** 2026-09-27  
**Strategic Classification:** Platform Differentiator / Regulatory Execution Safety  
**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`

**Related Baobab Architecture:**

- `ADR-BCP-020 — Administrative Authority, Delegated Administration, Privileged Access and Separation-of-Duties Model`
- `ADR-BCP-021 — Changeset, Impact Analysis, Approval and Controlled Mutation Model`
- `ADR-PULSE-001 — Engine Mission, Authority and System Boundary`
- applicable IAM assurance, privileged-access and audit ADRs
- applicable capability, context and provider contracts in `baobab-platform/shared`

**Primary Principle:**

> **A regulatory conclusion does not, by itself, confer authority to take an operational action.**

---

# 1. Executive Decision

Baobab Regulations SHALL separate:

```text
WHAT THE REGULATORY ASSESSMENT CONCLUDES
```

from:

```text
WHAT THE PLATFORM IS AUTHORISED TO DO ABOUT IT.
```

The engine SHALL therefore treat the following as separate first-class concepts:

```text
AssessmentOutcome
        │
        ▼
DecisionEffectClass
        │
        ▼
OperationalDisposition
        │
        ▼
EnforcementAction
```

The canonical flow SHALL be:

```text
Regulatory Sources
        │
        ▼
Verified Rule Set
        │
        ▼
Regulatory Context
        │
        ▼
Assessment
        │
        ▼
Assessment Outcome
        │
        ▼
Effect Policy
        │
        ├── rule assurance
        ├── source authority
        ├── ambiguity
        ├── evidence completeness
        ├── context completeness
        ├── risk
        ├── reversibility
        ├── tenant policy
        └── operational policy
        │
        ▼
Decision Effect Class
        │
        ▼
Consuming Engine
        │
        ▼
Operational Enforcement
```

Baobab Regulations SHALL NOT assume:

```text
assessment outcome = BLOCK
        therefore
automatically terminate transaction
```

Instead:

```text
Assessment:
PROHIBITED

Effect Class:
REVIEW_GATE

Operational Engine:
places reversible hold

Human / Authorised Policy:
confirms disposition

Operational Engine:
blocks or releases
```

may be the correct behaviour.

The governing principle is:

> **Regulatory meaning, decision authority and operational enforcement are three different things.**

---

# 2. Why This ADR Is Necessary

`ADR-REG-0003` establishes that:

```text
Source
≠
Interpretation
≠
Rule
≠
Assessment
≠
Decision
```

This ADR adds another necessary separation:

```text
Decision
≠
Authority to execute an irreversible business action.
```

Without this distinction, a regulatory engine could evolve dangerously:

```text
LLM extracts rule
      │
      ▼
rule says "prohibited"
      │
      ▼
Regulations returns BLOCK
      │
      ▼
Trade cancels R5 million shipment
```

That architecture is rejected.

Baobab must determine separately:

```text
How reliable is the rule?

How authoritative is the source?

How complete is the context?

Is there ambiguity?

Is the decision deterministic?

What is the consequence of acting incorrectly?

Is the action reversible?

Does law require human review?

Does tenant governance require approval?

Who is authorised to override?

What evidence must be retained?
```

---

# 3. Strategic Position

Baobab Regulations is intended to become operational infrastructure.

That requires stronger safeguards than an informational compliance dashboard.

A dashboard may be wrong and inconvenience a researcher.

An execution engine may:

```text
hold shipment
deny market entry
prevent order fulfilment
require a permit
stop a product publication
prevent payment
prevent processing of data
```

A wrong automated decision can therefore cause:

```text
financial loss
breach of contract
customer harm
regulatory exposure
missed delivery
inventory cost
legal dispute
business interruption
```

The ability to enforce regulation is commercially valuable precisely because it is consequential.

The architecture SHALL earn that authority gradually.

---

# 4. Research Basis — Risk-Proportionate Oversight

NIST's AI Risk Management Framework states that human and AI roles must be explicitly defined and that human oversight requirements vary by context—from fully autonomous systems to human decision-making with AI as an additional input. NIST also calls for documented processes governing human oversight.

The OECD AI Principles similarly call for human agency and oversight appropriate to context and recommend mechanisms enabling systems that risk undue harm to be overridden, repaired or safely decommissioned.

Baobab SHALL therefore use **risk-proportionate decision authority**, not a universal human-in-the-loop requirement and not universal automation.

---

# 5. Research Basis — Effective Human Oversight

Article 14 of the EU AI Act provides a useful architectural precedent for high-risk automated systems. It requires oversight measures proportionate to risk, autonomy and context. It specifically provides for human overseers to understand system limitations, recognise automation bias, correctly interpret outputs, disregard or reverse outputs, and stop the system where appropriate.

Baobab does not adopt EU AI Act classifications as its universal regulatory scheme.

However, these principles are architecturally sound:

```text
oversight must be effective
reviewer must understand the system
reviewer must have authority
reviewer must be able to disagree
reviewer must be able to intervene
```

A human rubber stamp is not meaningful oversight.

---

# 6. Research Basis — South African Automated Decisions

South Africa's POPIA section 71 restricts certain decisions based solely on automated processing of personal information where those decisions create legal consequences or substantially affect a data subject. Where specified exceptions apply, appropriate safeguards include the opportunity to make representations and provision of sufficient information about the underlying logic.

This does not mean every Baobab regulatory transaction assessment falls under section 71.

It does establish an important platform principle:

> **The architecture must support human challenge, explanation and review whenever the governing law or the context requires them.**

---

# 7. Foundational Separation

Baobab SHALL model at least:

```text
AssessmentOutcome
DecisionEffectClass
OperationalDisposition
ReviewRequirement
EnforcementAction
OverrideDecision
```

These SHALL remain separate.

---

# 8. AssessmentOutcome

`AssessmentOutcome` describes what the regulatory analysis concluded.

It SHALL NOT describe the operational action itself.

The initial canonical vocabulary SHALL be:

```text
SATISFIED

SATISFIED_WITH_REQUIREMENTS

UNSATISFIED

PROHIBITED

INDETERMINATE

NOT_APPLICABLE
```

---

# 9. SATISFIED

Means:

> The evaluated regulatory requirements within the applicable rule set are satisfied for the supplied context.

It does NOT mean:

```text
no law anywhere could possibly apply
```

or:

```text
government has approved the transaction.
```

---

# 10. SATISFIED_WITH_REQUIREMENTS

Means:

> The activity may be capable of proceeding under the evaluated regulatory framework, but one or more obligations must continue to be satisfied.

Examples:

```text
retain certificate
submit declaration
carry permit
maintain documentation
report by deadline
```

---

# 11. UNSATISFIED

Means:

> One or more applicable regulatory requirements have not been demonstrated as satisfied.

Example:

```text
required certificate missing
```

It may be remediable.

It therefore differs from:

```text
PROHIBITED
```

---

# 12. PROHIBITED

Means:

> The verified applicable rule set indicates that the proposed action is prohibited under the evaluated context.

This is a regulatory conclusion.

It still does not automatically authorise an irreversible operational act.

---

# 13. INDETERMINATE

Means:

> Baobab cannot reliably determine regulatory disposition.

Potential reasons:

```text
missing facts
conflicting authority
unresolved interpretation
insufficient rule coverage
stale source
ambiguous classification
missing evidence
system dependency failure
```

`INDETERMINATE` SHALL be a legitimate production outcome.

---

# 14. NOT_APPLICABLE

Means:

> The evaluated regulatory rule/profile does not apply to the supplied context.

It SHALL NOT mean:

```text
no regulation applies.
```

---

# 15. Compatibility with Earlier ADR Vocabulary

`ADR-REG-0001` introduced conceptual outputs including:

```text
ALLOW
ALLOW_WITH_REQUIREMENTS
REVIEW_REQUIRED
BLOCK
INDETERMINATE
NOT_APPLICABLE
```

This ADR refines that vocabulary.

The canonical internal model SHALL distinguish:

```text
AssessmentOutcome
```

from:

```text
OperationalDisposition
```

Therefore:

```text
ALLOW
BLOCK
REVIEW_REQUIRED
```

MAY remain convenient API projections or consumer-facing dispositions.

They SHALL NOT collapse the underlying semantics.

---

# 16. Decision Effect Classes

Baobab SHALL introduce five increasing classes of permitted operational effect:

```text
E0 — INFORMATIONAL

E1 — ADVISORY

E2 — REVIEW_GATE

E3 — CONDITIONAL_ENFORCEMENT

E4 — AUTOMATED_ENFORCEMENT
```

The class SHALL represent the **maximum regulatory authority Baobab grants to downstream automation for that decision**.

---

# 17. E0 — INFORMATIONAL

E0 decisions may:

```text
display
log
report
support research
support simulation
```

They SHALL NOT:

```text
hold
deny
block
require acknowledgement
alter workflow
```

Typical sources include:

```text
unverified discovery
draft interpretation
secondary-source research
proposed regulation
low-assurance extraction
```

---

# 18. E1 — ADVISORY

E1 may:

```text
warn
recommend
flag
notify
suggest additional evidence
```

but SHALL normally allow the underlying workflow to continue.

Example:

```text
Potential permit requirement detected.
Review recommended.
```

The system MAY require acknowledgement for governance purposes.

Acknowledgement SHALL NOT transform advisory output into regulatory enforcement.

---

# 19. E2 — REVIEW_GATE

E2 permits Baobab to trigger a **reversible operational hold** pending authorised review.

Conceptually:

```text
Assessment
      │
      ▼
REVIEW_GATE
      │
      ▼
Temporary Hold
      │
      ▼
Human / Authorised Review
      │
      ├── Approve
      ├── Approve with conditions
      ├── Reject
      └── Escalate
```

E2 SHALL be the normal safe escalation class for:

```text
ambiguity
conflict
missing evidence
high-impact uncertainty
AI-identified anomaly
discretionary rule
novel transaction
```

---

# 20. Review Gate Is Not Regulatory Rejection

A review hold means:

```text
do not proceed yet
```

not:

```text
activity is legally prohibited.
```

This distinction SHALL be visible to consumers.

---

# 21. E3 — CONDITIONAL_ENFORCEMENT

E3 permits deterministic enforcement of objective, remediable conditions.

Examples:

```text
document required before dispatch

permit must be present

licence must be active

mandatory field must be supplied

certificate must not be expired
```

The canonical pattern is:

```text
Requirement unsatisfied
       │
       ▼
workflow blocked
       │
       ▼
requirement satisfied
       │
       ▼
automatic release
```

E3 is therefore typically **condition enforcement**, not final prohibition.

---

# 22. E4 — AUTOMATED_ENFORCEMENT

E4 permits an operational engine to enforce a verified regulatory result without case-by-case human approval.

Potential examples include:

```text
verified prohibited goods rule

expired mandatory licence

explicit statutory prohibition

objective restricted-market condition

machine-verifiable legal threshold
```

E4 SHALL be exceptional compared with E0–E3.

It SHALL require explicit eligibility.

---

# 23. E4 Does Not Authorise Every Consequence

Even an E4 decision SHALL ordinarily authorise only the configured enforcement action.

Example:

```text
E4:
do not release shipment
```

does NOT automatically authorise:

```text
cancel customer contract
destroy goods
report customer to regulator
terminate supplier relationship
refund money
close account
admit legal liability
```

Those are separate business actions.

---

# 24. Enforcement Shall Prefer Reversible Controls

Where possible:

```text
HOLD
```

is preferred over:

```text
DESTROY
```

```text
DENY TRANSITION
```

over:

```text
DELETE TRANSACTION
```

```text
QUARANTINE
```

over:

```text
TERMINATE RELATIONSHIP
```

Automation SHOULD first prevent an unsafe transition.

It SHOULD NOT gratuitously create irreversible consequences.

---

# 25. Regulatory Automation Asymmetry

Baobab SHALL deliberately allow automation to **escalate caution more easily than coercion**.

Therefore:

```text
AI anomaly
     │
     ▼
REVIEW_GATE
```

may be permitted.

But:

```text
AI anomaly
     │
     ▼
AUTOMATED_ENFORCEMENT
```

shall ordinarily be prohibited.

This is a foundational safety asymmetry.

---

# 26. AI Enforcement Ceiling

Unless a later domain-specific ADR explicitly authorises otherwise, a regulatory decision materially dependent upon unverified generative-AI inference SHALL have a maximum effect class of:

```text
E2 — REVIEW_GATE
```

It SHALL NOT independently qualify for:

```text
E3
E4
```

---

# 27. Why AI May Trigger Review

NIST identifies confabulation as confidently generated false content and specifically warns that generative AI may fabricate logic or citations that appear to justify consequential outputs.

Therefore AI can be valuable at:

```text
detect
extract
suggest
flag
escalate
```

while verified deterministic logic controls:

```text
enforce.
```

---

# 28. Deterministic Does Not Automatically Mean Enforceable

A rule can be deterministic but wrong.

Therefore:

```text
deterministic
≠
verified
≠
enforcement eligible
```

All relevant criteria must pass.

---

# 29. Enforcement Eligibility

A rule/decision SHOULD satisfy all applicable requirements before E4 eligibility:

```text
authoritative source identified

source authenticity sufficiently verified

source currently applicable

legal force understood

interpretation verified

machine rule verified

no material unresolved source conflict

no material unresolved interpretation conflict

context sufficiently complete

critical evidence sufficiently complete

effective time resolved

jurisdiction resolved

decision deterministic or otherwise approved

golden regulatory cases passing

decision reproducible

rule-set version pinned

operational action explicitly configured

tenant/domain policy authorises enforcement

override path exists

audit path exists

provider readiness satisfied
```

Failure of a critical requirement SHALL reduce the permitted class.

---

# 30. Enforcement Eligibility Is Not Permanent

E4 status SHALL NOT be considered an eternal property of a rule.

It may be suspended by:

```text
source change

rule amendment

source staleness

new court ruling

new authority interpretation

discovered defect

failed regression test

coverage degradation

unresolved conflict

security incident
```

---

# 31. Enforcement Ceiling

Each production rule or regulatory decision policy SHOULD carry:

```text
max_effect_class
```

Example:

```text
Rule:
ZA_RESTRICTED_GOODS_102

Verification:
VERIFIED

max_effect_class:
E4
```

while:

```text
Rule:
DRAFT_SPS_INTERPRETATION_34

max_effect_class:
E1
```

---

# 32. Consumer Cannot Escalate Regulatory Authority

If Regulations returns:

```text
max_effect_class = E1
```

Trade SHALL NOT relabel the regulatory decision as:

```text
E4
```

because Trade prefers caution.

---

# 33. Consumer May Apply Stricter Internal Policy

Trade MAY decide:

```text
Baobab Regulations:
E1 advisory

Tenant risk policy:
place transaction on hold
```

but the resulting action SHALL be attributed correctly:

```text
REGULATORY EFFECT:
E1

TENANT POLICY EFFECT:
HOLD
```

not:

```text
law requires hold.
```

---

# 34. Internal Policy Must Remain Distinguishable

This preserves the ADR-REG-0003 principle:

```text
external regulation
≠
tenant policy
```

Baobab must know why something was blocked.

---

# 35. Effect Policy

Baobab SHALL introduce a governed effect policy or equivalent model.

Conceptually:

```text
RegulatoryEffectPolicy
├── id
├── capability
├── regulatory_domain
├── tenant_scope?
├── legal_entity_scope?
├── market_scope?
├── jurisdiction_scope?
├── operation_type?
├── rule_class?
├── risk_class
├── max_effect_class
├── required_assurance
├── review_policy?
├── override_policy?
├── valid_from
├── valid_to?
└── version
```

---

# 36. Effect Policy Is Not Regulatory Law

The effect policy answers:

> **What may Baobab operationally do with a regulatory conclusion?**

It does not answer:

> **What does the law require?**

---

# 37. Default Effect Policy

A newly onboarded regulatory rule SHALL default conservatively.

Recommended initial ceiling:

```text
new / unverified
    → E0

machine-interpreted
    → E0 / E1

human-reviewed interpretation
    → E1 / E2

verified deterministic requirement
    → eligible for E3

verified explicit prohibition
+
complete deterministic context
+
governed approval
    → potentially eligible for E4
```

---

# 38. No Automatic Promotion

A rule SHALL NOT automatically become E4 because:

```text
it has existed for 30 days
```

or:

```text
many assessments used it
```

or:

```text
AI confidence increased.
```

Promotion requires governance.

---

# 39. Effect-Class Promotion

Promotion SHOULD follow:

```text
Current Class
      │
      ▼
Proposed Promotion
      │
      ▼
Impact Analysis
      │
      ▼
Golden Cases
      │
      ▼
Shadow Execution
      │
      ▼
Review
      │
      ▼
Approval
      │
      ▼
Controlled Activation
```

This aligns with Baobab's existing controlled-change architecture.

---

# 40. E4 Promotion Is Consequential Change

Promotion such as:

```text
E2 → E4
```

SHALL be treated as a consequential production change.

It SHOULD therefore be governed through Baobab Changeset semantics, including:

```text
exact proposed change
impact analysis
approval
execution
verification
audit
```

---

# 41. Assessment Risk

Baobab SHALL classify regulatory decision risk separately from regulatory authority.

Potential risk dimensions include:

```text
financial magnitude

legal consequence

contractual consequence

safety consequence

personal-data consequence

fundamental-rights impact

customer consequence

supplier consequence

shipment consequence

operational interruption

scale / number of affected objects

reversibility

time sensitivity

external reporting consequence

reputational consequence
```

---

# 42. Proposed Risk Classes

Initial conceptual classes:

```text
R0 — NEGLIGIBLE

R1 — LOW

R2 — MODERATE

R3 — HIGH

R4 — CRITICAL
```

Exact risk computation belongs in later implementation design.

---

# 43. Risk Does Not Equal Effect

A high-risk decision does not necessarily mean:

```text
BLOCK
```

It may instead mean:

```text
stronger review required.
```

---

# 44. Reversibility Is a First-Class Risk Attribute

The platform SHALL distinguish:

```text
easily reversible

operationally reversible

financially reversible

difficult to reverse

legally irreversible
```

The EU AI Act similarly treats corrigibility or reversibility of adverse outcomes as relevant when assessing system risk.

---

# 45. Irreversible Actions Require Higher Authority

Examples include:

```text
terminate contract

submit binding government filing

destroy inventory

report suspected misconduct

permanently close account

terminate employee

admit legal liability

waive legal right
```

Regulations SHALL NOT directly authorise these merely through ordinary E4 regulatory enforcement.

A separate authorised workflow is required.

---

# 46. Regulatory Block versus Business Cancellation

Example:

```text
Regulations:
shipment cannot currently be released
```

does not mean:

```text
Trade:
cancel sales contract.
```

The first is regulatory enforcement.

The second is commercial decision-making.

---

# 47. OperationalDisposition

A consumer-facing disposition MAY include:

```text
NO_ACTION

PROCEED

PROCEED_WITH_REQUIREMENTS

WARN

ACKNOWLEDGEMENT_REQUIRED

HOLD_FOR_REVIEW

REQUIRE_EVIDENCE

DENY_TRANSITION

REGULATORY_BLOCK
```

These dispositions SHALL map to decision effect classes.

---

# 48. Example Mapping

```text
Outcome:
SATISFIED

Effect:
E0

Disposition:
PROCEED
```

---

# 49. Example Mapping — Advisory

```text
Outcome:
INDETERMINATE

Effect:
E1

Disposition:
WARN
```

where the domain risk permits continued operation.

---

# 50. Example Mapping — Review

```text
Outcome:
INDETERMINATE

Effect:
E2

Disposition:
HOLD_FOR_REVIEW
```

where uncertainty concerns a material regulatory condition.

---

# 51. Example Mapping — Conditional

```text
Outcome:
UNSATISFIED

Reason:
certificate missing

Effect:
E3

Disposition:
REQUIRE_EVIDENCE
```

---

# 52. Example Mapping — Enforcement

```text
Outcome:
PROHIBITED

Rule:
verified restricted-goods prohibition

Effect:
E4

Disposition:
REGULATORY_BLOCK
```

---

# 53. Outcome and Effect Matrix

| Assessment outcome | Typical possible effect | Automatic E4? |
|---|---|---:|
| `SATISFIED` | E0–E1 | No need |
| `SATISFIED_WITH_REQUIREMENTS` | E1–E3 | Rare |
| `UNSATISFIED` | E1–E3 | Not normally |
| `PROHIBITED` | E2–E4 | Only if eligibility passes |
| `INDETERMINATE` | E1–E2 | Never |
| `NOT_APPLICABLE` | E0 | Never |

---

# 54. INDETERMINATE Maximum Effect

`INDETERMINATE` SHALL NEVER directly produce E4.

Its maximum normal effect SHALL be:

```text
E2 — REVIEW_GATE
```

because uncertainty cannot logically establish a definitive prohibition.

---

# 55. Conflict Maximum Effect

A materially unresolved legal/source conflict SHALL normally cap effect at:

```text
E2
```

until resolved.

---

# 56. Discretionary Rules

Rules involving:

```text
reasonable
appropriate
material
adequate
in the public interest
satisfactory to authority
```

or comparable discretionary tests SHOULD ordinarily require review unless reliable jurisdiction-specific decision machinery exists.

---

# 57. Machine-Resolvable Conditions

Rules involving objective facts such as:

```text
licence expiry date

numeric threshold

permit presence

product classification match

destination country

effective date
```

are stronger candidates for E3/E4.

---

# 58. Human Review Requirement

`ReviewRequirement` SHALL be explicit.

Potential values:

```text
NONE

SINGLE_REVIEWER

MAKER_CHECKER

DUAL_CONFIRMATION

SPECIALIST_REVIEW

LEGAL_REVIEW

AUTHORITY_REVIEW
```

---

# 59. Human Reviewer Must Have Authority

A reviewer SHALL be authorised for:

```text
regulatory domain

jurisdiction

tenant/legal entity

decision effect

risk class
```

where governance requires.

Any authenticated employee is not automatically a regulatory reviewer.

---

# 60. Reviewer Competence

Reviewer policy SHOULD consider:

```text
training
domain expertise
jurisdiction expertise
professional qualification where necessary
delegated authority
current role
```

This aligns with the EU AI Act principle that human overseers of high-risk systems require appropriate competence, training and authority.

---

# 61. Reviewer Must See Evidence

A reviewer SHOULD receive:

```text
proposed disposition

assessment outcome

applicable rules

source provisions

interpretations

missing evidence

conflicts

uncertainty

decision assurance

operational consequence
```

before deciding.

---

# 62. No Blind Review

Rejected:

```text
Baobab says BLOCK.

[Approve] [Reject]
```

with no supporting information.

That encourages automation bias.

---

# 63. Automation Bias

The reviewer experience SHALL explicitly avoid designing the human as a passive confirmer.

Useful mechanisms MAY include:

```text
show uncertainty

show conflicting evidence

show source status

show alternative interpretation

avoid pre-selecting approval

require reason for high-impact confirmation

allow independent source inspection
```

The EU AI Act explicitly identifies over-reliance on automated outputs as automation bias that human oversight should address.

---

# 64. Human Reviewer Must Be Able to Disagree

A reviewer SHALL be able, according to authority, to:

```text
confirm

override

reverse

defer

request evidence

escalate
```

A reviewer who cannot disagree is not exercising meaningful oversight.

---

# 65. Override

An override SHALL be first-class.

Conceptually:

```text
RegulatoryOverride
├── id
├── decision_id
├── actor
├── authority
├── action
├── reason
├── evidence_refs[]
├── valid_from
├── valid_until?
├── created_at
└── audit_metadata
```

---

# 66. Override Does Not Delete Original Decision

Correct:

```text
RegulatoryDecision:
BLOCK

Override:
ALLOW_ON_COUNSEL_AUTHORITY
```

Incorrect:

```text
UPDATE decision
SET outcome = ALLOW
```

The original decision remains.

---

# 67. Override Types

Potential categories:

```text
HUMAN_REGULATORY_REVIEW

TENANT_COUNSEL_OVERRIDE

PLATFORM_CORRECTION

AUTHORITY_RULING

EMERGENCY_EXCEPTION

FALSE_POSITIVE_CORRECTION
```

Exact vocabulary belongs in later contracts.

---

# 68. Override Scope

An override MAY apply to:

```text
one transaction

one product

one counterparty

one jurisdiction

one time window

one class of transactions
```

It SHALL never silently become global.

---

# 69. Override Expiry

Where appropriate, overrides SHOULD expire.

Example:

```text
valid_until:
2026-10-31
```

This avoids permanent policy emerging from temporary judgment.

---

# 70. Override Authority Must Be Separate from Rule Authoring

Where risk warrants, the person who authored a rule SHOULD NOT alone approve an override involving that same rule.

This follows Baobab's existing separation-of-duties architecture.

---

# 71. Maker-Checker

High-impact regulatory decisions MAY require:

```text
Reviewer A
      │
      ▼
decision
      │
      ▼
Reviewer B
      │
      ▼
confirmation
```

depending upon domain risk.

---

# 72. Dual Confirmation Is Not Universal

Two-person approval for every shipment would make the system economically unusable.

It SHALL therefore be applied selectively.

---

# 73. Review SLA

Review gates SHOULD support explicit:

```text
priority

due_at

escalation_at

review_queue

assigned_role
```

A review gate with no operational path becomes a hidden business outage.

---

# 74. Time-Critical Review

Some operations are time-sensitive:

```text
border clearance

perishable goods

cut-off shipment

real-time commerce
```

The engine SHOULD communicate urgency to the workflow.

Urgency SHALL not reduce regulatory assurance automatically.

---

# 75. Review Timeout

A review timeout SHALL NOT automatically become:

```text
ALLOW
```

or:

```text
BLOCK
```

unless explicitly configured by governance.

---

# 76. Default Review Timeout State

Preferred:

```text
REVIEW_EXPIRED
```

or:

```text
ESCALATION_REQUIRED
```

with domain policy determining what happens operationally.

---

# 77. Enforcement Owner

Regulations remains the **Policy Decision Point**.

The operational engine remains the **Policy Enforcement Point**.

OPA documents this architecture explicitly: the PDP evaluates policy and returns decisions, while applications acting as PEPs enforce them.

Baobab SHALL preserve the same conceptual separation.

---

# 78. Regulations Does Not Call Trade Database

Forbidden:

```text
Regulations:
UPDATE shipments
SET status='BLOCKED'
```

Required:

```text
Regulations:
RegulatoryDecision

        ↓

Trade:
authorised enforcement
```

---

# 79. Enforcement Receipt

When an operational engine enforces a consequential regulatory decision, it SHOULD emit an enforcement receipt or equivalent record.

Conceptually:

```text
RegulatoryEnforcementReceipt
├── decision_id
├── enforcement_engine
├── target_ref
├── action
├── enforced_at
├── actor/workload
├── outcome
└── correlation_id
```

---

# 80. Why Enforcement Receipts Matter

They allow Regulations to distinguish:

```text
decision issued
```

from:

```text
decision actually enforced
```

These are different business facts.

---

# 81. Regulations Does Not Own Enforcement Receipt State Necessarily

The receipt's canonical contract may be shared.

The operational engine remains authoritative for its action.

Regulations may retain a reference for lineage.

---

# 82. Example — ZuriBeans Export Permit

```text
Product:
Ugandan vanilla

Requirement:
valid export permit

Permit:
missing

Assessment:
UNSATISFIED

Effect:
E3 CONDITIONAL_ENFORCEMENT

Disposition:
REQUIRE_EVIDENCE
```

Trade may:

```text
prevent shipment release
```

until permit evidence arrives.

It need not cancel the order.

---

# 83. Example — Explicit Prohibited Product

```text
Product classification:
verified

Destination:
ZA

Rule:
verified explicit prohibition

Context:
complete

Conflicts:
none

Assessment:
PROHIBITED

Effect:
E4
```

Trade may automatically prevent import workflow progression.

A permanent commercial cancellation remains separate.

---

# 84. Example — Ambiguous Classification

```text
HS candidate:
0901...

alternative:
different tariff heading

classification confidence:
unresolved

Assessment:
INDETERMINATE

Effect:
E2

Disposition:
HOLD_FOR_REVIEW
```

No automated final block.

---

# 85. Example — AI Detects Possible New Rule

```text
AI extraction:
new government notice may affect coffee

verification:
pending

Effect:
E1 or E2
```

Potential action:

```text
alert regulatory analyst
```

or for high-impact open shipments:

```text
hold for review
```

Never:

```text
cancel shipments automatically.
```

---

# 86. Example — Proposed Regulation

A proposed rule SHALL normally be:

```text
E0
```

or potentially:

```text
E1
```

for preparedness.

It SHALL not enter current enforcement.

---

# 87. Future-Effective Regulation

A verified law with future effective date MAY produce:

```text
E1 today
```

for planning,

and automatically become eligible for the configured production class at:

```text
effective_from
```

subject to successful activation checks.

---

# 88. Effective-Date Activation

Future rule activation SHOULD itself be governed and observable.

The system SHALL verify:

```text
effective time reached

rule set ready

tests passed

provider healthy

no superseding change detected
```

before enabling higher effect classes.

---

# 89. Stale Regulatory Data

If a critical source exceeds its permitted freshness window:

```text
E4
```

SHOULD be suspended where freshness is material.

The engine may downgrade:

```text
E4 → E2
```

until regulatory state is verified.

---

# 90. Source Conflict After Promotion

If a new authoritative conflict appears:

```text
E4
```

SHALL be capable of immediate suspension.

A previously enforceable rule may temporarily become:

```text
REVIEW_GATE.
```

---

# 91. Emergency Suspension

Platform governance SHALL support an emergency kill-switch for:

```text
rule
interpretation
profile
effect policy
jurisdiction pack
```

without deleting historical decisions.

---

# 92. Kill-Switch Behaviour

Emergency suspension SHOULD:

```text
prevent new automated enforcement

retain historical state

create audit event

trigger impact analysis

notify affected operational consumers
```

---

# 93. Safe State

Where automated enforcement is suspended, the safe fallback SHALL depend on regulatory risk.

Potential:

```text
E1
```

or:

```text
E2
```

rather than universal fail-open.

---

# 94. Fail-Open Is Domain-Specific

Examples where advisory continuation may be reasonable:

```text
non-material reporting suggestion unavailable
```

Examples where hold may be appropriate:

```text
prohibited-goods screening unavailable
```

A global:

```text
fail_closed = true
```

is too crude.

---

# 95. Engine Failure Is Not Regulatory Outcome

If Regulations is unavailable:

```text
503
```

SHALL NOT be translated to:

```text
SATISFIED
```

or:

```text
PROHIBITED.
```

Infrastructure state and regulatory outcome remain separate.

---

# 96. Review Requirement May Be Legally Mandated

Where applicable law requires:

```text
human intervention

right to make representations

right to obtain explanation

right to challenge
```

the effect policy SHALL enforce those requirements.

South Africa's POPIA section 71 provides one relevant example for certain solely automated decisions based on personal information.

---

# 97. Human Review May Also Be Contractual

A customer may choose:

```text
All customs prohibitions:
manual confirmation
```

even where Baobab could technically automate.

Baobab SHALL support this.

---

# 98. Human Review May Also Be Internal Policy

A tenant may require:

```text
CFO review

Compliance Officer review

Legal Counsel review

Trade Manager review
```

for defined decision classes.

These are tenant governance policies.

They are not regulatory authority.

---

# 99. Effect Policies Are Tenant-Aware

Different customers MAY legitimately configure:

```text
E4 permitted
```

or:

```text
maximum E2
```

for the same Baobab rule.

The regulatory meaning remains the same.

The automation appetite differs.

---

# 100. Tenant Cannot Weaken Mandatory Platform Safety

Tenant configuration SHALL NOT be permitted to bypass Baobab's non-negotiable safeguards.

Example:

```text
tenant says:
allow LLM-generated E4 decisions
```

MUST be rejected if platform policy prohibits it.

---

# 101. Platform Safety Ceiling

The effective decision class SHALL be constrained by the most restrictive applicable ceiling:

```text
rule ceiling

interpretation ceiling

source ceiling

platform safety ceiling

tenant policy ceiling

domain policy ceiling
```

Conceptually:

```text
effective_effect_class
=
minimum(permitted ceilings)
```

This is a conceptual lattice, not necessarily numeric implementation.

---

# 102. More Restrictive Business Policy Is Allowed

The consuming engine may be more conservative than Regulations.

It may not falsely attribute its conservatism to law.

---

# 103. Less Restrictive Business Policy Is Not Always Allowed

If Regulations returns:

```text
E4 regulatory prohibition
```

and the tenant has contractually enabled that E4 class,

Trade SHALL not silently ignore it.

Override must follow authorised governance.

---

# 104. Explanation Required for Consequential Effects

E2–E4 decisions SHOULD be explainable.

At minimum:

```text
what happened

which rule applied

why it applied

what evidence was evaluated

what requirement failed

what can remediate it

who may review

which source supports it
```

---

# 105. Actionability

A useful enforcement message is not:

```text
FAILED COMPLIANCE.
```

It is:

```text
Shipment cannot proceed because
certificate X is required and not currently present.

Provide:
Certificate X

Authority:
...

Rule:
...

Review:
available
```

---

# 106. Explainability Does Not Mean Exposing Secrets

The engine SHALL balance explanation with:

```text
security

commercial confidentiality

third-party licensing

personal-information restrictions
```

Source references may sometimes require controlled access.

---

# 107. Appeal and Challenge

The architecture SHOULD support a challenge process for decisions where appropriate.

Conceptually:

```text
Decision
    │
    ▼
Challenge
    │
    ▼
Review
    │
    ├── Affirm
    ├── Override
    ├── Correct
    └── Escalate
```

---

# 108. Challenge Is Not Necessarily Legal Appeal

A Baobab challenge is an internal regulatory-decision review mechanism.

It SHALL not be presented as a statutory appeal unless the relevant authority recognises it as such.

---

# 109. Challenge Record

Conceptually:

```text
RegulatoryChallenge
├── decision_id
├── raised_by
├── reason
├── evidence_refs[]
├── submitted_at
├── review_state
├── reviewed_by
└── outcome
```

---

# 110. Decision Validity

A regulatory decision SHOULD carry temporal validity metadata.

Example:

```text
valid_from

valid_until

reassess_if_rule_changes

reassess_if_context_changes

reassess_if_evidence_changes
```

---

# 111. Decision Reuse

A prior assessment SHALL NOT automatically be reused when material context changes.

Examples:

```text
destination changed

product changed

classification changed

permit expired

law changed

counterparty changed

effective date changed
```

---

# 112. Enforcement Must Verify Decision Freshness

Before enforcing a cached regulatory decision, a PEP SHOULD confirm that:

```text
decision remains valid

rule-set version remains accepted

context remains materially unchanged

decision has not been revoked/suspended
```

according to contract.

---

# 113. Decision Revocation

A decision MAY become:

```text
SUPERSEDED

REVOKED

STALE

INVALIDATED
```

without deleting its historical existence.

---

# 114. Decision Revocation Event

Regulations SHOULD publish events where a previously relied-upon decision becomes invalid for future use.

Potential:

```text
regulation.decision.invalidated
```

Final event vocabulary belongs in Shared.

---

# 115. Impact Analysis

Promoting a rule to E3/E4 SHOULD identify potentially affected:

```text
products

markets

trade lanes

legal entities

transactions

shipments

Digital Estates

operational engines
```

before activation where feasible.

---

# 116. Shadow Enforcement

Prior to E4 activation:

```text
production flow
      │
      ├── actual policy:
      │      E1 / E2
      │
      └── shadow:
             what E4 would have done
```

SHOULD be supported.

This enables measurement of:

```text
false positives

false negatives

volume

business impact

review disagreement
```

without enforcing the new behaviour.

---

# 117. Canary Enforcement

Where appropriate, automated enforcement MAY be introduced gradually.

Example:

```text
one tenant

one legal entity

one product class

one market

one corridor
```

before wider activation.

---

# 118. Canary Must Not Create Legal Inconsistency

Canary use SHALL NOT be used where law requires uniform enforcement and selective enforcement would itself create an unacceptable legal or contractual issue.

Deployment experiments remain subordinate to legal obligations.

---

# 119. Decision Telemetry

Baobab SHOULD monitor:

```text
decision volume

outcomes

effect classes

review frequency

override rate

false-positive reports

average review time

decision reversals

stale-decision attempts

rule failures

consumer enforcement success
```

---

# 120. Override Rate Is a Quality Signal

If:

```text
60% of E4 decisions are overridden
```

that is a serious regulatory-system quality signal.

The rule/effect policy SHOULD be automatically flagged for review.

---

# 121. High Review Disagreement

Similarly:

```text
E2 recommendations
frequently rejected by specialists
```

may indicate:

```text
poor interpretation

bad context data

insufficient evidence

overly conservative policy
```

Pulse MAY later analyse these operational patterns.

Regulations owns the domain record.

---

# 122. Feedback Must Not Self-Modify Law

Human overrides SHALL NOT automatically retrain or mutate regulatory rules.

Feedback can:

```text
trigger review

inform analysis

create candidate correction
```

It cannot silently rewrite law.

---

# 123. Learning Boundary

Baobab may learn:

```text
which rules produce false positives

which evidence is often missing

which reviews take longest
```

without allowing statistical optimisation to supersede legal semantics.

---

# 124. Optimisation Objective

Regulations SHALL NOT optimise primarily for:

```text
maximum transaction throughput
```

or:

```text
minimum number of holds.
```

Its primary objective is:

```text
reliable regulatory decision-making
```

within reasonable operational performance.

---

# 125. Commercial Incentives Cannot Change Regulatory Outcome

A higher-paying customer SHALL NOT receive:

```text
more permissive law.
```

Commercial entitlement may affect:

```text
coverage

SLA

jurisdictions

automation level

features
```

not the meaning of authoritative regulation.

---

# 126. Commercial Tier May Affect Automation

For example:

```text
Basic:
E0–E1

Professional:
E0–E3

Enterprise:
E0–E4
```

could eventually be commercially viable.

But only where regulatory assurance qualifies.

Payment cannot convert an unverified rule into E4.

---

# 127. Regulations and Pulse

Pulse may produce:

```text
risk recommendation
```

but SHALL NOT upgrade a Regulations decision effect class.

Example:

```text
Pulse:
shipment commercially risky
```

does not create:

```text
Regulatory E4 block.
```

---

# 128. Pulse May Increase Business Review

Pulse MAY independently cause:

```text
commercial risk review
```

through its own authorised decision workflow.

The two holds must remain distinguishable:

```text
REGULATORY HOLD

COMMERCIAL RISK HOLD
```

---

# 129. Regulations and IAM

IAM SHALL authenticate:

```text
reviewer

override actor

workload
```

Regulations SHALL determine regulatory-domain authority using approved IAM/Control Plane context.

---

# 130. Regulations and Control Plane

Control Plane SHALL remain authoritative for:

```text
tenant

legal entity

administrative authority

capability grant

provider

engine instance
```

Regulations SHALL not invent a second administrator identity system.

---

# 131. Review Authority as Scoped Relationship

Following Baobab's existing administrative-authority model:

```text
person
≠
reviewer everywhere.
```

Authority SHALL be scoped.

---

# 132. Regulations and Trade

Trade SHALL map dispositions to trade workflow.

Example:

```text
REQUIRE_EVIDENCE
      │
      ▼
Trade:
REGULATORY_HOLD
```

Trade owns the hold state.

---

# 133. Regulations and ERP

ERP MAY enforce:

```text
posting constraint

tax-document requirement

reporting evidence requirement
```

where effect policy permits.

Regulations SHALL not post journals.

---

# 134. Regulations and CMS

CMS MAY prevent:

```text
product publication

claim publication

regulated-market content
```

where appropriate.

The content state remains CMS-owned.

---

# 135. Regulations and External Systems

External enterprise consumers SHALL receive the same decision/effect distinction.

Baobab SHALL not expose a simplified external API that destroys its trust model.

---

# 136. Canonical Decision Contract

A conceptual response SHOULD eventually contain:

```yaml
assessment:
  outcome: PROHIBITED

decision:
  effect_class: E2_REVIEW_GATE
  disposition: HOLD_FOR_REVIEW

assurance:
  source: VERIFIED
  interpretation: REVIEWED
  rule: VERIFIED
  context: COMPLETE

review:
  requirement: SPECIALIST_REVIEW

enforcement:
  maximum_authorized_action: REVERSIBLE_HOLD

provenance:
  assessment_id: ...
  rule_refs: [...]
  source_refs: [...]

validity:
  effective_at: ...
  valid_until: ...
```

This is illustrative.

Canonical schemas belong in Shared.

---

# 137. Effect Class Must Travel with Decision

Consumers SHALL NOT infer effect class from:

```text
outcome
```

alone.

Incorrect:

```text
if outcome == PROHIBITED:
    block()
```

Correct:

```text
evaluate:
outcome
+
effect_class
+
disposition
+
validity
```

---

# 138. Reason Codes

Decision contracts SHOULD contain machine-readable reasons.

Examples:

```text
VERIFIED_PROHIBITION

MISSING_REQUIRED_PERMIT

MISSING_REQUIRED_CERTIFICATE

CLASSIFICATION_REVIEW_REQUIRED

SOURCE_CONFLICT

INTERPRETATION_AMBIGUOUS

STALE_REGULATORY_STATE

INCOMPLETE_CONTEXT

EVIDENCE_EXPIRED

HUMAN_REVIEW_REQUIRED
```

---

# 139. Reason Code Is Not Explanation

A reason code supports machines.

Human explanation supports people.

Both are useful.

Neither substitutes for source provenance.

---

# 140. Regulatory Hold State

Operational systems SHOULD distinguish regulatory holds from other holds.

Example:

```text
HOLD_REGULATORY

HOLD_CREDIT

HOLD_FRAUD

HOLD_INVENTORY

HOLD_MANUAL
```

This allows correct operational diagnosis.

---

# 141. Multiple Holds

A transaction may simultaneously have:

```text
regulatory hold

credit hold

inventory hold
```

Releasing one SHALL not release the others.

---

# 142. Regulations Cannot Release Non-Regulatory Holds

A favourable regulatory decision SHALL not override:

```text
fraud

credit

inventory

commercial
```

holds.

Domain boundaries remain intact.

---

# 143. Multiple Regulatory Reasons

One regulatory hold may have several independent requirements.

Example:

```text
permit missing
+
certificate expired
+
classification unresolved
```

Resolution SHALL require all applicable conditions.

---

# 144. Partial Remediation

When one requirement is resolved:

```text
3 outstanding
      ↓
2 outstanding
```

the engine should reflect partial remediation.

It SHALL not prematurely release the hold.

---

# 145. Review Before Irreversible External Communication

Actions such as:

```text
reporting violation to authority

making statutory declaration

filing admission

submitting suspicious-activity report
```

may carry independent legal obligations and confidentiality rules.

Baobab Regulations SHALL not treat them as ordinary enforcement effects.

They require separate domain-specific ADRs/policies.

---

# 146. No Automatic Self-Reporting by Default

Detection of possible non-compliance SHALL NOT automatically trigger external reporting unless a verified regulatory workflow specifically authorises and governs it.

---

# 147. Emergency Action

There may be circumstances where immediate prevention is safer than waiting for review.

Example:

```text
clear prohibited-goods match
```

A reversible hold MAY be applied immediately even if human confirmation follows.

This is different from irreversible disposition.

---

# 148. Break-Glass Release

A high-impact regulatory hold MAY support break-glass override where governance permits.

Requirements SHOULD include:

```text
strong authentication

explicit authority

reason

time limitation

audit

notification

post-event review
```

---

# 149. Break-Glass Is Not Convenience

It SHALL NOT be used to bypass ordinary regulation because:

```text
customer is important

shipment is late

executive requested it
```

unless authorised governance provides a legitimate basis.

---

# 150. Decision Audit

A consequential decision SHALL retain:

```text
assessment

outcome

effect class

risk class

disposition

rule versions

source versions

context snapshot

review requirement

review decisions

overrides

enforcement receipt

validity

correlation
```

where applicable.

---

# 151. Audit Is Append-Only in Principle

A reviewer changing their mind SHALL create a new review action.

It SHALL not erase the old one.

---

# 152. Effect-Class Change Audit

If a rule changes:

```text
E2 → E4
```

the historical E2 state SHALL remain traceable.

---

# 153. Metrics Must Distinguish Recommendation and Enforcement

Dashboards SHALL not combine:

```text
10,000 regulatory alerts
```

with:

```text
10,000 regulatory blocks
```

These are materially different.

---

# 154. Decision-Class Metrics

Recommended metrics include:

```text
reg_decisions_total{effect_class}

reg_reviews_total

reg_overrides_total

reg_enforcement_total

reg_decision_downgrades_total

reg_rule_suspensions_total
```

Exact telemetry naming remains implementation-specific.

---

# 155. Review Quality

Operational reporting SHOULD monitor:

```text
reviewer agreement

review reversals

time-to-review

review backlog

override causes
```

without turning regulatory staff into simplistic productivity scores.

---

# 156. Testing by Effect Class

Each effect class SHALL have different test expectations.

E0/E1:

```text
semantic correctness
explanation quality
```

E2:

```text
hold routing
review workflow
override
```

E3:

```text
condition lifecycle
automatic release
```

E4:

```text
golden cases
negative tests
false-positive testing
failure-mode testing
rollback
override
consumer enforcement
```

---

# 157. E4 Requires Strongest Regression Suite

A rule eligible for E4 SHALL require materially stronger regression confidence than one used only for research.

That is architectural common sense and SHALL be policy.

---

# 158. Golden Cases

E4 qualification SHOULD include:

```text
positive case

negative case

boundary case

exception case

effective-date case

missing-data case

conflict case

historical case
```

---

# 159. Golden Cases Must Include "Should Not Block"

Testing only:

```text
known prohibited examples
```

is insufficient.

False positives are commercially dangerous.

The suite MUST include:

```text
known permitted / non-applicable examples
```

where relevant.

---

# 160. Production Defect

If an E4 rule is discovered to be materially wrong:

```text
suspend rule
        │
        ▼
downgrade effect
        │
        ▼
impact analysis
        │
        ▼
identify affected decisions
        │
        ▼
review affected transactions
```

SHOULD be the incident flow.

---

# 161. Previous Enforcement Requires Investigation

Correcting the rule does not erase consequences already imposed.

The system SHOULD identify:

```text
transactions wrongly held

transactions wrongly blocked

customers affected

financial impact
```

for remediation.

---

# 162. Post-Decision Monitoring

High-impact automated regulatory controls SHOULD undergo continued monitoring after production activation.

The principle is supported by modern risk-management approaches, including NIST's lifecycle-oriented AI RMF and the EU AI Act's emphasis on monitoring high-risk systems throughout operation.

---

# 163. No "Set and Forget" Enforcement

Regulations evolve.

Automated controls must be reviewed when:

```text
law changes

authority changes

case law changes

source changes

product context changes

business model changes

rule engine changes

model changes
```

---

# 164. Effect Policy Versioning

Every effect policy SHALL be versioned.

Historical decisions must identify which effect policy authorised their operational authority.

---

# 165. Rule Version and Effect Policy Version Are Separate

Example:

```text
Rule:
3.1

Effect Policy:
7.4

Decision Engine:
2.3
```

All may change independently.

---

# 166. Simulation

Simulation SHALL never produce enforceable operational effect.

Maximum:

```text
E0
```

even if the simulated rule would otherwise qualify for E4.

---

# 167. Future-Rule Simulation

Useful questions include:

```text
What will happen when tariff rule X becomes effective?

Which orders would be blocked?

Which suppliers will need new documentation?
```

This is valuable for Pulse and enterprise customers.

But it remains simulation until effective.

---

# 168. Research Environment

Development/test/sandbox environments SHALL NOT emit production E4 authority.

A sandbox decision MUST be visibly non-production.

---

# 169. Environment Boundary

Conceptually:

```text
environment = sandbox
effect ceiling = E0
```

unless a controlled staging enforcement test is explicitly configured.

---

# 170. Provider Migration

When Regulations provider/rule-engine implementation changes, E4 decisions SHOULD be shadow-compared before migration.

This extends ADR-REG-0002's provider replacement architecture.

---

# 171. Semantic Equivalence

A replacement engine must demonstrate:

```text
same input
+
same rule set
=
same consequential decision
```

for appropriate deterministic golden cases.

---

# 172. Non-Deterministic Components

Where non-deterministic AI assists evaluation, its output SHALL not control E4 unless converted through governed verification into deterministic or separately approved regulatory state.

---

# 173. Effect-Class Architecture Summary

```text
E0
INFORMATIONAL
│
│ no workflow impact
▼
Research / Display

E1
ADVISORY
│
│ warn / recommend
▼
Proceed with awareness

E2
REVIEW_GATE
│
│ reversible hold
▼
Human / authorised review

E3
CONDITIONAL_ENFORCEMENT
│
│ objective prerequisite
▼
Hold until condition satisfied

E4
AUTOMATED_ENFORCEMENT
│
│ verified prohibition / hard requirement
▼
Automatic regulatory guard
```

---

# 174. Enforcement Philosophy

The architecture SHALL favour:

```text
prevent unsafe transition
```

over:

```text
automatically execute irreversible consequence.
```

This is a critical distinction.

---

# 175. Platform Maxim

> **Automation may close a gate more readily than it may destroy what lies beyond the gate.**

That maxim SHALL guide high-impact design.

---

# 176. Rejected Alternative — Outcome Equals Action

Rejected:

```text
PROHIBITED
    =
block automatically.
```

Reason:

regulatory conclusion and execution authority are different.

---

# 177. Rejected Alternative — Everything Requires Human Approval

Rejected.

It would make Baobab Regulations expensive, slow and commercially unimpressive.

Clear deterministic rules should eventually automate safely.

---

# 178. Rejected Alternative — Everything Automated

Rejected.

Not every legal rule is deterministic.

Not every source is certain.

Not every consequence is reversible.

---

# 179. Rejected Alternative — AI Confidence Controls Automation

Rejected:

```text
if model_confidence > .95:
    E4
```

Model confidence is not legal authority.

---

# 180. Rejected Alternative — Tenant Chooses Any Automation Level

Rejected.

Tenant preference does not override platform safety invariants.

---

# 181. Rejected Alternative — Global Fail-Closed

Rejected.

Some regulatory failures justify hold.

Others justify advisory degradation.

Context matters.

---

# 182. Rejected Alternative — Global Fail-Open

Rejected.

Missing regulatory capability cannot always be treated as permission.

---

# 183. Rejected Alternative — Reviewer Is Rubber Stamp

Rejected.

Effective human oversight requires information, competence and actual authority to disagree.

---

# 184. Rejected Alternative — Override Mutates Decision

Rejected.

Decision and override must both remain auditable.

---

# 185. Rejected Alternative — E4 Allows Arbitrary Mutation

Rejected.

E4 authorises only specifically configured regulatory enforcement actions.

---

# 186. Rejected Alternative — "Compliant = true"

Rejected.

Regulatory compliance is always contextual and scoped to:

```text
rules
context
time
evidence
```

---

# 187. Positive Consequences

This architecture enables Baobab to become progressively more valuable:

```text
regulatory search
        ↓
regulatory advice
        ↓
regulatory review
        ↓
regulatory gating
        ↓
automated regulatory execution
```

without jumping irresponsibly from information to automation.

---

# 188. Commercial Consequence

Baobab can offer customers graduated operating modes.

Conceptually:

```text
OBSERVE

ADVISE

ASSIST

GOVERN

ENFORCE
```

while maintaining the same underlying regulatory knowledge model.

This could become commercially powerful.

---

# 189. Trust Consequence

Customers can understand:

```text
what Baobab concluded
```

and separately:

```text
what Baobab was authorised to do.
```

This is essential for enterprise adoption.

---

# 190. Operational Consequence

Trade, ERP, CMS, IAM and future engines receive machine-actionable regulatory effects without losing ownership of their business state.

---

# 191. Safety Consequence

Uncertainty tends toward:

```text
review
```

rather than fabricated certainty.

Verified objective regulation can progressively gain automation.

---

# 192. Cost Consequence

Human review has cost.

The architecture therefore creates an economic incentive to:

```text
improve source quality
improve interpretations
improve deterministic rules
improve testing
```

so common cases can safely move:

```text
E2 → E3 → E4.
```

That is desirable.

---

# 193. Profitable Automation Flywheel

```text
High review volume
       │
       ▼
identify repetitive regulatory cases
       │
       ▼
improve structured rules
       │
       ▼
verify / golden-test
       │
       ▼
promote safe automation
       │
       ▼
lower customer compliance cost
       │
       ▼
higher Baobab value
```

This is one of the commercial mechanisms by which Regulations can become highly profitable.

---

# 194. Architectural Invariants

| ID | Invariant |
|---|---|
| `REG-D-I01` | Assessment outcome and operational effect SHALL remain separate |
| `REG-D-I02` | A `PROHIBITED` outcome does not automatically imply E4 |
| `REG-D-I03` | `INDETERMINATE` SHALL never directly authorise E4 |
| `REG-D-I04` | Unverified generative-AI inference SHALL not independently authorise E3/E4 |
| `REG-D-I05` | E2 SHALL use reversible review gates |
| `REG-D-I06` | E3 SHALL primarily enforce objective remediable prerequisites |
| `REG-D-I07` | E4 requires explicit governed eligibility |
| `REG-D-I08` | E4 SHALL not automatically authorise irreversible business actions |
| `REG-D-I09` | Consumers SHALL not escalate Regulations' effect class |
| `REG-D-I10` | Consumers MAY apply stricter policy if the different authority is recorded |
| `REG-D-I11` | Effect-class promotion SHALL be audited |
| `REG-D-I12` | Regulatory rules SHALL support effect ceilings |
| `REG-D-I13` | Human review SHALL be meaningful, informed and attributable |
| `REG-D-I14` | Overrides SHALL preserve the original decision |
| `REG-D-I15` | Review authority SHALL be scoped |
| `REG-D-I16` | Infrastructure failure SHALL not become a regulatory outcome |
| `REG-D-I17` | Source/rule degradation may downgrade effect authority |
| `REG-D-I18` | Automated enforcement SHALL be suspendable |
| `REG-D-I19` | Every E3/E4 enforcement SHALL be traceable to its source/rule/decision |
| `REG-D-I20` | Regulatory enforcement and business consequences remain distinct |
| `REG-D-I21` | Simulation SHALL never carry production enforcement authority |
| `REG-D-I22` | Regulatory effect policy SHALL be versioned |
| `REG-D-I23` | Irreversible actions require separately authorised workflows |
| `REG-D-I24` | Review timeout SHALL not silently mean allow or deny |
| `REG-D-I25` | Automation may escalate caution more easily than coercion |

---

# 195. Initial ZuriBeans Rollout

The initial ZuriBeans implementation SHOULD deliberately start below E4.

Recommended rollout:

```text
PHASE 1
E0
Regulatory information

PHASE 2
E1
Warnings / obligations

PHASE 3
E2
Review holds

PHASE 4
E3
Verified documentation gates

PHASE 5
E4
Selected deterministic prohibitions
```

---

# 196. Initial E3 Candidates

Potential early candidates include objective requirements such as:

```text
mandatory permit absent

certificate expired

required document absent

mandatory licence not active
```

subject to rule verification.

---

# 197. Initial E4 Candidates

E4 should be much narrower.

Potential candidate:

```text
explicit verified prohibited-goods rule
+
unambiguous classification
+
complete context
+
current source
```

Even then, the automated action SHOULD initially be:

```text
prevent shipment progression
```

rather than:

```text
cancel commercial relationship.
```

---

# 198. Initial Non-E4 Cases

The following SHOULD remain review-oriented initially:

```text
ambiguous HS classification

complex rules-of-origin interpretation

discretionary SPS requirement

conflicting authority

AI-only interpretation

novel legal question

tenant counsel disagreement

newly changed legislation
```

---

# 199. Minimum Proof

Before ADR-REG-0004 is considered implemented, Baobab SHOULD demonstrate:

```text
1.
One E0 information-only case.

2.
One E1 advisory case.

3.
One E2 human-review case.

4.
One E3 documentary-condition gate.

5.
One shadow E4 case.

6.
Human reviewer can override E2.

7.
Override preserves original decision.

8.
Consumer cannot escalate E1 into E4.

9.
Stale source automatically downgrades an E4 candidate.

10.
Rule conflict forces review.

11.
LLM-only result cannot achieve E3/E4.

12.
Trade produces an enforcement receipt.

13.
Regulatory hold is separate from commercial hold.

14.
A decision can be suspended without deleting history.

15.
An irreversible action requires a separate workflow.
```

---

# 200. Production E4 Gate

No rule SHALL enter production E4 until, at minimum:

```text
source verified

authority identified

legal status understood

interpretation reviewed

machine rule verified

rule effective

coverage sufficient

context requirements explicit

golden tests pass

negative tests pass

exceptions tested

shadow execution reviewed

effect policy approved

override path tested

audit tested

consumer enforcement tested

suspension tested

observability enabled
```

---

# 201. Follow-On ADRs

This ADR enables:

```text
ADR-REG-0005
Provider-Neutral Regulatory Intelligence Architecture
```

and later:

```text
ADR-REG-0016
Machine-Executable Regulatory Rules Representation

ADR-REG-0017
Regulatory Context and Applicability Resolution

ADR-REG-0018
Regulatory Decision and Evaluation Engine

ADR-REG-0019
Policy Decision Point and Enforcement Point Separation

ADR-REG-0020
Decision Explainability, Replay and Reproducibility

ADR-REG-0022
Human Verification, Confidence and Governance Workflow

ADR-REG-0025
Testing, Golden Cases and Decision Regression
```

`ADR-REG-0019` will elaborate the technical PDP/PEP contract.

This ADR establishes the **authority model** that contract must carry.

---

# 202. Research Foundation

NIST's AI RMF states that organisations should explicitly define human/AI roles and document oversight processes according to context.

NIST's Generative AI Profile highlights confabulated facts, logic and citations as material risks in consequential decision-making, supporting Baobab's decision that generative inference alone must not obtain automatic enforcement authority.

The OECD AI Principles emphasise human agency, oversight, transparency, explainability, robustness and the ability to override systems that risk causing harm.

The EU AI Act's Article 14 provides a concrete risk-proportionate human-oversight model and requires appropriately positioned humans to understand system limitations, recognise automation bias, interpret outputs, override or reverse them and safely stop operation.

South Africa's POPIA section 71 provides a locally relevant example of legal safeguards around certain solely automated decisions with legal or substantial effects, including opportunities to make representations and access to information about underlying logic in specified cases.

Open Policy Agent demonstrates the mature architectural principle of separating a Policy Decision Point from a Policy Enforcement Point, reinforcing Baobab's decision that Regulations should determine regulatory effects while domain systems retain operational state ownership.

---

# 203. Final Decision

Baobab Regulations SHALL implement a progressive regulatory authority model:

```text
               REGULATORY KNOWLEDGE
                        │
                        ▼
                   ASSESSMENT
                        │
                        ▼
                     OUTCOME
                        │
                        ▼
               EFFECT AUTHORITY
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
      INFORM          REVIEW         ENFORCE
```

with five concrete effect classes:

```text
E0 INFORMATIONAL
        │
        ▼
No operational consequence


E1 ADVISORY
        │
        ▼
Warn / recommend


E2 REVIEW_GATE
        │
        ▼
Reversible hold + authorised review


E3 CONDITIONAL_ENFORCEMENT
        │
        ▼
Enforce objective remediable requirement


E4 AUTOMATED_ENFORCEMENT
        │
        ▼
Automatically prevent prohibited transition
under strictly governed conditions
```

The engine SHALL optimise for progression toward safe automation:

```text
research
    ↓
advice
    ↓
review
    ↓
conditional enforcement
    ↓
verified automatic enforcement
```

but SHALL never confuse technological ability with regulatory authority.

The most important consequence of this ADR is:

> **Baobab Regulations may eventually become powerful enough to stop a transaction automatically, but it must always be able to prove why it was entitled to do so.**

And even then:

> **Stopping a prohibited transition is not the same as granting a machine authority to decide every consequence that follows.**

That distinction protects customers.

It protects Baobab.

And commercially, it allows us to do something much stronger than either extreme:

```text
"AI tells you what regulations might say"
```

or:

```text
"black-box compliance software blocks things."
```

The intended Baobab proposition is:

> **Regulatory automation with graduated authority, explainable evidence, human challenge, controlled enforcement and safe escalation.**

That is the foundation required for Regulations to become a trusted part of the transaction path rather than merely another compliance dashboard.

---

## Decision Summary

```text
ADR-REG-0004
─────────────────────────────────────────────

CORE DECISION

Regulatory outcome
        ≠
Operational authority.

EFFECT CLASSES

E0  INFORMATIONAL
E1  ADVISORY
E2  REVIEW_GATE
E3  CONDITIONAL_ENFORCEMENT
E4  AUTOMATED_ENFORCEMENT

KEY RULE

Automation may escalate caution
more easily than coercion.

AI CEILING

Unverified generative AI:
maximum E2.

E4 REQUIRES

verified source
verified interpretation
verified rule
complete context
current law
no material conflict
deterministic evaluation
golden testing
approved effect policy
audit
override
suspension
consumer enforcement contract

HUMAN OVERSIGHT

must be informed
must be competent
must be authorised
must be able to disagree
must be able to override

ENFORCEMENT

Regulations decides.
Domain engine enforces.

IRREVERSIBLE ACTIONS

require separate explicit authority.

COMMERCIAL DIRECTION

Observe
 → Advise
 → Review
 → Govern
 → Enforce

STRATEGIC RESULT

Baobab can become regulatory infrastructure
without becoming an uncontrolled
automated decision-maker.
```
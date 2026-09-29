# ADR-REG-0023 — Regulatory Change Detection and Impact Analysis

**Subtitle:** Source Change Monitoring, Legal Change Qualification, Dependency Graph Propagation, Blast-Radius Analysis and Targeted Regulatory Reassessment

**Status:** Proposed — Foundational Regulatory Change Architecture  
**Decision ID:** `ADR-REG-0023`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-29  
**Decision Type:** Regulatory Change / Legal Lifecycle / Impact Analysis / Reassessment / Eventing / Change Intelligence  
**Strategic Classification:** Core Regulatory Change and Operational Resilience Infrastructure

---

# 1. Executive Decision

Baobab Regulations SHALL implement a governed regulatory change architecture that transforms:

```text
SOURCE SIGNAL
      │
      ▼
SOURCE CHANGE
      │
      ▼
LEGAL CHANGE CANDIDATE
      │
      ▼
VERIFICATION
      │
      ▼
VERIFIED REGULATORY CHANGE
      │
      ▼
REGULATORY KNOWLEDGE IMPACT
      │
      ▼
CANDIDATE BUSINESS IMPACT
      │
      ▼
TARGETED REASSESSMENT
      │
      ▼
CONFIRMED DECISION / TRANSACTION IMPACT
      │
      ▼
NOTIFICATION / REMEDIATION / ENFORCEMENT
```

The governing doctrine is:

> **A changed source is not necessarily a changed law; a changed law is not necessarily relevant to a tenant; relevance is not necessarily material impact; and material impact is not established until the affected regulatory context is reassessed.**

---

# 2. Depends On

This ADR SHALL be interpreted consistently with:

- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy`
- `ADR-REG-0008 — Instrument, Provision, Rule, Obligation and Requirement`
- `ADR-REG-0009 — Normative Semantics, Defeasibility and Conflict Resolution`
- `ADR-REG-0010 — Regulatory Knowledge Graph and Relationship Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0012 — Regulatory Content Acquisition, Licensing and Reuse Rights`
- `ADR-REG-0013 — Source Ingestion, Normalisation and Adapter Architecture`
- `ADR-REG-0014 — Provenance, Citation and Evidentiary Chain`
- `ADR-REG-0015 — Temporal and Bitemporal Regulatory Versioning`
- `ADR-REG-0016 — Machine-Executable Regulatory Rules Representation and Intermediate Language`
- `ADR-REG-0017 — Regulatory Context and Applicability Resolution`
- `ADR-REG-0018 — Regulatory Decision and Evaluation Engine`
- `ADR-REG-0019 — Policy Decision Point and Enforcement Point Separation`
- `ADR-REG-0020 — Decision Explainability, Replay and Reproducibility`
- `ADR-REG-0021 — AI-Assisted Regulatory Extraction and Interpretation Boundary`
- `ADR-REG-0022 — Human Verification, Confidence and Regulatory Knowledge Governance Workflow`

It SHALL also remain consistent with Baobab Control Plane's controlled-change principles:

```text
Change
  ↓
Validate
  ↓
Impact Analyse
  ↓
Plan
  ↓
Approve
  ↓
Execute
  ↓
Reconcile
  ↓
Verify.
```

---

# 3. Research Finding — Legislative Change Has Explicit Lifecycle Semantics

Akoma Ntoso explicitly models the lifecycle and evolution of legal documents and distinguishes events such as generation and amendment. Its amendment metadata can express operations such as:

```text
repeal

substitution

insertion

split

join

renumbering
```

and can record source, target/destination, temporal parameters and limitations of a modification.

Baobab SHALL preserve similarly explicit legal-change semantics.

---

# 4. Research Finding — Document Change and Legal Effect Are Distinct

Akoma Ntoso distinguishes:

```text
active modifications
```

from:

```text
passive modifications
```

and supports modifications concerning:

```text
text

meaning

scope

force

efficacy

legal system.
```

This demonstrates that regulatory change cannot safely be represented merely as a textual diff.

---

# 5. Research Finding — ELI Explicitly Models Legislative Relationships

The current ELI ontology includes relationships such as:

```text
changes / changed_by

amends / amended_by

repeals / repealed_by

corrects / corrected_by

commences / commenced_by

consolidates / consolidated_by
```

as well as legal validity/effective-date metadata.

Baobab SHOULD preserve equivalent expressive power in its canonical change model.

---

# 6. Research Finding — ELI-Impact Goes Further

ELI's current implementation guidance includes **ELI-Impact (ELI-I)**, a formal model intended to describe how legislative acts affect existing law and consolidated versions, including detailed amendment impact.

This validates Baobab's decision to model:

```text
what changed

what was targeted

how it changed

when that change takes effect
```

rather than merely recording that “a new document appeared.”

---

# 7. Research Finding — Synchronisation Is First-Class

ELI Pillar 4 defines mechanisms by which publishers can expose complete identifier sets and daily updates using sitemaps and Atom feeds, allowing downstream consumers to keep legislative metadata synchronised.

Baobab SHALL exploit such publisher-native mechanisms where available rather than relying solely on scraping.

---

# 8. Research Finding — Consolidated Text May Not Itself Carry Legal Effect

EUR-Lex explicitly distinguishes consolidation from codification and states that consolidated texts are documentation aids rather than new legal acts with independent legal effect.

Therefore:

```text
consolidated text changed
```

does not automatically mean:

```text
new legal authority created.
```

---

# 9. Research Finding — Revision Must Preserve Lineage

W3C PROV models revision as a specialised form of derivation in which the new entity is a revised version of an earlier entity, while invalidation records cessation or expiry.

Baobab SHALL maintain revision and supersession lineage rather than mutating regulatory objects in place.

---

# 10. Fundamental Distinctions

Baobab SHALL distinguish:

```text
SOURCE SIGNAL
≠
SOURCE CHANGE

SOURCE CHANGE
≠
DOCUMENT REVISION

DOCUMENT REVISION
≠
LEGAL CHANGE

LEGAL CHANGE
≠
REGULATORY KNOWLEDGE CHANGE

REGULATORY KNOWLEDGE CHANGE
≠
RULE CHANGE

RULE CHANGE
≠
APPLICABILITY CHANGE

APPLICABILITY CHANGE
≠
BUSINESS IMPACT

BUSINESS IMPACT
≠
CONFIRMED DECISION CHANGE.
```

---

# 11. Source Signal

A `SourceChangeSignal` means:

> **Something associated with a monitored source appears to have changed.**

Examples:

```text
new Atom entry

API change token

new Gazette issue

ETag changed

Last-Modified changed

hash changed

new regulator notice

new file

new court judgment

Pulse detected announcement

vendor webhook

manual analyst alert.
```

---

# 12. Signal Is Not Truth

A signal MAY represent:

```text
actual new law

metadata correction

website redesign

re-pagination

file recompression

OCR correction

publisher typo

duplicate document

provider schema change

irrelevant publication.
```

---

# 13. SourceChangeSignal

Conceptually:

```text
SourceChangeSignal
├── signal_id
├── source_ref
├── source_channel_ref
├── provider_ref?
├── signal_type
├── external_identifier?
├── observed_at
├── publisher_timestamp?
├── cursor/checkpoint?
├── content_locator?
├── prior_artifact_ref?
├── signal_payload_hash?
├── processing_priority
└── provenance
```

---

# 14. Signal Types

Initial values MAY include:

```text
NEW_RESOURCE

RESOURCE_UPDATED

RESOURCE_REMOVED

METADATA_UPDATED

FEED_ENTRY

WEBHOOK

HASH_CHANGED

ETAG_CHANGED

MANUAL_REPORT

PULSE_LEAD

AUTHORITY_NOTICE

PROVIDER_CORRECTION.
```

---

# 15. Detection Sources

Baobab SHOULD support:

```text
official API

official Gazette feed

ELI Pillar 4 feed

RSS / Atom

sitemap

bulk dataset

commercial provider API

webhook

scheduled polling

object/file delivery

manual analyst upload

Pulse discovery signal.
```

---

# 16. Preferred Detection Hierarchy

Where available, prefer:

```text
authoritative machine feed
        ↓
official API
        ↓
official structured metadata
        ↓
official publication page
        ↓
licensed provider
        ↓
controlled crawler
        ↓
general web discovery.
```

This hierarchy concerns detection reliability, not automatically legal authority.

---

# 17. Polling State

Each monitored source SHOULD maintain a durable:

# `SourceMonitorCheckpoint`

---

# 18. SourceMonitorCheckpoint

Conceptually:

```text
SourceMonitorCheckpoint
├── source_ref
├── channel_ref
├── provider_cursor?
├── last_seen_identifier?
├── last_modified?
├── etag?
├── last_content_hash?
├── last_successful_poll
├── next_poll?
├── consecutive_failures
├── adapter_version
└── provenance
```

---

# 19. Polling Checkpoint Is Operational State

It does not define legal chronology.

---

# 20. Missed Poll Does Not Mean No Change

Correct:

```text
MONITORING_GAP
```

not:

```text
NO_REGULATORY_CHANGE.
```

---

# 21. Immutable Acquisition

A credible change signal SHALL flow through ADR-REG-0013 acquisition.

```text
signal
  ↓
fetch
  ↓
new immutable SourceArtefact
```

---

# 22. Never Overwrite Prior Artefact

Even if publisher URL remains unchanged:

```text
Artefact v1
```

and:

```text
Artefact v2
```

SHALL remain separately identifiable.

---

# 23. Content Hash

Content hashes SHOULD detect byte-level differences.

But:

```text
hash change
```

does not tell Baobab:

```text
what legally changed.
```

---

# 24. Hash Stable

Likewise:

```text
same bytes
```

does not guarantee:

```text
same legal effect.
```

External commencement or judicial events may affect the law without changing those bytes.

---

# 25. Change Detection Layers

Baobab SHALL use multiple layers:

```text
L0 — Transport Change

L1 — Artefact Change

L2 — Structural Document Change

L3 — Semantic Legal Change Candidate

L4 — Verified Legal Change

L5 — Canonical Knowledge Impact

L6 — Business Impact Candidate

L7 — Confirmed Assessment/Decision Impact.
```

---

# 26. L0 — Transport Change

Examples:

```text
URL changed

HTTP metadata changed

feed item created.
```

---

# 27. L1 — Artefact Change

Examples:

```text
different bytes

different file

different official edition.
```

---

# 28. L2 — Structural Change

Examples:

```text
section added

paragraph replaced

table changed

schedule added

article renumbered.
```

---

# 29. L3 — Legal Change Candidate

Machine analysis proposes:

```text
this new act appears to amend Section 17

this notice appears to commence Regulation X

this Gazette appears to repeal Rule Y.
```

---

# 30. L4 — Verified Legal Change

Governed verification from ADR-REG-0022 establishes:

```text
what legal relationship actually changed

which legal objects are affected

what dates govern the effect.
```

---

# 31. L5 — Canonical Knowledge Impact

Determine whether canonical:

```text
InstrumentVersion

ProvisionVersion

Interpretation

RuleVersion

RegulatoryRegime

AuthorityRelationship
```

must change.

---

# 32. L6 — Business Impact Candidate

Traverse dependencies to identify potentially affected:

```text
jurisdictions

profiles

products

classifications

trade lanes

legal entities

transactions

decisions.
```

---

# 33. L7 — Confirmed Business Impact

Targeted reassessment determines:

```text
actual outcome changed

requirements changed

decision unchanged

review required.
```

---

# 34. RegulatoryChange

Baobab SHALL define a first-class:

# `RegulatoryChange`

---

# 35. RegulatoryChange

Conceptually:

```text
RegulatoryChange
├── change_id
├── change_type
├── source_refs[]
├── authority_ref
├── triggering_artifact_refs[]
├── affected_instrument_refs[]
├── affected_provision_refs[]
├── legal_effect_description
├── legal_valid_from?
├── legal_valid_to?
├── publication_time?
├── knowledge_time
├── observed_at
├── change_status
├── verification_state
├── provenance
└── change_fingerprint
```

---

# 36. Change Types

Initial canonical values SHOULD include:

```text
ENACTMENT

AMENDMENT

INSERTION

SUBSTITUTION

REPEAL

PARTIAL_REPEAL

CORRECTION

RECTIFICATION

COMMENCEMENT

SUSPENSION

REVIVAL

EXPIRY

EXTENSION

RENUMBERING

CONSOLIDATION

SCOPE_CHANGE

FORCE_CHANGE

EFFICACY_CHANGE

MEANING_CHANGE

JURISDICTION_CHANGE

REGIME_MEMBERSHIP_CHANGE

AUTHORITY_CHANGE

GUIDANCE_CHANGE

JUDICIAL_INTERPRETATION

ADMINISTRATIVE_RULING

TARIFF_CHANGE

RATE_CHANGE

THRESHOLD_CHANGE

CLASSIFICATION_CHANGE

DOCUMENT_REQUIREMENT_CHANGE

PERMIT_REQUIREMENT_CHANGE

UNKNOWN_CHANGE_TYPE.
```

---

# 37. Textual and Normative Change Are Different

Example:

```text
"shall submit within 30 days"
```

changes to:

```text
"shall submit within 14 days".
```

This is both:

```text
TEXTUAL CHANGE
```

and:

```text
NORMATIVE DEADLINE CHANGE.
```

---

# 38. Pure Editorial Change

Example:

```text
spelling correction

formatting change

page numbering.
```

May produce:

```text
DOCUMENT_CHANGE
```

but:

```text
NO_NORMATIVE_CHANGE.
```

---

# 39. Normative Change Without Direct Text Replacement

Examples:

```text
commencement notice

court ruling

expiry

authority ruling

treaty entering into force.
```

Legal effect may change although base statutory wording remains unchanged.

---

# 40. Consolidation Change

A new consolidated document SHALL normally be treated as:

```text
DERIVED REPRESENTATION_CHANGE
```

until its underlying amendment relationships are established.

---

# 41. Consolidation SHALL NOT Manufacture New Legal Effect

Consistent with source-specific legal status.

---

# 42. Correction versus Amendment

Baobab SHALL distinguish:

```text
publisher correction

legal corrigendum / rectification

parser correction

Baobab interpretation correction.
```

These have very different consequences.

---

# 43. Parser Correction

If Baobab previously parsed:

```text
15%
```

as:

```text
5%
```

and fixes extraction:

```text
SOURCE LAW DID NOT CHANGE.
```

Baobab knowledge changed.

---

# 44. Knowledge Correction

This is:

```text
REGULATORY_KNOWLEDGE_CORRECTION
```

rather than:

```text
LEGAL_AMENDMENT.
```

---

# 45. Important Consequence

Knowledge corrections can still have enormous business impact.

Therefore impact analysis applies to both:

```text
external legal change
```

and:

```text
internal knowledge correction.
```

---

# 46. RegulatoryChangeOrigin

Initial values:

```text
EXTERNAL_LEGAL_CHANGE

OFFICIAL_CORRECTION

NEW_AUTHORITY_DECISION

BAOBAB_SOURCE_CORRECTION

BAOBAB_EXTRACTION_CORRECTION

BAOBAB_INTERPRETATION_CORRECTION

BAOBAB_RULE_CORRECTION

PROVIDER_CORRECTION.
```

---

# 47. Change Status

Potential:

```text
DETECTED

ACQUIRED

ANALYSING

CANDIDATE

UNDER_REVIEW

VERIFIED

REJECTED

PUBLISHED

IMPACT_ANALYSING

REASSESSMENT_REQUIRED

COMPLETED

SUPERSEDED.
```

---

# 48. Time Is Multidimensional

A change SHALL preserve at least:

```text
publication_time

legal_valid_time

system_observed_time

knowledge_time.
```

where applicable.

---

# 49. Example

Gazette published:

```text
1 October
```

Rule takes effect:

```text
15 October
```

Baobab discovers it:

```text
3 October
```

Baobab verifies it:

```text
4 October.
```

These are four distinct times.

---

# 50. Retroactive Change

Law may state:

```text
effective from 1 September
```

while published:

```text
20 September.
```

ADR-REG-0015 bitemporal rules apply.

---

# 51. Retroactive Impact

Potentially affects:

```text
decisions made after 1 September

or even earlier transactions
whose legal event time falls within retroactive scope.
```

---

# 52. Future-Effective Change

A law may be published today but take effect later.

Baobab SHOULD support:

```text
verified now

future effective.
```

---

# 53. Future Change Can Trigger Planning Impact

Even before legal commencement:

```text
planned January shipment
```

may be affected by:

```text
rule effective January 1.
```

---

# 54. Change Candidate Detection

Docling/Haystack/AI MAY identify:

```text
new provisions

deleted provisions

changed tables

amendment targets

legal dates

normative phrases

relationships.
```

---

# 55. AI Change Detection Is Candidate State

As established in ADR-REG-0021:

```text
model detected change
```

does not equal:

```text
verified legal change.
```

---

# 56. Structural Diff

Baobab SHOULD implement legal-aware structural differencing.

---

# 57. LegalStructuralDiff

Conceptually:

```text
LegalStructuralDiff
├── old_artifact_ref
├── new_artifact_ref
├── matched_nodes[]
├── inserted_nodes[]
├── removed_nodes[]
├── modified_nodes[]
├── moved_nodes[]
├── renumbered_nodes[]
├── table_changes[]
├── citation_changes[]
└── provenance
```

---

# 58. Node Matching

Should use, where available:

```text
canonical IDs

ELI IDs

Akoma Ntoso eId/wId

official section identifiers

structural position

textual similarity.
```

---

# 59. Renumbering Must Not Look Like Repeal + New Rule

Example:

```text
Section 13
→
Section 14
```

with same underlying provision.

Correct:

```text
RENUMBERING
```

rather than:

```text
DELETE Section 13
+
ADD unrelated Section 14.
```

---

# 60. Akoma Ntoso Supports This Distinction

Its amendment model explicitly supports renumbering and references between previous and current structural identifiers.

---

# 61. Semantic Diff

Structural change SHALL feed:

# `LegalSemanticDiff`

---

# 62. LegalSemanticDiff

Conceptually:

```text
LegalSemanticDiff
├── changed_normative_effects[]
├── changed_actor_roles[]
├── changed_conditions[]
├── changed_exceptions[]
├── changed_thresholds[]
├── changed_deadlines[]
├── changed_classifications[]
├── changed_jurisdictions[]
├── changed_scope[]
├── changed_effective_dates[]
├── changed_cross_references[]
├── changed_hierarchy_relations[]
└── unresolved_semantic_changes[]
```

---

# 63. Semantic Diff Requires Governance

A model MAY draft it.

Qualified review establishes the verified change.

---

# 64. No Universal Severity Score

Rejected:

```text
change_severity = 87.
```

---

# 65. Change Materiality Is Multidimensional

Potential dimensions:

```text
legal force

subject scope

jurisdiction scope

activity scope

product scope

effect type

timing

number of dependencies

decision consequence.
```

---

# 66. Change May Be Narrow but Critical

Example:

```text
one HS code

one prohibited commodity

one jurisdiction

one effective date.
```

Few objects affected.

But for those objects:

```text
critical.
```

---

# 67. Change May Be Broad but Low Consequence

Example:

```text
renumber all sections
without changing semantics.
```

Large textual blast radius.

Small regulatory decision impact.

---

# 68. Change Verification

ADR-REG-0022 governance SHALL apply to substantive legal changes.

---

# 69. Verified Change Needs

Depending on consequence:

```text
source verification

authority verification

amendment relationship

target verification

legal effective time

semantic analysis

maker/checker

specialist/legal review

tests.
```

---

# 70. Impact Shall Not Wait for Full Publication Where Useful

Baobab MAY perform:

```text
PRELIMINARY_IMPACT_ANALYSIS
```

on verified-enough candidate information.

---

# 71. Preliminary Impact Is Not Confirmed Impact

Clearly label:

```text
CANDIDATE IMPACT.
```

---

# 72. Regulatory Knowledge Graph Is Central

ADR-REG-0010 becomes the foundation for blast-radius analysis.

---

# 73. Change Graph

Conceptually:

```text
SourceArtefact
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
RuleVersion
      │
      ▼
RegulatoryEffect
      │
      ▼
RegulatoryProfile
      │
      ▼
Context Dimensions
      │
      ▼
Assessment
      │
      ▼
Decision
      │
      ▼
Enforcement
```

---

# 74. Reverse Traversal

Change impact moves:

```text
LEGAL SOURCE
      ↓
KNOWLEDGE
      ↓
RULE
      ↓
BUSINESS.
```

---

# 75. Decision Explanation Traversal Moves Opposite

```text
Decision
      ↓
Rule
      ↓
Source.
```

The same graph supports both.

---

# 76. Direct and Transitive Impact

Baobab SHALL distinguish:

```text
DIRECT_DEPENDENCY

TRANSITIVE_DEPENDENCY.
```

---

# 77. Direct Impact

Example:

```text
Provision P changed.

Rule R directly interprets P.
```

---

# 78. Transitive Impact

```text
P changes
  ↓
Definition D changes
  ↓
Rules R1, R2, R3 depend on D.
```

---

# 79. Constitutive Rule Impact

Changes to legal definitions may propagate widely.

Example:

```text
definition of "processed coffee"
```

may alter applicability of many rules.

---

# 80. Cross-Reference Impact

A rule not textually changed may be impacted because it references:

```text
another amended provision.
```

---

# 81. Hierarchy Impact

A new superior rule may defeat:

```text
existing lower-level rules.
```

even where those rules' wording remains unchanged.

---

# 82. Regime Impact

New trade-agreement membership or commencement may affect:

```text
rules of origin

tariffs

document requirements

applicability.
```

---

# 83. Authority Impact

A regulator's jurisdiction or competence may itself change.

This can affect:

```text
source authority

rule applicability

decision authority.
```

---

# 84. RegulatoryChangeImpact

Baobab SHALL define:

# `RegulatoryChangeImpact`

---

# 85. RegulatoryChangeImpact

Conceptually:

```text
RegulatoryChangeImpact
├── impact_id
├── change_ref
├── impacted_entity_ref
├── impacted_entity_type
├── impact_path[]
├── impact_kind
├── impact_status
├── materiality
├── legal_time_range
├── tenant_scope?
├── requires_reassessment
├── reason_codes[]
└── provenance
```

---

# 86. Impact Kinds

Initial values MAY include:

```text
DIRECT

DEPENDENCY

APPLICABILITY

INTERPRETATION

RULE_SEMANTICS

REQUIREMENT

CLASSIFICATION

COVERAGE

DECISION

ENFORCEMENT

CONTENT

INFORMATIONAL.
```

---

# 87. Impact Status

Potential:

```text
CANDIDATE

CONFIRMED

NOT_IMPACTED

REASSESSMENT_REQUIRED

REVIEW_REQUIRED

RESOLVED.
```

---

# 88. Impact Path Is Valuable

Example:

```text
Amending Act A
  ↓ AMENDS
Provision P
  ↓ INTERPRETED_BY
Rule R
  ↓ USED_BY
Decision D.
```

---

# 89. Impact Path Provides Explainability

User can ask:

> Why was my prior shipment decision reassessed?

Answer:

```text
because new Act A amended Provision P,
which Rule R interpreted,
and Rule R contributed to Decision D.
```

---

# 90. Candidate Blast Radius

The graph first computes a superset:

# `CandidateImpactSet`

---

# 91. CandidateImpactSet May Include

```text
RuleVersions

DecisionPolicies

RegulatoryProfiles

JurisdictionPacks

ProductClassifications

Tenants

LegalEntities

TradeLanes

OpenTransactions

HistoricalDecisions

CMS projections

Pulse subscriptions.
```

---

# 92. Candidate Impact Is Not Confirmed

Graph reachability alone does not establish material business impact.

---

# 93. Example

Provision P changes.

Decision D used Rule R linked to P.

But:

```text
new amendment effective after D's legal time.
```

Therefore historical decision may remain unaffected.

---

# 94. Temporal Filtering Is Mandatory

Blast-radius traversal SHALL apply:

```text
legal time

knowledge time

effective period
```

before confirming reassessment eligibility.

---

# 95. Applicability Filtering Is Mandatory

A rule may cover:

```text
all coffee imports
```

while transaction uses:

```text
vanilla.
```

Graph relationship alone is insufficient.

---

# 96. Context Filtering

Candidate impacted decisions SHOULD be filtered by:

```text
jurisdiction

activity

actor role

classification

regime

legal entity

transaction geography

legal time.
```

---

# 97. Progressive Impact Analysis

Preferred stages:

```text
Stage 1
Graph reachability

Stage 2
Temporal filtering

Stage 3
Context filtering

Stage 4
Rule semantic comparison

Stage 5
Targeted reassessment.
```

---

# 98. This Prevents Reassessing Everything

Baobab SHALL avoid:

```text
one Gazette change
→
recalculate every transaction ever.
```

---

# 99. Reassessment Candidate

Baobab SHALL define:

# `ReassessmentCandidate`

---

# 100. ReassessmentCandidate

Conceptually:

```text
ReassessmentCandidate
├── candidate_id
├── change_ref
├── prior_assessment_ref?
├── prior_decision_ref?
├── subject_ref
├── context_snapshot_ref?
├── candidate_reason[]
├── affected_rule_refs[]
├── priority
├── requested_mode
├── legal_time
├── status
└── provenance
```

---

# 101. Historical Decisions

A change can affect historical decisions in at least three different ways.

---

# 102. Case 1 — Law Actually Changed Later

Example:

```text
old decision: March

law changed: June.
```

March decision remains historically correct.

No historical restatement required.

---

# 103. Case 2 — Baobab Discovered Old Law Late

Example:

```text
law effective March

Baobab discovers in June.
```

Historical decisions from March onward may require:

```text
CURRENT_KNOWLEDGE_RESTATEMENT.
```

---

# 104. Case 3 — Baobab Had Knowledge Defect

Example:

```text
wrong tariff threshold encoded.
```

All decisions using defective RuleVersion may require restatement/review.

---

# 105. ADR-REG-0020 Modes Apply

Impact analysis SHALL choose explicitly between:

```text
HISTORICAL_EXACT_REPLAY

HISTORICAL_SEMANTIC_REPLAY

CURRENT_KNOWLEDGE_RESTATEMENT

CURRENT_REASSESSMENT

FUTURE_SIMULATION.
```

---

# 106. New Law Does Not Rewrite Old Decisions

Hard invariant.

---

# 107. Knowledge Correction May Create Restatement

Original decision remains.

New restated decision explains difference.

---

# 108. Open Transaction Reassessment

For currently active:

```text
RFQ

order

shipment

customs entry

supplier approval
```

a material change MAY trigger current reassessment.

---

# 109. Closed Transaction

A closed historical transaction may require:

```text
audit restatement

post-event remediation

no action
```

depending on change type and obligations.

---

# 110. Future Transaction

Future orders/plans may require:

```text
prospective reassessment
```

against future-effective rules.

---

# 111. Reassessment Priority

Should consider:

```text
legal effective time

potential prohibition

E3/E4 effect

transaction imminence

transaction value

affected population size

regulatory domain

known enforcement deadline.
```

---

# 112. Priority Is Operational

It SHALL not imply:

```text
more legally valid.
```

---

# 113. ImpactMateriality

Avoid one numeric score.

Use structured dimensions.

---

# 114. Candidate Dimensions

```text
CURRENT_TRANSACTION_BLOCKING

FUTURE_REQUIREMENT

HISTORICAL_ONLY

FINANCIAL_CALCULATION

DOCUMENT_CHANGE

PROHIBITION_RISK

LICENCE_RISK

CLASSIFICATION_RISK

INFORMATIONAL_ONLY.
```

---

# 115. Confirmed Change Outcome

After reassessment, classify:

```text
NO_DECISION_CHANGE

DECISION_OUTCOME_CHANGED

REQUIREMENTS_CHANGED

EFFECT_CLASS_CHANGED

REMEDIATION_CHANGED

COVERAGE_CHANGED

REVIEW_REQUIRED.
```

---

# 116. DecisionDiff Integration

ADR-REG-0020's `DecisionDiff` SHALL explain:

```text
what changed

why outcome changed.
```

---

# 117. Example

```text
Previous:
SATISFIED

Current:
UNSATISFIED

Change:
threshold reduced from 100kg to 50kg

Transaction:
75kg

New requirement:
Permit P.
```

---

# 118. No Change Example

```text
new rule affects HS 0902

transaction HS 0901.
```

Outcome:

```text
NOT_IMPACTED.
```

---

# 119. Rule Recompilation

Verified change may produce:

```text
new RuleVersion
```

and therefore:

```text
new BRIR

new compiled policy

new RegulatoryExecutionPackage.
```

---

# 120. Knowledge Change and Runtime Rollout Are Separate

```text
RuleVersion published
```

does not mean:

```text
every OPA runtime has activated it.
```

ADR-REG-0019 reconciliation applies.

---

# 121. ChangeReadiness

A regulatory change SHALL have a deployment/readiness view.

Potential:

```text
KNOWLEDGE_VERIFIED

RULES_PUBLISHED

COMPILED

DISTRIBUTING

RUNTIMES_READY

REASSESSING

OPERATIONALLY_CURRENT.
```

---

# 122. Effective-Date Deadline

For a future-effective change:

```text
runtime readiness deadline
```

SHOULD precede:

```text
legal effective time.
```

---

# 123. Example

```text
published:
1 December

effective:
1 January

bundle:
deployed 20 December.
```

Good.

---

# 124. Bad

```text
law effective:
00:00 1 January

Baobab starts compilation:
00:01 1 January.
```

---

# 125. Pre-Staging

Future-effective RuleVersions SHOULD be compiled and staged where appropriate.

---

# 126. OPA Runtime Verification

OPA status exposes active bundle revisions and activation timestamps, which Baobab can use to verify whether runtime execution has caught up with a regulatory package.

---

# 127. Decision Logs Identify Old-Rule Exposure

OPA decision logs can include the bundle revision used for each evaluation.

Therefore Baobab can identify:

```text
decisions made on outdated package revision
```

during rollout incidents.

---

# 128. Example Runtime Lag

```text
RuleSet 42 effective
        │
        ├── runtime A → revision 42
        └── runtime B → revision 41
```

Impact analysis SHALL detect:

```text
decisions issued by runtime B
during lag window.
```

---

# 129. Runtime Lag Is Not Legal Change

It is:

```text
EXECUTION_DRIFT.
```

But may create business impact requiring reassessment.

---

# 130. Change Impact Sources

Impact may originate from:

```text
law

Baobab knowledge

source trust

content rights

runtime deployment

evidence

context.
```

---

# 131. Source Trust Change

Suppose Source S is later discovered to be:

```text
unofficial mirror

corrupted

incomplete.
```

Rules depending solely on S may require revalidation.

---

# 132. Rights Change

If licensing rights change:

```text
legal semantics may remain valid.
```

But:

```text
customer output

RAG indexing

raw display

AI processing
```

may change.

---

# 133. Rights Change Is Not Law Change

Yet it has operational impact.

---

# 134. Evidence Change

A permit expires or is revoked.

This is:

```text
transaction evidence-state change
```

not:

```text
regulatory law change.
```

But reassessment may produce different result.

---

# 135. Distinguish Change Domains

Canonical:

```text
LEGAL_CHANGE

KNOWLEDGE_CHANGE

SOURCE_CHANGE

RIGHTS_CHANGE

EVIDENCE_CHANGE

CONTEXT_CHANGE

RUNTIME_CHANGE.
```

---

# 136. Unified Impact Engine

All may reuse graph/decision-impact infrastructure.

---

# 137. But Provenance Must Preserve Cause

User should know:

```text
"Decision changed because law changed"
```

versus:

```text
"Decision changed because your permit expired."
```

---

# 138. Change Set

Related changes SHOULD be groupable into:

# `RegulatoryChangeSet`

---

# 139. RegulatoryChangeSet

Conceptually:

```text
RegulatoryChangeSet
├── changeset_id
├── source_event_ref?
├── change_refs[]
├── jurisdiction_scope[]
├── release/effective context
├── verification_status
├── aggregate_impact_ref?
└── provenance
```

---

# 140. Example

One Act may:

```text
substitute Section 5

repeal Section 7

insert Section 8A

change Schedule 2.
```

These should remain individually traceable but grouped.

---

# 141. One Publication May Contain Many Independent Changes

Hard invariant.

---

# 142. One Legal Change May Require Multiple Source Artefacts

Example:

```text
principal Act

commencement notice

official correction.
```

---

# 143. Change Fingerprint

Verified changes SHOULD have deterministic fingerprints based upon stable semantic identifiers.

---

# 144. Duplicate Detection

If provider A and official feed B report the same legal change:

```text
one RegulatoryChange
```

with:

```text
multiple observations.
```

---

# 145. Multiple Reports Do Not Create Multiple Laws

---

# 146. ChangeObservation

Conceptually:

```text
ChangeObservation
├── observation_id
├── change_ref?
├── source_ref
├── provider_ref?
├── observed_at
├── reported_identifier
├── raw_signal_ref
└── provenance
```

---

# 147. Source Corroboration

Multiple observations MAY strengthen detection confidence.

They do not automatically establish legal effect.

---

# 148. Change Completeness

A verified amendment may still have unresolved:

```text
commencement

target

exception

scope.
```

---

# 149. ChangeVerificationState

Potential:

```text
FULLY_VERIFIED

VERIFIED_WITH_OPEN_ISSUES

INTERPRETATION_REQUIRED

EXTERNAL_AUTHORITY_REQUIRED

UNRESOLVED.
```

---

# 150. Effect Ceiling

A partially understood change SHALL limit downstream automation.

---

# 151. Preliminary Warning

Baobab may inform:

```text
"Regulatory change detected.
Impact under review."
```

without claiming:

```text
"Your shipment is now illegal."
```

---

# 152. Pulse Coordination

Pulse is particularly useful for detecting:

```text
announcements

draft changes

regulator speeches

industry developments

enforcement signals.
```

---

# 153. Pulse Output to Regulations

Pulse MAY emit:

```text
RegulatoryChangeLead
```

with:

```text
source candidate

event summary

potential jurisdiction

potential domain

discovery evidence.
```

---

# 154. Pulse Lead Is Discovery State

It SHALL NOT directly trigger:

```text
RuleVersion publication

transaction block.
```

---

# 155. Regulations Verification

```text
Pulse signal
    ↓
official-source discovery
    ↓
Source Registry
    ↓
acquisition
    ↓
legal-change verification
    ↓
RegulatoryChange.
```

---

# 156. Regulations Output to Pulse

After verification:

```text
VerifiedRegulatoryChange
```

can feed Pulse.

---

# 157. Pulse Then Evaluates

```text
revenue impact

supplier impact

market opportunity

cost exposure

competitive effect.
```

---

# 158. Normative versus Probabilistic Impact

Regulations:

```text
"What obligations changed?"
```

Pulse:

```text
"What does that mean commercially?"
```

---

# 159. CMS Coordination

A verified change MAY trigger:

```text
CMS content staleness analysis.
```

---

# 160. CMS Projection Impact

Graph:

```text
RuleVersion
  ↓
RegulatoryContentProjection
  ↓
CMS Article.
```

---

# 161. Stale CMS Content

If underlying rule changes:

```text
article_status = REGULATORY_REVIEW_REQUIRED
```

may be appropriate.

---

# 162. Do Not Edit CMS Automatically Without Governance

A regulatory change may draft:

```text
content update candidate.
```

CMS owns editorial publication.

---

# 163. CMS Does Not Determine Regulatory Change

Hard invariant.

---

# 164. Trade Coordination

Trade SHOULD subscribe to verified decision-impact events relevant to:

```text
active orders

shipments

RFQs

supplier transactions.
```

---

# 165. Trade SHALL Not Reimplement Impact Graph

Regulations supplies:

```text
reassessment request

new decision

requirement change.
```

Trade manages workflow/state response.

---

# 166. Example

```text
new import permit rule
        ↓
Regulations reassesses Shipment S
        ↓
UNSATISFIED / E3
        ↓
Trade places regulatory hold.
```

---

# 167. ERP Coordination

ERP MAY be affected by:

```text
tax rates

filing obligations

reporting requirements

accounting classifications.
```

---

# 168. Ledger Coordination

Future Ledger may consume:

```text
tax/rate regulatory changes
```

through canonical decision contracts rather than scraping regulations itself.

---

# 169. Control Plane Coordination

Control Plane remains authority for:

```text
tenant

legal entity

market participation

trade lane

provider bindings

engine readiness.
```

---

# 170. Change Impact Shall Use Current CP Context Where Current Reassessment Is Intended

Historical restatement uses historical snapshots.

---

# 171. No Cross-Tenant Leakage

Impact graph traversal SHALL enforce tenant isolation.

---

# 172. Shared Public Rule

A public RuleVersion may affect:

```text
many tenants.
```

Candidate impact calculation MAY traverse shared context indices.

---

# 173. Tenant Private Overlay

Only relevant tenant may be traversed.

---

# 174. Impact Index

For scale, Baobab MAY maintain derived indexes of:

```text
Rule → Decision

Rule → Profile

Profile → Tenant

Classification → Transaction

Jurisdiction → Open Transaction.
```

---

# 175. Impact Index Is Derived

Canonical truth remains domain relationships.

---

# 176. PostgreSQL First

Initial implementation SHOULD use PostgreSQL for:

```text
typed relations

recursive graph traversal

temporal filters

impact queues.
```

---

# 177. Graph Database Not Required Initially

Consistent with ADR-REG-0010.

---

# 178. Qdrant Is Not Impact Engine

Vector similarity SHALL NOT determine blast radius.

---

# 179. Haystack Is Not Impact Authority

Haystack may help:

```text
discover semantic relationship candidates.
```

Canonical impact uses verified typed relationships.

---

# 180. LangGraph Role

LangGraph MAY orchestrate complex review such as:

```text
change candidate
  ↓
legal review
  ↓
impact review
  ↓
reassessment approval
  ↓
publication.
```

---

# 181. LangGraph Does Not Own Change State

Canonical:

```text
RegulatoryChange

ImpactAnalysis

ReassessmentCampaign
```

live in Regulations PostgreSQL state.

---

# 182. Reassessment Campaign

Large change MAY generate:

# `ReassessmentCampaign`

---

# 183. ReassessmentCampaign

Conceptually:

```text
ReassessmentCampaign
├── campaign_id
├── change_refs[]
├── selection_criteria
├── candidate_count
├── confirmed_scope
├── priority
├── mode
├── status
├── progress
├── started_at
├── completed_at?
└── provenance
```

---

# 184. Campaign Modes

Potential:

```text
DRY_RUN

SHADOW

ADVISORY

ACTIVE.
```

---

# 185. Dry Run

Computes:

```text
candidate impact

expected decision differences
```

without issuing new production decisions.

---

# 186. Shadow

Creates comparison decisions but does not supersede operative decisions.

---

# 187. Active

May produce new canonical decisions according to governance.

---

# 188. Campaign Selection

Example:

```text
all open ZA-import shipments
with HS prefix 0901
with customs-entry date >= 1 Jan 2027.
```

---

# 189. Idempotency

Each:

```text
change × target × reassessment mode
```

SHOULD be idempotent.

---

# 190. Avoid Duplicate Reassessments

Multiple source observations of same legal change SHALL not cause repeated identical campaigns.

---

# 191. Reassessment Coalescing

If three related amendments affect one transaction before reassessment executes:

```text
one coherent latest RuleSet reassessment
```

may be preferable to three redundant evaluations.

---

# 192. Preserve Causality

Even if coalesced:

```text
all triggering change IDs
```

must be recorded.

---

# 193. Reassessment Against RuleSet

Reassessment SHALL use a pinned:

```text
new ApplicableRuleSetSnapshot.
```

---

# 194. Previous and New Decisions

Use ADR-REG-0020:

```text
DecisionDiff.
```

---

# 195. ConfirmedImpact

Conceptually:

```text
ConfirmedRegulatoryImpact
├── change_ref
├── subject_ref
├── previous_decision_ref?
├── new_decision_ref?
├── decision_diff_ref?
├── impact_outcome
├── remediation[]
├── confirmed_at
└── provenance
```

---

# 196. Confirmed Impact Outcomes

```text
NO_MATERIAL_CHANGE

NEW_OBLIGATION

REMOVED_OBLIGATION

NEW_PROHIBITION

PROHIBITION_REMOVED

REQUIREMENT_TIGHTENED

REQUIREMENT_RELAXED

CALCULATION_CHANGED

CLASSIFICATION_CHANGED

DECISION_BECAME_UNSATISFIED

DECISION_BECAME_SATISFIED

DECISION_BECAME_INDETERMINATE

REVIEW_REQUIRED.
```

---

# 197. Removed Requirement Matters Too

Change intelligence SHALL detect both:

```text
new burdens
```

and:

```text
removed burdens.
```

---

# 198. Commercial Opportunity

A removed restriction may be highly valuable.

Regulations publishes normative change.

Pulse identifies opportunity.

---

# 199. Reassessment Safety

Change-triggered reassessment SHALL not automatically produce irreversible operational mutations without respecting:

```text
DecisionEffectClass

PDP/PEP boundary

current object version

enforcement governance.
```

---

# 200. Stale Transaction State

If target changed since candidate selection:

```text
refresh current context
```

before active reassessment.

---

# 201. Historical Campaign

Historical restatement SHALL use immutable historical ContextSnapshots rather than current transaction state.

---

# 202. Change Notification

Not every verified change needs transaction-level reassessment.

---

# 203. Notification Classes

Potential:

```text
SOURCE_UPDATE

REGULATORY_CHANGE_VERIFIED

FUTURE_CHANGE

IMPACT_CANDIDATE

IMPACT_CONFIRMED

REASSESSMENT_REQUIRED

DECISION_CHANGED

URGENT_ACTION_REQUIRED.
```

---

# 204. Events Are Covered More Fully in ADR-REG-0024

This ADR defines semantic triggers.

`0024` SHALL define subscriptions/delivery contracts.

---

# 205. Change Urgency

Possible:

```text
ROUTINE

TIME_BOUND

URGENT

IMMEDIATE.
```

---

# 206. Urgency Must Be Evidence-Based

Not:

```text
LLM says urgent.
```

---

# 207. Immediate Example

Official prohibition:

```text
effective immediately.
```

---

# 208. Routine Example

Editorial correction with no normative effect.

---

# 209. Change Coverage

Impact analysis SHALL know whether Baobab's legal coverage is sufficient.

---

# 210. New Unknown Area

A change may reveal:

```text
new regulatory domain
```

Baobab does not yet model.

Result:

```text
COVERAGE_GAP_CREATED.
```

---

# 211. Example

A new regulation introduces:

```text
special environmental certificate
```

outside existing profile.

Baobab SHALL not silently ignore it.

---

# 212. Jurisdiction Pack Readiness

Change may cause:

```text
UG_COFFEE_PACK = DEGRADED
```

until new semantics are verified.

---

# 213. Coverage Degradation

May reduce:

```text
E3/E4 decision ceiling.
```

---

# 214. Hard-Prohibition Emergency

If authoritative verified change introduces a clear prohibition but full implementation not yet deployed:

```text
E2 review gate
```

may be safer than continuing under known-obsolete rules.

---

# 215. Never Pretend Old RuleSet Is Current

---

# 216. Change Detection Failure

Source monitor unavailable.

Result:

```text
SOURCE_MONITORING_DEGRADED.
```

---

# 217. Freshness Policy May React

Depending on source importance:

```text
jurisdiction pack readiness
```

may degrade.

---

# 218. Source Freshness SLO

Each high-value source SHOULD have:

```text
expected update mechanism

expected polling interval

maximum monitoring gap

escalation policy.
```

---

# 219. Not All Sources Need Same Cadence

Tariff/sanctions feeds may warrant:

```text
high frequency.
```

Slow-moving statute archives:

```text
lower frequency.
```

---

# 220. Detection Latency Metrics

Track:

```text
publication → observed

observed → acquired

acquired → candidate change

candidate → verified

verified → RuleVersion published

RuleVersion → runtime ready

runtime ready → impacted objects reassessed.
```

---

# 221. These Latencies Are Different

One average:

```text
change latency
```

would hide operational bottlenecks.

---

# 222. Example

```text
detected in 5 minutes

review took 3 days.
```

Problem is governance throughput, not source monitoring.

---

# 223. Another

```text
verified in 1 hour

bundle activation took 8 hours.
```

Problem is distribution.

---

# 224. Change Detection Quality Metrics

Potential:

```text
missed-change rate

duplicate-signal rate

false-change rate

amendment-target accuracy

effective-date accuracy

exception-change recall

time-to-detection.
```

---

# 225. Impact Analysis Metrics

Potential:

```text
candidate blast-radius size

confirmed-impact ratio

reassessment count

decision-change rate

false-positive impact rate

reassessment latency.
```

---

# 226. Why False Positives Matter

If every minor change causes:

```text
millions of reassessments
```

the architecture becomes commercially expensive.

---

# 227. Why False Negatives Matter More

Missing one material prohibition can be serious.

---

# 228. Evaluation Must Weight Error Types

No generic precision metric alone.

---

# 229. Golden Change Corpus

Baobab SHALL maintain test cases for:

```text
amendment

repeal

correction

commencement

expiry

renumbering

table rate change

exception insertion

retroactive change

future-effective change.
```

---

# 230. Impact Golden Cases

Examples:

```text
change affects no decisions

change affects one classification

change affects all imports

change affects future only

change requires historical restatement.
```

---

# 231. Structural Diff Test

Renumbering should not produce false semantic repeal.

---

# 232. Consolidation Test

New consolidated document without new amendment should not create false legal change.

---

# 233. Knowledge Correction Test

Parser correction must trigger decision restatement without asserting law changed.

---

# 234. Runtime Drift Test

Old OPA bundle decision must be discoverable via bundle revision telemetry. OPA status and decision logs provide the relevant runtime revision information.

---

# 235. Draft Regulation

Draft/proposed regulation MAY enter:

```text
FUTURE_SCENARIO_CHANGE
```

but SHALL NOT affect binding production RuleSets.

---

# 236. Pulse Can Use Drafts

Pulse may analyse:

```text
future risk/opportunity.
```

---

# 237. Regulations May Simulate

ADR-REG-0020:

```text
FUTURE_SIMULATION.
```

---

# 238. Draft Becomes Enacted

Do not mutate draft candidate into law silently.

Establish:

```text
draft
  ↓ resulting/related enacted act
```

with provenance.

---

# 239. Change Relationship Model

Potential typed edges:

```text
AMENDS

REPEALS

CORRECTS

COMMENCES

SUSPENDS

EXTENDS

SUPERSEDES

REPLACES

RENUMBERS

CONSOLIDATES

INTERPRETS

INVALIDATES

REVISES.
```

---

# 240. W3C PROV Compatibility

Where useful:

```text
new entity
    prov:wasRevisionOf
old entity.
```

Invalidation and derivation relationships MAY also be exported through PROV-compatible projections.

---

# 241. Canonical Baobab Semantics Remain Richer

PROV does not itself tell us:

```text
legal repeal

statutory commencement

normative exception.
```

Baobab retains domain-specific relationships.

---

# 242. Change Source Authority

A commercial provider may report an amendment before Baobab obtains official evidence.

State:

```text
CHANGE_CANDIDATE
```

until authority requirements are met.

---

# 243. Provider Correction

Provider says:

```text
previous record erroneous.
```

Baobab SHALL determine whether:

```text
law changed
```

or merely:

```text
provider data changed.
```

---

# 244. Competing Sources

If two official channels conflict:

```text
SOURCE_CONFLICT.
```

Change publication may require review.

---

# 245. Ambiguous Effective Date

State:

```text
TEMPORAL_INTERPRETATION_REQUIRED.
```

---

# 246. Ambiguous Amendment Target

State:

```text
AMENDMENT_TARGET_UNRESOLVED.
```

---

# 247. No Guessing

Impact engine SHALL not guess a target because:

```text
Section 7 looks similar.
```

---

# 248. Renumbered Target Resolution

Use verified mappings where available.

---

# 249. Deleted Provision

Deletion can mean:

```text
repealed

moved

consolidated

renumbered

publisher omission.
```

Do not infer automatically.

---

# 250. Change Governance Incident

If Baobab misses a material regulatory change:

# `RegulatoryChangeIncident`

---

# 251. Incident

Conceptually:

```text
RegulatoryChangeIncident
├── incident_id
├── source_ref
├── missed_change_ref
├── detection_gap
├── affected_period
├── impacted_rules[]
├── candidate_decisions[]
├── severity
├── remediation_status
└── provenance
```

---

# 252. Incident Response

Potential:

```text
freeze affected E4 automation

verify legal change

patch knowledge

publish corrected RuleVersion

identify impact population

reassess

notify affected consumers

perform root-cause analysis.
```

---

# 253. Root Cause

Potential:

```text
source monitor failed

provider schema drift

parser missed amendment

AI missed exception

human review defect

wrong effective date

bundle rollout failure.
```

---

# 254. Change Detection Is Safety-Critical

For mature E3/E4 regulatory automation, monitoring freshness is part of decision assurance.

---

# 255. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-CHG-I01` | Source signal SHALL remain distinct from verified legal change |
| `REG-CHG-I02` | Byte-level change SHALL not automatically imply normative change |
| `REG-CHG-I03` | Normative change MAY exist without base-document byte change |
| `REG-CHG-I04` | New consolidated text SHALL not automatically create new legal authority |
| `REG-CHG-I05` | Legal change SHALL remain distinct from Baobab knowledge correction |
| `REG-CHG-I06` | Parser correction SHALL not be represented as statutory amendment |
| `REG-CHG-I07` | Legal publication time SHALL remain distinct from effective time |
| `REG-CHG-I08` | Observed time SHALL remain distinct from legal time |
| `REG-CHG-I09` | Future-effective change SHALL be first-class |
| `REG-CHG-I10` | Retroactive change SHALL be first-class |
| `REG-CHG-I11` | Structural diff SHALL remain distinct from semantic diff |
| `REG-CHG-I12` | Renumbering SHALL not automatically appear as repeal plus insertion |
| `REG-CHG-I13` | Verified legal change SHALL require governed authority/source analysis |
| `REG-CHG-I14` | AI-detected change SHALL remain candidate state until verification |
| `REG-CHG-I15` | Graph reachability SHALL indicate candidate impact, not confirmed business impact |
| `REG-CHG-I16` | Temporal filtering SHALL precede confirmed impact |
| `REG-CHG-I17` | Context/applicability filtering SHALL precede confirmed transaction impact |
| `REG-CHG-I18` | Targeted reassessment SHALL establish confirmed decision impact |
| `REG-CHG-I19` | New law SHALL not rewrite historically correct earlier decisions |
| `REG-CHG-I20` | Late-discovered historical law MAY require historical restatement |
| `REG-CHG-I21` | Baobab knowledge defects MAY require historical restatement |
| `REG-CHG-I22` | DecisionDiff SHALL explain confirmed decision changes |
| `REG-CHG-I23` | Runtime rollout SHALL remain distinct from legal publication |
| `REG-CHG-I24` | Runtime bundle revision SHALL be auditable for impacted decisions |
| `REG-CHG-I25` | Pulse SHALL detect leads but SHALL NOT publish legal change |
| `REG-CHG-I26` | CMS SHALL receive regulatory projections but SHALL NOT establish legal change |
| `REG-CHG-I27` | Qdrant similarity SHALL not determine blast radius |
| `REG-CHG-I28` | Haystack relationships SHALL remain candidates until canonically verified |
| `REG-CHG-I29` | PostgreSQL SHALL remain authoritative for change and impact state |
| `REG-CHG-I30` | Reassessment SHALL preserve PDP/PEP separation |
| `REG-CHG-I31` | Change campaigns SHALL be idempotent |
| `REG-CHG-I32` | Duplicate source observations SHALL not duplicate canonical legal change |
| `REG-CHG-I33` | Impact causality SHALL be preserved through coalesced campaigns |
| `REG-CHG-I34` | Coverage gaps introduced by new regulation SHALL be explicit |
| `REG-CHG-I35` | Monitoring failure SHALL never be interpreted as absence of regulatory change |

---

# 256. Rejected Alternative — Poll Website and Diff HTML

Rejected as complete architecture.

Useful only as one detection mechanism.

---

# 257. Rejected Alternative — Hash Changed Means Law Changed

Rejected.

---

# 258. Rejected Alternative — Hash Unchanged Means Law Unchanged

Rejected.

---

# 259. Rejected Alternative — LLM Compares Two PDFs and Publishes Amendment

Rejected.

---

# 260. Rejected Alternative — New Consolidated Text Is New Law

Rejected.

---

# 261. Rejected Alternative — Treat Every New Gazette Item as Applicable

Rejected.

---

# 262. Rejected Alternative — Reassess Every Decision on Every Change

Rejected.

---

# 263. Rejected Alternative — Vector Similarity Determines Affected Transactions

Rejected.

---

# 264. Rejected Alternative — Graph Reachability Means Confirmed Impact

Rejected.

---

# 265. Rejected Alternative — One Change Severity Score

Rejected.

---

# 266. Rejected Alternative — Late Discovery Rewrites Historical Decision

Rejected.

Use historical restatement.

---

# 267. Rejected Alternative — Rule Publication Means Runtime Current

Rejected.

---

# 268. Rejected Alternative — OPA Is Healthy, Therefore New Law Deployed

Rejected.

OPA's current Status API exposes actual active bundle revision and activation status; Baobab must compare that to desired regulatory state.

---

# 269. Rejected Alternative — Pulse Decides Legal Change

Rejected.

---

# 270. Rejected Alternative — CMS Article Is Change Source of Truth

Rejected.

---

# 271. Rejected Alternative — Provider Says Changed, Therefore Law Changed

Rejected.

---

# 272. Rejected Alternative — No Event Means No Change

Rejected.

Monitoring coverage matters.

---

# 273. Rejected Alternative — Manual Review of Entire Corpus After Every Update

Rejected.

Targeted dependency traversal is required for scale.

---

# 274. Minimum Implementation Proof

Before `ADR-REG-0023` is considered implemented, Baobab SHOULD demonstrate:

```text
1. SourceChangeSignal model.

2. official-feed adapter.

3. polling adapter.

4. ETag processing.

5. Last-Modified processing.

6. content hashing.

7. SourceMonitorCheckpoint.

8. missed-monitoring-gap state.

9. ELI-style feed ingestion seam.

10. immutable new SourceArtefact on update.

11. same-URL multiple artefact versions.

12. ChangeObservation.

13. duplicate observation deduplication.

14. RegulatoryChange aggregate.

15. RegulatoryChangeSet.

16. external-law-change origin.

17. Baobab-knowledge-correction origin.

18. provider-correction origin.

19. ENACTMENT type.

20. AMENDMENT type.

21. INSERTION type.

22. SUBSTITUTION type.

23. REPEAL type.

24. CORRECTION type.

25. COMMENCEMENT type.

26. SUSPENSION type.

27. EXPIRY type.

28. EXTENSION type.

29. RENUMBERING type.

30. SCOPE_CHANGE type.

31. RATE_CHANGE type.

32. THRESHOLD_CHANGE type.

33. CLASSIFICATION_CHANGE type.

34. GUIDANCE_CHANGE type.

35. JUDICIAL_INTERPRETATION type.

36. LegalStructuralDiff.

37. LegalSemanticDiff.

38. section insertion detection.

39. section removal detection.

40. table change detection.

41. renumbering detection.

42. cross-reference change detection.

43. exception change detection.

44. effective-date change detection.

45. structural change with no normative change.

46. normative change without base-document text change.

47. consolidated-text-only update.

48. parser correction.

49. OCR correction.

50. publisher legal corrigendum.

51. publication time.

52. legal effective time.

53. observed time.

54. knowledge time.

55. retroactive effective date.

56. future effective date.

57. AI change candidate.

58. human/governed change verification.

59. ambiguous target review.

60. ambiguous effective-date review.

61. competing-source review.

62. RegulatoryChangeImpact.

63. typed impact path.

64. direct dependency.

65. transitive dependency.

66. constitutive-rule dependency.

67. definition blast radius.

68. cross-reference blast radius.

69. hierarchy/precedence blast radius.

70. regime-membership impact.

71. source-trust impact.

72. rights-change impact.

73. runtime-change impact.

74. evidence-change distinction.

75. CandidateImpactSet.

76. PostgreSQL recursive impact traversal.

77. temporal filtering.

78. jurisdiction filtering.

79. activity filtering.

80. classification filtering.

81. legal-entity filtering.

82. trade-lane filtering.

83. tenant-isolation filtering.

84. public shared-rule multi-tenant candidate impact.

85. tenant-private overlay isolated impact.

86. ReassessmentCandidate.

87. open-transaction candidate.

88. historical-decision candidate.

89. future-transaction candidate.

90. historical exact replay selection.

91. historical restatement selection.

92. current reassessment selection.

93. future simulation selection.

94. ReassessmentCampaign.

95. DRY_RUN campaign.

96. SHADOW campaign.

97. ACTIVE campaign.

98. campaign idempotency.

99. duplicate signal campaign dedupe.

100. multi-change campaign coalescing.

101. causal change IDs retained.

102. DecisionDiff integration.

103. ConfirmedRegulatoryImpact.

104. NO_MATERIAL_CHANGE.

105. NEW_OBLIGATION.

106. REMOVED_OBLIGATION.

107. NEW_PROHIBITION.

108. PROHIBITION_REMOVED.

109. REQUIREMENT_TIGHTENED.

110. REQUIREMENT_RELAXED.

111. DECISION_BECAME_UNSATISFIED.

112. DECISION_BECAME_SATISFIED.

113. DECISION_BECAME_INDETERMINATE.

114. RuleVersion generation from verified change.

115. BRIR generation.

116. compilation.

117. RegulatoryExecutionPackage revision.

118. future-effective package pre-staging.

119. OPA active-revision verification.

120. decision-log bundle-revision correlation.

121. stale runtime identification.

122. decisions affected by stale runtime discovery.

123. monitoring-latency metrics.

124. verification-latency metrics.

125. runtime-rollout latency.

126. reassessment latency.

127. change detection precision metric.

128. missed-change metric.

129. false-impact metric.

130. decision-change metric.

131. legal amendment golden fixture.

132. renumbering golden fixture.

133. consolidation golden fixture.

134. retroactive-change golden fixture.

135. future-effective-change fixture.

136. knowledge-correction fixture.

137. bundle-drift fixture.

138. Pulse RegulatoryChangeLead seam.

139. verified change event back to Pulse.

140. CMS stale-content projection.

141. Trade active-transaction reassessment.

142. ERP obligation/rate-change seam.

143. Control Plane context use.

144. jurisdiction-pack degraded state.

145. new coverage-gap detection.

146. effect-ceiling reduction on coverage gap.

147. RegulatoryChangeIncident.

148. missed change incident.

149. root-cause recording.

150. end-to-end source update → verified change → new RuleVersion → impact graph → targeted reassessment → DecisionDiff → operational event.
```

---

# 275. Initial Uganda → South Africa Change Proof

The first meaningful end-to-end change test SHOULD include synthetic or verified test fixtures for:

```text
Uganda export requirement change

South Africa import requirement change

SPS certificate change

HS/tariff rate update

rule-of-origin change

permit requirement change

future-effective amendment

retroactive correction.
```

---

# 276. Example — Tariff Rate Change

Old verified rule:

```text
HS X
import duty = 10%.
```

New official schedule:

```text
HS X
import duty = 15%
effective 1 January.
```

Pipeline:

```text
source feed
   ↓
new artefact
   ↓
table structural diff
   ↓
rate-change candidate
   ↓
human/deterministic verification
   ↓
RegulatoryChange:
RATE_CHANGE
   ↓
RuleVersion R2
   ↓
impact graph:
HS X
   ↓
future shipments
   ↓
reassessment.
```

---

# 277. Historical Result

Shipments imported:

```text
before 1 January
```

remain under previous rate.

---

# 278. Future Result

Planned imports:

```text
on/after 1 January
```

use new rate.

---

# 279. Pulse Result

Pulse MAY calculate:

```text
margin impact

price impact

alternative sourcing opportunity.
```

---

# 280. Example — New Permit Requirement

New regulation:

```text
Product class X requires Permit P
from 1 November.
```

Impact traversal:

```text
Provision
  ↓
RuleVersion
  ↓
Classification X
  ↓
ZA imports
  ↓
open transactions
  ↓
planned import dates >= 1 Nov.
```

---

# 281. Transaction A

Import:

```text
20 October.
```

No impact.

---

# 282. Transaction B

Import:

```text
5 November.
```

Reassessment:

```text
permit absent
   ↓
UNSATISFIED.
```

---

# 283. Example — Missed Exception

Original Baobab RuleVersion:

```text
all Product X imports prohibited.
```

Later quality audit discovers source actually says:

```text
prohibited,
except Permit P holders.
```

This is not a new law.

It is:

```text
BAOBAB_INTERPRETATION_CORRECTION.
```

---

# 284. Impact

Find:

```text
all decisions using defective RuleVersion.
```

---

# 285. Historical Restatement

For transactions where Permit P was valid:

```text
original:
PROHIBITED

restated:
potentially SATISFIED
```

depending on other rules.

---

# 286. Preserve Original Decision

Audit shows:

```text
what Baobab decided then
```

and:

```text
what Baobab now knows.
```

---

# 287. Example — Consolidated Text Update

Official site publishes new consolidated PDF.

Hash changes.

Structural text differs.

But Baobab already processed the underlying amending acts.

Correct:

```text
DERIVED_REPRESENTATION_UPDATE

no duplicate legal amendment.
```

---

# 288. Example — Commencement Notice

Base Act published months ago.

No base Act bytes change.

New notice says:

```text
Sections 5–8 commence 1 December.
```

Pipeline creates:

```text
COMMENCEMENT RegulatoryChange.
```

Affected RuleVersions become effective accordingly.

---

# 289. Example — Renumbering

Old:

```text
Section 14
```

New consolidation:

```text
Section 15
```

No semantic change.

Canonical rule lineage remains stable.

Citation representation updates.

---

# 290. Example — Future Trade-Regime Change

Country joins qualifying regime from Date T.

No individual product rule wording changes.

But:

```text
regime membership
```

changes.

Impact:

```text
rules of origin

tariff preference applicability

documentation
```

may change.

---

# 291. Example — Runtime Drift

Regulations publishes:

```text
REP-22
```

effective at midnight.

Runtime A loads it.

Runtime B remains:

```text
REP-21.
```

OPA status shows different active revision and decision logs identify decisions evaluated using the old bundle.

Baobab identifies:

```text
all B decisions in exposure window
```

and reassesses them.

---

# 292. Change Detection Architecture

```text
                   SOURCE ECOSYSTEM
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Official API    Feed/Poll       Pulse Lead
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 SourceChangeSignal
                         │
                         ▼
                    Acquisition
                         │
                         ▼
               Immutable Artefact
                         │
                         ▼
              Structural Comparison
                         │
                         ▼
                 Change Candidate
                         │
                         ▼
               Semantic Analysis
                         │
                         ▼
              Governance / Verification
                         │
                         ▼
                RegulatoryChange
                         │
                         ▼
              Canonical Rule Update
                         │
                         ▼
                  Knowledge Graph
                         │
                         ▼
               Candidate Blast Radius
                         │
                    ┌────┴────┐
                    ▼         ▼
                 Filter    Coverage
                    │         │
                    └────┬────┘
                         ▼
                ReassessmentCampaign
                         │
                         ▼
                   DecisionDiff
                         │
                         ▼
                 Confirmed Impact
```

---

# 293. Business Impact Architecture

```text
RegulatoryChange
      │
      ▼
Affected RuleVersions
      │
      ▼
Affected Profiles
      │
      ▼
Affected Context Dimensions
      │
      ├── Jurisdiction
      ├── Activity
      ├── Product / HS
      ├── Regime
      ├── Legal Entity
      └── Legal Time
      │
      ▼
Candidate Transactions / Decisions
      │
      ▼
Targeted Reassessment
      │
      ▼
DecisionDiff
      │
      ├── No Change
      ├── New Requirement
      ├── Unsatisfied
      ├── Prohibited
      ├── Satisfied
      └── Indeterminate
```

---

# 294. Why This Matters Strategically

A traditional regulatory-content system often answers:

> **What changed in the law?**

Baobab's target is substantially richer:

> **What changed, what does that change legally mean, which canonical rules are affected, which customers and transactions could be affected, which are actually affected, what decisions have changed, and what action now follows?**

---

# 295. Regulatory Intelligence versus Regulatory Execution

Pulse may say:

```text
"An import-control change appears likely."
```

Regulations eventually establishes:

```text
"Verified Rule R changes on Date T."
```

Then Regulations can answer:

```text
"These 42 open transactions require reassessment."
```

And after reassessment:

```text
"11 now require Permit P.
31 remain unchanged."
```

---

# 296. This Is the Core Differentiator

The moat is not merely:

```text
more regulatory documents.
```

It is:

```text
Source
  ↓
Legal Change
  ↓
Rule
  ↓
Applicability
  ↓
Transaction
  ↓
Decision
  ↓
Business Consequence.
```

---

# 297. Research Foundation Summary

Akoma Ntoso provides a mature conceptual basis for tracking legislative lifecycle events and distinguishes original, consolidated/single-version and multiple-version legal expressions. It also models modification types and explicit source/target relationships for amendments, which supports Baobab's decision to represent change as typed legal relationships rather than generic text differences.

ELI's current ontology similarly represents explicit legal relationships such as amendment, repeal, correction, commencement and consolidation together with legal-validity metadata. Its current ELI-Impact extension goes further by formally modelling how legislative acts impact existing acts and consolidated versions.

ELI Pillar 4 also demonstrates a useful operational approach to legislative synchronisation: publishers can expose exhaustive identifiers and regular update feeds so downstream users can discover new or updated resources without repeatedly crawling an entire publication system. Baobab should consume such authoritative mechanisms wherever available.

EUR-Lex's distinction between consolidation and legal enactment demonstrates why a new consolidated representation cannot simply be treated as a new legal rule: consolidation may provide a convenient current-text view without itself producing independent legal effect.

W3C PROV provides generic revision, derivation and invalidation semantics that fit Baobab's immutable lineage model. Baobab uses these concepts for provenance interoperability while retaining richer legal-domain semantics such as amendment, repeal, commencement and suspension.

OPA provides the runtime observability needed after canonical regulatory change becomes executable policy: Status exposes active bundle revisions and activation failures, while Decision Logs record the bundle revision used for each decision. Those facilities allow Baobab to detect regulatory runtime drift and identify decisions produced during an obsolete-policy exposure window.

---

# 298. Final Decision

Baobab Regulations SHALL implement **Regulatory Change Detection and Impact Analysis as a governed, temporal and graph-driven domain capability**.

The canonical lifecycle is:

```text
                  OBSERVE
                     │
                     ▼
             SourceChangeSignal
                     │
                     ▼
                  ACQUIRE
                     │
                     ▼
            Immutable Artefact
                     │
                     ▼
                  COMPARE
                     │
                     ▼
              Change Candidate
                     │
                     ▼
                 INTERPRET
                     │
                     ▼
                  VERIFY
                     │
                     ▼
             RegulatoryChange
                     │
                     ▼
             UPDATE KNOWLEDGE
                     │
                     ▼
                RuleVersion
                     │
                     ▼
               IMPACT GRAPH
                     │
                     ▼
          CandidateImpactSet
                     │
                     ▼
         Temporal/Context Filter
                     │
                     ▼
          ReassessmentCampaign
                     │
                     ▼
               DecisionDiff
                     │
                     ▼
            Confirmed Impact
                     │
                     ▼
             BUSINESS ACTION
```

The signal principle is:

> **An update notification, feed item, changed hash or AI alert is evidence that something may have changed—not evidence that the law changed.**

The legal-change principle is:

> **A legal change becomes canonical only after Baobab establishes the authoritative source, change relationship, target, legal effect and applicable time.**

The semantic principle is:

> **Regulatory change SHALL be expressed in legal semantics such as amendment, repeal, correction, commencement, suspension, scope change or rate change—not merely as text inserted or deleted.**

The temporal principle is:

> **Publication date, effective date, observation date and Baobab knowledge time are independent dimensions and SHALL remain separately queryable.**

The provenance principle is:

> **Every revision SHALL preserve lineage to what preceded it and why it changed.**

The graph principle is:

> **Regulatory impact begins with typed dependency traversal from source to provision to interpretation to rule to applicability to decision.**

The impact principle is:

> **Graph reachability establishes candidate impact; only temporal/context filtering and reassessment establish confirmed business impact.**

The historical principle is:

> **A later change in law does not rewrite an earlier correctly issued decision, while late discovery or correction of the historical legal state may create a current-knowledge restatement.**

The runtime principle is:

> **Publishing a new RuleVersion is not enough; Baobab must know whether every consequential evaluator has activated the correct execution package and which decisions were produced under older revisions.**

The Pulse principle is:

> **Pulse discovers and assesses signals; Regulations establishes normative change.**

The CMS principle is:

> **CMS publishes change explanations; it does not decide what legally changed.**

The efficiency principle is:

> **Baobab SHALL identify the smallest defensible affected population rather than blindly reassessing the platform.**

The safety principle is:

> **Monitoring gaps, unresolved amendments and incomplete coverage produce explicit uncertainty or reduced decision readiness—not silent continuation as though nothing changed.**

And the strategic principle is:

> **Baobab's regulatory advantage is not merely detecting that regulation changed. It is being able to trace that change all the way from authoritative source to the exact rules, products, markets, legal entities, transactions and prior decisions whose regulatory position has actually changed.**

That is the architecture established by `ADR-REG-0023`.

---

## Decision Summary

```text
ADR-REG-0023
────────────────────────────────────────────

CHANGE CHAIN

Signal
 ↓
Source Change
 ↓
Legal Change Candidate
 ↓
Verification
 ↓
RegulatoryChange
 ↓
Rule Change
 ↓
Impact Graph
 ↓
Targeted Reassessment
 ↓
Confirmed Impact


CRITICAL DISTINCTIONS

Source update
≠
Law change

Text diff
≠
Normative change

Consolidation
≠
New law

Knowledge correction
≠
Legal amendment

Graph reachability
≠
Confirmed impact


CHANGE TYPES

Amend
Repeal
Insert
Substitute
Correct
Commence
Suspend
Expire
Extend
Renumber
Change scope
Change rate
Change threshold
Change classification


TIME

Publication time

Legal effective time

Observed time

Knowledge time


DETECTION

Official APIs
Feeds
ELI Pillar 4
Webhooks
Polling
Pulse leads


AI

Detects candidates.

Does not verify law.


IMPACT GRAPH

Source
 ↓
Provision
 ↓
Interpretation
 ↓
Rule
 ↓
Profile
 ↓
Context
 ↓
Decision


FILTER

Legal time
Jurisdiction
Activity
Classification
Regime
Tenant
Legal entity


REASSESSMENT

Historical replay

Historical restatement

Current reassessment

Future simulation


OPA

Rule published
≠
runtime current.

Verify active
bundle revision.


PULSE

Detect signal
and commercial impact.

Not legal authority.


CMS

Publish explanation.

Not legal authority.


STRATEGIC RESULT

"What changed?"

becomes

"Who and what
actually changes because of it?"
```
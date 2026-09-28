# ADR-REG-0014 — Provenance, Citation and Evidentiary Chain

**Status:** Proposed — Foundational Trust Architecture  
**Decision ID:** `ADR-REG-0014`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Provenance / Citation / Evidence / Chain of Custody / Decision Traceability / Reproducibility  
**Strategic Classification:** Core Regulatory Assurance Infrastructure

---

## 1. Depends On

This ADR depends upon and SHALL be interpreted consistently with:

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics and Defeasible Reasoning Model`
- `ADR-REG-0010 — Regulatory Knowledge Graph, Relationship, Provenance and Traversal Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`
- `ADR-REG-0012 — Regulatory Content Acquisition, Licensing, Reuse, AI Processing and Derived-Data Rights`
- `ADR-REG-0013 — Source Ingestion, Normalisation and Adapter Architecture`

It also aligns with existing Baobab principles established in:

- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- `ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture`
- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`

---

# 2. Executive Decision

Baobab Regulations SHALL implement a **first-class, immutable and traversable regulatory evidentiary chain** connecting:

```text
REGULATORY AUTHORITY
        │
        ▼
REGULATORY SOURCE
        │
        ▼
SOURCE EDITION
        │
        ▼
SOURCE ARTEFACT
        │
        ▼
ACQUISITION
        │
        ▼
DOCUMENT REPRESENTATION
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
        ▼
REGULATORY CONTEXT
        │
        ▼
FACT / EVIDENCE
        │
        ▼
ASSESSMENT
        │
        ▼
DECISION
        │
        ▼
ENFORCEMENT / OPERATIONAL OUTCOME
```

Every consequential decision SHALL be capable of answering:

```text
What source established the law?

Which exact source version was used?

Which provision or fragment was relied upon?

How was that source acquired?

Was the artefact intact?

How was it transformed?

Who or what interpreted it?

Which rule version was produced?

Which facts were evaluated?

Which evidence established those facts?

Which exceptions or overrides were considered?

Which policy/evaluator version ran?

Who reviewed or approved it?

What decision was returned?

What operational action followed?
```

---

# 3. Fundamental Doctrine

Baobab SHALL distinguish:

```text
CITATION
≠
PROVENANCE
≠
LINEAGE
≠
CHAIN OF CUSTODY
≠
EVIDENCE
≠
EVIDENCE ASSESSMENT
≠
EVIDENTIARY SUFFICIENCY
≠
DECISION TRACE
≠
AUDIT LOG
≠
REPRODUCIBILITY
```

These concepts complement each other.

They SHALL NOT be collapsed into a generic:

```text
audit_metadata JSONB
```

field.

---

# 4. Citation

A **citation** answers:

> Where can the relevant legal or evidentiary material be located?

Examples:

```text
Act 12 of 2026, s 14(2)

Government Gazette No. 12345,
Notice 321 of 2026,
Schedule 2

Treaty Article 19(1)

Customs Tariff Schedule,
heading 0901
```

A citation supports human and machine navigation.

It does not by itself prove:

```text
authenticity
correct interpretation
applicability
satisfaction of a requirement.
```

---

# 5. Provenance

**Provenance** answers:

> Where did this information or object come from, and through what process was it produced?

W3C PROV models provenance around `Entity`, `Activity` and `Agent`, together with derivation, usage, generation and responsibility relationships.

Baobab SHALL remain semantically compatible with those concepts.

---

# 6. Lineage

**Lineage** answers:

> What depends on what?

Example:

```text
Rule R17
    ↓ derived from
Interpretation I9
    ↓ interprets
Provision P14
    ↓ extracted from
Artefact A8.
```

Forward:

```text
Artefact A8
   ↓
Provision P14
   ↓
Rule R17
   ↓
Assessment A55
   ↓
Decision D20.
```

---

# 7. Chain of Custody

**Chain of custody** answers:

> What happened to this evidentiary artefact from acquisition until its present state, and can its integrity/history be demonstrated?

NIST's digital-evidence preservation guidance emphasises recording the original source, how the file was obtained or transferred, and using hashes or signatures to support integrity.

Baobab SHALL borrow these integrity principles.

This ADR does **not** declare that Baobab regulatory records automatically satisfy every jurisdiction's evidentiary rules for court proceedings.

---

# 8. Evidence

**Evidence** is material relied upon to establish, corroborate, contradict or contextualise a claim or regulatory fact.

Examples:

```text
official permit

certificate

licence

regulator response

customs declaration

inspection record

product composition

registry record

signed authority determination

shipment document

source provision.
```

---

# 9. Evidence Assessment

Evidence does not prove itself.

Therefore:

```text
Evidence
    ≠
EvidenceAssessment.
```

`EvidenceAssessment` determines whether evidence is:

```text
relevant

authentic enough

valid

current

properly scoped

issued by competent actor

sufficient for the requirement.
```

---

# 10. Evidentiary Sufficiency

**Evidentiary sufficiency** answers:

> Does the currently accepted evidence set establish enough to support this regulatory conclusion?

This is different from:

```text
Is the evidence genuine?
```

A genuine certificate may be:

```text
expired

for another shipment

for another legal entity

for another product

insufficient by itself.
```

---

# 11. Decision Trace

A `DecisionTrace` answers:

> Which rule/fact/evidence/evaluator path actually produced this decision?

It is not an application debug stack trace.

---

# 12. Audit Log

An audit log records:

```text
who did what
when
to which object.
```

It is necessary but insufficient for regulatory explainability.

---

# 13. Reproducibility

Reproducibility answers:

> Can Baobab reconstruct the material inputs, rules, context and evaluator state sufficiently to explain or re-evaluate the historical decision?

Exact byte-for-byte regeneration of every AI intermediate output is not always required.

The canonical promoted state must nevertheless remain reproducible enough for the decision.

---

# 14. Canonical Evidence Chain

The normative chain SHALL be:

```text
                    LEGAL AUTHORITY
                          │
                          ▼
                        SOURCE
                          │
                          ▼
                     SOURCE EDITION
                          │
                          ▼
                      ARTEFACT
                          │
                     hash / signature
                          │
                          ▼
                     ACQUISITION
                          │
                          ▼
                 DOCUMENT TRANSFORMATION
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
                          ▼
                    RULESET SNAPSHOT
                          │
                          ▼
                 REGULATORY CONTEXT
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
             FACTS               EVIDENCE
                │                   │
                └─────────┬─────────┘
                          ▼
                     ASSESSMENT
                          │
                          ▼
                      DECISION
                          │
                          ▼
                 OPERATIONAL RESULT
```

---

# 15. Two Evidence Domains

Baobab SHALL distinguish two broad evidentiary domains:

```text
A. LEGAL / RULE EVIDENCE

B. TRANSACTION / FACTUAL EVIDENCE
```

---

# 16. Legal / Rule Evidence

This supports:

```text
Why does this rule exist?

What law created it?

Why is this interpretation used?

Why does this rule override another?
```

Typical chain:

```text
Source Artefact
   ↓
Provision
   ↓
Interpretation
   ↓
Rule.
```

---

# 17. Transaction / Factual Evidence

This supports:

```text
Does the rule apply to this transaction?

Was the requirement satisfied?

Was a prohibition breached?
```

Typical chain:

```text
External Fact
    ↓
Evidence
    ↓
EvidenceAssessment
    ↓
Regulatory Fact
    ↓
Rule Evaluation.
```

---

# 18. These Evidence Domains SHALL NOT Be Confused

A Gazette proves:

```text
a regulation was published
```

but does not prove:

```text
Shipment S has a valid phytosanitary certificate.
```

A shipment certificate may establish a transaction fact but does not establish:

```text
which statute required the certificate.
```

---

# 19. LegalRuleML Alignment

LegalRuleML explicitly identifies the need to preserve connections between formal norms and the legally binding textual provisions that express them.

Its model supports fine-grained source relationships and N:M linkage between rules and textual provisions.

Baobab SHALL support at least the same semantic capability.

---

# 20. Provision-to-Rule N:M Provenance

This architecture SHALL support:

```text
Provision A ───┐
Provision B ───┼──► Rule R
Provision C ───┘
```

and:

```text
             ┌──► Rule R1
Provision P ─┼──► Rule R2
             └──► Rule R3
```

No assumption of:

```text
one provision = one rule.
```

---

# 21. Fine-Grained Legal Locator

A rule MAY derive from:

```text
entire instrument

section

article

paragraph

subparagraph

sentence

table cell

schedule item

definition

footnote

incorporated provision.
```

The provenance model SHALL preserve the finest reliable locator available.

---

# 22. Citation Identity

`RegulatoryCitation` SHALL be a first-class value/object.

Conceptually:

```text
RegulatoryCitation
├── citation_id
├── authority_ref?
├── jurisdiction_ref
├── instrument_ref?
├── provision_ref?
├── source_ref
├── source_edition_ref?
├── external_identifier?
├── publication_name?
├── publication_number?
├── notice_number?
├── publication_date?
├── provision_locator?
├── page_locator?
├── language
├── canonical_uri?
├── external_uri?
└── citation_text?
```

---

# 23. Citation Is Structured First

Baobab SHOULD generate human-readable citation strings from structured metadata.

It SHOULD NOT use citation prose as the only canonical representation.

---

# 24. Persistent Legal Identifiers

Where authoritative persistent identifiers exist, they SHOULD be preserved.

ELI provides a common model for identifying and exchanging legislation metadata, with stable legal-resource identifiers as a core objective.

Examples include:

```text
ELI

CELEX

Gazette number

Act number

official notice number

official judgment identifier.
```

---

# 25. External Identifier Is Not Baobab Canonical ID

Example:

```text
ELI URI
```

remains an external legal identifier.

Baobab may still use:

```text
reginst_...
```

as its canonical internal identity.

---

# 26. Citation Versions

Citations SHALL be capable of resolving to the relevant:

```text
InstrumentExpression

ProvisionVersion

SourceEdition
```

rather than always resolving to a mutable "latest" view.

---

# 27. Citation to Consolidation

If a citation points to a consolidated text:

```text
citation target = consolidation
```

SHALL be distinguishable from:

```text
authoritative promulgating publication.
```

---

# 28. Citation Resolution

Baobab SHOULD provide:

```text
resolveCitation(citation)
```

which may return:

```text
canonical object

official identifier

source edition

source artefact

human display citation.
```

---

# 29. Broken External Links

A source URL disappearing SHALL NOT break historical citation identity.

Baobab SHALL retain:

```text
source ID

edition ID

external identifier

historical URI

artefact reference where rights permit.
```

---

# 30. Provenance Entity

Conceptually aligned with W3C PROV, evidentiary objects such as:

```text
SourceArtefact

RegulatoryDocumentIR

ProvisionVersion

Interpretation

RuleVersion

EvidenceRecord

Decision
```

are provenance `Entities`.

W3C PROV treats an Entity as a physical, digital or conceptual thing with fixed aspects.

---

# 31. Provenance Activity

Activities include:

```text
Acquisition

Conversion

OCR

Extraction

Normalisation

Translation

Interpretation

Rule compilation

Review

Rule publication

Evidence verification

Rule evaluation

Decision generation.
```

---

# 32. Provenance Agent

Agents include:

```text
RegulatoryAuthority

Publisher

Human Reviewer

Tenant Counsel

Baobab Service

Docling Adapter

Haystack Pipeline

LLM Provider

OPA Runtime

Rules Compiler.
```

---

# 33. Software Agent Is an Agent

The provenance model SHALL record software as responsible processing agents where material.

Example:

```text
activity:
DOCUMENT_CONVERSION

agent:
docling 2.x

configuration:
conversion-profile-v4
```

---

# 34. Human Agent

Where human review materially affects regulatory knowledge:

```text
reviewer identity

role

scope of authority

action

time
```

SHALL be preserved.

---

# 35. Review Role Matters

The record SHOULD distinguish:

```text
extractor

legal reviewer

regulatory analyst

maker

checker

approver

tenant counsel

platform administrator.
```

---

# 36. Acting-on-Behalf-Of Relationship

Where appropriate, Baobab MAY represent:

```text
Reviewer A
acted_on_behalf_of
Tenant T
```

or:

```text
Employee R
acted_on_behalf_of
Baobab Platform.
```

This is consistent with PROV's responsibility model.

---

# 37. Provenance Activity Record

Conceptually:

```text
ProvenanceActivity
├── activity_id
├── activity_type
├── started_at
├── ended_at?
├── actor_refs[]
├── software_agent_refs[]
├── input_refs[]
├── output_refs[]
├── configuration_ref?
├── model_ref?
├── rights_decision_ref?
├── status
├── trace_id?
└── metadata
```

---

# 38. Derivation Relationship

Every material transformation SHALL support:

```text
output
    DERIVED_FROM
input.
```

Examples:

```text
DocumentIR
    DERIVED_FROM
SourceArtefact

ProvisionVersion
    EXTRACTED_FROM
DocumentIR

RuleVersion
    DERIVED_FROM
Interpretation.
```

---

# 39. Transformation Parameters

Material transformations SHALL record configuration sufficiently to determine:

```text
which transformation occurred
```

without requiring all source code to be embedded in the database.

---

# 40. Code Version

Processing activities SHOULD reference:

```text
application version

component version

pipeline version

Git commit or immutable build identifier
```

where operationally feasible.

---

# 41. Container/Image Identity

High-assurance processing MAY also record:

```text
container image digest
```

for important transformation workers.

This is particularly useful for replay investigations.

---

# 42. Parser Provenance

Document conversion SHOULD record:

```text
provider = Docling

provider version

configuration profile

input artefact

output IR fingerprint

warnings.
```

---

# 43. Haystack Provenance

Knowledge-processing steps SHOULD record:

```text
pipeline version

component versions

input references

model calls where relevant

candidate outputs.
```

---

# 44. Qdrant Is Not Evidentiary Truth

Qdrant search results SHALL NOT become provenance roots.

A retrieved Qdrant chunk SHALL resolve to:

```text
source chunk
    ↓
DocumentIR
    ↓
SourceArtefact.
```

---

# 45. Retrieval Provenance

Where a retrieval result materially informed an AI-generated candidate, Baobab SHOULD retain:

```text
retrieval query identity

retrieved canonical/chunk IDs

ranking metadata if relevant

retriever version

embedding model

filter context.
```

---

# 46. No Need to Store Every Similarity Score Forever

Operationally irrelevant retrieval diagnostics MAY be governed by retention policy.

But the set of material source chunks supporting a promoted interpretation SHOULD remain identifiable.

---

# 47. AI Provenance

Where an AI model assists with:

```text
extraction

classification

interpretation

rule generation

explanation
```

the provenance record SHOULD include:

```text
provider

model identifier

model version where exposed

request/template version

input references

structured output

execution time

human-review outcome.
```

---

# 48. Prompt Template Version

Prompts SHALL be versioned where their semantics materially affect candidate generation.

Example:

```text
reg_rule_extraction:v7
```

---

# 49. Prompt Text Retention

Full prompts containing:

```text
licensed

privileged

tenant-private
```

content need not always be retained.

Baobab MAY instead preserve:

```text
template version

input IDs

prompt hash

execution parameters
```

subject to governance.

---

# 50. No Private Model Chain-of-Thought Dependency

Baobab SHALL NOT depend upon hidden model chain-of-thought as evidence for a regulatory conclusion.

Evidence SHALL be based on:

```text
source material

structured inputs

structured outputs

explicit rule relationships

review actions.
```

---

# 51. AI Output Is Not Evidence of Law

An LLM saying:

```text
"Section 14 creates a prohibition"
```

is not legal-source evidence.

The underlying:

```text
Section 14
```

is the legal source.

The AI output is a candidate interpretation artefact.

---

# 52. Interpretation Provenance

`RegulatoryInterpretation` SHALL identify:

```text
provision versions interpreted

other legal materials considered

interpretation origin

authors/reviewers

AI assistance if any

verification state

jurisdiction

effective scope.
```

---

# 53. Alternative Interpretation Provenance

Competing interpretations SHALL retain separate evidence chains.

Example:

```text
Provision P
   ├── Interpretation I1
   │      └── Counsel A
   │
   └── Interpretation I2
          └── Reviewer B
```

Selecting I1 SHALL not delete I2.

---

# 54. Rule Derivation

Every `RuleVersion` SHALL identify:

```text
interpretation_ref

provision_refs[]

rule origin

compiler/author

verification

publication state.
```

---

# 55. Authority-Supplied Rule

For an authority-supplied machine rule:

```text
rule origin =
AUTHORITY_SUPPLIED_MACHINE_RULE
```

and provenance SHALL connect directly to:

```text
authority

official machine artefact

human-readable legal source
```

where available.

---

# 56. Compiled Rule Provenance

When Baobab Rule IR is compiled into:

```text
Rego

OPA bundle

future evaluator representation
```

that output SHALL retain:

```text
source RuleVersion IDs

compiler version

IR version

bundle revision

build fingerprint.
```

---

# 57. OPA Decision Provenance

OPA decision logs can expose:

```text
decision_id

trace_id

policy path

bundle revisions
```

for a policy decision.

Baobab SHOULD capture these identifiers when OPA materially participates in a regulatory or processing decision.

---

# 58. OPA Bundle Revision

OPA bundle manifests support revision metadata and optional signature verification.

Baobab SHOULD therefore be able to establish:

```text
which policy bundle revision
```

produced an OPA decision.

---

# 59. OPA Provenance Is a Segment

OPA provenance SHALL NOT be treated as the complete regulatory provenance.

Correct:

```text
Legal Source
→ RuleVersion
→ Baobab IR
→ OPA Bundle Revision
→ OPA Decision ID
→ RegulatoryDecision.
```

---

# 60. Runtime Fact Provenance

Every material fact used in consequential assessment SHOULD identify its source.

Examples:

```text
product classification
    ← Trade product record

destination
    ← Shipment

legal entity
    ← Control Plane

permit validity
    ← authority API / evidence

tax registration
    ← ERP / verified registry.
```

---

# 61. Fact Snapshot

Runtime assessment SHALL ordinarily use immutable:

```text
RegulatoryFactSnapshot
```

records or equivalent references.

---

# 62. RegulatoryFact

Conceptually:

```text
RegulatoryFact
├── fact_id
├── fact_type
├── subject_ref
├── value
├── unit?
├── valid_at
├── source_system_ref
├── source_object_ref?
├── evidence_refs[]
├── verification_state
├── observed_at
└── provenance
```

---

# 63. Facts Are Not Master Data

Regulations MAY preserve:

```text
fact used in Decision D
```

without becoming authoritative owner of:

```text
Shipment S
```

or:

```text
Product P.
```

---

# 64. Context Snapshot

Every consequential assessment SHALL record a stable representation of the material regulatory context.

This MAY include:

```text
tenant

legal entity

organisation

market

jurisdiction roles

origin

destination

transit jurisdictions

product

classification

counterparty

transaction

effective evaluation date.
```

---

# 65. Platform Context Provenance

Context facts resolved by Control Plane SHALL carry:

```text
context_id

resolver/version where material

canonical IDs

resolved_at.
```

---

# 66. Caller Claims Versus Resolved Facts

The evidence chain SHALL preserve whether a value came from:

```text
caller request
```

versus:

```text
authoritative platform context resolution.
```

---

# 67. EvidenceRecord

Transaction/regulatory evidence SHALL use a canonical object such as:

```text
RegulatoryEvidence
├── evidence_id
├── evidence_type
├── subject_ref
├── scope
├── issuer_ref?
├── issued_at?
├── valid_from?
├── valid_to?
├── artefact_ref?
├── external_reference?
├── claimed_facts[]
├── submitted_by?
├── obtained_by?
├── classification
├── rights_profile_ref?
├── status
└── provenance
```

---

# 68. Evidence Scope

Evidence SHALL declare relevant scope where possible:

```text
ENTITY

LEGAL_ENTITY

PRODUCT

SHIPMENT

TRANSACTION

LOCATION

ACTIVITY

PERIOD

MARKET

JURISDICTION.
```

---

# 69. Evidence Authenticity

Evidence authenticity SHALL be evaluated separately from its relevance.

Possible dimensions:

```text
issuer verified

signature verified

source verified

document integrity verified

registry corroborated.
```

---

# 70. Evidence Validity

Validity may include:

```text
valid date range

revocation state

expiry

status

jurisdiction.
```

---

# 71. Evidence Relevance

Evidence may be authentic and valid but irrelevant.

Example:

```text
valid export permit
```

for:

```text
another product category.
```

---

# 72. Evidence Sufficiency

One evidence object may be insufficient.

Example:

```text
Requirement:
origin must be demonstrated.

Evidence:
commercial invoice only.
```

The evidence may be genuine but insufficient under the applicable rule.

---

# 73. EvidenceSet

Baobab SHOULD support:

```text
EvidenceSet
```

for conclusions requiring several pieces of evidence.

Conceptually:

```text
EvidenceSet
├── evidence_set_id
├── purpose
├── evidence_refs[]
├── assessment_refs[]
├── completeness
├── contradictions[]
├── outcome
└── provenance
```

---

# 74. Evidence Relationship Types

At minimum:

```text
SUPPORTS

SATISFIES

PARTIALLY_SATISFIES

CORROBORATES

CONTRADICTS

WEAKENS

CONTEXTUALISES

SUPERSEDES

REVOKES.
```

---

# 75. Evidence Independence

Ten evidence records are not necessarily ten independent pieces of evidence.

Example:

```text
Article A
Article B
Article C
```

may all repeat:

```text
one regulator press release.
```

Baobab SHOULD preserve common-source lineage where known.

This follows the same evidence-quality principle already established for Pulse.

---

# 76. Missing Evidence

Missing evidence SHALL remain:

```text
MISSING
```

or:

```text
UNKNOWN
```

depending on semantics.

It SHALL NOT automatically become:

```text
NEGATIVE_EVIDENCE.
```

---

# 77. Negative Evidence

Negative evidence requires an affirmative basis.

Example:

```text
Official permit register
exhaustively searched
and permit not present.
```

Even then, the legal significance depends upon the reliability/completeness of that register.

---

# 78. EvidenceAssessment

Conceptually:

```text
EvidenceAssessment
├── assessment_id
├── evidence_ref
├── requirement_ref?
├── fact_ref?
├── relevance
├── authenticity
├── validity
├── scope_match
├── issuer_status
├── temporal_match
├── contradictions[]
├── result
├── assessor
├── policy_version
└── assessed_at
```

---

# 79. EvidenceAssessment Result

Possible:

```text
ACCEPTED

ACCEPTED_WITH_LIMITATIONS

PARTIALLY_ACCEPTED

REJECTED

INDETERMINATE

REVIEW_REQUIRED.
```

---

# 80. Requirement Satisfaction

`EvidenceAssessment` may support a `RequirementSatisfaction` result.

It SHALL not mutate the requirement itself.

---

# 81. One Evidence Can Satisfy Multiple Requirements

Example:

```text
Certificate C
```

may satisfy:

```text
Requirement R1

Requirement R2
```

if legally appropriate.

Each satisfaction relationship SHALL be explicit.

---

# 82. One Requirement Can Require Multiple Evidence Objects

Example:

```text
ALL_OF:
certificate
invoice
origin declaration.
```

The evidentiary model SHALL support composite requirements from ADR-REG-0008.

---

# 83. Evidence Revision

A newer artefact MAY supersede older evidence.

Historical assessments SHALL continue to reference what they actually used.

---

# 84. Evidence Revocation

If an authority revokes a permit/certificate:

```text
revocation
```

SHALL be represented as an event/evidence relationship.

It SHALL not silently delete the prior evidence.

---

# 85. Historical Validity

An evidence item can be:

```text
invalid today
```

yet have been:

```text
valid on the transaction date.
```

ADR-REG-0015 will deepen this temporal model.

---

# 86. Chain-of-Custody Record

For material artefacts, Baobab SHOULD maintain:

```text
ArtefactCustodyEvent
├── custody_event_id
├── artefact_ref
├── event_type
├── actor_ref
├── system_ref?
├── occurred_at
├── from_location?
├── to_location?
├── hash_before?
├── hash_after?
├── reason
└── provenance
```

---

# 87. Custody Event Types

Possible:

```text
ACQUIRED

RECEIVED

UPLOADED

HASHED

SCANNED

QUARANTINED

RELEASED

COPIED

MIGRATED

ARCHIVED

RESTORED

EXPORTED

DELETED.
```

---

# 88. Storage Copy Is Not New Legal Source

Copying an artefact:

```text
primary object storage
→ disaster recovery storage
```

does not create a new underlying legal source.

It creates a new custody/storage event.

---

# 89. Hashes

Cryptographic hashes SHOULD be used to support artefact-integrity verification.

NIST describes hashes as values used to substantiate integrity of digital evidence, and its digital-evidence guidance recommends hashing digital evidence as a preservation best practice.

---

# 90. Hash Is Not Authenticity

A matching hash proves:

```text
same bytes
```

relative to the recorded reference.

It does not prove:

```text
legal authenticity.
```

---

# 91. Hash Does Not Prove Truth

A perfectly hashed fraudulent certificate remains fraudulent.

---

# 92. Signature Evidence

Where official sources/evidence provide digital signatures:

```text
signature value

certificate chain

validation status

validation time

algorithm

signer identity
```

SHOULD be retained where appropriate.

---

# 93. Signature Does Not Prove Current Validity

A document can have a valid signature while being:

```text
expired

revoked

superseded.
```

---

# 94. Trusted Timestamps

High-value evidence MAY use a trusted timestamp service.

RFC 3161 defines a protocol for a Time-Stamp Authority to provide evidence that a datum existed before a specified time.

This SHALL remain optional initially.

---

# 95. Timestamp Is Not Legal Effective Time

A trusted timestamp proves:

```text
datum existed by time T.
```

It does not prove:

```text
regulation legally took effect at T.
```

---

# 96. Acquisition Timestamp

Likewise:

```text
retrieved_at
```

is different from:

```text
published_at
effective_from
observed_at
signed_at.
```

---

# 97. Evidence Time Dimensions

The model SHALL be capable of distinguishing:

```text
event_time

legal_valid_time

publication_time

acquisition_time

verification_time

knowledge_time

decision_time.
```

ADR-REG-0015 will make this bitemporal model normative.

---

# 98. DecisionEvidenceSet

Every consequential regulatory assessment SHOULD produce or reference a:

```text
DecisionEvidenceSet.
```

---

# 99. DecisionEvidenceSet Contents

At minimum where relevant:

```text
context snapshot

ruleset fingerprint

rule version refs

hierarchy/override refs

fact refs

evidence refs

evidence-assessment refs

source/provision refs

exceptions considered

unresolved issues

evaluator identity/version.
```

---

# 100. RuleSetSnapshot

Consequential decisions SHALL bind to a stable:

```text
RuleSetSnapshot
```

or equivalent immutable fingerprint.

---

# 101. No Mid-Decision Rule Mutation

An assessment SHALL NOT begin using:

```text
RuleSet V1
```

and finish after silently switching to:

```text
RuleSet V2.
```

---

# 102. Decision Context Fingerprint

A decision MAY calculate a deterministic fingerprint over material context and rule/evidence identities.

Conceptually:

```text
decision_input_fingerprint =
HASH(
  ruleset_snapshot
  + context_snapshot
  + evidence_set
  + evaluator_version
)
```

The exact canonicalisation format SHALL be defined later.

---

# 103. Decision Record

Conceptually:

```text
RegulatoryDecision
├── decision_id
├── assessment_ref
├── context_snapshot_ref
├── ruleset_snapshot_ref
├── evidence_set_ref
├── decision_effect
├── assessment_outcome
├── effect_class
├── reason_codes[]
├── unresolved_issues[]
├── evaluator_ref
├── evaluator_version
├── opa_decision_ref?
├── trace_id
├── decided_at
└── provenance
```

---

# 104. Decision Explanation

The system SHOULD be able to produce:

> Shipment `SHP-001` requires Permit P because Rule R17 applies to imports of Product Class X into South Africa. Rule R17 derives from Provision 14(2) of Instrument I, effective on the transaction date. Permit evidence E44 was supplied but expired before shipment date, so Requirement Q12 was unsatisfied.

This SHALL be generated from structured evidence.

---

# 105. Explanation Is a Projection

Human-readable explanation is a projection of:

```text
DecisionTrace
```

and SHALL NOT itself become the source of decision truth.

---

# 106. DecisionTrace

Conceptually:

```text
DecisionTrace
├── decision_id
├── candidate_rules[]
├── applicable_rules[]
├── excluded_rules[]
├── facts[]
├── evidence[]
├── conditions[]
├── exceptions[]
├── conflicts[]
├── hierarchy_resolution[]
├── resolved_effects[]
├── requirements[]
├── rule_results[]
└── decision_result
```

---

# 107. Deliberate Trace, Not Hidden Reasoning

The trace SHALL store:

```text
machine-evaluable conditions

facts

rule references

evidence references

decision transitions.
```

It SHALL NOT depend on hidden internal LLM reasoning.

---

# 108. Evaluation Provenance

Every material rule evaluation SHOULD capture:

```text
rule_id

rule_version

input facts

result

error/unknown reason

execution engine

execution version.
```

---

# 109. OPA Evaluation

When OPA evaluates compiled regulatory policy:

```text
Baobab decision trace
    ↓
OPA decision ID
    ↓
bundle revision
    ↓
policy entrypoint
    ↓
OPA result
```

SHALL be linkable.

OPA's own API supports reporting the loaded bundle revision as provenance information.

---

# 110. Non-OPA Evaluator

Equivalent provenance requirements SHALL apply if OPA is later replaced.

OPA-specific identifiers SHALL therefore remain infrastructure metadata beneath Baobab-owned evaluator contracts.

---

# 111. Compiler Provenance

The rule compiler SHALL produce something like:

```text
CompiledRuleArtifact
├── compiled_artifact_id
├── rule_ir_version
├── source_rule_refs[]
├── compiler_version
├── target
├── target_version
├── content_hash
├── built_at
└── build_provenance
```

---

# 112. Bundle Provenance

For OPA:

```text
OPA Bundle
├── bundle_revision
├── compiled rule refs
├── manifest
├── bundle hash
├── signature?
└── build identity
```

---

# 113. Bundle Signing

OPA supports bundle signature verification, providing a useful integrity mechanism for distributed compiled policy.

Baobab SHOULD consider signed bundles for high-assurance deployment.

---

# 114. Bundle Signature Does Not Establish Legal Authority

It proves:

```text
bundle integrity / signer
```

not:

```text
law correctness.
```

---

# 115. Human Review Evidence

A consequential review decision SHALL capture:

```text
reviewer identity

reviewer role

scope

candidate reviewed

sources viewed

decision

reason code

free-text rationale where appropriate

timestamp.
```

---

# 116. Reviewer Rationale

Free-text rationale MAY supplement structured decision reasons.

It SHALL NOT replace:

```text
rule/source/provenance links.
```

---

# 117. Maker-Checker Provenance

Where two-person approval is required:

```text
Maker M
    ↓ submits
Candidate C
    ↓ checks
Checker K
    ↓ promotes
RuleVersion R.
```

All actions SHALL remain independently visible.

---

# 118. No Self-Approval by Accident

If policy requires separation of duties:

```text
maker_id ≠ checker_id
```

SHALL be enforceable rather than documented informally.

---

# 119. LangGraph Workflow Provenance

Where LangGraph orchestrates review:

```text
workflow_run_id

workflow_definition_version

checkpoint IDs

interrupt/review transitions

final canonical action
```

MAY be retained as workflow provenance.

Canonical governance state remains in Regulations.

---

# 120. Workflow State Is Not Evidence of Law

LangGraph saying:

```text
state = APPROVED
```

does not itself establish regulatory authority.

The canonical review/promotion record does.

---

# 121. Source Trust Evidence

A decision's legal-source provenance SHOULD be able to traverse into:

```text
SourceTrustAssessment
```

from ADR-REG-0011.

Thus:

```text
Decision
 → Rule
 → Source
 → Trust assessment.
```

---

# 122. Rights Provenance

Where relevant, provenance SHALL also link to:

```text
ContentRightsProfile
```

or:

```text
RightsDecision
```

that permitted processing.

---

# 123. Rights Provenance Is Not Legal Evidence

The fact that Baobab was licensed to process a Gazette does not establish the Gazette's legal force.

These dimensions remain separate.

---

# 124. Source Trust Is Not Evidence Sufficiency

Likewise:

```text
highly authoritative source
```

does not mean:

```text
this transaction requirement is satisfied.
```

---

# 125. Contradictory Evidence

Baobab SHALL preserve contradictions.

Example:

```text
Authority API:
Permit ACTIVE

Submitted certificate:
Permit EXPIRED.
```

Correct:

```text
EVIDENCE_CONFLICT.
```

Not:

```text
pick newest record automatically
```

unless policy establishes such precedence.

---

# 126. Contradiction Relationship

Evidence graph relationships SHOULD include:

```text
CONTRADICTS
```

with explicit subject/fact scope.

---

# 127. Corroboration

Two genuinely independent evidence sources may:

```text
CORROBORATE
```

a fact.

That relationship MAY increase assurance.

It SHALL not become an opaque numeric trust score.

---

# 128. Rejected Evidence

Rejected evidence SHALL usually remain in the evidence history with:

```text
rejection reason.
```

It SHALL not disappear merely because it was unusable.

---

# 129. Fraudulent Evidence

Suspected fraudulent evidence SHALL be classified appropriately.

Regulations SHALL NOT automatically conclude:

```text
criminal fraud
```

unless a competent process establishes that conclusion.

---

# 130. Evidence Correction

If Baobab mis-parses evidence:

```text
parser correction
```

SHALL remain distinct from:

```text
source document correction.
```

---

# 131. Decision Correction

If a decision is later found erroneous:

```text
corrected decision
```

SHALL preserve:

```text
original decision

reason for correction

new decision

affected operational actions.
```

---

# 132. Decision Supersession

Preferred:

```text
Decision D2
SUPERSEDES
Decision D1.
```

Not destructive replacement.

---

# 133. Appeal / Challenge Provenance

Where a decision is reviewed or challenged:

```text
Decision
    ↓
Challenge
    ↓
Review
    ↓
Confirmed / Varied / Reversed.
```

The chain SHALL remain intact.

---

# 134. Operational Enforcement Evidence

Domain engines SHOULD eventually provide an enforcement receipt or equivalent.

Example:

```text
RegulatoryDecision D
      │
      ▼
Trade Enforcement
      │
      ▼
Shipment transitioned to HOLD
```

---

# 135. EnforcementReceipt

Conceptually:

```text
EnforcementReceipt
├── receipt_id
├── decision_ref
├── consumer_engine
├── canonical_object_ref
├── action
├── status
├── executed_at
├── correlation_id
└── result_metadata
```

---

# 136. Decision ≠ Enforcement

A Regulations decision may say:

```text
REVIEW_REQUIRED
```

while Trade performs:

```text
HOLD_ORDER.
```

Both must be visible.

---

# 137. Enforcement Failure

If Trade fails to enforce an E4 decision:

```text
decision provenance remains valid
```

while:

```text
enforcement failure
```

becomes a separate operational event.

---

# 138. Outcome Evidence

Later real-world outcomes MAY feed back as evidence.

Examples:

```text
customs cleared shipment

regulator rejected filing

permit accepted

authority issued ruling.
```

---

# 139. Outcome Does Not Retroactively Rewrite Rule

One customs clearance does not automatically prove:

```text
Rule R was universally correct.
```

It may:

```text
support

contradict

trigger review.
```

---

# 140. Evidence Bundle

Baobab SHOULD support a portable:

```text
RegulatoryEvidenceBundle
```

for selected decisions.

---

# 141. Evidence Bundle Contents

A bundle MAY include:

```text
decision record

assessment

context snapshot

rule references

rule versions

source citations

evidence records

evidence assessments

decision trace

review actions

OPA decision metadata

enforcement receipt

integrity manifest.
```

---

# 142. Evidence Bundle Shall Respect Rights

Restricted commercial or privileged content SHALL not automatically be embedded.

Instead a bundle MAY contain:

```text
source identifier

hash

citation

restricted-content marker.
```

---

# 143. Evidence Bundle Manifest

Conceptually:

```text
EvidenceBundleManifest
├── bundle_id
├── decision_ref
├── generated_at
├── included_objects[]
├── excluded_objects[]
├── exclusion_reasons[]
├── hashes[]
├── schema_version
└── signature?
```

---

# 144. Evidence Bundle Integrity

A bundle MAY be cryptographically signed.

This proves integrity/authorship of the bundle.

It does not certify the legal conclusion as correct.

---

# 145. Audit Export

Possible formats MAY include:

```text
JSON

human-readable report

archive with manifests

RDF/PROV projection.
```

---

# 146. W3C PROV Export

Baobab SHOULD be capable of projecting selected provenance into W3C PROV-compatible structures:

```text
Entity

Activity

Agent

wasDerivedFrom

used

wasGeneratedBy

wasAssociatedWith.
```

This supports external interoperability without making PROV the internal domain model.

---

# 147. LegalRuleML Export

Likewise, rule provenance MAY eventually expose LegalRuleML-compatible source/isomorphism information.

Internal canonical semantics remain Baobab-owned.

---

# 148. Provenance Graph and Regulatory Knowledge Graph

ADR-REG-0010 established the logical Regulatory Knowledge Graph.

This ADR defines one important family within it:

```text
PROVENANCE / EVIDENCE GRAPH.
```

The graphs SHALL NOT require physically distinct databases.

---

# 149. Core Provenance Relationship Types

Initial relationships SHOULD include:

```text
ACQUIRED_FROM

PUBLISHED_AS

EXTRACTED_FROM

NORMALISED_FROM

TRANSLATED_FROM

DERIVED_FROM

INTERPRETS

ENCODES

COMPILED_FROM

GENERATED_BY

USED_BY

REVIEWED_BY

VERIFIED_BY

SUPPORTED_BY

SATISFIED_BY

CONTRADICTED_BY

SUPERSEDED_BY

ENFORCED_BY.
```

---

# 150. Generic `RELATED_TO` Is Insufficient

Consequential provenance SHALL use typed relationships.

---

# 151. Immutability

Material provenance events SHALL be append-oriented.

Corrections SHOULD create:

```text
new record
+
supersession/correction relation
```

rather than rewrite history.

---

# 152. Audit Logs Shall Be Tamper Evident Where Practical

Important audit/provenance stores SHOULD use controls such as:

```text
restricted mutation

append-only patterns

cryptographic integrity

immutable storage

controlled retention.
```

Exact infrastructure remains a deployment decision.

---

# 153. Blockchain Is Not Required

This ADR explicitly rejects:

```text
"provenance requires blockchain."
```

Cryptographic hashes, signatures, access controls, immutable storage and auditable event chains are sufficient for the initial architecture.

---

# 154. Blockchain MAY Be Considered Later

Only if a concrete multi-party trust problem justifies it.

It SHALL not be adopted as architectural theatre.

---

# 155. Centralised Provenance Can Be Valid

Baobab may remain the responsible system of record for provenance without pretending that decentralisation automatically improves legal assurance.

---

# 156. Retention

Provenance retention SHALL follow:

```text
decision criticality

contractual obligations

legal requirements

rights restrictions

tenant policies

audit requirements.
```

---

# 157. Decision Retention

Evidence required to defend a consequential decision SHOULD generally survive as long as the decision's required audit horizon.

---

# 158. Source Licence Limitation

Where source rights prohibit retention:

```text
retain citation/hash/metadata
```

MAY be necessary in place of the complete source artefact.

The resulting replay limitation SHALL be visible.

---

# 159. Audit Assurance State

A decision MAY expose:

```text
FULLY_REPRODUCIBLE

REPRODUCIBLE_WITH_EXTERNAL_SOURCE

PARTIALLY_REPRODUCIBLE

PROVENANCE_INCOMPLETE.
```

---

# 160. Reproducibility Is Multidimensional

Baobab SHOULD distinguish:

```text
SOURCE_REPRODUCIBILITY

RULE_REPRODUCIBILITY

FACT_REPRODUCIBILITY

EVALUATOR_REPRODUCIBILITY

EXPLANATION_REPRODUCIBILITY.
```

---

# 161. Exact Model Reproduction

LLM providers may update models or offer nondeterministic inference.

Therefore exact AI candidate recreation may be impossible.

This SHALL not compromise a decision if:

```text
the promoted interpretation/rule version
```

was durably persisted and verified.

---

# 162. Canonical Promotion Breaks Runtime AI Dependency

Once verified:

```text
AI candidate
    ↓
human/governed promotion
    ↓
canonical RuleVersion
```

future transactional decisions depend on the RuleVersion—not on reproducing the original AI response.

---

# 163. Decision Replay

A decision replay SHOULD support two modes:

```text
HISTORICAL_REPLAY

CURRENT_REEVALUATION.
```

---

# 164. Historical Replay

Uses:

```text
historical context
historical evidence
historical ruleset
historical evaluator version/policy
```

to reconstruct the historical decision.

---

# 165. Current Reevaluation

Uses:

```text
same business object
```

against:

```text
current rules
current evidence/current context.
```

The two SHALL never be conflated.

---

# 166. Historical Replay May Not Re-execute External Systems

If historical external provider state cannot be recreated:

```text
persisted fact/evidence snapshot
```

SHALL be used.

---

# 167. Reproducibility Fingerprint

A consequential Decision MAY retain:

```text
source_set_fingerprint

ruleset_fingerprint

context_fingerprint

evidence_set_fingerprint

compiled_policy_fingerprint.
```

---

# 168. Canonicalisation Before Hashing

Fingerprints over structured data SHALL use a defined canonical serialisation.

Otherwise logically identical objects could produce inconsistent hashes.

Exact canonicalisation is deferred to technical specification.

---

# 169. Trace Correlation

End-to-end operations SHOULD propagate:

```text
trace_id

correlation_id

decision_id.
```

---

# 170. Trace ID Is Not Domain ID

A distributed tracing identifier serves observability.

It does not replace:

```text
decision_id

assessment_id

acquisition_id.
```

---

# 171. OpenTelemetry Alignment

Baobab SHOULD correlate domain provenance with OpenTelemetry traces where useful.

Tracing MAY be ephemeral.

Domain provenance remains durable where required.

---

# 172. Observability Logs Are Not Canonical Provenance

Logs can expire.

Canonical provenance needed for regulatory reconstruction SHALL live in governed domain state.

---

# 173. Sensitive Provenance

Provenance itself may reveal:

```text
tenant activity

legal strategy

counsel identity

commercial providers

disputes

regulatory exposure.
```

Therefore it SHALL be access controlled.

---

# 174. Tenant Isolation

Tenant-private evidence SHALL remain tenant-scoped throughout:

```text
storage

PostgreSQL

Qdrant

LangGraph review

evidence bundles

AI retrieval.
```

---

# 175. Privileged Legal Material

Counsel opinions MAY be:

```text
LEGAL_PRIVILEGED
```

or equivalent.

Their existence, metadata and contents may all require restricted visibility.

---

# 176. Privilege Does Not Disappear in Provenance

A graph link to privileged evidence can itself leak sensitive information.

Relationship visibility SHALL therefore also be classified.

---

# 177. Redacted Provenance

Consumers MAY receive a redacted decision explanation:

```text
"verified tenant counsel interpretation"
```

without access to the privileged opinion.

---

# 178. Rights-Aware Citation

A consumer may receive:

```text
official citation
```

even where:

```text
licensed secondary commentary
```

cannot be displayed.

---

# 179. Evidence Access Is Purpose-Specific

A Trade service may need:

```text
Decision outcome
Requirement IDs
Reason codes
```

but not:

```text
full legal-counsel memorandum.
```

---

# 180. Provenance APIs

Potential task-oriented APIs include:

```text
GET /decisions/{id}/explanation

GET /decisions/{id}/evidence

GET /decisions/{id}/provenance

GET /rules/{id}/sources

GET /rules/{id}/derivation

GET /evidence/{id}/assessment

POST /decisions/{id}/evidence-bundle.
```

Exact routes are deferred.

---

# 181. No Unrestricted Graph Dump by Default

The provenance graph can expose sensitive relationships.

Public APIs SHALL remain capability-scoped.

---

# 182. Provenance Read Capability

Potential capability:

```text
regulations.provenance.read
```

SHALL be separate from:

```text
regulations.decision.read.
```

---

# 183. Evidence Bundle Capability

High-value export may require:

```text
regulations.evidence.export.
```

---

# 184. Administrative Correction Capability

Provenance correction SHALL require stronger privileges than ordinary reading.

---

# 185. Correction Does Not Mean Deletion

Corrections SHALL preserve:

```text
original assertion

corrected assertion

who corrected it

why.
```

---

# 186. Provenance Validation

Publication/promotion SHOULD validate:

```text
all canonical rules have provision/source path

all consequential decisions have ruleset

all material evidence has origin

all promoted interpretations have reviewers/origin

all compiled rules map to canonical RuleVersions.
```

---

# 187. Orphan Detection

The platform SHOULD detect:

```text
rule without source

decision without assessment

assessment without ruleset

evidence without origin

compiled bundle without source rule

Qdrant chunk without source reference.
```

---

# 188. Provenance Completeness

Potential states:

```text
COMPLETE

SUFFICIENT_FOR_PURPOSE

PARTIAL

BROKEN

UNKNOWN.
```

---

# 189. Provenance Completeness Can Cap Enforcement

An E4 decision SHALL not rely on:

```text
BROKEN
```

material legal provenance.

---

# 190. Evidence Sufficiency Can Cap Enforcement

Likewise:

```text
source rule provenance complete
```

but:

```text
transaction evidence indeterminate
```

may require:

```text
E2 REVIEW_GATE
```

or other conservative disposition.

---

# 191. Provenance Integrity Incident

Examples:

```text
hash mismatch

missing source artefact

deleted review action

unresolvable bundle revision

broken decision lineage.
```

These SHALL be treated as integrity/governance incidents.

---

# 192. Impact Analysis

A broken provenance object SHOULD support forward traversal:

```text
Compromised Artefact
       │
       ▼
Provisions
       │
       ▼
Rules
       │
       ▼
Assessments
       │
       ▼
Decisions.
```

This integrates directly with ADR-REG-0010 and future ADR-REG-0023.

---

# 193. Source Correction Blast Radius

If:

```text
Official Gazette correction
```

changes Provision P:

```text
P
 ↓
Interpretations
 ↓
Rules
 ↓
Decision dependencies
```

must become discoverable.

---

# 194. Evidence Revocation Blast Radius

If:

```text
Permit E
```

is revoked retroactively or determined fraudulent:

```text
Evidence E
 ↓
EvidenceAssessments
 ↓
RequirementSatisfaction
 ↓
Assessments
 ↓
Decisions.
```

Candidate impact SHALL be identifiable.

---

# 195. Pulse Boundary

Pulse maintains its own Intelligence Evidence Graph.

Regulations SHALL not copy Pulse conclusions into its legal evidence chain as authoritative law.

---

# 196. Pulse Evidence Can Be Discovery Evidence

A Pulse signal MAY appear as:

```text
DISCOVERY_EVIDENCE
```

triggering regulatory investigation.

It SHALL not become:

```text
LEGAL_SOURCE_EVIDENCE
```

without verification.

---

# 197. Regulations → Pulse

Regulations MAY provide Pulse:

```text
verified change ID

effective date

affected concepts

affected products

decision impact.
```

Pulse need not consume restricted legal provenance unless explicitly entitled.

---

# 198. CMS Boundary

CMS MAY publish citations and approved regulatory projections.

It SHALL not become the source of regulatory provenance simply because it displays the result.

---

# 199. CMS Publication Provenance

CMS MAY maintain its own separate chain:

```text
RegulatoryProjection
   ↓
CMS Article
   ↓
Public Page.
```

That is editorial provenance.

The regulatory provenance remains upstream in Regulations.

---

# 200. Public Citation

Digital Estates SHOULD ordinarily receive:

```text
verified citation
+
plain-language explanation
+
last-verified date
```

instead of a raw internal evidence graph.

---

# 201. Citation Freshness

A public citation MAY point to a valid rule even if an external URL later changes.

The canonical citation identity remains.

---

# 202. No Citation Hallucination

Generative components SHALL NOT invent citations.

Any cited legal source in a published explanation SHALL resolve to a canonical/source-registry object or clearly be presented as unverified.

---

# 203. AI Citation Verification

Before an AI-produced citation enters promoted regulatory content:

```text
citation exists

source resolves

locator resolves where possible

authority/source status known.
```

---

# 204. Citation Extraction

Haystack/AI MAY propose citation candidates.

Canonical citation resolution remains deterministic/governed where possible.

---

# 205. Document Locator Drift

If re-OCR/reparsing changes page/character locations:

```text
historical locator
```

SHALL remain associated with the historical representation.

A new representation may create new locators.

---

# 206. Stable Legal Locator Preferred

Where available:

```text
Section 14(2)(a)
```

is more durable than:

```text
character offsets 12,044–12,128.
```

Both may be retained.

---

# 207. Physical Page Locator

Page numbers remain useful for documentary verification, especially Gazette/PDF sources.

They SHALL not be the sole legal identity where structural identifiers exist.

---

# 208. Table Cell Citation

For tariff and schedule data, citation SHOULD support:

```text
schedule

table

row

column

classification entry.
```

---

# 209. Calculation Provenance

A regulatory calculation SHALL retain:

```text
formula version

input values

input source/evidence

rounding

currency/unit

output

calculation engine version.
```

---

# 210. Tariff Example

```text
Duty = customs_value × tariff_rate
```

The evidence chain SHALL identify:

```text
customs_value source

classification

tariff rule

rate

effective date

formula.
```

---

# 211. Deadline Provenance

For computed deadlines:

```text
rule

anchor date

calendar type

offset

holiday adjustment

timezone

derived due date
```

SHALL be explainable.

---

# 212. Classification Provenance

HS/product classifications SHALL identify:

```text
classification scheme

version

classification result

classifier/human determination

evidence

effective period.
```

---

# 213. Classification Change

Changing a classification MAY affect:

```text
tariffs

permits

SPS

restrictions.
```

The provenance graph SHALL support impact traversal.

---

# 214. Decision Reproduction Without Qdrant

A historical regulatory decision SHALL not depend on reconstructing Qdrant ranking.

The material promoted rules/evidence shall already be canonical.

---

# 215. Decision Reproduction Without Haystack

Likewise, canonical historical decisions SHALL remain explainable if Haystack is unavailable.

---

# 216. Decision Reproduction Without LangGraph

The final governance actions SHALL remain canonical even if the original workflow framework no longer exists.

---

# 217. Decision Reproduction Without OPA Version Availability

Where exact OPA runtime reproduction is impossible, Baobab SHALL retain:

```text
compiled policy

bundle revision/hash

decision trace

inputs

result.
```

---

# 218. Framework Replacement Principle

Provenance SHALL describe:

```text
what occurred
```

without forcing future Baobab versions to continue using the same framework.

---

# 219. Evidence Independence From Technology

`RegulatoryEvidence` SHALL NOT be:

```text
HaystackDocument

QdrantPoint

LangGraphState

OPAInput.
```

It is a Baobab domain concept.

---

# 220. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-PROV-I01` | Citation SHALL remain distinct from provenance |
| `REG-PROV-I02` | Provenance SHALL remain distinct from lineage |
| `REG-PROV-I03` | Chain of custody SHALL remain distinct from evidentiary sufficiency |
| `REG-PROV-I04` | Evidence SHALL not prove itself |
| `REG-PROV-I05` | Evidence assessment SHALL be independently addressable |
| `REG-PROV-I06` | Missing evidence SHALL not automatically become negative evidence |
| `REG-PROV-I07` | Legal/rule evidence and transaction evidence SHALL remain distinguishable |
| `REG-PROV-I08` | Every production rule SHALL retain legal-source provenance |
| `REG-PROV-I09` | Provision-to-rule provenance SHALL support N:M relationships |
| `REG-PROV-I10` | Fine-grained provision locators SHALL be retained where available |
| `REG-PROV-I11` | Material transformations SHALL be versioned |
| `REG-PROV-I12` | AI output SHALL not become legal-source evidence |
| `REG-PROV-I13` | Hidden LLM reasoning SHALL not be required for regulatory explanation |
| `REG-PROV-I14` | Human review actions SHALL be attributable |
| `REG-PROV-I15` | Maker-checker actions SHALL remain separately attributable |
| `REG-PROV-I16` | Cryptographic hash SHALL not be interpreted as proof of legal authenticity |
| `REG-PROV-I17` | Digital signature SHALL not automatically establish current legal validity |
| `REG-PROV-I18` | Trusted timestamp SHALL remain distinct from legal effective time |
| `REG-PROV-I19` | Historical evidence SHALL not be destructively overwritten |
| `REG-PROV-I20` | Corrected decisions SHALL retain the original decision |
| `REG-PROV-I21` | Every consequential assessment SHALL bind to a stable ruleset/context snapshot |
| `REG-PROV-I22` | Mid-assessment rule mutation SHALL not be permitted |
| `REG-PROV-I23` | OPA decision provenance SHALL remain linked to canonical RuleVersions |
| `REG-PROV-I24` | Qdrant retrieval SHALL resolve back to canonical/source provenance |
| `REG-PROV-I25` | Framework-native objects SHALL not become canonical evidence types |
| `REG-PROV-I26` | Tenant-private provenance SHALL remain isolated |
| `REG-PROV-I27` | Privileged provenance relationships SHALL be access-controlled |
| `REG-PROV-I28` | Evidence exports SHALL respect content rights |
| `REG-PROV-I29` | Provenance completeness SHALL influence enforcement eligibility |
| `REG-PROV-I30` | Consequential decisions SHALL be traversable backward to authoritative sources |

---

# 221. Rejected Alternative — Citation as Provenance

Rejected.

A citation does not tell us:

```text
who extracted it

how it was transformed

which interpretation was used.
```

---

# 222. Rejected Alternative — Logs as Provenance

Rejected.

Operational logs are neither sufficiently structured nor necessarily retained long enough.

---

# 223. Rejected Alternative — Hash Means Authentic

Rejected.

Integrity and authenticity differ.

---

# 224. Rejected Alternative — Signature Means Applicable

Rejected.

Signed documents may still be:

```text
expired

superseded

out of scope.
```

---

# 225. Rejected Alternative — Store Final Decision Only

Rejected.

A decision without its evidentiary basis is not acceptable for serious regulatory infrastructure.

---

# 226. Rejected Alternative — Store LLM Explanation as Evidence

Rejected.

AI narrative is a presentation layer.

---

# 227. Rejected Alternative — Screenshot as Sole Legal Evidence

Rejected where structured/official source identity is available.

Screenshots may supplement evidence but are weak for machine provenance.

---

# 228. Rejected Alternative — Delete Rejected Evidence

Rejected.

Rejection is itself part of governance history where retention permits.

---

# 229. Rejected Alternative — Recalculate Historical Decisions Using Current Law

Rejected.

That is current reevaluation, not historical replay.

---

# 230. Rejected Alternative — One `verified=true` Flag

Rejected.

Baobab needs to know:

```text
what was verified

by whom

against what evidence

at what time.
```

---

# 231. Rejected Alternative — Blockchain by Default

Rejected.

No demonstrated requirement currently justifies it.

---

# 232. Minimum Implementation Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text
1. Source → Edition → Artefact chain.

2. Artefact cryptographic hash.

3. Acquisition provenance.

4. Custody event history.

5. Docling conversion provenance.

6. Normalisation provenance.

7. Provision locator to exact source location.

8. One Provision → several Rules.

9. Several Provisions → one Rule.

10. Interpretation reviewer attribution.

11. AI-assisted interpretation attribution.

12. Rule compiler provenance.

13. Rule IR → OPA bundle relationship.

14. OPA bundle revision captured.

15. OPA decision ID captured.

16. Regulatory fact with external engine provenance.

17. Context snapshot.

18. Evidence record.

19. Evidence authenticity assessment.

20. Evidence relevance assessment.

21. Evidence insufficient despite authenticity.

22. Multiple evidence items satisfying one requirement.

23. One evidence item satisfying multiple requirements.

24. Contradictory evidence.

25. Missing evidence not treated as negative evidence.

26. Evidence revocation.

27. Evidence supersession.

28. Stable ruleset snapshot.

29. Decision input fingerprint.

30. Structured DecisionTrace.

31. Human-readable explanation generated from trace.

32. Maker-checker provenance.

33. LangGraph workflow reference without framework ownership.

34. Enforcement receipt from a consumer engine.

35. Historical decision correction preserving original.

36. Historical replay.

37. Current reevaluation producing a different result.

38. Rights-filtered evidence bundle.

39. Tenant-private evidence isolation.

40. Privileged evidence redaction.

41. Broken-provenance detection.

42. Source correction blast-radius traversal.

43. Evidence revocation blast-radius traversal.

44. W3C PROV-compatible bounded export.

45. Decision explainable without Haystack/Qdrant availability.
```

---

# 233. Initial ZuriBeans Proof

The first end-to-end case SHOULD demonstrate something like:

```text
Uganda / South Africa transaction
        │
        ▼
Official regulatory publication
        │
        ▼
Provision
        │
        ▼
Verified rule:
Certificate required
        │
        ▼
Shipment context
        │
        ▼
Certificate evidence
        │
        ▼
Evidence validity check
        │
        ▼
Assessment
        │
        ▼
Decision
```

and allow a reviewer to traverse:

```text
Decision
→ Requirement
→ Rule
→ Provision
→ Gazette

AND

Decision
→ EvidenceAssessment
→ Certificate
→ Issuer / validity / shipment scope.
```

---

# 234. Initial Negative Proof

The system SHOULD also demonstrate:

```text
Certificate genuine
        │
        ▼
but belongs to Shipment A
        │
        ▼
assessment concerns Shipment B
        │
        ▼
EvidenceAssessment:
AUTHENTIC
BUT
SCOPE_MISMATCH
        │
        ▼
Requirement remains UNSATISFIED.
```

This distinction is essential.

---

# 235. Initial Conflict Proof

```text
Authority API:
Permit ACTIVE

Tenant PDF:
Permit EXPIRED
        │
        ▼
EVIDENCE_CONFLICT
        │
        ▼
REVIEW_REQUIRED
```

rather than silently choosing one.

---

# 236. Initial Provenance Failure Proof

```text
Rule R17 exists

but source/provision lineage missing
        │
        ▼
PROVENANCE_BROKEN
        │
        ▼
not eligible for E3/E4.
```

---

# 237. Initial Correction Proof

```text
Original Gazette parser
misread table row

        ↓

new parser discovers error

        ↓

candidate corrected rule

        ↓

review

        ↓

new RuleVersion

        ↓

affected decisions identified.
```

Historical decisions remain reconstructable using the old state.

---

# 238. Commercial Capability — Explainable Decision

The evidence architecture enables a premium API response:

```text
Decision:
REVIEW_REQUIRED

Reason:
Import permit expired.

Legal basis:
Provision 14(2), Instrument X.

Rule:
reg_rule_123 v4.

Evidence:
Permit P-889.

Evidence result:
Authentic,
but expired 3 days before shipment.

Regulatory source:
Official Gazette issue Y.

Evaluated:
28 September 2026.
```

---

# 239. Commercial Capability — Audit Bundle

Baobab can provide:

> Produce the evidence package demonstrating why this shipment was blocked on 28 September 2026.

That is far more valuable than a generic compliance screenshot.

---

# 240. Commercial Capability — Decision Defence

Enterprise customers can answer:

```text
What did we know?

What rule did we use?

What evidence did we have?

Why did the system act?

Who reviewed it?
```

---

# 241. Commercial Capability — Historical Reconstruction

A customer may ask two years later:

> Would this transaction have been permitted under the rules applicable on its original shipment date?

This architecture is the prerequisite.

---

# 242. Commercial Capability — Provenance API

Possible higher-value products include:

```text
Regulatory Decision Evidence API

Rule Provenance API

Regulatory Audit Bundle

Compliance Evidence Register

Historical Regulatory Replay.
```

---

# 243. Coordination with Pulse

Pulse and Regulations SHOULD use compatible provenance principles.

But their evidence semantics remain different.

```text
PULSE:
evidence → intelligence

REGULATIONS:
legal source/evidence → normative decision.
```

---

# 244. Cross-Engine Correlation

A verified Regulations change event consumed by Pulse SHOULD carry:

```text
regulatory_change_id

source references

effective date

affected domain
```

without requiring Pulse to duplicate the full evidence chain.

---

# 245. Coordination with CMS

CMS publications SHOULD reference:

```text
canonical regulatory IDs

citations

last-verified state.
```

They need not copy the complete internal provenance graph.

---

# 246. CMS Staleness Detection

If a regulatory object used by CMS changes:

```text
Regulations provenance/version
```

allows CMS to determine:

```text
content references stale RuleVersion.
```

---

# 247. Strategic Principle

The real enterprise product is not simply:

```text
"Baobab says you need a permit."
```

It is:

```text
"Baobab says you need a permit,

here is the exact legal source,

here is the verified rule,

here are the facts used,

here is the evidence supplied,

here is what failed,

here is the evaluator version,

and here is the complete decision history."
```

---

# 248. Research Foundation Summary

W3C PROV provides a mature interoperability model centred on Entities, Activities and Agents, with explicit derivation, usage, generation, attribution, association and role semantics. Baobab will align conceptually while retaining richer domain-specific regulatory semantics.

LegalRuleML explicitly requires traceability between formal legal rules and legally binding textual sources and supports fine-grained N:M source-to-rule relationships, directly validating Baobab's source → provision → interpretation → rule evidence architecture.

ELI supplies a mature approach for persistent legal-resource identification and exchange of legislation metadata, supporting Baobab's structured citation and external-identifier architecture.

NIST digital-evidence preservation guidance emphasises documenting source/transfer history and using secure hashes or signatures to protect the integrity of retained digital evidence. Baobab adopts these technical integrity principles without claiming that its records automatically satisfy every court's procedural evidentiary requirements.

RFC 3161 provides a standards-based mechanism for creating trusted evidence that a datum existed before a particular time and may be used selectively for high-assurance artefacts or evidence bundles.

OPA's current decision-log and provenance facilities can expose decision IDs, traces, policy paths and exact loaded bundle revisions. Baobab will capture these where OPA executes deterministic policy while preserving the larger source-to-decision provenance chain independently of OPA.

---

# 249. Final Decision

Baobab Regulations SHALL adopt a **durable, cryptographically supportable, source-to-decision evidentiary architecture**.

The canonical chain is:

```text
                         AUTHORITY
                             │
                             ▼
                           SOURCE
                             │
                             ▼
                         PUBLICATION
                             │
                             ▼
                      SOURCE ARTEFACT
                             │
                  hash / signature / custody
                             │
                             ▼
                     PROCESSING ACTIVITY
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
                      RULESET SNAPSHOT
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       CONTEXT / FACTS                   EVIDENCE
              │                             │
              │                       assessment
              │                             │
              └──────────────┬──────────────┘
                             ▼
                         ASSESSMENT
                             │
                             ▼
                     DECISION TRACE
                             │
                             ▼
                     REGULATORY DECISION
                             │
                             ▼
                    ENFORCEMENT RECEIPT
                             │
                             ▼
                         OUTCOME
```

The engine SHALL always preserve the distinction:

```text
Citation
    tells us where.

Provenance
    tells us origin.

Lineage
    tells us dependencies.

Chain of custody
    tells us what happened to the artefact.

Evidence
    supports a claim or fact.

Evidence assessment
    tells us whether it is usable.

Decision trace
    tells us how the result was reached.

Reproducibility
    lets us reconstruct the material historical state.
```

The decisive principle is:

> **No consequential regulatory decision should exist without an evidentiary path back to both the law that created the requirement and the facts that established its application.**

A second principle is:

> **Integrity is not authenticity; authenticity is not relevance; relevance is not sufficiency; sufficiency is not legal authority.**

A third is:

> **A regulatory decision that cannot explain its evidence is not ready for autonomous enforcement.**

And the strategic objective is:

> **Baobab Regulations should make regulatory decisions not merely executable, but defensible.**

That is the architecture established by `ADR-REG-0014`.

---

## Decision Summary

```text
ADR-REG-0014
───────────────────────────────────────────────

CORE CHAIN

Authority
  ↓
Source
  ↓
Artefact
  ↓
Provision
  ↓
Interpretation
  ↓
Rule
  ↓
Context + Evidence
  ↓
Assessment
  ↓
Decision
  ↓
Enforcement


DISTINCTIONS

Citation ≠ Provenance

Provenance ≠ Lineage

Lineage ≠ Chain of Custody

Evidence ≠ Evidence Assessment

Authenticity ≠ Relevance

Relevance ≠ Sufficiency

Integrity ≠ Legal Authority


PROVENANCE MODEL

Entity
Activity
Agent

compatible with W3C PROV.


RULE PROVENANCE

N:M:

Provision ↔ Rule

compatible with
LegalRuleML principles.


EVIDENCE

Source-backed
Scoped
Temporal
Assessable
Contradictable
Revocable


CRYPTOGRAPHIC SUPPORT

Hashes
Signatures
Optional trusted timestamps

support integrity.

They do not manufacture
legal truth.


OPA

Decision ID
Bundle revision
Policy path

form one segment of
decision provenance.


AI

Model outputs are
candidate interpretations,
not evidence of law.

No hidden chain-of-thought
dependency.


HISTORICAL REPLAY

Historical law
+
historical context
+
historical evidence
+
historical evaluator

≠

current reevaluation.


COMMERCIAL RESULT

Every material decision can answer:

What law?

Which version?

What rule?

What evidence?

Which facts?

Who reviewed?

Which evaluator?

Why this outcome?
```
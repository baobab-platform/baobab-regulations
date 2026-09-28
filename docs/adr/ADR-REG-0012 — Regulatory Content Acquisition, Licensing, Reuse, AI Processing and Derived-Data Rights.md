# ADR-REG-0012 — Regulatory Content Acquisition, Licensing, Reuse, AI Processing and Derived-Data Rights

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0012`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Intellectual Property / Content Rights / Licensing / Reuse / AI Processing / Provider Exit Architecture  
**Strategic Classification:** Core Regulatory Content Governance / Commercial Sustainability / Platform Risk Control

**Parent Decisions**

- `ADR-REG-0001 — Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries`
- `ADR-REG-0010 — Regulatory Knowledge Graph, Relationship, Provenance and Traversal Model`
- `ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model`

**Relevant Baobab Architecture**

- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- applicable Shared external-reference, audit, event, tenancy and entitlement contracts

**Technology Context**

- Docling — candidate document-intelligence provider
- Haystack — candidate regulatory knowledge-processing provider
- LangGraph — candidate regulatory governance-workflow provider
- PostgreSQL 17 — likely canonical regulatory persistence
- object storage — likely immutable source-artefact retention

---

# 1. Executive Decision

Baobab Regulations SHALL treat **content rights as executable platform policy**, not merely procurement paperwork.

For every material regulatory source, Baobab SHALL determine separately whether it may:

```text
ACCESS

FETCH

DOWNLOAD

COPY

CACHE

STORE

ARCHIVE

BACKUP

OCR

PARSE

EXTRACT

NORMALISE

TRANSLATE

TRANSFORM

INDEX

FULL_TEXT_SEARCH

CREATE_EMBEDDINGS

USE_FOR_RAG

SEND_TO_EXTERNAL_MODEL

USE_FOR_MODEL_TRAINING

USE_FOR_FINE_TUNING

DERIVE_STRUCTURED_FACTS

DERIVE_INTERPRETATIONS

DERIVE_EXECUTABLE_RULES

QUOTE

DISPLAY_SNIPPETS

DISPLAY_FULL_TEXT

REDISTRIBUTE_RAW_CONTENT

REDISTRIBUTE_TRANSFORMED_CONTENT

REDISTRIBUTE_DERIVED_DATA

COMMERCIALISE_DERIVED_CAPABILITY

SHARE_WITH_TENANT

SHARE_ACROSS_TENANTS

EXPORT_TO_CUSTOMER

RETAIN_AFTER_PROVIDER_TERMINATION

RETAIN_FOR_AUDIT

RETAIN_DERIVED_RULES_AFTER_TERMINATION
```

The answer MAY differ for every right.

Baobab SHALL reject:

```text
source.is_public = true
therefore
all_use_permitted = true
```

and:

```text
source.is_government = true
therefore
public_domain = true
```

as architectural assumptions.

---

# 2. Governing Doctrine

The governing doctrine is:

> **Access to information is not the same thing as permission to reuse it.**

And:

> **Permission to read is not automatically permission to copy, transform, embed, redistribute, train models on, or commercialise the content.**

And:

> **Permission to derive a regulatory conclusion does not necessarily permit redistribution of the underlying source expression.**

---

# 3. Research Foundation — Internet Availability

WIPO explicitly warns that material available on the Internet is not thereby in the public domain. Copyright-protected material generally remains protected unless a licence, applicable limitation/exception or other legal basis permits the intended use. WIPO also notes that limitations and exceptions differ between jurisdictions.

This validates a fundamental Baobab invariant:

```text
PUBLICLY_ACCESSIBLE
≠
PUBLIC_DOMAIN
≠
OPEN_LICENCE
≠
UNRESTRICTED_REUSE
```

---

# 4. Research Foundation — Government Works Are Jurisdiction-Specific

South Africa's Copyright Act expressly provides copyright protection for eligible works made by or under the direction or control of the State.

Uganda's current Copyright and Neighbouring Rights Act similarly provides that copyright in certain works created under the direction or control of Government or prescribed international bodies may vest in Government or the relevant body.

Therefore:

```text
GOVERNMENT_SOURCE
≠
COPYRIGHT_FREE
```

as a universal rule.

---

# 5. Research Foundation — Open Government Licensing

The UK's Open Government Licence v3.0 illustrates the opposite case: it expressly grants worldwide, royalty-free, perpetual, non-exclusive rights to copy, publish, distribute, transmit, adapt and commercially exploit qualifying information, subject to conditions including attribution and exclusions for specified material and third-party rights.

This demonstrates why Baobab must parse:

```text
licence scope
+
conditions
+
exclusions
```

rather than infer rights from source type.

---

# 6. Research Foundation — Creative Commons

Creative Commons licences vary materially. For example, certain licences allow adaptation and commercial reuse, while `NoDerivatives` licences restrict sharing adapted material and `NonCommercial` variants restrict commercial use.

CC also emphasises that its legal code, rather than a summary/deed, is the legally operative licence layer.

Baobab SHALL therefore model:

```text
licence identifier
+
licence version
+
actual legal terms
```

rather than:

```text
"Creative Commons"
```

as a sufficient rights description.

---

# 7. Research Foundation — AI Use Is Not a Simple Licence Flag

Creative Commons' current guidance acknowledges that copyright treatment of AI training is complex and that the applicability of CC licence conditions depends on whether copyright-restricted acts occur in the particular context.

Therefore Baobab SHALL NOT infer:

```text
OPEN_LICENCE
⇒
ALL_AI_USE_ALLOWED
```

or:

```text
COPYRIGHT_PROTECTED
⇒
ALL_AI_PROCESSING_PROHIBITED
```

without applicable legal/licence analysis.

---

# 8. Research Foundation — Facts versus Expression

WIPO notes that copyright protects expression rather than ideas, procedures, methods of operation or mathematical concepts as such.

This supports Baobab's separation between:

```text
SOURCE EXPRESSION
```

and:

```text
DERIVED FACT /
CANONICAL RELATIONSHIP /
EXECUTABLE REGULATORY RULE
```

but it does **not** mean every derived regulatory dataset is unrestricted. Contractual terms, database rights, confidentiality, jurisdiction-specific copyright law and other rights may still apply.

---

# 9. Fundamental Rights Layers

Baobab SHALL distinguish at least six rights layers:

```text
L1 — LEGAL / STATUTORY RIGHTS

L2 — COPYRIGHT / DATABASE / RELATED RIGHTS

L3 — CONTRACT / PROVIDER LICENCE RIGHTS

L4 — CONFIDENTIALITY / PRIVILEGE / DATA PROTECTION

L5 — TECHNICAL ACCESS RIGHTS

L6 — BAOBAB PRODUCT / DERIVED-DATA RIGHTS
```

No one layer SHALL silently override another.

---

# 10. Technical Access Does Not Establish Legal Rights

Having:

```text
API key
```

means Baobab can technically access a source.

It does not automatically mean Baobab may:

```text
redistribute it
train models on it
retain it forever
expose it to customers.
```

---

# 11. Legal Accessibility Does Not Guarantee Technical Access

Conversely, material may be lawfully reusable but technically difficult to acquire.

Rights and operations remain separate.

---

# 12. RightsProfile

Every production source SHOULD have a governed:

```text
ContentRightsProfile
```

Conceptually:

```text
ContentRightsProfile
├── rights_profile_id
├── source_ref
├── provider_ref?
├── rights_basis
├── governing_jurisdiction?
├── licence_identifier?
├── licence_version?
├── contract_ref?
├── copyright_status
├── database_right_status?
├── permitted_uses[]
├── prohibited_uses[]
├── conditional_uses[]
├── attribution_requirements[]
├── notice_requirements[]
├── share_alike_requirements[]
├── third_party_rights_constraints[]
├── AI_processing_policy
├── retention_policy
├── termination_policy
├── redistribution_policy
├── derived_data_policy
├── verification_state
├── valid_from
├── valid_to?
└── provenance
```

---

# 13. RightsBasis

Possible rights bases include:

```text
PUBLIC_DOMAIN

STATUTORY_PERMISSION

OPEN_LICENCE

GOVERNMENT_OPEN_LICENCE

COMMERCIAL_CONTRACT

API_TERMS

DATA_LICENCE

DIRECT_PERMISSION

CUSTOMER_PERMISSION

INTERNAL_OWNERSHIP

LEGAL_EXCEPTION

MULTIPLE_BASES

UNKNOWN.
```

---

# 14. `UNKNOWN` Is Valid

If Baobab has not established reuse rights:

```text
rights_basis = UNKNOWN
```

SHALL remain valid state.

Unknown SHALL NOT be converted into implied permission.

---

# 15. CopyrightStatus

Conceptually:

```text
PUBLIC_DOMAIN_CONFIRMED

COPYRIGHT_APPLIES

COPYRIGHT_POSSIBLE

GOVERNMENT_COPYRIGHT

THIRD_PARTY_COPYRIGHT

LICENCE_GOVERNS

UNKNOWN
```

Exact terminology may vary by jurisdiction.

---

# 16. No Global Government-Copyright Rule

The implementation SHALL NOT contain:

```python
if source.is_government:
    copyright = False
```

This would be demonstrably unsafe across jurisdictions.

---

# 17. Rights Are Action-Specific

The core model SHALL use:

```text
ContentUsePermission
```

rather than one:

```text
can_use = true.
```

---

# 18. UsePermission

Conceptually:

```text
ContentUsePermission
├── use_type
├── status
├── conditions[]
├── jurisdiction_scope?
├── customer_scope?
├── model/provider_scope?
├── attribution_requirement?
├── retention_limit?
├── legal_basis_refs[]
└── verification_state
```

---

# 19. Permission Status

Possible:

```text
PERMITTED

PERMITTED_WITH_CONDITIONS

PROHIBITED

REQUIRES_SEPARATE_PERMISSION

REQUIRES_LEGAL_REVIEW

UNKNOWN
```

---

# 20. Access Right

`ACCESS` covers lawful access to the source.

This may arise through:

```text
public website

subscription

contract

tenant-provided credentials

government API.
```

---

# 21. Fetch Right

`FETCH` covers automated retrieval.

A website being human-readable SHALL NOT automatically establish permission for:

```text
bulk crawler

high-frequency scraper

automated archival.
```

---

# 22. Download Right

The ability to click:

```text
Download PDF
```

does not necessarily determine downstream commercial reuse rights.

---

# 23. Copy Right

Baobab often needs to make internal copies for:

```text
processing

backup

audit

replication.
```

These rights SHALL be evaluated separately where necessary.

---

# 24. Cache Right

Some provider licences may permit:

```text
short-lived cache
```

while prohibiting:

```text
long-term archive.
```

Baobab must represent this distinction.

---

# 25. Archive Right

`ARCHIVE` is strategically important because regulatory decision replay may require historical source material years later.

A provider that prohibits archival retention may be unsuitable as the sole lineage source for consequential rules.

---

# 26. Backup Right

Permission to operate on content SHOULD include clarity regarding:

```text
backup

DR replicas

encrypted disaster-recovery copies.
```

---

# 27. OCR Right

Docling or another parser may need to create a machine-readable transformation of a scanned source.

That processing can involve reproduction/transformation.

Rights policy SHALL therefore explicitly cover:

```text
OCR
```

where material.

---

# 28. Parsing Right

Likewise:

```text
PDF
    ↓
structured blocks
```

is a transformation activity.

---

# 29. Normalisation Right

Normalisation may produce:

```text
canonical metadata

structured tables

provision hierarchy

cleaned text.
```

Rights policy SHALL distinguish internal transformation from customer redistribution.

---

# 30. Translation Right

Translation may constitute an adaptation/derivative work under relevant copyright law.

Therefore:

```text
TRANSLATE
```

SHALL be a separate rights dimension.

---

# 31. Indexing Right

Full-text search may require internal copies/indexes.

Baobab SHALL determine whether provider terms permit indexing.

---

# 32. Embedding Right

Creating vector embeddings SHALL have its own use-policy state:

```text
CREATE_EMBEDDINGS.
```

---

# 33. Why Embeddings Need Explicit Treatment

Embeddings create a derived machine representation.

Different licences/contracts may treat:

```text
derived vectors

search indexes

feature representations
```

differently.

The architecture SHALL not assume they are always unrestricted.

---

# 34. RAG Right

`USE_FOR_RAG` SHALL mean the source may participate in runtime retrieval for model context.

This is separate from:

```text
MODEL_TRAINING.
```

---

# 35. RAG ≠ Training

Baobab SHALL distinguish:

```text
retrieving content at inference time
```

from:

```text
changing model parameters through training/fine-tuning.
```

---

# 36. External Model Transfer

Baobab SHALL separately control:

```text
SEND_TO_EXTERNAL_MODEL.
```

Even if internal RAG is allowed, licence/confidentiality terms may prohibit transmitting material to:

```text
external LLM API.
```

---

# 37. External Provider Terms

Model-provider terms concerning:

```text
retention
training
subprocessors
region
data handling
```

SHALL be evaluated independently from source-content rights.

---

# 38. AI Processing Matrix

Conceptually:

| Use | Example | Separate right? |
|---|---|---:|
| OCR | image → text | Yes |
| Structured extraction | provision extraction | Yes |
| Embedding | text → vectors | Yes |
| RAG | text supplied as runtime context | Yes |
| Candidate interpretation | LLM interprets provision | Yes |
| Candidate rule extraction | LLM proposes machine rule | Yes |
| Fine-tuning | adjust model weights | Yes |
| Model training | training corpus use | Yes |
| Evaluation | use source in benchmark | Yes |

---

# 39. Default AI Policy

Where rights are unclear:

```text
MODEL_TRAINING = NOT_APPROVED
```

SHOULD be the conservative platform default.

---

# 40. Fine-Tuning

Fine-tuning SHALL be treated separately from generic AI inference.

Commercial or licensed regulatory material SHALL not automatically enter model fine-tuning datasets.

---

# 41. Provider-Native AI Features

A commercial regulatory vendor may permit use through its:

```text
own AI interface
```

without permitting export to a third-party LLM.

These rights SHALL remain separate.

---

# 42. Docling Boundary

Docling's role in Regulations SHOULD be:

```text
source artefact
      ↓
permitted document transformation
      ↓
structured candidate representation
```

The `ContentRightsProfile` SHALL be checked before processing where required.

---

# 43. Haystack Boundary

Haystack may:

```text
index
retrieve
embed
rerank
provide context
orchestrate extraction
```

only within the approved rights policy.

---

# 44. LangGraph Boundary

LangGraph may orchestrate:

```text
review
approval
human verification
```

but SHALL NOT override content rights.

A reviewer clicking:

```text
APPROVE
```

does not manufacture missing copyright permission.

---

# 45. Rights Gate Before AI

Preferred:

```text
Source
   ↓
Rights Evaluation
   ↓
Allowed Processing Profile
   ↓
Docling / Haystack / Model
```

Not:

```text
Source
   ↓
LLM
   ↓
later ask if allowed.
```

---

# 46. Derived Facts

Baobab SHALL distinguish:

```text
source expression
```

from derived facts such as:

```text
effective date

authority identifier

HS code

rate

jurisdiction

rule relationship.
```

---

# 47. Facts May Still Carry Other Restrictions

Even where copyright does not protect bare facts in a particular context, Baobab SHALL still consider:

```text
database rights

contract

confidentiality

access terms

trade secrets

data protection.
```

---

# 48. Derived Regulatory Rule

`DERIVE_EXECUTABLE_RULES` SHALL be an explicit permitted-use category.

---

# 49. Rule Derivation Is Core to Baobab

A source is strategically weak for Regulations if Baobab may:

```text
read it
```

but may not:

```text
derive durable machine-executable regulatory rules.
```

Such a source may still be useful for discovery or review.

---

# 50. Derived Rule Independence

Where law and rights permit, Baobab SHOULD structure derived rules so they encode:

```text
regulatory semantics
```

rather than reproducing unnecessary protected source expression.

---

# 51. Do Not Copy Entire Provisions Into Rules

Preferred:

```text
rule.condition = product_class in X

rule.effect = permit_required
```

rather than embedding:

```text
full source paragraph
```

inside every rule object.

---

# 52. Citation Remains

The derived rule SHALL retain source citations and provenance even when it does not reproduce full source expression.

---

# 53. DerivedDataRight

Baobab SHALL model rights in and restrictions on derived outputs.

Conceptually:

```text
DerivedDataPolicy
├── derivative_type
├── ownership_position
├── source_restrictions[]
├── redistribution_allowed
├── commercial_use_allowed
├── attribution_required
├── share_alike_required
├── provider_dependency
├── termination_effect
└── provenance
```

---

# 54. Derived Output Types

At minimum:

```text
NORMALISED_METADATA

STRUCTURED_PROVISION

CANONICAL_FACT

RELATIONSHIP_EDGE

INTERPRETATION

RULE

EMBEDDING

SEARCH_INDEX

ANALYTIC_METRIC

REGULATORY_DECISION

CUSTOMER_REPORT.
```

---

# 55. Not All Derived Outputs Have Same Rights

A provider may permit:

```text
customer-facing regulatory decision
```

while prohibiting:

```text
redistribution of its raw database.
```

The architecture SHALL preserve this distinction.

---

# 56. Raw Content Redistribution

`REDISTRIBUTE_RAW_CONTENT` is one of the highest-risk rights.

Default:

```text
PROHIBITED
```

unless positively established.

---

# 57. Snippet Display

Short source excerpts may have separate legal/licensing treatment from full-text redistribution.

Therefore:

```text
DISPLAY_SNIPPETS
```

SHALL be separate from:

```text
DISPLAY_FULL_TEXT.
```

---

# 58. Quotation

`QUOTE` SHALL be governed by:

```text
licence
or
applicable statutory limitation/exception
```

and attribution requirements.

WIPO confirms quotation exceptions exist in many regimes but their scope differs by jurisdiction.

---

# 59. Do Not Hard-Code Fair Use

Baobab SHALL NOT contain a global rule:

```text
under N words = fair use.
```

No universal numeric rule exists.

---

# 60. Fair Dealing / Exceptions

Where an exception is relied upon, the rights record SHOULD identify:

```text
jurisdiction
legal basis
purpose
scope
review
```

rather than generically saying:

```text
fair use.
```

---

# 61. Attribution

Sources/licences may require attribution.

Attribution SHALL therefore become machine-readable policy.

---

# 62. AttributionRequirement

Conceptually:

```text
AttributionRequirement
├── required
├── prescribed_text?
├── provider_name?
├── source_name?
├── licence_notice?
├── link_required?
├── placement_requirements?
└── version
```

---

# 63. OGL Example

The UK OGL expressly requires acknowledgement of the information provider/source and provides default attribution language where none is supplied.

Baobab SHOULD be capable of generating such notices automatically.

---

# 64. Attribution Propagation

Attribution obligations may need to flow into:

```text
customer report

API response

downloaded evidence bundle

public web page.
```

---

# 65. Share-Alike

Some licences may require downstream adaptations to remain under compatible terms.

Therefore:

```text
SHARE_ALIKE
```

SHALL be explicit.

---

# 66. NoDerivatives

A `NoDerivatives` licence may materially limit:

```text
translation

adaptation

redistribution of transformed content.
```

Creative Commons expressly distinguishes these licence conditions.

---

# 67. NonCommercial

A `NonCommercial` condition is generally incompatible with unrestricted use in Baobab's paid commercial products unless a separate legal basis exists.

The system SHALL flag this.

---

# 68. No Endorsement

Open government licences may prohibit implying official endorsement.

The UK OGL expressly contains a non-endorsement condition.

Baobab SHALL therefore avoid user-facing language such as:

```text
"Government-approved by virtue of source use"
```

unless independently true.

---

# 69. Third-Party Rights

Government publications may contain:

```text
third-party photographs

standards

maps

logos

commercial tables

licensed datasets.
```

A broad government reuse licence may exclude such material.

The UK OGL explicitly excludes third-party rights not owned/licensable by the provider.

---

# 70. Rights at Sub-Document Level

A single artefact MAY therefore contain several rights zones.

---

# 71. ContentSegmentRights

Conceptually:

```text
ContentSegmentRights
├── artefact_ref
├── locator
├── rights_profile_ref
├── owner_ref?
└── exclusions[]
```

---

# 72. Example

```text
Government Gazette PDF
├── statutory notice → government rights policy
├── third-party standard extract → separate rights
└── government logo → trademark restrictions.
```

---

# 73. Standards Organisations

Privately produced standards incorporated into law may carry separate copyright/licensing restrictions.

Baobab SHALL NOT assume:

```text
incorporated by reference
⇒
free to redistribute.
```

---

# 74. Legal Incorporation Does Not Erase IP Rights

Legal applicability and content reuse rights SHALL remain separate.

---

# 75. Commercial Database Rights

Commercial regulatory datasets may contain additional contractual or database-related restrictions beyond individual document copyright.

`ContentRightsProfile` SHALL support this explicitly.

---

# 76. Database Extraction

The architecture SHALL distinguish:

```text
individual factual lookup
```

from:

```text
systematic extraction of substantial dataset.
```

The exact legal significance varies by jurisdiction and contract.

---

# 77. Bulk Export

`BULK_EXPORT` SHOULD be an explicit use permission if commercial providers are involved.

---

# 78. Bulk Replication

Baobab SHALL NOT accidentally reproduce an entire licensed regulatory database into its own canonical store beyond permitted rights.

---

# 79. Anti-Corruption Layer

ADR-REG-0005's provider anti-corruption layer SHALL map provider data into Baobab canonical concepts while respecting rights.

It is not a mechanism for rights laundering.

---

# 80. Rights Laundering Is Prohibited

Rejected:

```text
licensed proprietary record
    ↓
rename fields
    ↓
"Baobab-owned data"
```

Canonical transformation does not automatically extinguish upstream rights.

---

# 81. Provenance Prevents Rights Laundering

Every derived object SHALL retain enough upstream lineage to evaluate continuing rights obligations.

---

# 82. Multi-Source Derivation

A RuleVersion MAY derive from:

```text
official legislation
+
commercial structured annotation
+
Baobab interpretation.
```

Its rights profile must account for each material dependency.

---

# 83. Rights Dependency Graph

ADR-REG-0010 SHALL support:

```text
Derived Object
      │
      ▼
DEPENDS_ON_CONTENT
      │
      ▼
Source / Provider
```

---

# 84. Rights Blast Radius

If a licence expires, Baobab SHALL determine:

```text
which artefacts
which indexes
which embeddings
which interpretations
which rules
which customer products
```

depend upon it.

---

# 85. Termination Must Not Be an Emergency Archaeology Project

Every commercial source SHALL have a documented provider-exit policy before production dependency is accepted.

---

# 86. TerminationPolicy

Conceptually:

```text
SourceTerminationPolicy
├── raw_content_retention
├── archive_retention
├── backup_retention
├── index_retention
├── embedding_retention
├── derived_fact_retention
├── interpretation_retention
├── rule_retention
├── audit_retention
├── customer_output_retention
├── deletion_deadline
├── certification_requirement?
└── exit_export_rights
```

---

# 87. Post-Termination Question

For each licensed source Baobab SHALL know:

> What remains legally usable the day after the contract ends?

---

# 88. Raw Source May Need Deletion

A provider contract may require:

```text
delete provider content
after termination.
```

---

# 89. Derived Rules May or May Not Survive

Whether Baobab may retain:

```text
derived rules
```

after provider termination SHALL be established contractually/legal-review-wise.

It SHALL never be assumed.

---

# 90. Rule Survivability Is Commercially Critical

A provider whose termination causes:

```text
all derived executable rules to become unusable
```

creates severe vendor lock-in.

This SHALL affect procurement.

---

# 91. Provider Exit Scorecard

Procurement SHOULD assess:

```text
raw-data portability

historical archive rights

derived-rule survivability

embedding survivability

audit retention rights

customer-continuity rights.
```

---

# 92. Provider-Neutrality Requires Rights Neutrality

Technical adapter replaceability is insufficient if licence terms make the derived knowledge impossible to retain.

---

# 93. Preferred Commercial Source Terms

Where possible Baobab SHOULD negotiate:

```text
durable derived-data rights

durable rule/model rights

historical audit retention

reasonable transition period

export rights

provider replacement rights.
```

---

# 94. Immutable Audit Requirement

Consequential regulatory decisions may need evidence years later.

Baobab SHOULD avoid source arrangements that make historical decision defence impossible after termination.

---

# 95. Audit Exception

If raw content must be deleted but limited retention for:

```text
legal defence

audit

regulatory compliance
```

is contractually permitted, that scope SHALL be represented explicitly.

---

# 96. Legal Hold

A source may become subject to:

```text
legal hold
```

overriding normal deletion schedules where legally appropriate.

Detailed records policy is deferred.

---

# 97. Retention Categories

Baobab SHOULD distinguish:

```text
OPERATIONAL_CACHE

ACTIVE_SOURCE_COPY

HISTORICAL_ARCHIVE

AUDIT_EVIDENCE

BACKUP_COPY

DERIVED_REPRESENTATION.
```

---

# 98. Cache TTL

Rights may specify:

```text
maximum cache duration.
```

This SHALL be enforceable.

---

# 99. Backup Deletion

Where contract requires deletion, backup-deletion behaviour and practical restore handling SHALL be documented.

---

# 100. Object Storage Policy

Immutable source storage SHALL not become an uncontrolled permanent archive.

Each artefact SHALL reference a retention policy.

---

# 101. Customer-Supplied Content

Tenants may provide:

```text
legal opinions

contracts

regulatory correspondence

subscriptions

private guidance.
```

These SHALL carry separate customer rights.

---

# 102. Customer Licence to Baobab

Baobab SHALL establish whether customer terms permit:

```text
processing

storage

AI use

derived rule generation

cross-tenant reuse.
```

---

# 103. Default Tenant Isolation

Tenant-supplied proprietary material SHALL default to:

```text
NO_CROSS_TENANT_REUSE.
```

---

# 104. No Training by Default

Tenant-private regulatory materials SHALL not automatically enter:

```text
shared model training

shared embeddings corpus

platform-wide examples.
```

---

# 105. Privileged Counsel Material

Attorney/client counsel material may require heightened restrictions.

Default:

```text
tenant private
restricted retrieval
no model training
no cross-tenant derivation.
```

---

# 106. Derived Tenant Rule

A tenant counsel opinion MAY create:

```text
tenant-scoped RuleVersion
```

without authorising platform-wide reuse.

---

# 107. Government Data as Shared Layer

Where rights permit, public regulatory materials SHOULD be stored once in the shared regulatory layer.

---

# 108. Licensed Data May Need Entitlement Filtering

A commercial source may be available only to subscribed customers or internal functions.

Graph traversal SHALL enforce this.

---

# 109. Rights Are Not Entitlements

Separate:

```text
Baobab has legal right to use Content X
```

from:

```text
Tenant A purchased access to Product Y.
```

---

# 110. Product Entitlement

A customer may not be entitled to view the raw source even where Baobab itself is licensed to use it for derived decisions.

---

# 111. Output Licensing

Every outward-facing API response SHOULD consider whether it contains:

```text
Baobab-owned result

public legal citation

licensed snippet

raw provider data.
```

---

# 112. API Contract Types

Potential output modes:

```text
DECISION_ONLY

DECISION_PLUS_CITATION

DECISION_PLUS_SNIPPET

FULL_EVIDENCE_BUNDLE

RAW_SOURCE_EXPORT.
```

Each may have different rights gates.

---

# 113. Decision-Only Output

Preferred commercial design where source licensing is restrictive:

```text
customer receives decision
+
Baobab explanation
+
official citation
```

without provider's proprietary annotation.

---

# 114. Citation Link-Out

Where redistribution is restricted, Baobab MAY link the customer to the original official source rather than republishing source text.

---

# 115. Customer Download

Download rights SHALL be separately evaluated.

Web display permission does not automatically mean:

```text
customer may download archive.
```

---

# 116. Evidence Bundle

Audit bundles SHALL include only content Baobab is entitled to redistribute.

Restricted evidence may instead be represented by:

```text
hash
citation
source identifier
retrieval metadata.
```

---

# 117. Rights-Aware Explainability

The explanation layer SHALL distinguish:

```text
what Baobab may explain
```

from:

```text
what source material it may reproduce.
```

---

# 118. AI Narrative

Generative explanations SHALL avoid reproducing excessive protected source text when not permitted.

---

# 119. Quote Budgeting

For sources with restrictive quotation rights, Baobab MAY enforce:

```text
snippet limits
```

as platform policy.

These limits SHALL derive from the actual legal/licence basis, not invented universal thresholds.

---

# 120. Search Index

Full-text search over restricted content MAY be:

```text
internal-only.
```

The customer-facing result may show:

```text
metadata + permitted snippet.
```

---

# 121. Embedding Isolation

Embeddings derived from tenant-private or specially licensed content SHOULD be stored in separate logical namespaces where required.

---

# 122. Rights-Scoped Retrieval

Haystack retrieval SHALL filter by:

```text
tenant

licence entitlement

purpose

rights policy.
```

---

# 123. Rights Metadata Must Travel With Documents

A Haystack/Docling document SHALL carry at least a reference to:

```text
rights_profile_id.
```

---

# 124. Rights Metadata Cannot Be Lost During Chunking

When a source is split into chunks:

```text
rights constraints
```

SHALL propagate.

---

# 125. Chunk Rights

A chunk does not become unrestricted because its parent document was split.

---

# 126. Embedding Provenance

An embedding SHOULD retain:

```text
source_ref
rights_profile_ref
model_ref
created_at
```

where needed for deletion and provider exit.

---

# 127. Vector Deletion

If source rights are revoked/expire and embeddings may not be retained:

```text
embedding deletion
```

SHALL be possible.

---

# 128. Index Deletion

The same applies to:

```text
search index records.
```

---

# 129. Derived Rule Revalidation

When source rights change, Baobab SHALL determine whether dependent rules remain legally usable.

---

# 130. Rights Change Is Not Legal Change

A licence ending does not mean:

```text
regulation repealed.
```

It means:

```text
Baobab's permissible use path changed.
```

---

# 131. Alternative Source Substitution

Provider neutrality SHOULD allow:

```text
Commercial Source A unavailable
      ↓
Official Source B
      ↓
Rule provenance rebased / verified
```

without changing underlying legal semantics.

---

# 132. Provenance Rebase

A derived rule may gain a new permissible source path.

The historical original derivation remains recorded.

---

# 133. Rights Risk Classification

Sources MAY be operationally classified:

```text
R0 — unrestricted/open

R1 — attribution/notice

R2 — limited transformation/display

R3 — commercial contractual restrictions

R4 — highly restricted/confidential/privileged
```

This SHALL be a workflow convenience only.

It SHALL NOT replace the full rights matrix.

---

# 134. No Universal Rights Score

Just as ADR-REG-0011 rejects one trust score, this ADR rejects:

```text
rights_score = 80.
```

---

# 135. Rights Assessment

Conceptually:

```text
ContentRightsAssessment
├── source_ref
├── intended_use
├── tenant_ref?
├── product_ref?
├── processing_provider?
├── jurisdiction?
├── applicable_rights_profiles[]
├── outcome
├── conditions[]
├── required_attributions[]
├── required_controls[]
├── legal_review_required
└── evaluated_at
```

---

# 136. Assessment Outcomes

```text
PERMITTED

PERMITTED_WITH_CONDITIONS

NOT_PERMITTED

LEGAL_REVIEW_REQUIRED

INDETERMINATE
```

---

# 137. Rights Policy Engine

Rights assessment SHOULD be deterministic where licence terms have been structured.

---

# 138. Legal Interpretation Still Possible

Complex rights questions MAY require legal review.

The platform SHALL not fabricate permission.

---

# 139. Rights Policy Is Separate from Regulatory Rule Engine

Do not merge:

```text
rights to use regulatory content
```

with:

```text
regulatory rules affecting customer transactions.
```

They are distinct bounded concerns inside Regulations.

---

# 140. Content Governance Domain

A practical internal component:

```text
Regulatory Content Governance
```

MAY own:

```text
source rights

licence metadata

use policies

attribution

retention

provider exit.
```

---

# 141. Acquisition Gate

Before activating a source adapter:

```text
Source Registry
    ↓
Rights Assessment
    ↓
Approved Acquisition Policy
    ↓
Adapter Enabled
```

---

# 142. Unknown Rights

Sources with unknown rights MAY be used for limited:

```text
discovery
```

where legally appropriate.

They SHALL not automatically be ingested into production content stores.

---

# 143. Robots.txt

`robots.txt` is a technical crawling signal.

It SHALL not be treated as complete copyright/licensing permission or prohibition.

---

# 144. Website Terms

Website terms may impose contractual conditions independent of copyright.

These SHALL be captured where relevant.

---

# 145. API Terms

API contracts often govern:

```text
rate limits
storage
caching
redistribution
derived products
termination.
```

The Registry SHALL capture these.

---

# 146. Contract Documents

Commercial licence contracts SHOULD be referenced through secure contract identifiers rather than duplicated into general source metadata.

---

# 147. Contract Confidentiality

Provider contracts themselves may be confidential.

Rights policy can expose:

```text
derived machine-readable permissions
```

without exposing the contract document broadly.

---

# 148. Legal Review Record

Where counsel interprets contractual rights:

```text
RightsInterpretation
```

SHOULD be versioned and attributable.

---

# 149. Contract Amendment

Provider terms can change independently from regulatory law.

Rights profiles SHALL be temporally versioned.

---

# 150. Terms-at-Acquisition

Baobab SHOULD preserve, where practical:

```text
which licence / contract version
governed an artefact when acquired.
```

---

# 151. Licence URL Is Not Enough

A URL may later change.

The governing licence identifier/version or snapshot SHOULD be preserved.

---

# 152. Open Licence Versioning

Example:

```text
CC BY 4.0
```

and:

```text
CC BY 3.0
```

are not interchangeable labels.

---

# 153. Licence Compatibility

Combining sources may create downstream compatibility constraints.

---

# 154. Share-Alike Composition

If source-derived material triggers share-alike obligations, Baobab SHALL identify whether the combined output can be commercialised under intended terms.

---

# 155. NoDerivatives Composition

A source with `NoDerivatives` restrictions may still permit verbatim redistribution under specified conditions but constrain transformed external publication.

---

# 156. Open Government Licensing Is Not Universal

The UK's OGL is an example, not a global rule.

Baobab SHALL not infer similar rights for Uganda, South Africa or other jurisdictions without evidence.

---

# 157. Uganda Rights Review

The current Ugandan copyright framework expressly contemplates Government ownership of certain works, so Baobab SHALL establish rights source-by-source rather than assuming official publication is unrestricted.

---

# 158. South Africa Rights Review

South African law likewise expressly recognises State copyright in eligible works made under State direction/control.

Therefore the initial South African jurisdiction pack SHALL include a specific rights review for:

```text
Gazette material
SARS material
ITAC material
departmental publications
datasets.
```

---

# 159. Source Authority ≠ Reuse Authority

A source may be:

```text
perfect authoritative law
```

while:

```text
reuse rights remain restrictive.
```

This distinction is mandatory.

---

# 160. Reuse Rights ≠ Legal Authority

Conversely, a CC BY blog may be freely reusable while possessing no legal authority.

---

# 161. Rights and Source Trust Are Orthogonal

Conceptually:

```text
                 High Legal Authority
                        ▲
                        │
 restrictive rights    │    permissive rights
                        │
────────────────────────┼────────────────────────▶
                        │
                        │
                 Low Legal Authority
```

Sources can exist anywhere on this matrix.

---

# 162. Rights-Aware Source Selection

Where several equivalent sources exist, Regulations SHOULD prefer sources offering:

```text
strong authority
+
sufficient rights
+
stable access
+
good structure.
```

---

# 163. Rights Can Influence Provider Routing

Example:

```text
Provider A:
better structure
but no customer redistribution

Provider B:
slightly weaker structure
but broader rights
```

Different tasks may route differently.

---

# 164. Do Not Let Licensing Change Law

A more permissively licensed source does not become legally superior.

Source authority remains governed by ADR-REG-0011.

---

# 165. Source Composition Strategy

Preferred architecture:

```text
Authoritative source
       +
Permissible structured source
       +
Baobab canonical interpretation
       ↓
Regulatory capability.
```

---

# 166. Dual-Source Rights Strategy

For strategically important rules, Baobab MAY deliberately maintain:

```text
authoritative citation source
+
replaceable structured-data source
```

to reduce commercial-provider lock-in.

---

# 167. Rule Provenance Independence

The regulatory rule SHOULD point directly to authoritative legal provisions even when a commercial provider helped extract/normalise them.

---

# 168. Provider Contribution Provenance

Do not erase the provider's contribution.

Record:

```text
commercial provider assisted extraction
```

where material to rights/governance.

---

# 169. AI Output Ownership

Ownership/use rights in AI-generated output may depend on:

```text
provider terms
input rights
jurisdiction
human contribution.
```

Baobab SHALL not make sweeping universal assumptions.

---

# 170. Canonical Rule Is Baobab Domain State

A verified Baobab rule becomes canonical domain state only when its rights lineage supports the intended use.

---

# 171. AI Model Terms Registry

The platform SHOULD eventually maintain:

```text
AIProviderDataPolicy
```

covering:

```text
input retention

training use

output rights

subprocessors

region

confidentiality.
```

---

# 172. Restricted Sources and External LLMs

A source MAY permit:

```text
internal deterministic processing
```

while prohibiting:

```text
submission to external AI service.
```

Haystack SHALL obey that constraint.

---

# 173. Local Models

Where licensing/confidentiality prevents external transfer, Baobab MAY route processing to:

```text
approved local/self-hosted model.
```

This is an operational consequence of provider neutrality.

---

# 174. Model Routing by Rights

Future:

```text
ContentRightsProfile
        ↓
AI Routing Policy
        ↓
External LLM / Private LLM / No LLM
```

---

# 175. Rights-Driven Degradation

If external model use is prohibited:

```text
AI enrichment unavailable
```

does not mean:

```text
source unusable.
```

Docling/local deterministic processing may continue.

---

# 176. AI Training Corpus

No regulatory source SHALL enter shared model training/fine-tuning without an explicit:

```text
TRAINING_APPROVED
```

policy.

---

# 177. Evaluation Corpus

Using material for:

```text
golden test cases
```

also requires rights consideration.

---

# 178. Synthetic Fixtures

Where source redistribution is restricted, Baobab SHOULD create:

```text
synthetic / abstracted test fixtures
```

when appropriate rather than putting licensed text into public repositories.

---

# 179. GitHub Repository Safety

Licensed or restricted regulatory content SHALL NOT be committed to public or broadly accessible Git repositories.

---

# 180. Fixtures Classification

Test fixtures SHOULD be classified:

```text
PUBLIC

INTERNAL

LICENSED

TENANT_PRIVATE

SYNTHETIC.
```

---

# 181. CI Safety

CI logs SHALL not print:

```text
licensed source text

privileged counsel content

restricted API payloads.
```

---

# 182. Observability Safety

Telemetry SHALL use:

```text
IDs
hashes
counts
status
```

rather than full protected content where not required.

---

# 183. Logging

Logging source text SHALL default to:

```text
disabled.
```

---

# 184. Prompt Logging

AI prompt/response logging involving restricted material SHALL obey rights/privacy policy.

---

# 185. Model Observability

Operational tracing should retain:

```text
source IDs

chunk IDs

model IDs

rights policy decision
```

without necessarily retaining full prompt text.

---

# 186. Data Residency

Content licences may include territorial hosting restrictions.

These SHALL integrate with Baobab isolation/residency architecture.

---

# 187. Territorial Licence

A source may be licensed for:

```text
South Africa only

specified corporate group

specific users.
```

The rights engine SHALL support scoped use.

---

# 188. User Seat Limits

Some providers license content per user/seat.

Baobab SHALL distinguish:

```text
machine processing rights
```

from:

```text
named human user access.
```

---

# 189. API-Based Provider Restrictions

A provider might require all end-user exposure through its own API.

Baobab SHALL not bypass such terms by copying data into PostgreSQL if prohibited.

---

# 190. Customer-Bring-Your-Own-Licence

Baobab MAY support:

```text
BYOL regulatory provider
```

where a tenant brings its own commercial data subscription.

---

# 191. BYOL Isolation

BYOL content SHALL default to tenant-private source scope unless provider terms allow wider use.

---

# 192. Platform Licence versus Tenant Licence

Separate:

```text
BAOBAB_PLATFORM_LICENSE
```

from:

```text
TENANT_OWNED_LICENSE.
```

---

# 193. Expired Tenant Licence

When tenant subscription ends:

```text
access to provider content
```

may stop while legally survivable historical decisions remain.

---

# 194. Customer Export

A tenant leaving Baobab may be entitled to:

```text
its own data
decisions
audit history
```

without being entitled to:

```text
Baobab licensed source corpus.
```

---

# 195. Portability Bundle

Customer exit export SHOULD distinguish:

```text
CUSTOMER_OWNED

BAOBAB_DERIVED

THIRD_PARTY_RESTRICTED.
```

---

# 196. Raw Content Exclusion

Third-party restricted raw content may need to be omitted from export and replaced with citations/references.

---

# 197. Provider Portability

Baobab itself should be able to change source providers without rewriting customer-facing canonical contracts.

---

# 198. Rights Reconciliation

A scheduled reconciliation SHOULD identify:

```text
expired licences

unknown rights

source artefacts beyond retention

orphan embeddings

restricted content in wrong index

derived rules with terminated dependencies.
```

---

# 199. Licence Expiry Watch

Commercial licences SHOULD generate future-dated operational alerts before expiry.

---

# 200. Rights Incident

Examples:

```text
unauthorised raw redistribution

content sent to prohibited external model

expired licence still serving data

tenant-private source indexed globally.
```

These SHALL be treated as security/compliance incidents.

---

# 201. Rights Revocation

Where a licence/provider revokes rights:

```text
rights.revoked
```

SHOULD trigger impact analysis.

---

# 202. Rights Event Model

Potential events:

```text
regulation.source.rights.approved

regulation.source.rights.changed

regulation.source.rights.expiring

regulation.source.rights.expired

regulation.source.rights.revoked

regulation.source.retention.required

regulation.source.deletion.required
```

Final contracts belong in Shared.

---

# 203. Rights Enforcement at Runtime

Customer-facing content retrieval SHOULD evaluate:

```text
principal
tenant
entitlement
purpose
rights profile
source classification.
```

---

# 204. Enforcement Point

The content delivery layer SHALL be an enforcement point for rights policy.

---

# 205. Rule Evaluation Does Not Need Raw Source Exposure

A deterministic regulatory decision may rely on a verified RuleVersion without transmitting licensed source content to the caller.

This helps separate:

```text
knowledge use
```

from:

```text
content redistribution.
```

---

# 206. Commercial Architecture Benefit

This separation permits Baobab to monetise:

```text
regulatory decisions
```

rather than becoming dependent on reselling source documents.

---

# 207. Build Intellectual Property Around Semantics

Baobab's strategic IP SHOULD increasingly reside in:

```text
canonical relationships

verified interpretations

rule models

applicability

decision logic

workflow integration.
```

Not in copying source text.

---

# 208. But Do Not Assume Derived IP Automatically Belongs to Baobab

Upstream contract terms must support that outcome.

---

# 209. Procurement Gate

No commercial regulatory provider SHOULD become production-critical until Baobab has reviewed:

```text
access rights

machine processing

storage

cache

embedding

RAG

AI transfer

derived data

rule derivation

customer output

redistribution

audit retention

termination

portability.
```

---

# 210. Procurement Anti-Pattern

Rejected contract:

```text
"You may use our API during subscription."
```

with no clarity on:

```text
derived rules
historical decisions
post-termination retention.
```

---

# 211. Commercial Negotiation Priority

For Baobab Regulations, the most strategically important provider right may not be:

```text
raw redistribution.
```

It may be:

```text
durable derived regulatory semantics.
```

---

# 212. Provider Lock-In Analysis

A provider is high-lock-in if:

```text
raw content cannot be exported

derived rules must be deleted

historical audit copies cannot be retained

provider IDs become canonical

customer outputs require provider runtime.
```

---

# 213. Prefer Low-Lock-In Providers

Where content quality is comparable, provider selection SHOULD prefer:

```text
portable lineage
durable derived rights
transparent sources
replaceable identifiers.
```

---

# 214. Open Data Sources

Openly licensed public-sector data can substantially lower source costs.

The EU Open Data Directive demonstrates a policy framework specifically encouraging reuse of public-sector information, including legal information, but that is a jurisdiction-specific regime rather than a universal global rule.

---

# 215. Open Data Still Has Conditions

Even permissive open-government licences can impose:

```text
attribution

non-endorsement

third-party exclusions.
```


---

# 216. Public Domain

Where content is genuinely public domain:

```text
reuse may be broad
```

but Baobab SHALL retain provenance/citation anyway.

Public domain status is a rights conclusion, not merely "old/publicly available." WIPO describes public domain as material whose relevant economic rights no longer have a right owner, such as where protection has expired.

---

# 217. CC0

Where a rights holder validly applies CC0, it seeks to waive copyright/database rights to the extent possible.

Baobab SHALL still preserve:

```text
source
authority
provenance
```

because rights openness does not establish regulatory authority.

---

# 218. Trademarks

Copyright permission does not automatically grant:

```text
logo

trademark

official emblem
```

rights.

The OGL itself illustrates this by excluding certain logos, crests and other IP rights.

---

# 219. Branding

Baobab SHALL avoid incorporating authority logos into customer outputs unless authorised.

---

# 220. Personal Data

Open-source/content licences do not override privacy/data-protection obligations.

---

# 221. OGL Example

The UK OGL explicitly excludes personal data from its licence scope.

Baobab SHOULD reflect such exclusions.

---

# 222. Court Decisions

Court documents may contain personal information even where legally published.

Content-rights and privacy policies SHALL both apply.

---

# 223. Confidential Regulatory Correspondence

Tenant-provided regulator correspondence may be:

```text
legally significant
+
confidential.
```

Its use policy SHALL reflect both.

---

# 224. Data Minimisation

Only the content necessary for:

```text
rule derivation
evidence
decision
```

SHOULD be carried into derived layers.

---

# 225. Source Text in Embeddings

Where a source may not be retained after expiry, embeddings derived from the source may also require deletion depending on the applicable licence/legal interpretation.

The platform SHALL be able to locate them.

---

# 226. Provenance-to-Embedding

Therefore:

```text
Embedding
    DERIVED_FROM
Chunk
    DERIVED_FROM
Artefact
```

is required.

---

# 227. Rights-Aware Graph

ADR-REG-0010's graph SHALL support:

```text
USES_CONTENT_FROM

DERIVED_FROM

SUBJECT_TO_RIGHTS_PROFILE.
```

---

# 228. Rights-Aware Blast Radius

Example:

```text
Commercial licence expires
          │
          ▼
Source S
          │
          ├── 12 artefacts
          ├── 1,200 chunks
          ├── 1,200 embeddings
          ├── 78 interpretations
          └── 44 rules
```

The platform must know which objects:

```text
delete
retain
re-source
reverify.
```

---

# 229. Re-Sourcing

A rule whose original commercial source can no longer be used MAY be re-sourced against:

```text
official publication
```

if independently verified.

---

# 230. Re-Sourcing Does Not Rewrite History

Historical provenance remains:

```text
original source
```

while the active RuleVersion gains a new valid source lineage.

---

# 231. Rights and Historical Replay

Replay may require the historical content.

If retention rights do not permit this, the rule's replay assurance SHALL reflect the limitation.

---

# 232. Rights Deficiency Can Cap Decision SLA

Baobab SHALL not sell:

```text
10-year reproducibility
```

for a source whose licence allows only 30-day caching.

---

# 233. Commercial SLA Must Reflect Rights

`ADR-REG-0030` SHALL incorporate rights constraints into product commitments.

---

# 234. Source Cost Attribution

Commercial source usage SHOULD be attributable to:

```text
regulatory domain
tenant
capability
decision volume
```

where licensing permits/needs metering.

---

# 235. Usage Caps

Some licences may impose:

```text
API calls

documents

users

transactions.
```

The system SHALL monitor these.

---

# 236. Source Billing Failure

Provider billing/licence exhaustion SHALL not silently produce:

```text
ALLOW.
```

Affected regulatory capabilities should degrade safely.

---

# 237. Rights Failure State

Potential:

```text
SOURCE_RIGHTS_UNAVAILABLE
```

shall remain distinct from:

```text
SOURCE_UNAVAILABLE.
```

---

# 238. Safe Degradation

If a required licensed source becomes legally unavailable:

```text
use verified alternative
```

or:

```text
REVIEW_REQUIRED / INDETERMINATE.
```

---

# 239. No Silent Licence Circumvention

Baobab SHALL NOT automatically scrape a public website to bypass a terminated commercial source agreement where this would violate applicable terms/law.

---

# 240. Discovery from One Source, Verification from Another

Permissible architecture:

```text
Commercial alert
       ↓
change discovered
       ↓
official Gazette located
       ↓
rule verified.
```

This reduces dependence on redistributing commercial content.

---

# 241. Rights and Provider Neutrality

This should become the preferred pattern where possible:

```text
provider helps us find
+
authority lets us prove.
```

---

# 242. Technology Independence

The rights layer SHALL not depend on:

```text
Docling

Haystack

LangGraph

specific vector store

specific LLM.
```

Those technologies are consumers of rights decisions.

---

# 243. RightsContract

A generic internal contract MAY resemble:

```text
evaluate_use(
    source_ref,
    use_type,
    tenant_ref,
    processing_provider_ref,
    purpose
) -> RightsDecision
```

---

# 244. RightsDecision

Conceptually:

```text
RightsDecision
├── outcome
├── rights_profile_version
├── permitted_use
├── conditions[]
├── required_attribution[]
├── retention_limit?
├── external_transfer_allowed
├── tenant_scope
├── reason_codes[]
└── evaluated_at
```

---

# 245. Rights Reason Codes

Examples:

```text
OPEN_LICENCE_PERMITS_USE

CONTRACT_PERMITS_INTERNAL_PROCESSING

COMMERCIAL_REUSE_PROHIBITED

EXTERNAL_MODEL_TRANSFER_PROHIBITED

ATTRIBUTION_REQUIRED

NO_DERIVATIVES

NONCOMMERCIAL_ONLY

RIGHTS_UNKNOWN

THIRD_PARTY_RIGHTS_PRESENT

RETENTION_LIMIT_APPLIES.
```

---

# 246. Enforcement in Source Pipeline

```text
Acquire
   ↓
RightsDecision(ACQUIRE)
   ↓
Store
   ↓
RightsDecision(PROCESS)
   ↓
Docling
   ↓
RightsDecision(INDEX/EMBED)
   ↓
Haystack
   ↓
RightsDecision(EXTERNAL_AI?)
   ↓
Model
```

---

# 247. Enforcement on Output

```text
Decision requested
     ↓
Content required
     ↓
RightsDecision(DISPLAY)
     ↓
safe projection
```

---

# 248. Policy Fail Closed

For restricted content use:

```text
UNKNOWN
```

SHALL NOT become:

```text
PERMITTED.
```

---

# 249. Discovery Exception

A limited metadata-only discovery path MAY exist where lawful.

That exception SHALL be explicit.

---

# 250. Rights Verification State

Possible:

```text
UNREVIEWED

MACHINE_CLASSIFIED

HUMAN_REVIEWED

LEGAL_REVIEWED

CONTRACT_VERIFIED

EXPIRED

DISPUTED.
```

---

# 251. Legal Review Is Not Permanent

A rights opinion may need reconsideration after:

```text
law change

licence change

new use case

new model provider.
```

---

# 252. New Use Requires Reassessment

Source approved for:

```text
RAG
```

is not automatically approved for:

```text
fine-tuning.
```

---

# 253. New Product Requires Reassessment

Internal use approval does not automatically authorise:

```text
public customer redistribution.
```

---

# 254. New Geography

A rights conclusion may differ by jurisdiction.

Global deployment MAY require jurisdiction-specific rights analysis.

---

# 255. RightsPolicyVersion

Every material rights decision SHOULD retain:

```text
rights_policy_version.
```

---

# 256. Historical Rights Audit

Baobab SHOULD be able to answer:

> Why was this source use considered permitted on 3 March 2027?

---

# 257. Rights Snapshot

Consequential processing MAY persist a compact:

```text
RightsDecision snapshot
```

rather than re-evaluating old decisions under today's policy.

---

# 258. Licence Breach Prevention

Preventive controls SHOULD be preferred over retrospective discovery.

---

# 259. Deletion Jobs

Rights-driven deletion SHALL be:

```text
auditable

idempotent

bounded

reconcilable.
```

---

# 260. Deletion Receipt

A commercial licence may require proof of deletion.

Baobab SHOULD support:

```text
DeletionReceipt
```

where appropriate.

---

# 261. Derived-Object Reconciliation

Deletion of raw source SHOULD not accidentally delete legally retainable:

```text
Baobab decision history.
```

Object policies SHALL be evaluated individually.

---

# 262. No Cascading Delete by Convenience

Rejected:

```sql
DELETE source
CASCADE;
```

for rights termination across all derived regulatory state.

---

# 263. Quarantine

Content whose rights become disputed SHOULD support:

```text
QUARANTINED
```

state.

---

# 264. Quarantine Effects

Quarantined content:

```text
not available for new rule generation
not exposed externally
```

while historical preservation may remain subject to policy.

---

# 265. Public Repository Hygiene

The `baobab-regulations` repository SHALL contain:

```text
schemas
synthetic fixtures
public-domain/open fixtures
```

rather than proprietary regulatory corpora unless explicitly approved.

---

# 266. Documentation Citations

ADR documentation MAY cite provider/legal materials according to applicable quotation/linking rules.

It SHALL not reproduce excessive proprietary content.

---

# 267. Developer Tooling

Developer tooling SHOULD surface rights metadata visibly.

Example:

```text
Source: provider_x
Rights: internal processing only
External LLM: prohibited
Redistribution: prohibited
Retention: 90 days
```

---

# 268. Prevent Developer Guesswork

A developer SHALL NOT have to infer rights from:

```text
folder name

provider name

URL.
```

---

# 269. Content Labels

Processed documents SHOULD carry labels such as:

```text
PUBLIC_OPEN

PUBLIC_RESTRICTED

COMMERCIAL_LICENSED

TENANT_PRIVATE

LEGAL_PRIVILEGED.
```

These are operational classifications, not substitutes for detailed rights.

---

# 270. Model Provider Isolation

Restricted content MAY require a dedicated:

```text
no-retention / enterprise API configuration
```

or local model, depending on contractual terms.

---

# 271. Haystack Connector Rules

Haystack components SHALL be selected/configured with rights policy in mind.

A generic generator component SHALL not automatically receive every retrieved document.

---

# 272. Rights-Aware Router

A future component:

```text
BaobabRightsAwareModelRouter
```

MAY determine:

```text
external model
private model
deterministic only
```

per source.

---

# 273. Docling Local Processing Advantage

Local/self-hosted Docling processing can reduce external-content transfer risk for sensitive/licensed documents.

---

# 274. LangGraph Governance Advantage

LangGraph can orchestrate rights review workflows such as:

```text
new source
  ↓
rights extraction
  ↓
human review
  ↓
legal review if required
  ↓
approved use matrix.
```

---

# 275. AI Extraction of Licence Terms

AI MAY extract candidate contractual permissions.

It SHALL NOT be the final authority for consequential rights interpretation.

---

# 276. Contract Clause Extraction

Candidate fields may include:

```text
storage
redistribution
derivative works
AI
termination
audit
attribution.
```

Human/legal verification remains required where consequential.

---

# 277. Machine-Readable Rights

Where licences provide machine-readable rights expressions, Baobab SHOULD ingest them.

---

# 278. Machine-Readable ≠ Fully Interpreted

The machine-readable licence still requires correct scope/application.

---

# 279. Provenance of Rights

Every rights profile SHALL identify:

```text
licence

contract

law

reviewer

evidence.
```

---

# 280. Rights Conflict

If:

```text
website licence says A
contract says B
```

the system SHALL not choose automatically unless precedence is legally/contractually established.

---

# 281. Rights Conflict Outcome

```text
LEGAL_REVIEW_REQUIRED
```

is valid.

---

# 282. Conflicting Third-Party Terms

A provider may have no authority to sublicense embedded third-party material.

Those exclusions SHALL propagate.

---

# 283. Licence Warranty Is Not Assumed

Even open licences may disclaim warranties.

The OGL, for example, expressly provides information "as is" and excludes warranties/liability to the extent permitted.

This reinforces:

```text
permission to reuse
≠
guarantee of legal accuracy.
```

---

# 284. Rights and Trust Independence

An openly licensed source can be inaccurate.

A restricted source can be authoritative.

Rights policy and trust policy SHALL therefore remain separate.

---

# 285. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-RGT-I01` | Public accessibility SHALL NOT imply unrestricted reuse |
| `REG-RGT-I02` | Government publication SHALL NOT imply public-domain status |
| `REG-RGT-I03` | Technical access SHALL remain distinct from legal reuse rights |
| `REG-RGT-I04` | Rights SHALL be modelled per use, not as one Boolean |
| `REG-RGT-I05` | Access, storage, transformation, redistribution and AI processing SHALL be separately governable |
| `REG-RGT-I06` | RAG SHALL remain distinct from model training/fine-tuning |
| `REG-RGT-I07` | External-model transfer SHALL be separately authorised |
| `REG-RGT-I08` | Derived regulatory rules SHALL retain rights provenance |
| `REG-RGT-I09` | Canonical transformation SHALL not launder upstream rights |
| `REG-RGT-I10` | Raw-content redistribution SHALL default to denied unless positively established |
| `REG-RGT-I11` | Tenant-private content SHALL default to no cross-tenant reuse |
| `REG-RGT-I12` | Privileged counsel material SHALL not be used for shared model training by default |
| `REG-RGT-I13` | Attribution requirements SHALL be machine-enforceable where possible |
| `REG-RGT-I14` | Share-alike / NoDerivatives / NonCommercial restrictions SHALL remain explicit |
| `REG-RGT-I15` | Third-party rights SHALL remain explicit |
| `REG-RGT-I16` | Open licence SHALL not imply legal authority |
| `REG-RGT-I17` | Legal authority SHALL not imply open reuse rights |
| `REG-RGT-I18` | Provider termination SHALL not be accepted without an exit policy |
| `REG-RGT-I19` | Post-termination rule survivability SHALL be established, not assumed |
| `REG-RGT-I20` | Historical audit requirements SHALL be considered during provider contracting |
| `REG-RGT-I21` | Search/vector indexes SHALL remain traceable to rights-governed sources |
| `REG-RGT-I22` | Source-rights expiry SHALL support impact traversal |
| `REG-RGT-I23` | Rights changes SHALL not be misclassified as changes in law |
| `REG-RGT-I24` | Content deletion SHALL not use uncontrolled cascading deletion |
| `REG-RGT-I25` | Rights-unknown state SHALL remain explicit |
| `REG-RGT-I26` | High-risk rights questions SHALL fail closed or route to review |
| `REG-RGT-I27` | AI SHALL not autonomously declare contractual reuse rights for production |
| `REG-RGT-I28` | Rights policies SHALL be temporally versioned |
| `REG-RGT-I29` | Customer export SHALL distinguish customer-owned, Baobab-derived and third-party-restricted content |
| `REG-RGT-I30` | Every material content use SHALL be explainable by an applicable rights basis |

---

# 286. Rejected Alternative — Public Web Means Free to Use

Rejected.

WIPO expressly identifies this as a common misconception.

---

# 287. Rejected Alternative — Government Content Is Always Public Domain

Rejected.

South African and Ugandan law alone demonstrate why this is unsafe.

---

# 288. Rejected Alternative — One `can_reuse` Flag

Rejected.

Rights differ by:

```text
processing

storage

display

commercialisation

AI

retention.
```

---

# 289. Rejected Alternative — Open Licence Means No Conditions

Rejected.

Open licences can require attribution, impose share-alike or other conditions, and exclude specified rights/material.

---

# 290. Rejected Alternative — RAG and Training Are the Same

Rejected.

Their technical and legal characteristics differ.

---

# 291. Rejected Alternative — Embeddings Are Automatically Free of Source Restrictions

Rejected.

Their treatment depends on applicable rights and contractual terms.

---

# 292. Rejected Alternative — Rename Provider Fields and Own the Data

Rejected as rights laundering.

---

# 293. Rejected Alternative — Contract Ends, Keep Everything

Rejected.

Retention must follow governing rights.

---

# 294. Rejected Alternative — Contract Ends, Delete Everything

Also rejected.

Historical regulatory decisions, permitted audit records and independently derived canonical state may have different retention rights.

---

# 295. Rejected Alternative — AI Provider Terms Do Not Matter

Rejected.

Sending protected/confidential material to an external service is itself a governed use.

---

# 296. Rejected Alternative — Tenant Upload Means Baobab Can Reuse Globally

Rejected.

Customer-provided rights are scope-specific.

---

# 297. Rejected Alternative — One Global Copyright Interpretation

Rejected.

Copyright limitations, public-sector works and exceptions vary by jurisdiction. WIPO explicitly highlights jurisdictional variation.

---

# 298. Minimum Implementation Proof

Before this ADR is considered implemented, Baobab SHOULD demonstrate:

```text
1. One open government source.

2. One government source with
   non-trivial copyright status.

3. One CC BY source.

4. One CC BY-ND source.

5. One commercial licensed source.

6. One tenant-private source.

7. One privileged counsel source.

8. One source with third-party
   embedded content.

9. Separate access and redistribution
   permissions.

10. Separate OCR / parse permission.

11. Separate indexing permission.

12. Separate embedding permission.

13. Separate RAG permission.

14. Separate external-LLM transfer permission.

15. Separate training/fine-tuning permission.

16. Attribution propagation.

17. A NonCommercial incompatibility detected.

18. A NoDerivatives restriction detected.

19. A raw-content redistribution block.

20. A decision-only customer output allowed.

21. Rights metadata propagated
    through Docling conversion.

22. Rights metadata propagated
    through Haystack chunking.

23. Rights-scoped vector retrieval.

24. Restricted source blocked
    from external LLM.

25. Tenant source blocked
    cross-tenant.

26. Licence-expiry event.

27. Rights blast-radius query.

28. Embedding deletion after rights expiry.

29. Raw source deleted while
    retainable decision history remains.

30. Provider re-sourcing.

31. Post-termination derived-rule
    survivability test.

32. Customer portability export
    excluding restricted provider data.

33. Historical rights-decision replay.

34. Rights-conflict requiring legal review.

35. Rights-aware production gate
    blocking unapproved source ingestion.
```

---

# 299. Initial Uganda–South Africa Programme

The first regulatory corridor SHALL explicitly establish rights profiles for every production source used for:

```text
Uganda Gazette

Ugandan customs/tax/agricultural sources

South African Government Gazette

SARS materials

ITAC materials

SPS/agricultural materials

AfCFTA sources

EAC sources

SACU sources

WCO reference materials.
```

---

# 300. Initial Rights Deliverable

For each source:

```text
authority

copyright/licence basis

storage

parsing

indexing

embedding

RAG

external AI

rule derivation

quotation

customer display

retention

post-termination treatment.
```

shall be documented.

---

# 301. Provider Evaluation Template

Every commercial provider considered for Regulations SHOULD answer:

```text
Can Baobab store your data?

Can Baobab cache it?

For how long?

Can Baobab normalise it?

Can Baobab create embeddings?

Can Baobab use it in RAG?

Can content be sent to our chosen AI provider?

Can Baobab derive rules?

Who owns derived rules?

May derived rules survive termination?

May historical source artefacts survive for audit?

Can Baobab expose source snippets?

Can Baobab expose derived decisions?

Can customers export derived decisions?

Can Baobab move to another provider
without deleting all derived regulatory knowledge?
```

If these answers are unclear, the provider is not production-ready for Baobab.

---

# 302. Relationship to Docling

Docling SHALL operate as:

```text
DocumentIntelligenceProvider
```

behind a Baobab contract.

Its processing SHALL occur only for uses permitted by the source's rights policy.

---

# 303. Relationship to Haystack

Haystack SHALL operate as:

```text
RegulatoryKnowledgeProcessor
```

behind Baobab contracts.

Its document stores, indexes, chunks and embeddings SHALL remain rights-aware projections rather than ungoverned copies.

---

# 304. Relationship to LangGraph

LangGraph SHALL be eligible to orchestrate:

```text
rights review

approval

exception handling

provider onboarding

licence renewal

deletion certification
```

without owning canonical rights state.

---

# 305. Relationship to ADR-REG-0013

`ADR-REG-0013 — Source Ingestion, Normalisation and Adapter Architecture` SHALL implement the following gate:

```text
Source Registry
      ↓
Rights Policy
      ↓
Acquisition Adapter
      ↓
Immutable Artefact
      ↓
Docling
      ↓
Haystack
      ↓
Candidate Regulatory Knowledge.
```

Rights SHALL therefore constrain ingestion before the content-processing pipeline begins.

---

# 306. Relationship to ADR-REG-0014

`ADR-REG-0014` SHALL make rights lineage part of evidentiary provenance.

A decision should ultimately be able to prove both:

```text
where the rule came from
```

and, where relevant:

```text
under what content-use basis
Baobab processed its source.
```

---

# 307. Relationship to ADR-REG-0021

`ADR-REG-0021 — AI-Assisted Regulatory Extraction and Interpretation Boundary` SHALL adopt this ADR's distinctions between:

```text
RAG

external inference

model training

fine-tuning

evaluation.
```

---

# 308. Relationship to ADR-REG-0028

`ADR-REG-0028` SHALL integrate:

```text
tenant isolation

privileged material

data residency

licence entitlements

rights-sensitive retrieval.
```

---

# 309. Relationship to ADR-REG-0030

Commercial packaging SHALL reflect actual source rights.

Premium content providers may impose:

```text
separate entitlements

usage costs

display limitations

customer restrictions.
```

Baobab pricing SHALL account for these without allowing source licensing to redefine canonical regulatory semantics.

---

# 310. Strategic Decision

Baobab SHALL optimise for:

```text
AUTHORITATIVE SOURCES
        +
DURABLE DERIVED RIGHTS
        +
PROVIDER REPLACEABILITY
```

rather than maximising the amount of third-party content copied into the platform.

---

# 311. Why This Matters Commercially

A regulatory-data platform can appear technically provider-neutral while remaining contractually locked in.

Example:

```text
Provider API replaceable
```

but:

```text
44,000 derived rules must be deleted
if provider contract ends.
```

That is not provider neutrality.

---

# 312. True Provider Neutrality

True neutrality requires:

```text
technical replaceability
+
identity independence
+
source provenance
+
contractual portability
+
durable derived knowledge.
```

---

# 313. Baobab's Preferred Intellectual Property Position

Where legally and contractually possible:

```text
Official law
    ↓
Baobab interpretation
    ↓
Baobab canonical rule
    ↓
Baobab applicability model
    ↓
Baobab regulatory decision
```

should become a durable Baobab capability while preserving all required attribution/provenance and without claiming ownership of underlying law or protected third-party expression.

---

# 314. Research Foundation Summary

WIPO confirms that Internet availability does not make content public domain and that copyright exceptions vary by jurisdiction. It also distinguishes protected expression from underlying ideas, processes and methods.

South Africa's Copyright Act recognises copyright in eligible works made by or under direction/control of the State, showing that government-created material cannot globally be presumed public domain.

Uganda's current Copyright and Neighbouring Rights Act similarly contains provisions governing works created under Government direction/control and economic rights in works, reinforcing the need for jurisdiction-specific rights analysis.

The UK Open Government Licence demonstrates a mature permissive government-reuse model: it expressly permits copying, adaptation and commercial reuse subject to attribution and other exclusions, including third-party rights and specified excluded materials.

Creative Commons demonstrates that apparently "open" licences contain materially different permissions and restrictions, including NonCommercial and NoDerivatives conditions, while current CC guidance acknowledges unresolved complexity concerning copyright licensing and AI uses.

The EU Open Data Directive provides another jurisdiction-specific example of a policy architecture encouraging reuse of public-sector information, including legal information, while confirming that such reuse regimes are matters of explicit legal policy rather than a universal property of public-sector content.

---

# 315. Final Decision

Baobab Regulations SHALL implement regulatory-content rights as a **machine-readable, source-specific, use-specific, temporal governance layer**.

The final content pipeline SHALL conceptually be:

```text
                     REGULATORY SOURCE
                            │
                            ▼
                       SOURCE TRUST
                            │
                            ▼
                     CONTENT RIGHTS
                            │
           ┌────────────────┼──────────────────┐
           │                │                  │
           ▼                ▼                  ▼
       ACQUIRE          TRANSFORM             AI USE
           │                │                  │
           │                ▼                  │
           │             DOCLING               │
           │                │                  │
           └────────────────┼──────────────────┘
                            ▼
                         HAYSTACK
                            │
                            ▼
                    CANDIDATE KNOWLEDGE
                            │
                            ▼
                        LANGGRAPH
                    GOVERNED REVIEW
                            │
                            ▼
                  CANONICAL BAOBAB RULE
                            │
                            ▼
                  REGULATORY DECISION
                            │
                            ▼
                     CUSTOMER OUTPUT
                            │
                            ▼
                     RIGHTS FILTER
```

At every transition, Baobab SHALL know:

```text
May we acquire it?

May we retain it?

May we transform it?

May we index it?

May we embed it?

May we give it to an external model?

May we use it in RAG?

May we train a model with it?

May we derive regulatory rules?

May those rules survive provider termination?

May we expose the source to customers?

May we expose only snippets?

May we expose only Baobab's derived decision?

What attribution is required?

What must be deleted when rights end?
```

The critical principle is:

> **Baobab must never confuse the right to know the law with the right to copy another party's representation of the law.**

The commercial principle is:

> **Baobab should buy access to regulatory knowledge without selling its future independence to the source provider.**

The AI principle is:

> **RAG, embeddings, inference, fine-tuning and model training are separate content uses and SHALL be governed separately.**

And the provider-neutral principle is:

> **An engine is not truly provider-neutral if changing the provider requires deleting the regulatory intelligence derived from it.**

That is the foundation established by `ADR-REG-0012`.

---

## Decision Summary

```text
ADR-REG-0012
─────────────────────────────────────────────

CORE DECISION

Rights are executable policy.

NOT:

"public = reusable"


SEPARATE RIGHTS

Access
Fetch
Download
Copy
Cache
Archive
OCR
Parse
Normalise
Translate
Index
Embed
RAG
External AI
Training
Fine-tuning
Rule derivation
Quote
Display
Redistribute
Commercialise
Retain
Export


CORE DISTINCTIONS

Publicly accessible ≠ Public domain

Government ≠ Copyright free

Open licence ≠ No conditions

Access ≠ Redistribution

RAG ≠ Training

Technical access ≠ Legal right

Legal authority ≠ Reuse permission

Reuse permission ≠ Legal authority


TECHNOLOGY FLOW

Rights Policy
    ↓
Docling
    ↓
Haystack
    ↓
LangGraph
    ↓
Canonical Rule


AI

Every source gets explicit policy for:

Embeddings
RAG
External inference
Fine-tuning
Training


DERIVED DATA

Normalised data
Facts
Relationships
Interpretations
Rules
Embeddings
Decisions

retain upstream
rights provenance.


PROVIDER EXIT

Know before onboarding:

What must be deleted?

What can be retained?

Do rules survive?

Do audit records survive?

Can another source replace
the provider?


TENANCY

Tenant-private source
→ no cross-tenant reuse by default.

Counsel material
→ restricted / privileged.


STRATEGIC PRINCIPLE

Technical provider neutrality
is insufficient.

Baobab requires:

technical portability
+
rights portability
+
derived-knowledge durability.
```
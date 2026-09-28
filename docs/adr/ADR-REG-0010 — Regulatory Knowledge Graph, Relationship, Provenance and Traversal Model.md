# ADR-REG-0010 — Regulatory Knowledge Graph, Relationship, Provenance and Traversal Model

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0010`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Knowledge Graph / Relationship Semantics / Provenance / Traversal / Impact Architecture  
**Strategic Classification:** Core Regulatory IP / Platform Differentiator

**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`
- `ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture`
- `ADR-REG-0006 — Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries`
- `ADR-REG-0007 — Jurisdiction, Regulatory Authority and Legal Hierarchy Model`
- `ADR-REG-0008 — Regulatory Instrument, Provision, Rule, Obligation and Requirement Model`
- `ADR-REG-0009 — Normative Semantics, Defeasibility, Discretion, Rights, Violations and Reparative Rules Model`

**Relevant Baobab Architecture:**

- `ADR-PULSE-002 — Canonical Intelligence Domain Model and Aggregate Boundaries`
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- `ADR-BCP-004 — Context, Market, Geography, Legal-Entity and Digital Estate Resolution Model`
- `ADR-SHARED-012 — Topology Identifiers and External System Registry`
- `ADR-SHARED-013 — External References and Canonical Mapping Administration`

**Primary Principle:**

> **Baobab Regulations SHALL represent regulatory knowledge as a provenance-rich logical graph of typed canonical relationships while keeping graph representation separate from graph storage technology.**

---

# 1. Executive Decision

Baobab Regulations SHALL implement a canonical **Regulatory Knowledge Graph** connecting:

```text
AUTHORITY
   │
   ▼
REGIME
   │
   ▼
INSTRUMENT
   │
   ▼
EXPRESSION
   │
   ▼
PROVISION
   │
   ▼
INTERPRETATION
   │
   ▼
RULE
   │
   ▼
REGULATORY EFFECT
   │
   ▼
REQUIREMENT
   │
   ▼
EVIDENCE
   │
   ▼
ASSESSMENT
   │
   ▼
DECISION
   │
   ▼
OPERATIONAL CONSEQUENCE
```

together with horizontal and contextual relationships such as:

```text
AMENDS

REPEALS

IMPLEMENTS

INTERPRETS

EXCEPTS

OVERRIDES

DERIVED_FROM

APPLIES_TO

ISSUED_BY

HAS_JURISDICTION

MEMBER_OF_REGIME

SATISFIED_BY

CONFLICTS_WITH

HAS_PRECEDENCE_OVER

AFFECTS

SUPERSEDES
```

The graph SHALL support traversal:

```text
BACKWARD
```

for:

```text
provenance

explanation

audit

source verification
```

and:

```text
FORWARD
```

for:

```text
impact analysis

change propagation

reassessment

affected-object discovery.
```

---

# 2. The Graph Is Logical Architecture

The term:

```text
Regulatory Knowledge Graph
```

SHALL describe the semantic connectivity of Baobab Regulations.

It SHALL NOT prescribe:

```text
Neo4j

Amazon Neptune

JanusGraph

RDF triple store

property graph database

any other dedicated graph database.
```

The initial authoritative implementation SHOULD remain relational-first unless demonstrated graph workloads justify another authoritative persistence technology.

---

# 3. Strategic Purpose

The strategic asset is not:

```text
10 million regulatory documents.
```

The strategic asset is:

```text
Regulation
    │
    ▼
Meaning
    │
    ▼
Applicability
    │
    ▼
Business Object
    │
    ▼
Requirement
    │
    ▼
Evidence
    │
    ▼
Decision
    │
    ▼
Outcome.
```

That relationship network allows Baobab to answer questions conventional regulatory search products often cannot answer directly.

---

# 4. Questions the Graph Must Answer

The graph SHALL support queries such as:

```text
Which authority issued this requirement?

Which source provisions support this rule?

Which interpretation transformed those provisions?

Which rules depend on this definition?

Which exceptions defeat this prohibition?

Which authority has competence over this rule?

Which regulation superseded this one?

Which currently active obligations arose from this provision?

Which evidence satisfied this obligation?

Why was Shipment S blocked?

Which version of the law produced Decision D?

Which transactions depend on Rule R?

Which customers are affected by Amendment A?

Which products depend on HS code X?

Which open shipments must be reassessed?

What breaks if Source S is discovered to be wrong?
```

---

# 5. Research Foundation — Provenance

W3C PROV defines provenance around three foundational concepts:

```text
Entity
Activity
Agent
```

and relationships describing generation, use, derivation, attribution and responsibility.

Baobab SHALL remain semantically compatible with these ideas.

It SHALL not require the internal domain model to use PROV-O classes directly.

---

# 6. PROV Alignment

Conceptually:

```text
SourceArtefact
        =
PROV Entity

RuleCompilation
        =
PROV Activity

RegulatoryReviewer
        =
PROV Agent
```

and:

```text
RuleVersion
    DERIVED_FROM
Interpretation

Interpretation
    DERIVED_FROM
ProvisionVersion
```

map naturally to provenance semantics.

---

# 7. Research Foundation — ELI

The European Legislation Identifier ontology v1.5 provides a common model for exchanging legislation metadata and reinforces the distinction between stable legal-resource identity and its representations.

The Regulatory Knowledge Graph SHALL preserve those identity separations established in `ADR-REG-0006`.

---

# 8. Research Foundation — LegalRuleML

LegalRuleML explicitly requires traceability between legally binding textual provisions and formal machine rules because the textual legal source remains critical for:

```text
authority

authenticity

validation

provenance

rule maintenance.
```


This strongly supports Baobab's decision to make source-to-rule relationships first-class graph edges.

---

# 9. Research Foundation — RDF

Stable RDF 1.1 defines a graph as subject-predicate-object triples and datasets as collections of graphs. RDF 1.2 is under active standardisation and, as of September 2026, remains at Candidate Recommendation stage rather than final Recommendation.

Baobab SHALL therefore:

```text
support RDF-compatible export where useful
```

but SHALL NOT make evolving RDF 1.2 representation requirements its canonical persistence dependency.

---

# 10. Research Foundation — SHACL

SHACL is a W3C Recommendation for validating RDF graphs against machine-readable constraints. A newer SHACL 1.2 specification is also under active development in 2026.

Baobab MAY use SHACL for:

```text
interchange validation

external graph conformance

ontology export testing.
```

Internal domain invariants SHALL remain enforceable independently of SHACL.

---

# 11. Knowledge Graph versus Ontology

These concepts SHALL remain distinct.

```text
Ontology
=
meaning of classes and relationships.

Knowledge Graph
=
actual canonical instances and relationships.
```

Example:

```text
Ontology says:
Instrument AMENDS Instrument.

Knowledge graph says:
Instrument X AMENDS Instrument Y.
```

---

# 12. Knowledge Graph versus Rule Engine

Likewise:

```text
Knowledge Graph
≠
Rule Evaluator.
```

The graph answers:

```text
what is connected?
```

The evaluator answers:

```text
what conclusion follows for this context?
```

---

# 13. Knowledge Graph versus Search Index

```text
Knowledge Graph
≠
Search Index.
```

Search indexes MAY project graph content.

They SHALL not become canonical authority.

---

# 14. Knowledge Graph versus Vector Store

```text
Knowledge Graph
≠
Vector Store.
```

Embeddings may answer:

```text
what looks semantically similar?
```

They do not establish:

```text
legal identity

authority

precedence

derivation.
```

---

# 15. Knowledge Graph versus AI Memory

The graph SHALL NOT be treated as:

```text
LLM memory.
```

It is governed regulatory domain state.

AI systems may query it.

They do not own it.

---

# 16. Canonical Graph Layers

The graph SHALL conceptually contain at least seven layers:

```text
G0 — SOURCE & PROVENANCE

G1 — LEGAL AUTHORITY

G2 — LEGAL RESOURCE

G3 — NORMATIVE KNOWLEDGE

G4 — APPLICABILITY & EFFECT

G5 — EVIDENCE & DECISION

G6 — BUSINESS IMPACT
```

---

# 17. G0 — Source & Provenance Layer

Includes:

```text
RegulatorySourceProvider

RegulatorySource

RegulatoryEndpoint

AcquisitionRun

SourceArtefact

ProviderNativeRecord

NormalisedSourceRecord.
```

---

# 18. G1 — Legal Authority Layer

Includes:

```text
Jurisdiction

RegulatoryRegime

RegulatoryAuthority

RegulatoryCompetence

RegimeMembership

AuthorityRelationship

LegalHierarchyPolicy.
```

---

# 19. G2 — Legal Resource Layer

Includes:

```text
RegulatoryInstrument

InstrumentExpression

RegulatoryProvision

ProvisionVersion

JudicialDecision

AuthorityDetermination.
```

---

# 20. G3 — Normative Knowledge Layer

Includes:

```text
RegulatoryConcept

RegulatoryInterpretation

RegulatoryRule

RegulatoryRuleVersion

RuleException

NormativeEffectTemplate

DefeasibilityProfile.
```

---

# 21. G4 — Applicability & Effect Layer

Includes:

```text
RegulatoryContext

ApplicabilityResult

RegulatoryEffect

RegulatoryRequirement

RegulatoryViolation

ReparativeObligation.
```

---

# 22. G5 — Evidence & Decision Layer

Includes:

```text
Evidence

EvidenceAssessment

RegulatoryAssessment

RegulatoryDecision

Override

Challenge

Verification.
```

---

# 23. G6 — Business Impact Layer

References—but does not own—Baobab business objects such as:

```text
LegalEntity

Product

Counterparty

Order

Shipment

Invoice

Payment

DigitalEstate

Market

TradeLane

ContentPublication.
```

---

# 24. Graph Boundary Principle

G6 references cross-engine canonical identities.

It SHALL NOT duplicate authoritative operational objects.

---

# 25. Canonical Node Identity

Every independently addressable graph node SHALL use stable canonical identity.

Examples:

```text
regauth_...

reginst_...

regprov_...

reginterp_...

regrule_...

regeffect_...

regassess_...

regdec_...
```

Exact identifier grammar remains a Shared concern.

---

# 26. External Identity

Provider-native IDs SHALL remain:

```text
ExternalReference.
```

This aligns with Shared's accepted mapping architecture.

An ExternalReference records a native identity while governed mappings relate it to canonical objects.

---

# 27. Node Identity Survives Representation Change

A canonical:

```text
RegulatoryInstrument
```

SHALL retain its identity if its:

```text
URL changes

PDF changes

provider changes

serialization changes.
```

---

# 28. Edge as First-Class Domain Object

Material regulatory relationships SHALL be independently addressable.

Conceptually:

```text
RegulatoryRelationship
├── relationship_id
├── relationship_type
├── source_ref
├── target_ref
├── direction
├── scope
├── valid_time
├── recorded_time
├── tenant_scope
├── authority_basis_refs[]
├── interpretation_ref?
├── provenance
├── verification_state
├── lifecycle_state
└── metadata
```

---

# 29. Why Edges Need Identity

Relationships themselves may be:

```text
verified

disputed

superseded

limited in scope

effective-dated

tenant-specific

derived

corrected.
```

Example:

```text
Rule A
HAS_PRECEDENCE_OVER
Rule B
```

is a legal proposition requiring its own provenance.

---

# 30. Not Every Relationship Needs Heavyweight Persistence

Structural relationships such as:

```text
Provision
BELONGS_TO
Instrument
```

may be enforceable through ordinary foreign keys.

The conceptual graph still recognises them.

Only relationships requiring independent semantics need full `RegulatoryRelationship` identity.

---

# 31. Relationship Families

Initial canonical relationship families SHALL include:

```text
AUTHORITY

RESOURCE_STRUCTURE

LIFECYCLE

DERIVATION

NORMATIVE

HIERARCHY

APPLICABILITY

EVIDENCE

DECISION

CONTEXT

IMPACT

IDENTITY
```

---

# 32. Authority Relationships

Examples:

```text
ISSUED_BY

ADMINISTERED_BY

ENFORCED_BY

INTERPRETED_BY

DELEGATES_TO

DERIVES_AUTHORITY_FROM

SUPERVISES

APPEAL_TO

SUCCESSOR_TO

PREDECESSOR_OF.
```

---

# 33. Regime Relationships

Examples:

```text
MEMBER_OF_REGIME

IMPLEMENTS_REGIME

HIGHER_INTEGRATION_THAN

PREVAILS_OVER_TO_EXTENT_OF_CONFLICT

COEXISTS_WITH

CARVES_OUT.
```

---

# 34. Resource Structure Relationships

Examples:

```text
HAS_EXPRESSION

CONTAINS_PROVISION

HAS_VERSION

HAS_TRANSLATION

INCORPORATES_BY_REFERENCE

CITES.
```

---

# 35. Lifecycle Relationships

Examples:

```text
AMENDS

REPEALS

CORRECTS

COMMENCES

CONSOLIDATES

SUPERSEDES

REPLACES

REVOKES.
```

---

# 36. Derivation Relationships

Examples:

```text
DERIVED_FROM

EXTRACTED_FROM

NORMALISED_FROM

INTERPRETS

ENCODES

COMPILED_FROM

CALCULATED_FROM.
```

---

# 37. Normative Relationships

Examples:

```text
CREATES_EFFECT

DEFINES_CONCEPT

REQUIRES

PERMITS

PROHIBITS

EXCEPTS

QUALIFIES

DEFEATS

OVERRIDES

TRIGGERS

REPAIRS_VIOLATION_OF.
```

---

# 38. Applicability Relationships

Examples:

```text
APPLIES_TO

DOES_NOT_APPLY_TO

HAS_BEARER

HAS_SUBJECT

HAS_OBJECT

HAS_JURISDICTION

USES_CLASSIFICATION

BOUND_TO_CONTEXT.
```

---

# 39. Evidence Relationships

Examples:

```text
SUPPORTED_BY

SATISFIED_BY

CORROBORATED_BY

CONTRADICTED_BY

VERIFIED_BY

REJECTED_BY

REVOKED_BY.
```

---

# 40. Decision Relationships

Examples:

```text
ASSESSED_BY

PRODUCED_DECISION

OVERRIDDEN_BY

CHALLENGED_BY

CONFIRMED_BY

SUPERSEDED_BY

ENFORCED_BY.
```

---

# 41. Context Relationships

Examples:

```text
REFERENCES_ENTITY

REFERENCES_PRODUCT

REFERENCES_COUNTERPARTY

REFERENCES_SHIPMENT

REFERENCES_ORDER

REFERENCES_MARKET

REFERENCES_TRADE_LANE.
```

---

# 42. Impact Relationships

Examples:

```text
AFFECTS

MAY_AFFECT

REQUIRES_REASSESSMENT_OF

INVALIDATES

CHANGES_REQUIREMENT_FOR

CHANGES_DECISION_FOR.
```

---

# 43. Identity Relationships

Examples:

```text
MAPS_TO

ALIAS_OF

POSSIBLY_SAME_AS

EXTERNAL_REFERENCE_OF.
```

Identity relationships SHALL follow Shared mapping authority where applicable.

---

# 44. Avoid Generic `RELATED_TO`

The core graph SHALL not represent consequential relationships simply as:

```text
RELATED_TO.
```

That destroys semantic value.

---

# 45. Direction Matters

Canonical direction SHALL be defined for each edge.

Example:

```text
Rule
DERIVED_FROM
Provision
```

not arbitrary orientation.

Reverse traversal is a query concern.

---

# 46. Inverse Relationships

The ontology MAY define inverses.

Example:

```text
Rule DERIVED_FROM Provision
```

inverse:

```text
Provision SUPPORTS_RULE Rule.
```

The implementation need not physically persist both.

---

# 47. Symmetric Relationships

Some relationships may be symmetric.

Example:

```text
CONFLICTS_WITH.
```

Canonical persistence SHALL still avoid unnecessary duplication.

---

# 48. Relationship Vocabulary Governance

Relationship types SHALL be centrally governed.

Developers SHALL NOT freely invent:

```text
sort_of_based_on

kind_of_related

similar_to_rule.
```

---

# 49. Relationship Semantics Registry

The engine SHOULD maintain a registry defining:

```text
relationship key

family

allowed source node types

allowed target node types

direction

symmetric?

transitive?

temporal?

tenant-scoped?

requires provenance?

requires verification?
```

---

# 50. Transitivity Must Be Explicit

Do not assume:

```text
A relationship B
B relationship C
therefore A relationship C.
```

unless the relationship semantics allow it.

---

# 51. Example — `AMENDS`

```text
A AMENDS B
B AMENDS C
```

does not mean:

```text
A AMENDS C.
```

---

# 52. Example — `DERIVED_FROM`

Transitive derivation MAY be useful:

```text
Decision
DERIVED_FROM
Assessment

Assessment
DERIVED_FROM
Rule

Rule
DERIVED_FROM
Provision.
```

Traversal can reveal full provenance even if direct transitive edges are not persisted.

---

# 53. Example — `SUPERSEDES`

Whether supersession is effectively transitive depends on scope and time.

It SHALL not be blindly materialised.

---

# 54. Scope Is a First-Class Relationship Property

A relationship may apply only:

```text
within customs domain

for Product Class X

in South Africa

between 2027 and 2029

for Tenant A.
```

Therefore relationship scope SHALL be modelled explicitly where relevant.

---

# 55. Scope Model

Conceptually:

```text
RelationshipScope
├── jurisdiction_refs[]
├── regime_refs[]
├── regulatory_domains[]
├── subject_refs/classes[]
├── activity_types[]
├── product/classification_refs[]
├── tenant_ref?
├── legal_entity_ref?
└── context_constraints?
```

---

# 56. Simple Triple Is Sometimes Insufficient

This proposition:

```text
Rule A
HAS_PRECEDENCE_OVER
Rule B
```

may omit essential facts:

```text
only in customs

only for specified products

only after date X

only in jurisdiction Y

because of Treaty Article Z.
```

---

# 57. Qualified Relationship Pattern

Complex relationships SHALL therefore support a qualified relationship object:

```text
Rule A
   │
   ▼
PrecedenceRelationship PR-1
   │
   ├── target → Rule B
   ├── scope → Customs
   ├── jurisdiction → J
   ├── effective → [T1,T2)
   ├── legal_basis → Provision Z
   └── verified_by → Reviewer R
```

This is effectively an n-ary/hyperedge representation.

---

# 58. Why Hyperedges Matter

Legal relationships frequently depend on more than two participants.

Example:

```text
Authority A
delegates Function F
to Authority B
under Instrument I
for Domain D
during Time T.
```

A plain:

```text
A DELEGATES_TO B
```

loses legally essential meaning.

---

# 59. Relationship Nodes

Where the relationship itself carries substantial semantics, Baobab SHOULD reify it as a canonical relationship record.

---

# 60. Relationship Versioning

A relationship's legal meaning MAY change over time.

Example:

```text
Authority A delegates customs function
to Authority B

2026–2028.
```

Later:

```text
Authority C
takes over.
```

The historical relationship SHALL remain.

---

# 61. Temporal Relationship Model

Every legally consequential edge SHALL be capable of carrying:

```text
valid_from

valid_to

recorded_at

superseded_at
```

or later bitemporal equivalents under `ADR-REG-0015`.

---

# 62. PostgreSQL Temporal Fit

PostgreSQL 17 provides native range and multirange types with containment, overlap and indexing operations, making temporal validity ranges a strong relational implementation option.

A likely implementation may therefore use:

```text
tstzrange

daterange
```

for effective intervals.

That is an implementation recommendation, not canonical semantics.

---

# 63. Provenance on Nodes

Material nodes SHALL record provenance.

Example:

```text
RuleVersion
├── provision refs
├── interpretation refs
├── source artefact refs
├── author/reviewer
└── transformation version.
```

---

# 64. Provenance on Relationships

Material edges SHALL also record provenance.

This is critical.

Example:

```text
Rule A OVERRIDES Rule B
```

must answer:

```text
Who established this?

From which source?

Under which interpretation?

When?

With what verification?
```

---

# 65. W3C PROV Compatibility

Baobab graph projections SHOULD be capable of representing:

```text
Entity

Activity

Agent
```

and standard provenance relationships where external interoperability benefits.

---

# 66. Domain Semantics Override Generic PROV

PROV can say:

```text
Rule R wasDerivedFrom Provision P.
```

Baobab may additionally know:

```text
derivation_type = LEGAL_INTERPRETATION

interpretation = I

review_status = VERIFIED.
```

Canonical domain meaning remains richer.

---

# 67. Graph Statements May Be Contested

A relationship may be:

```text
PROPOSED

VERIFIED

DISPUTED

REJECTED

SUPERSEDED

SUSPENDED.
```

---

# 68. Contested Relationship

Example:

```text
Interpretation A claims:
Rule X overrides Rule Y.

Interpretation B claims:
they coexist.
```

Both candidate relationships may exist with different governance states.

---

# 69. Canonical Active Graph

Operational evaluation SHALL normally traverse:

```text
verified

published

effective
```

relationships.

Draft/candidate edges remain available for research but do not control production.

---

# 70. Graph Views

Baobab SHOULD provide at least:

```text
RESEARCH_GRAPH

PUBLISHED_GRAPH

EFFECTIVE_GRAPH

HISTORICAL_GRAPH

TENANT_EFFECTIVE_GRAPH.
```

These MAY be query projections rather than physical stores.

---

# 71. Research Graph

May contain:

```text
candidate sources

AI-suggested relationships

draft interpretations

potential conflicts.
```

---

# 72. Published Graph

Contains approved regulatory knowledge.

---

# 73. Effective Graph

Contains knowledge applicable at:

```text
specified legal time.
```

---

# 74. Historical Graph

Allows reconstruction of prior regulatory state.

---

# 75. Tenant Effective Graph

Conceptually:

```text
Platform Published Graph
        +
tenant-private overlays
        +
tenant-approved interpretations
        +
tenant-specific authority determinations
```

subject to isolation.

---

# 76. Overlay Architecture

Tenant-specific regulatory knowledge SHALL overlay shared knowledge.

It SHALL NOT physically mutate shared canonical nodes.

---

# 77. Example

```text
Shared Provision P
       │
       ├── Platform Interpretation I1
       │
       └── Tenant A Counsel Interpretation I2
```

Tenant A's graph may use:

```text
I2
```

while other tenants continue using:

```text
I1.
```

---

# 78. Tenant Isolation

Tenant-private nodes and edges SHALL carry explicit tenant scope.

Cross-tenant traversal SHALL fail closed.

---

# 79. Public/Shared Nodes

Generally applicable public regulatory knowledge MAY be globally shared where source rights permit.

---

# 80. Licensed Nodes

Commercially licensed annotations MAY be:

```text
shared internally

restricted by entitlement

provider-specific

tenant-specific
```

according to licensing policy.

---

# 81. Graph Rights Filtering

Traversal SHALL respect:

```text
tenant isolation

licensing rights

security classification

capability grants

principal authority.
```

---

# 82. Query Results Must Preserve Access Policy

A user SHALL NOT gain access to restricted source text merely because:

```text
a public decision node links to it.
```

---

# 83. Relationship Visibility

An edge itself MAY contain sensitive information.

Example:

```text
Tenant Counsel Opinion
INTERPRETS
Public Regulation.
```

Even existence of that relationship may be tenant confidential.

---

# 84. Public Citation versus Restricted Evidence

The engine MAY expose:

```text
public citation
```

while withholding:

```text
licensed provider analysis.
```

---

# 85. Graph Traversal API

A future internal graph-query capability SHOULD support bounded traversals such as:

```text
ancestors

descendants

shortest explainability path

impact closure

dependency closure

source lineage

affected-object closure.
```

---

# 86. Arbitrary Graph Queries Are Not Default Public API

Exposing an unrestricted:

```text
Cypher endpoint

SPARQL endpoint
```

to every Digital Estate is NOT required.

Canonical Baobab APIs SHALL expose task-oriented regulatory capabilities.

---

# 87. Task-Oriented API Examples

```text
ExplainDecision(decision_id)

GetRuleSources(rule_id)

GetAffectedObjects(change_id)

GetOutstandingRequirements(context)

GetRuleDependencies(rule_id)

GetInstrumentHistory(instrument_id)
```

---

# 88. Internal Graph Query API

Regulations MAY implement a richer administrative/research graph API internally.

---

# 89. Traversal Limits

Every graph traversal SHALL support bounds such as:

```text
maximum depth

maximum nodes

relationship filters

time filters

tenant filters

domain filters.
```

---

# 90. Why Limits Matter

Malformed or highly connected relationships could otherwise produce:

```text
unbounded traversal

expensive queries

denial-of-service risk.
```

---

# 91. Cycle Awareness

Some legitimate regulatory graphs may contain cycles.

Example:

```text
Concept A defined with reference to B

Concept B refers back to A.
```

Traversal SHALL therefore implement cycle detection.

---

# 92. PostgreSQL Recursive Traversal

PostgreSQL 17 supports recursive common-table expressions for hierarchical and graph-like traversal and explicitly documents cycle-detection techniques.

This supports a relational-first graph implementation for the initial scale.

---

# 93. Relational-First Authoritative Store

The initial system SHOULD use relational authoritative persistence for:

```text
canonical nodes

typed relationships

version state

scope

temporal validity

tenant isolation

foreign-key integrity

governance.
```

---

# 94. Why Relational First

The domain contains many requirements for:

```text
transactions

referential integrity

effective dating

uniqueness

governance state

tenant isolation

auditable mutation

controlled versioning.
```

These map naturally to PostgreSQL.

---

# 95. Why Not Graph Database First

A dedicated graph database introduces additional:

```text
operational complexity

backup complexity

consistency concerns

cross-store synchronisation

skills requirements

failure modes.
```

The primary justification would need to be demonstrable graph workloads that materially outperform an acceptable relational design.

---

# 96. Rejected Premature Graph Database

This ADR explicitly rejects:

```text
The data is a graph,
therefore install Neo4j.
```

---

# 97. Graph Projection

A dedicated graph store MAY later be added as a **derived projection**.

Conceptually:

```text
PostgreSQL Canonical Store
          │
          ▼
Domain Events
          │
          ▼
Graph Projection Builder
          │
          ▼
Specialised Graph Store
```

---

# 98. Derived Graph Store Is Rebuildable

A graph projection SHALL be reconstructable from canonical state/events.

It SHALL not become an untracked second source of truth.

---

# 99. Graph Projection Uses

Potential future specialised use cases:

```text
large-scale multi-hop impact analysis

interactive relationship exploration

complex path discovery

semantic research

graph analytics.
```

---

# 100. Graph Projection Consistency

Every projection SHALL record:

```text
source event position

projection version

schema version

last rebuild

health state.
```

---

# 101. Projection Lag

Graph projection lag SHALL be observable.

A stale projection SHALL not silently serve high-impact regulatory decisions.

---

# 102. Evaluation Path

High-impact runtime rule evaluation SHOULD normally use:

```text
canonical published rule state
```

rather than rely solely on asynchronously projected graph data.

---

# 103. Graph Is Not Mandatory Runtime Dependency for Every Assessment

This is strategically important.

A Trade assessment SHOULD not fail merely because a graph-visualisation projection is unavailable.

---

# 104. RDF Export

Baobab SHOULD remain capable of projecting appropriate graph portions to RDF for:

```text
legal-data interoperability

research

partner exchange

standards integration.
```

---

# 105. Stable RDF Baseline

Where RDF is used, stable standards such as RDF 1.1 SHOULD form the compatibility baseline until newer versions mature. RDF 1.2 remains under active W3C Candidate Recommendation work in September 2026.

---

# 106. Baobab IRIs

A future RDF export SHOULD use durable Baobab-controlled IRIs for canonical regulatory identities.

External provider URIs SHALL not become canonical identity by accident.

---

# 107. Named Graphs

RDF named graphs MAY be useful for:

```text
tenant overlays

source-specific assertions

publication states

jurisdiction packs.
```

This is optional interoperability design.

---

# 108. SHACL Validation

If Baobab exports RDF, SHACL MAY validate graph structures such as:

```text
Rule must have source provenance.

Provision must belong to Instrument.

Decision must reference Assessment.
```

SHACL is specifically designed for graph constraint validation.

---

# 109. SHACL Does Not Replace Domain Validation

The production service SHALL still enforce invariants at:

```text
domain

application

database

contract
```

layers.

---

# 110. Search Projection

Regulatory graph content MAY be projected into full-text search.

PostgreSQL 17 supports GIN and GiST full-text indexes, with GIN identified as the preferred text-search index type in the PostgreSQL documentation.

---

# 111. Search Nodes

Search indexes may include:

```text
instrument titles

provision text

rule explanations

concept labels

citations.
```

---

# 112. Search Is Candidate Retrieval

Search returns:

```text
potentially relevant regulatory objects.
```

It SHALL not establish authoritative graph relationships.

---

# 113. Vector Projection

Embeddings MAY be generated for:

```text
provisions

interpretations

rules

concept definitions.
```

---

# 114. Vector Links Are Suggestions

A similarity result MAY generate:

```text
POSSIBLY_RELATED_TO
```

candidate state.

It SHALL NOT automatically create:

```text
AMENDS

OVERRIDES

IMPLEMENTS

SAME_AS.
```

---

# 115. AI-Suggested Edges

AI MAY propose graph relationships.

Candidate edge:

```text
Rule R1
MAY_BE_EXCEPTION_TO
Rule R2.
```

This remains:

```text
CANDIDATE.
```

---

# 116. Promotion

A consequential AI-suggested relationship requires:

```text
source evidence

interpretation

verification

governed publication
```

before becoming effective graph state.

---

# 117. Graph Confidence

Baobab SHALL avoid one universal:

```text
edge_confidence = 0.91
```

as legal authority.

Instead graph assertions SHOULD preserve dimensions such as:

```text
source authority

verification status

interpretation status

mapping confidence

factual certainty.
```

---

# 118. Mapping Confidence

Identity mapping may legitimately carry probabilistic confidence.

Example:

```text
Provider object probably maps to Instrument X.
```

That confidence SHALL remain mapping-specific.

---

# 119. Legal Precedence Confidence

A legal precedence relation SHALL ordinarily require governed verification rather than statistical confidence alone.

---

# 120. Graph Assertion Provenance

Every consequential graph assertion SHOULD answer:

```text
Who asserted this?

When?

From which evidence?

Through which process?

Was AI involved?

Was a human reviewer involved?

Which version is current?
```

---

# 121. Assertion Model

Conceptually:

```text
GraphAssertion
├── assertion_id
├── subject_ref
├── predicate
├── object_ref/value
├── scope
├── valid_time
├── knowledge_time
├── asserted_by
├── source_refs[]
├── method
├── verification_state
├── tenant_scope
└── supersedes?
```

---

# 122. Relationship versus Assertion

Simple graph relations MAY be represented as assertions.

Domain relationships requiring richer semantics MAY have dedicated structures.

The implementation SHALL not force all graph information into one generic triple table.

---

# 123. No Universal Triple Table

Rejected as primary persistence:

```text
subject
predicate
object
```

for the entire Regulations domain.

It would weaken:

```text
foreign-key integrity

typed fields

constraints

domain invariants

efficient operational queries.
```

---

# 124. Hybrid Relational Model

Preferred:

```text
strongly typed domain tables

+

typed relationship table

+

specialised relationship tables
when richer semantics require them.
```

---

# 125. Example Physical Pattern

Illustrative only:

```text
regulatory_instruments

regulatory_provisions

regulatory_rule_versions

regulatory_assessments

regulatory_relationships
```

with:

```text
source_type
source_id
target_type
target_id
relationship_type
```

for generic graph-compatible relationships.

---

# 126. Referential Integrity Challenge

Polymorphic relationships make conventional foreign keys more difficult.

The implementation SHOULD therefore consider:

```text
canonical graph node registry
```

or:

```text
typed relationship tables
```

rather than accepting unconstrained arbitrary identifiers.

---

# 127. GraphNode Registry

A lightweight registry MAY conceptually contain:

```text
GraphNode
├── node_id
├── node_type
├── canonical_object_id
├── tenant_scope
└── lifecycle_state
```

allowing relationships to maintain referential integrity.

This remains an implementation option.

---

# 128. No Duplicate Canonical Identity

A domain object SHALL not acquire separate identities merely because it appears in:

```text
relational store

graph projection

search index

vector store.
```

---

# 129. One Canonical ID Everywhere

The same:

```text
regrule_123
```

SHALL identify the rule across:

```text
PostgreSQL

events

graph projection

search

RDF export

logs

audit.
```

---

# 130. Provenance Traversal

Given:

```text
regdec_1
```

the system SHOULD traverse:

```text
Decision
   ↓
Assessment
   ↓
Effect
   ↓
RuleVersion
   ↓
Interpretation
   ↓
ProvisionVersion
   ↓
InstrumentExpression
   ↓
SourceArtefact
   ↓
RegulatorySource
   ↓
Authority.
```

---

# 131. Explanation Path

This path SHALL support a concise human explanation.

Example:

```text
Shipment blocked because:

Rule R17 prohibited the transaction.

R17 was derived from
Section 14(2) of Instrument I.

Section 14(2) was effective
on the assessment date.

Instrument I was issued by Authority A.
```

---

# 132. Explainability Path Selection

Where multiple provenance paths exist, the engine SHOULD choose:

```text
minimum sufficient authoritative explanation
```

for user display.

The complete graph remains available for deeper investigation.

---

# 133. Impact Traversal

Forward traversal SHALL support:

```text
Provision changed
     │
     ▼
Interpretations
     │
     ▼
Rules
     │
     ▼
Profiles
     │
     ▼
Effects
     │
     ▼
Assessments
     │
     ▼
Decisions
     │
     ▼
Orders / Shipments / Products / Entities.
```

---

# 134. Why Forward Traversal Matters

A regulation update is commercially valuable only if Baobab can determine:

> What does this change affect?

---

# 135. Regulatory Change Impact

Example:

```text
Tariff Schedule Item 0901 amended.
```

The graph MAY reveal:

```text
12 Product classifications

4 active suppliers

16 open quotations

8 orders

3 shipments

2 pricing models

1 customer market-entry assessment.
```

---

# 136. Impact Candidate versus Confirmed Impact

Graph reachability may indicate:

```text
MAY_AFFECT.
```

Detailed reassessment determines:

```text
ACTUALLY_AFFECTS.
```

The two SHALL remain distinct.

---

# 137. Graph Reachability Is Not Legal Applicability

An object being connected downstream does not prove its legal outcome changes.

Traversal identifies candidates.

The evaluation engine confirms consequences.

---

# 138. Impact Closure

`RegulatoryImpact` may use graph closure to identify potentially affected objects within bounded relationship types.

---

# 139. Bounded Impact Traversal

Example traversal relationship whitelist:

```text
AMENDS
→ INTERPRETS
→ DERIVES_RULE
→ INCLUDED_IN_PROFILE
→ USED_BY_ASSESSMENT
→ PRODUCED_DECISION
→ REFERENCES_SHIPMENT.
```

---

# 140. Avoid Arbitrary Impact Explosion

The system SHALL not treat every two-hop graph neighbour as impacted.

Impact semantics SHALL use relationship-specific rules.

---

# 141. Dependency Graph

Rule dependencies SHALL support:

```text
definition dependencies

calculation dependencies

normative dependencies

exception dependencies

classification dependencies.
```

---

# 142. Rule Dependency Impact

If:

```text
Definition D changes
```

all rules depending on D become candidate reassessment targets.

---

# 143. Concept Graph

Regulatory concepts MAY connect to:

```text
definitions

synonyms

jurisdiction-specific meanings

broader concepts

narrower concepts

external taxonomies.
```

---

# 144. Concept Identity Must Respect Jurisdiction

```text
IMPORTER
```

in regime A may not have the same legal meaning as:

```text
IMPORTER
```

in regime B.

The graph SHALL not merge them merely because their labels match.

---

# 145. `SAME_AS` Is Dangerous

A strong identity relationship such as:

```text
SAME_AS
```

SHALL require high assurance.

Prefer weaker:

```text
MAPS_TO

CORRESPONDS_TO

POSSIBLY_EQUIVALENT_TO
```

where exact identity is uncertain.

---

# 146. External Ontology Mapping

Baobab MAY map concepts to:

```text
ELI

WCO

LegalRuleML

other legal vocabularies.
```

Those mappings SHALL remain external semantic mappings.

---

# 147. Mapping Does Not Surrender Canonical Authority

A Baobab concept can map to an external ontology without adopting its external identifier as canonical.

---

# 148. Cross-Engine Graph References

The graph SHALL reference canonical Baobab objects from:

```text
Control Plane

Trade

ERP

CMS

IAM

Pulse
```

using Shared contracts/mappings.

---

# 149. No Cross-Database Foreign Keys Required

Polyrepo/polyglot architecture means canonical cross-engine references will usually be logical rather than database-level foreign keys.

---

# 150. Cross-Engine Relationship Verification

A relationship to external engine object SHOULD include enough context to verify:

```text
object exists

tenant matches

canonical ID valid

mapping active.
```

---

# 151. Business Object Snapshot

For historical assessment, Regulations MAY retain selected immutable facts from external objects.

It SHALL still reference the canonical original object.

---

# 152. Graph Ownership

Regulations owns:

```text
regulatory graph edges.
```

Trade does not directly write:

```text
Rule R APPLIES_TO Shipment S
```

into the canonical regulatory graph unless through an authorised Regulations contract.

---

# 153. Trade Event Input

Trade may publish:

```text
shipment created

product classified

destination changed.
```

Regulations consumes these facts and determines regulatory relationships.

---

# 154. Pulse Graph Boundary

Pulse owns its Intelligence Evidence Graph.

Regulations owns its Regulatory Knowledge Graph.

---

# 155. Cross-Graph Relationship

The graphs MAY connect through canonical references/events.

Example:

```text
RegulatoryChange C
     │
     ▼
Pulse Analysis A
```

but neither engine SHALL mutate the other's canonical graph.

---

# 156. Shared Graph Infrastructure

Future common graph infrastructure MAY be reused.

That SHALL not imply merged bounded contexts.

---

# 157. Graph Event Model

Important graph changes MAY emit events:

```text
regulation.relationship.created

regulation.relationship.verified

regulation.relationship.superseded

regulation.relationship.invalidated.
```

Exact Shared contracts remain deferred.

---

# 158. Event Payload

Graph events SHOULD identify:

```text
relationship ID

type

subject

object

scope

version

tenant

correlation

effective time.
```

---

# 159. Event Idempotency

Graph mutation events SHALL use stable event identity/version to support idempotent projection.

---

# 160. Graph Mutation Governance

A consequential relationship SHALL not be modified by:

```text
direct SQL

manual graph-database console edit

ad-hoc script
```

outside controlled migration/governance processes.

---

# 161. Changeset Alignment

Consequential graph changes such as:

```text
Rule A now overrides Rule B
```

SHOULD flow through the same controlled-mutation principles established by the Control Plane Changeset architecture.

---

# 162. Four-Eyes Relationships

Certain graph assertions SHOULD require maker-checker approval.

Examples:

```text
HAS_PRECEDENCE_OVER

REPEALS

DIRECT_EFFECT_RECOGNISED

LEGAL_POWER_GRANTED_TO.
```

---

# 163. Low-Risk Automated Edges

Some structural edges may be auto-generated.

Examples:

```text
SourceArtefact
EXTRACTED_TO
NormalisedSourceRecord.
```

---

# 164. AI Graph Construction

AI MAY automatically propose:

```text
potential citation

potential amendment

potential definition dependency

potential exception relationship.
```

It SHALL not silently publish legally consequential edges.

---

# 165. Graph Validation

The engine SHALL validate:

```text
allowed node-type pairs

required scope

required provenance

temporal consistency

tenant consistency

forbidden self-relations

cycle rules

relationship cardinality.
```

---

# 166. Example Constraint

```text
AMENDS
```

should ordinarily connect:

```text
Instrument/Provision
→
Instrument/Provision
```

not:

```text
Shipment
→
Authority.
```

---

# 167. Relationship Cardinality

Some relationships have cardinality constraints.

Example:

```text
Provision
BELONGS_TO
exactly one Instrument
```

for a canonical structural version.

---

# 168. Other Relationships Are Many-to-Many

```text
Rule
DERIVED_FROM
Provision
```

is explicitly N:M.

---

# 169. Graph Constraint Validation

Internal validation MAY be supplemented by SHACL in interoperability projections because SHACL is specifically designed to validate RDF graph structure.

---

# 170. Graph Consistency Is Not Legal Consistency

A graph can be structurally valid while containing:

```text
two contradictory verified interpretations.
```

That contradiction is substantive regulatory state.

It SHALL not be automatically deleted by structural validation.

---

# 171. Contradiction Is First-Class

The graph SHALL represent:

```text
CONFLICTS_WITH

CONTRADICTS

DISPUTES
```

where appropriate.

---

# 172. Conflicting Evidence

Evidence A may:

```text
SUPPORT
```

an interpretation.

Evidence B may:

```text
CONTRADICT
```

it.

Both SHALL remain visible.

---

# 173. Graph Should Preserve Minority Interpretation

If platform governance selects:

```text
Interpretation A
```

as operational default, alternative:

```text
Interpretation B
```

may remain as:

```text
REJECTED

MINORITY

TENANT_ALTERNATIVE

UNDER_REVIEW.
```

---

# 174. Historical Graph

Graph edges SHALL not be destructively overwritten merely because interpretation changed.

---

# 175. Supersession

Preferred:

```text
Relationship R1
    superseded_by
Relationship R2.
```

Not:

```text
UPDATE R1
SET target = new_target.
```

for semantic changes.

---

# 176. Graph Version

The system MAY expose a:

```text
graph_snapshot_id

graph_version
```

for reproducible assessment.

---

# 177. Assessment Graph Snapshot

A consequential assessment SHALL identify enough graph state to reproduce:

```text
rules

hierarchy

interpretations

source lineage

context mappings.
```

---

# 178. Snapshot Does Not Require Full Database Copy

It may consist of:

```text
rule-set fingerprint

relationship version IDs

knowledge timestamp

context snapshot.
```

---

# 179. Regulatory Graph Snapshot

For audits, the engine SHOULD be able to reconstruct a bounded subgraph around a decision.

---

# 180. Decision Evidence Subgraph

Example:

```text
Decision D
   │
   ▼
Assessment A
   │
   ├── Rule R1
   │      └── Provision P1
   │             └── Instrument I
   │                    └── Authority X
   │
   ├── Requirement Q
   │      └── Evidence E
   │
   └── Context
          ├── Entity L
          ├── Product P
          └── Shipment S.
```

---

# 181. Evidence Bundle Export

A bounded decision subgraph SHOULD eventually be exportable as:

```text
audit evidence bundle

machine-readable JSON

human-readable report

RDF where requested.
```

---

# 182. Graph Query for Audit

Example:

> Show every source, interpretation, rule and evidence artefact that contributed to Decision D.

This should require graph traversal, not manual forensic SQL.

---

# 183. Graph Query for Regulators

Potential enterprise feature:

> Show every open transaction affected by Regulation R.

---

# 184. Graph Query for Counsel

Potential:

> Which Baobab rules depend upon Provision P?

---

# 185. Graph Query for Product Manager

Potential:

> Which customer workflows depend on this regulatory pack?

---

# 186. Graph Query for Operations

Potential:

> Which shipments are blocked solely because of Requirement Q?

---

# 187. Graph Query for Security

Potential:

> Which private counsel interpretations are accessible to Tenant T?

---

# 188. Graph Query for Commercial Teams

Potential:

> Which subscribed customers would benefit from a newly supported jurisdiction pack?

The graph may inform commercial projections, but commercial entitlement remains a separate domain.

---

# 189. Graph Analytics

Future graph analytics MAY identify:

```text
high-dependency rules

single-source regulatory risk

high-impact authorities

regulatory bottlenecks

frequently contested provisions

clusters of related obligations.
```

---

# 190. Analytics Cannot Establish Law

Graph centrality or clustering SHALL never establish:

```text
authority

precedence

applicability.
```

---

# 191. Single-Source Risk

One useful graph-derived metric:

```text
Which E4 rules depend on only
one external source path?
```

This directly supports provider resilience.

---

# 192. Regulatory Concentration Risk

Another:

```text
Which operational decisions depend
on one interpretation?
```

---

# 193. Change Blast Radius

One of the graph's most valuable functions SHALL be calculation of regulatory change blast radius.

---

# 194. Blast Radius Example

```text
Provision P amended
       │
       ▼
3 Interpretations
       │
       ▼
7 Rules
       │
       ▼
4 Regulatory Profiles
       │
       ▼
19 active Obligations
       │
       ▼
42 open business objects
       │
       ▼
11 potentially affected decisions.
```

---

# 195. Candidate Blast Radius versus Confirmed Blast Radius

The graph produces:

```text
candidate impact.
```

The evaluation engine confirms:

```text
actual impact.
```

---

# 196. Regulations ↔ Pulse Differentiation

Regulations:

```text
Which transactions are legally affected?
```

Pulse:

```text
What commercial consequences follow?
```

---

# 197. Example

Regulations:

```text
Tariff amendment affects
coffee imports under codes X and Y.
```

Pulse:

```text
Gross-margin impact
for ZuriBeans may be Z%.
```

---

# 198. Graph-Driven Alerts

Change traversal may enable:

```text
alert affected tenant

alert legal entity

alert trade operations

alert compliance reviewer.
```

Notification architecture belongs to `ADR-REG-0024`.

---

# 199. Subscription Query

A future customer MAY subscribe semantically:

```text
notify me when any regulation affecting
Product Class X in jurisdictions A/B changes.
```

The graph makes this feasible.

---

# 200. Regulatory Digital Twin Concept

Baobab SHOULD NOT market this prematurely, but strategically the graph approaches a:

```text
regulatory digital twin
```

of a customer's legal operating environment:

```text
legal entities
markets
products
transactions
regimes
rules
obligations
evidence
decisions.
```

The term is optional; the architecture is substantive.

---

# 201. Knowledge Graph as Commercial Moat

Raw laws are broadly obtainable.

The harder-to-copy asset is:

```text
source
→ provision
→ interpretation
→ executable rule
→ applicability
→ obligation
→ evidence
→ decision
→ operational outcome.
```

This graph improves with every governed deployment.

---

# 202. Network Effects Without Data Leakage

Baobab MAY learn platform-wide:

```text
which provisions cause frequent ambiguity

which regulatory domains cause recurring review

which source feeds are unreliable
```

without exposing one tenant's private operational data to another.

---

# 203. Tenant Privacy

Graph analytics SHALL operate on appropriately isolated or aggregated data.

---

# 204. No Secret Cross-Tenant Edges

The engine SHALL NOT create:

```text
Tenant A Shipment
RELATED_TO
Tenant B Shipment
```

merely because they resemble each other.

---

# 205. Shared Legal Knowledge Is Different

Both tenants may reference:

```text
same public Regulation R.
```

That is allowed.

The operational objects remain isolated.

---

# 206. Graph Partition Strategy

Conceptually:

```text
PLATFORM REGULATORY GRAPH

        +

TENANT A PRIVATE OVERLAY

        +

TENANT B PRIVATE OVERLAY
```

rather than:

```text
one fully duplicated graph per tenant.
```

---

# 207. Benefits

This avoids:

```text
duplicating law

diverging rule versions

duplicating source acquisition.
```

---

# 208. Shared Graph Corrections

If shared legal knowledge is corrected:

```text
impact analysis
```

can identify affected tenant overlays without mutating private data.

---

# 209. Tenant Overrides

A tenant-specific interpretation SHALL be connected as an overlay edge.

It SHALL not edit the shared interpretation.

---

# 210. Graph Entitlement

Some graph nodes may belong to premium regulatory packs.

Entitlement determines access.

It SHALL not change legal meaning.

---

# 211. Licensing Filtering

Provider-derived annotations may require entitlement/license checks before traversal returns them.

---

# 212. Resolved Decision Independence

Where licence permits, a customer may receive:

```text
decision + citation
```

without full provider annotations.

---

# 213. Graph Consistency Events

The system SHOULD detect:

```text
dangling edge

unknown node

expired relationship

cross-tenant edge

invalid node-type pair

temporal contradiction

duplicate active relationship.
```

---

# 214. Graph Repair

Repairs SHALL be governed and auditable.

No invisible cleanup job should alter legal semantics.

---

# 215. Orphan Prevention

Published RuleVersions SHALL never become orphaned from:

```text
source/provision lineage
```

unless explicitly classified as authority-supplied self-contained machine rules with equivalent provenance.

---

# 216. Graph Garbage Collection

Historical regulatory nodes SHALL not be physically garbage-collected merely because they are no longer effective.

Retention policy governs eventual deletion where permitted.

---

# 217. Search Materialisation

Frequently traversed paths MAY be materialised.

Example:

```text
Decision
→ source provisions
```

can be cached.

The cache SHALL retain dependency/version metadata.

---

# 218. Materialised Path Invalidations

If any underlying relationship changes:

```text
cached explanation path
```

must be invalidated or versioned.

---

# 219. Closure Tables

A relational implementation MAY use:

```text
closure tables
```

for selected hierarchical relationships where performance warrants.

This is not required canonically.

---

# 220. Recursive CTEs First

Initial implementation SHOULD favour:

```text
recursive CTEs
+
well-indexed edge tables
```

for bounded graph traversal.

PostgreSQL 17 provides recursive-query and cycle-handling support suitable for these workloads.

---

# 221. Indexing

Likely indexes include:

```text
(source_node_id, relationship_type)

(target_node_id, relationship_type)

(valid_period)

tenant_scope

relationship status.
```

Exact schema remains implementation-specific.

---

# 222. JSONB Use

JSONB MAY store extensible relationship metadata where semantics do not justify first-class columns.

It SHALL NOT replace core typed fields.

---

# 223. PostgreSQL JSONB

PostgreSQL 17 supports GIN indexing for JSONB containment and path-style operators, making JSONB suitable for carefully bounded extensibility.

---

# 224. Do Not Build Entire Graph in JSONB

Rejected:

```text
node.properties JSONB

edge.properties JSONB
```

as the whole regulatory domain.

Core legal semantics deserve typed structures.

---

# 225. Graph API Versioning

Relationship vocabulary and graph-query APIs SHALL be versioned.

---

# 226. Backward Compatibility

Renaming:

```text
DERIVES_FROM
```

to:

```text
DERIVED_FROM
```

is not merely cosmetic once external consumers exist.

Graph predicates are contracts.

---

# 227. Ontology Version

The Regulatory Knowledge Graph SHOULD carry:

```text
ontology_version
```

or semantic-model version.

---

# 228. Ontology Migration

Changing the meaning of an existing relationship SHOULD require:

```text
new semantic version

migration

impact analysis.
```

---

# 229. Do Not Reinterpret Historical Edges Silently

Historical queries must use the semantic interpretation valid for their graph version where necessary.

---

# 230. Export Version

External RDF/JSON graph exports SHOULD identify:

```text
schema version

ontology version

snapshot time.
```

---

# 231. Graph Snapshot Fingerprint

A bounded graph export MAY carry a content fingerprint for audit.

---

# 232. Signing

High-value evidence bundles MAY eventually be cryptographically signed.

Signing confirms integrity.

It does not prove legal correctness.

---

# 233. Regulatory Graph API Security

Graph traversal endpoints are highly sensitive because relationship discovery can reveal:

```text
business activity

legal concerns

customer suppliers

disputes

regulatory exposure.
```

They SHALL therefore require explicit capability grants.

---

# 234. Query Authorization

Authorization SHALL evaluate:

```text
principal

tenant

legal entity scope

graph capability

node classification

relationship classification.
```

---

# 235. Traversal Authorization Is Per-Hop

A starting node being visible does not mean all reachable nodes are visible.

Every traversed node/edge SHALL respect authorization.

---

# 236. Prevent Inference Leakage

A consumer SHALL not infer a secret object from:

```text
hidden-edge count

relationship existence

error difference.
```

Sensitive traversal APIs should fail in ways that avoid unnecessary information disclosure.

---

# 237. Audit Queries

Consequential graph traversal SHOULD generate audit logs including:

```text
principal

purpose

root object

query type

tenant

time.
```

---

# 238. Graph Privacy Classification

Nodes and edges SHOULD support classification such as:

```text
PUBLIC

LICENSED

PLATFORM_INTERNAL

TENANT_PRIVATE

RESTRICTED

LEGAL_PRIVILEGED
```

where appropriate.

---

# 239. Legal Privilege

Tenant counsel material MAY be legally privileged.

Regulations SHALL therefore not casually include:

```text
counsel opinions
```

in broad search indexes or AI training/retrieval contexts.

---

# 240. AI Retrieval Boundary

AI retrieval SHALL receive only graph content permitted by:

```text
tenant

rights

classification

purpose.
```

---

# 241. Graph Retrieval Does Not Expand AI Authority

Access to:

```text
HAS_PRECEDENCE_OVER
```

does not entitle an LLM to rewrite it.

---

# 242. Explainability without AI

The canonical graph SHALL support deterministic decision explanation even if every generative model is unavailable.

---

# 243. AI Enhances Narrative Only

AI MAY transform graph evidence into:

```text
human-readable explanation
```

but the structural explanation exists independently.

---

# 244. API Failure

Failure of:

```text
graph search projection
```

SHALL not corrupt canonical Regulations state.

---

# 245. Projection Failure

If graph projection is stale:

```text
graph_exploration service
```

may degrade.

Transactional regulatory assessment may continue using canonical relational state where safe.

---

# 246. Dedicated Graph Database Promotion Criteria

A dedicated graph store SHOULD be considered only when measured requirements demonstrate one or more of:

```text
multi-hop traversal latency unacceptable in PostgreSQL

relationship counts materially exceed relational design targets

interactive graph exploration requires specialised indexes

impact analysis cannot meet SLOs

graph analytics becomes a core production workload.
```

---

# 247. Technology Promotion Requires ADR

Introducing a dedicated graph database as authoritative or production-critical infrastructure SHALL require a later technology ADR.

---

# 248. Technology Evaluation Criteria

Future evaluation SHOULD compare:

```text
consistency model

transaction support

temporal relationships

multi-tenancy

backup/recovery

query language

observability

managed-service availability

cost

vendor lock-in

operational skills

rebuildability.
```

---

# 249. Knowledge Graph Is Not a Reason to Abandon PostgreSQL

The conceptual graph and physical persistence technology solve different problems.

---

# 250. Example — ZuriBeans UG → ZA

Conceptually:

```text
Uganda
   │
   ▼
Regulatory Authority UG-A
   │
   ▼
Instrument UG-I
   │
   ▼
Provision UG-P
   │
   ▼
Interpretation UG-INT
   │
   ▼
Rule UG-R
   │
   ▼
Obligation:
Export documentation
   │
   ▼
Requirement:
Certificate C
   │
   ▼
Evidence:
Document E
```

and:

```text
South Africa
   │
   ▼
Authority ZA-A
   │
   ▼
Instrument ZA-I
   │
   ▼
Provision ZA-P
   │
   ▼
Rule ZA-R
   │
   ▼
Import Requirement
```

connected through:

```text
Shipment S
   │
   ├── origin → Uganda
   ├── destination → South Africa
   ├── product → Coffee P
   └── legal entity → ZuriBeans
```

---

# 251. Regional Regime Layer

The same graph may include:

```text
AfCFTA
    │
    ▼
Rules-of-Origin Provision
    │
    ▼
Origin Rule
    │
    ▼
Certificate Requirement
```

alongside national requirements.

---

# 252. Classification Connection

```text
Product P
    │
    ▼
Classification C
    │
    ▼
Tariff Rule R
```

The classification version remains explicit.

---

# 253. Assessment Subgraph

```text
Shipment S
   │
   ▼
Assessment A
   │
   ├── uses → UG-R
   ├── uses → ZA-R
   ├── uses → AF-R
   │
   ▼
Requirement Q1
Requirement Q2
Requirement Q3
   │
   ▼
Decision D.
```

---

# 254. Explain Decision Example

Query:

```text
Why is Shipment S on regulatory hold?
```

Traversal:

```text
Shipment S
  ← referenced_by
Assessment A
  → produced
Decision D
  → based_on
Requirement Q2
  → created_by
Rule ZA-R
  → derived_from
Provision ZA-P
  → contained_in
Instrument ZA-I
  → issued_by
Authority ZA-A.
```

---

# 255. Change Impact Example

Suppose:

```text
ZA-P
AMENDED_BY
ZA-P-v2.
```

Forward traversal identifies:

```text
ZA-R

assessments using ZA-R

open requirements

affected shipments.
```

Each then undergoes actual reassessment.

---

# 256. Supplier Impact Example

If an SPS requirement changes:

```text
Rule
   ↓
Product Class
   ↓
Supplier Product Offerings
   ↓
Open Orders
```

may produce candidate affected business objects.

---

# 257. Graph and Regulatory Packs

`ADR-REG-0029` can later define jurisdiction/regulatory packs as graph compositions.

Conceptually:

```text
UG–ZA Coffee Corridor Pack
       │
       ├── jurisdictions
       ├── regimes
       ├── authorities
       ├── profiles
       ├── rules
       └── sources.
```

---

# 258. Pack Is Not Copy

A pack references canonical graph objects.

It should not duplicate entire rule sets unnecessarily.

---

# 259. Commercial Entitlement

Entitlement may grant access to a graph composition.

It SHALL not create a second copy of law.

---

# 260. Graph-Based Coverage

Coverage can be measured by examining whether required paths exist:

```text
Jurisdiction
   ↓
Authority
   ↓
Instrument
   ↓
Rule
   ↓
Profile.
```

---

# 261. Coverage Is More Than Source Count

Having 1,000 downloaded laws does not prove useful coverage.

More meaningful coverage questions include:

```text
Are competent authorities mapped?

Are active instruments known?

Are provisions structured?

Are executable rules verified?

Are hierarchy relationships known?

Are source lineages complete?
```

---

# 262. Graph Completeness Metrics

Potential future metrics:

```text
rules_without_sources

rules_without_interpretations

rules_without_effective_dates

active_instruments_without_rules

relationships_without_provenance

E4_rules_with_single_source_path

decisions_without_complete_lineage.
```

---

# 263. Graph Quality Metrics

Additional metrics:

```text
orphan_nodes

dangling_edges

unverified_edges

conflicting_edges

stale_relationships

projection_lag

max_traversal_latency.
```

---

# 264. Relationship Review Backlog

The platform SHOULD measure:

```text
candidate consequential edges
awaiting verification.
```

This is an operational indicator of regulatory knowledge readiness.

---

# 265. Graph Health

A jurisdiction pack MAY expose:

```text
graph_health
```

as a multidimensional diagnostic.

It SHALL not become a simplistic claim:

```text
98% legally correct.
```

---

# 266. Graph Completeness and Enforcement

Insufficient graph completeness MAY cap decision authority.

Example:

```text
Rule itself verified
but hierarchy path unresolved
```

may reduce:

```text
E4 → E2.
```

---

# 267. Graph Changes and Rule Compilation

A change to:

```text
Rule source

Override relation

Exception relation

Definition dependency
```

MAY require recompilation of affected rule packages.

---

# 268. Dependency Closure for Compilation

The graph SHALL support:

```text
Rule R
   ↓
all upstream semantic dependencies.
```

That dependency set may form part of:

```text
rule compilation fingerprint.
```

---

# 269. Rule Fingerprint

A high-assurance compiled rule SHOULD incorporate fingerprints of material upstream dependencies.

Thus a changed definition cannot leave an apparently unchanged compiled rule silently active.

---

# 270. Graph and Caching

Cache keys SHOULD include:

```text
graph semantic version

rule-set version

relationship versions

effective time.
```

where material.

---

# 271. Cache Poisoning Prevention

Unverified graph relationships SHALL not pollute production evaluation caches.

---

# 272. Graph Reconciliation

Periodic reconciliation SHOULD detect mismatches between:

```text
canonical relational state
```

and:

```text
derived graph/search projections.
```

---

# 273. Canonical Wins

Where a projection disagrees with canonical state:

```text
canonical Regulations state wins.
```

---

# 274. Disaster Recovery

A derived graph store SHALL be rebuildable after loss.

The platform SHALL not require restoring proprietary graph state that cannot be reconstructed.

---

# 275. Backup Priority

Canonical regulatory database and immutable source artefacts are primary recovery assets.

Graph/search/vector projections are secondary where reconstructable.

---

# 276. Graph Schema Evolution

Node and relationship schemas SHALL evolve with migrations.

---

# 277. Unknown Relationship Types

An older consumer encountering a new relationship type SHOULD:

```text
ignore safely
```

unless that type is mandatory for its decision.

It SHALL not reinterpret unknown predicates.

---

# 278. Required Semantics

A rule package may declare:

```text
requires_relationship_semantics_version >= X.
```

If evaluator lacks support:

```text
UNSUPPORTED_SEMANTIC.
```

---

# 279. Interchange Export

Future export MAY support:

```text
JSON

JSON-LD

RDF/Turtle

N-Quads

other standards
```

where justified.

The canonical internal model remains format-neutral.

---

# 280. JSON-LD

JSON-LD may be attractive for external web interoperability while retaining JSON developer ergonomics.

This ADR does not mandate it.

---

# 281. RDF-Star / RDF 1.2 Caution

RDF 1.2 is currently at Candidate Recommendation stage in September 2026, so Baobab SHALL avoid making new RDF 1.2-specific capabilities a hard production dependency until the specification and implementation ecosystem mature.

---

# 282. GraphQL Is Not the Knowledge Graph

If Baobab later exposes GraphQL APIs:

```text
GraphQL
```

is an API query technology.

It is not the regulatory graph semantic model.

---

# 283. Relationship Provenance Example

```text
Rule R17
OVERRIDES
Rule R4

because:
Provision P17 contains explicit exception

verified by:
Reviewer V

effective:
2026-07-01 onward

scope:
Product Class X
in Jurisdiction ZA.
```

This relationship itself is valuable knowledge.

---

# 284. Qualified Edge Example

```text
rel_001
type:
HAS_PRECEDENCE_OVER

source:
regrule_A

target:
regrule_B

scope:
  jurisdiction: ZA
  domain: CUSTOMS

valid_time:
  [2026-07-01, ...)

basis:
  provision_123

verification:
  VERIFIED
```

---

# 285. Decision Graph Example

```text
regdec_77
  │
  ├── PRODUCED_FROM → regassess_53
  │
  ├── ENFORCED_BY → baobab-trade
  │
  └── REFERENCES → shipment_900
```

---

# 286. Enforcement Receipt Relationship

```text
Decision
    │
    ▼
ENFORCED_BY
    │
    ▼
EnforcementReceipt
    │
    ▼
Shipment.
```

Regulations need not own the Shipment.

---

# 287. Outcome Relationship

Operational systems MAY later return:

```text
CLEARED_BY_CUSTOMS

REJECTED_BY_AUTHORITY

DOCUMENT_ACCEPTED.
```

These can link back to regulatory decisions as feedback evidence.

---

# 288. Outcome Does Not Rewrite Law

A customs officer accepting one shipment does not automatically create a general RuleVersion.

---

# 289. Repeated Outcomes May Trigger Research

Many operational outcomes inconsistent with Baobab's rule may trigger:

```text
rule review

source investigation

interpretation review.
```

---

# 290. Feedback Promotion

Operational evidence must pass governance before changing canonical regulatory meaning.

---

# 291. Rejected Alternative — Document Folder

Rejected.

Files alone cannot provide deterministic provenance or impact traversal.

---

# 292. Rejected Alternative — Search Index as Knowledge Graph

Rejected.

Search ranking lacks legal relationship semantics.

---

# 293. Rejected Alternative — Vector Database as Knowledge Graph

Rejected.

Semantic similarity does not establish legal relationships.

---

# 294. Rejected Alternative — Generic Triple Store as Entire Domain

Rejected.

It weakens core domain constraints and transactional integrity.

---

# 295. Rejected Alternative — Dedicated Graph Database Immediately

Rejected absent measured need.

---

# 296. Rejected Alternative — All Relationships as Foreign Keys Only

Rejected.

Many legal relationships are:

```text
N:M

scoped

temporal

versioned

provenance-bearing.
```

---

# 297. Rejected Alternative — `RELATED_TO`

Rejected for consequential regulatory knowledge.

---

# 298. Rejected Alternative — Edges Have No Provenance

Rejected.

Legal relationships themselves may be contested.

---

# 299. Rejected Alternative — Edges Are Mutable

Rejected for material semantic state.

Supersession/versioning preserves history.

---

# 300. Rejected Alternative — Shared Law Duplicated per Tenant

Rejected.

Use shared graph + tenant overlays.

---

# 301. Rejected Alternative — Tenant Interpretation Mutates Shared Rule

Rejected.

Overlay semantics preserve isolation and provenance.

---

# 302. Rejected Alternative — Graph Reachability Means Applicability

Rejected.

Traversal finds candidates.

Evaluation determines applicability.

---

# 303. Rejected Alternative — AI Similarity Creates Legal Edge

Rejected.

AI may propose candidate relationships only.

---

# 304. Rejected Alternative — Centrality Determines Authority

Rejected.

Graph analytics cannot establish legal force.

---

# 305. Rejected Alternative — One Graph View for Everyone

Rejected.

Research, production, historical and tenant-scoped views differ.

---

# 306. Rejected Alternative — Unbounded Public Graph Query

Rejected.

Task-oriented APIs and bounded internal traversal are safer.

---

# 307. Rejected Alternative — Graph Projection Is System of Record

Rejected unless separately authorised by later ADR.

---

# 308. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-G-I01` | The Regulatory Knowledge Graph SHALL be a semantic architecture, not a database mandate |
| `REG-G-I02` | Canonical graph identity SHALL use Baobab canonical IDs |
| `REG-G-I03` | Provider-native IDs SHALL remain external references |
| `REG-G-I04` | Consequential relationships SHALL use typed semantics |
| `REG-G-I05` | `RELATED_TO` SHALL not replace known consequential semantics |
| `REG-G-I06` | Direction of consequential relationships SHALL be defined |
| `REG-G-I07` | Scope SHALL be explicit where relationship applicability is limited |
| `REG-G-I08` | Effective time SHALL be representable on legally consequential relationships |
| `REG-G-I09` | Material relationships SHALL retain provenance |
| `REG-G-I10` | Consequential relationship assertions SHALL be versionable/supersedable |
| `REG-G-I11` | Complex n-ary legal relationships SHALL not be flattened when material meaning would be lost |
| `REG-G-I12` | Shared regulatory knowledge SHALL not be duplicated per tenant without need |
| `REG-G-I13` | Tenant-private graph state SHALL remain isolated |
| `REG-G-I14` | Tenant overlays SHALL not mutate platform-shared law |
| `REG-G-I15` | Search indexes SHALL remain derived |
| `REG-G-I16` | Vector stores SHALL remain derived |
| `REG-G-I17` | Dedicated graph stores SHALL initially remain derived projections |
| `REG-G-I18` | Canonical state SHALL remain rebuildable without a graph projection |
| `REG-G-I19` | Graph reachability SHALL not itself establish regulatory applicability |
| `REG-G-I20` | AI-suggested consequential edges SHALL require governance before publication |
| `REG-G-I21` | Conflict and contradiction SHALL remain representable |
| `REG-G-I22` | Historical graph relationships SHALL remain reconstructable |
| `REG-G-I23` | Cross-engine objects SHALL be referenced, not re-owned |
| `REG-G-I24` | Traversal SHALL respect tenant, entitlement, licensing and classification boundaries |
| `REG-G-I25` | Every consequential Decision SHALL be traversable backward to its legal source |
| `REG-G-I26` | Regulatory changes SHALL be traversable forward to candidate affected objects |
| `REG-G-I27` | Graph projection lag SHALL be observable |
| `REG-G-I28` | Projection failure SHALL not silently alter canonical regulatory state |
| `REG-G-I29` | Graph ontology/predicate evolution SHALL be versioned |
| `REG-G-I30` | Legal relationship meaning SHALL remain independent of graph technology |

---

# 309. Minimum Implementation Proof

Before `ADR-REG-0010` is considered implemented, Baobab SHOULD demonstrate:

```text
1.
Authority → Instrument relationship.

2.
Instrument → Provision hierarchy.

3.
ProvisionVersion → Interpretation.

4.
Interpretation → RuleVersion.

5.
One Rule derived from several Provisions.

6.
One Provision supporting several Rules.

7.
Rule → Exception relationship.

8.
Verified Rule override relationship.

9.
Scoped precedence relationship with
jurisdiction and effective date.

10.
Regime membership relationship.

11.
Authority delegation relationship.

12.
Requirement → Evidence relationship.

13.
Assessment → Rule relationships.

14.
Decision → Assessment relationship.

15.
Decision → operational object reference.

16.
Backward explanation traversal
Decision → Authority.

17.
Forward change traversal
Provision → affected Assessments.

18.
Cycle-safe recursive traversal.

19.
Tenant overlay interpretation.

20.
Cross-tenant traversal rejection.

21.
Licensed source relationship hidden
from unauthorised consumer.

22.
Candidate AI relationship separated
from published relationship.

23.
Relationship supersession preserving history.

24.
Historical graph reconstruction.

25.
Relational recursive traversal under
defined performance budget.

26.
Rebuildable graph projection.

27.
Search projection rebuilt from canonical state.

28.
RDF/JSON graph export for a bounded subgraph.

29.
Structural graph validation.

30.
Graph impact result that distinguishes
MAY_AFFECT from CONFIRMED_IMPACT.
```

---

# 310. Initial PostgreSQL-Oriented Implementation

Without pre-empting later technical design, the first implementation SHOULD be compatible with:

```text
PostgreSQL 17
```

using:

```text
typed canonical tables

relationship tables

effective-time ranges

recursive CTEs

appropriate B-tree/GiST/GIN indexes

immutable/versioned records

JSONB only for bounded extension metadata.
```

PostgreSQL 17 provides recursive CTEs for hierarchical/graph-like traversal and native range/multirange types suitable for effective-time modelling.

---

# 311. Initial Relationship Table Concept

Illustrative:

```text
RegulatoryRelationship
──────────────────────────────
relationship_id

relationship_type

source_node_id

target_node_id

valid_period

recorded_at

tenant_scope

verification_state

provenance_id

superseded_by

metadata
```

This is not yet a physical-schema decision.

---

# 312. Specialised Relationship Tables

Complex relationships MAY deserve explicit structures:

```text
PrecedenceRelationship

AuthorityDelegation

RegimeMembership

RuleDerivation

EvidenceSatisfaction

RegulatoryImpactRelation.
```

---

# 313. Graph Projection Phase

A dedicated graph projection SHOULD only be introduced after:

```text
real dataset

measured traversal patterns

measured PostgreSQL performance

documented SLO requirement.
```

---

# 314. Graph Database Trigger

Potential trigger:

```text
95th-percentile multi-hop impact query
cannot meet required SLO
despite reasonable relational optimisation.
```

Then a separate ADR evaluates specialised graph technology.

---

# 315. Commercial Capability — Regulatory Explainability

The graph enables a premium capability:

> **Explain exactly why this transaction received this regulatory decision.**

---

# 316. Commercial Capability — Regulatory Impact

Another:

> **Tell me which of my products, suppliers, orders and shipments are affected by this change.**

---

# 317. Commercial Capability — Regulatory Dependency Map

Another:

> **Show every active business process dependent upon this regulation.**

---

# 318. Commercial Capability — Audit Evidence

Another:

> **Produce the complete evidence chain for this decision as it existed on the decision date.**

---

# 319. Commercial Capability — Market Entry Graph

Another:

```text
New Market
   ↓
Regimes
   ↓
Authorities
   ↓
Applicable Rules
   ↓
Licences
   ↓
Requirements
   ↓
Readiness Gaps.
```

---

# 320. Commercial Capability — Regulatory Change Blast Radius

This is likely to become one of the strongest Regulations/Pulse combined features:

```text
Regulation changed
        │
        ▼
Baobab Regulations:
what is legally affected?
        │
        ▼
Baobab Pulse:
what does it mean commercially?
```

---

# 321. Moat Formation

Every verified relationship improves the platform's structured regulatory knowledge.

Unlike raw document acquisition, many of these relationships require:

```text
legal interpretation

context modelling

operational integration

verification

historical outcome data.
```

That makes the graph progressively more expensive for competitors to reproduce.

---

# 322. But Graph Size Is Not the Moat

The moat SHALL NOT be marketed as:

```text
"We have 100 million graph edges."
```

The valuable measure is:

```text
correct
source-backed
applicable
operationally useful
relationships.
```

---

# 323. Quality Over Density

A sparse verified graph is superior to:

```text
dense AI-generated pseudo-legal relationships.
```

---

# 324. Regulatory Graph Flywheel

```text
Source acquisition
       │
       ▼
Structured provisions
       │
       ▼
Verified interpretations
       │
       ▼
Executable rules
       │
       ▼
Transaction assessments
       │
       ▼
Operational outcomes
       │
       ▼
Impact / quality feedback
       │
       ▼
Better regulatory graph.
```

---

# 325. Graph and Profitability

The graph supports recurring revenue because customers can continuously consume:

```text
decisions

change monitoring

obligation monitoring

impact analysis

audit evidence

market-entry assessments

regulatory APIs.
```

A static legal database is easier to replace.

An operational regulatory dependency graph becomes embedded infrastructure.

---

# 326. Follow-On ADRs

This ADR directly enables:

```text
ADR-REG-0011
Authoritative Source Registry
and Source Trust Model
```

which SHALL define the graph's source authority and trust semantics in detail.

Then:

```text
ADR-REG-0012
Regulatory Content Acquisition,
Licensing and Reuse Rights
```

and:

```text
ADR-REG-0014
Provenance, Citation
and Evidentiary Chain
```

will deepen two major relationship families introduced here.

Later:

```text
ADR-REG-0023
Regulatory Change Detection
and Impact Analysis
```

will make heavy use of forward graph traversal.

---

# 327. Research Foundation Summary

W3C PROV provides a mature conceptual foundation for provenance through entities, activities, agents and derivation relationships.

ELI v1.5 provides an established legislation metadata model and reinforces stable legal-resource identification independent of representation.

LegalRuleML explicitly requires traceability between machine-processable norms and their authoritative textual legal sources, directly validating source-to-rule graph lineage.

Stable RDF 1.1 provides a mature external graph interchange model, while RDF 1.2 remains in Candidate Recommendation work as of September 2026; consequently Baobab should preserve RDF interoperability without coupling canonical persistence to the evolving specification.

SHACL provides a mature W3C mechanism for graph-constraint validation and may be useful for validating exported RDF views.

PostgreSQL 17 provides recursive CTEs, cycle-aware traversal approaches, temporal range types and indexable structured data facilities sufficient to justify a relational-first authoritative graph implementation before introducing specialised graph infrastructure.

---

# 328. Final Decision

Baobab Regulations SHALL establish a **typed, temporal, provenance-rich Regulatory Knowledge Graph** whose canonical relationship chain is:

```text
                          AUTHORITY
                              │
                              ▼
                            REGIME
                              │
                              ▼
                          INSTRUMENT
                              │
                              ▼
                          PROVISION
                              │
                              ▼
                        INTERPRETATION
                              │
                              ▼
                             RULE
                              │
               ┌──────────────┼───────────────┐
               ▼              ▼               ▼
           EXCEPTION      OVERRIDE         DEFINITION
               │              │               │
               └──────────────┼───────────────┘
                              ▼
                     REGULATORY EFFECT
                              │
                              ▼
                        REQUIREMENT
                              │
                              ▼
                           EVIDENCE
                              │
                              ▼
                         ASSESSMENT
                              │
                              ▼
                          DECISION
                              │
                              ▼
                    OPERATIONAL OBJECT
```

surrounded by:

```text
Jurisdiction

Competence

Hierarchy

Regime Membership

Source Provenance

Temporal Validity

Tenant Scope

Regulatory Change

Impact.
```

The graph SHALL permit two primary directions:

```text
BACKWARD

Decision
→ Rule
→ Provision
→ Instrument
→ Authority

"Why?"
```

and:

```text
FORWARD

Provision Change
→ Rules
→ Assessments
→ Decisions
→ Shipments / Products / Entities

"What is affected?"
```

The architectural doctrine is:

> **Every consequential regulatory conclusion should be traceable backward to authority and forward to impact.**

Baobab SHALL achieve this without prematurely equating:

```text
knowledge graph
```

with:

```text
graph database.
```

The first implementation SHALL favour:

```text
strongly typed relational canonical state
+
first-class relationships
+
recursive traversal
+
derived search/vector/graph projections.
```

A dedicated graph database may come later if measured workloads justify it.

The strategic objective is not to produce a visually impressive graph.

It is to create a durable platform asset capable of answering:

> **What regulation controls this decision?**

> **Why?**

> **Which evidence proves it?**

> **What depends on it?**

> **What changes if the regulation changes?**

Once Baobab can answer those questions reliably across every tenant, legal entity, market, product, transaction and regulatory regime, `baobab-regulations` becomes substantially harder to replace than a legal search product or compliance API.

That is the purpose of `ADR-REG-0010`.

---

## Decision Summary

```text
ADR-REG-0010
────────────────────────────────────────────

CORE DECISION

Build a logical Regulatory
Knowledge Graph.

NOT:

"Install a graph database."


PRIMARY PATH

Authority
 → Instrument
 → Provision
 → Interpretation
 → Rule
 → Effect
 → Requirement
 → Evidence
 → Assessment
 → Decision
 → Business Object


BACKWARD TRAVERSAL

Decision
 → Source

answers:

WHY?


FORWARD TRAVERSAL

Regulatory Change
 → Business Impact

answers:

WHAT IS AFFECTED?


EDGE MODEL

Typed
Directed
Scoped
Temporal
Versioned
Provenance-backed
Tenant-aware


IMPORTANT EDGE FAMILIES

Authority
Lifecycle
Derivation
Normative
Hierarchy
Applicability
Evidence
Decision
Context
Impact
Identity


COMPLEX RELATIONSHIPS

Use qualified relationship
objects / hyperedges when
scope, time or provenance
cannot be represented safely
by a simple pair.


TENANCY

Shared public regulatory graph

+

Tenant-private overlays.


PERSISTENCE

Initial authoritative store:
relational-first.

PostgreSQL 17 can support:
recursive traversal
cycle handling
temporal ranges
structured indexing.


DERIVED PROJECTIONS

Search
Vector
RDF
Dedicated graph store

remain rebuildable.


NO FALSE SEMANTICS

Graph reachability
≠ applicability

Similarity
≠ legal relationship

Centrality
≠ authority

AI suggestion
≠ verified edge


STRATEGIC ASSET

Source
→ Meaning
→ Rule
→ Context
→ Decision
→ Outcome


COMMERCIAL RESULT

Explainability
Impact analysis
Audit evidence
Regulatory monitoring
Market-entry readiness
Dependency mapping
become native platform
capabilities.
```
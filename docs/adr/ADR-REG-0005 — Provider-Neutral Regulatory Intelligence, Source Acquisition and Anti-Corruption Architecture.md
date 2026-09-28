# ADR-REG-0005 — Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0005`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Decision Type:** Regulatory Source, Provider-Neutrality, Acquisition and Anti-Corruption Architecture  
**Date:** 2026-09-27  
**Strategic Classification:** Platform Differentiator / Regulatory Infrastructure  
**Parent Decisions:**

- `ADR-REG-0001 — Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary`
- `ADR-REG-0002 — Baobab Regulations as a Headless Platform Engine and Capability Provider`
- `ADR-REG-0003 — Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary`
- `ADR-REG-0004 — Advisory, Review and Enforcement Decision Classes`

**Related Baobab Architecture:**

- `ADR-PULSE-003 — External Source Adapter, Intelligence Acquisition and Commercial Research Fabric`
- `ADR-PULSE-004 — Raw Acquisition, Immutable Evidence and Research Reproducibility`
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- `ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture`
- `ADR-PULSE-010 — Embedding Deepset Haystack as Pulse's Headless AI Orchestration Engine`
- `ADR-SHARED-012 — Topology Identifiers and External System Registry`
- `ADR-SHARED-013 — External References and Canonical Mapping Administration`
- applicable Control Plane capability, provider, topology, isolation and mapping ADRs

**Primary Architectural Principle:**

> **Baobab owns regulatory semantics, context, provenance and execution. External providers supply evidence, content or specialised services.**

---

# 1. Executive Decision

Baobab Regulations SHALL implement a **provider-neutral Regulatory Source Fabric** through which regulatory material is:

```text
discovered
registered
acquired
preserved
validated
classified
normalised
mapped
versioned
verified
interpreted
and promoted
```

without permitting any external source, data vendor, AI provider, scraping framework, regulatory API or document format to become the canonical Baobab regulatory model.

The governing architecture SHALL be:

```text
                    REGULATORY WORLD

 Government     Regional       Standards      Courts
 Authorities    Bodies         Bodies         / Rulings
      │            │              │               │
      └────────────┼──────────────┼───────────────┘
                   │
          Commercial Providers
                   │
          Customer / Partner Sources
                   │
                   ▼
       ┌───────────────────────────┐
       │ REGULATORY SOURCE FABRIC  │
       │                           │
       │ Source Registry           │
       │ Provider Registry         │
       │ Rights & Access Policy    │
       │ Adapter Boundary          │
       │ Acquisition               │
       │ Raw Evidence              │
       │ Structural Validation     │
       │ Normalisation             │
       │ Authority Resolution      │
       │ Provenance                │
       └──────────────┬────────────┘
                      │
          ANTI-CORRUPTION BOUNDARY
                      │
                      ▼
          BAOBAB REGULATORY MODEL
                      │
         ┌────────────┼─────────────┐
         ▼            ▼             ▼
     Instruments   Provisions      Rules
         │            │             │
         └────────────┼─────────────┘
                      ▼
                Applicability
                      │
                      ▼
                  Decision
```

The foundational invariant is:

```text
Provider Schema
      ≠
Baobab Regulatory Schema
```

A second is:

```text
Content Provider
      ≠
Regulatory Authority
```

A third is:

```text
Source Acquisition
      ≠
Source Verification
      ≠
Rule Publication
```

---

# 2. Strategic Decision

Baobab SHALL **not attempt to win by owning the largest proprietary regulatory corpus**.

That market already contains mature organisations with enormous collection operations.

Thomson Reuters currently markets continuously updated global trade content covering more than 220 countries and territories, with more than 150 researchers monitoring over 1,300 government sources and Content APIs capable of embedding regulatory information into enterprise systems.

RegGenome provides structured, machine-readable regulatory requirements linked back to source text, currently describing a corpus of millions of documents across more than 55 jurisdictions.

FiscalNote now exposes policy intelligence through enterprise APIs and, since March 2026, an MCP interface designed specifically for AI agents and enterprise workflows.

Therefore the economically rational Baobab strategy is:

```text
BUY / INTEGRATE
where excellent regulatory content already exists

BUILD
where Baobab differentiation exists

OWN
the canonical regulatory execution architecture
```

---

# 3. What Baobab Must Own

Baobab SHALL own:

```text
canonical regulatory identity

authority relationships

jurisdiction semantics

source provenance

source-rights metadata

temporal semantics

regulatory interpretation

machine-executable rule semantics

applicability

Baobab Context integration

regulatory assessments

decision effects

change impact

cross-engine contracts

regulatory evidence lineage
```

Baobab SHOULD NOT require ownership of every source document or every regulatory data feed.

---

# 4. What Baobab May Buy

Baobab MAY procure:

```text
structured regulatory content

tariff data

HS classification content

rules-of-origin data

sanctions/restricted-party data

legal databases

regulatory change feeds

commercial research

translation

document extraction

OCR

specialist legal taxonomies

machine-readable standards

government data aggregation
```

when buying provides superior:

```text
coverage

accuracy

speed

maintenance

economics

licensing clarity
```

to building internally.

---

# 5. Commercial Moat

The intended moat is not:

```text
"We downloaded more PDFs."
```

It is:

```text
Multiple authoritative and commercial sources
                    │
                    ▼
          Baobab Source Fabric
                    │
                    ▼
      Canonical Regulatory Knowledge
                    │
                    ▼
            Baobab Context
                    │
                    ▼
            Applicability
                    │
                    ▼
              Decision
                    │
                    ▼
          Operational Action
```

The provider can change.

The Baobab decision model remains.

---

# 6. OECD Strategic Validation

The OECD's current Law-as-Code consultation explicitly identifies duplicated translations of legal logic across government agencies, technology vendors and service providers as creating:

```text
duplication
inconsistent implementation
limited interoperability
limited transparency
provider dependency
```

and advocates shared, traceable machine-executable legal infrastructure while preserving authoritative legal texts.

Baobab SHALL design directly against the identified **provider-dependency problem**.

---

# 7. Meaning of "Regulatory Intelligence" in This ADR

The term:

```text
Regulatory Intelligence
```

SHALL mean:

> the acquisition, structuring, monitoring, contextualisation and change-awareness of regulatory information required to support Baobab Regulations.

It SHALL NOT mean the broader:

```text
commercial intelligence
market intelligence
strategic intelligence
forecasting
opportunity discovery
```

owned by Baobab Pulse.

---

# 8. Pulse and Regulations Acquisition Boundaries

Both Pulse and Regulations need external information.

Their semantic treatment differs.

```text
PULSE SOURCE FABRIC

Evidence
   ↓
Observation
   ↓
Analysis
   ↓
Insight


REGULATIONS SOURCE FABRIC

Regulatory Evidence
   ↓
Authority / Instrument
   ↓
Provision
   ↓
Interpretation
   ↓
Rule
   ↓
Applicability
```

They MAY share infrastructure patterns.

They SHALL NOT share canonical domain ownership.

---

# 9. Reuse Architecture, Not Domain Semantics

Baobab Regulations SHOULD reuse organisational patterns already proven by Pulse:

```text
Source Registry

Adapter boundary

Raw evidence preservation

Content hashing

Acquisition runs

Provider isolation

Provenance

Versioning

anti-corruption layers
```

But Regulations SHALL add stricter treatment of:

```text
legal authority

legal force

effective date

jurisdiction

amendment

repeal

interpretation

licensing

enforcement eligibility
```

---

# 10. Source Fabric

The logical **Regulatory Source Fabric** SHALL comprise:

```text
Source Discovery
       │
       ▼
Source Registration
       │
       ▼
Provider / Authority Resolution
       │
       ▼
Rights & Access Validation
       │
       ▼
Source Adapter
       │
       ▼
Acquisition
       │
       ▼
Raw Evidence Vault
       │
       ▼
Structural Validation
       │
       ▼
Source-Native Record
       │
       ▼
Normalised Source Record
       │
       ▼
Canonical Regulatory Mapping
       │
       ▼
Verification / Interpretation
```

---

# 11. Source Fabric Is Logical

"Fabric" SHALL NOT imply:

```text
service mesh

peer-to-peer network

distributed database

microservice topology
```

It describes the governed collection of sources, providers, adapters, acquisition pipelines and evidence.

---

# 12. Foundational Source Concepts

The domain SHALL distinguish at least:

```text
RegulatorySourceProvider

RegulatoryAuthority

RegulatorySource

RegulatoryEndpoint

RegulatoryDataset

RegulatoryDistribution

RegulatoryFeed

SourceAdapter

AcquisitionPlan

AcquisitionRun

SourceArtefact

ProviderNativeRecord

NormalisedSourceRecord

SourceCoverageProfile

SourceAccessProfile

SourceRightsProfile

SourceFreshnessPolicy
```

Exact schemas are deferred.

---

# 13. Provider Is Not Authority

This distinction is mandatory.

Example:

```text
Provider:
Thomson Reuters

Authority:
SARS

Content:
South African tariff requirement
```

Thomson Reuters may:

```text
collect
validate
structure
translate
enrich
distribute
```

the information.

It does not thereby become:

```text
South African sovereign authority.
```

---

# 14. Another Provider Example

```text
Provider:
RegGenome

Underlying authority:
Regulator X

RegGenome representation:
structured obligation

Baobab:
canonical mapping + applicability
```

The source chain remains explicit.

---

# 15. Provider Can Also Be Authority

Sometimes the provider and authority ARE the same organisation.

Example:

```text
Provider:
SARS API / website

Authority:
SARS
```

The model SHALL support this.

It SHALL not assume it.

---

# 16. Source Is Not Provider

One provider can expose many regulatory sources.

Example:

```text
Provider:
commercial vendor

Sources:
ZA customs
UG customs
EAC
EU
UK
US
```

Likewise, one regulatory source may be available through several providers.

---

# 17. Source Multiplicity

Example:

```text
SARS tariff schedule
       │
       ├── SARS website
       ├── commercial provider A
       ├── commercial provider B
       └── authorised internal snapshot
```

Baobab SHALL be capable of recognising them as representations of related underlying regulatory material.

---

# 18. Source Provider Registry

Baobab Regulations SHALL maintain a governed provider registry or provider-domain projection.

Conceptually:

```text
RegulatorySourceProvider
├── provider_id
├── provider_key
├── provider_type
├── canonical_name
├── ownership
├── access_methods[]
├── commercial_relationship?
├── service_regions[]
├── lifecycle_status
├── security_profile
├── contact_reference?
└── metadata
```

---

# 19. Provider Types

Initial conceptual types MAY include:

```text
PUBLIC_AUTHORITY

INTERGOVERNMENTAL

REGIONAL_BODY

STANDARDS_BODY

JUDICIAL

COMMERCIAL_REGULATORY_DATA

PROFESSIONAL_INFORMATION

TENANT_SUPPLIED

PARTNER_SUPPLIED

INTERNAL_BAOBAB

DISCOVERY_ONLY
```

Provider type SHALL not define legal authority.

---

# 20. External Systems Registry Alignment

Where an external provider becomes a persistent Baobab integration, its external system identity SHOULD be governed consistently with `ADR-SHARED-012`.

Baobab SHALL NOT invent provider namespaces independently in every adapter.

---

# 21. Provider Registration Is Governed

A new production provider SHALL require explicit registration.

It SHALL NOT enter production merely because a developer adds:

```text
requests.get("https://...")
```

to application code.

---

# 22. Provider Registration Is Architecture State

Registration SHOULD identify:

```text
provider

purpose

source categories

approved adapter

access mechanism

authentication

rights basis

security classification

coverage

freshness expectation

operational owner
```

---

# 23. RegulatorySource

`RegulatorySource` SHALL represent the logical source of regulatory information.

Conceptually:

```text
RegulatorySource
├── source_id
├── source_key
├── authority_ref?
├── provider_ref
├── title
├── source_type
├── jurisdiction_refs[]
├── regulatory_domains[]
├── canonical_uri?
├── official_status
├── publication_model
├── language[]
├── coverage
├── rights_profile
├── freshness_policy
├── trust_profile
└── lifecycle_state
```

---

# 24. Source Is Logical, Endpoint Is Physical

This distinction SHALL be explicit.

```text
RegulatorySource:
South African tariff schedule

RegulatoryEndpoint:
https://...
```

The endpoint may change.

Source identity should remain stable.

---

# 25. Endpoint Rotation

If SARS moves a website:

```text
old URL
   ↓
new URL
```

Baobab SHOULD update the endpoint.

It SHALL NOT mint an entirely new regulatory source merely because the URL changed.

---

# 26. RegulatoryEndpoint

Conceptually:

```text
RegulatoryEndpoint
├── endpoint_id
├── source_id
├── access_type
├── uri
├── authentication_profile?
├── media_types[]
├── protocol
├── pagination_model?
├── rate_limit_policy?
├── availability_state
└── valid_period
```

---

# 27. Access Types

Expected:

```text
REST_API

GRAPHQL_API

MCP

DATA_DOWNLOAD

RSS_ATOM

SFTP

OBJECT_FEED

WEB_PAGE

DOCUMENT_PORTAL

EMAIL_FEED

MANUAL_UPLOAD

SIGNED_PACKAGE

WEBHOOK

OTHER
```

The architecture SHALL not assume every regulator has an API.

---

# 28. Africa Requires Format Tolerance

Many high-value regulatory sources may still arrive through:

```text
PDF

Gazette scan

XLSX

CSV

HTML table

email notice

manual portal

downloadable ZIP

web page
```

Baobab SHALL design for that reality.

Provider-neutrality is meaningless if it only works with polished REST APIs.

---

# 29. Data Service Concepts

W3C DCAT 3 provides useful distinctions among:

```text
Dataset

Distribution

DataService

DatasetSeries

CatalogRecord
```

and supports metadata concerning:

```text
access

licence

rights

format

versions

release dates
```

for heterogeneous catalogued resources.

Baobab SHOULD borrow these concepts where they improve source interoperability.

It SHALL NOT require RDF/DCAT as its internal persistence model.

---

# 30. RegulatoryDataset

A source MAY expose a dataset.

Examples:

```text
tariff schedule

restricted-goods table

sanctions list

permit register

gazette archive

regulatory notices collection
```

The dataset identity SHALL remain separate from individual distributions.

---

# 31. Distribution

One dataset MAY be distributed as:

```text
CSV

XLSX

JSON API

XML

PDF
```

Baobab SHOULD model those distributions separately.

This follows the useful dataset/distribution distinction in DCAT.

---

# 32. Dataset Series

Repeated publications MAY form a series.

Example:

```text
Government Gazette
 ├── issue 1
 ├── issue 2
 ├── issue 3
 └── ...
```

or:

```text
monthly tariff amendment series
```

Dataset-series semantics SHOULD be representable.

---

# 33. SourceAdapter

Every external provider SHALL integrate through an adapter/anti-corruption boundary.

Conceptually:

```text
interface RegulatorySourceAdapter:
    discover(...)
    acquire(...)
    acquire_since(...)
    retrieve_by_id(...)
    verify_integrity(...)
    describe_coverage(...)
    describe_rights(...)
    health(...)
```

This is illustrative.

---

# 34. Adapter Responsibility

The adapter MAY know:

```text
vendor endpoint

vendor authentication

vendor pagination

vendor field names

vendor error codes

vendor throttling

vendor change token

vendor response schema
```

The canonical domain SHALL NOT.

---

# 35. Anti-Corruption Layer

The architecture SHALL be:

```text
Provider API
    │
    ▼
Provider Adapter
    │
    ▼
Provider-Native Representation
    │
    ▼
Normalisation
    │
    ▼
Baobab Canonical Regulatory Model
```

Never:

```text
Provider JSON
    │
    ▼
Baobab domain entity
```

directly.

---

# 36. Provider DTOs Stay at Boundary

Types such as:

```text
ThomsonTariffResponse

RegGenomeRequirementPayload

FiscalNotePolicyDocument
```

if ever created SHALL remain within provider infrastructure modules.

They SHALL NOT appear in:

```text
domain

canonical APIs

shared contracts

Digital Estates

Trade

ERP

Pulse
```

---

# 37. Provider Exceptions Stay at Boundary

Likewise:

```text
VendorRateLimitException
VendorPaginationException
VendorAuthException
```

SHALL be translated into canonical Baobab acquisition errors before crossing the adapter boundary.

---

# 38. Provider-Specific IDs Are External References

A vendor-native identifier SHALL not become a canonical Baobab regulatory identifier.

Instead:

```text
Canonical Regulatory Object
      │
      ▼
ExternalReference
      │
      ▼
Provider Native ID
```

This aligns with existing Shared canonical mapping principles.

---

# 39. Canonical Mapping

Mappings from provider-native identities into Baobab canonical regulatory entities SHALL be governed.

They SHALL NOT be guessed invisibly by application code.

---

# 40. Ambiguous Mapping

If:

```text
Provider requirement A
```

could map equally to:

```text
Baobab Rule X
Baobab Rule Y
```

the system SHALL create:

```text
MAPPING_AMBIGUOUS
```

or equivalent review state.

It SHALL NOT randomly select one.

---

# 41. Source Acquisition Is Not Canonical Promotion

An acquired provider record SHALL begin as:

```text
source evidence
```

not:

```text
canonical regulatory truth.
```

---

# 42. Acquisition Layers

The source pipeline SHALL preserve at least:

```text
L0 SOURCE ARTEFACT

L1 PROVIDER-NATIVE RECORD

L2 NORMALISED SOURCE RECORD

L3 CANONICAL REGULATORY REPRESENTATION

L4 INTERPRETATION / RULE
```

These SHALL not be collapsed.

---

# 43. L0 — Source Artefact

Examples:

```text
original JSON response

PDF

XML

CSV

XLSX

HTML snapshot where permitted

signed rule package
```

Where rights permit, native evidence SHOULD be preserved.

---

# 44. L1 — Provider-Native Record

This preserves provider semantics.

Example:

```text
Vendor obligation object

SARS tariff row

government API response
```

No Baobab meaning is imposed yet.

---

# 45. L2 — Normalised Source Record

Normalisation MAY standardise:

```text
dates

language tags

country identifiers

currency

classification format

document identifiers

encoding

field names
```

without yet asserting full regulatory meaning.

---

# 46. L3 — Canonical Regulatory Representation

Only at this stage does information map into Baobab concepts such as:

```text
Authority

Instrument

Provision

RegulatoryChange

Jurisdiction

Requirement
```

subject to verification.

---

# 47. L4 — Interpretation and Rule

Interpretations and machine rules are subsequent derived objects.

They SHALL not be created implicitly during acquisition without lineage.

---

# 48. Transformation May Add Meaning but Never Erase Origin

This SHALL reuse the principle established in Pulse:

> **Transformation may add meaning, but it must not erase origin.**

Regulations applies it more strictly because the transformed information may influence enforcement.

---

# 49. Raw Evidence Preservation

Where licensing permits, Baobab SHOULD preserve the exact source bytes retrieved.

This allows later:

```text
reprocessing

parser improvement

audit

change comparison

dispute investigation

interpretation replay
```

---

# 50. Immutable Acquisition

An acquisition SHALL be append-oriented.

If a source at the same URI changes:

```text
Artefact A
hash abc
```

becomes:

```text
Artefact B
hash xyz
```

not:

```text
overwrite A.
```

---

# 51. AcquisitionRun

Each acquisition operation SHOULD be identifiable.

Conceptually:

```text
AcquisitionRun
├── id
├── provider_id
├── source_id
├── adapter_version
├── started_at
├── completed_at
├── trigger
├── watermark_before
├── watermark_after
├── status
├── records_seen
├── artefacts_created
├── failures
└── correlation_id
```

---

# 52. Acquisition Trigger

Potential triggers:

```text
SCHEDULED

MANUAL

WEBHOOK

PROVIDER_EVENT

CHANGE_POLL

BACKFILL

REPLAY

INCIDENT_RECOVERY
```

---

# 53. Incremental Acquisition

Adapters SHOULD support provider-appropriate incremental mechanisms:

```text
modified_since

cursor

change token

sequence number

ETag

Last-Modified

published-after

event offset
```

where available.

---

# 54. Full Refresh

Where providers do not expose reliable change semantics, full snapshot acquisition MAY be necessary.

The architecture SHALL support it without pretending it is incremental.

---

# 55. Change Detection Is Separate from Acquisition

Acquisition says:

```text
we obtained new bytes.
```

Change detection asks:

```text
what materially changed?
```

These are distinct responsibilities.

---

# 56. Adapter Versioning

Each acquisition SHALL record:

```text
adapter version
```

where transformation depends materially on adapter behaviour.

This helps explain future parser corrections.

---

# 57. Adapter Change Does Not Rewrite Evidence

If adapter version 2 parses an old artefact differently:

```text
Artefact A
    │
    ├── parse v1
    └── parse v2
```

both derivations can remain traceable.

---

# 58. Adapter Architecture

The repository SHOULD enforce a structural boundary similar to Pulse's Haystack anti-corruption mechanism.

For example:

```text
infrastructure/providers/thomson_reuters/

infrastructure/providers/reggenome/

infrastructure/providers/sars/

infrastructure/providers/afcfta/
```

while domain code imports no provider SDK.

---

# 59. Architecture Tests

CI SHOULD eventually prove:

```text
provider SDK imports
exist only in provider infrastructure
```

and fail if:

```text
domain/
application/
contracts/
```

directly import vendor-specific libraries.

---

# 60. Why Mechanical Enforcement Matters

Provider neutrality written only in an ADR will eventually decay.

Provider neutrality enforced by:

```text
module boundaries

dependency rules

contract tests

architecture tests
```

is far more durable.

---

# 61. No Provider SDK in Shared

`baobab-platform/shared` SHALL contain no:

```text
Thomson Reuters client

RegGenome model

FiscalNote DTO

vendor authentication code
```

Shared defines Baobab contracts only.

---

# 62. No Provider SDK in Digital Estates

ZuriBeans SHALL never need to know:

```text
which data vendor produced the result.
```

It consumes Baobab regulatory capability.

---

# 63. No Provider SDK in Trade

Trade SHALL receive:

```text
RegulatoryDecision
```

not:

```text
ThomsonComplianceResponse.
```

---

# 64. Provider-Neutrality Test

The architecture SHALL pass this test:

> If Baobab terminates Provider X tomorrow, which modules must change?

Correct answer:

```text
provider adapter

provider configuration

source mappings

perhaps licences / commercial configuration
```

Incorrect answer:

```text
Shared contracts
Trade
ERP
Pulse
ZuriBeans
canonical regulatory domain
```

---

# 65. Multiple Providers May Coexist

Provider-neutrality does not require:

```text
exactly one active provider.
```

Baobab MAY combine several.

Example:

```text
Official source
      +
RegGenome
      +
Thomson Reuters
      +
tenant legal opinion
```

may collectively support one regulatory domain.

---

# 66. Multi-Provider Is Not Majority Voting

Baobab SHALL NOT use:

```text
3 sources say X
2 sources say Y
therefore X wins.
```

Regulatory authority is not democratic source counting.

---

# 67. Source Roles

Different providers may play different roles.

Example:

```text
Official Gazette:
authority

Commercial provider:
structured extraction

Trade portal:
operational procedure

Professional counsel:
interpretation

Baobab:
canonical applicability
```

This is preferred to forcing one provider to do everything.

---

# 68. Source Preference Policy

The engine SHOULD eventually support explicit source preference rules.

Conceptually:

```text
SourcePreferencePolicy
├── regulatory_domain
├── jurisdiction
├── purpose
├── preferred_source_types[]
├── fallback_sources[]
├── freshness_requirement
├── authority_requirement
└── conflict_policy
```

---

# 69. Preference Is Purpose-Specific

Example:

For:

```text
Was regulation promulgated?
```

preferred:

```text
official gazette.
```

For:

```text
Give me a structured list of obligations.
```

preferred may include:

```text
licensed structured provider
```

with traceability to the official source.

---

# 70. Primary Source Preference

Where economically and technically practical, Baobab SHOULD retain direct access to authoritative primary sources for consequential regulation.

This reduces the risk that a vendor becomes the only path between Baobab and the law.

---

# 71. Direct Primary Access Is Strategic

Even when commercial content is purchased, Baobab SHOULD preserve enough direct primary-source capability to:

```text
verify provider lineage

resolve disputes

validate material changes

audit enforcement rules
```

for high-impact domains.

---

# 72. Commercial Provider Strength

Commercial providers may outperform direct government acquisition in:

```text
normalisation

translation

coverage

classification

update speed

consistent APIs

specialist research

historical reconstruction
```

Baobab SHOULD exploit those strengths.

Provider-neutral does not mean anti-vendor.

---

# 73. Do Not Rebuild Commodity Infrastructure for Pride

If a provider can supply accurate, licensed and well-maintained:

```text
220-country tariff content
```

there is little strategic value in rebuilding all 220 countries manually merely to claim independence.

The strategic question is:

> Can Baobab replace, supplement or verify the provider without rewriting the platform?

---

# 74. Thomson Reuters as Example Provider

Thomson Reuters currently exposes:

```text
tariff schedules

duty rates

import/export controls

rules of origin

commercial documentation

sanctions data

classification content
```

through its trade-content ecosystem and APIs.

Architecturally this makes it a potentially valuable:

```text
RegulatorySourceProvider
```

not:

```text
Baobab Regulations.
```

---

# 75. RegGenome as Example Provider

RegGenome exposes structured requirements retaining:

```text
scope

conditions

relationships

source links
```

and supports regulatory inventories, applicability and change traceability.

Again:

```text
excellent provider candidate
```

does not mean:

```text
canonical Baobab ontology.
```

---

# 76. FiscalNote as Example Provider

FiscalNote's PolicyNote API and MCP capability demonstrate the direction of regulatory/policy vendors toward agent-accessible source infrastructure.

Baobab SHALL therefore assume future source providers may expose:

```text
REST

GraphQL

MCP

event streams

structured tool APIs
```

and design adapters accordingly.

---

# 77. MCP Is Transport, Not Canonical Semantics

A vendor MCP server SHALL be treated as:

```text
source access interface
```

not:

```text
trusted Baobab reasoning layer.
```

Tool output still crosses the anti-corruption boundary.

---

# 78. External AI Agent Is Not Source Authority

A provider may expose an AI assistant.

Its response SHALL be classified according to:

```text
underlying sources

provider assurance

citations

verification state
```

not according to how fluent the assistant sounds.

---

# 79. Provider AI Result

Example:

```text
Commercial provider AI answer
      │
      ▼
Provider-derived interpretation
      │
      ▼
Underlying provider citations
      │
      ▼
Official sources
```

Baobab SHOULD traverse to the underlying evidence where consequential.

---

# 80. Search Result Is Discovery Evidence

General web search MAY assist:

```text
source discovery

change detection

identifying official material
```

It SHALL not automatically populate production rule state.

---

# 81. Discovery Source

A discovered URL begins as:

```text
DISCOVERED
```

not:

```text
TRUSTED_SOURCE.
```

---

# 82. Source Discovery Pipeline

Conceptually:

```text
Candidate Source
      │
      ▼
Identity Resolution
      │
      ▼
Authority Resolution
      │
      ▼
Rights Review
      │
      ▼
Security Review
      │
      ▼
Coverage Review
      │
      ▼
Source Registration
```

---

# 83. Source Onboarding

Every production regulatory source SHOULD have:

```text
owner

purpose

authority relationship

jurisdiction coverage

regulatory-domain coverage

access mechanism

rights basis

freshness expectation

retention policy

security classification

adapter

operational runbook
```

---

# 84. Source Lifecycle

Recommended lifecycle:

```text
DISCOVERED

UNDER_REVIEW

APPROVED

ACTIVE

DEGRADED

SUSPENDED

DEPRECATED

RETIRED
```

---

# 85. Source Suspension

A source MAY be suspended because of:

```text
licensing dispute

authentication failure

security incident

quality failure

publication cessation

authority change

unresolved corruption

provider contract termination
```

Suspending a source SHALL not erase historical evidence.

---

# 86. Source Coverage

Every source SHOULD declare coverage explicitly.

Conceptually:

```text
SourceCoverageProfile
├── jurisdictions[]
├── regulatory_domains[]
├── instrument_types[]
├── languages[]
├── temporal_start?
├── temporal_end?
├── update_frequency?
├── product_classes?
└── known_exclusions[]
```

---

# 87. Coverage Is Not Binary

Possible states:

```text
FULL

PARTIAL

SELECTIVE

UNKNOWN
```

for a given scope.

---

# 88. Coverage Gap

If a source covers:

```text
South African tariffs
```

but not:

```text
South African phytosanitary controls
```

Baobab SHALL know the difference.

---

# 89. Coverage Gap Is Regulatory State

When an assessment depends upon an uncovered domain:

```text
coverage gap
```

SHOULD contribute to:

```text
INDETERMINATE
```

or reduced decision authority.

It SHALL not silently mean no rule exists.

---

# 90. Coverage Composition

Baobab MAY satisfy a regulatory profile using several sources:

```text
Tariffs:
Provider A

SPS:
Government source

Rules of origin:
AfCFTA source

Import controls:
Provider B
```

This is a feature.

---

# 91. Jurisdiction Pack Is Source-Agnostic

Future:

```text
ZA Regulatory Pack
```

SHALL NOT mean:

```text
Thomson Reuters ZA Pack.
```

It means a Baobab coverage composition that may use multiple providers.

---

# 92. Domain Pack Is Source-Agnostic

Likewise:

```text
Cross-Border Goods Pack
```

can be backed by several providers.

Provider replacement SHALL not redefine the pack.

---

# 93. Source Freshness Policy

Every material source SHOULD have freshness expectations.

Conceptually:

```text
SourceFreshnessPolicy
├── expected_refresh_interval
├── maximum_staleness
├── criticality
├── stale_effect
├── escalation_policy
└── monitoring_mode
```

---

# 94. Freshness Is Domain-Specific

A source updated annually may be current.

Another source unchanged for 48 hours may be suspicious.

Freshness SHALL not use one global TTL.

---

# 95. Publication Frequency

Baobab SHOULD distinguish:

```text
source expected update frequency
```

from:

```text
Baobab polling frequency.
```

Polling every minute does not make an annual statute source fresher.

---

# 96. Freshness State

Potential:

```text
CURRENT

AGING

STALE

UNKNOWN

UNAVAILABLE
```

---

# 97. Staleness Propagation

If a critical input becomes stale:

```text
Source stale
      ↓
Rule assurance affected
      ↓
Decision effect ceiling may fall
```

consistent with ADR-REG-0004.

---

# 98. Provider SLA Is Not Regulatory Freshness

A vendor can have:

```text
99.99% API uptime
```

while providing outdated content.

Baobab SHALL monitor:

```text
service availability
```

and:

```text
regulatory freshness
```

separately.

---

# 99. Acquisition Health

Metrics SHOULD distinguish:

```text
endpoint reachable

acquisition completed

record volume

source changed

parser successful

rights valid

freshness current

canonical promotion healthy
```

---

# 100. Sudden Record Drop

If a provider normally returns:

```text
100,000 records
```

and suddenly returns:

```text
300
```

Baobab SHOULD flag an acquisition anomaly.

It SHALL not assume 99,700 regulations were repealed.

---

# 101. Schema Drift

Providers change schemas.

Adapters SHALL detect unexpected schema changes.

Potential state:

```text
SCHEMA_DRIFT
```

Rather than silently discarding fields.

---

# 102. Provider Contract Testing

Each provider integration SHOULD maintain:

```text
fixture tests

schema tests

pagination tests

rate-limit tests

authentication tests

sample acquisition tests

mapping tests
```

where licences permit test fixtures.

---

# 103. Provider Sandbox

Where a provider exposes sandbox/test APIs, Baobab MAY use them for integration verification.

Sandbox content SHALL not enter production regulatory truth.

---

# 104. Provider Failure Isolation

Failure of:

```text
Provider A
```

SHALL not automatically disable unrelated sources.

---

# 105. Provider Redundancy

For high-value regulatory domains, Baobab MAY maintain multiple source routes.

Example:

```text
Official source
+
Commercial provider
```

provides stronger resilience than either alone.

---

# 106. Redundancy Is Not Duplicate Truth

Both representations SHALL map to the same canonical authority/instrument where appropriate.

They SHALL not create duplicate regulations.

---

# 107. Corroboration

Secondary or commercial providers MAY corroborate:

```text
publication

effective date

interpretation

classification
```

But corroboration and authority remain distinct.

---

# 108. Conflicting Providers

If Provider A and Provider B disagree:

```text
compare provenance
      │
      ▼
resolve underlying source
      │
      ▼
identify mapping / interpretation issue
```

not:

```text
choose cheapest provider.
```

---

# 109. Conflict Record

A `SourceConflict` or equivalent SHOULD eventually capture:

```text
objects in conflict

conflict type

discovered_at

severity

affected domains

resolution state

reviewer

resolution
```

---

# 110. Primary-Source Conflict

If a commercial provider conflicts with a directly acquired authoritative source, the authoritative source ordinarily deserves stronger legal-source treatment.

However, Baobab SHALL still investigate whether:

```text
direct source is outdated

wrong instrument selected

commercial provider incorporated amendment

Baobab parsing failed
```

before assuming provider error.

---

# 111. Official Sources Can Also Conflict

Two official publications may appear inconsistent.

This SHALL trigger legal-hierarchy analysis.

Generic provider ranking is insufficient.

---

# 112. Source Priority Is Not Legal Hierarchy

`SourcePreferencePolicy` controls acquisition/use preference.

`LegalHierarchy` determines normative precedence.

These SHALL remain separate.

---

# 113. Rights Metadata Is Mandatory

A source entering the fabric SHALL carry rights/access metadata.

At minimum conceptually:

```text
access_basis

licence

commercial_use

derivative_use

redistribution

storage_allowed

retention_allowed

training_allowed

customer_display_allowed

citation_required

attribution_required
```

The full licensing architecture belongs in `ADR-REG-0012`.

---

# 114. Public Access Is Not Reuse Permission

The architectural rule remains:

```text
visible on internet
      ≠
commercially reusable.
```

---

# 115. DCAT Rights Concepts

DCAT 3 explicitly models:

```text
access rights

licence

rights

policy
```

on dataset distributions and provides useful vocabulary for interoperable catalog metadata.

Baobab SHOULD preserve equivalent concepts.

---

# 116. Rights Gate

Before acquisition or persistence:

```text
Can we access it?
Can we store it?
Can we transform it?
Can we expose it?
Can we use it commercially?
```

SHOULD be answerable.

---

# 117. Rights May Differ by Layer

A provider may permit:

```text
API use
```

but prohibit:

```text
raw redistribution.
```

Baobab may therefore expose:

```text
derived decision
```

while withholding:

```text
licensed source content.
```

---

# 118. Customer Entitlement Cannot Override Provider Rights

A Baobab Enterprise subscription SHALL NOT grant rights Baobab itself does not possess.

---

# 119. Licence Expiry

If a commercial licence expires:

```text
new acquisitions
```

may stop.

Historical retention depends on contractual rights.

The source-rights model SHALL govern this explicitly.

---

# 120. Vendor Exit Must Be Planned Before Vendor Entry

Every material commercial provider integration SHOULD define:

```text
export rights

retention rights

termination behaviour

replacement strategy

mapping portability

historical decision survivability
```

before production dependence.

---

# 121. Vendor Exit Test

Baobab must answer:

> If this provider contract ends tomorrow, can we still explain decisions made yesterday?

For consequential decisions, the target answer SHOULD be:

```text
yes
```

within contractual rights.

---

# 122. Source Snapshot Rights Matter

This makes source-snapshot licensing a strategic procurement concern.

Baobab procurement SHALL evaluate technical and exit rights, not price alone.

---

# 123. Provider Procurement Criteria

Material provider assessment SHOULD consider:

```text
coverage

authority traceability

update latency

historical depth

API quality

structured semantics

source citations

licensing

redistribution

exit rights

availability

security

residency

commercial stability

support

pricing

vendor concentration risk
```

---

# 124. Price Is One Dimension

A cheap provider whose data cannot be:

```text
retained

audited

mapped

reproduced
```

may be commercially expensive in the long term.

---

# 125. Provider Concentration

Baobab SHOULD monitor dependence such as:

```text
percentage of E4 rules
whose only source path is Vendor X
```

This is more meaningful than counting adapters.

---

# 126. Concentration Risk

Potential metric:

```text
critical decision coverage
by provider
```

SHOULD inform strategic sourcing.

---

# 127. No One Vendor Should Become an Unreviewed Single Point of Regulatory Truth

For highly consequential regulatory domains, Baobab SHOULD have:

```text
direct authoritative verification
```

or another defensible verification path.

---

# 128. Standards Bodies

Baobab MAY integrate:

```text
ISO

SABS

Codex

UN/CEFACT

WCO

industry standards bodies
```

where regulations reference their standards.

---

# 129. Standards Licensing

Standards may carry stricter copyright/licensing terms than legislation.

Baobab SHALL not assume it can reproduce complete standards simply because regulation incorporates them by reference.

---

# 130. WCO Data Model

The WCO Data Model provides harmonised, reusable data definitions and messages specifically designed for customs and other cross-border regulatory agencies. It acts as a universal language for cross-border data exchange and is aligned with standards including UN/CEFACT and ISO.

Its current version 4.3.0 was approved in June 2026 and extends support for digital documents and JSON-oriented implementations.

Baobab SHOULD therefore align cross-border regulatory data mappings with WCO concepts where practical.

---

# 131. WCO Is Interoperability, Not Baobab Ontology

Baobab SHALL NOT simply import the entire WCO Data Model as its regulatory domain.

Instead:

```text
WCO concept
     │
     ▼
Interoperability mapping
     │
     ▼
Baobab canonical concept
```

where necessary.

---

# 132. Source-Native Standards Should Remain Traceable

If:

```text
provider uses WCO data element X
```

Baobab SHOULD retain that mapping.

This improves integration with customs and Single Window systems later.

---

# 133. LegalRuleML

LegalRuleML's specification explicitly emphasises the need to preserve links between formal machine rules and legally binding textual sources, including:

```text
provenance

authority

jurisdiction

multiple interpretations

authorial tracking
```

and treats those relationships as important for authenticity and updating rules when source law changes.

Baobab SHOULD preserve semantic compatibility with these principles.

---

# 134. Provider Rule Format Is Not Canonical Rule Format

If Vendor X provides:

```text
JSONLogic
```

and Vendor Y provides:

```text
LegalRuleML
```

Baobab SHALL not force its canonical regulatory model to equal either one.

Both pass through adapters.

---

# 135. Authority-Issued Machine Law

A future government may supply an authoritative machine-executable representation as contemplated by OECD Law as Code.

Such a source SHALL be first-class.

But Baobab still wraps it in canonical provenance/context.

---

# 136. Authority Rule Adapter

Conceptually:

```text
Authority Machine Rule
        │
        ▼
AuthorityRuleAdapter
        │
        ▼
Canonical Baobab Representation
        │
        ▼
Contextual Applicability
```

Baobab need not reinterpret logic unnecessarily.

---

# 137. Preserve Authority-Supplied Semantics

If an authority supplies:

```text
conditions

exceptions

effective periods

discretion markers

legal consequences
```

Baobab SHOULD preserve them faithfully.

---

# 138. Customer-Supplied Sources

Tenants MAY upload or register:

```text
legal opinions

customs rulings

permits

regulator correspondence

internal interpretations

licences

customer-specific determinations
```

These enter the same source fabric with tenant classification.

---

# 139. Customer Source Is Not Shared by Default

A private counsel opinion from Tenant A SHALL NOT become:

```text
platform public rule
```

without explicit governance and rights.

---

# 140. Customer Sources Need Provenance

Even customer-uploaded evidence requires:

```text
who uploaded

for which tenant

source claimed

date

scope

classification

retention

verification
```

---

# 141. Manual Upload Is a Valid Adapter

Not all important regulation will have machine APIs.

A governed:

```text
manual upload adapter
```

is legitimate.

It SHALL still create:

```text
AcquisitionRun

SourceArtefact

hash

provenance
```

---

# 142. Email Ingestion

Regulators or providers may distribute notices by email.

Baobab MAY support controlled mailbox ingestion later.

Email SHALL remain:

```text
source transport
```

not:

```text
source authority.
```

---

# 143. Web Scraping

Scraping MAY be used where:

```text
lawful

permitted

operationally necessary

technically appropriate
```

It SHALL not be the default architecture.

---

# 144. Scraper Is Adapter

A scraper belongs inside:

```text
SourceAdapter
```

and SHALL not leak HTML selectors into domain logic.

---

# 145. Scraper Fragility

Scraped sources SHOULD carry operational monitoring for:

```text
selector drift

page redesign

bot blocks

missing content

unexpected pagination

captcha
```

---

# 146. Scraping Failure Is Not "No Regulation"

If parsing fails:

```text
ACQUISITION_FAILED
```

not:

```text
NO_RULE_FOUND.
```

---

# 147. APIs Preferred Where Equivalent

Where the same authoritative source offers a stable official API with appropriate rights, Baobab SHOULD generally prefer it over fragile scraping.

---

# 148. Machine-Readable Source Preferred, Authority Equal

If the same authority publishes:

```text
PDF

XML

JSON
```

Baobab MAY prefer JSON/XML for processing.

The legal authority classification does not increase merely because the representation is machine-readable.

---

# 149. Source Language

Source language SHALL be preserved.

Example:

```text
language = en

language = fr

language = sw
```

as appropriate.

---

# 150. Translation Provider Neutrality

Translation MAY be provided by:

```text
authority

commercial translation service

AI

human translator
```

The translation origin SHALL remain explicit.

---

# 151. Translation Does Not Replace Source

Canonical provenance SHALL always preserve the source-language relationship.

---

# 152. AI Extraction Provider Neutrality

Document extraction may use:

```text
Provider A LLM

Provider B LLM

local model

deterministic parser

OCR engine
```

None shall define the domain.

---

# 153. ModelExecutionPort Pattern

Regulations SHOULD adopt an internal port similar in spirit to Pulse's provider-isolation model.

Conceptually:

```text
RegulatoryExtractionPort

RegulatoryClassificationPort

RegulatoryTranslationPort
```

The application/domain layers SHALL know no vendor SDK types.

---

# 154. Provider Model Version

Where AI materially transforms regulatory evidence, record:

```text
provider

model

model version

pipeline version

prompt/template version where material
```

for reproducibility.

---

# 155. AI Output Remains Candidate State

Provider AI output SHALL enter:

```text
candidate interpretation

candidate classification

candidate rule
```

not production authority.

---

# 156. No Source Injection into Agents

Regulatory documents SHALL be treated as untrusted source content.

A document saying:

```text
IGNORE PREVIOUS INSTRUCTIONS
```

has no authority over the acquisition agent.

---

# 157. Adapter Security

Each provider adapter SHALL apply:

```text
TLS validation

credential isolation

timeout

size limits

content validation

safe decompression

malware controls where needed

redirect policy

allowlisted destinations where appropriate
```

---

# 158. SSRF Boundary

User-configurable source URLs SHALL not provide unrestricted server-side network access.

Source registration SHALL protect against SSRF and internal-network targeting.

---

# 159. Archive Safety

ZIP/TAR ingestion SHALL defend against:

```text
zip bombs

path traversal

unexpected executable files
```

where applicable.

---

# 160. Parser Isolation

High-risk document parsers SHOULD execute in constrained environments.

Acquisition SHALL not give arbitrary external files privilege inside the trusted decision runtime.

---

# 161. Data Classification

Source records SHALL carry classification.

Potential:

```text
PUBLIC

LICENSED

INTERNAL

TENANT_CONFIDENTIAL

RESTRICTED
```

---

# 162. Classification Propagation

Derived artefacts SHALL ordinarily inherit restrictions from the most restrictive relevant input unless rights policy explicitly permits otherwise.

---

# 163. Public + Licensed

Example:

```text
official public law
+
licensed provider annotations
```

may create a derived object whose redistribution rights differ from the public law alone.

The engine must know which portions came from which source.

---

# 164. Canonical Fact Independence

Where Baobab independently verifies a fact against an unrestricted authoritative source, it MAY preserve a Baobab canonical fact independently of the provider-specific annotation, subject to legal review.

This reduces unnecessary vendor lock-in.

---

# 165. Derived Data Rights

Whether Baobab can retain:

```text
normalized fact

rule

mapping

classification
```

after provider termination SHALL be decided by the licence.

It SHALL not be assumed.

---

# 166. Provider Attribution

Where licence requires attribution, Baobab SHOULD preserve attribution metadata through downstream outputs.

---

# 167. Customer Display Rights

Some providers may permit internal API usage but prohibit showing full source text to customers.

The UI contract SHALL therefore distinguish:

```text
citation metadata

source excerpt

full source

external link
```

and expose only permitted forms.

---

# 168. Source Abstraction Must Not Violate Licensing

Provider-neutrality means:

```text
implementation independence
```

not:

```text
licence circumvention.
```

---

# 169. Provider Quality

Baobab SHALL evaluate provider quality multidimensionally.

Potential dimensions:

```text
coverage

freshness

source traceability

completeness

schema stability

historical depth

accuracy

operational reliability

update transparency

rights clarity
```

---

# 170. No Universal Provider Score

Avoid:

```text
provider_score = 87
```

as the only representation.

Different providers excel at different functions.

---

# 171. Provider May Be Great for Tariffs and Poor for SPS

Quality assessment SHALL be scoped to:

```text
jurisdiction

domain

purpose
```

where necessary.

---

# 172. Source Trust Is Separate from Provider Reliability

A vendor API may be technically reliable while its underlying source mapping is poor.

Conversely, an official authority site may be operationally unreliable while legally authoritative.

These dimensions remain separate.

---

# 173. Acquisition Provenance

Every material acquisition SHOULD answer:

```text
which provider?

which source?

which endpoint?

which credentials/profile?

which adapter?

which adapter version?

when?

what retrieval parameters?

what watermark?

what content hash?

what rights profile?
```

---

# 174. Canonical Promotion Provenance

Every canonical regulatory object SHOULD answer:

```text
which acquisition?

which source artefact?

which native record?

which normalisation?

which mapping?

which verifier?
```

---

# 175. Change Traceability

When:

```text
Rule R changes
```

Baobab SHOULD eventually answer:

```text
because Provider X delivered artefact A
representing Authority Y amendment Z.
```

---

# 176. Source Correction

If a provider corrects previously published data:

```text
provider correction
```

SHALL be distinct from:

```text
legal amendment.
```

---

# 177. Parser Correction

Likewise:

```text
Baobab parser fix
```

SHALL not be labelled:

```text
regulatory change.
```

---

# 178. Provider Change

A provider may alter its interpretation while the law remains unchanged.

That SHALL also remain distinguishable.

---

# 179. Four Change Types

The fabric SHOULD ultimately distinguish:

```text
SOURCE_LEGAL_CHANGE

PROVIDER_CONTENT_CHANGE

BAOBAB_EXTRACTION_CHANGE

BAOBAB_INTERPRETATION_CHANGE
```

This distinction will feed `ADR-REG-0023`.

---

# 180. Source Catalog

Baobab SHOULD provide an internal source catalogue.

It SHOULD answer:

```text
What sources exist?

What jurisdictions do they cover?

Who provides them?

What authority do they represent?

What rights apply?

How fresh are they?

Which adapters consume them?

What regulatory packs depend on them?
```

---

# 181. Source Catalogue Is Not Public by Default

Some commercial provider relationships, credentials and coverage limitations may be confidential.

The catalogue SHALL support access control.

---

# 182. Operational Source Dashboard

A future governance console SHOULD show:

```text
provider health

acquisition health

freshness

coverage

rights expiry

schema drift

unresolved conflict

change backlog
```

without becoming the canonical store itself.

---

# 183. Coverage Map

A strategically useful projection is:

```text
                 CUSTOMS   SPS   TAX   ORIGIN   RESTRICTIONS

Uganda             ✓       ✓     △      ✓          △
South Africa       ✓       ✓     ✓      ✓          ✓
Kenya              △       ✕     △      ✕          △
```

where:

```text
✓ supported
△ partial
✕ unsupported
```

with actual state derived from registered sources.

---

# 184. Coverage Is Commercially Valuable

Baobab can package:

```text
Jurisdiction Packs

Domain Packs

Corridor Packs
```

because source coverage is explicit and composable.

This is one direct path from source architecture to revenue.

---

# 185. Corridor Pack Example

```text
UG → ZA Cross-Border Goods
         │
         ├── UG export regulations
         ├── coffee/vanilla controls
         ├── SPS
         ├── rules of origin
         ├── AfCFTA
         ├── ZA import controls
         ├── SARS tariffs
         └── required documentation
```

Each layer may use a different source provider.

---

# 186. Corridor Pack Must Survive Provider Swap

If:

```text
Tariff Provider A
```

is replaced by:

```text
Tariff Provider B
```

the product remains:

```text
UG → ZA Cross-Border Goods
```

not:

```text
new commercial product.
```

---

# 187. Product Independence

Commercial products SHALL package:

```text
regulatory capability

jurisdiction coverage

domain coverage

service levels
```

not named vendors.

---

# 188. Provider Branding

Provider attribution MAY appear where contractually required or commercially useful.

It SHALL not become capability identity.

---

# 189. External Provider as Capability Provider

A future external regulatory service MAY itself be registered in Control Plane as a capability provider.

However, Baobab SHOULD normally preserve the Regulations canonical domain boundary between Digital Estates and that provider.

---

# 190. Direct External Provider Binding

A direct binding may be appropriate only where:

```text
the provider itself conforms to canonical Baobab capability contracts
```

or a governed adapter presents those contracts.

---

# 191. No Provider Bypass

A Digital Estate SHALL not call:

```text
Vendor X
```

directly for canonical Regulations functionality merely to avoid Baobab contracts.

That reintroduces lock-in.

---

# 192. Provider-Specific Advanced Features

If a vendor offers unique functionality not yet canonicalised, Baobab MAY expose it experimentally behind:

```text
provider-specific internal feature
```

but SHOULD not immediately pollute canonical contracts.

---

# 193. Promote Only Stable Semantics

A provider-specific feature SHOULD become a canonical capability only when:

```text
business meaning is understood

cross-provider semantics can be defined

long-term value exists
```

---

# 194. Build-versus-Buy Decision Framework

For each regulatory domain, Baobab SHOULD evaluate:

| Question | Build favoured when | Buy favoured when |
|---|---|---|
| Coverage | Narrow, strategic | Huge/global |
| Differentiation | High | Low |
| Source access | Direct/easy | Fragmented/expensive |
| Maintenance burden | Manageable | Large |
| Licensing | Clear | Provider already solved |
| Update latency | Baobab can compete | Vendor superior |
| Canonical context | Core Baobab IP | Generic data |
| Regulatory execution | Core Baobab IP | Rarely outsource fully |

---

# 195. Likely Buy Areas

Potentially:

```text
global tariff content

broad sanctions content

global company/legal data

large-scale translation

certain standards datasets

global regulatory monitoring
```

subject to commercial evaluation.

---

# 196. Likely Build Areas

Baobab SHOULD strongly favour owning:

```text
Context resolution

Applicability

Regulatory decision contracts

Decision effects

Jurisdiction packs

Corridor composition

Change impact

Cross-engine enforcement integration

Decision replay

Customer regulatory graph
```

These are closer to the strategic moat.

---

# 197. African Differentiation

Baobab MAY need to build more acquisition infrastructure in African markets where:

```text
official APIs are incomplete

documents are fragmented

machine readability is poor

regional layers overlap

commercial coverage is shallow
```

This is acceptable.

The source fabric exists specifically to make that complexity reusable.

---

# 198. African Sources Must Not Become Special Cases

Do not write:

```text
if Uganda:
    scrape portal

if South Africa:
    use API
```

inside regulatory application logic.

Use:

```text
Source
+
Adapter
+
Coverage
+
Canonical mapping
```

for each.

---

# 199. Competitive Context

Originvia's current positioning around Africa–Europe regulated trade explicitly combines provenance, corridor-specific compliance and workflow integration.

This is further evidence that Baobab cannot rely on:

```text
Africa + compliance
```

as its sole differentiation.

Baobab must win through the reusable multi-tenant platform architecture:

```text
sources
+
canonical context
+
regulatory execution
+
Trade
+
ERP
+
Pulse
+
Digital Estates
```

---

# 200. Source Fabric and Pulse Flywheel

Regulations may publish:

```text
regulatory change
```

to Pulse.

Pulse may discover:

```text
possible regulatory development
```

and feed discovery back to Regulations.

Conceptually:

```text
REGULATIONS
    │
    │ verified change
    ▼
PULSE
    │
    │ strategic impact
    ▼
Opportunity / Risk


PULSE
    │
    │ possible new development
    ▼
REGULATIONS
    │
    │ source discovery / verification
    ▼
Canonical Regulatory Change
```

---

# 201. Pulse Discovery Does Not Promote Rules

This feedback loop SHALL preserve authority boundaries.

Pulse discovery can trigger investigation.

Only Regulations governance can promote regulatory knowledge.

---

# 202. No Shared Raw Source Database

Pulse and Regulations MAY consume the same external authority.

They SHALL not be forced to share one mutable database of domain objects.

Shared source infrastructure MAY exist later at infrastructure level.

Domain authority remains separate.

---

# 203. Shared SourceArtefact References

Where economical and licit, the platform MAY reuse one immutable underlying object-storage artefact across engines through governed references.

But:

```text
storage deduplication
```

does not mean:

```text
domain ownership merger.
```

---

# 204. Source Identity Across Engines

A common external-source identity MAY eventually be promoted to Shared if multiple engines need exactly the same semantics.

Premature generalisation SHALL be avoided.

---

# 205. Operational Readiness

A regulatory pack SHALL not be `READY` merely because its APIs respond.

It depends on its sources.

Conceptually:

```text
Engine Healthy
      +
Sources Current
      +
Coverage Adequate
      +
Rights Valid
      +
Rules Published
      =
Regulatory Capability Ready
```

---

# 206. Provider Readiness Contribution

Each source/provider SHALL contribute to:

```text
profile readiness.
```

Failure of a non-critical optional source MAY degrade but not block capability.

Failure of a critical source may render it unavailable.

---

# 207. Critical Source

A source MAY be designated:

```text
CRITICAL
```

for a profile when no assessment can safely be made without it.

This status is profile-specific.

---

# 208. Critical Does Not Mean Authoritative

A commercial provider might be operationally critical.

Its legal authority remains separate.

---

# 209. Fallback Source

Profiles SHOULD be able to declare:

```text
primary source

fallback source

verification source
```

where appropriate.

---

# 210. Fallback Must Preserve Provenance

If the primary source fails and fallback is used, the resulting assessment SHALL know that.

---

# 211. Provider Outage

Provider outage SHALL produce:

```text
PROVIDER_UNAVAILABLE
```

not:

```text
NO_REGULATION.
```

---

# 212. Licence Expiry

Licence expiry SHALL produce:

```text
SOURCE_RIGHTS_UNAVAILABLE
```

or equivalent.

It SHALL not silently continue unauthorised use.

---

# 213. Source Deprecation

When an authority retires a source:

```text
Source A
    ↓
superseded by
Source B
```

the Source Registry SHALL preserve history and update acquisition policy.

---

# 214. Authority Migration

If a regulatory authority changes institution:

```text
Old authority
    ↓
New authority
```

source mappings SHALL preserve historical authority.

---

# 215. Source URLs Are Not Canonical IDs

This principle bears repeating.

A URL is an access location.

It is not:

```text
the regulation

the authority

the source identity

the instrument identity.
```

---

# 216. Source Hash Is Not Canonical ID

Likewise, a hash identifies content bytes.

It does not identify:

```text
legal meaning.
```

---

# 217. Deduplication

Exact duplicate artefacts MAY be content-deduplicated operationally.

Their separate acquisition/provenance events SHALL remain.

---

# 218. Near-Duplicate Detection

Baobab MAY identify:

```text
same document with formatting differences
```

through deterministic or AI-assisted methods.

This creates candidate relationships.

It SHALL not merge regulatory identities automatically without verification.

---

# 219. Source Reconciliation

The engine SHOULD support reconciliation:

```text
Expected source state
        │
        ▼
Observed provider state
        │
        ▼
Drift
```

Examples:

```text
expected daily feed absent

expected endpoint moved

expected licence active

expected document version missing
```

---

# 220. Source Drift

Operational drift SHALL be visible.

It SHALL not wait until a customer receives a wrong decision.

---

# 221. Source SLIs

Potential indicators:

```text
acquisition_success_rate

acquisition_latency

freshness_lag

schema_drift_count

records_received

source_conflict_count

coverage_gap_count

rights_expiry_days

provider_availability
```

---

# 222. Regulatory SLI Distinction

Infrastructure:

```text
API latency
```

Regulatory:

```text
latest verified rule age
```

Both matter.

---

# 223. Source Cost Telemetry

Commercial provider cost SHOULD be measurable by:

```text
tenant

capability

jurisdiction pack

API usage

dataset subscription
```

where contracts permit.

This supports pricing and margin management.

---

# 224. Cost-Aware Routing

Baobab MAY eventually choose between equivalent providers based partly on cost.

However:

```text
cheaper
```

SHALL never override:

```text
required authority
required freshness
required coverage
required assurance.
```

---

# 225. Regulatory Procurement as Architecture

Provider contracts materially affect:

```text
auditability

data retention

customer rights

exit strategy

product margins

coverage
```

Therefore provider procurement SHALL be treated as architectural input.

---

# 226. Source Fabric Does Not Become Marketplace Yet

This ADR SHALL NOT create a public provider marketplace.

`ADR-REG-0029` may later address extension/marketplace architecture.

For now, providers are governed integrations.

---

# 227. Customer Bring-Your-Own Provider

Future enterprise customers MAY wish to supply licences to:

```text
Vendor X
```

Baobab SHOULD eventually support:

```text
customer-specific source binding
```

without changing canonical regulatory semantics.

---

# 228. BYOP Isolation

Customer-provided provider credentials SHALL be:

```text
tenant scoped

secret managed

audited

non-exportable
```

and SHALL not leak to other tenants.

---

# 229. Customer Provider Does Not Change Authority

A customer choosing Vendor A over Vendor B changes:

```text
source acquisition
```

not:

```text
legal authority.
```

---

# 230. Private Regulatory Corpus

Enterprise customers MAY supply private regulatory interpretations or internal rules.

These SHALL live alongside, not overwrite:

```text
public canonical regulatory knowledge.
```

---

# 231. Source Fabric Is Extensible

Adding a new source SHOULD require:

```text
register provider/source

implement adapter

declare rights

declare coverage

map canonical concepts

test

approve
```

not:

```text
rewrite Regulations.
```

---

# 232. Adapter Developer Contract

Baobab SHOULD eventually publish an internal adapter SDK/specification defining:

```text
adapter lifecycle

acquisition result

error semantics

pagination

watermarks

content hashing

rights references

telemetry

test fixtures
```

without vendor-specific semantics.

---

# 233. Adapter SDK Is Not Domain SDK

The adapter SDK helps integrations talk to Regulations acquisition infrastructure.

It does not expose private domain entities as extensibility points indiscriminately.

---

# 234. Certification

Third-party adapters SHOULD eventually pass:

```text
contract tests

security tests

rights checks

provenance tests

failure tests
```

before production installation.

---

# 235. Source Governance Console

A future administrative UI MAY support:

```text
register source

review coverage

inspect acquisition

resolve mapping

review conflicts

suspend source

view rights

view freshness
```

The UI remains a client of headless governance APIs.

---

# 236. Source Governance Permissions

Permissions SHOULD be separate:

```text
source.view

source.register

source.configure

source.approve

source.suspend

mapping.review

rights.review
```

and integrated with Baobab administrative authority.

---

# 237. Separation of Duties

A developer adding an adapter SHOULD NOT automatically possess authority to:

```text
approve legal source

approve rights

publish rules
```

These are separate roles.

---

# 238. Provider Secret Access

Regulatory analysts generally SHOULD NOT need raw vendor API secrets.

Secret handling remains infrastructure/security responsibility.

---

# 239. Acquisition Operator versus Regulatory Reviewer

Similarly:

```text
source operator
```

does not imply:

```text
regulatory interpretation authority.
```

---

# 240. Build Pipeline Security

Dependencies used solely by a provider adapter SHOULD remain isolated where possible.

A compromised provider SDK should have minimal reach into the regulatory domain.

---

# 241. Egress Control

Production acquisition workers SHOULD restrict outbound connectivity to approved source destinations where practical.

This reduces supply-chain and SSRF risk.

---

# 242. Inbound Webhooks

Provider webhooks SHALL be:

```text
authenticated

validated

replay-resistant where appropriate

rate-limited

idempotent
```

and treated as change notifications, not unquestioned canonical truth.

---

# 243. Webhook Event Triggers Acquisition

Preferred:

```text
Webhook:
something changed
     │
     ▼
Baobab acquisition
     │
     ▼
retrieve canonical source
```

rather than trusting arbitrary webhook payload as entire regulatory truth where stronger retrieval is available.

---

# 244. Source Replay

The engine SHOULD support replaying historical source artefacts through newer extraction/normalisation pipelines.

This is important as parsers improve.

---

# 245. Replay Shall Not Rewrite Historical Knowledge Time

A replay in 2028 of a 2026 artefact SHALL preserve:

```text
source effective time
source publication time
original acquisition time
new processing time
```

separately.

---

# 246. Source Fabric and Bitemporality

This distinction prepares for `ADR-REG-0015`.

Baobab must eventually answer both:

```text
What was legally valid at time T?
```

and:

```text
What did Baobab know at time T?
```

Source acquisition metadata is essential to the second question.

---

# 247. Provider Replacement Procedure

Replacing a material source provider SHOULD follow:

```text
1. Register replacement provider

2. Implement adapter

3. Map coverage

4. Backfill necessary evidence

5. Compare canonical outputs

6. Resolve semantic differences

7. Shadow acquisition

8. Verify freshness

9. Verify rights

10. Migrate source preference

11. Monitor

12. Retire old provider
```

---

# 248. Provider Replacement Is Not Simple Endpoint Change

Different providers may disagree about:

```text
granularity

scope

terminology

version history

interpretation

coverage
```

Semantic comparison is necessary.

---

# 249. Replacement Regression

Critical regulatory cases SHOULD be rerun after provider migration.

A source-provider swap that changes E3/E4 decisions requires investigation.

---

# 250. Exit Architecture

Baobab SHALL aim for this test:

```text
Remove Provider X
        │
        ▼
Source coverage may degrade
        │
        ▼
But canonical contracts,
historical decisions,
Baobab context,
rule identities,
assessment semantics
remain intact.
```

That is genuine provider neutrality.

---

# 251. Rejected Alternative — One Global Regulatory Vendor

Rejected.

It creates:

```text
commercial concentration risk

semantic lock-in

licensing lock-in

coverage blind spots

pricing dependency

exit risk
```

---

# 252. Rejected Alternative — Build Every Source Ourselves

Rejected.

It would consume capital reproducing mature commodity content infrastructure.

---

# 253. Rejected Alternative — Government Sources Only

Rejected.

Official sources are essential for authority but often lack:

```text
normalisation

global consistency

translation

structured APIs

cross-jurisdiction comparison
```

Commercial providers can add substantial value.

---

# 254. Rejected Alternative — Commercial Sources Only

Rejected.

For consequential decisions Baobab requires defensible paths to underlying authority.

---

# 255. Rejected Alternative — Provider Schema as Domain Model

Rejected.

This produces structural vendor lock-in.

---

# 256. Rejected Alternative — Generic Web Crawler

Rejected as the main architecture.

Discovery is not regulatory governance.

---

# 257. Rejected Alternative — LLM Browses Law at Transaction Time

Rejected.

Transactional evaluation should rely on governed regulatory state.

Live research belongs in discovery/review paths.

---

# 258. Rejected Alternative — One Unified Source Trust Score

Rejected.

Authority, freshness, reliability, rights and coverage are different dimensions.

---

# 259. Rejected Alternative — Copy All Commercial Data into Baobab

Rejected.

Licensing may prohibit it, and unnecessary duplication increases cost and liability.

---

# 260. Rejected Alternative — Don't Store Any Source Evidence

Rejected.

It would destroy auditability and historical reproducibility.

---

# 261. Rejected Alternative — Provider-Level Majority Vote

Rejected.

Law is not established by counting vendor outputs.

---

# 262. Positive Consequences

The architecture enables:

```text
provider substitution

multi-provider sourcing

direct government sourcing

commercial data integration

tenant-specific sources

source conflict detection

licensing governance

coverage packaging

historical evidence

regulatory provenance

cost optimisation

future Law-as-Code ingestion
```

---

# 263. Commercial Consequences

Baobab can buy global commodity regulatory content while concentrating engineering investment on:

```text
African corridor depth

contextual applicability

transaction execution

change impact

Pulse integration

customer-specific decision infrastructure
```

This materially improves the chance of achieving attractive margins.

---

# 264. Margin Consequence

Provider cost can be allocated against:

```text
jurisdiction pack

customer

assessment volume

commercial tier
```

allowing Baobab to know whether each regulatory product is economically viable.

---

# 265. Expansion Consequence

Entering Kenya need not mean:

```text
build Kenya engine.
```

It can mean:

```text
register KE sources
+
acquire / license content
+
build mappings
+
verify rules
+
publish KE pack.
```

That is scalable platform economics.

---

# 266. Trust Consequence

Baobab can show:

```text
what came from government

what came from provider

what Baobab normalised

what Baobab interpreted

what the customer supplied
```

rather than presenting one opaque corpus.

---

# 267. Resilience Consequence

Provider failure can degrade:

```text
specific sources
```

without destroying the entire Regulations engine.

---

# 268. Negative Consequences

This architecture creates:

```text
adapter maintenance

provider governance

mapping complexity

rights management

source reconciliation

coverage tracking

commercial procurement complexity
```

These are accepted costs.

---

# 269. Architectural Invariants

| ID | Invariant |
|---|---|
| `REG-P-I01` | Provider schema SHALL never become canonical Baobab regulatory schema |
| `REG-P-I02` | Provider and regulatory authority SHALL remain distinct |
| `REG-P-I03` | Provider-native IDs SHALL remain external references |
| `REG-P-I04` | External providers SHALL enter through anti-corruption adapters |
| `REG-P-I05` | Digital Estates SHALL not depend on regulatory vendors directly |
| `REG-P-I06` | Trade, ERP and Pulse SHALL consume Baobab regulatory contracts, not vendor responses |
| `REG-P-I07` | Acquisition SHALL remain separate from verification and canonical promotion |
| `REG-P-I08` | Raw source provenance SHALL remain recoverable |
| `REG-P-I09` | Provider replacement SHALL not require canonical API redesign |
| `REG-P-I10` | Multiple providers MAY support one regulatory domain |
| `REG-P-I11` | Multiple providers SHALL not be reconciled by majority voting |
| `REG-P-I12` | Source rights SHALL be recorded and enforced |
| `REG-P-I13` | Public accessibility SHALL not imply commercial reuse rights |
| `REG-P-I14` | Source freshness and provider availability SHALL remain distinct |
| `REG-P-I15` | Coverage gaps SHALL be explicit |
| `REG-P-I16` | Source failure SHALL not mean no regulation exists |
| `REG-P-I17` | Source preference SHALL remain distinct from legal hierarchy |
| `REG-P-I18` | Authority-supplied machine rules SHALL be supported directly |
| `REG-P-I19` | AI provider output SHALL remain provider-derived until governed promotion |
| `REG-P-I20` | Translation origin SHALL remain traceable |
| `REG-P-I21` | Provider contract termination SHALL not silently destroy historical decision explainability |
| `REG-P-I22` | Provider concentration risk SHALL be measurable |
| `REG-P-I23` | Regulatory packs SHALL be source-provider agnostic |
| `REG-P-I24` | Vendor cost SHALL not override required regulatory assurance |
| `REG-P-I25` | Provider neutrality SHALL be mechanically testable where practical |

---

# 270. Initial Source Strategy — Uganda/South Africa

The first implementation SHOULD intentionally use a mixed source strategy.

Potential architecture:

```text
UGANDA

Official:
    Gazette / government sources
    Uganda Trade Portal
    URA / relevant agencies
    commodity authorities
    SPS authorities

Regional:
    EAC
    AfCFTA

Commercial:
    selected provider where economically justified


SOUTH AFRICA

Official:
    Government Gazette
    SARS
    ITAC
    DALRRD / relevant SPS authorities

Regional:
    SACU
    SADC
    AfCFTA

Commercial:
    selected provider where economically justified
```

Exact sources require domain-specific source onboarding and verification.

---

# 271. ZuriBeans Proving Scenario

For:

```text
Uganda
   ↓
Coffee / Vanilla
   ↓
South Africa
```

the source fabric SHOULD demonstrate:

```text
at least one official UG source

at least one official ZA source

one regional/supranational source

one structured commercial or simulated provider

one customer-specific evidence artefact
```

flowing through the same canonical acquisition architecture.

---

# 272. Provider Swap Proof

The proving architecture SHOULD then replace:

```text
commercial provider A
```

with:

```text
commercial provider B / test double
```

without changing:

```text
RegulatoryAssessment API

Trade integration

ZuriBeans UI

canonical rule identity

decision contract
```

---

# 273. Source Failure Proof

The proof SHOULD deliberately make:

```text
one provider unavailable
```

and demonstrate:

```text
affected coverage degrades

unaffected regulatory domains continue

no false "no regulation" result appears.
```

---

# 274. Schema Drift Proof

The implementation SHOULD change a provider fixture incompatibly and demonstrate:

```text
SCHEMA_DRIFT
```

rather than silent bad mapping.

---

# 275. Rights Proof

A source marked:

```text
redistribution_allowed = false
```

SHOULD remain usable according to policy while its raw text is prevented from unauthorised customer exposure.

---

# 276. Licensing Expiry Proof

A simulated expired licence SHOULD cause:

```text
new usage denied/degraded
```

according to rights policy without deleting historical decision references improperly.

---

# 277. Conflict Proof

Official source and commercial provider SHOULD deliberately disagree in a test fixture.

The system SHALL surface conflict rather than majority-select or last-write-win.

---

# 278. Historical Provenance Proof

A 2026 regulatory decision should remain able to say:

```text
Provider X delivered representation R

based on Authority Y source A

acquired at T

normalised by Adapter v3

mapped into Rule R17
```

even after Provider X is no longer active.

---

# 279. Machine-Law Proof

The architecture SHOULD include a synthetic authority-supplied executable rule.

It should demonstrate that Baobab can treat:

```text
AUTHORITY_SUPPLIED_MACHINE_RULE
```

differently from:

```text
BAOBAB_DERIVED_RULE.
```

---

# 280. Initial Implementation Sequence

```text
REG-P0
Canonical source/provider abstractions

REG-P1
Source registry

REG-P2
Adapter interface

REG-P3
Raw acquisition

REG-P4
Source artefact preservation

REG-P5
Normalisation boundary

REG-P6
Canonical mapping

REG-P7
Coverage/freshness

REG-P8
Rights metadata

REG-P9
Official UG adapter

REG-P10
Official ZA adapter

REG-P11
Commercial/test provider

REG-P12
Conflict/reconciliation

REG-P13
Production hardening
```

---

# 281. Production Gate

No material source SHALL support production E3/E4 decisions until:

```text
provider/source registered

authority relationship established

rights confirmed

security reviewed

adapter tested

schema validated

freshness monitored

coverage declared

provenance preserved

canonical mappings reviewed

conflict behaviour tested

failure behaviour tested

source lifecycle documented
```

---

# 282. Follow-On ADRs

This ADR establishes the acquisition and provider boundary needed by:

```text
ADR-REG-0006
Canonical Regulatory Domain Model

ADR-REG-0007
Jurisdiction, Regulatory Authority
and Legal Hierarchy Model

ADR-REG-0008
Instrument, Provision, Rule
and Obligation Model

ADR-REG-0010
Regulatory Knowledge Graph

ADR-REG-0011
Authoritative Source Registry
and Source Trust Model

ADR-REG-0012
Regulatory Content Acquisition,
Licensing and Reuse Rights

ADR-REG-0013
Source Ingestion,
Normalisation and Adapter Architecture

ADR-REG-0014
Provenance, Citation and Evidentiary Chain
```

There is deliberate overlap.

`ADR-REG-0005` establishes the **constitutional provider-neutrality rules**.

The later ADRs define their detailed domain and implementation semantics.

---

# 283. Research Foundation

The OECD's current Law-as-Code initiative explicitly identifies repeated vendor-specific translations of legal logic as producing inconsistency, interoperability problems and dependence on individual providers. It proposes authoritative, source-linked machine-executable law as shared infrastructure rather than a proprietary vendor format.

W3C DCAT 3 provides established distinctions among datasets, distributions, data services and dataset series, alongside metadata for versioning, access rights, licensing and provenance—useful concepts for Baobab's source catalogue without forcing Baobab to adopt RDF internally.

OASIS LegalRuleML explicitly treats links between machine rules and legally binding textual sources as necessary for provenance, authority, authenticity, validation and updating rules when source law changes.

The WCO Data Model provides harmonised reusable definitions and messages for customs and other cross-border regulatory agencies and continues to evolve; version 4.3.0 was approved in June 2026 with expanded digital-document and JSON-oriented capabilities.

Thomson Reuters demonstrates the scale and value of commercially maintained global regulatory content, advertising coverage across more than 220 countries and territories, more than 1,300 monitored government sources, structured trade content and APIs for integration into enterprise workflows.

RegGenome demonstrates the viability of structured regulatory data that preserves conditions, context, relationships and links to original source regulation while serving downstream compliance and risk platforms.

FiscalNote's 2026 PolicyNote API and MCP expansion demonstrates that policy and regulatory providers are increasingly exposing their data directly to enterprise applications and AI agents, reinforcing the need for Baobab to treat access protocol and provider as interchangeable infrastructure concerns.

Originvia provides a contemporary African competitive signal: provenance, corridor-specific compliance and workflow integration are already being positioned as regulated-trade infrastructure for Africa-linked corridors.

---

# 284. Final Decision

Baobab Regulations SHALL implement a **provider-neutral Regulatory Source Fabric**.

The canonical model is:

```text
                         EXTERNAL WORLD

          ┌───────────────┬────────────────┐
          │               │                │
     Governments      Commercial       Standards /
     & Regulators      Providers      Regional Bodies
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                  PROVIDER ADAPTERS
                          │
                anti-corruption layer
                          │
                          ▼
                  RAW SOURCE EVIDENCE
                          │
                          ▼
                    NORMALISATION
                          │
                          ▼
              AUTHORITY / SOURCE MAPPING
                          │
                          ▼
            BAOBAB REGULATORY KNOWLEDGE
                          │
                          ▼
                   INTERPRETATION
                          │
                          ▼
                       RULE
                          │
                          ▼
                   APPLICABILITY
                          │
                          ▼
                     DECISION
```

Baobab SHALL remain free to:

```text
add a provider

remove a provider

replace a provider

combine providers

use official sources directly

accept authority-supplied machine law

accept customer-specific evidence

use AI extraction

change AI provider

change parser

change source transport
```

without redefining:

```text
Regulatory Authority

Instrument

Provision

Rule

Obligation

Assessment

Decision

Capability

Digital Estate contract
```

The strategic doctrine is:

> **Use the best regulatory information available, but never rent Baobab's architecture from the company that supplies it.**

And commercially:

> **Buy commodity regulatory content where others have already built it well. Own the contextual regulatory execution layer they cannot easily replicate inside Baobab.**

This is the balance required for Baobab Regulations to scale internationally without either extreme:

```text
vendor dependency
```

or:

```text
reinventing the world's regulatory databases.
```

The winning architecture is:

```text
Best available sources
       +
Provider neutrality
       +
Source provenance
       +
Baobab canonical semantics
       +
Baobab Context
       +
Regulatory execution
```

That is what `ADR-REG-0005` establishes.

---

## Decision Summary

```text
ADR-REG-0005
──────────────────────────────────────────────

DECISION

Create a provider-neutral Regulatory
Source Fabric.

BAOBAB OWNS

canonical semantics
authority mapping
provenance
context
applicability
decision
execution contracts

PROVIDERS MAY SUPPLY

regulatory content
structured obligations
tariffs
rules of origin
monitoring
translations
classification
source aggregation

CORE RULE

Provider
    ≠
Authority
    ≠
Canonical Baobab model

PIPELINE

Provider
  ↓
Adapter
  ↓
Raw Evidence
  ↓
Normalisation
  ↓
Authority Mapping
  ↓
Canonical Regulation
  ↓
Interpretation
  ↓
Rule

ANTI-LOCK-IN TEST

Remove Vendor X.

Trade still works.
Pulse still works.
ZuriBeans still works.
Contracts remain stable.
Historical decisions remain explainable.

BUILD

Baobab context
applicability
execution
impact
decision graph

BUY WHERE RATIONAL

commodity regulatory content
global datasets
specialist coverage

STRATEGIC RESULT

Use the world's best regulatory data
without allowing any provider to become
Baobab Regulations.
```
# ADR-REG-0029 — Jurisdiction Packs, Regulatory Modules, Coverage Model and Regulatory Marketplace Architecture

**Subtitle:** Composable Regulatory Knowledge Products, Coverage Manifests, Signed Distribution, Supply-Chain Provenance, Publisher Governance, Marketplace Admission and Safe Third-Party Extensibility

**Status:** Proposed — Foundational Regulatory Distribution Architecture  
**Decision ID:** `ADR-REG-0029`  
**Engine:** `baobab-platform/baobab-regulations`  
**Cross-Repository Dependencies:** `baobab-platform/shared`, `baobab-platform/baobab-cp`, `baobab-platform/baobab-iam`, `baobab-platform/infrastructure`  
**Initial Reference Profile:** Uganda → South Africa, coffee and vanilla  
**Date:** 2026-09-29  
**Decision Type:** Regulatory Packaging / Coverage / Distribution / Marketplace / Extension Governance / Supply-Chain Security  
**Strategic Classification:** Core Regulatory Product and Ecosystem Architecture

---

# 1. Executive Decision

Baobab Regulations SHALL introduce a composable regulatory packaging architecture built around:

```text
RegulatoryModule

JurisdictionPack

RegulatoryRegimePack

CommodityProfile

CorridorProfile

CoverageManifest

PackRelease

PackAttestation

RegulatoryPackLock

MarketplaceCatalogEntry

PublisherProfile

PackActivation
```

The governing architecture is:

```text
                  AUTHORITATIVE SOURCES
                          │
                          ▼
                 Regulatory Knowledge
                          │
                          ▼
              Verified Regulatory Modules
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Jurisdiction   Regime       Domain
           Packs        Packs       Modules
             │            │            │
             └────────────┼────────────┘
                          ▼
                   Coverage Model
                          │
                          ▼
                 Pack Certification
                          │
                          ▼
                 Signed Pack Release
                          │
                          ▼
                   Pack Registry
                          │
                          ▼
               Regulatory Marketplace
                          │
                          ▼
               Entitlement / Selection
                          │
                          ▼
                  Pack Composition
                          │
                          ▼
                 Effective RuleSet
                          │
                          ▼
                  Signed OPA Bundle
                          │
                          ▼
                Regulatory Decision
```

The core doctrine is:

> **A regulatory pack packages verified regulatory knowledge; it does not create legal authority.**

---

# 2. Purpose

The initial Uganda → South Africa regulatory profile established in `ADR-REG-0027` must not become a one-off implementation.

Baobab needs to expand eventually toward corridors involving:

```text
Kenya

Tanzania

Rwanda

Uganda

South Africa

other African markets

regional arrangements

global trade regimes.
```

That requires reuse without duplication.

---

# 3. The Wrong Scaling Model

Rejected:

```text
if corridor == UG_ZA:
    rules = ug_za_rules

if corridor == UG_KE:
    rules = ug_ke_rules

if corridor == KE_ZA:
    rules = ke_za_rules
```

This creates:

```text
duplicated law

inconsistent updates

untraceable divergence

corridor-specific monoliths.
```

---

# 4. The Correct Scaling Model

```text
Uganda Pack
      │
      ├── Customs Export
      ├── Plant Health
      ├── Coffee Export
      └── Other UG modules


South Africa Pack
      │
      ├── Customs Import
      ├── Tariff
      ├── VAT
      ├── Plant Health
      └── Other ZA modules


AfCFTA Pack
      │
      ├── Origin
      ├── Preference
      └── Transport conditions


Coffee Profile
      │
      ├── classification facts
      └── commodity-specific mappings


Vanilla Profile
      │
      └── commodity-specific mappings


                  ↓ COMPOSITION ↓


        UG → ZA Regulatory Profile
```

---

# 5. Pack ≠ Law

Hard invariant:

```text
JurisdictionPack
≠
legal instrument.
```

A pack contains or references Baobab's structured representation of regulatory material.

---

# 6. Pack ≠ Regulatory Authority

A pack signed by:

```text
Baobab

law firm

consultant

government agency

commercial data provider
```

does not automatically determine the legal force of its contents.

Authority remains governed through:

```text
ADR-REG-0003

ADR-REG-0007

ADR-REG-0011.
```

---

# 7. Pack ≠ Capability

A jurisdiction pack is regulatory content.

A Control Plane capability is:

```text
what the tenant is permitted
to use.
```

Those remain different.

---

# 8. Pack ≠ Commercial Product

A pack may underpin:

```text
subscription product

market add-on

premium regulatory profile.
```

But commercial productisation belongs primarily to `ADR-REG-0030`.

---

# 9. Pack ≠ Installation

A pack can exist in the catalog without being:

```text
entitled

downloaded

staged

activated.
```

---

# 10. Pack ≠ Activation

A downloaded pack SHALL NOT automatically enter production regulatory evaluation.

---

# 11. Critical Lifecycle

```text
PACK EXISTS
    │
    ▼
PACK PUBLISHED
    │
    ▼
TENANT ENTITLED
    │
    ▼
PACK RESOLVED
    │
    ▼
PACK VERIFIED
    │
    ▼
PACK STAGED
    │
    ▼
COMPOSITION VALIDATED
    │
    ▼
RULESET BUILT
    │
    ▼
RULESET CERTIFIED
    │
    ▼
RUNTIME ACTIVATED.
```

Every transition is distinct.

---

# 12. Baobab Platform Alignment

The existing Baobab architecture establishes:

> **Standardise the contracts, not the implementations.**

and explicitly treats Baobab as a platform composed of independently implemented engines behind shared identity, API, event, audit, security and deployment conventions.

The regulatory packaging architecture SHALL follow the same principle.

---

# 13. Control Plane Desired State Remains Provider-Neutral

Baobab's current desired-state architecture already carries:

```text
tenant

legal_entities

products / profiles

market_participation

digital_estates

isolation_requirement

residency_requirement
```

while excluding:

```text
engine

EngineInstance

provider

CapabilityGrant

CapabilityBinding.
```



Regulatory-pack selection SHALL preserve this provider-neutral architecture.

---

# 14. Tenant Intent

A tenant SHOULD be able to request conceptually:

```text
Cross-border regulatory coverage:

Uganda → South Africa

Coffee

Customs
Origin
SPS
Documents
```

not:

```text
install OCI artifact
sha256:...
into OPA instance X.
```

---

# 15. Control Plane and Regulations Responsibilities

```text
CONTROL PLANE
─────────────────────────
Tenant entitlement

Commercial/product profile

Capability grants

Provider resolution

EngineInstance

Isolation

Residency


REGULATIONS
─────────────────────────
Pack registry

Coverage resolution

Pack dependencies

Pack composition

RuleSet construction

Certification

Activation readiness

Regulatory execution.
```

---

# 16. Core Packaging Types

Baobab SHALL define multiple package concepts rather than one universal pack.

---

# 17. RegulatoryModule

A:

# `RegulatoryModule`

is the smallest reusable governed regulatory rule family.

Examples:

```text
CUSTOMS_CLASSIFICATION

CUSTOMS_VALUATION

CUSTOMS_DECLARATION

IMPORT_TARIFF

IMPORT_VAT

EXPORT_CONTROL

IMPORT_CONTROL

SPS

PLANT_HEALTH

RULES_OF_ORIGIN

TRADE_PREFERENCE

DOCUMENT_REQUIREMENTS

LICENSING

LABELLING

SANCTIONS.
```

---

# 18. Module Is Semantic, Not Geographic

Example:

```text
customs-valuation
```

is a regulatory domain module.

Its concrete rules may vary by jurisdiction.

---

# 19. ModuleDefinition

Conceptually:

```text
RegulatoryModuleDefinition
├── module_key
├── canonical_name
├── regulatory_domain
├── semantic_contract_version
├── required_context_facets[]
├── output_types[]
├── dependencies[]
├── BRIR_feature_requirements[]
└── description
```

---

# 20. Module Definition ≠ Module Release

The definition describes:

```text
what this regulatory capability means.
```

A release contains actual verified knowledge.

---

# 21. JurisdictionPack

A:

# `JurisdictionPack`

packages regulatory knowledge associated with one legal jurisdiction or authority scope.

---

# 22. Examples

```text
ZA Customs Import

ZA Plant Health

ZA Import VAT

UG Customs Export

UG Coffee Export

UG Plant Health.
```

---

# 23. Jurisdiction Pack Does Not Need to Cover Everything

A South African pack MAY cover:

```text
customs
```

without covering:

```text
employment

competition

environmental law.
```

Coverage SHALL therefore be explicit.

---

# 24. RegulatoryRegimePack

A:

# `RegulatoryRegimePack`

models a regulatory regime spanning multiple jurisdictions.

Examples:

```text
AfCFTA

EAC

SACU

SADC

WTO-related rule families

bilateral trade agreements.
```

---

# 25. Regime ≠ Jurisdiction

Hard invariant.

---

# 26. Regime Pack Does Not Replace Domestic Implementation

An international/regional rule may require:

```text
domestication

national implementation

tariff schedule gazetting

authority action.
```

Regime pack and jurisdiction pack may therefore interact.

---

# 27. CommodityProfile

A:

# `CommodityRegulatoryProfile`

captures verified commodity-specific regulatory knowledge.

Examples:

```text
coffee

vanilla

tea

maize.
```

---

# 28. Commodity Profile Should Be Thin

It SHOULD primarily contain:

```text
classification facts

product-state semantics

commodity-specific requirements

domain mappings

golden cases.
```

It SHALL NOT duplicate every applicable national law.

---

# 29. CorridorProfile

A:

# `CrossBorderCorridorProfile`

is a governed composition.

Example:

```text
UG → ZA

coffee

requires:

UG export modules

UG plant-health modules

AfCFTA origin modules

ZA customs modules

ZA plant-health modules

commodity profile.
```

---

# 30. Corridor Profile Is Not a Giant Rules File

It is primarily:

```text
composition

scope

coverage

dependency

certification metadata.
```

---

# 31. Transit Profiles

Selected transport routes may additionally require:

```text
TransitJurisdictionPack

TransitCustomsProfile.
```

Those SHOULD be composed only when the actual route requires them.

---

# 32. Canonical Composition

```text
CrossBorder Profile
       │
       ├── Origin Jurisdiction Pack
       │
       ├── Export Modules
       │
       ├── Regional Regime Pack
       │
       ├── Transit Packs[]
       │
       ├── Import Jurisdiction Pack
       │
       ├── Destination Modules
       │
       └── Commodity Profile
       │
       ▼
Effective Regulatory RuleSet.
```

---

# 33. Regulatory Pack Manifest

Every published pack SHALL include a machine-readable:

# `RegulatoryPackManifest`

---

# 34. Conceptual Manifest

```yaml
pack_id: io.baobab.regulations.za.customs-import
pack_type: JURISDICTION_PACK

publisher_ref: baobab

release_version: 2026.09.29.1

jurisdictions:
  - ZA

domains:
  - CUSTOMS_IMPORT
  - TARIFF_CLASSIFICATION

compatible_contracts:
  brir: "1.x"
  regulations_api: "1.x"

dependencies:
  - pack_ref: io.baobab.regulations.core.customs
    digest: sha256:...

coverage_manifest_ref: sha256:...
source_manifest_ref: sha256:...
rules_manifest_ref: sha256:...
test_evidence_ref: sha256:...
provenance_ref: sha256:...

artifact_digest: sha256:...
```

The exact schema SHALL be defined canonically in `shared` where cross-platform consumption requires it.

---

# 35. Pack Identity

A pack SHALL have:

```text
stable logical identity
```

separate from:

```text
release version.
```

---

# 36. Example

```text
Pack:
ZA-CUSTOMS-IMPORT

Release:
2026.09.29.1
```

---

# 37. Release Version ≠ Legal Version

Critical invariant:

```text
PackReleaseVersion
≠
law effective date

≠
InstrumentVersion

≠
RuleVersion.
```

---

# 38. Why

A package release might contain:

```text
two legal changes

one parser correction

one test improvement.
```

Conversely:

```text
one new law
```

might require multiple packaging releases due to technical corrections.

---

# 39. SemVer SHALL NOT Encode Legal Significance

Rejected:

```text
major = big law change

minor = small law change.
```

Legal significance cannot safely be inferred that way.

---

# 40. Semantic Versioning May Still Be Used

SemVer MAY govern:

```text
manifest schema compatibility

BRIR API compatibility

module contract compatibility.
```

It SHALL NOT define legal chronology.

---

# 41. Content Addressability

Production releases SHALL have a cryptographic content digest.

Example:

```text
sha256:...
```

---

# 42. Digest Is Stronger Than Mutable Tag

Runtime activation SHALL reference immutable digest/version identity.

Rejected:

```text
regpack:latest
```

as the sole production identifier.

---

# 43. Human-Friendly Tags

Tags MAY exist for:

```text
stable

candidate

2026-09

ZA-current.
```

But runtime state SHALL record the underlying digest.

---

# 44. OCI Distribution

OCI provides a useful provider-neutral transport mechanism.

The OCI Image Manifest supports non-container artifacts through `artifactType`, descriptors, layers, digests and `subject` relationships. The OCI Distribution 1.1 referrers API can additionally retrieve associated artifacts such as signatures or attestations by subject digest.

Baobab SHOULD therefore support OCI-compatible distribution of regulatory pack artifacts.

---

# 45. OCI Is Transport, Not Domain Semantics

Hard invariant:

```text
OCI Artifact
≠
RegulatoryPack.
```

OCI transports pack bytes.

Baobab defines their meaning.

---

# 46. Candidate Media Type

Baobab MAY define a media type conceptually such as:

```text
application/vnd.baobab.regulations.pack.v1+tar
```

subject to appropriate media-type governance.

---

# 47. OCI Packaging Is Optional Implementation

The canonical pack format SHALL remain exportable/importable independently of one registry vendor.

---

# 48. Possible Artifact Layout

```text
manifest.json

coverage/
    coverage.json

sources/
    manifest.json

rules/
    ruleset.json

brir/
    ...

tests/
    golden-manifest.json

docs/
    README.md

provenance/
    attestations.json
```

Raw source documents SHOULD only be included where ADR-REG-0012 rights permit.

---

# 49. Pack SHALL Prefer References to Restricted Source Content

For licensed sources:

```text
source identity

hash

provenance

allowed derived data
```

may travel without redistributing the raw source.

---

# 50. Regulatory Package Bill of Materials

Baobab SHALL define a:

# `RegulatoryPackageBillOfMaterials`

or equivalent manifest.

---

# 51. It Should Enumerate

```text
SourceArtefact versions

InstrumentVersions

ProvisionVersions

Interpretations

RuleVersions

BRIR version

compiled outputs

golden suites

test evidence

dependency packs

compiler version.
```

---

# 52. Regulatory BOM ≠ Software SBOM

A software SBOM describes software components.

The Regulatory BOM describes the regulatory knowledge lineage inside a pack.

If a pack/distribution also includes software:

```text
normal software SBOM
```

should additionally apply.

---

# 53. Supply-Chain Provenance

Each published artifact SHOULD carry verifiable build provenance.

SLSA's current provenance specification defines machine-readable provenance describing where, when and how an artifact was produced and uses the in-toto attestation framework.

Baobab SHOULD adopt compatible supply-chain provenance concepts for pack construction.

---

# 54. SLSA Provenance Is Technical Provenance

It can establish:

```text
what repository

which builder

which workflow

which inputs

which artifact.
```

It does NOT establish:

```text
legal interpretation is correct.
```

---

# 55. Regulatory Attestation Is Separate

Baobab SHALL define a regulatory-domain:

# `RegulatoryPackAttestation`

---

# 56. RegulatoryPackAttestation

Conceptually:

```text
RegulatoryPackAttestation
├── pack_digest
├── source_manifest_digest
├── regulatory_review_refs[]
├── reviewer_policy_ref
├── golden_suite_digest
├── certification_ref
├── maximum_effect_class
├── known_gaps[]
├── issued_at
└── provenance
```

---

# 57. in-toto Compatibility

The in-toto Attestation Framework is designed for verifiable claims about how artifacts were produced and supports extensible predicates.

Baobab MAY therefore encode:

```text
build provenance

regulatory certification

test certification

rights verification
```

as distinct attestations attached to the same pack artifact.

---

# 58. Do Not Collapse Attestations

```text
artifact built correctly
```

and:

```text
regulatory interpretation verified
```

are separate statements.

---

# 59. Pack Signing

Every production-eligible pack release SHALL be signed.

---

# 60. Signature Establishes

```text
integrity

publisher identity

artifact authenticity.
```

It does not establish:

```text
legal correctness.
```

---

# 61. Sigstore Compatibility

Sigstore/Cosign supports signatures and verification material for artifacts, including identity-bound keyless signing and transparency-log evidence.

Baobab MAY use Sigstore-compatible signing for public/appropriate pack channels.

---

# 62. Transparency Logs Need Classification Awareness

A public transparency log may expose:

```text
artifact identity

publisher identity

timestamps

repository information.
```

Tenant-private pack metadata SHALL NOT be published to a public transparency service without explicit policy approval.

---

# 63. Private Signing

Private packs MAY use:

```text
KMS-backed signatures

private Sigstore deployment

offline signing

enterprise PKI.
```

The canonical requirement is cryptographic verifiability—not dependence on one signing provider.

---

# 64. Signature Verification Is Required Before Import

```text
Download
   ↓
Digest check
   ↓
Signature verification
   ↓
Provenance verification
   ↓
Only then parse/import.
```

---

# 65. Package Registry Attack Model

The marketplace must consider:

```text
artifact replacement

rollback

freeze

mix-and-match

publisher key compromise

dependency confusion

namespace takeover.
```

---

# 66. TUF Reference Architecture

The Update Framework is designed to secure update systems against attacks including rollback, freeze, mix-and-match and repository compromise. It uses signed root, targets, snapshot and timestamp roles and supports delegated trust with revocation.

Baobab SHOULD adopt TUF-compatible or equivalently strong update-metadata semantics for high-assurance marketplace distribution.

---

# 67. Why Registry Signatures Alone Are Insufficient

A correctly signed old pack might still be:

```text
cryptographically authentic
```

but:

```text
obsolete.
```

---

# 68. Anti-Rollback

Production pack resolution SHALL know:

```text
current authorised release
```

and SHALL reject an unintended older release.

---

# 69. Explicit Historical Pinning Is Not Rollback

Historical replay MAY intentionally load:

```text
old pack digest.
```

That is valid historical evaluation.

---

# 70. Operational Rollback

An operator MAY intentionally revert production to an earlier technically valid pack only through an explicit controlled-change process.

---

# 71. Rollback Requires Reason

Example:

```text
new package contains compiler defect.
```

The rollback SHALL remain audited.

---

# 72. Freeze Detection

If marketplace metadata has not refreshed within its expected update horizon:

```text
MARKETPLACE_METADATA_STALE.
```

This SHALL be distinguishable from:

```text
no regulatory change occurred.
```

---

# 73. Dependency Delegation

TUF-style delegation is also useful conceptually for publishers.

Example:

```text
Baobab marketplace root
      │
      ├── delegate:
      │     ZA/*
      │     to approved ZA publisher role
      │
      └── delegate:
            tax/*
            to specialised provider.
```

---

# 74. Platform Delegation ≠ Legal Authority

Marketplace permission to publish:

```text
ZA/*
```

does not make the publisher a South African legal authority.

---

# 75. PublisherProfile

Baobab SHALL define:

# `RegulatoryPublisherProfile`

---

# 76. Conceptual Model

```text
RegulatoryPublisherProfile
├── publisher_ref
├── organisation_ref
├── identity_verification
├── allowed_namespaces[]
├── allowed_pack_types[]
├── allowed_domains[]
├── allowed_jurisdictions[]
├── signing_identity[]
├── admission_status
├── governance_requirements[]
└── provenance
```

---

# 77. Publisher Types

Potential factual classifications:

```text
BAOBAB_FIRST_PARTY

AUTHORITY_SUPPLIED

COMMERCIAL_PROVIDER

REGULATORY_SPECIALIST

LEGAL_PROVIDER

TENANT_PRIVATE

COMMUNITY_SUBMISSION.
```

---

# 78. Publisher Type Is Not Quality Score

Hard invariant.

---

# 79. Authority-Supplied Pack

An authority-supplied artifact may carry greater source significance.

But Baobab must still determine:

```text
what is binding

what is guidance

what is draft

what is machine-readable representation

effective date.
```

---

# 80. Commercial Provider Pack

A commercial provider may supply excellent curated knowledge.

It still does not become:

```text
the law.
```

---

# 81. Tenant Private Pack

A tenant may create:

```text
private counsel interpretation

tenant exemption

binding ruling overlay.
```

Such packs remain isolated under `ADR-REG-0028`.

---

# 82. Community Pack

Community contributions MAY be admitted into:

```text
DISCOVERY

RESEARCH

CANDIDATE
```

states.

They SHALL NOT directly become E3/E4 executable regulation.

---

# 83. No Single Publisher Trust Score

Rejected:

```text
publisher_trust = 94.
```

Publisher assurance remains multidimensional.

---

# 84. Relevant Publisher Dimensions

Possible:

```text
verified identity

organisation verification

legal/regulatory competence

publication history

security posture

signing integrity

source provenance quality

licensing compliance

review history.
```

---

# 85. Publisher Assurance ≠ Source Trust

A highly reputable publisher can still cite:

```text
wrong source.
```

---

# 86. Publisher Assurance ≠ Pack Certification

A known publisher can still publish:

```text
broken pack release.
```

---

# 87. Publisher Assurance ≠ Legal Authority

These SHALL remain separate.

---

# 88. Marketplace Submission Pipeline

Third-party publishing SHALL flow through:

```text
Publisher
   │
   ▼
Submission
   │
   ▼
Quarantine
   │
   ▼
Artifact Integrity
   │
   ▼
Signature Verification
   │
   ▼
Rights Validation
   │
   ▼
Source Trust Validation
   │
   ▼
Schema Validation
   │
   ▼
Regulatory Semantic Review
   │
   ▼
Golden / Regression Tests
   │
   ▼
Pack Certification
   │
   ▼
Marketplace Publication
```

---

# 89. Marketplace Submission Never Writes Directly to OPA

Hard invariant.

---

# 90. Marketplace Submission Never Writes Directly to Canonical Rule Tables

It enters a governed staging boundary.

---

# 91. Quarantine

Untrusted pack content SHALL initially have:

```text
no production RuleSet authority

no tenant retrieval access

no OPA activation

no execution hooks.
```

---

# 92. No Arbitrary Executable Code in Standard Regulatory Packs

Standard regulatory packs SHOULD consist of:

```text
declarative metadata

canonical knowledge

BRIR

test fixtures

documentation

derived Rego/OPA artifacts

structured data.
```

---

# 93. Post-Install Scripts Are Prohibited

Rejected:

```text
install.sh

setup.py hook

npm postinstall

arbitrary executable migration script
```

inside a normal regulatory pack.

---

# 94. Why

A regulatory marketplace SHALL NOT become:

```text
remote code execution as a service.
```

---

# 95. Adapter Extensions Are Separate

A source adapter may genuinely require executable code.

That SHALL be governed as a separate:

```text
RegulatoryAdapterExtension
```

security domain.

---

# 96. Adapter Extension Requires

```text
source review

software supply-chain review

sandboxing

permissions

network policy

secrets policy

security testing.
```

It SHALL NOT gain executable privileges merely because a regulatory pack depends on it.

---

# 97. Marketplace Pack May Reference Adapter Capability

Example:

```text
requires source-adapter:
SARS_TARIFF_V1
```

The adapter remains independently installed and governed.

---

# 98. BRIR Is the Preferred Executable Portability Layer

Third-party pack authors SHOULD target:

```text
Baobab canonical regulatory semantics

+
BRIR.
```

They SHOULD NOT need to target one specific OPA deployment.

---

# 99. Third-Party Rego Is Candidate Material

A marketplace publisher MAY include Rego for:

```text
reference

comparison

candidate optimisation.
```

Baobab SHALL NOT automatically trust arbitrary supplied Rego as final E3/E4 executable policy.

---

# 100. Preferred Activation

```text
Verified Pack
      │
      ▼
Canonical RuleVersions
      │
      ▼
BRIR
      │
      ▼
Baobab Trusted Compiler
      │
      ▼
OPA Bundle
      │
      ▼
Baobab Signature
      │
      ▼
Runtime.
```

---

# 101. This Protects Semantics

A publisher cannot hide:

```text
network calls

unexpected built-ins

undeclared data

policy side effects
```

inside arbitrary execution code.

---

# 102. OPA Bundle Boundary

OPA bundles support policy/data packaging, bundle revisions and cryptographic verification. They can be dynamically downloaded and activated by OPA without restarting the runtime.

OPA bundles SHALL therefore remain the **runtime execution package**, not the marketplace regulatory package.

---

# 103. Pack → RuleSet → OPA Bundle

Not:

```text
Marketplace Pack
=
OPA Bundle.
```

---

# 104. Multiple Packs May Produce One OPA Bundle

Example:

```text
UG Export Pack
+
AfCFTA Origin Pack
+
ZA Import Pack
+
Coffee Profile
        │
        ▼
Effective RuleSet
        │
        ▼
one signed OPA execution package.
```

---

# 105. Pack Dependencies

A pack MAY depend upon other packs/modules.

---

# 106. Dependency Types

Potential:

```text
REQUIRED

OPTIONAL

CONDITIONAL

CONFLICTS_WITH

SUPERSEDES.
```

---

# 107. Dependency Resolution Must Be Deterministic

The same:

```text
requested profile

catalog state

lock file
```

SHALL resolve to the same exact package set.

---

# 108. No Floating Dependencies in Production

Rejected:

```text
requires:
  za-customs: latest
```

---

# 109. Production Dependencies Pin Digests

Preferred:

```text
za-customs:
    digest: sha256:...
```

---

# 110. RegulatoryPackLock

Baobab SHALL generate:

# `RegulatoryPackLock`

---

# 111. Conceptual Lock

```yaml
profile: UG-ZA-COFFEE

packs:
  - id: ug-customs-export
    release: 2026.09.1
    digest: sha256:...

  - id: afcfta-origin
    release: 2026.08.4
    digest: sha256:...

  - id: za-customs-import
    release: 2026.09.3
    digest: sha256:...

brir_schema: 1.0
compiler: ...
generated_at: ...
```

---

# 112. Pack Lock Supports Reproducibility

Historical replay can reconstruct:

```text
which regulatory packages
produced the active RuleSet.
```

---

# 113. Pack Lock ≠ RuleSet Fingerprint

The RuleSet fingerprint SHALL additionally capture the actual composed executable regulatory semantics.

---

# 114. Circular Dependencies

Pack dependency cycles SHALL be rejected unless a future explicit composition model safely supports them.

Default:

```text
acyclic.
```

---

# 115. Technical Dependency Conflict ≠ Legal Rule Conflict

Hard invariant.

---

# 116. Example Technical Conflict

```text
Pack A requires BRIR 2.x

Pack B requires BRIR 1.x.
```

---

# 117. Example Legal Conflict

```text
Rule A appears to permit

Rule B appears to prohibit.
```

The latter belongs to ADR-REG-0007/0009 semantics.

---

# 118. Do Not Solve Legal Conflict With Package Version Resolver

---

# 119. Namespace Ownership

Pack identifiers SHALL exist within governed namespaces.

Examples:

```text
baobab/za/...

baobab/ug/...

authority/sars/...

partner/example/...
```

Exact syntax remains a contract decision.

---

# 120. Namespace Squatting Is Prohibited

Publisher admission SHALL control which publisher may publish into which namespace.

---

# 121. Publisher Revocation

A publisher's future publishing rights MAY be revoked.

That SHALL NOT erase already-used historical pack versions.

---

# 122. Compromised Publisher Key

Response:

```text
revoke key

suspend affected releases

determine exposure window

verify pack digests

reissue clean packs

reassess affected deployments.
```

---

# 123. Marketplace Artifact Lifecycle

Potential:

```text
SUBMITTED

QUARANTINED

VALIDATING

UNDER_REVIEW

CERTIFIED

PUBLISHED

DEPRECATED

SUSPENDED

REVOKED

RETIRED.
```

---

# 124. Pack Activation Lifecycle Is Separate

Potential:

```text
NOT_ENTITLED

ENTITLED

RESOLVED

DOWNLOADED

VERIFIED

STAGED

ACTIVE

DEGRADED

SUPERSEDED

DISABLED.
```

---

# 125. Marketplace Status ≠ Runtime Status

Hard invariant.

---

# 126. A Pack Can Be Published but Not Certified for E3

---

# 127. A Pack Can Be Certified but Not Entitled to Tenant

---

# 128. A Pack Can Be Entitled but Not Activated

---

# 129. A Pack Can Be Active Historically but Superseded Currently

---

# 130. Coverage Is First-Class

The most important marketplace metadata is not:

```text
number of rules.
```

It is:

```text
what the pack actually covers.
```

---

# 131. Regulatory Coverage Model

Baobab SHALL define:

# `RegulatoryCoverageManifest`

---

# 132. Coverage Dimensions

Coverage MAY include:

```text
jurisdiction

jurisdiction role

regulatory regime

regulatory domain

regulated activity

actor role

commodity

HS chapter/heading/subheading

transaction stage

direction

trade lane

legal-time interval

source language

document/evidence family.
```

---

# 133. Coverage Also Needs Assurance Dimensions

Separately:

```text
source coverage

interpretation coverage

rule coverage

execution coverage

test coverage

change-monitoring coverage.
```

---

# 134. Coverage Is Not One Percentage

Rejected:

```text
South Africa coverage = 93%.
```

Without a defined denominator this has little meaning.

---

# 135. Better

```text
ZA

Domain:
customs tariff

HS:
Chapters 01–97

Legal time:
from 2026-08-28

Source:
verified

Rule coverage:
complete for tariff lookup

Execution:
E3-certified

Change monitoring:
active.
```

---

# 136. CoverageClaim

Conceptually:

```text
CoverageClaim
├── coverage_claim_id
├── pack_ref
├── jurisdiction_scope[]
├── jurisdiction_roles[]
├── regime_scope[]
├── regulatory_domains[]
├── activities[]
├── actor_roles[]
├── commodity_scope[]
├── classification_scope[]
├── transaction_stages[]
├── legal_time_range
├── source_coverage
├── interpretation_coverage
├── rule_coverage
├── execution_coverage
├── change_monitoring_coverage
├── assurance_ref
└── provenance
```

---

# 137. Coverage State

Canonical states SHOULD remain descriptive.

Potential:

```text
UNKNOWN

NOT_COVERED

PARTIAL

COVERED

COVERED_WITH_KNOWN_GAPS.
```

---

# 138. Assurance Is Separate

For example:

```text
coverage = COVERED

certification =
REVIEW_GATE_READY.
```

---

# 139. Or

```text
coverage = PARTIAL

certification =
ADVISORY_READY.
```

---

# 140. Known Gap

Baobab SHALL model:

# `CoverageGap`

---

# 141. Conceptually

```text
CoverageGap
├── gap_id
├── pack_ref
├── domain
├── scope
├── reason
├── consequence
├── discovered_at
├── remediation_ref?
└── provenance
```

---

# 142. Gap Reasons

Potential:

```text
SOURCE_UNAVAILABLE

RIGHTS_RESTRICTED

INTERPRETATION_UNRESOLVED

RULE_NOT_ENCODED

TESTS_INCOMPLETE

AUTHORITY_CONFLICT

EFFECTIVE_DATE_UNRESOLVED

CHANGE_MONITORING_UNAVAILABLE.
```

---

# 143. Marketplace Listing Must Show Gaps

A marketplace SHALL NOT market:

```text
“South Africa regulatory coverage”
```

while hiding:

```text
SPS not modelled.
```

---

# 144. Coverage Query

Baobab SHOULD expose a machine-readable query such as conceptually:

```text
Can you support:

jurisdiction = ZA

role = IMPORT

domain = SPS

commodity = coffee

origin = UG

legal_time = T?
```

---

# 145. Response

Conceptually:

```text
coverage:
PARTIAL

assurance:
REVIEW_GATE_READY

known_gaps:
- commodity-specific permit exemption unresolved

maximum_effect_class:
E2
```

---

# 146. This Is More Valuable Than “Feature Supported”

---

# 147. Coverage Composition

When a corridor uses multiple packs:

```text
combined coverage
```

must be computed over the required modules.

---

# 148. Composition Does Not Mean Union Only

If one required module is missing:

```text
whole cross-border question
```

may remain incomplete.

---

# 149. Example

```text
UG export:
covered

AfCFTA origin:
covered

ZA tariff:
covered

ZA coffee SPS:
partial.
```

Result:

```text
full shipment clearance:
PARTIAL.
```

---

# 150. Effect Ceiling Is Question-Specific

The overall pack may contain:

```text
tariff E3

SPS E2.
```

A tariff-only calculation MAY be E3-capable.

A full shipment admissibility decision requiring SPS cannot exceed the assurance of the contributing SPS module.

---

# 151. Do Not Apply Global Lowest Module to Unrelated Questions

If:

```text
labelling module = advisory only
```

it should not necessarily reduce a:

```text
pure customs tariff query.
```

---

# 152. Coverage Graph

```text
Question
   │
   ▼
Required Regulatory Domains
   │
   ├── Classification
   ├── Origin
   ├── SPS
   ├── Tariff
   └── VAT
   │
   ▼
Pack Coverage Claims
   │
   ▼
Coverage Gaps
   │
   ▼
Assurance Composition
   │
   ▼
Maximum Decision Effect.
```

---

# 153. Pack Certification

`ADR-REG-0025` certification applies at pack/module scope.

---

# 154. Production Marketplace Pack Requires

As applicable:

```text
verified sources

rights assessment

source trust

canonical semantic validation

golden cases

BRIR conformance

OPA differential tests

historical regression

security validation

coverage manifest

known gaps

signed artifact.
```

---

# 155. Certification Does Not Mean All Laws Covered

It means:

```text
declared coverage
```

meets its declared assurance standard.

---

# 156. Marketplace Search Must Be Coverage-Aware

A useful marketplace search is:

```text
South Africa
+
coffee
+
import
+
SPS
```

not merely:

```text
search package name.
```

---

# 157. CatalogEntry

Baobab SHALL define:

# `RegulatoryMarketplaceCatalogEntry`

---

# 158. Conceptually

```text
RegulatoryMarketplaceCatalogEntry
├── pack_ref
├── publisher_ref
├── title
├── description
├── pack_type
├── current_release_ref
├── coverage_summary
├── certification_summary
├── jurisdictions[]
├── regimes[]
├── domains[]
├── license_summary
├── availability
├── update_channel
└── marketplace_status
```

---

# 159. Catalog Metadata Is Not Canonical Regulatory Knowledge

---

# 160. Marketplace Search Index Is Derived

It MAY use:

```text
PostgreSQL search

Qdrant

another search provider.
```

Search ranking has no regulatory authority.

---

# 161. Ranking Cannot Influence Rule Precedence

Critical invariant.

---

# 162. Five-Star Marketplace Pack Cannot Defeat Superior Law

---

# 163. Popularity Cannot Establish Applicability

---

# 164. Marketplace Reviews

If future marketplace UX allows user reviews, those remain:

```text
commercial/user feedback.
```

They SHALL not change:

```text
source trust

legal hierarchy

regulatory applicability.
```

---

# 165. Marketplace Admission

A publisher requires:

```text
authenticated identity

verified organisation

publisher agreement

namespace authority

rights commitments

signing identity.
```

---

# 166. Marketplace Publication Requires More

```text
pack validation

regulatory governance

test evidence

security checks

licensing validation

coverage declaration.
```

---

# 167. Marketplace Does Not Equal Open Upload

Initial architecture SHALL be:

# **curated marketplace**

not:

```text
anyone uploads anything
and tenants run it.
```

---

# 168. Recommended Rollout

```text
PHASE 1
Baobab first-party packs

        ↓

PHASE 2
Approved specialist publishers

        ↓

PHASE 3
Authority-supplied packs

        ↓

PHASE 4
Controlled broader ecosystem submissions.
```

There is no architectural requirement to ever enable unrestricted executable publication.

---

# 169. First-Party Registry Comes First

Before public marketplace UX exists, Baobab SHOULD build:

```text
internal pack catalog

artifact registry

signature verification

coverage query

activation pipeline.
```

---

# 170. Marketplace UX Is Secondary

The regulatory packaging architecture provides value before public marketplace commercialisation.

---

# 171. Tenant-Private Marketplace

Enterprises MAY eventually maintain private catalogs.

Example:

```text
Tenant T
   ├── public Baobab packs
   └── Tenant T private legal overlays.
```

---

# 172. Private Pack Cannot Be Discovered by Other Tenant

Hard invariant.

---

# 173. Private Pack Publication

Still requires:

```text
schema validation

security validation

tenant governance.
```

It MAY use a different regulatory-review policy where it represents tenant counsel rather than Baobab shared interpretation.

---

# 174. Rights

Every pack SHALL carry explicit content-rights/licensing metadata.

---

# 175. Pack Licence ≠ Underlying Source Licence

Example:

```text
pack metadata code:
Apache-2.0

underlying commercial source:
restricted.
```

Baobab cannot launder the source rights through its pack licence.

---

# 176. Marketplace Listing Must Distinguish

```text
package licence

source-content rights

customer output rights

post-termination retention rights.
```

---

# 177. Rights Determine Distribution Form

A pack may be fully distributable.

Another may contain only:

```text
derived rules

source references

source hashes.
```

---

# 178. Offline Packs

High-assurance/dedicated tenants MAY require:

```text
offline

air-gapped

restricted-network
```

installation.

---

# 179. Offline Pack Bundle

SHALL carry enough:

```text
digest

signature

provenance

attestations

dependency lock

certificate chain
```

for offline verification.

---

# 180. Mirror Support

Regulatory packs MAY be mirrored between registries.

---

# 181. Mirror ≠ Publisher

A mirror copying identical digest does not become legal/content authority.

---

# 182. Digest Preservation

Mirrors SHALL preserve artifact digests.

---

# 183. Private Mirrors

A tenant may mirror approved artifacts into its regional/private registry.

---

# 184. Residency Applies

Marketplace distribution SHALL respect `ADR-REG-0028`.

A tenant-private pack SHALL not be mirrored to an unapproved region.

---

# 185. Pack Update

A verified regulatory change may produce:

```text
new RuleVersion
```

and subsequently:

```text
new PackRelease.
```

---

# 186. Pack Release Pipeline

```text
Regulatory Change
      │
      ▼
RuleVersion Published
      │
      ▼
Affected Packs Determined
      │
      ▼
Pack Composition Updated
      │
      ▼
Golden/Regression Tests
      │
      ▼
Certification
      │
      ▼
Artifact Build
      │
      ▼
Signature
      │
      ▼
Registry
      │
      ▼
Marketplace Update Metadata.
```

---

# 187. Pack Update ≠ Automatic Tenant Activation

A tenant/runtime MAY follow:

```text
AUTOMATIC_SECURITY_UPDATE

AUTOMATIC_LOW_RISK

REVIEW_REQUIRED

PINNED
```

update policy.

Exact commercial/user policies may be refined under ADR-REG-0030.

---

# 188. Regulatory Urgency May Override Normal Cadence

Example:

```text
verified immediate prohibition.
```

Baobab may require:

```text
urgent pack release

runtime readiness warning

E2 safety hold
```

before a fully automated update is activated.

---

# 189. Still No Silent Code Push

Urgency does not remove:

```text
signature

provenance

semantic verification.
```

---

# 190. Update Channels

Potential:

```text
DRAFT

CANDIDATE

STABLE

SECURITY

EMERGENCY.
```

---

# 191. Channel ≠ Certification

A candidate channel can still carry an independently certified artifact for pre-production testing.

---

# 192. Stable ≠ Legally Immutable

Stable means:

```text
distribution channel readiness.
```

Law can change tomorrow.

---

# 193. Pack Freshness

Pack release should expose:

```text
last source verification

last successful source monitor

last legal-change review

next expected freshness check.
```

---

# 194. Pack Freshness ≠ Source Freshness

A pack may be recently rebuilt from:

```text
stale regulatory source.
```

Both timestamps matter.

---

# 195. Pack Deprecation

A pack may be deprecated because:

```text
jurisdiction model superseded

authority changed

pack merged into another

technical format obsolete.
```

---

# 196. Deprecated Does Not Mean Historically Invalid

Historical decisions may continue to depend upon it.

---

# 197. Pack Revocation

A release MAY be revoked due to:

```text
security compromise

critical semantic defect

rights violation

publisher compromise.
```

---

# 198. Revoked Pack

New activation SHALL be prohibited.

Existing runtime impact SHALL be assessed.

---

# 199. Historical Replay

The revoked pack MAY still need to remain securely available for:

```text
forensics

historical replay

audit.
```

---

# 200. Marketplace Revocation Event

Potential canonical events:

```text
pack.published

pack.deprecated

pack.suspended

pack.revoked

pack.release.available

pack.coverage.changed

pack.certification.changed.
```

---

# 201. Activation Event

Separately:

```text
pack.staged

pack.activated

pack.superseded

pack.activation-failed.
```

---

# 202. Events Do Not Replace Registry State

ADR-REG-0024 applies.

---

# 203. Control Plane Entitlement Integration

Marketplace availability SHALL not bypass:

```text
CapabilityGrant

Subscription

tenant entitlement.
```

---

# 204. Example

Catalog contains:

```text
ZA Premium Regulatory Pack.
```

Tenant without entitlement may:

```text
discover metadata
```

if marketplace policy permits.

It SHALL NOT:

```text
activate protected package.
```

---

# 205. Entitlement ≠ Regulatory Applicability

Even when tenant is entitled:

```text
ZA tariff pack
```

its rules apply only when regulatory context makes them applicable.

---

# 206. Applicability Remains Deterministic Rule Evaluation

---

# 207. Entitlement Boundary

`ADR-REG-0030` SHALL define:

```text
commercial products

subscription tiers

entitlement

metering

SLA.
```

This ADR only establishes the packaging/catalog interface required by that commercial layer.

---

# 208. Product Mapping

Conceptually:

```text
Commercial Product
       │
       ▼
Entitlement
       │
       ▼
Regulatory Profile
       │
       ▼
Pack Composition.
```

---

# 209. Product SHALL Not Name Infrastructure

A commercial offering might be:

```text
Southern Africa Cross-Border Regulatory
```

not:

```text
OPA Pack v4.
```

---

# 210. Pack Composition Resolver

Baobab SHALL implement a deterministic:

# `RegulatoryPackResolver`

---

# 211. Input

```text
requested profile

tenant entitlement

PlatformContext

legal time

required regulatory domains

supported pack catalog

compatibility rules.
```

---

# 212. Output

```text
resolved exact pack releases

digests

dependencies

coverage

known gaps

assurance

effect ceiling.
```

---

# 213. Resolver Does Not Decide Legal Applicability

It determines:

```text
available knowledge packages.
```

Rule evaluation later determines:

```text
which laws apply.
```

---

# 214. Critical Distinction

```text
Pack Resolution
≠
Regulatory Applicability Resolution.
```

---

# 215. Example

ZA Pack resolved because:

```text
tenant operates in ZA.
```

A specific:

```text
plant-health rule
```

may still not apply to roasted coffee.

---

# 216. Resolver Failures

Potential:

```text
PACK_NOT_FOUND

PACK_NOT_ENTITLED

DEPENDENCY_UNSATISFIED

PACK_INCOMPATIBLE

PACK_REVOKED

PACK_SIGNATURE_INVALID

PACK_PROVENANCE_INVALID

COVERAGE_INCOMPLETE

PACK_RESIDENCY_INCOMPATIBLE.
```

---

# 217. Marketplace Downtime

Once verified packs are activated locally, temporary marketplace outage SHOULD NOT normally disable existing deterministic regulatory execution.

---

# 218. Marketplace Is Control/Distribution Plane

It is not:

```text
transaction hot path.
```

---

# 219. Fast-Path Independence

```text
Marketplace down
      │
      ▼
existing verified RuleSet
      │
      ▼
OPA continues evaluation.
```

subject to freshness/readiness policy.

---

# 220. Marketplace Outage Cannot Freeze Forever

Freshness monitoring still detects:

```text
unable to verify updates.
```

---

# 221. Pack Compiler Independence

The runtime SHOULD not need:

```text
OCI registry

Sigstore service

marketplace search
```

for each transaction.

---

# 222. Artifact Verification Happens Before Activation

---

# 223. Coverage API

Baobab SHOULD make coverage machine-readable.

Example conceptually:

```text
POST /regulatory-coverage/resolve

{
  "origin": "UG",
  "destination": "ZA",
  "commodity": "coffee",
  "domains": [
    "CUSTOMS",
    "ORIGIN",
    "SPS"
  ],
  "legal_time": "..."
}
```

---

# 224. Example Response

```json
{
  "coverage": "COVERED_WITH_KNOWN_GAPS",
  "modules": {
    "CUSTOMS": "COVERED",
    "ORIGIN": "COVERED",
    "SPS": "PARTIAL"
  },
  "maximum_effect_class": "E2",
  "gaps": [
    "ZA commodity-specific plant import exemption unresolved"
  ]
}
```

---

# 225. Coverage API Is Valuable Before Decision API

It allows consumers to ask:

> **Can Baobab answer this question safely?**

before asking:

> **What is the answer?**

---

# 226. Marketplace UX Should Display Coverage Visually

Example:

| Domain | Coverage | Assurance |
|---|---|---|
| Classification | Covered | E3-ready |
| Customs tariff | Covered | E3-ready |
| AfCFTA origin | Covered | E2/E3 according to evidence path |
| SPS | Partial | E2 |
| Import VAT | Covered | E3-ready |
| Transit | Route-dependent | Advisory/review |

Illustrative only; actual certification must come from testing.

---

# 227. Avoid Marketing “Complete Compliance”

The catalog SHALL not use unsupported claims such as:

```text
100% compliant

all laws covered

fully legally certified.
```

---

# 228. Coverage Claims Need Provenance

Every marketplace coverage claim SHALL be derivable from:

```text
CoverageManifest

PackCertification

SourceManifest.
```

---

# 229. Automatic Catalog Generation

Marketplace metadata SHOULD be generated from canonical pack metadata rather than manually maintained marketing copy wherever possible.

---

# 230. Human Description Can Supplement

But cannot override:

```text
machine-readable coverage.
```

---

# 231. Pack Search

Queries MAY support:

```text
jurisdiction

regime

regulatory domain

commodity

HS classification

business activity

transaction stage

publisher

coverage state.
```

---

# 232. Search by Country Alone Is Insufficient

---

# 233. Search by Trade Lane

Useful:

```text
UG → ZA

coffee
```

which resolves a composition rather than requiring one monolithic corridor artifact.

---

# 234. Reuse Example — Kenya Expansion

Suppose Baobab adds Kenya.

Required new knowledge may include:

```text
KE Customs

KE Plant Health

KE tax/import requirements.
```

Existing:

```text
Coffee commodity profile

AfCFTA pack

possibly EAC regime pack
```

can be reused where legally applicable.

---

# 235. No Copying UG Rules Into KE

---

# 236. Reuse Example — Tanzania

```text
TZ Jurisdiction Pack
+
existing commodity profiles
+
relevant regime packs
```

produces new corridor compositions.

---

# 237. Rwanda

Same architecture.

---

# 238. Regional Pack

An EAC pack MAY contain:

```text
regional customs/origin semantics.
```

National implementation still remains in jurisdiction packs where necessary.

---

# 239. External Customer

A future Baobab customer with multiple subsidiaries can consume the same packs under its own:

```text
Tenant

Organisation

LegalEntity

MarketParticipation
```

context.

Packs do not belong to Nabhold subsidiaries.

---

# 240. Pack Portability Is Core Commercial Leverage

One verified:

```text
ZA import tariff module
```

may serve:

```text
ZuriBeans

Thamani

external B2B customer

future tenants
```

while tenant-private facts remain isolated.

---

# 241. This Creates Scale

Shared regulatory knowledge cost is amortised across customers without sharing their private transactions.

---

# 242. Marketplace Economic Boundary

The reusable object is:

```text
verified regulatory knowledge coverage.
```

Not:

```text
customer data.
```

---

# 243. Regulatory Marketplace Can Support Specialist Ecosystem

Potential publishers may eventually include:

```text
legal specialists

customs specialists

tax specialists

SPS specialists

industry associations

official authorities

commercial data providers.
```

---

# 244. But Baobab Remains the Execution Gatekeeper

No publisher can directly assign:

```text
E4
```

to its own pack.

---

# 245. Certification Authority

Baobab governance determines:

```text
what effect class
Baobab runtime may use.
```

---

# 246. Publisher May Supply Evidence

They MAY provide:

```text
test corpus

legal memorandum

source analysis

provenance.
```

Certification still applies.

---

# 247. Marketplace Conflict

Two publishers may offer competing interpretations.

Baobab SHALL NOT decide correctness based on:

```text
price

popularity

download count

publisher rating.
```

---

# 248. Competing Interpretation Resolution

Use:

```text
source authority

legal hierarchy

interpretive status

governance

evidence

verification.
```

---

# 249. Multiple Packs May Coexist

Example:

```text
Baobab standard interpretation

Tenant counsel overlay.
```

Regulations semantics determine which is applicable in that tenant context.

---

# 250. Tenant Counsel Overlay

May be scoped:

```text
tenant only

specific LegalEntity

specific transaction family

specific time interval.
```

---

# 251. No Marketplace Promotion by Accident

Tenant counsel pack SHALL not become shared simply because:

```text
it has many users.
```

---

# 252. Supply-Chain Attestation Graph

```text
Source Repository
      │
      ▼
Regulatory Sources
      │
      ▼
Canonical RuleVersions
      │
      ▼
Pack Builder
      │
      ├── SLSA provenance
      ├── Regulatory attestation
      ├── Golden test evidence
      └── Coverage manifest
      │
      ▼
Content-Addressed Pack
      │
      ▼
Signature
      │
      ▼
OCI Registry
      │
      ▼
Marketplace
      │
      ▼
Pack Resolver
      │
      ▼
RuleSet Compiler
      │
      ▼
Signed OPA Bundle
```

---

# 253. OCI Referrers

OCI's referrers mechanism can associate artifacts such as:

```text
signatures

provenance

test evidence

SBOMs
```

with a subject digest without modifying the original artifact.

Baobab SHOULD exploit this where supported.

---

# 254. Example Artifact Relationship

```text
Regulatory Pack Digest
      │
      ├── Signature
      ├── SLSA Provenance
      ├── Regulatory Attestation
      ├── Test Evidence
      └── Software SBOM
```

---

# 255. Referrer Is Not Canonical Relationship

The canonical domain still records the corresponding provenance.

OCI relationships are distribution metadata.

---

# 256. Marketplace Database

Marketplace catalog state MAY reside in Regulations or a future catalog service.

However:

```text
marketplace catalog
```

SHALL NOT become canonical legal knowledge storage.

---

# 257. Initial Implementation

Avoid creating a separate marketplace microservice prematurely.

A Regulations module can initially own:

```text
pack registry

publisher registry

coverage registry

catalog API.
```

---

# 258. Extract Later If Necessary

Independent marketplace service is justified only when:

```text
scale

publisher ecosystem

commercial complexity

security separation
```

warrants it.

---

# 259. No Premature Marketplace Platform

The first milestone is:

```text
correct pack architecture.
```

Not:

```text
app store UI.
```

---

# 260. Initial Repository Layout

Conceptually:

```text
baobab-regulations/
│
├── packs/
│   ├── manifests/
│   ├── schemas/
│   ├── builder/
│   ├── resolver/
│   ├── verifier/
│   └── registry/
│
├── coverage/
│   ├── models/
│   ├── resolver/
│   └── api/
│
├── marketplace/
│   ├── publishers/
│   ├── submissions/
│   └── catalog/
│
└── runtime/
    └── composition/
```

Exact code layout remains implementation-specific.

---

# 261. Canonical Domain Objects

At minimum:

```text
RegulatoryModuleDefinition

RegulatoryPack

RegulatoryPackRelease

RegulatoryPackManifest

RegulatoryPackDependency

RegulatoryPackLock

RegulatoryCoverageManifest

CoverageClaim

CoverageGap

RegulatoryPackAttestation

RegulatoryPublisherProfile

RegulatoryMarketplaceSubmission

RegulatoryMarketplaceCatalogEntry

RegulatoryPackActivation.
```

---

# 262. PackRelease

Conceptually:

```text
RegulatoryPackRelease
├── pack_ref
├── release_version
├── artifact_digest
├── created_at
├── publisher_ref
├── source_manifest_ref
├── coverage_manifest_ref
├── dependency_manifest_ref
├── rights_manifest_ref
├── certification_ref
├── signature_refs[]
├── attestation_refs[]
├── status
└── provenance
```

---

# 263. PackActivation

Conceptually:

```text
RegulatoryPackActivation
├── tenant_scope?
├── profile_ref
├── pack_release_ref
├── resolved_digest
├── activation_status
├── activation_reason
├── ruleset_ref?
├── activated_at?
├── superseded_at?
└── provenance
```

---

# 264. Pack Activation Can Be Global or Tenant-Scoped

Shared public law may feed:

```text
global/shared RuleSets.
```

Private overlays remain:

```text
tenant-scoped.
```

---

# 265. Activation SHALL Respect Residency

Private pack retrieval/import SHALL satisfy `ADR-REG-0028`.

---

# 266. Compatibility Matrix

Pack manifests SHOULD declare compatibility with:

```text
Regulations contract version

BRIR schema

compiler capability

required module semantics

OPA target requirements

Shared canonical contracts.
```

---

# 267. Compatibility Is Checked Before Activation

---

# 268. Unknown Manifest Version

Result:

```text
PACK_MANIFEST_UNSUPPORTED.
```

Do not best-effort parse consequential unknown semantics.

---

# 269. Unknown Optional Metadata

May be preserved/ignored if contract explicitly permits forward-compatible extension.

---

# 270. Unknown Regulatory Semantics

Fail closed.

---

# 271. Dependency Resolution Evidence

Every activation SHALL retain:

```text
why each pack was selected

exact version

digest

dependency path.
```

---

# 272. Explainable Composition

User should be able to ask:

> Why is this AfCFTA rule present?

Answer:

```text
UG→ZA profile
    requires AfCFTA origin module
        resolved to
        pack X digest Y.
```

---

# 273. Explainability Continues to Legal Source

```text
Pack
  ↓
RuleVersion
  ↓
Interpretation
  ↓
Provision
  ↓
Source.
```

---

# 274. Package Abstraction Must Never Break Legal Explainability

Hard invariant.

---

# 275. Historical Decision Records

A RegulatoryDecision SHOULD record:

```text
RuleSet fingerprint
+
RegulatoryPackLock reference.
```

This enables reconstruction of packaging composition as well as regulatory semantics.

---

# 276. Pack Deletion

Published packs used in historical consequential decisions SHALL normally be:

```text
retired/archived
```

rather than physically destroyed while retention requires replay.

---

# 277. Mutable Marketplace Metadata

Descriptions, screenshots or pricing MAY change.

The signed pack digest SHALL not.

---

# 278. Artifact Immutability

Attempting to publish different bytes under the same immutable release identity SHALL be rejected.

---

# 279. Correct Fix

Publish:

```text
new release.
```

---

# 280. Yanked Release

A broken release can be:

```text
REVOKED
```

while preserving historical evidence.

---

# 281. Marketplace Security Incident

Baobab SHALL define incident types such as:

```text
PACK_TAMPERING

PUBLISHER_KEY_COMPROMISE

MALICIOUS_PACK

DEPENDENCY_CONFUSION

NAMESPACE_TAKEOVER

ROLLBACK_ATTEMPT

FREEZE_DETECTED

SIGNATURE_FAILURE

PROVENANCE_FAILURE

RIGHTS_VIOLATION.
```

---

# 282. Incident Response

```text
Detect
   ↓
Suspend Release
   ↓
Block New Activation
   ↓
Identify Active Tenants
   ↓
Determine RuleSet Impact
   ↓
Revalidate / Replace
   ↓
Reassess Decisions if needed
   ↓
Audit
   ↓
Regression Test.
```

---

# 283. Malicious Pack Cannot Execute Installer

Because standard packs contain no arbitrary installation code.

This substantially reduces blast radius.

---

# 284. Compromised Pack With Bad Rules

This remains possible.

Therefore:

```text
signature
```

is only one control among:

```text
source review

semantic review

tests

certification.
```

---

# 285. Testing

`ADR-REG-0025` SHALL test pack infrastructure itself.

---

# 286. Pack Builder Tests

```text
deterministic artifact build

manifest completeness

digest correctness

dependency completeness

rights manifest

coverage manifest.
```

---

# 287. Reproducible Builds

Where practical, identical canonical inputs and tooling SHOULD produce equivalent pack content.

---

# 288. Signature Tests

```text
valid signature accepted

tampered artifact rejected

wrong signer rejected

revoked signer rejected

expired credential handled.
```

---

# 289. Dependency Tests

```text
exact digest resolution

missing dependency

incompatible dependency

circular dependency

conflicting version requirement.
```

---

# 290. Anti-Rollback Tests

Attempt to activate older release over newer current release without controlled rollback authority.

Expected:

```text
rejected.
```

---

# 291. Freeze Tests

Marketplace timestamp/update metadata intentionally stale.

Expected:

```text
MARKETPLACE_METADATA_STALE.
```

---

# 292. Coverage Tests

Pack claiming:

```text
SPS = COVERED
```

without required certified module evidence SHALL fail publication validation.

---

# 293. Known-Gap Tests

Coverage gap SHALL remain visible after pack resolution.

---

# 294. Marketplace Isolation Tests

Tenant-private pack SHALL not appear in another tenant's:

```text
catalog

search

resolver

artifact fetch.
```

---

# 295. OCI Registry Tests

Where OCI distribution is used:

```text
push artifact

pull by digest

signature referrer retrieval

attestation referrer retrieval

mirror digest preservation.
```

---

# 296. Runtime Independence Test

Disconnect marketplace after activation.

Existing certified regulatory decisions SHALL continue to execute against local verified RuleSet.

---

# 297. Historical Replay Test

Old decision references PackLock P1.

Current marketplace points to P5.

Historical replay SHALL still resolve:

```text
P1
```

from archive.

---

# 298. Publisher Revocation Test

Publisher revoked today.

Historical valid pack remains reconstructable.

New submission blocked.

---

# 299. Third-Party Candidate Rego Test

Pack includes arbitrary Rego.

Baobab activation path SHALL not run it automatically.

---

# 300. Initial Uganda → South Africa Pack Composition

The `ADR-REG-0027` pilot SHOULD evolve conceptually into:

```text
CORE MODULES
────────────────────────
customs-classification

customs-valuation

trade-documents


UGANDA PACKS
────────────────────────
ug-customs-export

ug-coffee-export

ug-plant-health


REGIONAL PACKS
────────────────────────
afcfta-origin

afcfta-preference


SOUTH AFRICA PACKS
────────────────────────
za-customs-import

za-tariff

za-import-vat

za-plant-health


COMMODITY PROFILES
────────────────────────
coffee

vanilla


COMPOSITION
────────────────────────
ug-za-coffee

ug-za-vanilla.
```

---

# 301. Example Coffee Composition

```text
UG-ZA-COFFEE
      │
      ├── CORE/CUSTOMS-CLASSIFICATION
      ├── UG/COFFEE-EXPORT
      ├── UG/PLANT-HEALTH
      ├── AFCFTA/ORIGIN
      ├── ZA/CUSTOMS-IMPORT
      ├── ZA/TARIFF
      ├── ZA/IMPORT-VAT
      ├── ZA/PLANT-HEALTH
      └── COMMODITY/COFFEE.
```

---

# 302. Kenya Expansion

Future:

```text
UG → KE Coffee
```

may reuse:

```text
UG/COFFEE-EXPORT

UG/PLANT-HEALTH

COMMODITY/COFFEE

regional EAC modules where applicable
```

while adding:

```text
KE/CUSTOMS-IMPORT

KE/PLANT-HEALTH

KE/TAX.
```

---

# 303. South Africa Reuse

A future:

```text
KE → ZA Coffee
```

can reuse:

```text
ZA/CUSTOMS-IMPORT

ZA/TARIFF

ZA/IMPORT-VAT

ZA/PLANT-HEALTH.
```

---

# 304. This Is the Main Architectural Payoff

Regulatory knowledge becomes:

```text
composable

versioned

testable

reusable

auditable

commercialisable.
```

---

# 305. Coverage Graph Example

```text
                 UG→ZA Coffee
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
        Export      Regional      Import
           │           │           │
           ▼           ▼           ▼
       UG Packs      AfCFTA      ZA Packs
           │           │           │
           └───────────┼───────────┘
                       ▼
               Coverage Resolver
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          Covered              Gaps
             │                   │
             └─────────┬─────────┘
                       ▼
              Assurance Ceiling
```

---

# 306. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-PACK-I01` | A regulatory pack SHALL NOT itself constitute legal authority |
| `REG-PACK-I02` | Pack signature SHALL establish integrity/publisher identity, not legal correctness |
| `REG-PACK-I03` | Pack release version SHALL remain distinct from legal valid time |
| `REG-PACK-I04` | Technical SemVer SHALL NOT encode legal importance |
| `REG-PACK-I05` | Production pack activation SHALL use immutable content identity |
| `REG-PACK-I06` | Mutable tags such as `latest` SHALL NOT be the sole production identity |
| `REG-PACK-I07` | OCI SHALL remain a distribution mechanism rather than canonical regulatory semantics |
| `REG-PACK-I08` | Pack supply-chain provenance SHALL remain distinct from regulatory verification |
| `REG-PACK-I09` | Publisher identity SHALL remain distinct from source authority |
| `REG-PACK-I10` | Publisher reputation SHALL remain distinct from pack certification |
| `REG-PACK-I11` | Third-party pack submission SHALL enter quarantine before canonical promotion |
| `REG-PACK-I12` | Standard regulatory packs SHALL NOT execute arbitrary installation code |
| `REG-PACK-I13` | Source adapters requiring code SHALL use a separate governed extension boundary |
| `REG-PACK-I14` | Marketplace-provided Rego SHALL NOT directly become E3/E4 executable policy |
| `REG-PACK-I15` | BRIR/canonical RuleVersions SHALL remain the provider-neutral executable semantic layer |
| `REG-PACK-I16` | OPA bundles SHALL remain runtime packages, not marketplace packages |
| `REG-PACK-I17` | Pack dependencies SHALL resolve deterministically |
| `REG-PACK-I18` | Production dependencies SHALL be pinned to exact releases/digests |
| `REG-PACK-I19` | Technical dependency conflicts SHALL remain distinct from legal-rule conflicts |
| `REG-PACK-I20` | Pack namespace publishing SHALL require explicit publisher authority |
| `REG-PACK-I21` | Publisher revocation SHALL NOT erase historical regulatory decisions |
| `REG-PACK-I22` | Pack catalog state SHALL remain distinct from pack activation state |
| `REG-PACK-I23` | Coverage SHALL be multidimensional rather than one generic percentage |
| `REG-PACK-I24` | Coverage SHALL remain distinct from assurance/certification |
| `REG-PACK-I25` | Known gaps SHALL be explicit and machine-readable |
| `REG-PACK-I26` | Pack certification SHALL apply to declared scope, not imply all-law coverage |
| `REG-PACK-I27` | Marketplace ranking SHALL never affect legal hierarchy or rule precedence |
| `REG-PACK-I28` | Marketplace entitlement SHALL remain distinct from legal applicability |
| `REG-PACK-I29` | Pack resolution SHALL remain distinct from rule applicability resolution |
| `REG-PACK-I30` | Tenant-private packs SHALL remain isolated under ADR-REG-0028 |
| `REG-PACK-I31` | Pack rights SHALL not launder underlying source-content restrictions |
| `REG-PACK-I32` | Offline/mirrored packs SHALL remain cryptographically verifiable |
| `REG-PACK-I33` | Mirrors SHALL preserve immutable content identity |
| `REG-PACK-I34` | Production update channels SHALL provide anti-rollback/freshness protection |
| `REG-PACK-I35` | Explicit historical pinning SHALL remain distinct from unauthorised rollback |
| `REG-PACK-I36` | Pack activation SHALL preserve exact dependency and provenance history |
| `REG-PACK-I37` | Pack deprecation SHALL NOT invalidate historical decisions automatically |
| `REG-PACK-I38` | Marketplace availability SHALL remain outside the transaction hot path |
| `REG-PACK-I39` | An active local RuleSet SHOULD continue operating during temporary marketplace unavailability |
| `REG-PACK-I40` | Commercial productisation SHALL consume this architecture without redefining regulatory semantics |

---

# 307. Rejected Alternatives

The following approaches are rejected:

```text
one giant Africa regulatory pack

one giant pack per corridor

one package per tenant

copy the same South African law into every corridor

marketplace pack = OPA bundle

signed pack = legally correct

publisher popularity = legal authority

community upload = production rule

third-party arbitrary Rego auto-execution

post-install scripts

floating `latest` dependency in production

mutable release bytes

one coverage percentage

“country supported” without domain scope

hidden coverage gaps

pack entitlement = legal applicability

SemVer major = major legal change

OCI registry = source of legal truth

public registry = canonical regulatory database

rollback old pack automatically when new one fails

delete superseded packs used by historical decisions

rebuild historical decision using current packs

tenant counsel pack automatically shared

source licence ignored because pack is transformed

marketplace outage disables OPA transaction evaluation

pack search ranking determines precedence

pack publisher sets its own enforcement ceiling.
```

---

# 308. Minimum Implementation Proof

Before `ADR-REG-0029` is considered implemented, Baobab SHOULD demonstrate:

```text
1. RegulatoryModuleDefinition.

2. JurisdictionPack.

3. RegulatoryRegimePack.

4. CommodityRegulatoryProfile.

5. CrossBorderCorridorProfile.

6. RegulatoryPackManifest.

7. stable logical pack ID.

8. immutable PackRelease.

9. release version separate from legal time.

10. artifact digest.

11. source manifest.

12. rules manifest.

13. coverage manifest.

14. dependency manifest.

15. rights manifest.

16. RegulatoryPackageBillOfMaterials.

17. test-evidence reference.

18. RegulatoryPackAttestation.

19. build provenance.

20. canonical pack schema.

21. manifest schema version.

22. compatibility metadata.

23. BRIR compatibility check.

24. Regulations API compatibility check.

25. pack builder.

26. deterministic builder test.

27. OCI export.

28. OCI import.

29. custom OCI artifact type.

30. pull by digest.

31. OCI referrer for signature.

32. OCI referrer for provenance.

33. OCI referrer for regulatory attestation.

34. OCI referrer for test evidence.

35. registry mirror.

36. mirrored digest verification.

37. signature generation.

38. signature verification.

39. tamper rejection.

40. signer identity verification.

41. signing-key rotation.

42. signing-key revocation.

43. private-pack signing.

44. offline verification.

45. pack quarantine.

46. package decompression limits.

47. manifest validation.

48. path traversal protection.

49. no executable installer.

50. no arbitrary post-install hook.

51. publisher registry.

52. publisher identity.

53. publisher organisation.

54. namespace allocation.

55. namespace conflict rejection.

56. publisher signing identity.

57. publisher suspension.

58. publisher revocation.

59. publisher types.

60. publisher type does not influence legal authority automatically.

61. MarketplaceSubmission.

62. submission quarantine.

63. rights validation.

64. source-trust validation.

65. regulatory semantic validation.

66. golden-suite execution.

67. BRIR validation.

68. OPA differential test.

69. certification gate.

70. marketplace publication.

71. catalog entry.

72. catalog search by jurisdiction.

73. catalog search by domain.

74. catalog search by commodity.

75. catalog search by trade lane/profile.

76. catalog coverage summary.

77. catalog known-gap display.

78. RegulatoryCoverageManifest.

79. CoverageClaim.

80. CoverageGap.

81. jurisdiction coverage.

82. jurisdiction-role coverage.

83. regime coverage.

84. regulatory-domain coverage.

85. activity coverage.

86. actor-role coverage.

87. commodity coverage.

88. HS-range coverage.

89. transaction-stage coverage.

90. legal-time coverage.

91. source coverage.

92. interpretation coverage.

93. rule coverage.

94. execution coverage.

95. test coverage.

96. change-monitoring coverage.

97. UNKNOWN coverage state.

98. NOT_COVERED state.

99. PARTIAL state.

100. COVERED state.

101. COVERED_WITH_KNOWN_GAPS state.

102. coverage query API.

103. effect-ceiling calculation by contributing modules.

104. no universal coverage percentage.

105. RegulatoryPackDependency.

106. REQUIRED dependency.

107. OPTIONAL dependency.

108. CONDITIONAL dependency.

109. SUPERSEDES relation.

110. deterministic dependency resolver.

111. dependency cycle rejection.

112. incompatible dependency rejection.

113. missing dependency rejection.

114. digest-pinned dependency.

115. RegulatoryPackLock.

116. lock reproducibility.

117. RuleSet fingerprint link.

118. historical PackLock persistence.

119. package anti-rollback state.

120. explicit controlled rollback.

121. stale marketplace metadata detection.

122. timestamp/freshness metadata.

123. publisher delegation.

124. delegation revocation.

125. PackRelease lifecycle.

126. PackActivation lifecycle.

127. published ≠ active test.

128. entitled ≠ active test.

129. active ≠ legally applicable test.

130. PackResolver.

131. resolution by profile.

132. resolution by tenant entitlement.

133. resolution by required domains.

134. resolution by compatibility.

135. resolution by legal-time support.

136. PACK_NOT_FOUND.

137. PACK_NOT_ENTITLED.

138. PACK_INCOMPATIBLE.

139. PACK_REVOKED.

140. PACK_SIGNATURE_INVALID.

141. PACK_PROVENANCE_INVALID.

142. COVERAGE_INCOMPLETE.

143. PACK_RESIDENCY_INCOMPATIBLE.

144. shared pack activation.

145. tenant-private pack activation.

146. private-pack isolation.

147. tenant pack invisible to other tenants.

148. source-rights safe packaging.

149. restricted source referenced rather than redistributed.

150. licence metadata.

151. output-rights metadata.

152. offline export.

153. offline import.

154. marketplace unavailable runtime test.

155. existing OPA runtime continues.

156. marketplace freshness degradation.

157. new-pack update event.

158. pack deprecated event.

159. pack revoked event.

160. pack activated event.

161. pack superseded event.

162. third-party Rego not executed automatically.

163. trusted compiler rebuild.

164. signed OPA execution package generated.

165. pack → RuleSet provenance.

166. RuleSet → pack lock provenance.

167. decision → RuleSet fingerprint.

168. decision → PackLock reference.

169. Uganda customs-export pack.

170. Uganda coffee-export pack.

171. Uganda plant-health pack.

172. AfCFTA origin pack.

173. AfCFTA preference pack.

174. South Africa customs-import pack.

175. South Africa tariff pack.

176. South Africa import-VAT pack.

177. South Africa plant-health pack.

178. coffee commodity profile.

179. vanilla commodity profile.

180. UG→ZA coffee corridor profile.

181. UG→ZA vanilla corridor profile.

182. composition of shared modules.

183. incomplete SPS coverage propagated to corridor.

184. full tariff coverage retained independently.

185. per-question effect ceiling.

186. Kenya extension proof.

187. reuse South Africa pack in KE→ZA corridor.

188. no copied ZA law between corridors.

189. tenant overlay composition.

190. historical replay with superseded pack.

191. revoked-publisher historical replay.

192. malicious-pack incident.

193. signing-key compromise incident.

194. rollback-attempt detection.

195. dependency-confusion test.

196. namespace-takeover test.

197. registry-tamper test.

198. marketplace audit events.

199. pack security audit trail.

200. end-to-end source → RuleVersion → Pack → Registry → Entitlement → Composition → RuleSet → signed OPA bundle → decision.
```

---

# 309. Uganda → South Africa Reference Composition

The initial implementation SHOULD produce something conceptually equivalent to:

```text
regulatory-profile:
    ug-za-coffee

composition:

    core:
        - customs-classification
        - customs-valuation
        - trade-documentation

    origin:
        - ug-coffee-export
        - ug-plant-health

    regime:
        - afcfta-origin
        - afcfta-preference

    destination:
        - za-customs-import
        - za-tariff
        - za-import-vat
        - za-plant-health

    commodity:
        - coffee
```

---

# 310. Coverage Result Example

```text
UG → ZA Coffee

Classification
    COVERED
    E3-ready

Uganda Export
    COVERED
    E3-ready

AfCFTA Origin
    COVERED
    E2/E3 depending evidence

South African Tariff
    COVERED
    E3-ready

South African Import VAT
    COVERED
    E3-ready

South African Commodity-Specific SPS
    PARTIAL
    E2

Transit
    ROUTE_DEPENDENT
```

This is much more meaningful than:

```text
South Africa supported = true.
```

---

# 311. Future Kenya Example

```text
UG → KE Coffee
```

could resolve:

```text
UG Coffee Export

UG Plant Health

EAC rules where applicable

KE Customs Import

KE Plant Health

Coffee Commodity Profile.
```

No Ugandan or South African rule needs to be copied.

---

# 312. Future External Publisher Example

Suppose an approved East African plant-health specialist publishes:

```text
publisher:
REGULATORY_SPECIALIST

pack:
KE-PLANT-HEALTH
```

The marketplace flow remains:

```text
Signed Submission
      │
      ▼
Quarantine
      │
      ▼
Source Verification
      │
      ▼
Rights Verification
      │
      ▼
Regulatory Review
      │
      ▼
Golden Tests
      │
      ▼
Certification
      │
      ▼
Marketplace Publication.
```

Their publisher status does not allow:

```text
direct OPA installation.
```

---

# 313. Research Foundation

The OCI specifications provide a strong neutral transport mechanism for Baobab packs. OCI manifests are content-addressed and support typed non-container artifacts, while OCI Distribution 1.1 provides a referrers mechanism for associating other artifacts with an immutable subject digest. This allows Baobab to distribute the pack itself separately from its signatures, provenance, test evidence and related attestations while retaining cryptographically stable relationships.

Sigstore provides artifact signing and verification with traditional keys, KMS-backed keys and identity-bound keyless workflows; its verification bundles can contain certificates and transparency-log evidence that allow signing events to be independently verified. Baobab can use these capabilities for regulatory artifact integrity while remaining conscious that public transparency metadata may be inappropriate for tenant-private packages.

SLSA build provenance and the underlying in-toto Attestation Framework provide machine-readable mechanisms for proving how an artifact was produced. Baobab adopts their supply-chain concepts for pack builds but deliberately adds a separate RegulatoryPackAttestation because software-build provenance cannot establish source authority, legal interpretation or regulatory certification.

The Update Framework directly addresses repository attacks highly relevant to a regulatory marketplace, including rollback, freeze, mix-and-match and repository compromise. Its separation of root, target, snapshot and timestamp metadata—and its support for delegated trust and revocation—provides a strong reference architecture for securely distributing regulatory updates where merely verifying a package signature is insufficient to establish that the package is the current authorised release.

OPA's own bundle architecture remains useful downstream from the marketplace. OPA bundles support revisions, dynamically updated policy/data and signature verification, allowing Baobab's already verified pack composition to be compiled into an independently signed execution package for deterministic PDP runtimes. The marketplace pack and runtime OPA bundle therefore deliberately remain separate artifacts with different responsibilities.

The existing Baobab platform architecture likewise requires this separation. Baobab's foundational model standardises shared contracts while leaving engine implementations independent, and the current Control Plane desired-state architecture deliberately expresses client needs, profiles, isolation and residency without hard-coding providers or EngineInstances. Regulatory packs therefore enter Baobab as provider-neutral knowledge/profile constructs rather than infrastructure choices. 

---

# 314. Final Decision

Baobab Regulations SHALL implement **jurisdiction packs, regulatory modules, coverage manifests and a curated regulatory marketplace as the distribution architecture for reusable regulatory knowledge**.

The final architecture is:

```text
                    REGULATORY SOURCES
                           │
                           ▼
                   Verified Knowledge
                           │
                           ▼
                 Regulatory Modules
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    Jurisdiction       Regime          Commodity
       Packs            Packs           Profiles
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Coverage Manifest
                           │
                           ▼
                     Golden Tests
                           │
                           ▼
                    Certification
                           │
                           ▼
                   Content-Addressed
                    Regulatory Pack
                           │
                   ┌───────┼────────┐
                   ▼       ▼        ▼
               Signature Provenance Attestation
                   │       │        │
                   └───────┼────────┘
                           ▼
                      OCI Registry
                           │
                           ▼
                  Curated Marketplace
                           │
                           ▼
                 Tenant Entitlement
                           │
                           ▼
                    Pack Resolver
                           │
                           ▼
                  RegulatoryPackLock
                           │
                           ▼
                    Effective RuleSet
                           │
                           ▼
                    Trusted Compiler
                           │
                           ▼
                   Signed OPA Bundle
                           │
                           ▼
                 Regulatory Execution
```

The modularity principle is:

> **A corridor is composed from reusable jurisdiction, regime, domain and commodity knowledge rather than implemented as a bespoke body of duplicated rules.**

The authority principle is:

> **A pack distributes regulatory knowledge; it does not manufacture the authority of the sources it represents.**

The publisher principle is:

> **The right to publish into Baobab's marketplace is a platform permission, not a declaration that the publisher's interpretation is legally authoritative.**

The packaging principle is:

> **Every production pack is immutable, content-addressed, signed, provenance-bearing and independently identifiable from the legal versions it contains.**

The transport principle is:

> **OCI may transport regulatory packs, signatures and attestations, but OCI metadata never defines the law.**

The provenance principle is:

> **Technical build provenance and regulatory assurance are separate attestations and must remain separately inspectable.**

The marketplace-security principle is:

> **A marketplace submission enters quarantine and governance; it never acquires direct write access to canonical regulation or execution runtimes.**

The executable-content principle is:

> **Normal regulatory packs are declarative. Arbitrary installation code and unreviewed third-party policy code SHALL NOT execute merely because a pack was downloaded.**

The runtime principle is:

> **Marketplace packs are converted into canonical RuleVersions and BRIR, then compiled by trusted Baobab tooling into separately signed OPA execution packages.**

The dependency principle is:

> **Every production composition resolves to exact immutable pack digests recorded in a RegulatoryPackLock.**

The update principle is:

> **Pack distribution protects not only against tampering but also against unintended rollback, stale/frozen metadata and dependency substitution.**

The coverage principle is:

> **Coverage is multidimensional and explicit; Baobab SHALL state which jurisdiction, domain, commodity, activity, legal period and decision capability it can actually support.**

The uncertainty principle is:

> **A missing pack or known coverage gap produces explicit partial/unknown coverage rather than being hidden behind a generic “country supported” claim.**

The assurance principle is:

> **Coverage and certification are independent: Baobab may possess broad information but only limited enforcement assurance, or narrow information with high assurance.**

The entitlement principle is:

> **A tenant's ability to consume a pack is a Control Plane/commercial entitlement question; whether a rule applies remains a Regulations legal-context question.**

The historical principle is:

> **Superseded or revoked packs remain reconstructable for historical decisions when audit and replay require them.**

The availability principle is:

> **The marketplace belongs to the regulatory distribution/control plane, not the transaction hot path; existing verified RuleSets remain executable during temporary marketplace outages.**

The ecosystem principle is:

> **External legal, customs, tax and SPS specialists may contribute to Baobab without being allowed to bypass Baobab's source verification, rights, testing, certification and execution boundaries.**

The scale principle is:

> **One verified South African customs pack can serve ZuriBeans, Thamani and future external customers without sharing any of their private trade activity.**

And the strategic principle is:

> **Baobab's regulatory marketplace should not become an app store for arbitrary policy code. It should become a governed exchange for signed, source-backed, coverage-explicit and test-certified regulatory knowledge that can be composed safely into reproducible regulatory decisions across jurisdictions, industries and customers.**

That is the architecture established by **`ADR-REG-0029`**.

---

## Decision Summary

```text
ADR-REG-0029
─────────────────────────────────────

CORE UNIT

RegulatoryModule


PACK TYPES

JurisdictionPack

RegulatoryRegimePack

CommodityProfile

CorridorProfile


PACK

≠ law

≠ legal authority

≠ entitlement

≠ activation

≠ OPA bundle


COVERAGE

Jurisdiction

Role

Regime

Domain

Activity

Commodity

HS scope

Transaction stage

Legal time


COVERAGE

≠ assurance


DISTRIBUTION

Content-addressed

Signed

Provenance-bearing


OCI

Transport layer


SIGSTORE

Artifact integrity /
publisher identity


SLSA / IN-TOTO

Build provenance


REGULATORY ATTESTATION

Source/review/test/
effect assurance


TUF-STYLE METADATA

Anti-rollback

Anti-freeze

Delegation

Revocation


MARKETPLACE

Curated

Governed

Quarantined submissions


PUBLISHER

≠ authority


THIRD-PARTY REGO

Never auto-execute


EXECUTION

Pack
↓
RuleVersion
↓
BRIR
↓
Trusted Compiler
↓
Signed OPA Bundle


DEPENDENCIES

Exact digest

Deterministic

Locked


HISTORY

PackLock

RuleSet fingerprint

Immutable releases


UG → ZA

UG packs

+

AfCFTA packs

+

ZA packs

+

Coffee/Vanilla profiles


EXPANSION

Add Kenya

Add Tanzania

Add Rwanda

Reuse existing modules


COMMERCIALISATION

Defined next
in ADR-REG-0030.


STRATEGIC RESULT

Regulatory knowledge
becomes

composable

portable

testable

signed

reusable

commercialisable

without allowing
a marketplace publisher
to manufacture law.
```
# ADR-REG-0011 — Authoritative Source Registry and Multidimensional Source Trust Model

**Status:** Proposed — Normative Foundational Architecture  
**Decision ID:** `ADR-REG-0011`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-09-28  
**Decision Type:** Source Authority / Trust / Authenticity / Verification / Registry Architecture  
**Strategic Classification:** Core Regulatory Trust Infrastructure / Platform Differentiator

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
- `ADR-REG-0010 — Regulatory Knowledge Graph, Relationship, Provenance and Traversal Model`

**Relevant Baobab Architecture:**

- `ADR-BCP-023 — Organisation Evidence, Verification, Trust and Compliance Record Model`
- `ADR-PULSE-006 — Provenance, Lineage and Evidence Graph Architecture`
- `ADR-PULSE-009 — Data Quality, Evidence Reliability and Intelligence Confidence Architecture`
- `ADR-SHARED-012 — Topology Identifiers and External System Registry`
- `ADR-SHARED-013 — External References and Canonical Mapping Administration`

**Primary Principle:**

> **A regulatory source SHALL be trusted only for a defined purpose, scope and time, based on explicit evidence. Baobab SHALL NOT maintain a universal source trust score.**

---

# 1. Executive Decision

Baobab Regulations SHALL implement an authoritative, governed **Regulatory Source Registry**.

The Registry SHALL describe:

```text
WHO
published or supplied regulatory information

WHAT
regulatory source it represents

UNDER WHOSE AUTHORITY
the material exists

WHERE
the material was acquired

WHICH EDITION / VERSION
was obtained

WHEN
it was published, effective and retrieved

WHETHER
the artefact is authentic and intact

WHAT LEGAL STATUS
the source material has

WHAT COVERAGE
the source provides

HOW COMPLETE
the representation is

WHAT TRANSFORMATIONS
have occurred

WHAT RIGHTS
Baobab has to use it

FOR WHAT PURPOSE
the source may safely be relied upon
```

The source model SHALL be:

```text
multidimensional
+
purpose-specific
+
temporal
+
provenance-backed
+
provider-neutral
+
jurisdiction-aware
```

and SHALL explicitly reject:

```text
source.trust_score = 94
```

as the canonical trust architecture.

---

# 2. Fundamental Trust Doctrine

Baobab SHALL distinguish:

```text
SOURCE IDENTITY
    ≠
SOURCE AUTHORITY
    ≠
OFFICIAL STATUS
    ≠
AUTHENTICITY
    ≠
LEGAL FORCE
    ≠
CURRENTNESS
    ≠
COMPLETENESS
    ≠
ACCURACY
    ≠
PROVENANCE QUALITY
    ≠
INTERPRETIVE RELIABILITY
    ≠
LICENSING RIGHTS
    ≠
TECHNICAL AVAILABILITY
    ≠
FITNESS FOR PURPOSE
```

A source can be excellent on one dimension and weak on another.

---

# 3. Why a Single Trust Score Is Rejected

Consider four sources:

```text
A. Official Gazette

B. Official consolidated legislation portal

C. Commercial regulatory provider

D. Specialist legal counsel opinion
```

A single score such as:

```text
A = 95
B = 92
C = 87
D = 83
```

cannot answer:

```text
Which legally promulgated the regulation?

Which is easiest to read?

Which is most current?

Which provides machine-readable obligations?

Which is legally binding?

Which interpretation should this tenant use?

Which may Baobab redistribute?

Which is complete for customs tariffs?
```

The score destroys the dimensions that matter.

---

# 4. Existing Baobab Alignment

Control Plane already adopts the principle that:

```text
CLAIM
≠
EVIDENCE
≠
VERIFICATION
≠
CANONICAL FACT
≠
TRUST / ASSURANCE
≠
COMPLIANCE DECISION.
```

Baobab Regulations SHALL use the same architectural discipline.

For Regulations:

```text
SOURCE FOUND
        │
        ▼
SOURCE IDENTIFIED
        │
        ▼
AUTHORITY IDENTIFIED
        │
        ▼
ARTEFACT ACQUIRED
        │
        ▼
AUTHENTICITY ASSESSED
        │
        ▼
LEGAL STATUS ESTABLISHED
        │
        ▼
COVERAGE / CURRENTNESS ASSESSED
        │
        ▼
FITNESS FOR PURPOSE DETERMINED
        │
        ▼
REGULATORY USE AUTHORISED
```

---

# 5. Research Finding — Official Does Not Mean Binding

Official institutions routinely publish materials of differing legal force.

The WCO, for example, explicitly states that many of its Recommendations are **not binding instruments**, even though they are formally adopted by the WCO Council and are important tools for customs harmonisation.

Therefore:

```text
OFFICIAL
≠
BINDING.
```

---

# 6. Research Finding — Gazette Publication May Contain Different Statuses

South Africa's official government notices repository currently includes, side by side:

```text
final regulations

amendments

proclamations

regulatory notices

draft regulations

invitations for comment.
```

For example, current September 2026 Government Gazette listings include enacted customs amendments as well as proposed regulations explicitly marked for public comment.

Therefore:

```text
PUBLISHED IN OFFICIAL GAZETTE
≠
IN FORCE.
```

---

# 7. Research Finding — Authenticity May Be Legally Defined

The EU provides an instructive mature example.

Its legal framework specifies that the electronic Official Journal is the authentic edition producing legal effects and requires technical arrangements ensuring authenticity, integrity and inalterability.

Therefore:

```text
downloaded from official website
```

and:

```text
legally authentic edition
```

are conceptually different states.

---

# 8. Research Finding — Consolidated Does Not Necessarily Mean Authentic

EUR-Lex explicitly states that its consolidated texts are documentation tools and do not themselves have legal effect; authentic versions remain those published in the Official Journal.

This is a particularly important lesson for Baobab:

```text
most convenient text
≠
legally controlling publication.
```

---

# 9. Research Finding — Uganda Gazette

Uganda Printing and Publishing Corporation describes the Uganda Gazette as the **official Government publication** containing notices, declarations, Bills, statutes, statutory instruments and legal notices, and states that Acts of Parliament are required to be published in the Gazette. UPPC also now exposes a sizeable official e-Gazette archive.

This provides an important initial source-authority anchor for Uganda.

---

# 10. OECD Law-as-Code Principle

The OECD's 2026 Law-as-Code consultation makes an equally important distinction:

> the authoritative legal text remains the legally binding source even where an authoritative machine-executable representation is supplied.

The machine representation remains explicitly linked to the legal text from which it derives.

Baobab SHALL preserve that separation.

---

# 11. W3C Provenance Principle

W3C PROV defines provenance as information concerning entities, activities and agents involved in producing information and notes that provenance can support assessments of quality, reliability and trustworthiness.

Baobab SHALL therefore derive source assurance from provenance, not simply assign trust labels without evidence.

---

# 12. Core Source Chain

The canonical source chain SHALL distinguish:

```text
REGULATORY AUTHORITY
        │
        ▼
OFFICIAL / DESIGNATED PUBLISHER
        │
        ▼
REGULATORY SOURCE
        │
        ▼
PUBLICATION CHANNEL
        │
        ▼
SOURCE EDITION / RELEASE
        │
        ▼
SOURCE ARTEFACT
        │
        ▼
ACQUISITION
        │
        ▼
NORMALISED REPRESENTATION
        │
        ▼
CANONICAL REGULATORY OBJECT
```

These identities MAY coincide.

They SHALL NOT be assumed equivalent.

---

# 13. Authority

`RegulatoryAuthority` answers:

> Which institution possesses the relevant legal or regulatory authority?

Examples:

```text
Parliament

Ministry

Customs authority

Regulator

Court

Regional institution

Treaty body.
```

---

# 14. Publisher

`RegulatoryPublisher` answers:

> Which body officially publishes or disseminates the material?

The publisher may be:

```text
the authority itself

a government printer

an official publications office

a designated repository.
```

---

# 15. Uganda Example

Conceptually:

```text
Authority:
Parliament / relevant authority

Official publication:
Uganda Gazette

Official publisher:
UPPC.
```

UPPC explicitly identifies itself as the official publisher of the Uganda Gazette.

---

# 16. EU Example

Conceptually:

```text
Authority:
EU institution

Legal act:
Regulation / Directive / Decision

Authentic publication:
Official Journal

Publisher:
Publications Office.
```

The EU legal framework assigns responsibility for publication and authenticity of the electronic Official Journal to the Publications Office.

---

# 17. Source Provider

`RegulatorySourceProvider`, established in ADR-REG-0005, answers:

> Through whom did Baobab obtain the information?

Possible:

```text
official publisher

authority API

commercial vendor

legal database

tenant

professional counsel.
```

Provider SHALL remain separate from authority.

---

# 18. Repository

`RegulatoryRepository` or equivalent MAY identify:

```text
website

database

archive

API

portal

document repository
```

through which the source is accessed.

---

# 19. Source

`RegulatorySource` SHALL represent the logical information source.

Examples:

```text
Uganda Gazette

South African Government Gazette

SARS Customs Tariff schedules

AfCFTA legal instruments repository

WCO HS legal instruments

official court judgments repository.
```

---

# 20. Source Edition

A `SourceEdition` SHALL represent a particular published issue, release, edition or identifiable source state.

Examples:

```text
Uganda Gazette
Vol. CXIX No. 91
25 September 2026

South African Government Gazette
No. 55424
18 September 2026.
```

---

# 21. Source Artefact

`SourceArtefact` represents the bytes actually obtained:

```text
PDF

XML

JSON

HTML

CSV

XLSX

signed package.
```

---

# 22. Edition Is Not Artefact

One source edition may exist as:

```text
PDF

HTML

XML.
```

The legal edition identity and technical artefact identity SHALL therefore remain different.

---

# 23. Source Registry

The **Authoritative Source Registry** SHALL be a governed catalogue of regulatory sources.

It SHALL NOT merely be:

```text
table of URLs.
```

---

# 24. Source Registry Entry

Conceptually:

```text
RegulatorySource
├── source_id
├── source_key
├── canonical_name
├── source_type
├── authority_refs[]
├── publisher_refs[]
├── provider_refs[]
├── jurisdiction_refs[]
├── regime_refs[]
├── regulatory_domains[]
├── official_status
├── legal_publication_role
├── access_methods[]
├── language[]
├── coverage_profile
├── authenticity_profile
├── currency_profile
├── completeness_profile
├── rights_profile
├── use_policy
├── lifecycle_state
├── valid_from
├── valid_to?
└── provenance
```

---

# 25. Source Registry Is Canonical

Source identity SHALL be durable.

If:

```text
https://old.gov.example/gazette
```

moves to:

```text
https://new.gov.example/gazette
```

Baobab updates its endpoint.

It SHALL not invent a new Gazette identity.

---

# 26. Endpoint Is Operational

`RegulatoryEndpoint` SHALL continue to represent:

```text
URL

API

SFTP

MCP

download endpoint

RSS feed

portal.
```

Endpoint state SHALL not determine source authority.

---

# 27. Source Type

Initial source types SHOULD include:

```text
OFFICIAL_GAZETTE

OFFICIAL_JOURNAL

LEGISLATION_REPOSITORY

REGULATOR_PUBLICATION

COURT_REPOSITORY

TREATY_REPOSITORY

OFFICIAL_REGISTER

OFFICIAL_DATASET

OFFICIAL_API

OFFICIAL_MACHINE_RULE

OFFICIAL_GUIDANCE

OFFICIAL_CONSOLIDATION

INTERGOVERNMENTAL_PUBLICATION

COMMERCIAL_REGULATORY_PROVIDER

PROFESSIONAL_COMMENTARY

ACADEMIC_SOURCE

TENANT_COUNSEL

TENANT_SUPPLIED

MACHINE_DERIVED

AI_DERIVED

DISCOVERY_SOURCE
```

---

# 28. Source Type Does Not Define Trust

This is mandatory.

```text
source_type = OFFICIAL
```

does not automatically imply:

```text
binding

current

complete

applicable

authentic edition.
```

---

# 29. Source Authority Dimensions

Baobab SHALL assess sources along explicit dimensions.

The initial dimensions SHALL include:

```text
D1  AUTHORITY IDENTITY

D2  OFFICIAL PUBLICATION STATUS

D3  LEGAL FORCE / ROLE

D4  AUTHENTICITY

D5  INTEGRITY

D6  TEMPORAL CURRENTNESS

D7  COMPLETENESS

D8  COVERAGE

D9  PROVENANCE COMPLETENESS

D10 TRANSFORMATION DISTANCE

D11 INTERPRETIVE STATUS

D12 VERIFICATION STATUS

D13 RIGHTS / LICENSING

D14 TECHNICAL AVAILABILITY

D15 FITNESS FOR PURPOSE
```

---

# 30. No Aggregated Trust Score

These dimensions SHALL NOT be obligatorily collapsed into:

```text
87 / 100
```

or:

```text
HIGH TRUST.
```

A compact user-facing summary MAY exist.

The underlying dimensions SHALL remain accessible.

---

# 31. D1 — Authority Identity

This dimension asks:

> Is the institution whose authority is claimed correctly identified?

Possible state:

```text
VERIFIED

PROBABLE

UNVERIFIED

DISPUTED

UNKNOWN.
```

---

# 32. Authority Verification

Verification SHOULD rely upon:

```text
official institutional identity

enabling law

official government registry

official treaty structure

verified succession relationship.
```

---

# 33. Authority Identity Is Not Source Authenticity

We may know:

```text
SARS is the relevant authority
```

while still not knowing whether:

```text
the PDF we downloaded
is authentic.
```

---

# 34. D2 — Official Publication Status

Possible states:

```text
OFFICIAL_AUTHENTIC_PUBLICATION

OFFICIAL_PUBLICATION

OFFICIAL_REPOSITORY_COPY

OFFICIAL_MIRROR

OFFICIALLY_DESIGNATED_THIRD_PARTY

NON_OFFICIAL

UNKNOWN.
```

---

# 35. Authentic Legal Publication

`OFFICIAL_AUTHENTIC_PUBLICATION` SHALL be used only where the jurisdiction or competent authority establishes that the publication form itself is authentic or legally effective.

---

# 36. EU Example

The EU provides a clear model: its electronic Official Journal is legally designated authentic and legally effective under the relevant Regulation.

Baobab SHALL record such status where jurisdictions provide it.

---

# 37. Official Repository Copy

A government website may reproduce legislation without that reproduction itself being legally designated the authentic publication.

This is still valuable.

It is simply a different status.

---

# 38. D3 — Legal Force / Role

The source material SHALL describe its legal role separately.

Possible categories:

```text
BINDING_LEGAL_TEXT

BINDING_DECISION

OFFICIAL_NOTICE

OFFICIAL_INTERPRETATION

OFFICIAL_GUIDANCE

OFFICIAL_PROCEDURE

DRAFT

CONSULTATION

INFORMATIONAL

NON_BINDING_RECOMMENDATION

SECONDARY_INTERPRETATION

UNKNOWN.
```

---

# 39. Legal Force Belongs to Material, Not Website

The same official repository may contain:

```text
binding regulation

draft regulation

guidance

press release

consultation document.
```

Therefore:

```text
domain = gov.example
```

cannot determine legal force.

---

# 40. South African Example

Current South African Government Gazette listings illustrate this directly: published notices include final Customs and Excise schedule amendments alongside regulations marked for comment.

Each artefact therefore requires its own legal-status metadata.

---

# 41. WCO Example

WCO Recommendations demonstrate another case where:

```text
official
+
important
+
authoritative organisational source
```

does not imply:

```text
legally binding.
```


---

# 42. D4 — Authenticity

Authenticity asks:

> Is this artefact what it claims to be?

Possible states:

```text
CRYPTOGRAPHICALLY_VERIFIED

OFFICIAL_PUBLISHER_VERIFIED

VERIFIED_AGAINST_OFFICIAL

MANUALLY_VERIFIED

UNVERIFIED

AUTHENTICITY_FAILED

UNKNOWN.
```

---

# 43. Cryptographic Authenticity

Where an official source provides:

```text
digital signature

signed XML

certificate

cryptographic manifest
```

Baobab SHOULD verify it.

---

# 44. EU Example

The electronic Official Journal's authenticity architecture explicitly uses technical measures allowing its authentic character and integrity to be verified.

---

# 45. TLS Does Not Establish Legal Authenticity

A successful HTTPS request establishes transport security properties.

It does NOT itself prove:

```text
this is the legally authentic edition.
```

---

# 46. Domain Ownership Does Not Establish Legal Authenticity

Likewise:

```text
URL ends in .gov
```

does not by itself prove that every document is authentic or legally binding.

---

# 47. D5 — Integrity

Integrity asks:

> Have the acquired bytes remained unchanged?

Every retained artefact SHOULD carry a cryptographic content hash.

Conceptually:

```text
content_hash_algorithm
content_hash
retrieved_at
storage_hash_verified_at.
```

---

# 48. Hash Purpose

The hash proves:

```text
stored artefact A
is byte-identical
to acquired artefact A.
```

It does not prove:

```text
artefact A was legally correct.
```

---

# 49. Integrity versus Authenticity

```text
Integrity:
Has the object changed?

Authenticity:
Is the object genuinely what it claims?
```

They SHALL remain different dimensions.

---

# 50. Signed but Superseded

A cryptographically authentic publication can still be:

```text
repealed

superseded

expired.
```

Authenticity does not establish currentness.

---

# 51. D6 — Temporal Currentness

Currentness asks:

> Is this representation sufficiently current for the intended use?

Possible:

```text
CURRENT

CURRENT_AS_OF_DATE

SUPERSEDED

REPEALED

STALE

UPDATE_EXPECTED

UNKNOWN.
```

---

# 52. Currentness Is Purpose-Specific

A 2019 regulation may still be current law.

A tariff feed last updated six months ago may be dangerously stale.

Therefore:

```text
age
≠
staleness.
```

---

# 53. Freshness Policy

Each source SHOULD specify:

```text
expected publication cadence

expected update latency

maximum operational staleness

criticality

stale-source behaviour.
```

---

# 54. Publication Time versus Retrieval Time

Baobab SHALL separately record:

```text
published_at

effective_at

retrieved_at

verified_at.
```

---

# 55. Retrieval Time Does Not Establish Legal Time

A regulation retrieved today may have:

```text
effective_from = 2021.
```

---

# 56. Future Material

A source may publish an amendment today that becomes effective in three months.

Baobab SHALL represent:

```text
CURRENTLY_PUBLISHED

FUTURE_EFFECTIVE.
```

---

# 57. D7 — Completeness

Completeness asks:

> How much of the underlying regulatory object does this source representation contain?

Possible:

```text
COMPLETE

COMPLETE_FOR_DECLARED_SCOPE

PARTIAL

EXCERPT

SUMMARY

METADATA_ONLY

UNKNOWN.
```

---

# 58. Summary Is Not Full Legal Text

A government page summarising a regulation may be highly official and accurate but still incomplete for machine-rule derivation.

---

# 59. Consolidated Text Example

A consolidated text may be substantially more complete for current reading than an individual amendment notice while still not itself being the legally authentic edition.

EUR-Lex explicitly warns that its consolidated versions are documentation tools without independent legal effect.

This demonstrates why completeness and legal authenticity must be separate dimensions.

---

# 60. D8 — Coverage

Coverage asks:

> Which regulatory universe does this source claim to cover?

Dimensions may include:

```text
jurisdiction

regulatory domain

instrument type

historical period

language

product classification

authority

legal publication type.
```

---

# 61. Coverage Profile

Conceptually:

```text
SourceCoverageProfile
├── jurisdiction_refs[]
├── regime_refs[]
├── domain_refs[]
├── authority_refs[]
├── instrument_types[]
├── languages[]
├── temporal_start?
├── temporal_end?
├── included_material[]
├── excluded_material[]
└── completeness_state
```

---

# 62. Coverage Must Include Exclusions

A source saying:

```text
South Africa customs
```

may exclude:

```text
anti-dumping notices

SPS

excise

court decisions

provincial requirements.
```

Known exclusions SHALL be explicit.

---

# 63. Unknown Coverage

If Baobab does not know whether the source is exhaustive:

```text
coverage = UNKNOWN
```

is correct.

---

# 64. D9 — Provenance Completeness

Provenance asks whether Baobab can reconstruct:

```text
provider

source

publisher

authority

endpoint

retrieval

artefact

transformation

review

promotion.
```

---

# 65. Provenance Profile

Potential states:

```text
COMPLETE

SUFFICIENT_FOR_PURPOSE

PARTIAL

BROKEN

UNKNOWN.
```

---

# 66. W3C Alignment

W3C PROV's Entity–Activity–Agent model provides a useful foundation for describing how an artefact was produced and who was responsible for transformations.

Baobab's domain model SHALL remain richer but interoperable.

---

# 67. D10 — Transformation Distance

Baobab SHALL record how far a representation has moved from its authoritative source.

Possible conceptual levels:

```text
T0 ORIGINAL_AUTHENTIC

T1 OFFICIAL_REPRESENTATION

T2 OFFICIAL_CONSOLIDATION

T3 VERIFIED_MIRROR

T4 PROVIDER_NORMALISATION

T5 HUMAN_EXTRACTION

T6 MACHINE_EXTRACTION

T7 HUMAN_INTERPRETATION

T8 AI_ASSISTED_INTERPRETATION

T9 AI_GENERATED_SYNTHESIS.
```

---

# 68. Transformation Level Is Not Trust Rank

An excellent verified machine extraction can be operationally more useful than an original scanned Gazette.

But only the Gazette may possess authoritative publication status.

Different purposes require different dimensions.

---

# 69. Transformation Chain

Example:

```text
Official Gazette PDF
       │
       ▼
OCR extraction
       │
       ▼
Structured provision
       │
       ▼
Human interpretation
       │
       ▼
Machine rule.
```

Every stage SHALL remain linked.

---

# 70. No Provenance Collapse

Baobab SHALL never replace the chain with:

```text
source = AI.
```

The AI transformation and underlying legal source are both material.

---

# 71. D11 — Interpretive Status

Interpretive status asks:

> Is the material itself law, an authority interpretation, or someone else's analysis?

Potential:

```text
LEGAL_TEXT

AUTHORITY_INTERPRETATION

JUDICIAL_INTERPRETATION

AUTHORITY_GUIDANCE

BAOBAB_INTERPRETATION

TENANT_COUNSEL_INTERPRETATION

COMMERCIAL_PROVIDER_INTERPRETATION

PROFESSIONAL_COMMENTARY

ACADEMIC_COMMENTARY

AI_GENERATED_INTERPRETATION.
```

---

# 72. Interpretation Does Not Become Authority Through Quality

A sophisticated law-firm analysis may be excellent.

It remains:

```text
professional interpretation
```

unless a competent legal mechanism gives it another status.

---

# 73. Court Decisions

Judicial decisions SHALL be classified through the authority and precedent model established by ADR-REG-0007.

A case-summary website is not equivalent to the underlying judgment.

---

# 74. Regulator FAQ

A regulator FAQ may be:

```text
official

useful

current
```

while having different legal force from:

```text
statute

regulation

binding determination.
```

Baobab SHALL preserve that distinction.

---

# 75. D12 — Verification Status

The source registry SHALL distinguish:

```text
DISCOVERED

IDENTIFIED

AUTHORITY_VERIFIED

AUTHENTICITY_VERIFIED

LEGAL_STATUS_VERIFIED

COVERAGE_VERIFIED

RIGHTS_VERIFIED

FULLY_VERIFIED_FOR_PURPOSE

VERIFICATION_FAILED.
```

---

# 76. Verification Is Atomic

Avoid:

```text
verified = true.
```

Instead record **what** was verified.

---

# 77. Verification Record

Conceptually:

```text
SourceVerification
├── verification_id
├── source_ref
├── verification_type
├── verifier
├── method
├── result
├── evidence_refs[]
├── performed_at
├── expires_at?
├── notes
└── supersedes?
```

---

# 78. Verification Types

Potential:

```text
AUTHORITY_IDENTITY

PUBLISHER_IDENTITY

DOMAIN_OWNERSHIP

OFFICIAL_STATUS

AUTHENTICITY

LEGAL_FORCE

PUBLICATION_DATE

CURRENTNESS

COVERAGE

COMPLETENESS

RIGHTS

TECHNICAL_INTEGRITY.
```

---

# 79. Verification Expiry

Some verification may be stable.

Example:

```text
The Uganda Gazette is an official government publication.
```

Others may need periodic revalidation:

```text
This provider still has rights.

This endpoint remains official.

This tariff feed remains current.
```

---

# 80. D13 — Rights and Licensing

A source SHALL NOT be operationally approved without known or consciously accepted rights state.

Possible:

```text
PUBLIC_DOMAIN

OPEN_LICENCE

GOVERNMENT_REUSE_PERMITTED

COMMERCIAL_LICENCE

CONTRACTUAL_ACCESS

RESTRICTED

UNKNOWN.
```

Detailed semantics belong to `ADR-REG-0012`.

---

# 81. Rights Unknown Is Material

The architecture SHALL support:

```text
SOURCE_LEGALLY_AUTHORITATIVE
+
RIGHTS_UNKNOWN.
```

Baobab may know what the law says while still lacking rights to redistribute a commercial representation of it.

---

# 82. D14 — Technical Availability

Availability asks:

```text
Can Baobab currently acquire the source?
```

Possible:

```text
AVAILABLE

DEGRADED

RATE_LIMITED

AUTH_FAILURE

UNAVAILABLE

RETIRED.
```

---

# 83. Availability Is Not Trust

A source can be:

```text
legally perfect
but currently offline.
```

Or:

```text
highly available
but non-authoritative.
```

---

# 84. D15 — Fitness for Purpose

This is the central derived dimension.

Baobab SHALL evaluate whether a source is fit for a **specific regulatory use**.

---

# 85. SourceUsePurpose

Initial purposes SHALL include:

```text
DISCOVERY

CHANGE_DETECTION

CORROBORATION

LEGAL_CITATION

PROVISION_EXTRACTION

INTERPRETATION_SUPPORT

RULE_DERIVATION

RULE_VERIFICATION

ADVISORY_ASSESSMENT

REVIEW_GATE_ASSESSMENT

AUTOMATED_ENFORCEMENT

HISTORICAL_RECONSTRUCTION

CUSTOMER_DISPLAY.
```

---

# 86. Fitness Is Purpose-Specific

Example:

```text
Law-firm alert
```

may be excellent for:

```text
CHANGE_DETECTION
```

and unsuitable as sole support for:

```text
AUTOMATED_ENFORCEMENT.
```

---

# 87. Commercial Provider Example

A high-quality commercial provider may be excellent for:

```text
global monitoring

structured tariff content

normalisation

change detection

rule candidate generation.
```

It may still require linkage to authoritative sources before certain E4 decisions.

---

# 88. Official Scanned Gazette Example

A scanned official Gazette may be excellent for:

```text
LEGAL_CITATION

AUTHORITY

historical proof.
```

But poor for:

```text
real-time structured transactional computation.
```

Baobab solves this through derivation, not by downgrading the Gazette.

---

# 89. SourceUsePolicy

Baobab SHALL maintain governed policies describing source requirements for each purpose.

Conceptually:

```text
SourceUsePolicy
├── purpose
├── jurisdiction_scope?
├── regulatory_domain?
├── minimum_authority_status
├── authenticity_requirement
├── currentness_requirement
├── completeness_requirement
├── provenance_requirement
├── allowed_transformations[]
├── verification_requirement
├── rights_requirement
├── corroboration_requirement?
└── effect_ceiling
```

---

# 90. Discovery Policy

Discovery may allow:

```text
news

search

professional updates

commercial feeds

AI discovery.
```

But their discoveries enter:

```text
CANDIDATE
```

state.

---

# 91. Change Detection Policy

Change detection may use:

```text
official feeds

commercial monitoring

law-firm alerts

web-page diffing

AI-assisted discovery.
```

The detected event still requires source verification.

---

# 92. Legal Citation Policy

High-assurance legal citation SHOULD ordinarily prefer:

```text
authentic official publication
```

or:

```text
verified official source
```

according to jurisdiction.

---

# 93. Rule Derivation Policy

Production rule derivation SHOULD require traceability to:

```text
authoritative legal source

or

authority-issued machine rule.
```

Secondary sources MAY support interpretation.

---

# 94. Automated Enforcement Policy

E4 enforcement SHALL require stricter source-policy satisfaction than advisory output.

At minimum, relevant law SHOULD possess:

```text
verified authority

verified legal status

sufficient authenticity

sufficient currentness

complete provenance

verified interpretation/rule chain.
```

---

# 95. Enforcement Source Chain

Preferred:

```text
Authoritative Source
       │
       ▼
Verified Provision
       │
       ▼
Governed Interpretation
       │
       ▼
Verified Rule
       │
       ▼
E4 Decision.
```

---

# 96. Secondary-Only E4

A rule supported only by:

```text
blog

commercial summary

AI answer
```

SHALL NOT independently receive E4 authority.

---

# 97. Source Trust Assessment

Fitness SHALL be evaluated through a contextual `SourceTrustAssessment`.

Conceptually:

```text
SourceTrustAssessment
├── source_ref
├── purpose
├── effective_at
├── authority_state
├── official_status
├── authenticity_state
├── legal_force_state
├── currentness_state
├── completeness_state
├── coverage_state
├── provenance_state
├── transformation_state
├── verification_state
├── rights_state
├── availability_state
├── gaps[]
├── outcome
└── evaluated_at
```

---

# 98. Source Trust Assessment Outcome

Possible:

```text
FIT

FIT_WITH_CONDITIONS

FIT_FOR_DISCOVERY_ONLY

REVIEW_REQUIRED

NOT_FIT

INDETERMINATE.
```

---

# 99. No Numeric Average

The assessment SHALL not determine fitness by:

```text
average(all dimensions).
```

Some requirements are non-compensable.

---

# 100. Non-Compensable Failure Example

For E4:

```text
authenticity failed
```

cannot be offset by:

```text
great API availability.
```

---

# 101. Another Example

For customer display:

```text
redistribution prohibited
```

cannot be offset by:

```text
high legal authority.
```

---

# 102. Policy Logic

Conceptually:

```text
IF
    authority_verified
AND authenticity_sufficient
AND legal_status_verified
AND currentness_sufficient
AND provenance_complete
AND rights_allow_required_use

THEN
    source fit for Purpose P
ELSE
    condition/review/fail.
```

---

# 103. Source Trust Is Temporal

A source considered fit yesterday may become unfit today because:

```text
new edition published

licence expired

endpoint compromised

authority reorganised

source ceased updating.
```

---

# 104. Source Trust Is Versioned

Every consequential SourceTrustAssessment SHOULD record:

```text
policy_version

source_profile_version

effective_at.
```

---

# 105. Historical Trust

A historical assessment should evaluate whether:

```text
the source was valid for the historical regulatory decision
```

not whether the source is active today.

---

# 106. Source Registry Lifecycle

Source lifecycle SHOULD support:

```text
DISCOVERED

UNDER_REVIEW

APPROVED

ACTIVE

DEGRADED

SUSPENDED

DEPRECATED

RETIRED.
```

---

# 107. Discovered

`DISCOVERED` means:

```text
Baobab knows the source exists.
```

It does NOT mean:

```text
Baobab trusts it.
```

---

# 108. Under Review

`UNDER_REVIEW` means:

```text
identity / authority / rights / coverage
are being established.
```

---

# 109. Approved

`APPROVED` means the source has passed onboarding for at least one declared purpose.

---

# 110. Active

`ACTIVE` means:

```text
approved
+
operational acquisition enabled.
```

---

# 111. Degraded

`DEGRADED` may reflect:

```text
staleness

partial outage

schema drift

missing updates

rights uncertainty

coverage issue.
```

---

# 112. Suspended

`SUSPENDED` means no new authoritative use is permitted pending resolution.

---

# 113. Retired

`RETIRED` means the source is no longer used for new acquisition.

Historical provenance remains.

---

# 114. Source Suspension Does Not Delete History

A suspended or retired source SHALL remain traceable from historical decisions.

---

# 115. Source Approval Is Purpose-Scoped

A source MAY be:

```text
ACTIVE for DISCOVERY

APPROVED for INTERPRETATION_SUPPORT

NOT APPROVED for E4_ENFORCEMENT.
```

---

# 116. Source Registry Governance

Registering a production source SHALL require:

```text
source identity

provider identity

authority mapping

publisher mapping

jurisdiction/domain coverage

purpose

rights

operational owner

verification.
```

---

# 117. Source Approval Authority

Production source approval SHOULD require appropriate governance.

A developer implementing an adapter SHALL NOT automatically possess authority to declare:

```text
this is authoritative law.
```

---

# 118. Separation of Duties

Roles SHOULD conceptually include:

```text
SOURCE_DISCOVERER

SOURCE_OPERATOR

SOURCE_VERIFIER

REGULATORY_REVIEWER

RIGHTS_REVIEWER

SOURCE_APPROVER.
```

One person need not hold every role.

---

# 119. Four-Eyes for High-Impact Sources

Sources supporting E3/E4 decisions SHOULD receive maker-checker review for:

```text
authority

legal status

coverage

rights.
```

---

# 120. SourceRegistryChange

Material changes SHOULD flow through governed change state.

Examples:

```text
official endpoint changed

authority changed

legal authenticity mechanism changed

coverage expanded

source suspended.
```

---

# 121. Source Registry Audit

All material registry changes SHALL record:

```text
actor

timestamp

reason

previous state

new state

supporting evidence.
```

---

# 122. Source Identity Verification

Potential methods:

```text
official institutional page

enabling instrument

official Gazette

DNS / domain confirmation

cryptographic certificate

authority correspondence

contractual provider documentation.
```

---

# 123. Domain Verification Is Supportive

Owning:

```text
regulator.gov.xx
```

may strengthen source identity.

It is not sufficient alone to establish legal force.

---

# 124. Official Mirror

If an official authority republishes another authority's law, Baobab SHOULD distinguish:

```text
OFFICIAL_MIRROR
```

from:

```text
ORIGINAL_AUTHENTIC_PUBLICATION.
```

---

# 125. Third-Party Mirror

A trusted legal information institute may provide an exceptionally useful mirror.

It SHALL retain:

```text
SECONDARY_OR_MIRROR
```

status unless designated otherwise.

---

# 126. Mirror Verification

Baobab MAY verify:

```text
mirror artefact hash
=
official artefact hash
```

where formats permit.

This strengthens content equivalence.

---

# 127. Content Equivalence Is Not Publication Equivalence

Even byte-identical copies may have different legal publication status.

---

# 128. Official Consolidation

A source may supply:

```text
official consolidation.
```

Baobab SHALL record whether the jurisdiction assigns legal force to that consolidation.

---

# 129. Unofficial Consolidation

An unofficial consolidation may still be the best text for:

```text
search

reading

structuring

interpretation.
```

It simply requires linkage back to legally relevant source versions.

---

# 130. Amendments Chain

For an unofficial consolidation:

```text
Base Act
   +
Amendment 1
   +
Amendment 2
   +
Correction
        │
        ▼
Consolidated Text
```

Baobab SHALL preserve every upstream authoritative relationship.

---

# 131. Consolidation Verification

The consolidated representation SHOULD be capable of proving:

```text
which amendments were incorporated

which version date it represents

which amendments were excluded

who created it.
```

---

# 132. Court Judgment Sources

For judicial material, the Registry SHOULD distinguish:

```text
official judgment

court-hosted judgment

certified copy

legal database copy

case summary

headnote

commentary.
```

---

# 133. Case Summary Is Not Judgment

No high-assurance judicial rule SHALL derive solely from:

```text
case summary
```

where the judgment is reasonably obtainable.

---

# 134. Headnote

A headnote may be authored by:

```text
court

official reporter

commercial reporter

editor.
```

Its authority depends on the relevant source system.

---

# 135. Treaty Sources

Treaty materials SHOULD distinguish:

```text
authentic treaty text

depositary record

ratification/accession record

official protocol

annex

amendment

official status table

national implementing source.
```

---

# 136. Treaty Website Summary

A treaty website explaining implementation may be official but still:

```text
guidance
```

rather than treaty text.

---

# 137. Regional Organisations

AfCFTA, EAC, SACU and similar institutions may publish:

```text
treaties

protocols

annexes

decisions

guidance

manuals

tariff material.
```

Each item SHALL carry its own legal-role metadata.

---

# 138. WCO Sources

WCO source materials may include:

```text
Conventions

Recommendations

Data Model

Explanatory Notes

classification material

guidelines.
```

Their normative status differs.

For example, the WCO identifies its conventions separately from non-binding Recommendations.

---

# 139. Machine-Readable Official Source

An official API may provide authoritative data.

Baobab SHALL determine whether:

```text
the API output itself
```

is legally authoritative or:

```text
an official informational representation.
```

---

# 140. Authority-Supplied Machine Rules

Under the direction anticipated by OECD Law-as-Code:

```text
authoritative legal text
       │
       ▼
state-authorised machine representation
```

may eventually become available.

Baobab SHALL represent both objects and their relationship.

---

# 141. Machine Rule Authenticity

An authority-supplied machine rule SHOULD support:

```text
publisher identity

version

signature/hash where available

legal source references

effective dates.
```

---

# 142. Machine Rule Does Not Replace Legal Source Identity

Even where authoritative for computation:

```text
machine rule
```

and:

```text
human-readable legal text
```

SHALL remain separately addressable.

---

# 143. Commercial Providers

Commercial providers SHALL be first-class source providers.

They SHALL not be downgraded merely for being commercial.

---

# 144. Commercial Provider Strength

A commercial provider may offer superior:

```text
coverage

normalisation

translations

change detection

machine-readable structure

historical depth

API reliability.
```

---

# 145. Commercial Provider Limitation

A commercial provider normally does not become:

```text
sovereign legal authority
```

merely because its content is excellent.

---

# 146. Provider Provenance Requirement

Baobab SHOULD prefer commercial products that preserve:

```text
underlying authority

source reference

publication date

effective date

citation.
```

Opaque regulatory conclusions are harder to govern.

---

# 147. Provider Without Source Links

A provider lacking upstream source lineage MAY still support:

```text
discovery

corroboration.
```

Its suitability for:

```text
rule derivation

high-assurance enforcement
```

SHALL be limited by policy.

---

# 148. Professional Commentary

Professional sources include:

```text
law firms

accountancy firms

customs advisers

industry specialists.
```

These may be highly valuable for interpretation and change discovery.

---

# 149. Commentary Status

Professional commentary SHALL remain:

```text
SECONDARY_INTERPRETATION
```

unless another legal mechanism establishes different status.

---

# 150. Academic Sources

Academic material may support:

```text
interpretive research

comparative analysis

conceptual modelling.
```

It SHALL not ordinarily become primary regulatory authority.

---

# 151. News Sources

News MAY support:

```text
DISCOVERY

CHANGE_DETECTION.
```

News SHALL NOT independently establish production legal rules.

---

# 152. Search Engines

Search engine results are discovery mechanisms.

They SHALL never become canonical regulatory sources themselves.

---

# 153. AI Answers

An AI answer is:

```text
generated representation
```

not:

```text
legal authority.
```

---

# 154. AI With Citations

An AI answer containing citations may assist discovery and interpretation.

The citations, not the fluency of the answer, determine source authority.

---

# 155. AI Source Chain

Preferred:

```text
AI output
     │
     ▼
Citation
     │
     ▼
Official Source
```

Baobab SHOULD resolve through to the official source where consequential.

---

# 156. Hallucinated Citation

If cited material cannot be resolved:

```text
SOURCE_UNVERIFIED
```

not:

```text
rule accepted.
```

---

# 157. Tenant Counsel

Tenant-provided legal counsel opinions SHALL be supported as:

```text
TENANT_COUNSEL_INTERPRETATION.
```

They may be highly authoritative for the tenant's risk posture.

They are not public law.

---

# 158. Tenant Counsel Scope

The opinion SHALL record where known:

```text
tenant

legal entity

jurisdiction

subject

date

assumptions

counsel identity

scope.
```

---

# 159. Privilege

Counsel material MAY be legally privileged.

Registry metadata, graph access, search and AI retrieval SHALL respect its classification.

---

# 160. Tenant-Supplied Government Determination

A customer may provide:

```text
customs ruling

regulator correspondence

tax ruling

permit.
```

This may carry significantly stronger regulatory authority than ordinary tenant evidence.

The underlying authority and scope SHALL be verified.

---

# 161. Self-Asserted Source

Customer claims such as:

```text
"We have been told this permit is unnecessary."
```

remain:

```text
SELF_ASSERTED
```

until supported.

---

# 162. Conflicting Sources

The Registry SHALL support explicit source conflicts.

---

# 163. Source Conflict Types

Potential:

```text
CONTENT_CONFLICT

STATUS_CONFLICT

DATE_CONFLICT

AUTHORITY_CONFLICT

VERSION_CONFLICT

INTERPRETATION_CONFLICT

COVERAGE_CONFLICT.
```

---

# 164. Conflict Does Not Mean Majority Vote

Three secondary sources agreeing SHALL not necessarily override one authentic authoritative source.

---

# 165. Conflict Resolution Order

Conceptually:

```text
1. Confirm identities.

2. Confirm versions.

3. Confirm relevant legal time.

4. Confirm authority.

5. Confirm legal status.

6. Confirm authenticity.

7. Confirm whether texts actually conflict.

8. Apply legal hierarchy.

9. Review interpretation if unresolved.
```

---

# 166. Official Sources Can Conflict

Where two official sources apparently disagree:

```text
REVIEW_REQUIRED
```

may be correct.

Possible causes include:

```text
amendment timing

correction

different jurisdiction

different legal force

publication error

consolidation lag.
```

---

# 167. Correction

The source model SHALL distinguish:

```text
SOURCE_CORRECTION

LEGAL_CORRECTION

BAOBAB_EXTRACTION_CORRECTION.
```

---

# 168. Corrigendum

An official corrigendum may alter legally relevant source text.

It SHALL become part of the regulatory lifecycle graph.

---

# 169. Provider Correction

Commercial provider correction does not automatically mean the law changed.

---

# 170. Baobab Parser Correction

Likewise:

```text
OCR error corrected
```

is not:

```text
legal amendment.
```

---

# 171. Authenticity Failure

If a retained artefact fails authenticity validation:

```text
QUARANTINE
```

SHALL be considered.

It SHALL not continue supporting new consequential rules.

---

# 172. Integrity Failure

Hash mismatch SHALL be treated as security/data-integrity incident.

---

# 173. Source Compromise

If an official endpoint is suspected compromised:

```text
source lifecycle = SUSPENDED / DEGRADED
```

may be appropriate.

Existing historical artefacts remain separately evaluated.

---

# 174. Availability Failure

If an official portal is offline:

```text
UNAVAILABLE
```

does not mean:

```text
source untrustworthy.
```

---

# 175. Fallback Source

Baobab MAY use verified fallback representations when primary access is unavailable.

---

# 176. Fallback Requirements

Fallback use SHOULD preserve:

```text
which source was unavailable

which fallback was used

content equivalence evidence

fallback's authority status.
```

---

# 177. Offline Authentic Copy

An archived authentic copy may remain stronger legal evidence than a currently available secondary summary.

---

# 178. Source Snapshot

For consequential decisions, Baobab SHOULD preserve immutable source snapshots where licensing allows.

---

# 179. Snapshot Purpose

Snapshotting allows:

```text
historical proof

replay

audit

parser correction

source dispute investigation.
```

---

# 180. Snapshot Is Not Canonical Law

A snapshot represents:

```text
what Baobab acquired.
```

It does not independently become law.

---

# 181. Retention

Retention SHALL account for:

```text
legal audit need

source rights

customer requirements

data classification

historical decision survivability.
```

---

# 182. Source Hash

Every retained consequential source artefact SHOULD record:

```text
SHA-256
```

or another approved cryptographic hash.

Algorithm agility SHALL be supported.

---

# 183. Hash Migration

If a hash algorithm becomes unsuitable:

```text
new hash
```

may be added.

The old provenance shall remain.

---

# 184. Source Signature

Where a source supplies a digital signature:

```text
signature

certificate chain

verification time

verification result
```

SHOULD be retained.

---

# 185. Certificate Expiry

A signing certificate expiring later does not necessarily invalidate an artefact correctly signed while valid.

Signature validation semantics must preserve verification time.

---

# 186. Timestamping

Trusted timestamps MAY improve proof for high-value artefacts.

This is optional initially.

---

# 187. Retrieval Metadata

Every acquisition SHOULD retain:

```text
retrieved_at

endpoint

request identifier

HTTP validators where available

media type

content length

response metadata.
```

---

# 188. ETag / Last-Modified

These MAY support:

```text
change detection

retrieval optimisation.
```

They SHALL not substitute for legal versioning.

---

# 189. Source Edition Identifier

Where official publications expose:

```text
Gazette number

issue number

notice number

CELEX identifier

official treaty number
```

Baobab SHOULD preserve them as external references.

---

# 190. Canonical Baobab Source ID

Those official identifiers SHALL NOT automatically replace Baobab's stable internal identity.

---

# 191. Official Identifier Is Valuable

It SHOULD appear in:

```text
citations

audit evidence

customer explanations.
```

---

# 192. Source Citation

The Registry SHOULD support generation of structured citation metadata.

Conceptually:

```text
SourceCitation
├── authority
├── instrument
├── publication
├── publication_identifier
├── publication_date
├── provision_locator
├── language
├── canonical_uri?
└── artefact_ref
```

---

# 193. Citation Is Not Provenance

Citation tells the reader:

```text
where to find the legal material.
```

Provenance tells Baobab:

```text
how this system object was derived from it.
```

Both are needed.

---

# 194. Deep Citation

Where possible, citation SHOULD identify:

```text
section

article

paragraph

schedule

table row

gazette notice

page.
```

---

# 195. Stable Citation

Citation SHOULD prefer stable official identifiers over transient URLs where available.

---

# 196. Source Languages

The Registry SHALL record source language.

---

# 197. Authentic Language

Where only specified language versions are legally authentic:

```text
authentic_language_status
```

SHALL be representable.

---

# 198. Translation Status

Translations SHALL distinguish:

```text
OFFICIAL

AUTHORISED

HUMAN_UNOFFICIAL

PROVIDER

MACHINE.
```

---

# 199. Translation Cannot Conceal Original

Every translated regulatory representation SHALL retain a path to the original-language source.

---

# 200. Translation Conflict

Where translations diverge:

```text
TRANSLATION_CONFLICT
```

SHALL be supported.

---

# 201. Source Trust and Enforcement Authority

ADR-REG-0004's decision classes SHALL integrate with source fitness.

Conceptually:

```text
weak / incomplete source chain
       ↓
E0 / E1

verified source but interpretation unresolved
       ↓
E1 / E2

verified authority + rule + deterministic semantics
       ↓
potential E3 / E4
```

---

# 202. Source Trust Is Necessary but Not Sufficient

A perfect source cannot by itself create E4 authority.

The rule must also have:

```text
verified interpretation

applicability

context

evidence

decision policy.
```

---

# 203. Enforcement Ceiling

A SourceUsePolicy MAY specify:

```text
max_effect_class.
```

---

# 204. Example

```text
Professional commentary only
       ↓
max E1
```

unless corroborated by the required authoritative chain.

---

# 205. Another Example

```text
Official authentic regulation
+
verified rule
+
complete context
+
deterministic requirement
       ↓
potential E4.
```

---

# 206. Source Trust and Rule Assurance

Rule assurance SHALL include the state of every material upstream source.

If a source is suspended:

```text
dependent rule assurance
```

may need recalculation.

---

# 207. Trust Propagation Is Not Numeric

Do not calculate:

```text
source 90%
×
interpretation 90%
=
rule 81%.
```

---

# 208. Trust Dependency

Instead record:

```text
Source:
AUTHENTIC_VERIFIED

Interpretation:
HUMAN_REVIEWED

Rule:
REGRESSION_VERIFIED

Coverage:
COMPLETE_FOR_SCOPE.
```

---

# 209. Broken Source Chain

If an upstream artefact becomes invalid:

```text
Rule
```

SHOULD become:

```text
ASSURANCE_DEGRADED
```

or:

```text
SUSPENDED
```

according to policy.

---

# 210. Graph Integration

ADR-REG-0010 SHALL link:

```text
Rule
DERIVED_FROM
Interpretation
DERIVED_FROM
Provision
PUBLISHED_AS
Artefact
ACQUIRED_FROM
Source
ISSUED_BY
Authority.
```

---

# 211. Trust Traversal

A decision SHOULD be able to answer:

> What is the weakest unresolved trust dimension in this source chain?

---

# 212. Trust Path Example

```text
Decision
   │
   ▼
Rule
   │
   ▼
Provision
   │
   ▼
Official Gazette
   │
   ├── official status: VERIFIED
   ├── authenticity: VERIFIED
   ├── currentness: VERIFIED
   └── rights: VERIFIED.
```

---

# 213. Source Registry Query

Administrative interfaces SHOULD answer:

```text
Which official customs sources do we use for Uganda?

Which rules depend on Source X?

Which sources are stale?

Which sources lack rights verification?

Which E4 rules depend on commercial data?

Which sources lack authoritative publication verification?
```

---

# 214. Coverage Dashboard

Example:

| Jurisdiction | Domain | Primary authority source | Structured source | Verification |
|---|---|---|---|---|
| Uganda | Export / customs | Official government sources | adapters/provider | verified/partial |
| South Africa | Customs | Gazette/SARS | structured feeds | verified/partial |
| AfCFTA | Origin | Official AfCFTA instruments | normalised rules | verified/partial |

Actual production state SHALL be data-driven.

---

# 215. No Green Checkmark Without Scope

A UI showing:

```text
South Africa ✓
```

is insufficient.

It must identify:

```text
which domains

which source types

which periods

which confidence/verification dimensions.
```

---

# 216. Source Registry API

Conceptually:

```text
GET /sources

GET /sources/{id}

GET /sources/{id}/coverage

GET /sources/{id}/trust-profile

GET /sources/{id}/verifications

GET /sources/{id}/dependencies

GET /sources/{id}/artefacts
```

Exact API design is deferred.

---

# 217. Source Mutation API

Administrative changes might support:

```text
register

verify

approve

suspend

deprecate

retire.
```

These SHALL require privileged governance.

---

# 218. No Consumer Mutation

Digital Estates SHALL NOT directly alter source trust status.

---

# 219. Source Health

Operational health SHOULD include:

```text
acquisition success

freshness

schema drift

endpoint availability

content anomaly

signature verification

rights validity.
```

---

# 220. Health Is Not Authority

Keep:

```text
SourceHealth
```

separate from:

```text
SourceAuthorityProfile.
```

---

# 221. Source Anomaly

An anomaly may include:

```text
sudden document-volume drop

unexpected empty archive

schema change

missing edition

hash unexpectedly changed

publication sequence gap.
```

---

# 222. Gazette Sequence Monitoring

For Gazette-like sources, unexpected gaps in:

```text
issue sequence
```

may deserve investigation.

They SHALL not automatically imply missing law.

---

# 223. Duplicate Publication

A source may republish identical material.

Baobab SHOULD deduplicate content while preserving distinct publication/acquisition events.

---

# 224. Source Withdrawal

If an authority withdraws material:

```text
WITHDRAWN
```

SHALL be captured.

Historical artefacts remain unless retention rules require otherwise.

---

# 225. Source Retraction

Retraction differs from:

```text
repeal.
```

The source publication itself may have been withdrawn or corrected.

---

# 226. Source Authenticity Incident

Security incidents concerning regulatory sources SHALL potentially trigger:

```text
acquisition suspension

rule dependency review

decision impact analysis.
```

---

# 227. Dependency Blast Radius

Using ADR-REG-0010:

```text
Source compromised
      │
      ▼
Artefacts
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

---

# 228. Source Incident Reassessment

Baobab SHOULD be able to identify every consequential decision whose source chain depended materially on a compromised artefact.

---

# 229. Source Supersession

One source may replace another.

Example:

```text
old government portal
       ↓
new official publication portal.
```

Source identity MAY remain stable if the logical publication is unchanged.

Endpoint/provider relationships change.

---

# 230. New Official Publisher

If official publication responsibility transfers:

```text
Publisher A
       ↓
Publisher B
```

historical editions remain linked to A.

Future editions link to B.

---

# 231. Authority Succession

Similarly, authority succession from ADR-REG-0007 SHALL not rewrite source history.

---

# 232. Source Version versus Instrument Version

A new:

```text
website release
```

does not necessarily mean:

```text
new legal instrument version.
```

---

# 233. Provider Version versus Law Version

Commercial provider revision:

```text
v2026.09.2
```

may simply correct provider data.

It is not necessarily a legal amendment.

---

# 234. Source Evidence Chain

Every consequential regulatory object SHOULD support:

```text
Regulatory Object
        │
        ▼
SourceCitation
        │
        ▼
SourceArtefact
        │
        ▼
SourceEdition
        │
        ▼
RegulatorySource
        │
        ▼
Publisher
        │
        ▼
RegulatoryAuthority.
```

---

# 235. Provenance Activity Chain

Parallel chain:

```text
Artefact
    │
    ▼
Acquisition
    │
    ▼
Extraction
    │
    ▼
Normalisation
    │
    ▼
Interpretation
    │
    ▼
Rule compilation.
```

---

# 236. W3C Mapping

Conceptually:

```text
SourceArtefact
    PROV Entity

Acquisition
    PROV Activity

Extraction
    PROV Activity

Reviewer
    PROV Agent.
```

W3C PROV is expressly intended to support interoperable provenance and assessment of information quality/trustworthiness.

---

# 237. Trust Comes From Evidence

A `SourceTrustProfile` SHALL therefore be explainable through:

```text
verification records

provenance

legal basis

technical evidence.
```

Not opaque administrator opinion.

---

# 238. Manual Verification

Manual verification SHALL be valid where machine verification is impossible.

It SHALL record:

```text
reviewer

method

evidence

date

scope.
```

---

# 239. Manual Does Not Mean Weak

A manually verified official Gazette may be stronger legal evidence than an automated commercial feed.

---

# 240. Automation Does Not Mean Strong

Automated extraction may be technically reliable while being legally secondary.

---

# 241. Trust Policy Should Fail Closed for High Impact

For E3/E4:

```text
material trust dimension unknown
```

SHOULD ordinarily:

```text
degrade

review-gate

or deny authoritative use
```

rather than assume success.

---

# 242. Advisory Paths May Degrade Gracefully

For E0/E1:

```text
secondary sources
```

may be used with clear attribution/caveat.

---

# 243. User Explanations

Baobab SHOULD be able to say:

> This requirement is derived from an authentic official Gazette publication.

or:

> This is based on regulator guidance rather than binding legislation.

or:

> This interpretation comes from your organisation's counsel.

or:

> This change was detected from a commercial feed and is awaiting official-source verification.

Those distinctions build trust.

---

# 244. No Generic Badge

Avoid a UI that simply shows:

```text
Trusted ✓
```

without meaning.

---

# 245. Source Badge Examples

Better:

```text
Official publication

Authenticity verified

In force

Commercially structured

Human-reviewed interpretation.
```

---

# 246. Public Explanations May Be Simplified

End users need not see all source dimensions by default.

Detailed provenance SHALL remain accessible for audit.

---

# 247. Source Trust and Product Liability

Baobab SHALL avoid representing a source as legally authoritative beyond what its verification supports.

Marketing language SHALL not transform:

```text
secondary regulatory data
```

into:

```text
official legal publication.
```

---

# 248. Source Trust and Customer Contracting

Enterprise SLAs may promise:

```text
freshness

coverage

verification process

update latency.
```

They SHOULD NOT promise impossible abstractions such as:

```text
all law is always correct.
```

---

# 249. Source Trust and Commercial Tiers

Higher commercial tiers may provide:

```text
broader source coverage

faster updates

dual-source verification

historical archives

professional review.
```

The underlying law itself is not "premium truth."

---

# 250. Dual-Source Verification

Some high-value domains MAY require:

```text
authoritative source
+
independent structured provider
```

for additional operational assurance.

---

# 251. Dual Sources Are Not Majority Voting

The commercial provider:

```text
corroborates

structures

monitors
```

the authoritative source.

It does not obtain equal legal authority by being second.

---

# 252. Source Concentration

Baobab SHOULD measure:

```text
E4 rules with only one source path

jurisdictions dependent on one commercial provider

rules lacking direct primary-source verification.
```

---

# 253. Concentration Is Strategic Risk

This data can guide:

```text
procurement

source onboarding

resilience investment.
```

---

# 254. Initial Uganda Source Strategy

For Uganda, the initial Registry SHOULD include the official Uganda Gazette through UPPC as an important legal-publication source. UPPC describes the Gazette as Uganda's official government publication and currently operates an official e-Gazette archive.

Additional authorities and domain sources will be registered independently.

---

# 255. Initial South Africa Source Strategy

For South Africa, the Registry SHOULD incorporate official Government Gazette and relevant regulatory-authority sources, including domain-specific authorities such as SARS where applicable.

The official South African Government portal currently exposes Gazette numbers, Regulation Gazette identifiers, Government Notices, Proclamations and other notice types.

---

# 256. South Africa Source Status Test

The initial test corpus SHOULD deliberately include:

```text
final regulation

draft regulation

general notice

proclamation

customs schedule amendment.
```

Baobab must classify them differently despite originating through official publication infrastructure.

---

# 257. Regional Source Strategy

Initial regional sources SHOULD include where applicable:

```text
AfCFTA

EAC

SACU

SADC

WCO.
```

Each source SHALL receive:

```text
authority mapping

legal-role classification

coverage profile

publication status

rights profile.
```

---

# 258. WCO Test

The initial corpus SHOULD include:

```text
one WCO Convention

one WCO Recommendation.
```

The source model MUST distinguish their legal roles; WCO itself identifies its Recommendations as generally non-binding.

---

# 259. Official versus Non-Binding Golden Case

```text
Source:
WCO

Material:
official Recommendation

Official status:
YES

Legal role:
NON_BINDING_RECOMMENDATION

Result:
may support interpretation /
harmonisation

NOT automatically:
binding domestic obligation.
```

---

# 260. Authentic versus Convenient Golden Case

```text
Authentic publication:
Official Journal

Consolidated text:
easier current reading

Result:

use consolidation for
structured analysis

but retain path to
authentic published acts.
```

This pattern is directly demonstrated by EUR-Lex's own treatment of consolidated texts.

---

# 261. Draft versus Final Golden Case

```text
Official Gazette notice:
"Comments invited"

Status:
DRAFT / CONSULTATION

Result:
change monitoring / future impact

NOT:
current binding rule.
```

---

# 262. Commercial Provider Golden Case

```text
Commercial Provider:
structured tariff API

Authority:
national customs authority

Use:
fast structured evaluation

Requirement:
traceable source provenance

Legal authority:
remains national source.
```

---

# 263. AI Golden Case

```text
AI result:
"Licence required."

Citation:
official regulator guidance only

No underlying binding source located.

Outcome:
candidate interpretation

NOT E4 rule.
```

---

# 264. Tenant Counsel Golden Case

```text
Shared platform interpretation:
I1

Tenant counsel opinion:
I2

Tenant A policy:
uses I2

Outcome:
tenant overlay

not global rule mutation.
```

---

# 265. Broken Signature Golden Case

```text
Official publication

signature verification:
FAILED

Result:
artefact quarantined

alternative verified copy sought

no new E4 reliance.
```

---

# 266. Stale Feed Golden Case

```text
Commercial customs feed:
online and healthy

last regulatory update:
beyond permitted freshness window

Result:
AVAILABLE
but
STALE.
```

---

# 267. Source Rights Golden Case

```text
Commercial source:
authoritative citations
excellent coverage

redistribution:
prohibited

Result:
internal use permitted according to licence

raw provider content
not exposed to customer.
```

---

# 268. Source Registry Production Invariants

| ID | Invariant |
|---|---|
| `REG-S-I01` | Baobab SHALL NOT maintain one universal source trust score |
| `REG-S-I02` | Authority, publisher, provider, source, endpoint, edition and artefact SHALL remain distinguishable |
| `REG-S-I03` | Official status SHALL not imply binding legal force |
| `REG-S-I04` | Binding legal force SHALL not imply current applicability |
| `REG-S-I05` | Authenticity SHALL remain distinct from integrity |
| `REG-S-I06` | Authenticity SHALL remain distinct from currentness |
| `REG-S-I07` | Source currentness SHALL be purpose- and domain-sensitive |
| `REG-S-I08` | Completeness SHALL remain distinct from legal authority |
| `REG-S-I09` | Coverage SHALL state known exclusions where possible |
| `REG-S-I10` | Provider availability SHALL remain distinct from source authority |
| `REG-S-I11` | Source rights SHALL remain distinct from legal authority |
| `REG-S-I12` | Consolidated text SHALL not automatically be classified as legally authentic |
| `REG-S-I13` | Official guidance SHALL not automatically become binding law |
| `REG-S-I14` | Draft/consultation documents SHALL not become current enforceable rules |
| `REG-S-I15` | Secondary commentary SHALL not silently become primary authority |
| `REG-S-I16` | AI-generated content SHALL not be treated as legal authority |
| `REG-S-I17` | Source-use fitness SHALL be assessed for a named purpose |
| `REG-S-I18` | Production rule derivation SHALL retain authoritative source lineage |
| `REG-S-I19` | E3/E4 source requirements SHALL be stricter than discovery/advisory use |
| `REG-S-I20` | Unknown material trust dimensions SHALL remain explicit |
| `REG-S-I21` | Source conflicts SHALL not be resolved through majority voting |
| `REG-S-I22` | Source corrections SHALL remain distinct from legal amendments |
| `REG-S-I23` | Provider corrections SHALL remain distinct from legal amendments |
| `REG-S-I24` | Parser/OCR corrections SHALL remain distinct from legal amendments |
| `REG-S-I25` | Source trust shall be temporally reconstructable |
| `REG-S-I26` | Historical decisions SHALL retain their historical source chain |
| `REG-S-I27` | Source suspension SHALL not erase historical provenance |
| `REG-S-I28` | Tenant-private sources SHALL remain isolated |
| `REG-S-I29` | Privileged counsel material SHALL not be exposed through general graph/search access |
| `REG-S-I30` | Every consequential source assertion SHALL be explainable through provenance and verification evidence |

---

# 269. Rejected Alternative — Universal Trust Score

Rejected because it hides the actual basis of source reliability.

---

# 270. Rejected Alternative — Official Website = Binding Law

Rejected.

Official websites contain materials with many legal roles.

---

# 271. Rejected Alternative — Gazette = In Force

Rejected.

Gazettes can contain:

```text
drafts

consultations

notices

future-effective measures

final measures.
```

---

# 272. Rejected Alternative — Current Consolidated Text = Authentic Source

Rejected as a universal assumption.

The EU itself demonstrates that consolidated text may be convenient and current while not carrying legal effect.

---

# 273. Rejected Alternative — Commercial Source Is Untrustworthy

Rejected.

Commercial sources can be excellent.

Their legal role simply differs from sovereign authority.

---

# 274. Rejected Alternative — Government Source Is Always Complete

Rejected.

An authority may publish only its own domain.

---

# 275. Rejected Alternative — Newest Retrieval Wins

Rejected.

Retrieval time and legal effective time differ.

---

# 276. Rejected Alternative — HTTPS Means Authentic

Rejected.

Transport security is not legal authenticity.

---

# 277. Rejected Alternative — Digital Signature Means Current Law

Rejected.

An authentic signed document may have been repealed.

---

# 278. Rejected Alternative — More Sources Means More Trust

Rejected.

Twenty secondary summaries do not necessarily outweigh one authentic primary source.

---

# 279. Rejected Alternative — AI Citation Means Verified

Rejected.

Citations themselves must resolve and be classified.

---

# 280. Rejected Alternative — Verification Boolean

Rejected.

Baobab must know:

```text
what was verified.
```

---

# 281. Rejected Alternative — Trust Never Expires

Rejected.

Some trust dimensions are temporally volatile.

---

# 282. Rejected Alternative — Provider Status Determines Legal Status

Rejected.

Provider and authority remain distinct.

---

# 283. Rejected Alternative — Source Status Determines Rule Authority Alone

Rejected.

Interpretation, rule verification, applicability and decision policy remain necessary.

---

# 284. Minimum Implementation Proof

Before `ADR-REG-0011` is considered implemented, Baobab SHOULD demonstrate:

```text
1.
Registry of an official Gazette.

2.
Separate Authority / Publisher /
Provider / Source / Endpoint identities.

3.
One source with several endpoints.

4.
One source edition with several artefacts.

5.
Cryptographic content hashing.

6.
Official-status verification.

7.
Legal-force classification.

8.
Authenticity classification.

9.
Currentness classification.

10.
Coverage profile.

11.
Known exclusions.

12.
Rights status.

13.
Purpose-specific trust assessment.

14.
Discovery-approved source
that is not E4-approved.

15.
Official non-binding source.

16.
Official draft publication.

17.
Official authentic binding publication.

18.
Official but non-authentic consolidation.

19.
Commercial structured provider.

20.
Professional commentary.

21.
Tenant counsel opinion.

22.
AI-generated candidate source.

23.
Source conflict.

24.
Source correction.

25.
Provider correction.

26.
Parser correction.

27.
Suspended source.

28.
Retired source retained historically.

29.
Stale but available source.

30.
Unavailable but historically valid source.

31.
Source dependency blast-radius traversal.

32.
Cross-tenant source isolation.

33.
Restricted source-content filtering.

34.
Historical SourceTrustAssessment replay.

35.
A decision proving its full source chain.
```

---

# 285. Production Gate — Source Registry

No source SHALL support consequential production rule derivation until, at minimum:

```text
canonical source identity exists

authority identity is established

publisher/provider relationships known

jurisdiction/domain coverage declared

legal publication role classified

authenticity state recorded

currentness policy configured

provenance chain preserved

rights reviewed

source-use policy evaluated

operational ownership assigned.
```

---

# 286. E4 Additional Gate

For E4 support, the relevant source chain SHOULD additionally demonstrate:

```text
appropriate authoritative source

verified legal force

effective-date certainty

sufficient completeness

acceptable coverage

strong provenance

rule lineage

interpretation verification

no unresolved material source conflict.
```

---

# 287. Source Registry Event Model

Potential events:

```text
regulation.source.registered

regulation.source.approved

regulation.source.verified

regulation.source.degraded

regulation.source.suspended

regulation.source.retired

regulation.source.coverage.changed

regulation.source.trust.changed

regulation.source.rights.changed

regulation.source.authenticity.failed.
```

Exact contracts belong in Shared.

---

# 288. Source Status Change Impact

A consequential source status change SHOULD trigger:

```text
dependency traversal
        │
        ▼
affected rules
        │
        ▼
affected profiles
        │
        ▼
affected decisions.
```

---

# 289. Rule Reassessment

Not every source change requires customer reassessment.

The graph identifies candidate impact.

The Regulations evaluation layer determines actual impact.

---

# 290. Source Registry Observability

Metrics SHOULD include:

```text
active_sources

verified_sources

unverified_authority_sources

stale_sources

degraded_sources

suspended_sources

sources_with_unknown_rights

sources_with_incomplete_coverage

source_verification_backlog

E4_rules_with_source_gaps.
```

---

# 291. Alerting

High-severity alerts SHOULD include:

```text
authenticity failure

critical source stale

critical source disappeared

rights expired

signature invalid

unexpected source correction

official endpoint changed.
```

---

# 292. Source Registry and ADR-REG-0012

`ADR-REG-0012` SHALL deepen:

```text
licensing

commercial reuse

copying

transformation

derived-data rights

redistribution

retention

AI-training rights

termination / exit rights.
```

The Registry SHALL hold the resulting rights profile.

---

# 293. Source Registry and ADR-REG-0013

`ADR-REG-0013` SHALL deepen:

```text
connectors

adapters

ingestion

snapshots

normalisation

schema drift

quarantine

parsing.
```

The Registry tells those pipelines **what source they are processing and under what governance**.

---

# 294. Source Registry and ADR-REG-0014

`ADR-REG-0014` SHALL formalise the evidentiary chain:

```text
Authority
→ Source
→ Edition
→ Artefact
→ Provision
→ Interpretation
→ Rule
→ Assessment
→ Decision.
```

---

# 295. Source Registry and ADR-REG-0015

`ADR-REG-0015` SHALL make source state bitemporal:

```text
when was source legally valid?

when did Baobab know it?

when was it verified?

when was it superseded?
```

---

# 296. Source Registry and ADR-REG-0021

AI-assisted interpretation SHALL consume explicit source trust metadata.

The AI SHALL be able to distinguish:

```text
authentic law

guidance

commercial summary

counsel opinion

machine-generated text.
```

---

# 297. AI Prompt Context

A regulatory AI prompt SHOULD never present:

```text
official regulation

blog post
```

as equivalent anonymous chunks.

Source status SHALL accompany retrieval.

---

# 298. Retrieval Ranking

Search relevance MAY rank:

```text
semantic similarity.
```

Regulatory retrieval SHOULD additionally consider:

```text
authority

legal status

effective time

jurisdiction

source trust profile.
```

---

# 299. Relevance Is Not Authority

A blog may be the most semantically relevant search result.

The system SHALL still identify it as commentary.

---

# 300. Strategic Differentiation

This source model becomes an important differentiator because most AI regulatory experiences risk collapsing:

```text
search result
→ answer.
```

Baobab instead operates:

```text
Source Discovery
       │
       ▼
Authority Resolution
       │
       ▼
Authenticity
       │
       ▼
Legal Status
       │
       ▼
Temporal Validity
       │
       ▼
Coverage
       │
       ▼
Interpretation
       │
       ▼
Rule
       │
       ▼
Decision.
```

---

# 301. Trustworthy AI Foundation

The OECD's current Law-as-Code framing emphasises that machine representations must remain explicitly linked to authoritative legal text and preserve interpretation, discretion and institutional responsibility.

ADR-REG-0011 provides Baobab with the source architecture needed to honour that principle.

---

# 302. Regulatory Evidence Advantage

Over time Baobab will know not only:

```text
what the regulation says
```

but:

```text
which publication said it

whether that publication was authentic

whether it was in force

which version was used

what Baobab transformed

which interpretation was approved

which decision depended on it.
```

That is a much stronger enterprise trust proposition.

---

# 303. Competitive Moat

Competitors can acquire the same PDF.

The harder system to reproduce is:

```text
PDF
+
source identity
+
authority identity
+
legal status
+
authenticity
+
effective time
+
coverage
+
provenance
+
rule lineage
+
operational history.
```

---

# 304. Source Trust Flywheel

```text
Source discovered
      │
      ▼
Source verified
      │
      ▼
Source structured
      │
      ▼
Rules derived
      │
      ▼
Transactions assessed
      │
      ▼
Outcomes observed
      │
      ▼
Source / rule quality reviewed
      │
      ▼
Better source assurance.
```

---

# 305. Profitability Implication

A governed source registry also enables Baobab to combine:

```text
free public sources

commercial content

customer-owned subscriptions

Baobab-derived structure
```

without binding the platform's commercial model to any single regulatory-data vendor.

That is essential for maintaining gross margins as jurisdictional coverage expands.

---

# 306. Source Procurement Intelligence

Baobab can eventually answer:

```text
Which paid source creates unique value?

Which commercial source duplicates free official data?

Where do we lack official verification?

Which source costs support which customers?

Which provider can be replaced?
```

This supports strategic procurement.

---

# 307. Must-Have Product Behaviour

A customer should ultimately see something like:

```text
Requirement:
Import permit required

Authority:
South African competent authority

Legal source:
Official Government Gazette

Source status:
Official publication

Rule status:
Verified

Effective:
From 1 July 2027

Evidence:
Permit missing

Decision:
Action required before import.
```

Not merely:

```text
AI says permit probably needed.
```

---

# 308. Research Foundation Summary

Uganda's official publisher explicitly describes the Uganda Gazette as the official Government publication for important government communications, statutes, statutory instruments and legal notices, providing a concrete example of authoritative national publication infrastructure.

South Africa's official Government Gazette portal demonstrates that one official publication infrastructure may carry materials with very different legal status, including amendments, final regulations, proclamations and draft measures for public comment.

The EU's electronic Official Journal demonstrates a mature legal and technical authenticity model in which the legally authentic electronic edition is distinguished from other representations, while consolidated texts may be useful but carry no independent legal effect.

The WCO demonstrates the distinction between official institutional provenance and binding legal effect: its Recommendations are official WCO instruments but are generally non-binding.

W3C PROV provides an established provenance model specifically intended to describe entities, activities and agents involved in producing information and to support assessments of quality, reliability and trustworthiness.

The OECD's current Law-as-Code initiative reinforces the requirement to keep machine representations explicitly linked to authoritative legal texts and not to replace institutional authority or legal interpretation with opaque software transformations.

---

# 309. Final Decision

Baobab Regulations SHALL establish a governed **Authoritative Source Registry** in which regulatory source trust is represented as a multidimensional, purpose-specific and temporal profile.

The canonical model is:

```text
                    REGULATORY AUTHORITY
                            │
                            ▼
                    OFFICIAL PUBLISHER
                            │
                            ▼
                    REGULATORY SOURCE
                            │
                  ┌─────────┴──────────┐
                  ▼                    ▼
              ENDPOINT             EDITION
                                      │
                                      ▼
                               SOURCE ARTEFACT
                                      │
                                      ▼
                               AUTHENTICITY
                                      │
                                      ▼
                                 INTEGRITY
                                      │
                                      ▼
                                  LEGAL ROLE
                                      │
                                      ▼
                                 CURRENTNESS
                                      │
                                      ▼
                                 COMPLETENESS
                                      │
                                      ▼
                                   COVERAGE
                                      │
                                      ▼
                                 PROVENANCE
                                      │
                                      ▼
                               RIGHTS / LICENCE
                                      │
                                      ▼
                            FITNESS FOR PURPOSE
```

The Registry SHALL be capable of saying:

```text
This source is official
but non-binding.

This source is binding
but this copy is not yet authenticated.

This source is authentic
but superseded.

This source is current
but only a summary.

This source is complete
but licensed for internal use only.

This commercial feed is excellent
for change detection
but insufficient alone for E4.

This counsel opinion is authoritative
for Tenant A's approved interpretation
but is not public law.

This AI extraction is accurate enough
to propose a rule
but remains unverified.
```

That precision is the decision.

The governing doctrine is:

> **Trust is not a number. Trust is an explainable set of claims about authority, authenticity, legal status, currency, completeness, provenance and fitness for a particular regulatory purpose.**

And the operational doctrine is:

> **Baobab SHALL always know why it trusted the source that supported a consequential regulatory decision.**

That is what `ADR-REG-0011` establishes.

---

## Decision Summary

```text
ADR-REG-0011
──────────────────────────────────────────

CORE DECISION

Create a governed Authoritative
Regulatory Source Registry.


DO NOT USE

source.trust_score = 94


TRUST DIMENSIONS

Authority identity
Official status
Legal force
Authenticity
Integrity
Currentness
Completeness
Coverage
Provenance
Transformation distance
Interpretive status
Verification
Rights
Availability
Fitness for purpose


CORE SEPARATIONS

Official ≠ Binding

Binding ≠ In force

Authentic ≠ Current

Complete ≠ Authoritative

Available ≠ Trustworthy

Commercial ≠ Untrustworthy

Consolidated ≠ Authentic

AI-derived ≠ Legal authority


SOURCE CHAIN

Authority
   ↓
Publisher
   ↓
Source
   ↓
Edition
   ↓
Artefact
   ↓
Acquisition
   ↓
Canonical knowledge


PURPOSE-SPECIFIC TRUST

Discovery
Change detection
Interpretation
Rule derivation
Advisory assessment
Review gate
Automated enforcement
Historical reconstruction

may require different
source standards.


E4 PRINCIPLE

Consequential automated decisions
require a defensible authoritative
source chain.


FAILURE PRINCIPLE

Unknown
does not become trusted.

Conflicting sources
do not become majority vote.


TENANCY

Public authoritative sources:
shared where permissible.

Tenant counsel / private evidence:
isolated overlays.


STRATEGIC RESULT

Every regulatory decision can answer:

Which source?

Which authority?

Was it authentic?

Was it in force?

Was it complete?

How was it transformed?

Why was it fit for this purpose?
```
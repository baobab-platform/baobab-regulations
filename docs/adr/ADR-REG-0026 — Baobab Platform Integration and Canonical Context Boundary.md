# ADR-REG-0026 — Baobab Platform Integration and Canonical Context Boundary

**Subtitle:** Control Plane Context Resolution, Canonical Identity, Capability Binding, Cross-Engine Facts, Regulatory Context Enrichment and Platform Authority Separation

**Status:** Proposed — Foundational Platform Integration Architecture  
**Decision ID:** `ADR-REG-0026`  
**Engine:** Baobab Regulations  
**Target Repository:** `baobab-platform/baobab-regulations`  
**Cross-Repository Contract Targets:** `baobab-platform/shared`, `baobab-platform/baobab-cp`, `baobab-platform/baobab-trade-docs`, `baobab-platform/baobab-trade`  
**Date:** 2026-09-29  
**Amended:** 2026-10-05 — RTD-03, under accepted `ADR-SHARED-019` and aligned with `ADR-PULSE-012`, `ADR-TDOC-0001` and `ADR-TDOC-0002`  
**Platform Boundary Authority:** `ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary`  
**Decision Type:** Platform Integration / Context / Identity / Capability Resolution / Cross-Engine Contracts / Authority Boundaries  
**Strategic Classification:** Core Baobab Platform Architecture

---

# 1. Executive Decision

Baobab Regulations SHALL operate as a **provider-neutral Baobab capability engine behind the Baobab Control Plane**.

It SHALL NOT redefine or become authoritative for:

```text id="1w3frd"
Tenant

Organisation

CorporateGroup

PlatformAccount

LegalEntity

Market

MarketParticipation

TradeLane

DigitalEstate

Capability

CapabilityGrant

CapabilityBinding

Provider

Engine

EngineInstance

IsolationProfile

ResidencyRequirement

platform administrative authority

platform identity.
```

Those remain under their established Baobab platform authorities.

Baobab Regulations SHALL instead own:

```text id="bz12xj"
RegulatorySource

RegulatoryAuthority semantics

RegulatoryRegime

Instrument

Provision

Interpretation

RuleVersion

Obligation

Permission

Prohibition

Exception

RegulatoryRequirement

RegulatoryEvidenceAssessment

RegulatoryContext

Applicability

RegulatoryAssessment

RegulatoryDecision

RegulatoryChange

RegulatoryImpact

JurisdictionPack

regulatory assurance

regulatory execution semantics.
```

The primary integration relationship SHALL be:

```text id="z68xbx"
        BAOBAB CONTROL PLANE
     platform context + topology
              + authority
                  │
                  ▼
          PlatformContext
     CapabilityResolution
                  │
                  ▼
        BAOBAB REGULATIONS
             enriches
                  │
                  ▼
          RegulatoryContext
                  │
                  ▼
        Regulatory Evaluation
                  │
                  ▼
        RegulatoryDecision
                  │
         ┌────────┴─────────┐
         │                  │
         ▼                  ▼
  Baobab Trade Docs       Trade / TMS / ERP
  document/customs PEP    operational PEPs
         │                  │
         └────────┬─────────┘
                  ▼
       governed operational action
```

The governing principle is:

> **Control Plane tells Regulations who, where and under which platform scope a request operates. Domain engines tell Regulations what happened. Regulations determines what regulatory meaning follows.**

---


# 1A. RTD-03 Normative Amendment — Trade Docs Boundary

This section is a **normative amendment** to this ADR.

It exists because ADR-REG-0026 was written before Baobab Trade Docs became an explicit engine. The original ADR correctly separated Regulations from Control Plane, IAM, Trade, ERP, Pulse and CMS, but documentary and Customs-workflow responsibilities were still described through Trade, ERP or generic evidence terminology.

Accepted ADR-SHARED-019 now governs the platform-level boundary.

Where any earlier section of ADR-REG-0026 can reasonably be read as assigning to Regulations ownership of a concrete trade document, a document version, a Customs workflow aggregate, a declaration submission lifecycle or an authority-response record, this amendment controls.

The precedence is:

~~~text
ADR-SHARED-019
      │
      ▼
ADR-REG-0026 RTD-03 amendment
      │
      ├── aligns with ADR-TDOC-0001 / ADR-TDOC-0002
      ├── aligns with ADR-PULSE-012
      └── refines earlier ADR-REG-0026 wording
~~~

The core rule is:

> **Regulations determines regulatory meaning and requirement satisfaction. Trade Docs owns executable trade-document and Customs-workflow state. Operational engines enforce the resulting decision in the business state they own.**

---

# 1B. Four Authorities Must Remain Distinct

The platform SHALL distinguish four authority classes.

| Authority class | Canonical owner | Typical questions |
|---|---|---|
| Platform context authority | Control Plane | Who is the tenant, legal entity, market participant, trade lane and capability provider? |
| Regulatory meaning authority | Baobab Regulations | What applies? What is required? Is the requirement satisfied? What regulatory decision follows? |
| Documentary / Customs-workflow authority | Baobab Trade Docs | Which document exists? Which version? What was submitted? What authority response was received? |
| Operational state authority | Trade, TMS, ERP or another PEP | What shipment/order/payment/accounting transition is actually performed? |

External competent authorities remain authoritative for their own sovereign acts.

Therefore:

~~~text
Regulations record of a Customs release requirement
        !=
Customs authority release

Trade Docs record of a Customs authority response
        !=
Trade Docs becoming Customs authority

Trade enforcement of HOLD
        !=
Trade becoming regulatory decision authority
~~~

---

# 1C. Requirement, Document, Verification and Satisfaction Are Different Objects

The following distinctions are hard invariants.

~~~text
DocumentRequirement
        !=
TradeDocument

TradeDocument
        !=
DocumentVersion

DocumentVerification
        !=
RequirementSatisfaction

RequirementSatisfaction
        !=
OperationalEnforcement
~~~

Baobab Regulations owns:

~~~text
DocumentRequirement
PermitRequirement
EvidenceRequirement
ValidityCriteria
AcceptableIssuerCriteria
SignatureRequirement
TimingRequirement
Applicability
RequirementSatisfaction
RegulatoryEvidenceAssessment
RegulatoryDecision
~~~

Baobab Trade Docs owns:

~~~text
TradeDocument
DocumentVersion
DocumentContent
ContentArtifact
DocumentRelationship
issuer claim
document verification state
DocumentDossier
CustomsCase
CustomsDeclaration workflow
Submission
AuthorityResponse
document/customs workflow state
~~~

The competent external authority or issuer owns the underlying external legal act.

---

# 1D. Regulatory Requirement Is a Normative Proposition

A Regulations object such as:

~~~text
DocumentRequirement R-17
    type/purpose = PHYTOSANITARY_CERTIFICATE
    applies_to = consignment C
    acceptable_issuer = competent NPPO
    validity = valid at export/import event
    conditions = commodity/origin/destination-specific
    legal_basis = ...
~~~

states a normative proposition.

It does **not** mean that a document instance exists.

A Trade Docs object such as:

~~~text
TradeDocument TD-88
DocumentVersion TDV-4
issuer_claim = Uganda NPPO
subject = consignment C
issued_at = ...
verification_state = VERIFIED
~~~

states documentary facts.

It does **not** itself mean R-17 is legally satisfied.

Regulations must evaluate:

~~~text
R-17
   +
TDV-4 documentary facts
   +
current regulatory context
   +
legal time
   ↓
RequirementSatisfaction
~~~

---

# 1E. Two-Stage Document-Dependent Evaluation

Document-dependent regulation SHALL support two conceptually separate evaluation stages.

## Stage A — requirement determination

Regulations may determine what is required before the required document exists.

~~~mermaid
flowchart LR
    C[Regulatory Context] --> R[Regulations]
    R --> DR[DocumentRequirement]
    R --> PR[PermitRequirement]
    R --> ER[EvidenceRequirement]
~~~

This supports pre-flight planning.

## Stage B — satisfaction determination

After Trade Docs has acquired, generated, verified, versioned or submitted the relevant documentary object, Regulations evaluates whether the normative requirement is satisfied.

~~~mermaid
flowchart LR
    REQ[Regulations Requirement] --> EVAL[Regulations Satisfaction Evaluation]
    TDV[Trade Docs DocumentVersion] --> EVAL
    VER[Trade Docs Verification Facts] --> EVAL
    CTX[Current Regulatory Context] --> EVAL
    EVAL --> SAT[SATISFIED]
    EVAL --> UNSAT[UNSATISFIED]
    EVAL --> IND[INDETERMINATE]
~~~

Stage A and Stage B SHALL not be collapsed into one mutable document status.

---

# 1F. Trade Docs Boundary

Baobab Trade Docs is now an explicit platform engine and SHALL be treated as the canonical Baobab owner of executable trade-document and Customs-workflow state.

Its boundary includes, subject to its own ADR canon:

~~~text
TradeDocument identity
DocumentVersion
DocumentContent / rendition
document dossier
document relationships
issuer claim
document verification workflow
submission state
CustomsCase
CustomsDeclaration workflow
authority messages / responses
external authority references
document/customs provenance
~~~

Regulations SHALL NOT create shadow aggregates with the same semantics.

Prohibited by default:

~~~text
regulations.trade_documents
regulations.document_versions
regulations.customs_cases
regulations.customs_submissions
regulations.authority_responses
~~~

A Regulations evaluation snapshot may contain a bounded immutable representation of facts used for a decision. That snapshot remains decision evidence, not the current documentary master.

---

# 1G. Regulatory Source Documents Are Not Trade Documents

Regulations continues to own its regulatory source-acquisition objects.

A gazette, statute, tariff schedule, regulatory circular or official guidance acquired as a **source of law/regulatory meaning** remains inside the Regulations source/provenance architecture.

A commercial invoice, certificate of origin, phytosanitary certificate, import permit, bill of lading or Customs declaration used in an operational trade workflow belongs to the Trade Docs documentary boundary.

The same physical bytes can theoretically be relevant to more than one domain, but:

~~~text
same bytes
    !=
same aggregate
    !=
same purpose
    !=
same authority
~~~

The engine boundary follows semantic purpose and authority, not MIME type.

---

# 1H. Regulatory Evidence Assessment Uses Documentary Facts by Reference

Regulations may assess documentary evidence.

It SHALL normally do so through references to the Trade Docs canonical object and the exact version used.

Conceptually:

~~~text
RegulatoryEvidenceAssessment
├── requirement_ref
├── subject_ref
├── trade_document_ref
├── document_version_ref
├── verification_fact_refs[]
├── evaluated_at
├── legal_time
├── knowledge_time
├── criteria_version
├── result
├── reasons[]
└── provenance
~~~

The exact cross-engine reference shape is owned by Shared and remains a follow-up under RTD-05.

Until that contract exists, implementations SHALL avoid inventing a permanent incompatible local substitute.

---

# 1I. Documentary Verification Is Not Regulatory Sufficiency

Trade Docs verification MAY establish documentary properties such as:

~~~text
content integrity
issuer identity
signature validity
issuer credential validity
revocation state
expiry
subject association
data consistency
submission receipt
authority-response authenticity
~~~

Regulations evaluates regulatory sufficiency such as:

~~~text
is this issuer legally acceptable for requirement R?
is this version valid at the legally relevant time?
does this document cover the correct commodity?
does it cover this consignment?
does it satisfy destination-specific conditions?
does the evidence prove origin for the claimed preference?
does the permit satisfy the applicable regime?
~~~

Therefore:

~~~text
Trade Docs VERIFIED
        !=
Regulations SATISFIED
~~~

and:

~~~text
Trade Docs NOT_VERIFIED
        !=
Regulations automatically PROHIBITED
~~~

The latter may instead produce INDETERMINATE, UNSATISFIED, REVIEW_REQUIRED or another governed outcome depending on the rule.

---

# 1J. Permit and Licence Boundary

The platform SHALL distinguish:

~~~text
permit/licence requirement
        → Regulations

external permit/licence legal act
        → competent authority

TradeDocument representation of permit/licence
        → Trade Docs

regulatory standing / applicability / satisfaction
        → Regulations
~~~

An exporter-level regulatory licence may also produce reusable regulatory standing in Regulations.

Its issued certificate/documentary representation may still be held by Trade Docs.

The two objects SHALL reference one another where needed rather than being collapsed.

---

# 1K. Customs Decomposition

“Customs” is not one bounded context.

The fact type determines authority.

| Customs concern | Authority |
|---|---|
| Applicable classification, tariff rule, origin rule, prohibition, requirement | Regulations |
| Customs declaration workflow | Trade Docs |
| Declaration document/version | Trade Docs |
| Submission to Customs | Trade Docs |
| Authority acknowledgement/rejection/release message record | Trade Docs |
| Sovereign assessment/release/ruling | External Customs authority |
| Shipment/order operational hold/release | Trade/TMS or another operational PEP |
| Financial posting of duty/VAT | ERP/Ledger |
| Strategic analysis of Customs delays/cost | Pulse |

This ADR therefore amends any earlier shorthand suggesting “Trade owns Customs” or “Regulations owns Customs” without qualification.

---

# 1L. Customs Declaration Has Regulatory and Documentary Aspects

Regulations may determine:

~~~text
a declaration is required
which data/propositions are legally required
classification/origin/valuation rules
timing requirements
supporting evidence requirements
regulatory consequence of defects
~~~

Trade Docs owns:

~~~text
CustomsDeclaration workflow aggregate
draft / version
supporting-document bundle
submission
submission correlation
authority acknowledgement
rejection/error response
amendment/re-submission
authority status projection
~~~

A CustomsDeclaration MAY also have a TradeDocument representation.

The sovereign Customs administration remains authoritative for external acceptance, assessment and release.

---

# 1M. RegulatoryFactBundle Is Extended by Documentary References

The existing RegulatoryFactBundle concept remains valid.

For documentary evaluation, it MAY include typed facts/references such as:

~~~text
DocumentVersionReference
DocumentType
IssuerClaim
IssuerVerificationStatus
IssuedAt
ExpiresAt
SubjectAssociation
ConsignmentAssociation
SubmissionReference
AuthorityResponseReference
RevocationState
~~~

The bundle SHALL NOT contain an unbounded copy of a TradeDocument or CustomsCase aggregate.

The source owner, source object and version SHALL remain explicit.

---

# 1N. Cross-Engine Reference Semantics

ADR-SHARED-019 distinguishes:

~~~text
ExternalReference
    = native external-system identity

CrossEngineObjectReference
    = canonical Baobab object owned by another engine
~~~

Regulations SHALL follow that distinction.

A Trade Docs document version reference is not an ADR-SHARED-013 ExternalReference merely because it is “external” to Regulations.

Likewise, a Customs authority native reference MAY be represented through the platform's external-system identity mechanisms where appropriate, while the Trade Docs canonical AuthorityResponse remains a Baobab object.

---

# 1O. Document-Dependent Runtime Topology

The target synchronous choreography is:

~~~mermaid
sequenceDiagram
    participant DE as Digital Estate / Trade / TMS
    participant CP as Control Plane
    participant R as Regulations
    participant D as Trade Docs
    participant PEP as Operational PEP

    DE->>CP: resolve trusted context + capabilities
    CP-->>DE: PlatformContext + provider bindings

    DE->>R: initial regulatory assessment
    R-->>DE: RegulatoryDecision + DocumentRequirements

    DE->>D: obtain/create/associate required documents
    D->>D: version + verify + manage workflow
    D-->>R: documentary facts / references

    R->>R: evaluate requirement satisfaction
    R-->>DE: refreshed RegulatoryDecision

    DE->>PEP: enforce authorised disposition
~~~

Direct engine-to-engine calls may replace DE-mediated calls where architecture and authorisation permit, but authority ownership SHALL remain the same.

---

# 1P. Event Directionality

Cross-engine events state facts; they do not disguise commands.

## Regulations → Trade Docs

Examples of facts that MAY be emitted after Shared contract governance:

~~~text
regulatory decision issued
document requirement determined
document requirement changed
classification assigned
requirement satisfaction invalidated
decision superseded
~~~

## Trade Docs → Regulations

Examples:

~~~text
document version issued
document superseded
verification state changed
document expired
document revoked
submission completed
authority response received
Customs case materially changed
~~~

A Trade Docs event SHALL NOT assert canonical legal requirement satisfaction.

A Regulations event SHALL NOT pretend a TradeDocument instance was created.

Commands such as “create certificate workflow” or “submit declaration” belong to capability/API/command boundaries, not fact events.

---

# 1Q. Decision Reuse and Staleness

A prior RegulatoryDecision SHALL be reconsidered when material documentary context changes.

Examples include:

~~~text
DocumentVersion superseded
document expired
issuer verification revoked
permit revoked
authority response changed
consignment association changed
classification changed
route changed
legal time crossed effective boundary
requirement changed
~~~

Trade Docs SHALL not infer that a previously referenced RegulatoryDecision remains current merely because its identifier still resolves.

Regulations owns decision validity.

Consumers own whether they are permitted to use a cached decision.

---

# 1R. Historical Replay

For every consequential document-dependent decision, Regulations SHOULD preserve enough immutable evidence to answer:

> Which exact document version and verification state did the decision use?

A replay manifest SHOULD be able to resolve:

~~~text
RegulatoryDecision D
├── RegulatoryContext snapshot
├── RuleSet / BRIR fingerprint
├── Requirement versions
├── TradeDocument refs
├── DocumentVersion refs
├── verification fact refs
├── authority-response refs
├── legal_time
├── knowledge_time
└── evaluation provenance
~~~

A later document update SHALL NOT rewrite D's historical evidence.

---

# 1S. Failure Semantics

The following SHALL remain distinct:

~~~text
Trade Docs unavailable
        !=
document missing

document missing
        !=
document invalid

document invalid
        !=
requirement unsatisfied in every possible rule

Regulations unavailable
        !=
transaction prohibited

Customs authority has not responded
        !=
Customs rejected

authority response ambiguous
        !=
release granted
~~~

High-consequence operations SHALL fail safely according to the governing policy.

Unknown and indeterminate remain valid states.

---

# 1T. Security and Content Minimisation

Cross-engine documentary events SHOULD contain the minimum facts necessary for consumers.

Sensitive document content SHOULD remain behind the Trade Docs authorisation boundary.

A Regulations decision may cite a TradeDocumentVersion without exposing the underlying document bytes.

Knowledge of a document identifier SHALL NOT grant permission to retrieve its content.

Classification, tenant scope, source rights and purpose restrictions SHALL propagate across references.

---

# 1U. Corrected ZuriBeans Uganda → South Africa Flow

The earlier ZuriBeans example is retained as a platform-context example but is amended for document-dependent evaluation.

~~~mermaid
flowchart TD
    IAM[IAM authenticates principal] --> CP[Control Plane resolves PlatformContext + capabilities]
    CP --> T[Trade supplies shipment/commercial facts]
    T --> R1[Regulations determines applicable rules and requirements]
    R1 --> REQ[Document / permit / evidence requirements]

    REQ --> TD[Trade Docs obtains or associates document instances]
    TD --> V[Version + provenance + documentary verification]
    V --> R2[Regulations evaluates requirement satisfaction]

    R2 --> DEC[RegulatoryDecision]
    DEC --> PEP[Trade / TMS / ERP PEP]
    PEP --> ACT[Operational action]

    DEC --> P[Pulse may analyse decision asynchronously]
    TD --> P
~~~

Example phytosanitary case:

~~~text
Regulations:
PHYTOSANITARY_CERTIFICATE_REQUIRED
        ↓
Trade Docs:
TD-phyto / version 3
issuer verified
consignment = S
not expired
        ↓
Regulations:
Does version 3 satisfy the applicable SPS requirement?
        ↓
SATISFIED / UNSATISFIED / INDETERMINATE
        ↓
Trade:
maps disposition into shipment workflow
~~~

---

# 1V. Existing Section Reconciliation

The following interpretation is normative.

| Existing ADR-REG-0026 area | RTD-03 interpretation |
|---|---|
| §§63–68 Trade Boundary | Trade remains commerce/trade operational owner and PEP; documentary/Customs workflow moves to Trade Docs |
| §66 Regulatory Snapshot | Snapshot may include Trade Docs refs/versions but is not the document master |
| §§76–83 Mapping | Cross-engine canonical refs SHALL not be confused with ExternalReference |
| §§91–99 RegulatoryFactBundle | May carry bounded Trade Docs facts/references; never a whole document aggregate |
| §§102–110 Pulse | Retained; ADR-PULSE-012 now provides detailed reconciliation |
| §§158–163 Runtime Interaction | Add Regulations ↔ Trade Docs choreography for document-dependent decisions |
| §§169–175 API References | Future Shared CrossEngineObjectReference governs Baobab-owned foreign objects |
| §§183–191 Event Integration | Add Trade Docs material document/workflow events as reassessment triggers |
| §§196–207 ZuriBeans Example | Amended by §1U above |
| §§228–240 Freshness / cache | Document-version and verification changes are material invalidation inputs |
| §253 Invariants | Extended by RTD-03 invariants below |
| §§268–272 rejected alternatives | Also reject Regulations owning TradeDocument/CustomsCase and cross-engine DB access |
| §§285–291 implementation proof | Must prove Trade Docs references and requirement-satisfaction choreography |

---

# 1W. RTD-03 Platform Integration Invariants

| ID | Invariant |
|---|---|
| REG-RTD-I01 | DocumentRequirement SHALL remain distinct from TradeDocument |
| REG-RTD-I02 | TradeDocument SHALL remain distinct from DocumentVersion |
| REG-RTD-I03 | Trade Docs documentary verification SHALL not equal Regulations requirement satisfaction |
| REG-RTD-I04 | Regulations SHALL not own a competing TradeDocument aggregate |
| REG-RTD-I05 | Regulations SHALL not own a competing CustomsCase or Customs submission aggregate |
| REG-RTD-I06 | Trade Docs SHALL not contain jurisdiction-specific regulatory requirement logic except governed Regulations decisions or explicit authority protocol constraints |
| REG-RTD-I07 | Trade Docs facts SHALL enter consequential Regulations decisions by versioned reference/snapshot |
| REG-RTD-I08 | A document version change MAY invalidate a previous RegulatoryDecision |
| REG-RTD-I09 | A regulatory requirement change SHALL not silently mutate historical TradeDocument versions |
| REG-RTD-I10 | Customs authority responses SHALL preserve the external authority as sovereign source |
| REG-RTD-I11 | Regulations SHALL determine requirement satisfaction |
| REG-RTD-I12 | Trade/TMS/ERP or another owning engine SHALL perform business-state enforcement |
| REG-RTD-I13 | Cross-engine Baobab references SHALL not misuse ExternalReference |
| REG-RTD-I14 | Documentary content access SHALL remain separately authorised from reference access |
| REG-RTD-I15 | Historical replay SHALL identify the exact document versions used |
| REG-RTD-I16 | Regulations unavailability SHALL not be represented as legal prohibition |
| REG-RTD-I17 | Trade Docs unavailability SHALL not be represented as document absence |
| REG-RTD-I18 | Pulse SHALL remain asynchronous to the regulatory/documentary critical path by default |
| REG-RTD-I19 | Events SHALL state facts; cross-engine work requests SHALL use governed command/API/capability boundaries |
| REG-RTD-I20 | No direct database access SHALL exist between Regulations and Trade Docs |

---

# 1X. Implementation Consequences

RTD-03 does not require immediate runtime coupling.

It establishes the target boundary so later contract work can proceed safely.

The dependency order is:

~~~text
RTD-03
  Regulations ADR reconciliation
        ↓
RTD-04
  Shared TradeDocument contract reconciliation
        ↓
RTD-05
  canonical cross-engine reference contract
        ↓
RTD-06
  Regulations ↔ Trade Docs APIs/events
        ↓
RTD-07 / RTD-08
  event-context activation
        ↓
runtime adapters + conformance tests
~~~

Until RTD-04 through RTD-06 land:

1. Regulations SHALL not invent permanent Trade Docs wire schemas.
2. Trade Docs SHALL not invent regulatory decision semantics.
3. Repository-local prototypes MAY exist only behind ports/adapters and SHALL not be promoted as canonical Shared contracts.
4. The accepted Shared architecture remains the integration source of truth.

---

# 2. Architectural Foundation

The Baobab platform architecture already adopts:

> **Standardise the contracts, not the implementations.**

The platform is intentionally composed of specialised engines behind common identity, tenancy, API, event, audit and integration contracts rather than one monolithic backend.

`baobab-regulations` SHALL follow that architecture without exception.

---

# 3. Desired State Must Remain Provider-Neutral

Current Control Plane onboarding architecture deliberately separates:

```text id="qhjrrq"
Desired State

Provisioning Plan

Execution Operation

Readiness
```

and keeps provider/engine topology out of the tenant's desired-state declaration.

The current desired-state model describes needs such as:

```text id="vbueks"
tenant

legal entities

products / profiles

market participation

digital estates

isolation requirement

residency requirement
```

while explicitly excluding:

```text id="s0b5eo"
engine

engine instance

provider

capability grant

binding.
```



Baobab Regulations SHALL preserve this separation.

---

# 4. A Customer Does Not Request OPA or `baobab-regulations`

Incorrect desired state:

```text id="fd2fwx"
provider = baobab-regulations

engine = regulations

runtime = OPA

instance = reg-af-south-1.
```

Correct desired state:

```text id="pd6y43"
Tenant T needs:

cross-border regulatory assessment

for approved market participation

under required isolation

and residency constraints.
```

Control Plane derives:

```text id="sqrv8l"
Capability

Grant

Provider

CapabilityBinding

Engine

EngineInstance.
```

---

# 5. Platform Capability, Not Product Topology

Potential canonical capabilities include:

```text id="dxdndr"
REGULATORY_RULE_QUERY

REGULATORY_APPLICABILITY

REGULATORY_ASSESSMENT

REGULATORY_DECISION

REGULATORY_EXPLANATION

REGULATORY_CHANGE_INTELLIGENCE

REGULATORY_REASSESSMENT

REGULATORY_SOURCE_ADMINISTRATION

REGULATORY_KNOWLEDGE_GOVERNANCE.
```

Exact keys SHALL be established through Shared/Control Plane governance.

---

# 6. Regulations SHALL NOT Self-Entitle

Rejected:

```text id="1tjzxi"
if tenant exists:
    enable regulatory capability.
```

Capability entitlement belongs to Control Plane.

---

# 7. Regulations SHALL NOT Select Itself

Rejected:

```text id="y1mmwo"
provider = "baobab-regulations"
```

inside leaf application logic.

Provider resolution belongs to Control Plane.

---

# 8. Provider-Neutral Topology

Current Control Plane architecture distinguishes:

```text id="8t8p7a"
Capability

Provider

Engine

EngineInstance

CapabilityBinding.
```

A `CapabilityBinding` selects a Provider and EngineInstance for a governed scope.

Baobab Regulations SHALL consume that resolution rather than reconstruct it.

---

# 9. Future Provider Replacement

The same capability MAY eventually be provided by:

```text id="q0hrmo"
Baobab native Regulations

specialised commercial provider

jurisdiction-specific provider

hybrid regulatory provider.
```

Consumer contracts SHALL not assume the implementation.

---

# 10. Core Platform Boundary

```text id="doy22b"
                 CONTROL PLANE
────────────────────────────────────────
Tenant
Organisation
LegalEntity
Market
MarketParticipation
TradeLane
DigitalEstate
Capability
Grant
Provider
Binding
EngineInstance
Isolation
Residency
Administrative Authority
Context Resolution

                 REGULATIONS
────────────────────────────────────────
Legal Sources
Legal Authorities
Regimes
Instruments
Provisions
Interpretations
Rules
Applicability
Obligations
Requirements
Evidence Assessment
Regulatory Decisions
Regulatory Changes
Regulatory Impact
Jurisdiction Packs
```

---

# 11. Market Participation Is Regulatory Input

Control Plane's current onboarding model goes beyond saying:

```text id="8wwdxh"
market = UG.
```

It captures governed activities such as:

```text id="eqvopr"
LEGAL_PRESENCE

SOURCING

SELLING

EXPORTING.
```

The platform material correctly identifies:

```text id="3esdtr"
Organisation
+
Market
+
MarketParticipation
+
Business activities
```

as an appropriate precursor to future regulatory reasoning.

Baobab Regulations SHALL build upon this rather than creating a second market-participation model.

---

# 12. Platform Context and Regulatory Context Are Different

Hard invariant:

```text id="ynf1iy"
PlatformContext
≠
RegulatoryContext.
```

---

# 13. PlatformContext

Control Plane owns the resolution of platform-operational context.

Conceptually:

```text id="lma176"
PlatformContext
├── tenant_ref
├── organisation_ref?
├── legal_entity_ref?
├── market_ref?
├── market_participation_ref?
├── trade_lane_ref?
├── digital_estate_ref?
├── principal_ref?
├── platform_account_ref?
├── requested_capability?
├── isolation_requirement?
├── residency_requirement?
├── resolution_version
├── resolved_at
└── provenance
```

Exact schema remains Control Plane / Shared-owned.

---

# 14. RegulatoryContext

Regulations owns the regulatory evaluation envelope.

Conceptually:

```text id="d2y5cc"
RegulatoryContext
├── regulatory_context_id
│
├── platform_context_ref
├── platform_context_snapshot_ref
│
├── tenant_ref
├── organisation_ref?
├── legal_entity_ref?
│
├── market_context[]
├── market_participation_refs[]
├── trade_lane_ref?
│
├── jurisdiction_roles[]
├── regulatory_regimes[]
│
├── regulated_activity
├── subject_ref
├── product_ref?
├── commodity_classification?
├── regulatory_classifications[]
│
├── counterparties[]
├── transaction_ref?
├── shipment_ref?
│
├── legal_time
├── knowledge_time
│
├── fact_snapshot_ref
├── evidence_set_ref?
├── coverage_profile
└── provenance
```

---

# 15. Regulations Enriches Context

The correct transformation is:

```text id="m72528"
PlatformContext
       │
       ├── Tenant
       ├── Organisation
       ├── LegalEntity
       ├── Market
       ├── Participation
       └── TradeLane
       │
       ▼
Regulatory Context Enrichment
       │
       ├── Jurisdiction Roles
       ├── Regulatory Regimes
       ├── Product Classification
       ├── Regulatory Activity
       ├── Legal Time
       ├── Regulatory Facts
       └── Evidence
       │
       ▼
RegulatoryContext
```

---

# 16. Regulations SHALL NOT Resolve Tenant Identity Independently

Incorrect:

```text id="51i04y"
tenant_id =
request.headers["X-Tenant"]
```

Correct:

```text id="uf8bdg"
tenant_ref =
trusted resolved PlatformContext.
```

---

# 17. Client-Supplied Context Is Not Trusted

A caller MAY request:

```text id="8ylsvp"
market = ZA
```

as an input to resolution.

It SHALL NOT become authoritative merely because the request says so.

---

# 18. Context Resolution

Preferred:

```text id="53tc0w"
Request
   │
   ▼
IAM Authentication
   │
   ▼
Control Plane Context Resolution
   │
   ▼
Capability Resolution
   │
   ▼
Resolved PlatformContext
   │
   ▼
Regulations
```

---

# 19. Control Plane Is Not Business-Request Proxy

Consistent with existing Baobab architecture, Control Plane SHOULD generally:

```text id="mebuu5"
resolve

authorise

bind
```

rather than proxy every regulatory business request.

---

# 20. Preferred Runtime Path

```text id="yzgq2y"
Digital Estate / Trade
        │
        ├── authenticate via IAM
        │
        ▼
Control Plane
        │
        ├── resolve context
        └── resolve REGULATORY_DECISION capability
        │
        ▼
Resolved provider / EngineInstance
        │
        ▼
Baobab Regulations
        │
        ▼
Decision.
```

---

# 21. Context Reuse

A trusted PlatformContext MAY be reused for bounded periods where policy allows.

This avoids unnecessary synchronous Control Plane dependency for every internal operation.

---

# 22. Trusted Context Assertion

Baobab MAY define an integrity-protected:

# `PlatformContextAssertion`

for runtime propagation.

Conceptually:

```text id="ewyu80"
PlatformContextAssertion
├── context_ref
├── tenant_ref
├── legal_entity_ref?
├── market_ref?
├── participation_refs[]
├── trade_lane_ref?
├── capability_scope
├── isolation_profile
├── issued_at
├── expires_at
├── context_version
├── issuer
└── integrity_proof
```

---

# 23. Representation Not Mandated

The assertion MAY eventually use:

```text id="hr6f8d"
signed JWT

PASETO

signed structured object

opaque reference + CP lookup.
```

This ADR does not select one representation.

---

# 24. Integrity Is Mandatory for Trusted Propagation

Plain headers such as:

```text id="21olrb"
X-Tenant-ID

X-Legal-Entity-ID

X-Market
```

SHALL NOT independently establish trusted PlatformContext.

---

# 25. OpenTelemetry Baggage Is Not Trusted Context

OpenTelemetry explicitly warns that baggage may propagate to unintended downstream resources and has **no built-in integrity checks**.

Therefore Baobab SHALL NOT use observability baggage as authoritative:

```text id="ml91lz"
tenant context

legal entity identity

authorization

regulatory jurisdiction

capability grant.
```

---

# 26. Trace Context Is Observability Only

W3C Trace Context standardises propagation of:

```text id="d17zc2"
traceparent

tracestate
```

for distributed tracing.

It SHALL NOT become Baobab business context.

---

# 27. Identity Is Not Platform Context

Hard invariant:

```text id="r44alw"
OAuth access token
≠
PlatformContext.
```

---

# 28. IAM Boundary

`baobab-iam` owns:

```text id="mcnxwb"
authentication

principal identity

human sessions

service identities

credentials

token issuance

MFA/passkeys

authentication assurance

identity lifecycle.
```

---

# 29. IAM SHALL NOT Own

```text id="7yc3ne"
market participation

tenant provisioning

trade lane

regulatory applicability

regulatory reviewer competence

regulatory decision.
```

---

# 30. Regulations IAM Use

Regulations consumes:

```text id="iwyl75"
authenticated principal

service principal

authentication assurance

authorised scopes/capabilities
```

as inputs.

---

# 31. Regulatory Reviewer Competence

From ADR-REG-0022:

```text id="kug9dh"
identity
```

belongs to IAM.

```text id="n07ooy"
regulatory competence profile
```

belongs to Regulations.

---

# 32. Administrative Authority

A broad IAM role such as:

```text id="lp0r06"
admin
```

SHALL NOT itself confer Control Plane or Regulations administrative authority.

Control Plane's accepted authority architecture governs platform administrative grants.

---

# 33. Regulations Domain Authority

Regulations MAY additionally require:

```text id="nnsqcg"
review_rule

publish_rule

approve_interpretation

manage_source

certify_pack
```

domain permissions.

These SHALL remain scoped capabilities/permissions, not generic `admin=true`.

---

# 34. Service-to-Service Authentication

Engine-to-engine calls SHALL use authenticated service identities.

---

# 35. Resource-Audience Binding

RFC 8707 allows OAuth clients to identify the protected resource for which an access token is requested.

Where supported by Baobab IAM, service tokens SHOULD therefore be audience/resource-bound to the intended engine.

---

# 36. Example

A token intended for:

```text id="yn0cbg"
baobab-trade
```

SHOULD NOT automatically be valid for:

```text id="w3o74g"
baobab-regulations.
```

---

# 37. Token Exchange

RFC 8693 defines OAuth token exchange, including the ability for a resource server to obtain a more appropriate downstream token for a backend service.

Baobab IAM MAY use this pattern for delegated cross-engine calls.

---

# 38. Token Exchange Is Optional Architecture

This ADR does not require RFC 8693.

It requires:

```text id="hg4b54"
narrow service identity

audience restriction

least privilege

delegation provenance.
```

---

# 39. Token Is Not Regulatory Fact

Even a correctly authenticated user asserting:

```text id="mxcldi"
"I am importer"
```

does not make that a verified regulatory fact.

---

# 40. Organisation Boundary

Control Plane owns canonical:

```text id="oynm8q"
Organisation

CorporateGroup

PlatformAccount

tenant ↔ organisation relationships

legal-entity relationships.
```

Regulations references them.

---

# 41. Regulations SHALL NOT Build a Shadow Corporate Registry

Rejected:

```text id="ncomrj"
regulations.organisations

regulations.legal_entities

regulations.corporate_groups
```

as independent master registries.

---

# 42. Regulatory Attributes May Enrich Organisation

Regulations MAY own facts such as:

```text id="xpemlr"
regulated_entity_status

licensed_activity status

regulatory registration

jurisdiction-specific compliance role.
```

These SHALL reference the canonical Organisation/LegalEntity.

---

# 43. Legal Entity Boundary

Control Plane answers:

> **Which canonical legal entity is participating?**

Regulations answers:

> **What regulatory obligations attach to that legal entity in this context?**

---

# 44. Legal Entity ≠ Tenant

A tenant may represent:

```text id="h8qqad"
one

or multiple
```

legal entities according to platform architecture.

Regulations SHALL never infer:

```text id="rccg4i"
tenant_id
=
legal_entity_id.
```

---

# 45. Corporate Group ≠ Legal Entity

A group relationship does not automatically establish:

```text id="xswbgg"
legal liability

tax status

licence applicability

regulatory responsibility.
```

Those require regulatory/legal analysis.

---

# 46. Platform Account ≠ Regulatory Actor

Commercial account grouping is not legal actor identity.

---

# 47. Market Boundary

Control Plane owns canonical:

```text id="n3ro61"
Market

MarketParticipation

business activity participation.
```

---

# 48. Regulations Does Not Redefine Market

Rejected:

```text id="t7p03d"
RegulatoryMarket {
    country = ...
}
```

as a competing platform Market.

---

# 49. Market ≠ Country

Hard invariant.

---

# 50. Market ≠ Jurisdiction

Hard invariant.

---

# 51. MarketParticipation ≠ Regulatory Permission

A platform record stating:

```text id="jc6vmh"
ZuriBeans participates in ZA
activity = SELLING
```

means the platform has recorded that participation.

It does NOT mean:

```text id="04lq3z"
law permits every sale.
```

---

# 52. Regulations Tests Legality

```text id="321p1g"
MarketParticipation
        │
        ▼
RegulatoryContext
        │
        ▼
Regulatory rules
        │
        ▼
permission / obligations /
prohibitions / requirements.
```

---

# 53. TradeLane Boundary

Control Plane owns:

```text id="ao8z5g"
directional permitted platform trade relationship.
```

Regulations owns:

```text id="yhm9nq"
regulatory consequences
of that directional activity.
```

---

# 54. TradeLane ≠ Legal Route Approval

A configured:

```text id="gzm5qp"
UG → ZA
```

trade lane does not guarantee the transaction may legally proceed.

---

# 55. Jurisdiction Boundary

Baobab SHALL distinguish two aspects.

### Platform jurisdiction identity/reference

Stable jurisdiction identifiers used in shared context MAY be platform/shared-owned.

### Regulatory jurisdiction semantics

Regulations owns:

```text id="qaoy3m"
jurisdiction role

legal authority

legal hierarchy

regulatory regime

legal relationships

applicability semantics.
```

---

# 56. JurisdictionRole Is Regulations-Owned

Examples:

```text id="slflph"
ORIGIN

EXPORT

TRANSIT

IMPORT

DESTINATION

ESTABLISHMENT

REGISTRATION

TAX

CUSTOMS

SPS.
```

---

# 57. One Transaction May Have Multiple Jurisdictions

Example:

```text id="3aj9ue"
Uganda
  exporter establishment
  export
  origin

South Africa
  importer establishment
  import
  destination

EAC
  possible regional regime

SADC/AfCFTA
  possible regime relevance.
```

---

# 58. CP Market Does Not Collapse These

`market = ZA`

is insufficient as a complete RegulatoryContext.

---

# 59. Digital Estate Boundary

A Digital Estate is a client/entity-facing experience.

It MAY initiate regulatory operations.

It SHALL NOT own:

```text id="wjs7be"
tenant resolution

capability resolution

regulatory rule authority

legal applicability.
```

---

# 60. Server-Side Boundary

Digital estates SHOULD access consequential Regulations capabilities through:

```text id="5csv11"
server components

BFF

trusted backend.
```

---

# 61. Leaf UI Components SHALL NOT Resolve Markets or Providers

Rejected:

```text id="yhzs7r"
if country === "ZA":
    regulatoryApi = ...
```

---

# 62. Digital Estate Context

Estate context SHALL ultimately derive from trusted:

```text id="3d4yn8"
IAM identity

Control Plane context

server-side account/session state.
```

---

# 63. Trade Boundary

`baobab-trade` owns commerce and trade-execution state.

Examples:

```text id="q4x3jw"
customer

cart

quotation

order

commercial product

pricing

inventory

shipment workflow

trade transaction lifecycle.
```

---

# 64. Trade Is a Regulatory Fact Provider

Regulations MAY consume facts such as:

```text id="5n430y"
order reference

shipment reference

product reference

quantity

transaction value

origin

destination

Incoterm

customer/counterparty

planned shipment date

actual shipment date

delivery route.
```

---

# 65. Fact Ownership Does Not Move

When Regulations snapshots:

```text id="452rfq"
shipment.quantity = 100kg
```

Trade remains authoritative for the operational shipment.

---

# 66. Regulatory Snapshot Is Immutable Evaluation Evidence

Regulations records:

```text id="ceus29"
quantity used for Decision D
```

to support replay.

It does not become the shipment master.

---

# 67. Trade Is a PEP

Regulations may return:

```text id="ojc3in"
UNSATISFIED

recommended disposition = HOLD.
```

Trade decides how that maps into its own authorised state transition.

---

# 68. Regulations Does Not Update Trade Tables

Rejected:

```text id="h0br36"
UPDATE trade.shipment
SET status='HOLD'
```

from Regulations.

---


# 68A. Trade Docs Boundary — RTD-03 Amendment

Trade remains authoritative for commerce and trade-execution state.

Baobab Trade Docs is authoritative for executable trade-document and Customs-workflow state.

Regulations is authoritative for regulatory requirements, applicability, evidence sufficiency and decisions.

Therefore:

~~~text
Trade
  shipment/order/commercial state

Trade Docs
  documents/versions/dossiers/declarations/submissions/authority responses

Regulations
  rules/requirements/applicability/satisfaction/decisions
~~~

A document/customs workflow fact required by Regulations SHOULD be supplied by Trade Docs, not reconstructed from Trade tables.

---

# 68B. Regulations Does Not Update Trade Docs Tables

Rejected:

~~~text
UPDATE trade_docs.trade_document
SET verification_state = 'VERIFIED'
~~~

from Regulations.

Likewise, Trade Docs SHALL not directly mutate Regulations rules or decisions.

Cross-engine interaction occurs through governed APIs, events and references.

---

# 69. ERP Boundary

`baobab-erp` owns ERP-operational truth.

Examples:

```text id="tlljzl"
accounting

invoices

financial posting

tax execution

business partners

procurement

ERP documents

financial records.
```

---

# 70. ERP Is Also a Regulatory Fact Provider

Regulations MAY consume:

```text id="k7p2j1"
invoice values

declared tax information

registration identifiers

legal-document references

financial transaction facts.
```

---

# 71. Regulations Does Not Become ERP Tax Engine

Regulations may establish:

```text id="qff1o0"
which regulatory tax rule applies

what formula/rate is required.
```

ERP/Ledger owns:

```text id="70072w"
financial posting

accounting state

journal entries

settlement.
```

---

# 72. Tax Determination versus Accounting Execution

```text id="5y50uy"
Regulations
     │
     ▼
tax obligation /
regulatory rate rule
     │
     ▼
ERP / Ledger
     │
     ▼
financial calculation/posting
as appropriate to domain.
```

Exact future Ledger boundary remains governed separately.

---

# 73. Product Boundary

Trade owns:

```text id="02ndjb"
commercial product.
```

Regulations may own:

```text id="23ldzf"
regulatory classification assertion.
```

---

# 74. Product ≠ HS Classification

Example:

```text id="jzwri2"
Commercial Product:
ZuriBeans Bugisu Arabica 60kg

Regulatory classifications:
HS code
SPS category
commodity class
origin classification.
```

---

# 75. Classification Has Its Own Evidence

Regulations SHALL NOT silently mutate Trade product metadata to make classification authoritative.

---

# 76. Canonical Entity Resolution

Cross-engine references SHALL use Baobab's canonical identity and mapping contracts.

---

# 77. Shared Mapping Concepts

Relevant canonical platform concepts include:

```text id="5lfg9k"
CanonicalEntity

ExternalReference

Mapping

MappingScope.
```

---

# 78. Regulations SHALL NOT Create Parallel Cross-Engine Mapping Tables

Rejected:

```text id="bn7u9j"
regulations.trade_product_map

regulations.erp_customer_map

regulations.cms_entity_map.
```

---

# 79. Correct Cross-Engine Identity Path

```text id="duj4g6"
Trade native ID
      │
      ▼
ExternalReference
      │
      ▼
CanonicalEntity
      │
      ▼
Regulations reference.
```

---

# 80. Ambiguous Mapping

If mapping returns more than one valid target:

```text id="2br8po"
MAPPING_AMBIGUOUS.
```

Consequential evaluation SHALL fail closed/review-required.

---

# 81. Missing Mapping

```text id="0rjuvk"
MAPPING_NOT_FOUND
```

is not permission to guess.

---

# 82. External Legal Identifiers Are Different

Regulations MAY own identifiers such as:

```text id="j464yc"
ELI URI

official instrument number

Gazette number

regulatory permit identifier

court citation.
```

These are regulatory-domain identifiers.

They SHALL not be forced into Control Plane mapping solely because they are "external references."

---

# 83. Distinguish Identity Domains

```text id="di6kk5"
Cross-engine native object identity
     → Shared / CP Mapping

Legal-source/legal-instrument identity
     → Regulations domain.
```

---

# 84. Shared Repository Boundary

`baobab-platform/shared` owns reusable canonical contracts.

It SHALL remain:

```text id="5ikg08"
non-deployable

implementation-neutral

provider-neutral.
```

---

# 85. Shared SHALL NOT Become Platform Database

No engine SHALL query a:

```text id="x26wit"
Shared database.
```

There is none.

---

# 86. Regulations Contract Ownership

Preferred:

```text id="mo3uz7"
baobab-regulations
     │
     ├── owns semantic source contract
     │
     ▼
shared
     │
     └── distributes canonical cross-engine schema.
```

---

# 87. Avoid Contract Forking

Incorrect:

```text id="7rhk4m"
Regulations schema says
tenant_id string

Trade copy says
tenant UUID

CP copy says
tenant slug.
```

---

# 88. Contract Locking

Consumers SHOULD pin shared contract revisions through the platform's established contract-lock mechanisms.

---

# 89. Contract Drift

CI SHALL detect divergence between:

```text id="69grd1"
Regulations implementation

Shared schema

OpenAPI

AsyncAPI.
```

---

# 90. Platform Contract Versioning

Breaking shared contract change SHALL use explicit versioning/migration.

---

# 91. Canonical Fact Provider Pattern

Regulations SHALL define provider-neutral fact-provider interfaces.

---

# 92. RegulatoryFactBundle

Conceptually:

```text id="hklvop"
RegulatoryFactBundle
├── provider_ref
├── subject_refs[]
├── facts[]
├── captured_at
├── business_effective_at?
├── source_versions[]
├── classification
├── integrity
└── provenance
```

---

# 93. RegulatoryFact

Conceptually:

```text id="yy3zs8"
RegulatoryFact
├── fact_type
├── subject_ref
├── value
├── unit?
├── valid_at?
├── source_engine
├── native_reference?
├── canonical_reference?
└── evidence_ref?
```

---

# 94. Fact Bundle Is Not Generic JSON Dump

Rejected:

```text id="2pe4uj"
facts = entire_order_json.
```

---

# 95. Regulatory Minimum

Only regulatory-relevant facts SHOULD cross the boundary.

---

# 96. Fact Contracts SHALL Be Typed

Examples:

```text id="d1ppld"
ShipmentOrigin

ShipmentDestination

CommodityQuantity

DeclaredValue

Incoterm

ImporterLegalEntity

ExporterLegalEntity

ProductClassification

PermitReference.
```

---

# 97. Domain Engines Remain Fact Authorities

Regulations SHALL preserve:

```text id="7a7dg6"
source engine

source object

source version.
```

---

# 98. Fact Snapshot

For each consequential decision:

```text id="425gvf"
live external facts
       │
       ▼
Regulatory Fact Snapshot
       │
       ▼
DecisionInputEnvelope.
```

---

# 99. No Live Data Re-Fetch for Historical Replay

ADR-REG-0020 applies.

---

# 100. Counterparty Boundary

Control Plane/shared may own canonical organisation/counterparty identity relationships.

Trade/ERP own operational counterparty use.

Regulations owns:

```text id="d4q18u"
regulatory role in a particular legal context.
```

---

# 101. Example

Canonical Organisation:

```text id="e9uehs"
Acme Ltd.
```

Trade role:

```text id="msya3m"
customer.
```

Regulatory role:

```text id="0ynzyw"
importer of record.
```

These are distinct facts.

---

# 102. Pulse Boundary

`baobab-pulse` owns probabilistic intelligence.

Examples:

```text id="dbq6n0"
Observation

Signal

Insight

Opportunity

Risk

Forecast

Recommendation.
```

---

# 103. Regulations Owns Normative Determination

```text id="auwu61"
required

permitted

prohibited

exempted

applicable

unsatisfied.
```

---

# 104. Pulse → Regulations

Pulse MAY submit:

```text id="hm3oj2"
RegulatorySourceCandidate

RegulatoryChangeLead

RegulatoryRiskSignal.
```

---

# 105. Pulse Signal Is Never Canonical Law

Hard invariant.

---

# 106. Regulations → Pulse

Regulations publishes:

```text id="87f4w4"
VerifiedRegulatoryChange

RequirementChanged

ConfirmedRegulatoryImpact

RegulatoryDecision summary.
```

---

# 107. Pulse Then Adds Intelligence

Example:

```text id="ny3pa3"
Verified tariff increase
        │
        ▼
Pulse
        │
        ▼
margin-risk forecast.
```

---

# 108. Pulse and Regulations May Share Technologies

Both MAY use:

```text id="hh06fi"
Haystack

Qdrant

model providers.
```

They SHALL not share:

```text id="vd4yw8"
canonical domain state

knowledge truth

vector namespace by default

authority semantics.
```

---

# 109. Separate Qdrant Collections / Namespaces

Regulatory retrieval SHALL be isolated from Pulse intelligence retrieval.

---

# 110. Why

A Pulse market article SHOULD NOT accidentally outrank:

```text id="kbvfj3"
official regulatory source
```

inside the high-assurance Regulations corpus.

---

# 111. CMS Boundary

`baobab-cms` owns:

```text id="6soekj"
editorial content

composition

publication

content lifecycle

presentation metadata.
```

---

# 112. Regulations Owns Regulatory Semantics

CMS does not own:

```text id="o2azw0"
RuleVersion

legal applicability

RegulatoryDecision

legal-source authority.
```

---

# 113. Regulations → CMS

```text id="497dy6"
Verified regulatory knowledge
        │
        ▼
Rights-safe content projection
        │
        ▼
CMS
        │
        ▼
Editorial publication.
```

---

# 114. CMS → Regulations

Ordinary editorial content SHALL NOT automatically enter regulatory evidence.

---

# 115. CMS Could Supply Registered Material

Only if explicitly classified and processed through:

```text id="qpy4z6"
Source Registry

trust

rights

verification.
```

---

# 116. Avoid Regulatory Feedback Loop

Rejected:

```text id="ffy5ng"
Official law
    ↓
Regulations summary
    ↓
CMS article
    ↓
Regulations RAG
    ↓
article treated as source law.
```

---

# 117. IAM, CP, Regulations Security Chain

```text id="3c7v82"
IAM
   │
   └── Who is this?
          │
          ▼
Control Plane
   │
   └── What platform authority/context
       does this principal have?
          │
          ▼
Regulations
   │
   └── Is this principal permitted
       to perform this regulatory action?
```

---

# 118. No Layer Collapsing

Rejected:

```text id="68r52p"
IAM role = regulatory publisher.
```

---

# 119. Authentication Assurance

For consequential publication/review:

```text id="84iyfc"
Regulations
```

may require IAM authentication assurance compatible with ADR-REG-0022.

---

# 120. Context Authority and Fact Authority Are Different

Example:

```text id="zb1c57"
CP says:
legal entity = ZuriBeans Uganda Ltd

Trade says:
shipment destination = South Africa

Regulations says:
ZA import jurisdiction applies.
```

Each engine remains authoritative for its portion.

---

# 121. Context Provenance

Regulatory decisions SHALL identify the authority for each material context facet.

---

# 122. ContextFacet

Conceptually:

```text id="qv4t82"
ContextFacet
├── type
├── value
├── authority
├── source_ref
├── resolved_at
├── valid_at
└── assurance_state
```

---

# 123. Example

```text id="e385nt"
tenant
authority = Control Plane

shipment destination
authority = Trade

HS classification
authority = Regulations verified classification

principal
authority = IAM.
```

---

# 124. No Single Context Authority

Different facts have different owners.

---

# 125. Context Assembly

Regulations SHALL assemble:

```text id="cws0ru"
Platform context
+
transaction facts
+
regulatory classification
+
evidence
+
temporal perspective.
```

---

# 126. Context Assembly Does Not Transfer Ownership

---

# 127. Context Snapshot

Consequential evaluation SHALL persist:

# `RegulatoryPlatformContextSnapshot`

---

# 128. RegulatoryPlatformContextSnapshot

Conceptually:

```text id="507hkx"
RegulatoryPlatformContextSnapshot
├── platform_context_ref
├── platform_context_version
├── tenant_ref
├── organisation_ref?
├── legal_entity_ref?
├── market_refs[]
├── participation_refs[]
├── trade_lane_ref?
├── digital_estate_ref?
├── principal_ref?
├── isolation_profile_ref?
├── residency_requirement_ref?
├── resolved_at
├── valid_until?
├── resolver_provenance
└── digest
```

---

# 129. Snapshot Is Regulations Evidence

It preserves:

```text id="82vsor"
what platform context was used.
```

It does not become the master PlatformContext.

---

# 130. Context Freshness

A resolved context MAY have freshness constraints.

---

# 131. High-Consequence Evaluation

E3/E4 SHOULD require:

```text id="tvn2j4"
current enough

unrevoked

non-ambiguous

correctly scoped
```

PlatformContext.

---

# 132. Stale Context

Potential:

```text id="fr1oxp"
PLATFORM_CONTEXT_STALE.
```

---

# 133. Revoked Participation

If CP records:

```text id="5a34jl"
market participation suspended
```

Regulations SHALL not continue treating old context as indefinitely valid.

---

# 134. Context Revocation Event

CP SHOULD expose changes that invalidate cached:

```text id="p8vx9z"
tenant

legal entity

participation

capability binding

isolation

residency
```

context.

---

# 135. Context Invalidation Is Not Regulatory Law Change

But it may require reassessment.

---

# 136. Capability Resolution

Consumer SHALL resolve the desired capability through CP.

Conceptually:

```text id="iwqj70"
CapabilityResolution
├── capability_ref
├── grant_ref
├── provider_ref
├── engine_ref
├── engine_instance_ref
├── binding_ref
├── isolation_profile
├── region
├── readiness
├── resolution_version
└── resolved_at
```

---

# 137. Regulatory Semantics Must Not Depend on Engine Instance ID

Example:

```text id="66jfwo"
reg-af-south-1
```

is runtime topology.

It is not:

```text id="i8ultg"
legal jurisdiction.
```

---

# 138. Engine Region ≠ Jurisdiction

A Regulations instance hosted in:

```text id="05q8l9"
South Africa
```

may evaluate:

```text id="2rq5no"
Ugandan law

EAC law

AfCFTA rules.
```

subject to residency and service configuration.

---

# 139. Residency Is Platform Constraint

Control Plane determines acceptable provider topology based on:

```text id="nl099o"
isolation

residency

capability

environment

health/readiness.
```

---

# 140. Regulations SHALL Enforce Its Local Portion

Once bound to an EngineInstance, Regulations must still:

```text id="gs1v9c"
isolate tenant data

route to allowed storage

respect residency

restrict cross-tenant retrieval.
```

---

# 141. Stronger Isolation Cannot Resolve to Weaker Runtime

This follows current Control Plane provider/topology architecture.

Regulations SHALL expose sufficient topology/readiness information for CP to enforce it.

---

# 142. Regulations Provider Descriptor

Regulations SHOULD expose provider metadata such as:

```text id="9c02ad"
supported capabilities

regions

isolation modes

residency capabilities

API versions

event contract versions

jurisdiction-pack availability

runtime health.
```

---

# 143. Provider Descriptor Does Not Grant Capability

CP remains authority.

---

# 144. Onboarding Integration

Tenant onboarding SHALL not directly call:

```text id="wh3cl0"
create Regulations tenant row
```

from a frontend.

---

# 145. Correct Onboarding

```text id="p65e71"
Approved Organisation
        │
        ▼
TenantOnboardingRequest
        │
        ▼
ProvisioningDesiredState
        │
        ▼
Control Plane Planner
        │
        ├── required capability
        ├── grant
        ├── provider
        └── EngineInstance
        │
        ▼
Provisioning Operation
        │
        ▼
Regulations provider configuration
        │
        ▼
Readiness Evidence
        │
        ▼
Control Plane Readiness
```

---

# 146. Regulations Provisioning Scope

May include:

```text id="cp8x0a"
tenant namespace

jurisdiction-pack access

regulatory profiles

tenant-private knowledge overlay

retention policy

regional storage

event subscriptions

service credentials.
```

---

# 147. Regulations SHALL NOT Provision CP State

It SHALL report provider-owned provisioning state back to CP.

---

# 148. Desired State Separation

The platform material explicitly separates desired state from plan, execution and readiness.

Regulations SHALL expose operations compatible with that lifecycle rather than inventing a parallel onboarding state machine.

---

# 149. Readiness Boundary

Control Plane owns:

```text id="741chi"
platform-composed readiness.
```

Regulations owns:

```text id="zydb08"
provider/component readiness evidence.
```

---

# 150. Regulations Readiness Dimensions

Potential:

```text id="5xmzut"
SERVICE_READY

DATABASE_READY

SOURCE_MONITORING_READY

JURISDICTION_PACK_READY

RULESET_READY

OPA_RUNTIME_READY

REGULATORY_EXECUTION_PACKAGE_READY

EVENT_PUBLICATION_READY

TENANT_ISOLATION_READY.
```

---

# 151. AI Plane Is Not Necessarily Fast-Path Readiness

For existing published rules:

```text id="gevndy"
Haystack unavailable

Qdrant unavailable

LLM unavailable
```

does not necessarily mean:

```text id="rn6sdt"
REGULATORY_DECISION unavailable.
```

---

# 152. Capability-Specific Readiness

Example:

```text id="tqcq07"
REGULATORY_DECISION = READY

REGULATORY_CHANGE_INTELLIGENCE = DEGRADED.
```

This distinction SHOULD be exposed.

---

# 153. Coverage Readiness

A running API with zero verified rules is:

```text id="zk59eg"
SERVICE_HEALTHY
```

but not:

```text id="byu53f"
REGULATORY_COVERAGE_READY.
```

---

# 154. Health ≠ Readiness

Hard invariant.

---

# 155. Readiness ≠ Legal Coverage

Hard invariant.

---

# 156. Capability Readiness Contract

Conceptually:

```text id="twxez7"
RegulatoryCapabilityReadiness
├── capability_ref
├── service_health
├── coverage_state
├── jurisdiction_pack_refs[]
├── execution_package_state
├── data_freshness
├── degradation_reasons[]
├── checked_at
└── provenance
```

---

# 157. CP Composes Platform Readiness

Regulations SHALL not decide:

```text id="mmpqkx"
tenant is globally READY.
```

---

# 158. Runtime Interaction — Synchronous

Use synchronous APIs for:

```text id="tldyz4"
regulatory assessment

decision

applicability

explanation

rule query
```

where immediate answer is needed.

---

# 159. Runtime Interaction — Asynchronous

Use events/jobs for:

```text id="1kdtza"
regulatory change processing

bulk reassessment

large impact analysis

jurisdiction-pack publication

notifications

content projections.
```

---

# 160. No Distributed Transaction Across Engines

Regulations SHALL NOT require:

```text id="642gu9"
Trade DB

+

Regulations DB

+

ERP DB
```

to commit in one ACID transaction.

---

# 161. Use Local Transactions + Events

Consistent with ADR-REG-0024.

---

# 162. Synchronous Decision Does Not Need Cross-Engine Write

Consumer:

```text id="os7l30"
reads/provides facts
→ Regulations decides
→ consumer acts.
```

---

# 163. Decision Receipt

Consumer SHOULD persist:

```text id="xm5xl0"
RegulatoryDecision reference

decision version

RuleSet fingerprint

context snapshot/digest

decision validity.
```

---

# 164. Do Not Copy Entire Regulations Database

---

# 165. API Error Model

Regulations HTTP APIs SHOULD use RFC 9457 Problem Details for general machine-readable API errors. RFC 9457 defines `application/problem+json` and explicitly exists to avoid every API inventing a new error shape.

---

# 166. Regulatory Domain Errors

Potential stable problem types:

```text id="37y963"
CONTEXT_NOT_RESOLVED

CONTEXT_STALE

CAPABILITY_NOT_GRANTED

CAPABILITY_NOT_BOUND

ENGINE_INSTANCE_NOT_READY

MAPPING_NOT_FOUND

MAPPING_AMBIGUOUS

REGULATORY_COVERAGE_INCOMPLETE

RULESET_NOT_READY

EVIDENCE_REQUIRED

ASSESSMENT_INDETERMINATE

TENANT_SCOPE_MISMATCH.
```

---

# 167. HTTP Error ≠ Regulatory Outcome

For example:

```text id="1p5fbr"
HTTP 200
RegulatoryDecision = PROHIBITED
```

is valid.

`PROHIBITED` is not necessarily an HTTP error.

---

# 168. Likewise

```text id="lfbtzq"
HTTP 503
```

means service/evaluator unavailable.

It SHALL NOT mean:

```text id="ht68iu"
regulation prohibits transaction.
```

---

# 169. Canonical References in APIs

Cross-engine contracts SHOULD exchange:

```text id="0byd7e"
canonical refs

not local database integer IDs.
```

---

# 170. Native IDs Where Necessary

A source-engine native ID may accompany:

```text id="21qxwt"
CanonicalEntity ref

ExternalReference ref.
```

---

# 171. Context Request Pattern

A regulatory request SHOULD resemble conceptually:

```text id="0pd3yv"
RegulatoryDecisionRequest
├── platform_context_ref
├── capability_resolution_ref?
├── regulatory_question
├── subject_refs[]
├── fact_bundle_refs[]
├── evidence_refs[]
├── legal_time
└── idempotency/correlation metadata
```

---

# 172. Caller SHALL Not Set Authoritative Tenant Arbitrarily

If request contains:

```text id="3lmmqj"
tenant_ref
```

it must match trusted resolved context.

---

# 173. Context Mismatch

Result:

```text id="0dv9ho"
TENANT_SCOPE_MISMATCH.
```

---

# 174. Legal Entity Mismatch

Similarly:

```text id="bipdm1"
LEGAL_ENTITY_SCOPE_MISMATCH.
```

---

# 175. Subject Authorization

A principal allowed to operate for:

```text id="m09u9l"
LegalEntity A
```

cannot obtain private regulatory decisions for:

```text id="h3ikld"
LegalEntity B
```

merely by supplying its identifier.

---

# 176. Control Plane Administrative Authority

The current CP architecture correctly treats IAM identity and administrative authority as separate concepts.

Regulations SHALL follow the same principle for platform-scoped regulatory administration.

---

# 177. Changes to Regulatory Platform Configuration

Examples:

```text id="n7q2bk"
enable jurisdiction pack

change data residency

change provider binding

change execution instance

change tenant regulatory profile
```

SHOULD flow through CP controlled-change architecture where platform desired state is affected.

---

# 178. Regulations Internal Knowledge Change

Examples:

```text id="xh94rd"
publish RuleVersion

verify Interpretation

correct Provision
```

remain Regulations-governed changes.

---

# 179. Distinguish Platform Change and Regulatory Knowledge Change

```text id="tiyzuc"
Move tenant to different
Regulations EngineInstance
        │
        ▼
Control Plane change


Publish new tariff rule
        │
        ▼
Regulations change.
```

---

# 180. Changeset Boundary

CP changesets govern:

```text id="hfncjs"
platform desired-state mutation.
```

Regulations governance workflows govern:

```text id="4wldh4"
regulatory knowledge publication.
```

---

# 181. Both May Interact

Example:

```text id="f2mc8b"
new jurisdiction pack
requires dedicated regional deployment
```

may create:

```text id="zt3c89"
Regulations knowledge change
+
CP topology/desired-state change.
```

---

# 182. Neither Should Silently Perform the Other

---

# 183. Event Integration

ADR-REG-0024 canonical events SHALL use Shared event contracts where cross-engine.

---

# 184. Regulations Events

Examples:

```text id="u5gdf8"
change.verified

reassessment.required

decision.issued

decision.outcome-changed

requirement.changed

jurisdiction-pack.degraded.
```

---

# 185. CP Events Relevant to Regulations

Examples:

```text id="vkatph"
tenant suspended

legal entity changed

market participation changed

trade lane changed

capability revoked

binding changed

isolation changed

residency changed.
```

Exact event names remain CP-owned.

---

# 186. CP Context Change May Invalidate Regulatory Decisions

Example:

```text id="6l7skm"
LegalEntity changed
```

may make:

```text id="whgeap"
existing cached decision stale.
```

---

# 187. Context Change Is Reassessment Trigger

Not necessarily law change.

---

# 188. Regulations Should Subscribe Selectively

Do not consume every CP administrative event.

Only context-changing events relevant to regulatory semantics/readiness.

---

# 189. Shared Event Envelope

CloudEvents conventions from ADR-REG-0024 apply.

---

# 190. Correlation

A complete flow SHOULD preserve:

```text id="vm754u"
correlation_id

causation_id

trace context.
```

---

# 191. Correlation Does Not Confer Trust

A matching correlation ID does not authenticate context.

---

# 192. Observability

Every consequential cross-engine call SHOULD record:

```text id="eb6hcm"
trace_id

caller engine

provider resolution

platform context ref

tenant ref

capability ref

decision ref

latency

result class.
```

Subject to privacy controls.

---

# 193. Do Not Log Sensitive Evidence by Default

Avoid raw:

```text id="oiy8op"
identity documents

legal opinions

permit contents

personal information.
```

---

# 194. Logs ≠ Audit

Operational logs aid diagnostics.

Canonical audit records establish regulatory/platform history.

---

# 195. Audit Authority

Each domain records its own audit.

Cross-engine correlation allows reconstruction.

---

# 196. Example Audit Chain

```text id="9mimue"
IAM
principal authenticated
        │
        ▼
CP
PlatformContext resolved
        │
        ▼
CP
REGULATORY_DECISION provider resolved
        │
        ▼
Trade
Shipment facts supplied
        │
        ▼
Regulations
Decision D issued
        │
        ▼
Trade
Regulatory hold enforced.
```

---

# 197. Every Step Has Different Authority

That is desirable.

---

# 198. ZuriBeans Example — Uganda to South Africa


> **RTD-03 amendment:** Steps 4–8 below describe the original non-documentary happy path. For any decision dependent on certificates, permits, declarations or authority responses, §1U is normative: Trade Docs supplies the canonical documentary/workflow facts and Regulations evaluates requirement satisfaction from their versioned references.

Consider:

```text id="mkuc3k"
ZuriBeans
exports coffee
from Uganda
to South Africa.
```

---

# 199. Step 1 — IAM

IAM establishes:

```text id="38gscu"
principal P

authenticated service/user

assurance level.
```

---

# 200. Step 2 — Control Plane

CP establishes:

```text id="lw4m3i"
tenant = ZuriBeans

organisation = ZuriBeans canonical organisation

legal entity = exporting entity

market participation:
UG / EXPORTING
ZA / SELLING or IMPORTING where relevant

trade lane:
UG → ZA

digital estate:
ZuriBeans estate

capability:
REGULATORY_DECISION.
```

---

# 201. Step 3 — Capability Resolution

CP resolves:

```text id="0org7x"
Capability
        ↓
Grant
        ↓
Provider
        ↓
CapabilityBinding
        ↓
Regulations EngineInstance.
```

---

# 202. Step 4 — Trade Facts

Trade supplies:

```text id="w6yd50"
shipment S

commercial product P

quantity

origin

destination

transaction value

planned date

counterparty references.
```

---

# 203. Step 5 — Regulations Enrichment

Regulations resolves:

```text id="zrzpxq"
origin jurisdiction role = Uganda

export jurisdiction role = Uganda

import jurisdiction role = South Africa

destination jurisdiction = South Africa

commodity classification

HS classification

relevant regimes

legal time.
```

---

# 204. Step 6 — Regulatory Evaluation

Regulations evaluates:

```text id="i82k6n"
customs

tariff

origin

SPS

permit

documentation

applicable restrictions.
```

---

# 205. Step 7 — Decision

Example:

```text id="fug6cw"
UNSATISFIED

reason:
phytosanitary certificate missing

effect class:
E3

recommended disposition:
HOLD.
```

---

# 206. Step 8 — Enforcement

Trade receives Decision D.

Trade:

```text id="t6hoau"
checks decision validity

checks current shipment version

maps disposition through its policy

places shipment on regulatory hold.
```

---

# 207. What Regulations Did Not Do

It did not:

```text id="qzbtdx"
authenticate P

create tenant

create ZuriBeans legal entity

create market participation

select its own EngineInstance

own the shipment

mutate the Trade database.
```

---

# 208. Another Example — Platform Relationship Change

Suppose CP later records:

```text id="x6nxke"
ZA market participation suspended.
```

That is a platform context change.

---

# 209. Regulations Reaction

Potential:

```text id="8h4250"
invalidate affected cached contexts

identify active regulatory decisions

request reassessment where appropriate.
```

---

# 210. It Does Not Reinterpret the CP Decision

Regulations does not decide whether participation should have been suspended.

---

# 211. Example — Law Change

South African import rule changes.

That is:

```text id="yi8ebg"
Regulations-owned change.
```

---

# 212. CP Is Not Asked to Interpret the Law

Regulations:

```text id="qcl2lu"
verifies rule

publishes RuleVersion

identifies impacted contexts

reassesses.
```

---

# 213. Example — Provider Migration

CP migrates:

```text id="59hsxn"
REGULATORY_DECISION
```

from:

```text id="2qe78q"
Regulations EngineInstance A
```

to:

```text id="e4uuwf"
EngineInstance B.
```

---

# 214. Regulatory Semantics SHALL Remain Stable

Consumer still requests:

```text id="38k956"
REGULATORY_DECISION.
```

No estate code change should be necessary.

---

# 215. Decision Package Portability

New provider/instance must support:

```text id="xpgfd5"
required RuleSet

BRIR semantics

decision contracts

effect classes

explanation contracts.
```

---

# 216. Provider Migration Test

ADR-REG-0025 differential/historical tests SHALL validate semantic equivalence.

---

# 217. Platform Context Contract Versioning

Regulations SHALL explicitly declare compatible:

```text id="f144ox"
PlatformContext schema versions.
```

---

# 218. Unsupported Context Version

Return:

```text id="xebpq3"
PLATFORM_CONTEXT_VERSION_UNSUPPORTED.
```

Do not guess fields.

---

# 219. Shared Contract Compatibility Tests

CI SHOULD test Regulations against:

```text id="lf2y30"
current pinned Shared

next Shared candidate where appropriate.
```

---

# 220. Contract Lock

`contracts.lock.yaml` or equivalent platform-standard mechanism SHOULD pin exact compatible Shared revisions.

---

# 221. No Copy-Paste Drift

Schemas SHALL be vendored/generated only according to platform contract-governance conventions.

---

# 222. Context Evolution

New optional dimensions MAY be added.

Example:

```text id="dwgslo"
customs_regime_ref.
```

Older consumers may ignore optional fields if safe.

---

# 223. New Material Semantics

A new required context dimension may require:

```text id="l2xdfc"
new contract version.
```

---

# 224. Fail Closed on Missing Material Context

If new rule depends on:

```text id="zgcdg6"
importer establishment jurisdiction
```

and it is missing:

```text id="1rre9o"
INDETERMINATE
```

rather than:

```text id="ju9boo"
assume destination country.
```

---

# 225. Context Resolution Explanations

Regulations explanation SHOULD distinguish:

```text id="wsfrol"
CP-resolved fact

Trade fact

Regulations-derived regulatory fact.
```

---

# 226. Example

```text id="nuq4m6"
LegalEntity:
resolved by Control Plane.

Shipment destination:
supplied by Trade.

Import jurisdiction:
derived by Regulations
from destination and regulatory rule.
```

---

# 227. This Supports Decision Defence

ADR-REG-0020 can show not only:

```text id="v1copj"
what facts were used
```

but:

```text id="3swmpj"
which engine was authoritative for each.
```

---

# 228. Cross-Engine Freshness

Each fact bundle/context SHOULD expose:

```text id="lsnisd"
captured_at

source_version

validity.
```

---

# 229. Different Freshness Policies

Example:

```text id="ddvs5t"
tenant/legal entity:
longer-lived

shipment status:
short-lived

FX/tariff reference:
time-bound

permit:
validity-period-bound.
```

---

# 230. No Universal TTL

---

# 231. Idempotency

Cross-engine decision requests SHOULD support idempotency where repeated requests represent the same intended operation.

---

# 232. Idempotency ≠ Decision Reuse

If material context changes:

```text id="ldl8ug"
new assessment required.
```

---

# 233. Context Fingerprint

Decision input SHOULD compute a deterministic:

```text id="jgmfvu"
context_fingerprint
```

from material regulatory context.

---

# 234. Non-Material Metadata Excluded

Trace IDs or UI language SHALL not normally change regulatory fingerprint.

---

# 235. Material Data Included

Examples:

```text id="8q59ig"
legal entity

jurisdictions

classification

quantity

legal time

evidence state.
```

---

# 236. Cached Decision Validity

A cached RegulatoryDecision MAY be reused only if:

```text id="6p1506"
context fingerprint still valid

RuleSet still valid

decision validity unexpired

no invalidating event.
```

---

# 237. Platform Context Change May Invalidate Cache

---

# 238. Regulations Context Change May Invalidate Cache

---

# 239. Event Change May Invalidate Cache

---

# 240. Decision Validity Is Regulations-Owned

CP does not decide whether a regulatory decision remains legally valid.

---

# 241. Consumer Owns Cache Use

Trade may store decisions.

It must respect validity contracts.

---

# 242. No Shared Regulatory Cache

A tenant-private decision SHALL not become reusable by another tenant merely because inputs appear similar.

---

# 243. Isolation

Canonical context always includes sufficient tenant/isolation scope to prevent cross-tenant reuse.

---

# 244. Data Residency

Control Plane provides residency requirements.

Regulations SHALL map them to its:

```text id="qtpiv3"
PostgreSQL

object store

Qdrant

workflow state

logs

backups.
```

---

# 245. AI Provider Routing Also Respects Residency

External model transfer may be prohibited by:

```text id="tjlcbl"
rights

residency

tenant policy.
```

---

# 246. Provider Binding Alone Is Not Enough

A correctly bound Regulations instance must still enforce its internal:

```text id="y15tek"
data-plane controls.
```

---

# 247. Infrastructure Context Must Not Leak into Rule Semantics

Rejected:

```text id="sl9yac"
if engine_instance.region == "ZA":
    apply South African law.
```

---

# 248. Legal Context Comes from Regulatory Facts

Never infrastructure location.

---

# 249. Multi-Region Future

The same RegulatoryContext may execute in:

```text id="01nqa7"
different compliant regions
```

without changing legal result.

---

# 250. Provider-Neutrality Test

Run same:

```text id="6g37ax"
Context

RuleSet

DecisionPolicy
```

against different approved provider/runtime.

Expected:

```text id="685p5m"
semantic equivalence.
```

---

# 251. Problem Details

Cross-engine API failures SHOULD use stable RFC 9457 problem types while domain outcomes remain explicit business representations.

---

# 252. Context Propagation Security Summary

```text id="h1igjd"
OAuth token
   = authenticated/authorised caller

PlatformContext
   = CP-resolved business/platform scope

Trace Context
   = observability

Baggage
   = optional telemetry metadata

RegulatoryContext
   = Regulations evaluation envelope.
```

These SHALL NOT be conflated.

---

# 253. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-INT-I01` | Regulations SHALL be a platform capability engine, not a replacement Control Plane |
| `REG-INT-I02` | Control Plane SHALL remain authority for Tenant identity and lifecycle |
| `REG-INT-I03` | Control Plane SHALL remain authority for Organisation/LegalEntity platform relationships |
| `REG-INT-I04` | Control Plane SHALL remain authority for Market and MarketParticipation |
| `REG-INT-I05` | Control Plane SHALL remain authority for Capability, Grant, Binding, Provider, Engine and EngineInstance |
| `REG-INT-I06` | Regulations SHALL NOT self-entitle tenants |
| `REG-INT-I07` | Regulations SHALL NOT self-select its provider/EngineInstance |
| `REG-INT-I08` | PlatformContext SHALL remain distinct from RegulatoryContext |
| `REG-INT-I09` | Regulations SHALL enrich, not redefine, PlatformContext |
| `REG-INT-I10` | Client-supplied tenant/legal-entity context SHALL not be authoritative |
| `REG-INT-I11` | Trusted propagated context SHALL have integrity and freshness controls |
| `REG-INT-I12` | OpenTelemetry baggage SHALL NOT establish trusted business context |
| `REG-INT-I13` | Trace Context SHALL remain observability metadata |
| `REG-INT-I14` | Authentication token SHALL remain distinct from business/regulatory context |
| `REG-INT-I15` | IAM SHALL authenticate principals but SHALL NOT determine regulatory applicability |
| `REG-INT-I16` | Regulatory reviewer competence SHALL remain Regulations-owned |
| `REG-INT-I17` | Market SHALL remain distinct from Jurisdiction |
| `REG-INT-I18` | MarketParticipation SHALL remain distinct from legal permission |
| `REG-INT-I19` | TradeLane SHALL remain distinct from regulatory approval |
| `REG-INT-I20` | Regulations SHALL NOT maintain a shadow corporate master registry |
| `REG-INT-I21` | Domain engines SHALL remain authoritative for their operational facts |
| `REG-INT-I22` | Regulations SHALL preserve immutable snapshots of facts used for decisions |
| `REG-INT-I23` | Fact snapshots SHALL NOT become upstream operational masters |
| `REG-INT-I24` | Trade/ERP SHALL act as PEPs for their domain rather than Regulations mutating their databases |
| `REG-INT-I25` | Cross-engine native IDs SHALL use canonical mapping contracts |
| `REG-INT-I26` | Missing or ambiguous mappings SHALL fail closed/review-required |
| `REG-INT-I27` | Legal-source identifiers SHALL remain distinct from cross-engine native-object mappings |
| `REG-INT-I28` | Shared SHALL distribute contracts but SHALL NOT own runtime domain state |
| `REG-INT-I29` | Pulse intelligence SHALL not become verified regulation |
| `REG-INT-I30` | CMS editorial content SHALL not become legal authority |
| `REG-INT-I31` | Technology reuse between Pulse and Regulations SHALL not imply shared truth |
| `REG-INT-I32` | Provider deployment geography SHALL not determine legal jurisdiction |
| `REG-INT-I33` | CP platform readiness SHALL remain distinct from Regulations provider readiness |
| `REG-INT-I34` | Service health SHALL remain distinct from legal coverage readiness |
| `REG-INT-I35` | Consequential cross-engine decisions SHALL preserve source-engine provenance for material facts |
| `REG-INT-I36` | No distributed database transaction SHALL be required across engines |
| `REG-INT-I37` | Platform desired-state changes and regulatory knowledge changes SHALL remain separate governance domains |
| `REG-INT-I38` | Capability resolution SHALL remain provider-neutral |
| `REG-INT-I39` | Shared contract versions SHALL be pinned and compatibility-tested |
| `REG-INT-I40` | High-consequence decisions SHALL fail safely when material platform context is stale, ambiguous or unavailable |

---


# 253A. RTD-03 Additional Invariants

The RTD-03 invariants in §1W are normative extensions of this section.

In particular, architecture conformance tests SHOULD eventually prove:

~~~text
Regulations domain model
  contains no canonical TradeDocument / DocumentVersion / CustomsCase aggregate

Trade Docs domain model
  contains no canonical RegulatoryDecision / RegulatoryRequirement aggregate

Regulations adapters
  depend on ports / Shared contracts
  not Trade Docs database schemas

Trade Docs adapters
  depend on Regulations contracts
  not Regulations database schemas
~~~

---

# 254. Rejected Alternative — Regulations Owns Tenant

Rejected.

---

# 255. Rejected Alternative — Regulations Owns Legal Entity Master Data

Rejected.

---

# 256. Rejected Alternative — Regulations Has Its Own Market Registry

Rejected.

---

# 257. Rejected Alternative — Market Equals Jurisdiction

Rejected.

---

# 258. Rejected Alternative — Market Participation Means Legal Permission

Rejected.

---

# 259. Rejected Alternative — Trade Lane Means Regulatory Clearance

Rejected.

---

# 260. Rejected Alternative — Every Engine Resolves Tenant Differently

Rejected.

The engine may translate canonical context into native isolation, but the platform identity must remain shared.

---

# 261. Rejected Alternative — Trust `X-Tenant-ID`

Rejected.

---

# 262. Rejected Alternative — Use OpenTelemetry Baggage as Authorization Context

Rejected.

OpenTelemetry itself warns that baggage has no built-in integrity mechanism.

---

# 263. Rejected Alternative — Put Entire PlatformContext Inside OAuth Token Forever

Rejected.

Identity/token lifecycle and business-context lifecycle differ.

---

# 264. Rejected Alternative — IAM Role Defines Market Participation

Rejected.

---

# 265. Rejected Alternative — `admin=true`

Rejected.

---

# 266. Rejected Alternative — Digital Estate Chooses Regulatory Provider

Rejected.

---

# 267. Rejected Alternative — Browser Directly Calls OPA

Rejected.

---

# 268. Rejected Alternative — Regulations Updates Trade Shipment Directly

Rejected.

---

# 269. Rejected Alternative — Regulations Writes ERP Journals

Rejected.

---

# 270. Rejected Alternative — Regulations Replicates Whole Trade/ERP Schemas

Rejected.

---

# 271. Rejected Alternative — Cross-Engine Database Joins

Rejected.

---

# 272. Rejected Alternative — Shared Database

Rejected.

---

# 273. Rejected Alternative — Pulse Insight Is Regulatory Fact

Rejected.

---

# 274. Rejected Alternative — CMS Article Is Regulatory Source by Default

Rejected.

---

# 275. Rejected Alternative — Qdrant Collection Shared Uncritically with Pulse

Rejected.

---


# 275A. Rejected Alternative — Regulations Owns Trade Documents

Rejected because regulatory requirement semantics and documentary lifecycle have different authorities, temporal models and operational workflows.

---

# 275B. Rejected Alternative — Trade Docs Decides Requirement Satisfaction

Rejected because documentary verification cannot by itself determine legal applicability, issuer acceptability, regime-specific sufficiency or consequence.

---

# 275C. Rejected Alternative — One Customs Aggregate in Regulations

Rejected because Customs regulation, documentary submission workflow, sovereign authority action, operational shipment state and financial posting are different authority domains.

---

# 276. Rejected Alternative — Engine Region Determines Applicable Law

Rejected.

---

# 277. Rejected Alternative — Healthy API Means Regulatory Pack Ready

Rejected.

---

# 278. Rejected Alternative — AI Plane Required for Existing Deterministic Decision

Rejected.

---

# 279. Rejected Alternative — CP Proxies Every Regulatory Evaluation

Rejected as normal architecture.

---

# 280. Rejected Alternative — Regulations Self-Provisions on First Request

Rejected.

---

# 281. Rejected Alternative — Unsupported Shared Contract Is Best-Effort Parsed

Rejected.

---

# 282. Rejected Alternative — Mapping Ambiguity Resolved by First Match

Rejected.

---

# 283. Rejected Alternative — Missing Context Filled by Country Guess

Rejected.

---

# 284. Rejected Alternative — One Universal Context TTL

Rejected.

---

# 285. Minimum Implementation Proof

Before `ADR-REG-0026` is considered implemented, Baobab SHOULD demonstrate:

```text id="h0332n"
1. Regulations Engine registration.

2. Regulations Provider registration.

3. regulatory capability definitions.

4. capability grants controlled by CP.

5. CapabilityBinding resolution.

6. EngineInstance resolution.

7. no hard-coded provider in digital estate.

8. no hard-coded provider in Trade.

9. provider migration test.

10. provider-neutral desired state.

11. Regulations absent from desired-state provider fields.

12. PlatformContext contract consumption.

13. PlatformContext version validation.

14. tenant reference consumption.

15. organisation reference consumption.

16. legal-entity reference consumption.

17. market reference consumption.

18. MarketParticipation reference consumption.

19. TradeLane reference consumption.

20. DigitalEstate reference consumption.

21. principal reference consumption.

22. PlatformContextSnapshot.

23. context provenance.

24. context digest.

25. context freshness.

26. context stale error.

27. context revocation handling.

28. client tenant spoof rejection.

29. client legal-entity spoof rejection.

30. context mismatch rejection.

31. trusted context assertion interface.

32. integrity validation.

33. expiry validation.

34. context version validation.

35. proof that OTel baggage cannot establish tenant.

36. W3C Trace Context propagation.

37. trace IDs excluded from regulatory fingerprint.

38. IAM service authentication.

39. human authentication.

40. service principal authentication.

41. resource/audience-scoped service token.

42. token cannot replace PlatformContext.

43. reviewer competence separate from IAM identity.

44. domain permissions separate from generic IAM role.

45. Regulations RegulatoryContext aggregate.

46. PlatformContextRef inside RegulatoryContext.

47. jurisdiction-role enrichment.

48. multi-jurisdiction context.

49. market != jurisdiction test.

50. market participation != permission test.

51. trade lane != legal clearance test.

52. origin jurisdiction role.

53. export jurisdiction role.

54. transit jurisdiction role.

55. import jurisdiction role.

56. destination jurisdiction role.

57. establishment jurisdiction role.

58. trade fact provider interface.

59. ERP fact provider interface.

60. RegulatoryFactBundle.

61. typed RegulatoryFact.

62. source-engine provenance.

63. source-object version.

64. fact snapshot.

65. no historical live-fact fetch.

66. Trade shipment snapshot.

67. ERP financial-fact snapshot.

68. product canonical reference.

69. product regulatory classification.

70. Product != HS test.

71. counterparty canonical reference.

72. counterparty regulatory-role enrichment.

73. Shared CanonicalEntity use.

74. Shared ExternalReference use.

75. Shared Mapping use.

76. Shared MappingScope use.

77. missing mapping fails closed.

78. ambiguous mapping fails closed.

79. legal-source identifier kept outside cross-engine mapping semantics.

80. contract lock for Shared.

81. contract drift CI.

82. Shared schema compatibility test.

83. OpenAPI compatibility.

84. AsyncAPI compatibility.

85. RFC 9457 Problem Details.

86. CONTEXT_NOT_RESOLVED problem.

87. CONTEXT_STALE problem.

88. CAPABILITY_NOT_GRANTED problem.

89. CAPABILITY_NOT_BOUND problem.

90. ENGINE_INSTANCE_NOT_READY problem.

91. MAPPING_NOT_FOUND problem.

92. MAPPING_AMBIGUOUS problem.

93. REGULATORY_COVERAGE_INCOMPLETE problem.

94. regulatory outcome not encoded as HTTP error.

95. Pulse RegulatoryChangeLead seam.

96. Pulse lead cannot publish RuleVersion.

97. verified Regulations change event to Pulse.

98. separate Pulse/Regulations Qdrant namespaces.

99. CMS rights-safe projection.

100. CMS editorial content excluded from primary authority.

101. no CMS→law feedback loop.

102. Trade PEP integration.

103. Trade does not expose DB to Regulations.

104. Regulations does not mutate Trade DB.

105. ERP PEP/integration seam.

106. Regulations does not mutate ERP DB.

107. no cross-engine ACID transaction.

108. synchronous decision API.

109. asynchronous reassessment flow.

110. canonical CloudEvents integration.

111. CP context-change event consumption.

112. capability-revocation event handling.

113. participation-change invalidation.

114. legal-entity-change invalidation.

115. provider-binding-change handling.

116. tenant-suspension handling.

117. provider readiness endpoint.

118. service health state.

119. coverage readiness state.

120. RuleSet readiness.

121. OPA readiness.

122. execution-package readiness.

123. tenant-isolation readiness.

124. capability-specific readiness.

125. AI-plane degradation distinct from decision readiness.

126. provider provisioning callback/operation.

127. CP onboarding operation integration.

128. jurisdiction-pack provisioning.

129. tenant-private knowledge overlay provisioning.

130. residency configuration.

131. isolation configuration.

132. CP composes final readiness.

133. Regulations does not mark tenant globally ACTIVE.

134. context fingerprint.

135. material context included in fingerprint.

136. non-material telemetry excluded.

137. decision cache validity.

138. CP change invalidates cached decision.

139. Ruleset change invalidates cached decision.

140. fact change invalidates cached decision.

141. no cross-tenant decision reuse.

142. ZuriBeans UG→ZA context flow.

143. Trade shipment fact flow.

144. Regulations multi-jurisdiction enrichment.

145. regulatory decision flow.

146. Trade regulatory hold PEP flow.

147. platform participation suspension reassessment.

148. South African law-change reassessment.

149. Regulations provider migration.

150. historical semantic equivalence after provider migration.
```

---

# 286. Initial ZuriBeans Integration Proof

The first production-grade integration proof SHOULD execute this flow:

```text id="7sqy20"
ZuriBeans Digital Estate
          │
          ▼
      IAM / Ory
          │
          ▼
 authenticated principal
          │
          ▼
 Baobab Control Plane
          │
          ├── Tenant
          ├── Organisation
          ├── LegalEntity
          ├── MarketParticipation
          ├── TradeLane
          ├── CapabilityGrant
          └── CapabilityBinding
          │
          ▼
  Resolved PlatformContext
          │
          ▼
     Baobab Trade
          │
          ├── Shipment
          ├── Product
          ├── Quantity
          ├── Value
          ├── Parties
          └── Dates
          │
          ▼
  Regulatory Fact Bundle
          │
          ▼
  Baobab Regulations
          │
          ├── Jurisdiction Roles
          ├── Regimes
          ├── HS / classification
          ├── Rules
          ├── Evidence
          └── Legal Time
          │
          ▼
    RegulatoryDecision
          │
          ▼
      Baobab Trade
          │
          ▼
           PEP
```

---

# 287. Example Platform Context

```text id="p3nb6q"
Tenant:
ZuriBeans

Organisation:
ZuriBeans

LegalEntity:
ZuriBeans Uganda entity

Market participation:
UG / EXPORTING

Trade lane:
UG → ZA

Capability:
REGULATORY_DECISION
```

---

# 288. Example Trade Facts

```text id="0dxfwk"
Shipment:
S-1008

Product:
Arabica Coffee

Quantity:
60kg

Origin:
Uganda

Destination:
South Africa

Expected customs entry:
2027-02-03.
```

---

# 289. Regulations Adds

```text id="gmvo4z"
Origin jurisdiction:
Uganda

Export jurisdiction:
Uganda

Import jurisdiction:
South Africa

Regulatory classification:
HS X

Applicable regimes:
verified applicable regimes

Legal time:
2027-02-03.
```

---

# 290. Decision

```text id="m4ize3"
SATISFIED_WITH_REQUIREMENTS

Requirement:
valid phytosanitary certificate

Requirement timing:
must remain valid at required control point.
```

---

# 291. No Boundary Was Violated

```text id="tu365t"
IAM owned identity.

CP owned platform context.

Trade owned shipment.

Regulations owned regulatory meaning.

Trade owned enforcement.
```

That is the intended architecture.

---

# 292. Context Authority Matrix

| Context / Object | Canonical Authority | Regulations Role |
|---|---|---|
| Principal | IAM | Reference |
| Authentication assurance | IAM | Consume |
| Tenant | Control Plane | Reference |
| Organisation | Control Plane | Reference |
| Corporate relationship | Control Plane | Reference |
| Legal entity | Control Plane | Reference |
| Platform Account | Control Plane | Reference |
| Market | Control Plane | Reference |
| MarketParticipation | Control Plane | Consume |
| TradeLane | Control Plane | Consume |
| DigitalEstate | CP/estate contract | Reference |
| Capability | Control Plane | Consume |
| CapabilityGrant | Control Plane | Consume |
| CapabilityBinding | Control Plane | Consume |
| Provider | Control Plane | Consume |
| Engine/EngineInstance | Control Plane | Consume runtime resolution |
| Commercial product | Trade | Reference |
| Order / Shipment | Trade | Fact source |
| Financial record | ERP | Fact source |
| Regulatory classification | Regulations / verified authority | Own |
| Jurisdiction role | Regulations | Own |
| Regulatory regime | Regulations | Own |
| Legal source | Regulations | Own |
| RuleVersion | Regulations | Own |
| RegulatoryDecision | Regulations | Own |
| Enforcement action | Domain PEP | Observe/result reference |
| Intelligence signal | Pulse | Candidate input |
| Editorial content | CMS | Projection/presentation |

---

# 293. Runtime Trust Matrix

```text id="g7boil"
DATA / CLAIM                      TRUST SOURCE
──────────────────────────────────────────────────

Who is caller?                    IAM

Which tenant?                     CP

Which legal entity?               CP

Which market participation?       CP

Which provider?                   CP

Which EngineInstance?             CP

What shipment exists?             Trade

What quantity/value?              Trade

What invoice exists?              ERP

What legal rule applies?          Regulations

What evidence satisfies it?       Regulations assessment

What commercial risk follows?     Pulse

How is explanation published?     CMS

What operational action occurs?   PEP domain engine
```

---

# 294. Research and Architecture Foundation

The existing Baobab platform architecture already establishes the engine model: specialised engines retain independent implementations and domain persistence while sharing a common platform contract for identity, organisation, tenancy, APIs, events, audit, configuration and observability. That architecture is the direct foundation for treating Regulations as another specialised platform engine rather than expanding the Control Plane into regulatory business logic.

The current onboarding architecture further establishes the provider-neutral desired-state principle: customer intent records tenants, legal entities, profiles, market participation, estates, isolation and residency, while provider, engine, EngineInstance, grant and binding remain derived platform topology. Regulations therefore integrates through capabilities rather than appearing as customer-authored infrastructure.

The same onboarding architecture explicitly enriches market scope with governed business activities and identifies Organisation + Market + MarketParticipation + activity as the appropriate precursor to regulatory reasoning. Regulations adopts those facts as inputs and adds legal-jurisdiction and regulatory semantics instead of introducing competing commercial geography concepts.

OAuth Resource Indicators provide a standards-based mechanism for requesting tokens intended for a particular protected resource, supporting Baobab's preference for audience/resource-bounded service authentication rather than universally reusable bearer credentials.

OAuth Token Exchange provides a standard mechanism through which one resource server can obtain a token more appropriate for a downstream service, which is compatible with future provider-neutral Baobab service delegation without requiring that downstream engines simply forward the original user credential.

W3C Trace Context provides interoperable distributed tracing propagation. Baobab deliberately treats this as operational context only; its trace identifiers support observability and forensic correlation but never establish tenancy, legal identity or regulatory applicability.

OpenTelemetry's own documentation warns that baggage can propagate outside intended service boundaries and has no built-in integrity checks. This strongly supports the decision that Baobab business context cannot be trusted merely because tenant or legal-entity identifiers appear in telemetry baggage.

RFC 9457 supplies the standard HTTP Problem Details representation for machine-readable API errors. Regulations adopts it for technical/platform failures while keeping regulatory outcomes such as `PROHIBITED` or `INDETERMINATE` as regulatory domain results rather than misusing HTTP status semantics.

---

# 295. Final Decision

Baobab Regulations SHALL participate in the Baobab ecosystem as a **capability-resolved, context-aware, independently authoritative regulatory engine**.

The final architecture is:

```text id="00pklh"
                       IAM
                        │
                        ▼
                   Principal
                        │
                        ▼
                CONTROL PLANE
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 PlatformContext   Capability       Engine Topology
                   Resolution
        │               │                │
        └───────────────┼────────────────┘
                        ▼
               Consumer / BFF / Engine
                        │
              ┌─────────┴───────────┐
              ▼                     ▼
        Domain Facts          Provider Resolution
              │                     │
              └─────────┬───────────┘
                        ▼
                BAOBAB REGULATIONS
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Jurisdiction      Regulatory       Fact/Evidence
  Enrichment         Rules            Snapshot
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                RegulatoryContext
                        │
                        ▼
                RegulatoryDecision
                        │
                ┌───────┼───────┐
                ▼       ▼       ▼
              Trade    ERP    Other PEPs
```

The Control Plane principle is:

> **Control Plane owns platform identity, context, entitlement, provider resolution, topology, isolation, residency and composed readiness.**

The Regulations principle is:

> **Regulations owns regulatory sources, legal meaning, applicability, obligations, requirements, evidence assessment, regulatory decisions and regulatory change.**

The IAM principle is:

> **IAM establishes authenticated identity and authentication assurance; it does not decide tenant context, legal applicability or regulatory competence.**

The context principle is:

> **RegulatoryContext is an enrichment of trusted PlatformContext and domain facts—not an independent replacement for them.**

The market principle is:

> **Market, MarketParticipation, TradeLane, Jurisdiction and RegulatoryRegime are different concepts and SHALL remain different concepts.**

The fact principle is:

> **Each engine remains authoritative for its operational facts; Regulations snapshots those facts for reproducible decisions without assuming ownership of them.**

The mapping principle is:

> **Cross-engine identity flows through CanonicalEntity, ExternalReference and Mapping contracts rather than ad hoc pairwise mapping tables.**

The Trade/ERP principle is:

> **Regulations determines regulatory meaning; domain engines enforce resulting dispositions within the business state they own.**

The Pulse principle is:

> **Pulse may detect and analyse regulatory signals, but Regulations alone promotes verified normative regulatory knowledge.**

The CMS principle is:

> **CMS owns editorial publication and presentation, not law, applicability or regulatory decisions.**

The provider-neutrality principle is:

> **Consumers request regulatory capabilities, not `baobab-regulations`, OPA or a particular EngineInstance.**

The infrastructure principle is:

> **Where Regulations executes is topology; what law applies is regulatory context. Infrastructure geography SHALL never determine legal jurisdiction.**

The trust principle is:

> **OAuth identity, PlatformContext, regulatory facts, observability context and RegulatoryContext have different purposes and different authorities and SHALL never be collapsed into one unverified request envelope.**

The readiness principle is:

> **A healthy service is not necessarily a ready regulatory capability; Control Plane composes provider health with coverage, RuleSet, isolation and runtime readiness.**

The evolution principle is:

> **Shared contracts standardise integration while each Baobab engine remains free to evolve its internal implementation independently.**

And the strategic principle is:

> **Baobab Regulations should know enough about the wider platform to make contextually correct regulatory decisions, but never so much that it begins impersonating the engines whose facts, identity, topology and business state it depends upon.**

That is the architecture established by `ADR-REG-0026`.

---

## Decision Summary

```text id="j5rj1b"
ADR-REG-0026
────────────────────────────────────────

REGULATIONS

Baobab engine
not platform core.


CONTROL PLANE OWNS

Tenant
Organisation
LegalEntity
Market
MarketParticipation
TradeLane
DigitalEstate refs

Capability
Grant
Provider
Binding
Engine
EngineInstance

Isolation
Residency
Platform Context
Administrative authority


REGULATIONS OWNS

RegulatorySource
Authority semantics
Regime
Instrument
Provision
Interpretation
RuleVersion
Applicability
Obligation
Requirement
Evidence Assessment
Decision
Change
Impact


IAM OWNS

Identity
Authentication
Sessions
Service principals
Tokens
MFA assurance


TRADE OWNS

Products
Orders
Shipments
Commerce facts

and acts as PEP.


ERP OWNS

Financial / ERP state

and acts as PEP.


PULSE OWNS

Signals
Insights
Risk
Opportunity

not legal truth.


CMS OWNS

Editorial publication

not legal truth.


SHARED OWNS

Canonical wire contracts

not runtime state.


CORE TRANSFORMATION

PlatformContext
+
Domain Facts
+
Regulatory Enrichment
=
RegulatoryContext


MARKET

≠ Jurisdiction


MARKET PARTICIPATION

≠ legal permission


TRADE LANE

≠ regulatory clearance


ENGINE REGION

≠ legal jurisdiction


AUTHENTICATION TOKEN

≠ PlatformContext


TRACE / BAGGAGE

≠ trusted context


CROSS-ENGINE IDENTITY

ExternalReference
+
CanonicalEntity
+
Mapping


PROVIDER RESOLUTION

Capability
→ Grant
→ Provider
→ Binding
→ EngineInstance


DESIRED STATE

Customer intent

not provider topology.


REGULATORY DECISION

Regulations decides.

Domain engine enforces.


STRATEGIC RESULT

One Baobab context

Many specialised engines

Clear authority

No shadow domains.
```
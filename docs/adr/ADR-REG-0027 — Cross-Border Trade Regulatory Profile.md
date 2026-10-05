# ADR-REG-0027 — Cross-Border Trade Regulatory Profile: Customs, HS Classification, Origin, SPS and Trade Documentation

**Subtitle:** Uganda → South Africa Coffee and Vanilla Pilot, Tariff Classification, Preferential Origin, Plant Health, Customs Valuation, Import Taxes, Documentary Requirements and Trade-Readiness Composition

**Status:** Proposed — Foundational Cross-Border Regulatory Profile  
**Decision ID:** `ADR-REG-0027`  
**Engine:** `baobab-regulations`  
**Initial Corridor:** Uganda → South Africa  
**Initial Commodities:** Coffee and vanilla  
**Date:** 2026-09-29  
**Amended:** 2026-10-05 — RTD-03, under accepted ADR-SHARED-019 and aligned with the ADR-REG-0026 RTD-03 amendment, ADR-TDOC-0001, ADR-TDOC-0002 and ADR-PULSE-012  
**Platform Boundary Authority:** ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary  
**Decision Type:** Cross-Border Trade / Customs / Origin / SPS / Documentation / Tax / Regulatory Profiles

---

## 1. Executive Decision

Baobab Regulations SHALL model cross-border trade regulation as a **composition of independently authoritative and independently versioned regulatory rule families**.

It SHALL NOT implement:

```text
ImportCompliance {
    compliant: true | false
}
```

Instead, the initial Uganda → South Africa profile SHALL evaluate at least:

```text
Exporter eligibility
        │
        ▼
Product identity
        │
        ▼
HS / tariff classification
        │
        ▼
Origin determination
        │
        ▼
Preferential-regime eligibility
        │
        ▼
Uganda export requirements
        │
        ▼
SPS / phytosanitary export requirements
        │
        ▼
Trade documentation
        │
        ▼
Transit / direct-transport conditions
        │
        ▼
South African import admissibility
        │
        ▼
SPS / plant-health import conditions
        │
        ▼
Customs valuation
        │
        ▼
Customs duty
        │
        ▼
Import VAT / other border charges
        │
        ▼
Customs declaration
        │
        ▼
Release readiness
```

Each layer SHALL produce its own:

```text
applicability

requirements

evidence

status

legal basis

effective time

explanation.
```

The resulting cross-border decision is a composition of those determinations.

> **Classification determines what the goods are for customs purposes. Origin determines where they legally originate. A trade regime determines whether preference is available. SPS determines whether the goods may cross the plant-health boundary. Customs determines declaration, valuation and border charges. Documentation proves the propositions on which those determinations depend.**

Those concepts SHALL remain separate.

---


# 1A. RTD-03 Normative Amendment — Documentary and Customs Workflow Decomposition

This section is a **normative amendment** to ADR-REG-0027.

The original profile was intentionally comprehensive because, when written, Baobab Trade Docs did not yet exist as an explicit engine. It therefore described both:

~~~text
what documentary evidence regulation requires
~~~

and, in some places, wording that could be interpreted as:

~~~text
Regulations owns the document/document workflow itself.
~~~

That second interpretation is now rejected.

The target architecture is:

~~~mermaid
flowchart LR
    T[Trade / TMS\ncommercial + shipment facts] --> R[Baobab Regulations\nnormative meaning]
    R -->|DocumentRequirement\nPermitRequirement\nEvidenceRequirement| D[Baobab Trade Docs\ndocument + Customs workflow]
    D -->|DocumentVersion refs\nverification facts\nauthority responses| R
    R --> DEC[RegulatoryDecision]
    DEC --> PEP[Trade / TMS / ERP PEP]
    R --> P[Pulse\nrisk / opportunity / intelligence]
    D --> P
~~~

The profile therefore continues to model **documentation as a regulatory rule family**, but Regulations owns the **requirements and satisfaction decisions**, while Trade Docs owns the **document instances and workflow**.

---

# 1B. The Cross-Border Profile Has Three Different Documentary Layers

The profile SHALL distinguish:

| Layer | Meaning | Canonical authority |
|---|---|---|
| Documentary requirement | What the law/regime requires and under what conditions | Regulations |
| Documentary object/workflow | The concrete document/version/submission/response | Trade Docs |
| Regulatory sufficiency | Whether the concrete documentary facts satisfy the requirement | Regulations |

This means:

~~~text
PHYTOSANITARY_CERTIFICATE_REQUIRED
        → Regulations

TradeDocument TD-100 / DocumentVersion 3
        → Trade Docs

TD-100/v3 satisfies requirement R-22
        → Regulations
~~~

---

# 1C. Documentation Remains a Regulatory Rule Family

ADR-REG-0027's original architecture is preserved:

~~~text
classification
origin
trade regime
SPS
documentation
transit
valuation
duty
tax
declaration
release readiness
~~~

But the word **documentation** now means:

~~~text
regulatory documentary requirements
+
regulatory evaluation of documentary sufficiency
~~~

It does **not** mean:

~~~text
document repository
document lifecycle
document versioning
document rendering
submission workflow
Customs authority message store
~~~

Those are Trade Docs concerns.

---

# 1D. Requirement-Type Semantics Versus Document-Type Semantics

Regulations MAY define or use controlled regulatory requirement concepts such as:

~~~text
PHYTOSANITARY_CERTIFICATE
CERTIFICATE_OF_ORIGIN
IMPORT_PERMIT
EXPORT_LICENCE
QUALITY_CERTIFICATE
COMMERCIAL_INVOICE
PACKING_LIST
CUSTOMS_DECLARATION
TRANSPORT_DOCUMENT
~~~

for the purpose of stating requirements.

Trade Docs MAY classify concrete TradeDocument objects using compatible document-type vocabulary.

Neither side SHALL turn a type registry into a hidden rule engine.

The critical distinction is:

~~~text
document_type
    = semantic classification

DocumentRequirement
    = regulatory proposition

TradeDocument
    = concrete documentary object
~~~

---

# 1E. Canonical Ownership Matrix for This Profile

| Concept | Owner |
|---|---|
| HS classification decision | Regulations |
| Origin determination | Regulations |
| Preferential eligibility | Regulations |
| SPS requirement | Regulations |
| Permit requirement | Regulations |
| Document requirement | Regulations |
| Evidence requirement | Regulations |
| Acceptable issuer criteria | Regulations |
| Required signature/form/validity criteria | Regulations |
| Requirement satisfaction | Regulations |
| TradeDocument | Trade Docs |
| DocumentVersion | Trade Docs |
| DocumentContent / ContentArtifact | Trade Docs |
| DocumentDossier | Trade Docs |
| issuer claim | Trade Docs |
| document authenticity/verification workflow | Trade Docs |
| CustomsCase | Trade Docs |
| CustomsDeclaration workflow | Trade Docs |
| submission lifecycle | Trade Docs |
| authority-response record | Trade Docs |
| external legal effect of certificate/permit/release | Competent external authority |
| shipment/order hold/release | Trade/TMS |
| accounting/payment of border charges | ERP/Ledger |
| commercial risk/opportunity | Pulse |

---

# 1F. Regulatory Document Requirement Model

The conceptual DocumentRequirement in this ADR remains Regulations-owned.

It SHOULD be interpreted as:

~~~text
DocumentRequirement
├── requirement_id
├── document_purpose
├── acceptable_document_types[]
├── applies_to
├── legal_basis_refs[]
├── jurisdiction
├── regime
├── required_issuer_role?
├── acceptable_issuer_refs[]?
├── signature_requirement?
├── required_data_elements[]?
├── format_constraints[]?
├── original_copy_electronic_rule?
├── valid_from
├── valid_until?
├── timing_rule
├── quantity/value threshold?
├── condition_expression
├── evidence_requirement_refs[]
├── effect_if_unsatisfied
└── version / provenance
~~~

It SHALL not contain mutable TradeDocument lifecycle state.

---

# 1G. Documentary Instance Model Is External to Regulations

A concrete documentary object is referenced from Trade Docs.

Conceptually:

~~~text
TradeDocumentReference
├── owner = baobab-trade-docs
├── trade_document_id
├── document_version_id
├── document_type
├── issuer_claim_ref?
├── subject_refs[]
├── issued_at?
├── expires_at?
├── verification_fact_refs[]
└── provenance/version metadata
~~~

The exact portable shape belongs to Shared RTD-05.

Regulations SHALL not prematurely freeze this conceptual shape into an incompatible local cross-engine contract.

---

# 1H. Document Authenticity, Validity and Sufficiency

ADR-REG-0027 already states:

~~~text
DocumentAuthenticity
    !=
RequirementSatisfaction
~~~

RTD-03 makes the intermediate distinctions explicit.

~~~text
Integrity
    ↓
Authenticity
    ↓
Issuer verification
    ↓
Document lifecycle validity
    ↓
Regulatory-context validity
    ↓
Requirement satisfaction
~~~

These are not guaranteed implications.

A document can be authentic but fail because it is:

- expired;
- for the wrong consignment;
- for the wrong commodity;
- from an issuer not acceptable under the rule;
- valid only in another jurisdiction;
- missing required data;
- outside the permitted timing window;
- revoked;
- applicable to another origin/destination;
- insufficient for the claimed preference.

Trade Docs provides documentary facts.

Regulations applies the legal criteria.

---

# 1I. Permit and Certificate Semantics

A permit or certificate has at least three relevant identities:

~~~text
1. External legal act / credential
   authority = issuing institution

2. TradeDocument / DocumentVersion
   authority = Trade Docs for Baobab documentary representation

3. Regulatory standing / satisfaction result
   authority = Regulations
~~~

Example:

~~~text
NPPOZA import permit
        │
        ├── issued by competent authority
        │
        ├── represented as TradeDocument TD-501
        │
        └── evaluated by Regulations against PermitRequirement PR-19
~~~

None of those three identities should be collapsed.

---

# 1J. Exporter-Level Licence Versus Consignment Document

The original distinction remains important.

An exporter-level coffee licence may establish reusable standing across many consignments.

Regulations MAY maintain:

~~~text
RegulatoryRegistration / RegulatoryStanding
├── legal_entity_ref
├── registration/licence type
├── authority_ref
├── legal status
├── valid_from
├── valid_until
└── verification/evidence refs
~~~

Trade Docs MAY hold the licence's documentary representation.

A single TradeDocument instance is therefore not necessarily the regulatory standing itself.

---

# 1K. Origin Evidence Boundary

The following remain separate:

~~~text
Origin determination
        → Regulations

Proof-of-origin requirement
        → Regulations

Certificate/declaration document instance
        → Trade Docs

Document verification
        → Trade Docs

Preferential evidence sufficiency
        → Regulations
~~~

Example:

~~~mermaid
flowchart LR
    O[Regulations\nOrigin = Uganda] --> P[Regulations\nAfCFTA proof required]
    TD[Trade Docs\nCertificate of Origin v2] --> V[Trade Docs\nissuer/signature/version facts]
    P --> E[Regulations\nPreference Evidence Assessment]
    V --> E
    E --> PREF[PreferentialTariffAssessment]
~~~

Failure to prove preference does not automatically reclassify or prohibit the goods.

---

# 1L. SPS Documentary Boundary

For phytosanitary requirements:

~~~text
commodity/origin/destination/legal-time facts
        ↓
Regulations
        ↓
SPS requirement
        ↓
phytosanitary document requirement
        ↓
Trade Docs document workflow
        ↓
Trade Docs verified documentary facts
        ↓
Regulations satisfaction evaluation
        ↓
SPS decision
~~~

The NPPO remains the authority that issues the certificate.

Trade Docs does not become NPPO.

Regulations does not become the certificate repository.

---

# 1M. Customs Declaration Decomposition

The phrase “Customs declaration” SHALL be decomposed.

Regulations owns:

~~~text
whether declaration is required
which classification/origin/valuation rules apply
required regulatory propositions/data
required supporting evidence
timing/legal consequences
regulatory assessment of defects
~~~

Trade Docs owns:

~~~text
CustomsDeclaration workflow aggregate
declaration document/version
supporting-document dossier
submission
amendment
resubmission
authority acknowledgement
authority rejection/error
authority message
status projection
~~~

The competent Customs administration owns:

~~~text
official acceptance
assessment
hold
release
ruling
~~~

Trade/TMS owns:

~~~text
shipment operational state
~~~

ERP/Ledger owns:

~~~text
financial posting
~~~

---

# 1N. Customs Release Readiness Versus Customs Release

Regulations MAY produce:

~~~text
release-readiness recommendation
requirements satisfied / unsatisfied / indeterminate
recommended disposition
~~~

That is not a sovereign release.

Trade Docs MAY record:

~~~text
authority response = RELEASED
~~~

That is a Baobab record of an external authority act.

It is still not Trade Docs exercising sovereign release authority.

---

# 1O. Two-Phase Cross-Border Documentary Evaluation

The profile SHALL support a planning phase and an execution/reassessment phase.

## Phase 1 — pre-flight requirement determination

~~~mermaid
flowchart TD
    C[CrossBorderTradeContext] --> R[Regulations]
    R --> CL[Classification]
    R --> OR[Origin]
    R --> SPS[SPS]
    R --> DR[DocumentRequirements]
    R --> PR[PermitRequirements]
    R --> PRE[Pre-flight RegulatoryDecision]
~~~

The result may identify what is still needed.

## Phase 2 — evidence-backed satisfaction

~~~mermaid
flowchart TD
    REQ[Document / Permit Requirements] --> TD[Trade Docs]
    TD --> DOCS[DocumentVersions + verification facts]
    DOCS --> R2[Regulations reassessment]
    CTX[Current cross-border context] --> R2
    R2 --> FINAL[RegulatoryDecision]
    FINAL --> PEP[Trade / TMS / ERP PEP]
~~~

This model avoids the anti-pattern:

~~~text
document exists?
    yes → compliant
    no  → prohibited
~~~

---

# 1P. Cross-Border Context Adds Documentary References, Not Documents

The CrossBorderTradeContext in §78 MAY be extended with references such as:

~~~text
document_dossier_ref?
document_version_refs[]
customs_case_refs[]
authority_response_refs[]
~~~

where those are material to evaluation.

It SHALL not embed entire Trade Docs aggregates.

The authoritative documentary state remains resolvable from Trade Docs under access control.

---

# 1Q. Evidence Graph for a Document-Dependent Decision

A cross-border RegulatoryDecision SHOULD be explainable through a graph such as:

~~~mermaid
flowchart LR
    SRC[Legal Source] --> RULE[RuleVersion]
    RULE --> REQ[DocumentRequirement]
    REQ --> SAT[RequirementSatisfaction]

    TDV[Trade Docs\nDocumentVersion] --> SAT
    VER[Trade Docs\nVerification Facts] --> SAT
    CTX[CrossBorderTradeContext] --> SAT

    SAT --> DEC[RegulatoryDecision]
    DEC --> ACT[Operational Disposition]
~~~

The graph preserves the difference between legal basis, documentary evidence and operational action.

---

# 1R. Evidence Snapshot and Replay

For a consequential decision Regulations SHALL preserve:

~~~text
requirement version
document reference
document version
verification state/reference
legal time
knowledge time
relevant authority response reference
decision ruleset fingerprint
evaluation result
~~~

This is immutable decision evidence.

If Trade Docs later receives a corrected certificate or new authority response, the old decision remains replayable as made.

---

# 1S. Documentary Staleness

Material documentary events MAY invalidate a prior decision.

Examples:

~~~text
document superseded
certificate expired
permit revoked
issuer verification changed
consignment changed
quantity changed
origin changed
authority response changed
declaration amended
submission rejected
~~~

The owner of the RegulatoryDecision remains Regulations.

Trade Docs SHALL emit or expose the documentary fact.

Regulations SHALL determine whether reassessment is required.

---

# 1T. Event Directionality for the Cross-Border Profile

Subject to Shared contract governance:

## Regulations → Trade Docs

~~~text
document requirement determined
permit requirement determined
classification assigned
requirement changed
regulatory decision issued/superseded
~~~

## Trade Docs → Regulations

~~~text
document issued/versioned
document verification changed
document superseded/expired/revoked
declaration submitted
submission rejected
authority response received
Customs case materially changed
~~~

## Regulations → Trade / TMS / ERP

~~~text
RegulatoryDecision
classification result
tariff/duty assessment
tax assessment
recommended disposition
~~~

## Regulations / Trade Docs → Pulse

Facts may be consumed asynchronously for intelligence.

Events state facts. Requests to create, submit, amend or reassess belong to governed API/capability/command boundaries.

---

# 1U. Error and Unknown Semantics

The profile SHALL distinguish:

~~~text
document not yet supplied
document supplied but unverified
document verified but legally insufficient
document expired
document revoked
wrong document version
issuer unresolved
requirement applicability unresolved
Trade Docs unavailable
Regulations unavailable
authority response pending
authority response unknown
~~~

These are materially different states.

They SHALL not collapse into one DOCUMENT_ERROR or one NON_COMPLIANT state.

The correct result may be:

~~~text
REQUIREMENT_PENDING
UNSATISFIED
INDETERMINATE
REVIEW_REQUIRED
WAITING_FOR_AUTHORITY
~~~

depending on the rule and workflow.

---

# 1V. Updated Integration Topology

The original profile listed Trade, ERP and Pulse integrations.

Trade Docs is now a first-class peer.

~~~mermaid
flowchart TB
    CP[Control Plane\ntrusted platform context] --> R[Baobab Regulations]

    T[Trade / TMS\nproduct shipment route value] --> R
    R -->|requirements + decision refs| D[Baobab Trade Docs]
    D -->|document/version/verification/authority refs| R

    R -->|RegulatoryDecision| T
    R -->|duty/VAT assessment| ERP[ERP / Ledger]

    R --> P[Pulse]
    D --> P

    D --> AUTH[External Customs / Issuers]
    AUTH --> D
~~~

---

# 1W. Profile-Specific Reference Rules

Cross-engine references SHALL preserve:

~~~text
owner engine
object type
object id
version/revision where material
tenant/scope
resolved/observed time
classification
provenance
~~~

The exact Shared schema remains RTD-05 work.

This profile SHALL not use ADR-SHARED-013 ExternalReference as a substitute for Baobab-to-Baobab canonical object references.

---

# 1X. Reconciliation of Existing Sections

The following interpretation is normative.

| Existing ADR-REG-0027 area | RTD-03 interpretation |
|---|---|
| §§20–25 origin/document distinctions | Retained; concrete document instances belong to Trade Docs |
| §25 Documentary Purpose | Regulatory purpose/criteria belong to Regulations; documentary object metadata belongs to Trade Docs |
| §§31–44 exporter/SPS/importer standing | Requirements/standing remain Regulations; documentary representations may be Trade Docs |
| §§45–52 Customs documentation | Requirements remain Regulations; declaration/document workflow moves to Trade Docs |
| §49 Documentary Families | Families are requirement/type semantics, not Regulations-owned document instances |
| §50 Certificate Graph | Treat as regulatory requirement/evidence graph; concrete nodes resolve to Trade Docs versions |
| §52 Document Validity | Documentary facts from Trade Docs; legal sufficiency from Regulations |
| §§72–78 composite decision/context | Add documentary references where material |
| §§89–95 data/AI/OPA | OPA evaluates verified requirement semantics, not document lifecycle |
| §§96–98 Trade Integration | Add Trade Docs as separate document/Customs workflow provider |
| §§99–102 ERP/Pulse/CMS | Retained |
| §§103–106 material regulatory events | Retained; document events separately originate in Trade Docs |
| §§107–116 golden cases | Cases must distinguish requirement state, document state and satisfaction |
| §§127–129 certification/invariants | Extended by RTD-03 invariants |
| §§131–132 implementation proof | Must include Trade Docs contract/reference integration |
| §§133–137 realistic flow/final decision | Amended by §1V and updated final architecture |

---

# 1Y. RTD-03 Cross-Border Invariants

The existing REG-XBT invariants remain valid and are extended by:

| ID | Invariant |
|---|---|
| REG-XBT-I36 | DocumentRequirement SHALL remain distinct from TradeDocument |
| REG-XBT-I37 | Concrete trade-document identity/version SHALL be owned by Trade Docs |
| REG-XBT-I38 | Regulations SHALL own documentary requirement semantics and satisfaction decisions |
| REG-XBT-I39 | Trade Docs verification SHALL not automatically establish regulatory sufficiency |
| REG-XBT-I40 | CustomsDeclaration workflow SHALL be distinct from declaration regulatory requirements |
| REG-XBT-I41 | External Customs acceptance/release SHALL remain sovereign authority facts |
| REG-XBT-I42 | Permit requirement SHALL remain distinct from permit document representation |
| REG-XBT-I43 | Exporter regulatory standing SHALL remain distinct from licence document storage |
| REG-XBT-I44 | Document-version changes SHALL be capable of triggering regulatory reassessment |
| REG-XBT-I45 | Historical decisions SHALL retain the exact document versions used |
| REG-XBT-I46 | Cross-engine documentary references SHALL retain owner identity |
| REG-XBT-I47 | ExternalReference SHALL not substitute for a Baobab cross-engine canonical object reference |
| REG-XBT-I48 | Trade Docs unavailability SHALL not be interpreted as documentary absence |
| REG-XBT-I49 | Regulations unavailability SHALL not be interpreted as legal prohibition |
| REG-XBT-I50 | No Regulations-to-Trade-Docs direct database dependency is permitted |
| REG-XBT-I51 | No jurisdiction-specific legal requirement logic SHALL be hidden in a generic Trade Docs document-type registry |
| REG-XBT-I52 | Regulatory document families SHALL describe legal purpose, not imply lifecycle ownership |
| REG-XBT-I53 | A Customs authority response record SHALL preserve the external authority as the source of legal effect |
| REG-XBT-I54 | Pulse SHALL not be placed synchronously between Regulations and Trade Docs for requirement satisfaction |

---

# 1Z. Revised Implementation Sequence

The original implementation sequence is amended to make the documentary boundary executable in the right order.

~~~text
Authoritative source registration
        │
        ▼
Regulatory source ingestion / provenance
        │
        ▼
Classification / origin / SPS / tariff rule domains
        │
        ▼
DocumentRequirement / PermitRequirement domain
        │
        ▼
RTD-04 Shared TradeDocument contract reconciliation
        │
        ▼
RTD-05 cross-engine object reference contract
        │
        ▼
RTD-06 Regulations ↔ Trade Docs APIs/events
        │
        ▼
Trade Docs document/version/customs workflow integration
        │
        ▼
Requirement-satisfaction evaluation
        │
        ▼
Trade / TMS PEP integration
        │
        ▼
ERP/Ledger financial handoff
        │
        ▼
Pulse asynchronous intelligence
        │
        ▼
Golden corpus + historical replay + shadow evaluation
~~~

Regulations may implement requirement semantics before Trade Docs runtime integration.

It SHALL not fake the missing document engine by permanently absorbing TradeDocument lifecycle into Regulations.

---

# 1AA. Revised Minimum Documentary Proof

Before the cross-border profile is considered production-capable for documentary decisions, the implementation SHOULD demonstrate at least:

| Proof | Expected authority |
|---|---|
| Phytosanitary certificate requirement generated from verified rule | Regulations |
| Certificate TradeDocument created/ingested | Trade Docs |
| Immutable DocumentVersion established | Trade Docs |
| Issuer claim captured | Trade Docs |
| Issuer/document verification facts produced | Trade Docs |
| Requirement-satisfaction evaluation cites exact version | Regulations |
| Expired version yields correct reassessment | Regulations |
| Superseded version preserves historical replay | Both by reference |
| AfCFTA proof requirement distinct from ICO certificate requirement | Regulations |
| Two concrete origin-document types remain distinct | Trade Docs |
| Missing preference proof falls back according to rule rather than prohibiting automatically | Regulations |
| Import permit requirement determined from commodity/origin/use/time | Regulations |
| Permit documentary representation versioned | Trade Docs |
| Permit revocation/expiry triggers reassessment | Cross-engine |
| Customs declaration requirement determined | Regulations |
| CustomsDeclaration workflow/submission managed | Trade Docs |
| Authority acknowledgement/rejection captured | Trade Docs |
| Sovereign release not manufactured by either engine | Architecture invariant |
| Shipment hold/release action remains Trade/TMS-owned | Trade/TMS |
| Duty/VAT accounting remains ERP/Ledger-owned | ERP/Ledger |
| Pulse can analyse events without entering the synchronous critical path | Pulse |

---

# 1AB. Revised Realistic ZuriBeans Flow

~~~mermaid
sequenceDiagram
    participant T as ZuriBeans / Trade
    participant CP as Control Plane
    participant R as Regulations
    participant D as Trade Docs
    participant A as Customs / Issuers
    participant ERP as ERP / Ledger

    T->>CP: resolve UG→ZA context + capabilities
    CP-->>T: trusted PlatformContext

    T->>R: shipment/product/value/route facts
    R->>R: classify + origin + SPS + tariff + requirements
    R-->>T: pre-flight RegulatoryDecision
    R-->>D: document/permit requirement references

    D->>A: obtain / submit / query where authorised
    A-->>D: issued document / acknowledgement / authority response
    D->>D: version + provenance + documentary verification
    D-->>R: document/version/verification references

    R->>R: evaluate documentary sufficiency
    R-->>T: refreshed RegulatoryDecision
    R-->>ERP: duty/VAT assessment where applicable
    T->>T: enforce shipment disposition
~~~

---

# 1AC. Updated Final Cross-Border Mental Model

~~~text
COMMERCIAL / SHIPMENT FACTS
          │
          ▼
      REGULATIONS
 classification / origin /
 tariff / SPS / requirements
          │
          ├──────────────┐
          │              │
          ▼              ▼
 DocumentRequirement   PermitRequirement
          │              │
          └──────┬───────┘
                 ▼
           TRADE DOCS
 document / version / dossier /
 declaration / submission /
 authority response
                 │
                 ▼
           documentary facts
                 │
                 ▼
           REGULATIONS
 requirement satisfaction /
 cross-border decision
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
      Trade     ERP       Pulse
      PEP    accounting  intelligence
~~~

The documentary principle is:

> **Regulations decides what documentary proof is legally required and whether the proof supplied is sufficient; Trade Docs owns the concrete documentary and Customs-workflow state used to answer that question.**

---

# 2. Why This ADR Exists

The preceding Regulations ADRs established:

```text
sources
→ interpretations
→ rules
→ applicability
→ BRIR
→ deterministic evaluation
→ decisions
→ events
→ assurance
→ Baobab platform integration.
```

`ADR-REG-0027` applies that architecture to the first serious vertical:

> **ZuriBeans exporting Ugandan coffee and vanilla into South Africa.**

This is deliberately narrow enough to implement and verify, but rich enough to exercise:

```text
multiple legal jurisdictions

multiple competent authorities

HS classification

preferential origin

customs valuation

SPS

licensing

certificates

transit

tax

temporal tariff schedules

document verification

cross-engine facts.
```

---

# 3. Cross-Border Trade Is Not One Rule

The canonical model SHALL reject:

```text
Coffee
+
Uganda
+
South Africa
=
one regulatory rule.
```

The actual regulatory relationship is closer to:

```text
PRODUCT
   │
   ├── physical form
   ├── processing state
   ├── species
   ├── intended use
   └── quantity/value
   │
   ▼
HS CLASSIFICATION
   │
   ├──────────────┐
   ▼              ▼
TARIFF       CONTROL MEASURES
   │              │
   ▼              ▼
ORIGIN           SPS
   │              │
   ▼              ▼
PREFERENCE      PERMIT
   │              │
   └───────┬──────┘
           ▼
       DOCUMENTS
           │
           ▼
       VALUATION
           │
           ▼
         TAXES
           │
           ▼
        RELEASE
```

---

# 4. The Initial Product Family Is Not Just “Coffee”

For customs purposes, materially different product states already exist.

The current South African Schedule 1 identifies, among others:

| Product state | South African tariff classification |
|---|---|
| Green Arabica, not decaffeinated | `0901.11.10` |
| Green Robusta, not decaffeinated | `0901.11.20` |
| Other green coffee, not decaffeinated | `0901.11.90` |
| Roasted coffee, not decaffeinated | `0901.21` |
| Roasted coffee, decaffeinated | `0901.22` |
| Coffee husks and skins | `0901.90.10` |
| Coffee substitutes containing coffee | `0901.90.20` |

Under the current SARS tariff schedule, unroasted Arabica and Robusta are duty-free under both the general and AfCFTA columns. Roasted coffee currently carries a general duty of `6c/kg` and an AfCFTA rate of `2.4c/kg`; coffee husks and skins currently show `20%` general and `8%` AfCFTA. :chatgpt-content-reference{index="0"}

This immediately demonstrates why:

```text
product = coffee
```

is not sufficient regulatory context.

---

# 5. Vanilla Is Also Form-Sensitive

The current South African tariff schedule separately identifies:

```text
0905.10
Vanilla — neither crushed nor ground

0905.20
Vanilla — crushed or ground
```

Both currently show duty-free treatment in the general and AfCFTA columns. :chatgpt-content-reference{index="1"}

Therefore ZuriBeans product modelling MUST preserve distinctions such as:

```text
vanilla pods

crushed vanilla

ground vanilla

vanilla extract
```

because vanilla extract may cease to fall under heading `09.05`; the current tariff, for example, separately contains vanilla oleoresin under another heading. :chatgpt-content-reference{index="2"}

---

# 6. Canonical Product Identity ≠ Customs Classification

Hard invariant:

```text
CommercialProduct
≠
HSClassification.
```

Example:

```text
Commercial product:
ZuriBeans Mt Elgon Arabica AA 60kg

Customs classification candidate:
0901.11.10
```

---

# 7. HS Classification Is a Regulatory Determination

SARS explicitly states that all commercial import/export transactions require tariff classification and that classification affects not only the applicable duty but also matters including import controls, rules of origin and rebate provisions. :chatgpt-content-reference{index="3"}

Accordingly:

# `RegulatoryClassification`

SHALL be a first-class Regulations aggregate.

Conceptually:

```text
RegulatoryClassification
├── classification_id
├── subject_ref
├── nomenclature
├── nomenclature_version
├── jurisdiction
├── heading
├── subheading
├── national_tariff_line?
├── description
├── statistical_unit?
├── classification_facts[]
├── legal_basis_refs[]
├── determination_method
├── assurance_state
├── valid_time
├── knowledge_time
└── provenance
```

---

# 8. Never Infer HS from Product Name Alone

Rejected:

```text
if "coffee" in product.name:
    hs = 0901
```

Classification SHALL consider facts such as:

```text
species

roasted/unroasted

decaffeinated/non-decaffeinated

whole/crushed/ground

extract versus raw commodity

processing

composition.
```

---

# 9. HS Candidate ≠ Verified Classification

Haystack/LLM may propose:

```text
0901.11.10
```

OPA SHALL NOT turn that candidate into an E3/E4 regulatory decision until the classification reaches the necessary assurance state.

---

# 10. Classification Version Matters

South Africa's tariff schedules are continuously amended. SARS's Schedule 1 page records Part 1 as updated on 28 August 2026, while SARS maintains a separate 2026 tariff-amendment history. :chatgpt-content-reference{index="4"}

Therefore:

```text
HS code
+
jurisdiction
```

is insufficient.

Baobab needs:

```text
tariff nomenclature version

tariff schedule version

effective date.
```

---

# 11. Classification SHALL Drive, Not Contain, Other Rules

Avoid:

```text
HSClassification {
    duty_rate
    permit_required
    phytosanitary_required
}
```

Instead:

```text
HSClassification
       │
       ├──► TariffRule
       ├──► ImportControlRule
       ├──► SPSRule
       ├──► OriginRule
       └──► StatisticalRule
```

This keeps independently changing legal instruments independently versioned.

---

# 12. Origin Is Separate from Classification

Hard invariant:

```text
HS classification
≠
country of origin.
```

---

# 13. Origin Is Also Separate from Shipment Origin

```text
CountryOfOrigin
≠
CountryOfDispatch
≠
CountryOfExport
≠
ShipmentOrigin.
```

A coffee consignment might:

```text
grow in Uganda
be warehoused in Kenya
depart from Mombasa
enter South Africa
```

without Kenya becoming the commodity's origin.

---

# 14. AfCFTA Origin Architecture

The AfCFTA Rules of Origin provide that a product can qualify as originating when it is wholly obtained in a State Party or satisfies the applicable substantial-transformation conditions. The Rules of Origin Manual specifically identifies plants and plant products grown or harvested in a State Party among the wholly obtained categories. :chatgpt-content-reference{index="5"}

That makes the pilot particularly suitable for origin reasoning.

For Ugandan-grown:

```text
coffee

vanilla
```

a **wholly obtained** origin pathway is the obvious rule family to test, subject to verified facts and the applicable AfCFTA instruments.

---

# 15. OriginClaim

Baobab SHALL represent:

```text
OriginClaim
├── product_ref
├── claimed_country
├── origin_regime
├── origin_criterion
├── producer_refs[]
├── harvest/production facts
├── non_originating_materials?
├── supporting_evidence[]
├── verification_state
└── provenance
```

---

# 16. Preferential Origin Is a Decision

Never:

```text
country = Uganda
→ AfCFTA duty automatically.
```

Instead:

```text
State Party eligibility
        +
Applicable tariff concession
        +
Origin rule satisfied
        +
Proof of origin valid
        +
Direct transport / transit requirements
        +
Claim made correctly
        =
Preferential treatment eligibility.
```

---

# 17. AfCFTA Preference Is Currently Relevant to This Corridor

South Africa states that preferential AfCFTA trade is available only with countries that have implemented the relevant preferential arrangements, including ratification and gazetting/domestication of tariff schedules. The Department of Trade, Industry and Competition listed Uganda among the countries whose schedules had been gazetted as of October 2024. :chatgpt-content-reference{index="6"}

The current SARS tariff book itself includes an AfCFTA duty column. :chatgpt-content-reference{index="7"}

Baobab SHALL nevertheless evaluate the claim dynamically rather than treating:

```text
UG → ZA
```

as permanently preference-eligible.

---

# 18. Why This Still Matters for Duty-Free Green Coffee

Current green coffee lines already show:

```text
General = free
AfCFTA = free.
``` :chatgpt-content-reference{index="8"}


Therefore, for those lines:

```text
AfCFTA preference
```

may presently produce no customs-duty saving.

That does NOT make origin modelling irrelevant.

Origin remains relevant to:

```text
preference for other products

future tariff changes

origin declarations

traceability

trade statistics

regime-specific obligations

customer evidence

audit.
```

---

# 19. Roasted Coffee Demonstrates the Difference

Current:

```text
0901.21

General:
6c/kg

AfCFTA:
2.4c/kg
``` :chatgpt-content-reference{index="9"}


Thus:

```text
classification
+
origin qualification
+
preference claim
```

can alter the applicable duty.

---

# 20. Proof of Origin Is Separate from Origin

Hard invariant:

```text
Product is originating
≠
required proof has been supplied.
```

---

# 21. AfCFTA Proof of Origin

The AfCFTA Rules of Origin Manual states that qualifying originating goods receive preferential treatment on submission of the prescribed proof of origin; it also states a normal twelve-month validity period for proof of origin. :chatgpt-content-reference{index="10"}

Therefore Baobab SHALL separately assess:

```text
OriginStatus

OriginEvidenceStatus.
```

---

# 22. Origin Evidence Types

Potential:

```text
AFCFTA_CERTIFICATE_OF_ORIGIN

AFCFTA_ORIGIN_DECLARATION

PRODUCER_DECLARATION

SUPPLIER_DECLARATION

HARVEST_RECORD

FARM_TRACEABILITY_RECORD

CUSTOMS_SUPPORTING_DOCUMENT.
```

---

# 23. ICO Certificate of Origin ≠ AfCFTA Certificate of Origin

This distinction is critical for coffee.

Uganda's Trade Portal identifies coffee quality and International Coffee Organization certificate-of-origin procedures for coffee exports. :chatgpt-content-reference{index="11"}

That document SHALL NOT be semantically conflated with:

```text
AfCFTA Certificate of Origin
```

used to support preferential customs origin.

Canonical document types SHALL therefore distinguish:

```text
ICO_COFFEE_CERTIFICATE_OF_ORIGIN

AFCFTA_CERTIFICATE_OF_ORIGIN

NON_PREFERENTIAL_CERTIFICATE_OF_ORIGIN.
```

---

# 24. Neither Is a Phytosanitary Certificate

Likewise:

```text
Certificate of Origin
≠
Phytosanitary Certificate
≠
Quality Certificate.
```

---

# 25. Documentary Purpose Must Be Explicit

> **RTD-03 amendment:** Regulations owns the regulatory purpose and criteria below. The concrete TradeDocument / DocumentVersion that carries these facts is owned by Trade Docs.

Every **DocumentRequirement and RegulatoryEvidenceAssessment** SHALL identify, where material:

```text
required document type / purpose

legal purpose

acceptable issuer criteria

subject

consignment scope

regulatory validity criteria

jurisdiction

regime

evidence relationships

legal basis.
```

Trade Docs SHALL preserve the concrete document's issuer claim, version, lifecycle and documentary verification facts.

---

# 26. Direct Transportation and Transit

Uganda is landlocked.

A naïve rule:

```text
Uganda product
must physically travel
Uganda → South Africa directly
```

would be commercially nonsensical.

The AfCFTA Rules of Origin Manual permits qualifying consignments to transit other State Parties or third countries under the prescribed conditions, including remaining under customs supervision. :chatgpt-content-reference{index="12"}

---

# 27. Trade Route Must Therefore Be Modelled

```text
TradeRoute
├── origin
├── export_exit
├── transit_legs[]
├── transshipment_points[]
├── import_entry
└── destination
```

---

# 28. TransitLeg

```text
TransitLeg
├── jurisdiction
├── customs_regime
├── entry_point
├── exit_point
├── carrier
├── transport_document_ref
├── customs_control_state
├── seal/container refs?
└── evidence
```

---

# 29. Direct-Transport Assessment

```text
Originating Product
        │
        ▼
Transit Route
        │
        ├── remained under customs control?
        ├── prohibited processing?
        ├── preservation only?
        └── supporting transport evidence?
        │
        ▼
Origin Preference Transit Status
```

---

# 30. Transit Rules Are Not Fully Defined by This Pilot ADR

Detailed:

```text
Tanzania

Kenya

Zambia

Zimbabwe

Mozambique

other transit-state
```

requirements SHALL be added as jurisdiction profiles when actual routes are selected.

Do not invent them from geography.

---

# 31. Uganda Exporter Eligibility — Coffee

Uganda's current Trade Portal states that a trader wishing to export coffee requires an annual coffee export licence issued by the Ministry of Agriculture, Animal Industry and Fisheries' Department of Coffee Development. The relevant procedure was updated in August 2026. :chatgpt-content-reference{index="13"}

Therefore coffee exports require an exporter-level rule family distinct from consignment rules.

---

# 32. Exporter-Level versus Consignment-Level Requirements

Example:

```text
EXPORTER LEVEL
────────────────
Coffee export licence


CONSIGNMENT LEVEL
────────────────
Phytosanitary certificate
Quality certificate
Origin documentation
Commercial invoice
Packing list
Customs declaration
Transport documents.
```

---

# 33. Authority Identity Must Be Temporal

The Uganda Trade Portal currently contains mixed institutional wording: newer operational records identify the **MAAIF Department of Coffee Development**, while some descriptive text still retains references to the former UCDA terminology. :chatgpt-content-reference{index="14"}

This is not a reason for Baobab to guess.

It is evidence for the architecture already established in ADR-REG-0011/0015:

```text
RegulatoryAuthority

AuthorityVersion

SourceCurrentness

effective time

knowledge time.
```

---

# 34. Never Hard-Code Agency Names Into Rules

Rejected:

```python
issuer == "Uganda Coffee Development Authority"
```

Prefer:

```text
authority_ref =
UG_COFFEE_COMPETENT_AUTHORITY

resolved at legal_time.
```

---

# 35. Uganda Phytosanitary Authority

Uganda's Ministry of Agriculture identifies its National Plant Protection Organization as the Department of Crop Inspection and Certification and operates electronic phytosanitary certification through ePhyto. :chatgpt-content-reference{index="15"}

---

# 36. Uganda Export Phytosanitary Requirement

The Uganda Trade Portal currently states that traders require a phytosanitary certificate for every consignment of fresh and dry produce for export; the certificate confirms compliance with the importing country's requirements. :chatgpt-content-reference{index="16"}

For the pilot, phytosanitary applicability SHALL therefore be evaluated against the precise commodity condition rather than inferred merely from:

```text
product category = agricultural.
```

---

# 37. Export NPPO and Import NPPO Form a Regulatory Chain

```text
South African
import conditions
        │
        ▼
communicated to exporter
        │
        ▼
Uganda NPPO
inspection/certification
        │
        ▼
Phytosanitary Certificate
        │
        ▼
South African NPPO
entry verification.
```

---

# 38. South African Plant-Health Import Controls

The South African government states that imports of plants, plant products and regulated articles may require an NPPOZA import permit. If the commodity is not exempt, the importer must obtain the permit; the exporter receives the permit conditions, the exporting country's NPPO verifies compliance and issues the phytosanitary certificate, and South African inspectors inspect the goods and certificate before customs release. :chatgpt-content-reference{index="17"}

---

# 39. Do Not Implement `plant_product → permit required`

Incorrect:

```text
if plant_product:
    require import permit
```

Correct:

```text
commodity
+
physical condition
+
origin
+
intended use
+
current exemption
+
current import protocol
+
legal time
→ permit requirement.
```

---

# 40. Commodity-Specific SPS Conditions Require Further Acquisition

This ADR establishes the **architecture and initial verified corridor facts**.

It does NOT assert that every form of:

```text
green coffee

roasted coffee

vanilla pods

ground vanilla
```

has identical South African plant-health treatment.

The exact NPPOZA commodity import condition / exemption SHALL be obtained, versioned and verified during jurisdiction-pack implementation.

Until then:

```text
SPS coverage gap
```

may yield:

```text
INDETERMINATE
```

rather than assumed admissibility.

---

# 41. SPS Status Is Independent from Customs Duty

Example:

```text
customs duty = free
```

does NOT imply:

```text
plant health = satisfied.
```

---

# 42. And Vice Versa

A valid:

```text
Phytosanitary Certificate
```

does not establish:

```text
correct tariff classification

origin preference

customs value

VAT payment.
```

---

# 43. South African Importer Registration

SARS states that persons importing goods into South Africa must generally register as importers; foreign importers are required to nominate a registered agent in South Africa before registration. :chatgpt-content-reference{index="18"}

This SHALL be represented as an importer/entity eligibility rule.

---

# 44. Importer Registration Is Not Per-Consignment Evidence

It is reusable regulatory standing.

Conceptually:

```text
RegulatoryRegistration
├── legal_entity_ref
├── registration_type
├── authority_ref
├── registration_number
├── status
├── valid_from
├── valid_until?
└── verification
```

---

# 45. Customs Declaration

SARS requires importers/exporters or their agents to lodge a Goods Declaration unless specifically exempted. :chatgpt-content-reference{index="19"}

---

# 46. 2026 South African Declaration Changes

SARS updated its goods-declaration requirements on 14 August 2026, including mandatory electronic invoice data and worksheet requirements. :chatgpt-content-reference{index="20"}

This is precisely why documentary requirements SHALL be:

```text
versioned

effective-dated

source-backed.
```

---

# 47. Customs Documentation Is Not a Static Checklist

Rejected:

```text
required_docs = [
  "invoice",
  "packing list",
  "certificate"
]
```

Instead:

```text
DocumentRequirement
├── document_type
├── applicability
├── issuer constraints
├── timing
├── validity
├── format
├── original/copy/electronic
├── data requirements
├── condition
└── legal basis
```

---

# 48. Uganda Customs Export Procedure

Uganda Revenue Authority currently describes export clearance as requiring applicable permits and documents, potentially including export licences, invoices, packing lists and certificates of origin; exporters use licensed clearing agents and electronic customs declaration through ASYCUDA World, with inspection possible before release. :chatgpt-content-reference{index="21"}

---

# 49. Initial Documentary Families

The initial profile SHALL support at least:

| Family | Example |
|---|---|
| Commercial | Commercial invoice |
| Packing | Packing list |
| Transport | Bill of lading / airway bill / road consignment note |
| Export authorisation | Coffee export licence |
| Quality | Coffee quality certificate |
| Commodity-specific international | ICO coffee certificate |
| SPS | Phytosanitary certificate |
| Preferential origin | AfCFTA Certificate/Declaration of Origin |
| Non-preferential origin | Relevant certificate where required |
| Customs | Uganda export declaration |
| Customs | South African import declaration |
| Import-control | NPPOZA import permit where applicable |
| Financial | Customs-duty/VAT assessment evidence |

---

# 50. Certificate Graph

```text
Consignment
    │
    ├── Commercial Invoice
    │
    ├── Packing List
    │
    ├── Transport Document
    │
    ├── Coffee Export Licence
    │
    ├── Coffee Quality Certificate
    │
    ├── ICO Certificate
    │
    ├── Phytosanitary Certificate
    │
    ├── AfCFTA Origin Proof
    │
    ├── Plant Import Permit?
    │
    ├── UG Export Declaration
    │
    └── ZA Import Declaration
```

No edge implies equivalence.

---

# 51. Evidence Scope Matters

Example:

```text
Coffee export licence
```

may cover:

```text
exporter
+
licence period
```

whereas:

```text
phytosanitary certificate
```

usually applies to:

```text
specific consignment.
```

---

# 52. Document Validity Must Be Contextual

A document can be:

```text
authentic
```

but:

```text
expired

wrong commodity

wrong consignment

wrong issuer

wrong destination

wrong quantity.
```

Therefore:

```text
DocumentAuthenticity
≠
RequirementSatisfaction.
```

---

# 53. Customs Valuation Is Another Independent Rule Family

SARS describes six customs-valuation methods applied hierarchically, beginning with transaction value where applicable. :chatgpt-content-reference{index="22"}

Therefore:

```text
invoice amount
≠
automatically customs value.
```

---

# 54. CustomsValuationAssessment

```text
CustomsValuationAssessment
├── jurisdiction
├── method
├── transaction_price
├── additions[]
├── deductions[]
├── currency
├── exchange_rate
├── customs_value
├── evidence[]
├── legal_basis[]
└── provenance
```

---

# 55. Incoterms Are Facts, Not Valuation Rules

An:

```text
FOB

CIF

CFR
```

term provides relevant commercial facts.

The customs valuation engine still applies the legally prescribed method.

---

# 56. Value and Classification Combine at Duty Calculation

```text
Customs Value
      +
Tariff Classification
      +
Applicable Tariff Schedule
      +
Preference Eligibility
      +
Quantity where specific rate
      =
Customs Duty
```

---

# 57. Tariff Rate Type Must Be First Class

Support:

```text
AD_VALOREM

SPECIFIC

COMPOUND

MIXED

FREE

QUOTA

SAFEGUARD

ANTI_DUMPING

COUNTERVAILING.
```

---

# 58. `FREE` Is a Legal Rate

Do not encode:

```text
rate = null
```

for duty-free treatment.

Use:

```text
rate_type = FREE
```

with tariff provenance.

---

# 59. Import VAT Is Independent of Customs Duty

Even where:

```text
customs duty = free
```

South African import VAT may still arise.

---

# 60. Current South African Import VAT Example

SARS currently states the VAT rate on imported goods is 15%. For goods imported from outside the BLNS/SACU customs area, its published calculation adds 10% of customs value to the Added Tax Value before applying VAT, plus applicable non-rebated duty. Uganda is outside that BLNS exception. :chatgpt-content-reference{index="23"}

For the current pilot, conceptually:

```text
Customs Value
       +
10% uplift
       +
non-rebated duty
       =
Added Tax Value

Added Tax Value
       ×
15%
       =
Import VAT
```

The rate and formula SHALL be stored as effective-dated regulatory rules, not application constants.

---

# 61. Never Hardcode `0.15`

Rejected:

```python
vat = value * 1.15
```

---

# 62. Duty ≠ VAT ≠ Fee

Canonical types SHALL distinguish:

```text
CUSTOMS_DUTY

IMPORT_VAT

LEVY

INSPECTION_FEE

PERMIT_FEE

ANTI_DUMPING_DUTY

OTHER_BORDER_CHARGE.
```

---

# 63. Tax Assessment versus Financial Posting

Regulations determines:

```text
applicable formula

regulatory amount/basis

legal provenance.
```

ERP/Ledger owns:

```text
posting

payment

settlement

accounting treatment.
```

---

# 64. Trade Agreement Eligibility Is Independent from Rate Retrieval

Incorrect:

```text
get AfCFTA rate
→ therefore use it.
```

Correct:

```text
retrieve rates
        │
        ▼
determine regime availability
        │
        ▼
determine origin
        │
        ▼
verify proof
        │
        ▼
verify transport conditions
        │
        ▼
select legally applicable rate.
```

---

# 65. TariffRate

```text
TariffRate
├── jurisdiction
├── tariff_line
├── regime
├── rate_type
├── rate
├── unit?
├── valid_from
├── valid_to?
├── source_ref
└── provenance
```

---

# 66. PreferentialTariffAssessment

```text
PreferentialTariffAssessment
├── trade_regime
├── exporter_state
├── importer_state
├── tariff_line
├── schedule_eligibility
├── origin_status
├── proof_status
├── direct_transport_status
├── preference_status
├── selected_rate_ref?
└── reasons[]
```

---

# 67. No Preference Claim

A trader may decline to claim preference.

Therefore:

```text
ELIGIBLE_FOR_PREFERENCE
```

and:

```text
PREFERENCE_CLAIMED
```

are separate.

---

# 68. Most-Favoured-Nation/General Rate Fallback

Where preference:

```text
does not apply

cannot be proved

is not claimed
```

the applicable non-preferential tariff treatment SHALL be determined independently.

---

# 69. Failure to Prove Origin Does Not Reclassify Product

Hard invariant.

---

# 70. Failure to Prove Origin Does Not Mean Product Is Prohibited

It may simply change:

```text
tariff treatment.
```

---

# 71. SPS Failure May Be More Consequential

If plant-health admission requires a valid condition and evidence is absent, the import may be:

```text
UNSATISFIED

PROHIBITED

INDETERMINATE
```

depending on the applicable legal rule.

---

# 72. Regulatory Stages

Baobab SHALL model cross-border evaluation through stage-specific assessments:

```text
1. ExporterEligibilityAssessment

2. ProductClassificationAssessment

3. OriginAssessment

4. PreferenceAssessment

5. ExportControlAssessment

6. ExportSPSAssessment

7. DocumentationAssessment

8. TransitAssessment

9. ImportControlAssessment

10. ImportSPSAssessment

11. CustomsValuationAssessment

12. CustomsDutyAssessment

13. ImportTaxAssessment

14. CustomsDeclarationAssessment

15. BorderReleaseReadinessAssessment.
```

---

# 73. Composite Decision

# `CrossBorderRegulatoryDecision`

Conceptually:

```text
CrossBorderRegulatoryDecision
├── decision_id
├── trade_context_ref
├── stage_assessments[]
├── requirements[]
├── prohibitions[]
├── unknowns[]
├── coverage_gaps[]
├── overall_outcome
├── maximum_effect_class
├── recommended_disposition
├── legal_time
├── ruleset_ref
└── provenance
```

---

# 74. Composition Is Not Boolean AND

Some failed requirements:

```text
prevent export
```

others:

```text
prevent preference only
```

others:

```text
create payment obligation.
```

Therefore stage semantics matter.

---

# 75. Example

```text
AfCFTA proof missing
```

might yield:

```text
PreferenceAssessment:
UNSATISFIED

CustomsImportAssessment:
SATISFIED_WITH_REQUIREMENTS

Duty:
general rate applies
```

rather than:

```text
whole shipment prohibited.
```

---

# 76. Another Example

```text
mandatory phytosanitary certificate missing
```

may prevent admissibility.

Very different consequence.

---

# 77. Operational Dispositions

Potential recommendations:

```text
PROCEED

PROCEED_WITH_REQUIREMENTS

OBTAIN_DOCUMENT

OBTAIN_PERMIT

CORRECT_DECLARATION

PAY_DUTY

PAY_TAX

CUSTOMS_REVIEW

SPS_HOLD

REGULATORY_REVIEW

DO_NOT_SHIP

DO_NOT_RELEASE.
```

The actual operational transition remains with Trade/ERP/other PEPs.

---

# 78. Cross-Border Regulatory Context

Extend ADR-REG-0017/0026 with:

```text
CrossBorderTradeContext
├── tenant_ref
├── exporter_legal_entity_ref
├── importer_legal_entity_ref
├── seller_ref
├── buyer_ref
│
├── commercial_product_ref
├── regulatory_classification_refs[]
│
├── country_of_origin
├── export_jurisdiction
├── transit_jurisdictions[]
├── import_jurisdiction
├── destination
│
├── market_participation_refs[]
├── trade_lane_ref
│
├── quantity
├── unit
├── transaction_value
├── currency
├── incoterm
│
├── shipment_ref
├── route
├── transport_mode
│
├── planned_export_at
├── planned_import_at
├── legal_time
│
├── evidence_refs[]
└── fact_snapshot_ref
```

---

# 79. Transaction Time Is Multi-Point

A cross-border transaction may require:

```text
contract date

export declaration date

shipment date

border crossing

import declaration date

release date.
```

Different rules may evaluate at different legal times.

---

# 80. Do Not Use One `transaction_date`

---

# 81. Product Transformation During Trade

If goods change from:

```text
green coffee
```

to:

```text
roasted coffee
```

before import, classification and potentially origin treatment may change.

The regulatory subject must describe the goods at the relevant customs event.

---

# 82. Customs Classification and Commercial SKU Lifecycle

```text
SKU
  │
  ├── raw state
  ├── processed state
  └── packaged state
        │
        ▼
Regulatory Product Variant
        │
        ▼
Classification.
```

---

# 83. Current Pilot Facts — Verified versus To Be Verified

| Matter | Pilot status |
|---|---|
| Green Arabica SA tariff line `0901.11.10` | Current official SARS schedule |
| Green Robusta SA tariff line `0901.11.20` | Current official SARS schedule |
| Green coffee current duty | Free |
| Roasted coffee current general duty | `6c/kg` |
| Roasted coffee current AfCFTA tariff column | `2.4c/kg` |
| Vanilla `0905.10` / `0905.20` | Current official SARS schedule |
| Vanilla current duty | Free |
| Uganda coffee exporter licence | Current official Uganda Trade Portal procedure |
| Uganda NPPO / ePhyto | Current MAAIF source |
| Uganda fresh/dry produce phytosanitary requirement | Current Trade Portal operational source |
| South African plant import permit framework | Current government/NPPO source |
| Commodity-specific ZA coffee/vanilla SPS protocol | **Must be acquired and verified** |
| AfCFTA origin framework | Verified official AU framework |
| Ugandan-grown plant “wholly obtained” pathway | Supported by AfCFTA origin rules, subject to product facts |
| Specific AfCFTA proof for transaction | Must be supplied/verified |
| Transit-state requirements | Route-specific; not yet modelled |
| SA importer registration | Current SARS requirement |
| SA customs declaration | Current SARS requirement |
| SA import VAT rate/formula | Current SARS operational guidance |

---

# 84. This Table Is Not the Rule Database

The implementation SHALL acquire the underlying authoritative artefacts into ADR-REG-0011 through ADR-REG-0015 source/provenance infrastructure.

---

# 85. Source Families for the Pilot

Initial source adapters should cover:

```text
South African Revenue Service

South African Department of Agriculture / NPPOZA

Uganda Revenue Authority

Uganda Ministry of Agriculture, Animal Industry and Fisheries

Uganda Trade Information Portal

African Union / AfCFTA Secretariat

applicable official Gazettes

applicable customs/tariff schedules.
```

---

# 86. Source Priority Is Purpose-Specific

Example:

```text
tariff rate
→ SARS tariff schedule

Uganda phytosanitary issuer
→ MAAIF

AfCFTA origin semantics
→ AfCFTA legal instruments

operational procedure
→ relevant official trade portal / authority procedure.
```

---

# 87. Do Not Treat Trade Portal Procedure as Statute

Trade portals are highly valuable operational sources.

But:

```text
procedure
≠
underlying legal instrument.
```

Consequential rules SHOULD retain links to both where practical.

---

# 88. Mixed/Stale Portal Content Is Expected

The Uganda coffee material illustrates precisely why Regulations needs:

```text
source versioning

currentness

authority resolution

cross-source corroboration.
```

It SHALL not quietly rewrite history to hide institutional changes.

---

# 89. Data Architecture

Canonical structured regulatory state:

```text
PostgreSQL 17
```

shall contain:

```text
TariffLine

TariffRate

OriginRule

OriginClaim

PreferenceAssessment

SPSRule

PermitRequirement

DocumentRequirement

CustomsValuationRule

TaxRule

TradeProfile

TradeRegulatoryDecision.
```

---

# 90. Qdrant Boundary

Qdrant MAY support retrieval of:

```text
tariff explanatory material

permit guidance

legal provisions

SPS protocols

historical notices.
```

Qdrant SHALL NOT be canonical storage of:

```text
applicable duty rate

verified HS classification

RegulatoryDecision.
```

---

# 91. Haystack Boundary

Haystack MAY:

```text
retrieve source material

identify candidate tariff provisions

extract permit conditions

find amendment relationships.
```

It SHALL NOT select the legally effective tariff rate for E3/E4 execution without canonical promotion.

---

# 92. LangGraph Boundary

LangGraph MAY govern:

```text
classification review

source verification

SPS rule review

new tariff-version publication

jurisdiction-pack certification.
```

---

# 93. OPA Boundary

OPA is suitable for deterministic published conditions such as:

```text
classification condition

origin rule

proof validity

permit requirement

deadline

tariff selection

document completeness

tax formula applicability.
```

---

# 94. OPA Does Not Perform Source Discovery

---

# 95. OPA Does Not Decide HS Using LLM Semantics

It may execute already verified classification criteria.

---

# 96. Trade Integration

`baobab-trade` supplies:

```text
product

order

shipment

seller/buyer

quantity

price

Incoterm

route

dates.
```

---


# 96A. Trade Docs Integration — RTD-03

Baobab Trade Docs supplies documentary and Customs-workflow facts such as:

~~~text
TradeDocument reference
DocumentVersion reference
document type
issuer claim
issuer verification facts
issued / expiry / revocation facts
consignment association
document dossier
CustomsCase reference
CustomsDeclaration workflow reference
submission reference
authority-response reference
~~~

Regulations consumes those facts to determine:

~~~text
DocumentRequirement satisfaction
PermitRequirement satisfaction
OriginEvidenceStatus
SPS evidence sufficiency
Customs documentary readiness
RegulatoryDecision
~~~

Trade Docs SHALL not calculate legal applicability merely because it stores the document.

Regulations SHALL not create or mutate the TradeDocument lifecycle merely because it evaluates the document.

---

# 96B. Requirement-to-Document Choreography

~~~mermaid
sequenceDiagram
    participant R as Regulations
    participant D as Trade Docs

    R-->>D: DocumentRequirement / PermitRequirement
    D->>D: obtain/create/version/verify document
    D-->>R: DocumentVersion + verification facts
    R->>R: evaluate legal sufficiency
    R-->>D: requirement-satisfaction / decision reference where workflow needs it
~~~

---

# 97. Regulations Returns

Regulations returns **normative decisions and requirements**, not concrete document instances.

```text
classification decision

DocumentRequirement references/specifications

PermitRequirement references/specifications

origin status

SPS requirements

tariff assessment

tax assessment

requirement-satisfaction results

release-readiness recommendation.
```

Concrete TradeDocument / DocumentVersion objects are resolved from Trade Docs.

---

# 98. Trade Acts as PEP

Example:

```text
Regulations:
SPS_HOLD

Trade:
shipment.status =
REGULATORY_HOLD
```

according to Trade's own controlled workflow.

---

# 99. ERP Integration

ERP/Ledger consumes:

```text
customs duty assessment

import VAT assessment

fees.
```

It owns payment/accounting.

---

# 100. Pulse Integration

Pulse may consume:

```text
tariff changed

permit process changed

regulatory restriction introduced

origin preference changed.
```

It may produce:

```text
cost impact

margin risk

supply-chain opportunity.
```

---

# 101. Pulse Shall Not Recalculate Legal Duty

The verified tariff assessment comes from Regulations.

---

# 102. CMS Integration

CMS may publish:

```text
“How to import Ugandan coffee into South Africa”
```

derived from verified regulatory projections.

But the article is not the executable rule.

---

# 103. Classification Changes Are Material Events

Potential:

```text
regulations.classification.superseded

regulations.tariff-rate.changed

regulations.origin-rule.changed

regulations.sps-requirement.changed

regulations.permit-requirement.changed

regulations.document-requirement.changed.
```

---

# 104. Tariff Change Impact

```text
TariffRate changed
      │
      ▼
Find active/future shipments
      │
      ▼
Recalculate border cost
      │
      ▼
DecisionDiff
      │
      ▼
Trade / ERP / Pulse.
```

---

# 105. SPS Change Impact

```text
new permit condition
      │
      ▼
Find future consignments
      │
      ▼
Reassess documentation
      │
      ▼
missing permit?
      │
      ▼
SPS_HOLD / REVIEW.
```

---

# 106. Origin Rule Change Impact

May invalidate:

```text
preference claim
```

without making:

```text
commodity prohibited.
```

---

# 107. Testing Architecture

ADR-REG-0025 SHALL establish golden cases for the corridor.

Minimum initial cases include:

```text
Ugandan green Arabica → ZA

Ugandan green Robusta → ZA

Ugandan roasted coffee → ZA

Ugandan vanilla pods → ZA

crushed/ground vanilla → ZA

valid origin proof

missing origin proof

valid phytosanitary certificate

missing phytosanitary certificate

import permit required and present

import permit required and absent

permit exemption verified

unknown SPS coverage

direct route

third-country transit under customs control

origin evidence failure

wrong HS classification

general versus AfCFTA duty

customs value adjustment

import VAT calculation.
```

---

# 108. Golden Case — Green Arabica

Given:

```text
commodity:
green Arabica coffee

classification:
0901.11.10

origin:
Uganda

import:
South Africa

tariff legal time:
2026-09-29
```

the current South African tariff result should identify:

```text
general customs duty:
FREE

AfCFTA tariff:
FREE.
``` :chatgpt-content-reference{index="24"}


---

# 109. Golden Case — Green Robusta

```text
classification:
0901.11.20

general:
FREE

AfCFTA:
FREE.
``` :chatgpt-content-reference{index="25"}


---

# 110. Golden Case — Roasted Coffee

```text
classification:
0901.21

general:
6c/kg

AfCFTA tariff column:
2.4c/kg.
``` :chatgpt-content-reference{index="26"}


Test variants SHALL cover:

```text
qualifying AfCFTA origin

non-qualifying origin

missing proof.
```

---

# 111. Golden Case — Vanilla Pod

```text
classification:
0905.10

current general duty:
FREE

current AfCFTA:
FREE.
``` :chatgpt-content-reference{index="27"}


---

# 112. Golden Case — Wrong Product State

Input:

```text
vanilla extract
```

MUST NOT automatically classify as:

```text
0905.10.
```

---

# 113. Golden Case — Missing Preferential Origin Proof

For roasted coffee:

```text
origin potentially qualifies

proof unavailable.
```

Expected:

```text
origin factual assessment:
potentially satisfied

preference evidence:
UNSATISFIED

preferential tariff claim:
not established

fallback:
evaluate general tariff.
```

Not:

```text
PROHIBITED.
```

---

# 114. Golden Case — Missing SPS Evidence

Where verified commodity rule requires a phytosanitary certificate:

```text
certificate absent
```

must result in the appropriate:

```text
UNSATISFIED / HOLD
```

rather than merely falling back to another tariff.

---

# 115. Golden Case — Unknown SPS Protocol

If Baobab has not yet verified whether a specific processed commodity is permit-exempt:

```text
SPS outcome =
INDETERMINATE.
```

No guessing.

---

# 116. Golden Case — Import VAT

For a Uganda-origin import, test the currently published South African import-VAT calculation using:

```text
customs value
+
10% customs-value uplift
+
applicable duty

×
15%.
``` :chatgpt-content-reference{index="28"}


The fixture SHALL pin the exact tax-rule version used.

---

# 117. Golden Case — Transit

Ugandan originating commodity:

```text
UG
→ third country transit
→ ZA
```

with goods remaining under customs control.

The AfCFTA direct-transport condition SHALL remain potentially satisfiable rather than failing solely because the goods crossed a third territory. :chatgpt-content-reference{index="29"}

---

# 118. Regulatory Profile

Baobab SHALL define:

# `CrossBorderRegulatoryProfile`

```text
CrossBorderRegulatoryProfile
├── profile_id
├── origin_market/jurisdiction
├── destination_market/jurisdiction
├── trade_direction
├── commodity_scope[]
├── regulatory_domains[]
├── source_manifest
├── coverage_manifest
├── RuleSet refs[]
├── golden_suite_ref
├── known_gaps[]
├── assurance_state
├── maximum_effect_class
├── valid_from
└── version
```

---

# 119. Initial Profile

Conceptually:

```text
REG-PROFILE-UG-ZA-AGRI-001

Origin:
Uganda

Destination:
South Africa

Products:
coffee
vanilla

Domains:
export eligibility
classification
origin
AfCFTA preference
customs
SPS
plant health
documents
valuation
duty
VAT
```

---

# 120. Product Coverage SHALL Be Explicit

Do not say merely:

```text
coffee supported.
```

Say:

```text
green Arabica

green Robusta

roasted coffee

coffee husks?
```

with separate assurance status.

Likewise:

```text
whole vanilla pods

crushed vanilla

ground vanilla

extract
```

as distinct scopes.

---

# 121. Coverage Is Directional

```text
UG → ZA
```

does not imply:

```text
ZA → UG.
```

---

# 122. Profile Does Not Mean Every Product Is Supported

---

# 123. Profile Does Not Mean Every Transit Route Is Supported

---

# 124. Profile Does Not Mean Every Regulatory Domain Is Complete

Known gaps SHALL remain visible.

---

# 125. Pilot Enforcement Strategy

Initial rollout SHOULD follow:

```text
ADVISORY
    │
    ▼
SHADOW
    │
    ▼
REVIEW GATE
    │
    ▼
CONDITIONAL ENFORCEMENT
```

---

# 126. Customs Calculation May Mature Faster Than SPS

Example:

```text
HS + tariff:
E3-ready

commodity-specific SPS:
E2 review-only.
```

The entire profile need not share one assurance ceiling.

---

# 127. Domain-Level Effect Ceiling

```text
ProfileCapabilityCertification
├── CLASSIFICATION       E2
├── TARIFF               E3
├── ORIGIN               E2
├── SPS                  E2
├── DOCUMENTS            E3
└── TAX                  E3
```

illustrative only.

Actual certification comes from ADR-REG-0025.

---

# 128. No Highest-Common-Denominator Pretence

A fully tested tariff engine does not make an incomplete SPS engine safe.

---

# 129. Architecture Invariants

| ID | Invariant |
|---|---|
| `REG-XBT-I01` | Cross-border regulatory status SHALL be composed from separate regulatory domains |
| `REG-XBT-I02` | Commercial product identity SHALL remain distinct from HS classification |
| `REG-XBT-I03` | HS classification SHALL remain versioned against a nomenclature/tariff schedule |
| `REG-XBT-I04` | HS classification SHALL NOT be inferred solely from product name |
| `REG-XBT-I05` | Country of origin SHALL remain distinct from country of dispatch/export |
| `REG-XBT-I06` | Origin SHALL remain distinct from proof of origin |
| `REG-XBT-I07` | AfCFTA preference SHALL not follow merely from country pair |
| `REG-XBT-I08` | Tariff preference SHALL require applicable origin/regime evidence |
| `REG-XBT-I09` | ICO coffee origin documentation SHALL remain distinct from AfCFTA origin proof |
| `REG-XBT-I10` | Phytosanitary certification SHALL remain distinct from origin certification |
| `REG-XBT-I11` | Customs duty SHALL remain distinct from import VAT |
| `REG-XBT-I12` | Duty-free treatment SHALL not imply SPS admissibility |
| `REG-XBT-I13` | SPS satisfaction SHALL not establish customs classification |
| `REG-XBT-I14` | Plant-product status alone SHALL not prove that an import permit is required |
| `REG-XBT-I15` | Commodity-specific permit/exemption conditions SHALL be verified |
| `REG-XBT-I16` | Unknown regulatory coverage SHALL produce INDETERMINATE rather than assumed compliance |
| `REG-XBT-I17` | Exporter-level licences SHALL remain distinct from consignment-level documents |
| `REG-XBT-I18` | Competent-authority identity SHALL be temporally versioned |
| `REG-XBT-I19` | Portal guidance SHALL not silently replace underlying legal authority |
| `REG-XBT-I20` | Transit through third territories SHALL be explicitly represented |
| `REG-XBT-I21` | Transit geography SHALL not automatically destroy preferential origin |
| `REG-XBT-I22` | Customs valuation SHALL not automatically equal invoice amount |
| `REG-XBT-I23` | Incoterm SHALL be an input fact, not the valuation rule itself |
| `REG-XBT-I24` | Tariff rates SHALL be effective-dated regulatory data, never application constants |
| `REG-XBT-I25` | Tax rates/formulas SHALL be effective-dated regulatory rules |
| `REG-XBT-I26` | A missing preference document SHALL not automatically prohibit import |
| `REG-XBT-I27` | Different failed requirements SHALL preserve different regulatory consequences |
| `REG-XBT-I28` | Regulations SHALL not perform financial posting |
| `REG-XBT-I29` | Trade SHALL remain the operational PEP |
| `REG-XBT-I30` | Cross-border profile certification SHALL declare product/domain coverage explicitly |
| `REG-XBT-I31` | Jurisdiction profile coverage SHALL be directional |
| `REG-XBT-I32` | Each regulatory subdomain MAY carry a different enforcement ceiling |
| `REG-XBT-I33` | Current tariff examples SHALL be pinned to their legal-effective schedule |
| `REG-XBT-I34` | Historical transactions SHALL remain replayable against historical tariffs/rules |
| `REG-XBT-I35` | Regulatory documents SHALL be typed by legal purpose, not filename |
| `REG-XBT-I36` | DocumentRequirement SHALL remain distinct from TradeDocument |
| `REG-XBT-I37` | Concrete trade-document identity/version SHALL be owned by Trade Docs |
| `REG-XBT-I38` | Regulations SHALL own documentary requirement semantics and satisfaction decisions |
| `REG-XBT-I39` | Trade Docs verification SHALL not automatically establish regulatory sufficiency |
| `REG-XBT-I40` | CustomsDeclaration workflow SHALL remain distinct from declaration regulatory requirements |
| `REG-XBT-I41` | External Customs acceptance/release SHALL remain sovereign authority facts |
| `REG-XBT-I42` | Permit requirement SHALL remain distinct from permit document representation |
| `REG-XBT-I43` | Exporter regulatory standing SHALL remain distinct from licence document storage |
| `REG-XBT-I44` | Material document-version changes SHALL be capable of triggering regulatory reassessment |
| `REG-XBT-I45` | Historical decisions SHALL retain the exact document versions used |
| `REG-XBT-I46` | Cross-engine documentary references SHALL retain owner identity |
| `REG-XBT-I47` | ExternalReference SHALL not substitute for a Baobab cross-engine canonical object reference |
| `REG-XBT-I48` | Trade Docs unavailability SHALL not be interpreted as documentary absence |
| `REG-XBT-I49` | Regulations unavailability SHALL not be interpreted as legal prohibition |
| `REG-XBT-I50` | No Regulations-to-Trade-Docs direct database dependency is permitted |
| `REG-XBT-I51` | No jurisdiction-specific legal requirement logic SHALL be hidden in a generic Trade Docs document-type registry |
| `REG-XBT-I52` | Regulatory document families SHALL describe legal purpose, not imply lifecycle ownership |
| `REG-XBT-I53` | A Customs authority response record SHALL preserve the external authority as the source of legal effect |
| `REG-XBT-I54` | Pulse SHALL remain outside the synchronous Regulations ↔ Trade Docs satisfaction path by default |

---

# 130. Rejected Alternatives

The following designs are rejected:

```text
one import-compliance Boolean

country → hard-coded HS

country pair → hard-coded preference

plant product → automatic permit requirement

duty free → compliant

valid certificate → compliant

one generic CertificateOfOrigin

one generic permit document

one static trade checklist

tax/VAT constants in Trade code

tariff tables copied manually into Medusa

SPS rules embedded in frontend code

Regulations directly changing shipments

Regulations posting customs tax into ERP

AI-selected tariff code used directly for enforcement

first Google result treated as legal authority

latest agency name rewriting historical records.
```

---

# 131. Implementation Sequence

The first implementation SHOULD proceed:

```text
Authoritative source registration
        │
        ▼
SARS tariff ingestion
        │
        ▼
UG coffee authority/export rules
        │
        ▼
UG phytosanitary rules
        │
        ▼
ZA NPPO import-control rules
        │
        ▼
AfCFTA origin rules
        │
        ▼
Classification domain
        │
        ▼
Origin domain
        │
        ▼
Document-requirement domain
        │
        ▼
Shared TradeDocument / cross-engine reference contracts
        │
        ▼
Trade Docs document + Customs workflow integration
        │
        ▼
Requirement-satisfaction integration
        │
        ▼
SPS domain
        │
        ▼
Tariff/duty evaluation
        │
        ▼
VAT calculation
        │
        ▼
Trade integration
        │
        ▼
Golden corpus
        │
        ▼
Shadow evaluation.
```

---

# 132. Minimum Implementation Proof

Before `ADR-REG-0027` is regarded as implemented, Baobab SHOULD demonstrate at least:

```text
Current SARS Schedule 1 source registration

Chapter 9 tariff ingestion

0901.11.10 Arabica classification

0901.11.20 Robusta classification

0901.21 roasted classification

0905.10 vanilla classification

0905.20 vanilla classification

effective tariff versions

general-rate representation

AfCFTA-rate representation

FREE tariff type

specific c/kg tariff type

TariffRate selection

Classification evidence

classification review workflow

OriginClaim

wholly-obtained origin

AfCFTA preference assessment

origin evidence assessment

AfCFTA proof validity

direct-transport assessment

third-country transit representation

coffee export licence

licence validity check

Uganda phytosanitary certificate

NPPO issuer verification

South African plant import-permit rule

permit exemption state

SPS coverage gap

document requirements

ICO coffee certificate type

AfCFTA origin certificate type

non-preferential origin certificate type

DocumentRequirement for commercial invoice

DocumentRequirement for packing list

DocumentRequirement for transport document

DocumentRequirement for Uganda export declaration

DocumentRequirement for South African import declaration

Trade Docs TradeDocument references for each required family

immutable DocumentVersion references

issuer/document verification facts

requirement-satisfaction evaluation against exact document versions

South African importer registration

CustomsValuationAssessment

transaction-value method

tariff duty assessment

South African import-VAT assessment

Trade RegulatoryFactBundle

CrossBorderTradeContext

CrossBorderRegulatoryDecision

Trade PEP integration

ERP/Ledger assessment handoff

Pulse regulatory-change events

golden Arabica case

golden Robusta case

golden roasted-coffee case

golden vanilla case

missing-origin-proof case

missing-phytosanitary case

permit-required case

permit-exempt case

INDETERMINATE SPS case

transit case

historical tariff replay

new-tariff DecisionDiff

tenant isolation

profile certification.
```

---

# 133. Initial Realistic ZuriBeans Flow

```text
ZURIBEANS
Ugandan coffee purchase
       │
       ▼
Trade Product
       │
       ▼
Shipment Draft
       │
       ▼
Control Plane Context
       │
       ├── Tenant
       ├── Legal Entity
       ├── UG EXPORTING participation
       ├── ZA market participation
       └── UG → ZA TradeLane
       │
       ▼
Regulations
       │
       ├── classify commodity
       │
       ├── verify exporter licence
       │
       ├── determine origin
       │
       ├── evaluate AfCFTA
       │
       ├── determine export document requirements
       │
       ├── determine phytosanitary rules
       │
       ├── evaluate transit
       │
       ├── determine ZA import conditions
       │
       ├── value goods
       │
       ├── calculate duty
       │
       ├── calculate import VAT
       │
       └── emit document / permit requirements
       │
       ▼
Trade Docs
       │
       ├── obtain / associate documents
       ├── version them
       ├── preserve issuer/provenance
       ├── verify documentary properties
       └── return document-version references
       │
       ▼
Regulations
       │
       └── evaluate requirement satisfaction
       │
       ▼
RegulatoryDecision
       │
       ├── shipment may proceed?
       ├── missing documents?
       ├── estimated border charges?
       └── review/hold?
       │
       ▼
Trade PEP
```

---

# 134. Example Decision

Suppose:

```text
Product:
green Arabica

Classification:
0901.11.10

Origin:
verified Uganda

Coffee exporter licence:
valid

Phytosanitary certificate:
valid

ZA import permit:
required by verified commodity rule

Import permit:
missing

Current customs duty:
FREE
```

Potential result:

```text
Classification:
SATISFIED

Origin:
SATISFIED

Tariff:
SATISFIED
duty = FREE

Uganda export:
SATISFIED

SPS:
UNSATISFIED

Documentation:
UNSATISFIED

Overall:
UNSATISFIED

Recommended disposition:
SPS_HOLD

Reason:
REQUIRED_IMPORT_PERMIT_MISSING
```

Notice:

```text
Duty free
```

did not override:

```text
SPS failure.
```

---

# 135. Example Preferential Difference

Roasted Ugandan coffee:

```text
0901.21
```

Current schedule:

```text
general = 6c/kg

AfCFTA = 2.4c/kg.
``` :chatgpt-content-reference{index="30"}


If qualifying origin and proof are established:

```text
selected tariff =
applicable AfCFTA rate.
```

If proof fails:

```text
preference not established

evaluate general rate.
```

The product does not magically become:

```text
prohibited.
```

---

# 136. Strategic Significance

This profile demonstrates why Baobab Regulations can become more than a regulatory search system.

A trader does not ultimately need only:

> “What does South African law say about coffee?”

The operational question is:

> **Can this exact shipment, by this legal entity, of this exact product state, with this origin, route, evidence, documents, value and planned date, legally proceed from Uganda into South Africa—and what remains to be done before it can?**

The engine should answer:

```text
what applies

why it applies

what evidence proves it

what is missing

what it costs

what changes if origin preference applies

what blocks release

what is uncertain

what changed since the previous assessment.
```

---

# 137. Final Decision

Baobab Regulations SHALL implement cross-border regulation as an **explainable composition of classification, origin, trade-regime, customs, SPS, valuation, taxation and documentation decisions**, beginning with Uganda → South Africa coffee and vanilla.

The final semantic architecture is:

```text
                    COMMERCIAL PRODUCT
                            │
                            ▼
                  Regulatory Product Facts
                            │
                            ▼
                    HS CLASSIFICATION
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Tariff       Controls/SPS      Origin
             │              │              │
             │              │              ▼
             │              │          Trade Regime
             │              │              │
             │              │              ▼
             │              │       Preferential Rate
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                       Documentation
                            │
                            ▼
                         Transit
                            │
                            ▼
                    Customs Valuation
                            │
                            ▼
                  Duties / VAT / Charges
                            │
                            ▼
                  Document Requirements
                            │
                            ▼
                         Trade Docs
                  documents / versions /
                  Customs workflow state
                            │
                            ▼
              Requirement Satisfaction
                            │
                            ▼
                  Regulatory Decision
                            │
                            ▼
                         Trade PEP
```

The documentary principle is:

> **Regulations determines which documents, permits and evidence are legally required and whether the supplied documentary facts satisfy those requirements. Trade Docs owns the concrete TradeDocument, DocumentVersion, dossier, declaration, submission and authority-response lifecycle.**

The Customs-workflow principle is:

> **Regulations may determine regulatory readiness, but only the competent Customs authority can exercise sovereign Customs authority, and Trade Docs merely preserves and executes the documentary workflow around that authority.**

The classification principle is:

> **Determine what the goods legally are before determining which customs, origin or control rules attach to them.**

The origin principle is:

> **Origin is a legal determination supported by facts and evidence; it is not the shipment's departure country.**

The preference principle is:

> **Preferential treatment is earned through the applicable trade regime, qualifying origin and valid proof; it is never inferred from geography alone.**

The SPS principle is:

> **A product may be duty-free and still be inadmissible for plant-health reasons.**

The document principle is:

> **A certificate proves a particular proposition for a particular purpose; no generic “certificate present” flag is acceptable.**

The authority principle is:

> **Regulatory authorities and their institutional identities are effective-dated because agencies, mandates and procedures change.**

The tariff principle is:

> **Tariff schedules are regulatory data with legal time, not constants copied into commerce code.**

The valuation principle is:

> **Commercial price, customs value, customs duty and import VAT are distinct computations governed by distinct rules.**

The transit principle is:

> **A landlocked origin does not invalidate preferential trade merely because transit occurs; the actual customs-control and direct-transport conditions must be evaluated.**

The uncertainty principle is:

> **Where commodity-specific SPS or permit coverage has not yet been verified, Baobab returns `INDETERMINATE`; it does not manufacture certainty.**

The enforcement principle is:

> **Regulations determines the legal outcome; Trade decides and performs the operational enforcement transition.**

The pilot principle is:

> **Uganda → South Africa coffee and vanilla will be the first jurisdiction-pack profile proving that Baobab can turn fragmented customs, origin, SPS, tax and documentary regulation into an executable, source-backed cross-border decision.**

And the strategic principle is:

> **The moat is not possessing tariff tables. It is being able to connect a real shipment to the correct product classification, origin regime, legal authorities, permits, SPS conditions, documentary evidence, border taxes and operational consequence—at the correct point in legal time, with every conclusion traceable to its source.**


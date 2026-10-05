# Baobab Regulations Architecture Decision Records

This directory is the engine-local ADR canon for `baobab-platform/baobab-regulations`.

Platform-wide and cross-engine authority decisions remain governed by `baobab-platform/shared/docs/adr/`. Where an accepted Shared ADR and a Regulations-local ADR overlap, the Shared decision governs the cross-engine boundary and the local ADR must be reconciled explicitly rather than silently diverging.

## Cross-engine precedence relevant to Regulations

- **ADR-SHARED-019 — Regulatory Intelligence, Trade Documents and Evidence Cross-Engine Boundary** is the platform authority for the Regulations ↔ Trade Docs ↔ Pulse relationship.
- **ADR-PULSE-012** reconciles Pulse's regulatory/customs intelligence semantics with that boundary.
- **ADR-TDOC-0001 / ADR-TDOC-0002** define Trade Docs mission and canonical TradeDocument/DocumentVersion ownership.
- **ADR-REG-0026 / ADR-REG-0027** were amended on 2026-10-05 under RTD-03 to conform to those decisions.

The central RTD-03 distinction is:

```text
Regulations
  owns regulatory meaning, requirements, applicability,
  requirement satisfaction and RegulatoryDecision

Trade Docs
  owns TradeDocument, DocumentVersion, documentary verification facts,
  CustomsCase, declaration/submission workflow and authority responses

Trade / TMS / ERP
  own operational enforcement and business state

External authorities
  retain sovereign/legal authority

Pulse
  owns downstream intelligence, risk, opportunity, forecast and recommendation
```

## ADR register

| ADR | Decision |
|---|---|
| ADR-REG-0001 | Baobab Regulations Mission, Authority, Regulatory Execution and System Boundary |
| ADR-REG-0002 | Baobab Regulations as a Headless Platform Engine and Capability Provider |
| ADR-REG-0003 | Regulatory Authority, Source Authenticity, Interpretation and Derived Rule Boundary |
| ADR-REG-0004 | Advisory, Review and Enforcement Decision Classes |
| ADR-REG-0005 | Provider-Neutral Regulatory Intelligence, Source Acquisition and Anti-Corruption Architecture |
| ADR-REG-0006 | Canonical Regulatory Domain Model, Legal Resource Identity and Aggregate Boundaries |
| ADR-REG-0007 | Jurisdiction, Regulatory Authority and Legal Hierarchy Model |
| ADR-REG-0008 | Regulatory Instrument, Provision, Rule, Obligation and Requirement Model |
| ADR-REG-0009 | Normative Semantics, Defeasibility, Discretion, Rights, Violations and Reparative Rules Model |
| ADR-REG-0010 | Regulatory Knowledge Graph, Relationship, Provenance and Traversal Model |
| ADR-REG-0011 | Authoritative Source Registry and Multidimensional Source Trust Model |
| ADR-REG-0012 | Regulatory Content Acquisition, Licensing, Reuse, AI Processing and Derived-Data Rights |
| ADR-REG-0013 | Source Ingestion, Normalisation and Adapter Architecture |
| ADR-REG-0014 | Provenance, Citation and Evidentiary Chain |
| ADR-REG-0015 | Temporal and Bitemporal Regulatory Versioning |
| ADR-REG-0016 | Machine-Executable Regulatory Rules Representation and Intermediate Language |
| ADR-REG-0017 | Regulatory Context and Applicability Resolution |
| ADR-REG-0018 | Regulatory Decision and Evaluation Engine |
| ADR-REG-0019 | Policy Decision Point and Enforcement Point Separation |
| ADR-REG-0020 | Decision Explainability, Replay and Reproducibility |
| ADR-REG-0021 | AI-Assisted Regulatory Extraction and Interpretation Boundary |
| ADR-REG-0022 | Human Verification, Confidence and Regulatory Knowledge Governance Workflow |
| ADR-REG-0023 | Regulatory Change Detection and Impact Analysis |
| ADR-REG-0024 | Regulatory Events, Subscriptions and Notifications |
| ADR-REG-0025 | Regulatory Testing, Golden Cases and Decision Regression Architecture |
| ADR-REG-0026 | Baobab Platform Integration and Canonical Context Boundary — **amended by RTD-03** |
| ADR-REG-0027 | Cross-Border Trade Regulatory Profile — **amended by RTD-03** |
| ADR-REG-0028 | Multi-Tenancy, Isolation, Security, Audit and Regulatory Data Residency |
| ADR-REG-0029 | Jurisdiction Packs, Regulatory Modules, Coverage Model and Regulatory Marketplace Architecture |
| ADR-REG-0030 | Commercial Product Model, Entitlements, Metering, SLA and Regulatory Service Packaging |

## Governance rule

Implementation must consult both the engine-local ADRs and any applicable accepted Shared ADR.

If code, a local ADR and an accepted cross-engine Shared decision disagree, the disagreement must be resolved architecturally. It must not be hidden behind adapters, copied schemas, database coupling or undocumented exceptions.

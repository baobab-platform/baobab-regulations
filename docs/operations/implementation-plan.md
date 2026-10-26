# Baobab Regulations — implementation gates (refreshed 2026-10-26)

**Governing plans:** Accepted Shared EA v2.3 / EA-DEV; Shared ADR-019/021/022/024/027/028; Regulations ADR-0001–0035. This is a source roadmap and **not** a deployment, legal-source certification or product activation receipt.

## Source implementation evidence

| Gate | Source status | Truthful limitation |
|---|---|---|
| REG-0–3 | Implemented | Domain, tenant/context contracts, source registry and provenance scaffold |
| REG-4 | Implemented bounded fragment | BRIR v1 with deliberately limited typed semantics, not arbitrary law |
| REG-5 | Implemented offline reference/golden foundation | Uganda→South Africa coffee fixtures are synthetic examples, not official clearance |
| R-CAP-01/02/04/05/06 | Source implemented within declared PARTIAL support | Exact RTD-06 endpoint shape, evidence/idempotency and transactional outbox; actual IAM/CP/transport gates remain |
| R-CAP-07/08/09 | Source implementation and automated conformance | Three PARTIAL capabilities; Rego/OPA and decision contract are not independent legal assurance |
| R-CAP-10 | **DEFER_PROMOTION (Accepted ADR-REG-0035)** | Reviewed actual sources, signed production policy, issuer/context, CP invocation, EA-09 are not independently qualified |
| REG-INGEST-01 (this PR) | Offline scaffold | Source-pinned untrusted candidate intake, independent reviewer authority port and non-publishing review decisions |

## Next bounded engineering gates

1. REG-INGEST-02: source acquisition ports with quarantine, response hash/size/rights/checkpoint metadata and SSRF/unsafe-format denial. Keep adapters provider-neutral; never infer legal authority from URL or provider.
2. REG-IR-01: lossless RegulatoryDocumentIR and deterministic parsers; version and locator/citation quality tests, restricted-data handling, no direct rule publication.
3. REG-GOV-01: durable PostgreSQL tenant-scoped candidate review history, externally verified IAM/CP reviewer competence, maker-checker E3/E4 controls, independent publication approver and terminal/replay testing.
4. REG-PUBLISH-01: separate source-backed, legally reviewed rule/requirement publication with bitemporal pinning, affected-entity analysis, expert golden-case signoff and immutable audit evidence.
5. REG-RUNTIME-01: source-authorised signatures/bundles, audience-verified IAM resource-server, current CP capability/tenant scope, actual broker transport, fail-closed negative cases and EA-09 independent certification.
6. EA-DEV DEV-14 adoption: consume the Shared reusable onboarding profile only when real Regulations IAM/CP/runtime adapters are available; engine-specific tests cover distinct legal-actor/market/tenant and time, revoked grants, missing source, invalid bundle, replay and teardown.

**Boundaries:** Regulations does not own TradeDocument, customs case, Trade order, ERP posting or TMS shipment, and does not act as a sovereign source. Pulse suggestions and AI candidates cannot authorise regulatory enforcement. No source PR merge implies `IMPLEMENTED`, `CERTIFIED`, CP `ACTIVE` or live market permission.

See [audit](adr-conformance-audit-2026-10-26.md), [scaffold status](scaffold-status.md) and [ADR-REG-0035](../adr/ADR-REG-0035%20%E2%80%94%20R-CAP-10%20Provider%20Promotion%2C%20Evidence%20Admissibility%20and%20Production%20Acceptance.md).

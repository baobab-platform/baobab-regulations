# Scaffold status — baobab-regulations

**Audit refreshed:** 2026-10-26  
**Current engineering status:** Source implementation substantially exceeds the September REG-0–3 scaffold. The canonical provider remains **PARTIAL / non-registerable** under Accepted ADR-REG-0035.

## Implemented source foundation

- Python 3.14 domain and FastAPI structure, capability contracts, reference evaluator and UG→ZA synthetic case.
- Authoritative source registry, rights/provenance models, bitemporal records and PostgreSQL migrations 000001–000006.
- BRIR v1 → deterministic Rego compiler, checksum-pinned OPA integration, rule-set assurance checks and canonical decision evaluation.
- Exact RTD-06 requirement and evidence endpoints, PostgreSQL tenant RLS/immutable requirement projections, transactionally recorded event outbox and durable decision replay.
- R-CAP-07/08/09/10 conformance workflows and explicit deferred provider promotion.
- REG ingestion candidate-review **scaffold**: fingerprinted untrusted candidate, pinned source artefact, non-production review queue and checker/competence authority port. No publication is performed.

## Still open

- Source acquisition quarantine, documentary IR parsing, full rights/citation assurance, qualified human review and persistent candidate publication with audit.
- Signed production OPA policy bundles, live actual IAM/CP resource-server and capability-invocation authority, production event delivery.
- Domain expert legal/market goldens, independent EA-09 provider certification, CP registration/activation and observed real-component acceptance.
- Developer-only DEV-14 engine onboarding adapter and comprehensive engine-specific L4 negative/positive acceptance.

For detailed source-versus-runtime classifications, see
[`adr-conformance-audit-2026-10-26.md`](adr-conformance-audit-2026-10-26.md).
Do not use historic `REG-4 NEXT` headings as a current maturity gauge.

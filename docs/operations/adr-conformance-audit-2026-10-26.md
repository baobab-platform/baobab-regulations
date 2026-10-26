# Regulations ADR and EA v2.3 engineering audit — 2026-10-26

**Baseline:** main commit `89a113104410121deca43e9ce48ea865bacbfbe8` (11 October 2026); scoped to repository code, ADRs and manifest evidence. This is a source audit, not an independently witnessed runtime certification.

**Normative hierarchy:** Shared EA v2.3 (Accepted, 20 October), EA-DEV (Accepted, 23 October), Shared ADR-019/021/022/024/027/028, local ADR-REG-0001–0035, and the R-CAP-10 deferred-promotion decision. Shared owns canonical cross-engine contracts; CP owns tenant/context/registration/grant/binding; IAM owns identity; Regulations owns regulatory meaning and its protected decisions; Trade Docs owns TradeDocument and actual documentary workflow; Pulse is advisory only. Development source work does **not** require protected staging approval; real provider/production acceptance remains separate.

## Existing evidence and observations

| ADR / EA topic | Observed source evidence | Remaining work / rule |
|---|---|---|
| REG-0001–0005, -0019, EA-13 | Domain separations, reference evaluator, provider-neutral ports, policy-engine adapter | Never let OPA, an LLM, Trade Docs or Pulse define sovereign law or native enforcement |
| REG-0006–0010, -0015–0018 | Domain types, BRIR v1, deterministic compiler, bitemporal rule authority, rule tests | Broader legal defeasibility and semantic coverage remain intentionally unsupported |
| REG-0011–0014 | AuthoritativeSource, SourceArtefact, rights classes, provenance link, in-memory source registry, migration 000002 | Actual acquisition, quarantine/SSRF protection, secure parser, source rights proof, legally reviewed ingestion are not qualified |
| REG-0021–0022 | Candidate extraction and reviewer governance specified in ADRs | Before this PR there was no candidate lifecycle/reviewer port; this PR adds *non-publishing* source-pinned candidate admission and independently verified checker-port scaffold |
| REG-0025, -0027 | UG→ZA coffee reference, BRIR compiler and engine tests | Synthetic golden cases do not assert actual customs/SPS permit approval |
| REG-0026, -0028 | CP context authority adapter, explicit tenant-scoped storage and PostgreSQL RLS cases | Actual IAM workload identity, caller-bound CP grant resolution and native PEP acceptance still outstanding |
| REG-0031–0035 | Three canonically declared PARTIAL capabilities, authenticated route shape, durable RTD-06 requirement/evidence and R-CAP-09 evaluation, R-CAP-10 evidence register | Production bundle signatures, legal-source assurance, external IAM/CP/transport evidence, EA-09 provider certification and activation remain BLOCKED |
| EA-DEV DEV-14/15 | Shared reusable engine run-profile standard exists; Pulse/Payments are the initial required profiles | Regulations may adopt a future **optional** headless engine profile only when this engine's actual protected/native adapter exists; no dummy green profile |
| EA-DEV DEV-07/08 | Trade/Logistics may eventually consume Regulations/Docs via accepted contracts | Never create a native customs/TradeDocs/Trade/TMS provider or enforcement bypass here |

## Findings to correct

1. `docs/operations/implementation-plan.md` and `scaffold-status.md` still describe REG-4 as NEXT and live OPA as absent, although BRIR-to-Rego, OPA and R-CAP-09/10 have since landed. Refresh source-status wording and link acceptance separately.
2. Source registry proof is in-memory; source review, candidate capture and promotion are not linked to a durable governed publication workflow. A content hash proves *bytes*, not provenance legality, rights, competence or legal force.
3. Candidate production is a **data** operation. Machine confidence, high source trust, test fixtures and successful compilation cannot mark a RuleVersion VERIFIED or make documentary requirements active. REG-0022 independent checker and expert signoff must precede promotion.
4. Provider status remains PARTIAL by Accepted ADR-REG-0035; no local manifest edit can supply IAM, CP, signed bundle or independent EA-09 evidence. Test fake verifiers may only appear in test/offline-only wiring.
5. Capability correctness remains an engine-specific obligation under EA-DEV. The shared generic DEV-14 descriptor is not a replacement for this engine's migration, issuer/context/resource, rule assurance, denial and teardown cases.

## Bounded source increment in this PR

- New immutable, fingerprinted `RegulatoryCandidate` with source/artefact SHA-256 pin, extraction lineage, scope, original producer and JSON proposed meaning.
- Source-backed intake refuses missing/mismatched/unpinned artefacts and duplicate candidate identity; rights are owned by `SourceArtefact`, not hallucinated from the adapter.
- Repository seam and non-production in-memory queue with expected-revision compare-and-swap, review history, independent checker, current competence verification, attribution and evidence-backed approval.
- `APPROVED_FOR_PROMOTION` means **candidate reviewed**, *not* RuleVersion/BRIR published, REG-0035 promoted, or regulatory clearance. No HTTP route, RuleSet writer, entitlement, authority grant or event producer is added.
- Automated negative tests for tampering, missing source, unsupported AI lineage, maker/checker collision, expired competence, missing approval evidence, duplicate and stale review.

## Next owned implementation order

1. **Regulations-owned ingestion and governance:** source-acquisition metadata/quarantine and deterministic `RegulatoryDocumentIR`, durable tenant-isolated candidate/review/event audit, IAM/CP qualified reviewer adapter and correct legal-source rights and provenance checks.
2. **Separate publication gate:** independently authorised maker/checker and rule-engineering TEVV, source and legal/knowledge-time assurance, stable versioned rules/requirements, negative and historical replay golden cases. No direct in-place candidate conversion.
3. **Runtime/provider dependencies:** signed production policy bundles/trust root, governed requirement projection ingestion, resource-server audience and CP `context:validate` identity, capability resolution, event-transport acknowledgements, EA-09 and explicit activation.
4. **EA-DEV composition:** adopt reusable DEV-14 integration descriptor as a Regulations **consumer**, with engine-local source and decision scenarios; qualify genuine IAM→CP→Regulations results and wrong-tenant/missing-grant/outage/replay/teardown, while keeping protected/production gates separate.

**Acceptance:** Source tests and code review may accept this scaffold; they cannot elevate the three provider-support entries above PARTIAL or claim an active compliance decision service.

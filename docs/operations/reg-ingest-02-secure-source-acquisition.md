# REG-INGEST-02 — Secure source acquisition

Status: **Source implementation / synthetic qualification. Protected-runtime onboarding HELD.**

Governing ADRs: REG-0003, REG-0005, REG-0011, REG-0012,
REG-0013, REG-0014, REG-0021, REG-0022, REG-0026, REG-0028 and REG-0035.
Platform contract: Shared EA v2.3, EA-DEV and governed DEV-14 adapter onboarding.

## Implemented boundary

SecureSourceAcquisitionService takes a registered source ID, registered
endpoint reference and CP context ID, never a caller URL. It requires a
verified IAM token, CP-redeemed context and a separate CP capability
authorization port before acquisition. All three are mandatory and cannot
be replaced by a caller-provided tenant/role header. The canonical source
registry must recognize the source ID and the governed endpoint registry
must explicitly approve the endpoint.

The rights provider supplies attributable, versioned ACQUIRE_AND_STORE
and TRANSFORM_AND_PROCESS decisions with evidence references. DENY/HOLD
prevents all outbound requests. Retrieval on ALLOW uses approved HTTPS
with allowed host and media types, no credentials/query parameters,
public-address-only DNS validation, numeric IP-pinned connection, TLS
SNI/certificate verification against the registered hostname, no proxy,
no redirects and deadline. Network egress controls must independently
enforce the same policy for protected deployments.

Raw bytes, not a parser representation, enter quarantine with a hard
32 MiB *absolute maximum* (individual endpoints may specify less).
SHA-256 is computed while streaming. Every acquisition and artefact has
an independent UUID; equal hashes are never conflated with evidentiary
identity. Metadata and rights/security decisions are appended to
tenant-scoped PostgreSQL tables; no raw HTTP headers, tokens, signed URLs,
document bodies, legal interpretations or rule publications are persisted.

PostgreSQL migration 000007 provides tenant-scoped acquisitions, events
and artefact metadata via the existing baobab.tenant_id transaction
context and ENABLE / FORCE ROW LEVEL SECURITY. The runtime database role
must have INSERT/SELECT only and be non-superuser/non-BYPASSRLS.

## Security and acceptance boundaries

- QuarantineOnlySecurity is a conservative signature detector and NEVER
  certifies malware safety or processing readiness. Archives and unknown
  formats remain blocked. Plug an independent qualified scanner into
  SourceSecurityPort for any protected runtime.
- InMemoryQuarantine and the in-memory journal are development-only,
  not durable or independent evidence custody. A private encrypted
  immutable/versioned object-store adapter, residency/retention/key
  policy, integrity read-back and orphan reconciliation are still required.
- CP redemption/grants, source/endpoint registration and rights decisions
  are mandatory *ports*, not real production connections in this PR.
  Missing adapters fail closed; no self-approval route is exposed.
- Successful TLS and SHA-256 do not confer legal authenticity. Acquired
  documents remain UNTRUSTED EVIDENCE. No REG-IR-01 parsing, normative
  rule, canonical publication, BRIR/OPA or Trade Docs decision is produced.
  ADR-REG-0035's R-CAP-10 provider remains PARTIAL / DEFER_PROMOTION.
- No arbitrary URL fetch route, caller-appointed reviewer, or request
  body/header field asserting CP/IAM authority has been introduced.

## Evidence

The reg-ingest-02-secure-acquisition workflow pins GitHub Actions to
specific commit hashes and runs Python 3.14 Ruff/mypy/unit tests plus
PostgreSQL 17 integration tests with non-superuser RLS role. Synthetic
cases prove DENY/HOLD = zero fetch, missing grant/source denial, streaming
limits, quarantine on scan failure, hash identity separation, metadata
integrity, cross-tenant isolation and private/metadata DNS and URL denial.
CI does not contact regulatory publishers.

Green CI means source engineering is qualified, NOT that protected
staging, legal rights, independent custody or provider activation passed.

## Remaining protected-runtime work

1. Govern official endpoint profiles and rights evidence/revisions.
2. Implement encrypted immutable object-store custody with independent
   read-back, retention, residency, key management and orphan reconciliation.
3. Wire real IAM/CP context and grants, qualified scanner and bounded
   network-egress worker.
4. Qualify negative cases and real-component staging evidence under
   EA-DEV, keeping merge separate from production promotion.

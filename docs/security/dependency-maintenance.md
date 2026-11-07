# BA-SEC-DEP-001 — baobab-regulations dependency and security maintenance audit

**Review date:** 7 November 2026. **Repository:** `baobab-platform/baobab-regulations`. **Status:** SOURCE_COMMITTED only.

## Observed manifests and Dependabot coverage

GitHub Actions /; pip / (actual root pyproject.toml, no uv.lock); Docker Compose / (PostgreSQL/OPA local stack). No Dockerfile exists and container production capability is explicitly disabled in .baobab/repository.yaml.

## Actual dependency/security surveillance

Daily isolated Python 3.14 package install and pip-audit 2.10.1 --local --strict on the resolver-installed third-party graph. This is an unlocked, time-dependent graph; use the evidence label UNLOCKED_PYTHON and do not claim lockfile reproducibility.

## Findings, unqualified boundaries and exception custody

P0: No committed uv.lock despite .baobab/repository.yaml claiming Python package manager uv. Reconcile to a reviewed uv lock and immutable runtime resolution before full qualification. The local Compose pins an OPA 0.70.0 image while a separate R-CAP-09 workflow installs checksum-verified OPA 1.21.1; this toolchain drift requires actual decision parity testing and security review. Do not confuse deterministic policy evaluator with Pulse's intelligence. Security CODEOWNERS previously pointed to @nabhold rather than @baobab-platform; corrected in this PR. Do not activate Qdrant/knowledge plane.

**Current disposition:** Source-only pip manifest surveillance, not pinned Python or protected regulatory decisioning acceptance.

## Governance and evidence levels

Governing authority: [approved BA-SEC-DEP-001 v1.0, Shared #429](https://github.com/baobab-platform/shared/pull/429). The proposed stricter Shared validator is NOT released; this branch uses the SHA-pinned accepted Shared v2.3.0 structural validator and an owner-local positive/negative source suite. Weekly Monday Africa/Johannesburg version updates are distinct from advisory-driven security response. Routine groups apply only to minor/patch version-updates; major or security updates require independent review.

Evidence state **SOURCE_COMMITTED** means source reviewed/committed, not executed. **CI_VERIFIED**, **SECURITY_ALERT_PATH_VERIFIED**, **CONSUMER_QUALIFIED**, **STAGING_VERIFIED**, and **PRODUCTION_VERIFIED** are NOT claimed. Findings are **BLOCKED** pending an independently approved remediation or expiring exception. **WAIVED is not PASSED**. Security CODEOWNERS review applies to manifest and exception changes.

## Exit criteria

1. Run the actual final-head policy regression and accepted Shared validator; inspect live GitHub Dependabot job logs, dependency graph, Alerts, automatic security update settings and actual dependency scan results.
2. Repair reported security vulnerabilities promptly using real installed package/image provenance; independent time-bounded evidence and Security approval are required for any unpatched exceptions. Do not permit scanner errors, no-ops or ignored advisories to appear as success.
3. Re-run owner-specific native runtime, IAM/CP authority, supplier/consumer isolation, replay, migration and negative acceptance tests after a major or security update. No synthetic PSP, carrier, rule or issuer success counts as a real integration.
4. Obtain separate staging/production approvals and deployment evidence. No protected environment, credential, provider or release is activated by this policy adoption.

No CI run or monitoring, PR merge or protected business approval has been claimed.

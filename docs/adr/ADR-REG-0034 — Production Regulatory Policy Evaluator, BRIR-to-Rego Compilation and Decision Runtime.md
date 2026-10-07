# ADR-REG-0034 — Production Regulatory Policy Evaluator, BRIR-to-Rego Compilation and Decision Runtime

**Status:** Accepted — R-CAP-09 Implementation Decision  
**Decision ID:** ADR-REG-0034  
**Engine:** Baobab Regulations  
**Date:** 2026-10-06  
**Implements:** R-CAP-09  
**Depends On:** ADR-REG-0016, ADR-REG-0018, ADR-REG-0019, ADR-REG-0020, ADR-REG-0022, ADR-REG-0033  
**Shared Contract Authority:** ADR-SHARED-028

---

## 1. Decision

R-CAP-09 SHALL implement the first production-shaped runtime path for:

```text
regulations.decision.evaluate
```

without allowing the evaluator technology to become the domain contract.

The initial execution chain is:

```text
Shared DecisionEvaluateRequest
        ↓
authenticated caller
        ↓
caller-bound PlatformContext
        ↓
tenant/reference integrity
        ↓
exact pinned RuleSet authority
        ↓
legal_time + knowledge_time
        ↓
verified/certified BRIR
        ↓
deterministic BRIR compiler
        ↓
Rego v1 artifact
        ↓
OPA Data API
        ↓
typed evaluator result
        ↓
canonical DecisionEvaluateResponse
        ↓
durable replay/idempotency snapshot
```

OPA is the first production evaluator implementation.

OPA is not the canonical Regulations model.

---

## 2. Capability maturity

After this increment:

```text
regulations.decision.evaluate
    implementation_status: PARTIAL
```

under:

```text
provider_key: baobab-regulations.core
```

R-CAP-09 SHALL NOT promote the capability to `IMPLEMENTED`.

The remaining production/certification/activation gates are intentionally left
for R-CAP-10 and post-R-CAP activation work.

---

## 3. Canonical contract remains Shared

R-CAP-09 implements exactly the R-CAP-08 contract:

```text
contracts/regulatory-decision/v1/domain.schema.json
contracts/regulatory-decision/v1/regulations.openapi.yaml
```

No OPA-specific field may be introduced into that contract.

In particular, the canonical request/response SHALL NOT expose:

```text
OPA URL
Rego package
Rego query
OPA decision_id
OPA bundle revision
compiler implementation type
Kubernetes identity
runtime pod
AWS resource identity
```

Those are execution provenance.

---

## 4. BRIR is the semantic executable authority

The evaluator SHALL NOT execute hand-authored Rego as regulatory truth.

The governed chain is:

```text
RegulatoryRuleVersion
        ↓
typed BRIR
        ↓
semantic fingerprint
        ↓
trusted compiler
        ↓
CompiledPolicyArtifact
        ↓
OPA
```

The first R-CAP-09 compiler supports a deliberately bounded deterministic BRIR
subset.

Unsupported semantics fail compilation or remain non-executable.

They do not fall through into arbitrary Rego.

---

## 5. Bounded BRIR v1 subset

The first executable subset supports deterministic requirement rules:

```text
BrirRuleSet
  rules[]
    rule_version_reference
    legal_basis_reference
    when_all[]
      fact_code
      operator = EQ | EXISTS
      value?
    requirement_fact_code
    expected_value
    failure_reason_code
    failure_message
```

The rule set also carries:

```text
success reason
allow disposition
hold disposition
enforcement class
not-applicable reason
```

This is not the complete ADR-REG-0016 language.

It is the first governed executable subset.

---

## 6. Predicate semantics

`EQ` means:

```text
fact exists
AND
fact value == expected scalar
```

`EXISTS` means:

```text
fact key is present
```

It SHALL NOT mean:

```text
truthy
```

Therefore a present fact whose value is `false` still satisfies an
`EXISTS` predicate.

---

## 7. Applicability is distinct from satisfaction

The compiler SHALL distinguish:

```text
rule applies?
```

from:

```text
applied rule satisfied?
```

If no executable rule applies:

```text
outcome = NOT_APPLICABLE
recommended_disposition = null
```

It SHALL NOT manufacture:

```text
SATISFIED
ALLOW
```

from absence of applicable rules.

---

## 8. Deterministic fingerprints

BRIR canonical JSON is serialized with stable key ordering and compact
separators.

Its SHA-256 becomes the semantic rule-set fingerprint.

The compiler produces a deterministic Rego source artifact and SHA-256 artifact
fingerprint.

The same:

```text
BRIR
+
compiler version
```

must produce the same:

```text
semantic fingerprint
compiled source
artifact fingerprint
entrypoint
```

---

## 9. Compiler provenance

`CompiledPolicyArtifact` records:

```text
rule_set_id
rule_set_fingerprint
compiler_id
compiler_version
target
entrypoint
source
artifact_fingerprint
```

The initial compiler is:

```text
compiler_id      = baobab-regulations-rego
compiler_version = 1
target           = rego/v1
entrypoint       = baobab/regulations/decision
```

Compiler version is execution provenance.

It is not part of the Shared decision contract.

---

## 10. OPA anti-corruption boundary

OPA SHALL remain behind:

```text
RegulatoryPolicyEvaluatorPort
```

The adapter:

1. requires a governed rule-set/entrypoint mapping;
2. checks OPA readiness with bundle-aware health semantics;
3. submits one canonical semantic input document;
4. requires HTTP 200;
5. requires a `result`;
6. validates the result against a typed internal protocol;
7. verifies input fingerprint;
8. verifies rule-set fingerprint;
9. translates only the typed decision fragment into Regulations domain output.

---

## 11. Undefined is not a legal outcome

OPA Data API semantics permit a query to be undefined.

R-CAP-09 maps:

```text
HTTP 200
without result
```

to:

```text
EVALUATOR_UNDEFINED
HTTP 503
```

It SHALL NOT map undefined to:

```text
UNSATISFIED
INDETERMINATE
NOT_APPLICABLE
false
```

---

## 12. Evaluator failure taxonomy

The runtime distinguishes:

```text
EVALUATOR_UNDEFINED
EVALUATOR_PROTOCOL_ERROR
EVALUATOR_RUNTIME_ERROR
EVALUATOR_NOT_READY
```

All are technical failure classes.

All remain outside the canonical regulatory outcome enum.

---

## 13. OPA readiness

Before policy evaluation the adapter checks:

```text
GET /health?bundles=true
```

A non-200 result means the evaluator is not ready for governed policy
evaluation.

Reachability alone is not enough.

---

## 14. Rule-set authority

The runtime resolves one exact pinned:

```text
REGULATORY_RULE_SET
```

from Regulations authority.

Resolution validates:

- reference owner/type;
- platform versus tenant scope;
- tenant consistency;
- semantic fingerprint shape;
- optional VERSION_PINNED content hash;
- legal-time interval;
- knowledge-time interval;
- assurance state.

---

## 15. Bitemporal rule sets

A rule set is valid only if both are true:

```text
legal_valid_from <= legal_time < legal_valid_to?
knowledge_from   <= knowledge_time < knowledge_to?
```

The evaluator MUST NOT silently substitute wall-clock current time.

---

## 16. Assurance

For standard evaluation, the rule set must be:

```text
VERIFIED | CERTIFIED
```

For:

```text
requested_assurance = HIGH_ASSURANCE
```

the rule set must be:

```text
CERTIFIED
```

A lower-assurance rule set produces a technical conflict/readiness failure, not
a lower-confidence legal answer.

---

## 17. Tenant-scoped rule sets

Rule sets may be:

```text
platform
tenant
```

Platform rule sets carry no tenant owner.

Tenant rule sets require:

```text
record.tenant_id
==
reference.tenant_id
==
trusted PlatformContext tenant
```

PostgreSQL applies RLS to tenant-scoped rule-set records.

---

## 18. Enforcement ceiling

The request carries:

```text
requested_enforcement_class_ceiling
```

The evaluator result must not exceed it.

An evaluator returning a higher consequence class is an integrity failure.

The ceiling does not command the evaluator to return that class.

---

## 19. Evidence citation integrity

The evaluator may cite only evidence that was present in the canonical request,
either:

- directly under `evidence_references`; or
- as a fact `source_reference`.

An evaluator may not manufacture a foreign evidence reference during decision
assembly.

---

## 20. Decision identity

R-CAP-09 derives deterministic Regulations-owned identities from:

```text
trusted tenant
+
replay_key
+
input_fingerprint
+
rule_set_fingerprint
```

for:

```text
REGULATORY_DECISION
REGULATORY_ASSESSMENT
```

This makes concurrent equivalent command candidates converge on the same
semantic decision identity.

---

## 21. Idempotency and semantic replay

R-CAP-09 preserves the R-CAP-08 distinction:

```text
Idempotency-Key
    command identity

replay_key
    semantic decision input identity
```

PostgreSQL enforces both:

```text
UNIQUE (tenant_id, idempotency_key)

UNIQUE (tenant_id, replay_key)
```

---

## 22. Replay before live dependencies

If a durable semantic decision already exists for:

```text
tenant
+
replay_key
+
input_fingerprint
```

the runtime returns that exact canonical decision without requiring:

```text
current OPA
current rule-set resolver
current network state
```

This preserves deterministic historical replay and avoids accidental
re-evaluation against mutable runtime state.

---

## 23. Durable decision snapshot

The persistence layer stores:

```text
decision_id
assessment_id
tenant_id
idempotency_key
replay_key
request_fingerprint
input_fingerprint
result_fingerprint
contract_major
rule_set_object_id
rule_set_fingerprint
outcome
enforcement_class
exact request JSON
exact response JSON
legal_time
knowledge_time
evaluated_at
```

The request/response fingerprints are revalidated on replay.

---

## 24. RLS

`regulatory_decision_evaluations` uses:

```text
ENABLE ROW LEVEL SECURITY
FORCE ROW LEVEL SECURITY
```

with transaction-local:

```text
baobab.tenant_id
```

A runtime connection without tenant context sees no tenant decision rows.

---

## 25. Authenticated canonical route

R-CAP-09 activates:

```text
POST /decisions/evaluate
operationId: evaluateRegulatoryDecision
```

through the existing R-CAP-04 authenticated capability shell.

The route requires:

```text
Authorization: Bearer ...
Idempotency-Key: ...
```

and still depends on caller-bound Control Plane context validation.

---

## 26. Reference evaluator role

The existing `ReferenceEvaluator` is not production traffic infrastructure.

R-CAP-09 adapts it only as:

```text
differential oracle
golden semantic comparator
```

The production decision service must not import or depend on it.

---

## 27. Differential proof

For the supported first rule profile:

```text
canonical input
      ├── ReferenceEvaluator adapter
      └── OPA adapter
              ↓
compare:
  outcome
  enforcement class
  reason codes
  disposition
```

This is necessary because successful OPA execution alone does not prove
regulatory-semantic equivalence.

---

## 28. Live OPA proof

CI SHALL execute a real OPA binary, not only a mocked HTTP client.

The OPA binary SHALL be:

- explicitly version pinned;
- checksum verified;
- statically checked against compiler-generated Rego;
- started locally in CI;
- queried through the same HTTP adapter used by application code.

As of this decision, CI pins OPA `v1.21.1` and verifies the official
`opa_linux_amd64_static` SHA-256.

The live policy is generated from typed BRIR during CI.

No handwritten Rego fixture is regulatory authority.

---

## 29. Signed bundle boundary

ADR-REG-0016 ultimately requires:

```text
BRIR
  ↓
trusted compiler
  ↓
signed OPA bundle
  ↓
OPA runtime
```

R-CAP-09 establishes:

```text
typed BRIR
+
deterministic compiler
+
artifact fingerprint
+
live OPA execution
```

Repository code does not yet contain the production signing key, bundle
distribution service or deployment trust root.

Those are deployment/governance authorities and SHALL NOT be fabricated in
source code.

Therefore production signed-bundle **deployment evidence remains a blocker for
R-CAP-10 IMPLEMENTED promotion**, even though the evaluator implementation
itself now exists.

---

## 30. No raw Rego authority

The BRIR models use:

```text
extra = forbid
```

and do not expose raw target-language fields.

A document attempting to supply:

```text
rego
source
opa_query
bundle
```

as BRIR fails validation.

---

## 31. Unsupported semantics

The bounded compiler does not pretend to support the full ADR-REG-0016 model.

Examples not yet executable in the first subset include:

- defeasible overrides;
- explicit exemptions;
- reparations;
- deadlines;
- arithmetic calculations;
- permissions/powers;
- constitutive derivation chains;
- unknown-value algebra beyond bounded input semantics.

Such rules must remain non-executable or use a later compiler version.

They may not be approximated silently.

---

## 32. Live deployment still separate

R-CAP-09 does not itself establish:

- production OPA cluster;
- signed bundle registry;
- signing keys/trust roots;
- workload identity;
- caller audience allocation;
- Control Plane provider registration;
- provider lifecycle ACTIVE;
- CapabilityBinding;
- CapabilityGrant.

These are separate readiness/activation facts.

---

## 33. Why PARTIAL remains correct

The code now contains a real evaluator implementation and executable path.

However `IMPLEMENTED` remains premature because at least these are still
outside the repository/runtime proof:

```text
signed production OPA bundle distribution
production workload authenticator
Shared/IAM baobab-regulations workload allocation
caller aud=baobab-regulations authority
production requirement authority for documentary capability
event transport deployment binding
EA-09 certification
Control Plane provider registration/activation
```

Therefore:

```text
PARTIAL = truthful
IMPLEMENTED = overclaim
```

---

## 34. R-CAP-09 exit criteria

R-CAP-09 is complete when CI proves:

1. exact Shared R-CAP-08 request/response compatibility;
2. authenticated canonical route;
3. tenant mismatch denial;
4. bitemporal rule-set resolution;
5. assurance gating;
6. deterministic BRIR fingerprint;
7. deterministic Rego compilation;
8. no raw-Rego BRIR escape hatch;
9. real OPA policy validation;
10. real OPA Data API execution;
11. OPA bundle-aware readiness;
12. undefined result is technical failure;
13. protocol mismatch is technical failure;
14. runtime failure is technical failure;
15. input fingerprint integrity;
16. rule-set fingerprint integrity;
17. enforcement ceiling;
18. evidence citation integrity;
19. command idempotency;
20. semantic replay identity;
21. PostgreSQL concurrency convergence;
22. decision RLS;
23. rule-set RLS;
24. differential/golden agreement for supported profile;
25. no operational domain mutation;
26. provider support remains PARTIAL.

---

## 35. Final decision

> **R-CAP-09 implements the first production-shaped deterministic Regulations
> evaluator: canonical Shared input is resolved through caller-bound context and
> bitemporal rule-set authority, executed as trusted-compiler-derived Rego
> behind an OPA anti-corruption layer, assembled into a canonical
> RegulatoryDecision and persisted for deterministic replay. The capability is
> real enough for PARTIAL provider support, but signed-bundle deployment,
> identity/certification and runtime activation remain explicit later gates.**

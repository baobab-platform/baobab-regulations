# ADR-REG-0032 — First Canonical Provider Declaration, Partial Support and Activation Boundary

**Status:** Accepted — Provider-Readiness Decision  
**Decision ID:** ADR-REG-0032  
**Engine:** Baobab Regulations  
**Repository:** `baobab-platform/baobab-regulations`  
**Date:** 2026-10-06  
**Implements:** R-CAP-07  
**Depends On:** ADR-SHARED-017, ADR-SHARED-027, ADR-REG-0031  
**Contract Authority:** `baobab-platform/shared`  
**Runtime Authority:** `baobab-platform/baobab-cp`  
**Identity Authority:** `baobab-platform/baobab-iam`

---

## 1. Decision

R-CAP-07 SHALL move the two canonical RTD-06 Regulations capabilities from:

```text
planned_capabilities
proposal_status: CONTRACTED
```

to repository-level provider implementation evidence under:

```text
provider: baobab-regulations.core

regulations.requirement.resolve
    implementation_status: PARTIAL

regulations.evidence.assess
    implementation_status: PARTIAL
```

The declaration SHALL NOT claim either capability as `IMPLEMENTED`.

The provider SHALL be:

```text
provider_key:          baobab-regulations.core
provider_type:         BAOBAB_ENGINE
implementation_key:    core
simulated:             false
production_permitted:  true
```

`production_permitted: true` means only that this first-party provider family
is allowed to pursue later production certification and activation.

It does **not** mean:

```text
production ready
certified
ACTIVE
healthy
deployed
bound
granted
runtime resolvable
```

Those facts remain outside this repository declaration.

---

## 2. Why R-CAP-07 Is No Longer CONTRACTED-Only

ADR-REG-0031 established this explicit sequence:

```text
R-CAP-01  requirement.resolve adapter
R-CAP-02  evidence.assess adapter
R-CAP-03  exact contract proof
R-CAP-04  authenticated/context-bound routes
R-CAP-05  durable assessment persistence/idempotency
R-CAP-06  canonical event outbox
R-CAP-07  PARTIAL provider support if canonical paths are covered
```

R-CAP-01 through R-CAP-06 now provide repository evidence for every required
canonical path.

The repository therefore no longer truthfully belongs at:

```text
canonical contract exists
+
no provider implementation
```

The correct state is:

```text
canonical contract exists
+
provider implementation exists
+
implementation is incomplete for production
```

which Shared names:

```text
PARTIAL
```

---

## 3. Shared Governance Semantics

ADR-SHARED-017 deliberately separates:

```text
canonical capability
        !=
provider implementation
        !=
certification
        !=
production permission
        !=
Control Plane activation
        !=
engine instance health
        !=
tenant entitlement
        !=
binding
        !=
runtime resolution
```

A `PARTIAL` support declaration is repository architecture evidence only.

Shared's registration generator excludes `PARTIAL` support entirely.

Therefore this R-CAP-07 state cannot accidentally become runtime
`ProviderCapabilitySupport` through the current registration generation path.

---

## 4. Repository Lifecycle Decision

Shared G-FCI-1 forbids an engine whose Foundation repository lifecycle is
`experimental` from declaring `providers[]`.

R-CAP-07 therefore promotes:

```text
.baobab/repository.yaml

repository.lifecycle:
    experimental
        ↓
    active
```

This is a **repository governance lifecycle**, not a production deployment
lifecycle.

It means:

> Baobab Regulations is now an actively implemented engine with real provider
> code and evidence rather than an experimental architecture repository.

It does not imply production readiness. Production remains governed by the
separate provider, certification, release, deployment, health and Control Plane
lifecycles.

---

## 5. Provider Identity

ADR-REG-0002 permits the initial provider identity:

```text
baobab-regulations.core
```

R-CAP-07 adopts that identity.

The provider is intentionally not named after:

```text
Python
FastAPI
PostgreSQL
OPA
AWS
South Africa
Uganda
ZuriBeans
Trade Docs
```

because provider identity must survive implementation and deployment changes.

No `invocation` block is declared yet.

That omission is intentional: the repository has an HTTP implementation, but
there is not yet governed deployment/service-registration evidence strong
enough to claim a logical invocation registration.

---

## 6. Capability Decision — regulations.requirement.resolve

### 6.1 Evidence now present

The capability now has:

1. exact RTD-06 request model;
2. exact RTD-06 response model;
3. canonical FastAPI operation;
4. workload-authentication boundary;
5. caller-bound Control Plane context-validation adapter;
6. tenant/reference ownership validation;
7. exact pinned requirement lookup;
8. stale/conflicting reference behavior;
9. not-found vs authority-unavailable separation;
10. exact Shared contract tests;
11. canonical OpenAPI/error-surface tests.

Therefore:

```text
CONTRACTED-only
```

would understate implementation.

### 6.2 Why it remains PARTIAL

The repository still has no production requirement-authority persistence adapter
for the RTD-06 requirement projection.

The concrete implementation currently available for that port is:

```text
InMemoryRequirementRepository
```

which is explicitly a test/local adapter.

Consequently:

```text
regulations.requirement.resolve
    = PARTIAL
```

not `IMPLEMENTED`.

---

## 7. Capability Decision — regulations.evidence.assess

### 7.1 Evidence now present

The capability now has:

1. exact `documentEvidenceAssessmentRequest`;
2. exact `documentEvidenceAssessmentResult`;
3. exact pinned Trade Docs DocumentVersion references;
4. context/tenant mismatch fail-closed behavior;
5. documentary verification distinct from regulatory satisfaction;
6. deterministic assessment semantics;
7. Regulations-owned assessment identity;
8. tenant-scoped durable idempotency;
9. concurrent duplicate convergence;
10. PostgreSQL RLS;
11. canonical RTD-08 `requirement-satisfaction.evaluated` event creation;
12. assessment + outbox atomicity;
13. lease/retry/dead-letter outbox behavior;
14. stable event occurrence identity;
15. exact Shared contract tests;
16. real PostgreSQL integration tests.

Therefore the provider path is materially implemented.

### 7.2 Why it remains PARTIAL

The runtime still lacks:

- a production workload-token authenticator;
- a production requirement authority backing the referenced requirement;
- deployed transport binding for `CanonicalEventPublisherPort`;
- governed caller capability-resolution proof at the provider boundary;
- cross-repository workload/audience activation.

Therefore:

```text
regulations.evidence.assess
    = PARTIAL
```

not `IMPLEMENTED`.

---

## 8. Cross-Repository Activation Audit

R-CAP-07 audited these exact repository baselines:

| Authority | Audited revision |
|---|---|
| Shared | `d99288e7f525d87b2d41f1d03245a65115606b8c` |
| IAM | `a927259753a0d2dee16f8df6f5509c5dc9cb18e9` |
| Control Plane | `be2a81465f6b0844bc7a5b6ba2e6cb26991f7c65` |

The current Shared workload registry explicitly states:

```text
No workload holds context:validate yet.
```

It contains no:

```text
baobab-regulations-workload
```

entry.

The current IAM repository likewise contains workload clients for engines such
as Trade, ERP, CMS and Pulse but no Regulations workload client.

The Control Plane already implements the correct validator admission model:

```text
validator must be ACTIVE
+
validator must be allowed context:validate
+
validator must explicitly validate the subject resource-server audience
```

but there is no Regulations registry allocation to consume that runtime path.

This means the Control Plane implementation exists while the Regulations
identity allocation does not.

---

## 9. Required Validator Relationship

Before the Regulations resource server can validate caller-bound contexts in a
real deployment, Shared/IAM must establish an explicit validator relationship
equivalent in meaning to:

```yaml
baobab-regulations-workload:
  repository: baobab-platform/baobab-regulations
  runtime: baobab-regulations service
  environment: production
  allowed_audiences:
    - baobab-control-plane
  allowed_scopes:
    - context:validate
  validates_audiences:
    - baobab-regulations
  status: <PROVISIONED until end-to-end proof>
```

The exact credential type and activation sequence remain IAM/Shared governance
decisions.

The Regulations repository SHALL NOT invent or self-authorise this registry
entry.

---

## 10. Consumer Audience Requirement

A caller of the Regulations provider must present a subject token actually
addressed to the Regulations resource-server audience.

Therefore the eventual proving consumer also needs governed authority to obtain:

```text
aud = baobab-regulations
```

The validator relationship above does not grant that audience to callers.

Caller audience/scopes and the Regulations validator workload are separate
authorisation facts and must be governed separately.

---

## 11. Capability Resolution Gap

R-CAP-04 proves caller-bound `PlatformContext` validation.

It does not yet prove that every direct invocation carries a trusted artifact
showing that the caller previously resolved and was granted the specific
Regulations capability through the Control Plane.

The architecture target remains:

```text
grant
  +
binding
  +
provider
  +
contract
  +
context
  ↓
authorised provider invocation
```

R-CAP-07 therefore treats provider invocation authorisation as a production
hardening gate rather than silently assuming:

```text
valid workload + valid context
    ==
capability entitlement
```

They are not equivalent.

---

## 12. Why IMPLEMENTED Is Rejected

Declaring `IMPLEMENTED` now would imply the canonical contract major is
complete enough for generated runtime registration.

Shared's generator registers only `IMPLEMENTED` support.

That would be premature while the following remain unresolved:

| Gate | Current state |
|---|---|
| exact adapters/routes | complete |
| Shared contract tests | complete |
| durable evidence assessment | complete |
| canonical satisfaction event outbox | complete |
| production requirement authority | missing |
| production resource-server authenticator | missing |
| Regulations validator workload in Shared | missing |
| IAM Regulations workload mechanics | missing |
| caller `baobab-regulations` audience allocation | missing |
| event transport deployment adapter | missing |
| capability-resolution invocation proof | missing |
| EA-09 certification | not performed |
| Control Plane provider registration | intentionally absent |
| provider activation/bindings/grants | intentionally absent |

Therefore:

```text
PARTIAL = truthful
IMPLEMENTED = overclaim
```

---

## 13. Why No Control Plane Registration Is Added

Shared's current registration generator explicitly selects only:

```text
implementation_status == IMPLEMENTED
```

and refuses a provider with no IMPLEMENTED support.

That is the correct behavior for R-CAP-07.

The provider declaration becomes architecture-visible while remaining
non-routable.

No registration bundle, provider lifecycle record, support activation,
CapabilityBinding or CapabilityGrant is created by this decision.

---

## 14. Readiness State After R-CAP-07

```text
Shared canonical capability
        ✅

Repository provider identity
        ✅ baobab-regulations.core

Canonical route implementation
        ✅

Contract tests
        ✅

Durable evidence state
        ✅

Canonical satisfaction event intent
        ✅

Provider declaration
        ✅ PARTIAL

Repository lifecycle
        ✅ active

EA-09 certification
        ❌

Shared validator workload
        ❌

IAM Regulations workload
        ❌

Production auth adapter
        ❌

Production requirement authority
        ❌

Transport deployment binding
        ❌

Control Plane registration
        ❌

Provider activation
        ❌

Bindings/grants/resolution
        ❌
```

---

## 15. Promotion to IMPLEMENTED

Neither support entry may move from `PARTIAL` to `IMPLEMENTED` until at
minimum all capability-local runtime dependencies required by its canonical
contract are production implementations rather than test/local seams.

For `regulations.requirement.resolve`, this includes a durable authoritative
requirement projection repository.

For `regulations.evidence.assess`, this includes the same requirement
authority plus production authentication and a deployable event publication
adapter.

Promotion SHALL include new evidence and a fresh R-CAP readiness decision.

---

## 16. Activation After IMPLEMENTED

Even `IMPLEMENTED` SHALL NOT directly imply activation.

The later chain remains:

```text
IMPLEMENTED
    ↓
EA-09 certification
    ↓
Control Plane provider registration
    ↓
provider lifecycle approval
    ↓
EngineRelease / EngineInstance evidence
    ↓
health
    ↓
CapabilityBinding
    ↓
CapabilityGrant
    ↓
CapabilityResolution
```

No step may be inferred from the previous one.

---

## 17. Invariants

```text
R-CAP-07-001
PARTIAL support is repository implementation evidence, not runtime support.

R-CAP-07-002
No PARTIAL support is generated into EngineRegistration.

R-CAP-07-003
Repository lifecycle active does not mean provider lifecycle ACTIVE.

R-CAP-07-004
production_permitted does not mean production ready.

R-CAP-07-005
A valid PlatformContext does not prove capability entitlement.

R-CAP-07-006
Regulations cannot self-authorise context:validate.

R-CAP-07-007
A validator's validates_audiences does not grant that audience to callers.

R-CAP-07-008
No provider invocation topology is declared without deployment authority.

R-CAP-07-009
No IMPLEMENTED claim is made while production requirement authority is absent.

R-CAP-07-010
Control Plane remains the only activation/binding/grant/resolution authority.
```

---

## 18. Final Decision

> **R-CAP-07 establishes `baobab-regulations.core` as the first real Regulations capability provider and truthfully declares both canonical RTD-06 capabilities PARTIAL. The repository is now an active engine, but the provider remains non-routable and non-certified until production authority adapters, workload identity, event transport, certification and Control Plane activation are independently proven.**

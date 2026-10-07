# ADR-REG-0033 — Canonical Decision Evaluation Contract Adoption and R-CAP-09 Boundary

**Status:** Accepted — Contract Adoption  
**Decision ID:** ADR-REG-0033  
**Engine:** Baobab Regulations  
**Repository:** baobab-platform/baobab-regulations  
**Date:** 2026-10-06  
**Implements:** R-CAP-08  
**Shared Authority:** ADR-SHARED-028  
**Depends On:** ADR-REG-0018, ADR-REG-0019, ADR-REG-0020, ADR-REG-0031, ADR-REG-0032

---

## 1. Decision

Baobab Regulations SHALL adopt the Shared contract for:

```text
regulations.decision.evaluate
```

exactly as defined by:

```text
contracts/regulatory-decision/v1/domain.schema.json
contracts/regulatory-decision/v1/regulations.openapi.yaml
```

The local repository SHALL expose executable Pydantic contract adapters and
contract-conformance tests during R-CAP-08.

R-CAP-08 SHALL NOT implement the production evaluator.

---

## 2. Capability state

The repository declaration SHALL move:

```text
regulations.decision.evaluate

PROPOSED
   ↓
CONTRACTED
```

It SHALL remain under:

```text
planned_capabilities
```

and SHALL NOT be added to:

```text
providers[].support
```

until a later implementation increment provides evidence.

The target provider is:

```text
baobab-regulations.core
```

but target intent is not provider support.

---

## 3. Why the contract comes before the evaluator

The existing repository already has:

```text
RegulatoryPolicyEvaluatorPort
ReferenceEvaluator
domain RegulatoryDecision
rule-set metadata
decision persistence scaffold
```

Those artefacts pre-date a canonical Shared API contract.

R-CAP-08 reverses the dependency direction deliberately:

```text
Shared semantic contract
        ↓
Regulations adapter
        ↓
R-CAP-09 evaluator implementation
```

not:

```text
OPA/Rego runtime
        ↓
whatever JSON it returns
        ↓
platform contract
```

The evaluator implements the contract. It does not define it.

---

## 4. Canonical request adopted

The request requires:

```text
context_id
question
assessment_purpose
decision_stage?
subject_references[]
regulated_activities[]
facts[]
evidence_references[]
rule_set_reference
legal_time
knowledge_time
evaluation_profile
requested_assurance
requested_enforcement_class_ceiling
replay_key
```

No root `tenant_id` is accepted.

Trusted tenant authority remains caller-bound Control Plane context.

---

## 5. Cross-engine references

R-CAP-08 reuses ADR-SHARED-021 reference semantics already adopted by RTD-06.

Consequential inputs are pinned.

The contract introduces Regulations-owned pinned types:

```text
REGULATORY_RULE_SET
REGULATORY_RULE_VERSION
REGULATORY_ASSESSMENT
REGULATORY_DECISION
```

and generic pinned references for externally owned subjects/evidence/legal
basis.

A reference preserves authority; it does not copy or take ownership of the
foreign aggregate.

---

## 6. Legal time and knowledge time

Both are mandatory semantic inputs.

```text
legal_time
    what regulatory state applies then?

knowledge_time
    what verified regulatory knowledge perspective is being used?
```

R-CAP-09 MUST evaluate against these fields explicitly.

It MUST NOT quietly replace them with current wall-clock time.

---

## 7. Regulatory question

The API does not accept an ambiguous generic "compliance" question.

Every evaluation declares the question, including:

```text
MAY_TRANSACTION_PROCEED
WHAT_OBLIGATIONS_APPLY
WHAT_REQUIREMENTS_REMAIN
WHAT_DOCUMENTS_ARE_REQUIRED
IS_REQUIREMENT_SATISFIED
IS_ACTION_PROHIBITED
IS_EXPLICIT_PERMISSION_AVAILABLE
WHAT_DUTY_OR_AMOUNT_APPLIES
WHAT_REGULATORY_GAPS_EXIST
WHAT_CHANGED
WHAT_WOULD_APPLY_AT_FUTURE_TIME
```

This vocabulary may evolve only through Shared contract governance.

---

## 8. Facts are bounded inputs

The canonical boundary accepts typed scalar facts:

```text
fact_code
value
observed_at
unit?
currency?
source_reference?
```

R-CAP-09 SHALL not require callers to provide evaluator-specific input trees.

Any conversion from canonical facts to an evaluator input document belongs
behind the evaluator anti-corruption boundary.

---

## 9. Pinned rule set

Every request carries one pinned Regulations-owned:

```text
REGULATORY_RULE_SET
```

Every response returns:

```text
same semantic rule-set identity
+
rule_set_fingerprint
```

R-CAP-09 MUST prove that the loaded executable artefact corresponds to the
requested pinned rule set/fingerprint.

---

## 10. Outcomes

The canonical decision outcome is:

```text
SATISFIED
SATISFIED_WITH_REQUIREMENTS
UNSATISFIED
PROHIBITED
INDETERMINATE
NOT_APPLICABLE
```

No evaluator/runtime failure is an outcome.

---

## 11. Technical failures remain technical

R-CAP-09 SHALL preserve at least these semantic distinctions:

```text
EVALUATOR_UNDEFINED
EVALUATOR_PROTOCOL_ERROR
EVALUATOR_RUNTIME_ERROR
EVALUATOR_NOT_READY
```

They map to technical ProblemDetails, not:

```text
UNSATISFIED
INDETERMINATE
NOT_APPLICABLE
```

An unavailable policy engine does not mean the business is non-compliant.

---

## 12. Decision response

The adopted response contains:

```text
decision_reference
assessment_reference
outcome
enforcement_class
reasons[]
legal_basis_references[]
evidence_references[]
recommended_disposition | null
rule_set_reference
rule_set_fingerprint
evaluated_at
legal_time
knowledge_time
provenance
replay_identity
```

The structure is intentionally richer than the current scaffold
`RegulatoryDecision` domain model.

R-CAP-09 SHALL reconcile the domain model to the canonical response, not weaken
the Shared response to fit the scaffold.

---

## 13. Structured reasons

Each reason contains:

```text
stable code
message
legal basis references
rule version references
evidence references
```

Canonical explanation depends on these structured facts.

OPA traces, logs or hidden model reasoning are not canonical decision reasons.

---

## 14. Enforcement boundary

`recommended_disposition` is non-enforcing.

```text
Regulations = PDP
Domain owner = PEP
```

R-CAP-09 MUST NOT add operational shipment/order mutation to
`regulations.decision.evaluate`.

---

## 15. Idempotency vs replay

The HTTP request uses:

```text
Idempotency-Key
```

The semantic body uses:

```text
replay_key
```

They remain different identities.

The production implementation will need durable command idempotency while also
preserving semantic replay identity/fingerprints.

---

## 16. Provider-neutral provenance

Canonical provenance includes:

```text
contract major
input fingerprint
rule-set identity
rule-set fingerprint
evaluation profile
```

Implementation provenance may separately contain:

```text
OPA decision_id
bundle revision
compiler revision
compiled artefact fingerprint
runtime version
trace identifiers
```

but those values do not enter the Shared decision contract.

---

## 17. Existing ReferenceEvaluator

The current `ReferenceEvaluator` remains:

```text
offline scaffold / golden-test evaluator
```

It is not promoted to the production provider by R-CAP-08.

Its current output also does not yet satisfy the entire R-CAP-08 canonical
response.

R-CAP-09 must either adapt/reconcile it for differential testing or replace its
runtime role while retaining it as a reference oracle where useful.

---

## 18. Existing evaluator port

`RegulatoryPolicyEvaluatorPort` remains the provider-neutral execution seam.

R-CAP-09 is expected to evolve its input/output types so it consumes canonical
decision input semantics and returns a result sufficient to assemble the exact
Shared response.

The port SHALL continue to avoid OPA types.

---

## 19. Production evaluator boundary for R-CAP-09

The expected R-CAP-09 architecture is:

```text
DecisionEvaluateRequest
        │
        ▼
authority/context validation
        │
        ▼
canonical input snapshot
        │
        ▼
rule-set resolver
        │
        ▼
verified executable artefact
        │
        ▼
RegulatoryPolicyEvaluatorPort
        │
        ├── production evaluator adapter (OPA initially)
        └── reference evaluator (differential/golden proof)
        │
        ▼
decision assembler
        │
        ▼
DecisionEvaluateResponse
        │
        ├── durable decision/replay material
        └── canonical event intent where contracted
```

---

## 20. R-CAP-09 mandatory proof

Before `regulations.decision.evaluate` may become provider support, R-CAP-09
must demonstrate:

1. exact Shared request acceptance;
2. caller-bound context/tenant enforcement;
3. pinned rule-set resolution;
4. rule-set fingerprint equality;
5. legal-time evaluation;
6. knowledge-time evaluation;
7. bounded canonical fact translation;
8. evidence/reference authority validation;
9. deterministic evaluator invocation;
10. undefined-result failure;
11. protocol-error failure;
12. runtime-unavailable failure;
13. evaluator-not-ready failure;
14. result-schema validation;
15. structured reason/legal/evidence assembly;
16. enforcement-class ceiling behavior;
17. durable command idempotency;
18. replay identity/fingerprint persistence;
19. no operational business-state mutation;
20. differential/golden conformance against the reference evaluator for the
    supported BRIR subset.

---

## 21. R-CAP-08 is not implementation evidence

The following are contract-adoption evidence:

```text
src/baobab_regulations/contracts/decision.py
tests/contract/test_r_cap_08_decision_contract.py
```

They prove:

```text
Regulations understands the canonical contract
```

They do not prove:

```text
baobab-regulations.core implements regulations.decision.evaluate
```

Therefore the capability remains CONTRACTED, not PARTIAL.

---

## 22. R-CAP-10 boundary

R-CAP-10 may promote provider support only after R-CAP-09 and the other
production-readiness dependencies described by ADR-REG-0032 are complete.

Even then:

```text
IMPLEMENTED != certified != ACTIVE != bound != granted != resolved
```

---

## 23. Final decision

> **R-CAP-08 adopts Shared's canonical `regulations.decision.evaluate`
> semantics exactly, moves the capability from PROPOSED to CONTRACTED, and
> creates executable contract adapters/tests. It deliberately stops before
> production evaluation. R-CAP-09 must implement the contract; it may not
> redefine it around OPA or any other evaluator.**

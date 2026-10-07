#!/usr/bin/env python3
"""R-CAP-09 production evaluator implementation invariants."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

DECISION_KEY = "regulations.decision.evaluate"
BASE_PARTIAL = {
    "regulations.requirement.resolve",
    "regulations.evidence.assess",
}


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return value


def fail(message: str) -> None:
    raise SystemExit(f"R-CAP-09 FAIL: {message}")


def require_text(path: Path, *needles: str) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path}: missing required production-evaluator marker {needle!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repository_root.resolve()

    declaration = load_yaml(root / ".baobab/capability-provider.yaml")
    providers = declaration.get("providers")
    if not isinstance(providers, list) or len(providers) != 1:
        fail("exactly one Regulations core provider must remain declared")

    provider = providers[0]
    if not isinstance(provider, dict):
        fail("provider declaration must be an object")
    if provider.get("provider_key") != "baobab-regulations.core":
        fail("R-CAP-09 must implement baobab-regulations.core")
    if "invocation" in provider:
        fail("R-CAP-09 implementation must not invent deployment invocation topology")

    support = provider.get("support")
    if not isinstance(support, list):
        fail("provider support must be a list")
    support_by_key = {
        item.get("capability_key"): item
        for item in support
        if isinstance(item, dict)
    }
    if not BASE_PARTIAL.issubset(support_by_key):
        fail("R-CAP-09 must preserve R-CAP-07 base support")
    decision = support_by_key.get(DECISION_KEY)
    if not isinstance(decision, dict):
        fail("decision.evaluate must enter provider support at R-CAP-09")
    if decision.get("implementation_status") != "PARTIAL":
        fail("decision.evaluate must remain PARTIAL until R-CAP-10")
    if decision.get("contract_versions") != [1]:
        fail("decision.evaluate must implement only canonical contract major 1")

    evidence = decision.get("implementation_evidence")
    if not isinstance(evidence, list) or not evidence:
        fail("decision.evaluate PARTIAL support requires implementation evidence")
    evidence_paths = {
        item.get("path")
        for item in evidence
        if isinstance(item, dict)
    }
    required_evidence = {
        "src/baobab_regulations/brir/models.py",
        "src/baobab_regulations/brir/compiler.py",
        "src/baobab_regulations/application/services/decision_evaluation.py",
        "src/baobab_regulations/infrastructure/opa/client.py",
        "src/baobab_regulations/infrastructure/rule_sets.py",
        "src/baobab_regulations/infrastructure/persistence/decision_idempotency_postgres.py",
        "migrations/000005_regulatory_decision_evaluations.sql",
        "tests/unit/test_brir_compiler.py",
        "tests/unit/test_opa_evaluator.py",
        "tests/unit/test_decision_evaluation.py",
        "tests/unit/test_rule_set_authority.py",
        "tests/api/test_r_cap_09_decision_route.py",
        "tests/integration/test_live_opa_decision_evaluation.py",
        "tests/integration/test_postgres_decision_evaluation.py",
    }
    missing = required_evidence - evidence_paths
    if missing:
        fail(f"decision.evaluate evidence is incomplete: {sorted(missing)}")
    for path in required_evidence:
        if not (root / path).is_file():
            fail(f"declared R-CAP-09 evidence does not exist: {path}")

    planned = declaration.get("planned_capabilities")
    if not isinstance(planned, list):
        fail("planned capability registry must remain present")
    if any(
        isinstance(item, dict)
        and (
            item.get("capability_key") == DECISION_KEY
            or item.get("proposed_key") == DECISION_KEY
        )
        for item in planned
    ):
        fail("decision.evaluate cannot remain planned once PARTIAL support exists")

    if any(
        isinstance(item, dict) and item.get("implementation_status") == "IMPLEMENTED"
        for item in support
    ):
        fail("R-CAP-09 must not promote any Regulations capability to IMPLEMENTED")

    require_text(
        root / "src/baobab_regulations/brir/compiler.py",
        'compiler_id = "baobab-regulations-rego"',
        'compiler_version = "1"',
        'target = "rego/v1"',
        'entrypoint = "baobab/regulations/decision"',
        'decision_outcome := "NOT_APPLICABLE"',
        "artifact_fingerprint",
    )
    require_text(
        root / "src/baobab_regulations/infrastructure/opa/client.py",
        '"/health"',
        '"bundles": "true"',
        '"/v1/data/',
        "EvaluatorUndefinedError",
        "EvaluatorProtocolError",
        "EvaluatorRuntimeError",
        "EvaluatorNotReadyError",
        "input_fingerprint",
        "rule_set_fingerprint",
    )
    require_text(
        root / "src/baobab_regulations/application/services/decision_evaluation.py",
        "legal_time=request.legal_time",
        "knowledge_time=request.knowledge_time",
        "requested_enforcement_class_ceiling",
        "replay_key=request.replay_key",
        "DecisionEvaluationIdempotencyPort",
    )
    require_text(
        root / "migrations/000005_regulatory_decision_evaluations.sql",
        "UNIQUE (tenant_id, idempotency_key)",
        "UNIQUE (tenant_id, replay_key)",
        "ENABLE ROW LEVEL SECURITY",
        "FORCE ROW LEVEL SECURITY",
        "regulatory_rule_sets_scope_isolation",
    )
    require_text(
        root / "src/baobab_regulations/api/routes.py",
        '"/decisions/evaluate"',
        'operation_id="evaluateRegulatoryDecision"',
        "DecisionEvaluatorUndefinedError",
    )

    if (root / "tests/fixtures/opa/r_cap_09.rego").exists():
        fail("live R-CAP-09 policy must be compiler-generated from BRIR, not handwritten Rego")

    # The reference evaluator is a differential/golden oracle, never the
    # production service dependency.
    service_text = (
        root / "src/baobab_regulations/application/services/decision_evaluation.py"
    ).read_text(encoding="utf-8")
    if "ReferenceEvaluator" in service_text:
        fail("production decision service must not depend on ReferenceEvaluator")

    print(
        "R-CAP-09 production evaluator passed: OPA anti-corruption boundary, "
        "bitemporal rule-set authority, durable replay/RLS, authenticated route, "
        "decision.evaluate PARTIAL support and zero IMPLEMENTED/activation claim"
    )


if __name__ == "__main__":
    main()

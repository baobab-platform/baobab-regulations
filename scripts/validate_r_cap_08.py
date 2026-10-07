#!/usr/bin/env python3
"""R-CAP-08 contract-adoption maturity invariants."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

DECISION_KEY = "regulations.decision.evaluate"


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return value


def fail(message: str) -> None:
    raise SystemExit(f"R-CAP-08 FAIL: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--shared-root", type=Path, default=Path(".shared"))
    args = parser.parse_args()

    root = args.repository_root.resolve()
    shared = args.shared_root.resolve()

    declaration = load_yaml(root / ".baobab/capability-provider.yaml")
    providers = declaration.get("providers")
    if not isinstance(providers, list) or len(providers) != 1:
        fail("exactly one Regulations provider must remain declared")

    provider = providers[0]
    if not isinstance(provider, dict):
        fail("provider declaration must be an object")
    support = provider.get("support")
    if not isinstance(support, list):
        fail("provider support must be a list")
    decision_support = [
        item
        for item in support
        if isinstance(item, dict) and item.get("capability_key") == DECISION_KEY
    ]
    if decision_support:
        if len(decision_support) != 1:
            fail("decision.evaluate must have one provider support entry")
        if decision_support[0].get("implementation_status") != "PARTIAL":
            fail("R-CAP-09 follow-on may promote decision.evaluate only to PARTIAL")

    planned = declaration.get("planned_capabilities")
    if not isinstance(planned, list):
        fail("planned_capabilities must remain present")
    contracted = [
        item
        for item in planned
        if isinstance(item, dict) and item.get("capability_key") == DECISION_KEY
    ]
    if decision_support:
        if contracted:
            fail("R-CAP-09 provider support must remove decision.evaluate from planned_capabilities")
        decision = decision_support[0]
    else:
        if len(contracted) != 1:
            fail("decision.evaluate must remain CONTRACTED until implementation exists")
        decision = contracted[0]
        if decision.get("proposal_status") != "CONTRACTED":
            fail("decision.evaluate must be CONTRACTED after Shared R-CAP-08")
        if decision.get("target_provider_key") != "baobab-regulations.core":
            fail("decision.evaluate target provider must remain baobab-regulations.core")
        if "proposed_key" in decision:
            fail("a CONTRACTED capability must not retain proposed_key")

    provenance = decision.get("provenance")
    if not isinstance(provenance, dict):
        fail("decision.evaluate must retain Shared provenance")
    authority = provenance.get("authority")
    if not isinstance(authority, dict):
        fail("decision.evaluate provenance authority is missing")
    if authority.get("repository") != "baobab-platform/shared":
        fail("Shared must be the canonical decision contract authority")
    if authority.get("decision") != "ADR-SHARED-028":
        fail("decision.evaluate must cite ADR-SHARED-028")

    catalogue = load_yaml(shared / "contracts/capability/v1/catalogue.yaml")
    catalogued = {
        item.get("capability_key")
        for item in (catalogue.get("capabilities") or [])
        if isinstance(item, dict)
    }
    if DECISION_KEY not in catalogued:
        fail("pinned Shared checkout does not catalogue decision.evaluate")

    definitions = load_yaml(shared / "contracts/regulations/v1/capabilities.yaml")
    definition = next(
        (
            item
            for item in (definitions.get("capabilities") or [])
            if isinstance(item, dict) and item.get("capability_key") == DECISION_KEY
        ),
        None,
    )
    if not isinstance(definition, dict):
        fail("pinned Shared checkout has no decision.evaluate definition")
    if definition.get("lifecycle") != "DRAFT" or definition.get("maturity") != "EXPERIMENTAL":
        fail("R-CAP-08 must not promote canonical capability lifecycle/maturity")
    contracts = definition.get("contracts")
    if not isinstance(contracts, list) or len(contracts) != 1:
        fail("decision.evaluate must define exactly one contract major in R-CAP-08")
    if contracts[0].get("major") != 1:
        fail("decision.evaluate must adopt contract major 1")

    required_local = (
        root / "src/baobab_regulations/contracts/decision.py",
        root / "tests/contract/test_r_cap_08_decision_contract.py",
        root
        / "docs/adr/ADR-REG-0033 — Canonical Decision Evaluation Contract Adoption and R-CAP-09 Boundary.md",
    )
    for path in required_local:
        if not path.is_file():
            fail(f"missing local R-CAP-08 adoption evidence: {path.relative_to(root)}")

    routes = (root / "src/baobab_regulations/api/routes.py").read_text(encoding="utf-8")
    runtime_markers = ("/decisions/evaluate", "evaluateRegulatoryDecision")
    if decision_support:
        for marker in runtime_markers:
            if marker not in routes:
                fail(f"R-CAP-09 provider support requires runtime route marker {marker}")
    else:
        for marker in runtime_markers:
            if marker in routes:
                fail(f"R-CAP-08 CONTRACTED-only state must not expose {marker}")

    profile = load_yaml(root / ".baobab/rtd-conformance.yaml")
    shared_profile = profile.get("shared")
    if not isinstance(shared_profile, dict):
        fail("RTD profile Shared section is missing")
    pin = shared_profile.get("commit")
    source_revision = provenance.get("source_revision")
    if pin != source_revision:
        fail(
            "decision contract provenance must use the same Shared revision as RTD-10"
        )
    required_contracts = set(shared_profile.get("required_contracts") or [])
    for path in (
        "contracts/regulatory-decision/v1/domain.schema.json",
        "contracts/regulatory-decision/v1/regulations.openapi.yaml",
    ):
        if path not in required_contracts:
            fail(f"RTD-10 profile must require {path}")

    print(
        "R-CAP-08/R-CAP-09 maturity passed: canonical decision contract remains "
        "governed while later PARTIAL implementation may add runtime support"
    )


if __name__ == "__main__":
    main()

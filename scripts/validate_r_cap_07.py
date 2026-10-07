#!/usr/bin/env python3
"""R-CAP-07 local provider-readiness invariants.

This script validates the Regulations-owned decision. Shared's
capability_catalogue.py remains the authority for canonical schema/catalogue
conformance.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

CANONICAL_SUPPORT = {
    "regulations.evidence.assess",
    "regulations.requirement.resolve",
}
PROPOSED_ONLY = {
    "regulations.change.subscribe",
    "regulations.context.resolve",
    "regulations.decision.evaluate",
    "regulations.pack.compose",
}


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return value


def fail(message: str) -> None:
    raise SystemExit(f"R-CAP-07 FAIL: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repository_root.resolve()

    repository = load_yaml(root / ".baobab/repository.yaml")
    repo_meta = repository.get("repository")
    if not isinstance(repo_meta, dict) or repo_meta.get("lifecycle") != "active":
        fail("provider support requires repository.lifecycle=active")

    declaration = load_yaml(root / ".baobab/capability-provider.yaml")
    providers = declaration.get("providers")
    if not isinstance(providers, list) or len(providers) != 1:
        fail("exactly one Regulations provider must be declared at R-CAP-07")

    provider = providers[0]
    if not isinstance(provider, dict):
        fail("provider declaration must be an object")
    if provider.get("provider_key") != "baobab-regulations.core":
        fail("the first canonical provider must be baobab-regulations.core")
    if provider.get("provider_type") != "BAOBAB_ENGINE":
        fail("core provider must be a BAOBAB_ENGINE")
    if provider.get("implementation_key") != "core":
        fail("core provider implementation_key must remain provider-neutral")
    if provider.get("simulated") is not False:
        fail("core provider is real implementation, not a simulation")
    if provider.get("production_permitted") is not True:
        fail("core provider must remain eligible for later governed production promotion")
    if "invocation" in provider:
        fail("R-CAP-07 must not claim governed invocation/deployment topology")

    support = provider.get("support")
    if not isinstance(support, list):
        fail("core provider must declare support")
    support_keys = {
        item.get("capability_key")
        for item in support
        if isinstance(item, dict)
    }
    if support_keys != CANONICAL_SUPPORT:
        fail(f"support must be exactly {sorted(CANONICAL_SUPPORT)}")

    for item in support:
        if not isinstance(item, dict):
            fail("support entries must be objects")
        capability = item.get("capability_key")
        if item.get("implementation_status") != "PARTIAL":
            fail(f"{capability} must remain PARTIAL at R-CAP-07")
        if item.get("contract_versions") != [1]:
            fail(f"{capability} must implement only canonical contract major 1")
        evidence = item.get("implementation_evidence")
        if not isinstance(evidence, list) or not evidence:
            fail(f"{capability} must carry implementation evidence")
        for entry in evidence:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                fail(f"{capability} has malformed implementation evidence")
            evidence_path = (root / entry["path"]).resolve()
            if root not in evidence_path.parents and evidence_path != root:
                fail(f"{capability} evidence escapes repository: {entry['path']}")
            if not evidence_path.exists():
                fail(f"{capability} evidence does not exist: {entry['path']}")

    planned = declaration.get("planned_capabilities")
    if not isinstance(planned, list):
        fail("broader Regulations proposals must remain visible")
    contracted_in_planned = {
        item.get("capability_key")
        for item in planned
        if isinstance(item, dict) and item.get("proposal_status") == "CONTRACTED"
    }
    if contracted_in_planned:
        fail(
            "canonical supported capabilities must not remain duplicated under "
            f"planned_capabilities: {sorted(contracted_in_planned)}"
        )

    proposed = {
        item.get("proposed_key")
        for item in planned
        if isinstance(item, dict) and item.get("proposal_status") == "PROPOSED"
    }
    if proposed != PROPOSED_ONLY:
        fail(f"broader proposals changed unexpectedly: {sorted(proposed)}")

    print(
        "R-CAP-07 provider readiness passed: active repository, "
        "baobab-regulations.core, two PARTIAL canonical supports, "
        "zero IMPLEMENTED/runtime activation claims"
    )


if __name__ == "__main__":
    main()

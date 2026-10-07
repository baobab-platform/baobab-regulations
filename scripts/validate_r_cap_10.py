#!/usr/bin/env python3
"""R-CAP-10 fail-closed promotion decision: local proof != external acceptance.

This validator deliberately accepts *no* self-asserted external verification.
Future promotion must replace this gate with a trusted cross-repository
attestation verifier, not change BLOCKED to VERIFIED in a local YAML file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

CAPABILITIES = {
    "regulations.requirement.resolve",
    "regulations.evidence.assess",
    "regulations.decision.evaluate",
}
EXTERNAL_GATES = {
    "requirement_ingestion_authority",
    "source_backed_regulatory_assurance",
    "signed_policy_bundle_and_trust",
    "resource_server_authentication",
    "identity_and_audience_allocation",
    "invocation_authorization",
    "event_transport_binding",
}
ACTIVATION_GATES = {
    "ea_09_certification",
    "provider_lifecycle_registration",
    "engine_release_instance_health",
    "capability_binding_grants_resolution",
}

GATE_OWNERS = {
    "requirement_ingestion_authority": "baobab-regulations",
    "source_backed_regulatory_assurance": "baobab-regulations",
    "signed_policy_bundle_and_trust": "infrastructure",
    "resource_server_authentication": "baobab-iam",
    "identity_and_audience_allocation": "baobab-iam",
    "invocation_authorization": "baobab-cp",
    "event_transport_binding": "infrastructure",
    "ea_09_certification": "platform-certification",
    "provider_lifecycle_registration": "baobab-cp",
    "engine_release_instance_health": "baobab-cp",
    "capability_binding_grants_resolution": "baobab-cp",
}


class ReadinessInvariantError(ValueError):
    """The source tree tries to claim or imply unsupported provider readiness."""


def _object(path: Path) -> dict[str, Any]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ReadinessInvariantError(f"{path}: expected YAML object")
    return doc


def evaluate_readiness(root: Path) -> dict[str, Any]:
    manifest = _object(root / ".baobab/r-cap-10-readiness.yaml")
    declaration = _object(root / ".baobab/capability-provider.yaml")
    if manifest.get("schema") != "baobab-regulations-r-cap-10-readiness":
        raise ReadinessInvariantError("R-CAP-10 manifest has wrong schema")
    if manifest.get("version") != "1.0" or manifest.get("programme") != "R-CAP-10":
        raise ReadinessInvariantError("R-CAP-10 manifest schema/version is not pinned")
    if manifest.get("provider_key") != "baobab-regulations.core":
        raise ReadinessInvariantError("manifest provider must be baobab-regulations.core")
    if manifest.get("decision") != "DEFER_PROMOTION":
        raise ReadinessInvariantError("promotion cannot be approved by self-declaration")
    if manifest.get("implementation_status_ceiling") != "PARTIAL":
        raise ReadinessInvariantError("status ceiling must remain PARTIAL")

    external = manifest.get("external_gates")
    activation = manifest.get("activation_gates")
    if not isinstance(external, dict) or set(external) != EXTERNAL_GATES:
        raise ReadinessInvariantError("external acceptance gates missing or unknown")
    if not isinstance(activation, dict) or set(activation) != ACTIVATION_GATES:
        raise ReadinessInvariantError("EA-09/Control Plane activation gates missing or unknown")

    for gate_id, gate in {**external, **activation}.items():
        if not isinstance(gate, dict) or not gate.get("owner"):
            raise ReadinessInvariantError(f"{gate_id}: missing independent owner")
        if gate.get("owner") != GATE_OWNERS[gate_id]:
            raise ReadinessInvariantError(
                f"{gate_id}: authority owner must remain {GATE_OWNERS[gate_id]}"
            )
        if gate.get("state") != "BLOCKED" or gate.get("evidence") is not None:
            raise ReadinessInvariantError(
                f"{gate_id}: locally asserted evidence is not an independently "
                "verified platform/EA-09 attestation"
            )

    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, dict) or set(capabilities) != CAPABILITIES:
        raise ReadinessInvariantError("all three canonical capability gates are required")

    providers = declaration.get("providers")
    if not isinstance(providers, list) or len(providers) != 1:
        raise ReadinessInvariantError("one canonical Regulations provider is required")
    provider = providers[0]
    if not isinstance(provider, dict) or provider.get("provider_key") != manifest["provider_key"]:
        raise ReadinessInvariantError("readiness manifest and provider declaration disagree")
    if "invocation" in provider:
        raise ReadinessInvariantError("deployment invocation cannot be declared without authority")
    supports = provider.get("support")
    if not isinstance(supports, list):
        raise ReadinessInvariantError("no provider support declarations")
    support_by_key = {
        record.get("capability_key"): record
        for record in supports if isinstance(record, dict)
    }
    if set(support_by_key) != CAPABILITIES or len(supports) != len(CAPABILITIES):
        raise ReadinessInvariantError("provider support must contain exactly canonical tranche")

    results: dict[str, Any] = {}
    for capability, config in capabilities.items():
        if not isinstance(config, dict):
            raise ReadinessInvariantError(f"{capability}: malformed evidence")
        gates = config.get("promotion_gates")
        sources = config.get("locally_proven")
        if not isinstance(gates, list) or not gates or len(set(gates)) != len(gates):
            raise ReadinessInvariantError(f"{capability}: missing promotion prerequisites")
        if not isinstance(sources, list) or not sources or len(set(sources)) != len(sources):
            raise ReadinessInvariantError(f"{capability}: missing local implementation sources")
        if not set(gates).issubset(EXTERNAL_GATES):
            raise ReadinessInvariantError(f"{capability}: unknown external gate")
        for path in sources:
            if not isinstance(path, str) or not path.startswith(("src/", "tests/", "migrations/")):
                raise ReadinessInvariantError(f"{capability}: invalid local source path")
            if not (root / path).is_file():
                raise ReadinessInvariantError(f"{capability}: local evidence not found: {path}")
        claim = support_by_key[capability]
        declared_evidence = claim.get("implementation_evidence")
        if not isinstance(declared_evidence, list) or not declared_evidence:
            raise ReadinessInvariantError(
                f"{capability}: provider declaration is missing implementation evidence"
            )
        declared_paths = {
            item.get("path")
            for item in declared_evidence
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        missing_declared = set(sources) - declared_paths
        if missing_declared:
            raise ReadinessInvariantError(
                f"{capability}: provider implementation evidence omits local proof: "
                f"{sorted(missing_declared)}"
            )
        if claim.get("implementation_status") != "PARTIAL":
            raise ReadinessInvariantError(
                f"{capability}: IMPLEMENTED is unsupported without independent "
                "accepted promotion evidence"
            )
        if claim.get("contract_versions") != [1]:
            raise ReadinessInvariantError(f"{capability}: contract major mismatch")
        results[capability] = {
            "implementation_status": "PARTIAL",
            "promotable": False,
            "blocked_by": gates,
            "local_evidence_count": len(sources),
        }

    return {
        "programme": "R-CAP-10",
        "decision": "DEFER_PROMOTION",
        "provider": manifest["provider_key"],
        "activation_authorized": False,
        "capabilities": results,
        "activation_blockers": sorted(ACTIVATION_GATES),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--report", type=Path)
    parser.add_argument("--require-promotable", action="store_true")
    args = parser.parse_args()
    report = evaluate_readiness(args.repository_root.resolve())
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    if args.require_promotable:
        raise SystemExit("R-CAP-10: promotion is BLOCKED by independent authorities")


if __name__ == "__main__":
    main()

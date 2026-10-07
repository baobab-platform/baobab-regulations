"""R-CAP-10 readiness is an evidence gate, not a YAML status toggle."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
import yaml


def _load_readiness_validator() -> ModuleType:
    path = Path(__file__).resolve().parents[2] / "scripts" / "validate_r_cap_10.py"
    spec = importlib.util.spec_from_file_location("r_cap_10_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load R-CAP-10 validator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_validator = _load_readiness_validator()
ReadinessInvariantError = _validator.ReadinessInvariantError
evaluate_readiness = _validator.evaluate_readiness


def _fixture_tree(tmp_path: Path) -> Path:
    source = Path(".baobab")
    destination = tmp_path / ".baobab"
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("r-cap-10-readiness.yaml", "capability-provider.yaml"):
        (destination / name).write_text(
            (source / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    manifest = yaml.safe_load(
        (destination / "r-cap-10-readiness.yaml").read_text(encoding="utf-8")
    )
    for capability in manifest["capabilities"].values():
        for relative in capability["locally_proven"]:
            path = tmp_path / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("test evidence fixture\n", encoding="utf-8")
    return tmp_path


def _edit(root: Path, filename: str, mutate: object) -> None:
    path = root / ".baobab" / filename
    obj = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutate(obj)  # type: ignore[operator]
    path.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")


def test_current_declaration_remains_partial_and_non_routable() -> None:
    report = evaluate_readiness(Path(".").resolve())
    assert report["decision"] == "DEFER_PROMOTION"
    assert report["activation_authorized"] is False
    assert len(report["capabilities"]) == 3
    for cap in report["capabilities"].values():
        assert cap["implementation_status"] == "PARTIAL"
        assert cap["promotable"] is False
        assert cap["blocked_by"]


def test_unverified_yaml_cannot_self_promote_to_implemented(tmp_path: Path) -> None:
    root = _fixture_tree(tmp_path)

    def promote(doc: dict) -> None:
        doc["providers"][0]["support"][0]["implementation_status"] = "IMPLEMENTED"

    _edit(root, "capability-provider.yaml", promote)
    with pytest.raises(ReadinessInvariantError, match="IMPLEMENTED"):
        evaluate_readiness(root)


def test_fake_external_attestation_cannot_self_certify(tmp_path: Path) -> None:
    root = _fixture_tree(tmp_path)

    def forge(doc: dict) -> None:
        doc["external_gates"]["signed_policy_bundle_and_trust"]["state"] = "VERIFIED"
        doc["external_gates"]["signed_policy_bundle_and_trust"]["evidence"] = {
            "self_report": "opa ready"
        }

    _edit(root, "r-cap-10-readiness.yaml", forge)
    with pytest.raises(ReadinessInvariantError, match="independently"):
        evaluate_readiness(root)


def test_deleting_an_identity_or_invocation_gate_fails_closed(tmp_path: Path) -> None:
    root = _fixture_tree(tmp_path)

    def remove(doc: dict) -> None:
        del doc["external_gates"]["invocation_authorization"]

    _edit(root, "r-cap-10-readiness.yaml", remove)
    with pytest.raises(ReadinessInvariantError, match="gates"):
        evaluate_readiness(root)


def test_missing_local_evidence_is_rejected(tmp_path: Path) -> None:
    root = _fixture_tree(tmp_path)
    manifest = yaml.safe_load(
        (root / ".baobab/r-cap-10-readiness.yaml").read_text(encoding="utf-8")
    )
    missing = manifest["capabilities"]["regulations.requirement.resolve"]["locally_proven"][0]
    (root / missing).unlink()
    with pytest.raises(ReadinessInvariantError, match="evidence not found"):
        evaluate_readiness(root)


def test_local_readiness_proof_must_be_declared_as_provider_evidence(
    tmp_path: Path,
) -> None:
    root = _fixture_tree(tmp_path)

    def omit(doc: dict) -> None:
        support = next(
            item
            for item in doc["providers"][0]["support"]
            if item["capability_key"] == "regulations.requirement.resolve"
        )
        support["implementation_evidence"] = [
            item
            for item in support["implementation_evidence"]
            if item["path"]
            != "src/baobab_regulations/infrastructure/persistence/requirements_postgres.py"
        ]

    _edit(root, "capability-provider.yaml", omit)
    with pytest.raises(ReadinessInvariantError, match="omits local proof"):
        evaluate_readiness(root)


def test_bad_activation_and_new_capability_claims_fail_closed(tmp_path: Path) -> None:
    root = _fixture_tree(tmp_path)

    def fake_activation(doc: dict) -> None:
        doc["activation_gates"]["ea_09_certification"]["state"] = "VERIFIED"

    _edit(root, "r-cap-10-readiness.yaml", fake_activation)
    with pytest.raises(ReadinessInvariantError, match="independently"):
        evaluate_readiness(root)

    root = _fixture_tree(tmp_path)

    def new_capability(doc: dict) -> None:
        extra = copy.deepcopy(doc["capabilities"]["regulations.requirement.resolve"])
        doc["capabilities"]["regulations.pack.compose"] = extra

    _edit(root, "r-cap-10-readiness.yaml", new_capability)
    with pytest.raises(ReadinessInvariantError, match="three canonical"):
        evaluate_readiness(root)

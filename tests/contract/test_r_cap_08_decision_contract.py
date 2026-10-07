"""Exact Shared R-CAP-08 decision-evaluation contract proof."""

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, RefResolver
from pydantic import ValidationError

from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
)

SHARED_ROOT = Path(".shared")
CONTRACTS_ROOT = SHARED_ROOT / "contracts"
SCHEMA_PATH = CONTRACTS_ROOT / "regulatory-decision/v1/domain.schema.json"
REQUEST_EXAMPLE = CONTRACTS_ROOT / "regulatory-decision/v1/examples/evaluate-request.json"
RESPONSE_EXAMPLE = CONTRACTS_ROOT / "regulatory-decision/v1/examples/evaluate-response.json"

if not SCHEMA_PATH.exists():
    pytest.skip(
        "pinned Shared checkout is required for R-CAP-08 contract tests",
        allow_module_level=True,
    )


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object in {path}")
    return value


def _schema_store() -> dict[str, dict[str, Any]]:
    store: dict[str, dict[str, Any]] = {}
    for path in CONTRACTS_ROOT.rglob("*.json"):
        try:
            schema = _load_json(path)
        except (json.JSONDecodeError, TypeError):
            continue
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            store[schema_id] = schema
    return store


ROOT_SCHEMA = _load_json(SCHEMA_PATH)
STORE = _schema_store()
RESOLVER = RefResolver.from_schema(ROOT_SCHEMA, store=STORE)


def _validate(definition: str, payload: dict[str, Any]) -> None:
    Draft202012Validator(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": f"{ROOT_SCHEMA['$id']}#/$defs/{definition}",
        },
        resolver=RESOLVER,
        format_checker=FormatChecker(),
    ).validate(payload)


@pytest.mark.contract
def test_shared_decision_request_round_trips_exactly() -> None:
    shared_request = _load_json(REQUEST_EXAMPLE)

    adapted = DecisionEvaluateRequest.model_validate(shared_request)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_request
    _validate("decisionEvaluateRequest", serialized)


@pytest.mark.contract
def test_shared_decision_response_round_trips_exactly() -> None:
    shared_response = _load_json(RESPONSE_EXAMPLE)

    adapted = DecisionEvaluateResponse.model_validate(shared_response)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_response
    _validate("decisionEvaluateResponse", serialized)


@pytest.mark.contract
def test_request_cannot_select_tenant_authority() -> None:
    payload = _load_json(REQUEST_EXAMPLE)
    payload["tenant_id"] = "tn_01k4m7x9q2v6c8r3d5f1h0j4"

    with pytest.raises(ValidationError):
        DecisionEvaluateRequest.model_validate(payload)


@pytest.mark.contract
def test_rule_set_must_be_historically_pinned() -> None:
    payload = _load_json(REQUEST_EXAMPLE)
    rule_set = payload["rule_set_reference"]
    assert isinstance(rule_set, dict)
    rule_set["reference_mode"] = "CURRENT"

    with pytest.raises(ValidationError):
        DecisionEvaluateRequest.model_validate(payload)


@pytest.mark.contract
def test_technical_failure_cannot_become_regulatory_outcome() -> None:
    payload = _load_json(RESPONSE_EXAMPLE)
    payload["outcome"] = "EVALUATOR_NOT_READY"

    with pytest.raises(ValidationError):
        DecisionEvaluateResponse.model_validate(payload)


@pytest.mark.contract
def test_provider_runtime_fields_are_not_canonical_request_fields() -> None:
    for field, value in (
        ("opa_url", "http://opa:8181"),
        ("rego_package", "baobab.regulations"),
        ("bundle_revision", "rev-123"),
        ("compiler_version", "1.2.3"),
    ):
        payload = _load_json(REQUEST_EXAMPLE)
        payload[field] = value
        with pytest.raises(ValidationError):
            DecisionEvaluateRequest.model_validate(payload)


@pytest.mark.contract
def test_idempotency_and_replay_identity_are_not_collapsed() -> None:
    payload = _load_json(REQUEST_EXAMPLE)
    adapted = DecisionEvaluateRequest.model_validate(payload)

    assert adapted.replay_key == "replay-ug-za-coffee-0001"
    assert "idempotency_key" not in adapted.model_fields

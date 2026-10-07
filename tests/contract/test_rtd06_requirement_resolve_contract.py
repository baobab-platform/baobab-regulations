"""Contract proof for R-CAP-01 against the pinned Shared RTD-06 schemas."""

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, RefResolver

from baobab_regulations.contracts.rtd06 import (
    RegulatoryDocumentRequirementProjection,
    RequirementResolveRequest,
    RequirementResolveResponse,
)

SHARED_ROOT = Path(".shared")
CONTRACTS_ROOT = SHARED_ROOT / "contracts"
RTD06_SCHEMA_PATH = CONTRACTS_ROOT / "regulatory-document-exchange/v1/domain.schema.json"
REQUEST_EXAMPLE_PATH = (
    CONTRACTS_ROOT
    / "regulatory-document-exchange/v1/examples/requirement-resolve-request.json"
)
REQUIREMENT_SET_EXAMPLE_PATH = (
    CONTRACTS_ROOT / "regulatory-document-exchange/v1/examples/requirement-set.json"
)

if not RTD06_SCHEMA_PATH.exists():
    pytest.skip(
        "pinned Shared checkout is required for RTD-06 contract tests",
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


ROOT_SCHEMA = _load_json(RTD06_SCHEMA_PATH)
STORE = _schema_store()
RESOLVER = RefResolver.from_schema(ROOT_SCHEMA, store=STORE)


def _validate(definition: str, payload: dict[str, Any]) -> None:
    wrapper = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": f"{ROOT_SCHEMA['$id']}#/$defs/{definition}",
    }
    validator = Draft202012Validator(
        wrapper,
        resolver=RESOLVER,
        format_checker=FormatChecker(),
    )
    validator.validate(payload)


@pytest.mark.contract
def test_shared_requirement_resolve_request_round_trips_through_adapter() -> None:
    shared_request = _load_json(REQUEST_EXAMPLE_PATH)

    adapted = RequirementResolveRequest.model_validate(shared_request)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_request
    _validate("requirementResolveRequest", serialized)


@pytest.mark.contract
def test_shared_requirement_projection_round_trips_through_adapter() -> None:
    requirement_set = _load_json(REQUIREMENT_SET_EXAMPLE_PATH)
    shared_projection = requirement_set["requirements"][0]
    assert isinstance(shared_projection, dict)

    adapted = RegulatoryDocumentRequirementProjection.model_validate(shared_projection)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_projection
    _validate("regulatoryDocumentRequirementProjection", serialized)


@pytest.mark.contract
def test_requirement_resolve_response_validates_against_shared_schema() -> None:
    requirement_set = _load_json(REQUIREMENT_SET_EXAMPLE_PATH)
    projection = RegulatoryDocumentRequirementProjection.model_validate(
        requirement_set["requirements"][0]
    )
    response = RequirementResolveResponse(requirement=projection)
    serialized = response.model_dump(mode="json")

    assert set(serialized) == {"requirement"}
    _validate("requirementResolveResponse", serialized)

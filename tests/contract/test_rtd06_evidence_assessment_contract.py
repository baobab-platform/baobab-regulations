"""Exact Shared RTD-06 contract proof for R-CAP-02."""

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, RefResolver

from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    DocumentEvidenceFactBundle,
)

SHARED_ROOT = Path(".shared")
CONTRACTS_ROOT = SHARED_ROOT / "contracts"
RTD06_SCHEMA_PATH = CONTRACTS_ROOT / "regulatory-document-exchange/v1/domain.schema.json"
REQUEST_EXAMPLE_PATH = (
    CONTRACTS_ROOT / "regulatory-document-exchange/v1/examples/assessment-request.json"
)
RESULT_EXAMPLE_PATH = (
    CONTRACTS_ROOT / "regulatory-document-exchange/v1/examples/assessment-result.json"
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
    Draft202012Validator(
        wrapper,
        resolver=RESOLVER,
        format_checker=FormatChecker(),
    ).validate(payload)


@pytest.mark.contract
def test_shared_assessment_request_round_trips_through_adapter() -> None:
    shared_request = _load_json(REQUEST_EXAMPLE_PATH)

    adapted = DocumentEvidenceAssessmentRequest.model_validate(shared_request)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_request
    _validate("documentEvidenceAssessmentRequest", serialized)


@pytest.mark.contract
def test_shared_document_fact_bundle_round_trips_through_adapter() -> None:
    shared_request = _load_json(REQUEST_EXAMPLE_PATH)
    shared_evidence = shared_request["evidence"][0]
    assert isinstance(shared_evidence, dict)

    adapted = DocumentEvidenceFactBundle.model_validate(shared_evidence)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_evidence
    _validate("documentEvidenceFactBundle", serialized)


@pytest.mark.contract
def test_shared_assessment_result_round_trips_through_adapter() -> None:
    shared_result = _load_json(RESULT_EXAMPLE_PATH)

    adapted = DocumentEvidenceAssessmentResult.model_validate(shared_result)
    serialized = adapted.model_dump(mode="json")

    assert serialized == shared_result
    _validate("documentEvidenceAssessmentResult", serialized)


@pytest.mark.contract
def test_canonical_request_forbids_regulations_time_selection() -> None:
    payload = _load_json(REQUEST_EXAMPLE_PATH)
    payload["legal_time"] = "2026-10-05T12:00:00Z"

    validator = Draft202012Validator(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": f"{ROOT_SCHEMA['$id']}#/$defs/documentEvidenceAssessmentRequest",
        },
        resolver=RESOLVER,
        format_checker=FormatChecker(),
    )

    errors = list(validator.iter_errors(payload))
    assert errors

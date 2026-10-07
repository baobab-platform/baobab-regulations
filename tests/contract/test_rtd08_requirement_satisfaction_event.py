"""R-CAP-06 exact Shared RTD-08 requirement-satisfaction event contract proof."""

import json
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
from jsonschema import Draft202012Validator, FormatChecker, RefResolver
from pydantic import ValidationError

from baobab_regulations.contracts.events import (
    EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED,
    REGULATIONS_EVENT_SOURCE,
    REQUIREMENT_SATISFACTION_DATASCHEMA,
    RequirementSatisfactionEvaluatedEvent,
    build_requirement_satisfaction_evaluated_event,
)
from baobab_regulations.contracts.rtd06 import DocumentEvidenceAssessmentResult

SHARED_ROOT = Path(".shared")
CONTRACTS_ROOT = SHARED_ROOT / "contracts"
ENVELOPE_SCHEMA_PATH = CONTRACTS_ROOT / "events/v1/envelope.schema.json"
EVENTS_SCHEMA_PATH = (
    CONTRACTS_ROOT / "regulatory-document-exchange/v1/events.schema.json"
)
EXAMPLE_PATH = (
    CONTRACTS_ROOT
    / "regulatory-document-assessment/v1/examples/requirement-satisfaction-evaluated.json"
)

if not ENVELOPE_SCHEMA_PATH.exists():
    pytest.skip(
        "pinned Shared checkout is required for RTD-08 contract tests",
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


STORE = _schema_store()
ENVELOPE_SCHEMA = _load_json(ENVELOPE_SCHEMA_PATH)
EVENTS_SCHEMA = _load_json(EVENTS_SCHEMA_PATH)


def _validator(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(
        schema,
        resolver=RefResolver.from_schema(schema, store=STORE),
        format_checker=FormatChecker(),
    )


@pytest.mark.contract
def test_requirement_satisfaction_event_validates_against_exact_shared_contracts() -> None:
    example = _load_json(EXAMPLE_PATH)
    data = example["data"]
    assert isinstance(data, dict)
    shared_result = data["result"]
    assert isinstance(shared_result, dict)

    result = DocumentEvidenceAssessmentResult.model_validate(shared_result)
    event = build_requirement_satisfaction_evaluated_event(
        tenant_id=str(data["tenant_id"]),
        idempotency_key="r-cap-06-assessment-0001",
        result=result,
        correlation_id=UUID(str(example["correlationid"])),
        traceparent="00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    )
    wire = event.model_dump(mode="json", exclude_none=True)

    _validator(ENVELOPE_SCHEMA).validate(wire)
    payload_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": (
            f"{EVENTS_SCHEMA['$id']}"
            "#/$defs/requirementSatisfactionEvaluatedEventData"
        ),
    }
    _validator(payload_schema).validate(wire["data"])

    assert wire["type"] == EVENT_TYPE_REQUIREMENT_SATISFACTION_EVALUATED
    assert wire["source"] == REGULATIONS_EVENT_SOURCE
    assert wire["dataschema"] == REQUIREMENT_SATISFACTION_DATASCHEMA
    assert wire["subject"] == (
        f"regulatory-evidence-assessment:{result.assessment_reference.object_id}"
    )
    assert wire["time"] == result.model_dump(mode="json")["evaluated_at"]
    assert wire["tenantid"] == wire["data"]["tenant_id"]
    assert wire["idempotencykey"] == "r-cap-06-assessment-0001"


@pytest.mark.contract
def test_event_occurrence_id_is_stable_across_delivery_metadata_changes() -> None:
    example = _load_json(EXAMPLE_PATH)
    data = example["data"]
    assert isinstance(data, dict)
    result_data = data["result"]
    assert isinstance(result_data, dict)
    result = DocumentEvidenceAssessmentResult.model_validate(result_data)
    tenant_id = str(data["tenant_id"])

    first = build_requirement_satisfaction_evaluated_event(
        tenant_id=tenant_id,
        idempotency_key="r-cap-06-assessment-0001",
        result=result,
        correlation_id=UUID("7d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f11"),
    )
    second = build_requirement_satisfaction_evaluated_event(
        tenant_id=tenant_id,
        idempotency_key="r-cap-06-assessment-0001",
        result=result,
        correlation_id=UUID("8d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f12"),
    )

    assert first.id == second.id
    assert first.correlationid != second.correlationid


@pytest.mark.contract
def test_event_rejects_nested_tenant_mismatch() -> None:
    example = _load_json(EXAMPLE_PATH)
    payload = example.copy()
    data = dict(payload["data"])
    data["tenant_id"] = "tn_01k4m7x9q2v6c8r3d5f1h0j5"
    payload["data"] = data

    with pytest.raises(ValidationError):
        RequirementSatisfactionEvaluatedEvent.model_validate(payload)

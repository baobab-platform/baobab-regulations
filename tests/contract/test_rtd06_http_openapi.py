"""R-CAP-04 generated OpenAPI conformance for the exact RTD-06 HTTP surface."""

from baobab_regulations.api.app import create_app


def _operation(path: str) -> dict[str, object]:
    schema = create_app().openapi()
    paths = schema["paths"]
    assert isinstance(paths, dict)
    route = paths[path]
    assert isinstance(route, dict)
    operation = route["post"]
    assert isinstance(operation, dict)
    return operation


def test_generated_openapi_declares_workload_oidc_scheme() -> None:
    schema = create_app().openapi()
    components = schema["components"]
    assert isinstance(components, dict)
    schemes = components["securitySchemes"]
    assert isinstance(schemes, dict)

    workload = schemes["workloadOidc"]
    assert workload == {
        "type": "openIdConnect",
        "openIdConnectUrl": (
            "https://identity.baobab-platform.com/.well-known/openid-configuration"
        ),
        "description": (
            "Short-lived workload/delegated identity. Runtime authorisation binds "
            "the authenticated caller to the redeemed Control Plane context tenant."
        ),
    }


def test_requirement_resolve_openapi_matches_rtd06_operation() -> None:
    operation = _operation("/documentary-requirements/resolve")

    assert operation["operationId"] == "resolveDocumentaryRequirement"
    assert operation["security"] == [{"workloadOidc": []}]
    responses = operation["responses"]
    assert isinstance(responses, dict)
    assert "422" not in responses
    for status in ("400", "401", "403", "404", "409", "503"):
        response = responses[status]
        assert isinstance(response, dict)
        content = response["content"]
        assert isinstance(content, dict)
        assert "application/problem+json" in content

    parameters = operation["parameters"]
    assert isinstance(parameters, list)
    names = {
        (parameter["name"], parameter["in"])
        for parameter in parameters
        if isinstance(parameter, dict)
    }
    assert ("X-Correlation-ID", "header") in names
    assert ("traceparent", "header") in names
    traceparent = next(
        parameter
        for parameter in parameters
        if isinstance(parameter, dict) and parameter.get("name") == "traceparent"
    )
    trace_schema = traceparent["schema"]
    assert isinstance(trace_schema, dict)
    assert trace_schema["pattern"] == (
        "^00-(?!00000000000000000000000000000000)[0-9a-f]{32}-"
        "(?!0000000000000000)[0-9a-f]{16}-[0-9a-f]{2}$"
    )
    assert ("Authorization", "header") not in names


def test_evidence_assessment_openapi_matches_rtd06_operation() -> None:
    operation = _operation("/documentary-evidence/assessments")

    assert operation["operationId"] == "assessDocumentaryEvidence"
    assert operation["security"] == [{"workloadOidc": []}]
    responses = operation["responses"]
    assert isinstance(responses, dict)
    assert "200" in responses
    assert "201" in responses
    assert "422" not in responses

    parameters = operation["parameters"]
    assert isinstance(parameters, list)
    idempotency = next(
        parameter
        for parameter in parameters
        if isinstance(parameter, dict) and parameter.get("name") == "Idempotency-Key"
    )
    assert idempotency["in"] == "header"
    assert idempotency["required"] is True
    schema = idempotency["schema"]
    assert isinstance(schema, dict)
    assert schema["minLength"] == 16
    assert schema["maxLength"] == 128
    assert schema["pattern"] == "^[A-Za-z0-9][A-Za-z0-9._:-]*$"

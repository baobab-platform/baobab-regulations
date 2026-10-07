"""FastAPI application factory."""

import re
from collections.abc import Awaitable, Callable
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response

from baobab_regulations import __version__
from baobab_regulations.api.problems import ApiProblem, problem_response
from baobab_regulations.api.routes import router as capability_router
from baobab_regulations.api.runtime import CapabilityApiRuntime
from baobab_regulations.configuration.settings import get_settings

_CORRELATION_HEADER = "X-Correlation-ID"
_TRACEPARENT_PATTERN = (
    r"^00-(?!00000000000000000000000000000000)[0-9a-f]{32}-"
    r"(?!0000000000000000)[0-9a-f]{16}-[0-9a-f]{2}$"
)
_TRACEPARENT_RE = re.compile(_TRACEPARENT_PATTERN)
_CANONICAL_PATHS = {
    "/documentary-requirements/resolve",
    "/documentary-evidence/assessments",
}


class RegulationsFastAPI(FastAPI):
    """FastAPI app whose generated schema is normalized to RTD-06."""

    def openapi(self) -> dict[str, object]:
        return _custom_openapi(self)


def _validation_errors(exc: RequestValidationError) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for item in exc.errors()[:50]:
        location = "/" + "/".join(str(part) for part in item.get("loc", ()))
        errors.append(
            {
                "code": "VALIDATION_ERROR",
                "field": location,
                "message": str(item.get("msg", "invalid request value"))[:500],
            }
        )
    return errors


def _custom_openapi(app: FastAPI) -> dict[str, object]:
    if app.openapi_schema is not None:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    components = schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["workloadOidc"] = {
        "type": "openIdConnect",
        "openIdConnectUrl": "https://identity.baobab-platform.com/.well-known/openid-configuration",
        "description": (
            "Short-lived workload/delegated identity. Runtime authorisation binds "
            "the authenticated caller to the redeemed Control Plane context tenant."
        ),
    }

    paths = schema.get("paths", {})
    if isinstance(paths, dict):
        for route_path in _CANONICAL_PATHS:
            route = paths.get(route_path)
            if not isinstance(route, dict):
                continue
            operation = route.get("post")
            if not isinstance(operation, dict):
                continue
            responses = operation.get("responses")
            if isinstance(responses, dict):
                responses.pop("422", None)
                for status in ("400", "401", "403", "404", "409", "503"):
                    response = responses.get(status)
                    if not isinstance(response, dict):
                        continue
                    content = response.get("content")
                    if isinstance(content, dict) and "application/json" in content:
                        content["application/problem+json"] = content.pop("application/json")
            parameters = operation.get("parameters")
            if isinstance(parameters, list):
                for parameter in parameters:
                    if not isinstance(parameter, dict) or parameter.get("in") != "header":
                        continue
                    name = parameter.get("name")
                    if name == "Idempotency-Key":
                        parameter["required"] = True
                        parameter["schema"] = {
                            "type": "string",
                            "pattern": r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
                            "minLength": 16,
                            "maxLength": 128,
                        }
                    elif name == "X-Correlation-ID":
                        parameter["required"] = False
                        parameter["schema"] = {
                            "type": "string",
                            "format": "uuid",
                        }
                    elif name == "traceparent":
                        parameter["required"] = False
                        parameter["schema"] = {
                            "type": "string",
                            "pattern": _TRACEPARENT_PATTERN,
                        }

    app.openapi_schema = schema
    return schema


def create_app(runtime: CapabilityApiRuntime | None = None) -> FastAPI:
    settings = get_settings()
    app = RegulationsFastAPI(
        title="Baobab Regulations",
        version=__version__,
        description=(
            "Headless regulatory context and deterministic decision engine. "
            "Policy Decision Point only — operational enforcement stays with domain PEPs."
        ),
    )
    app.state.capability_runtime = runtime

    @app.middleware("http")
    async def canonical_request_metadata(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        raw_correlation = request.headers.get(_CORRELATION_HEADER)
        if raw_correlation is None:
            correlation_id = uuid4()
        else:
            try:
                correlation_id = UUID(raw_correlation)
            except ValueError:
                request.state.correlation_id = uuid4()
                return problem_response(
                    request,
                    status=400,
                    code="CORRELATION_ID_INVALID",
                    title="Invalid request",
                    detail="X-Correlation-ID must be a UUID",
                )
        request.state.correlation_id = correlation_id

        traceparent = request.headers.get("traceparent")
        if traceparent is not None:
            if _TRACEPARENT_RE.fullmatch(traceparent) is None:
                return problem_response(
                    request,
                    status=400,
                    code="TRACEPARENT_INVALID",
                    title="Invalid request",
                    detail="traceparent does not satisfy the RTD-06 contract",
                )
            request.state.trace_id = traceparent.split("-")[1]

        response = await call_next(request)
        response.headers.setdefault(_CORRELATION_HEADER, str(correlation_id))
        return response

    @app.exception_handler(ApiProblem)
    async def handle_api_problem(request: Request, exc: ApiProblem) -> Response:
        return problem_response(
            request,
            status=exc.status,
            code=exc.code,
            title=exc.title,
            detail=exc.detail,
            retryable=exc.retryable,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(
        request: Request,
        exc: RequestValidationError,
    ) -> Response:
        return problem_response(
            request,
            status=400,
            code="VALIDATION_FAILED",
            title="Invalid request",
            detail="request does not satisfy the canonical RTD-06 contract",
            errors=_validation_errors(exc),
        )

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name, "version": __version__}

    @app.get("/readyz")
    async def readyz() -> dict[str, str]:
        # Capability routes fail closed independently when runtime dependencies are absent.
        return {"status": "ready", "service": settings.app_name}

    app.include_router(capability_router)

    return app

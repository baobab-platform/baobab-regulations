"""FastAPI dependencies for canonical and legacy request boundaries."""

import re
from dataclasses import dataclass, replace
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Header, Request

from baobab_regulations.api.problems import ApiProblem
from baobab_regulations.api.runtime import CapabilityApiRuntime
from baobab_regulations.application.ports.authentication import (
    WorkloadAuthenticationError,
    WorkloadAuthenticationUnavailableError,
)
from baobab_regulations.application.ports.context_authority import AuthenticatedCaller
from baobab_regulations.application.ports.events import EventPublicationMetadata
from baobab_regulations.tenancy.request import (
    HEADER_CONTEXT,
    HEADER_CORRELATION,
    HEADER_TENANT,
    RequestScope,
    platform_from_headers,
)

_IDEMPOTENCY_KEY_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:-]*$"
_IDEMPOTENCY_KEY = re.compile(_IDEMPOTENCY_KEY_PATTERN)
_CORRELATION_ID_PATTERN = (
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)
_TRACEPARENT_HEADER_PATTERN = (
    r"^00-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$"
)


@dataclass(frozen=True, slots=True)
class AuthenticatedCapabilityRequest:
    """Verified workload caller plus the capability runtime used by the route."""

    caller: AuthenticatedCaller
    runtime: CapabilityApiRuntime


def _runtime(request: Request) -> CapabilityApiRuntime:
    runtime = getattr(request.app.state, "capability_runtime", None)
    if not isinstance(runtime, CapabilityApiRuntime):
        raise ApiProblem(
            status=503,
            code="CAPABILITY_RUNTIME_UNAVAILABLE",
            title="Capability runtime unavailable",
            detail="canonical Regulations capability runtime is not configured",
            retryable=True,
        )
    return runtime


def _bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise ApiProblem(
            status=401,
            code="AUTH_TOKEN_REQUIRED",
            title="Authentication required",
            detail="a workload bearer token is required",
        )
    scheme, separator, token = authorization.partition(" ")
    if separator != " " or scheme.lower() != "bearer" or not token.strip():
        raise ApiProblem(
            status=401,
            code="AUTH_TOKEN_INVALID",
            title="Authentication failed",
            detail="Authorization must contain a valid Bearer token",
        )
    token = token.strip()
    if not 16 <= len(token) <= 8192:
        raise ApiProblem(
            status=401,
            code="AUTH_TOKEN_INVALID",
            title="Authentication failed",
            detail="the workload bearer token is invalid",
        )
    return token


async def require_authenticated_capability_request(
    request: Request,
) -> AuthenticatedCapabilityRequest:
    """Authenticate a workload for the baobab-regulations resource server."""
    token = _bearer_token(request.headers.get("Authorization"))
    runtime = _runtime(request)
    try:
        caller = await runtime.authenticator.authenticate(token)
    except WorkloadAuthenticationError as exc:
        raise ApiProblem(
            status=401,
            code="AUTH_TOKEN_INVALID",
            title="Authentication failed",
            detail="the workload bearer token could not be verified",
        ) from exc
    except WorkloadAuthenticationUnavailableError as exc:
        raise ApiProblem(
            status=503,
            code="AUTHENTICATION_UNAVAILABLE",
            title="Authentication unavailable",
            detail="the workload authentication authority is unavailable",
            retryable=True,
        ) from exc

    if caller.access_token != token:
        caller = replace(caller, access_token=token)
    return AuthenticatedCapabilityRequest(caller=caller, runtime=runtime)


async def require_canonical_metadata_headers(
    x_correlation_id: Annotated[
        str | None,
        Header(alias="X-Correlation-ID", pattern=_CORRELATION_ID_PATTERN),
    ] = None,
    traceparent: Annotated[
        str | None,
        Header(alias="traceparent", pattern=_TRACEPARENT_HEADER_PATTERN),
    ] = None,
) -> None:
    """Expose exact optional RTD-06 metadata headers in generated OpenAPI."""
    del x_correlation_id, traceparent


async def require_event_publication_metadata(
    request: Request,
) -> EventPublicationMetadata:
    """Carry canonical request correlation/trace metadata into RTD-08 events."""
    correlation = getattr(request.state, "correlation_id", None)
    if not isinstance(correlation, UUID):
        correlation = uuid4()
    traceparent = request.headers.get("traceparent")
    return EventPublicationMetadata(
        correlation_id=correlation,
        traceparent=traceparent,
    )


async def require_idempotency_key(
    idempotency_key: Annotated[
        str | None,
        Header(
            alias="Idempotency-Key",
            min_length=16,
            max_length=128,
            pattern=_IDEMPOTENCY_KEY_PATTERN,
        ),
    ] = None,
) -> str:
    """Enforce the exact RTD-06 Idempotency-Key grammar without FastAPI 422s."""
    if idempotency_key is None:
        raise ApiProblem(
            status=400,
            code="IDEMPOTENCY_KEY_REQUIRED",
            title="Invalid request",
            detail="Idempotency-Key is required",
        )
    value = idempotency_key.strip()
    if not 16 <= len(value) <= 128 or _IDEMPOTENCY_KEY.fullmatch(value) is None:
        raise ApiProblem(
            status=400,
            code="IDEMPOTENCY_KEY_INVALID",
            title="Invalid request",
            detail="Idempotency-Key does not satisfy the RTD-06 contract",
        )
    return value


async def require_request_scope(
    x_baobab_tenant_id: Annotated[str | None, Header(alias=HEADER_TENANT)] = None,
    x_baobab_context_id: Annotated[str | None, Header(alias=HEADER_CONTEXT)] = None,
    x_baobab_correlation_id: Annotated[str | None, Header(alias=HEADER_CORRELATION)] = None,
) -> RequestScope:
    """Legacy scaffold boundary; canonical RTD-06 routes do not use tenant headers."""
    return platform_from_headers(
        tenant_id=x_baobab_tenant_id,
        context_id=x_baobab_context_id,
        correlation_id=x_baobab_correlation_id,
    )


__all__ = [
    "AuthenticatedCapabilityRequest",
    "require_authenticated_capability_request",
    "require_canonical_metadata_headers",
    "require_event_publication_metadata",
    "require_idempotency_key",
    "require_request_scope",
]

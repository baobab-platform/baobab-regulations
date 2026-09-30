"""FastAPI dependencies for request-scoped platform context."""

from typing import Annotated

from fastapi import Header

from baobab_regulations.tenancy.request import (
    HEADER_CONTEXT,
    HEADER_CORRELATION,
    HEADER_TENANT,
    RequestScope,
    platform_from_headers,
)


async def require_request_scope(
    x_baobab_tenant_id: Annotated[str | None, Header(alias=HEADER_TENANT)] = None,
    x_baobab_context_id: Annotated[str | None, Header(alias=HEADER_CONTEXT)] = None,
    x_baobab_correlation_id: Annotated[str | None, Header(alias=HEADER_CORRELATION)] = None,
) -> RequestScope:
    """Fail-closed tenant/context gate for evaluation routes (not health)."""
    return platform_from_headers(
        tenant_id=x_baobab_tenant_id,
        context_id=x_baobab_context_id,
        correlation_id=x_baobab_correlation_id,
    )

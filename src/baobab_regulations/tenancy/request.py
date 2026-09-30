"""HTTP request-scoped platform context extraction (ADR-REG-0026, ADR-REG-0028)."""

from dataclasses import dataclass

from baobab_regulations.domain.context.models import PlatformContextRef
from baobab_regulations.tenancy.context import (
    ContextRedemptionNotImplementedError,
    TenantContextError,
    resolve_platform_context,
)

HEADER_TENANT = "x-baobab-tenant-id"
HEADER_CONTEXT = "x-baobab-context-id"
HEADER_CORRELATION = "x-baobab-correlation-id"


@dataclass(frozen=True, slots=True)
class RequestScope:
    """Resolved request boundary for evaluation routes."""

    platform: PlatformContextRef
    correlation_id: str | None = None


def platform_from_headers(
    *,
    tenant_id: str | None = None,
    context_id: str | None = None,
    correlation_id: str | None = None,
) -> RequestScope:
    """Build a request scope from HTTP headers (evaluation routes)."""
    ref = PlatformContextRef(
        tenant_id=tenant_id.strip() if tenant_id else None,
        context_id=context_id.strip() if context_id else None,
    )
    resolved = resolve_platform_context(ref)
    return RequestScope(
        platform=resolved,
        correlation_id=correlation_id.strip() if correlation_id else None,
    )


def merge_platform(
    body: PlatformContextRef,
    *,
    header_tenant_id: str | None = None,
    header_context_id: str | None = None,
) -> PlatformContextRef:
    """Merge body platform with optional header overrides (headers win if set)."""
    tenant = (header_tenant_id or body.tenant_id or "").strip() or None
    context = (header_context_id or body.context_id or "").strip() or None
    merged = body.model_copy(
        update={
            "tenant_id": tenant,
            "context_id": context,
        },
    )
    return resolve_platform_context(merged)


__all__ = [
    "HEADER_CONTEXT",
    "HEADER_CORRELATION",
    "HEADER_TENANT",
    "ContextRedemptionNotImplementedError",
    "RequestScope",
    "TenantContextError",
    "merge_platform",
    "platform_from_headers",
]

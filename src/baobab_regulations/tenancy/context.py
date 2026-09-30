"""Structural tenant-context gate (ADR-REG-0028)."""

from baobab_regulations.domain.context.models import PlatformContextRef


class TenantContextError(ValueError):
    """Raised when tenant context is missing or empty — fail closed."""


class ContextRedemptionNotImplementedError(RuntimeError):
    """Raised when only context_id is supplied and CP redemption is not wired."""

    code = "CONTEXT_REDEMPTION_NOT_IMPLEMENTED"


def require_tenant_context(tenant_id: str | None) -> str:
    if not tenant_id or not str(tenant_id).strip():
        raise TenantContextError("tenant_id is required; unrestricted evaluation is forbidden")
    return str(tenant_id).strip()


def resolve_platform_context(platform: PlatformContextRef) -> PlatformContextRef:
    """Ensure a usable platform context for evaluation.

    - Inline ``tenant_id``: accepted (scaffold / offline).
    - Only ``context_id``: fail with a structured not-implemented error until
      Control Plane redemption is wired (REG-1 contract; live client later).
    """
    if platform.tenant_id and str(platform.tenant_id).strip():
        return platform.model_copy(
            update={"tenant_id": str(platform.tenant_id).strip()},
        )
    if platform.context_id and str(platform.context_id).strip():
        raise ContextRedemptionNotImplementedError(
            "context_id redemption via Control Plane is not implemented in this scaffold; "
            "supply platform.tenant_id for offline evaluation",
        )
    raise TenantContextError("tenant_id is required; unrestricted evaluation is forbidden")

"""Structural tenant-context gate (ADR-REG-0028)."""


class TenantContextError(ValueError):
    """Raised when tenant context is missing or empty — fail closed."""


def require_tenant_context(tenant_id: str | None) -> str:
    if not tenant_id or not str(tenant_id).strip():
        raise TenantContextError("tenant_id is required; unrestricted evaluation is forbidden")
    return str(tenant_id).strip()

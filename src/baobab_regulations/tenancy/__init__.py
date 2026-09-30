"""Tenant-context enforcement — fail closed."""

from baobab_regulations.tenancy.context import require_tenant_context, TenantContextError

__all__ = ["require_tenant_context", "TenantContextError"]

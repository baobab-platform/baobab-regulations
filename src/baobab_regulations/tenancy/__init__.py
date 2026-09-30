"""Tenant-context enforcement — fail closed."""

from baobab_regulations.tenancy.context import TenantContextError, require_tenant_context

__all__ = ["TenantContextError", "require_tenant_context"]

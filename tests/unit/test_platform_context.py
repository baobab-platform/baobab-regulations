"""REG-1 platform context redemption and fail-closed tenancy."""

import pytest
from pydantic import ValidationError

from baobab_regulations.domain.context.models import PlatformContextRef
from baobab_regulations.tenancy.context import (
    ContextRedemptionNotImplementedError,
    TenantContextError,
    require_tenant_context,
    resolve_platform_context,
)
from baobab_regulations.tenancy.request import merge_platform, platform_from_headers


def test_require_tenant_rejects_empty() -> None:
    with pytest.raises(TenantContextError):
        require_tenant_context("")
    with pytest.raises(TenantContextError):
        require_tenant_context(None)


def test_platform_ref_requires_tenant_or_context_id() -> None:
    with pytest.raises(ValidationError):
        PlatformContextRef()


def test_inline_tenant_resolves() -> None:
    ref = PlatformContextRef(tenant_id="tenant-zuribeans")
    resolved = resolve_platform_context(ref)
    assert resolved.tenant_id == "tenant-zuribeans"


def test_context_id_only_not_implemented() -> None:
    ref = PlatformContextRef(context_id="ctx-abc")
    with pytest.raises(ContextRedemptionNotImplementedError) as exc:
        resolve_platform_context(ref)
    assert exc.value.code == "CONTEXT_REDEMPTION_NOT_IMPLEMENTED"


def test_headers_build_request_scope() -> None:
    scope = platform_from_headers(
        tenant_id="tenant-a",
        correlation_id="corr-1",
    )
    assert scope.platform.tenant_id == "tenant-a"
    assert scope.correlation_id == "corr-1"


def test_merge_platform_header_wins() -> None:
    body = PlatformContextRef(tenant_id="tenant-body")
    merged = merge_platform(body, header_tenant_id="tenant-header")
    assert merged.tenant_id == "tenant-header"

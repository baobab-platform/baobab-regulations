"""Trusted Control Plane context boundary for capability adapters.

RTD-06 requires context_id to be redeemed against the authenticated caller.
The request body is therefore never trusted to choose a tenant by itself.
"""

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AuthenticatedCaller:
    """Authenticated workload/delegated subject presented to Regulations.

    The access token is retained only as short-lived subject evidence for
    Control Plane context validation. It is excluded from repr/equality so
    ordinary diagnostics do not expose a bearer credential.
    """

    subject: str
    access_token: str | None = field(default=None, repr=False, compare=False)
    client_id: str | None = None
    tenant_id: str | None = None
    scopes: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("authenticated caller subject must not be empty")
        if self.access_token is not None and not self.access_token.strip():
            raise ValueError("access_token must not be empty when supplied")


@dataclass(frozen=True, slots=True)
class TrustedPlatformContext:
    """Minimum authoritative context needed by RTD-06 capability adapters."""

    context_id: UUID
    tenant_id: str


class ContextAuthenticationError(PermissionError):
    """The caller subject token could not be independently verified."""


class ContextAccessDeniedError(PermissionError):
    """Caller may not redeem/use the requested platform context."""


class ContextNotFoundError(LookupError):
    """Context is unknown, expired, unbounded or owned by another principal."""


class ContextAuthorityUnavailableError(RuntimeError):
    """The authoritative context service could not be reached."""


class ContextAuthorityPort(Protocol):
    """Redeem a persisted Control Plane context for an authenticated caller."""

    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext: ...


__all__ = [
    "AuthenticatedCaller",
    "ContextAccessDeniedError",
    "ContextAuthenticationError",
    "ContextAuthorityPort",
    "ContextNotFoundError",
    "ContextAuthorityUnavailableError",
    "TrustedPlatformContext",
]

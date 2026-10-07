"""Trusted Control Plane context boundary for capability adapters.

RTD-06 requires context_id to be redeemed against the authenticated caller.
The request body is therefore never trusted to choose a tenant by itself.
"""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AuthenticatedCaller:
    """Authenticated workload/delegated subject presented to Regulations."""

    subject: str

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("authenticated caller subject must not be empty")


@dataclass(frozen=True, slots=True)
class TrustedPlatformContext:
    """Minimum authoritative context needed by RTD-06 capability adapters."""

    context_id: UUID
    tenant_id: str


class ContextAccessDeniedError(PermissionError):
    """Caller may not redeem/use the requested platform context."""


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
    "ContextAuthorityPort",
    "ContextAuthorityUnavailableError",
    "TrustedPlatformContext",
]

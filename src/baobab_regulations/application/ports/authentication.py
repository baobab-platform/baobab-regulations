"""Provider-neutral workload authentication boundary for HTTP resource-server routes."""

from typing import Protocol

from baobab_regulations.application.ports.context_authority import AuthenticatedCaller


class WorkloadAuthenticationError(PermissionError):
    """The presented bearer token is missing, invalid or not a workload token."""


class WorkloadAuthenticationUnavailableError(RuntimeError):
    """The configured workload token verifier/introspection authority is unavailable."""


class WorkloadAuthenticatorPort(Protocol):
    """Verify a bearer token for the baobab-regulations resource-server audience.

    Implementations MUST verify issuer, expiry, audience and actor_type=workload.
    Token format is intentionally not constrained here.
    """

    async def authenticate(self, access_token: str) -> AuthenticatedCaller: ...


__all__ = [
    "WorkloadAuthenticationError",
    "WorkloadAuthenticationUnavailableError",
    "WorkloadAuthenticatorPort",
]

"""Outbound workload credential boundary for Control Plane validation calls."""

from typing import Protocol


class ValidatorCredentialUnavailableError(RuntimeError):
    """Regulations could not obtain its own Control Plane workload credential."""


class ValidatorTokenProviderPort(Protocol):
    """Return a short-lived baobab-regulations token for baobab-control-plane."""

    async def token(self) -> str: ...


__all__ = [
    "ValidatorCredentialUnavailableError",
    "ValidatorTokenProviderPort",
]

"""R-CAP-01 application adapter for regulations.requirement.resolve."""

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthorityPort,
    ContextAuthorityUnavailableError,
)
from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityUnavailableError,
    RequirementLookupStatus,
    RequirementRepositoryPort,
)
from baobab_regulations.contracts.rtd06 import (
    PinnedRegulationsReference,
    RequirementResolveRequest,
    RequirementResolveResponse,
)


class RequirementResolutionAccessDeniedError(PermissionError):
    """Caller/context/reference authority mismatch."""

    code = "REGULATIONS_REQUIREMENT_ACCESS_DENIED"


class RequirementResolutionNotFoundError(LookupError):
    """The exact requirement identity is not known to Regulations."""

    code = "REGULATIONS_REQUIREMENT_NOT_FOUND"


class RequirementResolutionConflictError(RuntimeError):
    """The requested pin/version conflicts with governed Regulations state."""

    code = "REGULATIONS_REQUIREMENT_REFERENCE_CONFLICT"


class RequirementResolutionUnavailableError(RuntimeError):
    """An authority required to resolve the requirement is unavailable."""

    code = "REGULATIONS_REQUIREMENT_AUTHORITY_UNAVAILABLE"


class RequirementResolutionIntegrityError(RuntimeError):
    """The owner adapter returned a projection inconsistent with the requested pin."""

    code = "REGULATIONS_REQUIREMENT_INTEGRITY_FAILURE"


class RequirementResolutionService:
    """Resolve one exact already-established RTD-06 requirement.

    This is deliberately narrower than regulatory context/applicability
    resolution. It performs no legal evaluation and no Trade Docs mutation.
    """

    def __init__(
        self,
        *,
        contexts: ContextAuthorityPort,
        requirements: RequirementRepositoryPort,
    ) -> None:
        self._contexts = contexts
        self._requirements = requirements

    async def resolve(
        self,
        *,
        request: RequirementResolveRequest,
        caller: AuthenticatedCaller,
    ) -> RequirementResolveResponse:
        """Redeem context, enforce tenant authority and resolve the exact pin."""
        try:
            trusted_context = await self._contexts.redeem(
                context_id=request.context_id,
                caller=caller,
            )
        except ContextAccessDeniedError as exc:
            raise RequirementResolutionAccessDeniedError(
                "caller is not authorised for the supplied context_id"
            ) from exc
        except ContextAuthorityUnavailableError as exc:
            raise RequirementResolutionUnavailableError(
                "Control Plane context authority is unavailable"
            ) from exc

        self._enforce_reference_tenant(
            reference=request.requirement_reference,
            trusted_tenant_id=trusted_context.tenant_id,
        )

        try:
            lookup = await self._requirements.resolve_exact(request.requirement_reference)
        except RequirementAuthorityUnavailableError as exc:
            raise RequirementResolutionUnavailableError(
                "Regulations requirement authority is unavailable"
            ) from exc

        if lookup.status is RequirementLookupStatus.NOT_FOUND:
            raise RequirementResolutionNotFoundError(
                "exact Regulations requirement was not found"
            )
        if lookup.status is RequirementLookupStatus.CONFLICT:
            raise RequirementResolutionConflictError(
                "requirement reference is stale, superseded, or conflicts with governed state"
            )

        requirement = lookup.requirement
        if requirement is None:
            raise RequirementResolutionIntegrityError(
                "requirement repository returned FOUND without a projection"
            )

        if requirement.requirement_reference != request.requirement_reference:
            raise RequirementResolutionIntegrityError(
                "resolved requirement reference does not equal the exact requested pin"
            )

        self._enforce_reference_tenant(
            reference=requirement.requirement_reference,
            trusted_tenant_id=trusted_context.tenant_id,
        )
        self._enforce_reference_tenant(
            reference=requirement.regulatory_decision_reference,
            trusted_tenant_id=trusted_context.tenant_id,
        )

        return RequirementResolveResponse(requirement=requirement)

    @staticmethod
    def _enforce_reference_tenant(
        *,
        reference: PinnedRegulationsReference,
        trusted_tenant_id: str,
    ) -> None:
        """Tenant-scoped nested references must match the redeemed CP tenant."""
        if reference.scope != "tenant":
            return
        if reference.tenant_id != trusted_tenant_id:
            raise RequirementResolutionAccessDeniedError(
                "tenant-scoped Regulations reference does not match trusted context tenant"
            )


__all__ = [
    "RequirementResolutionAccessDeniedError",
    "RequirementResolutionConflictError",
    "RequirementResolutionIntegrityError",
    "RequirementResolutionNotFoundError",
    "RequirementResolutionService",
    "RequirementResolutionUnavailableError",
]

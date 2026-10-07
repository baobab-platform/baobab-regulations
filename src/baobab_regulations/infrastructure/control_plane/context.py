"""HTTP adapter for caller-bound Control Plane PlatformContext validation."""

from uuid import UUID

import httpx
from pydantic import BaseModel, ConfigDict, ValidationError

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
    TrustedPlatformContext,
)
from baobab_regulations.application.ports.control_plane import (
    ValidatorCredentialUnavailableError,
    ValidatorTokenProviderPort,
)


class _ContextValidationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_id: UUID
    tenant_id: str
    resolved_at: str
    expires_at: str
    market_id: str | None = None
    organisation_id: str | None = None


class ControlPlaneContextAuthority:
    """Redeem context_id by asking Control Plane to validate the actual caller.

    The inbound bearer token is forwarded only as subject_token in the
    authenticated validator request. It is never included in exceptions.
    """

    def __init__(
        self,
        *,
        client: httpx.AsyncClient,
        base_url: str,
        validator_tokens: ValidatorTokenProviderPort,
    ) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._validator_tokens = validator_tokens

    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        subject_token = caller.access_token
        if subject_token is None:
            raise ContextAuthenticationError(
                "authenticated caller is missing subject-token evidence"
            )

        try:
            validator_token = await self._validator_tokens.token()
        except ValidatorCredentialUnavailableError as exc:
            raise ContextAuthorityUnavailableError(
                "Control Plane validator credential is unavailable"
            ) from exc

        try:
            response = await self._client.post(
                f"{self._base_url}/v1/platform-context/validate",
                headers={
                    "Authorization": f"Bearer {validator_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "context_id": str(context_id),
                    "subject_token": subject_token,
                },
            )
        except httpx.HTTPError as exc:
            raise ContextAuthorityUnavailableError(
                "Control Plane context validation is unavailable"
            ) from exc

        if response.status_code == 200:
            try:
                validated = _ContextValidationResponse.model_validate(response.json())
            except (ValueError, ValidationError) as exc:
                raise ContextAuthorityUnavailableError(
                    "Control Plane returned an invalid context validation response"
                ) from exc
            if validated.context_id != context_id:
                raise ContextAuthorityUnavailableError(
                    "Control Plane returned a mismatched context_id"
                )
            return TrustedPlatformContext(
                context_id=validated.context_id,
                tenant_id=validated.tenant_id,
            )

        if response.status_code == 401:
            raise ContextAuthenticationError(
                "caller subject token could not be independently verified"
            )
        if response.status_code == 403:
            raise ContextAccessDeniedError(
                "caller is not authorised for the referenced context"
            )
        if response.status_code == 404:
            raise ContextNotFoundError(
                "context is unknown, expired, unbounded, or owned by another principal"
            )
        if response.status_code >= 500:
            raise ContextAuthorityUnavailableError(
                "Control Plane context validation is unavailable"
            )

        raise ContextAccessDeniedError(
            "Control Plane rejected the context-validation request"
        )


__all__ = ["ControlPlaneContextAuthority"]

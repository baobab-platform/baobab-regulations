"""R-CAP-04 Control Plane context-validation adapter behavior."""

import json
from uuid import UUID

import httpx
import pytest

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
)
from baobab_regulations.application.ports.control_plane import (
    ValidatorCredentialUnavailableError,
)
from baobab_regulations.infrastructure.control_plane.context import (
    ControlPlaneContextAuthority,
)

CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
SUBJECT_TOKEN = "subject-workload-token-r-cap-04"
VALIDATOR_TOKEN = "regulations-validator-token-r-cap-04"


class FakeValidatorTokens:
    def __init__(self, *, unavailable: bool = False) -> None:
        self.unavailable = unavailable

    async def token(self) -> str:
        if self.unavailable:
            raise ValidatorCredentialUnavailableError("validator token unavailable")
        return VALIDATOR_TOKEN


def _caller(*, with_token: bool = True) -> AuthenticatedCaller:
    return AuthenticatedCaller(
        subject="workload:trade-docs",
        access_token=SUBJECT_TOKEN if with_token else None,
        client_id="baobab-trade-docs-workload",
    )


def _transport(status: int) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/platform-context/validate"
        assert request.headers["Authorization"] == f"Bearer {VALIDATOR_TOKEN}"
        payload = json.loads(request.content)
        assert payload == {
            "context_id": str(CONTEXT_ID),
            "subject_token": SUBJECT_TOKEN,
        }
        if status == 200:
            return httpx.Response(
                200,
                json={
                    "context_id": str(CONTEXT_ID),
                    "tenant_id": TENANT_ID,
                    "resolved_at": "2026-10-06T08:00:00Z",
                    "expires_at": "2026-10-06T08:15:00Z",
                },
            )
        return httpx.Response(status, json={"code": "ignored-by-adapter"})

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_control_plane_validates_actual_subject_token() -> None:
    async with httpx.AsyncClient(transport=_transport(200)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        trusted = await authority.redeem(context_id=CONTEXT_ID, caller=_caller())

    assert trusted.context_id == CONTEXT_ID
    assert trusted.tenant_id == TENANT_ID


@pytest.mark.asyncio
async def test_context_not_found_preserves_indistinguishable_404_semantics() -> None:
    async with httpx.AsyncClient(transport=_transport(404)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        with pytest.raises(ContextNotFoundError):
            await authority.redeem(context_id=CONTEXT_ID, caller=_caller())


@pytest.mark.asyncio
async def test_subject_verification_failure_is_authentication_error() -> None:
    async with httpx.AsyncClient(transport=_transport(401)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        with pytest.raises(ContextAuthenticationError):
            await authority.redeem(context_id=CONTEXT_ID, caller=_caller())


@pytest.mark.asyncio
async def test_tenant_or_validator_denial_is_access_denied() -> None:
    async with httpx.AsyncClient(transport=_transport(403)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        with pytest.raises(ContextAccessDeniedError):
            await authority.redeem(context_id=CONTEXT_ID, caller=_caller())


@pytest.mark.asyncio
async def test_control_plane_unavailability_is_distinct_from_absence() -> None:
    async with httpx.AsyncClient(transport=_transport(503)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        with pytest.raises(ContextAuthorityUnavailableError):
            await authority.redeem(context_id=CONTEXT_ID, caller=_caller())


@pytest.mark.asyncio
async def test_validator_credential_unavailability_fails_closed() -> None:
    async with httpx.AsyncClient(transport=_transport(200)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(unavailable=True),
        )

        with pytest.raises(ContextAuthorityUnavailableError):
            await authority.redeem(context_id=CONTEXT_ID, caller=_caller())


@pytest.mark.asyncio
async def test_missing_subject_token_evidence_fails_before_network_call() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(500)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        authority = ControlPlaneContextAuthority(
            client=client,
            base_url="https://control.baobab-platform.com",
            validator_tokens=FakeValidatorTokens(),
        )

        with pytest.raises(ContextAuthenticationError):
            await authority.redeem(
                context_id=CONTEXT_ID,
                caller=_caller(with_token=False),
            )

    assert calls == 0


def test_authenticated_caller_repr_never_contains_bearer_token() -> None:
    caller = _caller()

    assert SUBJECT_TOKEN not in repr(caller)

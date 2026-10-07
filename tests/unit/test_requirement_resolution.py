"""R-CAP-01 exact pinned requirement resolution behavior."""

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthorityUnavailableError,
    TrustedPlatformContext,
)
from baobab_regulations.application.services.requirement_resolution import (
    RequirementResolutionAccessDeniedError,
    RequirementResolutionConflictError,
    RequirementResolutionIntegrityError,
    RequirementResolutionNotFoundError,
    RequirementResolutionService,
    RequirementResolutionUnavailableError,
)
from baobab_regulations.contracts.rtd06 import (
    ObjectVersion,
    RegulatoryDecisionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
    RequirementResolveRequest,
)
from baobab_regulations.infrastructure.persistence.requirements_memory import (
    InMemoryRequirementRepository,
)

CONTEXT_ID = UUID("6d7e8f9a-0b1c-4d1e-8f2a-4b5c6d7e8f10")
TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
OTHER_TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j5"


class FakeContextAuthority:
    def __init__(
        self,
        *,
        tenant_id: str = TENANT_ID,
        allowed_subject: str = "workload:trade-docs",
        available: bool = True,
    ) -> None:
        self.tenant_id = tenant_id
        self.allowed_subject = allowed_subject
        self.available = available

    async def redeem(
        self,
        *,
        context_id: UUID,
        caller: AuthenticatedCaller,
    ) -> TrustedPlatformContext:
        if not self.available:
            raise ContextAuthorityUnavailableError("context authority unavailable")
        if context_id != CONTEXT_ID or caller.subject != self.allowed_subject:
            raise ContextAccessDeniedError("context denied")
        return TrustedPlatformContext(context_id=context_id, tenant_id=self.tenant_id)


def _requirement_reference(
    *,
    tenant_id: str = TENANT_ID,
    reference_mode: str = "IDENTITY_PINNED",
    version: str | None = None,
) -> RegulatoryRequirementReference:
    payload: dict[str, object] = {
        "owner_engine_id": "baobab-regulations",
        "object_type": "DOCUMENT_REQUIREMENT",
        "object_id": "regreq_01k7rtd6phyto01",
        "reference_mode": reference_mode,
        "scope": "tenant",
        "tenant_id": tenant_id,
    }
    if version is not None:
        payload["object_version"] = ObjectVersion(kind="REVISION", value=version)
    return RegulatoryRequirementReference.model_validate(payload)


def _projection(
    *,
    requirement_reference: RegulatoryRequirementReference | None = None,
    decision_tenant_id: str = TENANT_ID,
) -> RegulatoryDocumentRequirementProjection:
    return RegulatoryDocumentRequirementProjection(
        requirement_reference=requirement_reference or _requirement_reference(),
        regulatory_decision_reference=RegulatoryDecisionReference(
            owner_engine_id="baobab-regulations",
            object_type="REGULATORY_DECISION",
            object_id="regdec_01k7rtd6decision01",
            reference_mode="IDENTITY_PINNED",
            scope="tenant",
            tenant_id=decision_tenant_id,
        ),
        requirement_kind="DOCUMENT",
        requirement_code="PHYTOSANITARY_CERTIFICATE_REQUIRED",
        purpose_code="SPS",
        acceptable_document_types=["PHYTOSANITARY_CERTIFICATE"],
        required_issuer_roles=["COMPETENT_AUTHORITY"],
        required_data_elements=[
            "CONSIGNMENT_REFERENCE",
            "ORIGIN_COUNTRY",
            "COMMODITY_DESCRIPTION",
        ],
        unsatisfied_effect_code="SPS_HOLD_REQUIRED",
        effective_from=datetime(2026, 10, 5, tzinfo=UTC),
        effective_to=None,
        determined_at=datetime(2026, 10, 5, 20, 30, tzinfo=UTC),
    )


def _service(
    projection: RegulatoryDocumentRequirementProjection | None = None,
    *,
    context_authority: FakeContextAuthority | None = None,
) -> tuple[RequirementResolutionService, InMemoryRequirementRepository]:
    repository = InMemoryRequirementRepository([projection or _projection()])
    service = RequirementResolutionService(
        contexts=context_authority or FakeContextAuthority(),
        requirements=repository,
    )
    return service, repository


def _request(
    reference: RegulatoryRequirementReference | None = None,
) -> RequirementResolveRequest:
    return RequirementResolveRequest(
        context_id=CONTEXT_ID,
        requirement_reference=reference or _requirement_reference(),
    )


@pytest.mark.asyncio
async def test_resolves_exact_pinned_requirement() -> None:
    service, _ = _service()

    response = await service.resolve(
        request=_request(),
        caller=AuthenticatedCaller(subject="workload:trade-docs"),
    )

    assert response.requirement.requirement_code == "PHYTOSANITARY_CERTIFICATE_REQUIRED"
    assert response.requirement.requirement_reference == _requirement_reference()


@pytest.mark.asyncio
async def test_wrong_tenant_reference_is_denied_before_lookup() -> None:
    service, _ = _service()

    with pytest.raises(RequirementResolutionAccessDeniedError):
        await service.resolve(
            request=_request(_requirement_reference(tenant_id=OTHER_TENANT_ID)),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_context_must_be_authorised_for_authenticated_caller() -> None:
    service, _ = _service()

    with pytest.raises(RequirementResolutionAccessDeniedError):
        await service.resolve(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:unknown"),
        )


@pytest.mark.asyncio
async def test_context_authority_unavailability_is_not_not_found() -> None:
    service, _ = _service(
        context_authority=FakeContextAuthority(available=False),
    )

    with pytest.raises(RequirementResolutionUnavailableError):
        await service.resolve(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_requirement_authority_unavailability_is_not_not_found() -> None:
    service, repository = _service()
    repository.set_available(False)

    with pytest.raises(RequirementResolutionUnavailableError):
        await service.resolve(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_unknown_requirement_is_not_found() -> None:
    service = RequirementResolutionService(
        contexts=FakeContextAuthority(),
        requirements=InMemoryRequirementRepository(),
    )

    with pytest.raises(RequirementResolutionNotFoundError):
        await service.resolve(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_different_pin_for_same_identity_is_conflict_not_current_substitution() -> None:
    stored_reference = _requirement_reference(
        reference_mode="VERSION_PINNED",
        version="2",
    )
    requested_reference = _requirement_reference(
        reference_mode="VERSION_PINNED",
        version="1",
    )
    service, _ = _service(_projection(requirement_reference=stored_reference))

    with pytest.raises(RequirementResolutionConflictError):
        await service.resolve(
            request=_request(requested_reference),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_nested_decision_reference_must_match_trusted_tenant() -> None:
    service, _ = _service(_projection(decision_tenant_id=OTHER_TENANT_ID))

    with pytest.raises(RequirementResolutionAccessDeniedError):
        await service.resolve(
            request=_request(),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


@pytest.mark.asyncio
async def test_repository_cannot_return_a_different_requirement_pin() -> None:
    requested = _requirement_reference()
    different = RegulatoryRequirementReference(
        owner_engine_id="baobab-regulations",
        object_type="DOCUMENT_REQUIREMENT",
        object_id="regreq_01k7rtd6other01",
        reference_mode="IDENTITY_PINNED",
        scope="tenant",
        tenant_id=TENANT_ID,
    )

    class BrokenRequirementRepository:
        async def resolve_exact(
            self,
            reference: RegulatoryRequirementReference,
        ) -> object:
            del reference
            from baobab_regulations.application.ports.requirements import (
                RequirementLookup,
                RequirementLookupStatus,
            )

            return RequirementLookup(
                status=RequirementLookupStatus.FOUND,
                requirement=_projection(requirement_reference=different),
            )

    service = RequirementResolutionService(
        contexts=FakeContextAuthority(),
        requirements=BrokenRequirementRepository(),  # type: ignore[arg-type]
    )

    with pytest.raises(RequirementResolutionIntegrityError):
        await service.resolve(
            request=_request(requested),
            caller=AuthenticatedCaller(subject="workload:trade-docs"),
        )


def test_current_reference_is_rejected_by_wire_adapter() -> None:
    with pytest.raises(ValidationError):
        _requirement_reference(reference_mode="CURRENT")


def test_wrong_owner_is_rejected_by_wire_adapter() -> None:
    payload = _requirement_reference().model_dump(mode="json")
    payload["owner_engine_id"] = "baobab-trade-docs"

    with pytest.raises(ValidationError):
        RegulatoryRequirementReference.model_validate(payload)

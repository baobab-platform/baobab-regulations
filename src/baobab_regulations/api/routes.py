"""Canonical RTD-06 HTTP routes for Regulations capabilities."""

from typing import Annotated

from fastapi import APIRouter, Depends

from baobab_regulations.api.deps import (
    AuthenticatedCapabilityRequest,
    require_authenticated_capability_request,
    require_canonical_metadata_headers,
    require_event_publication_metadata,
    require_idempotency_key,
)
from baobab_regulations.api.problems import ApiProblem, ProblemDetails
from baobab_regulations.application.ports.events import EventPublicationMetadata
from baobab_regulations.application.services.evidence_assessment import (
    EvidenceAssessmentAccessDeniedError,
    EvidenceAssessmentAuthenticationError,
    EvidenceAssessmentConflictError,
    EvidenceAssessmentContextNotFoundError,
    EvidenceAssessmentIntegrityError,
    EvidenceAssessmentInvalidIdempotencyKeyError,
    EvidenceAssessmentNotFoundError,
    EvidenceAssessmentUnavailableError,
)
from baobab_regulations.application.services.requirement_resolution import (
    RequirementResolutionAccessDeniedError,
    RequirementResolutionAuthenticationError,
    RequirementResolutionConflictError,
    RequirementResolutionContextNotFoundError,
    RequirementResolutionIntegrityError,
    RequirementResolutionNotFoundError,
    RequirementResolutionUnavailableError,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    RequirementResolveRequest,
    RequirementResolveResponse,
)

router = APIRouter()


def _problem_responses() -> dict[int | str, dict[str, object]]:
    return {
        400: {"model": ProblemDetails, "description": "Malformed or semantically invalid request"},
        401: {"model": ProblemDetails, "description": "Authentication required"},
        403: {"model": ProblemDetails, "description": "Caller/context/reference authority denied"},
        404: {"model": ProblemDetails, "description": "Exact pinned object or context not found"},
        409: {"model": ProblemDetails, "description": "Stale or conflicting governed state"},
        503: {"model": ProblemDetails, "description": "Required authority/provider unavailable"},
    }


@router.post(
    "/documentary-requirements/resolve",
    operation_id="resolveDocumentaryRequirement",
    response_model=RequirementResolveResponse,
    responses=_problem_responses(),
    dependencies=[Depends(require_canonical_metadata_headers)],
    openapi_extra={"security": [{"workloadOidc": []}]},
)
async def resolve_documentary_requirement(
    body: RequirementResolveRequest,
    auth: Annotated[
        AuthenticatedCapabilityRequest,
        Depends(require_authenticated_capability_request),
    ],
) -> RequirementResolveResponse:
    """Resolve one exact pinned Regulations-owned requirement projection."""
    try:
        return await auth.runtime.requirement_resolution.resolve(
            request=body,
            caller=auth.caller,
        )
    except RequirementResolutionAuthenticationError as exc:
        raise ApiProblem(
            status=401,
            code=exc.code,
            title="Authentication failed",
            detail="the caller could not be verified for the referenced context",
        ) from exc
    except RequirementResolutionContextNotFoundError as exc:
        raise ApiProblem(
            status=404,
            code=exc.code,
            title="Context not found",
            detail="the referenced context_id does not exist, has expired, or is unavailable to this caller",
        ) from exc
    except RequirementResolutionAccessDeniedError as exc:
        raise ApiProblem(
            status=403,
            code=exc.code,
            title="Request forbidden",
            detail="the caller or nested tenant references are not authorised for this context",
        ) from exc
    except RequirementResolutionNotFoundError as exc:
        raise ApiProblem(
            status=404,
            code=exc.code,
            title="Requirement not found",
            detail="the exact pinned Regulations requirement was not found",
        ) from exc
    except RequirementResolutionConflictError as exc:
        raise ApiProblem(
            status=409,
            code=exc.code,
            title="Requirement reference conflict",
            detail="the pinned requirement reference is stale, superseded, or conflicts with governed state",
        ) from exc
    except RequirementResolutionUnavailableError as exc:
        raise ApiProblem(
            status=503,
            code=exc.code,
            title="Requirement authority unavailable",
            detail="a required Regulations or Control Plane authority is unavailable",
            retryable=True,
        ) from exc
    except RequirementResolutionIntegrityError as exc:
        raise ApiProblem(
            status=503,
            code=exc.code,
            title="Requirement integrity failure",
            detail="a required authority returned an inconsistent requirement projection",
        ) from exc


@router.post(
    "/documentary-evidence/assessments",
    operation_id="assessDocumentaryEvidence",
    response_model=DocumentEvidenceAssessmentResult,
    responses={
        **_problem_responses(),
        201: {
            "model": DocumentEvidenceAssessmentResult,
            "description": "New assessment created",
        },
    },
    dependencies=[Depends(require_canonical_metadata_headers)],
    openapi_extra={"security": [{"workloadOidc": []}]},
)
async def assess_documentary_evidence(
    body: DocumentEvidenceAssessmentRequest,
    auth: Annotated[
        AuthenticatedCapabilityRequest,
        Depends(require_authenticated_capability_request),
    ],
    idempotency_key: Annotated[str, Depends(require_idempotency_key)],
    event_metadata: Annotated[
        EventPublicationMetadata,
        Depends(require_event_publication_metadata),
    ],
) -> DocumentEvidenceAssessmentResult:
    """Assess bounded Trade Docs documentary facts against one exact requirement."""
    try:
        return await auth.runtime.evidence_assessment.assess(
            request=body,
            caller=auth.caller,
            idempotency_key=idempotency_key,
            event_metadata=event_metadata,
        )
    except EvidenceAssessmentAuthenticationError as exc:
        raise ApiProblem(
            status=401,
            code=exc.code,
            title="Authentication failed",
            detail="the caller could not be verified for the referenced context",
        ) from exc
    except EvidenceAssessmentContextNotFoundError as exc:
        raise ApiProblem(
            status=404,
            code=exc.code,
            title="Context not found",
            detail="the referenced context_id does not exist, has expired, or is unavailable to this caller",
        ) from exc
    except EvidenceAssessmentAccessDeniedError as exc:
        raise ApiProblem(
            status=403,
            code=exc.code,
            title="Request forbidden",
            detail="the caller or nested tenant references are not authorised for this context",
        ) from exc
    except EvidenceAssessmentNotFoundError as exc:
        raise ApiProblem(
            status=404,
            code=exc.code,
            title="Requirement not found",
            detail="the exact pinned Regulations requirement was not found",
        ) from exc
    except (EvidenceAssessmentConflictError, EvidenceAssessmentInvalidIdempotencyKeyError) as exc:
        status = 400 if isinstance(exc, EvidenceAssessmentInvalidIdempotencyKeyError) else 409
        raise ApiProblem(
            status=status,
            code=exc.code,
            title="Evidence assessment conflict" if status == 409 else "Invalid request",
            detail=str(exc),
        ) from exc
    except EvidenceAssessmentUnavailableError as exc:
        raise ApiProblem(
            status=503,
            code=exc.code,
            title="Evidence assessment unavailable",
            detail="a required Regulations or Control Plane authority is unavailable",
            retryable=True,
        ) from exc
    except EvidenceAssessmentIntegrityError as exc:
        raise ApiProblem(
            status=503,
            code=exc.code,
            title="Evidence assessment integrity failure",
            detail="a required authority returned an inconsistent evidence-assessment result",
        ) from exc


__all__ = ["router"]

"""RFC 9457 Problem Details support for canonical Regulations HTTP routes."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field


class ProblemDetails(BaseModel):
    """Shared errors/v1 ProblemDetails runtime projection."""

    model_config = ConfigDict(extra="forbid")

    type: str
    title: str
    status: int = Field(ge=400, le=599)
    detail: str | None = Field(default=None, max_length=2048)
    instance: str | None = Field(default=None, max_length=512)
    code: str
    correlation_id: UUID
    trace_id: str | None = None
    retryable: bool
    errors: list[dict[str, Any]] | None = None


@dataclass(frozen=True, slots=True)
class ApiProblem(Exception):
    status: int
    code: str
    title: str
    detail: str
    retryable: bool = False


def request_correlation_id(request: Request) -> UUID:
    value = getattr(request.state, "correlation_id", None)
    if isinstance(value, UUID):
        return value
    return uuid4()


def request_trace_id(request: Request) -> str | None:
    value = getattr(request.state, "trace_id", None)
    return value if isinstance(value, str) else None


def problem_response(
    request: Request,
    *,
    status: int,
    code: str,
    title: str,
    detail: str,
    retryable: bool = False,
    errors: list[dict[str, Any]] | None = None,
) -> JSONResponse:
    problem = ProblemDetails(
        type=f"https://problems.baobab-platform.com/{code.lower().replace('_', '-')}",
        title=title,
        status=status,
        detail=detail,
        instance=request.url.path,
        code=code,
        correlation_id=request_correlation_id(request),
        trace_id=request_trace_id(request),
        retryable=retryable,
        errors=errors,
    )
    return JSONResponse(
        status_code=status,
        content=problem.model_dump(mode="json", exclude_none=True),
        media_type="application/problem+json",
        headers={"X-Correlation-ID": str(problem.correlation_id)},
    )


__all__ = [
    "ApiProblem",
    "ProblemDetails",
    "problem_response",
    "request_correlation_id",
    "request_trace_id",
]

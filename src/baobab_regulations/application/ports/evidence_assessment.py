"""R-CAP-02 Regulations-owned documentary evidence assessment port."""

from dataclasses import dataclass
from typing import Protocol

from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    RegulatoryDocumentRequirementProjection,
)


@dataclass(frozen=True, slots=True)
class EvidenceAssessmentIdentity:
    """Stable owner-side identity allocated from the idempotency boundary."""

    assessment_id: str
    tenant_id: str


class DocumentaryEvidenceAssessorUnavailableError(RuntimeError):
    """The Regulations assessment authority/runtime is unavailable."""


class DocumentaryEvidenceAssessorPort(Protocol):
    """Evaluate RTD-06 documentary facts against one exact requirement projection."""

    async def assess(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        requirement: RegulatoryDocumentRequirementProjection,
        identity: EvidenceAssessmentIdentity,
    ) -> DocumentEvidenceAssessmentResult: ...


__all__ = [
    "DocumentaryEvidenceAssessorPort",
    "DocumentaryEvidenceAssessorUnavailableError",
    "EvidenceAssessmentIdentity",
]

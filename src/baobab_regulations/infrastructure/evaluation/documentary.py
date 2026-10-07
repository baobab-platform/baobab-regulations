"""Deterministic RTD-06 reference assessor for documentary requirement projections.

This adapter deliberately evaluates only semantics carried by the exact RTD-06
projection. It does not infer broader legal applicability, mutate Trade Docs, or
replace the future production policy-evaluator path.
"""

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Literal

from baobab_regulations.application.ports.evidence_assessment import (
    EvidenceAssessmentIdentity,
)
from baobab_regulations.contracts.rtd06 import (
    DocumentEvidenceAssessmentRequest,
    DocumentEvidenceAssessmentResult,
    DocumentEvidenceFactBundle,
    DocumentVersionReference,
    RegulatoryDocumentRequirementProjection,
    RegulatoryEvidenceAssessmentReference,
    RejectedEvidence,
)


def _utc_now() -> datetime:
    return datetime.now(UTC)


class ProjectionDocumentaryEvidenceAssessor:
    """Evaluate the bounded executable requirement projection deterministically."""

    def __init__(self, *, clock: Callable[[], datetime] = _utc_now) -> None:
        self._clock = clock

    async def assess(
        self,
        *,
        request: DocumentEvidenceAssessmentRequest,
        requirement: RegulatoryDocumentRequirementProjection,
        identity: EvidenceAssessmentIdentity,
    ) -> DocumentEvidenceAssessmentResult:
        accepted: list[DocumentVersionReference] = []
        rejected: list[RejectedEvidence] = []
        global_reasons: list[str] = []
        has_review = False
        has_indeterminate = False

        for evidence in request.evidence:
            reasons, disposition = self._evaluate_evidence(
                evidence=evidence,
                requirement=requirement,
            )
            self._append_unique(global_reasons, reasons)

            if disposition == "ACCEPT":
                accepted.append(evidence.document_version_reference)
                continue

            rejected.append(
                RejectedEvidence(
                    document_version_reference=evidence.document_version_reference,
                    reason_codes=reasons,
                )
            )
            if disposition == "REVIEW":
                has_review = True
            elif disposition == "INDETERMINATE":
                has_indeterminate = True

        outcome: Literal["SATISFIED", "UNSATISFIED", "INDETERMINATE", "REVIEW_REQUIRED"]
        if accepted:
            outcome = "SATISFIED"
        elif has_review:
            outcome = "REVIEW_REQUIRED"
        elif has_indeterminate:
            outcome = "INDETERMINATE"
        else:
            outcome = "UNSATISFIED"

        evaluated_at = self._clock()
        if evaluated_at.utcoffset() is None:
            raise ValueError("assessment clock must return an offset-aware datetime")

        return DocumentEvidenceAssessmentResult(
            assessment_reference=RegulatoryEvidenceAssessmentReference(
                owner_engine_id="baobab-regulations",
                object_type="REGULATORY_EVIDENCE_ASSESSMENT",
                object_id=identity.assessment_id,
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=identity.tenant_id,
            ),
            regulatory_decision_reference=request.regulatory_decision_reference,
            requirement_reference=request.requirement_reference,
            outcome=outcome,
            accepted_document_version_references=accepted,
            rejected_evidence=rejected,
            reason_codes=global_reasons,
            resulting_regulatory_decision_reference=None,
            evaluated_at=evaluated_at,
        )

    def _evaluate_evidence(
        self,
        *,
        evidence: DocumentEvidenceFactBundle,
        requirement: RegulatoryDocumentRequirementProjection,
    ) -> tuple[list[str], str]:
        reasons: list[str] = []
        hard_failure = False
        review_required = False
        indeterminate = False

        if evidence.document_type in requirement.acceptable_document_types:
            self._append_unique(reasons, ["DOCUMENT_TYPE_ACCEPTED"])
        else:
            self._append_unique(reasons, ["DOCUMENT_TYPE_NOT_ACCEPTED"])
            hard_failure = True

        if (
            not requirement.required_issuer_roles
            or evidence.issuer_claim.issuer_role in requirement.required_issuer_roles
        ):
            self._append_unique(reasons, ["ISSUER_ROLE_ACCEPTED"])
        else:
            self._append_unique(reasons, ["ISSUER_ROLE_NOT_ACCEPTED"])
            hard_failure = True

        assertions = {
            assertion.element_code: assertion
            for assertion in evidence.documentary_assertions
        }
        missing = [
            code
            for code in requirement.required_data_elements
            if code not in assertions
        ]
        if missing:
            self._append_unique(reasons, ["REQUIRED_DATA_ELEMENT_MISSING"])
            hard_failure = True
        elif requirement.required_data_elements:
            self._append_unique(reasons, ["REQUIRED_DATA_ELEMENTS_PRESENT"])

        for code in requirement.required_data_elements:
            assertion = assertions.get(code)
            if assertion is None or assertion.field_verification_state is None:
                continue
            state = assertion.field_verification_state
            if state == "FAILED":
                self._append_unique(reasons, ["REQUIRED_DATA_ELEMENT_VERIFICATION_FAILED"])
                hard_failure = True
            elif state == "DISPUTED":
                self._append_unique(reasons, ["REQUIRED_DATA_ELEMENT_DISPUTED"])
                review_required = True
            elif state in {"UNVERIFIED", "PENDING", "UNKNOWN"}:
                self._append_unique(reasons, ["REQUIRED_DATA_ELEMENT_VERIFICATION_INDETERMINATE"])
                indeterminate = True

        verification = evidence.verification.verification_state
        if verification == "VERIFIED":
            self._append_unique(reasons, ["DOCUMENT_VERIFIED"])
        elif verification == "FAILED":
            self._append_unique(reasons, ["DOCUMENT_VERIFICATION_FAILED"])
            hard_failure = True
        elif verification == "DISPUTED":
            self._append_unique(reasons, ["DOCUMENT_VERIFICATION_DISPUTED"])
            review_required = True
        else:
            self._append_unique(reasons, ["DOCUMENT_VERIFICATION_INDETERMINATE"])
            indeterminate = True

        validity = evidence.temporal_validity.temporal_validity_state
        if validity == "CURRENTLY_VALID":
            self._append_unique(reasons, ["DOCUMENT_CURRENTLY_VALID"])
        elif validity == "UNKNOWN":
            self._append_unique(reasons, ["DOCUMENT_VALIDITY_INDETERMINATE"])
            indeterminate = True
        else:
            self._append_unique(reasons, [f"DOCUMENT_{validity}"])
            hard_failure = True

        if hard_failure:
            return reasons, "REJECT"
        if review_required:
            return reasons, "REVIEW"
        if indeterminate:
            return reasons, "INDETERMINATE"
        return reasons, "ACCEPT"

    @staticmethod
    def _append_unique(target: list[str], values: list[str]) -> None:
        for value in values:
            if value not in target:
                target.append(value)


__all__ = ["ProjectionDocumentaryEvidenceAssessor"]

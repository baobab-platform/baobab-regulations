"""Fail-closed, non-publishing regulatory candidate review scaffold.

ADR-REG-0013/0022: source extraction produces candidates, never executable
rules. ADR-REG-0026/0028 and EA v2.3: reviewer authority belongs to IAM/CP;
the engine consumes a verifier port, never caller assertions or local roles.
This module has no HTTP route and cannot promote a candidate into a RuleSet.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from baobab_regulations.application.ports.sources import SourceRegistryPort
from baobab_regulations.domain.knowledge.candidates import (
    CandidateKind,
    CandidateReviewDecision,
    CandidateReviewRecord,
    CandidateState,
    RegulatoryCandidate,
    ReviewAction,
)


class CandidateAdmissionError(ValueError):
    """Missing, stale or inconsistent source evidence."""


class CandidateReviewDenied(PermissionError):
    """Qualified current reviewer authority or SoD was not established."""


class CandidateReviewConflict(RuntimeError):
    """An immutable submission, prior decision or revision conflicts."""


@dataclass(frozen=True, slots=True)
class QualifiedReviewer:
    """Verification result supplied ONLY by a trusted external authority port."""

    principal_id: str
    competence_profile_ref: str
    candidate_kinds: frozenset[CandidateKind]
    actions: frozenset[ReviewAction]
    valid_until: datetime


class ReviewerAuthorityPort(Protocol):
    async def verify(
        self, *, principal_id: str, candidate: RegulatoryCandidate
    ) -> QualifiedReviewer: ...


class CandidateReviewRepositoryPort(Protocol):
    async def insert(self, candidate: RegulatoryCandidate) -> CandidateReviewRecord: ...

    async def get(self, candidate_id: str) -> CandidateReviewRecord | None: ...

    async def record_decision(
        self, *, decision: CandidateReviewDecision, expected_revision: int
    ) -> CandidateReviewRecord: ...


class CandidateReviewService:
    """Source-bound candidate admission and independently checked review.

    A successful review only marks a candidate APPROVED_FOR_PROMOTION. This
    service cannot write a RuleVersion, BRIR, requirement projection, grant,
    provider status or legal approval. Such a publication service must later
    enforce separate source, competency, rules tests and approval gates.
    """

    def __init__(
        self,
        *,
        sources: SourceRegistryPort,
        candidates: CandidateReviewRepositoryPort,
        reviewers: ReviewerAuthorityPort,
    ) -> None:
        self._sources = sources
        self._candidates = candidates
        self._reviewers = reviewers

    async def submit(self, candidate: RegulatoryCandidate) -> CandidateReviewRecord:
        source = await self._sources.get_source(candidate.source_id)
        artefact = await self._sources.get_artefact(candidate.artefact_id)
        if source is None or artefact is None:
            raise CandidateAdmissionError("candidate lacks a registered source and artefact")
        if artefact.source_id != source.source_id:
            raise CandidateAdmissionError("candidate source does not own its artefact")
        if artefact.content_hash != f"sha256:{candidate.artefact_sha256}":
            raise CandidateAdmissionError("candidate source content hash is not pinned")
        return await self._candidates.insert(candidate)

    async def review(
        self,
        *,
        candidate_id: str,
        reviewer_principal_id: str,
        action: ReviewAction,
        expected_revision: int,
        reason_codes: tuple[str, ...],
        supporting_evidence_refs: tuple[str, ...],
        decided_at: datetime,
    ) -> CandidateReviewRecord:
        record = await self._candidates.get(candidate_id)
        if record is None:
            raise CandidateReviewConflict("candidate not found")
        candidate = record.candidate
        if record.state in {CandidateState.REJECTED, CandidateState.APPROVED_FOR_PROMOTION}:
            raise CandidateReviewConflict("candidate review already terminal")
        if record.revision != expected_revision:
            raise CandidateReviewConflict("candidate review revision is stale")
        if record.candidate_fingerprint != candidate.fingerprint():
            raise CandidateReviewConflict("candidate payload changed after submission")
        if not reviewer_principal_id or reviewer_principal_id == candidate.producer_principal_id:
            raise CandidateReviewDenied("independent checker must differ from candidate maker")

        # No fallback to supplied roles, token claims or locally inferred CP grants.
        authority = await self._reviewers.verify(
            principal_id=reviewer_principal_id, candidate=candidate
        )
        if authority.principal_id != reviewer_principal_id:
            raise CandidateReviewDenied("reviewer authority is not caller-bound")
        if authority.valid_until.utcoffset() is None or decided_at.utcoffset() is None:
            raise CandidateReviewDenied("qualified authority requires timezone-aware validity")
        if authority.valid_until <= decided_at:
            raise CandidateReviewDenied("reviewer authority is expired")
        if candidate.kind not in authority.candidate_kinds or action not in authority.actions:
            raise CandidateReviewDenied("reviewer has no current competence for this action")

        decision = CandidateReviewDecision(
            candidate_id=candidate.candidate_id,
            candidate_fingerprint=record.candidate_fingerprint,
            reviewer_principal_id=reviewer_principal_id,
            competence_profile_ref=authority.competence_profile_ref,
            action=action,
            reason_codes=reason_codes,
            supporting_evidence_refs=supporting_evidence_refs,
            decided_at=decided_at,
        )
        return await self._candidates.record_decision(
            decision=decision, expected_revision=expected_revision
        )


__all__ = [
    "CandidateAdmissionError", "CandidateReviewConflict",
    "CandidateReviewDenied", "CandidateReviewRepositoryPort",
    "CandidateReviewService", "QualifiedReviewer", "ReviewerAuthorityPort",
]

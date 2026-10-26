"""Non-production review queue for deterministic offline qualification.

Never register this adapter as a production regulatory authority. PostgreSQL
review history, trust-bound IAM/CP reviewer verification, and legal approval
must be developed and qualified separately before publication is permitted.
"""

from __future__ import annotations

from copy import deepcopy

from baobab_regulations.application.services.candidate_review import CandidateReviewConflict
from baobab_regulations.domain.knowledge.candidates import (
    CandidateReviewDecision,
    CandidateReviewRecord,
    CandidateState,
    RegulatoryCandidate,
    ReviewAction,
)


class InMemoryCandidateReviewRepository:
    def __init__(self) -> None:
        self._records: dict[str, CandidateReviewRecord] = {}

    async def insert(self, candidate: RegulatoryCandidate) -> CandidateReviewRecord:
        key = str(candidate.candidate_id)
        if key in self._records:
            raise CandidateReviewConflict("candidate identity already exists; no overwrite")
        snapshot = deepcopy(candidate)
        record = CandidateReviewRecord(
            candidate=snapshot,
            candidate_fingerprint=snapshot.fingerprint(),
        )
        self._records[key] = record
        return deepcopy(record)

    async def get(self, candidate_id: str) -> CandidateReviewRecord | None:
        record = self._records.get(candidate_id)
        return deepcopy(record) if record else None

    async def record_decision(
        self, *, decision: CandidateReviewDecision, expected_revision: int
    ) -> CandidateReviewRecord:
        key = str(decision.candidate_id)
        record = self._records.get(key)
        if record is None or record.revision != expected_revision:
            raise CandidateReviewConflict("review subject missing or revision changed")
        if record.candidate_fingerprint != record.candidate.fingerprint():
            raise CandidateReviewConflict("candidate content integrity failure")
        if decision.candidate_fingerprint != record.candidate_fingerprint:
            raise CandidateReviewConflict("review decision is bound to another candidate version")
        if decision.reviewer_principal_id == record.candidate.producer_principal_id:
            raise CandidateReviewConflict("maker cannot check their own candidate")
        if record.state in {CandidateState.REJECTED, CandidateState.APPROVED_FOR_PROMOTION}:
            raise CandidateReviewConflict("terminal candidate cannot be reviewed")
        next_state = {
            ReviewAction.APPROVE: CandidateState.APPROVED_FOR_PROMOTION,
            ReviewAction.REQUEST_CHANGES: CandidateState.CHANGES_REQUESTED,
            ReviewAction.REJECT: CandidateState.REJECTED,
            ReviewAction.ABSTAIN: CandidateState.NEEDS_REVIEW,
        }[decision.action]
        changed = record.model_copy(update={
            "state": next_state,
            "revision": record.revision + 1,
            "decisions": (*record.decisions, deepcopy(decision)),
        })
        self._records[key] = changed
        return deepcopy(changed)


__all__ = ["InMemoryCandidateReviewRepository"]

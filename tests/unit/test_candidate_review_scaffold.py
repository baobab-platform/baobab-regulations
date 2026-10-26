"""ADR-REG-0013/0022 and EA v2.3 candidate and review boundary tests."""

import hashlib
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from baobab_regulations.application.services.candidate_review import (
    CandidateAdmissionError,
    CandidateReviewConflict,
    CandidateReviewDenied,
    CandidateReviewService,
    QualifiedReviewer,
)
from baobab_regulations.domain.knowledge.candidates import (
    CandidateKind,
    CandidateState,
    ExtractionMethod,
    RegulatoryCandidate,
    ReviewAction,
)
from baobab_regulations.domain.shared.ids import RegulatoryId
from baobab_regulations.domain.sources.models import (
    AuthoritativeSource,
    RightsClass,
    SourceArtefact,
)
from baobab_regulations.infrastructure.persistence.candidate_review_memory import (
    InMemoryCandidateReviewRepository,
)
from baobab_regulations.infrastructure.persistence.sources_memory import InMemorySourceRegistry

NOW = datetime(2026, 10, 26, 12, tzinfo=UTC)
HASH = hashlib.sha256(b"synthetic government notice").hexdigest()


class TestReviewerAuthority:
    """Injected verifier fake, never a production CP/IAM authorisation adapter."""

    def __init__(self, *, expires: datetime = NOW + timedelta(days=1)) -> None:
        self.expires = expires
        self.called = False

    async def verify(
        self, *, principal_id: str, candidate: RegulatoryCandidate
    ) -> QualifiedReviewer:
        self.called = True
        return QualifiedReviewer(
            principal_id=principal_id,
            competence_profile_ref="synthetic-profile-checker",
            candidate_kinds=frozenset({CandidateKind.REQUIREMENT}),
            actions=frozenset(ReviewAction),
            valid_until=self.expires,
        )


def make_candidate(**changes: object) -> RegulatoryCandidate:
    args: dict[str, object] = dict(
        candidate_id=RegulatoryId("candidate-001"),
        candidate_version=1,
        kind=CandidateKind.REQUIREMENT,
        source_id=RegulatoryId("source-ug-test"),
        artefact_id=RegulatoryId("artefact-ug-test"),
        artefact_sha256=HASH,
        source_locator="synthetic section 3",
        proposed_payload={"requirement_code": "TEST_ONLY", "condition": True},
        extraction_method=ExtractionMethod.DETERMINISTIC,
        producer_principal_id="maker-1",
        proposed_at=NOW,
        scope="tenant",
        tenant_id="tn_test123",
    )
    args.update(changes)
    return RegulatoryCandidate.model_validate(args)


async def set_up() -> tuple[CandidateReviewService, InMemoryCandidateReviewRepository, TestReviewerAuthority]:
    sources = InMemorySourceRegistry()
    await sources.save_source(AuthoritativeSource(
        source_id=RegulatoryId("source-ug-test"),
        name="Synthetic source (not law)",
        publisher="Synthetic test authority",
    ))
    await sources.save_artefact(SourceArtefact(
        artefact_id=RegulatoryId("artefact-ug-test"),
        source_id=RegulatoryId("source-ug-test"),
        uri="https://example.invalid/synthetic-notice",
        retrieved_at=NOW,
        content_hash=f"sha256:{HASH}",
        rights_class=RightsClass.CITATION_ONLY,
    ))
    queue = InMemoryCandidateReviewRepository()
    reviewers = TestReviewerAuthority()
    return CandidateReviewService(
        sources=sources, candidates=queue, reviewers=reviewers
    ), queue, reviewers


@pytest.mark.asyncio
async def test_admission_requires_registered_exact_source_content() -> None:
    service, _, _ = await set_up()
    with pytest.raises(CandidateAdmissionError, match="content hash"):
        await service.submit(make_candidate(artefact_sha256="f" * 64))
    with pytest.raises(CandidateAdmissionError, match="registered source"):
        await service.submit(make_candidate(source_id=RegulatoryId("wrong-source")))
    record = await service.submit(make_candidate())
    assert record.state is CandidateState.NEEDS_REVIEW
    assert record.revision == 1
    with pytest.raises(CandidateReviewConflict, match="no overwrite"):
        await service.submit(make_candidate(proposed_payload={"changed": True}))


@pytest.mark.asyncio
async def test_independent_checker_only_approves_candidate_not_rule() -> None:
    service, queue, reviewers = await set_up()
    await service.submit(make_candidate())
    with pytest.raises(CandidateReviewDenied, match="independent checker"):
        await service.review(
            candidate_id="candidate-001", reviewer_principal_id="maker-1",
            action=ReviewAction.APPROVE, expected_revision=1,
            reason_codes=("MATCHES_SOURCE",),
            supporting_evidence_refs=("review-note-1",), decided_at=NOW,
        )
    assert not reviewers.called
    reviewed = await service.review(
        candidate_id="candidate-001", reviewer_principal_id="checker-2",
        action=ReviewAction.APPROVE, expected_revision=1,
        reason_codes=("MATCHES_SOURCE",),
        supporting_evidence_refs=("review-note-1",), decided_at=NOW,
    )
    assert reviewed.state is CandidateState.APPROVED_FOR_PROMOTION
    assert reviewed.revision == 2
    assert reviewed.decisions[0].candidate_fingerprint == reviewed.candidate.fingerprint()
    assert (await queue.get("candidate-001")).state is CandidateState.APPROVED_FOR_PROMOTION
    # No rule-set/requirement writer is present or invoked by this service.
    with pytest.raises(CandidateReviewConflict, match="terminal"):
        await service.review(
            candidate_id="candidate-001", reviewer_principal_id="checker-3",
            action=ReviewAction.APPROVE, expected_revision=2,
            reason_codes=("MATCHES_SOURCE",),
            supporting_evidence_refs=("review-note-2",), decided_at=NOW,
        )


@pytest.mark.asyncio
async def test_stale_revision_and_expired_reviewer_are_denied() -> None:
    service, _, reviewers = await set_up()
    await service.submit(make_candidate())
    reviewers.expires = NOW - timedelta(seconds=1)
    with pytest.raises(CandidateReviewDenied, match="expired"):
        await service.review(
            candidate_id="candidate-001", reviewer_principal_id="checker-2",
            action=ReviewAction.APPROVE, expected_revision=1,
            reason_codes=("OK",), supporting_evidence_refs=("e-1",), decided_at=NOW,
        )
    reviewers.expires = NOW + timedelta(days=1)
    with pytest.raises(CandidateReviewConflict, match="stale"):
        await service.review(
            candidate_id="candidate-001", reviewer_principal_id="checker-2",
            action=ReviewAction.APPROVE, expected_revision=0,
            reason_codes=("OK",), supporting_evidence_refs=("e-1",), decided_at=NOW,
        )


@pytest.mark.asyncio
async def test_abstain_does_not_promote_and_approval_requires_evidence() -> None:
    service, _, _ = await set_up()
    await service.submit(make_candidate())
    result = await service.review(
        candidate_id="candidate-001", reviewer_principal_id="checker-2",
        action=ReviewAction.ABSTAIN, expected_revision=1,
        reason_codes=("INSUFFICIENT_BASIS",),
        supporting_evidence_refs=(), decided_at=NOW,
    )
    assert result.state is CandidateState.NEEDS_REVIEW
    assert result.revision == 2
    with pytest.raises(ValidationError, match="supporting evidence"):
        await service.review(
            candidate_id="candidate-001", reviewer_principal_id="checker-2",
            action=ReviewAction.APPROVE, expected_revision=2,
            reason_codes=("OK",), supporting_evidence_refs=(), decided_at=NOW,
        )


@pytest.mark.asyncio
async def test_submitted_candidate_payload_is_defensively_copied() -> None:
    service, queue, _ = await set_up()
    candidate = make_candidate()
    record = await service.submit(candidate)
    candidate.proposed_payload["requirement_code"] = "MUTATED"
    assert (await queue.get("candidate-001")).candidate.fingerprint() == record.candidate_fingerprint


def test_ai_lineage_and_tenant_scope_are_mandatory() -> None:
    with pytest.raises(ValidationError, match="model and prompt"):
        make_candidate(extraction_method=ExtractionMethod.AI_ASSISTED)
    with pytest.raises(ValidationError, match="tenant reference"):
        make_candidate(tenant_id=None)
    with pytest.raises(ValidationError, match="tenant identity"):
        make_candidate(scope="platform")

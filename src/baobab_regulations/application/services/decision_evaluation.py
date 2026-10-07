"""R-CAP-09 production orchestration for regulations.decision.evaluate."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable, Iterable
from datetime import UTC, datetime

from baobab_regulations.application.ports.context_authority import (
    AuthenticatedCaller,
    ContextAccessDeniedError,
    ContextAuthenticationError,
    ContextAuthorityPort,
    ContextAuthorityUnavailableError,
    ContextNotFoundError,
)
from baobab_regulations.application.ports.decision_idempotency import (
    DecisionEvaluationIdempotencyPort,
    DecisionIdempotencyConflictError,
    DecisionIdempotencyIntegrityError,
    DecisionIdempotencyUnavailableError,
)
from baobab_regulations.application.ports.evaluator import (
    EvaluatorNotReadyError,
    EvaluatorProtocolError,
    EvaluatorRuntimeError,
    EvaluatorUndefinedError,
    RegulatoryEvaluationInput,
    RegulatoryEvaluationResult,
    RegulatoryPolicyEvaluatorPort,
)
from baobab_regulations.application.ports.rule_sets import (
    RuleSetAuthorityPort,
    RuleSetAuthorityUnavailableError,
    RuleSetConflictError,
    RuleSetIntegrityError,
    RuleSetNotFoundError,
)
from baobab_regulations.contracts.decision import (
    DecisionEvaluateRequest,
    DecisionEvaluateResponse,
    DecisionProvenance,
    PinnedCrossEngineReference,
    RegulatoryAssessmentReference,
    RegulatoryDecisionReference,
    ReplayIdentity,
)

_IDEMPOTENCY_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_ENFORCEMENT_RANK = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4}
_OUTCOMES = {
    "SATISFIED",
    "SATISFIED_WITH_REQUIREMENTS",
    "UNSATISFIED",
    "PROHIBITED",
    "INDETERMINATE",
    "NOT_APPLICABLE",
}


class DecisionEvaluationAuthenticationError(PermissionError):
    code = "REGULATIONS_DECISION_AUTHENTICATION_FAILED"


class DecisionEvaluationContextNotFoundError(LookupError):
    code = "REGULATIONS_CONTEXT_NOT_FOUND"


class DecisionEvaluationAccessDeniedError(PermissionError):
    code = "REGULATIONS_DECISION_ACCESS_DENIED"


class DecisionEvaluationNotFoundError(LookupError):
    code = "REGULATIONS_DECISION_RULE_SET_NOT_FOUND"


class DecisionEvaluationConflictError(RuntimeError):
    code = "REGULATIONS_DECISION_CONFLICT"


class DecisionEvaluationInvalidRequestError(ValueError):
    code = "REGULATIONS_DECISION_INVALID_REQUEST"


class DecisionEvaluationInvalidIdempotencyKeyError(ValueError):
    code = "REGULATIONS_DECISION_INVALID_IDEMPOTENCY_KEY"


class DecisionEvaluationIntegrityError(RuntimeError):
    code = "REGULATIONS_DECISION_INTEGRITY_FAILURE"


class DecisionEvaluatorUndefinedError(RuntimeError):
    code = "EVALUATOR_UNDEFINED"


class DecisionEvaluatorProtocolError(RuntimeError):
    code = "EVALUATOR_PROTOCOL_ERROR"


class DecisionEvaluatorRuntimeError(RuntimeError):
    code = "EVALUATOR_RUNTIME_ERROR"


class DecisionEvaluatorNotReadyError(RuntimeError):
    code = "EVALUATOR_NOT_READY"


class DecisionEvaluationUnavailableError(RuntimeError):
    code = "REGULATIONS_DECISION_AUTHORITY_UNAVAILABLE"


class DecisionEvaluationService:
    """Execute the canonical decision contract without operational side effects."""

    def __init__(
        self,
        *,
        contexts: ContextAuthorityPort,
        rule_sets: RuleSetAuthorityPort,
        evaluator: RegulatoryPolicyEvaluatorPort,
        idempotency: DecisionEvaluationIdempotencyPort,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._contexts = contexts
        self._rule_sets = rule_sets
        self._evaluator = evaluator
        self._idempotency = idempotency
        self._clock = clock or (lambda: datetime.now(UTC))

    async def evaluate(
        self,
        *,
        request: DecisionEvaluateRequest,
        caller: AuthenticatedCaller,
        idempotency_key: str,
    ) -> DecisionEvaluateResponse:
        key = self._validate_idempotency_key(idempotency_key)
        self._validate_temporal_profile(request)

        try:
            trusted = await self._contexts.redeem(
                context_id=request.context_id,
                caller=caller,
            )
        except ContextAuthenticationError as exc:
            raise DecisionEvaluationAuthenticationError(
                "caller token could not be independently verified"
            ) from exc
        except ContextNotFoundError as exc:
            raise DecisionEvaluationContextNotFoundError(
                "supplied context_id is unavailable to this caller"
            ) from exc
        except ContextAccessDeniedError as exc:
            raise DecisionEvaluationAccessDeniedError(
                "caller is not authorised for the supplied context_id"
            ) from exc
        except ContextAuthorityUnavailableError as exc:
            raise DecisionEvaluationUnavailableError(
                "Control Plane context authority is unavailable"
            ) from exc

        tenant_id = trusted.tenant_id
        self._enforce_request_tenant(request=request, trusted_tenant_id=tenant_id)
        request_fingerprint = self._request_fingerprint(request)
        input_fingerprint = self._input_fingerprint(
            request=request,
            trusted_tenant_id=tenant_id,
        )

        try:
            replay = await self._idempotency.replay(
                tenant_id=tenant_id,
                idempotency_key=key,
                request_fingerprint=request_fingerprint,
                replay_key=request.replay_key,
                input_fingerprint=input_fingerprint,
            )
        except DecisionIdempotencyConflictError as exc:
            raise DecisionEvaluationConflictError(str(exc)) from exc
        except DecisionIdempotencyIntegrityError as exc:
            raise DecisionEvaluationIntegrityError(str(exc)) from exc
        except DecisionIdempotencyUnavailableError as exc:
            raise DecisionEvaluationUnavailableError(
                "decision replay authority is unavailable"
            ) from exc

        if replay is not None:
            self._validate_response_integrity(
                request=request,
                response=replay.response,
                trusted_tenant_id=tenant_id,
            )
            return replay.response

        try:
            rule_set = await self._rule_sets.resolve_exact(
                reference=request.rule_set_reference,
                legal_time=request.legal_time,
                knowledge_time=request.knowledge_time,
                requested_assurance=request.requested_assurance,
                trusted_tenant_id=tenant_id,
            )
        except RuleSetNotFoundError as exc:
            raise DecisionEvaluationNotFoundError(str(exc)) from exc
        except RuleSetConflictError as exc:
            raise DecisionEvaluationConflictError(str(exc)) from exc
        except RuleSetIntegrityError as exc:
            raise DecisionEvaluationIntegrityError(str(exc)) from exc
        except RuleSetAuthorityUnavailableError as exc:
            raise DecisionEvaluationUnavailableError(
                "Regulations rule-set authority is unavailable"
            ) from exc

        evaluation = RegulatoryEvaluationInput(
            request=request,
            tenant_id=tenant_id,
            rule_set=rule_set,
            input_fingerprint=input_fingerprint,
        )

        try:
            result = await self._evaluator.evaluate(evaluation)
        except EvaluatorUndefinedError as exc:
            raise DecisionEvaluatorUndefinedError(str(exc)) from exc
        except EvaluatorProtocolError as exc:
            raise DecisionEvaluatorProtocolError(str(exc)) from exc
        except EvaluatorNotReadyError as exc:
            raise DecisionEvaluatorNotReadyError(str(exc)) from exc
        except EvaluatorRuntimeError as exc:
            raise DecisionEvaluatorRuntimeError(str(exc)) from exc

        self._validate_evaluator_result(
            request=request,
            result=result,
            trusted_tenant_id=tenant_id,
        )
        now = self._clock()
        if now.utcoffset() is None:
            raise DecisionEvaluationIntegrityError("decision clock must be timezone-aware")

        identity_seed = (
            f"{tenant_id}\n{request.replay_key}\n{input_fingerprint}\n{rule_set.fingerprint}"
        )
        identity_hash = hashlib.sha256(identity_seed.encode("utf-8")).hexdigest()

        response = DecisionEvaluateResponse(
            decision_reference=RegulatoryDecisionReference(
                owner_engine_id="baobab-regulations",
                object_type="REGULATORY_DECISION",
                object_id=f"regdec_{identity_hash[:24]}",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=tenant_id,
            ),
            assessment_reference=RegulatoryAssessmentReference(
                owner_engine_id="baobab-regulations",
                object_type="REGULATORY_ASSESSMENT",
                object_id=f"regassess_{identity_hash[24:48]}",
                reference_mode="IDENTITY_PINNED",
                scope="tenant",
                tenant_id=tenant_id,
            ),
            outcome=result.outcome,
            enforcement_class=result.enforcement_class,
            reasons=list(result.reasons),
            legal_basis_references=list(result.legal_basis_references),
            evidence_references=list(result.evidence_references),
            recommended_disposition=result.recommended_disposition,
            rule_set_reference=rule_set.reference,
            rule_set_fingerprint=rule_set.fingerprint,
            evaluated_at=now,
            legal_time=request.legal_time,
            knowledge_time=request.knowledge_time,
            provenance=DecisionProvenance(
                contract_major=1,
                input_fingerprint=input_fingerprint,
                rule_set_reference=rule_set.reference,
                rule_set_fingerprint=rule_set.fingerprint,
                evaluation_profile=request.evaluation_profile,
            ),
            replay_identity=ReplayIdentity(
                replay_key=request.replay_key,
                input_fingerprint=input_fingerprint,
                rule_set_fingerprint=rule_set.fingerprint,
            ),
        )
        self._validate_response_integrity(
            request=request,
            response=response,
            trusted_tenant_id=tenant_id,
        )

        try:
            committed = await self._idempotency.commit(
                tenant_id=tenant_id,
                idempotency_key=key,
                request_fingerprint=request_fingerprint,
                input_fingerprint=input_fingerprint,
                request=request,
                response=response,
            )
        except DecisionIdempotencyConflictError as exc:
            raise DecisionEvaluationConflictError(str(exc)) from exc
        except DecisionIdempotencyIntegrityError as exc:
            raise DecisionEvaluationIntegrityError(str(exc)) from exc
        except DecisionIdempotencyUnavailableError as exc:
            raise DecisionEvaluationUnavailableError(
                "decision persistence authority is unavailable"
            ) from exc

        self._validate_response_integrity(
            request=request,
            response=committed.response,
            trusted_tenant_id=tenant_id,
        )
        return committed.response

    @staticmethod
    def _validate_idempotency_key(value: str) -> str:
        key = value.strip()
        if not 16 <= len(key) <= 128 or _IDEMPOTENCY_KEY.fullmatch(key) is None:
            raise DecisionEvaluationInvalidIdempotencyKeyError(
                "Idempotency-Key must be 16-128 characters and match "
                "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
            )
        return key

    @staticmethod
    def _validate_temporal_profile(request: DecisionEvaluateRequest) -> None:
        historical = request.assessment_purpose == "HISTORICAL_REPLAY"
        future = request.assessment_purpose == "FUTURE_SIMULATION"
        if historical != (request.evaluation_profile == "HISTORICAL_REPLAY"):
            raise DecisionEvaluationInvalidRequestError(
                "HISTORICAL_REPLAY purpose/profile must be selected together"
            )
        if future != (request.evaluation_profile == "FUTURE_SIMULATION"):
            raise DecisionEvaluationInvalidRequestError(
                "FUTURE_SIMULATION purpose/profile must be selected together"
            )

    @staticmethod
    def _request_fingerprint(request: DecisionEvaluateRequest) -> str:
        encoded = json.dumps(
            request.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _input_fingerprint(
        *,
        request: DecisionEvaluateRequest,
        trusted_tenant_id: str,
    ) -> str:
        semantic = request.model_dump(mode="json")
        semantic.pop("replay_key", None)
        encoded = json.dumps(
            {
                "contract_major": 1,
                "trusted_tenant_id": trusted_tenant_id,
                "request": semantic,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _enforce_request_tenant(
        self,
        *,
        request: DecisionEvaluateRequest,
        trusted_tenant_id: str,
    ) -> None:
        refs: list[PinnedCrossEngineReference] = [
            *request.subject_references,
            *request.evidence_references,
        ]
        for fact in request.facts:
            if fact.source_reference is not None:
                refs.append(fact.source_reference)
        refs.append(PinnedCrossEngineReference.model_validate(
            request.rule_set_reference.model_dump(mode="json")
        ))
        self._enforce_reference_tenants(refs, trusted_tenant_id=trusted_tenant_id)

    def _validate_evaluator_result(
        self,
        *,
        request: DecisionEvaluateRequest,
        result: RegulatoryEvaluationResult,
        trusted_tenant_id: str,
    ) -> None:
        if result.outcome not in _OUTCOMES:
            raise DecisionEvaluationIntegrityError(
                f"evaluator returned unsupported regulatory outcome {result.outcome!r}"
            )
        if result.enforcement_class not in _ENFORCEMENT_RANK:
            raise DecisionEvaluationIntegrityError("evaluator returned unknown enforcement class")
        ceiling = request.requested_enforcement_class_ceiling
        if _ENFORCEMENT_RANK[result.enforcement_class] > _ENFORCEMENT_RANK[ceiling]:
            raise DecisionEvaluationIntegrityError(
                "evaluator exceeded requested enforcement-class ceiling"
            )

        returned_refs: list[PinnedCrossEngineReference] = [
            *result.legal_basis_references,
            *result.evidence_references,
        ]
        for reason in result.reasons:
            returned_refs.extend(reason.legal_basis_references)
            returned_refs.extend(reason.evidence_references)
            returned_refs.extend(
                PinnedCrossEngineReference.model_validate(item.model_dump(mode="json"))
                for item in reason.rule_version_references
            )
        if result.recommended_disposition is not None:
            returned_refs.extend(
                PinnedCrossEngineReference.model_validate(item.model_dump(mode="json"))
                for item in result.recommended_disposition.missing_requirement_references
            )
        self._enforce_reference_tenants(
            returned_refs,
            trusted_tenant_id=trusted_tenant_id,
        )

        supplied_evidence = {
            item.model_dump_json()
            for item in request.evidence_references
        }
        supplied_evidence.update(
            fact.source_reference.model_dump_json()
            for fact in request.facts
            if fact.source_reference is not None
        )
        for reference in [
            *result.evidence_references,
            *(ref for reason in result.reasons for ref in reason.evidence_references),
        ]:
            if reference.model_dump_json() not in supplied_evidence:
                raise DecisionEvaluationIntegrityError(
                    "evaluator cited evidence that was not supplied by the canonical request"
                )

    def _validate_response_integrity(
        self,
        *,
        request: DecisionEvaluateRequest,
        response: DecisionEvaluateResponse,
        trusted_tenant_id: str,
    ) -> None:
        if response.rule_set_reference != request.rule_set_reference:
            raise DecisionEvaluationIntegrityError(
                "decision response changed the requested rule-set reference"
            )
        if response.legal_time != request.legal_time:
            raise DecisionEvaluationIntegrityError("decision response changed legal_time")
        if response.knowledge_time != request.knowledge_time:
            raise DecisionEvaluationIntegrityError("decision response changed knowledge_time")
        if response.replay_identity.replay_key != request.replay_key:
            raise DecisionEvaluationIntegrityError("decision response changed replay_key")
        if response.provenance.input_fingerprint != response.replay_identity.input_fingerprint:
            raise DecisionEvaluationIntegrityError("decision input fingerprints diverge")
        if response.provenance.rule_set_fingerprint != response.rule_set_fingerprint:
            raise DecisionEvaluationIntegrityError("decision rule-set fingerprints diverge")
        if response.replay_identity.rule_set_fingerprint != response.rule_set_fingerprint:
            raise DecisionEvaluationIntegrityError("replay rule-set fingerprint diverges")

        refs: list[PinnedCrossEngineReference] = [
            PinnedCrossEngineReference.model_validate(
                response.decision_reference.model_dump(mode="json")
            ),
            PinnedCrossEngineReference.model_validate(
                response.assessment_reference.model_dump(mode="json")
            ),
            *response.legal_basis_references,
            *response.evidence_references,
        ]
        self._enforce_reference_tenants(refs, trusted_tenant_id=trusted_tenant_id)

    @staticmethod
    def _enforce_reference_tenants(
        references: Iterable[PinnedCrossEngineReference],
        *,
        trusted_tenant_id: str,
    ) -> None:
        for reference in references:
            if reference.scope == "tenant" and reference.tenant_id != trusted_tenant_id:
                raise DecisionEvaluationAccessDeniedError(
                    "tenant-scoped reference does not match trusted context tenant"
                )


__all__ = [
    "DecisionEvaluationAccessDeniedError",
    "DecisionEvaluationAuthenticationError",
    "DecisionEvaluationConflictError",
    "DecisionEvaluationContextNotFoundError",
    "DecisionEvaluationIntegrityError",
    "DecisionEvaluationInvalidIdempotencyKeyError",
    "DecisionEvaluationInvalidRequestError",
    "DecisionEvaluationNotFoundError",
    "DecisionEvaluationService",
    "DecisionEvaluationUnavailableError",
    "DecisionEvaluatorNotReadyError",
    "DecisionEvaluatorProtocolError",
    "DecisionEvaluatorRuntimeError",
    "DecisionEvaluatorUndefinedError",
]

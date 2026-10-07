"""OPA HTTP adapter for the production deterministic evaluator path.

OPA is an implementation detail behind RegulatoryPolicyEvaluatorPort. Canonical
Shared request/response models never expose Rego package paths or OPA metadata.
"""

from __future__ import annotations

from typing import Annotated, Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from baobab_regulations.application.ports.evaluator import (
    EvaluatorNotReadyError,
    EvaluatorProtocolError,
    EvaluatorRuntimeError,
    EvaluatorUndefinedError,
    RegulatoryEvaluationInput,
    RegulatoryEvaluationResult,
)
from baobab_regulations.contracts.decision import (
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
)


class _OpaDecisionEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    rule_set_fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    outcome: str
    enforcement_class: str
    reasons: list[DecisionReason]
    legal_basis_references: list[PinnedCrossEngineReference]
    evidence_references: list[PinnedCrossEngineReference]
    recommended_disposition: RecommendedDisposition | None


class OpaRegulatoryPolicyEvaluator:
    """Evaluate canonical decision inputs through OPA's Data API."""

    def __init__(
        self,
        *,
        client: httpx.AsyncClient,
    ) -> None:
        self._client = client

    async def evaluate(
        self,
        evaluation: RegulatoryEvaluationInput,
    ) -> RegulatoryEvaluationResult:
        entrypoint = evaluation.rule_set.entrypoint.strip("/")
        if not entrypoint:
            raise EvaluatorNotReadyError("governed OPA entrypoint is empty")
        if evaluation.rule_set.target != "rego/v1":
            raise EvaluatorNotReadyError(
                "resolved policy artifact is not compatible with the OPA Rego v1 adapter"
            )

        await self._require_ready()

        payload = {
            "input": {
                "contract_major": 1,
                "tenant_id": evaluation.tenant_id,
                "input_fingerprint": evaluation.input_fingerprint,
                "rule_set": {
                    "object_id": evaluation.rule_set.reference.object_id,
                    "fingerprint": evaluation.rule_set.fingerprint,
                    "assurance_state": evaluation.rule_set.assurance_state,
                },
                "request": evaluation.request.model_dump(mode="json"),
            }
        }

        try:
            response = await self._client.post(
                f"/v1/data/{entrypoint}",
                json=payload,
            )
        except (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError) as exc:
            raise EvaluatorRuntimeError("OPA evaluation transport failed") from exc

        if response.status_code >= 500:
            raise EvaluatorRuntimeError(
                f"OPA evaluation failed with HTTP {response.status_code}"
            )
        if response.status_code != 200:
            raise EvaluatorProtocolError(
                f"OPA Data API returned unexpected HTTP {response.status_code}"
            )

        try:
            document: Any = response.json()
        except ValueError as exc:
            raise EvaluatorProtocolError("OPA response was not valid JSON") from exc
        if not isinstance(document, dict):
            raise EvaluatorProtocolError("OPA response root must be an object")
        if "result" not in document:
            raise EvaluatorUndefinedError(
                "OPA query was undefined and returned no result"
            )

        try:
            result = _OpaDecisionEnvelope.model_validate(document["result"])
        except ValidationError as exc:
            raise EvaluatorProtocolError(
                "OPA result does not satisfy the Regulations evaluator protocol"
            ) from exc

        if result.input_fingerprint != evaluation.input_fingerprint:
            raise EvaluatorProtocolError(
                "OPA result does not match the canonical input fingerprint"
            )
        if result.rule_set_fingerprint != evaluation.rule_set.fingerprint:
            raise EvaluatorProtocolError(
                "OPA result does not match the resolved rule-set fingerprint"
            )

        return RegulatoryEvaluationResult(
            outcome=result.outcome,
            enforcement_class=result.enforcement_class,
            reasons=tuple(result.reasons),
            legal_basis_references=tuple(result.legal_basis_references),
            evidence_references=tuple(result.evidence_references),
            recommended_disposition=result.recommended_disposition,
        )

    async def _require_ready(self) -> None:
        try:
            response = await self._client.get(
                "/health",
                params={"bundles": "true"},
            )
        except (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError) as exc:
            raise EvaluatorRuntimeError("OPA readiness transport failed") from exc

        if response.status_code != 200:
            raise EvaluatorNotReadyError(
                "OPA is not ready with configured bundles activated"
            )


__all__ = ["OpaRegulatoryPolicyEvaluator"]

"""Reference (in-process) deterministic evaluator for scaffold / offline tests.

Not production OPA. Implements a minimal Uganda→South Africa coffee path so
unit and architecture tests can exercise the decision model without a live
OPA sidecar. Production path will compile BRIR → Rego and call OPA
(ADR-REG-0016, ADR-REG-0018).
"""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from baobab_regulations.domain.context.models import RegulatoryContext
from baobab_regulations.domain.decisions.models import (
    DecisionReason,
    RecommendedDisposition,
    RegulatoryDecision,
)
from baobab_regulations.domain.shared.enums import DecisionOutcome, EnforcementClass
from baobab_regulations.domain.shared.ids import RegulatoryId


class ReferenceEvaluator:
    """Deterministic offline evaluator for scaffold golden cases."""

    async def evaluate(
        self,
        *,
        context: RegulatoryContext,
        facts: dict[str, Any],
        rule_set_id: str,
        enforcement_class_ceiling: str | None = None,
    ) -> RegulatoryDecision:
        now = datetime.now(UTC)
        decision_id = RegulatoryId(str(uuid4()))
        assessment_id = RegulatoryId(str(uuid4()))

        has_phyto = bool(facts.get("phytosanitary_certificate_present"))
        has_origin_proof = bool(facts.get("origin_certificate_present"))
        hs = facts.get("hs_code") or (
            str(context.hs_classification) if context.hs_classification else None
        )

        reasons: list[DecisionReason] = []
        missing: list[str] = []

        if not hs:
            reasons.append(
                DecisionReason(
                    code="HS_CLASSIFICATION_MISSING",
                    message="No HS classification supplied for the goods.",
                    legal_basis_refs=["ADR-REG-0027§7"],
                )
            )
            missing.append("hs_classification")

        if not has_phyto:
            reasons.append(
                DecisionReason(
                    code="REQUIRED_PHYTOSANITARY_CERTIFICATE_MISSING",
                    message="Plant-health (SPS) import conditions require a valid phytosanitary certificate.",
                    legal_basis_refs=["ADR-REG-0027§SPS"],
                )
            )
            missing.append("phytosanitary_certificate")

        if context.origin_regime == "AfCFTA" and not has_origin_proof:
            reasons.append(
                DecisionReason(
                    code="ORIGIN_PROOF_MISSING_FOR_PREFERENCE",
                    message="Preferential origin claim under AfCFTA requires valid proof of origin.",
                    legal_basis_refs=["ADR-REG-0027§16"],
                )
            )
            missing.append("origin_certificate")

        if missing:
            outcome = DecisionOutcome.UNSATISFIED
            disposition = RecommendedDisposition(
                disposition="HOLD",
                rationale="One or more mandatory documentary requirements are unsatisfied.",
                missing_requirements=missing,
            )
            explanation = (
                "Shipment is not release-ready: "
                + ", ".join(missing)
                + ". Operational enforcement remains with the owning PEP (e.g. baobab-trade)."
            )
        else:
            outcome = DecisionOutcome.SATISFIED
            disposition = RecommendedDisposition(
                disposition="ALLOW",
                rationale="Mandatory documentary requirements for the reference profile are present.",
                missing_requirements=[],
            )
            explanation = "Reference evaluator: all checked requirements satisfied for this profile."
            reasons.append(
                DecisionReason(
                    code="REFERENCE_PROFILE_SATISFIED",
                    message="HS present; phytosanitary certificate present; origin proof present when claimed.",
                )
            )

        return RegulatoryDecision(
            decision_id=decision_id,
            assessment_id=assessment_id,
            outcome=outcome,
            enforcement_class=EnforcementClass.E1_ADVISORY,
            reasons=reasons,
            recommended_disposition=disposition,
            explanation=explanation,
            rule_set_fingerprint=rule_set_id,
            evaluated_at=now,
            legal_time=context.legal_time,
            knowledge_time=context.knowledge_time,
            provenance={
                "evaluator": "reference",
                "enforcement_class_ceiling": enforcement_class_ceiling,
            },
            replay_key=f"{decision_id}:{rule_set_id}",
        )

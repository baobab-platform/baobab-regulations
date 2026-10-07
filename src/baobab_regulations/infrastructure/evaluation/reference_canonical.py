"""Canonical adapter over the existing offline ReferenceEvaluator.

This is a differential/golden oracle only. Production traffic uses the OPA
adapter behind the same provider-neutral evaluator port.
"""

from baobab_regulations.application.ports.evaluator import (
    RegulatoryEvaluationInput,
    RegulatoryEvaluationResult,
)
from baobab_regulations.contracts.decision import (
    DecisionReason,
    PinnedCrossEngineReference,
    RecommendedDisposition,
)
from baobab_regulations.domain.context.models import (
    JurisdictionRole,
    JurisdictionRoleKind,
    PlatformContextRef,
    RegulatoryContext,
)
from baobab_regulations.domain.shared.ids import HSCode, JurisdictionCode, RegimeCode
from baobab_regulations.infrastructure.evaluation.reference import ReferenceEvaluator


class ReferenceEvaluatorCanonicalAdapter:
    """Translate the supported UG→ZA coffee canonical subset to the legacy oracle."""

    def __init__(self, reference: ReferenceEvaluator | None = None) -> None:
        self._reference = reference or ReferenceEvaluator()

    async def evaluate(
        self,
        evaluation: RegulatoryEvaluationInput,
    ) -> RegulatoryEvaluationResult:
        facts = {item.fact_code: item.value for item in evaluation.request.facts}

        origin = str(facts.get("ORIGIN_COUNTRY", "UG"))
        destination = str(facts.get("IMPORT_COUNTRY", "ZA"))
        hs_value = facts.get("HS_CODE")
        regime_value = facts.get("ORIGIN_REGIME")

        context = RegulatoryContext(
            platform=PlatformContextRef(tenant_id=evaluation.tenant_id),
            jurisdiction_roles=[
                JurisdictionRole(
                    role=JurisdictionRoleKind.ORIGIN,
                    jurisdiction=JurisdictionCode(origin),
                ),
                JurisdictionRole(
                    role=JurisdictionRoleKind.IMPORT_JURISDICTION,
                    jurisdiction=JurisdictionCode(destination),
                ),
            ],
            regulatory_regimes=(
                [RegimeCode(str(regime_value))]
                if regime_value is not None
                else []
            ),
            hs_classification=(
                HSCode(str(hs_value))
                if hs_value is not None
                else None
            ),
            origin_claimed_country=JurisdictionCode(origin),
            origin_regime=(
                RegimeCode(str(regime_value))
                if regime_value is not None
                else None
            ),
            legal_time=evaluation.request.legal_time,
            knowledge_time=evaluation.request.knowledge_time,
        )
        legacy_facts = {
            "hs_code": hs_value,
            "phytosanitary_certificate_present": bool(
                facts.get("PHYTOSANITARY_CERTIFICATE_PRESENT", False)
            ),
            "origin_certificate_present": bool(
                facts.get("ORIGIN_CERTIFICATE_PRESENT", False)
            ),
        }
        legacy = await self._reference.evaluate(
            context=context,
            facts=legacy_facts,
            rule_set_id=evaluation.rule_set.reference.object_id,
            enforcement_class_ceiling=evaluation.request.requested_enforcement_class_ceiling,
        )

        evidence = tuple(evaluation.request.evidence_references)
        reasons = tuple(
            DecisionReason(
                code=reason.code,
                message=reason.message,
                legal_basis_references=tuple(
                    PinnedCrossEngineReference(
                        owner_engine_id="baobab-regulations",
                        object_type="REGULATORY_PROVISION_VERSION",
                        object_id=self._safe_object_id(value),
                        reference_mode="IDENTITY_PINNED",
                        scope="platform",
                    )
                    for value in reason.legal_basis_refs
                ),
                rule_version_references=(),
                evidence_references=evidence,
            )
            for reason in legacy.reasons
        )
        disposition = None
        if legacy.recommended_disposition is not None:
            disposition = RecommendedDisposition(
                disposition_code=legacy.recommended_disposition.disposition,
                rationale=legacy.recommended_disposition.rationale,
                missing_requirement_references=[],
            )

        legal_basis = tuple(
            reference
            for reason in reasons
            for reference in reason.legal_basis_references
        )
        return RegulatoryEvaluationResult(
            outcome=legacy.outcome.value,
            enforcement_class=legacy.enforcement_class.value,
            reasons=reasons,
            legal_basis_references=legal_basis,
            evidence_references=evidence,
            recommended_disposition=disposition,
        )

    @staticmethod
    def _safe_object_id(value: str) -> str:
        digest = __import__("hashlib").sha256(value.encode("utf-8")).hexdigest()
        return f"legalbasis_{digest[:24]}"


__all__ = ["ReferenceEvaluatorCanonicalAdapter"]

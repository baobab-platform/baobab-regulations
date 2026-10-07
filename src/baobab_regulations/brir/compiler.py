"""Deterministic BRIR v1 subset -> Rego v1 compiler for R-CAP-09."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from baobab_regulations.brir.models import BrirRuleSet


@dataclass(frozen=True, slots=True)
class CompiledPolicyArtifact:
    rule_set_id: str
    rule_set_fingerprint: str
    compiler_id: str
    compiler_version: str
    target: str
    entrypoint: str
    source: str
    artifact_fingerprint: str


class BrirCompilationError(ValueError):
    """BRIR cannot be represented safely by this bounded compiler."""


class RegoV1Compiler:
    """Compile the governed requirement-rule subset into deterministic Rego."""

    compiler_id = "baobab-regulations-rego"
    compiler_version = "1"
    target = "rego/v1"
    entrypoint = "baobab/regulations/decision"

    def compile(self, rule_set: BrirRuleSet) -> CompiledPolicyArtifact:
        semantic_fingerprint = rule_set.fingerprint()
        rules = [
            {
                "rule_version_reference": item.rule_version_reference.model_dump(
                    mode="json"
                ),
                "legal_basis_reference": item.legal_basis_reference.model_dump(
                    mode="json"
                ),
                "when_all": [
                    predicate.model_dump(mode="json")
                    for predicate in item.when_all
                ],
                "requirement_fact_code": item.requirement_fact_code,
                "expected_value": item.expected_value,
                "failure_reason_code": item.failure_reason_code,
                "failure_message": item.failure_message,
            }
            for item in rule_set.rules
        ]

        source = self._render(
            rule_set=rule_set,
            semantic_fingerprint=semantic_fingerprint,
            rules_json=json.dumps(
                rules,
                sort_keys=True,
                separators=(",", ":"),
            ),
        )
        artifact_fingerprint = hashlib.sha256(source.encode("utf-8")).hexdigest()
        return CompiledPolicyArtifact(
            rule_set_id=rule_set.rule_set_id,
            rule_set_fingerprint=semantic_fingerprint,
            compiler_id=self.compiler_id,
            compiler_version=self.compiler_version,
            target=self.target,
            entrypoint=self.entrypoint,
            source=source,
            artifact_fingerprint=artifact_fingerprint,
        )

    @staticmethod
    def _render(
        *,
        rule_set: BrirRuleSet,
        semantic_fingerprint: str,
        rules_json: str,
    ) -> str:
        success_code = json.dumps(rule_set.success_reason_code)
        success_message = json.dumps(rule_set.success_message)
        allow_code = json.dumps(rule_set.allow_disposition_code)
        hold_code = json.dumps(rule_set.hold_disposition_code)
        enforcement_class = json.dumps(rule_set.enforcement_class)
        not_applicable_code = json.dumps(rule_set.not_applicable_reason_code)
        not_applicable_message = json.dumps(rule_set.not_applicable_message)
        fingerprint = json.dumps(semantic_fingerprint)
        rules_literal = rules_json

        return f"""package baobab.regulations

import rego.v1

expected_rule_set_fingerprint := {fingerprint}

rules := {rules_literal}

facts := {{fact.fact_code: fact.value | some fact in input.request.facts}}

predicate_matches(predicate) if {{
    predicate.operator == "EQ"
    facts[predicate.fact_code] == predicate.value
}}

predicate_matches(predicate) if {{
    predicate.operator == "EXISTS"
    predicate.fact_code in object.keys(facts)
}}

rule_applies(rule) if {{
    every predicate in rule.when_all {{
        predicate_matches(predicate)
    }}
}}

rule_satisfied(rule) if {{
    rule_applies(rule)
    object.get(facts, rule.requirement_fact_code, null) == rule.expected_value
}}

applicable_rules := [rule |
    some index
    rule := rules[index]
    rule_applies(rule)
]

failed_rules := [rule |
    some index
    rule := rules[index]
    rule_applies(rule)
    not rule_satisfied(rule)
]

failed_reasons := [reason |
    some index
    rule := failed_rules[index]
    reason := {{
        "code": rule.failure_reason_code,
        "message": rule.failure_message,
        "legal_basis_references": [rule.legal_basis_reference],
        "rule_version_references": [rule.rule_version_reference],
        "evidence_references": input.request.evidence_references,
    }}
]

all_legal_basis := [rule.legal_basis_reference |
    some index
    rule := applicable_rules[index]
]
all_rule_versions := [rule.rule_version_reference |
    some index
    rule := applicable_rules[index]
]

success_reason := {{
    "code": {success_code},
    "message": {success_message},
    "legal_basis_references": all_legal_basis,
    "rule_version_references": all_rule_versions,
    "evidence_references": input.request.evidence_references,
}}

not_applicable_reason := {{
    "code": {not_applicable_code},
    "message": {not_applicable_message},
    "legal_basis_references": [],
    "rule_version_references": [],
    "evidence_references": input.request.evidence_references,
}}

decision_reasons := [not_applicable_reason] if {{
    count(applicable_rules) == 0
}}

decision_reasons := [success_reason] if {{
    count(applicable_rules) > 0
    count(failed_rules) == 0
}}

decision_reasons := failed_reasons if {{
    count(failed_rules) > 0
}}

decision_outcome := "NOT_APPLICABLE" if {{
    count(applicable_rules) == 0
}}

decision_outcome := "SATISFIED" if {{
    count(applicable_rules) > 0
    count(failed_rules) == 0
}}

decision_outcome := "UNSATISFIED" if {{
    count(failed_rules) > 0
}}

recommended_disposition := null if {{
    count(applicable_rules) == 0
}}

recommended_disposition := {{
    "disposition_code": {allow_code},
    "rationale": "All executable requirements in the pinned BRIR rule set are satisfied.",
    "missing_requirement_references": [],
}} if {{
    count(applicable_rules) > 0
    count(failed_rules) == 0
}}

recommended_disposition := {{
    "disposition_code": {hold_code},
    "rationale": "One or more executable requirements in the pinned BRIR rule set are unsatisfied.",
    "missing_requirement_references": [],
}} if {{
    count(failed_rules) > 0
}}

decision := {{
    "input_fingerprint": input.input_fingerprint,
    "rule_set_fingerprint": expected_rule_set_fingerprint,
    "outcome": decision_outcome,
    "enforcement_class": {enforcement_class},
    "reasons": decision_reasons,
    "legal_basis_references": all_legal_basis,
    "evidence_references": input.request.evidence_references,
    "recommended_disposition": recommended_disposition,
}} if {{
    input.contract_major == 1
    input.rule_set.object_id == {json.dumps(rule_set.rule_set_id)}
    input.rule_set.fingerprint == expected_rule_set_fingerprint
    input.input_fingerprint != ""
}}
"""


__all__ = [
    "BrirCompilationError",
    "CompiledPolicyArtifact",
    "RegoV1Compiler",
]

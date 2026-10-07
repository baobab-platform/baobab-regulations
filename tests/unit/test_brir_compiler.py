"""R-CAP-09 bounded BRIR model and deterministic compiler tests."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirPredicate, BrirRuleSet

FIXTURE = Path("tests/fixtures/brir/r_cap_09_rule_set.json")


def _rule_set() -> BrirRuleSet:
    return BrirRuleSet.model_validate(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )


def test_brir_fingerprint_and_rego_artifact_are_deterministic() -> None:
    rule_set = _rule_set()
    compiler = RegoV1Compiler()

    first = compiler.compile(rule_set)
    second = compiler.compile(rule_set)

    assert first == second
    assert first.rule_set_fingerprint == rule_set.fingerprint()
    assert len(first.rule_set_fingerprint) == 64
    assert len(first.artifact_fingerprint) == 64
    assert first.compiler_id == "baobab-regulations-rego"
    assert first.compiler_version == "1"
    assert first.target == "rego/v1"
    assert first.entrypoint == "baobab/regulations/decision"


def test_compiled_policy_distinguishes_not_applicable() -> None:
    source = RegoV1Compiler().compile(_rule_set()).source

    assert 'decision_outcome := "NOT_APPLICABLE"' in source
    assert 'count(applicable_rules) == 0' in source
    assert 'recommended_disposition := null' in source


def test_exists_predicate_checks_presence_not_truthiness() -> None:
    source = RegoV1Compiler().compile(_rule_set()).source

    assert "predicate.fact_code in object.keys(facts)" in source
    assert 'object.get(facts, predicate.fact_code, false) != false' not in source


def test_exists_predicate_rejects_a_value() -> None:
    with pytest.raises(ValidationError, match="EXISTS predicates must omit value"):
        BrirPredicate(
            fact_code="SOME_FACT",
            operator="EXISTS",
            value=False,
        )


def test_eq_predicate_requires_a_value() -> None:
    with pytest.raises(ValidationError, match="EQ predicates require"):
        BrirPredicate(
            fact_code="SOME_FACT",
            operator="EQ",
            value=None,
        )


def test_raw_rego_cannot_be_smuggled_into_brir() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    document["rego"] = "allow := true"

    with pytest.raises(ValidationError):
        BrirRuleSet.model_validate(document)


def test_duplicate_rule_version_identity_is_rejected() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    document["rules"].append(document["rules"][0])

    with pytest.raises(ValidationError, match="rule_version_reference"):
        BrirRuleSet.model_validate(document)

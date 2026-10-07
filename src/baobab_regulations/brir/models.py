"""Bounded executable BRIR v1 subset for the first production rule profile.

This is intentionally smaller than the full ADR-REG-0016 language. Unsupported
semantics must remain non-executable until the BRIR model/compiler grows under
governance; raw target code is never accepted.
"""

from __future__ import annotations

import hashlib
import json
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from baobab_regulations.contracts.decision import (
    PinnedCrossEngineReference,
    RuleVersionReference,
)

Scalar = str | int | float | bool
FactCode = Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_.-]{1,127}$")]
ReasonCode = Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$")]


class BrirPredicate(BaseModel):
    """One deterministic applicability predicate in the bounded v1 subset."""

    model_config = ConfigDict(extra="forbid")

    fact_code: FactCode
    operator: Literal["EQ", "EXISTS"]
    value: Scalar | None = None

    @model_validator(mode="after")
    def validate_operator_value(self) -> BrirPredicate:
        if self.operator == "EQ" and self.value is None:
            raise ValueError("EQ predicates require a non-null scalar value")
        if self.operator == "EXISTS" and self.value is not None:
            raise ValueError("EXISTS predicates must omit value")
        return self


class BrirRequirementRule(BaseModel):
    """A deterministic requirement rule supported by the first compiler."""

    model_config = ConfigDict(extra="forbid")

    rule_version_reference: RuleVersionReference
    legal_basis_reference: PinnedCrossEngineReference
    when_all: list[BrirPredicate] = Field(default_factory=list, max_length=32)
    requirement_fact_code: FactCode
    expected_value: Scalar
    failure_reason_code: ReasonCode
    failure_message: Annotated[str, Field(min_length=1, max_length=1024)]

    @field_validator("when_all")
    @classmethod
    def unique_predicates(
        cls,
        value: list[BrirPredicate],
    ) -> list[BrirPredicate]:
        encoded = [item.model_dump_json() for item in value]
        if len(encoded) != len(set(encoded)):
            raise ValueError("BRIR applicability predicates must be unique")
        return value


class BrirRuleSet(BaseModel):
    """Canonical semantic input to the bounded R-CAP-09 Rego compiler."""

    model_config = ConfigDict(extra="forbid")

    brir_version: Literal["baobab.regulations.brir/v1"]
    rule_set_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=160,
            pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
        ),
    ]
    rules: Annotated[list[BrirRequirementRule], Field(min_length=1, max_length=256)]
    success_reason_code: ReasonCode = "REFERENCE_PROFILE_SATISFIED"
    success_message: Annotated[str, Field(min_length=1, max_length=1024)]
    allow_disposition_code: Annotated[
        str,
        Field(pattern=r"^[A-Z][A-Z0-9_]{1,63}$"),
    ] = "ALLOW"
    hold_disposition_code: Annotated[
        str,
        Field(pattern=r"^[A-Z][A-Z0-9_]{1,63}$"),
    ] = "HOLD"
    enforcement_class: Literal["E0", "E1", "E2", "E3", "E4"] = "E1"
    not_applicable_reason_code: ReasonCode = "NO_APPLICABLE_RULE"
    not_applicable_message: Annotated[str, Field(min_length=1, max_length=1024)] = (
        "No executable rule in the pinned BRIR rule set applies to the supplied facts."
    )

    @field_validator("rules")
    @classmethod
    def unique_rule_versions(
        cls,
        value: list[BrirRequirementRule],
    ) -> list[BrirRequirementRule]:
        references = [
            item.rule_version_reference.model_dump_json()
            for item in value
        ]
        if len(references) != len(set(references)):
            raise ValueError("BRIR rule_version_reference values must be unique")
        return value

    def canonical_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        )

    def fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


__all__ = [
    "BrirPredicate",
    "BrirRequirementRule",
    "BrirRuleSet",
]

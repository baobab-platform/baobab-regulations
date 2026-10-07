"""R-CAP-09 exact bitemporal rule-set authority tests."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from baobab_regulations.application.ports.rule_sets import (
    RuleSetConflictError,
    RuleSetIntegrityError,
)
from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet
from baobab_regulations.contracts.decision import RuleSetReference
from baobab_regulations.domain.rules.models import RuleSetRecord
from baobab_regulations.domain.shared.enums import AssuranceState
from baobab_regulations.infrastructure.persistence.memory import InMemoryRuleSetRepository
from baobab_regulations.infrastructure.rule_sets import RepositoryRuleSetAuthority

TENANT_ID = "tn_01k4m7x9q2v6c8r3d5f1h0j4"
NOW = datetime(2026, 10, 6, 10, tzinfo=UTC)
BRIR_FIXTURE = Path("tests/fixtures/brir/r_cap_09_rule_set.json")
BRIR = BrirRuleSet.model_validate(
    json.loads(BRIR_FIXTURE.read_text(encoding="utf-8"))
)
ARTIFACT = RegoV1Compiler().compile(BRIR)
FINGERPRINT = ARTIFACT.rule_set_fingerprint


async def _authority(
    *,
    assurance: AssuranceState = AssuranceState.VERIFIED,
    scope: str = "platform",
    tenant_id: str | None = None,
    fingerprint: str = FINGERPRINT,
) -> RepositoryRuleSetAuthority:
    repository = InMemoryRuleSetRepository()
    await repository.save(
        RuleSetRecord(
            rule_set_id="ruleset_ug_za_coffee_2026_10",
            corridor_profile="UG-ZA-COFFEE",
            assurance_state=assurance,
            fingerprint=fingerprint,
            legal_valid_from=NOW - timedelta(days=30),
            legal_valid_to=NOW + timedelta(days=30),
            knowledge_from=NOW - timedelta(days=10),
            knowledge_to=None,
            scope=scope,  # type: ignore[arg-type]
            tenant_id=tenant_id,
            brir_payload=BRIR.model_dump(mode="json"),
            compiler_id=ARTIFACT.compiler_id,
            compiler_version=ARTIFACT.compiler_version,
            compiled_target=ARTIFACT.target,
            compiled_entrypoint=ARTIFACT.entrypoint,
            compiled_artifact_fingerprint=ARTIFACT.artifact_fingerprint,
        )
    )
    return RepositoryRuleSetAuthority(repository)


def _reference(
    *,
    scope: str = "platform",
    tenant_id: str | None = None,
    versioned: bool = False,
) -> RuleSetReference:
    payload: dict[str, object] = {
        "owner_engine_id": "baobab-regulations",
        "object_type": "REGULATORY_RULE_SET",
        "object_id": "ruleset_ug_za_coffee_2026_10",
        "reference_mode": "VERSION_PINNED" if versioned else "IDENTITY_PINNED",
        "scope": scope,
    }
    if tenant_id is not None:
        payload["tenant_id"] = tenant_id
    if versioned:
        payload["object_version"] = {
            "kind": "CONTENT_HASH",
            "value": FINGERPRINT,
        }
    return RuleSetReference.model_validate(payload)


@pytest.mark.asyncio
async def test_resolves_verified_platform_rule_set_for_bitemporal_point() -> None:
    authority = await _authority()

    result = await authority.resolve_exact(
        reference=_reference(),
        legal_time=NOW,
        knowledge_time=NOW,
        requested_assurance="STANDARD",
        trusted_tenant_id=TENANT_ID,
    )

    assert result.fingerprint == FINGERPRINT
    assert result.assurance_state == "VERIFIED"
    assert result.entrypoint == ARTIFACT.entrypoint
    assert result.artifact_fingerprint == ARTIFACT.artifact_fingerprint


@pytest.mark.asyncio
async def test_version_pinned_content_hash_must_match() -> None:
    authority = await _authority()
    payload = _reference(versioned=True).model_dump(mode="json")
    payload["object_version"] = {
        "kind": "CONTENT_HASH",
        "value": "b" * 64,
    }
    reference = RuleSetReference.model_validate(payload)

    with pytest.raises(RuleSetConflictError, match="content fingerprint"):
        await authority.resolve_exact(
            reference=reference,
            legal_time=NOW,
            knowledge_time=NOW,
            requested_assurance="STANDARD",
            trusted_tenant_id=TENANT_ID,
        )


@pytest.mark.asyncio
async def test_high_assurance_requires_certified_rule_set() -> None:
    authority = await _authority(assurance=AssuranceState.VERIFIED)

    with pytest.raises(RuleSetConflictError, match="CERTIFIED"):
        await authority.resolve_exact(
            reference=_reference(),
            legal_time=NOW,
            knowledge_time=NOW,
            requested_assurance="HIGH_ASSURANCE",
            trusted_tenant_id=TENANT_ID,
        )


@pytest.mark.asyncio
async def test_out_of_legal_time_fails_closed() -> None:
    authority = await _authority()

    with pytest.raises(RuleSetConflictError, match="legal/knowledge time"):
        await authority.resolve_exact(
            reference=_reference(),
            legal_time=NOW + timedelta(days=60),
            knowledge_time=NOW,
            requested_assurance="STANDARD",
            trusted_tenant_id=TENANT_ID,
        )


@pytest.mark.asyncio
async def test_tenant_rule_set_requires_same_trusted_tenant() -> None:
    authority = await _authority(scope="tenant", tenant_id=TENANT_ID)

    result = await authority.resolve_exact(
        reference=_reference(scope="tenant", tenant_id=TENANT_ID),
        legal_time=NOW,
        knowledge_time=NOW,
        requested_assurance="STANDARD",
        trusted_tenant_id=TENANT_ID,
    )

    assert result.reference.tenant_id == TENANT_ID


@pytest.mark.asyncio
async def test_non_sha256_rule_set_fingerprint_is_integrity_failure() -> None:
    authority = await _authority(fingerprint="not-a-sha")

    with pytest.raises(RuleSetIntegrityError, match="SHA-256"):
        await authority.resolve_exact(
            reference=_reference(),
            legal_time=NOW,
            knowledge_time=NOW,
            requested_assurance="STANDARD",
            trusted_tenant_id=TENANT_ID,
        )

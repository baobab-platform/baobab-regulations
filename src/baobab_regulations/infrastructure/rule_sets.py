"""Production rule-set authority adapter over Regulations persistence."""

import re
from datetime import datetime

import asyncpg
from pydantic import ValidationError

from baobab_regulations.application.ports.evaluator import ResolvedRuleSet
from baobab_regulations.application.ports.repository import RuleSetRepositoryPort
from baobab_regulations.application.ports.rule_sets import (
    RuleSetAuthorityUnavailableError,
    RuleSetConflictError,
    RuleSetIntegrityError,
    RuleSetNotFoundError,
)
from baobab_regulations.brir.compiler import RegoV1Compiler
from baobab_regulations.brir.models import BrirRuleSet
from baobab_regulations.contracts.decision import RuleSetReference
from baobab_regulations.domain.shared.enums import AssuranceState

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class RepositoryRuleSetAuthority:
    """Resolve one exact, governed rule set and compiled execution binding."""

    def __init__(
        self,
        repository: RuleSetRepositoryPort,
        *,
        compiler: RegoV1Compiler | None = None,
    ) -> None:
        self._repository = repository
        self._compiler = compiler or RegoV1Compiler()

    async def resolve_exact(
        self,
        *,
        reference: RuleSetReference,
        legal_time: datetime,
        knowledge_time: datetime,
        requested_assurance: str,
        trusted_tenant_id: str,
    ) -> ResolvedRuleSet:
        try:
            record = await self._repository.get(
                reference.object_id,
                tenant_id=trusted_tenant_id if reference.scope == "tenant" else None,
            )
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise RuleSetAuthorityUnavailableError(
                "Regulations rule-set authority is unavailable"
            ) from exc

        if record is None:
            raise RuleSetNotFoundError("exact pinned rule set was not found")

        if not _SHA256.fullmatch(record.fingerprint):
            raise RuleSetIntegrityError("rule-set fingerprint is not canonical SHA-256")

        if reference.scope != record.scope:
            raise RuleSetConflictError("rule-set reference scope conflicts with governed record")
        if reference.scope == "tenant":
            if reference.tenant_id != trusted_tenant_id:
                raise RuleSetConflictError("rule-set reference tenant differs from trusted context")
            if record.tenant_id != trusted_tenant_id:
                raise RuleSetConflictError("governed rule set belongs to another tenant")
        elif record.tenant_id is not None:
            raise RuleSetIntegrityError("platform rule set unexpectedly carries tenant ownership")

        if reference.reference_mode == "VERSION_PINNED":
            version = reference.object_version
            if version is None:
                raise RuleSetIntegrityError("VERSION_PINNED rule set lost object_version")
            if version.kind != "CONTENT_HASH" or version.value != record.fingerprint:
                raise RuleSetConflictError(
                    "VERSION_PINNED rule set does not match the governed content fingerprint"
                )

        if not record.is_valid_for(
            legal_time=legal_time,
            knowledge_time=knowledge_time,
        ):
            raise RuleSetConflictError(
                "rule set is not valid for the requested legal/knowledge time"
            )

        if record.brir_payload is None:
            raise RuleSetIntegrityError(
                "production rule set has no governed BRIR payload"
            )
        try:
            brir = BrirRuleSet.model_validate(record.brir_payload)
        except ValidationError as exc:
            raise RuleSetIntegrityError("persisted BRIR payload is invalid") from exc

        if brir.rule_set_id != record.rule_set_id:
            raise RuleSetIntegrityError(
                "persisted BRIR rule_set_id does not match rule-set record"
            )
        if brir.fingerprint() != record.fingerprint:
            raise RuleSetIntegrityError(
                "persisted BRIR semantic fingerprint does not match rule-set record"
            )

        compiled = self._compiler.compile(brir)
        expected_compiled = {
            "compiler_id": record.compiler_id,
            "compiler_version": record.compiler_version,
            "target": record.compiled_target,
            "entrypoint": record.compiled_entrypoint,
            "artifact_fingerprint": record.compiled_artifact_fingerprint,
        }
        actual_compiled = {
            "compiler_id": compiled.compiler_id,
            "compiler_version": compiled.compiler_version,
            "target": compiled.target,
            "entrypoint": compiled.entrypoint,
            "artifact_fingerprint": compiled.artifact_fingerprint,
        }
        if any(value is None for value in expected_compiled.values()):
            raise RuleSetIntegrityError(
                "production rule set lacks complete compiled policy metadata"
            )
        if expected_compiled != actual_compiled:
            raise RuleSetIntegrityError(
                "compiled policy artifact does not match governed rule-set metadata"
            )

        if requested_assurance == "HIGH_ASSURANCE":
            if record.assurance_state is not AssuranceState.CERTIFIED:
                raise RuleSetConflictError(
                    "HIGH_ASSURANCE evaluation requires a CERTIFIED rule set"
                )
        elif record.assurance_state not in {
            AssuranceState.VERIFIED,
            AssuranceState.CERTIFIED,
        }:
            raise RuleSetConflictError("rule set is not verified for production evaluation")

        return ResolvedRuleSet(
            reference=reference,
            fingerprint=record.fingerprint,
            assurance_state=record.assurance_state.value,
            compiler_id=compiled.compiler_id,
            compiler_version=compiled.compiler_version,
            target=compiled.target,
            entrypoint=compiled.entrypoint,
            artifact_fingerprint=compiled.artifact_fingerprint,
        )


__all__ = ["RepositoryRuleSetAuthority"]

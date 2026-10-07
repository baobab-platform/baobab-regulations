"""Durable Regulations-owned RTD-06 requirement projections (R-CAP-10).

The read adapter can run as a SELECT-only, non-BYPASSRLS workload. The
append-only writer must be injected solely into a governed source-review /
promotion process, never into the canonical capability request handler.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import asyncpg
from pydantic import ValidationError

from baobab_regulations.application.ports.requirements import (
    RequirementAuthorityIntegrityError,
    RequirementAuthorityUnavailableError,
    RequirementLookup,
    RequirementLookupStatus,
)
from baobab_regulations.contracts.rtd06 import (
    RegulatoryDocumentRequirementProjection,
    RegulatoryRequirementReference,
)


def _canonical(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _fingerprint(value: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _row_projection(row: Any, reference: RegulatoryRequirementReference) -> RegulatoryDocumentRequirementProjection:
    try:
        payload = row["requirement_payload"]
        if isinstance(payload, (str, bytes)):
            payload = json.loads(payload)
        if not isinstance(payload, dict):
            raise TypeError("requirement_payload must be an object")
        projection = RegulatoryDocumentRequirementProjection.model_validate(payload)
        if _fingerprint(projection.model_dump(mode="json")) != str(row["projection_fingerprint"]):
            raise ValueError("projection fingerprint differs from stored content")
        if _fingerprint(projection.requirement_reference.model_dump(mode="json")) != str(row["reference_fingerprint"]):
            raise ValueError("reference fingerprint differs from stored content")
        if projection.requirement_reference != reference:
            raise ValueError("stored pinned requirement reference differs from requested reference")
        stored_reference = projection.requirement_reference
        if (
            row["object_type"] != stored_reference.object_type
            or row["object_id"] != stored_reference.object_id
            or row["scope"] != stored_reference.scope
            or row["tenant_id"] != stored_reference.tenant_id
            or row["reference_mode"] != stored_reference.reference_mode
            or row["version_kind"] != (
                stored_reference.object_version.kind
                if stored_reference.object_version is not None else None
            )
            or row["version_value"] != (
                stored_reference.object_version.value
                if stored_reference.object_version is not None else None
            )
        ):
            raise ValueError("stored requirement identity columns disagree with payload")
    except (TypeError, ValueError, ValidationError, KeyError) as exc:
        raise RequirementAuthorityIntegrityError(
            "persisted Regulations requirement has inconsistent canonical content"
        ) from exc
    return projection


class PostgresRequirementRepository:
    """Resolve historical pins with RLS and NOT_FOUND versus CONFLICT semantics."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def resolve_exact(
        self,
        reference: RegulatoryRequirementReference,
    ) -> RequirementLookup:
        ref = reference.model_dump(mode="json")
        tenant_id = reference.tenant_id
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                if tenant_id is not None:
                    await conn.execute(
                        "SELECT set_config('baobab.tenant_id', $1, true)",
                        tenant_id,
                    )
                exact = await conn.fetchrow(
                    """
                    SELECT *
                    FROM regulatory_requirement_projections
                    WHERE reference_fingerprint = $1
                      AND object_type = $2
                      AND object_id = $3
                      AND scope = $4
                      AND tenant_id IS NOT DISTINCT FROM $5::text
                    """,
                    _fingerprint(ref),
                    reference.object_type,
                    reference.object_id,
                    reference.scope,
                    tenant_id,
                )
                if exact is not None:
                    return RequirementLookup(
                        status=RequirementLookupStatus.FOUND,
                        requirement=_row_projection(exact, reference),
                    )
                conflict = await conn.fetchval(
                    """
                    SELECT 1
                    FROM regulatory_requirement_projections
                    WHERE object_type = $1
                      AND object_id = $2
                      AND scope = $3
                      AND tenant_id IS NOT DISTINCT FROM $4::text
                    LIMIT 1
                    """,
                    reference.object_type,
                    reference.object_id,
                    reference.scope,
                    tenant_id,
                )
        except RequirementAuthorityIntegrityError:
            raise
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise RequirementAuthorityUnavailableError(
                "governed Regulations requirement repository is unavailable"
            ) from exc

        return RequirementLookup(
            status=(
                RequirementLookupStatus.CONFLICT
                if conflict is not None else RequirementLookupStatus.NOT_FOUND
            )
        )


class GovernedRequirementProjectionWriter:
    """Append reviewed projections without superseding historical content.

    An ingestion/governance subsystem provides authority and audit evidence.
    This writer does not promote unverified source text into law.
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def append_reviewed(
        self,
        projection: RegulatoryDocumentRequirementProjection,
    ) -> None:
        reference = projection.requirement_reference
        ref = reference.model_dump(mode="json")
        document = projection.model_dump(mode="json")
        version = reference.object_version
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                if reference.tenant_id is not None:
                    await conn.execute(
                        "SELECT set_config('baobab.tenant_id', $1, true)",
                        reference.tenant_id,
                    )
                row = await conn.fetchrow(
                    """
                    INSERT INTO regulatory_requirement_projections (
                        reference_fingerprint, projection_fingerprint,
                        object_type, object_id, scope, tenant_id,
                        reference_mode, version_kind, version_value,
                        requirement_payload
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb
                    )
                    ON CONFLICT (reference_fingerprint) DO NOTHING
                    RETURNING reference_fingerprint
                    """,
                    _fingerprint(ref),
                    _fingerprint(document),
                    reference.object_type,
                    reference.object_id,
                    reference.scope,
                    reference.tenant_id,
                    reference.reference_mode,
                    version.kind if version is not None else None,
                    version.value if version is not None else None,
                    _canonical(document),
                )
                if row is not None:
                    return
                prior = await conn.fetchrow(
                    """
                    SELECT *
                    FROM regulatory_requirement_projections
                    WHERE reference_fingerprint = $1
                    """,
                    _fingerprint(ref),
                )
                if prior is None:
                    raise RequirementAuthorityIntegrityError(
                        "governed duplicate pin is not visible to the writer"
                    )
                _row_projection(prior, reference)
                if str(prior["projection_fingerprint"]) != _fingerprint(document):
                    raise RequirementAuthorityIntegrityError(
                        "attempt to replace immutable pinned requirement content"
                    )
        except RequirementAuthorityIntegrityError:
            raise
        except (asyncpg.PostgresError, asyncpg.InterfaceError, OSError) as exc:
            raise RequirementAuthorityUnavailableError(
                "governed requirement append authority is unavailable"
            ) from exc


__all__ = ["GovernedRequirementProjectionWriter", "PostgresRequirementRepository"]

"""Bounded write-once quarantine for synthetic tests only; not persistent storage."""

import hashlib
from collections.abc import AsyncIterator
from uuid import UUID

from baobab_regulations.domain.ingestion.models import StoredEvidence


class QuarantineLimitExceeded(ValueError):
    """Stream exceeded its registered maximum size."""


class InMemoryQuarantine:
    """Development-only; production requires private immutable object storage."""

    def __init__(self) -> None:
        self._objects: dict[str, bytes] = {}

    async def store(
        self, *, artefact_id: UUID, chunks: AsyncIterator[bytes], max_bytes: int
    ) -> StoredEvidence:
        if not 1 <= max_bytes <= 33554432:
            raise ValueError("invalid acquisition size limit")
        key = str(artefact_id)
        if key in self._objects:
            raise ValueError("artefact already exists (write-once)")
        digest = hashlib.sha256()
        output = bytearray()
        prefix = bytearray()
        async for chunk in chunks:
            if not isinstance(chunk, bytes):
                raise TypeError("quarantine requires raw bytes")
            if len(output) + len(chunk) > max_bytes:
                raise QuarantineLimitExceeded("hard streaming size limit exceeded")
            digest.update(chunk)
            if len(prefix) < 512:
                prefix.extend(chunk[: 512 - len(prefix)])
            output.extend(chunk)
        if not output:
            raise ValueError("empty response cannot become a source artefact")
        self._objects[key] = bytes(output)
        return StoredEvidence(
            storage_ref="memory-quarantine:" + key,
            content_hash=digest.hexdigest(), size_bytes=len(output),
            prefix=bytes(prefix)
        )

    async def verify(self, *, artefact_id: UUID, expected_sha256: str) -> bool:
        current = self._objects.get(str(artefact_id))
        return current is not None and hashlib.sha256(current).hexdigest() == expected_sha256

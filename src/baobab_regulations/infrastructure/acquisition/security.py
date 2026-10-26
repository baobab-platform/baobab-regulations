"""Conservative content signature gate, not a malware scanner.

Production callers must compose this *and* an independently qualified malware
scanner through SourceSecurityPort before any artefact can be processable.
"""

from baobab_regulations.domain.ingestion.models import (
    SecurityAssessment,
    SourceEvidenceRecord,
)

_MAGIC_ARCHIVES = (b"PK\x03\x04", b"PK\x05\x06", b"\x1f\x8b", b"7z\xbc\xaf", b"Rar!")


def signature_matches(media: str, prefix: bytes) -> bool:
    """Only narrow deterministic hints; HTML/XML/JSON are never parsed here."""
    if not prefix or prefix.startswith(_MAGIC_ARCHIVES):
        return False
    if media == "application/pdf":
        return prefix.startswith(b"%PDF-")
    if media == "application/json":
        return prefix.lstrip().startswith((b"{", b"["))
    if media in ("application/xml", "text/xml"):
        return prefix.lstrip().startswith(b"<?xml")
    if media == "text/html":
        return prefix.lstrip().lower().startswith((b"<!doctype html", b"<html"))
    if media == "text/plain":
        return b"\x00" not in prefix
    return False


class QuarantineOnlySecurity:
    """Safe default: detects mismatches; deliberately never approves processing."""

    async def assess(
        self, *, artefact: SourceEvidenceRecord, signature: bytes
    ) -> SecurityAssessment:
        matches = signature_matches(artefact.declared_media_type, signature)
        return SecurityAssessment(
            permitted=False,
            scanner_ref="reg-local-signature-only",
            scanner_version="1",
            evidence_ref="local-format:" + str(artefact.artefact_id),
            reason_code="AWAITING_QUALIFIED_MALWARE_SCAN" if matches else "FORMAT_REJECTED",
        )

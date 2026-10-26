"""No actual external publisher or network access in REG-INGEST-02 CI."""

from dataclasses import replace

import pytest

from baobab_regulations.domain.ingestion.models import RegisteredEndpoint
from baobab_regulations.infrastructure.acquisition.https import (
    PinnedHttpsSourceFetcher,
    UnsafeDestinationError,
    safe_http_value,
    validate_endpoint,
    validated_addresses,
)


def endpoint():
    return RegisteredEndpoint(
        source_id="reg_official_1", endpoint_ref="official_pdf",
        uri="https://gazette.example.org/regulation.pdf",
        allowed_hosts=frozenset({"gazette.example.org"}),
        permitted_media_types=frozenset({"application/pdf"}),
        max_bytes=1024, adapter_id="pinned-https", adapter_version="1",
        approved=True,
    )


@pytest.mark.parametrize("uri", [
    "http://gazette.example.org/act.pdf",
    "https://127.0.0.1/act.pdf",
    "https://localhost/act.pdf",
    "https://169.254.169.254/metadata",
    "https://gazette.example.org:8443/act.pdf",
    "https://user:pass@gazette.example.org/act.pdf",
    "https://gazette.example.org/act.pdf?token=secret",
    "https://gazette.example.org/act.pdf#fragment",
    "https://another.example.org/act.pdf",
    "https://gazette.example.org\\@127.0.0.1/act.pdf",
])
def test_rejects_unsafe_registry_destinations(uri):
    with pytest.raises(UnsafeDestinationError):
        validate_endpoint(replace(endpoint(), uri=uri))


@pytest.mark.parametrize("answers", [
    ("127.0.0.1",),
    ("10.0.0.1",),
    ("172.16.0.10",),
    ("192.168.1.1",),
    ("169.254.169.254",),
    ("::1",),
    ("fc00::1",),
    ("8.8.8.8", "127.0.0.1"),
    (),
    ("garbage",),
])
def test_disallows_local_or_mixed_dns_addresses(answers):
    with pytest.raises(UnsafeDestinationError):
        validated_addresses(answers)


def test_public_dns_ip_can_be_pinned_and_metadata_never_copies_secrets():
    assert validated_addresses(("8.8.8.8",)) == ("8.8.8.8",)
    assert safe_http_value('"etag"') == '"etag"'
    assert safe_http_value("secret\r\nset-cookie: x") is None
    assert safe_http_value("x" * 300) is None


@pytest.mark.asyncio
async def test_private_dns_answer_denied_without_constructing_http_client():
    calls = 0

    async def resolver(host):
        nonlocal calls
        calls += 1
        return ("169.254.169.254",)

    fetcher = PinnedHttpsSourceFetcher(resolver=resolver)
    with pytest.raises(UnsafeDestinationError, match="internal"):
        await fetcher.fetch(endpoint())
    assert calls == 1

"""HTTPS-only transport with DNS/IP pinning and redirect denial.

The remote peer is untrusted. Every DNS answer must be globally routable,
and the actual TCP connection is made to the validated numeric address.
The original registered hostname is retained for HTTP Host, SNI and TLS
certificate verification (httpcore sni_hostname request extension).
No proxies, cookies, credentials, caller URLs or automatic redirects.
"""

import asyncio
import ipaddress
import re
import socket
from collections.abc import AsyncIterator, Callable, Coroutine
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import httpx

from baobab_regulations.domain.ingestion.models import FetchedSource, RegisteredEndpoint


class UnsafeDestinationError(ValueError):
    """Rejected external destination or untrusted response."""


async def system_resolver(host: str) -> tuple[str, ...]:
    result = await asyncio.get_running_loop().getaddrinfo(
        host, 443, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
    )
    return tuple(item[4][0] for item in result)


Resolver = Callable[[str], Coroutine[Any, Any, tuple[str, ...]]]
_HOSTNAME = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?$")
_MEDIA = re.compile(r"^[a-z0-9!#$&^_.+-]+/[a-z0-9!#$&^_.+-]+$")


def validate_endpoint(endpoint: RegisteredEndpoint) -> tuple[str, str, str]:
    """Validate even registry-controlled values; registration is not sanitization."""
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in endpoint.uri):
        raise UnsafeDestinationError("control characters in endpoint")
    parts = urlsplit(endpoint.uri)
    host = (parts.hostname or "").lower()
    if (
        parts.scheme != "https" or not host or parts.port not in (None, 443)
        or parts.username is not None or parts.password is not None
        or parts.query or parts.fragment or "\\" in endpoint.uri
        or _HOSTNAME.fullmatch(host) is None
        or host not in endpoint.allowed_hosts or ".." in host
        or host.endswith(".local") or host.endswith(".internal")
        or host == "localhost"
    ):
        raise UnsafeDestinationError("destination violates registered HTTPS host policy")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise UnsafeDestinationError("IP-literal destinations are not permitted")
    return host, parts.path or "/", parts.scheme


def validated_addresses(addresses: tuple[str, ...]) -> tuple[str, ...]:
    if not addresses:
        raise UnsafeDestinationError("DNS returned no destinations")
    result: list[str] = []
    for item in addresses:
        try:
            ip = ipaddress.ip_address(item)
        except ValueError as exc:
            raise UnsafeDestinationError("DNS result is not an IP address") from exc
        if not ip.is_global:
            raise UnsafeDestinationError("DNS returned an internal or non-global address")
        result.append(ip.compressed)
    return tuple(result)


def safe_http_value(value: str | None) -> str | None:
    if value is None:
        return None
    if len(value) > 256 or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return None
    return value


class PinnedHttpsSourceFetcher:
    """One-shot GET; no proxy, redirect, cookie jar or unpinned DNS connection.

    A synthetic resolver may be injected for deterministic offline security tests.
    Egress network policy remains mandatory defence-in-depth in protected runtimes.
    """

    def __init__(self, resolver: Resolver = system_resolver) -> None:
        self._resolver = resolver

    async def fetch(self, endpoint: RegisteredEndpoint) -> FetchedSource:
        host, path, scheme = validate_endpoint(endpoint)
        addresses = validated_addresses(await self._resolver(host))
        selected = addresses[0]
        address = f"[{selected}]" if ":" in selected else selected
        # Numeric peer ensures DNS cannot be silently re-resolved by the client.
        pinned = urlunsplit((scheme, address, path, "", ""))
        client = httpx.AsyncClient(
            timeout=httpx.Timeout(8.0, connect=4.0),
            trust_env=False,
            follow_redirects=False,
            http2=False,
        )
        try:
            request = client.build_request(
                "GET",
                pinned,
                headers={"Host": host, "Accept-Encoding": "identity"},
                extensions={"sni_hostname": host},
            )
            response = await client.send(request, stream=True)
            if response.status_code != 200 or response.is_redirect:
                await response.aclose()
                raise UnsafeDestinationError("unexpected HTTP status or redirect")
            if response.headers.get("content-encoding", "identity").lower() != "identity":
                await response.aclose()
                raise UnsafeDestinationError("content encoding is not identity")
            media = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if _MEDIA.fullmatch(media) is None:
                await response.aclose()
                raise UnsafeDestinationError("unrecognised response media type")
            length = response.headers.get("content-length")
            if length is not None:
                try:
                    parsed_length = int(length)
                except ValueError as exc:
                    await response.aclose()
                    raise UnsafeDestinationError("invalid Content-Length") from exc
                if parsed_length < 0 or parsed_length > endpoint.max_bytes:
                    await response.aclose()
                    raise UnsafeDestinationError("response exceeds maximum bytes")
            else:
                parsed_length = None
        except BaseException:
            await client.aclose()
            raise

        async def body() -> AsyncIterator[bytes]:
            try:
                async with asyncio.timeout(25):
                    async for chunk in response.aiter_raw(chunk_size=65536):
                        yield chunk
            finally:
                await response.aclose()
                await client.aclose()

        return FetchedSource(
            body=body(), media_type=media, content_length=parsed_length,
            etag=safe_http_value(response.headers.get("etag")),
            last_modified=safe_http_value(response.headers.get("last-modified"))
        )

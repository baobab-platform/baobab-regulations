"""Enforce that domain does not import infrastructure or FastAPI."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2] / "src" / "baobab_regulations"
DOMAIN = ROOT / "domain"

FORBIDDEN_IN_DOMAIN = (
    "baobab_regulations.infrastructure",
    "baobab_regulations.api",
    "fastapi",
    "asyncpg",
    "opentelemetry",
)


@pytest.mark.architecture
def test_domain_has_no_forbidden_imports() -> None:
    violations: list[str] = []
    for path in DOMAIN.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in FORBIDDEN_IN_DOMAIN:
            if needle in text:
                violations.append(f"{path.relative_to(ROOT)}: imports/mentions {needle}")
    assert not violations, "Domain boundary violations:\n" + "\n".join(violations)

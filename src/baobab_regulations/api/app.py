"""FastAPI application factory."""

from fastapi import FastAPI

from baobab_regulations import __version__
from baobab_regulations.configuration.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Baobab Regulations",
        version=__version__,
        description=(
            "Headless regulatory context and deterministic decision engine. "
            "Policy Decision Point only — operational enforcement stays with domain PEPs."
        ),
    )

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name, "version": __version__}

    @app.get("/readyz")
    async def readyz() -> dict[str, str]:
        # Scaffold: no hard dependency on Postgres/OPA yet for readiness.
        return {"status": "ready", "service": settings.app_name}

    return app

"""HTTP health endpoints."""

from fastapi.testclient import TestClient

from baobab_regulations.api.app import create_app


def test_healthz() -> None:
    client = TestClient(create_app())
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "baobab-regulations"


def test_readyz() -> None:
    client = TestClient(create_app())
    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"

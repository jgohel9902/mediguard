"""Tests for the /health endpoint."""

from fastapi.testclient import TestClient

from app import __version__
from app.main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """The /health endpoint must respond with HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok() -> None:
    """The /health endpoint must return status 'ok' in the response body."""
    response = client.get("/health")
    payload = response.json()
    assert payload["status"] == "ok"


def test_health_returns_version() -> None:
    """The /health endpoint must include the application version."""
    response = client.get("/health")
    payload = response.json()
    assert payload["version"] == __version__

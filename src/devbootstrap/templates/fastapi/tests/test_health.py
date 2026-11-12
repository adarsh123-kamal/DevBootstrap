"""Tests for the FastAPI service endpoints and initialization."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "__SERVICE_NAME__", "status": "running"}


def test_application_initialization() -> None:
    assert app.title == "__SERVICE_NAME__"
    assert "/health" in app.openapi()["paths"]

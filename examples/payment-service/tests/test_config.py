"""Tests for environment-backed configuration."""

from app.core.config import get_settings


def test_configuration_uses_safe_defaults(monkeypatch) -> None:
    for key in ("APP_NAME", "ENVIRONMENT", "PORT", "DEBUG"):
        monkeypatch.delenv(key, raising=False)

    settings = get_settings()

    assert settings.app_name == "payment-service"
    assert settings.environment == "development"
    assert settings.port == 8000
    assert settings.debug is False


def test_configuration_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "test-api")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("PORT", "9010")
    monkeypatch.setenv("DEBUG", "yes")

    settings = get_settings()

    assert settings.app_name == "test-api"
    assert settings.environment == "testing"
    assert settings.port == 9010
    assert settings.debug is True

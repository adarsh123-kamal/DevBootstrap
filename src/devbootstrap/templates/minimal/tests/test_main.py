"""Tests for the minimal service."""

from app.main import health_check
from app.core.config import get_settings


def test_health_check() -> None:
    assert health_check() == {"status": "healthy"}


def test_application_initialization() -> None:
    assert get_settings().app_name

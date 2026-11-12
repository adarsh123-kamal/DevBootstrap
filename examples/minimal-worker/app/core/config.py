"""Environment-backed application settings."""

from dataclasses import dataclass
import os


def _read_bool(value: str) -> bool:
    """Parse common environment-variable representations of true."""
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Runtime settings with safe local-development defaults."""

    app_name: str
    environment: str
    port: int
    debug: bool


def get_settings() -> Settings:
    """Load settings from the process environment."""
    return Settings(
        app_name=os.getenv("APP_NAME", "minimal-worker"),
        environment=os.getenv("ENVIRONMENT", "development"),
        port=int(os.getenv("PORT", "8000")),
        debug=_read_bool(os.getenv("DEBUG", "false")),
    )

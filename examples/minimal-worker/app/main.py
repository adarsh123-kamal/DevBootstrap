"""Minimal service entry point."""

from app.core.config import get_settings
from app.core.logging_config import configure_logging


def health_check() -> dict[str, str]:
    """Return a simple process health status."""
    return {"status": "healthy"}


def main() -> None:
    """Start the minimal service and report its configured identity."""
    settings = get_settings()
    configure_logging()
    print(f"{settings.app_name} is ready on port {settings.port}")


if __name__ == "__main__":
    main()

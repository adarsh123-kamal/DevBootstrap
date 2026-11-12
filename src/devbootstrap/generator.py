"""Generate service projects from the templates bundled with DevBootstrap."""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

from devbootstrap.errors import (
    DestinationExistsError,
    InvalidServiceNameError,
    TemplateNotFoundError,
)

TEMPLATES: dict[str, str] = {
    "fastapi": "FastAPI backend service with a health endpoint.",
    "minimal": "Dependency-free Python service with a health check.",
}
_SERVICE_NAME_PATTERN = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")


def validate_service_name(service_name: str) -> None:
    """Raise an explicit error unless a name is safe for a project directory."""
    if len(service_name) > 50 or not _SERVICE_NAME_PATTERN.fullmatch(service_name):
        raise InvalidServiceNameError(
            "Service names must be 1-50 lowercase letters/digits, start with a "
            "letter, and use single hyphens between segments."
        )


def list_templates() -> dict[str, str]:
    """Return the names and descriptions of bundled templates."""
    return TEMPLATES.copy()


def create_project(
    service_name: str,
    output_dir: Path | str = Path.cwd(),
    template: str = "fastapi",
) -> Path:
    """Create a new project directory and return its absolute path."""
    validate_service_name(service_name)
    if template not in TEMPLATES:
        raise TemplateNotFoundError(
            f"Template '{template}' was not found. Available templates: "
            f"{', '.join(TEMPLATES)}."
        )

    parent = Path(output_dir).expanduser().resolve()
    destination = parent / service_name
    if destination.exists():
        raise DestinationExistsError(
            f"Destination already exists: {destination}"
        )

    template_dir = Path(__file__).parent / "templates" / template
    if not template_dir.is_dir():
        raise TemplateNotFoundError(f"Bundled template files are missing: {template}")

    staging: Path | None = None
    try:
        parent.mkdir(parents=True, exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(prefix=f".{service_name}-", dir=parent)
        )
        shutil.copytree(
            template_dir,
            staging,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]"),
        )
        for file_path in staging.rglob("*"):
            if file_path.is_file():
                content = file_path.read_text(encoding="utf-8")
                file_path.write_text(
                    content.replace("__SERVICE_NAME__", service_name),
                    encoding="utf-8",
                )
        staging.rename(destination)
    except OSError as exc:
        if staging is not None and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise OSError(f"Could not create project at '{destination}': {exc}") from exc

    return destination

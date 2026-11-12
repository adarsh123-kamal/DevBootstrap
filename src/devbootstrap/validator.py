"""Validate the structure and essential files of generated service projects."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from devbootstrap.errors import ProjectPathError


@dataclass(frozen=True)
class ValidationCheck:
    """One named project validation result."""

    name: str
    passed: bool
    detail: str


def validate_project(project_path: Path | str) -> list[ValidationCheck]:
    """Return all required checks for a project path without modifying it."""
    root = Path(project_path).expanduser()
    if not root.exists():
        raise ProjectPathError(f"Project path does not exist: {root}")
    if not root.is_dir():
        raise ProjectPathError(f"Project path is not a directory: {root}")

    requirements = root / "requirements.txt"
    requirements_text = (
        _read_text(requirements) if requirements.is_file() else ""
    )
    main_path = root / "app" / "main.py"
    main_source = _read_text(main_path) if main_path.is_file() else ""
    is_fastapi = "fastapi" in requirements_text.lower() or "FastAPI" in main_source
    checks = [
        _directory_check(root, "app"),
        _directory_check(root, "tests"),
        _file_check(root, "requirements.txt", non_empty=True),
        _file_check(root, "README.md", non_empty=True),
        _file_check(root, ".env.example"),
        _file_check(root, ".gitignore"),
        _file_check(root, "Dockerfile", non_empty=True),
        _file_check(root, "pyproject.toml", non_empty=True),
        _file_check(root, "app/__init__.py"),
        _file_check(root, "app/main.py", non_empty=True),
        _file_check(root, "app/core/config.py"),
        _file_check(root, "app/core/logging_config.py"),
    ]

    if is_fastapi:
        health_path = root / "app" / "routes" / "health.py"
        health_source = (
            _read_text(health_path) if health_path.is_file() else ""
        )
        has_fastapi_dependency = "fastapi" in requirements_text.lower()
        checks.append(
            ValidationCheck(
                "FastAPI dependency",
                has_fastapi_dependency,
                "requirements.txt includes FastAPI"
                if has_fastapi_dependency
                else "requirements.txt must include FastAPI",
            )
        )
        checks.extend(
            [
                _file_check(root, "app/routes/__init__.py"),
                ValidationCheck(
                    "FastAPI application entry point",
                    "FastAPI" in main_source and "app =" in main_source,
                    "app/main.py defines a FastAPI application"
                    if "FastAPI" in main_source and "app =" in main_source
                    else "app/main.py must define a FastAPI application",
                ),
                ValidationCheck(
                    "Health route",
                    health_path.is_file() and "/health" in health_source,
                    "app/routes/health.py defines the health route"
                    if health_path.is_file() and "/health" in health_source
                    else "app/routes/health.py must define a /health route",
                ),
            ]
        )
    else:
        checks.append(
            ValidationCheck(
                "Health check",
                "health_check" in main_source,
                "app/main.py defines health_check"
                if "health_check" in main_source
                else "app/main.py must define health_check",
            )
        )

    return checks


def _directory_check(root: Path, relative_path: str) -> ValidationCheck:
    passed = (root / relative_path).is_dir()
    return ValidationCheck(
        f"Directory: {relative_path}",
        passed,
        f"{relative_path} exists" if passed else f"Missing directory: {relative_path}",
    )


def _file_check(
    root: Path, relative_path: str, *, non_empty: bool = False
) -> ValidationCheck:
    path = root / relative_path
    passed = path.is_file() and (not non_empty or path.stat().st_size > 0)
    detail = (
        f"{relative_path} exists"
        if passed
        else f"Missing or empty file: {relative_path}"
    )
    return ValidationCheck(f"File: {relative_path}", passed, detail)


def _read_text(path: Path) -> str:
    """Read a project text file and report invalid or inaccessible files clearly."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ProjectPathError(f"Unable to read project file '{path}': {exc}") from exc

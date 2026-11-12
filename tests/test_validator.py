"""Tests for project structure validation."""

from pathlib import Path

import pytest

from devbootstrap.errors import ProjectPathError
from devbootstrap.generator import create_project
from devbootstrap.validator import validate_project


@pytest.mark.parametrize("template", ["fastapi", "minimal"])
def test_generated_projects_pass_validation(tmp_path: Path, template: str) -> None:
    project = create_project("test-service", tmp_path, template)

    checks = validate_project(project)

    assert checks
    assert all(check.passed for check in checks), [
        check for check in checks if not check.passed
    ]


def test_reports_missing_health_route(tmp_path: Path) -> None:
    project = create_project("broken-service", tmp_path)
    (project / "app" / "routes" / "health.py").unlink()

    checks = validate_project(project)

    health_check = next(check for check in checks if check.name == "Health route")
    assert not health_check.passed


@pytest.mark.parametrize("path", ["missing", "."])
def test_rejects_missing_or_non_directory_paths(tmp_path: Path, path: str) -> None:
    candidate = tmp_path / path if path == "missing" else tmp_path / "file"
    if path == ".":
        candidate.write_text("not a directory", encoding="utf-8")

    with pytest.raises(ProjectPathError):
        validate_project(candidate)

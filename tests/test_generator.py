"""Tests for template generation and error handling."""

from pathlib import Path

import pytest

from devbootstrap.errors import (
    DestinationExistsError,
    InvalidServiceNameError,
    TemplateNotFoundError,
)
from devbootstrap.generator import create_project, list_templates, validate_service_name


def test_generates_fastapi_project_with_substituted_name(tmp_path: Path) -> None:
    project = create_project("payment-service", tmp_path)

    assert project == tmp_path / "payment-service"
    assert (project / "app" / "main.py").is_file()
    assert (project / "app" / "routes" / "health.py").is_file()
    assert "payment-service" in (project / "README.md").read_text(encoding="utf-8")


def test_generates_minimal_project(tmp_path: Path) -> None:
    project = create_project("batch-worker", tmp_path, "minimal")

    assert (project / "app" / "main.py").is_file()
    assert "fastapi" not in (project / "requirements.txt").read_text(
        encoding="utf-8"
    ).lower()


@pytest.mark.parametrize("name", ["../outside", "Uppercase", "-bad", "bad--name", "a" * 51])
def test_rejects_invalid_service_names(name: str) -> None:
    with pytest.raises(InvalidServiceNameError):
        validate_service_name(name)


def test_rejects_existing_destination_without_changing_it(tmp_path: Path) -> None:
    existing = tmp_path / "payment-service"
    existing.mkdir()
    marker = existing / "keep.txt"
    marker.write_text("user data", encoding="utf-8")

    with pytest.raises(DestinationExistsError):
        create_project("payment-service", tmp_path)

    assert marker.read_text(encoding="utf-8") == "user data"


def test_rejects_unknown_template_without_creating_project(tmp_path: Path) -> None:
    with pytest.raises(TemplateNotFoundError):
        create_project("payment-service", tmp_path, "missing")

    assert not (tmp_path / "payment-service").exists()


def test_reports_output_directory_creation_failure(tmp_path: Path) -> None:
    output_file = tmp_path / "not-a-directory"
    output_file.write_text("keep this file", encoding="utf-8")

    with pytest.raises(OSError, match="Could not create project"):
        create_project("payment-service", output_file)

    assert output_file.read_text(encoding="utf-8") == "keep this file"


def test_lists_both_templates() -> None:
    assert set(list_templates()) == {"fastapi", "minimal"}

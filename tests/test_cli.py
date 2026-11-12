"""Tests for CLI commands and exit behavior."""

from pathlib import Path

from typer.testing import CliRunner

from devbootstrap.cli import app

runner = CliRunner()


def test_create_and_validate_commands(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["create", "payment-service", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "payment-service" / "app" / "main.py").is_file()

    validation = runner.invoke(
        app, ["validate", str(tmp_path / "payment-service")]
    )
    assert validation.exit_code == 0, validation.output
    assert "PASS" in validation.output


def test_template_listing_and_version() -> None:
    templates = runner.invoke(app, ["list-templates"])
    version = runner.invoke(app, ["version"])

    assert templates.exit_code == 0
    assert "fastapi" in templates.output
    assert "minimal" in templates.output
    assert version.exit_code == 0
    assert "1.0.0" in version.output


def test_invalid_create_fails_clearly(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["create", "../unsafe", "--output-dir", str(tmp_path)]
    )

    assert result.exit_code == 1
    assert "Error:" in result.output

"""Command-line interface for DevBootstrap."""

from pathlib import Path
from typing import Annotated

import typer

from devbootstrap import __version__
from devbootstrap.errors import DevBootstrapError
from devbootstrap.generator import create_project, list_templates
from devbootstrap.validator import validate_project

app = typer.Typer(
    name="devbootstrap",
    help="Generate and validate standardized backend service projects.",
    no_args_is_help=True,
    add_completion=False,
)


def _handle_error(error: DevBootstrapError) -> None:
    typer.echo(f"Error: {error}", err=True)
    raise typer.Exit(code=1) from error


@app.command()
def create(
    service_name: Annotated[str, typer.Argument(help="New service directory name.")],
    template: Annotated[
        str, typer.Option("--template", help="Template name: fastapi or minimal.")
    ] = "fastapi",
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Parent directory where the new service will be created.",
            file_okay=False,
            writable=True,
        ),
    ] = Path.cwd(),
) -> None:
    """Create a new service project."""
    try:
        created_path = create_project(service_name, output_dir, template)
    except DevBootstrapError as error:
        _handle_error(error)
    except OSError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"Created {template} service at {created_path}")


@app.command("list-templates")
def show_templates() -> None:
    """List available service templates."""
    for name, description in list_templates().items():
        typer.echo(f"{name}: {description}")


@app.command()
def validate(
    project_path: Annotated[
        Path, typer.Argument(help="Path to the service project to validate.")
    ],
) -> None:
    """Check a service project and display each result."""
    try:
        checks = validate_project(project_path)
    except DevBootstrapError as error:
        _handle_error(error)
    failed = False
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        typer.echo(f"{status} {check.name}: {check.detail}")
        failed = failed or not check.passed
    if failed:
        raise typer.Exit(code=1)
    typer.echo("Project validation passed.")


@app.command()
def version() -> None:
    """Print the installed DevBootstrap version."""
    typer.echo(f"DevBootstrap {__version__}")


if __name__ == "__main__":
    app()

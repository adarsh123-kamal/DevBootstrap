# DevBootstrap — Automated Service Template Generator

DevBootstrap is a small Python command-line tool that creates consistent backend service projects from reusable templates. It helps teams start new services with a working health endpoint, configuration, structured logs, tests, and setup instructions instead of repeating boilerplate by hand.

## Problem statement

New services often begin with inconsistent layouts and missing operational basics. DevBootstrap standardizes that starting point while keeping generated projects small, readable, and easy to customize.

## Architecture

- `src/devbootstrap/cli.py` defines the Typer command-line interface.
- `src/devbootstrap/generator.py` validates names and copies bundled templates.
- `src/devbootstrap/validator.py` checks generated project structure and content.
- `src/devbootstrap/templates/` contains the FastAPI and minimal Python service templates.
- `tests/` exercises generation, validation, and command behavior in temporary directories.

## Features

- Generate a FastAPI service or a minimal Python service.
- JSON-formatted application logging and environment-based settings.
- Validate a project and report each check as `PASS` or `FAIL`.
- Safe name and destination checks; generation never overwrites an existing directory.
- Pytest coverage, Python 3.12 support, and a GitHub Actions CI workflow.

## Installation

Use Python 3.12 or newer:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The `devbootstrap` command is installed by the project entry point. Alternatively, run it with `python -m devbootstrap`.

## Usage

Create a FastAPI project in the current directory:

```bash
devbootstrap create payment-service
```

Choose a template or a different output directory:

```bash
devbootstrap create report-worker --template minimal --output-dir ./services
devbootstrap list-templates
devbootstrap validate ./payment-service
devbootstrap version
```

Generated FastAPI service:

```bash
cd payment-service
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The service is available at `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/health`.
Set `APP_NAME`, `ENVIRONMENT`, `PORT`, or `DEBUG` in the environment. `.env.example` documents the variables; install a dotenv loader separately if you want automatic `.env` loading.

## CLI commands

| Command | Description |
| --- | --- |
| `devbootstrap create <service-name>` | Generate a project. Supports `--template` and `--output-dir`. |
| `devbootstrap list-templates` | List available template names and descriptions. |
| `devbootstrap validate <project-path>` | Check required project files and service entry points. |
| `devbootstrap version` | Print the installed DevBootstrap version. |

Service names must be lowercase, begin with a letter, and contain only lowercase letters, digits, or single hyphens.

## Generated folder structure (FastAPI)

```text
payment-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── health.py
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       └── logging_config.py
├── tests/
│   └── test_health.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

The minimal Python template uses the same app/core layout but provides a dependency-free health check instead of an HTTP server.

## Testing

Install development dependencies and run:

```bash
python -m pytest
```

Generator tests use pytest's temporary directories and do not write into existing user projects.

## Technologies

Python 3.12, FastAPI, Typer, pytest, Python logging, JSON, Git, and GitHub Actions.

## Future enhancements

- Additional framework and worker templates.
- Optional Git initialization and interactive configuration.
- Template versioning and organization-specific template repositories.

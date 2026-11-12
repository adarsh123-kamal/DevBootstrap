"""FastAPI application entry point."""

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.routes.health import router as health_router

settings = get_settings()
configure_logging()

app = FastAPI(
    title=settings.app_name,
    description=f"API service for {settings.app_name}.",
    version="1.0.0",
    debug=settings.debug,
)
app.include_router(health_router)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Return basic service information."""
    return {"service": settings.app_name, "status": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
    )

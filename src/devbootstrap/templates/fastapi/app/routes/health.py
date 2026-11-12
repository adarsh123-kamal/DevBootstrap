"""Health check route."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Report that the service process is healthy."""
    return {"status": "healthy"}

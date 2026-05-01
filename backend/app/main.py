"""MediGuard backend application entry point.

This module defines the FastAPI application instance and the lightweight
meta endpoints (such as `/health`) that uptime monitors and CI smoke tests
rely on.
"""

from typing import Final

from fastapi import FastAPI

from app import __version__

API_TITLE: Final[str] = "MediGuard API"
API_DESCRIPTION: Final[str] = (
    "Backend service for MediGuard - a privacy-first medication "
    "interaction tracker for patients on multiple prescriptions."
)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=__version__,
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Return service health status.

    Used by:
    - Container/platform health probes (Render, Docker)
    - Uptime monitoring services
    - CI smoke tests after deployment

    Returns:
        A small JSON document with the literal status `"ok"` and the
        currently running application version.
    """
    return {"status": "ok", "version": __version__}

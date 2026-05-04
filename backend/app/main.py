"""MediGuard backend application entry point.

This module defines the FastAPI application instance, the lifespan
hooks that run on startup and shutdown, and the lightweight meta
endpoints (such as `/health`) that uptime monitors and CI smoke
tests rely on.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final

import structlog
from fastapi import FastAPI

from app import __version__
from app.core.config import get_settings
from app.core.logging import configure_logging

API_TITLE: Final[str] = "MediGuard API"
API_DESCRIPTION: Final[str] = (
    "Backend service for MediGuard - a privacy-first medication "
    "interaction tracker for patients on multiple prescriptions."
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: configure logging and emit lifecycle events.

    The body before ``yield`` runs on startup, before the first request
    is served. The body after ``yield`` runs on graceful shutdown.
    """

    configure_logging()
    settings = get_settings()
    logger = structlog.get_logger(__name__)
    logger.info(
        "application_startup",
        app_name=settings.APP_NAME,
        app_env=settings.APP_ENV,
        version=__version__,
        debug=settings.DEBUG,
    )
    yield
    logger.info("application_shutdown")


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=__version__,
    lifespan=lifespan,
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

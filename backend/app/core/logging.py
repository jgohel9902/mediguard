"""Structured logging configuration using structlog.

Configures both structlog and the stdlib logging module to produce
consistent, structured output. Logs are JSON-formatted in production
(machine-readable) and human-friendly with colors in development.
All output goes to stdout, which plays nicely with container log
collectors and platform log agents.

Usage:

    from app.core.logging import configure_logging
    import structlog

    configure_logging()
    logger = structlog.get_logger(__name__)
    logger.info("event_name", key1="value1", key2=42)
"""

import logging
import sys

import structlog
from structlog.types import Processor

from app.core.config import get_settings

# Map our typed string log levels to stdlib integer constants.
_LOG_LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def configure_logging() -> None:
    """Configure structlog and the stdlib logging module.

    Should be called once at application startup, before any logging
    happens. Subsequent calls are safe but redundant.
    """
    settings = get_settings()
    log_level = _LOG_LEVEL_MAP[settings.LOG_LEVEL]

    # Route stdlib logging output through stdout at the configured level.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Shared processors enrich every event with timestamps and context.
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # JSON in production, pretty colored console in development.
    renderer: Processor
    if settings.LOG_JSON:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

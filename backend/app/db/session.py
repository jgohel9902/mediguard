"""Database engine and session management.

Exposes a SQLAlchemy ``Engine`` constructed from the ``DATABASE_URL``
setting, a ``SessionLocal`` factory for per-request sessions, and a
``get_db`` FastAPI dependency that yields a session and closes it
after each request.
"""

from collections.abc import Iterator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def _make_engine() -> Engine:
    """Construct the SQLAlchemy engine from settings.

    SQLite requires ``check_same_thread=False`` because FastAPI may
    dispatch requests across threads. PostgreSQL has no such constraint.
    ``pool_pre_ping=True`` validates connections before use so that
    stale connections (e.g., after a database restart) are recycled
    transparently.
    """
    settings = get_settings()

    connect_args: dict[str, Any] = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args=connect_args,
        pool_pre_ping=True,
    )


engine: Engine = _make_engine()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Iterator[Session]:
    """Yield a database session for FastAPI route handlers.

    Use as a FastAPI dependency::

        from fastapi import Depends
        from sqlalchemy.orm import Session
        from app.db.session import get_db

        @router.get("/users/{user_id}")
        def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
            ...

    The session is closed automatically after the request completes,
    even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

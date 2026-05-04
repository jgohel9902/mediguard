"""Tests for the User ORM model."""

import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.user import User


@pytest.fixture
def session() -> Iterator[Session]:
    """Provide a fresh in-memory SQLite session for each test.

    Each test gets its own engine so there is no state leakage between
    tests. The schema is materialized via ``Base.metadata.create_all``
    rather than running migrations — faster and avoids dependency on
    Alembic version state.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    test_session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = test_session_factory()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


def test_create_user_with_required_fields(session: Session) -> None:
    """A user can be persisted with email and hashed_password only."""
    user = User(
        email="alice@example.com",
        hashed_password="hash_of_a_real_password",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.email == "alice@example.com"


def test_user_defaults_are_correct(session: Session) -> None:
    """``is_active`` defaults to True; ``is_superuser`` to False; ``full_name`` to None."""
    user = User(email="bob@example.com", hashed_password="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.is_active is True
    assert user.is_superuser is False
    assert user.full_name is None


def test_user_timestamps_are_auto_set(session: Session) -> None:
    """``created_at`` and ``updated_at`` are populated by the database server default."""
    user = User(email="carol@example.com", hashed_password="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.created_at is not None
    assert user.updated_at is not None


def test_email_is_unique(session: Session) -> None:
    """Two users cannot share the same email address."""
    first = User(email="dup@example.com", hashed_password="hash1")
    session.add(first)
    session.commit()

    duplicate = User(email="dup@example.com", hashed_password="hash2")
    session.add(duplicate)

    with pytest.raises(IntegrityError):
        session.commit()


def test_user_repr_does_not_leak_password(session: Session) -> None:
    """``User.__repr__`` shows id and email but never the password hash."""
    user = User(
        email="eve@example.com",
        hashed_password="THIS_IS_A_SECRET",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    repr_str = repr(user)

    assert "eve@example.com" in repr_str
    assert "THIS_IS_A_SECRET" not in repr_str

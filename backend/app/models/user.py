"""User ORM model.

Represents an authenticated user of MediGuard. A user owns their own
medication list and their own interaction-check history; data is
strictly scoped per-user.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    """A user account.

    Attributes:
        id: UUID primary key, generated client-side at insert time.
        email: Unique email address, used as the login identifier.
        hashed_password: bcrypt-hashed password. Never plaintext.
        full_name: Optional human-readable display name.
        is_active: Soft-deletion flag. Inactive users cannot log in.
        is_superuser: Privilege flag for admin-only endpoints.
        created_at: Server-set creation timestamp (UTC, timezone-aware).
        updated_at: Server-managed last-modified timestamp.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Concise representation for logs and debugging."""
        return f"<User id={self.id!s} email={self.email!r}>"

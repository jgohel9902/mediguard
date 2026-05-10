"""Pydantic schemas for user signup, login, and read responses.

Strict input/output separation: ``UserCreate`` and ``UserLogin`` accept
plaintext passwords on the way in. ``UserRead`` returns user data with
no password field — neither plaintext nor hash. This separation makes
it structurally impossible for the password hash to leak through any
endpoint that responds with a ``UserRead``.
"""

import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ---------- Shared base ----------


class UserBase(BaseModel):
    """Fields shared by user create and read schemas."""

    email: EmailStr
    full_name: str | None = Field(default=None, max_length=255)


# ---------- Input schemas (request bodies) ----------


class UserCreate(UserBase):
    """Signup request body.

    Accepts a plaintext password. The hash is produced server-side by
    ``app.core.security.hash_password`` before persistence — the plain
    password never reaches the database or the logs.
    """

    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserLogin(BaseModel):
    """Login request body."""

    email: EmailStr
    password: Annotated[str, Field(min_length=1, max_length=128)]


# ---------- Output schemas (response bodies) ----------


class UserRead(UserBase):
    """User data returned to API clients.

    Notably absent: ``hashed_password``. There is no schema that exposes
    the hash — by construction, the hash cannot leak through any
    endpoint that returns a ``UserRead``.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


# ---------- Token schemas ----------


class Token(BaseModel):
    """JWT response body returned by ``/auth/login``."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Decoded JWT payload — used inside the auth dependency for typing."""

    sub: str
    exp: int
    iat: int

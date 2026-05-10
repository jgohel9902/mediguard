"""Authentication API routes: signup and login.

Endpoints:

- ``POST /auth/signup`` — create a new user account.
- ``POST /auth/login`` — verify credentials, issue a JWT.

The router is exported as ``router`` and mounted in ``app/main.py``.
"""

from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserRead

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
)
def signup(
    payload: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Create a new user.

    Hashes the plaintext password before persistence. Returns the new
    user's public view via the ``UserRead`` response model — no password
    field is ever returned.

    Raises:
        HTTPException 409: if the email is already registered.
    """
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.info("signup_conflict", email=payload.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from None

    db.refresh(user)
    logger.info("signup_success", user_id=str(user.id), email=user.email)
    return user


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and receive a JWT access token",
)
def login(
    payload: UserLogin,
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """Verify credentials and issue a JWT access token.

    Both an unknown email and a wrong password return the same 401 so
    we don't leak which emails are registered — defense in depth against
    user enumeration.

    Raises:
        HTTPException 401: on any credential failure.
        HTTPException 403: if the account exists but is inactive.
    """
    stmt = select(User).where(User.email == payload.email)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.hashed_password):
        logger.info("login_failed", email=payload.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.info("login_inactive", user_id=str(user.id))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    token = create_access_token(subject=str(user.id))
    logger.info("login_success", user_id=str(user.id))
    return Token(access_token=token)

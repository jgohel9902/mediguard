"""Application configuration loaded from environment variables.

Single source of truth for runtime configuration. All values are
validated and typed at import time. Reads from environment variables
and an optional `.env` file at the backend root.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

AppEnvironment = Literal["development", "staging", "production", "test"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Typed application settings.

    Values are loaded in this priority order:

    1. Environment variables
    2. ``.env`` file at the backend root (if present)
    3. Defaults defined below

    Environment-variable names are matched case-insensitively.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---------- Application ----------
    APP_NAME: str = "MediGuard API"
    APP_ENV: AppEnvironment = "development"
    DEBUG: bool = False

    # ---------- Server ----------
    HOST: str = "127.0.0.1"
    PORT: int = Field(default=8000, ge=1, le=65535)

    # ---------- Logging ----------
    LOG_LEVEL: LogLevel = "INFO"
    LOG_JSON: bool = Field(
        default=False,
        description="Render logs as JSON. Recommended in production.",
    )

    # ---------- Database ----------
    DATABASE_URL: str = "sqlite:///./mediguard.db"

    # ---------- Security ----------
    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
        description="Used for JWT signing. MUST be replaced in production.",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Uses ``lru_cache`` so settings are loaded once at first call and
    reused. Tests that need different settings can clear this cache
    via ``get_settings.cache_clear()``.
    """
    return Settings()

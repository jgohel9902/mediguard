"""Tests for the application configuration module (``app.core.config``)."""

import pytest
from app.core.config import Settings, get_settings
from pydantic import ValidationError

# Every settings-relevant environment variable. Scrubbed before each
# test so the OS environment can't leak into our assertions.
_SETTINGS_ENV_VARS: tuple[str, ...] = (
    "APP_NAME",
    "APP_ENV",
    "DEBUG",
    "HOST",
    "PORT",
    "LOG_LEVEL",
    "LOG_JSON",
    "DATABASE_URL",
    "SECRET_KEY",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
)


@pytest.fixture(autouse=True)
def _isolated_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Give each test a clean environment and a fresh settings cache."""
    for var in _SETTINGS_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    get_settings.cache_clear()


def test_settings_defaults_are_valid() -> None:
    """Settings constructs successfully with all defaults."""
    settings = Settings(_env_file=None)

    assert settings.APP_NAME == "MediGuard API"
    assert settings.APP_ENV == "development"
    assert settings.DEBUG is False
    assert settings.HOST == "127.0.0.1"
    assert settings.PORT == 8000
    assert settings.LOG_LEVEL == "INFO"
    assert settings.LOG_JSON is False
    assert settings.DATABASE_URL.startswith("sqlite")
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30


def test_settings_override_via_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Environment variables override the defaults."""
    monkeypatch.setenv("APP_NAME", "MediGuard Test API")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings(_env_file=None)

    assert settings.APP_NAME == "MediGuard Test API"
    assert settings.APP_ENV == "test"
    assert settings.PORT == 9000
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.DEBUG is True


def test_invalid_port_raises_validation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """PORT outside the TCP range fails validation."""
    monkeypatch.setenv("PORT", "70000")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_app_env_raises_validation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """APP_ENV outside the allowed Literal fails validation."""
    monkeypatch.setenv("APP_ENV", "wonderland")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_get_settings_is_cached() -> None:
    """get_settings returns the same instance across calls."""
    first = get_settings()
    second = get_settings()

    assert first is second

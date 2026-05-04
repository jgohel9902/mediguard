"""Alembic environment script.

Wires Alembic to MediGuard's SQLAlchemy metadata and pulls the
database URL from our application settings rather than from
``alembic.ini`` (so secrets stay in environment variables).

Invoked by:
- ``alembic revision --autogenerate -m "<message>"`` to generate a new
  migration based on diffs between ``Base.metadata`` and the live DB.
- ``alembic upgrade head`` to apply migrations.
- ``alembic downgrade <rev>`` to roll back.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_settings
from app.db.base import Base
import app.models  # noqa: F401  # register all ORM models with Base.metadata

# Alembic Config object, providing access to ``alembic.ini`` values.
config = context.config

# Override the sqlalchemy.url with the value from our settings layer.
# This means alembic.ini's placeholder URL is never used in real runs;
# the real URL always comes from environment variables / .env.
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configure Python logging from alembic.ini's logging sections.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for ``--autogenerate`` support.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode without a live DB connection.

    Generates SQL scripts that can be applied later (e.g., reviewed and
    executed by a DBA in a strictly controlled environment).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,  # SQLite needs this for ALTER TABLE
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode against a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,  # SQLite needs this for ALTER TABLE
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

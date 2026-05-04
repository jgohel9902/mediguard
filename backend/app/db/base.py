"""Declarative base for all ORM models.

The ``Base`` class is what every model inherits from. The metadata
attached to it carries a constraint **naming convention** so Alembic
can generate consistent index, unique-constraint, foreign-key, and
primary-key names across database backends. This matters because:

- Without a naming convention, SQLite and PostgreSQL will name
  auto-generated constraints differently, leading to noisy migration
  diffs whenever you switch databases.
- Named constraints are also far easier to manage in migrations
  (e.g., ``op.drop_constraint("uq_users_email", "users")``).

The convention used here is the one recommended by the SQLAlchemy
documentation and by Alembic.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Constraint naming convention — applied at the MetaData level.
# Tokens (e.g., ``%(table_name)s``) are filled in by SQLAlchemy.
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base for every ORM model in MediGuard.

    All models must inherit from this class so they share the same
    ``metadata`` (and therefore the same naming convention and the
    same target for ``Base.metadata.create_all`` and Alembic
    autogeneration).
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)

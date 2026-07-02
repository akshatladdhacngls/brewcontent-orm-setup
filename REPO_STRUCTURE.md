# Repository Structure (Starter Template)

This document defines the recommended baseline structure that each FastAPI microservice should follow for ORM and Alembic.

## Top-Level Layout

```text
service-name/
  app/
    api/
    core/
    db/
      __init__.py
      base.py
      config.py
      session.py
      mixins.py
      models/
        __init__.py
        user.py
    main.py
  alembic/
    versions/
  alembic.ini
  Makefile
  pyproject.toml
  .env.example
  README.md
```

## DB Folder Contract (`app/db/`)

### `app/db/config.py`
- Reads DB-related environment variables.
- Exposes a single function for the SQLAlchemy connection URL.
- Must support local/dev/prod connection strings.

### `app/db/base.py`
- Defines SQLAlchemy `DeclarativeBase`.
- Applies shared metadata naming conventions.
- Exposes `Base.metadata` for Alembic `target_metadata`.

### `app/db/session.py`
- Creates SQLAlchemy engine.
- Creates `sessionmaker` (or async equivalent if chosen per service standard).
- Exposes FastAPI dependency for request-scoped DB session.

### `app/db/mixins.py`
- Shared mixins for common columns.
- Recommended v1 mixins:
  - `UUIDPrimaryKeyMixin` (or service-standard ID mixin)
  - `TimestampMixin` (`created_at`, `updated_at` in UTC)
  - Optional `SoftDeleteMixin` (`deleted_at`)

### `app/db/models/`
- Contains service-owned ORM models.
- `__init__.py` should import models so Alembic autogenerate can discover metadata.

## Alembic Contract

### `alembic.ini`
- Base Alembic config.
- DB URL can be set from env or overwritten in `env.py`.

### `alembic/env.py`
- Imports service `Base.metadata` and model modules.
- Sets `target_metadata` to service-local metadata only.
- Never include metadata from other services.

### `alembic/versions/`
- Contains migration revisions for this service only.
- One migration history chain per service.

## Naming Conventions (Required)

Define centrally in `app/db/base.py`:
- `ix_%(column_0_label)s`
- `uq_%(table_name)s_%(column_0_name)s`
- `ck_%(table_name)s_%(constraint_name)s`
- `fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s`
- `pk_%(table_name)s`

This prevents drift/noisy diffs and keeps migration output deterministic.

## Makefile Contract (Required)

Every service should expose consistent DB commands:
- `make db-revision message="add foo table"`
- `make db-upgrade`
- `make db-downgrade step=-1`
- `make db-current`
- `make db-history`
- `make db-drift-check`

Reference implementation is documented in `COMMANDS.md`.

## CI Expectations

Each service pipeline should validate:
1. Upgrade from empty DB to head
2. Downgrade one revision
3. Re-upgrade to head
4. Drift check for unexpected model/schema mismatch

## What Must Stay Service-Local
- ORM models
- Alembic history
- Connection settings
- DB credentials

## What Can Be Shared Across Services
- Base mixin patterns
- Naming convention policy
- Command contract
- Migration safety policy

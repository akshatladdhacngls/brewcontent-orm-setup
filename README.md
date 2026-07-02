# Microservice ORM Base

Starter scaffolding for FastAPI microservices with PostgreSQL, SQLAlchemy 2.x, and Alembic.

## For Coding Agents

Before implementing schema/model changes, read `AGENTS_INSTRUCTION.md`.

## Quick Start

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Copy environment variables:

```bash
cp .env.example .env
```

4. Ensure PostgreSQL is running and `DATABASE_URL` points to your service database.

If you store variables in `.env`, export them in your shell before running commands:

```bash
set -a; source .env; set +a
```

5. Run migrations:

```bash
make db-upgrade
```

6. Start API:

```bash
uvicorn app.main:app --reload --port 8000
```

## Migration Commands

```bash
make db-revision message="create prompts table"
make db-upgrade
make db-downgrade step=-1
make db-current
make db-history
make db-drift-check
```

## What To Customize Per Service

- `app/db/models/` with your service-specific ORM models.
- `DATABASE_URL` for your service database.
- API routes in `app/main.py` (or your service modules).

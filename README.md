# Microservice ORM Base (Web Search PoC)

Simple FastAPI microservice to validate PostgreSQL + SQLAlchemy + Alembic using a DuckDuckGo-backed search PoC.

## For Coding Agents

Before making implementation changes, read `AGENTS_INSTRUCTION.md`.
It defines required safety rules, migration workflow, and done criteria.

## What This PoC Covers

- SQLAlchemy ORM models (`search_jobs`, `search_results`)
- Alembic migration lifecycle
- Dockerized PostgreSQL for local testing
- Minimal API to write/read search jobs and results

## Quick Start

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Copy environment variables (you can edit later):

```bash
cp .env.example .env
```

4. Start PostgreSQL in Docker:

```bash
docker compose up -d postgres
```

5. Run migrations:

```bash
make db-upgrade
```

6. Start API:

```bash
uvicorn app.main:app --reload --port 8000
```

## Test The PoC

Create a search job:

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"fastapi alembic sqlalchemy","max_results":5}'
```

Fetch search job details:

```bash
curl http://127.0.0.1:8000/search/<JOB_ID>
```

## Migration Commands

```bash
make db-revision message="create table"
make db-upgrade
make db-downgrade step=-1
make db-current
make db-history
make db-drift-check
```

## Docker Commands

```bash
docker compose up -d postgres
docker compose ps
docker compose logs postgres
docker compose down
```

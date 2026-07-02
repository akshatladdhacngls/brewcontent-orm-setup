# Team Onboarding (ORM + Alembic Base)

## What You Get
- Standard PostgreSQL ORM setup for FastAPI
- Pre-configured Alembic migration scaffolding
- Shared conventions and CI expectations

## Team Responsibilities
- Define and maintain your service models
- Own your service migration lifecycle
- Follow migration policy and CI checks

## What Not To Do
- Do not access another service database directly
- Do not create cross-service foreign keys
- Do not bypass migration scripts for schema changes

## Recommended Workflow
1. Add/modify SQLAlchemy models.
2. Generate Alembic revision.
3. Manually review migration SQL/operations.
4. Run upgrade/downgrade tests.
5. Open PR with migration notes and risk assessment.

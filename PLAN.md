# Microservice ORM + Alembic Base Plan

## Purpose
Create a reusable base module that gives every FastAPI microservice a consistent, safe, and scalable setup for:
- SQLAlchemy ORM
- Alembic migrations
- PostgreSQL conventions
- CI migration validation

This repository is the starting point for all teams building new services.

## Scope (v1)
- SQLAlchemy 2.x setup (engine, session, base metadata)
- Alembic integration with service-local migration history
- Shared model conventions (IDs, timestamps, naming)
- Migration safety playbook (expand/contract)
- CI checks for migration integrity

## Non-Goals (v1)
- Cross-service joins/foreign keys
- Global monolithic migration chain
- Distributed transactions framework
- Multi-tenant/sharding framework

## Guiding Principles
1. Each service owns its data and migrations.
2. Services deploy independently.
3. Migrations are backward-compatible by default.
4. Schema changes must be observable, reviewable, and reversible.

## Architecture Direction
- Database ownership: per microservice (preferred).
- Transitional fallback: same PostgreSQL cluster, but isolated DB/schema per service plus strict credentials.
- Alembic ownership: each service has its own `alembic/` directory and migration history.
- ORM ownership: each service defines only its own models.

## Repository Deliverables
- Base package/template structure for ORM and Alembic
- Example model(s) and migration flow
- Team docs:
  - Quickstart
  - Migration policy
  - CI expectations
  - Common pitfalls

## Work Phases

### Phase 1: Foundation
- Define project skeleton for service DB layer
- Configure SQLAlchemy base plus naming conventions
- Configure Alembic `env.py` to target service metadata
- Add sample initial migration

### Phase 2: Standards + Guardrails
- Add migration command wrappers (create/upgrade/downgrade/history/current)
- Add CI migration test flow:
  - Upgrade from empty DB to head
  - Downgrade one step
  - Upgrade again
- Add model drift check (autogenerate should not produce unexpected diff)

### Phase 3: Documentation
- Quickstart for service teams
- Migration safety guide (expand/contract)
- PR checklist for schema changes
- Troubleshooting guide (locks, enum changes, rename patterns)

### Phase 4: Pilot Adoption
- Integrate in 1-2 services
- Capture friction points
- Refine templates and docs
- Release v1.0 for wider adoption

## Success Criteria
- New service can reach first migration in under 30 minutes.
- Schema PRs use consistent conventions and pass CI checks.
- No breaking migration incidents during rollout.
- Teams can independently evolve schemas without cross-team coupling.

## Risks and Mitigation
- Risk: teams bypass migration conventions.
  - Mitigation: CI checks plus PR checklist plus docs.
- Risk: destructive changes cause downtime.
  - Mitigation: expand/contract policy and staged rollouts.
- Risk: shared DB reintroduces monolith coupling.
  - Mitigation: enforce strict isolation and no shared tables.

## Ownership
- Platform/architecture team: base module, standards, governance.
- Service teams: service-specific models and migrations.

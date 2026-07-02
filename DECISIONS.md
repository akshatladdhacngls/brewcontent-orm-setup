# Architecture Decisions (ORM + Alembic)

This document records locked decisions for microservice database architecture.

## ADR-001: ORM and Migration Stack
**Decision:** Use SQLAlchemy 2.x ORM + Alembic with PostgreSQL for all Python/FastAPI microservices.

**Why:**
- Mature ecosystem and tooling
- Strong compatibility with FastAPI
- Reliable migration workflow

**Status:** Accepted

---

## ADR-002: Data Ownership Model
**Decision:** Each microservice owns its own database (preferred).
If infrastructure constraints exist, use one PostgreSQL cluster with strict per-service DB/schema isolation.

**Why:**
- Independent deploy and rollback
- Reduced coupling
- Clear ownership boundaries

**Rules:**
- No shared tables across services
- No cross-service foreign keys
- Inter-service data access via APIs/events only

**Status:** Accepted

---

## ADR-003: Migration Ownership
**Decision:** Each microservice maintains its own Alembic migration history.

**Why:**
- Independent release cadence
- Avoid global migration bottlenecks
- Service-local accountability

**Status:** Accepted

---

## ADR-004: Migration Safety Strategy
**Decision:** Use expand/contract for breaking schema changes.

**Pattern:**
1. Expand: add nullable/new structures
2. Migrate application behavior safely
3. Backfill data via controlled jobs
4. Contract: remove old structures later

**Why:**
- Minimize downtime and lock contention
- Preserve rollback safety

**Status:** Accepted

---

## ADR-005: Schema Conventions
**Decision:** Standardize naming conventions for constraints and indexes at SQLAlchemy metadata level.

**Why:**
- Deterministic migration diffs
- Better operability and debugging

**Status:** Accepted

---

## ADR-006: CI Migration Validation
**Decision:** Every service must validate migrations in CI.

**Minimum checks:**
- Upgrade from empty DB to head
- Downgrade (at least one revision)
- Re-upgrade to head
- Drift check for unexpected autogenerate diffs

**Status:** Accepted

---

## ADR-007: Cross-Service Data Access
**Decision:** Services must not query other service databases directly.

**Why:**
- Prevent tight coupling
- Maintain service autonomy
- Preserve security boundaries

**Status:** Accepted

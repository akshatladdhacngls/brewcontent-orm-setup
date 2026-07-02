# Migration Policy

## Objectives
- Safe schema evolution
- Backward-compatible deployments
- Predictable rollback paths

## Required Rules
1. Every schema change must be tracked via an Alembic migration.
2. Autogenerate is allowed, but migration scripts require manual review.
3. Migrations must include downgrade unless explicitly justified.
4. Destructive changes (drop/rename/type narrowing) must use expand/contract.
5. Large data backfills should run as separate controlled jobs, not long blocking migrations.

## Expand/Contract Standard
- Expand: add new columns/tables/indexes in backward-compatible form.
- Dual-write/read transition: app supports old + new paths as needed.
- Backfill: execute in batches with monitoring.
- Contract: remove old schema in a later release.

## Operational Checks
- Assess lock impact for table rewrites/index creation.
- Prefer online-safe patterns where possible.
- Schedule risky migration windows if needed.

## PR Checklist
- Migration reviewed manually
- Upgrade + downgrade tested locally
- Lock/performance impact considered
- Rollback strategy documented

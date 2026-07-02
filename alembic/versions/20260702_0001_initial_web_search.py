"""initial web search tables

Revision ID: 20260702_0001
Revises:
Create Date: 2026-07-02 12:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260702_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_jobs",
        sa.Column("query", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("result_count", sa.Integer(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_search_jobs")),
    )
    op.create_index(op.f("ix_search_jobs_query"), "search_jobs", ["query"], unique=False)
    op.create_index(op.f("ix_search_jobs_status"), "search_jobs", ["status"], unique=False)

    op.create_table(
        "search_results",
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["search_jobs.id"], name=op.f("fk_search_results_job_id_search_jobs"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_search_results")),
    )
    op.create_index(op.f("ix_search_results_job_id"), "search_results", ["job_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_search_results_job_id"), table_name="search_results")
    op.drop_table("search_results")
    op.drop_index(op.f("ix_search_jobs_status"), table_name="search_jobs")
    op.drop_index(op.f("ix_search_jobs_query"), table_name="search_jobs")
    op.drop_table("search_jobs")

"""add search provider to search jobs

Revision ID: 8c2db4dcd024
Revises: 20260702_0001
Create Date: 2026-07-02 16:28:13.145606
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '8c2db4dcd024'
down_revision = '20260702_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "search_jobs",
        sa.Column(
            "search_provider",
            sa.String(length=80),
            nullable=False,
            server_default="duckduckgo",
        ),
    )
    op.alter_column("search_jobs", "search_provider", server_default=None)


def downgrade() -> None:
    op.drop_column("search_jobs", "search_provider")

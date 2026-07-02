from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class SearchJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "search_jobs"

    search_provider: Mapped[str] = mapped_column(String(80), nullable=False, default="duckduckgo")
    query: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="queued", index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    results: Mapped[list[SearchResult]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )


class SearchResult(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "search_results"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("search_jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="duckduckgo")

    job: Mapped[SearchJob] = relationship(back_populates="results")

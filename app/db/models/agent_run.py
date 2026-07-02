from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AgentRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_runs"

    agent_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="queued", index=True)
    provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    response_text: Mapped[str | None] = mapped_column(Text, nullable=True)

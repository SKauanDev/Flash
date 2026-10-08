from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, Integer, String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.models import Base
from app.tools.registry import Tool, ToolKind, registry


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(500))
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("UTC")))


async def create_task(user_id: int, title: str, due_at: str | None = None) -> dict:
    # Runtime injects the DB session into this tool context in the next layer.
    return {"status": "accepted", "user_id": user_id, "title": title, "due_at": due_at}


async def list_tasks(user_id: int, status: str = "pending") -> dict:
    return {"status": "accepted", "user_id": user_id, "filter": status}


registry.register(Tool(
    name="tasks.create",
    description="Create a persistent reminder/task for the user.",
    kind=ToolKind.WRITE,
    schema={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "due_at": {"type": ["string", "null"], "description": "ISO-8601 datetime or null"},
        },
        "required": ["title"],
        "additionalProperties": False,
    },
    executor=create_task,
))

registry.register(Tool(
    name="tasks.list",
    description="List the user's tasks.",
    kind=ToolKind.READ,
    schema={
        "type": "object",
        "properties": {"status": {"type": "string", "default": "pending"}},
        "additionalProperties": False,
    },
    executor=list_tasks,
))

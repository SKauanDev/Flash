from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.models import Base
from app.tools.registry import Tool, ToolKind, registry


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(500))
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


def _db(context: dict) -> Session:
    db = context.get("db")
    if not isinstance(db, Session):
        raise RuntimeError("Database session is required")
    return db


async def create_task(*, context: dict, title: str, due_at: str | None = None) -> dict:
    db = _db(context)
    parsed_due = datetime.fromisoformat(due_at.replace("Z", "+00:00")) if due_at else None
    if parsed_due and parsed_due.tzinfo is None:
        parsed_due = parsed_due.replace(tzinfo=timezone.utc)

    task = Task(
        user_id=int(context["user_id"]),
        title=title.strip(),
        due_at=parsed_due,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"status": "created", "task_id": task.id, "title": task.title, "due_at": task.due_at.isoformat() if task.due_at else None}


async def list_tasks(*, context: dict, status: str = "pending") -> dict:
    db = _db(context)
    tasks = db.scalars(
        select(Task)
        .where(Task.user_id == int(context["user_id"]), Task.status == status)
        .order_by(Task.due_at, Task.created_at)
    ).all()
    return {
        "status": "ok",
        "tasks": [
            {"id": t.id, "title": t.title, "due_at": t.due_at.isoformat() if t.due_at else None}
            for t in tasks
        ],
    }


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

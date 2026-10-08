from datetime import datetime
from sqlalchemy import select
from app.db.session import SessionLocal
from app.tools.tasks import Task


def claim_due_tasks(now: datetime) -> list[Task]:
    with SessionLocal() as db:
        tasks = list(db.scalars(
            select(Task)
            .where(Task.status == "pending", Task.due_at <= now)
            .order_by(Task.due_at)
        ).all())
        for task in tasks:
            task.status = "processing"
        db.commit()
        return tasks

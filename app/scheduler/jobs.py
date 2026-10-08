from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.tools.tasks import Task

def claim_due_tasks(db: Session, now: datetime) -> list[Task]:
    tasks = list(db.scalars(
        select(Task).where(Task.status == "pending", Task.due_at.is_not(None), Task.due_at <= now)
        .order_by(Task.due_at).with_for_update()
    ).all())
    for task in tasks:
        task.status = "processing"
    db.flush()
    return tasks

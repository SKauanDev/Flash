import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from app.db.models import User
from app.db.session import SessionLocal
from app.scheduler.jobs import claim_due_tasks
from app.whatsapp.client import whatsapp_client

async def scheduler_loop() -> None:
    while True:
        with SessionLocal() as db:
            tasks = claim_due_tasks(db, datetime.now(timezone.utc))
            for task in tasks:
                user = db.scalar(select(User).where(User.id == task.user_id))
                if not user:
                    task.status = "failed"
                    continue
                try:
                    await whatsapp_client.send_text(user.whatsapp_id, f"⏰ Lembrete: {task.title}")
                    task.status = "completed"
                except Exception:
                    task.status = "pending"
            db.commit()
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(scheduler_loop())

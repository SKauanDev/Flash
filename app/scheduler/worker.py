import asyncio
from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.scheduler.jobs import claim_due_tasks


async def scheduler_loop() -> None:
    while True:
        with SessionLocal() as db:
            # Claiming in a transaction prevents the same task from being
            # processed repeatedly by this worker instance.
            tasks = claim_due_tasks(db, datetime.now(timezone.utc))
            for task in tasks:
                # Notification delivery will be delegated to the WhatsApp
                # notification service. Marking delivery separately comes next.
                task.status = "completed"
            db.commit()
        await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(scheduler_loop())

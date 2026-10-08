import asyncio
from datetime import datetime, timezone
from app.db.session import SessionLocal
from app.scheduler.jobs import claim_due_tasks

async def scheduler_loop() -> None:
    while True:
        with SessionLocal() as db:
            tasks = claim_due_tasks(db, datetime.now(timezone.utc))
            for task in tasks:
                task.status = "completed"
            db.commit()
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(scheduler_loop())

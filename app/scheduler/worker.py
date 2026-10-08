import asyncio
from datetime import datetime, timezone

from app.scheduler.jobs import claim_due_tasks


async def scheduler_loop() -> None:
    while True:
        claim_due_tasks(datetime.now(timezone.utc))
        await asyncio.sleep(15)

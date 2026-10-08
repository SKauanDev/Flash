import asyncio
from app.scheduler.worker import scheduler_loop

if __name__ == "__main__":
    asyncio.run(scheduler_loop())

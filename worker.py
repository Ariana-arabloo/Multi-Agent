import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")
    print("✅ با موفقیت به سرور Temporal وصل شد!")

    worker = Worker(
        client,
        task_queue="agent-tasks-queue",
        workflows=[],
        activities=[],
    )

    print("⏳ ورکر روشن شد و منتظر دریافت تسک است...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
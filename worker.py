import asyncio
from datetime import timedelta
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import activity, workflow

@activity.defn
async def call_litellm_activity(prompt: str) -> str:
    print(f"Processing prompt: {prompt}")
    return f"Model response for: {prompt}"

@workflow.defn
class AgenticWorkflow:
    @workflow.run
    async def run(self, prompt: str) -> str:
        return await workflow.execute_activity(
            call_litellm_activity,
            prompt,
            start_to_close_timeout=timedelta(seconds=15),
        )

async def main():
    client = await Client.connect("127.0.0.1:7233")
    print("Connected to Temporal server successfully!")

    worker = Worker(
        client,
        task_queue="agent-tasks-queue",
        workflows=[AgenticWorkflow],
        activities=[call_litellm_activity],
    )

    print("Worker is running and listening for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
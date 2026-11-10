from datetime import timedelta
from temporalio import workflow

# این بخش به تمپورال می‌گوید گیر نده و اجازه بده اکتیویتی را وارد کنیم
with workflow.unsafe.imports_passed_through():
    from activities import call_litellm_activity

@workflow.defn
class AgenticWorkflow:
    @workflow.run
    async def run(self, prompt: str) -> str:
        result = await workflow.execute_activity(
            call_litellm_activity,
            prompt,
            start_to_close_timeout=timedelta(seconds=60),
        )
        return result
import asyncio
import json
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="Multi-Agent Platform API")

@app.get("/")
async def root():
    return {"message": "سرور بک‌اند با موفقیت اجرا شد!"}

async def log_generator(request: Request, project_id: str):
    counter = 1
    while True:
        if await request.is_disconnected():
            break
        
        fake_log = {
            "node_id": f"agent-{counter}",
            "status": "processing", 
            "message": f"در حال پردازش پروژه {project_id} - پیام شماره {counter}"
        }
        
        yield {
            "event": "node_update",
            "data": json.dumps(fake_log)
        }
        
        counter += 1
        await asyncio.sleep(2.0)

@app.get("/api/v1/projects/{project_id}/stream")
async def stream_project_logs(project_id: str, request: Request):
    return EventSourceResponse(log_generator(request, project_id))
import uuid
import asyncio
import json
from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ProjectCreate

app = FastAPI(
    title="Multi-Agent System API",
    description="Core asynchronous communication API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ساب‌تسک ۴: لایه مدیریت خطاهای عمومی (Global Exception Handler)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "خطای پیش‌بینی نشده‌ای رخ داده است."
        },
    )

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and Docker!"}

@app.post("/api/v1/projects", status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    project_id = str(uuid.uuid4())
    return {
        "message": "Project creation accepted",
        "project_id": project_id,
        "status": "processing"
    }

# اضافه شدن مسیر استریم (SSE) برای ارسال آپدیت‌های زنده به فرانت‌اند
@app.get("/api/v1/projects/{project_id}/stream")
async def stream_project_events(project_id: str):
    async def event_generator():
        # ۱. پیام اولیه: تایید اتصال
        yield {"data": json.dumps({"node_id": "system", "status": "connected"})}
        
        # ۲. رفتن به حالت پردازش (زرد)
        await asyncio.sleep(2)
        yield {"data": json.dumps({"node_id": "3", "status": "processing"})}
        
        # ۳. رفتن به حالت موفقیت (سبز)
        await asyncio.sleep(3)
        yield {"data": json.dumps({"node_id": "3", "status": "success"})}

        # ۴. حلقه ضربان قلب (Heartbeat) فقط برای باز نگه داشتن اتصال بدون تغییر رنگ
        while True:
            await asyncio.sleep(15)
            yield {"data": json.dumps({"node_id": "system", "status": "ping"})}

    return EventSourceResponse(event_generator())
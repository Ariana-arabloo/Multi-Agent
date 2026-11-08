import asyncio
import json
from datetime import datetime
from fastapi import FastAPI, Request, Depends
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# ایمپورت مدل دیتابیس (با توجه به ساختار شما، مدل‌ها در پوشه app هستند)
try:
    from app.models import MessageLog
except ImportError:
    pass  # در صورتی که هنوز ایمپورت‌ها تنظیم نیستند، سرور کرش نکند

app = FastAPI(title="Multi-Agent Platform API")

# --- تابع موقت اتصال به دیتابیس ---
# (بعداً که سیستم دیتابیس پروژه را کامل کردید، این را با سشن واقعی جایگزین کنید)
async def get_db():
    yield None

@app.get("/")
async def root():
    return {"message": "سرور بک‌اند با موفقیت اجرا شد!"}

async def live_log_generator(request: Request, project_id: str, db: AsyncSession):
    last_checked = datetime.utcnow()
    counter = 1

    while True:
        # اگر کاربر صفحه را بست، استریم متوقف شود تا منابع سرور هدر نرود
        if await request.is_disconnected():
            break

        # اگر دیتابیس متصل بود و آیدی پروژه یک عدد واقعی بود، از دیتابیس می‌خوانیم:
        if db is not None and project_id.isdigit():
            stmt = select(MessageLog).where(
                MessageLog.project_id == int(project_id),
                MessageLog.logged_at > last_checked
            ).order_by(MessageLog.logged_at.asc())
            
            try:
                result = await db.execute(stmt)
                new_logs = result.scalars().all()
                
                for log in new_logs:
                    log_data = {
                        "node_id": log.sender,
                        "status": "processing",
                        "message": log.message,
                        "logged_at": log.logged_at.isoformat()
                    }
                    yield {
                        "event": "node_update",
                        "data": json.dumps(log_data, ensure_ascii=False)
                    }
                    last_checked = log.logged_at
            except Exception as e:
                print(f"Database error: {e}")
                
        # در غیر این صورت (برای اینکه تست‌های pytest و تست مرورگر شما فعلاً خراب نشود)، دیتای تستی می‌فرستیم:
        else:
            fake_log = {
                "node_id": f"agent-{counter}",
                "status": "processing",
                "message": f"لاگ تستی پروژه {project_id} - شماره {counter}"
            }
            yield {
                "event": "node_update",
                "data": json.dumps(fake_log, ensure_ascii=False)
            }
            counter += 1

        # هر ۲ ثانیه بررسی تکرار می‌شود
        await asyncio.sleep(2.0)

@app.get("/api/v1/projects/{project_id}/stream")
async def stream_project_logs(request: Request, project_id: str, db: AsyncSession = Depends(get_db)):
    """
    مسیر استریم زنده رویدادهای پروژه (پشتیبانی از دیتابیس و داده‌های تستی)
    """
    return EventSourceResponse(live_log_generator(request, project_id, db))
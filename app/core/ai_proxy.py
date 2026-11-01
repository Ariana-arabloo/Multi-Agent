import logging
import asyncio
import redis.asyncio as redis
from litellm import acompletion
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FALLBACK_MODELS = ["deepseek/deepseek-chat", "gpt-3.5-turbo"]

# ساب‌تسک ۱: ایجاد ماژول ارتباطی با Redis (Async)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# ساب‌تسک ۲: پیاده‌سازی Throttling و محدودیت RPM
async def rate_limit_and_throttle(limit: int = 15):
    requests = await redis_client.incr("api_requests")
    if requests == 1:
        await redis_client.expire("api_requests", 60)
    
    if requests > limit:
        logger.warning(f"ترافیک بالا (درخواست {requests}). اعمال قطره‌چکانی (Throttling)...")
        await asyncio.sleep(2)

# ساب‌تسک ۳: پیاده‌سازی Exponential Backoff
@retry(
    wait=wait_exponential(multiplier=1, min=1, max=4),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
async def call_model_with_backoff(model, messages):
    return await acompletion(model=model, messages=messages, temperature=0.7)

async def get_ai_response(prompt: str) -> str:
    await rate_limit_and_throttle() # کنترل ترافیک
    
    messages = [{"role": "user", "content": prompt}]
    for model in FALLBACK_MODELS:
        try:
            response = await call_model_with_backoff(model, messages)
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"مدل {model} پس از ۳ تلاش ناموفق قطع شد: '{str(e)}'. سوئیچ به جایگزین...")
            continue
            
    return "Error: تمامی مدل‌های اصلی و جایگزین با خطا مواجه شدند."
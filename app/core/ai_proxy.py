import logging
from litellm import acompletion
from dotenv import load_dotenv

# بارگذاری کلیدهای API
load_dotenv()

# فعال‌سازی سیستم لاگینگ برای ثبت خطاها (ساب‌تسک ۴)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تعریف لیست مدل‌ها به ترتیب اولویت (ساب‌تسک ۱ و ۲)
FALLBACK_MODELS = ["deepseek/deepseek-chat", "gpt-3.5-turbo"]

async def get_ai_response(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    
    for model in FALLBACK_MODELS:
        try:
            response = await acompletion(
                model=model,
                messages=messages,
                temperature=0.7 # ساب‌تسک ۳: پارامتر پیش‌فرض
            )
            return response.choices[0].message.content
            
        except Exception as e:
            # ثبت خطای مدل فعلی و ادامه تلاش با مدل بعدی
            logger.warning(f"مدل {model} با خطا مواجه شد: '{str(e)}'. در حال سوئیچ به مدل جایگزین...")
            continue
            
    # اگر تمام مدل‌های لیست قطع باشند
    return "Error: تمامی مدل‌های اصلی و جایگزین با خطا مواجه شدند."
from litellm import acompletion
from dotenv import load_dotenv

# بارگذاری امن کلیدهای API از فایل .env
load_dotenv()

# ساب‌تسک ۲ و ۳: تابع ناهمگام با پارامترهای پیش‌فرض
async def get_ai_response(prompt: str, model: str = "deepseek/deepseek-chat") -> str:
    try:
        response = await acompletion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7, # ساب‌تسک ۳: پارامتر پیش‌فرض
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
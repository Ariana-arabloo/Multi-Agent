import pytest
from unittest.mock import patch
from app.core.ai_proxy import get_ai_response

@pytest.mark.asyncio
@patch("app.core.ai_proxy.acompletion")
async def test_get_ai_response(mock_acompletion):
    # تنظیم یک پاسخ تقلبی (Mock) برای تست بدون مصرف توکن واقعی
    mock_acompletion.return_value.choices = [
        type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ تستی موفق"})})()
    ]
    
    # فراخوانی تابع
    response = await get_ai_response("سلام، این یک تست است.")
    
    # بررسی صحت عملکرد
    assert response == "پاسخ تستی موفق"
    mock_acompletion.assert_called_once()
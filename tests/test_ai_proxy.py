import pytest
from unittest.mock import patch, AsyncMock
from app.core.ai_proxy import get_ai_response

@pytest.mark.asyncio
@patch("app.core.ai_proxy.acompletion")
async def test_get_ai_response(mock_acompletion):
    # تست حالت عادی (موفقیت‌آمیز بودن مدل اول)
    mock_acompletion.return_value.choices = [
        type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ تستی موفق"})()})()
    ]
    response = await get_ai_response("سلام، این یک تست است")
    assert response == "پاسخ تستی موفق"
    mock_acompletion.assert_called_once()

@pytest.mark.asyncio
@patch("app.core.ai_proxy.acompletion", new_callable=AsyncMock)
async def test_fallback_routing_on_error(mock_acompletion):
    # ساخت یک پاسخ موفقیت‌آمیز برای مدل دوم (جایگزین)
    mock_success_response = type("Obj", (object,), {
        "choices": [type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ از مدل جایگزین"})()})()]
    })()

    # شبیه‌سازی مکانیزم Fallback: بار اول خطای 403، بار دوم پاسخ موفق
    mock_acompletion.side_effect = [
        Exception("403 Forbidden - Access Denied"),
        mock_success_response
    ]
    
    response = await get_ai_response("تست مسیریابی")
    
    # تایید اینکه خروجی نهایی از مدل دوم گرفته شده است
    assert response == "پاسخ از مدل جایگزین"
    # تایید اینکه سیستم دقیقاً دو بار درخواست ارسال کرده است (تلاش اول ناموفق، تلاش دوم موفق)
    assert mock_acompletion.call_count == 2
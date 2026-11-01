import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from app.core.ai_proxy import get_ai_response

# این بخش ارتباط با دیتابیس واقعی را در محیط تست قطع می‌کند
@pytest.fixture(autouse=True)
def bypass_rate_limit():
    with patch("app.core.ai_proxy.rate_limit_and_throttle", new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
@patch("app.core.ai_proxy.call_model_with_backoff")
async def test_get_ai_response(mock_call):
    mock_call.return_value.choices = [
        type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ تستی موفق"})()})()
    ]
    response = await get_ai_response("سلام، این یک تست است")
    assert response == "پاسخ تستی موفق"

@pytest.mark.asyncio
@patch("app.core.ai_proxy.call_model_with_backoff", new_callable=AsyncMock)
async def test_fallback_routing_on_error(mock_call):
    mock_success_response = type("Obj", (object,), {
        "choices": [type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ از مدل جایگزین"})()})()]
    })()
    mock_call.side_effect = [
        Exception("403 Forbidden - Access Denied"),
        mock_success_response
    ]
    response = await get_ai_response("تست مسیریابی")
    assert response == "پاسخ از مدل جایگزین"
    assert mock_call.call_count == 2

@pytest.mark.asyncio
@patch("app.core.ai_proxy.call_model_with_backoff")
async def test_load_20_concurrent_requests(mock_call):
    mock_success = type("Obj", (object,), {
        "choices": [type("Obj", (object,), {"message": type("Obj", (object,), {"content": "پاسخ"})()})()]
    })()
    mock_call.return_value = mock_success
    
    tasks = [get_ai_response(f"تست فشار شماره {i}") for i in range(20)]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 20
    assert mock_call.call_count == 20
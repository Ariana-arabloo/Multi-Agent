import pytest
import httpx
import json

@pytest.mark.asyncio
async def test_sse_stream_continuous_data():
    # وصل شدن به سرور واقعی که روی پورت 8000 روشن است
    url = "http://127.0.0.1:8000/api/v1/projects/test-123/stream"
    
    # تنظیم تایم‌اوت 10 ثانیه‌ای تا تست تحت هیچ شرایطی گیر نکند
    timeout = httpx.Timeout(10.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream("GET", url) as response:
            assert response.status_code == 200
            
            event_count = 0
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data_content = line.replace("data: ", "")
                    parsed_data = json.loads(data_content)
                    assert "status" in parsed_data
                    event_count += 1
                    
                # خروج از حلقه بعد از دریافت موفق 2 پیام
                if event_count >= 2:
                    break
            
            assert event_count == 2
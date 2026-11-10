from temporalio import activity
import httpx

@activity.defn
async def call_litellm_activity(prompt: str) -> str:
    litellm_url = "http://localhost:4000/chat/completions"
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(litellm_url, json=payload, timeout=60.0)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
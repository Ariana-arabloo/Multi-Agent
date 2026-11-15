from openai import OpenAI
from pydantic import ValidationError
from schemas import ProgrammerOutput

client = OpenAI(api_key="YOUR_API_KEY")

def generate_code_with_structured_output():
    messages = [
        {"role": "system", "content": "You are a professional Python programmer. Output strictly in JSON."},
        {"role": "user", "content": "Write a function to add two numbers."}
    ]
    
    for attempt in range(3):
        print(f"--- Attempt {attempt + 1} ---")
        
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        ai_text = response.choices[0].message.content
        
        try:
            result = ProgrammerOutput.model_validate_json(ai_text)
            print("Success! JSON is valid.")
            return result
            
        except ValidationError as e:
            print("Pydantic Error! Sending back to AI for fixing...")
            
            messages.append({"role": "assistant", "content": ai_text})
            messages.append({
                "role": "user", 
                "content": f"Your JSON was invalid. Here is the Pydantic error:\n{e}\nPlease fix it."
            })
            
    print("Not Done")
    return None
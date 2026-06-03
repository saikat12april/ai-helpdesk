import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(prompt: str, context: str = "") -> str:
    print(f"DEBUG: Using GROQ_API_KEY: {'[SET]' if GROQ_API_KEY else '[MISSING]'}")
    
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is missing."
        
    system_prompt = "You are an expert IT Helpdesk Assistant. Provide clear, concise, and accurate technical support."
    if context:
        system_prompt += f"\n\nCONTEXT:\n{context}"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"DEBUG: Groq API Error Body: {response.text}")
            return f"Groq API Error: {response.status_code}"
    except Exception as e:
        print(f"DEBUG: Exception: {str(e)}")
        return f"Connection Error: {str(e)}"
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-3-8b-instruct")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_haiku(prompt, system_instruction=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 100
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Error generating haiku:", response.text)
        return "Haiku generation failed."

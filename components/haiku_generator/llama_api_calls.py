import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL_ID = os.getenv("LLAMA_MODEL_ID", "llama-3.1-8b-instant")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_haiku(prompt, system_instruction=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    if isinstance(prompt, list):
        prompt = "\n\n".join(prompt)

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": LLAMA_MODEL_ID,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 300
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Error generating haiku:", response.text)
        return "Haiku generation failed."
    

def classify_emotion_via_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "user", "content": prompt}
    ]

    payload = {
        "model": LLAMA_MODEL_ID,
        "messages": messages,
        "temperature": 0.0,        #deterministic
        "max_tokens": 200          
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        response_text = result["choices"][0]["message"]["content"].strip()
        
        parsed = json.loads(response_text)
        emotion = parsed.get("emotion", "neutral")
        confidence = parsed.get("confidence", 0.5)
        #print(response_text)
        #print("Hello.")
        return emotion, confidence

    except Exception as e:
        print("Error classifying emotion:", response.text)
        return "neutral", 0.5  # fallback if anything fails

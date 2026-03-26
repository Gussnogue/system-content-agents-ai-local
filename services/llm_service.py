import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.url = os.getenv("LM_STUDIO_CHAT_URL")
        self.model = os.getenv("LLM_MODEL_NAME", "hermes-3-llama-3.2-3b")

    def generate(self, prompt, max_tokens=800, temperature=0.7):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        start = time.time()
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            latency = (time.time() - start) * 1000
            return data["choices"][0]["message"]["content"], latency
        except Exception as e:
            return f"Erro: {e}", 0
        
        
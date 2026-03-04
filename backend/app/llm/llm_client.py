# app/llm/llm_client.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # load .env variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
# supported_models = client.list_models()
# print(supported_models)

# LLM wrapper
# llama3-8b-8192
class GroqLLM:
    def __init__(self, model: str = "llama-3.1-8b-instant", temperature: float = 0.3, max_tokens: int = 2048):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def invoke(self, prompt: str) -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content


llm = GroqLLM()


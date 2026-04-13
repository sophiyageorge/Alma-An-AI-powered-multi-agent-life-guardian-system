"""
LLM Client Wrapper
------------------
Optimized for single-day generation to stay within Groq TPM limits.
"""

import os
import logging
import json
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# -----------------------------
# API Key Setup
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY not found in environment")
    raise RuntimeError("GROQ_API_KEY not found in environment")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# LLM Wrapper Class
# -----------------------------
class GroqLLM:
    """
    Wrapper for Groq LLM client.
    
    Optimized for JSON generation on the Groq Free Tier.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant", temperature: float = 0.1, max_tokens: int = 2000):
        self.model = model
        self.temperature = temperature  # Lower temperature is better for strict JSON
        self.max_tokens = max_tokens
        self.tpm_limit = 6000 
        logger.info(f"GroqLLM initialized | model={self.model}")

    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4

    def invoke(self, prompt: str) -> str:
        """
        Sends prompt to LLM and returns the raw string content.
        Includes a safeguard for the 6000 TPM limit.
        """
        system_prompt = "You are a professional assistant that outputs only valid JSON."
        
        estimated_input = self._estimate_tokens(system_prompt + prompt)
        
        # Prevent 413 error by capping the request
        if (estimated_input + self.max_tokens) > self.tpm_limit:
            actual_max = max(500, self.tpm_limit - estimated_input - 100)
            logger.warning(f"Input large ({estimated_input}). Reducing max_tokens to {actual_max}")
        else:
            actual_max = self.max_tokens

        try:
            logger.info(f"Invoking LLM for Day Plan...")
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=actual_max,
                response_format={"type": "json_object"} # Forces Groq to return JSON
            )
            
            content = response.choices[0].message.content
            return content

        except Exception as e:
            logger.error(f"LLM API Call failed: {str(e)}")
            raise RuntimeError(f"LLM failure: {e}")

# -----------------------------
# Singleton instance
# -----------------------------
llm = GroqLLM()
"""
LLM Client Wrapper
------------------

Provides a wrapper around the Groq LLM API for generating
AI completions. Designed to be reusable across agents
(e.g., Nutrition, Exercise, Mental Health).
"""

import os
import logging
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

# -----------------------------
# Initialize Groq Client
# -----------------------------
client = Groq(api_key=GROQ_API_KEY)
logger.info("Groq client initialized successfully")


# -----------------------------
# LLM Wrapper Class
# -----------------------------
class GroqLLM:
    """
    Wrapper for Groq LLM client with convenient defaults.

    Attributes:
        model (str): Model name to use.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum tokens to generate.
    """

    def __init__(self, model: str = "llama-3.1-8b-instant", temperature: float = 0.3, max_tokens: int = 8000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info(f"GroqLLM initialized | model={self.model}, temperature={self.temperature}, max_tokens={self.max_tokens}")

    def invoke(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and return the generated response.

        Args:
            prompt (str): The user input or instruction for the LLM.

        Returns:
            str: Generated text from the model.

        Raises:
            RuntimeError: If the API call fails.
        """
        try:
            logger.info(f"Invoking LLM | model={self.model} | prompt_length={len(prompt)}")
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            result = response.choices[0].message.content
            logger.info(f"LLM response received | length={len(result)}")
            return result

        except Exception as e:
            logger.exception("Failed to invoke LLM")
            raise RuntimeError(f"LLM invocation failed: {str(e)}") from e


# -----------------------------
# Singleton instance
# -----------------------------
llm = GroqLLM()


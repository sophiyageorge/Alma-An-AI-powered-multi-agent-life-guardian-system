from app.llm.llm_client import GroqLLM  # or wherever your wrapper is
from dotenv import load_dotenv

load_dotenv()  # ensure .env is loaded

def test_groq_key():
    """
    Simple manual test to verify that the GROQ API key works
    and the LLM responds.
    """
    try:
        llm = GroqLLM()
        prompt = "Hello, can you respond with a short greeting?"
        response = llm.invoke(prompt)
        print("✅ GROQ API key works! Response:")
        print(response)
    except Exception as e:
        print("❌ GROQ test failed:", str(e))


if __name__ == "__main__":
    test_groq_key()
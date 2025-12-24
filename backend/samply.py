# hf_llm.py
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint

# Load environment variables from .env
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_API_KEY:
    raise ValueError("Hugging Face API key not found in .env as HUGGINGFACEHUB_API_TOKEN")

# Model repository
MODEL_REPO = "meta-llama/Meta-Llama-3-8B-Instruct"

# Initialize LLM endpoint
llm = HuggingFaceEndpoint(
    repo_id=MODEL_REPO,
    task="conversational",           # correct for chat/instruction models
    huggingfacehub_api_token=HF_API_KEY,
    temperature=0.7,
    max_new_tokens=200
)

def test_llm(prompt: str):
    """Simple test for your LLM."""
    try:
        return llm.invoke(prompt)
    except Exception as e:
        return f"Error invoking LLM: {e}"

# Only run this block if executing the file directly
if __name__ == "__main__":
    prompt = "Write a friendly greeting in one sentence."
    response = test_llm(prompt)
    print("\n--- Model Response ---")
    print(response)

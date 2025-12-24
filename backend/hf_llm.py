# hf_llm.py
from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL_REPO = "HuggingFaceH4/zephyr-7b-beta"

# Base Hugging Face conversational endpoint
_base_llm = HuggingFaceEndpoint(
    repo_id=MODEL_REPO,
    task="conversational",
    huggingfacehub_api_token=HF_API_KEY,
    max_new_tokens=120,
    temperature=0.4,
)

# Chat-ready LLM for LangChain / LangGraph
llm = ChatHuggingFace(llm=_base_llm)

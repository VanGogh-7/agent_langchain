from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

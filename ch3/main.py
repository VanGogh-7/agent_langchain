import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import TokenTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel


project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

book_path = project_root / "data" / "Moby-Dick.txt"

with open(book_path, "r", encoding="utf-8") as f:
    moby_dick_book = f.read()


text_splitter = TokenTextSplitter(
    chunk_size=3000,
    chunk_overlap=100,
)

text_chunks_chain = RunnableLambda(
    lambda text: [
        {"chunk": chunk}
        for chunk in text_splitter.split_text(text)
    ]
)

summarize_chunk_prompt = PromptTemplate.from_template(
    """
Summarize the following passage concisely.

Include:
- main events
- important characters
- key details

Text:
{chunk}
"""
)

summarize_chunk_chain = summarize_chunk_prompt | llm | StrOutputParser()

summarize_map_chain = RunnableParallel(
    {
        "summary": summarize_chunk_chain
    }
)

summarize_summaries_prompt = PromptTemplate.from_template(
    """
Write a concise final summary based on the following partial summaries.

Keep the main plot, characters, conflicts, and important details.

Text:
{summaries}
"""
)

summarize_reduce_chain = (
        RunnableLambda(
            lambda mapped_results: {
                "summaries": "\n\n".join(
                    item["summary"] for item in mapped_results
                )
            }
        )
        | summarize_summaries_prompt
        | llm
        | StrOutputParser()
)

map_reduce_chain = (
        text_chunks_chain
        | summarize_map_chain.map()
        | summarize_reduce_chain
)

summary = map_reduce_chain.invoke(moby_dick_book)

print(summary)

"""Builds a LangGraph agent that can search your ingested docs to answer questions.

The agent gets one tool -- search_docs -- and decides for itself whether a given
question needs a lookup. See modules/04-agents and modules/06-rag for how this works.
"""

import os
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent

PERSIST_DIR = Path(__file__).parent / "chroma_db"

SYSTEM_PROMPT = (
    "You answer questions using the search_docs tool whenever the question could be "
    "about the user's documents. If the tool doesn't return a relevant answer, say so "
    "instead of guessing."
)


def build_agent():
    if not PERSIST_DIR.exists():
        raise RuntimeError(
            f"No index found at {PERSIST_DIR}. Run `python ingest.py` first."
        )

    embeddings = OpenAIEmbeddings(
        base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("EMBED_MODEL", "nomic-embed-text"),
        api_key="not-needed",
        check_embedding_ctx_length=False,
    )
    store = Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embeddings)
    retriever = store.as_retriever(search_kwargs={"k": 3})

    retriever_tool = create_retriever_tool(
        retriever,
        name="search_docs",
        description="Search the user's ingested documents for relevant passages.",
    )

    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        api_key="not-needed",
        temperature=0,
    )

    return create_react_agent(llm, tools=[retriever_tool], prompt=SYSTEM_PROMPT)


def ask(agent, question: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content

"""A router decides, per question, whether to send it to a docs specialist or a
chitchat specialist. Reuses the flagship project's ingested Chroma index.

Run ingest.py in projects/chat-with-your-docs first if you haven't already.
Run: python 07-multi-agent-orchestration/supervisor_demo.py
"""

import json
import os
from pathlib import Path
from typing import Literal

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from dotenv import load_dotenv
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

FLAGSHIP_DIR = Path(__file__).parent.parent.parent / "projects" / "chat-with-your-docs"
CHROMA_DIR = FLAGSHIP_DIR / "chroma_db"


class Route(BaseModel):
    route: Literal["docs", "chitchat"]


def build_router():
    client = OpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key="not-needed",
    )
    model = os.environ.get("LLM_MODEL", "llama3.2:3b")

    def route(question: str) -> str:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        'Classify the question as {"route": "docs"} if it could be about '
                        'a company handbook, product FAQ, or team directory, otherwise '
                        '{"route": "chitchat"}. Reply with only that JSON.'
                    ),
                },
                {"role": "user", "content": question},
            ],
            response_format={"type": "json_object"},
        )
        return Route.model_validate(json.loads(response.choices[0].message.content)).route

    return route


def build_docs_agent(llm):
    if not CHROMA_DIR.exists():
        raise RuntimeError(f"No index found at {CHROMA_DIR}. Run ingest.py in {FLAGSHIP_DIR} first.")

    embeddings = OpenAIEmbeddings(
        base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("EMBED_MODEL", "nomic-embed-text"),
        api_key="not-needed",
        check_embedding_ctx_length=False,
    )
    store = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)
    retriever_tool = create_retriever_tool(
        store.as_retriever(search_kwargs={"k": 3}),
        name="search_docs",
        description="Search the ingested documents for relevant passages.",
    )
    return create_react_agent(llm, tools=[retriever_tool])


def answer(question: str, route_fn, docs_agent, chitchat_llm) -> tuple[str, str]:
    picked = route_fn(question)
    if picked == "docs":
        result = docs_agent.invoke({"messages": [{"role": "user", "content": question}]})
        return picked, result["messages"][-1].content
    return picked, chitchat_llm.invoke(question).content


def main():
    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        api_key="not-needed",
        temperature=0,
    )

    route_fn = build_router()
    docs_agent = build_docs_agent(llm)

    for question in [
        "How many vacation days do employees get?",
        "What's a fun fact about octopuses?",
    ]:
        picked, response = answer(question, route_fn, docs_agent, llm)
        print(f"Q: {question}\n  -> routed to: {picked}\n  -> {response}\n")


if __name__ == "__main__":
    main()

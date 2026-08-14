"""Runs a small test set against the flagship project's agent, checks each answer for
the expected fact, and reports timing/token usage plus an illustrative cost comparison.

Run ingest.py in projects/chat-with-your-docs first if you haven't already.
Run: python 08-evaluation-and-cost-comparison/eval.py
"""

import os
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from dotenv import load_dotenv
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent

load_dotenv()

FLAGSHIP_DIR = Path(__file__).parent.parent.parent / "projects" / "chat-with-your-docs"
CHROMA_DIR = FLAGSHIP_DIR / "chroma_db"

# Illustrative cloud API pricing (per million tokens) -- update from your provider's
# current pricing page before treating these as anything but a rough shape of the tradeoff.
CLOUD_INPUT_PER_M = 3.00
CLOUD_OUTPUT_PER_M = 15.00

TEST_CASES = [
    ("How many vacation days do employees get per year?", "18"),
    ("How long does the Home Hub battery last during a power outage?", "14"),
    ("Who leads the support team?", "Lena Fischer"),
    ("How many days can employees work remotely without approval?", "3"),
]


def build_agent():
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
    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        api_key="not-needed",
        temperature=0,
    )
    return create_react_agent(llm, tools=[retriever_tool])


def run_case(agent, question: str, expected: str):
    start = time.perf_counter()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    elapsed = time.perf_counter() - start

    answer = result["messages"][-1].content
    passed = expected.lower() in answer.lower()

    input_tokens = output_tokens = 0
    for message in result["messages"]:
        if isinstance(message, AIMessage) and message.usage_metadata:
            input_tokens += message.usage_metadata.get("input_tokens", 0)
            output_tokens += message.usage_metadata.get("output_tokens", 0)

    return {
        "question": question,
        "passed": passed,
        "elapsed": elapsed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def main():
    agent = build_agent()
    results = [run_case(agent, q, expected) for q, expected in TEST_CASES]

    print(f"{'PASS' if all(r['passed'] for r in results) else 'FAIL'} overall\n")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['elapsed']:.1f}s  {r['question']}")

    total_input = sum(r["input_tokens"] for r in results)
    total_output = sum(r["output_tokens"] for r in results)
    total_time = sum(r["elapsed"] for r in results)

    print(f"\nTotal: {total_time:.1f}s, {total_input} input tokens, {total_output} output tokens")

    if total_input or total_output:
        cloud_estimate = (total_input / 1_000_000 * CLOUD_INPUT_PER_M) + (
            total_output / 1_000_000 * CLOUD_OUTPUT_PER_M
        )
        print(f"Local cost: $0.00 (electricity only)")
        print(
            f"Illustrative cloud cost for the same run at "
            f"${CLOUD_INPUT_PER_M}/M input + ${CLOUD_OUTPUT_PER_M}/M output tokens: "
            f"${cloud_estimate:.5f}"
        )
        print("Re-run this script repeatedly: the local cost stays $0 every time; the cloud estimate does not.")
    else:
        print("No token usage reported by this runtime -- cost comparison skipped.")


if __name__ == "__main__":
    main()

"""Builds a LangGraph agent with three tools over a folder of your own files:
read one file, semantically search all of them, or extract a runtime-chosen set of
fields from every file into a CSV. Which tool(s) get used is decided per conversation
by the agent -- there's no fixed schema baked in ahead of time.
"""

import csv
import json
import os
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from openai import OpenAI
from pydantic import create_model, ValidationError

INPUT_DIR = Path(os.environ.get("INPUT_DIR", "input_docs"))
INPUT_GLOB = os.environ.get("INPUT_GLOB", "*.txt")
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "output"))
PERSIST_DIR = Path(__file__).parent / "chroma_db"

SYSTEM_PROMPT = """You help the user work with a folder of their own documents.

Use search_docs when they ask a question but you don't know which file has the answer.
Use read_file when they name one specific file.
Use extract_structured when they want ONE output file built from ALL documents, with
specific fields pulled out of each one -- figure out the field names from what they
asked for (ask them to clarify if it's genuinely ambiguous), then call the tool once
with that full field list and a sensible output filename ending in .csv.

A tool's result is ground truth. If search_docs or read_file returns an answer to the
question, use that exact information in your reply -- never say you don't have the
information after a tool already gave it to you.
"""


def _raw_client() -> OpenAI:
    return OpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key="not-needed",
    )


def _model_name() -> str:
    return os.environ.get("LLM_MODEL", "llama3.2:3b")


@tool
def read_file(filename: str) -> str:
    """Read the raw contents of one specific file by name from the input folder."""
    path = (INPUT_DIR / filename).resolve()
    if INPUT_DIR.resolve() not in path.parents and path != INPUT_DIR.resolve():
        return "Error: can only read files inside the input folder."
    if not path.is_file():
        return f"Error: {filename} not found."
    return path.read_text()


def _build_extract_structured_tool():
    @tool
    def extract_structured(fields: list[str], output_filename: str) -> str:
        """Extract the given field names from every file in the input folder and write
        one CSV row per file to output_filename (e.g. "customers.csv"). Use this only
        when the user wants a single structured file built from ALL documents, not just
        an answer about one."""
        client = _raw_client()
        model = _model_name()

        row_model = create_model(
            "ExtractedRow", **{name: (str | None, None) for name in fields}
        )
        field_template = json.dumps({name: "<value or null>" for name in fields}, indent=2)
        system_prompt = (
            "You extract structured fields from a document.\n"
            "Always reply with a single JSON object with exactly these keys, replacing\n"
            "each placeholder with the actual value found in the text:\n"
            f"{field_template}\n"
            "Use null for any field not present in the text. Do not invent values that aren't there."
        )

        files = sorted(INPUT_DIR.rglob(INPUT_GLOB))
        if not files:
            return f"No files matching {INPUT_GLOB} found in {INPUT_DIR}."

        rows = []
        failures = []
        for path in files:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": path.read_text()},
            ]
            record = None
            for attempt in range(2):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0,
                )
                raw = response.choices[0].message.content
                try:
                    record = row_model.model_validate(json.loads(raw))
                    break
                except (json.JSONDecodeError, ValidationError) as e:
                    if attempt == 0:
                        messages.append({"role": "assistant", "content": raw})
                        messages.append(
                            {"role": "user", "content": f"That didn't match the required shape ({e}). Try again."}
                        )
                        continue
                    failures.append(str(path.relative_to(INPUT_DIR)))
            if record is not None:
                rows.append({"source_file": str(path.relative_to(INPUT_DIR)), **record.model_dump()})

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / output_filename
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["source_file", *fields])
            writer.writeheader()
            writer.writerows(rows)

        summary = f"Wrote {len(rows)}/{len(files)} rows to {output_path}."
        if failures:
            summary += f" Failed after retry: {failures}."
        return summary

    return extract_structured


def build_agent():
    if not PERSIST_DIR.exists():
        raise RuntimeError(f"No index found at {PERSIST_DIR}. Run `python ingest.py` first.")

    embeddings = OpenAIEmbeddings(
        base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("EMBED_MODEL", "nomic-embed-text"),
        api_key="not-needed",
        check_embedding_ctx_length=False,
    )
    store = Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embeddings)
    retriever_tool = create_retriever_tool(
        store.as_retriever(search_kwargs={"k": 3}),
        name="search_docs",
        description="Search the input folder's documents for relevant passages when you don't know which file has the answer.",
        document_prompt=PromptTemplate.from_template("Source: {source}\n{page_content}"),
    )

    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=_model_name(),
        api_key="not-needed",
        temperature=0,
    )

    tools = [retriever_tool, read_file, _build_extract_structured_tool()]
    return create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)


def ask(agent, question: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"recursion_limit": 15},
    )
    return result["messages"][-1].content

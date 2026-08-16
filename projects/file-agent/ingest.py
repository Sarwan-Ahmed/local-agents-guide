"""Loads input_docs/*.txt, chunks them, embeds them locally, and persists to a Chroma store.

Run once before main.py: `python ingest.py`
Re-run any time you change the contents of input_docs/ (or point INPUT_DIR at your own folder).
"""

import os
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

INPUT_DIR = Path(os.environ.get("INPUT_DIR", "input_docs"))
INPUT_GLOB = os.environ.get("INPUT_GLOB", "*.txt")
PERSIST_DIR = Path(__file__).parent / "chroma_db"


def load_documents():
    docs = []
    for path in sorted(INPUT_DIR.glob(INPUT_GLOB)):
        docs.extend(TextLoader(str(path)).load())
    return docs


def main():
    documents = load_documents()
    print(f"Loaded {len(documents)} document(s) from {INPUT_DIR}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = OpenAIEmbeddings(
        base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("EMBED_MODEL", "nomic-embed-text"),
        api_key="not-needed",
        check_embedding_ctx_length=False,
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
    )
    print(f"Stored embeddings in {PERSIST_DIR}")


if __name__ == "__main__":
    main()

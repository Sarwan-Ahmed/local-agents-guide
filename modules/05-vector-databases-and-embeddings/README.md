# 05 — Vector databases & embeddings

🚧 **Outline only — full write-up and code coming in a future pass.**

## What you'll learn

What an embedding actually is, and what a vector database gives you beyond a regular database — the two pieces RAG is built from.

## Planned outline

- Embeddings as "meaning as a list of numbers": similar sentences produce nearby vectors, dissimilar ones produce distant vectors
- Generating embeddings locally with Ollama's `nomic-embed-text` (already used in the flagship project — this module explains what it was doing)
- Similarity search: cosine similarity in a few lines of plain Python, on ~10 example sentences, before touching a real vector DB
- Why a regular database can't do this efficiently at scale, and what a vector DB (Chroma, in this repo) indexes to make nearest-neighbor search fast
- Chunking: why documents get split into smaller pieces before embedding, and how chunk size/overlap affects retrieval quality
- Alternatives worth knowing: FAISS (library, not a DB), LanceDB, pgvector (Postgres extension) — one line each on when you'd reach for them instead of Chroma

## Prerequisite

[Module 00 — Fundamentals](../00-fundamentals/) (no agent/tool knowledge needed for this one)

## Next

[Module 06 — RAG →](../06-rag/)

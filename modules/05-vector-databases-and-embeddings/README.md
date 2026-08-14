# 05 — Vector databases & embeddings

Goal: understand what an embedding actually is, and what a vector database gives you beyond a plain list of numbers you compare by hand. This module has no agent/tool prerequisite — it only needs [module 00](../00-fundamentals/)'s vocabulary.

## Embeddings: meaning as a list of numbers

An embedding model turns text into a fixed-length list of numbers (a **vector**) such that texts with similar meaning end up as nearby vectors, and dissimilar texts end up far apart. "Nearby" is measured with **cosine similarity** — a value from -1 to 1, where 1 means "pointing in the same direction" (same meaning), 0 means unrelated, and -1 means opposite.

This repo uses Ollama's `nomic-embed-text` for embeddings — note it's a different kind of model from `llama3.2:3b`: it only turns text into vectors, it doesn't chat or generate text.

## Part 1 — similarity search with no database at all

[`similarity_demo.py`](similarity_demo.py) embeds 10 short sentences, embeds one query sentence, and ranks all 10 by cosine similarity to the query — using nothing but Python and `numpy`. This is the entire idea behind retrieval, before any database is involved.

```bash
cd modules
source .venv/bin/activate
python 05-vector-databases-and-embeddings/similarity_demo.py
```

Expected output: the query sentence, followed by all 10 sentences ranked by similarity score — the most related ones (by meaning, not shared keywords) should land at the top.

## Part 2 — why you need an actual vector database

The script above compares the query against every sentence, one at a time — fine for 10 sentences, unworkable for 100,000 documents. A **vector database** (Chroma, in this repo) indexes embeddings so it can find the nearest ones quickly without scanning everything, and it persists them to disk so you don't re-embed your documents on every run.

[`chroma_demo.py`](chroma_demo.py) stores the same 10 sentences in a local Chroma collection and runs the same query through it, to show the same result coming from a real vector DB instead of hand-rolled cosine similarity. The printed numbers won't match `similarity_demo.py` exactly — Chroma's default distance metric is a different scale (lower = closer, instead of higher = closer for cosine similarity) — but the top-ranked sentences should agree.

```bash
python 05-vector-databases-and-embeddings/chroma_demo.py
```

## Chunking (why this matters once you move to real documents)

Real documents are longer than one sentence, so they get split into smaller **chunks** before embedding — otherwise one giant embedding represents an entire document too vaguely to match specific questions well. Two settings control this:

- **Chunk size** — how much text per chunk. Too large: retrieval becomes vague. Too small: a chunk may lose context it needs.
- **Chunk overlap** — how much adjacent chunks share, so a sentence that spans a chunk boundary isn't lost from both sides.

The flagship project's `ingest.py` (`projects/chat-with-your-docs/ingest.py`) uses `chunk_size=500, chunk_overlap=50` — module 06 explains that choice in context.

## Alternatives to Chroma, briefly

- **FAISS** — a similarity-search *library*, not a database; faster for huge in-memory collections, but you manage persistence/metadata yourself.
- **LanceDB** — similar embedded-database model to Chroma, columnar storage, good for larger local datasets.
- **pgvector** — a Postgres extension; the right choice if you already run Postgres and want vectors alongside your regular relational data.

## Prerequisite

[Module 00 — Fundamentals](../00-fundamentals/)

## Next

[Module 06 — RAG →](../06-rag/)

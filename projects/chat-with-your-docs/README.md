# Chat with your own docs — a local RAG agent

A working agent that answers questions about your own files, using nothing but your laptop: no API keys, no cloud calls, no per-token billing.

```
question
   │
   ▼
┌─────────────┐        "does this need         ┌──────────────┐
│  LangGraph   │──────  a document lookup?" ───▶│ search_docs  │
│    agent     │◀────────  retrieved chunks ────│    tool      │
│ (local LLM)  │                                 └──────┬───────┘
└──────┬───────┘                                        │
       │                                                 ▼
       ▼                                          ┌──────────────┐
    answer                                        │  Chroma DB   │
                                                   │ (local, on   │
                                                   │  your disk)  │
                                                   └──────────────┘
```

The agent decides for itself, per question, whether it needs to search your documents — it isn't forced to retrieve on every turn.

## What's in `sample_docs/`

Three short, clearly-fictional `.md` files (a company handbook, a product FAQ, a team directory) so you can try this immediately without providing your own content. Once it's working, delete them and drop in your own notes, PDFs-converted-to-text, or a codebase's `.md` files instead.

## Setup

1. Make sure [module 01](../../modules/01-running-models-locally/) is done: Ollama running, `llama3.2:3b` and `nomic-embed-text` pulled.
2. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # defaults already match Ollama, edit only if using a different runtime
```

## Run it

```bash
python ingest.py   # builds the local vector index from sample_docs/ -- run once, or whenever sample_docs/ changes
python main.py      # starts the chat loop
```

Try asking:

- "How many vacation days do I get?"
- "How long does the Home Hub's battery last during an outage?"
- "Who leads the support team?"

Each answer should be grounded in the matching sample doc, not the model's own guess — that's the RAG pipeline working.

## How it maps to the code

| File | Role |
|---|---|
| `ingest.py` | Loads `sample_docs/*.md`, splits into chunks, embeds them via Ollama's `nomic-embed-text`, stores in a local Chroma DB (`chroma_db/`, created on first run) |
| `agent.py` | Builds a LangGraph ReAct agent with one tool (`search_docs`, backed by the Chroma retriever) and a chat model pointed at your local runtime |
| `main.py` | A CLI REPL that feeds your questions to the agent and prints its answers |

Both the chat model and the embedding model are configured via `LLM_BASE_URL`/`LLM_MODEL` and `EMBED_BASE_URL`/`EMBED_MODEL` in `.env` — see [docs/choosing-a-runtime.md](../../docs/choosing-a-runtime.md) to point this at LM Studio or llama.cpp instead of Ollama.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `RuntimeError: No index found at .../chroma_db` | Run `python ingest.py` before `python main.py` |
| Connection refused / timeout talking to `localhost:11434` | Ollama isn't running — run `ollama serve` |
| `model not found` type errors | The model in `.env` hasn't been pulled — `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text` |
| Answers ignore the docs / seem made up | Check `ingest.py` actually ran without errors and `chroma_db/` exists and isn't empty |
| First response is very slow | Normal — Ollama loads the model into memory on first use each session; later questions are faster |

## Next

Once this works, go deepen your understanding of each piece: [Module 04 — Agents](../../modules/04-agents/), [Module 05 — Vector databases & embeddings](../../modules/05-vector-databases-and-embeddings/), [Module 06 — RAG](../../modules/06-rag/).

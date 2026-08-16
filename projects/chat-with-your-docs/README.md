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

## Run with Docker (recommended — no local Python or Ollama install needed)

Needs only Docker Desktop (or Docker Engine + Compose) installed.

```bash
cd projects/chat-with-your-docs
docker compose up -d ollama                          # starts a local Ollama server in a container
docker compose exec ollama ollama pull llama3.2:3b        # one-time, cached in a Docker volume
docker compose exec ollama ollama pull nomic-embed-text   # one-time, cached in a Docker volume
docker compose run --rm --build app                   # builds the vector index (first run only) and starts the chat REPL
```

The model pulls only need to happen once — they're stored in a Docker volume (`ollama_data`) that survives container restarts. The vector index (`chroma_db`) is likewise cached in its own volume, and only gets rebuilt if it's missing, so later runs skip straight to the chat prompt.

Try asking the same questions as below. To use your own documents instead of `sample_docs/`, either replace the files in that folder, or edit the `./sample_docs:/app/sample_docs` line in `docker-compose.yml` to mount a different folder — then force a re-index with `docker compose down -v && docker compose run --rm --build app`.

## Run without Docker

1. Make sure [module 01](../../modules/01-running-models-locally/) is done: Ollama running, `llama3.2:3b` and `nomic-embed-text` pulled.
2. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # defaults already match Ollama, edit only if using a different runtime
```

3. Run it:

```bash
python ingest.py   # builds the local vector index from sample_docs/ -- run once, or whenever sample_docs/ changes
python main.py      # starts the chat loop
```

## Try asking

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
| `RuntimeError: No index found at .../chroma_db` | Run `python ingest.py` before `python main.py` (without Docker) |
| Connection refused / timeout talking to `localhost:11434` | Without Docker: Ollama isn't running — run `ollama serve`. With Docker: run `docker compose up -d ollama` first |
| `model not found` type errors | The model hasn't been pulled yet — `ollama pull llama3.2:3b` / `nomic-embed-text` (or the `docker compose exec ollama ollama pull ...` equivalent) |
| Answers ignore the docs / seem made up | Check `ingest.py` ran without errors and `chroma_db/` (or the `chroma_data` volume) isn't empty |
| First response is very slow | Normal — Ollama loads the model into memory on first use each session; later questions are faster |
| Docker: schema/code changes don't seem to take effect | Rebuild the image — use `docker compose run --rm --build app` rather than plain `run`, or `docker compose build` |

## Next

Once this works, go deepen your understanding of each piece: [Module 04 — Agents](../../modules/04-agents/), [Module 05 — Vector databases & embeddings](../../modules/05-vector-databases-and-embeddings/), [Module 06 — RAG](../../modules/06-rag/).

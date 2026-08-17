# File agent — ask questions or extract structured data, decided at runtime

A single local agent over a folder of your own files that doesn't force you to decide ahead of
time what you're doing with them. Ask it a question about one specific file, ask it something
you'd need to search across all of them to answer, or ask it to build a structured CSV out of
every file with whatever fields you name in the moment — it picks the right approach per request.
Runs entirely on your own machine: no API keys, no cloud calls, no per-token billing.

```
your message
     │
     ▼
┌─────────────┐     "which tool does this need?"      ┌───────────────┐
│  LangGraph   │───────────────────────────────────────▶  read_file    │  one specific file, by name
│    agent     │                                        ├───────────────┤
│ (local LLM)  │◀───────────────────────────────────────┤  search_docs  │  semantic search, unknown file
└──────┬───────┘                                        ├───────────────┤
       │                                                 │  extract_     │  runtime field list, ALL
       ▼                                                 │  structured   │  files → one CSV
    answer, or                                           └───────────────┘
    "wrote N rows to output/whatever.csv"
```

Unlike a fixed extraction schema decided ahead of time (module 02's approach), `extract_structured`'s
field list is whatever you ask for in that conversation — the agent builds the extraction prompt on
the fly instead of reading it from a Python file.

## What's in `input_docs/`

Ten short, clearly-fictional customer records in different formats (a form, call notes, terse
notes) — a stand-in for "100 real files in a specific format" without using real data. Three of
them are deliberately missing one field, so you can check the agent reports it as empty rather
than inventing a value. One (`archived/customer_009.txt`) is nested in a subfolder, to prove all
three tools actually search/read/extract recursively rather than just the top-level folder —
`INPUT_DIR.rglob(INPUT_GLOB)`, not `.glob(...)`, is what makes that work. One (`customer_010.log`)
is a different extension, deliberately *excluded* by the default `INPUT_GLOB` — see below. Once
it works, replace these with your own files (see "Using this on real data" below).

### Mixing file extensions

`INPUT_GLOB` defaults to `*.txt`, which is why `customer_010.log` above doesn't show up in
`ingest.py`'s file count or an `extract_structured` run until you opt in. It accepts a
comma-separated list of patterns, so a folder with both `.txt` and `.log` files (for example)
works by setting, in `.env` or `docker-compose.yml`'s `environment:`:

```
INPUT_GLOB=*.txt,*.log
```

Try it: re-ingest with that set and ask about Sofia Ricci (in `customer_010.log`) — she won't be
found until `INPUT_GLOB` includes `*.log`.

Every tool (`ingest.py`, `search_docs`, `extract_structured`) resolves the file list the same
way, so you only need to set this once. `read_file` doesn't use `INPUT_GLOB` at all — it reads
whatever filename it's given directly, any extension, as long as it's a plain text file.

## Run with Docker (recommended — no local Python or Ollama install needed)

```bash
cd projects/file-agent
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.2:3b
docker compose exec ollama ollama pull nomic-embed-text
docker compose run --rm --build app
```

First run builds the vector index from `input_docs/` (needed for `search_docs`) and drops you
into the chat prompt; later runs skip straight to chatting since the index persists in a Docker
volume. `input_docs/` and `output/` mount straight from this folder, so files you extract land on
your normal filesystem.

**Switching to your own files?** The index only rebuilds when it's missing — if you change which
folder `input_docs` points to without clearing the old index, `search_docs` keeps answering from
whatever was ingested before. Clear just the index (not the Ollama models) before pointing
`docker-compose.yml`'s `input_docs` mount at a new folder:

```bash
docker compose down
docker volume rm file-agent_chroma_data
```

Then re-run `docker compose run --rm --build app` — it'll detect the empty index and re-ingest
automatically. (Without Docker: `rm -rf chroma_db && python ingest.py`.)

## Run without Docker

```bash
cd projects/file-agent
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python ingest.py   # builds the vector index -- run once, or whenever input_docs/ changes
python main.py      # starts the chat loop
```

## Try asking

- "What's Priya Kapoor's account number?" (`search_docs` — you don't know which file)
- "Read customer_005.txt" (`read_file` — you know the exact file)
- "Extract full_name, account_number, and email from every file into customers.csv" (`extract_structured` — the field list is entirely yours, decided right now)

Then try a second extraction with a *different* field list in the same session (e.g. add `phone`,
or drop `email`) — nothing needs to be edited or rebuilt for that to work.

## How it maps to the code

| File | Role |
|---|---|
| `ingest.py` | Loads `input_docs/*.txt`, splits into chunks, embeds via `nomic-embed-text`, stores in a local Chroma DB — needed only for the `search_docs` tool |
| `agent.py` | Defines all three tools and builds the LangGraph ReAct agent; `extract_structured` builds a `pydantic.create_model(...)` on the fly from whichever field names it's given, then runs the same JSON-mode + validate + retry-once technique as module 02, once per file |
| `main.py` | CLI REPL that feeds your messages to the agent and prints its answers |

Both models are configured via `LLM_BASE_URL`/`LLM_MODEL` and `EMBED_BASE_URL`/`EMBED_MODEL` — see [docs/choosing-a-runtime.md](../../docs/choosing-a-runtime.md) to point this at LM Studio or llama.cpp instead of Ollama.

## Using this on real data

- **Keep real files outside this git repo.** Without Docker: point `INPUT_DIR` in `.env` at an absolute path elsewhere on disk. With Docker: change the `./input_docs` line in `docker-compose.yml`'s `volumes:` to your real folder, or override it for a one-off run with `docker compose run --rm --build -v /Users/you/private/customer-files:/app/input_docs app`. `output/` is already gitignored, but don't rely on that alone.
- **Check with your organization's data handling process first**, even though everything runs locally — this solves the vendor data-retention problem, not necessarily every other requirement your organization or a client engagement may have for real customer data.
- **Spot-check extraction output.** Small local models don't always extract perfectly, especially for a field list you've never tried before — skim a sample of the output CSV against the source files before trusting a full run.

## Performance expectations

Tested with 8 files on `llama3.2:3b`, CPU-only: a few seconds per file for `extract_structured`, similar for a single lookup question. For "100 files," that's roughly a coffee-break batch job for a full extraction — module 08 covers measuring this properly rather than guessing.

## Prerequisite

[Module 02 — Prompting & structured output](../../modules/02-prompting-and-structured-output/) and [Module 03 — Tool use / function calling](../../modules/03-tool-use-function-calling/)

# Modules 02-08 — setup

Modules 00 and 01 need no Python. From module 02 onward, each module has a small runnable script, and they all share one virtual environment (separate from the flagship project's own venv in `projects/chat-with-your-docs/`).

```bash
cd modules
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # defaults already match Ollama
```

Make sure [module 01](01-running-models-locally/) is done first: Ollama running, `llama3.2:3b` and `nomic-embed-text` pulled.

Then run any module's script directly, e.g.:

```bash
python 02-prompting-and-structured-output/extract.py
```

Each module's own README has the exact command and what output to expect.

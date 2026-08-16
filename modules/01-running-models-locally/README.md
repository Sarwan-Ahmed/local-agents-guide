# 01 — Running models locally

Goal: have a model running on your machine, answering questions over HTTP, before writing any Python.

This module uses [Ollama](https://ollama.com) as the runtime (see [docs/choosing-a-runtime.md](../../docs/choosing-a-runtime.md) if you'd rather use LM Studio or llama.cpp instead — the rest of this repo works the same either way).

## 1. Install Ollama

```bash
# macOS
brew install ollama

# or download the installer from https://ollama.com/download
```

Start the server (the installer usually sets this up to run automatically — if not):

```bash
ollama serve
```

## 2. Pull a model

```bash
ollama pull llama3.2:3b
```

This downloads a ~2GB quantized model. See [docs/choosing-a-model.md](../../docs/choosing-a-model.md) for why this size, and alternatives.

## 3. Talk to it from the command line

```bash
ollama run llama3.2:3b
```

Type a question, see it respond, `Ctrl+D` or `/bye` to exit. This confirms the model itself works before we touch the API.

## 4. Talk to it over HTTP (the part that matters for code)

Ollama exposes an OpenAI-compatible endpoint at `http://localhost:11434/v1`. Confirm it with `curl`:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Say hello in exactly 3 words."}]
  }'
```

You should get back a JSON response containing the model's reply, plus a `usage` field with `prompt_tokens` and `completion_tokens` — the token counts from [module 00](../00-fundamentals/), now visible for real. Every project from here on talks to this same endpoint, just from Python instead of `curl`.

## 5. Pull the embedding model too

The flagship project ([projects/file-agent](../../projects/file-agent/)) needs one more model, used only to turn text into vectors (not for chatting):

```bash
ollama pull nomic-embed-text
```

## Checkpoint

You should now have:
- [ ] `ollama serve` running in the background
- [ ] `llama3.2:3b` pulled and responding to `ollama run`
- [ ] `nomic-embed-text` pulled
- [ ] The `curl` command above returning a JSON response

If all four are true, go build the flagship project: [projects/file-agent →](../../projects/file-agent/)

## Next

[Module 02 — Prompting & structured output →](../02-prompting-and-structured-output/)

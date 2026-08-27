# Choosing a model

This repo assumes a **CPU-only laptop with 8–16GB of RAM** — no GPU. Every default model below is picked to run acceptably on that baseline. If you have more RAM or a GPU, see "Upgrading" at the bottom.

## What "3B", "7B", and "quantized" mean

- **3B / 7B / 8B** = how many parameters the model has, in billions. Roughly: more parameters → better reasoning, but slower and more RAM.
- **Quantization** = storing each parameter in fewer bits (e.g. 4-bit instead of 16-bit) to shrink the model and speed it up, at a small quality cost. Ollama's default downloads are already quantized (usually 4-bit, labeled `Q4_K_M` or similar) — you don't need to do anything extra to get this benefit.
- Rule of thumb for RAM needed: roughly (parameters in billions) × 0.6–0.8 GB for a 4-bit quantized model. A 3B model needs ~2GB, a 7B model needs ~4–5GB — leaving headroom for your OS and other apps is why this repo defaults to the smaller end.

## Recommended defaults (8–16GB RAM, CPU-only)

| Model | Ollama tag | Size (4-bit) | Tool calling? | Notes |
|---|---|---|---|---|
| **Llama 3.2 3B Instruct** (this repo's default) | `llama3.2:3b` | ~2GB | Yes | Good general instruction-following, fast on CPU |
| Qwen2.5 3B Instruct | `qwen2.5:3b` | ~2GB | Yes | Comparable alternative, sometimes stronger at structured output |
| Phi-3.5 mini | `phi3.5` | ~2.2GB | **No** | Microsoft's small model, strong for its size — but see warning below |

Pull the default with:

```bash
ollama pull llama3.2:3b
```

**`phi3.5` cannot do tool/function calling.** `ollama show <model>` lists each model's declared
capabilities — `llama3.2:3b` and `qwen2.5:3b`/`qwen2.5:7b` list `completion` and `tools`, but
`phi3.5` only lists `completion`. Point `LLM_MODEL` at it for anything that calls tools —
module 03, module 04, module 07, or `projects/file-agent` — and you'll get an immediate
`400 ... does not support tools` error, not a slow or subtle failure. `phi3.5` is still a fine
choice for module 02 (plain JSON-mode structured output, no `tools` param involved). Check
`ollama show <model>` before assuming any two "small instruct model" tags are interchangeable.

## Embedding model (used by the RAG project)

| Model | Ollama tag | Notes |
|---|---|---|
| **Nomic Embed Text** (default) | `nomic-embed-text` | Small, fast, purpose-built for retrieval — this is *not* a chat model, only used to turn text into vectors |

```bash
ollama pull nomic-embed-text
```

## Upgrading if you have more hardware

- **16GB+ RAM:** try 7–8B models, e.g. `llama3.1:8b` or `qwen2.5:7b` — noticeably better reasoning, still fine on CPU though slower.
- **Discrete GPU with 8GB+ VRAM:** most runtimes (Ollama included) will use it automatically — you can comfortably run 7–13B models with much faster responses.
- Whatever you choose, just change `LLM_MODEL` in the project's `.env` — the code doesn't need to change.

A concrete, tested example of what "noticeably better reasoning" buys you: `projects/file-agent`'s
`extract_structured` tool asks the model to invent its own field names from a vague request (no
fixed schema — that's the point). Given "create a csv with each customer's name and email," the
default `llama3.2:3b` would loop asking which exact field names to use instead of just picking
some and proceeding. `qwen2.5:7b` got it right in one turn, no back-and-forth, on the exact same
request. If you hit that kind of stuck-in-clarification loop with the 3B default, that's the
first thing worth trying before assuming your prompt is unclear.

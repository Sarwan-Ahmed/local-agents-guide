# Choosing a model

This repo assumes a **CPU-only laptop with 8–16GB of RAM** — no GPU. Every default model below is picked to run acceptably on that baseline. If you have more RAM or a GPU, see "Upgrading" at the bottom.

## What "3B", "7B", and "quantized" mean

- **3B / 7B / 8B** = how many parameters the model has, in billions. Roughly: more parameters → better reasoning, but slower and more RAM.
- **Quantization** = storing each parameter in fewer bits (e.g. 4-bit instead of 16-bit) to shrink the model and speed it up, at a small quality cost. Ollama's default downloads are already quantized (usually 4-bit, labeled `Q4_K_M` or similar) — you don't need to do anything extra to get this benefit.
- Rule of thumb for RAM needed: roughly (parameters in billions) × 0.6–0.8 GB for a 4-bit quantized model. A 3B model needs ~2GB, a 7B model needs ~4–5GB — leaving headroom for your OS and other apps is why this repo defaults to the smaller end.

## Recommended defaults (8–16GB RAM, CPU-only)

| Model | Ollama tag | Size (4-bit) | Notes |
|---|---|---|---|
| **Llama 3.2 3B Instruct** (this repo's default) | `llama3.2:3b` | ~2GB | Good general instruction-following, fast on CPU |
| Qwen2.5 3B Instruct | `qwen2.5:3b` | ~2GB | Comparable alternative, sometimes stronger at structured output |
| Phi-3.5 mini | `phi3.5` | ~2.2GB | Microsoft's small model, strong for its size |

Pull the default with:

```bash
ollama pull llama3.2:3b
```

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

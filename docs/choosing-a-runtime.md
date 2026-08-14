# Choosing a local runtime

A "runtime" here means the program that actually loads a model file and serves it over HTTP on your machine. Every code example in this repo talks to a runtime over HTTP — it never cares which one you picked, because of one shared detail explained at the bottom of this page.

| Runtime | Interface | Setup friction | Best for |
|---|---|---|---|
| **[Ollama](https://ollama.com)** (default here) | CLI + REST API | Lowest — one installer, one `ollama pull` command | Beginners, scripting, this repo's default |
| **[LM Studio](https://lmstudio.ai)** | Desktop GUI (+ REST API) | Low — download models by clicking in a browsable catalog | People who want a visual model browser/chat UI before writing code |
| **[llama.cpp](https://github.com/ggerganov/llama.cpp)** (`llama-server`) | CLI, build from source or Homebrew | Higher — you manage model files (GGUF) yourself | Learning what's actually happening underneath Ollama/LM Studio (both are built on it) |
| **[vLLM](https://docs.vllm.ai)** | CLI + REST API | Highest — effectively requires a GPU | Once you outgrow a laptop and want production-grade throughput |

All four are fine choices. This repo defaults to Ollama purely because it has the lowest setup friction for a first run — pick whichever you like and the code should keep working.

## The trick that makes this repo runtime-agnostic

Ollama, LM Studio, and llama.cpp's server all expose an **OpenAI-compatible API** at a path ending in `/v1` — the same request/response shape OpenAI's API uses, which LangChain (and most AI tooling) already knows how to speak. That means switching runtimes is just pointing a `base_url` at a different port:

| Runtime | Default OpenAI-compatible base URL |
|---|---|
| Ollama | `http://localhost:11434/v1` |
| LM Studio | `http://localhost:1234/v1` |
| llama.cpp (`llama-server`) | `http://localhost:8080/v1` |

Every project in this repo reads its runtime's URL and model name from environment variables (see each project's `.env.example`) instead of hardcoding Ollama. If you'd rather use LM Studio: install it, load a model, start its local server, then set `LLM_BASE_URL=http://localhost:1234/v1` and `LLM_MODEL=<the model name shown in LM Studio>`. Nothing else changes.

## Installing Ollama (the default)

```bash
# macOS
brew install ollama
# or download the installer from https://ollama.com/download

# start the background server (installer usually does this for you)
ollama serve
```

Verify it's running:

```bash
curl http://localhost:11434/api/tags
```

An empty `{"models":[]}` response means it's up and you just haven't pulled a model yet — continue to [module 01](../modules/01-running-models-locally/).

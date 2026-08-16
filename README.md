# Local Agents & LLMs — A Zero-to-Working Guide

Learn how LLMs, agents, tools, vector databases, and RAG fit together by running all of it **on your own laptop, for free, with no API keys and no per-token billing.** No prior AI/ML experience assumed.

Every cloud LLM API charges per token. That's fine for production, but it makes *learning* expensive — every experiment, typo, and re-run costs money. Running small open models locally removes that constraint entirely, so you can iterate as much as you want while you build intuition.

## Prerequisites

- A laptop with **8–16GB RAM, no GPU required** (everything here is sized for that; if you have more RAM/a GPU, see [docs/choosing-a-model.md](docs/choosing-a-model.md) for bigger options)
- Python 3.10+
- Comfortable running commands in a terminal — no other experience assumed

## Start here

If you want to see the whole point of this repo working in 15 minutes before reading any theory, skip ahead to **[projects/chat-with-your-docs](projects/chat-with-your-docs/)** — a fully working local agent that answers questions about your own files, using nothing but your laptop.

Have a pile of files you're manually copying data out of by hand — especially ones with sensitive/PII content you can't run through a hosted AI tool? See **[projects/batch-field-extraction](projects/batch-field-extraction/)** instead — it pulls structured fields out of many files at once, entirely locally.

Then come back and work through the modules in order — each one explains a concept the flagship project already used.

**Modules 02-08 below are outlines, meant as assignments** — try building each one yourself from its outline. Stuck, or want to check your work? The [`reference-solutions`](https://github.com/Sarwan-Ahmed/local-agents-guide/tree/reference-solutions) branch has a full write-up and working code for every module.

## Learning path

| # | Module | Status | What it covers |
|---|--------|--------|-----------------|
| 00 | [Fundamentals](modules/00-fundamentals/) | ✅ Ready | Tokens, context windows, why local inference has no per-token cost |
| 01 | [Running models locally](modules/01-running-models-locally/) | ✅ Ready | Installing Ollama, pulling a model, talking to it over HTTP |
| 02 | [Prompting & structured output](modules/02-prompting-and-structured-output/) | 🚧 Outline | Getting reliable, parseable answers out of a small model |
| 03 | [Tool use / function calling](modules/03-tool-use-function-calling/) | 🚧 Outline | How a model "calls" a function — the mechanic behind agent skills |
| 04 | [Agents](modules/04-agents/) | 🚧 Outline | Looping a model + tools together (LangGraph) |
| 05 | [Vector databases & embeddings](modules/05-vector-databases-and-embeddings/) | 🚧 Outline | What an embedding is, what a vector DB stores |
| 06 | [RAG](modules/06-rag/) | 🚧 Outline | Wiring retrieval into the agent loop from module 04 |
| 07 | [Multi-agent orchestration](modules/07-multi-agent-orchestration/) | 🚧 Outline (advanced) | Multiple agents cooperating |
| 08 | [Evaluation & cost comparison](modules/08-evaluation-and-cost-comparison/) | 🚧 Outline | Measuring local vs. cloud cost/latency/quality with real numbers |

Modules marked ✅ have full explanations and runnable steps today. Modules marked 🚧 have a scoped outline of what's coming so you know what to expect next — they are not yet complete, and this table will be updated as they land.

## Repo layout

```
docs/       reference docs that don't belong to one specific module (runtime choice, model choice)
modules/    the numbered curriculum — read in order
projects/   complete, runnable projects that combine multiple modules
resources.md  curated external links, grouped by topic
```

## Design decisions worth knowing up front

- **Runtime-agnostic by default.** Code examples talk to `http://localhost:<port>/v1`, the OpenAI-compatible API shape that Ollama, LM Studio, and llama.cpp's server all implement. Default runtime is [Ollama](https://ollama.com) (simplest to install), but you can point the same code at a different local runtime by changing one environment variable — see [docs/choosing-a-runtime.md](docs/choosing-a-runtime.md).
- **Small models on purpose.** Every default model fits in 8–16GB RAM with no GPU. See [docs/choosing-a-model.md](docs/choosing-a-model.md) if you have more hardware to spare.
- **Agent framework: LangChain / LangGraph.** Used from module 04 onward, once you've seen the raw mechanics (prompting, tool calling) that the framework is wrapping.

## License

[MIT](LICENSE) — use, fork, and adapt freely.

## Contributing

This guide is a work in progress (see the 🚧 modules above). Issues and PRs that fill in a module, fix an inaccuracy, or add a clearer example are welcome once this repo is public.

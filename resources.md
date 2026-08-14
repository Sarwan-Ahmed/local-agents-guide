# Resources

Curated links, grouped by topic. Kept short and current on purpose — prefer official docs over blog posts, since APIs here move fast.

## Runtimes

- [Ollama docs](https://ollama.com) — install, model library, REST API reference
- [LM Studio docs](https://lmstudio.ai/docs) — GUI runtime, also exposes an OpenAI-compatible server
- [llama.cpp](https://github.com/ggerganov/llama.cpp) — the inference engine both Ollama and LM Studio build on
- [vLLM docs](https://docs.vllm.ai) — production/GPU-oriented serving, for when you outgrow a laptop

## Models

- [Ollama model library](https://ollama.com/library) — browse available models and sizes
- [Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) — compare small model quality
- ["Quantization" explained (Hugging Face)](https://huggingface.co/docs/optimum/concept_guides/quantization) — why a "4-bit" model is smaller and faster with a small quality tradeoff

## Prompting & structured output

- [Anthropic prompt engineering guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — applies to any model, not just Claude
- [OpenAI's function calling / structured outputs guide](https://platform.openai.com/docs/guides/structured-outputs) — same API shape Ollama/LM Studio implement

## Agents & tool use

- [LangGraph docs](https://langchain-ai.github.io/langgraph/) — the agent framework used from module 04 onward
- [LangChain docs](https://python.langchain.com/) — building blocks LangGraph is built on
- [ReAct paper](https://arxiv.org/abs/2210.03629) — the reasoning+acting loop most tool-using agents are based on

## Vector databases & RAG

- [Chroma docs](https://docs.trychroma.com/) — the vector DB used in the flagship project
- [Nomic Embed model card](https://ollama.com/library/nomic-embed-text) — the local embedding model used in the flagship project
- ["What is RAG?" (LangChain)](https://python.langchain.com/docs/concepts/rag/) — concept overview

## Evaluation & cost

- [Ollama API reference](https://github.com/ollama/ollama/blob/main/docs/api.md) — token counts are returned in every response, useful for module 08's cost comparisons

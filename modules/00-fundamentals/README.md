# 00 — Fundamentals

Before running anything, it helps to have the vocabulary straight. This module has no code — it's the mental model the rest of the repo builds on.

## What a token is

A model doesn't read text letter-by-letter or word-by-word — it reads **tokens**, chunks that are often shorter than a word (`"unbelievable"` might split into `un`, `believ`, `able`). As a rough estimate, 1 token ≈ 4 characters of English text, or about 0.75 words.

Every request you send an LLM — your prompt, the conversation history, any retrieved documents, the model's reply — is counted in tokens. This matters for two reasons:

1. **Context window** — a model can only "see" a fixed number of tokens at once (e.g. 8K, 32K, 128K). Once a conversation or a stuffed-in document exceeds that, older content gets dropped or the request fails outright.
2. **Cost** — cloud APIs (OpenAI, Anthropic, etc.) bill per token, split into *input* tokens (what you send) and *output* tokens (what the model generates), usually at different rates.

## The cost math that motivates this whole repo

Say a cloud model costs $3 per million input tokens and $15 per million output tokens (roughly OpenAI/Anthropic mid-tier pricing as of 2025–2026). A single agent "turn" that reads a 2,000-token document, plus conversation history, and writes a 300-token answer costs a small fraction of a cent — but multiply that by:

- Hundreds of experiment iterations while you're learning
- Every retry when a prompt didn't work
- Every document your RAG pipeline retrieves and re-sends on every question

...and a learning project can rack up real, recurring cost with zero revenue behind it. **Local inference has none of this** — once a model is downloaded, running it a thousand times costs the same electricity as running it once. That's the entire reason this repo runs everything on your own machine: nothing here is about avoiding cloud APIs forever, it's about removing cost as a variable *while you're still learning*.

The tradeoff: local models you can run on a laptop are smaller and less capable than the largest cloud models. Module 08 (evaluation & cost comparison) comes back to this with real numbers once you've built something to measure.

## The vocabulary this repo will build up, in order

| Term | One-line definition | Where it's covered |
|---|---|---|
| **Model / runtime** | The neural network, and the program that serves it over HTTP on your machine | [Module 01](../01-running-models-locally/) |
| **Prompt / structured output** | What you send the model, and getting it to reply in a predictable, parseable shape | [Module 02](../02-prompting-and-structured-output/) |
| **Tool / function calling** | A model requesting that *your* code run a specific function, then using the result | [Module 03](../03-tool-use-function-calling/) |
| **Agent** | A loop: model decides an action → your code runs it → model sees the result → repeat until done | [Module 04](../04-agents/) |
| **Skill** | A named, reusable capability an agent can invoke — in practice, usually just a tool with a clear description | [Module 04](../04-agents/) |
| **Embedding** | A list of numbers (a vector) representing the *meaning* of a piece of text, such that similar meanings end up as nearby vectors | [Module 05](../05-vector-databases-and-embeddings/) |
| **Vector database** | A database built to store embeddings and quickly find the nearest ones to a query | [Module 05](../05-vector-databases-and-embeddings/) |
| **RAG** (Retrieval-Augmented Generation) | Look up relevant text via a vector database, then hand it to the model as context before it answers | [Module 06](../06-rag/) |

## Next

[Module 01 — Running models locally →](../01-running-models-locally/)

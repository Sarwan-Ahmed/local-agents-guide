# 02 — Prompting & structured output

🚧 **Outline only — full write-up and code coming in a future pass.**

## What you'll learn

How to get a small local model to answer reliably and in a shape your code can parse, which is the foundation every later module (tools, agents, RAG) depends on — an agent that can't reliably produce structured output can't reliably call tools.

## Planned outline

- System prompts vs. user prompts, and why small models need more explicit instructions than large cloud models
- Few-shot examples: showing the model 1–2 examples of the output shape you want
- Asking for JSON output directly, and why it sometimes fails on smaller models
- Using the OpenAI-compatible `response_format`/JSON mode supported by Ollama and LM Studio
- Validating model output against a schema (e.g. with Pydantic) and retrying on failure
- A small worked example: extract structured fields (title, date, tags) from a block of free text

## Prerequisite

[Module 01 — Running models locally](../01-running-models-locally/)

## Next

[Module 03 — Tool use / function calling →](../03-tool-use-function-calling/)

# 02 — Prompting & structured output

Goal: get a small local model to answer in a shape your code can actually parse. This is the foundation every later module depends on — an agent that can't reliably produce structured output can't reliably call tools.

## Why this is harder with small local models

Large cloud models are trained on enormous instruction-following datasets and tend to follow formatting instructions even when you're vague. A 3B model needs you to be explicit: tell it exactly what shape you want, ideally show it an example, and validate what comes back instead of trusting it blindly.

## System prompts vs. user prompts

The **system prompt** sets standing instructions for the whole conversation ("you are a data-extraction assistant, always reply with JSON matching this schema"). The **user prompt** is the actual per-request input. Small models follow formatting instructions more reliably when they're in the system prompt, not buried in the user message.

## Few-shot examples

Showing the model 1-2 examples of exactly the output you want ("few-shot prompting") measurably improves format compliance on small models. This module's example script includes one.

## Asking for JSON directly

Ollama's OpenAI-compatible endpoint supports `response_format={"type": "json_object"}`, which constrains the model's output to valid JSON syntax. It does **not** guarantee the JSON matches the *schema* you wanted — only that it parses. That's why you still need a validation step after.

## Validating with Pydantic, and retrying

Define the expected shape as a Pydantic model. Parse the model's JSON into it — if a field is missing or the wrong type, Pydantic raises a `ValidationError`. On failure, send the error back to the model as feedback and ask it to correct its answer, rather than crashing or silently accepting bad data.

## Worked example

[`extract.py`](extract.py) takes a free-text note and extracts structured fields (`title`, `date`, `tags`) into a `NoteFields` Pydantic model, with one retry if the first response doesn't validate.

```bash
cd modules
source .venv/bin/activate   # see modules/README.md for setup if you haven't yet
python 02-prompting-and-structured-output/extract.py
```

Expected output: a validated `NoteFields` object printed to the console, extracted from the hardcoded sample note at the top of the script. Try editing that note's text and re-running — notice how a vaguer note produces a less confident `tags` list, and how malformed model output (rare on `llama3.2:3b`, more common on smaller models) triggers the retry path.

## Prerequisite

[Module 01 — Running models locally](../01-running-models-locally/)

## Next

[Module 03 — Tool use / function calling →](../03-tool-use-function-calling/)

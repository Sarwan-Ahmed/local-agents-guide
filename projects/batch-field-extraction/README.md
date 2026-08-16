# Batch field extraction — pull structured data out of many files, locally

The use case this solves: you have a folder of files (customer intake notes, forms, records — often containing PII) and you're manually reading each one to copy specific fields into a spreadsheet or database. That's slow, and if the files contain sensitive data, you may not be able to run them through a hosted AI tool (ChatGPT, Claude.ai, Copilot) at all, since those retain data per their terms. This project does the extraction with a model running entirely on your own machine — nothing in these files ever leaves your laptop, the same guarantee covered in [module 01](../../modules/01-running-models-locally/) and confirmed for the flagship RAG project's data flow.

This generalizes [module 02](../../modules/02-prompting-and-structured-output/)'s single-note `extract.py` into a batch pipeline: same JSON-mode + Pydantic-validation technique, but looping over every file in a folder, continuing past failures instead of crashing, and writing everything to one CSV.

## What's in `input_docs/`

Three short, clearly-fictional customer records in different formats (a form, a call note, a terse note missing a field) — enough to see the extraction handle messy real-world formatting and a genuinely missing field. Once it works, point `INPUT_DIR` at your own folder instead (see "Using this on real data" below).

## Setup

```bash
cd projects/batch-field-extraction
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Needs [module 01](../../modules/01-running-models-locally/) done: Ollama running, `llama3.2:3b` pulled.

## Run it

```bash
python extract_batch.py
```

Expected output: an `OK`/`FAIL` line per file, then a summary, then `output/extracted.csv` with one row per file — `full_name`, `date_of_birth`, `account_number`, `email`, `phone`, plus which source file each row came from. `record_003.txt` is missing a phone number on purpose — check that its row has `phone` as empty rather than a made-up value.

## Adapting this to your own fields

Everything field-specific lives in [`schema.py`](schema.py) — the extraction prompt in `extract_batch.py` is built automatically from that schema, so you don't need to touch the pipeline code to extract different fields. Change the `CustomerRecord` model's fields to whatever your documents actually contain (invoice number, claim ID, diagnosis code, whatever applies), rename the class if you like, and re-run.

This assumes **the same fields, every file** — if different documents in your folder need different fields extracted, you'll need either separate runs per document type (with separate schemas) or a more involved classify-then-extract pipeline (combine with [module 07](../../modules/07-multi-agent-orchestration/)'s routing pattern: classify the doc type first, then dispatch to the matching schema).

### Tuning it with the `schema-tuner` Claude Code agent

You don't have to edit `schema.py` by hand. This project ships a custom Claude Code subagent, [`.claude/agents/schema-tuner.md`](.claude/agents/schema-tuner.md), that does it for you — the whole point being it never needs to see your real files. Its job is to take your *description* of what fields you want and what your files look like, update `schema.py` (and `extract_batch.py`'s `INPUT_GLOB` if your file extension differs), invent a few new fake sample files to test against, and verify the updated pipeline works — all without touching real data.

To use it:

```bash
cd projects/batch-field-extraction
claude
```

Launching Claude Code with this folder as your working directory is what makes the agent discoverable (Claude Code looks for `.claude/agents/` from your current directory upward). Then just describe what you need, e.g.:

> Use the schema-tuner agent: my files are call center notes, I need `customer_name`, `ticket_id`, `issue_category`, and `resolved` (yes/no) extracted. Notes look roughly like: "Called about [issue], ticket #[id], resolved: [yes/no]."

The agent will update the schema, generate its own fake test files, run `extract_batch.py` against them, and report back once it's verified working. **Never paste real customer data into this conversation, even to describe the format** — describe the structure in words or with obviously fake example values instead, the same way the example above does. Once you're happy with the result, point `INPUT_DIR` in your own `.env` at your real files yourself and run `python extract_batch.py` locally — that step is intentionally not part of the Claude Code conversation.

## Using this on real data

A few things worth doing before pointing this at actual customer files:

- **Keep real input files outside this git repo entirely.** Point `INPUT_DIR` in `.env` at an absolute path elsewhere on disk (e.g. `INPUT_DIR=/Users/you/private/customer-files`), rather than copying real files into `input_docs/`. `output/` is already gitignored, but don't rely on that alone — real PII shouldn't be created inside a folder that's ever been (or could accidentally be) pushed to a public remote.
- **Check with your organization's data handling process first**, even though this runs entirely locally. Running a model on your own machine solves the *vendor data-retention* problem (nothing is sent to a hosted AI provider), but it doesn't automatically satisfy every other requirement your organization or a specific client engagement may have for handling customer PII — data residency, encryption at rest, access logging, which devices are approved for this kind of data. Confirm with your security/compliance process before running this on real customer records, not just because the model happens to be local.
- **Spot-check the output.** Module 03 and 08 both cover this: small local models don't always extract perfectly. Skim a sample of `output/extracted.csv` against the source files before trusting the full batch, especially for a schema change you haven't tested yet.

## Performance expectations

Tested with 3 files on `llama3.2:3b`, CPU-only: each file takes a few seconds. For tens to low hundreds of files, that's a coffee-break batch job, not real-time. For thousands+, measure actual throughput on a handful of files first (module 08 covers timing an agent's runs) before assuming it'll finish in a reasonable window — a bigger model or GPU may be worth it at that scale.

## Prerequisite

[Module 02 — Prompting & structured output](../../modules/02-prompting-and-structured-output/)

# 07 — Multi-agent orchestration (advanced, optional)

Everything through module 06 is a single agent with tools, which covers the large majority of real use cases. Only continue here once that's solid and you have a concrete reason to split work across multiple agents.

## Why multi-agent at all

Two reasons it's worth doing, beyond "it sounds more advanced":

- **Specialization** — a narrowly-scoped agent (one tool, one job) is easier to prompt reliably than one agent juggling many unrelated tools.
- **Context isolation** — keeping one agent's tool-call noise out of another's context window. A document-search agent's retrieved chunks don't need to clutter a general chit-chat agent's history.

## The pattern: supervisor / router

A router decides, per question, which specialist should handle it. [`supervisor_demo.py`](supervisor_demo.py) implements this with two specialists reusing pieces you already have:

- **`docs_agent`** — has the `search_docs` tool from the flagship project ([projects/file-agent](../../projects/file-agent/)), for questions about the ingested documents
- **`chitchat_agent`** — plain LLM, no tools, for anything else

The router itself is a small structured-output call (module 02's pattern) that classifies the incoming question as `"docs"` or `"chitchat"`, then a conditional edge sends it to the matching specialist.

## Setup

This module reuses the flagship project's index, so it needs that ingested first:

```bash
cd projects/file-agent
source .venv/bin/activate && python ingest.py   # skip if you already ran this
```

Then, from `modules/`:

```bash
cd modules
source .venv/bin/activate
python 07-multi-agent-orchestration/supervisor_demo.py
```

Expected output: the script asks one docs-related question and one general question, printing which specialist the router picked for each, and that specialist's answer.

## A second real quirk this hit: the fix isn't always more instructions

`docs_agent` originally had no system prompt at all, and `llama3.2:3b` flatly refused the account-number question ("I can't provide information about a private citizen") even though `search_docs` had already retrieved the correct answer — a *different* failure from module 06's, since this wasn't retrieval-related, it was the model treating a name-plus-account-number pattern as a privacy request to decline. The instinctive fix — explicitly telling it "these are fictional test records, not real people's private data" — made it *worse*, not better; naming the privacy concept at all seemed to trigger more refusals, differently worded each time. What actually fixed it was giving `docs_agent` the same system prompt shape already proven in `projects/file-agent/agent.py` (module/tool framing plus "a tool's result is ground truth"), with no mention of privacy at all. Worth remembering: adding a disclaimer isn't automatically a safe move, and copying a prompt structure that's already been tested is often more reliable than writing a new one from a plausible-sounding idea.

## The real cost of multi-agent

Every specialist call is a separate model invocation. On a cloud API that's a few more cents; on local CPU inference it's a few more seconds of latency per request, since each call to the model runs one at a time (see module 08 for what that actually measures out to). Multi-agent setups multiply that by however many hops a question takes through the system — worth it for genuine specialization, wasteful if it's splitting up work a single well-designed agent with more tools would have handled in one call.

## Prerequisite

[Module 04 — Agents](../04-agents/) and the ingested flagship project from [Module 06 — RAG](../06-rag/)

## Next

[Module 08 — Evaluation & cost comparison →](../08-evaluation-and-cost-comparison/)

# 06 — RAG (Retrieval-Augmented Generation)

🚧 **Outline only — full write-up and code coming in a future pass.**

Note: the flagship project, [projects/file-agent](../../projects/file-agent/), already includes a complete working RAG tool (`search_docs`) — this module is the deeper explanation of *why* it's built the way it is.

## What you'll learn

How retrieval (module 05) and agents (module 04) combine into RAG, and the design decisions that determine whether a RAG pipeline actually gives good answers.

## Planned outline

- The RAG loop end to end: question → embed it → retrieve nearest chunks → stuff them into the prompt as context → model answers grounded in that context
- Walking through `projects/file-agent/ingest.py` and `agent.py` line by line against this loop
- Retrieval-as-a-tool vs. always-retrieve: giving the agent a `search_docs` tool it *decides* to call (what the flagship project does) vs. always retrieving before every answer
- Failure modes: retrieving the wrong chunks, chunks too small to contain the answer, context window overflow with too many retrieved chunks
- Citing sources: returning which chunks/documents were used, not just an answer
- When RAG isn't the right tool: questions that need reasoning across the whole corpus rather than a few relevant snippets

## Prerequisite

[Module 04 — Agents](../04-agents/) and [Module 05 — Vector databases & embeddings](../05-vector-databases-and-embeddings/)

## Next

[Module 07 — Multi-agent orchestration →](../07-multi-agent-orchestration/) (optional/advanced), or [Module 08 — Evaluation & cost comparison →](../08-evaluation-and-cost-comparison/)

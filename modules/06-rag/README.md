# 06 — RAG (Retrieval-Augmented Generation)

The flagship project, [projects/chat-with-your-docs](../../projects/chat-with-your-docs/), is a complete working RAG agent — if you haven't run it yet, do that first. This module is the deeper explanation of *why* it's built the way it is, walking through the actual code rather than introducing new code.

## The RAG loop end to end

1. A question comes in
2. Embed the question with the same embedding model used to index the documents
3. Retrieve the nearest chunks from the vector database
4. Hand those chunks to the LLM as context, alongside the question
5. The LLM answers, grounded in that context instead of only its own training data

Modules 04 (agents) and 05 (vector databases) are exactly the two halves this combines.

## Walking through the flagship project's code

**`ingest.py`** does steps 2-3 once, ahead of time: it loads `sample_docs/*.md`, splits them into chunks (`chunk_size=500, chunk_overlap=50` — see [module 05](../05-vector-databases-and-embeddings/) for what these control), embeds each chunk via `nomic-embed-text`, and persists everything into a local Chroma collection.

**`agent.py`** does steps 1, 4, and 5, live, per question:

```python
retriever_tool = create_retriever_tool(
    retriever,
    name="search_docs",
    description="Search the user's ingested documents for relevant passages.",
)
```

This line is the key design decision in the whole project: retrieval is wrapped as a **tool**, exactly like module 03/04's `get_current_time` and `read_file`. The agent decides, per question, whether it needs to call `search_docs` at all — it isn't forced to retrieve before every single answer.

## Retrieval-as-a-tool vs. always-retrieve

| | Retrieval-as-a-tool (what the flagship project does) | Always-retrieve |
|---|---|---|
| How | The agent gets a `search_docs` tool and calls it if it decides the question needs it | Every question is retrieved against before the LLM ever sees it |
| Pro | Cheap follow-up questions ("thanks, one more thing...") skip an unnecessary retrieval | Simpler control flow, no dependence on the model deciding correctly |
| Con | On a small model, the decision of *whether* to retrieve can be wrong — see module 03/04's note on small models not always behaving as expected | Wastes a retrieval call (and context window) on questions that don't need it, e.g. "thanks!" |

Neither is strictly better — this repo picked retrieval-as-a-tool because it's the more general pattern (it's the same shape as any other tool an agent might have), and because it directly demonstrates the module 03/04 mechanic being reused for something practical.

## Failure modes to watch for

- **Wrong chunks retrieved** — the embedding model matched on surface similarity, but the actually-relevant chunk didn't rank in the top-k. Try asking the flagship project a question that's phrased very differently from the wording in `sample_docs/` and see retrieval quality drop.
- **Chunk too small to contain the answer** — a fact split across a chunk boundary might only get half-retrieved. This is what `chunk_overlap` in `ingest.py` mitigates.
- **Context window overflow** — retrieving too many chunks (`k` too high in `store.as_retriever(search_kwargs={"k": 3})`) can push a small model's limited context window past capacity, especially alongside a long conversation history.

## Citing sources

The flagship project currently returns only an answer, not which chunks it used. To add citations, change `agent.py`'s tool description to ask the model to mention which document a fact came from, or — more reliably — have the tool itself return `(content, source_filename)` pairs and have `ask()` in `agent.py` collect which sources were retrieved during the run, independent of whether the model chooses to mention them in prose. The second approach is more reliable specifically because of the same reason module 03 called out: don't trust a small model's prose to faithfully report something you can just track programmatically instead.

## When RAG isn't the right tool

RAG retrieves a *few relevant snippets* — it's a poor fit for questions that need reasoning across an entire corpus at once ("summarize every complaint mentioned across all documents"), since no single top-k retrieval surfaces everything relevant. That class of question needs a different approach (e.g., map-reduce summarization over every document), not more retrieval tuning.

## Prerequisite

[Module 04 — Agents](../04-agents/) and [Module 05 — Vector databases & embeddings](../05-vector-databases-and-embeddings/)

## Next

[Module 07 — Multi-agent orchestration →](../07-multi-agent-orchestration/) (optional/advanced), or [Module 08 — Evaluation & cost comparison →](../08-evaluation-and-cost-comparison/)

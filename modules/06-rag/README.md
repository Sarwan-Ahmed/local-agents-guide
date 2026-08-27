# 06 — RAG (Retrieval-Augmented Generation)

The flagship project, [projects/file-agent](../../projects/file-agent/), already includes a complete working RAG tool (`search_docs`) — if you haven't run it yet, do that first. This module is the deeper explanation of *why* it's built the way it is, walking through the actual code rather than introducing new code.

## The RAG loop end to end

1. A question comes in
2. Embed the question with the same embedding model used to index the documents
3. Retrieve the nearest chunks from the vector database
4. Hand those chunks to the LLM as context, alongside the question
5. The LLM answers, grounded in that context instead of only its own training data

Modules 04 (agents) and 05 (vector databases) are exactly the two halves this combines.

## Walking through the flagship project's code

**`ingest.py`** does steps 2-3 once, ahead of time: it loads `input_docs/*.txt`, splits them into chunks (`chunk_size=500, chunk_overlap=50` — see [module 05](../05-vector-databases-and-embeddings/) for what these control), embeds each chunk via `nomic-embed-text`, and persists everything into a local Chroma collection.

**`agent.py`** does steps 1, 4, and 5, live, per question:

```python
retriever_tool = create_retriever_tool(
    store.as_retriever(search_kwargs={"k": 3}),
    name="search_docs",
    description="Search the input folder's documents for relevant passages when you don't know which file has the answer.",
    document_prompt=PromptTemplate.from_template("Source: {source}\n{page_content}"),
)
```

Two design decisions here matter more than they look:

1. **Retrieval is wrapped as a tool**, exactly like module 03/04's `get_current_time` and `read_file`. The agent decides, per question, whether it needs to call `search_docs` at all — it isn't forced to retrieve before every single answer, and it also has two *other* tools (`read_file`, `extract_structured`) it might reach for instead, depending on what's actually asked.
2. **`document_prompt` labels each retrieved chunk with its source file.** This isn't cosmetic — see the failure mode below.

## A real failure this caught: unlabeled chunks break lookup questions

`search_docs` originally used `create_retriever_tool`'s default formatting, which just concatenates chunks with no indication of which file each came from. With `file-agent`'s multi-customer `input_docs/`, a query like "what is Carlos Mendez's email" would retrieve three different customers' records back to back — and `llama3.2:3b` would then answer "I don't have that information," *even though the correct email was sitting right there in the tool's result*. Not a wrong guess — a flat, confident denial with the right answer in context. This happened on 2 of 3 test questions.

Adding the `document_prompt` above — one line labeling each chunk with `Source: {source}` — fixed every case. The lesson: when a retriever tool feeds a small model chunks from *multiple* documents at once, unlabeled context is enough to make the model lose track of which fact belongs to which document. This is a sharper version of the "don't trust the model's prose" lesson from module 03 — here it wasn't even a paraphrase error, the model just failed to ground its answer in adjacent, unlabeled context.

## Retrieval-as-a-tool vs. always-retrieve

| | Retrieval-as-a-tool (what the flagship project does) | Always-retrieve |
|---|---|---|
| How | The agent gets a `search_docs` tool and calls it if it decides the question needs it | Every question is retrieved against before the LLM ever sees it |
| Pro | Cheap follow-up questions ("thanks, one more thing...") skip an unnecessary retrieval | Simpler control flow, no dependence on the model deciding correctly |
| Con | On a small model, the decision of *whether* to retrieve can be wrong — see module 03/04's note on small models not always behaving as expected | Wastes a retrieval call (and context window) on questions that don't need it, e.g. "thanks!" |

Neither is strictly better — this repo picked retrieval-as-a-tool because it's the more general pattern (it's the same shape as any other tool an agent might have), and because it directly demonstrates the module 03/04 mechanic being reused for something practical.

## Failure modes to watch for

- **Wrong chunks retrieved** — the embedding model matched on surface similarity, but the actually-relevant chunk didn't rank in the top-k. Try asking the flagship project a question that's phrased very differently from the wording in `input_docs/` and see retrieval quality drop.
- **Unlabeled chunks from multiple documents** — see above; this is the failure mode that's easy to miss because the tool call itself looks completely correct in a trace.
- **Chunk too small to contain the answer** — a fact split across a chunk boundary might only get half-retrieved. This is what `chunk_overlap` in `ingest.py` mitigates.
- **Context window overflow** — retrieving too many chunks (`k` too high in `store.as_retriever(search_kwargs={"k": 3})`) can push a small model's limited context window past capacity, especially alongside a long conversation history.

## Citing sources

`file-agent`'s `document_prompt` already labels each chunk with its source filename in the tool's *input* to the model — but the model's *answer* to the user doesn't necessarily repeat which file a fact came from. To surface that to the user, the more reliable approach (per the lesson above: don't trust prose) is to have the tool return `(content, source_filename)` pairs and collect which sources were actually retrieved during the run programmatically, rather than hoping the model mentions them.

## When RAG isn't the right tool

RAG retrieves a *few relevant snippets* — it's a poor fit for questions that need reasoning across an entire corpus at once ("summarize every complaint mentioned across all documents"), since no single top-k retrieval surfaces everything relevant. That class of question needs a different approach (e.g., map-reduce summarization over every document), not more retrieval tuning. It's also the wrong tool for "build me a structured file from every document" — that's exactly what `file-agent`'s `extract_structured` tool is for instead, since it loops every file directly rather than retrieving a top-k subset.

## Prerequisite

[Module 04 — Agents](../04-agents/) and [Module 05 — Vector databases & embeddings](../05-vector-databases-and-embeddings/)

## Next

[Module 07 — Multi-agent orchestration →](../07-multi-agent-orchestration/) (optional/advanced), or [Module 08 — Evaluation & cost comparison →](../08-evaluation-and-cost-comparison/)

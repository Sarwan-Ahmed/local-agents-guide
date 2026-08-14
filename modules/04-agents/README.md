# 04 — Agents

🚧 **Outline only — full write-up and code coming in a future pass.**

## What you'll learn

How to turn the manual tool-calling loop from module 03 into a proper agent using **LangGraph**, and what a framework is actually buying you over the hand-rolled version.

## Planned outline

- Recap: an agent is "model → tool call → result → model, repeat until done" — module 03 built this by hand
- Introducing LangGraph's `StateGraph`: nodes, edges, and the state that flows between them
- Rebuilding the module 03 example (time + file-read tools) as a LangGraph graph, side-by-side with the hand-rolled version, to see exactly what the framework replaces
- `create_react_agent` as a shortcut once the manual graph is understood
- Stopping conditions: max iterations, and why agents need a hard cap to avoid infinite tool-call loops
- Connecting to a local model: constructing LangChain's `ChatOpenAI` client pointed at your local runtime's `base_url` (the same pattern used in the flagship project)

## Prerequisite

[Module 03 — Tool use / function calling](../03-tool-use-function-calling/)

## Next

[Module 05 — Vector databases & embeddings →](../05-vector-databases-and-embeddings/)

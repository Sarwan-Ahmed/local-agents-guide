# 04 — Agents

Goal: see the module 03 loop rebuilt with **LangGraph**, and understand exactly what the framework is buying you over the hand-rolled version.

## Recap

Module 03's loop was: model responds → if it requested a tool, run it and feed the result back → repeat until the model gives a final answer. That loop *is* an agent. LangGraph gives you a structured way to define it — nodes, edges, and state that flows between them — instead of a hand-written `while` loop.

## `graph_agent.py` — the manual graph

[`graph_agent.py`](graph_agent.py) rebuilds module 03's exact two tools (`get_current_time`, `read_file`) as a LangGraph `StateGraph` with two nodes:

- `call_model` — invokes the LLM with the current message history
- `tools` — LangGraph's built-in `ToolNode`, which runs whichever tool(s) the model just requested

An edge routes from `call_model` back to `tools` whenever the model's response contains a tool call, and to `END` otherwise. Read this file side-by-side with module 03's `tools_demo.py` — it's the same loop, just expressed as a graph instead of a `while` statement.

```bash
cd modules
source .venv/bin/activate
python 04-agents/graph_agent.py
```

## `shortcut_agent.py` — the one-liner version

Once the manual graph makes sense, `langgraph.prebuilt.create_react_agent` builds the same kind of graph for you in one call. [`shortcut_agent.py`](shortcut_agent.py) does the identical task using that shortcut — this is the pattern the flagship project (`projects/file-agent`) and later modules actually use day to day.

```bash
python 04-agents/shortcut_agent.py
```

Note: you may see the same thing module 03 called out — correct tool calls, but a final summary that doesn't perfectly reflect them. Same model limitation, same reason; see module 03's README for why that's expected and not a bug here either.

## Stopping conditions

Both scripts cap iterations (via `recursion_limit` for the manual graph, and implicitly for `create_react_agent`) — without a hard cap, a model that keeps requesting tools (or requests one that keeps failing) loops forever. Always set a limit.

## Connecting to a local model

Both scripts construct `ChatOpenAI` with `base_url`/`model` read from `LLM_BASE_URL`/`LLM_MODEL` — the same runtime-agnostic pattern used everywhere else in this repo.

## Prerequisite

[Module 03 — Tool use / function calling](../03-tool-use-function-calling/)

## Next

[Module 05 — Vector databases & embeddings →](../05-vector-databases-and-embeddings/)

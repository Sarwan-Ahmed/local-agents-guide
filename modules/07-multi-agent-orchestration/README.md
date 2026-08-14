# 07 — Multi-agent orchestration (advanced, optional)

🚧 **Outline only — full write-up and code coming in a future pass.**

This module is marked optional: everything in modules 00–06 is a single agent with tools, which covers the large majority of real use cases. Only continue here once that's solid and you have a concrete reason to split work across multiple agents.

## What you'll learn

When and why to use more than one agent, and the coordination patterns for doing it with LangGraph.

## Planned outline

- Why multi-agent at all: specialization (a "researcher" agent + a "writer" agent) and context isolation (keeping one agent's tool noise out of another's context window)
- Patterns: supervisor/router (one agent delegates to others), and pipeline (agents run in a fixed sequence)
- Building a small supervisor example in LangGraph: one router agent deciding which of two specialist agents (e.g. a docs-search agent vs. a general-chat agent) should handle a given question
- The real cost of multi-agent: more model calls per user request, which matters even more on local hardware where each call is slower than a cloud API
- When a single well-designed agent with more tools is simply the better answer than splitting into multiple agents

## Prerequisite

[Module 04 — Agents](../04-agents/)

## Next

[Module 08 — Evaluation & cost comparison →](../08-evaluation-and-cost-comparison/)

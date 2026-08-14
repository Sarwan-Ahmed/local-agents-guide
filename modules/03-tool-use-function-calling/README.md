# 03 — Tool use / function calling

🚧 **Outline only — full write-up and code coming in a future pass.**

## What you'll learn

The mechanic underneath every agent "skill": how a model requests that your code run a specific function, and how you feed the result back in.

## Planned outline

- What a "tool" actually is: a name, a description, and a JSON schema of its arguments — nothing more
- Why the model never runs code itself — it only ever outputs "please call `search_docs` with `{query: ...}`," and your code decides whether/how to actually run it
- The OpenAI-compatible `tools` parameter, and confirming Ollama/LM Studio support it for your chosen model (not every small model reliably calls tools — this module will note which do)
- A worked example: a `get_current_time()` tool and a `read_file(path)` tool, called from a plain Python loop with no framework yet
- Why this loop — model responds → you detect a tool call → you run it → you send the result back → model responds again — *is* an agent, once you let it repeat until done (bridges into module 04)

## Prerequisite

[Module 02 — Prompting & structured output](../02-prompting-and-structured-output/)

## Next

[Module 04 — Agents →](../04-agents/)

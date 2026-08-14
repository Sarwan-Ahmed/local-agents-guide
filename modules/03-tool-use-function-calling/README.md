# 03 — Tool use / function calling

Goal: understand the mechanic underneath every agent "skill" — by hand, before any framework hides it. This is the last module before we introduce LangGraph in module 04.

## What a tool actually is

A tool is just three things: a **name**, a **description**, and a **JSON schema of its arguments**. That's it — the model never runs any code. It only ever outputs "please call `get_current_time` with `{}`," and it's entirely up to *your* code to notice that, actually run the function, and hand the result back.

## The loop

1. Send the model your message plus a list of available tools
2. The model either answers directly, or responds with a tool call request (name + arguments)
3. If it requested a tool call: your code runs the matching Python function
4. You send the function's return value back to the model, tagged as a tool result
5. The model responds again — now with the tool's output available to it — either with a final answer or another tool call

Repeat step 2-5 until you get a final answer. **This loop, once you let it repeat, is an agent** — module 04 gives it a name and a framework, but the mechanic is exactly this.

## A note on small models and tool calling

Not every small model reliably calls tools — it's a capability that has to be specifically trained in. `llama3.2:3b` supports it (used in this module's example); some smaller/older models will just ignore the `tools` parameter and answer directly, or hallucinate a tool call in plain text without using the proper format. If you swap in a different model and this module's example stops calling tools, that's the model, not the code.

## Worked example

[`tools_demo.py`](tools_demo.py) gives the model two tools — `get_current_time()` and `read_file(path)` — and runs the loop above by hand, printing each step so you can see the model deciding to call a tool, your code running it, and the model using the result.

```bash
cd modules
source .venv/bin/activate
python 03-tool-use-function-calling/tools_demo.py
```

Expected output: a trace showing the model requesting `read_file` and `get_current_time`, and the tool's actual output for each.

## What you might notice — and why it matters

Watch the final answer closely against the tool trace above it. On `llama3.2:3b`, it's common for the printed tool results to be correct (you'll see the real file contents and the real time in the trace) while the model's final prose summary paraphrases or outright invents different text. **This is a genuine small-model limitation, not a bug in this script** — the correct data is right there in the message history, and the model still doesn't always transcribe it faithfully into its answer.

This is exactly why you can't just eyeball an agent's answer and call it correct — module 08 (evaluation) comes back to this and builds an automatic check that verifies an answer against ground truth instead of trusting how confident and fluent it sounds.

## Prerequisite

[Module 02 — Prompting & structured output](../02-prompting-and-structured-output/)

## Next

[Module 04 — Agents →](../04-agents/)

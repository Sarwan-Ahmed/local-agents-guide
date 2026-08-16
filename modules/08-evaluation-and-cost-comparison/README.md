# 08 — Evaluation & cost comparison

Goal: measure whether an agent is actually working (not just "it ran without crashing"), and put real numbers behind the local-vs-cloud tradeoff from [module 00](../00-fundamentals/).

## Why "it gave a reasonable-looking answer" isn't evaluation

Module 03 and 04 both showed the same failure mode: an agent can call the right tool, get the right result, and still produce a final answer that doesn't faithfully reflect it. A fluent, confident-sounding answer is not the same as a correct one — you need a check that doesn't rely on skimming the output yourself.

## A minimal automatic check

[`eval.py`](eval.py) runs a small test set of questions against the flagship project's agent — the same customer records from `projects/file-agent`'s `input_docs/` — and checks whether each answer contains the expected fact (a substring check, e.g. does the answer actually contain the right account number). This is deliberately simple: it's not asking a second model to judge quality, just verifying the concrete fact made it into the answer.

This catches exactly the failure mode module 03 demonstrated: if the agent's prose hallucinates instead of using the real retrieved/tool content, the expected substring won't be there and the check fails, even though the answer might *read* fine. It also caught a variant of module 07's refusal quirk: `eval.py`'s agent originally had no system prompt, and `llama3.2:3b` refused the very first question outright even with the correct answer already retrieved — giving a hard `FAIL` rather than a subtle wrong answer. Fixed the same way module 07 did: a system prompt matching `projects/file-agent/agent.py`'s proven structure, no privacy disclaimers.

## Timing and token usage

The same script records wall-clock time per question and, where the model reports it, token usage per question — giving you real numbers for "how slow/expensive is this" instead of a vague impression.

## Setup

Needs the flagship project ingested first (same as module 07):

```bash
cd projects/file-agent
source .venv/bin/activate && python ingest.py   # skip if already done
```

Then, from `modules/`:

```bash
cd modules
source .venv/bin/activate
python 08-evaluation-and-cost-comparison/eval.py
```

Expected output: a per-question pass/fail table, timing, total tokens used, and a cost comparison against illustrative cloud API pricing — closing the loop opened in module 00 with actual numbers from your own hardware.

## Reading the cost comparison honestly

The cloud pricing figures in `eval.py` are hardcoded, illustrative, and will drift out of date — the point isn't the exact dollar figure, it's the shape of the result: your local run costs electricity only, regardless of how many times you re-run it, while the cloud estimate scales linearly with every single request. Re-run `eval.py` a few times in a row and watch the local cost line stay at $0 while a hypothetical cloud bill would keep climbing.

## Where local stops being the right call

None of this means "always run local." Local wins while you're iterating and learning, where request volume is high and correctness bars are forgiving. It stops being the right call once you need a capability the local model genuinely lacks — much larger context windows, stronger reasoning on hard tasks, or production reliability/uptime guarantees a laptop can't offer.

## Prerequisite

[Module 06 — RAG](../06-rag/) — this module evaluates the project built there

## Next

You've reached the end of the current curriculum — see the root [README](../../README.md) for repo status.

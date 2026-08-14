# 08 — Evaluation & cost comparison

🚧 **Outline only — full write-up and code coming in a future pass.**

## What you'll learn

How to measure whether an agent is actually working well (not just "it ran without crashing"), and put real numbers behind the local-vs-cloud tradeoff introduced back in [module 00](../00-fundamentals/).

## Planned outline

- Why "it gave a reasonable-looking answer" isn't evaluation: building a small test set of question/expected-answer pairs for the flagship project's sample docs
- Simple automatic checks: did the answer mention the expected fact, did it cite a source, did it hallucinate a source that doesn't exist
- Using a second, larger model as a judge for less clear-cut answers, and the caveats of doing that
- Timing local inference: measuring tokens/second on your hardware for the default model, so "small model on a laptop" has a concrete number attached
- The cost comparison, with real figures: running the flagship project's test set N times locally (electricity cost, effectively $0) vs. estimated cost if the same requests hit a cloud API at current per-token pricing — closing the loop opened in module 00
- Where local stops being the right call: when you need a capability the small local model genuinely doesn't have (a real production workload, much larger context, etc.)

## Prerequisite

[Module 06 — RAG](../06-rag/) — this module evaluates the flagship project built there

## Next

You've reached the end of the current curriculum — see the root [README](../../README.md) for repo status and what's planned next.

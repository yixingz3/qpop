---
name: review
description: Audit current research, claims, or a diff against the auditable-research discipline — flag stories vs falsifiable claims, backtest/look-ahead leakage, over-admission, sycophancy, missing pre-registration, and ungated reasoning. Use to review your own or others' LLM-assisted findings before acting on them.
disable-model-invocation: false
---

# Review for research discipline

Audit the target (the current claims, a file, or a diff) and report violations of the Forward-QPOP
discipline. Look for:

- **Stories** — assertions that aren't falsifiable or lack a mechanism.
- **Over-admission** — accepting most candidates; no evidence of *rejection*.
- **Sycophancy** — agreeing with a pre-stated view without an independent, written-first bear case.
- **Backtest / look-ahead leakage** — "validating" an LLM-scored process on data the model already
  knew (its outcomes are in the training set).
- **Missing pre-registration** — acting on a claim with no dated, hashed record made *before* the outcome.
- **Tertiary-only evidence** moving a conclusion.

For each finding: cite it, name the rung of the ladder it violates (see the `auditable-research`
skill), and give the minimal fix. End with a verdict: how much should be admitted vs. sent to
"no action," and which surviving claims should be pre-registered (`/qpop:preregister`).

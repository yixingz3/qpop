---
name: preregister
description: Pre-register a research hypothesis to a tamper-evident, hash-chained ledger BEFORE evaluating its outcome — claim, mechanism, dated evidence, prior, and measurable exit triggers. Use before acting on any model-generated finding so the prediction is provably dated ahead of the result.
disable-model-invocation: false
argument-hint: "[ledger.jsonl]"
---

# Pre-register a hypothesis

Work with the user to state a *falsifiable* hypothesis, then write it to the ledger **before** the
outcome is known. Collect:

1. **claim** — one falsifiable sentence.
2. **mechanism** — why it should hold / is hard to bypass.
3. **evidence** — dated, source-tiered facts (primary > secondary > market-implied > tertiary).
4. **prior** — an honest prior probability (0–1).
5. **exit_triggers** — measurable conditions that would close it Supported / Weakened / Falsified,
   each with a checkable `data_source`. Reject any trigger you cannot actually check.

Then append it (this content-hashes the entry and chains it to the previous one):

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/qpop.py" register "${1:-ledger.jsonl}" --json '<the entry JSON>'
```

Report the new `entry_hash`, and remind the user the entry is now immutable — to revise a belief,
record a `/qpop` belief-update or open a new id; never edit a closed entry. (Falling back outside a
plugin context: `python scripts/qpop.py register …`.)

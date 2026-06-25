# forward-qpop

**A tamper-evident, append-only forward pre-registration ledger for auditable,
leakage-resistant research.**

Register a hypothesis — a claim, dated evidence, measurable exit triggers, and a prior —
*before* the evaluation window opens. Each entry is content-hashed over its frozen fields
and chained to its predecessor, so the record proves **what was predicted, and when**.
Any later edit, insertion, deletion, or reorder breaks the chain and is detectable.

This is the domain-agnostic core of the **Forward-QPOP** protocol from the methods paper
*Forward-Registered, Auditable LLM-Assisted Research* — useful for any pre-registered
work (ML experiments, forecasts, studies), not only the finance testbed in the paper.

- **Zero dependencies** — pure Python standard library.
- **`entry_hash = sha256(content_hash ‖ prev_hash)`** — a real hash chain, not just a set
  of independently-hashed rows.
- **CI-friendly** — `forward-qpop verify ledger.jsonl` exits non-zero on tampering.

## Install

```bash
pip install forward-qpop
```

## Quickstart

```python
from forward_qpop import Ledger

led = Ledger("ledger.jsonl")

# 1. Pre-register BEFORE the evaluation window:
led.register(
    "H-AI-01",
    claim="Method X reduces silent production-ML failures vs the ungated baseline.",
    mechanism="Deterministic gates reject low-evidence candidates before the expensive step.",
    prior=0.5,
    evidence=[{"summary": "pilot result", "tier": "primary", "date": "2026-06-24"}],
    exit_triggers=[{"id": "no_effect", "metric": "failure-rate delta", "op": "~0",
                    "data_source": {"tier": "primary"}}],
    fields={"domain": "ai-reliability"},   # any domain-specific payload, also hashed
)

# 2. Record belief updates as evidence arrives (tertiary-only is blocked by default):
led.update("H-AI-01", evidence=[{"summary": "replication", "tier": "secondary",
                                 "date": "2026-09-01"}])

# 3. Close with a pre-committed outcome (supported / weakened / falsified):
led.close("H-AI-01", "supported", observed={"failure_rate_delta": -0.31})

# 4. Verify integrity at any time:
res = led.verify()
print(res.ok, res.n_entries, res.problems)
```

## CLI

```bash
forward-qpop verify ledger.jsonl   # exit 0 if intact, 1 (with details) if tampered
forward-qpop show   ledger.jsonl   # list entries
```

## Why forward, and why a chain

A backward test of an LLM-scored process is structurally invalid (the outcomes are
already in the model's training data). Pre-registration replaces "fit the past" with
"commit, then observe the future"; the hash chain makes that commitment **auditable** —
an external reviewer can confirm a hypothesis was registered *before* its outcome, and
that no past entry was silently changed.

## License

MIT. Part of <https://github.com/yixingz3/chokepoint-research-engine>.

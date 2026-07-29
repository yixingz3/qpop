# forward-qpop

**A tamper-evident, append-only forward pre-registration ledger for auditable,
leakage-resistant research.**

Register a hypothesis — a claim, dated evidence, measurable exit triggers, and a prior —
*before* the evaluation window opens. Each entry is content-hashed over its frozen fields and
chained to its predecessor, so the record proves **what was predicted** and that no entry was later
edited, inserted, interior-deleted, or reordered (deleting a *suffix* leaves a valid shorter
chain — detecting rollback needs an anchored head: `anchor` / `--expected-head`). Proving it was registered *before* an outcome (wall-clock
time) needs an external anchor — see [`anchor` / `verify-anchor` / `anchor external` /
`verify-external`](#cli).

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

# optional: adds `opentimestamps-client`, needed for `anchor external --method ots`
pip install "forward-qpop[anchor]"
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
forward-qpop verify ledger.jsonl          # exit 0 if intact, 1 (with details) if tampered
forward-qpop show   ledger.jsonl          # list entries
forward-qpop anchor ledger.jsonl          # local manifest committing to the head
forward-qpop verify-anchor ledger.jsonl   # detect any drift since anchoring

# external anchor -- a publicly-dated, append-only submission (WI-19)
forward-qpop anchor external ledger.jsonl --method ots   # submit the head digest to OpenTimestamps
forward-qpop verify-external ledger.jsonl                # detect drift since the external submission

# sequential trigger test (e-value rule) over the ledger (WI-29; defects closed WI-40):
# per-hypothesis anytime-valid under stated assumptions — fixed registered-trigger
# membership + strict boolean checks (see research/docs/EVALUE_METHODS.md);
# NO book-wide (across-hypothesis) multiplicity control
forward-qpop evalue ledger.jsonl --alpha 0.05            # verified full replay; sidecar = derived snapshot
forward-qpop evalue ledger.jsonl --json --out report.json  # JSON report, also written to a file
```

`anchor external` requires the `anchor` extra (`pip install forward-qpop[anchor]`) and network
access; a missing `ots` binary or a network failure exits non-zero with a clear message and never
writes a sidecar that falsely claims success.

`evalue` reads a hypothesis's pre-registered `p0`/`p1`/`combine` from its admission entry's
`"evalue"` field and its per-step trigger observations from belief_update entries' `"trigger_checks"`
field (both additive, non-breaking conventions — see
[`research/docs/EVALUE_METHODS.md`](../../research/docs/EVALUE_METHODS.md)); every run verifies and
replays the full ledger, regenerating `<ledger>.evalue-state.json` as a derived inspection
snapshot (never read back; the ledger is never written). Hypotheses with no
`"evalue"` config are reported `no_config`, not fabricated.

## Why forward, and why a chain

A backward test of an LLM-scored process is structurally invalid (the outcomes are
already in the model's training data). Pre-registration replaces "fit the past" with
"commit, then observe the future"; the hash chain makes that commitment **auditable** — an external
reviewer can confirm that no past entry was silently changed. Proving the entry existed *before* its
outcome additionally requires binding the ledger head to an external, publicly-dated record: a
pushed Git commit (via `anchor` / `verify-anchor`), or a submission to a public timestamp service
(via `anchor external` / `verify-external`, currently OpenTimestamps — see the [main repo
README](https://github.com/yixingz3/qpop#external-anchor-what-it-proves-and-what-it-doesnt) for the
OTS-vs-Sigstore/Rekor tradeoff).

## License

MIT. Part of <https://github.com/yixingz3/qpop>.

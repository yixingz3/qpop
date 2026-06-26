---
name: auditable-research
description: Use when doing LLM-assisted research — screening candidate ideas, hypotheses, or theses, deciding whether to act on a model-generated finding, or any open-ended find-me-X task where the model could over-admit. Enforces gated, pre-registered, falsifiable research that rejects most ideas for defensible reasons, pre-registers the rest to a tamper-evident ledger, and validates forward rather than by a leaky backtest. Implements the Forward-QPOP protocol.
---

# Auditable research discipline (Forward-QPOP)

An LLM over-admits **by construction** — it is rewarded for *finding* ideas, not *refusing* them, and
it will rationalize a plausible story for almost anything. Your job here is **auditable restraint**:
admit few, and only what survives falsifiable, dated checks. "No action" is the correct, modal outcome.

## The ladder — apply IN ORDER; stop (no action) at the first failure
1. **Story or claim?** Restate the idea as a *falsifiable* claim with a mechanism. If it can't be
   stated as something that could be proven wrong, it's a story → reject.
2. **Deterministic gates (no LLM).** Apply the hard, reproducible eligibility rules for the task
   (in-scope? valid/tradeable? does it duplicate something already held → *replace, not stack*). A
   candidate that fails a gate is watchlist-only, never "free capacity."
3. **Bear case BEFORE the recommendation.** Write the strongest case *against* first. Sycophancy and
   self-generated theses collapse here. If the bear case isn't beaten on evidence, reject.
4. **Source tiers.** primary (filings/data) > secondary (reputable reporting) > market-implied
   (price/volume) > tertiary (social/opinion). **Tertiary alone never moves a conclusion.**
5. **Pre-register, forward.** Before you act, write the hypothesis to the ledger — the claim, dated
   evidence, a prior, and **measurable exit triggers** — content-hashed and dated *before* the
   outcome window. No pre-registration → no action. (See the CLI below, or the `/qpop:preregister` skill.)
6. **Forward, not backtest.** For an LLM-scored process a backward test is *structurally invalid* —
   the outcome is already in the model's training data. Validate on what happens *next*.
7. **On balance.** After overlap, cost, and uncertainty, does admitting beat doing nothing? If not → no action.

A process that admits most of what it surfaces is not doing research; it is autocompleting.

## Make it auditable: the bundled tamper-evident ledger (real, not prose)
Pre-register and verify with the hash-chained Forward-QPOP ledger — every entry is content-hashed and
chained, so any later edit, insertion, deletion, or reorder is detectable.

```bash
# 1) Register a hypothesis BEFORE evaluating its outcome:
python "$CLAUDE_PLUGIN_ROOT/scripts/qpop.py" register ledger.jsonl --json '{
  "id": "H-01",
  "claim": "<one falsifiable sentence>",
  "mechanism": "<why it should hold / is hard to bypass>",
  "prior": 0.5,
  "evidence": [{"summary": "...", "tier": "primary", "date": "YYYY-MM-DD"}],
  "exit_triggers": [{"id": "...", "metric": "...", "op": "<", "data_source": {"tier": "secondary"}}]
}'

# 2) Close it by its PRE-COMMITTED triggers (never a fresh narrative):
python "$CLAUDE_PLUGIN_ROOT/scripts/qpop.py" close ledger.jsonl --id H-01 --outcome supported

# 3) Verify nothing was changed after the fact (exits non-zero on tampering — good for CI):
python "$CLAUDE_PLUGIN_ROOT/scripts/qpop.py" verify ledger.jsonl
```

(Outcome values: `supported` | `weakened` | `falsified`. If `$CLAUDE_PLUGIN_ROOT` is unset, run from a
clone with `python scripts/qpop.py …`.)

## Deeper reference (in this plugin)
- Per-stage operating prompts: `src/prompts.md`; the deterministic gate spec: `src/gate_reference.md`.
- Full methodology + protocol: `research/docs/`.
- Theory + pilot evidence (the paper): `research/paper/`.

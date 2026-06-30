# ml_benchmark — pre-register an eval claim *before* you run it (non-finance)

The discipline isn't about finance. An ML benchmark claim has the same failure modes `qpop` exists to
counter: **over-claiming** (quietly report the seed/checkpoint that won), **look-ahead** (you tuned the
method already knowing the benchmark), and **post-hoc selection** (pick the metric or subset that looks
best after seeing results). The **over-admission rate** — accepting a weak claim as if it held — applies
verbatim.

The fix is the same as everywhere in `qpop`: state the claim *and what would falsify it*, commit it to a
tamper-evident ledger **before** the full run, anchor it, then close honestly.

> No supply-chain map, no `bottleneck_map.yml` — this uses only the domain-agnostic ledger.
> `pip install forward-qpop` (or run `python scripts/qpop.py` from a clone).

## 1. Pre-register the claim — before the full eval

```bash
forward-qpop register evals.jsonl --json '{
  "id": "ML-GSM8K-01",
  "claim": "Adapter-tuned 7B beats the LoRA baseline on GSM8K exact-match by >= 3 points.",
  "mechanism": "Adapter capacity targets arithmetic-chain steps the LoRA rank under-fits.",
  "prior": 0.5,
  "evidence": [
    {"summary": "Pilot on 200 held-out items: +4.1 EM.", "tier": "primary", "date": "2026-06-20"}
  ],
  "exit_triggers": [
    {"id": "no_gain",    "metric": "GSM8K exact-match delta vs baseline", "op": "<", "threshold": 3, "data_source": {"tier": "primary"}},
    {"id": "regression", "metric": "MMLU delta vs baseline",              "op": "<", "threshold": 0, "data_source": {"tier": "primary"}}
  ]
}'
```

The triggers are the honesty contract: "< 3 EM points" *or* "any MMLU regression" would **falsify** the
claim. You commit to them now, when you cannot yet see the full-test result.

## 2. Anchor it (so it provably predates the result)

```bash
forward-qpop anchor evals.jsonl                       # writes evals.jsonl.anchor.json
git add evals.jsonl && git commit -m "pre-register ML-GSM8K-01"   # the commit date is the anchor
```

## 3. Run the eval, then close honestly

```bash
# ... run the full GSM8K + MMLU eval ...
forward-qpop close evals.jsonl --id ML-GSM8K-01 --outcome weakened \
  --observed '{"gsm8k_em_delta": 1.2, "mmlu_delta": 0.3, "note": "full-set gain 1.2 < pilot 4.1; the >=3 bar was not met"}'
forward-qpop verify evals.jsonl    # OK — 2 entries, chain intact (the registered claim included)
git commit -am "close ML-GSM8K-01: weakened — under the pre-registered bar"
```

Because the claim and its falsifiers were locked and anchored first, "1.2 < 3 → weakened" is on the
record — you cannot retroactively soften the bar or drop the unflattering MMLU number. That is the
over-admission discipline applied to ML research instead of markets.

The pre-registration commit predates the close commit in your git history — that is the forward proof.
`verify` guarantees the chain (claim *and* outcome) was never edited. `verify-anchor` against the
**pre-eval** manifest will now report that the ledger *grew* (the outcome you legitimately appended) —
expected, not tampering; re-run `anchor` after closing if you want standalone drift-detection on the
final record.

## See also
- The method — [`auditable-research`](../../skills/auditable-research/SKILL.md)
- The ledger API — [`forward_qpop`](../../src/forward_qpop/README.md)
- The OAR benchmark — the paper, [`research/`](../../research)

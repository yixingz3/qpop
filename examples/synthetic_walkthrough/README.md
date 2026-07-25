# Synthetic end-to-end walkthrough — one candidate, every stage

**Everything in this directory is fictional.** `ZZNEO` / "Synthetica Gas Works" do not exist; the
UHP-neon-reclaim premise is a pedagogical construction. Any resemblance to a real security is
coincidental, and nothing here is investment analysis or advice. The point is the **method**: this
is the complete candidate-to-outcome trace the paper's review round asked for (R1-17), scored
against the released rubric ([`../../src/scoring_rubric.md`](../../src/scoring_rubric.md)) so a
reader can check every number.

Two kinds of steps appear below, and the boundary is marked honestly:

- **[RUNNABLE]** — executed by [`run_walkthrough.py`](run_walkthrough.py) with the public package
  on a clean clone, offline (`python examples/synthetic_walkthrough/run_walkthrough.py`).
- **[DOCUMENTED]** — the LLM/gate stages of the production funnel. The released artifacts specify
  them (stage prompts in [`../../src/prompts.md`](../../src/prompts.md), gate spec in
  [`../../src/gate_reference.md`](../../src/gate_reference.md)); this walkthrough shows their
  *inputs and outputs* for the synthetic candidate, worked by hand against those specs — the
  production engine that automates them is private.

## 0. The card [DOCUMENTED — SOURCE stage]

[`candidate_card.json`](candidate_card.json) (validates against
`schemas/candidate_card.schema.json`): `ZZNEO`, proposed for the synthetic node
`neon_reclaim_skids` ([`bottleneck_map.yml`](bottleneck_map.yml)) as a **direct** beneficiary —
one of two qualified reclaim-skid OEMs, with dated primary evidence (segment = 35% of revenue,
booked POs) and the risks stated up front (episodic pricing power; 65% of the company is
unrelated distribution).

## 1. GATE [DOCUMENTED — deterministic, no LLM]

Per `gate_reference.md`: tradeable venue listing ✓; price above floor ✓; 60-day dollar-volume
above floor ✓ (synthetic premise); max 60-day correlation to held core = 0.31 with zero existing
weight in the node → negligible overlap penalty → **PASS → finalist**. (A FAIL would end the walk
here as *watchlist, never free capacity*.)

## 2. TRIAGE [DOCUMENTED — cheapest tier]

Not an obvious non-starter: not a diversified giant with a trace segment (35% is material), not a
commodity price-taker (certification moat), not pre-revenue → **pursue**.

## 3. EVALUATE — bear case first, then the rubric [DOCUMENTED]

**Bear case (written before any recommendation, per the discipline):** reclaim capacity is
answerable by new-build air separation on a 2–3 year lag — the moat is a *lead time*, not a
permanent wall; pricing power is episodic (spikes on shocks, mean-reverts); 65% of the company
dilutes the thesis; a neon-frugal laser platform would break the node outright.

**Scores, each read off the released rubric's anchors:**

| Factor | Score | Anchor justification (rubric row) |
|---|---|---|
| `physical_indispensability` | 0.8 | no qualified laser operation without UHP neon; between "no route without it" (0.9) and substitutable-at-cost (0.5) |
| `substitutability`⁻¹ | 0.7 | alternatives exist (new ASU trains) but qualification barrier documented |
| `capacity_lead_time` | 0.8 | skid certification + fab qualification ≈ 2–3 y |
| `supplier_concentration` | 0.8 | two qualified OEMs (synthetic premise) |
| `pricing_power` | 0.6 | episodic, not contractual — between mixed (0.5) and realized escalation (0.9) |
| **`bottleneck_score`** | **0.740** | mean of the five dims (*reference definition*) |
| `exposure_purity` | 0.6 | 35% of revenue → "major line, 30–70%" row, low end (margin undisclosed → no credit) |
| `demand_score` | 0.7 | booked capacity POs in primary sources — the 0.7 anchor verbatim |
| `valuation_adjustment` | 0.8 | constraint partially priced after a supply-shock headline (between 0.85 and 0.7) |
| `crowding_adjustment` | 0.85 | known story, not crowded — the 0.85 anchor |

```
confidence = 0.740 × 0.6 × 0.7 × 0.8 × 0.85 = 0.2113
tier: 0.2113 < 0.22 (core)  and  ≥ 0.10  →  SATELLITE
```

**This case is deliberately threshold-marginal** (the rubric's sensitivity rule in action): the
minimum factor is purity (0.6), and purity 0.63 — a plausible read if the undisclosed skid margin
ran richer than the corporate average — would put confidence at 0.222, across the core line. Per
the rubric, the admission entry must say so: *threshold-marginal; tier flips on ±0.05 of one
factor; min factor = purity.* Two readers who differ by >0.1 on purity would send this to
watchlist, not average their disagreement away.

## 4. ADJUDICATE [DOCUMENTED — expensive tier, admit-flags only]

The admit-flag is re-judged with the full record: the bear case does not break the node (the lag
*is* the thesis window), the entry is not crowded, and satellite sizing already prices the
dilution → **admit at satellite**, with the contract below.

## 5. Pre-registration [RUNNABLE]

`run_walkthrough.py` registers `H-NEON-01` to a fresh hash-chained ledger **before any outcome
window**: the falsifiable claim, both dated evidence items, three checkable exit triggers
(capacity glut / substitution breakthrough / crowding reversal — each with a named source tier),
the full score decomposition, the tier, and a **frozen e-value commitment**
(`p0=0.10, p1=0.60, combine=average`) hashed with the entry.

## 6. Monitoring, sequential test, anchor, tamper-evidence [RUNNABLE]

A dated belief update carries `trigger_checks` for **all three registered triggers** (none
fired); `forward-qpop evalue` replays the ledger in registered fixed-membership mode — all three
triggers enter the average from step 0 (`n_triggers = 3`), merged e-value 0.4444 vs threshold 20
→ **continue**, the thesis stands. The anchor manifest is written and verified; then the script
edits one frozen word in a copy of the ledger and shows verification **fail loudly** — the
tamper-evidence the whole contract rests on.

Expected final line: `WALKTHROUGH PASS`.

## What this walkthrough is and is not

It **is** the complete decision trace the method produces — every number derivable from released
artifacts, every runnable step actually run, pinned by `tests/test_synthetic_walkthrough.py`. It
is **not** a claim that a clean clone can run the production funnel: the SOURCE/TRIAGE/EVALUATE/
ADJUDICATE stages above are documented against the released prompts and gate spec, and our
empirical results remain reported aggregates (see the paper's *Reproducibility and Release*).

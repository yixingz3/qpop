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
one of two qualified reclaim-skid OEMs, with dated evidence for **every scored factor**: segment
= 35% of revenue, booked POs, the two OEMs' ≥70% share of certified installs, rich valuation with
the cycle already in consensus, moderate non-crowded positioning, one partial price-escalator
clause — and the risks stated up front (episodic pricing power; 65% of the company is unrelated
distribution).

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
| `physical_indispensability` | 0.7 | ON-ANCHOR: a route exists only via qualified redesign (new ASU trains + laser re-qualification) |
| `substitutability`⁻¹ | 0.7 | ON-ANCHOR: alternatives exist behind a documented qualification barrier |
| `capacity_lead_time` | 0.7 | ON-ANCHOR: 2–3 years including fab qualification |
| `supplier_concentration` | 0.9 | ON-ANCHOR: two qualified OEMs ≥70% (synthetic premise) |
| `pricing_power` | 0.5 | STRADDLE→LOWER: evidence fully supports "mixed/episodic" (0.5) and one partial escalator clause only *suggests* "contracted escalators, partial" (0.7) → the rule takes 0.5 |
| **`bottleneck_score`** | **0.70** | mean of the five dims (*reference definition*) |
| `exposure_purity` | 0.7 | ON-ANCHOR: 35% of revenue = the "major line, 30–70%" row |
| `demand_score` | 0.7 | ON-ANCHOR: booked capacity POs in primary sources |
| `valuation_adjustment` | 0.70 | ON-ANCHOR: "rich; consensus already carries the thesis" — the card's peer-premium + cycle-in-consensus evidence |
| `crowding_adjustment` | 0.85 | ON-ANCHOR: known story, not crowded |

```
confidence = 0.70 × 0.7 × 0.7 × 0.70 × 0.85 = 0.2041
tier: 0.2041 < 0.22 (core)  and  ≥ 0.10  →  SATELLITE
```

Every score is a published anchor value assigned from evidence **in the released card** (the
scale is discrete — no free interpolation; the one straddle, pricing power, is resolved by the
rule), so two independent readers derive the **same factor vector**, tier, and marginality flag
without seeing this table.

**This case is threshold-marginal under the rubric's definition** (a one-step move of any single
factor to its adjacent published anchor flips the tier): valuation one step up (0.70 → 0.85,
"roughly fair") gives 0.70 × 0.7 × 0.7 × 0.85 × 0.85 = 0.2478 — across the core line — so the
admission entry must carry the marginality flag. And per the tier-aware disagreement rule, a
second reader who read the valuation evidence as "roughly fair" rather than "rich" would flip the
derived tier — that disagreement is unsettled regardless of its size, sending the candidate to
watchlist until a dated source settles it.

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

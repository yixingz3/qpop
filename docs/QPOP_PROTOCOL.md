# QPOP Protocol — forward pre-registration ledger

**QPOP** = a forward hypothesis ledger. It adapts pre-registration / registered-reports discipline
from empirical science into agent-assisted investment research, *without* relying on a backtest.

## Why forward, not backtest

For a young or structurally-shifting universe (recent IPOs, a thesis the market is actively
re-rating), a long backtest is fragile: regime change, survivorship, and lookahead leakage make it
easy to overfit a story. Pre-registration replaces "fit the past" with "commit, then observe the
future." The ledger is the contract against **HARKing** (hypothesizing after results are known) and
**data-snooping**.

## Entry types

1. **Admission** — a node or ticker enters the map (especially at meaningful weight) *only* via a
   pre-registered hypothesis: the binding-chokepoint claim, dated evidence + source tier, the
   expected return driver, the decomposed confidence, and **measurable exit triggers committed in
   advance**. No pre-registration → no capital.
2. **Belief update** — every confidence change is a recorded, **content-hash-protected** posterior
   update with cited evidence. *Tertiary sources alone cannot move confidence.*
3. **Outcome** — when a trigger fires or the thesis ages into consensus, the entry is closed
   **Supported / Weakened / Falsified**, with the observed metrics. **Closed entries are immutable —
   open a new id to revise.**

## Entry schema (illustrative)

```yaml
id: H-<DOMAIN>-<NN>
created: <date>
status: open            # open | supported | weakened | falsified
role_admitted: satellite   # never straight to core
claim: "<the binding-chokepoint claim, in one sentence>"
mechanism: "<why it is hard to bypass>"
decomposed_confidence:
  bottleneck_score: 0.0
  exposure_purity: 0.0
  demand_score: 0.0
  valuation_adjustment: 0.0
  crowding_adjustment: 0.0
  final_confidence: 0.0
objective_gates: { tradable: true, min_price: true, min_dollar_volume: true, overlap_penalty: 0.0 }
exit_triggers:            # committed BEFORE the position; each has a checkable data_source
  - { id: supply_easing,    metric: "...", op: "<", data_source: { name: "...", tier: secondary } }
  - { id: demand_slowing,   metric: "...", op: cut, data_source: { name: "...", tier: primary } }
  - { id: crowding,         metric: "price vs estimate-revision gap", op: ">", data_source: { tier: market_implied } }
prior_confidence: 0.0
evidence:                 # dated, source-tiered
  - { summary: "...", tier: primary, date: <date>, url: "..." }
content_hash: "<hash of the frozen fields>"
```

## The content hash

The load-bearing fields (claim, exit_triggers, decomposed_confidence, prior) are hashed at
creation. Any later edit to a *closed* entry breaks the hash and is rejected. This makes the ledger
**auditable** — an external reviewer can verify the hypothesis was registered *before* the outcome.

## Posterior recording

After each forward observation window:

- Did a pre-registered trigger fire? → reduce/exit per the rule, record the outcome. *Never a story.*
- Did the thesis age into consensus (valuation/crowding adjustments collapse)? → Weakened.
- Did the chokepoint hold and the driver play out? → Supported.

The accumulated `(hypothesis → decision → forward outcome)` tuples are a reusable, auditable
**dataset** — both the empirical core of the methods paper and the fuel for calibrating the gates on
realized outcomes (the self-improvement loop).

# Scoreboard — forward validation discipline

The objective is **not** raw P/L. It is **repeatable, benchmark-relative excess return subject to
drawdown, concentration, and auditability constraints** — and, in the research-framework framing,
the *discipline metrics* matter as much as the return.

> **Do not confuse being in a hot theme with generating alpha.** If the theme benchmark is +20% and
> the book is +18%, that is *negative* alpha. Judge against the theme benchmark, not against cash.

## Judged on conservative shadow fills

Track-record metrics are computed on a **conservative shadow fill** (opening print + an assumed
adverse slippage), not on optimistic fills. Paper/broker fills validate automation and idempotency
only. This keeps the record honest and forward-looking.

## Two kinds of metric

**Discipline metrics (available immediately, the methods-paper core):**

- candidate count · gate-pass rate · **admission rate** · no-action rate
- source-tier distribution of admitted evidence · overlap-penalty distribution
- pre-registration integrity (every admission has a content-hashed QPOP entry)

**Performance metrics (require ≥ ~20 forward snapshots before they mean anything):**

- excess return vs the theme benchmark · information ratio · active drawdown
- gross / net thematic beta · turnover · shadow-fill slippage

## Process gates first, performance gates later

Sample size is tiny early, so do **not** set "Sharpe must be X" before forward data exists.

1. **First weeks (process gates):** the daily loop works; shadow fills are realistic; every weight
   is explainable; no dumb concentration; the admission rate stays low and pre-registered.
2. **After ~20 forward snapshots (performance gates):** IR > 0; excess return > 0 vs the theme
   benchmark; drawdown not worse than the benchmark by more than a set band; turnover justified.

## Harvest through caps, not vibes

No "take profit at +X%" (that sells the best winners early). The book harvests *mechanically*: a
position over target + drift band, a binding ticker/node/layer cap, a binding thematic-beta cap, a
fired crowding trigger, a falling valuation adjustment, or a thesis aging into consensus.

## The headline result is the admission rate

For a *methods* paper, the most defensible empirical claim is not "we beat the market" (premature,
no forward record) — it is that **the disciplined pipeline rejects most LLM-surfaced ideas**, with
a low, pre-registered admission rate, and that every admitted position is explainable and auditable.
That restraint is the measurable contribution; the performance section is filled in as forward data
accrues.

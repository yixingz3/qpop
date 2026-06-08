# Initial Results (discipline metrics)

> **Not a performance claim.** Forward returns are not yet observed; these are *discipline* metrics
> from real candidate batches, reported per the experiment plan (H1 restraint, H5 rejection quality).
> They are the empirical core the paper can show *today* without waiting on the forward window.

## The funnel, on a real batch

A discovery session (2026-06-07, AI-supply-chain domain) over under-covered chokepoint layers:

```
~87 candidate cards sourced   (12 lenses: per-node + gaps + social + policy + literature)
   -> ~25 unique new symbols
   -> deterministic GATE       (tradeability + liquidity + overlap; foreign-OTC and
                                sub-threshold-liquidity names rejected mechanically)
   -> 24 evaluated finalists    (bear-case-written-before-recommendation)
   ->  0 admitted this session  (prior build-out sessions admitted 3, all at small satellite)
```

Admission rate among evaluated finalists **this session: 0/24**; trailing admission rate across the
build-out is **low single digits** — consistent with H1 (`< 10%`). Two consecutive 0-admit rounds
were *not* a failure of sourcing; the gate-passers were diversified mega-caps (chokepoint = a tiny
segment) or pre-revenue, and the genuinely pure vehicles surfaced were foreign-OTC and failed the
US-tradeability gate. "No action" is the modal outcome.

## Rejection-quality audit (H5)

The central objection to a low admission rate is that *a system can reject 95% of ideas by being
arbitrarily conservative.* So a **held-out independent LLM auditor** was shown only the steelmanned
**bull** case and the decision — **not** the engine's bear case — and asked to label each sampled
rejection JUSTIFIED or FALSE REJECTION with a category.

| Metric | Value |
|---|---|
| Sampled rejections audited | 14 |
| **Rejection precision** (judged justified) | **0.93** (13/14) |
| False rejections | 1 |
| False-rejection rate | 7% |

Category distribution of justified rejections: low-purity-conglomerate ×8, commodity-cycle ×2,
pre-revenue/hype ×2, duplicate-overlap ×1.

**The one flagged false rejection is reported, not hidden** — it is the most useful output. The
auditor judged an early-stage pure-play (a primary-sourced design win, no conglomerate dilution)
admissible at small satellite where the engine had said "watchlist," and noted a **mild systematic
over-caution on early-stage pure-plays.** That single disagreement is a credibility signal — the
audit is adversarial, not a rubber stamp.

**But the layering corrected the auditor, not the engine.** Because the audit's verdict was itself a
*flag*, not a final decision, the flagged name went to an independent capital-at-risk **adjudication**
(the expensive model, with fresh web verification). The adjudication surfaced the load-bearing fact
the bull-only auditor had missed — the name's headline design win is **shared across a 14-member
supplier alliance that already includes a name the book holds**, so the candidate is one of fourteen
substitutable suppliers, not a chokepoint owner — and **upheld the original rejection.** The
*effective* rejection precision after adjudication is therefore **14/14**. The methodological point
is the architecture, not the number: a cheap, bull-biased audit *should* occasionally push to admit,
and the expensive adjudication layer exists precisely to catch that over-correction — the same
cheap-screen → expensive-adjudicate asymmetry that governs admissions also governs the audit of
rejections. We report both the raw audit (0.93) and the post-adjudication result (1.00) rather than
only the flattering one.

## Worked example (one of each)

- **Admitted** (earlier session): a critical-material chokepoint, gated through purity *and* a
  separate critical-inputs concentration cap, admitted at **half** the unconstrained satellite weight
  — restraint expressed as *sizing*, not just selection.
- **Rejected:** a commodity-cycle miner — real AI-driven demand, but a price-taker with no supplier
  pricing power; admitting it would buy commodity beta, not chokepoint economics.
- **Overlap-penalized:** a high-purity pure-play that *duplicated* a held incumbent in a full node
  sleeve → routed to a **replace-not-stack** decision (a future replacement candidate), not a
  standalone add.

## What is still pending (declared)

- **Ablations / baselines** (ungated screener, debate-only, no-Forward-QPOP-lock, no-overlap-penalty)
  on the same candidate stream — the comparison that shows the full pipeline rejects *more* **and**
  *better*, per H2 and the baselines in the experiment plan.
- **Forward outcomes** (H4) — accrue over the forward window; reported only with the structural-
  validity checklist.

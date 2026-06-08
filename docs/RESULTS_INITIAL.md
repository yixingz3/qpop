# Initial Results (discipline metrics)

> **Pilot metrics — not a performance claim, and not confirmatory.** This validates *process
> discipline*, not investment profitability (which awaits H4). The numbers below are pilot / initial
> discipline metrics that *motivate* the registered evaluation, not confirm it. Forward returns are
> not yet observed; these are *discipline* metrics
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

**Metric precedence:** primary = raw auditor precision **0.93** (Wilson 95% CI [0.69, 0.99]);
secondary = post-adjudication resolution 1.00 (reported only to show the layering works);
interpretation = the single auditor/engine disagreement is a useful diagnostic signal. The takeaway
is the raw 0.93, *not* an "effective 14/14."

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
substitutable suppliers, not a chokepoint owner — and **upheld the original rejection.** A process
that overrules its own auditor and then reports 100% would read as circular, so we **headline the raw
auditor precision (0.93; Wilson 95% CI [0.69, 0.99]; disagreement 0.07)** and report the adjudicated
**1.00 only as a secondary resolution mechanism** — the 0.93 is already good and doesn't need the
1.00. The methodological point is the architecture, not the number: a cheap, bull-biased audit
*should* occasionally push to admit, and the expensive layer exists to catch that — the same
cheap-screen → expensive-adjudicate asymmetry that governs admissions.

## Worked example (one of each)

- **Admitted** (earlier session): a critical-material chokepoint, gated through purity *and* a
  separate critical-inputs concentration cap, admitted at **half** the unconstrained satellite weight
  — restraint expressed as *sizing*, not just selection.
- **Rejected:** a commodity-cycle miner — real AI-driven demand, but a price-taker with no supplier
  pricing power; admitting it would buy commodity beta, not chokepoint economics.
- **Overlap-penalized:** a high-purity pure-play that *duplicated* a held incumbent in a full node
  sleeve → routed to a **replace-not-stack** decision (a future replacement candidate), not a
  standalone add.

## Ablation: each discipline contributes to restraint (H2)

The same **38-candidate batch** was run through baselines that each *remove one discipline*, and
their admission rates compared to the full pipeline. (The batch is a real sourced round; the
candidate cards are identical across arms — only the decision discipline changes.) The full
baseline prompt, model version, and temperature are released (`src/prompts.md`; cards sanitized) so
a reader can judge whether the ungated arm was unfairly admission-biased — the ungated baseline was
**allowed to reject**, not a strawman forced to admit.

| Arm | Admitted | Rate |
|---|---|---|
| **Full pipeline** (gate + seen-set + triage + bear-case-first + overlap) | **0 / 38** | **0%** |
| − overlap penalty (judge each name on its own, ignore duplication with the held book) | 25 / 38 | 66% |
| − bear-case-first (recommend from the bull thesis, no written bear case) | 28 / 38 | 74% |
| **Ungated LLM screener** (no gate, purity, overlap, or bear case — "is the thesis good?") | **38 / 38** | **100%** |

The result is monotone and decisive: an **ungated LLM admits literally every candidate** (the
"over-admits by construction" failure made concrete); removing *any single* discipline raises the
admission rate far past H2's threshold (≥ 25% relative *or* ≥ 5 pp); and the full stack drives
100% → 0%. This is the comparison the headline needs — the pipeline admits **fewer** ideas, and the
earlier rejection audit (raw 0.93) shows the ones it keeps out are mostly the right ones. H2 is
**supported** for every ablated discipline.

> A reviewer's exact objection — "a system can reject 95% of ideas by being arbitrarily
> conservative" — is answered by these two results together: the ablation shows the rejections come
> from *specific, removable disciplines* (not blanket conservatism), and the audit shows they are
> *justified*.

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

- **Remaining baselines** (debate-only, no-Forward-QPOP-lock) — the three run here (ungated,
  bear-case-off, overlap-off) cover the core H2 disciplines; the remaining two are additive.
- **Forward outcomes** (H4) — accrue over the forward window; reported only with the structural-
  validity checklist.

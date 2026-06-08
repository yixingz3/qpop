# Method

The framework turns open-ended, LLM-driven discovery into *disciplined, auditable, falsifiable*
research by composing five mechanisms. Each exists to neutralize a specific, well-documented
failure mode of using LLMs for investment research.

| Mechanism | Failure mode it neutralizes |
|---|---|
| Bottleneck graph + confidence decomposition | "right theme → buy the ticker"; theme-chasing |
| Cheap-source → deterministic-gate → expensive-evaluate funnel | cost blow-up; shallow, ungrounded judgment |
| Bear-case-before-recommendation | sycophancy; one-sided narratives |
| Forward-QPOP pre-registration | HARKing; data-snooping; backtest overfitting |
| No-stories discipline + admission restraint | confabulation; over-admission; narrative drift |

## 1. The bottleneck graph (the portable thesis)

A domain is a **graph of physical chokepoints**. Nodes are bottlenecks (a step that is hard to
bypass, capacity-constrained, supplier-concentrated); edges encode dependency. The graph is
domain-agnostic: AI accelerators today, rare-earth refining / power transformers / LNG / uranium /
copper tomorrow — each is *a different `bottleneck_map.yml`*, not a different codebase.

Each node carries: a physical rationale, `bottleneck_dims` (physical_indispensability,
substitutability⁻¹, capacity_lead_time, supplier_concentration, pricing_power), a `demand_score`,
node-level `valuation_adjustment` / `crowding_adjustment`, and **measurable `exit_triggers`, each
with a checkable `data_source`** (an admission rejects any trigger you cannot actually check).

### What makes a chokepoint an *edge*: uncertainty about the constraint

A binding chokepoint is necessary but **not sufficient** for a tradeable edge. The edge lives in the
**uncertainty about the constraint** — how much of the scarcity is *not yet known or priced*. The
question is not only *"is this a chokepoint?"* but *"how anticipated is it?"*

- **Physical chokepoints** (refining capacity, fab lead-times, permits, ore grades) keep their
  pricing power because their magnitude and timing are **uncertain and discovered late** — the market
  learns the bottleneck is binding only as lead-times stretch and inventories empty. The
  `capacity_lead_time` and `supplier_concentration` dims are proxies for exactly this *unpriced*
  scarcity.
- A **synthetic / scheduled constraint** with a *known date and a known, shrinking magnitude* gets
  **arbitraged toward zero edge** — the market prices it in earlier each time it recurs. The
  canonical case is Bitcoin's *halving*: a real algorithmic supply cut, but the most pre-announced
  supply event in finance, whose marginal shock shrinks each cycle (≈1.7% → 0.83% → 0.41% of supply)
  *and* which the market now front-runs (a pre-halving all-time-high in 2024). Real constraint, no
  durable edge.

This is the same principle as **policy-as-evidence**: an event *already in the price* is sunk
information, not alpha (a signed award that has already fired, an extended/anticipated cycle). It is
why the `valuation_adjustment` and `crowding_adjustment` exist — they discount a constraint the
market has already learned. **Prefer chokepoints whose binding is still being discovered** (lead-times
stretching, the re-rate ahead) over ones whose schedule everyone already trades.

## 2. Confidence decomposition (kills theme-chasing)

```
confidence = bottleneck_score   # NODE: how binding the chokepoint is (composite of the dims)
           × exposure_purity     # TICKER: does this name actually capture the bottleneck economics
           × demand_score        # NODE: order visibility / capex pull
           × valuation_adjustment # TRADE (<=1): penalize already-priced-in
           × crowding_adjustment  # TRADE (<=1): penalize crowded / overextended
```

A correct node with a poor proxy (low purity) or a crowded entry yields *low* confidence. Tier is
**derived** from confidence (e.g. core ≥ 0.22, satellite ≥ 0.10, below → dropped), not asserted.

### Policy is *evidence*, not a factor

Government policy (subsidies, awards, export controls, strategic-autonomy programs) is a real,
sometimes durable driver — but it enters as **dated evidence + a monitor trigger**, never as a
multiplicative `policy_adjustment`. A multiplier manufactures a number from a *forecast* (is it
durable? bipartisan?) — the no-stories failure mode in a lab coat. Two cases instead:

- **Tailwind on a name with a real chokepoint** → record a (loader-inert) `policy:` evidence block
  + a wired `policy_reversal` exit trigger (clawback / milestone miss / reversal). It does **not**
  resize the name.
- **Underdog whose thesis *is* policy** → a *separate, capped* sleeve, admitted via the normal
  gates, never core.

**Fact vs announcement:** a *signed, dated, material* award is citable evidence; a political
headline / pledge is watchlist-context only. The clinching lesson: a multiplier *rewards the
existence* of policy — but a signed award that has *already fired* (in the price) with its clawback
removed is sunk information turned into a *liability*; the evidence-and-trigger framing forces the
right questions (*has it already fired? what would reverse it? does it unlock capacity?*).

## 3. The funnel (budget-aware multi-agent discovery)

```
SOURCE   →  GATE        →  EVALUATE
cheap LLM   deterministic   expensive LLM (finalists only)
wide        script, no LLM  bear-case-first, written before the recommendation
```

- **SOURCE** (cheap model, e.g. a small/fast LLM): high-volume, low-judgment candidate cards with
  dated, source-tiered evidence — one lens per node, plus gap / social / policy lenses.
- **GATE** (no LLM): tradeability + liquidity + **overlap penalty** vs the existing book. Pure,
  reproducible, cheap. A name failing the gate is watchlist-only, never "free capacity."
- **EVALUATE** (expensive model, *finalists only*): deep fit + a **bear case written before the
  recommendation** + a falsifiable decision. Reserve the scarce model for capital-at-risk judgment.

**Model allocation is a knob** (`docs/TUNING.md`): when the expensive pool is scarce, run a
*cheap-model first-pass* EVALUATE and reserve the expensive model to **adjudicate only the names the
first pass flags as admit** — the asymmetry is safe because a false-watchlist merely delays a name,
while a false-admit is caught by the adjudication.

## 4. Forward-QPOP (pre-registration without a backtest)

For a young or structurally-shifting universe, a long backtest is fragile (regime change,
survivorship, lookahead). Instead, every admission and belief change is a **pre-registered,
content-hashed entry** in a forward ledger (`docs/QPOP_PROTOCOL.md`): the binding-chokepoint claim,
dated evidence + source tier, the expected return driver, **measurable exit triggers committed in
advance**, and the decomposed confidence. Outcomes are recorded forward (Supported / Weakened /
Falsified) as triggers fire or the thesis ages. Pre-registration is the contract against HARKing —
you cannot rewrite the hypothesis after seeing the result.

## 5. No-stories discipline + forward validation

- **Source tiers:** primary (filings/transcripts) > secondary (reputable trade press) >
  market-implied (price/volume) > tertiary (social — *idea seed only*, never establishes
  confidence). A confidence move requires ≥ secondary or market-implied corroboration.
- **Overlap penalty:** every candidate is judged *against the book you already hold* — a great
  theme that duplicates a held bet must **replace, not stack** (gate = comparison, not veto).
- **Structural vs cyclical:** distinguish a hard chokepoint (few suppliers, multi-year capex) from
  a commodity-cycle peak riding a bullwhip; the latter is the trap that *looks* like the winner.
- **A position changes only on** a fired pre-registered trigger, a binding cap, or a risk limit —
  **never a narrative.**
- **Validation is forward:** track-record metrics are judged on *conservative shadow fills*
  (opening print + assumed slippage), benchmark-relative, with the accumulated ledger as the
  dataset. The system is optimized for *auditability*, not cleverness — every weight must be
  explainable by score × purity × adjustments × caps × drift, or no position is taken.

## Why the admission rate is the headline — and why it is not enough alone

A naïve LLM screener over-admits by construction — it is rewarded for *finding* ideas. This
framework is rewarded for *refusing* them: most candidates are on-theme yet fail "does this improve
the book after overlap, purity, valuation, and crowding?" The low admission rate, achieved by
pre-committed gates rather than after-the-fact judgment, is one measurable contribution.

But a low admission rate is **not, by itself, evidence of quality** — a system can reject 95% of
ideas by being arbitrarily conservative. So restraint is reported with two companions:

- **Rejection quality (rejection precision).** A held-out auditor (an independent LLM and/or a human),
  shown only the *bull* case and the decision — **not** the engine's bear case — labels each sampled
  rejection JUSTIFIED or a FALSE REJECTION, with a category (low-purity / duplicate-overlap /
  valuation-or-crowding / commodity-cycle / pre-revenue-or-hype / unverifiable-or-untradeable). The
  headline pairs *admission rate* (how much is rejected) with *rejection precision* (whether it
  should have been). High restraint + low rejection precision would be a failure, not a success.
- **Ablation against baselines.** The same candidate stream is run through an ungated screener,
  debate-only, no-Forward-QPOP-lock, and no-overlap-penalty variants; the claim is that the full
  pipeline admits *fewer* ideas **and** that its rejections are better justified — not merely that
  gates reduce the count.

Outcome decisions over many triggers and positions use a **sequential test with explicit Type-I
control** (an anytime-valid / e-value formulation), so monitoring many exit triggers does not inflate
false "Falsified" calls — the prospective analogue of the factor-zoo multiple-comparisons problem.

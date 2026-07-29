# Anchored scoring rubric (the released reference)

This is the anchored rubric for the five confidence factors — the release the v2 review round
committed to (R1-10; revise-round item C3-08). Together with the reference gate
([`gate_reference.md`](gate_reference.md)) and the stage prompts ([`prompts.md`](prompts.md)), it
makes the scoring **usable**: two independent readers can score the same sanitized card and see
why it crosses or misses a tier. A complete synthetic worked example applying every anchor is
[`../examples/synthetic_walkthrough/`](../examples/synthetic_walkthrough/).

**Boundary and provenance.** This file is a **post-hoc public operationalization** of the same
five factors and multiplicative structure the framework has always used, authored (2026-07-25) to
make future and adopter scoring inspectable. It is **not** a reconstruction of the exact rubric or
dim weighting that generated historical pilot scores (the contemporaneous private map labeled its
factor values draft/first-pass estimates, and production uses a private weighted dim composite
where this reference uses a mean). Where this file must choose a reference convention (marked
*reference definition*), the convention is normative for public use. Scores are assigned at the EVALUATE stage (bear-case-first), re-judged at ADJUDICATE for
admit-flags, and an operator may override only via a dated, hash-chained ledger amendment — never
silently.

```
confidence = bottleneck_score × exposure_purity × demand_score
           × valuation_adjustment × crowding_adjustment
tier: core ≥ 0.22 · satellite ≥ 0.10 · below → dropped
      (watchlist is a decision class — parked with a dated trigger — not a confidence tier)
```

**Threshold provenance.** The 0.22 / 0.10 tier cuts were chosen **heuristically** in the
2026-06-06 Phase-0/1 build-out configuration to partition the then-current seed map's
multiplicative-confidence range (roughly 0.06–0.34), before the 2026-06-08 forward window and
before any prospective outcomes accrued. They were **not fit to forward-window outcomes**; their
calibration remains unvalidated and is a declared December read-out question.

## Factor anchors

The released reference scale is **discrete**: a factor may take only the published anchor values
in its table below — no interpolation. **Straddle rule:** when the evidence fully supports one
anchor and partially suggests the next higher one, take the **lower** fully supported anchor (the
conservative tie-break; consistent with the framework's false-watchlist-over-false-admit
asymmetry). The 25% segment-revenue cut in `pricing_power` is an **uncalibrated
public-reference convention** chosen for determinism, not an empirically validated historical
threshold. **Never default a factor you cannot assess** (see Missing data below). Evidence tiers
apply: an anchor claimed from tertiary sources alone is not established (source-tier rule).

### `bottleneck_score` — node: how binding is the chokepoint?

*Reference definition:* the mean of the five `bottleneck_dims`, each anchored below. (The released reference scores every dim against these anchors; the private engine's
historical weighting and factor elaborations remain unspecified here.)

| Dim | 0.9 — binding | 0.7 — strong | 0.5 — contestable | 0.2 — soft |
|---|---|---|---|---|
| `physical_indispensability` | no known process route without this step/input | route exists only with qualified redesign | substitutable at material (2–3×) cost | convenience input; routes around it exist |
| `substitutability`⁻¹ | no qualified alternative supplier/process | alternatives exist behind a documented qualification barrier (certification, change-control) | alternatives exist; switching costs real but bounded | commodity — many interchangeable sources |
| `capacity_lead_time` | ≥3 years greenfield (permits, certification, construction) | 2–3 years including qualification | 1–2 years | <1 year, or idle capacity restartable |
| `supplier_concentration` | 1–2 suppliers hold ≥70% share | 2–3 suppliers dominate; entrant unqualified | top-3 hold ~50% | fragmented |
| `pricing_power` | realized price escalation across ≥25% of segment revenue, visible in filings/contracts | escalators contracted but not yet fully realized across ≥25% of segment revenue | mixed/episodic pricing, or escalator clauses covering <25% of segment revenue | price-taker |

### `exposure_purity` — ticker: does this name capture the node's economics?

| Anchor | Observable |
|---|---|
| 0.9 | pure play — the node is the principal business (segment >70% of revenue/EBIT, filings-verifiable) |
| 0.7 | major line — 30–70% of economics; the node drives the growth story |
| 0.5 | material but diluted — 10–30%; a conglomerate arm |
| 0.3 | minor segment — <10% of economics |
| 0.2 | trace or narrative-only exposure (the "integrated major with a 1% chokepoint segment" case) — reject territory; evidence below this description is a reject, not a lower numeric choice |

### `demand_score` — node: order visibility, not enthusiasm

| Anchor | Observable |
|---|---|
| 0.9 | contracted multi-year backlog / take-or-pay disclosed (primary) |
| 0.7 | purchase orders or capacity bookings visible in primary sources |
| 0.5 | credible forecast pull, corroborated by secondary sources |
| 0.3 | thematic inference only |
| 0.2 | narrative demand — no dated evidence; anything weaker is a reject, not a lower numeric choice |

### `valuation_adjustment` — trade (≤1): how much of the scarcity is already priced?

| Anchor | Observable |
|---|---|
| 1.00 | dislocated or ignored — valuation below information-peer median while the constraint is absent from consensus estimates |
| 0.85 | roughly fair; constraint partially priced |
| 0.70 | rich; consensus already carries the thesis |
| 0.50 | priced for perfection — the thesis reduces to "the multiple holds" (usually a bear-case watchlist, whatever the other factors say); nothing below 0.50 is assigned |

### `crowding_adjustment` — trade (≤1): positioning and attention

| Anchor | Observable |
|---|---|
| 1.00 | uncovered/ignored — thin coverage, low chatter |
| 0.85 | known but not crowded |
| 0.70 | consensus long; price extended vs estimate revisions |
| 0.50 | mania markers — parabolic price on flat revisions; nothing below 0.50 is assigned |

Both adjustments are capped at 1: they can only *cut* confidence. Information already in the
price is, to that extent, not edge.

## Why multiplication (and what it costs)

The product implements **veto logic**: a thesis is only as strong as its weakest link — a binding
chokepoint with a bad vehicle (low purity) is not a trade, however good the node. In log space the
product is a sum, so no strong factor can compensate past a sufficiently weak one. The known cost:
`valuation_adjustment` and `crowding_adjustment` are often correlated (crowded names are usually
rich), so multiplication double-penalizes that pair. This is **intentional conservatism** — the
framework's asymmetry prefers a false watchlist (a delay) to a false admit — and is disclosed
rather than corrected.

## Sensitivity (report it, don't hide it)

Near a tier cut the product is most sensitive to its *smallest* factor. Because the scale is
discrete, marginality is defined on legal moves only: a card is *threshold-marginal* when **at
least one legal single-factor move to either adjacent published anchor** flips the derived tier.
For the derived `bottleneck_score` (a mean with no anchors of its own), a legal move is one
bottleneck dim shifted one adjacent-anchor step, then the mean recomputed. Say so in the
admission entry, and report the product **and** the minimum factor with every score. A
sensitivity computed this way is a **counterfactual**, not an alternative reading of the
evidence — deterministic assignment and sensitivity are separate statements. The
[synthetic walkthrough](../examples/synthetic_walkthrough/) lands at 0.2041 vs the 0.22 core cut
precisely to make this concrete: one step of valuation (0.70 → 0.85) gives 0.2478, across the
cut.

## Missing data and disagreement

- A factor that cannot be assessed from ≥ secondary/market-implied evidence gets **no number** —
  the candidate is watchlisted, never scored with a neutral default (0.5 is a claim, not an
  absence).
- Two-reader check (the audit protocol this rubric is built for): both readers score
  independently from the card and its evidence. **Any disagreement that changes the derived tier
  is unsettled — regardless of its numeric size — → watchlist** until a dated source settles it;
  when both readers land in the same tier, a factor differing by more than 0.1 is likewise
  unsettled. Disagreement is measured, not averaged away.

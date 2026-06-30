# Candidate Process — the admission funnel

How a candidate earns capital. Two stages: **objective gates** (mechanical, automatable) then
**subjective evaluation** (expensive-model judgment + a pre-registered admission). A candidate never
enters at the top tier — it starts as a small, capped satellite.

## Mandate boundary (define it by the chokepoint criterion, not a sector label)

A domain's mandate is the set of nodes in scope. Define it by a **physical-input criterion** — *does
this chokepoint gate or feed the target system?* — **not** by a sector label. This matters because it
forces a distinction between two different "purities":

- **chokepoint-purity** — supplier concentration, no substitute, capacity lead-time (how *binding* the
  constraint is);
- **theme-demand-purity** — how much of the vehicle's demand is the headline theme vs adjacent uses.

A genuine *input* chokepoint can be a **pure chokepoint but low-theme-beta** (its demand is mostly
adjacent). That is a **feature, not a disqualifier**: it diversifies the book and does not consume the
theme-beta cap. So **admit on chokepoint strength + a *real* vehicle** (revenue / signed offtake /
capacity), and **do not reject for low theme-demand-purity alone**. Symmetrically, **do not admit a
pre-revenue, hot-narrative name on chokepoint strength alone** (the cycle-peak / hype trap). The
boundary is a *hypothesis*: re-evaluating a rejected name under a corrected boundary is itself
pre-registered and auditable.

> *Worked example (the AI domain):* critical-material inputs (rare earth, tungsten) are **in scope** —
> they gate AI hardware upstream — even though their demand is mostly EV/wind/defense; a different
> *compute paradigm* that is not an input (e.g. quantum) is **out of scope** unless the mandate is
> explicitly expanded.

```
idea → tradeability → liquidity → node fit → bottleneck relevance → exposure purity
     → valuation/crowding → correlation/overlap → role → pre-registered admission → probation
```

## Stage 1 — objective gates (no LLM)

Mechanical, reproducible, cheap:

- **Tradeable** on the target broker/venue (active, tradeable, correct asset class).
- **Liquidity:** minimum price and minimum average dollar-volume over a recent window.
- A name that fails these is **watchlist-only** — it is not eligible capacity.

## Stage 2 — overlap penalty (does it ADD or DUPLICATE?)

Every other gate judges a candidate in isolation; this one judges it against the held book.

```
incremental_value = candidate_score × (1 − overlap_penalty)
overlap_penalty = max( same_node_as_existing_core, correlation_to_existing_core )
```

A great-but-redundant name must **replace** part of an existing position, not stack more of the
same bet. The overlap penalty understates economic overlap when the held cluster is a *different
layer of the same demand cycle* — the evaluator corrects for that qualitatively.

## Stage 3 — subjective evaluation (expensive model, finalists only)

Each finalist gets: a **bear case written before the recommendation**, an explicit answer to *"does
this improve the portfolio after overlap, purity, valuation, and crowding?"*, measurable exit
triggers, and a falsifiable decision (reject / watchlist / satellite-probation / replace / admit).
Reserve the scarce model here (see `TUNING.md` for the cheap-first-pass option).

## Stage 4 — policy / strategic-autonomy lens (evidence, not a factor)

If a policy tailwind is present, apply the **fact-vs-announcement** rule (`RESEARCH_RULES.md`). A
*signed, dated, material* award becomes a `policy:` evidence note + a `policy_reversal` exit trigger
on a name with a real chokepoint; a name whose thesis is *only* policy goes to a separate, capped
sleeve, admitted via the normal gates. **Policy never multiplies confidence and never creates a top
tier without chokepoint economics.**

## Stage 5 — pre-registered admission + probation

Admission is a **pre-registered QPOP entry** (`QPOP_PROTOCOL.md`) plus a map edit, reviewed by a
human. New names enter at a **capped satellite** weight, ramped in over a short **probation window**
at reduced size, so bad data / over-scored purity / liquidity issues surface before full size.

## Candidate states

```
idea → gated_pass / gated_fail
     → qpop_pending (gated finalist awaiting evaluation)
     → watchlist  |  rejected  |  probation (admitted, satellite)
     → active
```

Most candidates terminate at **watchlist** — admitting one or two meaningful changes per cycle is
the norm, and a "no action" cycle is a healthy outcome, not a failure.

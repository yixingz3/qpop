# Tuning — model allocation & budget discipline

The funnel uses **two model tiers from separate budget pools**: a cheap, abundant model for
high-volume work and an expensive, scarce model for judgment that matters. Tuning the split is how
you get the most research per unit of the scarce pool.

## The default split

| Stage | Model | Why |
|---|---|---|
| **SOURCE** | cheap (abundant pool) | high-volume, low-judgment candidate gathering — run wide |
| **GATE** | none (deterministic script) | tradeability / liquidity / overlap — free, reproducible |
| **EVALUATE** | expensive (scarce pool) | capital-at-risk judgment + bear case — reserve for finalists |

Per-run cost is roughly `sourcing_lenses` (cheap) + `finalists + 1` (expensive). The funnel exists
precisely so the expensive pool is spent only on names that already passed the deterministic gate.

## When the expensive pool is scarce: cheap-first-pass EVALUATE

If the expensive (e.g. Opus-tier) pool is depleted but the cheap (e.g. Sonnet-tier) pool has
headroom, run a **two-tier EVALUATE**:

1. **Cheap-model first-pass** over *all* finalists — fact-verify, write the bear case, reach a
   *provisional* decision. The model knob makes this one parameter (`evalModel: 'cheap'`).
2. **Expensive-model adjudication** over *only* the names the first pass flags as **admit /
   probation** — the capital-at-risk decisions.

**Why this is safe (the asymmetry):** a cheap-model *false-watchlist* merely delays a name and is
catchable on review; a cheap-model *false-admit* is caught by the expensive adjudication before any
capital moves. Over-admission — the failure mode you most want to prevent — still passes through the
expensive gate. You trade a little recall (a borderline admit might be missed) for a large saving of
the scarce pool, with the downside bounded by the adjudication step.

## What can be trusted to the cheap model (justified, not forced)

- **Yes:** sourcing; fact-gathering and verification; drafting the bear case; *watchlist / reject*
  verdicts with a clear bear case (cost of error ≈ 0, since no capital moves).
- **Adjudicate with the expensive model:** any **admit / probation / replace** decision; borderline
  cases; anything where the cheap model expresses low confidence.

Do not *force* work onto the cheap model where judgment quality drives a capital decision — the
saving is not worth a worse admission. The rule is: cheap model does the breadth and the drafts;
expensive model owns the "should we put capital here" call.

## Budget-aware fan-out

- Size the fan-out to the scarce pool's window. A one-off oversized run that exhausts the budget is
  a failure mode; drain a backlog over several smaller runs instead.
- Log what was *not* covered when a run is capped — silent truncation reads as "covered everything"
  when it did not.

## Probation (ramp-in)

New admissions ramp in at reduced size for a short window so bad data / over-scored purity /
liquidity issues surface before full size. Keep the *beta / concentration safety cap* tight during
probation; loosen the *weight factor* only enough to avoid an unrealistically idle book. Build
*per-entry* probation (each admission ramps on its own clock) rather than a single book-level ramp,
so post-launch admissions also get a buffer. Promote to full size on a *clean* window (no fired
trigger, no stale data, acceptable slippage, no severe relative underperformance).

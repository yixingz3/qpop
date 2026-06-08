# Worked example — AI supply chain

This is the **reference domain** that motivated the framework. It illustrates the *method*; it is
**not** a portfolio, a set of recommendations, or the live book. The live paper-trading
implementation (broker integration, the full bottleneck map, the actual QPOP ledger and positions)
is maintained **privately** — see `DISCLAIMER.md`.

## The chokepoints (illustrative)

The AI accelerator supply chain is a graph of physical bottlenecks. Representative nodes:

| Node | The binding physical constraint |
|---|---|
| HBM / high-bandwidth memory | few qualified makers, multi-year capacity lead time |
| Advanced packaging (CoWoS/SoIC) | interposer + chip-on-wafer capacity gates assembled accelerators |
| Leading-edge foundry | effectively one volume supplier at the frontier |
| EDA / litho / WFE | the tools that make the fabs (single-supplier EUV; EDA duopoly) |
| Power delivery (grid + board-level) | transformers/switchgear upstream; sub-1V point-of-load silicon at the die |
| Cooling / thermal | liquid cooling + CDUs as rack power density rises |
| Optical interconnect / connectivity | transceivers, retimers, and the PCIe/CXL signal-integrity fabric |
| Back-end test | tester machine-hours per AI part are far higher than for mobile SoCs |

Each node carries decomposed scores and measurable exit triggers, exactly as in
`../template_domain/bottleneck_map.template.yml`.

## What the example demonstrates (the methodological findings)

- **Discovery surfaces far more than it should admit.** Across runs, the funnel sourced and
  evaluated dozens of candidates and admitted a small single-digit fraction; most cycles are "no
  action." That restraint is the result.
- **The gate catches duplication mechanically** — candidates proposed into a node that already holds
  a position, or highly correlated to the held book, are flagged before any expensive evaluation.
- **The evaluation catches what the gate cannot** — economic-substitute and competitive-displacement
  relationships, structural-vs-cyclical traps (a name with the biggest recent move is often the
  worst chokepoint), and fact-vs-announcement on policy.
- **Policy enters as evidence, not a multiplier** — a signed, dated, material award becomes durability
  evidence + a reversal trigger on a real chokepoint; a name whose thesis is *only* policy goes to a
  separate, capped sleeve.

## A worked candidate flow (real numbers)

One discovery round, end to end (counts are from a real run; tickers are sanitized where a name is
a live holding, named where it is a *reject* — a reject is not a position):

```
~40 candidate cards   sourced across 12 lenses (per-node + gaps + social + policy + literature)
   ~10 NEW symbols    the rest deduped against the persistent "seen" set (already-decided names)
    ~6 pass the GATE   deterministic: foreign-OTC and sub-liquidity names rejected mechanically
    ~4 survive TRIAGE  cheap model drops the obvious low-purity (conglomerate / commodity / pre-rev)
     0 admitted        Sonnet bear-case + Opus adjudication on survivors -> watchlist/reject
```

Most rounds end at **0 admitted**. Across the build-out the funnel evaluated dozens of finalists and
admitted a **low single-digit fraction**, all at small satellite weight. "No action" is the modal
outcome, and it is the result, not a failure.

## One admitted, one rejected, one overlap-penalized

- **Admitted** (an earlier round): a critical-material permanent-magnet chokepoint — a genuinely
  supplier-concentrated, hard-to-substitute input. Admitted at **half** the unconstrained satellite
  weight, because a separate critical-inputs concentration cap bound it. *Restraint expressed as
  sizing, not just selection.* (Vehicle sanitized — it is a live holding.)
- **Rejected — an integrated energy major pitched for a "helium chokepoint":** the helium scarcity is
  real and the supply-share claim checks out, but helium is **< 1%** of a ~$330B oil major; the stock trades on crude, not
  helium economics. The chokepoint is real, the *ticker* captures none of it. Canonical
  rounding-error-in-a-conglomerate reject.
- **Overlap-penalized — a pure-play 800G optical-transceiver name:** high purity, real
  chokepoint, but the optics sleeve was already **full** (at its node cap, holding the incumbent
  it would duplicate). Routed to a **replace-not-stack** decision — a *future replacement candidate*
  gated on the incumbent firing an exit trigger, not a standalone add. The gate caught the
  duplication before any expensive evaluation.

## Ablation — each discipline contributes to restraint

The same **38-candidate batch**, run through baselines that each remove one discipline:

| Arm | Admitted | Rate |
|---|---|---|
| **Full pipeline** (gate + seen-set + triage + bear-case-first + overlap) | **0 / 38** | **0%** |
| − overlap penalty | 25 / 38 | 66% |
| − bear-case-first | 28 / 38 | 74% |
| **Ungated LLM screener** (no discipline) | **38 / 38** | **100%** |

An ungated LLM admits *literally everything*; removing any single discipline raises admission far
past a "beyond noise" threshold; the full stack drives 100% → 0%. Paired with the rejection-quality
audit (an independent reviewer judged the rejections **0.93 justified**, rising to **1.00** after a
capital-at-risk adjudication overturned the one flagged false-rejection), this is the evidence that
the restraint is *discipline*, not blanket conservatism. Full write-up: `../../docs/RESULTS_INITIAL.md`.

## Reproducing the method (not the positions)

Use `../template_domain/` to build your own map and run the funnel. The *engine and disciplines* are
the reusable artifact here; the live AI book's specific holdings and trades are intentionally not
published (it would read as "copy these trades," which this project explicitly is not).

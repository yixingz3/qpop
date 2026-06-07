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

## Reproducing the method (not the positions)

Use `../template_domain/` to build your own map and run the funnel. The *engine and disciplines* are
the reusable artifact here; the live AI book's specific holdings and trades are intentionally not
published (it would read as "copy these trades," which this project explicitly is not).

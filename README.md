# chokepoint-research-engine

**A pre-registered, agent-assisted research framework for thematic investment hypotheses —
designed to resist LLM confabulation, narrative drift, over-admission, and backtest overfitting.**

> **What this is not.** This is **not** a trading strategy, a stock-picker, or a claim to beat the
> market. It is a *methodology and reference framework* for using LLM agents to do disciplined,
> auditable, falsifiable thematic research. The headline result is the opposite of most
> "LLM-picks-stocks" demos: a well-disciplined agent **rejects most of the ideas it surfaces**, and
> that restraint is the contribution. See [`DISCLAIMER.md`](DISCLAIMER.md).

## The idea in one line

```
discover  →  gate  →  evaluate  →  pre-register  →  forward-validate  →  record posterior
(cheap LLM)  (deterministic)  (expensive LLM)   (QPOP ledger)   (paper trading)   (dataset)
```

Open-ended discovery is powerful but unreliable; LLMs hallucinate, chase narratives, and
over-admit. This framework wraps agentic discovery in **deterministic gates** and a
**pre-registration discipline** so that an idea can only move capital after it survives
falsifiable, dated-evidence checks — and is validated **forward** (on paper trading), not via a
fragile backtest.

## The six contributions

1. **A domain-agnostic bottleneck graph** — nodes are physical chokepoints, edges are dependencies.
   AI today; rare earth, power, gas, mining, uranium, defense-industrial tomorrow. A new domain is
   *a config file*, not a new codebase.
2. **A decomposed confidence model** — `confidence = bottleneck × purity × demand × valuation ×
   crowding`, with **policy as evidence, not a multiplicative factor** (see `docs/METHOD.md`). This
   kills "right theme → buy the ticker."
3. **A budget-aware LLM funnel** — cheap-model **sourcing** (wide, high-volume) → **deterministic
   gating** (tradeability/liquidity/overlap, no LLM) → expensive-model **evaluation** of finalists
   only, each with a **bear-case-written-before-the-recommendation**.
4. **Forward-QPOP** — pre-registered, content-hashed belief updates validated **forward** on paper
   trading + conservative shadow fills, *not backtested*. Pre-registration is the contract against
   HARKing and data-snooping for a young / structurally-shifting universe.
5. **A "no-stories" discipline stack** — source tiers, fact-vs-announcement, overlap penalty,
   structural-vs-cyclical, admission restraint. A position changes only on a *fired pre-registered
   trigger, a binding cap, or a risk limit* — never a narrative.
6. **Forward validation** — judged on conservative shadow fills against a benchmark, with the
   accumulated pre-registration ledger forming a reusable, auditable dataset.

## Why "no action" is the result

Across early runs in the AI-supply-chain example domain, the pipeline evaluated dozens of
LLM-surfaced candidates and admitted a small single-digit fraction; most weeks are "no action."
That low admission rate is **the empirical finding**, not a failure — it is what separates
disciplined agent-assisted research from naïve LLM screening, which over-admits by construction.

## Repository layout

```
chokepoint-research-engine/
  docs/        METHOD · RESEARCH_RULES · QPOP_PROTOCOL · CANDIDATE_PROCESS · SCOREBOARD · TUNING
               · WRITING_STANDARDS · SYNC · PAPER_OUTLINE
  src/         engine interfaces: qpop · scoring · discovery · gating · evaluation · validation
  examples/    ai_supply_chain/ (worked example) · template_domain/ (copy this to start a new domain)
  paper/       paper.tex + Makefile · references.bib (verified) · abstract · contributions
               · experiment_plan · related_work
  data/        synthetic/ (prices · candidate cards · QPOP ledger · scoreboard — non-sensitive samples)
  scripts/     check_sync_drift.sh + sync_manifest.tsv (keep this repo in sync with the private impl)
  tests/
  ETHICS.md · DISCLAIMER.md · LICENSE · CITATION.cff
```

## Adding a new domain (the flywheel)

1. Copy `examples/template_domain/` → `examples/<your_domain>/`.
2. Author `bottleneck_map.yml` (nodes = chokepoints, edges = dependencies, per-node scores +
   measurable exit triggers with a data source) and `benchmark_config.yml`.
3. Run the funnel; pre-register admissions in the QPOP ledger; forward-validate.
4. Each domain reuses the *same engine* — the value compounds as domains and forward records accrue.

## Status

**v0 — framework + worked example. No live track record is claimed.** The reference implementation
(a live paper-trading deployment) is maintained privately; this repository is the *method*, the
*schema*, and *reproducible templates*. A methods paper is in `paper/` (see `docs/PAPER_OUTLINE.md`).

## License & citation

[MIT](LICENSE). If you use this framework, please cite it — see [`CITATION.cff`](CITATION.cff).
**Not investment advice** — [`DISCLAIMER.md`](DISCLAIMER.md).

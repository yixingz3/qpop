# chokepoint-research-engine

**A pre-registered, auditable framework for making LLM-assisted research reliable and reproducible —
designed to resist confabulation, narrative drift, over-admission, and evaluation (look-ahead) leakage.
Validated on thematic capital-markets research as an adversarial testbed.**

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

## What the framework provides

These are the framework's *components*. The companion methods paper groups them into **four
contributions** (framework · protocol · forward-QPOP · evaluation-and-release) — see
`docs/PAPER_OUTLINE.md` and `paper/contributions.md`.

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
6. **Literature ingestion with verify-before-cite** — credible published research enters as a SOURCE
   lens (mechanism + priors) and as a methods literature-watch (related work + gap), but **no paper
   can move a score or enter `references.bib` until an adversarial, refute-by-default auditor
   confirms its identifier resolves to the claimed title and author** (see `docs/LITERATURE.md`).
   A *published, tradeable anomaly* is treated as already-priced crowding evidence, not a buy signal.
7. **Forward validation** — judged on conservative shadow fills against a benchmark, with the
   accumulated pre-registration ledger forming a reusable, auditable dataset.

## Why "no action" is the result

Across early runs in the AI-supply-chain example domain, the pipeline evaluated dozens of
LLM-surfaced candidates and admitted a small single-digit fraction; most weeks are "no action."
That low admission rate is **the empirical finding**, not a failure — it is what separates
disciplined agent-assisted research from naïve LLM screening, which over-admits by construction.

## Install

The methodology's pre-registration core is open-sourced as a small, dependency-free Python package,
**`forward-qpop`** — the tamper-evident, append-only QPOP ledger (register a hypothesis before the
evaluation window; every entry is content-hashed and chained, so tampering/insertion/reorder is
detectable):

```bash
pip install forward-qpop
forward-qpop verify data/synthetic/qpop_ledger_sample.jsonl
```

See [`src/forward_qpop/`](src/forward_qpop/) and its [README](src/forward_qpop/README.md). The rest of
the engine (sourcing / gating / evaluation) remains spec + reference pseudocode — see `src/README.md`.

## Repository layout

```
chokepoint-research-engine/
  docs/        METHOD · RESEARCH_RULES · QPOP_PROTOCOL · CANDIDATE_PROCESS · SCOREBOARD · TUNING
               · WRITING_STANDARDS · LITERATURE · RESULTS_INITIAL · PAPER_OUTLINE
  src/         forward_qpop/ — runnable QPOP pre-registration ledger (pip install forward-qpop)
               + prompts + deterministic-gate reference spec (qpop · scoring · discovery · gating
               · evaluation · validation contracts — see src/README.md)
  examples/    ai_supply_chain/ (worked example) · template_domain/ (copy this to start a new domain)
  paper/       paper.tex + Makefile · references.bib (verified) · abstract · contributions
               · experiment_plan · related_work
  data/        synthetic/ (prices · candidate cards · QPOP ledger · scoreboard — non-sensitive samples)
  tests/       test_ledger.py (forward_qpop)
  pyproject.toml · ETHICS.md · DISCLAIMER.md · LICENSE · CITATION.cff
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

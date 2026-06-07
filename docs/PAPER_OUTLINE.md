# Paper Outline

**Working title:** *Pre-Registered, Agent-Assisted Thematic Research: A Framework for Reducing
Narrative Drift and LLM Confabulation in Investment Hypothesis Generation*

**Short title:** *Pre-Registered Agentic Research for Thematic Investing*

**Framing (load-bearing):** a *methods / systems* paper, not an alpha paper. The contribution is the
discipline system; the headline empirical result is the **low, pre-registered admission rate**, not
a return claim.

## Sections

1. **Introduction** — LLMs make open-ended thematic research cheap but unreliable (confabulation,
   narrative drift, over-admission, backtest overfitting). We present a framework that wraps agentic
   discovery in deterministic gates + forward pre-registration, and report that a disciplined agent
   *rejects most of what it surfaces*.
2. **Related Work** — see `paper/related_work.md` (LLM finance agents; LLM failure modes;
   pre-registration; multi-agent verification; thematic/crowding factors; trustworthy AI in finance).
3. **Method** — the bottleneck graph; confidence decomposition; policy-as-evidence; the
   source→gate→evaluate funnel; forward-QPOP; the no-stories stack. (Mirrors `docs/METHOD.md`.)
4. **System** — the multi-agent implementation; model-tier allocation (cheap-source / deterministic-
   gate / expensive-evaluate; cheap-first-pass option); the auditable content-hashed ledger;
   reproducibility.
5. **Experiment design (pre-registered)** — see `paper/experiment_plan.md`. Pre-register the
   evaluation *before* collecting forward data: domains, horizon, metrics, and decision rules.
6. **Results** —
   - *Discipline results (available first):* candidate count, gate-pass rate, **admission rate**,
     no-action rate, source-tier distribution, overlap-penalty distribution, ledger integrity.
   - *Forward results (accrue over months):* benchmark-relative excess return, IR, active drawdown
     on conservative shadow fills — reported honestly with confidence intervals, not cherry-picked.
   - *Ablations:* remove the gate / the bear-case-first rule / the overlap penalty → admission rate
     rises (showing each discipline's contribution to restraint).
7. **Cross-domain portability** — the same engine on a second domain (e.g. rare-earth / power /
   uranium) as a config; report that the disciplines transfer.
8. **Limitations** — no live track record; survivorship in forward data; LLM nondeterminism; the
   admission-rate metric is necessary, not sufficient, for alpha.
9. **Conclusion** — disciplined agent-assisted research is reproducible and auditable; restraint is
   measurable; the framework + ledger are open for others to extend.

## Venues (in order)

1. arXiv / SSRN preprint (immediate; establishes priority + citability)
2. GitHub repo + **Zenodo DOI** (software citation)
3. **ACM ICAIF** (AI in finance — agents, trustworthy AI, asset management: strong fit)
4. A workshop version (agents / AI-in-finance)
5. Later: a full paper after 6–12 months of forward data

## Strongest single claim

> A pre-registered, gated agent pipeline admits a small single-digit fraction of the
> LLM-surfaced candidates it evaluates — and each admission is explainable and auditable — whereas
> an ungated LLM screener over-admits by construction. Restraint, not selection, is the result.

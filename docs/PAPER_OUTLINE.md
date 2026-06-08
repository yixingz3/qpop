# Paper Outline

**Working title:** *Forward-Registered LLM-Assisted Thematic Research: An Auditable Framework for
Investment Hypothesis Generation*

**Alternate (punchier):** *No-Stories Investing: Forward-Registered LLM Agents for Auditable
Thematic Research*

**Short title:** *Forward-Registered Agentic Research for Thematic Investing*

**The spine (one sentence, everything supports it):** *forward-pre-registered, auditable
LLM-assisted thematic research* — LLMs are useful for **sourcing** hypotheses but dangerous as
**decision engines**; the contribution is a workflow that forces LLM-generated ideas through
deterministic gates, dated evidence, bear-case-first review, and forward (not backtest) evaluation
before any capital-allocation claim.

**Framing (load-bearing):** a *methods / systems* paper, not an alpha paper. The headline empirical
result is the **low, pre-registered admission rate**, not a return claim. Do not let it become eight
papers — keep one dominant spine; supporting ideas (no-stories stack, budget-aware funnel,
uncertainty-about-the-constraint) are *support*, not pillars.

## Sections (target: 6–8 page methods draft first)

1. **Introduction** — LLMs make thematic research cheap but unreliable; existing financial agents
   over-focus on backtests and recommendations; the need is *auditable restraint, not better
   prompts*. We report that a disciplined agent *rejects most of what it surfaces*.
2. **Related Work** — see `paper/related_work.md`: financial LLMs / trading agents; LLM failure
   modes; structural-validity & leakage critiques of LLM trading agents (forward-vs-backtest);
   pre-registration / research integrity; agent verification / judge bias; thematic investing &
   crowding; responsible/auditable AI in finance.
3. **Framework** — the bottleneck graph; confidence decomposition; **policy-as-dated-evidence (not a
   multiplier)**; source tiers and deterministic gates. (Mirrors `docs/METHOD.md` §1–2.)
4. **Forward-QPOP Protocol** — content hash; append-only ledger; dated admission / belief-update /
   exit triggers; paper trading and conservative shadow fills. (Mirrors `docs/QPOP_PROTOCOL.md`.)
5. **System Implementation** — cheap-source → deterministic-gate → expensive-evaluate; bear case
   before recommendation; model-tier split (incl. cheap-first-pass / adjudication) and
   reproducibility. (Mirrors `docs/METHOD.md` §3.)
6. **Experiment Plan (pre-registered)** — see `paper/experiment_plan.md`: H1 admission restraint,
   H2 ablations, H3 portability, H4 descriptive forward performance — with the testable thresholds
   and the fixed implementation details (models, prompts, timestamps, price source, fill rule,
   costs, corporate actions, post-admission-news rule).
7. **Worked Example (AI supply chain)** — show **one admitted, one rejected, one
   overlap-penalized** idea end-to-end (e.g. an admitted critical-material chokepoint at half size,
   a "next-MU" commodity-cycle reject, an overlap-penalized duplicate of a held bet).
8. **Results / Forward Log** — *discipline metrics first* (candidate count, gate-pass rate,
   **admission rate < 10%**, no-action rate, **rejection precision** from the H5 audit, source-tier &
   overlap distributions, ledger integrity) — initial real-batch numbers in `docs/RESULTS_INITIAL.md`
   (rejection precision 0.93 on a 14-rejection sample, one reported false rejection); *ablations vs
   baselines* (ungated screener / debate-only / no-QPOP-lock / no-overlap → admission rate rises AND
   rejection precision falls); *forward performance only when enough time passes* (excess return, IR,
   active drawdown on shadow fills, with CIs + the structural-validity checklist).
9. **Discussion** — cross-domain portability (the same engine on a second domain as a config); and a
   **short conceptual case study: uncertainty-about-the-constraint** (the Bitcoin-halving example —
   a real but *scheduled, known-magnitude* constraint is arbitraged toward zero edge, unlike a
   physical chokepoint whose binding is discovered late). Framed as an *illustration of why forward,
   unanticipated evidence matters*, **not** as a contribution.
10. **Limitations** — small sample / wide intervals; no live-money claim; LLM version instability;
    admission rate is necessary, not sufficient, for alpha.
11. **Conclusion** — disciplined, forward-registered agent-assisted research is reproducible and
    auditable; restraint is measurable; the framework + ledger are open for others to extend.

## Venues (in order)

1. arXiv / SSRN preprint (immediate; establishes priority + citability) — a **6–8 page methods /
   workshop draft** first, with one worked AI-supply-chain example + one synthetic/template example
   + the pre-registered forward plan; the GitHub repo is part of the contribution.
2. GitHub repo + **Zenodo DOI** (software citation)
3. **ACM ICAIF** (AI in finance — agents, trustworthy AI, asset management: strong fit)
4. A workshop version (agents / AI-in-finance)
5. Later: a full empirical paper after 6–12 months of forward data

## Strongest single claim

> A forward-registered, gated agent pipeline admits **< 10%** of the LLM-surfaced candidates it
> evaluates — and each admission is explainable and auditable from the ledger alone — whereas an
> ungated LLM screener lacks an explicit mechanism for calibrated rejection. Restraint, not
> selection, is the result.

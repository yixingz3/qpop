# Abstract (draft)

Large language models are increasingly used as decision engines for open-ended research, but they
are unreliable in characteristic ways: they generate plausible but unsupported claims, amplify
narrative priors, over-admit candidates, and — when evaluated retrospectively — overfit data that
postdate their training. We study this as a problem of **AI reliability and auditability**, using
open-ended thematic investment research as a concrete, adversarial testbed. We present **a
forward-registered, agent-assisted research framework** that wraps LLM-driven discovery in
deterministic gates and a forward pre-registration protocol, so that a hypothesis can be admitted to
a forward-evaluation portfolio only after surviving falsifiable, dated-evidence checks and being
evaluated *forward* on paper trading rather than by a fragile backtest.

The framework contributes four components. (1) A **framework**: a domain-agnostic bottleneck graph
in which nodes are physical chokepoints and a new domain is a configuration file, not new code, with
a decomposed confidence model (bottleneck × purity × demand × valuation × crowding). (2) A
**protocol** for disciplined judgment: deterministic gates, source-tier rules, a bear case written
before any recommendation, overlap penalties, and government policy entered as *dated evidence and a
reversal trigger, never as a multiplicative factor* — together an explicit mechanism for *rejecting*
candidates, not merely surfacing them. (3) **Forward-QPOP**, a **hash-chained**, append-only
pre-registration ledger for hypothesis admission, belief updates, and exits — the contribution is
the *forward-locked hypothesis contract* (dated evidence + entry/update/exit triggers committed
before the evaluation window), not the tamper-evidence alone. (4) A pre-registered **evaluation and
open release** measuring admission restraint, *rejection quality*, discipline ablations against
ungated baselines, cross-domain portability, and descriptive forward outcomes.

Rather than a return claim, our central contribution is methodological: **this validates process
discipline, not investment profitability** (which awaits the forward window). We test whether a
disciplined, forward-registered agent **rejects most of the candidates it surfaces** *for defensible
reasons*. We report **pilot** discipline metrics from early candidate batches — a low admission rate
and a **held-out rejection-quality audit** (raw precision 0.93) — which *motivate* the pre-registered
forward evaluation, not confirm it; forward returns are not yet observed. Every admitted position
remains explainable and auditable from the ledger alone, whereas ungated LLM screeners lack an
explicit rejection mechanism. We release the framework, a worked AI-supply-chain example with a real
candidate flow, and a template for new domains.

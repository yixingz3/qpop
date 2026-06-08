# Abstract (draft)

Large language models make open-ended thematic investment research cheap, but unreliable: they can
generate plausible but unsupported claims, amplify narrative priors, recommend more candidates than
a disciplined investment process should admit, and — when evaluated by backtest — overfit periods
that postdate their training data. We present **a forward-registered, agent-assisted research
framework** that wraps LLM-driven discovery in deterministic gates and a forward pre-registration
protocol, so that a hypothesis can be admitted to a forward-evaluation portfolio only after
surviving falsifiable, dated-evidence checks and being evaluated *forward* on paper trading rather
than by a fragile backtest.

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

Rather than a return claim, our central contribution is methodological, and our claims are
pre-registered rather than asserted: we test whether a disciplined, forward-registered agent
**rejects most of the candidates it surfaces** *for defensible reasons*. We report initial discipline
metrics from real candidate batches — a low, pre-committed admission rate and an **independent
rejection-quality audit** (whether rejections were justified) — and pre-register the forward
evaluation rather than reporting forward returns we have not yet observed. Every admitted position
remains explainable and auditable from the ledger alone, whereas ungated LLM screeners lack an
explicit rejection mechanism. We release the framework, a worked AI-supply-chain example with a real
candidate flow, and a template for new domains.

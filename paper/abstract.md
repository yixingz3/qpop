# Abstract (draft)

Large language models make open-ended thematic investment research cheap, but unreliable: they can
generate plausible but unsupported claims, amplify narrative priors, recommend more candidates than
a disciplined investment process should admit, and — when evaluated by backtest — overfit periods
that postdate their training data. We present **a forward-registered, agent-assisted research
framework** that wraps LLM-driven discovery in deterministic gates and a forward pre-registration
protocol, so that a hypothesis can be admitted to a forward-evaluation portfolio only after
surviving falsifiable, dated-evidence checks and being validated *forward* on paper trading rather
than by a fragile backtest.

The framework contributes four components. (1) A **framework**: a domain-agnostic bottleneck graph
in which nodes are physical chokepoints and a new domain is a configuration file, not new code, with
a decomposed confidence model (bottleneck × purity × demand × valuation × crowding). (2) A
**protocol** for disciplined judgment: deterministic gates, source-tier rules, a bear case written
before any recommendation, overlap penalties, and government policy entered as *dated evidence and a
reversal trigger, never as a multiplicative factor* — together an explicit mechanism for calibrated
rejection. (3) **Forward-QPOP**, a content-hashed, append-only pre-registration ledger for
hypothesis admission, belief updates, and exits. (4) A pre-registered **evaluation and open
release** measuring admission restraint, discipline ablations, cross-domain portability, and
descriptive forward outcomes.

Our central empirical finding is methodological rather than a return claim: a disciplined,
forward-registered agent **rejects most of the candidates it surfaces**, with a low and
pre-committed admission rate, while every admitted position remains explainable and auditable from
the ledger alone — whereas ungated LLM screeners lack an explicit mechanism for calibrated
rejection. We release the framework, a worked AI-supply-chain example, and a template for new
domains, and pre-register a forward evaluation across one or more additional thematic domains.

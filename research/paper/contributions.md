# Contributions

The paper has **one spine**: *forward-pre-registered, auditable LLM-assisted thematic research.*
Everything below supports it. Four contributions (not eight — supporting ideas are folded in):

1. **Framework.** A **domain-agnostic bottleneck graph** plus a **decomposed confidence model**
   (`bottleneck × purity × demand × valuation × crowding`) for thematic investment hypotheses. A new
   domain is a configuration file, not new code.

2. **Protocol (discipline against narrative drift and over-admission).** Deterministic objective
   gates (tradeability, liquidity), **source-tier rules**, **bear-case-before-recommendation**
   evaluation, **overlap penalties** (replace, don't stack), and **policy-as-dated-evidence** (never a
   multiplier). Together these give the agent an explicit mechanism for *calibrated rejection*.

3. **Forward-QPOP.** A **content-hashed, append-only pre-registration ledger** for hypothesis
   admission, belief updates, and exits — validated **forward** on paper trading and conservative
   shadow fills, not by backtest (which is exposed to leakage and lookahead for a young universe).

4. **Evaluation and open release.** A **pre-registered experiment** measuring admission *restraint*,
   discipline *ablations*, cross-domain *portability*, and *descriptive* forward paper-trading
   outcomes — released with the framework, a worked AI-supply-chain example, a `template_domain`,
   synthetic fixtures, and the ledger schema, so others can fork, extend to new domains, and
   contribute forward logs (the GitHub repo is part of the contribution).

> **Deliberately *not* a contribution (kept as discussion / a short case study):** the
> *uncertainty-about-the-constraint* principle and the Bitcoin-halving example. It is a sharp idea —
> a chokepoint is an edge only while the constraint is unpriced; a synthetic, scheduled constraint
> gets arbitraged away — but it would split the paper's focus ("is this about LLM research discipline
> or about supply constraints?"). It belongs in the Discussion as a conceptual illustration of why
> *forward, unanticipated* evidence matters, not as a pillar.

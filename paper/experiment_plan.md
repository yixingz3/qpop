# Experiment Plan (pre-registered)

This plan is itself pre-registered: it commits the evaluation **before** the forward data is
collected, consistent with the framework's own discipline. Edit only by appending dated amendments.

## Hypotheses

- **H1 (restraint):** the gated, forward-registered pipeline admits a **low fraction** of the
  candidates it *evaluates* (and a lower fraction of those it *sources*). Pre-committed threshold:
  admission rate among evaluated finalists **< 10%** over the study window. (The prose "low" and the
  numeric threshold are deliberately the same single-digit target — no looser fallback.)
- **H2 (each discipline contributes):** ablating any one of {deterministic gate, bear-case-first,
  overlap penalty} **raises** the admission rate vs the full pipeline. *Supported for an ablation
  if* its admission rate exceeds the full pipeline's by **≥ 25% relative OR ≥ 5 percentage points,
  whichever is larger** (the max guards against a tiny relative jump on a tiny base, and against a
  large relative jump that is still trivial in absolute terms).
- **H3 (portability):** the disciplines transfer to a second domain with only `bottleneck_map.yml`
  changed. *Supported if* (a) the second domain's admission rate stays **within 2×** the first
  domain's rate, **and** (b) **≥ 70%** of the second domain's rejections map to the **same gate /
  rejection-category taxonomy** used in the first (tradeability, liquidity, low purity, overlap,
  valuation, crowding, unverifiable-trigger); **and** (c) the second-domain run uses the **same
  engine code and prompt templates**, with changes limited to `bottleneck_map.yml`, the
  domain-specific source lists, and the benchmark config — otherwise "portability" could be satisfied
  by quietly modifying the system. "Comparable" is thus defined on rate, the failure-mode taxonomy,
  and a no-source-change constraint, not asserted qualitatively.
- **H4 (forward, reported honestly):** over the forward window, benchmark-relative excess return and
  information ratio on conservative shadow fills are reported with confidence intervals. *No
  threshold is pre-set for H4 with a small sample* — it is descriptive, not a success gate.
- **H5 (rejection *quality*, not just quantity):** restraint is only evidence of discipline if the
  rejected ideas were actually bad. We therefore audit rejections: an independent reviewer (a held-out
  LLM auditor and/or a human), given only the *bull* case and the decision — **not** the engine's
  bear case — labels each sampled rejection JUSTIFIED or a FALSE REJECTION and assigns a category
  (low-purity / duplicate-overlap / valuation-or-crowding / commodity-cycle / pre-revenue-or-hype /
  unverifiable-or-untradeable). *Supported if* **rejection precision ≥ 0.80** (≥ 80% of sampled
  rejections judged justified) **and** the false-rejection rate is **≤ 10%**. This directly answers
  "a system can reject 95% of ideas by being arbitrarily conservative" — H1 measures *how much* is
  rejected, H5 measures *whether it should have been*.

## Design

- **Domains:** the AI-supply-chain worked example, then 1–2 additional bottleneck domains as configs.
- **Horizon:** ≥ 6 months of forward observation per domain before any performance claim; discipline
  metrics reported from the first runs.
- **Unit of analysis:** a candidate (sourced → gated → evaluated → admitted/not) and a position
  (admitted → forward outcome).
- **Primary metrics:** sourced/gated/evaluated/admitted counts; admission rate; no-action rate;
  source-tier distribution; overlap-penalty distribution; ledger-integrity (% admissions with a
  valid hash, chained to the prior entry, registered before the position); **rejection precision**
  and **false-rejection rate** from the H5 audit.
- **Secondary (forward):** excess return vs the theme benchmark; information ratio; active drawdown;
  gross/net thematic beta; turnover; shadow-fill slippage.
- **Ablations and baselines:** rerun the same candidate stream against (a) **ungated LLM screener**
  (no deterministic gate); (b) **debate-only** (bull/bear with no pre-registration lock); (c) **no
  Forward-QPOP lock** (same evaluation, hypotheses not content-hashed before the window); (d) **no
  overlap penalty**; and, where feasible, (e) a **human/manual thematic shortlist** for the same
  domain. Report each one's admission rate **and** its rejection precision — the point is to show the
  full pipeline admits *fewer* ideas *and* that its rejections are better justified, not merely that
  gates reduce count.

## Decision rules (pre-committed)

- H1 is **supported** if the evaluated-finalist admission rate is **< 10%** over the window.
- H2 is **supported** (per ablation) if that ablation's admission rate exceeds the full pipeline's by
  **≥ 25% relative or ≥ 5 percentage points, whichever is larger**.
- H3 is **supported** if the second-domain admission rate is **within 2×** the first-domain rate
  **and ≥ 70%** of its rejections map to the shared rejection-category taxonomy.
- H5 is **supported** if **rejection precision ≥ 0.80** and the **false-rejection rate ≤ 10%** on the
  audited sample.
- A position's outcome is recorded **Supported / Weakened / Falsified** strictly by its
  pre-registered exit triggers — never by an after-the-fact narrative. Because a thesis is judged
  against *several* triggers over time, outcome decisions use a **sequential test with explicit
  Type-I error control** (an e-value / anytime-valid formulation, after Huang et al. 2025 [POPPER]),
  so that monitoring many triggers across many positions does not inflate false "Falsified" calls —
  the multiple-comparisons analogue of the factor-zoo problem, controlled *prospectively*.

## Implementation details (fixed in advance, for reproducibility)

Recorded here so the forward log is reproducible and leakage-resistant; any change is a dated,
additive amendment.

- **Model versions & prompts:** the exact model identifier (and version/date) for each tier
  (SOURCE / first-pass EVALUATE / adjudication) is logged per run; prompt templates are committed in
  the repo and referenced by commit hash. A model-version change is an amendment, not a silent swap.
- **Source timestamps:** every evidence item carries the publication date of the source and the
  retrieval date; an admission may rely only on evidence dated **on or before** the admission date.
- **Price source:** a single declared price vendor (e.g. daily adjusted closes) with corporate
  actions (splits/dividends/spin-offs) applied via the vendor's adjusted series; the vendor is named
  in the run config.
- **Paper-trading timestamp & fill rule:** admissions take effect at the **next session's opening
  print** after the content hash is registered (never the same bar as the signal). Forward
  track-record metrics use a **conservative shadow fill** = opening print **+ assumed slippage
  (default 10 bps)**; broker paper fills validate automation only and are not the metric of record.
- **Transaction cost / slippage:** the 10 bps slippage assumption plus declared commission (default
  $0) are applied to every shadow fill; turnover is reported so costs are auditable.
- **Corporate actions:** handled via the adjusted price series; admissions/exits triggered by a
  corporate action (e.g. acquisition close) are logged as such, not as thesis outcomes.
- **Post-admission news:** the system **may** read post-admission news, but it may only *fire a
  pre-registered exit trigger or open a new dated belief-update entry* — it may **not** retroactively
  edit the original hypothesis or its triggers (the content hash makes such an edit detectable).

## Integrity controls

- Every admission carries a hash-chained QPOP entry (each entry binds the prior entry's hash)
  registered before the position — tampering with any past entry breaks the chain.
- The ledger is append-only; closed entries are immutable.
- No metric is changed after seeing results; amendments are dated and additive.
- Forward results are **evaluated** on conservative shadow fills, not optimistic fills.
- **Structural-validity reporting (after Ye et al. 2026, *The Alpha Illusion*):** any forward
  performance number is reported only alongside its structural-validity checklist — temporal
  integrity (admission strictly precedes the evaluation bar), frictions (slippage + costs applied),
  robustness (across the accumulated ledger, not a cherry-picked window), calibration (admitted
  confidence vs realized outcome), and execution (shadow-fill rule). A return without this checklist
  is not reported as evidence.

## Threats to validity (declared in advance)

Small sample / wide intervals early; LLM nondeterminism across model versions; survivorship in
which domains get built; the admission-rate metric is *necessary but not sufficient* for alpha. The
paper reports these rather than hiding them.

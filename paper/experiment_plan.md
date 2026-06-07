# Experiment Plan (pre-registered)

This plan is itself pre-registered: it commits the evaluation **before** the forward data is
collected, consistent with the framework's own discipline. Edit only by appending dated amendments.

## Hypotheses

- **H1 (restraint):** the gated, pre-registered pipeline admits a **low single-digit %** of the
  candidates it *evaluates* (and a lower % of those it *sources*). Pre-committed threshold: admission
  rate among evaluated finalists **< 15%** over the study window.
- **H2 (each discipline contributes):** ablating any one of {deterministic gate, bear-case-first,
  overlap penalty} **raises** the admission rate vs the full pipeline.
- **H3 (portability):** the disciplines transfer to a second domain — the admission rate and the
  qualitative failure-modes caught are comparable, with only the `bottleneck_map.yml` changed.
- **H4 (forward, reported honestly):** over the forward window, benchmark-relative excess return and
  information ratio on conservative shadow fills are reported with confidence intervals. *No
  threshold is pre-set for H4 with a small sample* — it is descriptive, not a success gate.

## Design

- **Domains:** the AI-supply-chain worked example, then 1–2 additional bottleneck domains as configs.
- **Horizon:** ≥ 6 months of forward observation per domain before any performance claim; discipline
  metrics reported from the first runs.
- **Unit of analysis:** a candidate (sourced → gated → evaluated → admitted/not) and a position
  (admitted → forward outcome).
- **Primary metrics:** sourced/gated/evaluated/admitted counts; admission rate; no-action rate;
  source-tier distribution; overlap-penalty distribution; ledger-integrity (% admissions with a
  valid content hash registered before the position).
- **Secondary (forward):** excess return vs the theme benchmark; information ratio; active drawdown;
  gross/net thematic beta; turnover; shadow-fill slippage.
- **Ablations:** rerun the same candidate stream with (a) gate off, (b) bear-case-first off,
  (c) overlap penalty off; compare admission rates.

## Decision rules (pre-committed)

- H1 is **supported** if the evaluated-finalist admission rate is < 15% over the window.
- H2 is **supported** if each ablation's admission rate exceeds the full pipeline's by a margin
  beyond noise.
- A position's outcome is recorded **Supported / Weakened / Falsified** strictly by its
  pre-registered exit triggers — never by an after-the-fact narrative.

## Integrity controls

- Every admission carries a content-hashed QPOP entry registered before the position.
- The ledger is append-only; closed entries are immutable.
- No metric is changed after seeing results; amendments are dated and additive.
- Forward results are validated on conservative shadow fills, not optimistic fills.

## Threats to validity (declared in advance)

Small sample / wide intervals early; LLM nondeterminism across model versions; survivorship in
which domains get built; the admission-rate metric is *necessary but not sufficient* for alpha. The
paper reports these rather than hiding them.

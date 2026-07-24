# Working results for v2 (post-submission; sanitized aggregates)

Dated evidence gathered after the SSRN submission (2026-06-29), for the v2 revision. Aggregates
only — per-card records, symbols, and the held book stay in the private research repo per the
release boundary (paper §Reproducibility). All runs 2026-07-07 unless noted.

## Ablation (H2) — the two pending arms, run on the SAME preserved 38-candidate batch

The pilot's 38-card batch, per-arm decisions, and literal arm prompts were recovered in full from
the run journals and are now preserved as named artifacts (prompts released in `src/prompts.md` §8).
The two §9.5-pending arms were then run on the identical batch under the pilot protocol (batched
mid-tier model call; admit boolean + one-line each), with two independent replicates per arm and an
explicit as-of framing (dated amendment: retrospective run).

| Arm | Admission rate | Replicates | Per-card replicate agreement |
|---|---|---|---|
| Full pipeline (pilot, real funnel) | 0/38 (0%) | 1 | — |
| − overlap penalty (pilot) | 25/38 (66%) | 1 | — |
| − bear-case-first (pilot) | 28/38 (74%) | 1 | — |
| Ungated screener (pilot) | 38/38 (100%) | 1 | — |
| **Debate-only (new, arm b)** | **15/38, 13/38 (~37%)** | 2 | 89% |
| **No forward lock (new, arm c)** | **14/38, 17/38 (~41%)** | 2 | 82% |

Both new arms clear H2's pre-committed support threshold (≥25% relative or ≥5pp above the full
pipeline) by +37/+41pp. Two observations for v2:

1. **Monotone discipline ordering, with the new arms in between:** 100% → 74% → 66% → ~41% → ~37% →
   0%. The most disciplined single-pass prompt (bear-case-first + purity + overlap intact, only the
   forward lock removed) still admits ~4-in-10 — the residual gap to 0% belongs to the funnel's
   *structure* (deterministic gate, cheap-triage escalation asymmetry, capital-at-risk adjudication,
   and the falsifiable-contract requirement as practiced), not to prompt wording.
2. **The arms' consensus-admit core closely tracks the production funnel's WATCHLIST tier** (one
   consensus name later earned a pre-registered flip contract). Prompt-level discipline finds the
   same candidates; the staged funnel converts "interesting" into "watch with a dated trigger"
   rather than "commit capital now."

## Rejection-quality audit (H5) — expanded from n=14 to n=40, documented sampling

The pilot's 14-sample membership was never enumerated and its sampling method was never recorded;
the expansion therefore **supersedes** it with a fully documented draw: population = all 48
non-admitted candidates of the batch-era rounds (mechanical bull-only extraction, bear-case
exclusion enforced by test), sample n=40, fixed seed, round-stratified, content-hash-verifiable
manifest. Protocol: five fresh runs of a held-out bull-only auditor (8 records each; fresh contexts
within one model family, not statistically independent instances), every
FALSE_REJECTION flag escalated to an expensive-model capital-at-risk adjudication with the full
record (no-web retrospective — a dated deviation from the pilot's contemporaneous adjudication, to
avoid look-ahead).

*(Terminology revised 2026-07-23 per the v2 review — reported as model disagreement under
asymmetric information, not ground truth; "raw precision"/"adjudicated precision" renamed.)*

| Metric | Pilot (n=14, undocumented) | Expanded (n=40, seeded) |
|---|---|---|
| Bull-only auditor agreement (primary) | 0.929 (13/14); interval non-inferential (sample undocumented) | **0.775 (31/40), naive Wilson [0.625, 0.877]** |
| Bull-only flag / disagreement rate | 7.1% (1/14) | **22.5% (9/40)** |
| Full-record LLM uphold among flagged (secondary) | 1/1 | **9/9** |

**The honest v2 statement:** BOTH pre-committed H5 clauses fail on the documented sample (≥0.80
agreement: 0.775; ≤10% flag rate: 22.5% — on a single binary-labeled sample the clauses are
redundant, flag rate = 1 − agreement, effectively binding at 0.90). The pilot's 0.93 was the
optimistic read of a small
sample (the expanded point estimate lies inside the pilot's own interval, so nothing is
contradicted, but the n=14 headline did not survive a 2.86× larger documented sample; the flag
count rose 9×, from one to nine). The full-record adjudicator overriding all nine bull-only flags is
an escalation diagnostic, not independent validation: auditor and adjudicator are related models
judging under deliberately asymmetric information, so a full-record model overriding bull-only
flags is expected and does not establish the rejections were correct. Flags split evenly across the
funnel's cheap-drop and full-eval
stages (5/4 against a 20/20 sample), so the disagreement rate is not a sample-composition artifact.
Rejection quality remains **unresolved** pending the human lane — redesigned per review: two human
reviewers, neutral dated full-record packet, blind to LLM labels and pipeline decisions, source
verification allowed, third-reviewer tie rule, inter-rater agreement reported (supersedes the
earlier bull-only packet).

## Portability H3 clause (c) — config-only domain swap DEMONSTRATED (2026-07-07)

v1 honestly reported clause (c) as not met (prompt templates embedded the first domain's framing).
After the `domain` profile was threaded through the templates (byte-identical golden tests on the
live config), a full funnel run on the **uranium fuel cycle** — a domain v1's Discussion names as a
candidate — required **one new configuration file and zero prompt-construction code changes**
(verified: the change set is added-files-only; no generated prompt contains any first-domain string).

Funnel (live run): 20 cards sourced across 5 lenses → 10 unique symbols → deterministic gate 8 pass
/ 2 mechanical rejections (one foreign-OTC sub-liquidity, one min-price) → cheap triage 4 pursue /
3 drop (commodity-priced, two pre-revenue) → bear-case-first evaluation: 1 admit-class flag,
2 watchlist, 1 reject → expensive adjudication **upheld the single flag at probationary half-size**
with five dated exit triggers (a recorded disposition — the demo book is unfunded).

What transferred: the full rejection-category taxonomy, unprompted (no-domestic-vehicle,
low-purity-conglomerate, pre-revenue-hype, commodity-cycle, valuation/crowding); source-tier and
citation-verification discipline (the social lens held all its cards at tertiary-idea-seed; the
literature lens DOI-verified and downgraded a conflicted paper); and the escalation asymmetry in
BOTH directions — the mid tier corrected a cheap-tier purity misread (facility uniqueness ≠ ticker
exposure), and the expensive tier overturned two factual errors in the mid tier's bear case (an
inverted crowding read; an overstated single-customer claim) while still capping size. The one
upheld disposition is a de-rated sole-domestic-capacity chokepoint with a signed primary-source
contract — the forced-cheap-entry principle firing outside the first domain, and the funnel's first
admit-class outcome in any second-domain probe (restraint is not blanket conservatism).

## v2 to-do this enables

- §9.3: extend the ablation table (+ replicate agreement); correct the "all arm prompts are
  released" sentence to reference `src/prompts.md` §8 (true as of 2026-07-07).
- §9.2: report the n=40 documented-sample numbers as primary with the pilot alongside; add the
  sampling-method paragraph; state plainly that the raw gate was not met and why the two-layer
  audit is the metric that scales.
- Reproducibility: the ablation's cards/decisions/prompts are now preserved artifacts — the claim
  becomes fully true.

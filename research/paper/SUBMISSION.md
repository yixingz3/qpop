# Submission state

*Forward-Registered, Auditable LLM-Assisted Research: A Reliability Methodology, with a
Capital-Markets Testbed* — Yixing Zheng (NYU Stern). Source: [`paper.tex`](paper.tex) (28 pp).

| Venue | Status | Date | Notes |
|---|---|---|---|
| SSRN | **Submitted** | 2026-06-29 | Pre-submission verification 2026-06-28 (all funnel numbers ledger-reconciled). eJournals: CSRN (AI Alert, Computing Methodology Alert), FEN (Asset Pricing & Valuation, Market Efficiency), ERN (Econometrics: Computational Techniques). JEL: C45, C12, C53, C81, C88, G11, G17. Abstract ID / URL: *pending — fill in when SSRN posts.* |
| arXiv | Planned | — | cs.AI primary, q-fin.CP cross-list. Blocked on endorsement. Pre-upload: copy the source (do not edit the SSRN-submitted tex in place), scrub the line-1 `% … SSRN submission draft` comment, upload `.tex` + `references.bib` (figures are inline TikZ — no ancillary files). |

## Version log

| Version | Date | What |
|---|---|---|
| v0.1 | 2026-06-29 | SSRN submission draft (built 2026-06-29; `paper.log`: 28 pages) |

## Planned v2 (target ~2026-12)

Scheduled by the paper's own declared-pending list (§9.5 + Limitations): H4 forward read-out with the
structural-validity checklist; forward-scoring-registry first cohort; ~~remaining ablation arms
(debate-only, no-forward-lock)~~ **DONE 2026-07-07** (both support H2; see
[../docs/RESULTS_V2_WORKING.md](../docs/RESULTS_V2_WORKING.md)); ~~expanded rejection-quality audit
(n≥40)~~ **DONE 2026-07-07** (raw 0.775 [0.625, 0.877], adjudicated 9/9 upheld; human lane packet
prepared, pending operator); ~~`{domain}` prompt parameterization → config-only portability demo~~ **DONE 2026-07-07** (mechanism + a full uranium-fuel-cycle funnel run from one new config file, zero code edits — H3 clause (c) demonstrated; see [../docs/RESULTS_V2_WORKING.md](../docs/RESULTS_V2_WORKING.md));
~~external timestamp anchor~~ **DONE 2026-07-08** (OpenTimestamps anchor external / verify-external + sidecar receipt); **e-value sequential test DONE 2026-07-08** (anytime-valid Type-I control, 18 tests, methods note); aggregates regenerated from the run ledger (not by hand). Pilot ablation
artifacts (38-card batch, per-arm decisions, literal prompts) recovered and preserved 2026-07-07;
arm prompts released in `src/prompts.md` §8.

# Submission state

*Forward-Registered, Auditable LLM-Assisted Research: A Reliability Methodology, with a
Capital-Markets Testbed* — Yixing Zheng (NYU Stern). Source: [`paper.tex`](paper.tex) (28 pp).

| Venue | Status | Date | Notes |
|---|---|---|---|
| SSRN | **Submitted** | 2026-06-29 | Pre-submission verification 2026-06-28 (all funnel numbers ledger-reconciled). eJournals: CSRN (AI Alert, Computing Methodology Alert), FEN (Asset Pricing & Valuation, Market Efficiency), ERN (Econometrics: Computational Techniques). JEL: C45, C12, C53, C81, C88, G11, G17. Abstract ID / URL: *pending — fill in when SSRN posts.* |
| arXiv | Ready — needs endorser | — | cs.AI primary, q-fin.CP cross-list. **Source copy prepared (WI-21):** [`arxiv/paper.tex`](arxiv/paper.tex) + `references.bib` (+ `paper.bbl` fallback), line-1 `% … SSRN submission draft` comment scrubbed on the copy only (original tex untouched; diff = 1 line), builds clean (pdflatex+bibtex+pdflatex×2 → 28 pp, 0 undefined citations). Upload `.tex` + `references.bib` (figures are inline TikZ — no ancillary files). **Endorser prep (WI-20c):** [`../docs/ARXIV_ENDORSER_PREP.md`](../docs/ARXIV_ENDORSER_PREP.md) — verified cs.AI endorser shortlist + outreach template. Remaining blocker: operator obtains one manual (Path-2) endorsement, then upload. |

## Version log

| Version | Date | What |
|---|---|---|
| v0.1 | 2026-06-29 | SSRN submission draft (built 2026-06-29; `paper.log`: 28 pages) |
| v2 (draft) | 2026-07-09 | v2 revision drafted on branch `paper-v2` (executes the 2026-07-08 round-3 review §5 edit map). **Headline reversal:** H5 raw auditor precision is now **0.775 (31/40), Wilson [0.625, 0.877]** on a documented, seeded `n=40` sample — the pre-committed **≥0.80 raw gate is NOT met** (adjudicated precision 1.00, 9/9 flags upheld); reported as a result, per the paper's own no-stories discipline. Also folded in: both remaining ablation arms (debate-only ~37% / no-forward-lock ~41%; replicate agreement 89% / 82%; monotone ladder 100→74→66→~41→~37→0%), config-only uranium portability (H3 clause (c) → demonstrated), the e-value module (now ledger-integrated — frozen per-admission commitment + `forward-qpop evalue` CLI, 18 module + 17 integration tests) and the external OpenTimestamps anchor (opt-in / manual by design), neither used in the pilot, a refreshed ledger-derived funnel aggregate (9 rounds / 318 cards / 110 gate-pass / 0 admits, window 2026-06-08→2026-07-06), and a softened release-boundary table (gate + scoring engine is private). Not yet built as a public version — pending operator review. |

## v2 release plan (2026-07-09)

Sequencing decided for the `paper-v2` draft, after operator review:

- **SSRN UPDATE first.** v1 is still a `PRELIMINARY_UPLOAD` — SSRN has not yet processed or posted it
  (no Abstract ID assigned), so the v2 replacement will become the *first public version*. Update the
  SSRN submission with the v2 `paper.tex` as soon as the operator signs off; there is no live public v1
  to supersede, only a preliminary upload to replace. The H5 headline reversal is the integrity clock —
  ship the SSRN revision rather than sit on a known gate-failure until the December H4 window.
- **arXiv on endorsement.** Upload the v2 `.tex` + `references.bib` (via `arxiv/`, line-1 comment
  scrubbed) the moment the operator obtains one cs.AI endorsement. Endorser prep is done
  ([`../docs/ARXIV_ENDORSER_PREP.md`](../docs/ARXIV_ENDORSER_PREP.md) — verified shortlist + outreach
  template); the endorsement request itself is the only remaining external blocker, and the v2 draft is
  the artifact the request can point at.
- **December (v2.1 / SSRN rev 2)** then carries only the H4 forward read-out + the forward-scoring
  registry first cohort (+ the human-audit lane if that packet is filled by then).

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

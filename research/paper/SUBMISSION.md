# Submission state

*Forward-Registered, Auditable LLM-Assisted Research: A Reliability Methodology, with a
Capital-Markets Testbed* — Yixing Zheng (NYU Stern). Source: [`paper.tex`](paper.tex) (v2 revision,
33 pp on branch `paper-v2`; the posted SSRN v1 and the `arxiv/` copy are the 28 pp v0.1 build).

| Venue | Status | Date | Notes |
|---|---|---|---|
| SSRN | **Posted (public preprint)** | accepted 2026-07-22 (submitted 2026-06-29) | v1 is now publicly posted and receiving views/downloads (27 views / 15 downloads day one). It is a preprint, not a peer-reviewed publication. **Abstract ID 7017500 — <https://ssrn.com/abstract=7017500>** (operator-supplied 2026-07-23). Pre-submission verification 2026-06-28 (all funnel numbers ledger-reconciled). eJournals: CSRN (AI Alert, Computing Methodology Alert), FEN (Asset Pricing & Valuation, Market Efficiency), ERN (Econometrics: Computational Techniques). JEL: C45, C12, C53, C81, C88, G11, G17. |
| arXiv | Manuscript revision + endorsement pending | — | cs.AI primary, q-fin.CP cross-list. **The `arxiv/` bundle is still the v1 source — do NOT upload it; it must be re-synced from the canonical v2 after the SSRN revision lands (arXiv deferred by operator decision, 2026-07-24).** **Source copy prepared (WI-21):** [`arxiv/paper.tex`](arxiv/paper.tex) + `references.bib` (+ `paper.bbl` fallback), line-1 `% … SSRN submission draft` comment scrubbed on the copy only (original tex untouched; diff = 1 line), builds clean (pdflatex+bibtex+pdflatex×2 → 28 pp, 0 undefined citations). Upload `.tex` + `references.bib` (figures are inline TikZ — no ancillary files). **Endorser prep (WI-20c):** [`../docs/ARXIV_ENDORSER_PREP.md`](../docs/ARXIV_ENDORSER_PREP.md) — verified cs.AI endorser shortlist + outreach template. Remaining blocker: operator obtains one manual (Path-2) endorsement, then upload. |

## Version log

| Version | Date | What |
|---|---|---|
| v0.1 | 2026-06-29 | SSRN submission draft (built 2026-06-29; `paper.log`: 28 pages) |
| v2 (rev. 2) | 2026-07-23 | Review-driven revision on `paper-v2` (33 pp; `main` merged in — the branch previously lacked the e-value integration it cited). Executes Blocks 1–3 of the additive review log (`revise_log.md` — kept **private by operator decision, 2026-07-23**: a local working file, never committed to this public repo; preserved in the private research project): H5 reported as **model disagreement under asymmetric information** (bull-only agreement 31/40 = 0.775, flag rate 9/40 = 22.5%, **both** gate clauses fail; full-record uphold 9/9 is an escalation diagnostic, not ground truth; pilot cell corrected to 1/1); H2 → **inconclusive / not tested as registered** (exploratory system contrasts; monotone/saturation causality removed; no-lock arm renamed no-falsifiable-contract); H3 → **not supported as registered** (clauses read on different domains; uranium 1/4 stated; portability table added); rOAR/rOMR defined with fixed denominator; e-value guarantee narrowed to per-hypothesis with verified citations (Ramdas et al. 2023, Shafer 2021, Vovk–Wang 2021); evidence-status table added; reproducibility narrowed to mechanics-verification; Appendix A demoted to a hypothesis-generating case note (figure + exact percentages removed); funnel aggregate frozen at commit `1744608` (sha256 `bb0a9507…`); Table 5 clipping fixed; date → July 2026. Pending operator + reviewer verification (Block 4). |
| v2 (draft) — SUPERSEDED by v2 (rev. 2); wording below is pre-correction history | 2026-07-09 | v2 revision drafted on branch `paper-v2` (executes the 2026-07-08 round-3 review §5 edit map). **Headline reversal:** H5 raw auditor precision is now **0.775 (31/40), Wilson [0.625, 0.877]** on a documented, seeded `n=40` sample — the pre-committed **≥0.80 raw gate is NOT met** (adjudicated precision 1.00, 9/9 flags upheld); reported as a result, per the paper's own no-stories discipline. Also folded in: both remaining ablation arms (debate-only ~37% / no-forward-lock ~41%; replicate agreement 89% / 82%; monotone ladder 100→74→66→~41→~37→0%), config-only uranium portability (H3 clause (c) → demonstrated), the e-value module (now ledger-integrated — frozen per-admission commitment + `forward-qpop evalue` CLI, 18 module + 17 integration tests) and the external OpenTimestamps anchor (opt-in / manual by design), neither used in the pilot, a refreshed ledger-derived funnel aggregate (9 rounds / 318 cards / 110 gate-pass / 0 admits, window 2026-06-08→2026-07-06), and a softened release-boundary table (gate + scoring engine is private). Not yet built as a public version — pending operator review. |

## v2 release plan (2026-07-09; premise corrected 2026-07-23)

Sequencing decided for the `paper-v2` draft, after operator review:

- ~~**SSRN UPDATE first.** v1 is still a `PRELIMINARY_UPLOAD` — SSRN has not yet processed or posted it
  (no Abstract ID assigned), so the v2 replacement will become the *first public version*. Update the
  SSRN submission with the v2 `paper.tex` as soon as the operator signs off; there is no live public v1
  to supersede, only a preliminary upload to replace.~~ **PREMISE FALSIFIED 2026-07-22: SSRN accepted
  and posted v1**, so the superseded 0.93 (n=14) headline is now publicly circulating and v2 is a
  *revision of a live public preprint*, not a first public version — which makes the revision MORE
  urgent, not less. The H5 headline reversal is the integrity clock —
  ship the SSRN revision rather than sit on a known gate-failure until the December H4 window.
- **arXiv on endorsement.** Upload the v2 `.tex` + `references.bib` (via `arxiv/`, line-1 comment
  scrubbed) the moment the operator obtains one cs.AI endorsement. Endorser prep is done
  ([`../docs/ARXIV_ENDORSER_PREP.md`](../docs/ARXIV_ENDORSER_PREP.md) — verified shortlist + outreach
  template); the endorsement request itself is the only remaining external blocker, and the v2 draft is
  the artifact the request can point at.
- **December (v2.1 / SSRN rev 2)** then carries only the H4 forward read-out + the forward-scoring
  registry first cohort (+ the human-audit lane if that packet is filled by then).

## Current release step (2026-07-24)

The canonical v2 (branch `paper-v2`) is in the review loop for an **SSRN replacement of the posted
v1** — reviewer verification of the latest correction block is the gate. **arXiv is deferred by
operator decision (2026-07-24)** and is not part of this release step; the `arxiv/` bundle stays
untouched (and must not be uploaded) until separately requested. December (v2.1) scope: H4 forward
read-out + forward-scoring-registry first cohort + the human-audit lane.

## Planned v2 (target ~2026-12) — HISTORICAL (superseded)

> **HISTORICAL RECORD — superseded 2026-07-23/24.** Kept as dated history, not current
> instructions; several claims below use terminology the v2 revision has since corrected ("both
> support H2" → H2 is inconclusive/not tested as registered; "adjudicated 9/9 upheld" → a
> same-system escalation diagnostic, not ground truth; "anytime-valid Type-I control" → an
> experimental implementation that does not yet deliver the guarantee). See the v2 (rev. 2)
> version-log row and current collateral for the corrected framing.

Scheduled by the paper's own declared-pending list (§9.5 + Limitations): H4 forward read-out with the
structural-validity checklist; forward-scoring-registry first cohort; ~~remaining ablation arms
(debate-only, no-forward-lock)~~ **DONE 2026-07-07** (both support H2; see
[../docs/RESULTS_V2_WORKING.md](../docs/RESULTS_V2_WORKING.md)); ~~expanded rejection-quality audit
(n≥40)~~ **DONE 2026-07-07** (raw 0.775 [0.625, 0.877], adjudicated 9/9 upheld; human lane packet
prepared, pending operator); ~~`{domain}` prompt parameterization → config-only portability demo~~ **DONE 2026-07-07** (mechanism + a full uranium-fuel-cycle funnel run from one new config file, zero code edits — H3 clause (c) demonstrated; see [../docs/RESULTS_V2_WORKING.md](../docs/RESULTS_V2_WORKING.md));
~~external timestamp anchor~~ **DONE 2026-07-08** (OpenTimestamps anchor external / verify-external + sidecar receipt); **e-value sequential test DONE 2026-07-08** (anytime-valid Type-I control, 18 tests, methods note); aggregates regenerated from the run ledger (not by hand). Pilot ablation
artifacts (38-card batch, per-arm decisions, literal prompts) recovered and preserved 2026-07-07;
arm prompts released in `src/prompts.md` §8.

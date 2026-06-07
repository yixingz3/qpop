# Writing & Submission Standards

Standards for taking this work from notes to a submittable paper. The goal is a real, accepted
contribution — so language, citations, figures, reproducibility, and ethics all have to clear the bar.

## Language

- **No overclaiming — ever.** This is a *methods* paper. Do not claim alpha or that the system "beats
  the market." The defensible claim is the **low, pre-registered admission rate** and auditability.
  Every quantitative claim states its sample size and uncertainty.
- Precise, active voice. Define every term on first use (chokepoint, exposure purity, forward-QPOP).
  Prefer the shortest sentence that is still exact.
- State limitations plainly (no live track record yet; small early sample; LLM nondeterminism). A
  paper that names its own weaknesses is stronger, not weaker.
- Consistent terminology and notation throughout (use the symbols defined in `METHOD.md`).

## Citations (academic integrity — non-negotiable)

- **Every factual or prior-work claim carries a citation.** No claim rests on memory.
- **Verify every reference** against the primary source (arXiv abstract page, journal DOI). `references.bib`
  is the canonical list; it was verified 2026-06-07 and must be **re-verified at camera-ready**.
- **Never fabricate or pass through an unverified citation.** (The first draft contained one
  fabricated and one wrong-author entry, caught by verification — exactly the failure the framework
  is about.) When in doubt, remove it.
- Quote sparingly and attribute; paraphrase with citation. Check the venue's plagiarism/self-plagiarism
  and dual-submission policies before submitting.

## Figures & visual

- Each figure makes **one** point; the caption is self-contained (a reader gets it without the body).
- Vector formats (PDF/SVG) for diagrams; legible at print size; **colorblind-safe** palettes; no
  chartjunk. Label axes with units. Do not truncate axes to exaggerate.
- Planned figures: (1) the source→gate→evaluate funnel; (2) the candidate state machine; (3) the
  admission-rate / no-action distribution; (4) source-tier and overlap-penalty distributions;
  (5) the ablation (admission rate rises as each discipline is removed). Keep figure source in the repo.

## Structure & reproducibility

- Follow the standard arc (Intro · Related Work · Method · System · Pre-registered Experiment Design ·
  Results · Limitations · Ethics · Conclusion) — see `PAPER_OUTLINE.md`.
- The experiment design is **pre-registered** (`paper/experiment_plan.md`): metrics and decision
  rules committed before the forward data is read. Do not change a metric after seeing results;
  amendments are dated and additive.
- Ship a reproducibility appendix: model versions/dates, prompts (or a representative sample),
  configs, seeds where applicable, and the synthetic fixtures so the pipeline runs end-to-end.
  Complete a reproducibility checklist (NeurIPS-style) before submission.

## Ethics

- Include an ethics / responsible-use statement (`ETHICS.md`): not investment advice; no performance
  claim; auditability; data-provider and broker compliance; LLM-use and conflict-of-interest disclosure.

## Pre-submission checklist

- [ ] No overclaim; central claim is the admission rate, with sample size + uncertainty.
- [ ] Every reference verified against its primary source; `references.bib` rebuilt; no fabricated cites.
- [ ] Figures self-contained, vector, colorblind-safe, axes labelled.
- [ ] Experiment design pre-registered and unchanged post-hoc; amendments dated.
- [ ] Reproducibility appendix + checklist complete; synthetic fixtures run end-to-end.
- [ ] Ethics statement included; data/broker compliance confirmed; no secrets or live records in the repo.
- [ ] Venue formatting/anonymization/page-limit met; plagiarism/dual-submission policies checked.

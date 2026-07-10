# ai_supply_chain — OAR domain pack (v0, aggregate-only)

The reference domain pack for the discipline curve (design doc Sec 5). Every number in
[`aggregate_results.json`](aggregate_results.json) is sourced from already-published,
already-sanitized material:

- [`../../../../examples/ai_supply_chain/README.md`](../../../../examples/ai_supply_chain/README.md)
  — the worked example and its ablation table.
- [`../../../../src/prompts.md`](../../../../src/prompts.md) §8 — the literal arm prompts
  (recovered originals for arms a–c; the two pending arms b/c run under the identical
  protocol).
- [`../../../../research/docs/RESULTS_V2_WORKING.md`](../../../../research/docs/RESULTS_V2_WORKING.md)
  — the full ablation table (all six arms) and the H5 rejection-quality-audit expansion
  (n=14 pilot superseded by the documented n=40 draw).

## What this pack is (and is not)

**Is:** the aggregate admission count/rate for each of the six ablation arms on the
*same* preserved 38-candidate batch, plus the recorded rejection-precision figures (raw
+ adjudicated) for the full pipeline's rejections. This is exactly what the harness needs
to reproduce the discipline curve and OAR at a fixed admission budget.

**Is not:** a per-card dataset. The 38 candidates' identities, symbols, and per-card
admit/reject decisions live in the private research repo and are not released here (see
`domain_pack.json`'s `privacy_note`). A future pack version (v0.5, per the design doc's
staged roadmap) that ships *constructed* planted-bait cards with known-by-construction
labels will not have this limitation — those cards never touch a real name, so they carry
no privacy boundary to begin with.

## Why OAR is computable from the aggregate alone, here

The disciplined reference (`full_pipeline`) admitted **0 of 38** candidates. When a
reference admits nothing, its rejected set is the *entire* pool — so every card any
ablated arm admits is, by construction, an over-admission relative to that reference. OAR
therefore collapses to the arm's own admission rate for this specific pack (see
`benchmarks/oar/scoring.py::oar_from_aggregate_zero_reference`, which asserts this
precondition explicitly rather than assuming it silently). This is a special case of the
general per-card formula (`compute_oar`), not a shortcut invented for convenience.

## Run it

```bash
python -m benchmarks.oar.harness ai_supply_chain
python -m benchmarks.oar.harness ai_supply_chain --format json
```

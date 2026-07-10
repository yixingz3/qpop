# uranium — OAR domain pack (v0, aggregate-only)

The second v0 pack, demonstrating the `meta.domain` profile pattern's portability (design
doc Sec 2/4, H3 clause (c)): the same public schema/loader/scoring code applies to a
second domain with **one new config file and zero code changes**.

Every number in [`aggregate_results.json`](aggregate_results.json) is sourced from:

- [`../../../../research/docs/RESULTS_V2_WORKING.md`](../../../../research/docs/RESULTS_V2_WORKING.md)
  §"Portability H3 clause (c)" — the single live funnel run on the uranium fuel cycle.

## What this pack is (and is not)

**Is:** the funnel-stage counts (sourced → unique symbols → gate pass/fail → triage
pursue/drop → bear-case admit-flag/watchlist/reject → adjudicated) from one real,
documented funnel run, plus the admission rate computed off those counts.

**Is not:** an ablation batch. Unlike `ai_supply_chain`, no baselines with a discipline
removed were run on this domain in v0 — there is exactly one recorded run, at full
discipline. Consequently this pack has no `arms[]` in `aggregate_results.json`, and the
harness does not attempt to compute a discipline curve or OAR for it (`load_pack(...).
has_ablation` is `False`). It is **not** part of the discipline-curve reference — that
reference is the AI-supply-chain 38-card batch only.

**Not published:** a filled-in `bottleneck_map.yml` for uranium. The live map (nodes,
tickers, scores) is private; only the public
[`examples/template_domain/bottleneck_map.template.yml`](../../../../examples/template_domain/bottleneck_map.template.yml)
shape is released, which is what `domain_pack.json`'s `node_list_ref` points at.

## Run it

```bash
python -m benchmarks.oar.harness uranium
python -m benchmarks.oar.harness uranium --format json
```

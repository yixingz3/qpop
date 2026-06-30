# template_domain — start a new bottleneck domain here

Copy this directory to `examples/<your_domain>/` and fill in the two configs. The *engine* does not
change — only the domain map and the benchmark. That is the flywheel: a new domain is a config, not
a codebase.

```
examples/<your_domain>/
  bottleneck_map.yml      # the thesis: nodes (chokepoints), edges, scores, exit triggers
  benchmark_config.yml    # the theme benchmark + scoreboard settings
  candidate_process.md    # (optional) domain-specific gate thresholds / notes
```

## Steps

1. **Name the chokepoints.** What are the *physical*, hard-to-bypass steps in this supply chain
   (e.g. for rare earth: separation/refining capacity, magnet manufacturing, mining permits,
   substitution)? Each becomes a node in `bottleneck_map.yml`.
2. **Score each node** on `bottleneck_dims` (physical_indispensability, substitutability,
   capacity_lead_time, supplier_concentration, pricing_power) + `demand_score` +
   `valuation_adjustment` + `crowding_adjustment`.
3. **Write measurable `exit_triggers`** for each node — each with a checkable `data_source`. A
   trigger you cannot actually check is rejected.
4. **List candidate tickers** per node with `exposure_purity` + role. US-tradeable (or your venue)
   only; foreign-only listings are context, not candidates.
5. **Set the benchmark** in `benchmark_config.yml` (the theme benchmark you measure alpha against).
6. **Run the funnel** (source → gate → evaluate), **pre-register** admissions in the QPOP ledger,
   and **forward-validate**.

## Domains this schema fits

AI supply chain (the worked example) · rare earth / critical minerals · power grid / transformers ·
LNG / gas infrastructure · uranium / nuclear fuel cycle · copper / electrification · defense
industrial base · and others. Each is a different `bottleneck_map.yml` over the same engine.

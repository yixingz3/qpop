# src — engine interfaces

The engine is organized into six modules with clear boundaries. This `src/` tree defines the
**interfaces and contracts**; a working reference implementation exists in a private deployment
and is being progressively generalized and open-sourced here as
domain-agnostic code. Until then, this document is the authoritative spec — a contributor can
implement against these contracts. **Now open-sourced:** the QPOP pre-registration ledger (the
`qpop/` contract) ships as the runnable, dependency-free [`forward_qpop`](forward_qpop/) package
(`pip install forward-qpop`) — the first engine module generalized out of the private deployment.
The **stage prompts** (the disciplines themselves) are committed
in [`prompts.md`](prompts.md), and the **deterministic gate** is specified with reference pseudocode
in [`gate_reference.md`](gate_reference.md) — so the method is reproducible from this repo alone.

```
src/
  qpop/         forward pre-registration ledger (admission + belief-update + posterior)
  scoring/      confidence decomposition (bottleneck × purity × demand × valuation × crowding)
  discovery/    the SOURCE stage (cheap-model candidate sourcing, by node + gaps/social/policy lenses)
  gating/       the deterministic GATE (tradeability, liquidity, overlap penalty) — NO model
  evaluation/   the EVALUATE stage (expensive-model finalist judgment; bear-case-before-recommendation)
  validation/   forward validation (conservative shadow fills, benchmark-relative scoreboard)
```

## Module contracts

### `scoring/`
```
bottleneck_score(dims, weights) -> float in [0,1]      # substitutability is inverted
score_ticker(node, ticker) -> { final_confidence, ... } # = bottleneck × purity × demand × val × crowd
```
Tier is derived from `final_confidence` (core ≥ θ_core, satellite ≥ θ_sat, else dropped). Policy is
**not** an input — it is evidence + a trigger (see `qpop/` and `gating/`).

### `gating/`
```
evaluate_candidate(symbol, node, book) -> {
  gates: { tradable, min_price, min_dollar_volume },
  overlap_penalty,            # same-node-core + correlation-to-core
  corr_to_core, beta, incremental_value
}
```
Pure and deterministic. No LLM. A failing candidate is watchlist-only.

### `discovery/` and `evaluation/`
The funnel's model-backed stages, run as a cost cascade (cheapest models do the volume; the expensive
model only ever judges admits): **SOURCE** (cheap, wide — one lens per node + gaps/social/policy/
literature, deduped against a seen-set) → GATE → **TRIAGE** (cheapest — drop obvious low-purity) →
**EVALUATE** (mid — bear-case-before-recommendation on survivors) → **ADJUDICATE** (expensive — only
the admit-flags). Each stage's exact prompt is in [`prompts.md`](prompts.md); the model tier is a
**knob** (`docs/TUNING.md`). The asymmetry that makes the cascade safe — a false watchlist only
delays, a false admit is caught downstream — also governs the audit of rejections.

### `qpop/`
```
register_admission(hypothesis) -> entry_with_content_hash   # before any position
update_belief(id, evidence) -> posterior                    # content-hash protected
close(id, outcome)                                          # Supported | Weakened | Falsified (immutable)
```

### `validation/`
```
shadow_fill(open_price, slippage_bps) -> conservative_fill
scoreboard(book, benchmark) -> { excess_return, information_ratio, active_drawdown, ... }
```

## Contributing

Implement a module against its contract, with tests, against the `examples/template_domain/`
configs and `data/synthetic/` fixtures. Keep all live/secret/broker artifacts out of this repo
(`.gitignore` enforces the obvious cases).

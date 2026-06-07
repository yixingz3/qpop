# src — engine interfaces

The engine is organized into six modules with clear boundaries. This `src/` tree defines the
**interfaces and contracts**; a working reference implementation exists in a private deployment
(the live AI-supply-chain book) and is being progressively generalized and open-sourced here as
domain-agnostic code. Until then, this document is the authoritative spec — a contributor can
implement against these contracts.

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
The funnel's two model-backed stages. `discovery/` runs the cheap model wide (one lens per node +
gaps/social/policy). `evaluation/` runs the expensive model on finalists only, each producing a
**bear case written before the recommendation** and a falsifiable decision. The model tier for each
stage is a **knob** (`docs/TUNING.md`), including a cheap-first-pass / expensive-adjudication mode.

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

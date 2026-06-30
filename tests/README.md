# tests

Tests run against the `examples/template_domain/` configs and `data/synthetic/` fixtures — never
against live data or a real account.

Target coverage as the engine modules land:

- **gating/** — determinism (same inputs → same gate result); overlap-penalty math; liquidity/price
  thresholds; missing-price handling (flag, don't silently size).
- **scoring/** — the confidence decomposition; tier derivation at the thresholds; that adding a
  `policy:` block leaves a name's confidence **unchanged** (policy is evidence, not a factor).
- **qpop/** — content-hash integrity (editing a closed entry breaks the hash); append-only ledger.
- **validation/** — conservative shadow-fill sign conventions; benchmark-relative scoreboard.
- **discovery/evaluation/** — schema-validity of agent outputs; the bear-case field is populated
  before a recommendation; budget/fan-out caps are respected and any truncation is logged.

Keep tests fast and deterministic. Mock model calls in unit tests; reserve any live-model runs for
a clearly-marked, optional integration suite.

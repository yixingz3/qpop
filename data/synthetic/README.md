# data/synthetic

**Non-sensitive, illustrative fixtures only.** Use this directory for synthetic prices, sample
candidate cards, and sample QPOP ledger entries that exercise the engine for tests and demos.

Never place here (or anywhere in this repo): live broker logs, real trade records, paid-data
exports, or anything tied to an actual account. The forward paper-trading record, if released later,
is published as **aggregated** discipline/performance statistics — not as positions or trades.

Suggested contents:
- `prices_synthetic.csv` — deterministic synthetic price series for a handful of fake tickers.
- `candidate_cards_sample.jsonl` — example SOURCE output (the card schema).
- `qpop_ledger_sample.jsonl` — example pre-registration entries with content hashes.
- `scoreboard_sample.csv` — example discipline metrics (counts, admission rate) over a fake window.

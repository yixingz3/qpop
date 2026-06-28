# qpop schemas

Machine-readable [JSON Schema](https://json-schema.org/) (draft 2020-12) for the data structures the
discipline produces and consumes. They make `qpop` read as **infrastructure**, not a prompt pack: an
agent (or a CI gate) can validate a card, a ledger entry, or a run before trusting it.

| Schema | Validates | Notes |
|---|---|---|
| [`candidate_card.schema.json`](candidate_card.schema.json) | a SOURCE-stage candidate | the unit the gate + bear-case consume |
| [`qpop_entry.schema.json`](qpop_entry.schema.json) | one line of a ledger `.jsonl` | `oneOf` admission / belief_update / outcome, plus the hash-chain fields |
| [`evidence.schema.json`](evidence.schema.json) | a dated, tiered fact | the building block of cards + entries |
| [`exit_trigger.schema.json`](exit_trigger.schema.json) | a pre-committed exit condition | must name a checkable `data_source` |
| [`run_manifest.schema.json`](run_manifest.schema.json) | one `SOURCE → GATE → EVALUATE` run | provenance + funnel counts + admission rate |

**Self-contained on purpose.** `qpop_entry` and `candidate_card` embed `evidence` / `exit_trigger`
under `$defs` so they validate with no external `$ref` resolver (the standalone `evidence` and
`exit_trigger` files are the canonical, reusable copies). The hash fields follow the ledger
convention: `content_hash` is `sha256:<64-hex>`; `prev_hash` and `entry_hash` are bare `<64-hex>`
(64 zeros at genesis).

## Validate

```bash
pip install jsonschema
python repro/validate_samples.py     # checks data/synthetic/* against these schemas
```

Or inline:

```python
import json
from jsonschema import Draft202012Validator
schema = json.load(open("schemas/qpop_entry.schema.json", encoding="utf-8"))
Draft202012Validator(schema).validate(my_entry)
```

The synthetic fixtures in [`../data/synthetic/`](../data/synthetic) are kept valid against these
schemas by `repro/validate_samples.py`.

# Reproducing qpop's claims

Everything below runs from a **clean clone** with **Python 3.9+** (the ledger core has no
dependencies). Two steps need an extra: schema validation needs `jsonschema`; the paper build
needs `pdflatex` + `bibtex`. Total time is under a minute, excluding the paper build.

`make` targets are shown first; the raw command beneath each works without `make`.

## 1. Ledger + anchor integrity — the core claim (~1s)

```bash
make test            # or: python -m pytest -q
```

Expected: **`21 passed`** — 9 ledger + 7 anchor + 5 schema tests covering field-tamper, insert,
delete, reorder, terminal re-registration, tertiary-only blocking, anchor drift-detection, and
schema/fixture validation (with `format: date` enforced).

## 2. Verify the shipped sample ledger (~1s)

```bash
make verify-sample   # or: python scripts/qpop.py verify data/synthetic/qpop_ledger_sample.jsonl
```

Expected: **`OK — 3 entries, integrity verified.`**

## 3. Watch tamper-evidence fire (~3s)

```bash
python repro/tamper_demo.py
```

Expected: step 1 verifies clean; step 2 (after editing one frozen field) reports a
`content_hash mismatch`, and the script prints **`PASS`** (exit 0).

## 4. External timestamp anchor (~1s)

```bash
python scripts/qpop.py anchor        data/synthetic/qpop_ledger_sample.jsonl
python scripts/qpop.py verify-anchor data/synthetic/qpop_ledger_sample.jsonl
```

Expected: **`anchor OK`**. Now append or edit an entry and re-run `verify-anchor`: it reports
the head/digest drift and exits non-zero. The `.anchor.json` is gitignored; add `--ots` to
also OpenTimestamps-stamp it if the client is installed.

## 5. Fixtures match the published schemas (~1s, needs `pip install jsonschema`)

```bash
python repro/validate_samples.py
```

Expected: **`ALL SAMPLES VALID`** — every row in `data/synthetic/` validates against
[`schemas/`](../schemas).

## 6. Build the paper (~30s, needs pdflatex + bibtex)

```bash
make paper           # -> research/paper/paper.pdf
```

Expected: a clean 25-page PDF, no undefined references.

---

**What is *not* reproducible here, by design:** forward performance (the evaluation window is
open; no return is claimed) and the live book (positions and paid feeds are never released).
See the paper's *Reproducibility and Release* table.

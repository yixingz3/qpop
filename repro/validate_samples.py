#!/usr/bin/env python3
"""Validate the synthetic fixtures against schemas/ (JSON Schema draft 2020-12).

Run from the repo root:

    python repro/validate_samples.py

Needs `pip install jsonschema`. Exits non-zero if any sample fails its schema, so
this doubles as a CI gate that the fixtures and the published schemas stay in sync.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATA = ROOT / "data" / "synthetic"


def _load(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _jsonl(p: Path) -> list:
    return [json.loads(ln) for ln in Path(p).read_text(encoding="utf-8").splitlines() if ln.strip()]


def main() -> int:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema not installed  ->  pip install jsonschema")
        return 2

    cases = [
        ("qpop_entry.schema.json", _jsonl(DATA / "qpop_ledger_sample.jsonl"), "ledger entry"),
        ("candidate_card.schema.json", _jsonl(DATA / "candidate_cards_sample.jsonl"), "candidate card"),
        ("run_manifest.schema.json", [_load(DATA / "run_manifest_sample.json")], "run manifest"),
    ]

    failures = 0
    for schema_name, rows, label in cases:
        validator = Draft202012Validator(
            _load(SCHEMAS / schema_name),
            format_checker=Draft202012Validator.FORMAT_CHECKER,  # actually enforce `format: date`
        )
        for i, row in enumerate(rows):
            errs = sorted(validator.iter_errors(row), key=lambda e: list(e.path))
            if errs:
                failures += 1
                print(f"FAIL  {label}[{i}]  vs  {schema_name}")
                for e in errs:
                    print(f"        {list(e.path)}: {e.message}")
            else:
                print(f"ok    {label}[{i}]  vs  {schema_name}")

    print("\n" + ("ALL SAMPLES VALID" if not failures else f"{failures} FAILURE(S)"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

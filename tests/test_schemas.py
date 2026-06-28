"""Schema tests: fixtures validate (with `format: date` actually enforced), all three
ledger entry types are exercised, and the standalone "canonical" schemas stay byte-equivalent
(modulo descriptions) to the embedded ``$defs`` mirrors.

Needs jsonschema (skipped if absent). Runs under pytest, or standalone with ``PYTHONPATH=src``.
"""
import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")
from jsonschema import Draft202012Validator  # noqa: E402

from forward_qpop import Ledger  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATA = ROOT / "data" / "synthetic"


def _load(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _jsonl(p: Path) -> list:
    return [json.loads(ln) for ln in Path(p).read_text(encoding="utf-8").splitlines() if ln.strip()]


def _validator(name: str) -> "Draft202012Validator":
    return Draft202012Validator(_load(SCHEMAS / name), format_checker=Draft202012Validator.FORMAT_CHECKER)


def test_fixtures_validate_with_formats():
    cases = [
        ("qpop_entry.schema.json", _jsonl(DATA / "qpop_ledger_sample.jsonl")),
        ("candidate_card.schema.json", _jsonl(DATA / "candidate_cards_sample.jsonl")),
        ("run_manifest.schema.json", [_load(DATA / "run_manifest_sample.json")]),
    ]
    for name, rows in cases:
        v = _validator(name)
        for row in rows:
            errs = list(v.iter_errors(row))
            assert not errs, (name, [e.message for e in errs])


def test_sample_exercises_all_three_entry_types():
    rows = _jsonl(DATA / "qpop_ledger_sample.jsonl")
    assert {r["type"] for r in rows} == {"admission", "belief_update", "outcome"}


def test_belief_update_branch_roundtrip(tmp_path):
    led = Ledger(tmp_path / "l.jsonl")
    led.register("H-1", "a", prior=0.5)
    bu = led.update("H-1", evidence=[{"summary": "x", "tier": "secondary", "date": "2026-02-01"}])
    errs = list(_validator("qpop_entry.schema.json").iter_errors(bu))
    assert not errs, [e.message for e in errs]


def test_date_format_is_enforced():
    bad = {
        "id": "H", "type": "admission", "status": "open", "created": "NOT-A-DATE",
        "claim": "c", "evidence": [], "exit_triggers": [],
        "content_hash": "sha256:" + "0" * 64, "prev_hash": "0" * 64, "entry_hash": "0" * 64,
    }
    assert list(_validator("qpop_entry.schema.json").iter_errors(bad)), \
        "an invalid `created` date must be rejected when format_checker is active"


def test_embedded_defs_match_standalone():
    """The embedded $defs (mirrors) must equal the standalone 'canonical' schemas, ignoring
    descriptions / $id / $schema / title — so the schemas/README 'canonical copy' claim holds."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k not in ("description", "$id", "$schema", "title")}
        if isinstance(o, list):
            return [strip(x) for x in o]
        return o

    qpop = _load(SCHEMAS / "qpop_entry.schema.json")
    card = _load(SCHEMAS / "candidate_card.schema.json")
    evidence = strip(_load(SCHEMAS / "evidence.schema.json"))
    exit_trigger = strip(_load(SCHEMAS / "exit_trigger.schema.json"))

    assert strip(qpop["$defs"]["evidence"]) == evidence
    assert strip(card["$defs"]["evidence"]) == evidence
    assert strip(qpop["$defs"]["exit_trigger"]) == exit_trigger


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            import inspect
            if "tmp_path" in inspect.signature(fn).parameters:
                import tempfile
                fn(Path(tempfile.mkdtemp()))
            else:
                fn()
            print("PASS", fn.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)

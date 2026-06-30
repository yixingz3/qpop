"""Tests for forward_qpop.anchor.

Runs under pytest, or standalone (``python tests/test_anchor.py``) with no third-party
dependencies -- set ``PYTHONPATH=src`` if the package is not installed.
"""
import json
import tempfile
from pathlib import Path

from forward_qpop import (
    GENESIS,
    Ledger,
    build_manifest,
    ledger_head,
    ots_available,
    verify_anchor,
    write_manifest,
)

_CANON = dict(sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _tmp() -> Path:
    return Path(tempfile.mkdtemp()) / "ledger.jsonl"


def _seed(path: Path) -> Ledger:
    led = Ledger(path)
    led.register(
        "H-1", "a", prior=0.5,
        evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
    )
    led.register("H-2", "b", prior=0.4)
    return led


def test_manifest_matches_head():
    p = _tmp()
    led = _seed(p)
    m = build_manifest(p)
    head, n = ledger_head(p)
    assert m["head_entry_hash"] == head == led.entries()[-1]["entry_hash"]
    assert m["n_entries"] == n == 2
    assert m["schema"].startswith("forward-qpop/anchor")
    assert len(m["file_sha256"]) == 64


def test_write_and_verify_anchor_ok():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    res = verify_anchor(p)
    assert res.ok, res.problems
    assert any("head_entry_hash" in c for c in res.checks)


def test_verify_anchor_detects_append():
    p = _tmp()
    led = _seed(p)
    write_manifest(p)
    led.register("H-3", "c")  # append AFTER anchoring -> head + n + digest all move
    res = verify_anchor(p)
    assert not res.ok
    assert any(("head_entry_hash" in x or "n_entries" in x or "file_sha256" in x) for x in res.problems)


def test_verify_anchor_detects_field_tamper():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    lines = p.read_text(encoding="utf-8").splitlines()
    obj = json.loads(lines[0])
    obj["claim"] = "TAMPERED"  # edit a frozen field, leave the stored hashes
    lines[0] = json.dumps(obj, **_CANON)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    res = verify_anchor(p)  # chain break (content_hash) + file digest mismatch
    assert not res.ok
    assert res.problems


def test_verify_anchor_missing_manifest():
    p = _tmp()
    _seed(p)
    res = verify_anchor(p)  # no manifest written
    assert not res.ok
    assert any("manifest" in x for x in res.problems)


def test_empty_ledger_anchor():
    p = _tmp()
    write_manifest(p)  # nonexistent / empty ledger
    m = build_manifest(p)
    assert m["head_entry_hash"] == GENESIS and m["n_entries"] == 0
    assert verify_anchor(p).ok


def test_ots_available_is_bool():
    assert isinstance(ots_available(), bool)  # never raises, with or without `ots` installed


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print("PASS", fn.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)

"""Tests for forward_qpop.ledger.

Runs under pytest, or standalone (``python tests/test_ledger.py``) with no third-party
dependencies — set ``PYTHONPATH=src`` if the package is not installed.
"""
import json
import tempfile
from pathlib import Path

from forward_qpop import IntegrityError, Ledger, verify_file

_CANON = dict(sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _tmp() -> Path:
    return Path(tempfile.mkdtemp()) / "ledger.jsonl"


def test_register_and_verify():
    led = Ledger(_tmp())
    led.register(
        "H-X-01", "claim A", mechanism="m", prior=0.5,
        evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
        exit_triggers=[{"id": "t", "metric": "x", "op": "<", "data_source": {"tier": "secondary"}}],
        fields={"decomposed_confidence": {"final_confidence": 0.12}},
    )
    led.register("H-X-02", "claim B", prior=0.4)
    res = led.verify()
    assert res.ok, res.problems
    assert res.n_entries == 2


def test_chain_links():
    p = _tmp()
    led = Ledger(p)
    e1 = led.register("H-1", "a")
    e2 = led.register("H-2", "b")
    assert e1["prev_hash"] == "0" * 64            # genesis
    assert e2["prev_hash"] == e1["entry_hash"]    # chained
    assert verify_file(p).ok


def test_update_and_close():
    p = _tmp()
    led = Ledger(p)
    led.register("H-1", "a", prior=0.5)
    led.update("H-1", evidence=[{"tier": "primary", "summary": "new fact"}])
    led.close("H-1", "supported", observed={"note": "played out"})
    res = verify_file(p)
    assert res.ok and res.n_entries == 3


def test_tertiary_only_blocked_then_allowed():
    p = _tmp()
    led = Ledger(p)
    led.register("H-1", "a")
    try:
        led.update("H-1", evidence=[{"tier": "tertiary"}])
        raise AssertionError("tertiary-only update should have been blocked")
    except IntegrityError:
        pass
    led.update("H-1", evidence=[{"tier": "tertiary"}], allow_tertiary_only=True)
    assert verify_file(p).ok


def test_reregister_after_terminal_blocked():
    led = Ledger(_tmp())
    led.register("H-1", "a")
    led.close("H-1", "falsified")
    try:
        led.register("H-1", "a-again")
        raise AssertionError("re-registering a closed id should be blocked")
    except IntegrityError:
        pass


def test_detect_field_tamper():
    p = _tmp()
    led = Ledger(p)
    led.register("H-1", "original claim", prior=0.5)
    led.register("H-2", "b")
    lines = p.read_text(encoding="utf-8").splitlines()
    obj = json.loads(lines[0])
    obj["claim"] = "TAMPERED claim"               # edit a frozen field, leave hashes
    lines[0] = json.dumps(obj, **_CANON)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    res = verify_file(p)
    assert not res.ok
    assert any("content_hash mismatch" in x for x in res.problems)


def test_detect_reorder():
    p = _tmp()
    led = Ledger(p)
    led.register("H-1", "a")
    led.register("H-2", "b")
    led.register("H-3", "c")
    lines = p.read_text(encoding="utf-8").splitlines()
    lines[0], lines[1] = lines[1], lines[0]       # swap first two
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    res = verify_file(p)
    assert not res.ok
    assert any("prev_hash" in x or "reorder" in x.lower() for x in res.problems)


def test_detect_delete():
    p = _tmp()
    led = Ledger(p)
    led.register("H-1", "a")
    led.register("H-2", "b")
    led.register("H-3", "c")
    lines = p.read_text(encoding="utf-8").splitlines()
    del lines[1]                                  # delete the middle entry
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert not verify_file(p).ok


def test_empty_ledger_verifies():
    assert verify_file(_tmp()).ok                 # nonexistent / empty == 0 entries, ok


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

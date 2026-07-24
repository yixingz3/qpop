"""Tests for the WI-29 ledger integration in forward_qpop.evalue.

Covers the real wiring between a Ledger and SequentialTriggerTest: pre-registration
config lives in the admission entry's ``"evalue"`` field, per-step observations live in
belief_update entries' ``"trigger_checks"`` field, and state resumes across repeated
`run_ledger_evalue` / `forward-qpop evalue` invocations via a JSON sidecar next to the
ledger -- never mutating the ledger itself.

Runs under pytest, or standalone (``python tests/test_evalue_ledger.py``) with no
third-party dependencies -- set ``PYTHONPATH=src`` if the package is not installed.
"""
import json
import tempfile
from pathlib import Path

import pytest

from forward_qpop import Ledger
from forward_qpop.cli import main as cli_main
from forward_qpop.evalue import (
    EvalueLedgerError,
    default_state_path_for,
    run_ledger_evalue,
)


def _tmp() -> Path:
    return Path(tempfile.mkdtemp()) / "ledger.jsonl"


def _seed_with_config(path: Path, *, p0=0.1, p1=0.6, combine="average", hid="H-1") -> Ledger:
    led = Ledger(path)
    led.register(
        hid, "claim",
        prior=0.5,
        evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
        exit_triggers=[
            {"id": "trig_a", "metric": "m", "op": ">", "data_source": {"tier": "secondary"}},
            {"id": "trig_b", "metric": "n", "op": "<", "data_source": {"tier": "secondary"}},
        ],
        fields={"evalue": {"p0": p0, "p1": p1, "combine": combine}},
    )
    return led


def _observe(led: Ledger, hid: str, checks: dict, day: str) -> None:
    led.update(
        hid,
        evidence=[{"summary": "check", "tier": "secondary", "date": day}],
        fields={"trigger_checks": checks},
    )


# --------------------------------------------------------------------------- #
# Honest skip: no pre-registered evalue config
# --------------------------------------------------------------------------- #
def test_hypothesis_without_evalue_config_is_reported_not_fabricated():
    p = _tmp()
    led = Ledger(p)
    led.register("H-NOCFG", "claim", prior=0.5)  # no fields={"evalue": ...}
    rows, _ = run_ledger_evalue(p)
    assert len(rows) == 1
    assert rows[0].status == "no_config"
    assert rows[0].e_value is None
    assert rows[0].decision is None


# --------------------------------------------------------------------------- #
# Fresh run
# --------------------------------------------------------------------------- #
def test_fresh_run_computes_merged_evalue_from_trigger_checks():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")

    rows, _ = run_ledger_evalue(p, alpha=0.05)
    assert len(rows) == 1
    row = rows[0]
    assert row.status == "ok"
    assert row.n_triggers == 1
    assert row.n_observations == 1
    # average of one e-process: p1/p0 = 6.0
    assert abs(row.e_value - 6.0) < 1e-9
    assert row.threshold == 20.0
    assert row.decision == "continue"


def test_sidecar_state_file_is_written_next_to_ledger():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    run_ledger_evalue(p)
    sp = default_state_path_for(p)
    assert sp.exists()
    state = json.loads(sp.read_text(encoding="utf-8"))
    assert state["schema"].startswith("forward-qpop/evalue-state")
    assert "H-1" in state["hypotheses"]
    # The ledger file itself must be untouched by evalue (no mutation of ledger rows).
    ledger_lines_before = p.read_text(encoding="utf-8").splitlines()
    run_ledger_evalue(p)
    ledger_lines_after = p.read_text(encoding="utf-8").splitlines()
    assert ledger_lines_before == ledger_lines_after


def test_dry_run_does_not_persist_state():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    run_ledger_evalue(p, persist=False)
    sp = default_state_path_for(p)
    assert not sp.exists()


# --------------------------------------------------------------------------- #
# Resumed run: state round-trip, anytime-valid across invocations
# --------------------------------------------------------------------------- #
def test_resumed_run_with_no_new_observations_is_idempotent():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")

    rows1, _ = run_ledger_evalue(p, alpha=0.05)
    rows2, _ = run_ledger_evalue(p, alpha=0.05)  # nothing new appended
    assert rows1[0].e_value == rows2[0].e_value
    assert rows1[0].n_observations == rows2[0].n_observations == 1


def test_resumed_run_folds_in_only_the_new_observations():
    p = _tmp()
    led = _seed_with_config(p, p0=0.1, p1=0.6)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows1, _ = run_ledger_evalue(p, alpha=0.05)
    assert rows1[0].n_observations == 1
    e1 = rows1[0].e_value

    _observe(led, "H-1", {"trig_a": True}, "2026-01-03")
    rows2, _ = run_ledger_evalue(p, alpha=0.05)
    assert rows2[0].n_observations == 2  # not 1, not 3 -- exactly one new fold-in
    # Folding the same "fired" observation in again multiplies by p1/p0 again.
    assert abs(rows2[0].e_value - e1 * (0.6 / 0.1)) < 1e-9


def test_resumed_run_matches_a_single_from_scratch_run():
    """Resuming across two invocations must land on the same e-value as replaying the
    whole history in one shot -- the sidecar is a resume optimization, not a different
    computation."""
    p_incremental = _tmp()
    led = _seed_with_config(p_incremental, p0=0.15, p1=0.55)
    _observe(led, "H-1", {"trig_a": True, "trig_b": False}, "2026-01-02")
    run_ledger_evalue(p_incremental, alpha=0.05)
    _observe(led, "H-1", {"trig_a": False, "trig_b": True}, "2026-01-03")
    rows_incremental, _ = run_ledger_evalue(p_incremental, alpha=0.05)

    p_fromscratch = _tmp()
    led2 = _seed_with_config(p_fromscratch, p0=0.15, p1=0.55)
    _observe(led2, "H-1", {"trig_a": True, "trig_b": False}, "2026-01-02")
    _observe(led2, "H-1", {"trig_a": False, "trig_b": True}, "2026-01-03")
    rows_fromscratch, _ = run_ledger_evalue(p_fromscratch, alpha=0.05)

    assert abs(rows_incremental[0].e_value - rows_fromscratch[0].e_value) < 1e-9


# --------------------------------------------------------------------------- #
# Falsified decision at e >= 1/alpha
# --------------------------------------------------------------------------- #
def test_falsified_decision_once_evalue_crosses_threshold():
    p = _tmp()
    led = _seed_with_config(p, p0=0.1, p1=0.9)  # ratio 9 per fired observation
    alpha = 0.1  # threshold = 10
    for i in range(3):
        _observe(led, "H-1", {"trig_a": True}, f"2026-01-0{i + 2}")
    rows, _ = run_ledger_evalue(p, alpha=alpha)
    row = rows[0]
    assert row.e_value >= 1.0 / alpha
    assert row.decision == "falsified"


# --------------------------------------------------------------------------- #
# Loud failures -- schema/CLI errors never silently swallowed
# --------------------------------------------------------------------------- #
def test_evalue_config_missing_p1_loud_fails():
    p = _tmp()
    led = Ledger(p)
    led.register("H-BAD", "claim", fields={"evalue": {"p0": 0.1}})  # no p1
    with pytest.raises(EvalueLedgerError, match="p0.*p1|p1.*p0"):
        run_ledger_evalue(p)


def test_malformed_trigger_checks_type_loud_fails():
    p = _tmp()
    led = _seed_with_config(p)
    led.update(
        "H-1",
        evidence=[{"summary": "bad", "tier": "secondary", "date": "2026-01-02"}],
        fields={"trigger_checks": "not-a-dict"},
    )
    with pytest.raises(EvalueLedgerError, match="trigger_checks"):
        run_ledger_evalue(p)


def test_unregistered_trigger_id_loud_fails():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"never_registered": True}, "2026-01-02")
    with pytest.raises(EvalueLedgerError, match="unregistered"):
        run_ledger_evalue(p)


def test_invalid_alpha_rejected():
    p = _tmp()
    _seed_with_config(p)
    with pytest.raises(ValueError, match="alpha"):
        run_ledger_evalue(p, alpha=1.5)
    with pytest.raises(ValueError, match="alpha"):
        run_ledger_evalue(p, alpha=0.0)


def test_rewritten_ledger_since_sidecar_loud_fails():
    """If the sidecar's last_entry_hash can no longer be found in the ledger (the ledger
    was truncated/rewritten out from under it), resuming must fail loudly rather than
    silently re-deriving from scratch or skipping everything."""
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    run_ledger_evalue(p)  # writes a sidecar pointing at the belief_update's entry_hash

    # Simulate a rewritten ledger: truncate back to just the admission entry.
    lines = p.read_text(encoding="utf-8").splitlines()
    p.write_text(lines[0] + "\n", encoding="utf-8")

    with pytest.raises(EvalueLedgerError, match="rewritten|truncated"):
        run_ledger_evalue(p)


# --------------------------------------------------------------------------- #
# CLI-level
# --------------------------------------------------------------------------- #
def test_cli_evalue_prints_table_and_exits_zero(capsys):
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")

    rc = cli_main(["evalue", str(p), "--alpha", "0.05"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "H-1" in out
    assert "continue" in out


def test_cli_evalue_json_report(capsys):
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")

    rc = cli_main(["evalue", str(p), "--json", "--no-persist"])
    out = capsys.readouterr().out
    assert rc == 0
    report = json.loads(out)
    assert report[0]["id"] == "H-1"
    assert report[0]["status"] == "ok"
    assert not default_state_path_for(p).exists()  # --no-persist honored


def test_cli_evalue_writes_out_file(tmp_path, capsys):
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    out_path = tmp_path / "report.json"

    rc = cli_main(["evalue", str(p), "--out", str(out_path)])
    assert rc == 0
    report = json.loads(out_path.read_text(encoding="utf-8"))
    assert report[0]["id"] == "H-1"


def test_cli_evalue_loud_fail_returns_nonzero(capsys):
    p = _tmp()
    Ledger(p).register("H-BAD", "claim", fields={"evalue": {"p0": 0.1}})  # missing p1

    rc = cli_main(["evalue", str(p)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "FAILED" in out


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    skipped = 0
    for fn in fns:
        try:
            import inspect

            params = inspect.signature(fn).parameters
            if "capsys" in params or "tmp_path" in params:
                print("SKIP (needs pytest fixture)", fn.__name__)
                skipped += 1
                continue
            fn()
            print("PASS", fn.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"\n{len(fns) - failed - skipped}/{len(fns)} passed ({skipped} skipped, need pytest)")
    sys.exit(1 if failed else 0)

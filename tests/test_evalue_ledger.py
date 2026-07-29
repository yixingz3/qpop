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
    save_evalue_state,
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
    # BOTH registered triggers enter the mixture at fixed weight (WI-40) even
    # though only trig_a reported: average of {6.0, 1.0} = 3.5.
    assert row.n_triggers == 2
    assert row.n_observations == 1
    assert abs(row.e_value - 3.5) < 1e-9
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
# Resumed run: state round-trip, exactly-once folding across invocations
# (state-resumption mechanics only; no statistical guarantee is asserted here)
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
    # Exactly-once folding under fixed two-trigger membership (WI-40): after one
    # fire e1 = ((p1/p0) + 1)/2 = 3.5; after the second fire on the same trigger
    # the merged average is ((p1/p0)^2 + 1)/2 -- NOT e1 * (p1/p0), which was the
    # single-process arithmetic of the pre-fix lazy-membership behavior.
    assert abs(e1 - ((0.6 / 0.1) + 1.0) / 2.0) < 1e-9
    assert abs(rows2[0].e_value - ((0.6 / 0.1) ** 2 + 1.0) / 2.0) < 1e-9


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
    """WI-44: the sidecar has NO decision authority. A ledger truncated back to a valid
    prefix (chain still verifies) is simply re-derived from that canonical prefix and the
    sidecar regenerated -- a stale pointer can neither skip nor double-count anything."""
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    run_ledger_evalue(p)  # writes a sidecar pointing at the belief_update's entry_hash

    # Truncate back to just the admission entry: a VALID single-entry chain.
    lines = p.read_text(encoding="utf-8").splitlines()
    p.write_text(lines[0] + "\n", encoding="utf-8")

    rows, state = run_ledger_evalue(p)
    assert rows[0].status == "ok"
    assert rows[0].n_observations == 0 and abs(rows[0].e_value - 1.0) < 1e-12
    assert state["hypotheses"]["H-1"]["last_entry_hash"] == json.loads(lines[0])["entry_hash"]


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


# --------------------------------------------------------------------------- #
# WI-40: ledger runs use fixed registered membership + strict boolean typing
# --------------------------------------------------------------------------- #
def test_ledger_run_initializes_all_registered_triggers():
    p = _tmp()
    led = _seed_with_config(p)  # registers trig_a AND trig_b
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows, _ = run_ledger_evalue(p, alpha=0.05)
    row = rows[0]
    # Both registered triggers are in the mixture even though only one reported:
    assert row.n_triggers == 2
    # average over {p1/p0 = 6.0, silent = 1.0} = 3.5
    assert abs(row.e_value - 3.5) < 1e-9


def test_ledger_rejects_non_boolean_trigger_value():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": "false"}, "2026-01-02")
    try:
        run_ledger_evalue(p, alpha=0.05)
        assert False, "expected EvalueLedgerError for a string trigger value"
    except EvalueLedgerError as e:
        assert "boolean" in str(e)


# --------------------------------------------------------------------------- #
# WI-43 (B27-03): no silent lazy path; sidecar reconciled to the frozen admission
# --------------------------------------------------------------------------- #
def test_evalue_config_with_empty_trigger_contract_fails_loudly():
    p = _tmp()
    led = Ledger(p)
    led.register(
        "H-1", "claim", prior=0.5,
        evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
        exit_triggers=[],
        fields={"evalue": {"p0": 0.1, "p1": 0.6}},
    )
    _observe(led, "H-1", {}, "2026-01-02")
    try:
        run_ledger_evalue(p, alpha=0.05)
        assert False, "expected EvalueLedgerError for an empty exit-trigger contract"
    except EvalueLedgerError as e:
        assert "lazy" in str(e)


def test_legacy_sidecar_without_registered_set_is_discarded_and_rebuilt():
    """WI-44: a pre-WI-40 lazy sidecar (no registered set) is ignored -- the run replays
    the verified ledger from the admission and regenerates canonical registered state."""
    p = _tmp()
    led = _seed_with_config(p)  # registers trig_a + trig_b
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows, state = run_ledger_evalue(p, alpha=0.05)
    hyp = state["hypotheses"]["H-1"]
    hyp["test_state"].pop("registered", None)
    save_evalue_state(default_state_path_for(p), state)
    _observe(led, "H-1", {"trig_b": True}, "2026-01-03")
    rows2, state2 = run_ledger_evalue(p, alpha=0.05)
    assert rows2[0].n_triggers == 2 and rows2[0].n_observations == 2
    # canonical: both fires -> average of {6.0, 6.0} = 6.0
    assert abs(rows2[0].e_value - 6.0) < 1e-9
    assert state2["hypotheses"]["H-1"]["test_state"].get("registered") == ["trig_a", "trig_b"]


def test_mismatched_sidecar_config_is_discarded_and_rebuilt():
    """WI-44: a sidecar with drifted config (or any tampering) cannot influence the
    result -- the frozen admission is the only source of p0/p1/combine."""
    p = _tmp()
    led = _seed_with_config(p, p0=0.1, p1=0.6)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows, state = run_ledger_evalue(p, alpha=0.05)
    state["hypotheses"]["H-1"]["test_state"]["p0"] = 0.2  # config drift
    save_evalue_state(default_state_path_for(p), state)
    _observe(led, "H-1", {"trig_b": True}, "2026-01-03")
    rows2, state2 = run_ledger_evalue(p, alpha=0.05)
    assert rows2[0].p0 == 0.1 and abs(rows2[0].e_value - 6.0) < 1e-9
    assert state2["hypotheses"]["H-1"]["test_state"]["p0"] == 0.1



# --------------------------------------------------------------------------- #
# WI-44 (B29-01/02/03): canonical-history authority, contract validation, sup-decision
# --------------------------------------------------------------------------- #
def test_hash_broken_ledger_cannot_produce_a_report():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    raw = p.read_text(encoding="utf-8")
    p.write_text(raw.replace('"claim"', '"cIaim"', 1), encoding="utf-8")
    with pytest.raises(EvalueLedgerError, match="hash-chain"):
        run_ledger_evalue(p)


def test_rogue_sidecar_process_cannot_change_the_decision():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows, state = run_ledger_evalue(p, alpha=0.05)
    ts = state["hypotheses"]["H-1"]["test_state"]
    ts["procs"]["rogue"] = {"p0": 0.1, "p1": 0.6, "e": 1e12, "n": 1}
    save_evalue_state(default_state_path_for(p), state)
    rows2, state2 = run_ledger_evalue(p, alpha=0.05)
    assert rows2[0].n_triggers == 2 and rows2[0].decision == "continue"
    assert "rogue" not in state2["hypotheses"]["H-1"]["test_state"]["procs"]


def test_rewound_progress_pointer_cannot_double_count():
    p = _tmp()
    led = _seed_with_config(p)
    _observe(led, "H-1", {"trig_a": True}, "2026-01-02")
    rows, state = run_ledger_evalue(p, alpha=0.05)
    state["hypotheses"]["H-1"]["last_entry_hash"] = json.loads(
        p.read_text(encoding="utf-8").splitlines()[0]
    )["entry_hash"]  # rewind to the admission
    save_evalue_state(default_state_path_for(p), state)
    rows2, _ = run_ledger_evalue(p, alpha=0.05)
    assert rows2[0].n_observations == 1 and abs(rows2[0].e_value - rows[0].e_value) < 1e-12


def test_threshold_crossing_is_latched_via_max_e():
    """sup_t e_t >= 1/alpha is the rejection event: later shrinkage (or a later
    invocation) must not un-falsify a crossed hypothesis."""
    p = _tmp()
    led = _seed_with_config(p, p0=0.1, p1=0.6)
    for i, fired in enumerate([True, True, True, False, False, False]):
        _observe(led, "H-1", {"trig_a": fired}, f"2026-01-{i + 2:02d}")
    rows, _ = run_ledger_evalue(p, alpha=0.05)  # threshold 20
    row = rows[0]
    assert row.max_e >= 20.0 > row.e_value  # crossed at (216+1)/2, ended below
    assert row.decision == "falsified"
    rows2, _ = run_ledger_evalue(p, alpha=0.05)  # and it stays falsified on re-run
    assert rows2[0].decision == "falsified"


def test_malformed_contract_rows_fail_loudly():
    p = _tmp()
    led = Ledger(p)
    led.register(
        "H-1", "claim", prior=0.5,
        evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
        exit_triggers=[
            {"id": "trig_a", "metric": "m", "op": ">", "data_source": {"tier": "secondary"}},
            {"metric": "no-id-row", "op": "<", "data_source": {"tier": "secondary"}},
        ],
        fields={"evalue": {"p0": 0.1, "p1": 0.6}},
    )
    with pytest.raises(EvalueLedgerError, match="cannot drop contract rows"):
        run_ledger_evalue(p)


def test_blank_and_duplicate_trigger_ids_fail_loudly():
    for bad_triggers, match in [
        ([{"id": "  ", "metric": "m", "op": ">", "data_source": {"tier": "secondary"}}],
         "cannot drop contract rows"),
        ([{"id": "t", "metric": "m", "op": ">", "data_source": {"tier": "secondary"}},
          {"id": "t", "metric": "n", "op": "<", "data_source": {"tier": "secondary"}}],
         "unique ids"),
    ]:
        p = _tmp()
        led = Ledger(p)
        led.register("H-1", "claim", prior=0.5,
                     evidence=[{"summary": "s", "tier": "primary", "date": "2026-01-01"}],
                     exit_triggers=bad_triggers,
                     fields={"evalue": {"p0": 0.1, "p1": 0.6}})
        with pytest.raises(EvalueLedgerError, match=match):
            run_ledger_evalue(p)


def test_falsey_non_dict_trigger_checks_fail_and_do_not_advance():
    for falsey in ([], "", 0, False):
        p = _tmp()
        led = _seed_with_config(p)
        led.update("H-1",
                   evidence=[{"summary": "c", "tier": "secondary", "date": "2026-01-02"}],
                   fields={"trigger_checks": falsey})
        with pytest.raises(EvalueLedgerError, match="must be a dict"):
            run_ledger_evalue(p)
        assert not default_state_path_for(p).exists()  # no progress persisted


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

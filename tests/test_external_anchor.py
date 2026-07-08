"""Tests for forward_qpop.anchor's external-anchor extension (WI-19).

The local anchor manifest (``build_manifest`` / ``verify_anchor``) commits to the ledger
head but supplies no timestamp of its own -- the *external* anchor is what turns that
manifest into a "registered before the outcome" proof, per the paper's Limitations section:

    "a full 'registered before the outcome' guarantee requires an external timestamp
    anchor: a signed Git commit or release, a public CI artifact, or a public append-only
    timestamp service (e.g. OpenTimestamps, or a Sigstore/Rekor transparency-log entry)."

This module exercises ``external_anchor`` / ``verify_external_anchor`` entirely against a
FAKE OTS backend (no network, no ``ots`` binary required) so the suite stays hermetic and
fast. A true-network round-trip test exists (``test_live_ots_roundtrip``) but is skipped
unless ``QPOP_TEST_LIVE_OTS=1`` is set, matching the CI design: required CI never depends
on an external service being reachable.
"""
import json
import os
import tempfile
from pathlib import Path

import pytest

from forward_qpop import Ledger, build_manifest, write_manifest
from forward_qpop.anchor import (
    ExternalAnchorError,
    external_anchor,
    external_anchor_path_for,
    verify_external_anchor,
)


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


class _FakeOTSBackend:
    """Stands in for the network call an OTS stamp submission makes.

    ``submit`` returns a receipt dict shaped like what ``external_anchor`` expects back
    from the real backend; ``fail`` (if set) makes ``submit`` raise, exercising the
    degradation path.
    """

    def __init__(self, fail: Exception = None, log_index: int = 42):
        self.fail = fail
        self.log_index = log_index
        self.calls = []

    def submit(self, digest_hex: str) -> dict:
        self.calls.append(digest_hex)
        if self.fail:
            raise self.fail
        return {
            "log_index": self.log_index,
            "calendar_urls": ["https://alice.btc.calendar.opentimestamps.org"],
            "receipt_b64": "ZmFrZS1vdHMtcmVjZWlwdA==",  # "fake-ots-receipt"
        }


def test_external_anchor_writes_sidecar_with_submitted_status():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    backend = _FakeOTSBackend()

    sidecar_path = external_anchor(p, method="ots", backend=backend)

    assert sidecar_path.exists()
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert sidecar["method"] == "ots"
    assert sidecar["service"]
    assert sidecar["status"] == "submitted"
    assert sidecar["submitted_at"]
    assert len(sidecar["digest_sha256"]) == 64
    assert backend.calls == [sidecar["digest_sha256"]]


def test_external_anchor_path_defaults_next_to_ledger():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    sidecar_path = external_anchor(p, method="ots", backend=_FakeOTSBackend())
    assert sidecar_path == external_anchor_path_for(p)
    assert sidecar_path.name == "ledger.jsonl.external-anchor.json"


def test_external_anchor_digest_matches_current_manifest_head():
    p = _tmp()
    _seed(p)
    m = write_manifest(p, manifest=build_manifest(p))
    backend = _FakeOTSBackend()
    sidecar_path = external_anchor(p, method="ots", backend=backend)
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    manifest = json.loads(m.read_text(encoding="utf-8"))
    assert sidecar["digest_sha256"] == manifest["head_entry_hash"]


def test_external_anchor_requires_local_manifest_first():
    p = _tmp()
    _seed(p)  # no write_manifest() call
    with pytest.raises(ExternalAnchorError, match="manifest"):
        external_anchor(p, method="ots", backend=_FakeOTSBackend())


def test_external_anchor_network_failure_is_loud_not_silent():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    backend = _FakeOTSBackend(fail=ConnectionError("calendar server unreachable"))

    with pytest.raises(ExternalAnchorError, match="unreachable"):
        external_anchor(p, method="ots", backend=backend)

    # No sidecar should be written, or if partially written, it must not claim success.
    sidecar_path = external_anchor_path_for(p)
    if sidecar_path.exists():
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
        assert sidecar["status"] != "submitted"
        assert sidecar["status"] != "confirmed"


def test_external_anchor_rejects_unknown_method():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    with pytest.raises(ExternalAnchorError, match="method"):
        external_anchor(p, method="carrier-pigeon", backend=_FakeOTSBackend())


def test_verify_external_anchor_ok_when_digest_matches_current_head():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    external_anchor(p, method="ots", backend=_FakeOTSBackend())

    res = verify_external_anchor(p)
    assert res.ok, res.problems
    assert any("digest" in c for c in res.checks)


def test_verify_external_anchor_detects_ledger_rewrite_after_submission():
    p = _tmp()
    led = _seed(p)
    write_manifest(p)
    external_anchor(p, method="ots", backend=_FakeOTSBackend())

    led.register("H-3", "c")  # ledger moved AFTER the external submission
    write_manifest(p)  # local manifest re-synced to new head...

    res = verify_external_anchor(p)  # ...but the external sidecar is now stale
    assert not res.ok
    assert any("digest" in prob for prob in res.problems)


def test_verify_external_anchor_missing_sidecar():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    res = verify_external_anchor(p)  # external_anchor() never called
    assert not res.ok
    assert any("external anchor" in x for x in res.problems)


def test_external_anchor_sidecar_records_service_and_time_fields():
    p = _tmp()
    _seed(p)
    write_manifest(p)
    sidecar_path = external_anchor(p, method="ots", backend=_FakeOTSBackend())
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    for key in ("schema", "method", "service", "submitted_at", "status", "digest_sha256"):
        assert key in sidecar, f"missing {key}"


@pytest.mark.skipif(
    os.environ.get("QPOP_TEST_LIVE_OTS") != "1",
    reason="live network test; set QPOP_TEST_LIVE_OTS=1 to run against the real OTS calendar servers",
)
def test_live_ots_roundtrip():
    """True network round-trip: only runs when explicitly opted in (env-gated).

    Requires the `ots` binary on PATH (``pip install forward-qpop[anchor]``). Not part of
    required CI -- calendar-server availability is out of this project's control, and CI
    determinism matters more than exercising the live network path on every push.
    """
    from forward_qpop.anchor import ots_available

    if not ots_available():
        pytest.skip("`ots` binary not on PATH")

    p = _tmp()
    _seed(p)
    write_manifest(p)
    sidecar_path = external_anchor(p, method="ots")  # real backend, real network call
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert sidecar["status"] == "submitted"

    res = verify_external_anchor(p)
    assert res.ok, res.problems


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    skipped = 0
    for fn in fns:
        try:
            fn()
            print("PASS", fn.__name__)
        except pytest.skip.Exception:
            skipped += 1
            print("SKIP", fn.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"\n{len(fns) - failed - skipped}/{len(fns)} passed ({skipped} skipped)")
    sys.exit(1 if failed else 0)

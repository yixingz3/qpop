"""The synthetic walkthrough must stay runnable — it is the paper's R1-17 artifact.

Executes examples/synthetic_walkthrough/run_walkthrough.py in a subprocess (as a
clean-clone reader would) and pins its load-bearing outputs: the threshold-marginal
satellite tier, the WI-40 fixed-membership trigger count, and the final PASS line.
Also validates the shipped candidate card against the released schema when
jsonschema is installed (same optional dependency as repro/validate_samples.py).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "synthetic_walkthrough" / "run_walkthrough.py"


def test_walkthrough_runs_clean_and_pins_its_numbers():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "confidence = 0.2113  ->  tier = satellite" in out
    assert "(n_triggers = 3)" in out          # WI-40 fixed membership, visibly
    assert "tamper demo: edited one frozen word -> verify fails" in out
    assert out.rstrip().endswith("WALKTHROUGH PASS")


def test_walkthrough_card_validates_against_released_schema():
    try:
        import jsonschema
    except ImportError:
        import pytest
        pytest.skip("jsonschema not installed (optional, as in repro/)")
    card = json.loads(
        (ROOT / "examples" / "synthetic_walkthrough" / "candidate_card.json")
        .read_text(encoding="utf-8")
    )
    schema = json.loads(
        (ROOT / "schemas" / "candidate_card.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(card, schema)

"""Schema tests for benchmarks/oar/: both v0 packs validate against the new schemas, the
harness report validates against oar_report.schema.json, and the pack format reuses the
released card/evidence/exit-trigger schemas verbatim (never redefines them).

Needs jsonschema (skipped if absent), matching tests/test_schemas.py's posture.
"""
import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")
from jsonschema import Draft202012Validator  # noqa: E402

from benchmarks.oar import list_packs, load_pack  # noqa: E402
from benchmarks.oar.harness import run_pack  # noqa: E402
from benchmarks.oar.loader import PACKS_DIR, SCHEMAS_DIR  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RELEASED_SCHEMAS = ROOT / "schemas"


def _load(p: Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _validator(schema_name: str) -> "Draft202012Validator":
    return Draft202012Validator(
        _load(SCHEMAS_DIR / schema_name), format_checker=Draft202012Validator.FORMAT_CHECKER
    )


def test_both_v0_packs_present():
    assert list_packs() == ["ai_supply_chain", "uranium"]


@pytest.mark.parametrize("pack_name", ["ai_supply_chain", "uranium"])
def test_domain_pack_json_validates(pack_name):
    pack = load_pack(pack_name, validate=False)
    errs = list(_validator("domain_pack.schema.json").iter_errors(pack.domain_pack))
    assert not errs, [e.message for e in errs]


@pytest.mark.parametrize("pack_name", ["ai_supply_chain", "uranium"])
def test_aggregate_results_json_validates(pack_name):
    pack = load_pack(pack_name, validate=False)
    errs = list(_validator("aggregate_results.schema.json").iter_errors(pack.aggregate_results))
    assert not errs, [e.message for e in errs]


@pytest.mark.parametrize("pack_name", ["ai_supply_chain", "uranium"])
def test_load_pack_default_validation_passes(pack_name):
    # load_pack(validate=True) is the default; it must not raise for either shipped pack.
    load_pack(pack_name)


@pytest.mark.parametrize("pack_name", ["ai_supply_chain", "uranium"])
def test_harness_report_validates_against_oar_report_schema(pack_name):
    report = run_pack(pack_name)
    errs = list(_validator("oar_report.schema.json").iter_errors(report))
    assert not errs, [e.message for e in errs]


def test_ai_supply_chain_has_ablation_uranium_does_not():
    assert load_pack("ai_supply_chain").has_ablation is True
    assert load_pack("uranium").has_ablation is False


def test_bad_pack_fails_validation(tmp_path):
    """A pack missing required fields must fail validation, not silently pass."""
    from benchmarks.oar.loader import PackValidationError, load_pack as _load_pack

    bad_dir = tmp_path / "packs" / "broken"
    bad_dir.mkdir(parents=True)
    (bad_dir / "domain_pack.json").write_text(json.dumps({"name": "broken"}), encoding="utf-8")
    (bad_dir / "aggregate_results.json").write_text(json.dumps({"domain": "broken"}), encoding="utf-8")

    with pytest.raises(PackValidationError):
        _load_pack("broken", packs_dir=tmp_path / "packs")


def test_pack_schemas_do_not_redefine_released_card_schemas():
    """The design doc (Sec 2) requires the pack format to REUSE the released
    candidate_card / evidence / exit_trigger / qpop_entry schemas verbatim, not redefine
    them. Assert the new OAR schemas carry no competing '$id' for those released schemas
    and that the released files still exist and load cleanly (the reuse target is real)."""
    released = [
        "candidate_card.schema.json",
        "evidence.schema.json",
        "exit_trigger.schema.json",
        "qpop_entry.schema.json",
    ]
    for name in released:
        schema = _load(RELEASED_SCHEMAS / name)
        assert schema["$id"].endswith(name)

    new_schema_ids = set()
    for p in SCHEMAS_DIR.glob("*.schema.json"):
        new_schema_ids.add(_load(p)["$id"])
    for name in released:
        released_id = _load(RELEASED_SCHEMAS / name)["$id"]
        assert released_id not in new_schema_ids, f"{name} must not be redefined under benchmarks/oar/schemas/"


def test_pack_dirs_ship_no_per_card_content():
    """No pack directory may contain a raw per-card candidate list (e.g. a .jsonl of
    cards) -- v0 is aggregate-only by design; only domain_pack.json/aggregate_results.json
    (and README.md) belong in a pack directory."""
    allowed = {"domain_pack.json", "aggregate_results.json", "README.md"}
    for pack_dir in PACKS_DIR.iterdir():
        if not pack_dir.is_dir():
            continue
        names = {p.name for p in pack_dir.iterdir()}
        assert names <= allowed, f"{pack_dir} ships unexpected files: {names - allowed}"

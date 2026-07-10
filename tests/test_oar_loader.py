"""Loader tests for benchmarks/oar/loader.py: pack discovery, load success/failure paths.
Hermetic -- only reads the two shipped fixture packs plus a throwaway tmp_path pack.
"""
import pytest

from benchmarks.oar.loader import DomainPack, PackNotFoundError, list_packs, load_pack


def test_list_packs_returns_both_v0_packs_sorted():
    assert list_packs() == ["ai_supply_chain", "uranium"]


def test_list_packs_empty_dir_returns_empty_list(tmp_path):
    assert list_packs(tmp_path / "does-not-exist") == []


@pytest.mark.parametrize("name", ["ai_supply_chain", "uranium"])
def test_load_pack_returns_domain_pack(name):
    pack = load_pack(name)
    assert isinstance(pack, DomainPack)
    assert pack.name == name
    assert pack.domain_pack["name"]
    assert pack.aggregate_results["domain"]


def test_load_pack_missing_name_raises():
    with pytest.raises(PackNotFoundError):
        load_pack("does_not_exist")


def test_load_pack_missing_required_file_raises(tmp_path):
    pack_dir = tmp_path / "packs" / "incomplete"
    pack_dir.mkdir(parents=True)
    (pack_dir / "domain_pack.json").write_text("{}", encoding="utf-8")
    # aggregate_results.json intentionally absent
    with pytest.raises(PackNotFoundError):
        load_pack("incomplete", packs_dir=tmp_path / "packs")


def test_load_pack_validate_false_skips_schema_check(tmp_path):
    pack_dir = tmp_path / "packs" / "anything"
    pack_dir.mkdir(parents=True)
    (pack_dir / "domain_pack.json").write_text('{"name": "x"}', encoding="utf-8")
    (pack_dir / "aggregate_results.json").write_text('{"domain": "x"}', encoding="utf-8")
    # Missing required fields, but validate=False must let it through.
    pack = load_pack("anything", packs_dir=tmp_path / "packs", validate=False)
    assert pack.domain_pack == {"name": "x"}

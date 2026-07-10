"""benchmarks/oar/loader.py — domain-pack loader (the "meta.domain profile" pattern,
OAR_BENCHMARK_DESIGN_WORKING.md Sec 2).

Reads a pack's ``domain_pack.json`` + ``aggregate_results.json`` and validates each
against ``benchmarks/oar/schemas/`` when ``jsonschema`` is installed -- a soft dependency,
matching the posture already documented in ``schemas/README.md`` for the rest of the repo
(``repro/validate_samples.py`` behaves the same way). Pure filesystem + JSON reads: no
network, no LLM calls.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

PACKS_DIR = Path(__file__).resolve().parent / "packs"
SCHEMAS_DIR = Path(__file__).resolve().parent / "schemas"


class PackNotFoundError(FileNotFoundError):
    """Raised when a named pack directory (or a required file inside it) doesn't exist."""


class PackValidationError(ValueError):
    """Raised when a pack's JSON fails its schema."""


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate(instance: dict, schema_name: str) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return  # soft dependency -- same posture as schemas/README.md / repro/validate_samples.py
    schema = _load_json(SCHEMAS_DIR / schema_name)
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise PackValidationError(f"{schema_name}: {msgs}")


@dataclass(frozen=True)
class DomainPack:
    name: str
    domain_pack: Dict[str, Any]
    aggregate_results: Dict[str, Any]

    @property
    def has_ablation(self) -> bool:
        """True for a pack whose aggregate_results carries an arms[] ablation batch
        (AI supply chain); False for a funnel-only demonstration pack (uranium)."""
        return "arms" in self.aggregate_results


def load_pack(name: str, *, validate: bool = True, packs_dir: Path = PACKS_DIR) -> DomainPack:
    """Load and (by default) schema-validate one named OAR domain pack."""
    pack_dir = packs_dir / name
    if not pack_dir.is_dir():
        raise PackNotFoundError(f"no such OAR domain pack: {name!r} (looked in {pack_dir})")

    domain_pack_path = pack_dir / "domain_pack.json"
    aggregate_results_path = pack_dir / "aggregate_results.json"
    if not domain_pack_path.is_file():
        raise PackNotFoundError(f"pack {name!r} is missing domain_pack.json")
    if not aggregate_results_path.is_file():
        raise PackNotFoundError(f"pack {name!r} is missing aggregate_results.json")

    domain_pack = _load_json(domain_pack_path)
    aggregate_results = _load_json(aggregate_results_path)

    if validate:
        _validate(domain_pack, "domain_pack.schema.json")
        _validate(aggregate_results, "aggregate_results.schema.json")

    return DomainPack(name=name, domain_pack=domain_pack, aggregate_results=aggregate_results)


def list_packs(packs_dir: Path = PACKS_DIR) -> List[str]:
    """Names of every pack directory under ``packs/`` (sorted, deterministic)."""
    if not packs_dir.is_dir():
        return []
    return sorted(p.name for p in packs_dir.iterdir() if p.is_dir())

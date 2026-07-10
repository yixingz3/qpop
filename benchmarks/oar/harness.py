"""benchmarks/oar/harness.py — the v0 ablation harness.

Reads a domain pack's *recorded* aggregates, computes OAR at a fixed admission budget,
rejection precision (raw + adjudicated), and admission rate per arm, and renders the
monotone discipline-curve as a text or JSON artifact (no plotting dependency).

Pure and offline by construction: it never makes a network call and never invokes an
LLM. v0 demonstrates the scoring math on the two domain packs' already-recorded aggregate
results (see ``packs/*/README.md`` for what is aggregate-only vs per-card, and the package
``README.md`` for the full privacy boundary).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .loader import DomainPack, list_packs, load_pack
from .scoring import (
    admission_rate_per_arm,
    assert_monotone_nonincreasing,
    discipline_curve,
    rejection_precision_from_aggregate,
)


def run_pack(name: str, *, validate: bool = True) -> Dict[str, Any]:
    """Compute the full OAR report for one pack. Returns a plain dict matching
    ``schemas/oar_report.schema.json``."""
    pack = load_pack(name, validate=validate)
    agg = pack.aggregate_results

    report: Dict[str, Any] = {
        "domain": pack.domain_pack["name"],
        "provenance": agg.get("provenance"),
        "aggregate_only": True,
    }

    if pack.has_ablation:
        curve = discipline_curve(agg)
        assert_monotone_nonincreasing(curve)
        report["discipline_curve"] = [
            {"arm": p.arm, "label": p.label, "admission_rate": p.admission_rate, "oar": p.oar}
            for p in curve
        ]
        report["admission_rate_per_arm"] = admission_rate_per_arm(agg["arms"])

    if agg.get("rejection_precision"):
        rp = rejection_precision_from_aggregate(agg["rejection_precision"])
        report["rejection_precision"] = {
            "raw_point": rp.raw_point,
            "raw_n": rp.raw_n,
            "raw_justified": rp.raw_justified,
            "raw_ci": list(rp.raw_ci) if rp.raw_ci else None,
            "adjudicated_point": rp.adjudicated_point,
            "adjudicated_n": rp.adjudicated_n,
            "adjudicated_upheld": rp.adjudicated_upheld,
        }

    if agg.get("funnel"):
        report["funnel"] = agg["funnel"]
    if agg.get("admission_rate"):
        report["admission_rate"] = agg["admission_rate"]

    return report


def render_text(report: Dict[str, Any]) -> str:
    """Render a report as a plain-text discipline-curve artifact (no plotting deps)."""
    lines = [
        f"OAR benchmark v0 -- domain: {report['domain']}",
        f"provenance: {report.get('provenance')}",
        "aggregate-only: true (no per-card content)",
        "",
    ]
    if "discipline_curve" in report:
        lines.append("discipline curve (least- to most-disciplined arm):")
        for p in report["discipline_curve"]:
            oar_s = f"{p['oar'] * 100:5.1f}%" if p["oar"] is not None else "  n/a"
            lines.append(
                f"  {p['arm']:<20} admit={p['admission_rate'] * 100:5.1f}%   OAR={oar_s}   {p['label']}"
            )
        lines.append("")
    if "rejection_precision" in report:
        rp = report["rejection_precision"]
        adj = (
            f"{rp['adjudicated_point']:.3f} (n={rp['adjudicated_n']}, upheld={rp['adjudicated_upheld']})"
            if rp["adjudicated_point"] is not None
            else "n/a"
        )
        lines.append(
            f"rejection precision: raw={rp['raw_point']:.3f} (n={rp['raw_n']}, "
            f"justified={rp['raw_justified']}, CI95={rp['raw_ci']})  |  adjudicated={adj}"
        )
        lines.append("")
    if "funnel" in report:
        lines.append("funnel (single run, no ablation arms -- see the pack README):")
        for k, v in report["funnel"].items():
            lines.append(f"  {k}: {json.dumps(v)}")
        lines.append("admission_rate:")
        for k, v in (report.get("admission_rate") or {}).items():
            lines.append(f"  {k}: {v * 100:.1f}%")
    return "\n".join(lines).rstrip() + "\n"


def render_json(report: Dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=False) + "\n"


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m benchmarks.oar.harness",
        description="OAR benchmark v0 harness -- offline, aggregate-fixture ablation report.",
    )
    parser.add_argument("pack", nargs="?", choices=list_packs() or None, help="domain pack name")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--out", type=Path, default=None, help="write the artifact to this path")
    parser.add_argument("--list", action="store_true", help="list available packs and exit")
    args = parser.parse_args(argv)

    if args.list or not args.pack:
        for name in list_packs():
            print(name)
        return 0

    report = run_pack(args.pack)
    text = render_json(report) if args.format == "json" else render_text(report)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        _write_stdout(text)
    return 0


def _write_stdout(text: str) -> None:
    """Write to stdout as UTF-8 regardless of the console's active codepage.

    A plain ``sys.stdout.write`` can raise ``UnicodeEncodeError`` on a non-UTF-8 console
    (e.g. a Windows terminal on a legacy codepage) the moment a report contains any
    non-ASCII character. ``reconfigure`` (Python >= 3.7) is a no-op on already-UTF-8
    streams, so this is safe everywhere.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())

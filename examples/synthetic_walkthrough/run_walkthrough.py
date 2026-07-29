#!/usr/bin/env python3
"""Synthetic end-to-end walkthrough — every ledger-side step, runnable offline.

Everything here is FICTIONAL (ZZNEO / "Synthetica Gas Works" do not exist); the
point is the METHOD: score decomposition -> tier -> falsifiable contract ->
pre-registration -> trigger checks -> sequential test -> anchor -> tamper check.
The scoring numbers come from ../..//src/scoring_rubric.md's anchors and are
derived in README.md; this script executes the steps a clean clone can actually
run (the public ledger/e-value/anchor mechanics -- the SOURCE/TRIAGE/EVALUATE
model stages are documented in src/prompts.md and are not executed here).

Usage:  python examples/synthetic_walkthrough/run_walkthrough.py
        (stdlib only; writes ledger + sidecars into a temp dir; exits 0 on success)
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from forward_qpop import Ledger, run_ledger_evalue, verify_file  # noqa: E402
from forward_qpop.anchor import build_manifest, verify_anchor, write_manifest  # noqa: E402

# ---- 1. Score decomposition (rubric anchors; derivation in README.md) --------
# SINGLE numeric source of truth for the walkthrough (the YAML carries structure
# only). Every value below IS a published anchor of the discrete reference rubric;
# straddles resolved to the LOWER fully supported anchor per the rubric's rule.
DIMS = {  # bottleneck_dims for the synthetic node
    "physical_indispensability": 0.7,  # anchor: route exists only w/ qualified redesign
    "substitutability_inv": 0.7,       # anchor: alternatives behind qualification barrier
    "capacity_lead_time": 0.7,         # anchor: 2-3 years incl. qualification
    "supplier_concentration": 0.9,     # anchor: 1-2 suppliers >=70% (two qualified OEMs)
    "pricing_power": 0.5,              # straddle->lower: episodic + one partial escalator clause
}
bottleneck = sum(DIMS.values()) / len(DIMS)          # reference definition: mean
# purity: 35% of revenue -> the 0.7 'major line (30-70%)' anchor, on-anchor.
# demand: booked capacity POs -> the 0.7 anchor verbatim.
# valuation: on-anchor 0.70 'rich; consensus already carries the thesis' (card evidence).
# crowding: known, not crowded -> the 0.85 anchor.
purity, demand, valuation, crowding = 0.7, 0.7, 0.70, 0.85
confidence = bottleneck * purity * demand * valuation * crowding
CORE, SATELLITE = 0.22, 0.10
tier = "core" if confidence >= CORE else "satellite" if confidence >= SATELLITE else "dropped"


def main() -> int:
    out = Path(tempfile.mkdtemp(prefix="qpop_walkthrough_"))
    ledger_path = out / "ledger.jsonl"
    print(f"working dir: {out}")
    print(f"bottleneck_score (mean of dims) = {bottleneck:.3f}")
    print(f"confidence = {confidence:.4f}  ->  tier = {tier} "
          f"(core >= {CORE}, satellite >= {SATELLITE})")
    assert tier == "satellite", "walkthrough expects the threshold-marginal satellite case"

    # ---- 2. Pre-register the admission: claim + dated evidence + triggers +
    #         frozen e-value commitment, hash-chained BEFORE any outcome window.
    led = Ledger(ledger_path)
    led.register(
        "H-NEON-01",
        "Qualified UHP neon reclaim-skid capacity stays binding through 2027; "
        "ZZNEO (FICTIONAL) captures it as one of two certified OEMs.",
        prior=0.55,
        evidence=[
            {"summary": "Reclaim segment 35% of revenue; booked capacity POs.",
             "tier": "primary", "date": "2026-02-15"},
            {"summary": "Fab operators on multi-quarter skid waitlists.",
             "tier": "secondary", "date": "2026-03-02"},
        ],
        exit_triggers=[
            {"id": "capacity_glut",
             "metric": "announced reclaim capacity additions vs installed base",
             "op": ">", "data_source": {"name": "capacity tracker", "tier": "secondary"}},
            {"id": "substitution_breakthrough",
             "metric": "qualified neon-free or low-neon laser platform",
             "op": "exists", "data_source": {"name": "litho OEM disclosures", "tier": "primary"}},
            {"id": "crowding_reversal",
             "metric": "price vs estimate-revision gap",
             "op": ">", "data_source": {"tier": "market_implied"}},
        ],
        fields={
            "evalue": {"p0": 0.10, "p1": 0.60, "combine": "average"},
            "decomposed_confidence": {
                "bottleneck_score": round(bottleneck, 3), "exposure_purity": purity,
                "demand_score": demand, "valuation_adjustment": valuation,
                "crowding_adjustment": crowding, "final_confidence": round(confidence, 4),
            },
            "tier": tier,
        },
    )
    print("registered H-NEON-01 (satellite, 3 falsifiable triggers, frozen e-value commitment)")

    # ---- 3. A monitoring step: dated belief update carrying trigger checks.
    led.update(
        "H-NEON-01",
        evidence=[{"summary": "Monthly check: no capacity glut, no substitution, "
                              "crowding gap inside 2 sigma.",
                   "tier": "secondary", "date": "2026-04-01"}],
        fields={"trigger_checks": {
            "capacity_glut": False,
            "substitution_breakthrough": False,
            "crowding_reversal": False,
        }},
    )
    print("belief update recorded (all three registered triggers checked: none fired)")

    # ---- 4. Sequential test over the ledger (registered fixed-membership mode).
    rows, _ = run_ledger_evalue(ledger_path, alpha=0.05)
    row = rows[0]
    assert row.n_triggers == 3, "all registered triggers must be in the mixture"
    print(f"evalue: e = {row.e_value:.4f} vs threshold {row.threshold:.1f} "
          f"-> {row.decision} (n_triggers = {row.n_triggers})")
    assert row.decision == "continue"

    # ---- 5. Anchor the ledger head and verify; then prove tamper-evidence.
    write_manifest(ledger_path, manifest=build_manifest(ledger_path))
    res = verify_anchor(ledger_path)
    assert res.ok, res.message
    print("anchor manifest written and verified (local; add --ots externally)")

    res_v = verify_file(ledger_path)
    assert res_v.ok, res_v.problems
    print(f"chain verify: OK -- {res_v.n_entries} entries")

    raw = ledger_path.read_text(encoding="utf-8")
    tampered = out / "tampered.jsonl"
    tampered.write_text(raw.replace("stays binding", "stays SUPER binding"), encoding="utf-8")
    res_t = verify_file(tampered)
    assert not res_t.ok, "tampered ledger must fail verification"
    print(f"tamper demo: edited one frozen word -> verify fails ({res_t.problems[0][:60]}...)")

    print("WALKTHROUGH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Discipline-curve reproduction tests: the ai_supply_chain pack's recorded aggregates must
reproduce the exact monotone ordering the design doc quotes (Sec 5):

    100% -> 74% -> 66% -> ~41% -> ~37% -> 0%
    (ungated -> -bear-case-first -> -overlap -> no-forward-lock -> debate-only -> full pipeline)

and the harness must render that as a text/JSON artifact with no plotting dependency.
"""
import json

import pytest

from benchmarks.oar import load_pack
from benchmarks.oar.harness import render_json, render_text, run_pack
from benchmarks.oar.scoring import assert_monotone_nonincreasing, discipline_curve


def test_discipline_curve_reproduces_the_recorded_ordering():
    pack = load_pack("ai_supply_chain")
    curve = discipline_curve(pack.aggregate_results)
    names = [p.arm for p in curve]
    assert names == [
        "ungated_screener",
        "no_bear_case_first",
        "no_overlap_penalty",
        "no_forward_lock",
        "debate_only",
        "full_pipeline",
    ]
    rates_pct = [round(p.admission_rate * 100) for p in curve]
    assert rates_pct == [100, 74, 66, 41, 37, 0]


def test_discipline_curve_is_monotone_nonincreasing():
    pack = load_pack("ai_supply_chain")
    curve = discipline_curve(pack.aggregate_results)
    assert_monotone_nonincreasing(curve)  # must not raise


def test_discipline_curve_oar_equals_admission_rate_against_zero_reference():
    # Every non-reference arm's OAR must equal its own admission rate (the reference
    # admitted 0/38 -- see scoring.oar_from_aggregate_zero_reference's docstring).
    pack = load_pack("ai_supply_chain")
    curve = discipline_curve(pack.aggregate_results)
    for point in curve:
        if point.arm == "full_pipeline":
            assert point.oar == 0.0
        else:
            assert point.oar == pytest.approx(point.admission_rate)


def test_discipline_curve_raises_for_a_pack_without_ablation_arms():
    pack = load_pack("uranium")
    with pytest.raises(KeyError):
        discipline_curve(pack.aggregate_results)


def test_uranium_report_has_no_discipline_curve():
    report = run_pack("uranium")
    assert "discipline_curve" not in report
    assert "funnel" in report
    assert report["funnel"]["sourced"] == 20


def test_harness_text_artifact_contains_the_canonical_percentages():
    # Exact rendered rates (28/38=73.7%, 25/38=65.8%, mean(14,17)/38=40.8%, mean(15,13)/38=36.8%)
    # -- the design doc's "74% / 66% / ~41% / ~37%" are the rounded headline figures; see
    # test_discipline_curve_reproduces_the_recorded_ordering for that rounded reproduction.
    report = run_pack("ai_supply_chain")
    text = render_text(report)
    for pct in ("100.0%", "73.7%", "65.8%", "40.8%", "36.8%", "0.0%"):
        assert pct in text, f"expected {pct!r} in discipline-curve artifact:\n{text}"
    assert "full_pipeline" in text
    assert "ungated_screener" in text


def test_harness_json_artifact_round_trips():
    report = run_pack("ai_supply_chain")
    text = render_json(report)
    round_tripped = json.loads(text)
    assert round_tripped == report

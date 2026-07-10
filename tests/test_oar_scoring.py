"""Scorer-math tests for benchmarks/oar/scoring.py, on hand-computable fixtures.

No pack loading here (see test_oar_loader.py / test_oar_discipline_curve.py for that) --
this file exercises the pure scoring functions directly against inputs small enough to
verify by hand, per the project's test-discipline note (smallest input that still
exercises the property under test).
"""
import pytest

from benchmarks.oar.scoring import (
    OARResult,
    admission_rate_per_arm,
    arm_admission_rate,
    assert_monotone_nonincreasing,
    compute_oar,
    oar_from_aggregate_zero_reference,
    wilson_score_interval,
)
from benchmarks.oar.scoring import DisciplineCurvePoint


# ---------- arm_admission_rate ----------


def test_arm_admission_rate_single_replicate():
    assert arm_admission_rate({"admitted": 25, "total": 38}) == pytest.approx(25 / 38)


def test_arm_admission_rate_multi_replicate_is_mean_of_rates():
    # 14/38 and 17/38 -> mean = (0.368421... + 0.447368...) / 2
    rate = arm_admission_rate({"admitted_replicates": [14, 17], "total": 38})
    expected = (14 / 38 + 17 / 38) / 2
    assert rate == pytest.approx(expected)
    assert rate == pytest.approx(0.4079, abs=1e-3)  # "~41%" as reported in RESULTS_V2_WORKING.md


def test_arm_admission_rate_rejects_zero_total():
    with pytest.raises(ValueError):
        arm_admission_rate({"admitted": 0, "total": 0})


def test_arm_admission_rate_requires_admitted_or_replicates():
    with pytest.raises(ValueError):
        arm_admission_rate({"total": 10})


def test_admission_rate_per_arm_maps_every_arm():
    arms = [{"arm": "a", "admitted": 2, "total": 4}, {"arm": "b", "admitted": 1, "total": 4}]
    rates = admission_rate_per_arm(arms)
    assert rates == {"a": 0.5, "b": 0.25}


# ---------- compute_oar (general, per-card) ----------


def test_compute_oar_hand_computable_example():
    # 4-card fixture: arm admits cards 1,2,3; the disciplined reference admits only card 1.
    # Reference rejects 2,3,4 -> arm's admits {1,2,3} intersect rejects {2,3,4} = {2,3}.
    # OAR is normalized by the FIXED set size (4), not the arm's own admit count (3):
    # OAR = |over-admitted| / |fixed set| = 2 / 4 = 0.5.
    arm = {"c1": True, "c2": True, "c3": True, "c4": False}
    reference = {"c1": True, "c2": False, "c3": False, "c4": False}
    result = compute_oar(arm, reference)
    assert isinstance(result, OARResult)
    assert result.admitted == 3
    assert result.over_admitted == 2
    assert result.total == 4
    assert result.oar == pytest.approx(2 / 4)


def test_compute_oar_arm_admits_nothing_is_oar_zero():
    arm = {"c1": False, "c2": False}
    reference = {"c1": True, "c2": False}
    result = compute_oar(arm, reference)
    assert result.oar == 0.0
    assert result.admitted == 0


def test_compute_oar_zero_reference_matches_aggregate_reduction():
    # When the reference admits nothing, compute_oar and the aggregate reduction must agree.
    arm = {f"c{i}": (i < 25) for i in range(38)}  # 25 admits, matching -overlap-penalty arm
    reference = {f"c{i}": False for i in range(38)}  # full pipeline: 0/38
    per_card = compute_oar(arm, reference)
    aggregate = oar_from_aggregate_zero_reference(25, 38, 0, 38)
    assert per_card.oar == pytest.approx(aggregate)
    # every one of the 25 admits is over-admission vs an empty reference, so over_admitted == 25;
    # OAR is that count normalized by the FIXED set size (38), i.e. the arm's own admission rate.
    assert per_card.over_admitted == 25
    assert per_card.oar == pytest.approx(25 / 38)


def test_compute_oar_requires_identical_card_sets():
    with pytest.raises(ValueError):
        compute_oar({"c1": True}, {"c1": True, "c2": False})


# ---------- oar_from_aggregate_zero_reference ----------


def test_oar_from_aggregate_zero_reference_ai_supply_chain_arms():
    # Every ablated arm's OAR equals its own admission rate against the 0/38 reference.
    assert oar_from_aggregate_zero_reference(38, 38, 0, 38) == pytest.approx(1.0)
    assert oar_from_aggregate_zero_reference(28, 38, 0, 38) == pytest.approx(28 / 38)
    assert oar_from_aggregate_zero_reference(25, 38, 0, 38) == pytest.approx(25 / 38)


def test_oar_from_aggregate_zero_reference_rejects_mismatched_totals():
    with pytest.raises(ValueError):
        oar_from_aggregate_zero_reference(10, 20, 0, 38)


def test_oar_from_aggregate_zero_reference_rejects_nonzero_reference():
    with pytest.raises(ValueError):
        oar_from_aggregate_zero_reference(10, 38, 1, 38)


# ---------- wilson_score_interval (reproduces the published H5 CIs) ----------


def test_wilson_interval_reproduces_published_n40_ci():
    # RESULTS_V2_WORKING.md: raw precision 31/40 = 0.775, Wilson [0.625, 0.877]
    lo, hi = wilson_score_interval(31, 40)
    assert lo == pytest.approx(0.625, abs=5e-3)
    assert hi == pytest.approx(0.877, abs=5e-3)


def test_wilson_interval_reproduces_published_n14_ci():
    # RESULTS_V2_WORKING.md: pilot precision 13/14 ~= 0.93, Wilson [0.69, 0.99]
    lo, hi = wilson_score_interval(13, 14)
    assert lo == pytest.approx(0.69, abs=5e-3)
    assert hi == pytest.approx(0.99, abs=5e-3)


def test_wilson_interval_bounds_are_valid_probabilities():
    lo, hi = wilson_score_interval(9, 9)  # 100% -- adjudicated precision
    assert 0.0 <= lo <= hi <= 1.0


def test_wilson_interval_rejects_bad_inputs():
    with pytest.raises(ValueError):
        wilson_score_interval(5, 0)
    with pytest.raises(ValueError):
        wilson_score_interval(-1, 10)
    with pytest.raises(ValueError):
        wilson_score_interval(11, 10)


# ---------- monotonicity guard ----------


def test_assert_monotone_nonincreasing_passes_on_decreasing_sequence():
    points = [
        DisciplineCurvePoint("a", "a", 1.0, None),
        DisciplineCurvePoint("b", "b", 0.5, None),
        DisciplineCurvePoint("c", "c", 0.0, None),
    ]
    assert_monotone_nonincreasing(points)  # must not raise


def test_assert_monotone_nonincreasing_flags_an_increase():
    points = [
        DisciplineCurvePoint("a", "a", 0.5, None),
        DisciplineCurvePoint("b", "b", 0.9, None),
    ]
    with pytest.raises(ValueError):
        assert_monotone_nonincreasing(points)

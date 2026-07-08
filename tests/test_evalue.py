"""Tests for forward_qpop.evalue — the anytime-valid sequential trigger test.

Runs under pytest, or standalone (``python tests/test_evalue.py``) with no third-party
dependencies — set ``PYTHONPATH=src`` if the package is not installed.

The properties under test:

* **Type-I control (the headline)** — under the null (fire prob = p0), across many
  simulated monitoring paths *with optional stopping*, the empirical rate of a false
  ``"falsified"`` call is <= alpha. This is the Ville-inequality guarantee.
* **Power sanity** — under a true alternative (fire prob well above p0) the test does
  eventually falsify.
* **Supermartingale spot-check** — the mean e-value under the null at a fixed horizon
  is <= 1 (E[e] <= 1), the algebraic fact that makes Ville's inequality apply.
* **Combination behaviour** — product vs. average combiners behave as documented
  (product is larger under a shared true signal; average is the dependence-safe default).
* **State round-trip** — a test's state serializes to a plain dict and restores exactly,
  so the ledger can persist per-entry e-process state.

Kept fast: modest path counts, small horizons (the 15s per-test cap still applies).
"""
import random

from forward_qpop.evalue import (
    EProcess,
    SequentialTriggerTest,
    average_evalues,
    product_evalues,
)


# --------------------------------------------------------------------------- #
# EProcess: the single-trigger betting martingale
# --------------------------------------------------------------------------- #
def test_eprocess_starts_at_one():
    ep = EProcess(p0=0.1, p1=0.5)
    assert ep.e_value() == 1.0
    assert ep.n == 0


def test_eprocess_likelihood_ratio_update():
    # One fired obs multiplies e by p1/p0; one not-fired by (1-p1)/(1-p0).
    ep = EProcess(p0=0.1, p1=0.5)
    ep.observe(True)
    assert abs(ep.e_value() - (0.5 / 0.1)) < 1e-12
    ep.observe(False)
    assert abs(ep.e_value() - (0.5 / 0.1) * (0.5 / 0.9)) < 1e-12
    assert ep.n == 2


def test_eprocess_all_not_fired_shrinks():
    # If the trigger never fires, evidence against the thesis-holds null never builds.
    ep = EProcess(p0=0.1, p1=0.5)
    for _ in range(20):
        ep.observe(False)
    assert ep.e_value() < 1.0


# --------------------------------------------------------------------------- #
# Combiners
# --------------------------------------------------------------------------- #
def test_product_and_average_of_ones_are_one():
    assert product_evalues([1.0, 1.0, 1.0]) == 1.0
    assert average_evalues([1.0, 1.0, 1.0]) == 1.0


def test_product_ge_average_when_all_large():
    es = [4.0, 5.0, 6.0]
    assert product_evalues(es) > average_evalues(es)


def test_empty_combination_is_one():
    assert product_evalues([]) == 1.0
    assert average_evalues([]) == 1.0


# --------------------------------------------------------------------------- #
# SequentialTriggerTest: decisions
# --------------------------------------------------------------------------- #
def test_decision_continue_then_falsified():
    st = SequentialTriggerTest(p0=0.1, p1=0.6, combine="product")
    assert st.decision(alpha=0.05) == "continue"
    # Feed a stream of fires on one trigger — evidence against "thesis holds" mounts.
    for _ in range(12):
        st.observe("trig_a", True)
    assert st.e_value() >= 1.0 / 0.05
    assert st.decision(alpha=0.05) == "falsified"


def test_default_combiner_is_average():
    st = SequentialTriggerTest(p0=0.1, p1=0.5)
    assert st.combine == "average"


def test_unknown_trigger_ids_tracked_independently():
    st = SequentialTriggerTest(p0=0.1, p1=0.5, combine="average")
    st.observe("a", True)
    st.observe("b", False)
    st.observe("a", True)
    # Two distinct e-processes exist; the average reflects both.
    assert set(st.trigger_ids()) == {"a", "b"}


# --------------------------------------------------------------------------- #
# (a) Type-I control by simulation — the load-bearing test
# --------------------------------------------------------------------------- #
def _run_null_path(rng, p0, p1, alpha, n_triggers, horizon, combine):
    """Monitor n_triggers under the null (fire prob = p0) for up to `horizon` steps,
    stopping early ('optional stopping') the instant the test would call falsified.
    Return True iff a false 'falsified' call occurred anywhere along the path."""
    st = SequentialTriggerTest(p0=p0, p1=p1, combine=combine)
    ids = [f"t{i}" for i in range(n_triggers)]
    for _ in range(horizon):
        for tid in ids:
            st.observe(tid, rng.random() < p0)
        if st.decision(alpha) == "falsified":
            return True
    return False


def test_type_i_control_average_combiner():
    # Under the null, the false-falsify rate across many optional-stopping paths
    # must not exceed alpha (Ville's inequality). Averaging combiner (the default).
    rng = random.Random(20260707)
    alpha = 0.10
    p0, p1 = 0.15, 0.6
    n_paths = 400
    false_calls = sum(
        _run_null_path(rng, p0, p1, alpha, n_triggers=4, horizon=60, combine="average")
        for _ in range(n_paths)
    )
    rate = false_calls / n_paths
    # Anytime-valid guarantee: rate <= alpha. Allow a thin Monte-Carlo margin.
    assert rate <= alpha + 0.03, f"false-falsify rate {rate:.3f} exceeds alpha {alpha}"


def test_type_i_control_product_combiner():
    # Same guarantee holds for the product combiner (each e-process is a
    # supermartingale; independent product is too).
    rng = random.Random(11111)
    alpha = 0.10
    p0, p1 = 0.15, 0.6
    n_paths = 400
    false_calls = sum(
        _run_null_path(rng, p0, p1, alpha, n_triggers=4, horizon=60, combine="product")
        for _ in range(n_paths)
    )
    rate = false_calls / n_paths
    assert rate <= alpha + 0.03, f"false-falsify rate {rate:.3f} exceeds alpha {alpha}"


# --------------------------------------------------------------------------- #
# (b) Power sanity — under a true alternative the test falsifies
# --------------------------------------------------------------------------- #
def test_power_under_alternative():
    # If the trigger truly fires at p1 (the thesis is wrong), the test should
    # falsify on the large majority of paths within the horizon.
    rng = random.Random(2024)
    alpha = 0.10
    p0, p1 = 0.15, 0.6
    n_paths = 100
    detected = 0
    for _ in range(n_paths):
        st = SequentialTriggerTest(p0=p0, p1=p1, combine="average")
        for _ in range(80):
            st.observe("t0", rng.random() < p1)  # fires at the ALTERNATIVE rate
            if st.decision(alpha) == "falsified":
                detected += 1
                break
    power = detected / n_paths
    assert power > 0.8, f"power {power:.2f} too low under a true alternative"


# --------------------------------------------------------------------------- #
# (c) Supermartingale spot-check — E[e] <= 1 under the null at a fixed horizon
# --------------------------------------------------------------------------- #
def test_supermartingale_mean_under_null():
    rng = random.Random(777)
    p0, p1 = 0.2, 0.5
    horizon = 25
    n_paths = 3000
    total = 0.0
    for _ in range(n_paths):
        ep = EProcess(p0=p0, p1=p1)
        for _ in range(horizon):
            ep.observe(rng.random() < p0)  # fire at the NULL rate
        total += ep.e_value()
    mean_e = total / n_paths
    # A likelihood-ratio e-process is a *martingale* under the null: E[e] == 1.
    # Allow a Monte-Carlo band around 1; the load-bearing direction is E[e] <~ 1.
    assert 0.85 <= mean_e <= 1.15, f"mean e-value {mean_e:.3f} not ~1 under null"


# --------------------------------------------------------------------------- #
# (d) Averaging-vs-product combination behaviour
# --------------------------------------------------------------------------- #
def test_average_is_dependence_safe_vs_product():
    # Two triggers driven by the SAME underlying observation (perfect dependence):
    # the product double-counts the evidence; the average does not.
    st_prod = SequentialTriggerTest(p0=0.1, p1=0.6, combine="product")
    st_avg = SequentialTriggerTest(p0=0.1, p1=0.6, combine="average")
    for _ in range(6):
        fired = True  # identical stream to both triggers -> perfectly dependent
        for st in (st_prod, st_avg):
            st.observe("a", fired)
            st.observe("b", fired)
    # Product > average here: that inflation is exactly why averaging is the
    # dependence-safe default for correlated triggers.
    assert st_prod.e_value() > st_avg.e_value()


# --------------------------------------------------------------------------- #
# (e) State round-trip serialization
# --------------------------------------------------------------------------- #
def test_state_roundtrip_preserves_evalue_and_decision():
    st = SequentialTriggerTest(p0=0.12, p1=0.55, combine="average")
    for tid, fired in [("a", True), ("b", False), ("a", True), ("c", True)]:
        st.observe(tid, fired)
    state = st.to_state()
    # State must be plain JSON-serializable data (dict of primitives / dicts).
    import json

    round = json.loads(json.dumps(state))
    restored = SequentialTriggerTest.from_state(round)
    assert abs(restored.e_value() - st.e_value()) < 1e-12
    assert restored.decision(0.05) == st.decision(0.05)
    assert set(restored.trigger_ids()) == set(st.trigger_ids())
    # Continuing from restored state matches continuing the original.
    st.observe("a", True)
    restored.observe("a", True)
    assert abs(restored.e_value() - st.e_value()) < 1e-12


def test_eprocess_state_roundtrip():
    ep = EProcess(p0=0.2, p1=0.5)
    for f in [True, False, True, True, False]:
        ep.observe(f)
    ep2 = EProcess.from_state(ep.to_state())
    assert ep2.e_value() == ep.e_value()
    assert ep2.n == ep.n
    assert ep2.p0 == ep.p0 and ep2.p1 == ep.p1


# --------------------------------------------------------------------------- #
# Guardrails on registration parameters
# --------------------------------------------------------------------------- #
def test_invalid_p0_p1_rejected():
    for bad in [
        dict(p0=0.0, p1=0.5),   # p0 must be in (0,1)
        dict(p0=0.5, p1=0.5),   # p1 must be > p0
        dict(p0=0.6, p1=0.5),   # p1 must be > p0
        dict(p0=0.1, p1=1.0),   # p1 must be < 1
    ]:
        try:
            EProcess(**bad)
            raise AssertionError(f"expected ValueError for {bad}")
        except ValueError:
            pass


def test_invalid_combine_rejected():
    try:
        SequentialTriggerTest(p0=0.1, p1=0.5, combine="median")
        raise AssertionError("expected ValueError for unknown combiner")
    except ValueError:
        pass


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print("PASS", fn.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", fn.__name__, "->", repr(exc))
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)

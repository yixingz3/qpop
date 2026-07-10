"""benchmarks/oar/scoring.py — pure, dependency-free scoring functions for the OAR
(over-admission rate) benchmark (OAR_BENCHMARK_DESIGN_WORKING.md Sec 5).

Everything here is a pure function over plain dicts/mappings: no network, no LLM calls,
no filesystem access (that's ``loader.py``'s job). Two APIs are provided for OAR itself:

* :func:`compute_oar` — the **general**, per-card formula. It needs a per-card admit/reject
  decision for both the arm under test and the disciplined reference, on the identical
  candidate set (the "fixed admission budget" requirement). This is the form a future
  domain pack with real per-card labels (v0.5's constructed/perturbed sets) will use.
* :func:`oar_from_aggregate_zero_reference` — the **aggregate-only** reduction that applies
  to the v0 AI-supply-chain pack, where the reference (full pipeline) admitted literally
  0 of 38 candidates. When the reference's admitted set is empty, its rejected set is the
  *entire* pool, so every card any ablated arm admits is, by definition, an over-admission
  -- OAR collapses to the arm's own admission rate. The function still asserts the
  precondition explicitly rather than silently assuming it, so it fails loudly if handed
  a pack where the reference admitted anything (that case needs per-card membership, not
  just a count, to know which specific admits actually overlap).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

# The canonical v0 discipline-curve ordering, least- to most-disciplined arm
# (OAR_BENCHMARK_DESIGN_WORKING.md Sec 5: "100% -> 74% -> 66% -> ~41% -> ~37% -> 0%").
DISCIPLINE_CURVE_ORDER: Tuple[str, ...] = (
    "ungated_screener",
    "no_bear_case_first",
    "no_overlap_penalty",
    "no_forward_lock",
    "debate_only",
    "full_pipeline",
)


# ---------- admission rate ----------


def arm_admission_rate(arm: Mapping) -> float:
    """Admission rate for one recorded arm entry (an ``arms[]`` element of
    ``aggregate_results.json``). Handles both a single-replicate arm
    (``{"admitted": int, "total": int}``) and a multi-replicate arm
    (``{"admitted_replicates": [int, ...], "total": int}``) by averaging the
    per-replicate rate.
    """
    total = arm["total"]
    if total <= 0:
        raise ValueError("arm 'total' must be positive")
    if "admitted" in arm:
        return arm["admitted"] / total
    reps = arm.get("admitted_replicates")
    if not reps:
        raise ValueError("arm must carry either 'admitted' or 'admitted_replicates'")
    return sum(r / total for r in reps) / len(reps)


def admission_rate_per_arm(arms: Sequence[Mapping]) -> Dict[str, float]:
    """``{arm_name: admission_rate}`` for every arm in an ``arms[]`` list."""
    return {arm["arm"]: arm_admission_rate(arm) for arm in arms}


# ---------- OAR (over-admission rate) ----------


@dataclass(frozen=True)
class OARResult:
    oar: float
    admitted: int
    over_admitted: int
    total: int


def compute_oar(
    arm_decisions: Mapping[str, bool], reference_decisions: Mapping[str, bool]
) -> OARResult:
    """General, per-card OAR.

    ``arm_decisions`` / ``reference_decisions`` map ``card_id -> admitted (bool)``. Both
    must cover the identical card-id set -- the "same set / fixed admission budget"
    requirement (design doc Sec 5): OAR is only meaningful when both the arm and the
    reference were scored on the exact same candidates, same model id, same temperature.

    OAR = |admits by the arm that the reference would reject| / |the fixed candidate set|.

    The denominator is the fixed candidate-set size (the "admission budget"), **not** the
    arm's own admit count. This is deliberate, not incidental: normalizing by the arm's own
    (variable) admit count would let an arm trivially drive its OAR toward 0 by admitting
    almost nothing -- exactly the gaming the design doc calls out ("fixing the admission
    budget prevents gaming by trivially admitting nothing"). Normalizing by the fixed total
    instead means OAR is always "what fraction of the whole evaluated set did this pipeline
    wrongly let through," independent of how conservatively or liberally it admits.
    """
    if set(arm_decisions) != set(reference_decisions):
        raise ValueError(
            "OAR requires the arm and reference to be scored on the identical card set "
            "(the 'fixed admission budget' requirement)"
        )
    admitted_by_arm = {cid for cid, admitted in arm_decisions.items() if admitted}
    rejected_by_reference = {cid for cid, admitted in reference_decisions.items() if not admitted}
    over_admitted = admitted_by_arm & rejected_by_reference
    total = len(arm_decisions)
    oar = (len(over_admitted) / total) if total else 0.0
    return OARResult(
        oar=oar,
        admitted=len(admitted_by_arm),
        over_admitted=len(over_admitted),
        total=total,
    )


def oar_from_aggregate_zero_reference(
    arm_admitted: float, arm_total: int, reference_admitted: int, reference_total: int
) -> float:
    """Aggregate-only OAR, valid ONLY when the reference's admitted **count** is exactly 0
    on the identical fixed set (``arm_total == reference_total``).

    When the reference admitted 0, its rejected set is the entire pool, so any card the
    arm admits is by definition an over-admission -- OAR reduces to the arm's own admission
    rate (``arm_admitted / arm_total``). This is exactly the shape of the AI-supply-chain
    38-card pilot batch (full pipeline: 0/38 admitted).

    Raises ``ValueError`` if the precondition doesn't hold: a reference that admitted
    *anything* needs per-card membership (:func:`compute_oar`), not a bare count, to know
    which specific admits actually overlap.
    """
    if arm_total != reference_total:
        raise ValueError("arm and reference must be scored on the identical fixed set (same total)")
    if reference_admitted != 0:
        raise ValueError(
            "aggregate-only OAR needs per-card decisions when the reference admitted > 0 "
            "(the count alone can't tell you WHICH cards overlap); use compute_oar instead"
        )
    return arm_admitted / arm_total if arm_total else 0.0


# ---------- rejection precision (raw + adjudicated) ----------


@dataclass(frozen=True)
class RejectionPrecision:
    raw_point: float
    raw_n: int
    raw_justified: int
    raw_ci: Optional[Tuple[float, float]]
    adjudicated_point: Optional[float]
    adjudicated_n: Optional[int]
    adjudicated_upheld: Optional[int]


def rejection_precision_from_aggregate(block: Mapping) -> RejectionPrecision:
    """Read the raw + adjudicated rejection-precision figures straight from a pack's
    ``aggregate_results.json["rejection_precision"]`` block. Raw is primary; adjudicated
    is a secondary resolution figure and must never be reported as if it were the headline
    (the H5 discipline -- design doc Sec 2/5).
    """
    raw = block["raw"]
    adjud = block.get("adjudicated")
    raw_ci = tuple(raw["wilson_ci_95"]) if "wilson_ci_95" in raw else None
    return RejectionPrecision(
        raw_point=raw["point_estimate"],
        raw_n=raw["n"],
        raw_justified=raw["justified"],
        raw_ci=raw_ci,
        adjudicated_point=adjud["point_estimate"] if adjud else None,
        adjudicated_n=adjud["n"] if adjud else None,
        adjudicated_upheld=adjud["upheld"] if adjud else None,
    )


def wilson_score_interval(successes: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """The Wilson score confidence interval for a binomial proportion.

    Used here to sanity-check (not compute for the first time) the published raw
    rejection-precision CIs -- see ``research/docs/RESULTS_V2_WORKING.md``'s H5 section,
    which reports Wilson intervals for both the n=14 pilot and the n=40 documented draw.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0 <= successes <= n):
        raise ValueError("successes must be within [0, n]")
    phat = successes / n
    z2 = z * z
    denom = 1 + z2 / n
    center = (phat + z2 / (2 * n)) / denom
    margin = (z * math.sqrt(phat * (1 - phat) / n + z2 / (4 * n * n))) / denom
    lo, hi = center - margin, center + margin
    return (max(0.0, lo), min(1.0, hi))


# ---------- discipline curve ----------


@dataclass(frozen=True)
class DisciplineCurvePoint:
    arm: str
    label: str
    admission_rate: float
    oar: Optional[float]


def discipline_curve(aggregate_results: Mapping) -> List[DisciplineCurvePoint]:
    """Reproduce the canonical, monotone discipline curve (design doc Sec 5) from a pack's
    recorded ``aggregate_results.json``. Requires all six :data:`DISCIPLINE_CURVE_ORDER`
    arms to be present; raises otherwise (this pack has no ablation to report -- e.g.
    uranium -- and should not call this function).
    """
    arms_by_name = {a["arm"]: a for a in aggregate_results["arms"]}
    missing = [name for name in DISCIPLINE_CURVE_ORDER if name not in arms_by_name]
    if missing:
        raise ValueError(f"aggregate_results is missing canonical arm(s): {missing}")

    reference_name = aggregate_results["reference_arm"]
    reference = arms_by_name[reference_name]
    reference_total = reference["total"]
    reference_admitted = reference.get("admitted")

    points: List[DisciplineCurvePoint] = []
    for name in DISCIPLINE_CURVE_ORDER:
        arm = arms_by_name[name]
        rate = arm_admission_rate(arm)
        oar: Optional[float] = None
        if reference_admitted == 0 and arm["total"] == reference_total:
            if name == reference_name:
                oar = 0.0  # the reference can't over-admit relative to itself
            else:
                oar = oar_from_aggregate_zero_reference(
                    rate * arm["total"], arm["total"], 0, reference_total
                )
        points.append(
            DisciplineCurvePoint(arm=name, label=arm.get("label", name), admission_rate=rate, oar=oar)
        )
    return points


def assert_monotone_nonincreasing(points: Sequence[DisciplineCurvePoint], tol: float = 1e-9) -> None:
    """Raise if the discipline curve's admission rates are not monotone non-increasing in
    :data:`DISCIPLINE_CURVE_ORDER` -- the qualitative reliability signature the design doc
    calls for (Sec 5): each additional discipline should not *raise* admission.
    """
    rates = [p.admission_rate for p in points]
    for prev, cur in zip(rates, rates[1:]):
        if cur > prev + tol:
            raise ValueError(f"discipline curve is not monotone non-increasing: {rates}")

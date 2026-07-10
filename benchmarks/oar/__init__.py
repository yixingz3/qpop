"""benchmarks.oar — the OAR (over-admission rate) benchmark, v0 pilot.

v0 scope (OAR_BENCHMARK_DESIGN_WORKING.md, "Staged roadmap"): a 2-domain pilot built
entirely from already-preserved, already-public material (AI supply chain + uranium) --
the shared task-format spec, the domain-pack pattern, the ablation harness reading OAR
straight from recorded aggregates, and the monotone discipline curve as the reference.
No new forward data, no LLM calls in this package.

See ``README.md`` for the run-it-yourself instructions and the aggregate-vs-per-card /
privacy boundary.
"""
from .loader import DomainPack, PackNotFoundError, PackValidationError, list_packs, load_pack
from .scoring import (
    DISCIPLINE_CURVE_ORDER,
    DisciplineCurvePoint,
    OARResult,
    RejectionPrecision,
    admission_rate_per_arm,
    arm_admission_rate,
    assert_monotone_nonincreasing,
    compute_oar,
    discipline_curve,
    oar_from_aggregate_zero_reference,
    rejection_precision_from_aggregate,
    wilson_score_interval,
)

__all__ = [
    "DomainPack",
    "PackNotFoundError",
    "PackValidationError",
    "list_packs",
    "load_pack",
    "DISCIPLINE_CURVE_ORDER",
    "DisciplineCurvePoint",
    "OARResult",
    "RejectionPrecision",
    "admission_rate_per_arm",
    "arm_admission_rate",
    "assert_monotone_nonincreasing",
    "compute_oar",
    "discipline_curve",
    "oar_from_aggregate_zero_reference",
    "rejection_precision_from_aggregate",
    "wilson_score_interval",
]

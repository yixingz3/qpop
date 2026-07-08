"""Anytime-valid sequential trigger test — the paper's §7 Decision Rules, implemented.

A Forward-QPOP position is judged against *several* pre-registered exit triggers, and
each trigger is re-checked at every monitoring step (daily, per rebalance, ...). Naively
calling a thesis "Falsified" the first time any check fires would inflate the false-
"Falsified" rate exactly like the factor-zoo multiple-comparisons problem — here in its
*prospective, repeatedly-monitored* form. This module supplies the fix the paper commits
to: an **e-value (safe / anytime-valid) sequential test** with explicit Type-I control.

The model (per trigger)
-----------------------
Register, *before* the window, a binary null and a point alternative for each trigger's
per-step fire probability:

    H0 (thesis holds):  P(fire) <= p0      (the trigger rarely/never fires if the thesis is right)
    H1 (thesis broken): P(fire)  = p1 > p0

At each observation ``fired in {True, False}`` we multiply a running **betting
martingale** (an *e-process*) by the likelihood ratio of the point alternative over the
null-boundary p0:

    fired      -> multiply e by  p1 / p0
    not fired  -> multiply e by  (1 - p1) / (1 - p0)

Under H0 with per-step fire probability exactly p0, this ``e`` is a nonnegative
martingale with ``E[e_n] = 1``; for any ``P(fire) < p0`` it is a supermartingale
(``E[e_n] <= 1``). Either way **Ville's inequality** gives, for any alpha in (0,1),

    P_{H0}( sup_n e_n >= 1/alpha ) <= alpha .

So the rule "call *Falsified* only when ``e >= 1/alpha``" controls the Type-I error at
alpha **at any stopping time** — continuous monitoring and optional stopping included.
That is the whole point: you may peek after every trigger check and still keep the
false-"Falsified" rate at alpha.

Combining triggers / positions
------------------------------
E-values combine cleanly:

* **product** — valid when the component e-processes are *independent*; the merged
  process is again an e-process (``E[prod] <= 1`` under the joint null).
* **average** (the **default**) — the *arithmetic mean* of e-values is a valid e-value
  under **arbitrary dependence** between triggers (Vovk & Wang 2021). Exit triggers on
  one position (or across positions in one theme) are typically correlated, so averaging
  is the honest, dependence-safe merge; product would double-count shared evidence and
  break Type-I control. We therefore default to averaging and offer product only for the
  genuinely-independent case, documented at the call site.

Scope / limits (v1)
-------------------
* Binary trigger checks only (fired / not-fired per step). A metric-valued or
  one-sided-mean formulation is future work.
* ``p0`` and ``p1`` are **pre-registration parameters** — they must be fixed in the
  admission entry *before* the window opens, never tuned to the observed data. A point
  alternative (fixed ``p1``) is the simplest calibrated GRO-style bet; a mixture over p1
  is a documented future extension.

Pure standard library; no third-party dependencies.

References (verify titles/authors/venues before citing in the paper):
    Ramdas, Grünwald, Vovk & Shafer (2023), "Game-Theoretic Statistics and Safe
      Anytime-Valid Inference," Statistical Science 38(4):576-601. arXiv:2210.01948.
    Shafer (2021), "Testing by Betting," J. R. Statist. Soc. A 184(2):407-431.
    Vovk & Wang (2021), "E-values: calibration, combination and applications,"
      Ann. Statist. 49(3):1736-1754 (arithmetic averaging is the admissible merge
      under arbitrary dependence).
See research/docs/EVALUE_METHODS.md for the one-page methods note.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

__all__ = [
    "EProcess",
    "SequentialTriggerTest",
    "product_evalues",
    "average_evalues",
    "CONTINUE",
    "FALSIFIED",
]

CONTINUE: str = "continue"
FALSIFIED: str = "falsified"
_COMBINERS = ("product", "average")


def _check_p0_p1(p0: float, p1: float) -> None:
    if not (0.0 < p0 < 1.0):
        raise ValueError(f"p0 must be in the open interval (0, 1), got {p0!r}")
    if not (0.0 < p1 < 1.0):
        raise ValueError(f"p1 must be in the open interval (0, 1), got {p1!r}")
    if not (p1 > p0):
        raise ValueError(
            f"the alternative p1 must exceed the null boundary p0 (p1 > p0); "
            f"got p0={p0!r}, p1={p1!r}"
        )


@dataclass
class EProcess:
    """A single-trigger betting martingale (e-process) for a repeatedly-checked binary
    trigger, under the null ``P(fire) <= p0`` vs. point alternative ``P(fire) = p1``.

    ``e_value()`` is a nonnegative (super)martingale with ``E[e] <= 1`` under the null at
    any stopping time — the object Ville's inequality is applied to.
    """

    p0: float
    p1: float
    e: float = 1.0
    n: int = 0

    def __post_init__(self) -> None:
        _check_p0_p1(self.p0, self.p1)

    # Per-observation likelihood-ratio multipliers of the point alternative vs. the
    # null boundary p0. Precomputing keeps observe() a single multiply.
    @property
    def _lr_fired(self) -> float:
        return self.p1 / self.p0

    @property
    def _lr_not_fired(self) -> float:
        return (1.0 - self.p1) / (1.0 - self.p0)

    def observe(self, fired: bool) -> float:
        """Fold in one binary trigger check; return the updated e-value."""
        self.e *= self._lr_fired if fired else self._lr_not_fired
        self.n += 1
        return self.e

    def e_value(self) -> float:
        return self.e

    # ---------- serialization ----------
    def to_state(self) -> dict:
        """A plain JSON-serializable snapshot (so a ledger can persist it per entry)."""
        return {"p0": self.p0, "p1": self.p1, "e": self.e, "n": self.n}

    @classmethod
    def from_state(cls, state: dict) -> "EProcess":
        return cls(p0=state["p0"], p1=state["p1"], e=state["e"], n=state["n"])


def product_evalues(evalues: Iterable[float]) -> float:
    """Merge by product — valid when the component e-processes are **independent**.

    An empty collection merges to 1.0 (no evidence).
    """
    out = 1.0
    for e in evalues:
        out *= e
    return out


def average_evalues(evalues: Iterable[float]) -> float:
    """Merge by arithmetic average — valid under **arbitrary dependence** (the default).

    An empty collection merges to 1.0 (no evidence).
    """
    es = list(evalues)
    if not es:
        return 1.0
    return sum(es) / len(es)


@dataclass
class SequentialTriggerTest:
    """Anytime-valid sequential test over many binary exit triggers for one hypothesis.

    Consumes a stream of ``(trigger_id, fired)`` observations, maintaining one
    :class:`EProcess` per trigger id, and exposes:

    * :meth:`e_value` — the merged e-value across triggers (via ``combine``);
    * :meth:`decision` — ``"falsified"`` iff merged e >= 1/alpha, else ``"continue"``;
    * :meth:`to_state` / :meth:`from_state` — a serializable snapshot for the ledger.

    ``combine`` defaults to ``"average"`` (dependence-safe); use ``"product"`` only when
    the triggers are genuinely independent.
    """

    p0: float
    p1: float
    combine: str = "average"
    _procs: Dict[str, EProcess] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _check_p0_p1(self.p0, self.p1)
        if self.combine not in _COMBINERS:
            raise ValueError(
                f"combine must be one of {_COMBINERS}, got {self.combine!r}"
            )

    def observe(self, trigger_id: str, fired: bool) -> float:
        """Record one trigger check; return the merged e-value across all triggers."""
        proc = self._procs.get(trigger_id)
        if proc is None:
            proc = EProcess(p0=self.p0, p1=self.p1)
            self._procs[trigger_id] = proc
        proc.observe(fired)
        return self.e_value()

    def trigger_ids(self) -> List[str]:
        return list(self._procs.keys())

    def e_value(self) -> float:
        """The merged e-value across every trigger's e-process (1.0 if none seen)."""
        es = [p.e_value() for p in self._procs.values()]
        return product_evalues(es) if self.combine == "product" else average_evalues(es)

    def decision(self, alpha: float) -> str:
        """``"falsified"`` iff the merged e-value >= 1/alpha (Ville), else ``"continue"``.

        Calling this after every observation is safe: the guarantee is anytime-valid, so
        optional stopping does not inflate the false-"Falsified" rate beyond ``alpha``.
        """
        if not (0.0 < alpha < 1.0):
            raise ValueError(f"alpha must be in (0, 1), got {alpha!r}")
        return FALSIFIED if self.e_value() >= 1.0 / alpha else CONTINUE

    # ---------- serialization ----------
    def to_state(self) -> dict:
        """A plain JSON-serializable snapshot for per-entry ledger persistence."""
        return {
            "p0": self.p0,
            "p1": self.p1,
            "combine": self.combine,
            "procs": {tid: p.to_state() for tid, p in self._procs.items()},
        }

    @classmethod
    def from_state(cls, state: dict) -> "SequentialTriggerTest":
        st = cls(p0=state["p0"], p1=state["p1"], combine=state.get("combine", "average"))
        st._procs = {
            tid: EProcess.from_state(ps) for tid, ps in state.get("procs", {}).items()
        }
        return st

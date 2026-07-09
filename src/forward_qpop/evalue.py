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

## Ledger integration (WI-29)

The rest of this module (above) is the standalone e-process; the section below wires it
onto a real :class:`forward_qpop.ledger.Ledger` without any schema-breaking change:

* **Pre-registration parameters** (``p0``, ``p1``, ``combine``) live in the *admission*
  entry under a top-level ``"evalue"`` key -- an ordinary domain-specific field (like
  ``"node"`` or ``"decomposed_confidence"`` in the existing schema), passed via
  ``Ledger.register(..., fields={"evalue": {"p0": ..., "p1": ..., "combine": ...}})``.
  It is hashed like every other frozen field, so the bet is pre-committed, not tunable
  after the fact.
* **Per-step trigger observations** live in *belief_update* entries under a top-level
  ``"trigger_checks"`` key: ``{trigger_id: fired_bool, ...}``, passed via
  ``Ledger.update(..., fields={"trigger_checks": {...}})``. Each belief_update is one
  monitoring step; the triggers it names must already be in the admission's
  ``exit_triggers`` contract.
* :func:`run_ledger_evalue` walks a ledger, replays each hypothesis's belief_update
  stream through its own :class:`SequentialTriggerTest`, and reports the merged e-value,
  the ``1/alpha`` threshold, and the decision. State (the e-process, not the ledger) is
  persisted in a JSON **sidecar** file next to the ledger (``<ledger>.evalue-state.json``
  by default) so repeated invocations resume rather than silently re-deriving --
  anytime-valid across runs, never mutating a ledger row.
* Hypotheses with no ``"evalue"`` config are reported as ``no_config`` (skipped, not
  fabricated) -- see :data:`EVALUE_CONFIG_FIELD`.

CLI: ``forward-qpop evalue <ledger.jsonl> [--alpha 0.05] [--state <path>] [--json] [--out <path>]``.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from .ledger import Ledger

__all__ = [
    "EProcess",
    "SequentialTriggerTest",
    "product_evalues",
    "average_evalues",
    "CONTINUE",
    "FALSIFIED",
    "EVALUE_CONFIG_FIELD",
    "TRIGGER_CHECKS_FIELD",
    "EVALUE_STATE_SCHEMA",
    "EvalueLedgerError",
    "EvalueReportRow",
    "default_state_path_for",
    "load_evalue_state",
    "save_evalue_state",
    "run_ledger_evalue",
]

CONTINUE: str = "continue"
FALSIFIED: str = "falsified"
_COMBINERS = ("product", "average")

# Ledger integration (WI-29): field names for the two additive, schema-compatible hooks.
EVALUE_CONFIG_FIELD: str = "evalue"          # admission entry: {"p0", "p1", "combine"?}
TRIGGER_CHECKS_FIELD: str = "trigger_checks"  # belief_update entry: {trigger_id: fired_bool}
EVALUE_STATE_SCHEMA: str = "forward-qpop/evalue-state@1"


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

    def total_observations(self) -> int:
        """Total observe() calls folded in across every trigger id."""
        return sum(p.n for p in self._procs.values())

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


# --------------------------------------------------------------------------------------
# Ledger integration (WI-29): replay a ledger's belief_update stream through a
# SequentialTriggerTest per hypothesis, resuming from a persisted sidecar.
# --------------------------------------------------------------------------------------


class EvalueLedgerError(RuntimeError):
    """Raised when the ledger's e-value wiring is malformed -- loud, never silent.

    Covers: an ``"evalue"`` admission config missing ``p0``/``p1``; a ``"trigger_checks"``
    payload that isn't a ``{trigger_id: bool}`` mapping; a trigger id not present in the
    hypothesis's registered ``exit_triggers``; or a state sidecar whose ``last_entry_hash``
    can no longer be found in the ledger (the ledger was rewritten out from under the
    sidecar -- resuming would silently skip or double-count observations).
    """


@dataclass
class EvalueReportRow:
    """One report line: a hypothesis's e-value decision, or why it was skipped."""

    id: str
    status: str  # "ok" | "no_config"
    p0: Optional[float] = None
    p1: Optional[float] = None
    combine: Optional[str] = None
    n_triggers: int = 0
    n_observations: int = 0
    e_value: Optional[float] = None
    threshold: Optional[float] = None
    decision: Optional[str] = None
    ledger_outcome: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def default_state_path_for(ledger_path: Union[str, Path]) -> Path:
    p = Path(ledger_path)
    return p.with_name(p.name + ".evalue-state.json")


def load_evalue_state(state_path: Union[str, Path]) -> dict:
    """Load the e-value state sidecar, or a fresh empty one if it doesn't exist yet."""
    p = Path(state_path)
    if not p.exists():
        return {"schema": EVALUE_STATE_SCHEMA, "hypotheses": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save_evalue_state(state_path: Union[str, Path], state: dict) -> None:
    """Write the e-value state sidecar. Never touches the ledger file itself."""
    p = Path(state_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _group_by_id(entries: Iterable[dict]) -> Dict[str, List[dict]]:
    out: Dict[str, List[dict]] = {}
    for e in entries:
        out.setdefault(e["id"], []).append(e)
    return out


def _evalue_config(admission: dict) -> Tuple[float, float, str]:
    cfg = admission.get(EVALUE_CONFIG_FIELD)
    if not isinstance(cfg, dict):
        raise EvalueLedgerError(
            f"internal: _evalue_config called without a valid {EVALUE_CONFIG_FIELD!r} config"
        )
    try:
        p0 = float(cfg["p0"])
        p1 = float(cfg["p1"])
    except (KeyError, TypeError, ValueError) as exc:
        raise EvalueLedgerError(
            f"{admission.get('id', '?')}: {EVALUE_CONFIG_FIELD!r} admission config must "
            f"include numeric 'p0' and 'p1' (got {cfg!r})"
        ) from exc
    combine = cfg.get("combine", "average")
    return p0, p1, combine


def run_ledger_evalue(
    ledger_path: Union[str, Path],
    *,
    alpha: float = 0.05,
    state_path: Optional[Union[str, Path]] = None,
    persist: bool = True,
) -> Tuple[List[EvalueReportRow], dict]:
    """Fold newly-recorded trigger checks into each hypothesis's e-process and report.

    Anytime-valid across repeated invocations: the merged e-value only ever grows by
    folding in observations once each (tracked via ``last_entry_hash`` in the sidecar),
    so re-running after new belief_update entries land resumes rather than re-derives.
    The ledger file itself is read-only here -- state lives entirely in the sidecar.

    Returns ``(rows, state)``; ``state`` is the (possibly updated) sidecar dict, already
    written to disk unless ``persist=False`` (dry run).
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha must be in (0, 1), got {alpha!r}")

    entries = Ledger(ledger_path).entries()
    by_id = _group_by_id(entries)
    sp = Path(state_path) if state_path else default_state_path_for(ledger_path)
    state = load_evalue_state(sp)
    hyps_state: Dict[str, dict] = state.setdefault("hypotheses", {})

    rows: List[EvalueReportRow] = []
    for hid, hentries in by_id.items():
        admission = next((e for e in hentries if e.get("type") == "admission"), None)
        if admission is None:
            continue  # every hypothesis id roots at an admission entry; nothing to do

        ledger_outcome = next(
            (e.get("status") for e in hentries if e.get("type") == "outcome"), None
        )
        cfg_present = isinstance(admission.get(EVALUE_CONFIG_FIELD), dict)
        saved = hyps_state.get(hid)

        if not cfg_present and saved is None:
            rows.append(EvalueReportRow(id=hid, status="no_config", ledger_outcome=ledger_outcome))
            continue

        registered_trigger_ids = {t["id"] for t in admission.get("exit_triggers", []) if "id" in t}

        if saved is not None:
            test = SequentialTriggerTest.from_state(saved["test_state"])
            resume_after_hash = saved.get("last_entry_hash")
            skipping = resume_after_hash is not None
        else:
            p0, p1, combine = _evalue_config(admission)
            test = SequentialTriggerTest(p0=p0, p1=p1, combine=combine)
            resume_after_hash = None
            skipping = False

        # `resume_after_hash` is the fixed target we're skipping up through (from the
        # sidecar); `last_processed_hash` is a running tracker of the latest entry seen,
        # re-saved at the end. Keeping these as two variables matters: overwriting the
        # target while still searching for it would make the search unfindable.
        found_resume_point = not skipping
        last_processed_hash = None
        for e in hentries:
            eh = e.get("entry_hash")
            if skipping:
                if eh == resume_after_hash:
                    skipping = False
                    found_resume_point = True
                last_processed_hash = eh
                continue
            if e.get("type") == "belief_update":
                checks = e.get(TRIGGER_CHECKS_FIELD)
                if checks:
                    if not isinstance(checks, dict):
                        raise EvalueLedgerError(
                            f"{hid}: {TRIGGER_CHECKS_FIELD!r} must be a dict of "
                            f"{{trigger_id: bool}}, got {type(checks).__name__}"
                        )
                    for tid, fired in sorted(checks.items()):
                        if registered_trigger_ids and tid not in registered_trigger_ids:
                            raise EvalueLedgerError(
                                f"{hid}: {TRIGGER_CHECKS_FIELD!r} references unregistered "
                                f"trigger id {tid!r} (registered: {sorted(registered_trigger_ids)})"
                            )
                        test.observe(tid, bool(fired))
            last_processed_hash = eh

        if not found_resume_point:
            raise EvalueLedgerError(
                f"{hid}: state sidecar's last_entry_hash was not found in the ledger -- "
                f"the ledger was rewritten/truncated since the last `evalue` run; refusing "
                f"to silently skip or double-count observations (delete the sidecar to "
                f"restart this hypothesis from scratch if that's intended)"
            )

        hyps_state[hid] = {"test_state": test.to_state(), "last_entry_hash": last_processed_hash}
        e_value = test.e_value()
        rows.append(
            EvalueReportRow(
                id=hid,
                status="ok",
                p0=test.p0,
                p1=test.p1,
                combine=test.combine,
                n_triggers=len(test.trigger_ids()),
                n_observations=test.total_observations(),
                e_value=e_value,
                threshold=1.0 / alpha,
                decision=test.decision(alpha),
                ledger_outcome=ledger_outcome,
            )
        )

    if persist:
        save_evalue_state(sp, state)
    return rows, state

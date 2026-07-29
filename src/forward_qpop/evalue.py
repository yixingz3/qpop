"""Sequential trigger test (e-value rule) — per-hypothesis scope; registered mode delivers
the anytime-valid guarantee under stated assumptions (WI-40); legacy lazy mode is exploratory.

A Forward-QPOP position is judged against *several* pre-registered exit triggers, and
each trigger is re-checked at every monitoring step (daily, per rebalance, ...). Naively
calling a thesis "Falsified" the first time any check fires would inflate the false-
"Falsified" rate exactly like the factor-zoo multiple-comparisons problem — here in its
*prospective, repeatedly-monitored* form. This module implements the rule the paper's
§7 Decision Rules specifies for that problem: an **e-value (safe / anytime-valid)
sequential test**.

.. note:: **Guarantee status (WI-40, closed 2026-07-25).** The two defects named by the
   v2 review round are fixed with regression tests: (1) in registered (fixed-membership)
   mode every registered trigger's e-process is initialized at 1 with fixed mixture
   weights from step 0 — late- or never-reporting registered triggers stay in the
   average at e=1; (2) trigger values are strictly type-checked (``bool`` only — no
   ``bool()`` coercion, so ``"false"`` is rejected, not counted as fired). In registered
   mode the implementation now matches the rule, so the per-hypothesis anytime-valid
   Type-I property holds **under the stated assumptions** (conditional null
   ``P(fire_t=1 | past) <= p0``, non-overlapping observation periods — a persistent
   fired state must not be re-counted; product combiner only under genuine
   independence). Legacy lazy mode (``registered=None``) remains exploratory-only: it
   changes mixture membership mid-stream and carries no guarantee. Scope is
   **per-hypothesis only**: nothing here controls multiplicity across
   hypotheses/positions (book-wide control is future work), and the reporting-time
   ``alpha`` is not part of the hashed commitment. **WI-44 (2026-07-28):** the ledger runner verifies the hash chain BEFORE evaluating, replays the verified ledger from each admission on every run (the state sidecar is a cache with no decision authority — tampered, legacy, or rewound sidecars are discarded and rebuilt), validates the raw exit-trigger contract (no row silently dropped; checks validated by presence, not truthiness), and decides on the persisted running maximum (the rejection event is sup_t e_t >= 1/alpha, so a crossing within the verified history is never forgotten; it is latched within the verified ledger's recorded history; deleting a SUFFIX of the chain leaves a valid prefix that chain-only verification cannot distinguish from the true head, so rollback detection requires an anchored/expected head (the anchor feature / --expected-head).). Additional stated assumption: the decision to report or skip a scheduled check must be predictable from past information and independent of the current unseen outcome — outcome-dependent selective reporting (e.g., reporting only fires) voids the guarantee (demonstrated by an adversarial regression).

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

So the mathematical rule "call *Falsified* only when ``e >= 1/alpha``" controls the Type-I
error at alpha **at any stopping time** — continuous monitoring and optional stopping
included — *under its assumptions and with fixed mixture weights over all registered
triggers*. Registered mode implements exactly that requirement (see the note above);
legacy lazy mode does not and is exploratory-only.

Combining triggers (within ONE hypothesis)
------------------------------------------
E-values combine cleanly:

* **product** — valid when the component e-processes are *independent*; the merged
  process is again an e-process (``E[prod] <= 1`` under the joint null).
* **average** (the **default**) — the *arithmetic mean* of e-values is a valid e-value
  under **arbitrary dependence** between triggers (Vovk & Wang 2021). Exit triggers on
  one position are typically correlated, so averaging
  is the honest, dependence-safe merge; product would double-count shared evidence and
  break Type-I control. We therefore default to averaging and offer product only for the
  genuinely-independent case, documented at the call site. Averaging within one
  hypothesis provides NO multiplicity control across hypotheses/positions.

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
* :func:`run_ledger_evalue` (WI-44) first verifies the ledger's hash chain, then
  replays each hypothesis's belief_update stream FROM ITS ADMISSION through a fresh
  :class:`SequentialTriggerTest` on every invocation, and reports the merged e-value,
  the persisted running maximum ``max_e``, the ``1/alpha`` threshold, and the decision
  (``falsified`` iff ``max_e >= 1/alpha`` -- the sup-rule). The JSON **sidecar**
  (``<ledger>.evalue-state.json``) is regenerated each run purely for inspection: it is
  a cache with NO decision authority, so tampered/legacy/rewound sidecars are simply
  discarded and rebuilt, and the ledger is never mutated.
* Hypotheses with no ``"evalue"`` config are reported as ``no_config`` (skipped, not
  fabricated) -- see :data:`EVALUE_CONFIG_FIELD`.

CLI: ``forward-qpop evalue <ledger.jsonl> [--alpha 0.05] [--state <path>] [--json] [--out <path>]``.
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from .ledger import Ledger, verify_entries

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
    log_e: float = 0.0
    n: int = 0

    def __post_init__(self) -> None:
        _check_p0_p1(self.p0, self.p1)

    # WI-45 (B31-02): the martingale lives in LOG space so long valid histories can
    # neither overflow to Infinity nor underflow-then-NaN; decisions compare logs.
    @property
    def _log_lr_fired(self) -> float:
        return math.log(self.p1) - math.log(self.p0)

    @property
    def _log_lr_not_fired(self) -> float:
        return math.log(1.0 - self.p1) - math.log(1.0 - self.p0)

    def observe(self, fired: bool) -> float:
        """Fold in one binary trigger check; return the updated e-value.

        ``fired`` must be a real boolean (WI-40): truthy stand-ins like ``"false"``
        or ``1`` are rejected rather than coerced, because ``bool("false")`` is
        ``True`` and a silent coercion would count a non-firing as evidence.
        """
        if not isinstance(fired, bool):
            raise TypeError(
                f"fired must be a bool, got {type(fired).__name__}: {fired!r}"
            )
        self.log_e += self._log_lr_fired if fired else self._log_lr_not_fired
        self.n += 1
        return self.e_value()

    def log_e_value(self) -> float:
        return self.log_e

    def e_value(self) -> float:
        """Linear display value; ``inf`` past float range. Decisions use logs."""
        try:
            return math.exp(self.log_e)
        except OverflowError:
            return float("inf")

    # ---------- serialization ----------
    def to_state(self) -> dict:
        """A plain JSON-serializable snapshot (always finite: logs, not linear e)."""
        return {"p0": self.p0, "p1": self.p1, "log_e": self.log_e, "n": self.n}

    @classmethod
    def from_state(cls, state: dict) -> "EProcess":
        if "log_e" in state:
            log_e = state["log_e"]
        else:  # legacy linear-e snapshot
            e = state["e"]
            if not (isinstance(e, (int, float)) and e > 0 and math.isfinite(e)):
                raise ValueError(f"legacy e-process state has invalid e: {e!r}")
            log_e = math.log(e)
        return cls(p0=state["p0"], p1=state["p1"], log_e=log_e, n=state["n"])


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
    """Sequential test over many binary exit triggers for one hypothesis.

    Implements the e-value rule described in the module docstring. Pass ``registered``
    (the admission's exit-trigger ids) for fixed-membership mode — the mode with the
    per-hypothesis anytime-valid property under the stated assumptions (WI-40); leave
    it ``None`` only for exploratory use.

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
    registered: Optional[Tuple[str, ...]] = None
    _procs: Dict[str, EProcess] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _check_p0_p1(self.p0, self.p1)
        if self.combine not in _COMBINERS:
            raise ValueError(
                f"combine must be one of {_COMBINERS}, got {self.combine!r}"
            )
        if self.registered is not None:
            ids = tuple(sorted(dict.fromkeys(self.registered)))
            if not ids:
                raise ValueError("registered must be non-empty when provided")
            self.registered = ids
            # WI-40: every registered trigger's e-process exists from step 0 at
            # e=1 with fixed mixture membership/weights — the rule's requirement.
            for tid in ids:
                if tid not in self._procs:
                    self._procs[tid] = EProcess(p0=self.p0, p1=self.p1)

    def observe(self, trigger_id: str, fired: bool) -> float:
        """Record one trigger check; return the merged e-value across all triggers.

        In registered (fixed-membership) mode, an id outside the registered set is
        an error; in legacy lazy mode (``registered=None``, exploratory use only)
        an unseen id creates a new e-process, which changes mixture weights
        mid-stream and forfeits the anytime-valid property.
        """
        if not isinstance(fired, bool):
            raise TypeError(
                f"fired must be a bool, got {type(fired).__name__}: {fired!r}"
            )
        proc = self._procs.get(trigger_id)
        if proc is None:
            if self.registered is not None:
                raise ValueError(
                    f"trigger id {trigger_id!r} is not in the registered set "
                    f"{list(self.registered)}"
                )
            proc = EProcess(p0=self.p0, p1=self.p1)
            self._procs[trigger_id] = proc
        proc.observe(fired)
        return self.e_value()

    def trigger_ids(self) -> List[str]:
        return list(self._procs.keys())

    def total_observations(self) -> int:
        """Total observe() calls folded in across every trigger id."""
        return sum(p.n for p in self._procs.values())

    def log_e_value(self) -> float:
        """The merged LOG e-value (0.0 if none seen) -- the decision-bearing quantity.

        product: sum of component logs. average: log-sum-exp minus log(k), the
        numerically stable arithmetic-mean merge (WI-45)."""
        logs = [p.log_e_value() for p in self._procs.values()]
        if not logs:
            return 0.0
        if self.combine == "product":
            return sum(logs)
        m = max(logs)
        return m + math.log(sum(math.exp(x - m) for x in logs)) - math.log(len(logs))

    def e_value(self) -> float:
        """Linear display value of the merge; ``inf`` past float range (display only)."""
        try:
            return math.exp(self.log_e_value())
        except OverflowError:
            return float("inf")

    def decision(self, alpha: float) -> str:
        """``"falsified"`` iff the merged e-value >= 1/alpha (Ville), else ``"continue"``.

        In registered mode, calling this after every observation is safe (anytime-valid;
        optional stopping does not inflate the false-"Falsified" rate beyond ``alpha``)
        under the module-note assumptions. In legacy lazy mode the decision is
        exploratory/advisory only.
        """
        if not (0.0 < alpha < 1.0):
            raise ValueError(f"alpha must be in (0, 1), got {alpha!r}")
        # WI-45: compare in log space -- immune to overflow/underflow at extreme
        # parameters (log(1/alpha) is finite for every alpha in (0,1)).
        return FALSIFIED if self.log_e_value() >= -math.log(alpha) else CONTINUE

    # ---------- serialization ----------
    def to_state(self) -> dict:
        """A plain JSON-serializable snapshot for per-entry ledger persistence."""
        state = {
            "p0": self.p0,
            "p1": self.p1,
            "combine": self.combine,
            "procs": {tid: p.to_state() for tid, p in self._procs.items()},
        }
        if self.registered is not None:
            state["registered"] = list(self.registered)
        return state

    @classmethod
    def from_state(cls, state: dict) -> "SequentialTriggerTest":
        registered = state.get("registered")
        st = cls(
            p0=state["p0"],
            p1=state["p1"],
            combine=state.get("combine", "average"),
            registered=tuple(registered) if registered else None,
        )
        st._procs = {
            tid: EProcess.from_state(ps) for tid, ps in state.get("procs", {}).items()
        }
        if st.registered is not None:
            # Defensive: a registered trigger absent from the snapshot re-enters at
            # e=1 (fixed membership must survive the round-trip).
            for tid in st.registered:
                if tid not in st._procs:
                    st._procs[tid] = EProcess(p0=st.p0, p1=st.p1)
        return st


# --------------------------------------------------------------------------------------
# Ledger integration (WI-29): replay a ledger's belief_update stream through a
# SequentialTriggerTest per hypothesis, resuming from a persisted sidecar.
# --------------------------------------------------------------------------------------


class EvalueLedgerError(RuntimeError):
    """Raised when the ledger's e-value wiring is malformed -- loud, never silent.

    Covers (WI-43/WI-44): a ledger that fails hash-chain verification; an ``"evalue"``
    admission config missing ``p0``/``p1``; an empty, non-unique, or malformed
    exit-trigger contract (rows without a nonempty string ``id`` are never dropped
    silently); a ``"trigger_checks"`` payload that isn't a ``{trigger_id: bool}``
    mapping (presence-checked -- falsey non-dict payloads fail); a trigger id not in
    the registered contract; or a non-boolean trigger value.
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
    log_e: Optional[float] = None
    max_e: Optional[float] = None
    max_log_e: Optional[float] = None
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
    p.write_text(
        json.dumps(state, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


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
    expected_head: Optional[str] = None,
    state_path: Optional[Union[str, Path]] = None,
    persist: bool = True,
) -> Tuple[List[EvalueReportRow], dict]:
    """Replay the verified ledger and report each hypothesis's sequential test (WI-45).

    One immutable snapshot is parsed, hash-chain-verified in memory, lifecycle-validated
    (one admission first, at most one terminal outcome last, no orphan rows), and replayed
    from each admission on every invocation. The JSON sidecar is a regenerated **derived
    inspection snapshot** with no decision authority -- it is never read back. Decisions
    use the persisted running maximum in LOG space (``max_log_e >= -log(alpha)``). The
    ledger file itself is never written; state/report paths that alias it are rejected.

    Returns ``(rows, state)``; ``state`` is the (possibly updated) sidecar dict, already
    written to disk unless ``persist=False`` (dry run).
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha must be in (0, 1), got {alpha!r}")

    # WI-45 (B31-01): parse ONE immutable snapshot, verify that exact in-memory
    # sequence, and replay that same sequence -- no verify-then-re-read window.
    entries = Ledger(ledger_path).entries()
    vres = verify_entries(entries)
    if not vres.ok:
        raise EvalueLedgerError(
            f"ledger failed hash-chain verification; refusing to evaluate: "
            f"{vres.problems[:2]}"
        )
    if expected_head is not None:
        actual = entries[-1].get("entry_hash") if entries else None
        if actual != expected_head:
            raise EvalueLedgerError(
                f"ledger head {actual!r} does not match the expected/anchored head "
                f"{expected_head!r} -- possible suffix rollback (chain-only verification "
                f"cannot detect deletion of a suffix; see the anchor feature)"
            )
    by_id = _group_by_id(entries)
    sp = Path(state_path) if state_path else default_state_path_for(ledger_path)
    # WI-45 (B31-01): the sidecar/report paths must never alias the ledger itself.
    lp_resolved = Path(ledger_path).resolve()
    if sp.resolve() == lp_resolved:
        raise EvalueLedgerError(
            f"state_path resolves to the ledger file itself ({lp_resolved}); refusing "
            f"to overwrite the ledger"
        )
    # WI-44 (B29-01): the sidecar is a pure CACHE with no decision authority. Every run
    # replays the verified ledger from each admission and REGENERATES the sidecar, so a
    # tampered, legacy, or rewound sidecar is simply discarded and rebuilt -- it can
    # never alter membership, component state, progress, or the decision.
    state: Dict[str, Any] = {"schema": EVALUE_STATE_SCHEMA, "hypotheses": {}}
    hyps_state: Dict[str, dict] = state["hypotheses"]

    rows: List[EvalueReportRow] = []
    for hid, hentries in by_id.items():
        # WI-45 (B31-01): validate the hypothesis LIFECYCLE before replay.
        admissions = [e for e in hentries if e.get("type") == "admission"]
        outcomes = [e for e in hentries if e.get("type") == "outcome"]
        if not admissions:
            raise EvalueLedgerError(
                f"{hid}: entries exist with no admission (orphan/pre-admission rows)"
            )
        if len(admissions) > 1:
            raise EvalueLedgerError(f"{hid}: {len(admissions)} admission entries; expected 1")
        if hentries[0] is not admissions[0]:
            raise EvalueLedgerError(f"{hid}: the admission is not the first entry for this id")
        if len(outcomes) > 1:
            raise EvalueLedgerError(f"{hid}: {len(outcomes)} terminal outcomes; expected <= 1")
        if outcomes and hentries[-1] is not outcomes[0]:
            raise EvalueLedgerError(
                f"{hid}: entries appear after the terminal outcome -- a closed hypothesis "
                f"is immutable (open a new id to revise)"
            )
        admission = admissions[0]

        ledger_outcome = next(
            (e.get("status") for e in hentries if e.get("type") == "outcome"), None
        )
        if EVALUE_CONFIG_FIELD not in admission:
            rows.append(EvalueReportRow(id=hid, status="no_config", ledger_outcome=ledger_outcome))
            continue
        if not isinstance(admission.get(EVALUE_CONFIG_FIELD), dict):
            raise EvalueLedgerError(
                f"{hid}: {EVALUE_CONFIG_FIELD!r} is present but not a mapping "
                f"(got {type(admission.get(EVALUE_CONFIG_FIELD)).__name__}); only a "
                f"genuinely absent field is no_config"
            )

        # WI-44 (B29-02): validate the RAW contract -- a row without a nonempty string
        # id must fail loudly, never be silently dropped from the registered set.
        raw_triggers = admission.get("exit_triggers", [])
        if not isinstance(raw_triggers, list):
            raise EvalueLedgerError(f"{hid}: exit_triggers must be a list")
        trigger_id_list: List[str] = []
        for t in raw_triggers:
            if not isinstance(t, dict) or not isinstance(t.get("id"), str) or not t["id"].strip():
                raise EvalueLedgerError(
                    f"{hid}: every exit-trigger row must be a mapping with a nonempty "
                    f"string 'id' (got {t!r}); an e-value commitment cannot drop "
                    f"contract rows"
                )
            trigger_id_list.append(t["id"])
        registered_trigger_ids = set(trigger_id_list)
        # WI-43 (B27-03): an e-value commitment REQUIRES a nonempty, uniquely identified
        # exit-trigger contract -- the runner must never silently fall back to lazy mode.
        p0, p1, combine = _evalue_config(admission)
        if not registered_trigger_ids or len(trigger_id_list) != len(registered_trigger_ids):
            raise EvalueLedgerError(
                f"{hid}: an 'evalue' commitment requires a nonempty exit_triggers contract "
                f"with unique ids (got {trigger_id_list!r}); refusing to run in lazy mode"
            )
        expected_registered = tuple(sorted(registered_trigger_ids))
        test = SequentialTriggerTest(
            p0=p0,
            p1=p1,
            combine=combine,
            # WI-40: the admission's registered exit-trigger contract fixes the
            # mixture membership from step 0 (every registered trigger at e=1).
            registered=expected_registered,
        )

        # WI-44 (B29-01/03): full replay of the verified ledger, latching the running
        # maximum merged e-value after each complete belief-update step -- the decision
        # is the mathematical rejection event sup_t e_t >= 1/alpha, so a crossing can
        # never be forgotten by later shrinkage or across invocations.
        max_log_e = 0.0
        last_processed_hash = None
        for e in hentries:
            last_processed_hash = e.get("entry_hash")
            if e.get("type") != "belief_update":
                continue
            if TRIGGER_CHECKS_FIELD not in e:
                continue
            # WI-44 (B29-02): presence, not truthiness -- a falsey non-dict payload
            # ([], "", 0, false) is malformed, and an empty dict is a legal
            # zero-observation step.
            checks = e.get(TRIGGER_CHECKS_FIELD)
            if not isinstance(checks, dict):
                raise EvalueLedgerError(
                    f"{hid}: {TRIGGER_CHECKS_FIELD!r} must be a dict of "
                    f"{{trigger_id: bool}}, got {type(checks).__name__}: {checks!r}"
                )
            for tid, fired in sorted(checks.items()):
                if tid not in registered_trigger_ids:
                    raise EvalueLedgerError(
                        f"{hid}: {TRIGGER_CHECKS_FIELD!r} references unregistered "
                        f"trigger id {tid!r} (registered: {sorted(registered_trigger_ids)})"
                    )
                if not isinstance(fired, bool):
                    raise EvalueLedgerError(
                        f"{hid}: trigger {tid!r} value must be a JSON boolean, "
                        f"got {type(fired).__name__}: {fired!r} (WI-40: no "
                        f"coercion -- bool('false') would count as fired)"
                    )
                test.observe(tid, fired)
            max_log_e = max(max_log_e, test.log_e_value())

        hyps_state[hid] = {
            "test_state": test.to_state(),
            "last_entry_hash": last_processed_hash,
            "max_log_e": max_log_e,
        }
        def _finite_or_none(log_x):
            try:
                v = math.exp(log_x)
            except OverflowError:
                return None
            return v if math.isfinite(v) else None

        e_value = _finite_or_none(test.log_e_value())
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
                log_e=test.log_e_value(),
                max_e=_finite_or_none(max_log_e),
                max_log_e=max_log_e,
                threshold=1.0 / alpha,
                decision=FALSIFIED if max_log_e >= -math.log(alpha) else CONTINUE,
                ledger_outcome=ledger_outcome,
            )
        )

    if persist:
        save_evalue_state(sp, state)
    return rows, state

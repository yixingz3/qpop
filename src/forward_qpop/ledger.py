"""The Forward-QPOP ledger: an append-only, hash-chained pre-registration record.

Each entry is content-hashed over its *frozen* (load-bearing) fields and binds the
previous entry's hash, so the ledger is a hash chain:

    entry_hash = sha256(content_hash || prev_hash)

Two integrity properties follow:

* **Per-entry integrity** — editing any frozen field of a past entry changes its
  ``content_hash``; ``verify()`` detects the mismatch.
* **Append-order integrity** — because each entry commits to its predecessor, you
  cannot silently insert, delete, or reorder a past entry without breaking the chain
  for every entry after it.

The chained object is the *pre-registered hypothesis contract* (claim, dated evidence,
entry/update/exit triggers) committed before the evaluation window — so the chain
proves what was predicted and when, not merely what was recorded.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, List, Optional, Set, Union

GENESIS: str = "0" * 64
ADMISSION: str = "admission"
BELIEF_UPDATE: str = "belief_update"
OUTCOME: str = "outcome"
TERMINAL_STATUSES = ("supported", "weakened", "falsified")

_HASH_FIELDS = ("content_hash", "prev_hash", "entry_hash")
# Tiers that may move confidence; tertiary (social) is idea-seed only.
_CORROBORATING_TIERS = ("primary", "secondary", "market_implied")


def _canonical(obj: Any) -> str:
    """Deterministic JSON: sorted keys, compact separators, UTF-8 preserved."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def content_hash(entry: dict) -> str:
    """Hex SHA-256 over the frozen fields — everything except the hash fields."""
    frozen = {k: v for k, v in entry.items() if k not in _HASH_FIELDS}
    return hashlib.sha256(_canonical(frozen).encode("utf-8")).hexdigest()


def entry_hash(content_hex: str, prev_hash: str) -> str:
    """Chain link: sha256(content_hash || prev_hash)."""
    return hashlib.sha256((content_hex + prev_hash).encode("utf-8")).hexdigest()


def _strip(h: str) -> str:
    """Accept either ``sha256:<hex>`` or a bare ``<hex>``."""
    return h.split(":", 1)[1] if h and h.startswith("sha256:") else h


class IntegrityError(Exception):
    """Raised on an attempt that would violate the ledger's discipline."""


@dataclass
class VerifyResult:
    ok: bool
    n_entries: int
    problems: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.ok


class Ledger:
    """An append-only, hash-chained Forward-QPOP ledger backed by a JSONL file."""

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

    # ---------- read ----------
    def entries(self) -> List[dict]:
        if not self.path.exists():
            return []
        out: List[dict] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
        return out

    def _last_entry_hash(self) -> str:
        es = self.entries()
        return es[-1].get("entry_hash", GENESIS) if es else GENESIS

    def _terminal_ids(self) -> Set[str]:
        return {
            e["id"]
            for e in self.entries()
            if e.get("type") == OUTCOME and e.get("status") in TERMINAL_STATUSES
        }

    # ---------- write (append-only) ----------
    def _append(self, entry: dict) -> dict:
        ch = content_hash(entry)
        ph = self._last_entry_hash()
        full = {
            **entry,
            "content_hash": "sha256:" + ch,
            "prev_hash": ph,
            "entry_hash": entry_hash(ch, ph),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(_canonical(full) + "\n")
        return full

    def register(
        self,
        id: str,
        claim: str,
        *,
        mechanism: str = "",
        evidence: Optional[List[dict]] = None,
        exit_triggers: Optional[List[dict]] = None,
        prior: Optional[float] = None,
        role_admitted: Optional[str] = None,
        created: Optional[str] = None,
        fields: Optional[dict] = None,
    ) -> dict:
        """Pre-register a hypothesis BEFORE the evaluation window opens.

        ``fields`` carries any domain-specific payload (e.g. a decomposed-confidence
        dict, scores, a ticker) — it is hashed like every other frozen field.
        """
        if id in self._terminal_ids():
            raise IntegrityError(
                f"hypothesis {id!r} already has a terminal outcome; open a new id to "
                f"revise (closed entries are immutable)"
            )
        entry: dict = {
            "id": id,
            "type": ADMISSION,
            "status": "open",
            "created": created or date.today().isoformat(),
            "claim": claim,
            "mechanism": mechanism,
            "evidence": list(evidence or []),
            "exit_triggers": list(exit_triggers or []),
        }
        if prior is not None:
            entry["prior_confidence"] = prior
        if role_admitted is not None:
            entry["role_admitted"] = role_admitted
        if fields:
            entry.update(fields)
        return self._append(entry)

    def update(
        self,
        id: str,
        *,
        evidence: List[dict],
        recorded: Optional[str] = None,
        fields: Optional[dict] = None,
        allow_tertiary_only: bool = False,
    ) -> dict:
        """Record a content-hash-protected belief update with cited evidence.

        Tertiary sources alone cannot move confidence (pass ``allow_tertiary_only=True``
        to override that discipline explicitly).
        """
        if not evidence:
            raise ValueError("a belief update requires cited evidence")
        if not allow_tertiary_only and not any(
            e.get("tier") in _CORROBORATING_TIERS for e in evidence
        ):
            raise IntegrityError(
                "tertiary sources alone cannot move confidence; cite >= secondary or "
                "market-implied evidence (or pass allow_tertiary_only=True)"
            )
        entry: dict = {
            "id": id,
            "type": BELIEF_UPDATE,
            "recorded": recorded or date.today().isoformat(),
            "evidence": list(evidence),
        }
        if fields:
            entry.update(fields)
        return self._append(entry)

    def close(
        self,
        id: str,
        outcome: str,
        *,
        observed: Optional[dict] = None,
        recorded: Optional[str] = None,
    ) -> dict:
        """Close a hypothesis with a pre-committed outcome.

        ``outcome`` is one of ``supported`` / ``weakened`` / ``falsified``.
        """
        if outcome not in TERMINAL_STATUSES:
            raise ValueError(
                f"outcome must be one of {TERMINAL_STATUSES}, got {outcome!r}"
            )
        entry = {
            "id": id,
            "type": OUTCOME,
            "status": outcome,
            "outcome": outcome,
            "recorded": recorded or date.today().isoformat(),
            "observed": dict(observed or {}),
        }
        return self._append(entry)

    # ---------- verify ----------
    def verify(self) -> VerifyResult:
        """Recompute every content hash and the full chain; report any break."""
        problems: List[str] = []
        prev = GENESIS
        for i, e in enumerate(self.entries()):
            tag = f"entry {i} (id={e.get('id', '?')}, type={e.get('type', '?')})"
            stored_ch = _strip(e.get("content_hash", ""))
            recomputed = content_hash(e)
            if stored_ch != recomputed:
                problems.append(f"{tag}: content_hash mismatch — a frozen field was edited")
            if e.get("prev_hash", GENESIS) != prev:
                problems.append(
                    f"{tag}: prev_hash does not chain to the previous entry — "
                    f"insertion, deletion, or reorder"
                )
            if e.get("entry_hash", "") != entry_hash(stored_ch, e.get("prev_hash", GENESIS)):
                problems.append(f"{tag}: entry_hash inconsistent with content_hash || prev_hash")
            prev = e.get("entry_hash", "")
        return VerifyResult(ok=not problems, n_entries=len(self.entries()), problems=problems)


def verify_file(path: Union[str, Path]) -> VerifyResult:
    """Convenience: verify the integrity of a ledger file."""
    return Ledger(path).verify()

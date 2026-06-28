"""External-anchor helpers for a Forward-QPOP ledger.

The hash chain proves *tamper-evidence* -- that no entry was edited, inserted, deleted,
or reordered -- but not *wall-clock time*: a ledger written today could carry a backdated
``created`` field. To prove an entry existed *before* an outcome, the ledger's head must be
bound to an external, append-only, publicly-dated record.

This module builds a small **anchor manifest** committing to the ledger's current head (and
a digest of the whole file), and helps you bind it to an external timestamp:

* **git** (always available in a repo): commit the manifest; once pushed to a public remote,
  the commit's authored date is the external timestamp. ``git_committed_time`` surfaces it.
* **OpenTimestamps** (optional, ``opentimestamps-client``): ``ots stamp`` the manifest for a
  ``.ots`` proof backed by the Bitcoin blockchain. Degrades gracefully if ``ots`` is absent.

``verify_anchor`` re-derives the head and file digest from the *current* ledger and checks them
against the manifest, so any drift since anchoring is detected on top of the chain's own check.

Pure standard library (``subprocess`` only shells out to optional ``git`` / ``ots``).
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Union

from .ledger import GENESIS, Ledger

ANCHOR_SCHEMA = "forward-qpop/anchor@1"


def _file_digest(path: Path) -> str:
    data = path.read_bytes() if path.exists() else b""
    return hashlib.sha256(data).hexdigest()


def ledger_head(path: Union[str, Path]) -> Tuple[str, int]:
    """Return ``(head_entry_hash, n_entries)`` for a ledger (GENESIS / 0 if empty)."""
    entries = Ledger(path).entries()
    head = entries[-1].get("entry_hash", GENESIS) if entries else GENESIS
    return head, len(entries)


def manifest_path_for(ledger_path: Union[str, Path]) -> Path:
    p = Path(ledger_path)
    return p.with_name(p.name + ".anchor.json")


def build_manifest(ledger_path: Union[str, Path]) -> dict:
    """Build an anchor manifest committing to the ledger's current head + file digest.

    Records NO self-asserted timestamp by design -- the external anchor (a git commit, an
    OTS proof) supplies the trusted time; this manifest only fixes *what* is being anchored.
    """
    p = Path(ledger_path)
    head, n = ledger_head(p)
    return {
        "schema": ANCHOR_SCHEMA,
        "ledger": p.name,
        "head_entry_hash": head,
        "n_entries": n,
        "file_sha256": _file_digest(p),
        "note": (
            "Anchor this manifest externally (commit it to a public repo, or `ots stamp`) "
            "to prove the ledger head existed at the anchor time. The chain proves "
            "tamper-evidence; the external anchor proves time."
        ),
    }


def write_manifest(
    ledger_path: Union[str, Path],
    manifest_path: Optional[Union[str, Path]] = None,
    manifest: Optional[dict] = None,
) -> Path:
    """Write the anchor manifest next to the ledger (``<ledger>.anchor.json`` by default).

    Pass a prebuilt ``manifest`` to avoid re-reading and re-hashing the ledger.
    """
    mp = Path(manifest_path) if manifest_path else manifest_path_for(ledger_path)
    mp.parent.mkdir(parents=True, exist_ok=True)
    payload = manifest if manifest is not None else build_manifest(ledger_path)
    mp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return mp


def ots_available() -> bool:
    """True if the OpenTimestamps client (``ots``) is on PATH."""
    return shutil.which("ots") is not None


def ots_stamp(manifest_path: Union[str, Path]) -> Optional[Path]:
    """``ots stamp`` the manifest if the client is installed; return the ``.ots`` proof or None."""
    if not ots_available():
        return None
    mp = Path(manifest_path)
    subprocess.run(["ots", "stamp", str(mp)], check=True)
    proof = mp.with_name(mp.name + ".ots")
    return proof if proof.exists() else None


def git_committed_time(path: Union[str, Path]) -> Optional[str]:
    """ISO time of the last git commit touching ``path`` (the external timestamp once pushed),
    or None if the file is uncommitted or git is unavailable."""
    p = Path(path)
    cwd = str(p.parent) if str(p.parent) not in ("", ".") else "."
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", p.name],
            cwd=cwd, capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    ts = out.stdout.strip()
    return ts or None


@dataclass
class AnchorResult:
    ok: bool
    checks: List[str] = field(default_factory=list)
    problems: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.ok


def verify_anchor(
    ledger_path: Union[str, Path],
    manifest_path: Optional[Union[str, Path]] = None,
) -> AnchorResult:
    """Check the current ledger against its anchor manifest, and the chain itself.

    Detects chain breaks (via :meth:`Ledger.verify`), a changed head (entries appended or
    removed since anchoring), and any change to the file bytes (``file_sha256``).
    """
    lp = Path(ledger_path)
    mp = Path(manifest_path) if manifest_path else manifest_path_for(lp)
    checks: List[str] = []
    problems: List[str] = []

    chain = Ledger(lp).verify()
    if chain.ok:
        checks.append(f"chain integrity OK ({chain.n_entries} entries)")
    else:
        problems.extend(chain.problems)

    if not mp.exists():
        problems.append(f"no anchor manifest at {mp.name} (run `anchor` first)")
        return AnchorResult(ok=False, checks=checks, problems=problems)

    manifest = json.loads(mp.read_text(encoding="utf-8"))
    head, n = ledger_head(lp)

    if manifest.get("head_entry_hash") == head:
        checks.append("head_entry_hash matches the anchored head")
    else:
        problems.append("head_entry_hash differs from the anchor -- the ledger changed since anchoring")
    if manifest.get("n_entries") == n:
        checks.append(f"n_entries matches ({n})")
    else:
        problems.append(f"n_entries differs from the anchor ({manifest.get('n_entries')} -> {n})")
    if manifest.get("file_sha256") == _file_digest(lp):
        checks.append("file digest matches the anchor")
    else:
        problems.append("file_sha256 differs from the anchor -- the ledger bytes changed since anchoring")

    return AnchorResult(ok=not problems, checks=checks, problems=problems)

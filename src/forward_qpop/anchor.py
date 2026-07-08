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

## External anchor (WI-19)

The two helpers above prove tamper-evidence and give a *local* manifest, but neither, by
itself, is a publicly verifiable "this existed before time T" claim unless you also push the
commit or hold onto the ``.ots`` proof yourself. :func:`external_anchor` /
:func:`verify_external_anchor` add a submission step against a public, append-only service and
record the outcome in a small JSON sidecar (``<ledger>.external-anchor.json``) next to the
ledger, so the claim ("we submitted this digest to this service at this time") is itself
inspectable and versioned alongside the ledger.

**Route chosen: OpenTimestamps.** Two candidates were evaluated:

* **OpenTimestamps** -- stamp the manifest head digest via the ``ots`` CLI
  (``opentimestamps-client``, an optional extra). Pure stdlib ``subprocess`` call, no
  cryptography dependency, and the repo already has the local ``ots_stamp`` scaffolding this
  builds on. Honest caveat: the Bitcoin attestation is *not* instant -- a fresh stamp is
  "submitted" (pending calendar-server aggregation into a Bitcoin block, which takes hours);
  run ``ots upgrade`` later to pull down the completed attestation.
* **Sigstore/Rekor** (hashedrekord) -- would give an inclusion proof + log index immediately,
  but requires constructing a signed ``hashedrekord`` entry with an ephemeral keypair, which
  pulls in ``cryptography``/``sigstore`` (a materially heavier dependency) for a payload this
  project doesn't otherwise need (no code signing).

OpenTimestamps wins on dependency weight and reuses existing scaffolding; the tradeoff is a
submitted-not-yet-confirmed status window instead of Rekor's immediate log inclusion. Given the
paper's own framing ("a recommended deployment step," not a blocking claim of correctness), the
weaker immediacy is an acceptable, honestly-disclosed cost.

``external_anchor`` never silently claims success: a network failure raises
:class:`ExternalAnchorError` and no sidecar is written (or, if partially written, its
``status`` is never ``submitted``/``confirmed``).
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Union

from .ledger import GENESIS, Ledger

ANCHOR_SCHEMA = "forward-qpop/anchor@1"
EXTERNAL_ANCHOR_SCHEMA = "forward-qpop/external-anchor@1"
EXTERNAL_ANCHOR_METHODS = ("ots",)


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


# --------------------------------------------------------------------------------------
# External anchor (WI-19): submit the local manifest's head digest to a public,
# append-only timestamp service (OpenTimestamps) and record the outcome in a sidecar.
# --------------------------------------------------------------------------------------


class ExternalAnchorError(RuntimeError):
    """Raised on any external-anchor failure -- degradation is always loud, never silent."""


def external_anchor_path_for(ledger_path: Union[str, Path]) -> Path:
    p = Path(ledger_path)
    return p.with_name(p.name + ".external-anchor.json")


class _OTSBackend:
    """Real backend: shells out to the `ots` CLI (``opentimestamps-client``, optional extra)."""

    service = "OpenTimestamps (opentimestamps.org)"

    def submit(self, digest_hex: str) -> dict:
        if not ots_available():
            raise ExternalAnchorError(
                "`ots` binary not found on PATH -- install the optional extra with "
                "`pip install forward-qpop[anchor]` (wraps `opentimestamps-client`)."
            )
        with tempfile.TemporaryDirectory() as td:
            digest_file = Path(td) / "digest.sha256"
            digest_file.write_bytes(bytes.fromhex(digest_hex))
            try:
                subprocess.run(
                    ["ots", "stamp", "-d", str(digest_file)],
                    capture_output=True, text=True, check=True, timeout=60,
                )
            except FileNotFoundError as exc:
                raise ExternalAnchorError(f"`ots` binary not found on PATH: {exc}") from exc
            except subprocess.TimeoutExpired as exc:
                raise ExternalAnchorError(
                    f"OpenTimestamps calendar server(s) unreachable or slow (timed out): {exc}"
                ) from exc
            except subprocess.CalledProcessError as exc:
                raise ExternalAnchorError(
                    f"`ots stamp` failed (exit {exc.returncode}): {exc.stderr or exc.stdout}"
                ) from exc
            proof = digest_file.with_name(digest_file.name + ".ots")
            if not proof.exists():
                raise ExternalAnchorError("`ots stamp` reported success but wrote no .ots proof file.")
            return {"receipt_b64": base64.b64encode(proof.read_bytes()).decode("ascii")}


def external_anchor(
    ledger_path: Union[str, Path],
    method: str = "ots",
    manifest_path: Optional[Union[str, Path]] = None,
    sidecar_path: Optional[Union[str, Path]] = None,
    backend: Optional[object] = None,
) -> Path:
    """Submit the ledger's anchored head digest to a public, append-only timestamp service.

    Requires the local anchor manifest to already exist (run :func:`build_manifest` /
    :func:`write_manifest`, or the ``anchor`` CLI command, first) -- the manifest is what
    fixes *what* is being anchored; this submits that fixed digest externally.

    On any failure (unknown method, missing manifest, network error, missing ``ots``
    binary) this raises :class:`ExternalAnchorError` and writes NO sidecar claiming
    success -- callers must not treat a raised exception as "anchored anyway."

    ``backend`` is injectable for testing (must expose ``.submit(digest_hex) -> dict`` and
    a ``.service`` attribute); defaults to the real OpenTimestamps backend.
    """
    if method not in EXTERNAL_ANCHOR_METHODS:
        raise ExternalAnchorError(
            f"unknown external-anchor method {method!r}; supported: {EXTERNAL_ANCHOR_METHODS}"
        )

    lp = Path(ledger_path)
    mp = Path(manifest_path) if manifest_path else manifest_path_for(lp)
    if not mp.exists():
        raise ExternalAnchorError(
            f"no local anchor manifest at {mp.name} -- run `anchor` (build_manifest/write_manifest) first"
        )
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    digest = manifest.get("head_entry_hash")
    if not digest:
        raise ExternalAnchorError(f"manifest at {mp.name} has no head_entry_hash")

    be = backend if backend is not None else _OTSBackend()
    submitted_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        receipt = be.submit(digest)
    except ExternalAnchorError:
        raise
    except Exception as exc:  # noqa: BLE001 -- any backend/network failure, surfaced loudly
        raise ExternalAnchorError(f"external anchor submission failed ({method}): {exc}") from exc

    sidecar = {
        "schema": EXTERNAL_ANCHOR_SCHEMA,
        "ledger": lp.name,
        "method": method,
        "service": getattr(be, "service", method),
        "digest_sha256": digest,
        "submitted_at": submitted_at,
        "status": "submitted",
        "receipt": receipt,
        "note": (
            "status='submitted' means the digest was accepted by the service, not yet "
            "confirmed on-chain/in-log -- for OpenTimestamps, run `ots upgrade` later and "
            "re-run `verify-external` once the Bitcoin attestation completes (hours)."
        ),
    }
    sp = Path(sidecar_path) if sidecar_path else external_anchor_path_for(lp)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(sidecar, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sp


def verify_external_anchor(
    ledger_path: Union[str, Path],
    sidecar_path: Optional[Union[str, Path]] = None,
) -> AnchorResult:
    """Check the external-anchor sidecar's digest against the *current* ledger head.

    A mismatch means the ledger moved (or was rewritten) since the external submission --
    the same "loud, not silent" contract as :func:`verify_anchor`, one level up: this is
    tamper/rewrite evidence relative to the externally-timestamped commitment, not just the
    local manifest.
    """
    lp = Path(ledger_path)
    sp = Path(sidecar_path) if sidecar_path else external_anchor_path_for(lp)
    checks: List[str] = []
    problems: List[str] = []

    chain = Ledger(lp).verify()
    if chain.ok:
        checks.append(f"chain integrity OK ({chain.n_entries} entries)")
    else:
        problems.extend(chain.problems)

    if not sp.exists():
        problems.append(f"no external anchor sidecar at {sp.name} (run `anchor external` first)")
        return AnchorResult(ok=False, checks=checks, problems=problems)

    sidecar = json.loads(sp.read_text(encoding="utf-8"))
    if sidecar.get("status") not in ("submitted", "confirmed"):
        problems.append(f"external anchor sidecar status is {sidecar.get('status')!r}, not submitted/confirmed")
        return AnchorResult(ok=False, checks=checks, problems=problems)

    head, _ = ledger_head(lp)
    if sidecar.get("digest_sha256") == head:
        checks.append(f"external anchor digest matches the current ledger head (method={sidecar.get('method')})")
    else:
        problems.append(
            "external anchor digest_sha256 differs from the current ledger head -- "
            "the ledger changed since the external submission"
        )

    return AnchorResult(ok=not problems, checks=checks, problems=problems)

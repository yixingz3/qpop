"""forward_qpop — a tamper-evident, append-only forward pre-registration ledger.

Register a hypothesis (a claim + dated evidence + measurable exit triggers + a prior)
*before* the evaluation window opens. Each entry is content-hashed over its frozen
fields and chained to its predecessor, so the record proves **what was predicted, and
when** — and any later edit, insertion, deletion, or reorder is detectable.

This is the domain-agnostic core of the "Forward-QPOP" protocol from the methods paper
*Forward-Registered, Auditable LLM-Assisted Research* — usable for any pre-registered
research, not only the finance testbed in the paper.

Pure standard library; no third-party dependencies.
"""
from .anchor import (
    AnchorResult,
    ExternalAnchorError,
    build_manifest,
    external_anchor,
    external_anchor_path_for,
    git_committed_time,
    ledger_head,
    manifest_path_for,
    ots_available,
    verify_anchor,
    verify_external_anchor,
    write_manifest,
)
from .ledger import (
    ADMISSION,
    BELIEF_UPDATE,
    GENESIS,
    OUTCOME,
    TERMINAL_STATUSES,
    IntegrityError,
    Ledger,
    VerifyResult,
    content_hash,
    entry_hash,
    verify_file,
)

__all__ = [
    "Ledger",
    "VerifyResult",
    "IntegrityError",
    "content_hash",
    "entry_hash",
    "verify_file",
    "ADMISSION",
    "BELIEF_UPDATE",
    "OUTCOME",
    "TERMINAL_STATUSES",
    "GENESIS",
    "AnchorResult",
    "build_manifest",
    "write_manifest",
    "verify_anchor",
    "manifest_path_for",
    "ledger_head",
    "ots_available",
    "git_committed_time",
    "ExternalAnchorError",
    "external_anchor",
    "external_anchor_path_for",
    "verify_external_anchor",
]

__version__ = "0.1.2"

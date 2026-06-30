#!/usr/bin/env python3
"""Show the ledger's tamper-evidence end to end in ~3 seconds.

    python repro/tamper_demo.py

Copies the synthetic sample ledger to a scratch file, verifies it (OK), edits one frozen
field while leaving the stored hashes untouched, verifies again (FAILS), and reports. No
third-party dependencies; exits 0 on the expected behavior, non-zero if tamper-evidence did
NOT trigger.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))  # run from a clone without installing

from forward_qpop import verify_file  # noqa: E402

SAMPLE = ROOT / "data" / "synthetic" / "qpop_ledger_sample.jsonl"
_CANON = dict(sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def main() -> int:
    scratch = Path(tempfile.mkdtemp()) / "ledger.jsonl"
    scratch.write_text(SAMPLE.read_text(encoding="utf-8"), encoding="utf-8")

    clean = verify_file(scratch)
    print(f"1. clean ledger:   ok={clean.ok}  ({clean.n_entries} entries)")
    if not clean.ok:
        print("   unexpected: the shipped sample should verify clean")
        return 1

    lines = scratch.read_text(encoding="utf-8").splitlines()
    obj = json.loads(lines[0])
    obj["claim"] = obj.get("claim", "") + " (secretly edited)"  # tamper, keep stored hashes
    lines[0] = json.dumps(obj, **_CANON)
    scratch.write_text("\n".join(lines) + "\n", encoding="utf-8")

    tampered = verify_file(scratch)
    print(f"2. after edit:     ok={tampered.ok}  problems={len(tampered.problems)}")
    for prob in tampered.problems:
        print(f"     - {prob}")

    if tampered.ok:
        print("\nFAIL: tamper-evidence did NOT trigger.")
        return 1
    print("\nPASS: editing one frozen field broke the chain, exactly as designed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

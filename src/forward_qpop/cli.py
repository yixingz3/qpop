"""Command-line interface: ``forward-qpop verify|show <ledger.jsonl>``.

``verify`` exits non-zero on an integrity failure, so it can gate CI — proving a
pre-registration ledger has not been tampered with since it was written.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .ledger import Ledger, verify_file


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="forward-qpop",
        description="Forward-QPOP pre-registration ledger — verify integrity or list entries.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("verify", help="Verify a ledger's integrity (content hashes + chain).")
    pv.add_argument("path", help="Path to a JSONL ledger.")

    ps = sub.add_parser("show", help="List the entries in a ledger.")
    ps.add_argument("path", help="Path to a JSONL ledger.")

    args = parser.parse_args(argv)

    if args.cmd == "verify":
        res = verify_file(args.path)
        if res.ok:
            print(f"OK — {res.n_entries} entries, integrity verified.")
            return 0
        print(f"INTEGRITY FAILURE — {res.n_entries} entries, {len(res.problems)} problem(s):")
        for prob in res.problems:
            print("  - " + prob)
        return 1

    if args.cmd == "show":
        for e in Ledger(args.path).entries():
            status = e.get("status", e.get("outcome", ""))
            claim = (e.get("claim", "") or "")[:64]
            print(f"{e.get('id', '?'):18} {e.get('type', '?'):14} {status:10} {claim}")
        return 0

    return 2  # unreachable: subparser is required


if __name__ == "__main__":
    sys.exit(main())

"""Command-line interface for the Forward-QPOP ledger.

  forward-qpop verify   <ledger.jsonl>
  forward-qpop show     <ledger.jsonl>
  forward-qpop register <ledger.jsonl> --json '<entry>'   # or entry on stdin
  forward-qpop update   <ledger.jsonl> --json '<entry>'
  forward-qpop close    <ledger.jsonl> --id <id> --outcome supported|weakened|falsified [--observed '<json>']
  forward-qpop anchor   <ledger.jsonl> [--ots] [--manifest <path>]
  forward-qpop verify-anchor <ledger.jsonl> [--manifest <path>]

`register`/`update` take a JSON object so an agent can drive a tamper-evident pre-registration
ledger from the command line. `verify` exits non-zero on an integrity failure (gate CI).
`anchor` writes a manifest committing to the ledger head so it can be bound to an external
timestamp (a public commit, or OpenTimestamps); `verify-anchor` detects drift since anchoring.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from .anchor import build_manifest, git_committed_time, ots_stamp, verify_anchor, write_manifest
from .ledger import Ledger, TERMINAL_STATUSES, verify_file


def _load_json(arg: Optional[str]) -> dict:
    raw = arg if arg is not None else sys.stdin.read()
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise SystemExit("expected a JSON object")
    return obj


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="forward-qpop",
        description="Forward-QPOP pre-registration ledger — register, verify, and inspect a "
                    "tamper-evident, hash-chained record of forward predictions.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("verify", help="Verify a ledger's integrity (content hashes + chain).")
    pv.add_argument("path")

    psh = sub.add_parser("show", help="List the entries in a ledger.")
    psh.add_argument("path")

    pr = sub.add_parser("register", help="Pre-register a hypothesis (JSON: id, claim, "
                                         "[mechanism, prior, evidence, exit_triggers, role_admitted, created, fields]).")
    pr.add_argument("path")
    pr.add_argument("--json", default=None, help="JSON object; if omitted, read from stdin.")

    pu = sub.add_parser("update", help="Record a belief update (JSON: id, evidence, [fields, allow_tertiary_only]).")
    pu.add_argument("path")
    pu.add_argument("--json", default=None, help="JSON object; if omitted, read from stdin.")

    pc = sub.add_parser("close", help="Close a hypothesis with a pre-committed outcome.")
    pc.add_argument("path")
    pc.add_argument("--id", required=True)
    pc.add_argument("--outcome", required=True, choices=list(TERMINAL_STATUSES))
    pc.add_argument("--observed", default=None, help="JSON object of observed metrics.")

    pa = sub.add_parser("anchor", help="Write an anchor manifest committing to the ledger head.")
    pa.add_argument("path")
    pa.add_argument("--manifest", default=None, help="Manifest path (default: <ledger>.anchor.json).")
    pa.add_argument("--ots", action="store_true", help="Also OpenTimestamps-stamp the manifest if `ots` is installed.")

    pva = sub.add_parser("verify-anchor", help="Verify the ledger against its anchor manifest (and the chain).")
    pva.add_argument("path")
    pva.add_argument("--manifest", default=None, help="Manifest path (default: <ledger>.anchor.json).")

    args = p.parse_args(argv)

    if args.cmd == "verify":
        res = verify_file(args.path)
        if res.ok:
            print(f"OK — {res.n_entries} entries, integrity verified.")
            return 0
        print(f"INTEGRITY FAILURE — {res.n_entries} entries, {len(res.problems)} problem(s):")
        for prob in res.problems:
            print("  - " + prob)
        return 1

    led = Ledger(args.path)

    if args.cmd == "show":
        for e in led.entries():
            status = e.get("status", e.get("outcome", ""))
            claim = (e.get("claim", "") or "")[:64]
            print(f"{e.get('id', '?'):18} {e.get('type', '?'):14} {status:10} {claim}")
        return 0

    if args.cmd == "register":
        d = _load_json(args.json)
        e = led.register(
            d["id"], d["claim"],
            mechanism=d.get("mechanism", ""),
            evidence=d.get("evidence"),
            exit_triggers=d.get("exit_triggers"),
            prior=d.get("prior"),
            role_admitted=d.get("role_admitted"),
            created=d.get("created"),
            fields=d.get("fields"),
        )
        print(f"registered {e['id']}  entry_hash={e['entry_hash'][:16]}…")
        return 0

    if args.cmd == "update":
        d = _load_json(args.json)
        e = led.update(
            d["id"], evidence=d["evidence"],
            fields=d.get("fields"),
            allow_tertiary_only=bool(d.get("allow_tertiary_only", False)),
        )
        print(f"updated {e['id']}  entry_hash={e['entry_hash'][:16]}…")
        return 0

    if args.cmd == "close":
        observed = json.loads(args.observed) if args.observed else {}
        e = led.close(args.id, args.outcome, observed=observed)
        print(f"closed {e['id']} -> {args.outcome}")
        return 0

    if args.cmd == "anchor":
        m = build_manifest(args.path)
        mp = write_manifest(args.path, args.manifest, manifest=m)
        print(f"anchored {m['n_entries']} entries  head={m['head_entry_hash'][:16]}...")
        print(f"  manifest: {mp}")
        gt = git_committed_time(args.path)
        if gt:
            print(f"  git: ledger last committed {gt} (push to a public remote = external timestamp)")
        else:
            print("  git: ledger not committed yet -- commit + push the ledger and manifest to anchor in time")
        if args.ots:
            proof = ots_stamp(mp)
            if proof:
                print(f"  ots: stamped -> {proof}")
            else:
                print("  ots: opentimestamps-client not installed (pip install opentimestamps-client); stamp later")
        return 0

    if args.cmd == "verify-anchor":
        res = verify_anchor(args.path, args.manifest)
        for c in res.checks:
            print(f"  OK  {c}")
        for prob in res.problems:
            print(f"  XX  {prob}")
        print("anchor OK" if res.ok else "ANCHOR MISMATCH")
        return 0 if res.ok else 1

    return 2  # unreachable: subparser is required


if __name__ == "__main__":
    sys.exit(main())

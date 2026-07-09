"""Command-line interface for the Forward-QPOP ledger.

  forward-qpop verify   <ledger.jsonl>
  forward-qpop show     <ledger.jsonl>
  forward-qpop register <ledger.jsonl> --json '<entry>'   # or entry on stdin
  forward-qpop update   <ledger.jsonl> --json '<entry>'
  forward-qpop close    <ledger.jsonl> --id <id> --outcome supported|weakened|falsified [--observed '<json>']
  forward-qpop anchor   <ledger.jsonl> [--ots] [--manifest <path>]
  forward-qpop verify-anchor <ledger.jsonl> [--manifest <path>]
  forward-qpop anchor external <ledger.jsonl> [--method ots] [--manifest <path>] [--sidecar <path>]
  forward-qpop verify-external <ledger.jsonl> [--sidecar <path>]
  forward-qpop evalue   <ledger.jsonl> [--alpha 0.05] [--state <path>] [--json] [--out <path>] [--no-persist]

`anchor external ...` is sugar for `anchor ... --external ...`: `main()` rewrites a leading
["anchor", "external", ...] argv into ["anchor", "...", "--external", "ots", ...] before
argparse sees it, so both spellings work identically.

`register`/`update` take a JSON object so an agent can drive a tamper-evident pre-registration
ledger from the command line. `verify` exits non-zero on an integrity failure (gate CI).
`anchor` writes a manifest committing to the ledger head so it can be bound to an external
timestamp (a public commit, or OpenTimestamps); `verify-anchor` detects drift since anchoring.
`anchor external` submits that manifest's head digest to a public, append-only timestamp
service (OpenTimestamps by default) and records the outcome in a `<ledger>.external-anchor.json`
sidecar; `verify-external` checks that sidecar's digest against the current ledger head. A
network failure exits non-zero with a clear message -- it never silently claims anchored.
`evalue` replays each hypothesis's `trigger_checks` (belief_update entries) through its
pre-registered `SequentialTriggerTest` (the `"evalue"` admission config) and reports the
merged e-value, the `1/alpha` threshold, and the decision; state resumes across runs from a
`<ledger>.evalue-state.json` sidecar (never mutates the ledger) -- see
`research/docs/EVALUE_METHODS.md` for the wiring.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Sequence

from .anchor import (
    ExternalAnchorError,
    build_manifest,
    external_anchor,
    git_committed_time,
    ots_stamp,
    verify_anchor,
    verify_external_anchor,
    write_manifest,
)
from .evalue import FALSIFIED, EvalueLedgerError, EvalueReportRow, run_ledger_evalue
from .ledger import Ledger, TERMINAL_STATUSES, verify_file


def _load_json(arg: Optional[str]) -> dict:
    raw = arg if arg is not None else sys.stdin.read()
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise SystemExit("expected a JSON object")
    return obj


def _rewrite_anchor_external(argv: Sequence[str]) -> List[str]:
    """Rewrite ["anchor", "external", ...] into ["anchor", ..., "--external", <method>].

    Lets `forward-qpop anchor external <ledger> [--method ots] [...]` (the WI-19 spec's
    literal CLI shape) and `forward-qpop anchor <ledger> --external ots [...]` (the flag
    form on the existing `anchor` subcommand) both dispatch to the same handler.
    """
    argv = list(argv)
    if len(argv) >= 2 and argv[0] == "anchor" and argv[1] == "external":
        rest = argv[2:]
        method = "ots"
        cleaned: List[str] = []
        i = 0
        while i < len(rest):
            if rest[i] == "--method" and i + 1 < len(rest):
                method = rest[i + 1]
                i += 2
                continue
            cleaned.append(rest[i])
            i += 1
        return ["anchor"] + cleaned + ["--external", method]
    return argv


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = _rewrite_anchor_external(sys.argv[1:] if argv is None else argv)
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
    pa.add_argument(
        "--external", default=None, metavar="METHOD", choices=["ots"], dest="method",
        help="Submit the manifest head digest to a public timestamp service (currently: ots) "
             "and write a <ledger>.external-anchor.json sidecar. Non-zero exit + clear message "
             "on any network/tooling failure -- never silently claims anchored. "
             "(`anchor external <path> --method ots` is equivalent sugar for this flag.)",
    )
    pa.add_argument("--sidecar", default=None, help="External-anchor sidecar path (default: <ledger>.external-anchor.json).")

    pva = sub.add_parser("verify-anchor", help="Verify the ledger against its anchor manifest (and the chain).")
    pva.add_argument("path")
    pva.add_argument("--manifest", default=None, help="Manifest path (default: <ledger>.anchor.json).")

    pve = sub.add_parser(
        "verify-external",
        help="Verify the ledger against its external-anchor sidecar (digest match against the current head).",
    )
    pve.add_argument("path")
    pve.add_argument("--sidecar", default=None, help="External-anchor sidecar path (default: <ledger>.external-anchor.json).")

    pev = sub.add_parser(
        "evalue",
        help="Run the anytime-valid sequential trigger test over a ledger's registered hypotheses.",
    )
    pev.add_argument("path")
    pev.add_argument("--alpha", type=float, default=0.05, help="Type-I error bound; falsified iff e-value >= 1/alpha (default: 0.05).")
    pev.add_argument("--state", default=None, help="State sidecar path (default: <ledger>.evalue-state.json).")
    pev.add_argument("--json", dest="as_json", action="store_true", help="Print the report as JSON instead of a table.")
    pev.add_argument("--out", default=None, help="Also write the JSON report to this path.")
    pev.add_argument("--no-persist", dest="no_persist", action="store_true", help="Compute the report without writing/updating the state sidecar (dry run).")

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
        if args.method:
            try:
                sp = external_anchor(args.path, method=args.method, manifest_path=args.manifest, sidecar_path=args.sidecar)
            except ExternalAnchorError as exc:
                print(f"  external anchor FAILED ({args.method}): {exc}")
                return 1
            print(f"  external anchor: submitted via {args.method} -> {sp}")
            print("    status=submitted (not yet confirmed on-chain -- re-run `ots upgrade` + `verify-external` later)")
        return 0

    if args.cmd == "verify-anchor":
        res = verify_anchor(args.path, args.manifest)
        for c in res.checks:
            print(f"  OK  {c}")
        for prob in res.problems:
            print(f"  XX  {prob}")
        print("anchor OK" if res.ok else "ANCHOR MISMATCH")
        return 0 if res.ok else 1

    if args.cmd == "verify-external":
        res = verify_external_anchor(args.path, args.sidecar)
        for c in res.checks:
            print(f"  OK  {c}")
        for prob in res.problems:
            print(f"  XX  {prob}")
        print("external anchor OK" if res.ok else "EXTERNAL ANCHOR MISMATCH")
        return 0 if res.ok else 1

    if args.cmd == "evalue":
        try:
            rows, _state = run_ledger_evalue(
                args.path, alpha=args.alpha, state_path=args.state, persist=not args.no_persist,
            )
        except (EvalueLedgerError, ValueError) as exc:
            print(f"evalue FAILED: {exc}")
            return 1
        report = [r.to_dict() for r in rows]
        if args.out:
            outp = Path(args.out)
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.as_json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            _print_evalue_report(rows, args.alpha)
        return 0  # a "falsified" decision is a valid outcome, not a command failure

    return 2  # unreachable: subparser is required


def _print_evalue_report(rows: List[EvalueReportRow], alpha: float) -> None:
    print(f"e-value sequential trigger test -- alpha={alpha}, threshold(1/alpha)={1.0 / alpha:.4f}")
    print(f"{'ID':20} {'STATUS':10} {'E-VALUE':>12} {'DECISION':10} {'LEDGER-OUTCOME':15}")
    for r in rows:
        outcome = r.ledger_outcome or "open"
        if r.status != "ok":
            print(f"{r.id:20} {r.status:10} {'--':>12} {'--':10} {outcome:15}")
            continue
        falsified_flag = " *" if r.decision == FALSIFIED else ""
        print(f"{r.id:20} {r.status:10} {r.e_value:12.4f} {r.decision:10} {outcome:15}{falsified_flag}")


if __name__ == "__main__":
    sys.exit(main())

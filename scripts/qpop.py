#!/usr/bin/env python3
"""Launcher so the bundled Forward-QPOP ledger CLI runs without a pip install.

The qpop plugin skills call this. It adds the bundled `src/` to sys.path and dispatches to
`forward_qpop.cli`. Works inside Claude Code (where $CLAUDE_PLUGIN_ROOT is set) or from a plain
clone of the repo (falls back to the repo root relative to this file).

Usage:
  python scripts/qpop.py verify   ledger.jsonl
  python scripts/qpop.py register ledger.jsonl --json '{...}'
  python scripts/qpop.py close    ledger.jsonl --id H-01 --outcome supported
"""
import os
import sys

_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "src"))

from forward_qpop.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

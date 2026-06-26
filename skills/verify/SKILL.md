---
name: verify
description: Verify a Forward-QPOP ledger's integrity — recompute every content hash and the entry chain to detect any post-hoc edit, insertion, deletion, or reorder. Use to prove a pre-registration record was not tampered with. Exits non-zero on failure (CI-friendly).
disable-model-invocation: false
argument-hint: "[ledger.jsonl]"
---

# Verify ledger integrity

```bash
python "$CLAUDE_PLUGIN_ROOT/scripts/qpop.py" verify "${1:-ledger.jsonl}"
```

Report the result. A failure means either a frozen field was edited (content-hash mismatch) or an
entry was inserted / deleted / reordered (chain break) after the fact — name the exact entry and the
specific problem so the user can see what changed. (Outside a plugin context: `python scripts/qpop.py verify …`.)

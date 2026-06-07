#!/usr/bin/env bash
# check_sync_drift.sh — report which PRIVATE generic-source docs changed since the last sync.
# It ONLY hashes the generic docs listed in scripts/sync_manifest.tsv; it never reads live state
# (the scored map, the QPOP ledger, broker code). See docs/SYNC.md.
#
# Usage:  PRIVATE_REPO=/path/to/systematic-trading-project ./scripts/check_sync_drift.sh
#    or:  ./scripts/check_sync_drift.sh /path/to/systematic-trading-project
#
# Exit 0 = in sync; exit 1 = drift found (propagate the sanitized lesson, then update the manifest hash).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$HERE/scripts/sync_manifest.tsv"
PRIVATE_REPO="${1:-${PRIVATE_REPO:-}}"

if [[ -z "$PRIVATE_REPO" ]]; then
  echo "ERROR: set PRIVATE_REPO (env or first arg) to the private repo root." >&2
  exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
  echo "ERROR: sha256sum not found." >&2; exit 2
fi

drift=0; checked=0; missing=0
while IFS=$'\t' read -r priv pub base || [[ -n "$priv" ]]; do
  [[ -z "$priv" || "${priv:0:1}" == "#" ]] && continue
  f="$PRIVATE_REPO/$priv"
  if [[ ! -f "$f" ]]; then
    echo "MISSING  $priv  (not found under PRIVATE_REPO; manifest may be stale)"; missing=$((missing+1)); continue
  fi
  cur="$(sha256sum < "$f" | cut -d' ' -f1)"   # read via stdin: avoids GNU filename-escaping on Windows paths
  checked=$((checked+1))
  if [[ "$cur" != "$base" ]]; then
    echo "DRIFT    $priv  ->  $pub"
    echo "         baseline=$base"
    echo "         current =$cur"
    drift=$((drift+1))
  else
    echo "ok       $priv"
  fi
done < "$MANIFEST"

echo "---"
echo "checked=$checked  drift=$drift  missing=$missing"
if [[ $drift -gt 0 ]]; then
  echo "ACTION: review each DRIFT doc; if a GENERIC concept changed, propagate the SANITIZED lesson to"
  echo "        its public counterpart (docs/SYNC.md), then update the baseline hash in scripts/sync_manifest.tsv."
  exit 1
fi
echo "In sync."

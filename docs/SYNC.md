# Sync — keeping the public framework current with the private implementation

This public repo (`chokepoint-research-engine`) is the **method**. The live implementation
(`systematic-trading-project` / `ai-sid`) is **private**. As the private iteration improves a
*generic* concept, the lesson is propagated here — **sanitized**. As live *state* changes, nothing
moves. This doc is the contract for what flows, what never flows, and how.

## Direction of flow

```
PRIVATE (ai-sid live impl)  ──[generalize + sanitize]──▶  PUBLIC (this repo)
   live map / positions / ledger / broker / paid data        generic engine, schema, disciplines, paper
```

Flow is **one-way** (private → public) and **concept-only**. The public repo never sends anything to
the private repo, and the public repo never receives live state.

## What flows (propagate when it changes privately)

| Private source (ai-sid) | Public counterpart | Sanitize how |
|---|---|---|
| `RESEARCH_RULES.md`, `docs/CANDIDATE_PROCESS.md`, `docs/SCOREBOARD.md`, `docs/TUNING.md`, QPOP protocol | `docs/RESEARCH_RULES.md`, `docs/CANDIDATE_PROCESS.md`, `docs/SCOREBOARD.md`, `docs/TUNING.md`, `docs/QPOP_PROTOCOL.md` | generalize "ai-sid" → "the framework"; drop AI-specific node names where generic; keep the *discipline*, drop the *positions* |
| the discovery funnel / model-allocation logic | `docs/METHOD.md`, `docs/TUNING.md`, `src/README.md` | describe the mechanism, not the live config values |
| `bottleneck_map.yml` **structure** (new fields, new schema) | `examples/template_domain/bottleneck_map.template.yml`, `src/README.md` | template only — **never** the live scored map |
| new mechanisms / findings (e.g. policy-as-evidence, per-entry probation, structural-vs-cyclical) | `docs/METHOD.md`, `paper/*` | the generalized lesson + (for the paper) aggregate metrics |
| engine code, as it is generalized out of the private impl | `src/<module>/` | strip broker/account specifics; tests use `data/synthetic/` only |

## What NEVER flows (private-only, hard line)

- The live `bottleneck_map.yml` with real tickers / scores / weights / positions.
- The live QPOP ledger (`outputs/hyp_logs/`), `DISCOVERY_QUEUE.md` state, shadow-PnL snapshots, the
  rebalance log, any trade or PnL record.
- Broker / Alpaca code, `.env`, API keys, repo secrets, paid-data exports, course materials.
- Anything that reads as "here are trades to copy." Forward results, if ever published, go out as
  **aggregated** discipline/performance statistics (see `SCOREBOARD.md`), never as positions.

`.gitignore` enforces the obvious cases; the human enforces the judgment cases. **When in doubt, it
stays private.**

## Process (per sync)

1. Run the drift check (`scripts/check_sync_drift.sh`) pointed at the private repo — it reports which
   *generic-source* docs changed since the last sync (it never reads live state).
2. For each changed generic source, decide: does the change affect a *generic* concept? If yes,
   propagate the **sanitized** lesson to the public counterpart (table above). If it's live state, skip.
3. Re-run the citation verification if the paper's claims changed (`WRITING_STANDARDS.md`).
4. Commit the public update; update the sync baseline (`scripts/sync_manifest.tsv`) to the private
   repo's current commit for the files you propagated.
5. Bump `CITATION.cff` version on a meaningful release; tag + (optionally) mint a Zenodo DOI.

## Cadence

Sync on a *concept change*, not on every private commit. A good trigger: when a private PR changes a
discipline, the schema, or adds a mechanism (the kind of change that would alter `METHOD.md`). Most
private commits (a new admission, a queue update, a snapshot) change only *state* and sync nothing.

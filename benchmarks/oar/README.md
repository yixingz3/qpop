# OAR benchmark — v0 pilot

> **Status: v0 pilot — 2-domain, aggregate-only, from existing preserved material.** This is not
> the v1 public benchmark. The full design (task format, ground-truth protocol, anti-leakage
> analysis, domain expansion plan, release governance) is
> [`research/docs/OAR_BENCHMARK_DESIGN_WORKING.md`](../../research/docs/OAR_BENCHMARK_DESIGN_WORKING.md)
> — that document is the spec this package implements the v0 stage of; read it first for anything
> this README doesn't answer. Roadmap: **v0 (this)** → v0.5 (constructed planted-bait + blinded
> perturbation, ML-eval control domain, blinded multi-auditor lane) → v1 (public dataset +
> leaderboard, community pack-contribution protocol) → v2 (settled-outcome validation against the
> paper's forward-scoring registry).

`qpop`'s methods paper measures the **over-admission rate (OAR)** — the share of a candidate set an
ablated or ungated process admits that a disciplined reference would reject — in one domain and
names a multi-domain benchmark as future work. v0 ships the shared task-format spec, the
domain-pack pattern, an offline ablation harness, and the monotone discipline curve as the
reference, built entirely from **material that already exists and is already public** in this
repo. No new forward data was collected and no LLM is called anywhere in this package.

## What ships

```
benchmarks/oar/
  schemas/
    domain_pack.schema.json         # the "meta.domain" profile (pack-level metadata)
    aggregate_results.schema.json   # a pack's recorded ablation-arms batch OR funnel-run counts
    oar_report.schema.json          # the harness's output report
  packs/
    ai_supply_chain/                # the 38-card ablation pilot -- the discipline-curve reference
      domain_pack.json
      aggregate_results.json
      README.md
    uranium/                        # the config-only domain-swap demo (H3 clause c)
      domain_pack.json
      aggregate_results.json
      README.md
  loader.py      # load + schema-validate a pack
  scoring.py     # pure functions: admission rate, OAR, rejection precision, discipline curve
  harness.py     # CLI: render the discipline-curve artifact (text or JSON), no plotting deps
```

**Card format**: reused verbatim, not redefined. Any per-card content a future pack ships (v0.5's
constructed/perturbed sets) uses the already-released
[`schemas/candidate_card.schema.json`](../../schemas/candidate_card.schema.json),
[`evidence.schema.json`](../../schemas/evidence.schema.json), and
[`exit_trigger.schema.json`](../../schemas/exit_trigger.schema.json) as-is (design doc Sec 2). The
three schemas in `benchmarks/oar/schemas/` cover only the pack-level and report-level formats that
don't exist yet anywhere else in the repo.

## How to run

```bash
pip install jsonschema   # optional -- soft dependency, same posture as schemas/README.md

python -m benchmarks.oar.harness --list
python -m benchmarks.oar.harness ai_supply_chain
python -m benchmarks.oar.harness ai_supply_chain --format json
python -m benchmarks.oar.harness uranium
```

Or from Python:

```python
from benchmarks.oar import load_pack, discipline_curve, assert_monotone_nonincreasing

pack = load_pack("ai_supply_chain")
curve = discipline_curve(pack.aggregate_results)
assert_monotone_nonincreasing(curve)
```

### Sample artifact — `python -m benchmarks.oar.harness ai_supply_chain`

```text
OAR benchmark v0 -- domain: ai_supply_chain
provenance: recorded_real_funnel_pilot_batch
aggregate-only: true (no per-card content)

discipline curve (least- to most-disciplined arm):
  ungated_screener     admit=100.0%   OAR=100.0%   Ungated LLM screener (no discipline)
  no_bear_case_first   admit= 73.7%   OAR= 73.7%   - bear-case-first
  no_overlap_penalty   admit= 65.8%   OAR= 65.8%   - overlap penalty
  no_forward_lock      admit= 40.8%   OAR= 40.8%   No Forward-QPOP lock (pending arm c)
  debate_only          admit= 36.8%   OAR= 36.8%   Debate-only, bull/bear judge, no forward lock (pending arm b)
  full_pipeline        admit=  0.0%   OAR=  0.0%   Full pipeline (gate + seen-set + triage + bear-case-first + overlap + forward lock)

rejection precision: raw=0.775 (n=40, justified=31, CI95=[0.625, 0.877])  |  adjudicated=1.000 (n=9, upheld=9)
```

The rendered rates (73.7%, 65.8%, 40.8%, 36.8%) are the exact figures; the design doc's
"74% / 66% / ~41% / ~37%" are the rounded headline numbers for the same sequence — both round-trip
to the identical `100 → 74 → 66 → 41 → 37 → 0` ordering (see
`tests/test_oar_discipline_curve.py::test_discipline_curve_reproduces_the_recorded_ordering`).

## Aggregate-only vs per-card — and why

**Both v0 packs are aggregate-only. Neither ships a single per-card record.** This is not a
simplification of scope — it is the design doc's own stated fallback ("if per-card data is NOT
public, the pack ships the schema + arm RESULTS as fixtures, clearly labeled aggregate-level").

- **`ai_supply_chain`** — the 38-candidate identities, symbols, and per-card admit/reject decisions
  for every arm live in the private research repo (`examples/ai_supply_chain/README.md` and
  `src/prompts.md` §8 both say so explicitly). What *is* public and what this pack fixtures: the
  admit **count** per arm (38, 28, 25, ~15.5 mean, ~14 mean, 0 — out of 38), replicate agreement for
  the two multi-replicate arms, and the H5 rejection-quality-audit precision (raw n=40 documented
  draw + the adjudicated escalation), all sourced straight from
  `research/docs/RESULTS_V2_WORKING.md`.
- **`uranium`** — the live bottleneck map, tickers, and per-card decisions are private; what's
  public is the funnel **stage counts** from the one real run (20 sourced → 10 unique symbols → 8
  gate-pass → 4 triage-pursue → 1 admit-flag/2 watchlist/1 reject → 1 adjudicated-upheld), from the
  same source doc's H3 clause (c) section. No ablation arms exist for this domain in v0.

**Why OAR is still exactly computable from the aggregate for `ai_supply_chain`.** The disciplined
reference (`full_pipeline`) admitted **0 of 38**. A reference that admits nothing rejects the entire
pool, so every card any ablated arm admits is, by construction, an over-admission relative to that
reference — OAR (normalized by the *fixed* candidate-set size, not the arm's own variable admit
count, per the design doc's "fixed admission budget" framing) collapses to the arm's own admission
rate. `scoring.py::oar_from_aggregate_zero_reference` asserts this precondition explicitly (it
raises if handed a nonzero reference) rather than assuming it silently, and
`scoring.py::compute_oar` is the fully general per-card version any future pack with a nonzero
reference (or real per-card labels) will need instead. `uranium` has no ablation arms at all, so no
OAR is reported for it.

## Privacy boundary

**Public (this package):** the task-format schemas, the domain-pack pattern, the scoring harness,
and the recorded aggregate results (admission counts/rates, replicate agreement, the H5 audit
precision, and funnel-stage counts) for both v0 packs.

**Never released, here or anywhere in this repo (design doc Sec 6 / `DISCLAIMER.md` / `ETHICS.md`):**
the live engine, live positions, broker/paid data, or per-card live-book content — symbols, company
names, per-card admit/reject decisions, and the bottleneck maps that would identify them all stay
in the private research repo. Nothing in this package required or used any of it: every number
here traces to an already-published, already-sanitized line in `research/docs/RESULTS_V2_WORKING.md`,
`src/prompts.md`, or `examples/ai_supply_chain/README.md`.

## Tests

`tests/test_oar_schemas.py`, `test_oar_scoring.py`, `test_oar_discipline_curve.py`,
`test_oar_loader.py` — hermetic, fixture-driven, no network, run under the repo's normal
`python -m pytest -q`. They cover: schema validation (both packs, the harness report, and a
reuse-not-redefine check against the released card schemas), scorer math on hand-computable
fixtures (including a from-scratch reproduction of the published Wilson confidence intervals for
the H5 audit), and exact reproduction of the recorded discipline curve and its monotonicity.

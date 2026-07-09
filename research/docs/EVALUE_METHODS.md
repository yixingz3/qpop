# Anytime-valid sequential trigger test (paper §7 Decision Rules)

*Implements the decision rule the paper commits to: outcome decisions over many exit
triggers and positions use a sequential test with explicit Type-I error control (an
anytime-valid / e-value formulation from the safe-testing literature), so that monitoring
many triggers across many positions does not inflate false "Falsified" calls.* Module:
[`src/forward_qpop/evalue.py`](../../src/forward_qpop/evalue.py); tests:
[`tests/test_evalue.py`](../../tests/test_evalue.py) (the standalone e-process, 18 tests)
and [`tests/test_evalue_ledger.py`](../../tests/test_evalue_ledger.py) (the ledger wiring,
17 tests — see [§"How the ledger integrates it"](#how-the-ledger-integrates-it-wi-29-wired-2026-07-09) below).

## The problem it solves

A Forward-QPOP position is judged against **several** pre-registered exit triggers, and
each trigger is re-checked at **every** monitoring step. Calling a thesis *Falsified* the
first time any check fires — and re-checking after every step — is a repeated-looks
multiple-comparisons problem: it inflates the false-"Falsified" rate exactly like the
factor-zoo problem, here in its *prospective, continuously-monitored* form. A fixed-n
significance test does not license peeking after every observation; an **anytime-valid**
test does.

## The null model and the bet

Per trigger, register — **before** the evaluation window — a binary null and a point
alternative for the per-step fire probability:

- **H0 (thesis holds):** `P(fire) <= p0` — the trigger rarely/never fires if the thesis
  is right.
- **H1 (thesis broken):** `P(fire) = p1`, with `p1 > p0`.

At each observation `fired ∈ {True, False}` we multiply a running **betting martingale**
(an *e-process*) by the likelihood ratio of the point alternative over the null boundary
`p0`:

```
fired      ->  e *= p1 / p0
not fired  ->  e *= (1 - p1) / (1 - p0)
```

Under H0 with per-step fire probability exactly `p0`, the per-step expected multiplier is

```
E[LR | fire ~ Bernoulli(p0)] = p0 * (p1/p0) + (1-p0) * ((1-p1)/(1-p0)) = p1 + (1-p1) = 1,
```

so `e_n` is a **nonnegative martingale with `E[e_n] = 1`**; for any `P(fire) < p0` it is a
**supermartingale** (`E[e_n] <= 1`).

## Ville's inequality → anytime-valid Type-I control

Because `e_n` is a nonnegative (super)martingale starting at 1, **Ville's inequality**
gives, for any `α ∈ (0, 1)`,

```
P_H0( sup_n e_n >= 1/α ) <= α.
```

So the decision rule

> call **Falsified** only when `e >= 1/α`, otherwise **continue**

controls the Type-I (false-"Falsified") error at `α` **at any stopping time** — continuous
monitoring and optional stopping included. You may re-evaluate `decision(α)` after every
trigger check and still keep the false-"Falsified" rate at `α`. This is exactly the
guarantee a fixed-sample test lacks.

**Simulation check (in the test suite).** Under the null (`p0 = 0.15`, `p1 = 0.6`,
4 triggers, horizon 60, `α = 0.10`), across 400 optional-stopping paths that stop the
instant the rule would fire, the empirical false-"Falsified" rate is **0.050**
(averaging) / **0.0375** (product) — both `<= α`. Under a true alternative
(`P(fire) = p1`) the test falsifies on **100/100** paths (power sanity).

## Combining triggers and positions

E-values merge cleanly, and the merge choice is a dependence assumption:

- **product** — valid when the component e-processes are **independent**; the product is
  again an e-process (`E[∏] <= 1` under the joint null).
- **average** (arithmetic mean) — **the default** — is a valid e-value under **arbitrary
  dependence** between the component e-values (Vovk & Wang: the arithmetic average is the
  admissible symmetric merge of arbitrarily-dependent e-values).

Exit triggers on one position — and across positions in one theme — are typically
**correlated** (a supply shock trips several at once). Product would double-count that
shared evidence and break Type-I control; averaging stays valid regardless of the
dependence structure. We therefore **default to averaging** and expose product only for
the genuinely-independent case, to be chosen explicitly at the call site.

## How the ledger integrates it (WI-29, wired 2026-07-09)

The exit triggers are already the pre-registered contract in the admission entry
(`exit_triggers`, see [`schemas/exit_trigger.schema.json`](../../schemas/exit_trigger.schema.json)).
The sequential test rides on top of that contract via two additive, schema-compatible
fields (neither requires a breaking schema change — the ledger's `admission` /
`belief_update` entry variants don't set `additionalProperties: false`, so both are
ordinary domain-specific payload, hashed like every other frozen field):

1. **At registration** — pass `p0`, `p1`, and the combiner as a top-level `"evalue"`
   field via `fields`:

   ```python
   led.register(
       "H-1", "claim", ...,
       exit_triggers=[{"id": "supply_easing", "metric": "...", "op": "reverses",
                       "data_source": {"tier": "secondary"}}],
       fields={"evalue": {"p0": 0.1, "p1": 0.6, "combine": "average"}},
   )
   ```

   This is the pre-registration commitment: `p0`/`p1`/`combine` are frozen into the
   admission entry's content hash, so they cannot be tuned after the window opens.
2. **At each monitoring step** — record a belief_update with a top-level
   `"trigger_checks"` field mapping the triggers checked this step to whether they fired:

   ```python
   led.update("H-1", evidence=[...], fields={"trigger_checks": {"supply_easing": False}})
   ```

   Every trigger id named here must already be in the admission's `exit_triggers`
   contract — an unregistered id is a loud `EvalueLedgerError`, not a silent no-op.
3. **`forward-qpop evalue <ledger.jsonl>`** (or `run_ledger_evalue()` from Python) walks
   the ledger, replays each hypothesis's `trigger_checks` stream through its own
   `SequentialTriggerTest`, and reports the merged e-value, the `1/α` threshold
   (`--alpha`, default `0.05`), and the decision (`continue` / `falsified`). Hypotheses
   with no `"evalue"` config are reported as `no_config` — **skipped, not fabricated**.
4. **State resumes across invocations, never mutating the ledger.** Each run persists
   `SequentialTriggerTest.to_state()` plus the last-processed `entry_hash` per hypothesis
   in a JSON **sidecar** (`<ledger>.evalue-state.json` by default — `--state` to
   override). The next run loads that sidecar via `SequentialTriggerTest.from_state()`
   and folds in only the belief_update entries appended since, so the anytime-valid
   guarantee holds across repeated command invocations, not just within one process. If
   the ledger is ever rewritten/truncated out from under a sidecar (its recorded
   `last_entry_hash` can no longer be found), the command fails loudly rather than
   silently re-deriving or double-counting.
5. **The decision is advisory, not self-executing.** A `"falsified"` report is a signal
   for the operator (or an automation) to `close(id, "falsified", observed={...})` with
   the e-value and per-trigger state recorded in `observed` — `run_ledger_evalue` never
   calls `close()` itself. If the window ends without crossing `1/α`, the outcome is
   still decided by the other pre-registered gates (Supported / Weakened), never by an
   after-the-fact narrative.

```bash
forward-qpop evalue ledger.jsonl                       # table report, default alpha=0.05
forward-qpop evalue ledger.jsonl --alpha 0.1 --json     # JSON report to stdout
forward-qpop evalue ledger.jsonl --out report.json      # also write the JSON report to a file
forward-qpop evalue ledger.jsonl --no-persist            # dry run: compute, don't touch the sidecar
```

Tests: [`tests/test_evalue_ledger.py`](../../tests/test_evalue_ledger.py) — fresh run,
resumed run (state round-trip, including "resume matches a from-scratch replay"),
falsified-at-threshold, and five loud-failure cases (missing `p0`/`p1`, malformed
`trigger_checks`, unregistered trigger id, invalid `alpha`, rewritten-ledger/sidecar
mismatch), plus CLI-level table/JSON/`--out`/failure-exit-code coverage.

## Limitations (v1)

- **Binary checks only** — fired / not-fired per step. A metric-valued or
  one-sided-mean (test-supermartingale) formulation is future work.
- **`p0`, `p1` must be pre-registered** — fixed in the admission entry before the window,
  never tuned to observed data. A point alternative (fixed `p1`) is the simplest
  calibrated GRO-style bet; a mixture / plug-in over `p1` is a documented future
  extension.
- **Directionality** — the null is "the trigger rarely fires if the thesis holds," so the
  test accrues evidence *against* the thesis as fires accumulate. Triggers whose *absence*
  falsifies a thesis must be encoded so that the falsifying event is the "fire."
- **`alpha` is a report-time parameter, not a frozen one** — `decision(alpha)` (and the CLI's
  `--alpha`) can be re-evaluated at any threshold without touching the ledger, matching
  Ville's inequality (valid at any `alpha` simultaneously); it is not itself hashed into
  the admission entry the way `p0`/`p1`/`combine` are. Treat the reporting `alpha` as
  operationally pre-registered in the surrounding process (e.g. a fixed project-wide
  default) rather than picked after seeing the data.
- **The `"evalue"` / `"trigger_checks"` fields are a convention, not schema-enforced** —
  `schemas/qpop_entry.schema.json` permits them (no `additionalProperties: false` at the
  top level) but doesn't require or validate their shape; malformed input is caught by
  `run_ledger_evalue`'s own checks (`EvalueLedgerError`), not by JSON Schema validation.

## References (mark for citation-verification before paper use)

- Ramdas, A., Grünwald, P., Vovk, V., & Shafer, G. (2023). *Game-Theoretic Statistics and
  Safe Anytime-Valid Inference.* Statistical Science 38(4), 576–601. arXiv:2210.01948.
  (e-processes, Ville's inequality, anytime-valid Type-I control.)
- Shafer, G. (2021). *Testing by Betting: A Strategy for Statistical and Scientific
  Communication.* Journal of the Royal Statistical Society, Series A, 184(2), 407–431.
  (the betting-martingale framing of a test.)
- Vovk, V., & Wang, R. (2021). *E-values: calibration, combination and applications.*
  Annals of Statistics 49(3), 1736–1754. (arithmetic averaging as the admissible merge of
  arbitrarily-dependent e-values — the dependence-safe combiner used here.)

*Citation-verification note: titles, authors, venues, volumes and page ranges above were
drafted from the implementer's knowledge and should be verified against the primary
sources before they enter `research/paper/`.*

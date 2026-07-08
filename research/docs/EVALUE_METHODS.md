# Anytime-valid sequential trigger test (paper §7 Decision Rules)

*Implements the decision rule the paper commits to: outcome decisions over many exit
triggers and positions use a sequential test with explicit Type-I error control (an
anytime-valid / e-value formulation from the safe-testing literature), so that monitoring
many triggers across many positions does not inflate false "Falsified" calls.* Module:
[`src/forward_qpop/evalue.py`](../../src/forward_qpop/evalue.py); tests:
[`tests/test_evalue.py`](../../tests/test_evalue.py).

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

## How the ledger integrates it

The exit triggers are already the pre-registered contract in the admission entry
(`exit_triggers`, see [`schemas/exit_trigger.schema.json`](../../schemas/exit_trigger.schema.json)).
The sequential test rides on top of that contract:

1. **At registration** — fix `p0`, `p1`, `α`, and the combiner in the admission entry
   (they are pre-registration parameters, hashed like every other frozen field). A
   `SequentialTriggerTest(p0, p1, combine)` is instantiated with empty state.
2. **At each monitoring step** — for every trigger whose contract was checked, call
   `test.observe(trigger_id, fired)`. The per-entry test state is a plain dict from
   `test.to_state()` and is persisted alongside the entry (round-trips via
   `SequentialTriggerTest.from_state`), so monitoring can resume across runs.
3. **At close** — `test.decision(α)` returns `"falsified"` iff the merged e-value crosses
   `1/α`; the ledger's `close(id, "falsified", observed={...})` records the terminal
   outcome with the e-value and per-trigger state in `observed`. If the window ends
   without crossing, the outcome is decided by the other pre-registered gates
   (Supported / Weakened), never by an after-the-fact narrative.

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

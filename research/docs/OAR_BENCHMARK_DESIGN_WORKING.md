# OAR multi-domain benchmark — design working draft (WI-23)

> **Status: WORKING DRAFT — scoping/design only, no benchmark code yet.** Design notes for the
> long-term follow-up to the Forward-QPOP methods paper (`research/paper/`). This document is the
> scoping artifact the paper's own §Results "Over-admission rate as a reusable benchmark" paragraph
> calls for: *"a multi-domain OAR benchmark — many candidate sets, blinded auditors, and a shared
> task format — is future work, and an explicit invitation to build on this release."* It commits to
> nothing final; section numbers, the domain list, and the ground-truth protocol will move as the
> pilot is built. Aggregates cited here are the sanitized, already-published numbers from
> `RESULTS_V2_WORKING.md` and the paper — no live positions, weights, returns, or per-card content.

Last updated: 2026-07-09.

---

## 1. Motivation and positioning

The Forward-QPOP paper names a quantity and proposes it as portable: the **over-admission rate
(OAR)** — for a candidate set, *the share an ablated or ungated process admits but the full
discipline rejects*. The paper measures it in one domain (capital markets) and explicitly invites a
multi-domain benchmark. This document scopes that benchmark.

**What existing agent benchmarks measure vs what OAR measures.** The dominant agentic-evaluation
axis is **capability / task completion**: did the agent finish the task, pass the test, reach the
goal (SWE-bench, WebArena, GAIA, tool-use and coding suites). These reward *doing more, correctly*.
OAR measures the opposite-signed failure — **epistemic restraint under adversarial-plausibility
pressure**: when an agent is handed a stream of plausible-but-weak research candidates, how often
does it *admit* one that a disciplined process would *reject*? A capability benchmark punishes an
agent for not acting; an OAR benchmark punishes it for acting when the correct action is "no action."
The paper's headline — *the modal outcome is rejection* — is precisely the behavior no
task-completion benchmark can score, because completion frameworks have no notion of a candidate that
*should* be refused.

**Relation to POPPER-style hypothesis validation.** Recent work on automated hypothesis validation
(sequential/e-value control of false discovery over agent-proposed hypotheses) is the closest
neighbor: both treat an LLM as a *proposer* whose outputs must clear a falsification-style gate
before they count. OAR is complementary and one level up — it is not a single-hypothesis validity
test but a **workflow-reliability metric**: given the same candidate set, it scores how much a
pipeline's admissions are inflated by *removing* individual disciplines. The two compose cleanly: the
paper already wires an anytime-valid e-process (`forward-qpop evalue`) as the per-hypothesis Type-I
control, and OAR sits above it as the aggregate over-admission measure across a whole batch.

**Why finance was a good first testbed, and why the metric is domain-general.** Markets are a
*deliberately adversarial* substrate: they punish wishful thinking, settled outcomes are unambiguous,
and the "touches the theme ≠ owns the chokepoint" trap is dense. That density is exactly what makes
finance a hard first testbed — but nothing in the OAR definition is financial. The paper's own
formulation table maps `candidate → (method, benchmark) claim`, `realization vehicle → model /
dataset / config`, `admit → pre-register the eval claim` for an ML-evaluation setting, and ships a
non-finance worked example (`examples/ml_benchmark/`). Over-admission — *accepting a weak claim as if
it held* — is the same failure mode in a literature review, an ML-eval report, or a due-diligence
memo. The benchmark's job is to make that portability measurable rather than asserted.

## 2. Task format spec

A benchmark instance is a **domain pack** plus a **candidate set**; a submission runs its agent over
the set and emits a decision per card. The formats reuse the released schemas verbatim
(`schemas/candidate_card.schema.json`, `evidence.schema.json`, `exit_trigger.schema.json`,
`qpop_entry.schema.json`).

**Candidate card** (the unit an agent consumes — already a released schema):
- `claim` + `realization vehicle` — a falsifiable proposition paired with how one would act on it
  (a security, a model/dataset/config, a policy, etc.).
- `evidence[]` — dated facts, each tiered `primary > secondary > market_implied > tertiary`
  (tertiary is idea-seed only and can never move a conclusion alone).
- `known_risks` / `missing_info` — the strongest case against, stated up front.
- **falsifiable exit triggers** — each a `{metric, op, threshold, data_source}` with a *checkable*
  tier; an admission that names a trigger you cannot verify is itself a defect.

**Decision space** — `{reject, watchlist, admit}`. `admit` additionally requires a **forward-locked
contract**: the claim + dated evidence + exit triggers, hash-chained to the append-only ledger
*before* any outcome window (the Forward-QPOP admission entry). `watchlist` is the calibrated middle:
"interesting, with a dated trigger" rather than "commit now." The paper's ablation evidence shows the
staged funnel largely converts plausible names into *watchlist* rather than *admit* — so watchlist
calibration is a first-class scored quantity, not a dumping ground.

**What a domain pack consists of** — the `meta.domain` profile pattern, *proven portable by the
uranium config-only swap* (`RESULTS_V2_WORKING.md`, H3 clause (c)). A pack is a single config file
carrying:
- `name` / `domain_label` — machine name + a short human label for prompt example-asides.
- `thesis_frame` — the one-line framing the SOURCE/EVALUATE prompts specialize to.
- `example-sets` — `gaps_examples`, `social_sources`, `literature_examples`,
  `critical_input_examples`: the domain-specific fill-ins that thread through the (unmodified) prompt
  constructors.
- a node list (`bottleneck_map.yml`) naming the chokepoint layers.

The load-bearing claim, demonstrated once already: swapping this one file re-frames the entire funnel
with **zero prompt-construction code edits** (byte-identical golden tests on the live config;
sentinel check that no generated prompt contains a first-domain string). A domain pack is therefore a
*data artifact*, which is what makes a community-contributed multi-domain benchmark feasible.

**Ground-truth protocol — how over-admission is adjudicated.** OAR needs a per-card label: *should a
disciplined process reject this?* Three provenances, in decreasing leakage-safety:
- **Constructed** — planted over-admission bait with a known label by construction (see §3c).
- **Adjudicated** — a **blinded, multi-auditor lane**: independent auditors see the steelmanned bull
  case and the decision but *not* the engine's bear case, and label each `justified / false-rejection`
  with a category. This is the paper's rejection-quality audit generalized. Every `false-rejection`
  flag escalates to a **capital-at-risk adjudication analog** — an expensive, full-record re-judge
  that can uphold the rejection (the cheap-screen → expensive-adjudicate asymmetry applied to the
  audit itself, and it fires in *both* directions: it catches over-admission and over-caution).
- **Settled** — eventual forward outcomes (see §3a); the gold standard, but slow and leakage-exposed
  for real names.

**The H5 lesson, baked into the protocol as a hard requirement.** The paper's own audit expansion is
the cautionary tale: the pilot n=14 agreement headline (0.93) did *not* survive a documented n=40 draw
(bull-only auditor agreement 0.775, naive Wilson [0.625, 0.877]); the full-record adjudicator
overriding all nine flags (9/9) is an *escalation diagnostic under asymmetric information, not
ground truth* (terminology revised 2026-07-23 per the v2 review — see
`../paper/arxiv/revise_log.md`). The benchmark therefore mandates: (i) **documented, seeded,
content-hash-verifiable sampling**
(no undocumented membership); (ii) **pre-committed gates** locked before the set is scored; and
(iii) **both the raw auditor-agreement rate and the post-escalation resolution reported, clearly
labeled as disagreement metrics** — never collapse to the flattering
post-adjudication number, and never present same-system adjudication as ground truth. A submission
that reports only an "effective" precision fails validation.

## 3. Anti-leakage / anti-gaming design (the hard problem — stated honestly)

This is the design's central difficulty, and the paper is unusually blunt about why. For an
LLM-scored engine a **backward test is structurally invalid, not merely noisy**, and three properties
defeat it, each sufficient alone: (i) no information is injected backward — retrodicting historical
names measures the model's *hindsight*; (ii) the labels are already in the model — settled outcomes
sit in the pretraining corpus, so there is no clean train/test split; and (iii) **the features *are*
the fingerprint** — the very attributes the engine scores (which chokepoint, what purity, whose
capacity) uniquely identify the company and hence its known outcome, so anonymizing inputs cannot
restore a blind test. This is the *forward-scoring-registry insight*: any candidate set built from
already-settled real names is void as a leakage-clean OAR measurement, because the scoreable
attributes are the identifying fingerprint. A benchmark that ignores this is measuring recall of
training data, not restraint.

Four design options, with trade-offs:

**(a) Forward-only cohorts that settle after model cutoffs.** Freeze candidate sets and decisions
now; let outcomes settle *after* every evaluated model's knowledge cutoff. *Pro:* the only fully
clean route to *settled-outcome* ground truth; it is the paper's own approach (the forward-scoring
registry). *Con:* slow (multi-year, quarters-to-cohort), low throughput, and every new model release
re-opens the cutoff question.

**(b) Post-cutoff event windows per model.** Restrict each model's candidate set to events dated
after *that* model's cutoff. *Pro:* faster than (a), keeps some real-world realism. *Con:* inherits
the retrodiction invalidity the moment outcomes settle and a model is re-released over the window;
per-model set fragmentation makes cross-model comparison ragged; hard to keep honest at scale.
**Not recommended as a primary.**

**(c) Synthetic-but-grounded candidate sets with planted over-admission bait.** Author candidate sets
where the label is known *by construction*: each set mixes genuine chokepoint candidates with planted
traps drawn from the **transferred rejection taxonomy** — low-purity-conglomerate (theme-toucher),
pre-revenue hype, commodity price-taker, foreign/no-domestic-vehicle, priced-in/crowded, and
competitor-mislabeled-as-supplier. *Pro:* fully leakage-immune (no settled outcome exists), cheap to
scale across domains, gives a fixed known OAR label per card, and directly stress-tests
adversarial-plausibility (a well-built trap is *plausible*). *Con:* synthetic cards risk being *too
easy* or not capturing real adversarial texture — mitigated by grounding every trap in a real
taxonomy pattern and hardening with (d).

**(d) Blinded perturbation of real cards.** Take real rejected/admitted cards and perturb the
identifying surface (swap tickers/names, shift dates, mask the issuer) while preserving the
decision-relevant structure. *Pro:* real-world texture without the settled-outcome fingerprint. *Con:*
imperfect de-identification — a strong model may re-identify from residual structure — so it hardens
(c) rather than standing alone.

**Recommendation — primary + fallback.**
- **Primary: (c) planted-bait synthetic-but-grounded sets, hardened with (d) blinded perturbation.**
  OAR is fundamentally a *relative, adjudicable* metric (full discipline vs ablated arm on the *same*
  set) and does *not* require settled forward outcomes — it requires a known "should-reject" label,
  which construction provides directly and leakage-immune. This is the only option that is
  simultaneously scalable, repeatable across arbitrary domains, and clean against the
  features-are-the-fingerprint problem. The rejection taxonomy is the recipe book for authoring
  plausible bait.
- **Fallback / gold-standard anchor: (a) forward-only cohorts.** Reserved for the legs that genuinely
  need settled reality — rejection precision against *eventual* outcomes and the forward-contract
  falsification rate. Slow but clean; runs on the multi-year cadence of the paper's forward-scoring
  registry and validates that constructed/adjudicated OAR tracks settled OAR.
- **Explicitly rejected as primary: (b).** It re-imports the retrodiction invalidity the paper spends
  a full subsection dismantling.

## 4. Domain inventory and expansion plan

**Existing material (already run through the real funnel; sanitized aggregates published).**

| Domain | Status | Substrate | Ground-truth notes |
|---|---|---|---|
| AI supply chain | Live; ~300+ cards aggregate across build-out rounds | Physical | Forward cohort seeded (registry); dense trap population |
| Uranium fuel cycle | Demonstrated pack (config-only swap) | Physical | Full funnel run; taxonomy transferred unprompted |
| Pharma injectables / GLP-1 delivery | Probe (2nd domain, H3) | Physical | 0-admit; canonical closure chokepoint located |
| Launch / satellite-internet supply chain | Probe (3rd domain) | Physical | 0-admit; surfaced a new bypass mode (customer in-sourcing) |
| Proprietary-data / network monopolies | Probe (4th substrate, backtest-stage) | **Non-physical** | Labeled historical dislocations (forced-seller vs recognition) |
| ML-eval claims (`examples/ml_benchmark`) | Released worked example | **Non-finance** | Ground truth is *reproducible by re-running the eval* |

**Proposed additional domains (3–5), mixing physical/non-physical and finance/non-finance.**

1. **Grid interconnection & HV power equipment** (physical, finance). Multi-year-lead-time chokepoints
   (large-power transformers, interconnection-queue equipment). *Rationale:* an exceptionally dense
   theme-toucher population (every industrial conglomerate "touches" the grid), ideal for planted
   bait; forward cohorts feasible off capex/lead-time disclosures.
2. **Rare-earth separation & refining** (physical, finance). Separation/refining capacity, not mining.
   *Rationale:* the miner-vs-refiner confusion is a textbook purity trap; strong (c)-bait domain,
   moderate forward-cohort feasibility.
3. **Data / network monopolies** (non-physical, finance) — *promote the existing probe to a full pack*.
   *Rationale:* the strongest **non-physical** substrate test; ground truth is harder (no physical
   lead-time metronome), but the forced-seller-vs-recognition distinction already yields *labeled
   historical dislocations* for the backtest-style leg.
4. **ML-research / eval-reproducibility claims** (non-physical, non-finance) — *generalize
   `ml_benchmark` into a pack*. Candidates are `(method, benchmark)` claims; over-admission = accepting
   a weak eval claim (seed-cherry-picking, look-ahead tuning, post-hoc metric selection). *Rationale:*
   **the cleanest anti-leakage domain in the inventory** — ground truth is settled by *actually running
   the eval*, a fast, reproducible experiment the model cannot have memorized as an outcome. Serves as
   the benchmark's **control domain**.
5. *(situational 5th)* **Advanced packaging / HBM** or a **biosecurity fill-finish** domain — both are
   physical chokepoints with rich trap populations; hold as expansion candidates once the pilot
   harness is stable.

Per-domain ground-truth feasibility is scored on three axes when a pack is admitted: forward-cohort
feasibility, planted-bait feasibility, and settled-outcome leakage exposure. The ML-eval domain is the
outlier — low leakage, fast settlement — and is deliberately included as the honest-ground-truth
anchor against which the harder domains' constructed labels are sanity-checked.

## 5. Metrics and scoring harness sketch

**Primary metric.** **OAR at a fixed admission budget** — the share of a candidate set a pipeline
admits that a disciplined reference would reject, read straight from the ablation contrast on the
*same* set (identical cards, model id, temperature; only the discipline differs). Fixing the
admission budget prevents gaming by trivially admitting nothing.

**Secondary metrics.**
- **Rejection precision (raw + adjudicated, both reported).** Guards against the "reject everything"
  degenerate — a low OAR is only meaningful if the rejections are *justified*. Raw is primary;
  adjudicated is a secondary resolution figure, never the headline (the H5 discipline).
- **Watchlist calibration.** How well the middle tier separates "watch with a dated trigger" from
  "commit" — measured against the constructed labels and, where available, forward triggers.
- **Forward-contract falsification rate.** For admitted cards, how often the pre-committed exit
  triggers fire against settled data — the forward-only leg (§3a).

**Reporting.** Per-domain *and* pooled, with the **observed discipline-contrast ordering as a
descriptive reference "discipline curve"** (sorted post hoc; the arms are non-nested interventions,
so the curve is not a dose-response and carries no causal claim — wording revised 2026-07-23 per the
v2 review). The paper's own observed ordering, with the two v2 arms inserted, is
`100% → 74% → 66% → ~41% → ~37% → 0%` (ungated → −bear-case-first → −overlap → no-contract/lock →
debate-only → full pipeline). A submission reports its own arms' ordering for comparison; the
endpoint gap is the quantitative (reference-relative) OAR.

**What the harness reuses vs what is new.**
- *Reuses (already in the released `forward_qpop` package):* the hash-chained **ledger**
  (`ledger.py`) for forward-locked admission contracts; the **e-value** anytime-valid trigger test
  (`evalue.py`) for the falsification leg; the **anchor** (`anchor.py`, OpenTimestamps) to prove sets
  and decisions predate outcomes; the **JSON Schemas** for cards/entries; the **prompt templates**
  (`src/prompts.md`, incl. the five §8 ablation arms) as the reference discipline arms; the
  deterministic gate reference (`src/gate_reference.md`).
- *New (to be built):* a **candidate-set author/validator** (constructed-bait + perturbation
  tooling with label manifests); a **scoring harness** that runs an arbitrary agent over a pack,
  collects `{reject, watchlist, admit}` + contracts, and computes OAR / precision / calibration; the
  **blinded multi-auditor lane** runner; and the **leaderboard aggregator** (per-domain + pooled,
  with CIs). None of this touches the private engine — it consumes the released contracts only.

## 6. Release plan and governance

**Release boundary (mirrors the paper's honesty).** Released: **domain packs, schemas, the scoring
harness, candidate sets (constructed + perturbed), and aggregate results/leaderboard.** Never
released: the **live engine**, live positions, broker/paid data, or per-card live-book content — the
same firm boundary the paper's reproducibility table draws.

**Dataset / leaderboard shape.** A versioned dataset of domain packs + candidate sets (with label
manifests for constructed cards, held-out for forward-cohort cards), and a leaderboard reporting
per-domain and pooled OAR + raw/adjudicated rejection precision + watchlist calibration, with
confidence intervals and the discipline-curve plot per submission.

**Versioning.** Semantic pack versions; candidate-set membership content-hash-pinned and anchored so
a set provably predates any model it scores; a dated changelog for taxonomy/bait revisions.

**Community contribution protocol for new domain packs.** A pack PR ships: the `meta.domain` profile +
node list, a candidate set with a label manifest, the ground-truth-provenance declaration (constructed
/ adjudicated / settled), and a passing golden test that the unmodified prompt constructors produce
domain-framed prompts with zero code edits (the uranium swap is the reference). Blinded-auditor
credentials and constructed-label keys are held out of the public set to prevent overfitting to
answers.

**Staged roadmap.**
- **v0 — 2-domain pilot, from existing material.** AI supply chain + uranium (both already run through
  the real funnel; sanitized aggregates exist). Ships the shared task-format spec, the domain-pack
  pattern, the ablation harness reading OAR straight from the released package, and the monotone
  discipline curve as the reference. No new forward data required — reuses preserved batches.
- **v0.5 — leakage-clean expansion.** Add constructed planted-bait sets + blinded perturbation; add
  the ML-eval control domain (clean, fast ground truth); wire the blinded multi-auditor lane and the
  raw+adjudicated dual report.
- **v1 — public benchmark.** 4–5 domains; public dataset + leaderboard; community pack-contribution
  protocol live; forward-cohort anchor seeded (settles at the v2 horizon). Live engine stays private.
- **v2 — settled-outcome validation.** Forward-cohort read-out validates that constructed/adjudicated
  OAR tracks settled OAR; depends on the paper's H4 December read-out + forward-scoring-registry first
  cohort.

## 7. Relationship to paper v2 and the follow-up paper

**One-paragraph outline of the benchmark paper.** *Claim:* OAR paired with rejection precision is a
**portable, adversarial reliability benchmark for agentic research** — it measures epistemic restraint
under plausibility pressure, a failure mode orthogonal to the capability/task-completion axis existing
agent benchmarks score. *Evidence it needs:* (i) ≥4 domains spanning physical/non-physical and
finance/non-finance, each reproducing the monotone discipline curve; (ii) a leakage-clean
ground-truth protocol (primary: constructed + perturbed; anchored by forward cohorts) that survives
the features-are-the-fingerprint objection; (iii) **multi-agent** runs — the benchmark's point is that
it scores *any* agent's over-admission, not just this engine, so at least a handful of external agents
must be run over the shared packs; and (iv) the H5 discipline throughout (documented seeded samples,
pre-committed gates, raw+adjudicated both reported).

**Dependency on the v2 / H4 December read-out.** The benchmark can *launch* on constructed +
adjudicated ground truth without waiting — that is the whole point of the (c)-primary recommendation.
But its strongest claim — *constructed/adjudicated OAR tracks settled forward OAR* — is gated on the
paper v2 H4 forward read-out and the forward-scoring-registry first cohort (roughly two quarters out
from the paper's declared timeline, ~2026-12). Until that read-out, the benchmark paper reports OAR
against constructed and adjudicated ground truth and declares the settled-outcome validation as
pending — the same forward-first honesty the methods paper models.

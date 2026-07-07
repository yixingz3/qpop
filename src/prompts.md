# Reference prompts (the disciplines, as templates)

These are the load-bearing prompts of the funnel, sanitized to the generic framework (no live
positions, no broker calls, no paid-data text). The experiment plan commits to publishing the prompts
by reference; this is that reference. The exact production strings are versioned in the private
implementation and pinned by commit hash per run (see `../research/docs/RESULTS_INITIAL.md` → implementation
details). `{...}` are fill-ins.

## 0. Research contract (prepended to every LLM stage)

> Source tiers: PRIMARY (filings, transcripts, official guidance, peer-reviewed research) > SECONDARY
> (reputable trade press; arXiv/SSRN preprints — flag "preprint") > MARKET-IMPLIED (price/volume) >
> TERTIARY (social — idea seed only; corroborate with ≥ secondary, never establishes confidence). A
> cited paper must be VERIFIED (its identifier resolves to the claimed title + author) before it can
> support anything — never cite from memory; a paper is mechanism/prior evidence, not a buy signal.
> "No stories": every claim rests on a verifiable DATED fact; if you cannot verify with a dated
> source, say so in `missing_info`. Thesis = PHYSICAL, hard-to-bypass chokepoints; the decision
> standard is "does this IMPROVE the book?", not "is this on-theme?". Tradeable-universe only;
> foreign-only listings are context, not candidates. Current book: {held map}. Already covered (skip
> unless a material dated change): {seen set}.

## 1. SOURCE (cheap model, one lens per node + gap/social/policy/literature)

> You are the `{lens}` sourcing lens (as of {date}). High-volume, low-judgment: collect candidate
> CARDS with dated, source-tiered evidence; do NOT make final allocation decisions. {lens-specific
> instruction}. For each: the physical chokepoint it monetizes; direct / second-order / adjacent;
> dated source-tiered evidence; known risks; missing info. If it overlaps a held name, set
> `kind=replace_incumbent` and name the incumbent. {research contract}

The **literature** lens adds: *open the real source page and confirm the identifier resolves to the
cited title + author; unverifiable → `missing_info`, never asserted. Peer-reviewed → primary;
preprint → secondary (flagged). A paper is mechanism/prior, not a buy signal; a paper that announces
a profitable signal is already-priced crowding evidence.*

## 2. GATE (deterministic, no LLM)

Pure script — see `gate_reference.md`. Checks tradeability, liquidity (price + average dollar
volume), and the overlap penalty vs the held book. No model is invoked.

## 3. TRIAGE (cheapest model — purity pre-filter)

> CHEAP TRIAGE (a fast pre-filter, not the final judge). Candidate card: {card}. First estimate
> purity (0..1) = how much THIS ticker captures the chokepoint economics vs a tiny segment of a
> conglomerate. DROP **only** when purity is clearly low (< ~0.25) AND it is OBVIOUSLY a
> diversified-giant-tiny-segment / commodity price-taker / pre-revenue hype / illiquid. **If purity ≥
> ~0.30 you MUST PURSUE** (a borderline name is for the deeper pass). When unsure, PURSUE — a false
> drop is costly (a real pure-play never gets evaluated), a false pursue is cheap. Return
> `{verdict: pursue|drop, purity_estimate, category, reason}`.

A deterministic floor backs this: a `drop` with `purity_estimate ≥ 0.28` is overridden to pursue, and
a triage failure escalates (never a silent drop).

## 4. EVALUATE (mid model — bear-case-before-recommendation, triage survivors only)

> You are the FIRST-PASS EVALUATOR (as of {date}); this candidate passed the mechanical gate and a
> cheap triage. Card: {card}. With dated evidence: (1) what physical chokepoint, and is it a PURE
> vehicle or a tiny segment / commodity peak / pre-revenue hype? (2) direct / second-order / adjacent?
> (3) incremental vs the held book or a duplicate (note the incumbent)? (4) admit / replace / watchlist
> / reject? (5) measurable exit triggers. **WRITE THE BEAR CASE BEFORE the recommendation.** Reserve
> admit/replace for names that clearly improve the book after purity + overlap + valuation + crowding.
> {research contract}

## 5. ADJUDICATE (expensive model — admit-flags only)

> You are the capital-at-risk ADJUDICATOR (as of {date}). A first pass flagged this to ADMIT/REPLACE.
> Re-judge at max rigor — the asymmetry: a wrong watchlist only delays; a wrong admit puts capital on
> a bad thesis. First-pass decision: {decision}. Independently verify the chokepoint is real and
> hard-to-bypass, the vehicle is PURE, and it beats the held book after overlap + purity + valuation +
> crowding. You may DOWNGRADE. Re-write the bear case first, then the final action + max satellite
> weight + measurable exit triggers (each with a checkable data source). {research contract}

## 6. REJECTION-QUALITY AUDIT (held-out model — bull-only view)

> You are an INDEPENDENT analyst auditing rejection decisions. For each candidate you are given ONLY
> the steelmanned BULL case and the engine's decision — NOT the bear case. Judge INDEPENDENTLY whether
> the rejection was JUSTIFIED, and assign one category {low-purity-conglomerate, duplicate-overlap,
> valuation-or-crowding, commodity-cycle, pre-revenue-or-hype, unverifiable-or-untradeable,
> FALSE_REJECTION}. Report rejection precision (fraction justified) and any false rejections. Be a
> skeptic; do not rubber-stamp.

A flagged FALSE_REJECTION is not final — it is escalated to a capital-at-risk adjudication (§5), which
can uphold the rejection (the cheap-screen → expensive-adjudicate asymmetry applied to the audit
itself; see `../research/docs/RESULTS_INITIAL.md`).

## 7. CITATION VERIFICATION (refute-by-default, before any reference is used)

> You are a citation-integrity auditor. REFUTE by default. For each identifier, fetch the real source
> page and confirm it resolves to the claimed title + first author. A wrong title, wrong author,
> non-existent id, or different topic = REJECT. Treat near-misses as REJECT. Report
> CONFIRM / REJECT / UNRESOLVABLE with the actual title + author found. Only CONFIRMED entries may be
> cited.

## 8. ABLATION ARMS (the H2 baselines, literal prompts)

*Provenance note (2026-07-06).* The paper's pilot ablation (June 2026) ran its arms as deltas on §4;
the exact per-arm strings and per-card decisions of that pilot were not preserved as artifacts. The
prompts below are therefore the **canonical, literal arm prompts from the preserved re-run
(2026-07-06) onward** — the re-run's card set, per-card decisions, and run manifest are retained as
artifacts so the ablation is reproducible end-to-end. Shared rules across every arm: the SAME candidate
cards, the SAME model tier, one card-decision per candidate from
{admit, replace, watchlist, reject}, and the same capital-at-risk framing — every arm is explicitly
**allowed to reject**; none is a strawman forced to admit.

**Shared arm preamble (prepended to each arm below):**

> You are evaluating ONE candidate card for a real, capital-at-risk thematic book (as of {date}).
> Decide: admit / replace / watchlist / reject, with a one-paragraph reason. You are fully free to
> reject. Card: {card}.

### 8a. Ungated screener (no gate, no purity bar, no overlap penalty, no bear case)

> Judge this candidate as an investment idea for the theme on its own merits. There is no checklist:
> no tradeability/liquidity gate, no exposure-purity bar, no duplication penalty against a held book,
> and no requirement to write a bear case. Recommend what looks good for the theme.

### 8b. − bear-case-first (everything else intact)

> This candidate passed the mechanical gate and a cheap triage. With dated evidence: (1) what
> chokepoint, and is it a PURE vehicle or a tiny segment / commodity peak / pre-revenue hype?
> (2) direct / second-order / adjacent? (3) incremental vs the held book or a duplicate (note the
> incumbent)? (4) admit / replace / watchlist / reject? (5) measurable exit triggers. Recommend
> directly from the thesis; **you are not required to write a bear case.** Reserve admit/replace for
> names that clearly improve the book after purity + overlap + valuation + crowding. {research contract}

### 8c. − overlap penalty (everything else intact)

> This candidate passed the mechanical gate and a cheap triage. With dated evidence: (1) what
> chokepoint, and is it a PURE vehicle or a tiny segment / commodity peak / pre-revenue hype?
> (2) direct / second-order / adjacent? (3) admit / replace / watchlist / reject? (4) measurable exit
> triggers. **Judge the name entirely on its own merits — ignore any duplication or correlation with
> names already held; do not apply an overlap penalty or name an incumbent.** WRITE THE BEAR CASE
> BEFORE the recommendation. Reserve admit/replace for names that clearly improve the theme exposure
> after purity + valuation + crowding. {research contract}

### 8d. Debate-only (bull/bear staged, no forward lock) — pending arm (b)

> Stage a structured debate on this candidate, then judge it. First write the strongest BULL
> advocate's case (dated evidence). Then write the strongest BEAR advocate's case (dated evidence).
> Then, as the judge, weigh the debate and decide admit / replace / watchlist / reject. There is no
> required ordering of analysis before recommendation beyond the debate itself, and **no
> pre-registration lock**: you are NOT required to produce measurable exit triggers, a falsifiable
> hypothesis contract, or any commitment that would be hash-locked before a forward window. Decide
> from the debate alone. {research contract}

### 8e. No Forward-QPOP lock (same evaluation, no hash-locked contract) — pending arm (c)

> This candidate passed the mechanical gate and a cheap triage. With dated evidence: (1) what
> chokepoint, and is it a PURE vehicle or a tiny segment / commodity peak / pre-revenue hype?
> (2) direct / second-order / adjacent? (3) incremental vs the held book or a duplicate (note the
> incumbent)? (4) admit / replace / watchlist / reject? WRITE THE BEAR CASE BEFORE the
> recommendation. Reserve admit/replace for names that clearly improve the book after purity +
> overlap + valuation + crowding. **Exit triggers are OPTIONAL: admission does NOT require committing
> measurable, dated exit triggers or a hash-locked, falsifiable hypothesis contract before the
> forward window — an admitted thesis may remain open-ended and revisable.** {research contract}

The full pipeline's decisions for the same card set come from the production funnel records (gate →
triage → §4 evaluate → §5 adjudicate), so the comparison is: production full-pipeline vs each arm
above, card by card, on the preserved batch.

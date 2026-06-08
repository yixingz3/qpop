# Literature Ingestion

Academic literature enters the engine through one disciplined channel with two modes. The point is
to make the research **proper** — grounded in the credible published record, not solely in ideas the
operator happened to hear — *without* letting a citation become an authority-laundering backdoor
around the no-stories discipline.

Two modes, one gate:

| Mode | Question it answers | Feeds |
|---|---|---|
| **A. Domain literature lens** | "What does the credible published record say about *this chokepoint's mechanism*?" | the **SOURCE** stage of discovery (a new lens, alongside per-node / gap / social / policy) |
| **B. Methods literature watch** | "What has the field already published about *our method*, and where is our gap?" | the **paper** (`related_work`, the gap framing, the reference list) |

Both modes share the same non-negotiable **verify-before-cite** gate (below).

## The verify-before-cite gate (non-negotiable)

LLMs fabricate citations — a plausible title, real-sounding authors, an arXiv id that resolves to
something else, or nothing at all. A framework whose whole thesis is *auditable restraint* cannot
ship a fabricated reference. So **no paper may move a confidence score, enter a candidate card as
evidence, or be added to `references.bib` until it passes an adversarial verification pass**:

1. A second agent (independent of the one that surfaced the paper) fetches the **real** source page
   (arXiv abstract / DOI / publisher) and is instructed to **refute**: does the identifier actually
   resolve to the claimed title *and* first author? Default verdict is **REJECT**; a near-miss
   (wrong author, adjacent title, different topic) is a REJECT, not a pass.
2. Only **CONFIRMED** entries are written. REJECTED / UNRESOLVABLE entries are dropped and logged.
3. The verification verdict is recorded next to the citation (auditable).

This gate has already caught real failures in our own pipeline (a fabricated entry and a
wrong-author entry on an earlier pass) — that the framework **catches its own dogfood** is itself a
result reported in the paper, not an embarrassment hidden.

## Source-tier placement (a paper is evidence, not proof)

A paper is graded on the same source-tier ladder as any other evidence, with two finance-specific
rules that *prevent* citation from short-circuiting the discipline:

- **Peer-reviewed journal / top-venue conference → primary-grade** for a *mechanism* claim (why a
  chokepoint binds, lead-time physics, supplier concentration, factor structure).
- **Preprint (arXiv/SSRN, not yet peer-reviewed) → secondary-grade**, flagged "preprint." Useful,
  citable, but it has not cleared review — it cannot alone carry a confidence move.
- **Mechanism, not timing.** A paper informs *why* a node is a chokepoint and *what* would falsify it
  (priors and exit-trigger design) — **not** *when* to trade it. Academic findings are slow-moving;
  the engine still requires dated, ticker-level primary/secondary corroboration for any *position*.
- **A published, tradeable anomaly is the canonical "already-priced" case.** Documented factor /
  anomaly returns decay after publication as the market learns them (McLean & Pontiff 2016). So a
  paper that *announces a profitable signal* is treated as **crowding-risk evidence** (discounts
  `crowding_adjustment`), never as a buy signal. This is the same principle as
  policy-as-evidence and uncertainty-about-the-constraint: information already in the published
  record is, to that extent, already in the price.

Net: literature **raises the quality of priors and mechanism** and **sharpens falsification**, while
the gates still decide whether anything trades. A citation can never *be* the reason a position
exists — only deterministic score × purity × adjustments × caps × a dated trigger can.

## Mode A — domain literature lens (SOURCE)

Runs as one more SOURCE lens in the budget-aware funnel (`docs/METHOD.md` §3). It searches the
credible published record for the active domain — for AI supply chain: semiconductor-economics,
critical-materials, power-systems, and supply-chain-bottleneck literature — and emits candidate
cards with:

- the chokepoint/mechanism the paper supports, stated as a *falsifiable* claim;
- a **verified** citation (post-gate) with venue + date + source tier (`primary` peer-reviewed /
  `secondary` preprint);
- the specific exit-trigger or falsifier the paper implies (a paper that explains *why* a constraint
  binds usually also implies *what would relax it*).

These cards then pass the same deterministic GATE (tradeability, liquidity, overlap) and EVALUATE
(bear-case-first) as every other candidate. A literature-sourced idea earns **no** special standing —
it competes on the same decomposed confidence as a filings-sourced or social-sourced idea.

## Mode B — methods literature watch (the paper)

A periodic pass (run before each draft / camera-ready) over the field the *method* lives in:
financial LLM agents, lookahead/leakage & structural-validity critiques, pre-registration / research
integrity, LLM-as-judge & sycophancy, and auditable / model-risk AI in finance. It:

1. surfaces new work that should appear in `related_work`;
2. flags any paper that already does **two or more** of our four claimed elements (a *gap threat*)
   and forces an explicit positioning response, rather than letting us discover the overlap at
   review;
3. proposes verified BibTeX (post-gate) for the reference list.

The watch is itself an instance of the framework's discipline: it is adversarial (look for what
*refutes* our novelty), source-tiered, and every citation it proposes must clear verify-before-cite.

## Why this belongs in the engine, not bolted on

The literature channel reuses everything already built: it is a SOURCE lens (Mode A) or a research
pass (Mode B), it grades evidence on the existing source-tier ladder, it routes through the same
deterministic gates, and its integrity gate is the same *pre-commit, adversarial, auditable* pattern
as forward-QPOP. Nothing about "read the papers" requires relaxing the discipline — and the one new
rule it does require (verify-before-cite) is exactly the rule the paper argues the whole field is
missing.

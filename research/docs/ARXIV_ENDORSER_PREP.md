# arXiv Endorsement Prep (WI-20c)

**Purpose.** The arXiv upload of *Forward-Registered, Auditable LLM-Assisted Research: A Reliability
Methodology, with a Capital-Markets Testbed* (Zheng, NYU Stern; SSRN submitted 2026-06-29) is blocked
only on **endorsement**. This document gives the operator everything needed to unblock it: (1) the
current arXiv endorsement mechanics, (2) a **verified** shortlist of candidate endorsers, and (3) an
honest outreach template. The arXiv-ready source itself was prepared separately (WI-21) and lives at
[`../paper/arxiv/`](../paper/arxiv/) (builds clean: 28 pp, 0 undefined citations).

> **The outreach is the operator's action.** Nothing here has been sent to anyone. This file is a
> prep packet, not a contact log. One positive endorsement is sufficient — do **not** mass-email.

---

## 1. Why an endorsement is needed (the mechanics)

Sources fetched 2026-07-08: [`info.arxiv.org/help/endorsement.html`](https://info.arxiv.org/help/endorsement.html),
[`arxiv.org/help/endorsement`](https://arxiv.org/help/endorsement), and the
[2026-01-21 policy update](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/).

- **Endorsement is required before a user's first submission to arXiv, and again before their first
  submission to any new category.** Yixing has no prior arXiv paper, so a first cs.AI submission needs
  one positive endorsement.
- **The target category is `cs.AI` (primary), `q-fin.CP` (cross-list).** Endorsement is evaluated at
  the **endorsement-domain** level, and **all of computer science (`cs`) is a single endorsement
  domain** — `cs.AI`, `cs.LG`, `cs.CL`, etc. all fall under it. **This is the key enabling fact:** a
  prolific `cs.LG`/`cs.CL`/`stat.ML`-cross-listed author (e.g. the e-value / anytime-valid cohort
  below) can endorse a `cs.AI` submission. (Physics is the exception where sub-classes are their own
  domains; CS is not.)
- **Endorser eligibility threshold:** an endorser must have authored "a certain number of papers
  within the endorsement domain," counting only papers **submitted between three months and five years
  ago**. **arXiv does not publish the exact integer** for `cs` — the widely-repeated "3 papers"
  figure is community/Q&A folklore, *not* on arXiv's official page, so it is **not asserted as fact**
  here. arXiv's own wording: the bar "has been set so that any active scientist who has been working
  in their field for a few years should be able to endorse." Practically: any established, actively
  publishing CS/ML faculty or senior researcher clears it; arXiv performs the final check when the
  endorser enters the code (see below). Every "likely" rating in §3 means *high-probability, not
  guaranteed*.
- **Auto-endorsement no longer applies to Yixing.** Per the 2026-01-21 update, automatic endorsement
  now requires **both** an institutional/academic email **and** prior authorship of an accepted arXiv
  paper in the same domain. Yixing has the former but not the latter, so he must obtain a **manual
  endorsement** — which is exactly what this packet is for.
- **The mechanic.** Yixing initiates an endorsement request in the arXiv submission flow; arXiv issues
  a **six-character alphanumeric endorsement code** and a link. He sends the code/link to a
  prospective endorser, who enters it on arXiv's endorsement form (`/auth/endorse.php`) and grants or
  declines. The endorser does **not** need to read or vouch for the paper's content — only that it
  plausibly belongs in the category.

**Bottom line for the operator:** request the endorsement code in the arXiv flow, then send the §4
note to 2–3 top targets from §3. Stop as soon as one endorses.

---

## 2. How this shortlist was built (verification discipline)

This list was produced with the paper's own **verify-before-cite** discipline (refute-by-default),
so it can be trusted as an artifact of the same methodology the paper argues for:

1. **Multi-lens discovery** (4 parallel lenses): POPPER lineage; safe-anytime-valid-inference /
   e-value authors with a CS footprint; LLM-agent-evaluation / LLM-as-judge / research-integrity
   authors; and authors the paper **already cites** (pre-verified in `references.bib`).
2. **Dedupe** to 33 unique candidates.
3. **Adversarial per-candidate verification** — an independent agent fetched the real arXiv abstract
   page for each claimed paper and was instructed to **REJECT by default**: a near-miss (wrong author,
   adjacent title, unresolvable id) fails. Every entry below had its arXiv id resolve to the **exact**
   claimed title with the named person in the author list. Result: **33 confirmed, 0 rejected** —
   no fabricated papers survived (several near-namesake collisions were caught and excluded, e.g.
   Yiqiao Jin vs. Ying Jin, Ati Sharma vs. Amit Sharma, the astro-ph Duncan Watts).
4. **Eligibility rated separately from paper-existence.** "Confirmed" only means the paper and
   authorship are real. Endorser **eligibility** (recent in-window `cs.*` arXiv footprint) is a
   distinct column — three real authors are flagged **not currently eligible** (§3.3) and excluded
   from the outreach recommendation.

Two of the featured picks (Komiyama's `2605.05873`; the arXiv endorsement policy itself) were
independently re-fetched by hand before publishing this doc.

---

## 3. Verified endorser shortlist

Eligibility legend: **likely** = clear, active in-window `cs.*` arXiv record (arXiv makes the final
call); **uncertain / unlikely** = insufficient in-window `cs.*` record → not a usable endorser now.
"Cited?" = the paper already cites this author's work in its related-work section (an honest hook).

### 3.1 Recommended first contacts (ranked)

Best combination of *clearly eligible* + *tight methodological adjacency* + *low friction*. Send to
2–3 of these first.

| # | Name | Affiliation | Why this one first | Contact route |
|---|------|-------------|--------------------|---------------|
| 1 | **Junpei Komiyama** | NYU Stern (Asst. Prof.) | **Same institution as the author** — lowest-friction path; his *CITE* paper is anytime-valid inference for LLM self-consistency, directly the method family the paper uses | `junpei.komiyama@nyu.edu` · [jkomiyama.github.io](https://jkomiyama.github.io/) |
| 2 | **Huan Liu** | Arizona State (Regents Prof.) | **Cited** (his LLM-as-a-judge survey); unimpeachable endorser standing (ACM/AAAI/IEEE Fellow) | [faculty.engineering.asu.edu/huanliu](https://faculty.engineering.asu.edu/huanliu/) |
| 3 | **Kexin Huang** | Stanford (PhD, SNAP) | **POPPER first author** — POPPER is the paper's single closest methodological neighbor, and it is **cited**; public email; students often respond fast | `kexinh@stanford.edu` · [kexinhuang.com](https://www.kexinhuang.com/) |
| 4 | **Aaditya Ramdas** | CMU (Stats & ML) | Originator of the **testing-by-betting / e-value** machinery the paper's sequential test rests on; senior, prolific | [scholars.cmu.edu/7692-aaditya-ramdas](https://scholars.cmu.edu/7692-aaditya-ramdas) |
| 5 | **Amit Sharma** | Microsoft Research India | **Cited**; co-author of *Pre-registration for Predictive Modeling* — the exact discipline the paper formalizes | [amitsharma.in](http://www.amitsharma.in) |
| 6 | **Jessica Hullman** | Northwestern (Prof.) | **Cited** (same pre-registration paper); public institutional email | `jhullman@northwestern.edu` · [homepage](http://users.eecs.northwestern.edu/~jhullman/) |
| 7 | **Soroush Vosoughi** | Dartmouth (Assoc. Prof.) | **Cited** (multi-agent LLM-as-judge bias); paper is `cs.AI`-primary so his endorsement is squarely in-domain | [cs.dartmouth.edu/~soroush](https://cs.dartmouth.edu/~soroush/) |
| 8 | **Duncan J. Watts** | UPenn (Stevens Univ. Prof., CIS) | **Cited** (pre-registration for predictive modeling); very senior, CS appointment | [css.seas.upenn.edu/people/duncan-watts](https://css.seas.upenn.edu/people/duncan-watts/) |

### 3.2 Full verified roster (all eligible candidates)

Grouped by lens; every row's arXiv id was resolved to the exact title with the named author present.

**Already-cited authors** (outreach can honestly open "I cite your work in the related-work section"):

| Name | Affiliation | Relevant (cited) paper — arXiv | Elig. | Contact route |
|------|-------------|-------------------------------|-------|---------------|
| Huan Liu | Arizona State | *From Generation to Judgment: …LLM-as-a-judge* — [2411.16594](https://arxiv.org/abs/2411.16594) | likely | [faculty page](https://faculty.engineering.asu.edu/huanliu/) |
| Arman Cohan | Yale | *Judging with Many Minds* — [2505.19477](https://arxiv.org/abs/2505.19477) (also *SciVer* 2506.15569) | likely | [Yale directory](https://engineering.yale.edu/research-and-faculty/faculty-directory/arman-cohan) |
| Soroush Vosoughi | Dartmouth | *Judging with Many Minds* — [2505.19477](https://arxiv.org/abs/2505.19477) | likely | [homepage](https://cs.dartmouth.edu/~soroush/) |
| Kexin Huang | Stanford | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) (first author) | likely | `kexinh@stanford.edu` |
| Ying Jin | Wharton, UPenn | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) | likely | `yjinstat@wharton.upenn.edu` · [site](https://ying531.github.io/) |
| Ryan Li | Stanford | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) | likely | [Scholar](https://scholar.google.com/citations?user=zwcHlUMAAAAJ) (`lansong@stanford.edu`) |
| Michael Y. Li | Stanford | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) | likely | [michaelyli.github.io](https://michaelyli.github.io/) (email obscured on page) |
| Emmanuel Candès | Stanford (Stats/Math) | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) | likely | [candes.su.domains](https://candes.su.domains/) |
| Jure Leskovec | Stanford | *POPPER* — [2502.09858](https://arxiv.org/abs/2502.09858) (senior author) | likely | `jure@cs.stanford.edu` |
| Igor Mordatch | Google DeepMind | *Multiagent Debate* — [2305.14325](https://arxiv.org/abs/2305.14325) | likely | [Scholar](https://scholar.google.com/citations?user=Vzr1RukAAAAJ) |
| Antonio Torralba | MIT | *Multiagent Debate* — [2305.14325](https://arxiv.org/abs/2305.14325) | likely | [web.mit.edu/torralba](https://web.mit.edu/torralba/www/) |
| Joshua B. Tenenbaum | MIT | *Multiagent Debate* — [2305.14325](https://arxiv.org/abs/2305.14325) | likely | [CSAIL page](https://www.csail.mit.edu/person/joshua-tenenbaum) |
| Amit Sharma | MSR India | *Pre-registration for Predictive Modeling* — [2311.18807](https://arxiv.org/abs/2311.18807) | likely | [amitsharma.in](http://www.amitsharma.in) |
| Duncan J. Watts | UPenn | *Pre-registration for Predictive Modeling* — [2311.18807](https://arxiv.org/abs/2311.18807) | likely | [homepage](https://css.seas.upenn.edu/people/duncan-watts/) |
| Jessica Hullman | Northwestern | *Pre-registration for Predictive Modeling* — [2311.18807](https://arxiv.org/abs/2311.18807) | likely | `jhullman@northwestern.edu` |

*Note:* other co-authors of these cited papers are equally valid, honest targets — e.g. **Jake M.
Hofman** (Microsoft Research), first author of *Pre-registration for Predictive Modeling* (2311.18807).

**e-value / anytime-valid / sequential-testing** (the statistical machinery the paper uses — tight
methodological neighbors; CS-cross-listed so eligible under the single `cs` domain):

| Name | Affiliation | Relevant paper — arXiv | Elig. | Contact route |
|------|-------------|-----------------------|-------|---------------|
| Aaditya Ramdas | CMU | *Auditing Fairness by Betting* — [2305.17570](https://arxiv.org/abs/2305.17570) | likely | [CMU profile](https://scholars.cmu.edu/7692-aaditya-ramdas) |
| Jun-Kun Wang | UC San Diego | *Online Detection of LLM-Generated Texts via Sequential HT by Betting* — [2410.22318](https://arxiv.org/abs/2410.22318) | likely | `jkw005@ucsd.edu` · [site](https://jimwang123.github.io/) |
| Drew Prinster | Johns Hopkins (PhD) | *E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing* — [2512.03109](https://arxiv.org/abs/2512.03109) | likely | `drew@cs.jhu.edu` · [site](https://drewprinster.github.io/) |
| Junpei Komiyama | NYU Stern | *CITE: Anytime-Valid Statistical Inference in LLM Self-Consistency* — [2605.05873](https://arxiv.org/abs/2605.05873) | likely | `junpei.komiyama@nyu.edu` |
| Shubhanshu Shekhar | Univ. of Michigan | *Deep anytime-valid hypothesis testing* — [2310.19384](https://arxiv.org/abs/2310.19384) | likely | [UMich page](https://ece.engin.umich.edu/peoplenews/shekhar-shubhanshu) |
| Jean Feng | UCSF | *Adaptive auditing of AI systems with anytime-valid guarantees* — [2605.07002](https://arxiv.org/abs/2605.07002) | likely | [jeanfeng.com](https://www.jeanfeng.com/) |
| Anastasios N. Angelopoulos | LMArena / UC Berkeley | *Cost-Optimal Active AI Model Evaluation* — [2506.07949](https://arxiv.org/abs/2506.07949) | likely | [angelopoulos.ai](https://angelopoulos.ai/) |
| Osvaldo Simeone | King's College London | *Adaptive Prediction-Powered AutoEval* — [2505.18659](https://arxiv.org/abs/2505.18659) | likely | [KCL page](https://www.kcl.ac.uk/people/osvaldo-simeone) |
| Matt J. Kusner | UCL | *An Auditing Test To Detect Behavioral Shift in Language Models* — [2410.19406](https://arxiv.org/abs/2410.19406) | likely | [mkusner.github.io](https://mkusner.github.io/) |
| Yitao Li | Independent | *Who Drifted: the System or the Judge? Anytime-Valid Attribution…* — [2606.15474](https://arxiv.org/abs/2606.15474) | likely* | [yitao416.github.io](https://yitao416.github.io/) |

\* *Yitao Li:* eligible but **borderline count** — only one in-window `cs.AI` paper is fingerprint-confirmed his today (others age into the window monthly); publishes with a personal email / no institutional affiliation. Fine as a Path-2 endorser, but lower-confidence than the rest of this block.

**LLM-agent evaluation / benchmarks / reliability** (prolific `cs.*` authors, clearly eligible):

| Name | Affiliation | Relevant paper — arXiv | Elig. | Contact route |
|------|-------------|-----------------------|-------|---------------|
| Percy Liang | Stanford (CRFM/HELM) | *AutoBencher: Towards Declarative Benchmark Construction* — [2407.08351](https://arxiv.org/abs/2407.08351) | likely | [cs.stanford.edu/~pliang](https://cs.stanford.edu/~pliang/) |
| Tatsunori Hashimoto | Stanford | *AutoBencher* — [2407.08351](https://arxiv.org/abs/2407.08351) (senior author) | likely | [thashim.github.io](https://thashim.github.io/) |
| Graham Neubig | CMU (LTI) | *TheAgentCompany* — [2412.14161](https://arxiv.org/abs/2412.14161) | likely | `gneubig@cs.cmu.edu` |
| Arvind Narayanan | Princeton | *AI Agents That Matter* — [2407.01502](https://arxiv.org/abs/2407.01502) | likely | [cs.princeton.edu/~arvindn](https://www.cs.princeton.edu/~arvindn/) |
| Dan Hendrycks | Center for AI Safety / UC Berkeley | *Humanity's Last Exam* — [2501.14249](https://arxiv.org/abs/2501.14249) | likely | `dan@safe.ai` |
| Marko Čuljak | Univ. of Zagreb (FER / TakeLab) | *Sound Agentic Science Requires Adversarial Experiments* — [2604.22080](https://arxiv.org/abs/2604.22080) | likely | [FER page](https://www.fer.unizg.hr/en/marko.culjak) |

### 3.3 Real authors that are NOT currently usable endorsers (kept for transparency)

Verified as real people with real papers, but their in-window `cs.*` record does not currently
support endorser eligibility. **Do not contact for endorsement.**

| Name | Paper — arXiv | Why not eligible now |
|------|---------------|----------------------|
| Dionizije Fa | *Sound Agentic Science Requires Adversarial Experiments* — [2604.22080](https://arxiv.org/abs/2604.22080) | Single `cs.AI` paper, only ~2.5 months old — **under** arXiv's 3-month counting floor; no other `cs.*` history. (Co-author Marko Čuljak, above, *is* eligible.) |
| Abhinav Agarwal | *Refute-or-Promote: An Adversarial Stage-Gated Multi-Agent Review…* — [2604.19049](https://arxiv.org/abs/2604.19049) | One lone cross-listed preprint <3 months old; no established `cs.*` track record — likely a first-time submitter himself. Contact only via [GitHub](https://github.com/abhinavagarwal07/refute-or-promote). |

---

## 4. Outreach note (template — operator sends, personalize the bracketed hook)

> **Subject:** arXiv endorsement request — cs.AI (auditable LLM-assisted research methods paper)
>
> Dear [Prof./Dr. Name],
>
> I'm Yixing Zheng (NYU Stern). I've written a methods paper, *"Forward-Registered, Auditable
> LLM-Assisted Research: A Reliability Methodology, with a Capital-Markets Testbed"*
> (SSRN: **[SSRN LINK — fill in once posted]**), on making LLM-assisted research auditable:
> forward-registering LLM-generated hypotheses before outcomes settle, adversarially verifying the
> agent's claims, and controlling Type-I error with an e-value sequential test. I'd like to post it to
> arXiv (**cs.AI** primary, q-fin.CP cross-list), but as a first-time submitter I need an endorsement,
> and your work on **[SPECIFIC HOOK — e.g. "automated hypothesis validation via agentic sequential
> falsification (POPPER)" / "testing-by-betting and anytime-valid inference" / "pre-registration for
> predictive modeling"]** is among the closest methodological neighbors to what the paper formalizes.
> Would you be willing to endorse the submission for cs.AI? arXiv's six-character endorsement code is
> **[CODE]** (endorsement link: `https://arxiv.org/auth/endorse.php?x=[CODE]`) — there's no obligation
> to review the paper, though I'm glad to send the PDF if useful.
>
> With thanks,
> Yixing Zheng · [institutional email] · ORCID 0009-0000-0563-2398

Personalization hooks by cohort: **POPPER authors** → "automated hypothesis validation via agentic
sequential falsification"; **e-value cohort** → "testing-by-betting / anytime-valid sequential
inference"; **pre-registration authors** → "pre-registration for predictive modeling"; **LLM-as-judge
/ benchmark authors** → "reliability and auditing of LLM evaluation."

---

## 5. Operator checklist

1. Start the arXiv submission (upload from [`../paper/arxiv/`](../paper/arxiv/) — `paper.tex` +
   `references.bib`; `paper.bbl` is included as a fallback if arXiv's BibTeX pass misfires).
2. When arXiv prompts for endorsement, generate the **endorsement code**.
3. Paste the code into the §4 note and send to **2–3** §3.1 targets (lead with Komiyama — same
   institution — and one or two cited authors). Personalize the hook line.
4. **Stop as soon as one endorses.** Only one positive endorsement is required; do not mass-email.
5. Fill the real **SSRN URL** into the note (and into [`../paper/SUBMISSION.md`](../paper/SUBMISSION.md))
   once SSRN posts the abstract page.
6. After endorsement, complete the arXiv submission; record the arXiv ID in `SUBMISSION.md`.

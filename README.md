<div align="center">

# qpop

**Your AI agent will admit any plausible idea. `qpop` makes it earn each one — gated, pre-registered, and falsifiable.**

A Claude Code plugin that turns an over-eager LLM into a disciplined researcher. The headline result is
counterintuitive: a well-run agent **rejects most of what it surfaces** — and that restraint, recorded
in a tamper-evident ledger, is the point.

![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![License: MIT](https://img.shields.io/badge/License-MIT-blue)
![status: v0.1](https://img.shields.io/badge/status-v0.1-lightgrey)
<!-- ![GitHub stars](https://img.shields.io/github/stars/yixingz3/qpop) -->

</div>

---

> **Two audiences.** **Claude Code users:** [install the plugin](#install-claude-code) — that's the whole setup. **Researchers / citers:** jump to the paper in [Learn more](#learn-more). *One project, three names: the plugin & repo `qpop`, the Python package `forward-qpop`, and the method, **Forward-QPOP**.*

## The problem

LLMs are brilliant at *sourcing* ideas and unreliable as *decision* engines. Left ungated, an LLM
screener **over-admits by construction** — it is rewarded for *finding* ideas, not *refusing* them —
and it confabulates, agrees with itself (sycophancy), and, when "backtested," already knows the answer
(look-ahead leakage). The missing piece isn't better prompts. It's **auditable restraint**.

## What `qpop` does

It wraps your agent's research in a discipline and makes every decision auditable:

- **Rejects most candidates, for defensible reasons** — deterministic gates + a bear case written
  *before* the recommendation.
- **Pre-registers the survivors** to a tamper-evident, hash-chained ledger — the claim, dated
  evidence, and measurable exit triggers, committed *before* the outcome is known.
- **Validates forward**, not by a leaky backtest.

> **Pilot evidence** (the methods paper, [`research/paper/`](research/paper)): removing any single
> discipline pushed an LLM screener's admission rate from **0% to 66–100%**; a held-out **LLM-auditor**
> judged **93%** of the rejections justified (n=14; an LLM-on-LLM diagnostic, not a human audit);
> "no action" is the modal outcome. *These are pilot metrics — they validate process discipline, not
> investment performance.*

## Install (Claude Code)

```text
/plugin marketplace add yixingz3/qpop
/plugin install qpop@qpop
```

That's it. The `auditable-research` discipline activates when you screen ideas or act on a finding, and
the `/qpop:*` commands below are ready. *(Other agents: the discipline is portable markdown — see
[Learn more](#learn-more).)*

## 60-second demo

After installing, ask Claude Code:

> *"Screen these 3 research claims with qpop and pre-register only the survivors."*

A disciplined run looks like this (illustrative):

```text
3 candidates screened
2 rejected  — tertiary-only evidence / fails replace-don't-stack
1 preregistered — H-001
   entry_hash: sha256:9f3c…  (chained to prev)
verify: OK — 1 entry, chain intact
```

"2 of 3 rejected" is the feature, not a bug — **no action** is the correct, modal outcome. No Claude
Code? `pip install forward-qpop` gives you the same ledger from the command line (see [Learn more](#learn-more)).

## Commands

| Command | What it does |
|---|---|
| **`auditable-research`** | *(auto)* the full discipline, applied when you screen ideas or evaluate a finding |
| **`/qpop:preregister`** | register a hypothesis to the tamper-evident ledger *before* evaluating |
| **`/qpop:review`** | audit current claims / a diff for stories, leakage, over-admission, missing pre-registration |
| **`/qpop:verify`** | verify a ledger's integrity — detect any post-hoc edit, insertion, or reorder |

The ledger is a real hash chain (`entry_hash = sha256(content_hash ‖ prev_hash)`): edit a past entry,
insert one, delete one, or reorder them, and `verify` fails (and exits non-zero — drop it in CI).

## Status — what's runnable today

`qpop` is **auditable research infrastructure**, not a turnkey trading engine. What ships in this repo:

| Area | Status |
|---|---|
| Claude Code plugin discipline (`auditable-research` + `/qpop:*`) | **Working — v0.1** |
| Hash-chained Python ledger (`forward_qpop`) + CLI | **Working** (49/50 tests, 1 network test skipped by default) |
| Anytime-valid sequential trigger test (`evalue`) — Type-I control over many triggers | **Working** (18/18 tests) — e-value / Ville, [methods note](research/docs/EVALUE_METHODS.md) |
| Local anchor manifest (`anchor` / `verify-anchor`) | **Working** — manifest + drift-detection + git / local OpenTimestamps stamp |
| External timestamp anchor (`anchor external` / `verify-external`) | **Working** — submits to OpenTimestamps, sidecar receipt + drift-detection ([details](#external-anchor-what-it-proves-and-what-it-doesnt)) |
| JSON Schemas for cards / entries / runs | **Included** ([`schemas/`](schemas)) |
| Synthetic fixtures + worked examples | **Included** ([`examples/`](examples)) |
| Methods paper — theory + pilot evidence | **Included** ([PDF](research/paper/paper.pdf)) |
| Full `SOURCE → GATE → EVALUATE` engine (AI-supply-chain) | **Specified** — interfaces/contracts in [`src/`](src); the reference implementation is private and being generalized |
| PyPI package (`forward-qpop`) | **Published** — `pip install forward-qpop` |
| Forward performance results | **Pending — not claimed** |

Nothing here is finance-specific: the discipline and the ledger are domain-agnostic, and finance is a
deliberately *adversarial* testbed. The same flow fits an agentic literature review or an
[ML-eval claim](examples/ml_benchmark) — and the metric the ablations measure, the **over-admission
rate** (how often an agent admits plausible-but-weak ideas), is itself a reusable reliability benchmark.

## What the ledger proves (and what it doesn't)

The hash chain is **tamper-evidence, not a clock.** Be precise about the guarantee:

| Claim | Chain alone? | What closes the gap |
|---|---|---|
| A past entry was edited | ✅ detected | hash verification |
| An entry was inserted / deleted / reordered | ✅ detected | hash-chain verification |
| An entry existed *before* the outcome | ⚠️ partial | `anchor external` + OpenTimestamps (or a pushed public commit) |
| The LLM's reasoning was correct | ❌ no | human / source review |
| The strategy is profitable | ❌ no | a forward window + the validity checklist |

The "before the outcome" guarantee needs an **external anchor** — and `qpop` ships one:
`forward-qpop anchor <ledger>` writes a local manifest committing to the ledger head, and
`verify-anchor` detects any drift since. Bind it to time by committing the manifest to a public repo
(the commit date *is* the anchor) or by submitting it to a public, append-only timestamp service.

### External anchor: what it proves, and what it doesn't

`forward-qpop anchor external <ledger> --method ots` submits the manifest's head digest to
[OpenTimestamps](https://opentimestamps.org) (a public, append-only Bitcoin-backed timestamp
service) and records the outcome — method, service, digest, submission time, status — in a
`<ledger>.external-anchor.json` sidecar next to the ledger. `verify-external` re-checks that
sidecar's digest against the *current* ledger head, so any rewrite after submission is loud, not
silent:

```bash
forward-qpop anchor   <ledger>                          # local manifest first (always required)
forward-qpop anchor external <ledger> --method ots       # submit the head digest externally
forward-qpop verify-external <ledger>                    # detect drift since the external submission
```

**Route chosen: OpenTimestamps, not Sigstore/Rekor.** Both were evaluated:

- **OpenTimestamps** — one optional dependency (`pip install forward-qpop[anchor]`, wraps
  `opentimestamps-client`), stdlib-only integration (`subprocess`), and reuses this repo's existing
  local `ots_stamp` scaffolding. Honest caveat: a fresh stamp is **"submitted," not yet
  "confirmed"** — the Bitcoin attestation completes over hours, and the receipt is upgradeable
  later with `ots upgrade`.
- **Sigstore/Rekor** (`hashedrekord`) — would give an immediate inclusion proof + log index, but
  needs an ephemeral-key-signed entry, pulling in `cryptography`/`sigstore` for a payload this
  project otherwise has no use for (no code signing here). Passed on for now given the
  dependency weight; may revisit if Rekor's immediacy becomes worth the tradeoff.

**Degradation is always loud.** No `ots` binary on `PATH`, a network failure, or an unreachable
calendar server all exit non-zero with a specific message — `anchor external` never writes a
sidecar claiming success it didn't get. The unit tests exercise this against a faked backend (no
network needed for `pytest`); a true-network round-trip test exists but only runs when you
explicitly opt in (`QPOP_TEST_LIVE_OTS=1`) — see [`repro/`](repro) and
[`tests/test_external_anchor.py`](src/forward_qpop) for both.

## Learn more

- **The method** — the 7-step admission ladder (falsifiable claim → deterministic gates → bear-case-first → source tiers → forward pre-registration → forward-not-backtest → on-balance). Auto-applied by the [`auditable-research`](skills/auditable-research/SKILL.md) skill.
- **Reproduce every claim** — [`repro/`](repro): tests, tamper demo, schema validation, the anchor round-trip, and the paper build — each with expected output.
- **Data contracts** — [`schemas/`](schemas): JSON Schema for candidate cards, ledger entries, evidence, exit triggers, and run manifests.
- **Python library** — `pip install forward-qpop` (or run [`scripts/qpop.py`](scripts/qpop.py) from a clone): the dependency-free ledger + anchor. API in [the package README](src/forward_qpop/README.md).
- **The paper** — [PDF](research/paper/paper.pdf) / [source](research): theory, pilot evidence, and the **over-admission-rate (OAR)** benchmark. If you build on it, please cite [`CITATION.cff`](CITATION.cff).
- **Worked examples** — [`examples/`](examples): the AI-supply-chain funnel, a portable [template](examples/template_domain), and a non-finance [ML-benchmark pre-registration](examples/ml_benchmark).
- **Other agents & roadmap** — the discipline is portable markdown in [`skills/`](skills) (Codex / other agents can adopt it). Next: Codex/Cursor adapters, an MCP server, a LangChain/LangGraph wrapper. (The external timestamp anchor, previously roadmapped as "turnkey Sigstore/Rekor," shipped via OpenTimestamps instead — see [above](#external-anchor-what-it-proves-and-what-it-doesnt) for the tradeoff.)

## What this is not

Not investment advice, not a stock-picker, not a claim to beat the market. The finance domain is a
deliberately *adversarial testbed* (markets punish wishful thinking); `qpop` is a research
**discipline**. See [`DISCLAIMER.md`](DISCLAIMER.md) and [`ETHICS.md`](ETHICS.md).

## License

[MIT](LICENSE). Implements the **Forward-QPOP** protocol — see [`research/`](research) and
[`CITATION.cff`](CITATION.cff).

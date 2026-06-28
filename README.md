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

> **Two audiences.** **Claude Code users:** [install the plugin](#install-claude-code) — that's the whole setup. **Researchers / citers:** see [the paper](#two-pillars). *One project, three names: the plugin & repo `qpop`, the Python package `forward-qpop`, and the method, **Forward-QPOP**.*

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
> discipline pushed an LLM screener's admission rate from **0% to 66–100%**; a held-out auditor judged
> **93%** of the rejections justified; "no action" is the modal outcome. *These are pilot metrics —
> they validate process discipline, not investment performance.*

## Install (Claude Code)

```text
/plugin marketplace add yixingz3/qpop
/plugin install qpop@qpop
```

That's it. The `auditable-research` discipline activates when you screen ideas or act on a finding, and
the `/qpop:*` commands below are ready. *(Other agents: the discipline is portable markdown — see
[Other tools](#other-tools).)*

## How it works — the ladder

Apply **in order**; stop at the first failure → **no action** (the correct, modal outcome):

1. **Story or claim?** State it as something falsifiable, with a mechanism — or reject.
2. **Deterministic gates** (no LLM): eligibility, and *replace-don't-stack* on duplicates.
3. **Bear case first** — the strongest case *against*, written before the recommendation.
4. **Source tiers** — primary > secondary > market-implied > tertiary; tertiary alone never moves a conclusion.
5. **Pre-register, forward** — claim + dated evidence + exit triggers, hash-chained *before* the window.
6. **Forward, not backtest** — a backward test of an LLM-scored process is *structurally invalid*.
7. **On balance** — after overlap, cost, and uncertainty, does admitting beat doing nothing?

## Commands

| Command | What it does |
|---|---|
| **`auditable-research`** | *(auto)* the full discipline, applied when you screen ideas or evaluate a finding |
| **`/qpop:preregister`** | register a hypothesis to the tamper-evident ledger *before* evaluating |
| **`/qpop:review`** | audit current claims / a diff for stories, leakage, over-admission, missing pre-registration |
| **`/qpop:verify`** | verify a ledger's integrity — detect any post-hoc edit, insertion, or reorder |

The ledger is a real hash chain (`entry_hash = sha256(content_hash ‖ prev_hash)`): edit a past entry,
insert one, delete one, or reorder them, and `verify` fails (and exits non-zero — drop it in CI).

## Two pillars

- **The tool** — this plugin: the discipline + a runnable, tamper-evident ledger engine.
- **The paper** — *Forward-Registered, Auditable LLM-Assisted Research* — [**read the PDF**](research/paper/paper.pdf),
  or the LaTeX source in [`research/`](research). The theory and pilot evidence behind the method; if you
  build on it, please cite ([`CITATION.cff`](CITATION.cff)).

## Use the ledger without Claude Code (Python)

The pre-registration engine is a dependency-free package, bundled here and importable directly:

```bash
python scripts/qpop.py verify ledger.jsonl     # from a clone; no install needed
# (a PyPI release, `pip install forward-qpop`, is planned)
```

```python
from forward_qpop import Ledger
led = Ledger("ledger.jsonl")
led.register("H-01", claim="…", prior=0.5,
             evidence=[{"summary": "…", "tier": "primary", "date": "2026-06-24"}])
led.verify()   # ok=True — any later edit/insert/reorder flips it to False
```

## Other tools

Claude Code is supported today. The discipline lives as portable markdown in [`skills/`](skills), so
Codex / other agents can adopt it by pointing at the skill files; first-class support for more agents
is planned.

## What this is not

Not investment advice, not a stock-picker, not a claim to beat the market. The finance domain is a
deliberately *adversarial testbed* (markets punish wishful thinking); `qpop` is a research
**discipline**. See [`DISCLAIMER.md`](DISCLAIMER.md) and [`ETHICS.md`](ETHICS.md).

## License

[MIT](LICENSE). Implements the **Forward-QPOP** protocol — see [`research/`](research) and
[`CITATION.cff`](CITATION.cff).

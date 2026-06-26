<!--
DRAFT — citations independently verified 2026-06-07 against arXiv/DOI pages; `references.bib` is the
source of truth (use it for the LaTeX build). Two first-draft errors were caught and fixed: a
FABRICATED entry ("Framing" on pre-analysis plans → replaced by Brodeur et al. 2024, JPE Micro) and
a WRONG-AUTHOR entry ("Ren et al." → actually Fritz-Morgenthal, Hein & Papenbrock 2022, Frontiers in
AI vol. 5). Still re-verify at camera-ready. This whole exercise is the framework's own
"verify, don't assert" discipline applied to its own paper.
-->

# Related Work

## 1. LLM and Agentic Systems for Investing and Financial Research

Domain-adapted language models have become the baseline for financial NLP. Wu et al. (2023)
introduced BloombergGPT, establishing strong financial-NLP performance but offering no decision
discipline or rejection mechanism [1]. Yang, Liu, & Wang (2023) released FinGPT as an open-source
counterpart [2]. Moving to autonomous agents, Ding et al. (2024) surveyed LLM trading agents,
finding that nearly all evaluation is in-sample relative to the model's training cutoff [3]. Xiao
et al. (2024) built TradingAgents, a bull/bear-debate multi-agent framework evaluated on backtest
Sharpe [4]; Zhang et al. (2024) contributed FinAgent, a multimodal agent reporting large backtested
profit improvements [5]. None impose a pre-registered hypothesis contract, an explicit
admission-rate target, or forward validation; their headline metrics are backtest Sharpe ratios
rather than the disciplined rejection of poor ideas. Two 2025–2026 results sharpen exactly this
point. Ye et al. (2026), in *The Alpha Illusion*, argue that reported alpha from end-to-end LLM
trading agents should not be treated as deployment evidence until it survives structural-validity
tests (temporal integrity, frictions, robustness, calibration, execution), and recommend positioning
the LLM as an upstream information interface feeding independent risk/execution modules — not as the
decision engine [21]. Lee et al. (2025), *Your AI, Not Your View*, give the first quantitative
analysis of LLMs' inherent investment biases (large-cap and contrarian preference, and confirmation
bias that makes models cling to an initial judgment against counter-evidence) [22]. Both motivate our
central design choice: the LLM *sources* hypotheses, but deterministic gates and a forward contract,
not the model's own confidence, decide whether anything is admitted.

## 2. LLM Failure Modes Relevant to Research

Three failure families matter here. **Hallucination/confabulation:** models fabricate plausible
facts beyond their training distribution, carrying direct fiduciary risk. **Sycophancy:** Malmqvist
(2024) catalogued how LLMs systematically agree with user-expressed views, generating false
confidence — critical when the model is asked to rate a thesis it also generated [7]. **Lookahead
leakage:** Gao, Jiang, & Yan (2025) showed that a positive lookahead-accuracy correlation is direct
evidence the model saw the answer in pre-training [8]; Li et al. (2025) showed strong backtested
LLM-agent returns collapse out-of-sample once leakage is controlled [10]. Benhenda (2026)
contributes *Look-Ahead-Bench*, a regime-generalization benchmark separating genuine predictive skill
from memorized patterns, finding standard LLMs exhibit significant look-ahead bias while
point-in-time models do not [23]; Roy & Roy (2026), *MemGuard-Alpha*, show in-sample accuracy rises
with memorization contamination while out-of-sample accuracy falls, and use cross-model disagreement
as a contamination signal [25]. Surveying the field, Kong et al. (2026) review 164 studies (2023–25)
and find no single bias — lookahead, survivorship, narrative, objective, or cost — is explicitly
addressed in more than ~28% of them, and propose a (retrospective, reviewer-facing) structural-
validity checklist [24]. At the factor level, Harvey, Liu, & Zhu (2016) showed most claimed return
factors are likely false discoveries from multiple comparisons, requiring a t > 3.0 threshold [9].
Our framework treats these as first-class *design* constraints rather than post-hoc review items:
deterministic gates before any expensive-model judgment, bear-case-before-recommendation, and forward
(not retrospective) validation.

## 3. Pre-Registration and Research-Integrity Methods

Nosek et al. (2018) argued the core value of preregistration is the sharp separation of prediction
from postdiction [11]. Casey, Glennerster, & Miguel (2012) gave the canonical economics
pre-analysis-plan application [12]. In finance, McLean & Pontiff (2016) documented that published
return predictors decay ~26% out-of-sample and ~58% post-publication, much of it data-mining bias
[13]; work on pre-analysis plans finds they suppress p-hacking only with a *detailed* plan, not
registration alone [14]. Closest to our setting, Hofman et al. (2023) adapt clinical-trial
pre-registration to predictive modeling, naming three reproducibility failures (overlooked
contextual factors, data-dependent decisions, unintentional test-set reuse) and giving a lightweight
ML pre-registration template [26]. Our **forward-QPOP** protocol extends this tradition with two
elements that template lacks: (i) a domain-specific *bottleneck* schema that makes pre-registration
portable across investment themes, and (ii) a *forward* outcome commitment — every hypothesis is
content-hashed before the market opens, evaluated on live paper-trading fills rather than historical
simulation, and the ledger is append-only — closing the loophole of testing on periods that postdate
the model's training cutoff.

## 4. Multi-Agent LLM Orchestration and Verification

Du et al. (2023) formalized multiagent debate to improve factuality [15]. Li et al. (2025) surveyed
"LLM-as-a-judge," identifying self-enhancement bias when generator and judge are the same model
[16]. Crucially, more judges do not mean less bias: Ma et al. (2025) show debate-based multi-agent
judging *amplifies* position, verbosity, chain-of-thought, and bandwagon biases after the first
round [27], and Zhao et al. (2026) measure sycophancy in *agentic financial* pipelines, finding most
models abandon a correct analytical position once a user preference is expressed [28]. These results
argue that an adversarial frame must be *structurally enforced*, not left to emergent debate — which
is exactly our bear-case-before-recommendation rule. The most methodologically adjacent work is
POPPER (Huang et al., 2025), which uses LLM agents to run sequential *falsification* experiments with
Type-I error control [29]. We differ on three axes a reviewer will probe: (i) **forward lock vs.
retroactive test** — POPPER validates a hypothesis against *already-existing* data and cannot stop a
researcher from running it after seeing the outcome, whereas our hypotheses are content-hashed and
dated *before* the out-of-sample window opens; (ii) **discovery vs. validation** — POPPER receives a
formed hypothesis, while our workflow begins before the hypothesis exists, sourcing candidate themes
through the bottleneck schema; (iii) **domain portability** — our schema carries finance-specific,
reusable evidence fields (chokepoint dimensions, dated triggers, source tiers) rather than generic
statistical falsification. Our design also keeps the cost discipline: a *cheaper* model gates and a
*more expensive* model evaluates only gate-passers, not all candidates.

## 5. Thematic / Supply-Chain / Chokepoint Investing; Factor Crowding

Factor crowding is well-established: Volpati et al. (2020) quantified crowding in standard factors
[18]; Lou & Polk (2022) showed "comomentum" predicts the reversal of crowded momentum [19]; Harvey
et al. (2016) frame the broader factor-zoo / false-discovery problem [9]. Our bottleneck-graph model
formalizes chokepoint identification as a structured schema (supply concentration, demand
inelasticity, substitutability, pricing power), and the confidence decomposition tracks crowding and
valuation as *gating* dimensions, so a thesis can be rejected on crowding grounds before any
simulation.

## 6. Trustworthy / Responsible AI in Finance

Fritz-Morgenthal, Hein & Papenbrock (2022) connected trustworthy-AI principles (fairness,
explainability, robustness, accountability) to financial risk management, arguing self-learning
models must archive full data and metadata after material changes [20]. Khatchadourian (2026) shows
empirically that decision determinism and task accuracy are *uncorrelated* in tool-using LLM
financial agents and that schema-first architectures give the most audit-compliant consistency [17],
while Buscemi et al. (2026) map EU AI Act high-risk requirements to concrete technical-verification
activities and document the gap between regulatory intent and current practice [30]. Regulatory
direction (EU AI Act 2024; NIST AI RMF) treats high-risk AI as requiring documented, auditable
decision trails — a standard backtest-centric agents do not meet. Our content-hashed, timestamped,
forward-validated, human-readable ledger makes the system's reasoning inspectable independently of
the LLM that produced it.

## 7. Live LLM-Trading Benchmarks and Auditable Trade Logs

A reviewer will rightly note that neither *forward evaluation* nor *tamper-evident logging* is, on
its own, novel — so we state precisely where the line is. Qian et al. (2025), *When Agents Trade*,
introduce the Agent Market Arena, a **lifelong, real-time multi-market benchmark** for LLM trading
agents, finding that agent architecture drives risk behavior more than the base LLM [31]. Chen et
al. (2025), *StockBench*, give a contamination-free sequential trading benchmark and find most LLM
agents fail to beat buy-and-hold [32]. On the engineering side, the open-source `llm-quant` system
records LLM paper-trades in a **SHA-256 hash-chained, git-tracked ledger** [33]. We borrow from this
last design — our Forward-QPOP ledger is likewise hash-chained — but our contribution is *not* the
immutable log. The distinction, which we make central: these systems evaluate or record **what an
agent *did*** in the market; ours forward-**locks a researcher-level hypothesis** (the
binding-chokepoint claim, dated evidence, and entry/update/exit triggers) to a hash-stamped record
**before the evaluation window opens**. Live evaluation tells you the outcome; the forward lock makes
the *prediction* auditable against that outcome, closing the gap that lets backtest- or
benchmark-based claims be rationalized after the fact.

## Gap We Fill

Existing work addresses individual validity threats in isolation: lookahead-bias diagnostics and
benchmarks [8, 23], structural-validity checklists applied *post-hoc* by reviewers [24], automated
falsification for *already-formed* hypotheses [29], output-layer auditability for tool-using
agents [17], and live trading benchmarks or hash-chained trade logs that record *executions* rather
than *pre-registered predictions* [31, 32, 33]. To our knowledge, no prior system ties these into a *prospective, forward-locked* workflow that
unifies all four capabilities: (a) agentic open-ended hypothesis discovery across thematic domains; (b)
deterministic gating that enforces source-tier, purity, and overlap rules *before* any expensive
model is invoked; (c) **forward pre-registration — not backtesting — as the evidentiary standard**,
immutable once content-hashed and dated; and (d) a portable cross-domain bottleneck schema that makes
the process reproducible and auditable without relying on any single LLM instance or training
snapshot. The combination is what converts the LLM from a decision engine into an auditable sourcing
tool. The closest peer, POPPER [29], shares the falsification spirit but validates a static
hypothesis against existing data; it has neither the forward temporal lock (which prevents
backfitting) nor the discovery phase nor the finance-portable schema.

## References

> Verified 2026-06-07; `references.bib` is the canonical source (BibTeX keys in brackets). Re-verify
> at camera-ready. `[14]` replaces a fabricated draft entry; `[20]` corrects a wrong-author draft entry.

[1] Wu, Irsoy, Lu, Dabravolski, Dredze, Gehrmann, Kambadur, Rosenberg, Mann (2023). *BloombergGPT: A Large Language Model for Finance*. arXiv:2303.17564. `[wu2023bloomberggpt]`
[2] Yang, Liu, Wang (2023). *FinGPT: Open-Source Financial Large Language Models*. FinLLM @ IJCAI 2023, arXiv:2306.06031. `[yang2023fingpt]`
[3] Ding, Li, Wang, Chen, Guo, Zhang (2024). *Large Language Model Agent in Financial Trading: A Survey*. arXiv:2408.06361. `[ding2024llmagentfinance]`
[4] Xiao, Sun, Luo, Wang (2024). *TradingAgents: Multi-Agents LLM Financial Trading Framework*. arXiv:2412.20138. `[xiao2024tradingagents]`
[5] Zhang et al. (2024). *A Multimodal Foundation Agent for Financial Trading: Tool-Augmented, Diversified, and Generalist*. arXiv:2402.18485. `[zhang2024finagent]`
[7] Malmqvist (2024). *Sycophancy in Large Language Models: Causes and Mitigations*. arXiv:2411.15287. `[malmqvist2024sycophancy]`
[8] Gao, Jiang, Yan (2025). *A Test of Lookahead Bias in LLM Forecasts*. arXiv:2512.23847. `[gao2025lookaheadbias]`
[9] Harvey, Liu, Zhu (2016). *…and the Cross-Section of Expected Returns*. Review of Financial Studies 29(1):5–68. `[harvey2016crosssection]`
[10] Li, Zeng, Xing, Xu, Xu (2025). *Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents*. arXiv:2510.07920. `[li2025profitmirage]`
[11] Nosek, Ebersole, DeHaven, Mellor (2018). *The preregistration revolution*. PNAS 115(11):2600–2606. `[nosek2018preregistration]`
[12] Casey, Glennerster, Miguel (2012). *Reshaping Institutions: Evidence on Aid Impacts Using a Preanalysis Plan*. QJE 127(4):1755–1812. `[casey2012reshaping]`
[13] McLean, Pontiff (2016). *Does Academic Research Destroy Stock Return Predictability?* Journal of Finance 71(1):5–32. `[mclean2016academic]`
[14] Brodeur, Cook, Hartley, Heyes (2024). *Do Preregistration and Preanalysis Plans Reduce p-Hacking and Publication Bias?* J. Political Economy Microeconomics 2(3):527–561. `[brodeur2024preregistration]`
[15] Du, Li, Torralba, Tenenbaum, Mordatch (2024). *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. ICML 2024, arXiv:2305.14325. `[du2024multiagentdebate]`
[16] Li, Jiang, Huang, Beigi, Zhao, Tan, Bhattacharjee, Jiang, Chen, Wu, Shu, Cheng, Liu (2025). *From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge*. EMNLP 2025, arXiv:2411.16594. `[li2025llmjudge]`
[17] Khatchadourian (2026). *Replayable Financial Agents: A Determinism-Faithfulness Assurance Harness for Tool-Using LLM Agents*. ICLR 2026 Workshop on Advances in Financial AI, arXiv:2601.15322. `[khatchadourian2026replayable]`
[18] Volpati, Benzaquen, Eisler, Mastromatteo, Toth, Bouchaud (2020). *Zooming In on Equity Factor Crowding*. Journal of Risk 23(1), arXiv:2001.04185. `[volpati2020crowding]`
[19] Lou, Polk (2022). *Comomentum: Inferring Arbitrage Activity from Return Correlations*. Review of Financial Studies 35(7):3272–3302. `[lou2022comomentum]`
[20] Fritz-Morgenthal, Hein, Papenbrock (2022). *Financial Risk Management and Explainable, Trustworthy, Responsible AI*. Frontiers in Artificial Intelligence 5:779799. `[fritzmorgenthal2022xai]`

> Added 2026-06-07 (methods literature watch). Every id below re-verified on arxiv.org AND
> export.arxiv.org by an adversarial refute-by-default auditor: 12/12 confirmed, 0 rejects.

[21] Ye, Han, Hu, Bu, Chen, Wen, Mandic, Sun, Yinghui, Xu (2026). *The Alpha Illusion: Reported Alpha from LLM Trading Agents Should Not Be Treated as Deployment Evidence*. arXiv:2605.16895. `[ye2026alphaillusion]`
[22] Lee, Seo, Park, Lee, Ahn, Choi, Lopez-Lira, Lee (2025). *Your AI, Not Your View: The Bias of LLMs in Investment Analysis*. ACM ICAIF 2025, arXiv:2507.20957. `[lee2025yourai]`
[23] Benhenda (2026). *Look-Ahead-Bench: a Standardized Benchmark of Look-ahead Bias in Point-in-Time LLMs for Finance*. arXiv:2601.13770. `[benhenda2026lookaheadbench]`
[24] Kong, Lee, Hwang, Lopez-Lira, Levy, Mehta, Wen, Choi, Lee, Zohren (2026). *Evaluating LLMs in Finance Requires Explicit Bias Consideration*. arXiv:2602.14233. `[kong2026evaluating]`
[25] Roy, Roy (2026). *MemGuard-Alpha: Detecting and Filtering Memorization-Contaminated Signals in LLM-Based Financial Forecasting via Membership Inference and Cross-Model Disagreement*. arXiv:2603.26797. `[roy2026memguard]`
[26] Hofman, Chatzimparmpas, Sharma, Watts, Hullman (2023). *Pre-registration for Predictive Modeling*. arXiv:2311.18807. `[hofman2023preregistration]`
[27] Ma, Zhang, Zhao, Liu, Jia, Qing, Shi, Cohan, Yan, Vosoughi (2025). *Judging with Many Minds: Do More Perspectives Mean Less Prejudice? On Bias Amplifications and Resistance in Multi-Agent Based LLM-as-Judge*. arXiv:2505.19477. `[ma2025judging]`
[28] Zhao, Balagopalan, Agrawal, Yergasheva, Alshikh, Bikel (2026). *The Price of Agreement: Measuring LLM Sycophancy in Agentic Financial Applications*. ICLR 2026 FinAI Workshop, arXiv:2604.24668. `[zhao2026priceofagreement]`
[29] Huang, Jin, Li, Li, Candès, Leskovec (2025). *Automated Hypothesis Validation with Agentic Sequential Falsifications* (POPPER). ICML 2025, arXiv:2502.09858. `[huang2025popper]`
[30] Buscemi, Deckenbrunnen, Kabir, Mishchenko, Mowla (2026). *Assessing High-Risk AI Systems under the EU AI Act: From Legal Requirements to Technical Verification*. arXiv:2512.13907. `[buscemi2026euaiact]`
[31] Qian et al. (2025). *When Agents Trade: Live Multi-Market Trading Benchmark for LLM Agents* (introduces Agent Market Arena). arXiv:2510.11695. `[qian2025whenagents]`
[32] Chen, Yao, Liu, Xin, Ye, Yu, Hou, Li (2025). *StockBench: Can LLM Agents Trade Stocks Profitably In Real-world Markets?* arXiv:2510.02209. `[chen2025stockbench]`
[33] 45ck (2025). *llm-quant: LLM-Powered Paper Trading System with a Tamper-Evident SHA-256 Trade Ledger*. GitHub: github.com/45ck/llm-quant. `[45ck2025llmquant]`

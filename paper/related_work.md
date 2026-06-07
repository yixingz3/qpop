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
rather than the disciplined rejection of poor ideas.

## 2. LLM Failure Modes Relevant to Research

Three failure families matter here. **Hallucination/confabulation:** models fabricate plausible
facts beyond their training distribution, carrying direct fiduciary risk. **Sycophancy:** Malmqvist
(2024) catalogued how LLMs systematically agree with user-expressed views, generating false
confidence — critical when the model is asked to rate a thesis it also generated [7]. **Lookahead
leakage:** Gao, Jiang, & Yan (2025) showed that a positive lookahead-accuracy correlation is direct
evidence the model saw the answer in pre-training [8]; Li et al. (2025) showed strong backtested
LLM-agent returns collapse out-of-sample once leakage is controlled [10]. At the factor level,
Harvey, Liu, & Zhu (2016) showed most claimed return factors are likely false discoveries from
multiple comparisons, requiring a t > 3.0 threshold [9]. Our framework treats these as first-class
design constraints: deterministic gates before any expensive-model judgment, bear-case-before-
recommendation, and forward (not retrospective) validation.

## 3. Pre-Registration and Research-Integrity Methods

Nosek et al. (2018) argued the core value of preregistration is the sharp separation of prediction
from postdiction [11]. Casey, Glennerster, & Miguel (2012) gave the canonical economics
pre-analysis-plan application [12]. In finance, McLean & Pontiff (2016) documented that published
return predictors decay ~26% out-of-sample and ~58% post-publication, much of it data-mining bias
[13]; work on pre-analysis plans finds they suppress p-hacking only with a *detailed* plan, not
registration alone [14]. Our **forward-QPOP** protocol imports this tradition: every hypothesis is
content-hashed before the market opens, evaluated on live paper-trading fills rather than historical
simulation, and the ledger is append-only — closing the loophole of testing on periods that
postdate the model's training cutoff.

## 4. Multi-Agent LLM Orchestration and Verification

Du et al. (2023) formalized multiagent debate to improve factuality [15]. Li et al. (2025) surveyed
"LLM-as-a-judge," identifying self-enhancement bias when generator and judge are the same model
[16]. Our design differs: (a) a *cheaper* model gates and a *more expensive* model evaluates only
gate-passers, not all candidates; (b) the bear case is written first, structurally preventing
sycophantic endorsement; (c) the recommendation is validated forward, not by a retrospective rubric.

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
models must archive full data and metadata after material changes [20]. Regulatory direction (EU AI Act 2024; NIST AI RMF) treats
high-risk AI as requiring documented, auditable decision trails — a standard backtest-centric agents
do not meet. Our content-hashed, timestamped, forward-validated, human-readable ledger makes the
system's reasoning inspectable independently of the LLM that produced it.

## Gap We Fill

No prior system unifies all four capabilities: (a) agentic open-ended hypothesis discovery across
thematic domains; (b) deterministic gating that enforces source-tier, purity, and overlap rules
*before* any expensive model is invoked; (c) **forward pre-registration — not backtesting — as the
evidentiary standard**; and (d) a portable cross-domain bottleneck schema that makes the process
reproducible and auditable without relying on any single LLM instance or training snapshot.

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

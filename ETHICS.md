# Ethics & Responsible Use

This statement accompanies the framework and the paper. AI-in-finance venues (e.g. ACM ICAIF) and
responsible-AI norms expect it; it is also simply the right thing to publish.

## Not investment advice; no performance claim

The framework is a *research methodology*. It is **not** investment advice and makes **no claim of
investment performance**. There is no asserted live track record. The empirical claims are
*methodological* (admission rate, discipline behavior, auditability), not claims of profit. See
[`DISCLAIMER.md`](DISCLAIMER.md).

## Intended use and misuse

- **Intended:** disciplined, auditable, reproducible thematic research; studying how to use LLM agents
  responsibly for hypothesis generation; education.
- **Foreseeable misuse:** presenting LLM-generated theses as advice; over-trusting un-verified model
  output; "copy these trades." The design *reduces* but cannot eliminate these risks — every output
  requires independent human verification. The repo deliberately does **not** publish live positions
  or trades, to avoid a "follow my trades" reading.

## Market-impact and fairness

The system is a single-account research tool operating in liquid public equities; it is not designed
for and should not be used for market manipulation, coordinated activity, or anything that degrades
market fairness. Crowding is treated as a *risk to penalize*, not a signal to exploit at others'
expense.

## LLM use, limitations, and disclosure

- LLMs can hallucinate, be out of date, or be sycophantic. The framework's gates and bear-case-first
  rule are mitigations, not guarantees.
- Model versions and dates are recorded for reproducibility. The paper discloses where LLMs were used
  (sourcing, evaluation, and — disclosed — drafting/literature assistance that was then human-verified).
- Determinism is limited; results may vary across model versions. This is stated as a threat to validity.

## Data, compliance, and secrets

- Respect every data provider's and broker's terms. **No paid-data exports, broker credentials, live
  logs, or trade records** belong in this (public) repository; `.gitignore` covers the obvious cases,
  but the human is responsible.
- Anyone adapting this for live capital does so at their own risk and is solely responsible for legal,
  regulatory, and tax compliance.

## Conflicts of interest

Any financial interest of the authors in names discussed in examples is disclosed in the paper. The
example domains illustrate the *method*; example names are not endorsements.

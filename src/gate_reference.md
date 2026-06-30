# Deterministic gate — reference

The GATE is pure, reproducible, and **invokes no LLM**. It runs between SOURCE and the expensive
stages and is the cheapest, most auditable filter in the funnel. Given a candidate `(symbol, node)`
and the held book, it returns PASS (→ finalist) or FAIL (→ watchlist, never "free capacity").

```
def gate(symbol, node, book, prices, beta_series):
    # 1. Tradeability — the symbol must be a tradeable instrument in the venue.
    if not is_tradeable(symbol):                      return FAIL("untradeable / foreign-only")

    # 2. Liquidity — enough turnover to enter/exit a satellite without moving the print.
    last_price = prices[symbol].last
    adv_dollar = mean(prices[symbol].close * prices[symbol].volume, window=60)   # 60-day $ volume
    if last_price < MIN_PRICE:                         return FAIL("price floor")
    if adv_dollar < MIN_ADV_DOLLAR:                    return FAIL("liquidity floor")

    # 3. Overlap penalty — judge AGAINST the book you already hold (replace, don't stack).
    corr = max(correlation(returns[symbol], returns[h], window=60) for h in book.core)
    same_node = book.weight_in(node)                   # existing exposure in this node
    overlap_penalty = f(corr, same_node)               # 0 if orthogonal; rises with corr / node load
    #   overlap is a COMPARISON, not a veto: a name that duplicates a held bet must beat it to enter.

    return PASS(metrics = {adv_dollar, last_price, corr, overlap_penalty,
                           candidate_beta, gross_ai_beta})
```

Notes:

- **No model, no narrative** — every output is a number from price/volume/correlation, so the gate is
  byte-reproducible and cheap. A name that fails is *watchlist*, never counted as available capacity.
- **Missing data is conservative.** A missing beta or price uses a conservative fallback (never reads
  as zero risk); a name with un-checkable data is held out, not assumed safe.
- **Thresholds** (`MIN_PRICE`, `MIN_ADV_DOLLAR`, the overlap function) are config, not code — they are
  declared per domain and logged per run. The point is that the *decision* is deterministic given the
  config and the price data, independent of any LLM instance.
- The subjective scoring (bottleneck / purity / demand / valuation / crowding) and exit triggers stay
  a human-or-expensive-model call in a pre-registered admission entry — the gate only decides
  *tradeable + liquid + non-duplicative*, the things a script can settle.

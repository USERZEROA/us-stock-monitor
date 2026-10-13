# Premarket Report Evaluation Rubric

Score: 0 to 100. A report with a hard-fail item cannot pass even if the numeric
score is high.

## Scoring

| Category | Points | Checks |
|---|---:|---|
| Date, weekday, session state | 10 | Correct date, weekday, market hours, holiday status, and observation window |
| Event timing accuracy | 10 | Correct official times for macro releases, Fed events, earnings, auctions, and market sessions |
| Fact support and groundedness | 15 | Core facts have links, timestamps, and sources that actually support the text |
| Source quality | 10 | Uses first-party or authoritative sources for official facts; labels weaker sources |
| Core event coverage | 10 | Captures major macro, policy, earnings, sector, and overnight market drivers |
| Deduplication and freshness | 5 | Avoids repeated old news and separates new facts from recycled context |
| Analysis/fact separation | 8 | Clearly separates confirmed facts, market reaction, analysis, and unconfirmed items |
| Numbers, units, baselines | 8 | Uses correct units, comparisons, timestamps, revisions, and prior/expected/actual separation |
| Earnings and macro structure | 8 | Separates actuals, consensus, prior values, revisions, guidance, and call timing |
| Action list quality | 8 | Watchlist has catalysts, triggers, invalidation conditions, and risk level |
| Delivery and completeness | 4 | Telegram report is delivered completely and in readable segments |
| Contrary evidence | 4 | Includes important reverse evidence or why it is unavailable |

## Hard-Fail Items

- Fabricated news or numbers.
- Severe date error.
- Links do not support the claim.
- Treating a market holiday or closure as a regular open.
- Credential or token leakage.
- Unevidenced deterministic buy/sell advice.

## Independent Evaluator Requirement

The evaluator must be separate from the report-generation step. Evaluation
notes must cite concrete report lines, source links, and observed failures.
Do not let the report author declare its own report qualified without this
rubric-based check.

## Prompt Optimization Metrics

Monthly prompt optimization must compare:

- Total score
- Date accuracy
- Groundedness
- Source quality
- Coverage
- Hallucination rate
- Token use
- Elapsed time
- Hard-fail count

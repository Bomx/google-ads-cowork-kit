# 1. Account review

Use with `PROMPT.md` and the completed brief.

## Inputs

Required: a keyword or campaign performance export with cost, impressions, clicks, conversions, stable IDs, and the report period. Include conversion value only if it measures the business outcome in the brief. Useful extras: prior comparable period, bid strategy, budget status, conversion-action breakdown, change log, and tracking-health notes.

## Copy-paste task

Review the supplied performance export. First report its grain, coverage, and missing fields. Start with rows spending at least 20 account-currency units with zero reported conversions, unless my brief supplies a different threshold. Label these **review candidates**, not waste or pause instructions. Sort by spend descending and show their share of this report's spend, without implying it is a share of the whole account if coverage is partial.

For each candidate, list cost, clicks, conversions, CPA (`N/A` if none), source row, conversion-lag caveat, and the next diagnostic step. Check tracking health, campaign maturity, intent, lead quality, and economics before recommending a change. Separate rows below threshold into a watchlist when useful.

Summarize totals using weighted metrics. If campaign types differ, segment Search, Shopping, Display, and Performance Max rather than treating them as interchangeable. Do not rank brand against prospecting purely on CPA. Flag high-value converting rows for investigation as well, but never assume they can absorb unlimited extra budget.

If previous-period data is available and comparable, show deltas. If not, say there is no supported trend conclusion. Limit the executive summary to five findings and three proposed decisions.

## Deliverables and review

- `01-account-review.md`: scope, totals, ranked table, caveats, next checks.
- `01-review-candidates.csv`: IDs, source records, spend, conversions, reason, proposed diagnostic.
- Decision register entries, all proposed.

Verify total spend against the exact included rows. Do not call all zero-conversion spend recoverable savings. Automated rules, pausing, bid changes, and edits to conversion tracking are outside this workflow.

# Account review: selected keywords

**SYNTHETIC EXAMPLE · USD · Nov 1–6, 2026 · Search**

Scope: six selected keywords, not the full account. Source: `examples/inputs/keywords.csv`, records 2–7. Conversions are demo requests with up to seven days' lag and no lead-quality validation.

## What the data shows

- Subset spend: USD 400; clicks: 152; impressions: 5,300; conversions: 6.5.
- Weighted CPA: 400 / 6.5 = USD 61.54. CTR: 152 / 5,300 = 2.87%. CPC: 400 / 152 = USD 2.63.
- Two keywords meet the USD 20, zero-conversion triage rule. Their combined USD 89 is 22.25% of **this subset's** spend, not of full-account spend and not proven recoverable savings.

| Priority | Keyword and ID | Source record | Cost | Clicks | Conversions | CPA | Next check |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | free crm spreadsheet / K02 | 3 | 64 | 32 | 0 | N/A | Review actual queries; downloadable spreadsheet intent is outside the supplied offer |
| 2 | crm jobs / K03 | 4 | 25 | 10 | 0 | N/A | Review employment queries and existing exclusions |

K04, “agency crm comparison,” has USD 19 spend and zero conversions. It is below the threshold and has plausible buying intent. Monitor it; do not automatically exclude it. K05's 1.5 conversions are valid fractional attribution and must not be rounded before calculation.

## Decisions to review

1. Review the exact query-level exclusions in workflow 2. Keyword text alone is not enough to choose a broad negative.
2. Verify conversion tracking and allow for lag before calling recent spend unproductive.
3. Revisit mature data and qualified lead results before discussing bids or budget allocation.

Confidence: high in the arithmetic; moderate in intent classification from the brief; low in any performance conclusion because the sample is small, recent, and incomplete. No target CPA, profitability benchmark, or prior keyword period was supplied. No live changes made.

# Data contract and optional checks

The prompts work from clearly described exports. `tools/ads_checks.py` only accepts **normalized UTF-8 CSV** with one header row and exactly the listed field names, in any order. UTF-8 BOM is accepted. Do not pass raw Google Ads downloads with report titles, totals, currency symbols, percentages, localized decimals, or segment duplication.

## Common rules

- Fields must be present; no blank rows/IDs or header-only files. IDs are opaque text, not numbers. Use one account per file.
- Numerical inputs are finite nonnegative decimal numbers; zero is valid. Nonzero values must be at least `0.000000000001` and less than `10000000000000000000`. No currency symbols or thousands separators.
- Clicks and impressions are whole numbers. Conversions may be fractional.
- Totals/subtotals are not data rows. Duplicate records at the intended grain are rejected, not silently summed.
- Data errors exit with code 2 and identify the file/CSV record. CSV source rows count the header as row 1.
- Output is CSV to stdout. `--output path.csv` also saves a new file and refuses to overwrite an existing file or the input. Keep private outputs outside tracked examples.
- Decimal results are displayed to at most six decimal places. `null` means undefined, not zero. The utility does not check currency, date-range coverage, conversion quality, or source completeness: you must verify those in the brief.
- Free-text cells that could execute spreadsheet formulas are prefixed with an apostrophe on export. Treat all CSV content as untrusted when opening it in a spreadsheet.

## `audit`

```text
campaign_id,ad_group_id,keyword_id,keyword,cost,clicks,impressions,conversions
```

One row per `(campaign_id, ad_group_id, keyword_id)` for one period. Cost uses the account's currency, not micros. No cross-report aggregation. The tool emits every input row with source row, CPA, status, and reason. `review` means `cost >= threshold AND conversions == 0`. `no_flag` is only the result of that mechanical rule; it does not mean the keyword is healthy. CPA is `null` at zero conversions.

```bash
python3 tools/ads_checks.py audit data/keywords.csv --threshold 20 --output outputs/review.csv
```

The default 20 reflects the post's USD example. Change it for your currency, margin, target CPA, and conversion lag. Neither the script nor the prompt pauses keywords.

## `pacing`

```text
campaign_id,campaign,monthly_plan,spend_mtd
```

One row per campaign; independent monthly plans only. For shared budgets, consolidate to one pool row with a stable pool ID and label; do not count the same shared plan once per campaign. `--as-of YYYY-MM-DD` is the inclusive last fully complete date in the account timezone. Spend must cover day 1 through that date. Future dates, partial days, and wrong-month exports cannot be detected from this CSV alone.

```bash
python3 tools/ads_checks.py pacing data/budget-plan.csv --as-of 2026-11-06
```

The output calculates calendar-month elapsed/remaining days, straight-line expected spend and projection, signed remaining plan, and a nonnegative remaining daily allowance. At month end, the allowance is `null` because no days remain. `over_plan` means the linear projection exceeds plan, including overspend at month end; `within_plan` also includes underdelivery. `month_complete` labels a completed month that did not exceed plan.

These figures are **business-plan arithmetic, not Google Ads budget settings or hard caps**. They do not model seasonality, day-of-week demand, promotions, shared-budget allocation, conversion quality, or platform overdelivery.

## `rsa`

```text
campaign_id,ad_group_id,asset_type,text
```

One row per asset. Allowed types: `headline` (30), `description` (90), `path` (15). Identical scoped asset rows are rejected. Leading/trailing whitespace and control/format characters are invalid; ordinary spaces inside text are allowed. East Asian W/F characters count as two. Unusual scripts, combining sequences, emoji, and actual platform validation still require manual review.

```bash
python3 tools/ads_checks.py rsa outputs/rsa-assets.csv
```

The output gives each asset's character count, limit, and pass/fail. Any overlength asset exits 1 after writing the report. Valid lengths exit 0. Schema/input errors exit 2. It does **not** validate minimum asset counts, policy compliance, spelling, destination URLs, claim accuracy, pinning, or live Google Ads acceptance. One RSA needs at least three headlines and two descriptions; these prompts target 15 and 4 when the evidence supports them.

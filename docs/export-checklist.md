# Export checklist

## Before you export

- Use the account timezone and one currency. Record both in the brief.
- Choose the last fully complete date; do not mix a partial day with complete prior days.
- Record campaign types, filters, conversion actions, attribution settings, and normal conversion lag.
- Use `Conversions` consistently unless the brief explicitly specifies another measure. Do not combine `Conversions` with `All conversions`.
- Export IDs as text. Spreadsheet apps can round long IDs or remove leading zeros.
- Remove personal search-query details where possible. Do not include customer lists, emails, phone numbers, lead records, account credentials, or payment information.

## Reports to gather

Google Ads navigation changes. Use the relevant reporting table or Report editor, choose the fields below, and download CSV. No API access is needed.

| File | Needed fields | Grain and period |
| --- | --- | --- |
| Campaign performance | Campaign ID/name/type, impressions, clicks, cost, conversions; value if useful | One row per campaign for one period |
| Keyword performance | Campaign/ad-group/keyword IDs, keyword, impressions, clicks, cost, conversions | One row per keyword for one period; no device/day segments |
| Search terms | Campaign/ad-group IDs, search term, match type, clicks, cost, conversions | One row per observed query and scope for one period |
| Existing negatives | Text, match type, scope, scope IDs, shared-list attachment if any | Current configuration snapshot |
| Ads | Stable ad label/ID, ad-group IDs, assets, final URLs, status | Current configuration snapshot |
| Budget plan | Campaign IDs, approved monthly plan, MTD spend | Day 1 through the complete-through date |
| Change log | Date, scope, change, status, evidence | Completed changes distinct from proposals |

For weekly comparisons, export two comparable periods with the same filters and conversion definitions. For budget pacing, use the month-to-date period even when it differs from the weekly report. Keep the files clearly named.

## Normalize a copy, never the original

1. Keep original downloads outside this public repository. Use a private `data/` directory or a separate folder.
2. Remove report-title/date preamble lines and total/subtotal/footer rows from the normalized copy.
3. Map column names explicitly. For example `Cost` → `cost`, `Ad group ID` → `ad_group_id`. A click or impressions column is a whole-number count. `Conversions` may be fractional.
4. Resolve locale: `1,234.56` and `1.234,56` mean different things. Normalize to `1234.56`, no currency sign or thousands separator. Never infer locale from one ambiguous number.
5. Missing, `--`, or suppressed values are not zero. Resolve them or hold that calculation.
6. If data is segmented by day, device, network, or conversion action, aggregate additive metrics to the intended grain first. Do not add overlapping segments, total rows, or different conversion metrics.
7. Confirm normalized spend against the original report for the same scope. Record excluded rows and reasons. Search-term totals may be lower than campaign totals because some queries are not reported.
8. Follow the exact headers in [data-contract.md](data-contract.md) for the optional Python checks. The AI prompts can work with raw exports after explicit normalization, but the utility intentionally cannot guess export structure.

## Approval and privacy

You control what is shared with your AI provider. Check your client agreement and organization's rules first. No tool in this repository uploads data. Do not commit real account exports, generated client reports, environment files, or authentication material to GitHub. `.gitignore` helps with common folders but is not a security boundary: check every file before committing.

# Sources and limitations

Checked November 7, 2026. Product interfaces and policies change; check the linked official sources before applying live changes.

- [Original post](https://www.linkedin.com/feed/update/urn:li:activity:7524856591204941824/): the seven workflow topics and export-first, approval-first approach. This kit expands those topics into original prompts, templates, tools, and fictional examples. It is not a claimed export of a previously running automation.
- [Google: responsive search ads](https://support.google.com/google-ads/answer/7684791): headline, description, and path limits; asset minimums/maximums; double-width character rule. The kit uses 30/90/15, up to 15 headlines and 4 descriptions. Actual platform review remains necessary.
- [Google: negative keywords](https://support.google.com/google-ads/answer/2453972): Search negative broad, phrase, and exact behavior. Negative keywords do not behave like positive keyword match types. Review current rules and protected queries before implementation.
- [Google: average daily budgets](https://support.google.com/google-ads/answer/6385083): most campaigns' daily and monthly spending-limit relationship. Our calendar-month plan arithmetic is separate from the platform's 30.4-day average budget system.
- [Anthropic: getting started with Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork): current availability and file-work setup. This kit does not need a custom connector or a Google Ads login.

## What has and has not been validated

The Python utility is covered by local unit tests for input handling, arithmetic, CSV safety, and character-length checks. The worked sample outputs use synthetic inputs and explicit calculations. The prompts are human-readable task instructions, not a deterministic ad-management product.

No live Google Ads account was connected, no production campaign was changed, and no real client performance data is included. Cowork behavior, ad-policy acceptance, profitability, and account-specific recommendations are not end-to-end certified by these tests. Human review is part of every workflow.

Competitor examples are invented teaching material using reserved `.example` domains. Do not treat them as market research. Conversion value is omitted in the sample because a lead is not automatically revenue.

# Google Ads Cowork Kit

**Seven practical workflows. One clear brief. Review every change before it goes live.**

The companion kit to [Borja Obeso's seven-workflow LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7524856591204941824/). Turn Google Ads exports into an account review, negative-keyword proposals, competitor insights, RSA drafts, landing-page checks, budget pacing, and a client-ready weekly draft.

Start with files you choose. No Google Ads login, API key, paid integration, or automatic campaign changes required. Cowork access itself depends on your Claude plan. You can also use the prompts in another assistant that can read your files.

## Start here: no code needed

1. Download this repository using **Code → Download ZIP**, then unzip it.
2. Try the fictional account in [examples/inputs](examples/inputs) first. For your own account, complete [the brief](templates/account-brief.md) and follow [the export checklist](docs/export-checklist.md).
3. In Cowork, attach the selected inputs and relevant prompt files, or grant access to a dedicated folder containing only those files. Do not grant access to unrelated client folders. Follow [Claude's current setup guide](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) if the interface differs.
4. Copy [PROMPT.md](PROMPT.md) into the task. Choose one workflow, or ask for all seven after checking the inputs.
5. Review the evidence, calculations, and proposed changes. Apply approved changes yourself in Google Ads, then record what happened in the change log.

**Try this first:**

> Read PROMPT.md and workflows/01-account-review.md. Use examples/inputs/account-brief.md and examples/inputs/keywords.csv. Produce an account review, clearly labeled as a fictional demonstration. Do not access or change any live account.

Expected finding: two keywords have at least USD 20 spend and zero reported conversions, totaling **USD 89**. These are review candidates, not proven waste. [See the worked example](examples/outputs/01-account-review.md).

## Pick a workflow

| Workflow | Give it | Get back |
| --- | --- | --- |
| [1. Account review](workflows/01-account-review.md) | Keyword or campaign export, brief, conversion context | Prioritized review with source rows and caveats |
| [2. Search queries](workflows/02-search-queries.md) | Search terms, current negatives, protected terms | Proposed negatives, scope, match type, and conflict checks |
| [3. Competitor audit](workflows/03-competitor-audit.md) | Captured competitor ads/pages and your own | Evidence-backed comparison and original test ideas |
| [4. RSA copy](workflows/04-rsa-copy.md) | Ad-group intent, approved facts, landing pages | 15 headlines and 4 descriptions per group, with counts |
| [5. Ad-to-page match](workflows/05-ad-page-match.md) | Ad copy and captured destination pages | Promise/evidence matrix and specific fixes |
| [6. Budget checks](workflows/06-budget-pacing.md) | MTD spend, monthly plan, complete-through date | Pacing, projected spend, review priorities |
| [7. Weekly summary](workflows/07-weekly-summary.md) | Comparable exports and actual change log | Client-ready draft separating facts from proposals |

The [master prompt](PROMPT.md) handles missing inputs, confidentiality, calculation rules, and approvals. The [sample output pack](examples/outputs/README.md) shows the quality bar for all seven workflows.

## What is included

- Copy-paste master prompt and seven task-specific prompts.
- An account brief, normalized CSV templates, decision register, and weekly-report template.
- A consistent fictional example account with source references and worked outputs.
- Optional offline Python checks for zero-conversion spend, calendar-month pacing, and RSA character limits.
- Tests and GitHub Actions validation. Nothing calls Google Ads or sends data to an API.

## Optional: check the numbers locally

Python 3.10 or later; no packages to install. Run from the repository folder:

```bash
python3 tools/ads_checks.py audit examples/inputs/keywords.csv
python3 tools/ads_checks.py pacing examples/inputs/budget-plan.csv --as-of 2026-11-06
python3 tools/ads_checks.py rsa examples/outputs/04-rsa-assets.csv
python3 -m unittest discover -s tests -v
```

Use `python` instead of `python3` if that is your Python command. Run a subcommand with `--help` for options. The tools use the normalized templates, **not arbitrary raw Google Ads exports**. [Read the data contract](docs/data-contract.md) before using your own files. They are mechanical checks, not optimization recommendations or full policy checks.

## A few rules that matter

- USD 20 with zero conversions is the post's starting triage rule, not a universal pause rule. Use your account's currency and economics. Check conversion lag, tracking, lead quality, and sample size.
- Search-term reports may omit queries. Keyword, query, and campaign reports overlap: never add them together.
- Do not exclude every zero-conversion query. Protect buying intent and check the blast radius of negative match types.
- Monthly plan pacing is not a guaranteed Google Ads billing cap. Daily budgets can overdeliver; budget changes and shared budgets require separate review.
- AI can make up numbers, claims, and character counts. Check against the source files and the actual Google Ads editor.
- Do not upload customer lists, personal lead details, credentials, or confidential client data without permission. The examples are entirely synthetic. The optional scripts run locally; using Cowork shares selected data with that service under your account's settings.

## About

By [Borja Obeso / Distribb](https://distribb.io). For more practical walkthroughs: [Distribb on YouTube](https://youtube.com/@distribbapp).

Independent educational resource. Not affiliated with or endorsed by Google or Anthropic. No performance, savings, or revenue guarantees. [Sources and limitations](docs/sources-and-limitations.md).

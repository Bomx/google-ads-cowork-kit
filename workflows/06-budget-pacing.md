# 6. Budget checks

Use with `PROMPT.md` and the completed brief.

## Inputs

Campaign IDs, monthly spend plan, and MTD spend from day 1 through the last **fully completed account-timezone date**. Include current daily budget, shared-budget membership, bid strategy, planned pauses/promotions, and performance/quality evidence if available. Do not infer these from the spend plan.

## Copy-paste task

Confirm currency, month, account timezone, and inclusive complete-through date. Do not use today's partial spend as a completed day. Check that each campaign's spend starts on the first of the same month and does not contain duplicate segments. Separate shared-budget pools before proposing campaign changes.

Calculate using actual calendar days:
- elapsed days = day number of the complete-through date.
- remaining days = days in month minus elapsed days.
- expected spend to date = monthly plan × elapsed days / days in month.
- straight-line month-end projection = MTD spend / elapsed days × days in month.
- remaining plan = monthly plan minus MTD spend (retain negative values).
- remaining daily allowance = max(0, remaining plan) / remaining days; `N/A` at month end.

Show assumptions and the projection gap. This is a straight-line scenario, not a forecast with confidence intervals or a spending guarantee. Use day-of-week/seasonality scenarios only if enough historical evidence was supplied, and label them separately.

Prioritize campaigns projected above plan, then those below plan. Recommend “review cap/reallocation” or “investigate underdelivery” rather than mechanically raising spend. Raising a campaign requires verified efficiency, qualified conversions, headroom, and a specific amount approved by the account owner. Underspend alone is not a reason to spend more.

Do not equate the remaining daily allowance to Google's average daily budget setting. For most campaigns, Google describes daily spending limits of up to twice the average daily budget and a monthly limit based on 30.4 times that setting. Mid-month changes, budget types, and shared budgets complicate the limit. Check the platform's budget report before translating a plan into a setting.

## Deliverables and review

- `06-budget-pacing.csv`: calculations with date, units, and campaign IDs.
- `06-budget-review.md`: top risks, scenarios, missing context, exact decisions needed.

No budget or bid changes. Get approval for the amount, scope, effective date, and monitoring plan before implementation outside this kit.

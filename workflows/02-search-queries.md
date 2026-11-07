# 2. Search-query review

Use with `PROMPT.md` and the completed brief. This workflow covers **Search** query intent, not a universal cross-network exclusion strategy.

## Inputs

Required: search terms with campaign/ad-group IDs, cost, clicks, conversions; an offer/audience brief; protected brands/products/intents. Supply existing account/campaign/ad-group negatives and their match types when possible. If unavailable, mark existing-conflict checking incomplete.

## Copy-paste task

Classify observed queries as buying intent, irrelevant to this offer, ambiguous, or needing more data. Use the business brief, not zero conversions alone. Protect converting terms, brand/product names, high-intent commercial terms, and legitimate uses of words like “free,” “jobs,” or “training” when those are part of the offer.

Propose a negative only when its intent is clearly out of scope. Prefer the narrowest safe scope and match type. For each proposal provide the observed query, exact proposed negative text, negative match type, campaign/ad-group scope, cost, clicks, conversions, source row, reason, risk, and confidence.

Explain the blast radius: exact negatives target the matching full query; phrase negatives can block queries containing that ordered phrase; broad negatives can block queries containing all words in any order. Negative matching differs from positive matching. Do not assume synonyms, singulars, plurals, or all other close variants are covered. Check the current Google documentation if finer matching behavior matters.

For every negative, list at least one valuable query it must not block and test the proposal against the supplied converting/protected queries. Check current negatives for duplicates and conflicts. If a conflict remains or data is missing, mark `needs review`; do not silently widen the scope or convert it to an account-wide exclusion.

Keep ambiguous terms in a monitor list with the next evidence needed. A small sample or recent conversion lag can explain zero conversions. Show the search-report coverage caveat: missing queries and hidden terms mean the report is not necessarily complete account traffic.

## Deliverables and review

- `02-query-review.md`: classification and assumptions.
- `02-proposed-negatives.csv`: use the provided template; status remains proposed.
- Protected and ambiguous query lists.

This is a review format, **not a Google Ads import file**. Approve the exact negative, match type, scope, and intended account before entering it in Google Ads. Do not bulk upload or attach a shared negative list.

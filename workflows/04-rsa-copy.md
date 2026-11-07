# 4. Responsive search ad copy

Use with `PROMPT.md` and the completed brief.

## Inputs

Ad-group IDs and distinct intent, top relevant search terms, existing assets, final URL, and approved landing-page facts. Missing pricing, guarantees, certifications, discounts, or results must not be invented.

## Copy-paste task

Create one reviewable RSA asset set per supplied ad group: 15 distinct headlines and 4 descriptions. If evidence cannot support enough useful variation, say so rather than padding with repeated claims. Cover intent, benefit, differentiator, proof, and CTA. Keep assets coherent in different combinations and avoid repeating the same phrase in every asset.

Each headline must fit 30 Google Ads character units; each description 90; optional display paths 15 each. Spaces and punctuation count. Double-width language characters count as two. Compute counts with code where available, then verify them in Google Ads before publication. Do not merely assert “all within limits.”

For each asset show the text, measured count, type, ad-group ID, search intent, and supporting source. Provide a separate normalized `04-rsa-assets.csv` with exactly `campaign_id,ad_group_id,asset_type,text` for the optional validator; keep evidence in a companion table. Types are `headline`, `description`, or `path`.

Do not add dynamic keyword insertion, keyword stuffing, urgency, competitor trademarks, absolute claims, or unsupported superlatives. Do not pin assets by default; explain any required legal wording and ask a reviewer to confirm the final pinning requirements. Display paths do not change the final URL. Check the destination actually supports each promise.

## Deliverables and review

- `04-rsa-draft.md`: one asset/evidence table per ad group plus combination examples and gaps.
- `04-rsa-assets.csv`: normalized assets for character validation, not an upload-ready Ads Editor file.

Review policy compliance, offer accuracy, final URL, combinations, required disclosures, and actual platform acceptance. A passing character check is not ad-policy approval or a performance prediction.

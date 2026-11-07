"""Check the public examples and relative links as part of the release."""

import csv
from decimal import Decimal
import io
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def records(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class KitTests(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        for path in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                target = path.parent / unquote(link.split("#", 1)[0])
                self.assertTrue(target.exists(), f"{path.relative_to(ROOT)}: {link}")

    def test_seven_workflows(self):
        self.assertEqual(len(list((ROOT / "workflows").glob("*.md"))), 7)

    def test_all_csv_shapes(self):
        for path in ROOT.rglob("*.csv"):
            with path.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.reader(stream, strict=True))
            self.assertTrue(rows, str(path))
            self.assertEqual(len(rows[0]), len(set(rows[0])), str(path))
            for number, row in enumerate(rows[1:], 2):
                self.assertEqual(len(row), len(rows[0]), f"{path}:{number}")

    def test_example_audit_numbers(self):
        rows = records("examples/inputs/keywords.csv")
        spend = sum(Decimal(r["cost"]) for r in rows)
        flagged = [r for r in rows if Decimal(r["cost"]) >= 20 and Decimal(r["conversions"]) == 0]
        self.assertEqual(spend, 400)
        self.assertEqual(len(flagged), 2)
        self.assertEqual(sum(Decimal(r["cost"]) for r in flagged), 89)
        self.assertEqual(sum(Decimal(r["conversions"]) for r in rows), Decimal("6.5"))

    def test_campaign_totals_and_budget_reconciliation(self):
        campaign = records("examples/inputs/campaign-performance.csv")
        current = [r for r in campaign if r["period_start"] == "2026-11-01"]
        prior = [r for r in campaign if r["period_start"] == "2026-10-26"]
        self.assertEqual(sum(Decimal(r["cost"]) for r in current), 1800)
        self.assertEqual(sum(Decimal(r["conversions"]) for r in current), 36)
        self.assertEqual(sum(Decimal(r["cost"]) for r in prior), 1500)
        self.assertEqual(sum(Decimal(r["conversions"]) for r in prior), 30)
        budget = records("examples/inputs/budget-plan.csv")
        self.assertEqual({r["campaign_id"]: r["cost"] for r in current},
                         {r["campaign_id"]: r["spend_mtd"] for r in budget})

    def test_rsa_asset_counts(self):
        rows = records("examples/outputs/04-rsa-assets.csv")
        self.assertEqual(sum(r["asset_type"] == "headline" for r in rows), 15)
        self.assertEqual(sum(r["asset_type"] == "description" for r in rows), 4)

    def test_no_fabricated_approvals(self):
        for row in records("examples/outputs/decision-register.csv"):
            self.assertEqual(row["status"], "proposed")
            for field in ("reviewer", "approved_at", "implemented_at", "verification"):
                self.assertEqual(row[field], "")

    def test_generated_examples_match_tools(self):
        cases = [
            (["audit", "examples/inputs/keywords.csv"], "01-audit-check.csv"),
            (["pacing", "examples/inputs/budget-plan.csv", "--as-of", "2026-11-06"], "06-budget-pacing.csv"),
            (["rsa", "examples/outputs/04-rsa-assets.csv"], "04-rsa-check.csv"),
        ]
        for args, name in cases:
            result = subprocess.run([sys.executable, "tools/ads_checks.py", *args],
                                    cwd=ROOT, capture_output=True, text=True, check=True)
            actual = list(csv.reader(io.StringIO(result.stdout)))
            with (ROOT / "examples" / "outputs" / name).open(newline="") as stream:
                expected = list(csv.reader(stream))
            self.assertEqual(actual, expected, name)


if __name__ == "__main__":
    unittest.main()

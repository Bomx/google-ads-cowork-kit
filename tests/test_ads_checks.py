import contextlib
import csv
from datetime import date
from decimal import Decimal
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("ads_checks", Path(__file__).resolve().parents[1] / "tools" / "ads_checks.py")
ads = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ads)


class ChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "input.csv"

    def write(self, mode, rows):
        with self.path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(ads.SCHEMAS[mode])
            writer.writerows(rows)

    def cli(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = ads.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_audit_boundary_fractional_and_zero(self):
        self.write("audit", [
            ["1", "2", "3", "keyword", "20", "2", "10", "0"],
            ["1", "2", "4", "keyword", "19.99", "2", "10", "0"],
            ["1", "2", "5", "keyword", "20", "2", "10", "0.5"],
            ["1", "2", "6", "keyword", "0", "0", "0", "0"],
        ])
        code, out, err = self.cli("audit", str(self.path))
        rows = list(csv.DictReader(io.StringIO(out)))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual([r["status"] for r in rows], ["review", "no_flag", "no_flag", "no_flag"])
        self.assertEqual(rows[0]["cpa"], "null")
        self.assertEqual(rows[2]["cpa"], "40")
        self.assertEqual(rows[3]["source_row"], "5")
        code, out, _ = self.cli("audit", str(self.path), "--threshold", "19")
        self.assertEqual(list(csv.DictReader(io.StringIO(out)))[1]["status"], "review")

    def test_invalid_numbers(self):
        for bad in ("NaN", "sNaN", "inf", "-Infinity", "-1", "oops", "1e999", "1e-999", "1_000", "1,000"):
            with self.subTest(bad=bad):
                self.write("audit", [["1", "2", "3", "keyword", bad, "0", "0", "0"]])
                code, out, err = self.cli("audit", str(self.path))
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertIn(f"{self.path}:row 2:", err)

    def test_audit_keyword_id_scoped_to_campaign_and_ad_group(self):
        self.write("audit", [
            ["1", "2", "3", "keyword", "20", "1", "1", "0"],
            ["1", "4", "3", "keyword", "20", "1", "1", "0"],
            ["5", "2", "3", "keyword", "20", "1", "1", "0"],
        ])
        self.assertEqual(len(ads.read_rows(self.path, "audit")), 3)

    def test_header_only_all_modes(self):
        for mode in ads.SCHEMAS:
            self.write(mode, [])
            with self.assertRaisesRegex(ads.InputError, "no data rows"):
                ads.read_rows(self.path, mode)

    def test_integer_counts(self):
        self.write("audit", [["1", "2", "3", "keyword", "20", "0.5", "1", "0"]])
        self.assertEqual(self.cli("audit", str(self.path))[0], 2)

    def test_missing_ids_totals_and_duplicates(self):
        for row in (
            ["", "name", "100", "20"],
            ["Total:", "name", "100", "20"],
            ["1", "Grand Total", "100", "20"],
            ["1", "name", "100", "-1"],
        ):
            self.write("pacing", [row])
            self.assertEqual(self.cli("pacing", str(self.path), "--as-of", "2024-02-14")[0], 2)
        for mode, row in (
            ("audit", ["1", "2", "3", "keyword", "20", "1", "1", "0"]),
            ("pacing", ["1", "name", "100", "20"]),
            ("rsa", ["1", "2", "headline", "Hello"]),
        ):
            self.write(mode, [row, row])
            with self.assertRaisesRegex(ads.InputError, "row 3: duplicate"):
                ads.read_rows(self.path, mode)

    def test_malformed_headers_rows_quotes(self):
        for content in (
            "",
            "campaign_id,campaign_id,monthly_plan,spend_mtd\n1,hi,100,20\n",
            "campaign_id,campaign,monthly_plan,spend_mtd\n1,hi,100\n",
            "campaign_id,campaign,monthly_plan,spend_mtd\n",
            'campaign_id,campaign,monthly_plan,spend_mtd\n1,"unterminated,100,20',
            "campaign_id,campaign,monthly_plan,spend_mtd\n\n",
        ):
            self.path.write_text(content)
            with self.assertRaises(ads.InputError):
                ads.read_rows(self.path, "pacing")

    def test_pacing_leap_year_and_month_end(self):
        self.write("pacing", [["1", "name", "290", "70"]])
        rows = ads.read_rows(self.path, "pacing")
        _, results, _ = ads.pacing(rows, date(2024, 2, 7))
        row = results[0]
        self.assertEqual(row["days_in_month"], 29)
        self.assertEqual(row["remaining_days"], 22)
        self.assertEqual(row["expected_spend_mtd"], Decimal(70))
        self.assertEqual(row["projected_month_spend"], Decimal(290))
        self.assertEqual(row["allowed_remaining_daily_spend"], Decimal(10))
        for last in (date(2024, 2, 29), date(2023, 2, 28), date(2024, 4, 30), date(2024, 1, 31)):
            _, result, _ = ads.pacing(rows, last)
            self.assertEqual(result[0]["remaining_days"], 0)
            self.assertEqual(result[0]["allowed_remaining_daily_spend"], "null")
            self.assertEqual(result[0]["status"], "month_complete")

    def test_pacing_zero_and_overspend(self):
        self.write("pacing", [["1", "zero", "0", "0"], ["2", "over", "10", "20"]])
        _, results, _ = ads.pacing(ads.read_rows(self.path, "pacing"), date(2024, 1, 1))
        self.assertEqual(results[0]["projected_month_spend"], 0)
        self.assertEqual(results[1]["remaining_plan"], -10)
        self.assertEqual(results[1]["allowed_remaining_daily_spend"], 0)
        self.assertEqual(results[1]["status"], "over_plan")

    def test_pacing_projection_controls_status(self):
        self.write("pacing", [
            ["C100", "ahead of plan", "6000", "1500"],
            ["C200", "exact plan", "6000", "1200"],
            ["C300", "below plan", "6000", "900"],
        ])
        code, out, err = self.cli("pacing", str(self.path), "--as-of", "2026-11-06")
        rows = list(csv.DictReader(io.StringIO(out)))
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(rows[0]["projected_month_spend"], "7500")
        self.assertEqual(rows[0]["status"], "over_plan")
        self.assertEqual(rows[0]["remaining_plan"], "4500")
        self.assertEqual(rows[0]["allowed_remaining_daily_spend"], "187.5")
        self.assertEqual(rows[1]["status"], "within_plan")
        self.assertEqual(rows[2]["status"], "within_plan")
        self.write("pacing", [["C100", "over at month end", "6000", "7500"]])
        _, results, _ = ads.pacing(ads.read_rows(self.path, "pacing"), date(2026, 11, 30))
        self.assertEqual(results[0]["status"], "over_plan")
        self.assertEqual(results[0]["allowed_remaining_daily_spend"], "null")

    def test_invalid_dates(self):
        self.write("pacing", [["1", "name", "100", "20"]])
        for bad in ("2023-02-29", "2024-13-01", "2024-01-00", "20240201", "2024-2-1"):
            self.assertEqual(self.cli("pacing", str(self.path), "--as-of", bad)[0], 2)

    def test_rsa_limits_and_unicode(self):
        self.write("rsa", [
            ["1", "2", "headline", "a" * 30],
            ["1", "2", "headline", "a" * 31],
            ["1", "2", "description", "a" * 90],
            ["1", "2", "description", "a" * 91],
            ["1", "2", "path", "a" * 15],
            ["1", "2", "path", "a" * 16],
            ["1", "2", "headline", "界" * 15],
            ["1", "2", "headline", "Ａ" * 16],
        ])
        code, out, _ = self.cli("rsa", str(self.path))
        rows = list(csv.DictReader(io.StringIO(out)))
        self.assertEqual(code, 1)
        self.assertEqual([r["status"] for r in rows], ["pass", "fail"] * 4)
        self.assertEqual(rows[-1]["character_count"], "32")
        self.assertEqual(ads.character_count("Hello world"), 11)

    def test_rsa_invalid_text_and_type(self):
        for value in ("", " ", "Hello ", " Hello", "Hi\tthere", "Hi\nthere", "Hi\u200bthere"):
            self.write("rsa", [["1", "2", "headline", value]])
            self.assertEqual(self.cli("rsa", str(self.path))[0], 2)
        self.write("rsa", [["1", "2", "unknown", "Hello"]])
        self.assertEqual(self.cli("rsa", str(self.path))[0], 2)

    def test_formula_sanitization_and_output_safety(self):
        for text in ("=SUM(A1)", "+formula", "-formula", "@formula", "\tformula", "\rformula", "\nformula"):
            self.assertTrue(ads.safe_cell(text).startswith("'"))
        self.assertEqual(ads.safe_cell(Decimal("-10")), "-10")
        self.write("rsa", [["1", "2", "headline", "=SUM(A1)"]])
        output = Path(self.temp.name) / "result.csv"
        code, out, _ = self.cli("rsa", str(self.path), "--output", str(output))
        self.assertEqual(code, 0)
        self.assertIn("'=SUM(A1)", out)
        self.assertEqual(output.read_text(), out)
        self.assertEqual(self.cli("rsa", str(self.path), "--output", str(output))[0], 2)
        original = self.path.read_text()
        self.assertEqual(self.cli("rsa", str(self.path), "--output", str(self.path))[0], 2)
        self.assertEqual(self.path.read_text(), original)

    def test_reordered_headers_and_bom(self):
        self.path.write_text("\ufeffspend_mtd,monthly_plan,campaign,campaign_id\n20,100,Hi,1\n", encoding="utf-8")
        self.assertEqual(ads.read_rows(self.path, "pacing")[0][1]["campaign_id"], "1")


if __name__ == "__main__":
    unittest.main()

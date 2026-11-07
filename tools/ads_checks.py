#!/usr/bin/env python3
"""Offline CSV checks. Review signals only; never changes advertising accounts."""
from __future__ import annotations
import argparse
import calendar
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys
import unicodedata

SCHEMAS = {
    "audit": ("campaign_id", "ad_group_id", "keyword_id", "keyword", "cost", "clicks", "impressions", "conversions"),
    "pacing": ("campaign_id", "campaign", "monthly_plan", "spend_mtd"),
    "rsa": ("campaign_id", "ad_group_id", "asset_type", "text"),
}
LIMITS = {"headline": 30, "description": 90, "path": 15}


class InputError(ValueError):
    """A human-readable source validation error."""


def fail(path, row, message):
    raise InputError(f"{path}:row {row}: {message}")


def is_total(value):
    normalized = " ".join(re.sub(r"[_:\-]+", " ", value.strip().lower()).split())
    return normalized in {"total", "totals", "grand total", "subtotal", "summary"} or normalized.startswith("total ")


def number(value, path, row, field, integer=False):
    if len(value) > 100 or not re.fullmatch(r"[+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value):
        fail(path, row, f"{field} must be a finite nonnegative number")
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        fail(path, row, f"{field} must be a finite nonnegative number")
    if not parsed.is_finite() or parsed < 0:
        fail(path, row, f"{field} must be a finite nonnegative number")
    if integer and parsed != parsed.to_integral_value():
        fail(path, row, f"{field} must be a whole number")
    if parsed and (parsed.adjusted() > 18 or parsed.adjusted() < -12):
        fail(path, row, f"{field} is outside supported magnitude (1e-12 through less than 1e19)")
    return parsed


def read_rows(path, mode):
    expected = SCHEMAS[mode]
    seen, result = set(), []
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.reader(stream, strict=True)
            try:
                header = next(reader)
            except StopIteration:
                fail(path, 1, "missing header")
            if len(header) != len(expected) or set(header) != set(expected):
                fail(path, 1, "expected exactly these unique headers: " + ",".join(expected))
            while True:
                source_row = reader.line_num + 1
                try:
                    values = next(reader)
                except StopIteration:
                    break
                if len(values) != len(header):
                    fail(path, source_row, f"expected {len(header)} cells; got {len(values)}")
                record = dict(zip(header, values))
                for field, value in record.items():
                    if not value or not value.strip():
                        fail(path, source_row, f"{field} is empty")
                    if value != value.strip() or any(unicodedata.category(c).startswith("C") for c in value):
                        fail(path, source_row, f"{field} contains surrounding whitespace or control/format characters")
                    if field.endswith("_id") and (any(c.isspace() for c in value) or is_total(value)):
                        fail(path, source_row, f"{field} must be a single non-total ID")
                if is_total(record.get("keyword", record.get("campaign", ""))):
                    fail(path, source_row, "total/summary rows are not supported")
                if mode == "audit":
                    key = tuple(record[field] for field in ("campaign_id", "ad_group_id", "keyword_id"))
                    numeric = ("cost", "clicks", "impressions", "conversions")
                elif mode == "pacing":
                    key, numeric = record["campaign_id"], ("monthly_plan", "spend_mtd")
                else:
                    key, numeric = tuple(record[field] for field in expected), ()
                    if record["asset_type"] not in LIMITS:
                        fail(path, source_row, "asset_type must be headline, description, or path")
                if key in seen:
                    fail(path, source_row, f"duplicate row identifier: {key!r}")
                seen.add(key)
                for field in numeric:
                    record[field] = number(record[field], path, source_row, field, field in ("clicks", "impressions"))
                result.append((source_row, record))
            if not result:
                fail(path, 2, "no data rows")
    except (OSError, UnicodeError) as exc:
        fail(path, 0, str(exc))
    except csv.Error as exc:
        fail(path, reader.line_num, f"malformed CSV: {exc}")
    return result


def audit(rows, threshold):
    fields = ("source_row",) + SCHEMAS["audit"] + ("cpa", "status", "reason")
    output = []
    for source_row, row in rows:
        review = row["cost"] >= threshold and row["conversions"] == 0
        output.append(dict(row, source_row=source_row,
                           cpa=row["cost"] / row["conversions"] if row["conversions"] else "null",
                           status="review" if review else "no_flag",
                           reason="cost_at_or_above_threshold_and_zero_conversions" if review else ""))
    return fields, output, 0


def pacing(rows, as_of):
    days = calendar.monthrange(as_of.year, as_of.month)[1]
    elapsed, remaining = as_of.day, days - as_of.day
    fields = ("source_row",) + SCHEMAS["pacing"] + (
        "as_of", "days_in_month", "elapsed_days", "remaining_days", "expected_spend_mtd",
        "projected_month_spend", "remaining_plan", "allowed_remaining_daily_spend", "status")
    output = []
    for source_row, row in rows:
        plan, spent = row["monthly_plan"], row["spend_mtd"]
        remainder = plan - spent
        projection = spent * days / elapsed
        output.append(dict(row, source_row=source_row, as_of=as_of.isoformat(),
                           days_in_month=days, elapsed_days=elapsed, remaining_days=remaining,
                           expected_spend_mtd=plan * elapsed / days,
                           projected_month_spend=projection,
                           remaining_plan=remainder,
                           allowed_remaining_daily_spend=max(Decimal(0), remainder) / remaining if remaining else "null",
                           status="over_plan" if projection > plan else "month_complete" if remaining == 0 else "within_plan"))
    return fields, output, 0


def character_count(value):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in value)


def rsa(rows):
    fields = ("source_row",) + SCHEMAS["rsa"] + ("character_count", "limit", "status")
    output = []
    for source_row, row in rows:
        count, limit = character_count(row["text"]), LIMITS[row["asset_type"]]
        output.append(dict(row, source_row=source_row, character_count=count, limit=limit,
                           status="pass" if count <= limit else "fail"))
    return fields, output, int(any(row["status"] == "fail" for row in output))


def safe_cell(value):
    if isinstance(value, Decimal):
        return format(value, ".6f").rstrip("0").rstrip(".") or "0"
    if isinstance(value, str) and (value.startswith(("\t", "\r", "\n")) or value.lstrip().startswith(("=", "+", "-", "@"))):
        return "'" + value
    return value


def write_csv(stream, fields, rows):
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: safe_cell(value) for key, value in row.items()} for row in rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in SCHEMAS:
        subparser = commands.add_parser(command)
        subparser.add_argument("input", type=Path, help="normalized UTF-8 CSV")
        subparser.add_argument("--output", type=Path, help="also save CSV; never overwrite existing files")
        if command == "audit":
            subparser.add_argument("--threshold", default="20", help="review threshold in the input's single currency")
        if command == "pacing":
            subparser.add_argument("--as-of", required=True, help="YYYY-MM-DD, inclusive last COMPLETE date in month")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.resolve() == args.input.resolve():
            raise InputError("output must not overwrite input")
        if args.output and args.output.exists():
            raise InputError(f"output already exists: {args.output}")
        threshold = number(args.threshold, "--threshold", 0, "threshold") if args.command == "audit" else None
        as_of = None
        if args.command == "pacing":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.as_of):
                raise InputError("--as-of must be a valid YYYY-MM-DD date")
            try:
                as_of = date.fromisoformat(args.as_of)
            except ValueError:
                raise InputError("--as-of must be a valid YYYY-MM-DD date") from None
        rows = read_rows(args.input, args.command)
        if args.command == "audit":
            fields, result, status = audit(rows, threshold)
        elif args.command == "pacing":
            fields, result, status = pacing(rows, as_of)
        else:
            fields, result, status = rsa(rows)
        if args.output:
            with args.output.open("x", newline="", encoding="utf-8") as stream:
                write_csv(stream, fields, result)
        write_csv(sys.stdout, fields, result)
        return status
    except (InputError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

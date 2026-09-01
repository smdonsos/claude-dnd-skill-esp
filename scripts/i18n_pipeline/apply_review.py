#!/usr/bin/env python3
"""apply_review.py — apply completed rows from docs/i18n/pending_review.csv
back into dnd5e_srd.json.

Row semantics (see build_pending_review.py):
    correction empty        -> still pending, skipped
    correction == "OK"      -> confirmed correct, row removed from the CSV
    correction == anything  -> replaces `name` in the dataset, row removed

Rewrites pending_review.csv afterward keeping only the still-pending rows,
so re-running this script after another editing pass only ever processes
what's left.

Usage:
    python3 apply_review.py                # apply + rewrite the CSV
    python3 apply_review.py --dry-run
"""
import argparse
import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SRD_PATH = REPO_ROOT / "skills" / "dnd" / "data" / "dnd5e_srd.json"
CSV_PATH = REPO_ROOT / "docs" / "i18n" / "pending_review.csv"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not CSV_PATH.exists():
        print(f"{CSV_PATH} not found — run build_pending_review.py first.", file=sys.stderr)
        return 2

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_category: dict[str, dict[str, str]] = {}
    still_pending = []
    confirmed = 0
    corrected = 0
    for row in rows:
        correction = (row.get("correction") or "").strip()
        if not correction:
            still_pending.append(row)
            continue
        if correction.upper() == "OK":
            confirmed += 1
            continue
        by_category.setdefault(row["category"], {})[row["index"]] = correction
        corrected += 1

    if corrected == 0 and confirmed == 0:
        print("Nothing to apply — no rows have a correction filled in yet.")
        return 0

    with open(SRD_PATH, encoding="utf-8") as f:
        data = json.load(f)

    applied = 0
    for cat, fixes in by_category.items():
        for rec in data.get(cat, []):
            if rec["index"] in fixes:
                rec["name"] = fixes[rec["index"]]
                applied += 1

    print(f"{'[dry-run] would apply' if args.dry_run else 'Applied'} "
          f"{applied} name corrections, {confirmed} confirmed as-is, "
          f"{len(still_pending)} still pending.")

    if args.dry_run:
        return 0

    with open(SRD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "category", "index", "source_name_en", "current_name_es",
            "flag_reason", "correction",
        ])
        w.writeheader()
        w.writerows(still_pending)

    print(f"Merged. {len(still_pending)} rows remain in {CSV_PATH}. "
          f"Now run: python -m pytest tests/ -q")
    return 0


if __name__ == "__main__":
    sys.exit(main())

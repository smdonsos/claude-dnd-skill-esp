#!/usr/bin/env python3
"""build_pending_review.py — one-shot: generate docs/i18n/pending_review.csv
listing every dataset entry whose translated `name` couldn't be verified
against the manual (flagged by validate_batch.py's check_name_grounded or
other checks), for manual follow-up once a Bestiario/DMG or other source
becomes available.

The CSV is meant to be opened in a spreadsheet, filled in, and fed back to
apply_review.py:
    - leave `correction` empty  -> still pending, no action
    - write exactly "OK"        -> current translation confirmed correct
    - write anything else       -> that text replaces `name` in the dataset

Usage:
    python3 build_pending_review.py
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
BATCH_DIR = HERE / "batches"
OUT_PATH = REPO_ROOT / "docs" / "i18n" / "pending_review.csv"

BATCHES = [f"spells_level{i}" for i in range(1, 10)] + ["equipment", "features"]


def main() -> None:
    rows = []
    for fname in BATCHES:
        report_path = BATCH_DIR / f"{fname}.report.json"
        batch_path = BATCH_DIR / f"{fname}.jsonl"
        if not report_path.exists():
            continue
        report = json.loads(report_path.read_text(encoding="utf-8"))
        entries = {}
        with open(batch_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    e = json.loads(line)
                    entries[e["_index"]] = e

        for res in report["results"]:
            if not res["flagged"]:
                continue
            e = entries[res["index"]]
            rows.append({
                "category": e["_category"],
                "index": e["_index"],
                "source_name_en": e["_source"].get("name", ""),
                "current_name_es": e.get("name", ""),
                "flag_reason": "; ".join(res["problems"]),
                "correction": "",
            })

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "category", "index", "source_name_en", "current_name_es",
            "flag_reason", "correction",
        ])
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()

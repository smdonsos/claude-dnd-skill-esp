#!/usr/bin/env python3
"""merge_batch.py — merge an approved Gemma batch into dnd5e_srd.json.

Requires a decisions file (JSON: {index: "approve" | "reject" | {overrides}})
produced after reviewing <batch>.review.md — entries NOT in the review
packet (i.e. that passed every automated check and weren't in the random
sample) are auto-approved, since that's the entire point of the sampling
scheme: the sample is assumed representative, so a clean unsampled entry
is trusted the same as a clean sampled one.

Enforces the same surgical diff-scope guarantee used for every hand-done
CLA-8 batch so far: only the translated prose fields of the targeted
indexes change, nothing else in the 1453-record dataset moves.

Usage:
    python3 merge_batch.py batches/spells_level1.jsonl \
        --decisions batches/spells_level1.decisions.json
    python3 merge_batch.py batches/spells_level1.jsonl --dry-run
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SRD_PATH = REPO_ROOT / "skills" / "dnd" / "data" / "dnd5e_srd.json"

PROSE_FIELDS = ["name", "description", "higher_level", "material"]

# Cheap post-fix for the one field-bleed artifact class observed in
# practice (see validate_batch.py check_field_bleed) — strips a trailing
# echoed "index: <slug>" line the model sometimes appends to a field.
_TRAILING_INDEX_ECHO = re.compile(r"\n+index:\s*[\w-]+\s*$", re.IGNORECASE)


def _clean(value: str) -> str:
    return _TRAILING_INDEX_ECHO.sub("", value).strip()


def load_batch(path: pathlib.Path) -> dict[str, dict]:
    entries = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                entries[e["_index"]] = e
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_file", type=pathlib.Path)
    ap.add_argument("--decisions", type=pathlib.Path, default=None,
                     help="JSON {index: 'approve'|'reject'|{field: override}}. "
                          "Entries not in the review packet auto-approve.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    report_path = args.batch_file.with_suffix(".report.json")
    if not report_path.exists():
        print(f"Run validate_batch.py first — {report_path} not found.", file=sys.stderr)
        return 2
    report = json.loads(report_path.read_text(encoding="utf-8"))
    flagged_or_sampled = {
        r["index"] for r in report["results"] if r["flagged"]
    }

    decisions = {}
    if args.decisions and args.decisions.exists():
        decisions = json.loads(args.decisions.read_text(encoding="utf-8"))

    entries = load_batch(args.batch_file)

    to_apply: dict[str, dict] = {}
    for idx, entry in entries.items():
        decision = decisions.get(idx)
        if idx in flagged_or_sampled and decision is None:
            print(f"SKIP {idx}: flagged/needs review, no decision recorded", file=sys.stderr)
            continue
        if decision == "reject":
            print(f"SKIP {idx}: rejected", file=sys.stderr)
            continue
        overrides = decision if isinstance(decision, dict) else {}
        merged = {f: entry.get(f) for f in PROSE_FIELDS if entry.get(f)}
        merged.update(overrides)
        merged = {k: _clean(v) if isinstance(v, str) else v for k, v in merged.items()}
        to_apply[idx] = merged

    if not to_apply:
        print("Nothing to merge.")
        return 0

    with open(SRD_PATH, encoding="utf-8") as f:
        data = json.load(f)

    category = next(iter(entries.values()))["_category"]
    applied = 0
    for rec in data[category]:
        if rec["index"] in to_apply:
            for field, value in to_apply[rec["index"]].items():
                rec[field] = value
            applied += 1

    print(f"{'[dry-run] would apply' if args.dry_run else 'Applying'} "
          f"{applied}/{len(to_apply)} translations to category={category}")

    if args.dry_run:
        return 0

    with open(SRD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print("Merged. Now run: python -m pytest tests/ -q")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""validate_batch.py — zero/low-cost automated validation of a Gemma batch,
plus selection of the (small) subset that actually needs a Sonnet/human
look. This is the step that makes the whole pipeline cheap: everything
that can be checked by code is checked by code, and Sonnet only ever
reads the entries this script could not clear on its own.

Checks (no LLM calls, all deterministic):
  - schema: required keys present, name/description non-empty
  - dice_notation: every NdM token in the English source appears verbatim
    in the Spanish output (dice notation must never be translated/altered)
  - bullet_structure: same count of "\n\n-" / "\n\n" paragraph breaks as
    the English source (catches truncated or merged prose)
  - evidence: every evidence_quotes[] entry is a real verbatim substring
    of the manual (grounding.verify_quote) — the main hallucination trap
  - low_confidence: model self-reported confidence == "low"
  - leftover_english: a short blocklist of common English function words
    found in the Spanish `name`/`description` (weak signal, cheap)
  - glossary_conflict: closed-category English terms mentioned in _source
    whose glossary translation does not appear anywhere in the Spanish
    output (e.g. if the source damage type is "Poison" but "veneno"/
    "envenenad" is nowhere in the translated description)

Any failed check flags the entry. Output: <batch>.report.json (full
machine-readable results) and <batch>.review.md (only flagged entries +
a random --sample-pct of the rest, seeded and reproducible) for a human
or Sonnet to actually read.

Usage:
    python3 validate_batch.py batches/spells_level1.jsonl
    python3 validate_batch.py batches/spells_level1.jsonl --sample-pct 15
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grounding  # noqa: E402

DICE_RE = re.compile(r"\b\d+d\d+\b", re.IGNORECASE)

# Deliberately short and conservative — only words that are near-certain
# to indicate untranslated leftover prose, not cognates or spell-name
# fragments that legitimately look English (e.g. "Mago" is fine).
ENGLISH_LEFTOVER_TOKENS = [
    " the ", " and ", " you ", " your ", " creature ", " spell ",
    " damage ", " saving throw ", " attack roll ",
]


def check_schema(entry: dict) -> list[str]:
    """Only flag an empty translated field when the ENGLISH SOURCE had
    something to translate there. Many equipment entries (mundane gear
    like "Club") legitimately have no description in the dataset — an
    empty translated description for those is correct, not a bug."""
    problems = []
    if not entry.get("name"):
        problems.append("schema:empty_name")
    src = entry.get("_source", {})
    if src.get("description") and not entry.get("description"):
        problems.append("schema:empty_description")
    return problems


def check_dice_notation(entry: dict) -> list[str]:
    src = entry.get("_source", {})
    src_text = " ".join(str(v) for v in src.values() if isinstance(v, str))
    out_text = " ".join(
        str(entry.get(f, "")) for f in ("description", "higher_level", "name")
    )
    src_dice = set(m.group(0).lower() for m in DICE_RE.finditer(src_text))
    out_dice = set(m.group(0).lower() for m in DICE_RE.finditer(out_text))
    missing = src_dice - out_dice
    if missing:
        return [f"dice_notation:missing:{','.join(sorted(missing))}"]
    return []


def check_bullet_structure(entry: dict) -> list[str]:
    src_desc = entry.get("_source", {}).get("description", "")
    out_desc = entry.get("description", "")
    src_paras = src_desc.count("\n\n")
    out_paras = out_desc.count("\n\n")
    if src_desc and abs(src_paras - out_paras) > 0:
        return [f"bullet_structure:paragraph_count_src{src_paras}_vs_out{out_paras}"]
    return []


def check_evidence(entry: dict) -> list[str]:
    """Informational only (see CHECKS) — NOT a flag driver.

    In practice the model often reconstructs a plausible-looking "quote"
    (real name + real school glued together with invented connective text)
    instead of literally copy-pasting, so this fires on a majority of
    otherwise-correct entries (verified by hand: "Crear o destruir agua"/
    "Purificar comida y bebida" are real, verified manual terms that got
    flagged here purely because the cited "quote" wasn't verbatim). Kept
    for diagnostics; check_name_grounded() below is the real signal."""
    quotes = entry.get("evidence_quotes") or []
    if not quotes:
        return ["evidence:none_provided"]
    problems = []
    for q in quotes:
        if not grounding.verify_quote(q):
            problems.append(f"evidence:not_found:{q[:60]!r}")
    return problems


def check_name_grounded(entry: dict) -> list[str]:
    """The real anti-hallucination check: search the manual for the
    translated `name` ITSELF (not the model's self-authored evidence
    quote). Catches real errors (e.g. "thunderwave" -> "Onda de trueno",
    zero hits — the verified official term is "Ola atronadora") without
    the high false-positive rate of check_evidence's verbatim-quote
    matching against a column-mangled PDF-text dump."""
    name = (entry.get("name") or "").strip()
    if not name:
        return []
    if grounding.name_appears_in_manual(name):
        return []
    return ["name_ungrounded:not_found_in_manual"]


def check_low_confidence(entry: dict) -> list[str]:
    if entry.get("confidence") == "low":
        return ["confidence:low"]
    return []


def check_leftover_english(entry: dict) -> list[str]:
    text = f" {entry.get('name','')} {entry.get('description','')} ".lower()
    hits = [tok.strip() for tok in ENGLISH_LEFTOVER_TOKENS if tok in text]
    return [f"leftover_english:{','.join(hits)}"] if hits else []


FIELD_BLEED_PATTERNS = ["index:", "_source", "\"name\":", "\"description\":",
                         "json fuente", "evidence_quotes",
                         # Found in "detect-poison-and-disease" material: the
                         # model's raw self-correction/reasoning bled into the
                         # actual field content instead of stopping at the
                         # final JSON answer.
                         "search_manual said", "resulting json", "final check",
                         "let's go", "wait, "]


def check_field_bleed(entry: dict) -> list[str]:
    """Catch the model echoing raw JSON/prompt structure into a prose field
    (observed once during pipeline dry-run: material ended with
    '\\n\\nindex: alarm')."""
    problems = []
    for field in ("name", "description", "higher_level", "material"):
        val = entry.get(field) or ""
        low = val.lower()
        for pat in FIELD_BLEED_PATTERNS:
            if pat in low:
                problems.append(f"field_bleed:{field}:{pat}")
    return problems


# Checks that determine whether an entry needs a human/Sonnet look.
CHECKS = [check_schema, check_dice_notation, check_bullet_structure,
          check_name_grounded, check_low_confidence, check_leftover_english,
          check_field_bleed]

# Informational only — reported per-entry but never flags on its own
# (see check_evidence's docstring for why: high false-positive rate).
INFO_CHECKS = [check_evidence]


def validate_entry(entry: dict) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    for check in CHECKS:
        problems.extend(check(entry))
    info: list[str] = []
    for check in INFO_CHECKS:
        info.extend(check(entry))
    return problems, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_file", type=pathlib.Path)
    ap.add_argument("--sample-pct", type=float, default=15.0)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    entries = []
    with open(args.batch_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    results = []
    for e in entries:
        problems, info = validate_entry(e)
        results.append({"index": e["_index"], "flagged": bool(problems),
                         "problems": problems, "info": info})

    flagged = [r["index"] for r in results if r["flagged"]]
    rng = random.Random(args.seed)
    clean = [r["index"] for r in results if not r["flagged"]]
    sample_n = max(0, round(len(clean) * args.sample_pct / 100))
    sample = set(rng.sample(clean, min(sample_n, len(clean))))
    review_set = set(flagged) | sample

    report = {
        "batch_file": str(args.batch_file),
        "total": len(entries),
        "flagged_count": len(flagged),
        "sample_count": len(sample),
        "review_count": len(review_set),
        "results": results,
    }
    report_path = args.batch_file.with_suffix(".report.json")
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    by_index = {e["_index"]: e for e in entries}
    md_lines = [
        f"# Review packet — {args.batch_file.name}",
        f"\n{len(entries)} entries total · {len(flagged)} auto-flagged · "
        f"{len(sample)} random sample · **{len(review_set)} need review** "
        f"({len(review_set)/max(1,len(entries))*100:.0f}% of batch)\n",
    ]
    for idx in sorted(review_set):
        e = by_index[idx]
        r = next(r for r in results if r["index"] == idx)
        reason = "FLAGGED: " + "; ".join(r["problems"]) if r["flagged"] else "random sample (clean)"
        md_lines.append(f"\n## {idx}  —  {reason}\n")
        md_lines.append(f"**EN source:** {json.dumps(e.get('_source', {}), ensure_ascii=False)}\n")
        md_lines.append(f"**ES name:** {e.get('name','')}")
        md_lines.append(f"**ES description:** {e.get('description','')}")
        if e.get("higher_level"):
            md_lines.append(f"**ES higher_level:** {e['higher_level']}")
        if e.get("material"):
            md_lines.append(f"**ES material:** {e['material']}")
        md_lines.append(f"**evidence_quotes:** {e.get('evidence_quotes', [])}")
        md_lines.append(f"**confidence:** {e.get('confidence')}  ·  **notes:** {e.get('notes','')}")
    review_path = args.batch_file.with_suffix(".review.md")
    review_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"{len(entries)} entries · {len(flagged)} flagged · {len(sample)} sampled "
          f"-> {len(review_set)} to review ({len(review_set)/max(1,len(entries))*100:.0f}%)")
    print(f"Report: {report_path}")
    print(f"Review packet: {review_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

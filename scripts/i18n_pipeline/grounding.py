"""grounding.py — shared grounding sources for the Gemma translation pipeline.

Loads the two things that keep gemma4:26b from hallucinating terminology:

  1. The local pdftotext -layout dump of the Manual del Jugador 2024 (ESP)
     (gitignored, copyrighted — see docs/i18n/glosario.md "Método de
     verificación"). `search()` is a literal substring search, same
     methodology used by hand for the glossary and the conditions/cantrips
     batches — deliberately NOT fuzzy, so a hit is real evidence.
  2. docs/i18n/glosario.md's term tables, parsed into an English->Spanish
     dict per section, for the `glossary_lookup` tool and for the
     validator's terminology-consistency check.

Both are exposed as tool implementations the Ollama tool-calling loop can
invoke (see gemma_translate.py), and as plain functions the validator
calls directly with zero LLM cost.
"""
from __future__ import annotations

import functools
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MANUAL_PATH = REPO_ROOT / "ManualDelJugador2024_ESP.txt"
GLOSARIO_PATH = REPO_ROOT / "docs" / "i18n" / "glosario.md"


@functools.lru_cache(maxsize=1)
def _manual_text() -> str:
    if not MANUAL_PATH.exists():
        raise FileNotFoundError(
            f"{MANUAL_PATH} not found. Generate it locally with:\n"
            f"  pdftotext -layout ManualDelJugador2024_ESP.pdf ManualDelJugador2024_ESP.txt\n"
            f"(never committed — see docs/i18n/glosario.md)"
        )
    return MANUAL_PATH.read_text(encoding="utf-8", errors="replace")


@functools.lru_cache(maxsize=1)
def _manual_lines() -> list[str]:
    return _manual_text().splitlines()


@functools.lru_cache(maxsize=1)
def _manual_flat() -> str:
    """Whitespace-collapsed manual text (all runs of whitespace -> single
    space). The two-column PDF layout hard-wraps mid-phrase, so a name that
    spans a line break (e.g. "Sentido del\npeligro") never substring-matches
    against _manual_lines()'s per-line search even when it's genuinely
    present. Used by name_appears_in_manual() for a more lenient recheck."""
    return re.sub(r"\s+", " ", _manual_text())


def name_appears_in_manual(name: str) -> bool:
    """Lenient existence check for validate_batch.py's check_name_grounded:
    True if `name` appears verbatim (case-insensitive, whitespace-collapsed)
    anywhere in the manual — catches names split across a PDF line-wrap
    that the per-line search_manual() would miss."""
    name = re.sub(r"\s+", " ", name.strip())
    if not name:
        return False
    return name.lower() in _manual_flat().lower()


def search_manual(query: str, context_lines: int = 1, max_hits: int = 6) -> list[str]:
    """Literal, case-sensitive-off substring search over the manual dump.

    Returns up to `max_hits` snippets, each the matching line plus
    `context_lines` of surrounding lines — enough for a model (or a human)
    to see the school/table column context, same as the manual grep passes
    used for the conditions and level-0 spell batches.
    """
    query = query.strip()
    if not query:
        return []
    lines = _manual_lines()
    q_low = query.lower()
    hits: list[str] = []
    for i, line in enumerate(lines):
        if q_low in line.lower():
            lo = max(0, i - context_lines)
            hi = min(len(lines), i + context_lines + 1)
            snippet = "\n".join(lines[lo:hi])
            hits.append(snippet)
            if len(hits) >= max_hits:
                break
    return hits


def verify_quote(quote: str) -> bool:
    """True if `quote` appears verbatim (whitespace-normalized) in the manual.

    Used by the validator to catch a fabricated `evidence_quote` — the
    cheapest possible hallucination check: exact substring match, no LLM.
    """
    quote = re.sub(r"\s+", " ", quote.strip())
    if not quote:
        return False
    haystack = re.sub(r"\s+", " ", _manual_text())
    return quote.lower() in haystack.lower()


@functools.lru_cache(maxsize=1)
def _glossary_tables() -> dict[str, dict[str, str]]:
    """Parse docs/i18n/glosario.md's `| Inglés | Español |` tables.

    Returns {section_heading: {english_term: spanish_term}}. Section
    headings are the `## ...` lines immediately above each table.
    """
    text = GLOSARIO_PATH.read_text(encoding="utf-8")
    tables: dict[str, dict[str, str]] = {}
    section = None
    for line in text.splitlines():
        h = re.match(r"^##\s+(.+)$", line)
        if h:
            section = h.group(1).strip()
            continue
        row = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if row and section and row.group(1) not in ("Inglés", "---"):
            en, es = row.group(1), row.group(2)
            if set(en) == {"-"}:
                continue
            tables.setdefault(section, {})[en] = es
    return tables


def glossary_lookup(term: str) -> str | None:
    """Case-insensitive lookup of `term` across all glossary sections.

    Returns the canonical Spanish translation if `term` is a closed-category
    word already decided in Fase 0 (ability scores, skills, conditions,
    damage types, schools, sizes, alignments, common mechanic vocabulary),
    else None — meaning it's open vocabulary the model must translate/verify
    itself (e.g. a spell or monster name, which Fase 3 resolves entry by
    entry, not pre-built in the glossary).
    """
    term_low = term.strip().lower()
    for table in _glossary_tables().values():
        for en, es in table.items():
            if en.strip().lower() == term_low:
                return es
    return None


def all_glossary_terms() -> dict[str, str]:
    """Flat English->Spanish dict across every glossary section (for prompts)."""
    out: dict[str, str] = {}
    for table in _glossary_tables().values():
        out.update(table)
    return out


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_manual",
            "description": (
                "Search the official Spanish D&D Player's Handbook 2024 text "
                "for a literal substring (Spanish text). Use this to verify a "
                "candidate Spanish name/term before committing to it — do not "
                "guess a translation without checking. Returns matching lines "
                "with context, or an empty list if nothing matched."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Spanish text to search for, e.g. a candidate spell name.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "glossary_lookup",
            "description": (
                "Look up the canonical Spanish translation of a closed-category "
                "D&D term (ability scores, skills, conditions, damage types, "
                "magic schools, sizes, alignments, common mechanic vocabulary "
                "like Hit Points/Saving Throw/Advantage). Returns null if the "
                "term isn't in the glossary (e.g. it's a specific spell/monster "
                "name you must verify via search_manual instead)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "term": {"type": "string", "description": "English term, e.g. 'Poisoned' or 'Evocation'."}
                },
                "required": ["term"],
            },
        },
    },
]


def call_tool(name: str, arguments: dict) -> object:
    if name == "search_manual":
        return search_manual(arguments.get("query", ""))
    if name == "glossary_lookup":
        return glossary_lookup(arguments.get("term", ""))
    raise ValueError(f"unknown tool: {name}")

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is **`claude-dnd-skill-esp`**, a fork of [neuralinitiative/claude-dnd-skill](https://github.com/neuralinitiative/claude-dnd-skill) whose entire purpose is **translating the project to Spanish** — the skill's DM instructions, command procedures, UI strings, templates, and docs. It is not a feature fork: functional changes should generally still flow from upstream, and work here should stay translation-scoped unless the user explicitly asks for something else.

The underlying project is a Claude Code **plugin** (`dm`, providing the `dnd` skill) that turns Claude into a persistent D&D 5e Dungeon Master. The actual DM behavior — narration rules, the twelve DM standards, command procedures, script call conventions — lives in the skill's own markdown files, not in Python. This repo's Python code is the *mechanical* layer the skill leans on: dice, combat math, XP, character sheets, campaign data plumbing, and an optional Flask-based "cinematic display" companion.

Read `skills/dnd/SKILL.md` before touching anything DM-behavior-related — it is the actual system prompt content and is authoritative over any assumption you'd otherwise make about tone, roll handling, or session flow. `SKILL-scripts.md` and `SKILL-commands.md` are the other two reference files loaded at session start (script syntax and `/dm:dnd` command procedures respectively).

### Translation status and conventions

Translation is tracked as an 8-phase project in Linear (team `Claude-dnd-skill-esp`, project "Traducción al español", issues CLA-5 through CLA-13). As of Fase 0 (CLA-5): the terminology glossary and this policy are in place; `skills/dnd/*.md`, templates, the dataset, and display UI strings are still untranslated (upstream English content) pending later phases.

**Scope decided for this fork:** full translation — UI, docs, and DM narration in Spanish by default, **including game terminology** (spell/monster/condition names use official Devir/WotC Spanish terms, not literal translations). Register: **español neutro, tuteo** — no "vosotros", no single-country idioms.

**Terminology glossary:** `docs/i18n/glosario.md` is the canonical source for closed-category terms (classes, ability scores, skills, conditions, damage types, magic schools, sizes, alignments, common mechanic/UI vocabulary), verified against the official *Manual del Jugador 2024 (ESP)*. That PDF itself is never committed (`.gitignore` excludes `/*.pdf` — copyrighted commercial content); only the extracted terminology is redistributable. Spell/monster/item names in `data/dnd5e_srd.json` are resolved entry-by-entry during Fase 3, using the same verify-against-source method, not pre-built in the glossary.

- **Translate:** prose the player/DM sees — `SKILL.md` / `SKILL-commands.md` / `SKILL-scripts.md` narrative instructions and examples, `templates/*.md` (character sheet, state, world, npcs, session-log), `display/templates/` UI strings, `README.md`, and (Fase 3) `data/dnd5e_srd.json`'s `name`/`description`/prose fields.
- **Do not translate:** Python identifiers, CLI flag names (`--stat-hp`, `--dice-request`, etc.), file/field keys that scripts parse (`**Ruleset:**`, `## Live State Flags`, `## Session Flags`, YAML/JSON keys), command names (`/dm:dnd load`), the `/dm:dnd` command surface itself (`name: dnd` in SKILL.md, `name: "dm"` in plugin.json), and anything `paths.py`/other scripts match on by exact string. These are load-bearing — scripts and `SKILL*.md` procedures key off the literal English text, so silently translating a heading or flag name breaks parsing across the whole system. If a user-facing label must change, update every script and doc that greps/matches on it in the same change. In `dnd5e_srd.json`, the `index` field (stable English slug) never changes — only `name`/prose fields translate.
- **Known code-level dependencies on narration language** (from the architecture audit, `docs/architecture-review.md`): the 17-scene keyword detector in `dnd-display-app.py` (`SCENES`) and the deterministic relationship-graph extractor (`graph_extract_deterministic.py` + `data/graph/verb_table_seed.yaml`) both pattern-match English words against narration text. Scene detection gets a Spanish keyword set added alongside the English one (Fase 5, CLA-10). The graph verb-table is explicitly **out of scope** for this translation pass (deferred, Linear CLA-13/Fase 8) — deterministic extraction degrades for Spanish session logs until that's tackled as its own effort; manual `add-node`/`add-edge` still work.
- `display/audio.py` already ships a Spanish SFX trigger pack (`_SFX_TRIGGERS["es"]`) — inactive by default (`_SFX_LANGUAGES = ["en"]`). Fase 6 (CLA-11) flips the campaign template default to `sfx_languages: es`; no code change needed there.
- Keep `CHANGELOG.md`, `VERSION`, and plugin metadata (`.claude-plugin/*.json`) in sync with upstream semantics — translation is a presentation concern, not a version-bump trigger, unless the user says otherwise. `LICENSE` stays verbatim (AGPL-3.0 canonical text) and `CHANGELOG.md`/`docs/research/graph/` are out of scope for translation (historical/internal, not user-facing).
- When in doubt whether a string is a display label (translate) or a machine-parsed key (don't), grep for the literal string across `scripts/` and `display/` before touching it.

## Commands

```bash
# Run the full test suite
python -m pytest tests/ -q

# Run a single test file / test
python -m pytest tests/test_utf8io.py -q
python -m pytest tests/test_utf8io.py::test_gbk_roundtrip -q

# Test dependencies (not in requirements.txt — see .github/workflows/tests.yml)
pip install pytest flask flask-cors pyyaml

# Display companion runtime deps (separate from test deps)
pip3 install flask flask-cors numpy cryptography
pip3 install pymupdf   # optional: PDF campaign import with column-aware extraction

# Version bump helper (updates VERSION, plugin.json, marketplace.json together)
python scripts/bump_version.py <new-version>
```

CI (`.github/workflows/tests.yml`) runs the suite on ubuntu/macos/windows × py3.10/3.13, plus a dedicated job that forces a non-UTF-8 (`LC_ALL=C`, `PYTHONUTF8=0`, `PYTHONCOERCECLOCALE=0`) locale on Linux — this repo has a real history of encoding bugs (GBK-written legacy files, Windows codepage stdout) and that job exists specifically to catch reads/writes that assume a UTF-8-friendly environment. When touching any file I/O, run that mental check even if you can't run the Windows/locale matrix locally: use `scripts/utf8io.py`'s `read_text()` for anything that might touch a legacy campaign file, and never rely on the platform default encoding for stdout/stdin.

There is no lint/typecheck command configured — match the style of the surrounding file.

## Architecture

### Two roots, never confused

- **CODE root** (`skill_root()` in `skills/dnd/scripts/paths.py`) — this repo's `skills/dnd/` directory: `scripts/`, `data/` (bundled SRD JSON), `templates/`, `display/`. Resolved via `CLAUDE_SKILL_DIR` when set (plugin/installed contexts) or by walking up from `paths.py`'s own location otherwise (dev clone). Never hardcode a path into this tree — always resolve through `paths.py`.
- **DATA root** (`DND_CAMPAIGN_ROOT`, default `~/.claude/dnd/`) — user's actual campaigns and characters (`campaigns/<name>/{state,world,npcs,session-log}.md`, `characters/<name>.md`). Lives outside the plugin so it survives updates/uninstalls. All scripts import path helpers from `scripts/paths.py` rather than constructing these paths themselves.

Every script in `skills/dnd/scripts/` and `skills/dnd/display/` is invoked as a subprocess from within a live Claude Code DM session, driven by instructions in `SKILL.md`/`SKILL-commands.md`/`SKILL-scripts.md` — not as a standalone application. When changing a script's CLI surface (flags, output format), check whether `SKILL*.md` documents that exact invocation and update it in lockstep, or the DM will silently start calling it wrong.

### Script-first / model-routing split

`SKILL.md` enforces a "script-first rule": any calculation with a script (dice, HP, XP, initiative, conditions, dates, SRD lookups) must go through Python, never be computed by the LLM in-context. This is why `scripts/` is deep and mechanical — `dice.py`, `combat.py`, `xp.py`, `ability-scores.py`, `character.py`, `tracker.py`, `calendar.py`, `lookup.py`. Keep new mechanics here rather than pushing them into prose instructions.

### Display companion (`skills/dnd/display/`)

An optional Flask + Server-Sent-Events app (`dnd-display-app.py`) that turns narration/dice/stats into a live browser page (TV/tablet/phone). Flow: DM session → `send.py` / `push_stats.py` (HTTP POST) → Flask app broadcasts via SSE → browser renders typewriter narration + party sidebar. Player phones POST actions back; `check_input.py` / `autorun_wait.py` let the DM session poll for them without a human pressing Enter (autorun/"taxi mode"). Security-relevant surface: device pairing/approval and input sanitization happen in `dnd-display-app.py` before anything reaches the autorun queue — the DM-side Bash loop only reads pre-sanitized files, it doesn't execute untrusted input.

### Campaign import & the relationship graph

`import_campaign.py` + `graph_extract_deterministic.py` turn a pre-written module (PDF/md/docx/txt) into structured campaign files (acts, chapters, key beats, NPCs, quest hooks) plus a lazily-loaded source corpus (one file per chapter, loaded on demand — never the whole book at once). `campaign_graph.py` maintains a typed-edge relationship graph alongside the markdown files, with verbatim source-anchors on every edge, used to answer "who knows whom" without re-reading full NPC files. Background/rationale: `docs/research/graph/`.

### Encoding discipline

This codebase has had real data-loss bugs from encoding mismatches (see git log around "UTF-8 text IO across the tree"). The load-bearing pattern is `scripts/utf8io.py`: try strict UTF-8, fall back to a *verified round-trip* GBK decode (legacy files from an old Windows-codepage-writing version of the plugin), otherwise raise loudly rather than silently mangling content with `errors="replace"`. `paths.py` also force-reconfigures `stdout`/`stderr` to UTF-8 on import for the same reason (Windows CJK codepage default). Follow this pattern for any new file I/O rather than using bare `open()`/`.read_text()`.

### Ruleset duality (2014 vs 2024 SRD)

Campaigns declare `**Ruleset:** 2014` or `2024` in `state.md`; `migrate_ruleset.py` handles the one-time backward-compat migration for legacy campaigns with no such field. Scripts and narration must respect whichever ruleset is active per-campaign (see the mechanic-differences table in `SKILL.md`) rather than assuming one globally.

## Contributing conventions (from CONTRIBUTING.md)

- Licensed AGPL-3.0-or-later; contributions are licensed the same way.
- For substantive changes, open an issue first to align on scope before writing code.
- PR descriptions should explain *why*, not just *what*.

#!/usr/bin/env python3
"""gemma_translate.py — generate Spanish translations for a batch of
dnd5e_srd.json entries using a local gemma4:26b (via Ollama), grounded on
the official manual text + Fase 0 glossary through real tool calls.

This ONLY generates candidate translations to a JSONL file under
scripts/i18n_pipeline/batches/ — it never touches dnd5e_srd.json directly.
Run validate_batch.py next, then merge_batch.py after human/Sonnet review.

Usage:
    python3 gemma_translate.py --category spells --level 1
    python3 gemma_translate.py --category spells --level 1 --resume
    python3 gemma_translate.py --category equipment
    python3 gemma_translate.py --category features

Requires Ollama running locally with the model pulled:
    ollama pull gemma4:26b
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SRD_PATH = REPO_ROOT / "skills" / "dnd" / "data" / "dnd5e_srd.json"
BATCH_DIR = HERE / "batches"

sys.path.insert(0, str(HERE))
import grounding  # noqa: E402

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:26b"

# Fields we ask Gemma to translate per category. `index`, `school`,
# `casting_time`, `range`, `duration`, `components`, `category`, `rarity`,
# `damage_type`, `size`, `alignment` etc. are enum-ish fields explicitly
# out of scope for this pass (CLA-8's separate enum review) — the schema
# below only ever asks for prose fields, so there is no code path that
# could let Gemma touch them.
PROSE_FIELDS = {
    "spells": ["name", "description", "higher_level", "material"],
    "equipment": ["name", "description"],
    "features": ["name", "description"],
}

# Few-shot anchor: the human/Sonnet-verified level-0 spell translations,
# used verbatim as in-context examples so Gemma's register (voseo/tuteo)
# and terminology style match what's already merged, instead of drifting.
FEWSHOT_SPELL_INDEXES = ["fire-bolt", "poison-spray", "mage-hand"]

SYSTEM_PROMPT = """Eres un traductor experto de D&D 5e (inglés -> español) para una \
mesa hispanohablante. Traduces terminología oficial de D&D en español \
(estilo Devir/WotC), registro español neutro con tuteo \
("tú", "puedes", "tienes", "lanzas") — NUNCA "vosotros" ni voseo \
argentino ("vos", "podés", "tenés").

Reglas estrictas:
1. NUNCA inventes un nombre propio de conjuro/objeto/monstruo sin \
verificarlo primero. Llama a search_manual con candidatos plausibles \
ANTES de responder. Si search_manual no encuentra nada tras 2-3 intentos \
razonables, traduce de la forma más literal y consistente con el glosario, \
y marca confidence="low".
2. Para vocabulario de mecánica cerrado (tipos de daño, características, \
condiciones/estados, escuelas de magia, ventaja/desventaja, tirada de \
salvación, etc.) llama a glossary_lookup en vez de traducir por tu cuenta \
— ya está decidido y verificado.
3. La prosa que traduces es el texto MECÁNICO de la SRD 2014 en inglés que \
te paso — tradúcelo fielmente, NO copies reglas del manual 2024 aunque \
las encuentres (pueden diferir mecánicamente entre ediciones).
4. Convierte distancias imperiales a métricas usando la convención oficial \
que confirmes en el manual (5 ft = 1,5 m, 10 ft = 3 m, 60 ft = 18 m, etc.) \
— busca en el manual si no estás seguro de una conversión.
5. Preserva intacta toda la notación de dados (1d6, 2d8, etc.) y la \
estructura de párrafos/viñetas del original.
6. En evidence_quotes, cita TEXTUALMENTE (copy-paste exacto, sin \
parafrasear) el fragmento del manual que encontraste con search_manual que \
respalda el nombre elegido. Si no hay evidencia directa, deja una lista \
vacía y baja tu confidence.
7. Responde SOLO con el JSON pedido, nada de texto fuera del JSON."""


def build_schema(fields: list[str]) -> dict:
    props = {f: {"type": "string"} for f in fields if f != "name"}
    props["name"] = {"type": "string"}
    props["evidence_quotes"] = {"type": "array", "items": {"type": "string"}}
    props["confidence"] = {"type": "string", "enum": ["high", "low"]}
    props["notes"] = {"type": "string"}
    required = ["name", "description", "evidence_quotes", "confidence", "notes"]
    return {
        "type": "object",
        "properties": props,
        "required": [r for r in required if r in props] + ["name"],
    }


def _ollama_chat(messages: list[dict], tools: list[dict] | None = None,
                  fmt: dict | None = None, timeout: int = 180) -> dict:
    # think=False: measured ~15x speedup (90-110s -> ~6s per entry) with no
    # loss of real tool-calling behavior — confirmed via a live test where
    # the model still searched the manual twice ("Web" then "telaraña")
    # before answering, converging on a verified name. What's lost is the
    # verbose reasoning trace, not the grounding itself — evidence_quotes
    # (verified separately by validate_batch.py) is what we actually rely
    # on for auditability, not the thinking text.
    payload = {"model": MODEL, "messages": messages, "stream": False, "think": False}
    if tools:
        payload["tools"] = tools
    if fmt:
        payload["format"] = fmt
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _fewshot_block(category: str) -> str:
    if category != "spells":
        return ""
    with open(SRD_PATH, encoding="utf-8") as f:
        data = json.load(f)
    lines = ["EJEMPLOS YA VERIFICADOS Y MERGEADOS (sigue este estilo exacto):"]
    for s in data["spells"]:
        if s["index"] in FEWSHOT_SPELL_INDEXES:
            lines.append(f"- {s['index']} -> name: \"{s['name']}\" | description: \"{s['description'][:200]}...\"")
    return "\n".join(lines)


def translate_entry(rec: dict, category: str, fewshot: str) -> dict:
    fields = PROSE_FIELDS[category]
    present_fields = [f for f in fields if rec.get(f)]
    src = {k: rec[k] for k in present_fields}
    src["index"] = rec["index"]

    user_msg = (
        f"{fewshot}\n\n" if fewshot else ""
    ) + (
        f"Traduce esta entrada de {category} (índice '{rec['index']}', "
        f"NUNCA traduzcas el índice). Campos en inglés a traducir: "
        f"{', '.join(present_fields)}.\n\n"
        f"JSON fuente:\n{json.dumps(src, ensure_ascii=False, indent=2)}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    schema = build_schema(present_fields)
    max_tool_rounds = 6
    for _ in range(max_tool_rounds):
        resp = _ollama_chat(messages, tools=grounding.TOOL_SCHEMAS)
        msg = resp["message"]
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if not calls:
            break
        for call in calls:
            fn = call["function"]
            try:
                result = grounding.call_tool(fn["name"], fn.get("arguments", {}))
            except Exception as e:  # noqa: BLE001 — feed the error back to the model
                result = f"ERROR: {e}"
            messages.append({
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False),
            })
    else:
        # Ran out of tool rounds — ask once more, forcing a final answer.
        messages.append({"role": "user", "content": "Dejá de buscar y respondé ahora con el JSON final."})

    parsed = None
    last_error = None
    for attempt in range(3):
        raw = None
        try:
            final = _ollama_chat(messages, fmt=schema)
            raw = final["message"]["content"]
            parsed = json.loads(raw)
            break
        except (json.JSONDecodeError, KeyError, urllib.error.URLError) as e:
            last_error = f"{e} | raw={raw!r}"
            if attempt < 2:
                messages.append({
                    "role": "user",
                    "content": "Tu última respuesta no fue JSON válido. Respondé de "
                               "nuevo, SOLO el objeto JSON pedido, sin texto extra.",
                })
    if parsed is None:
        parsed = {"name": "", "description": "", "evidence_quotes": [],
                  "confidence": "low", "notes": f"PARSE_ERROR after 3 attempts: {last_error}"}
    parsed["_index"] = rec["index"]
    parsed["_category"] = category
    parsed["_source"] = src
    return parsed


def load_targets(category: str, level: int | None) -> list[dict]:
    with open(SRD_PATH, encoding="utf-8") as f:
        data = json.load(f)
    recs = data[category]
    if level is not None:
        recs = [r for r in recs if r.get("level") == level]
    return recs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True, choices=list(PROSE_FIELDS))
    ap.add_argument("--level", type=int, default=None, help="spells only: filter by level (0-9)")
    ap.add_argument("--limit", type=int, default=None, help="cap number of entries (testing)")
    ap.add_argument("--resume", action="store_true", help="skip indexes already in the output file")
    args = ap.parse_args()

    slug = f"{args.category}" + (f"_level{args.level}" if args.level is not None else "")
    out_path = BATCH_DIR / f"{slug}.jsonl"
    BATCH_DIR.mkdir(exist_ok=True)

    done = set()
    if args.resume and out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["_index"])
                except (json.JSONDecodeError, KeyError):
                    pass

    targets = load_targets(args.category, args.level)
    targets = [t for t in targets if t["index"] not in done]
    if args.limit:
        targets = targets[: args.limit]

    print(f"Translating {len(targets)} entries -> {out_path}")
    fewshot = _fewshot_block(args.category)

    with open(out_path, "a", encoding="utf-8") as out:
        for i, rec in enumerate(targets, 1):
            t0 = time.time()
            try:
                result = translate_entry(rec, args.category, fewshot)
            except (urllib.error.URLError, TimeoutError) as e:
                print(f"  [{i}/{len(targets)}] {rec['index']}: NETWORK ERROR: {e}", file=sys.stderr)
                continue
            out.write(json.dumps(result, ensure_ascii=False) + "\n")
            out.flush()
            dt = time.time() - t0
            print(f"  [{i}/{len(targets)}] {rec['index']} -> {result.get('name','?')!r} "
                  f"(confidence={result.get('confidence')}, {dt:.1f}s)")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

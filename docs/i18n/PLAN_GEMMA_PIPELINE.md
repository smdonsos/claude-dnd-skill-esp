# Plan — traducción del dataset SRD (CLA-8) delegada a gemma4:26b local

## Por qué

CLA-8 requiere traducir ~1453 registros del SRD (319 hechizos, 237 objetos,
362 objetos mágicos, 334 monstruos, 186 rasgos) verificando cada término
contra el Manual del Jugador 2024 (ESP) — el mismo método usado a mano para
el glosario (Fase 0), `conditions` (15/15) y los 24 trucos de nivel 0. A
mano, ese método cuesta ~10-15 minutos y varios miles de tokens de Sonnet
por cada entrada compleja. Para ~1200 entradas restantes eso es
insostenible en tokens de un modelo caro.

Este plan delega la generación a un modelo local (`gemma4:26b` vía Ollama,
gratis, ya instalado) y reserva Sonnet para lo que un modelo más chico no
puede garantizar por sí solo: juicio de calidad sobre una muestra acotada.

## Qué hace cada pieza (`scripts/i18n_pipeline/`)

```
grounding.py        # carga manual + glosario; funciones search_manual(),
                     # glossary_lookup(), verify_quote() — usadas TANTO como
                     # tools que Gemma llama en vivo COMO por el validador
                     # (sin costo de LLM) para chequear evidencia después.
gemma_translate.py   # genera candidatos -> batches/<categoria>.jsonl
                     # (NUNCA toca dnd5e_srd.json directamente)
validate_batch.py    # checks automáticos + arma el paquete de revisión
                     # (<batch>.report.json, <batch>.review.md)
merge_batch.py       # aplica al dataset real, con el mismo guardrail de
                      # diff quirúrgico usado en cada PR anterior de CLA-8
```

## Por qué gemma4:26b y no otro enfoque

Verificado en este repo: `ollama show gemma4:26b` reporta
`context length 262144`, capacidades `tools`, `thinking`, `vision`. Eso
habilita tres cosas concretas que un modelo sin tool-calling no tendría:

1. **`tools` (function calling)** — en vez de dejar que el modelo "sepa"
   el nombre en español de memoria (con el riesgo de inventar, como pasó
   con el error de Grappled/Restrained del glosario original), el system
   prompt lo OBLIGA a llamar `search_manual` con candidatos antes de
   responder, y `glossary_lookup` para vocabulario cerrado ya decidido.
   Confirmado en un smoke test real (ver más abajo): ante "Magic Missile"
   el modelo razonó en su traza de `thinking` que no sabía el término
   oficial y llamó a `search_manual("misil mágico")` antes de contestar,
   en vez de adivinar.
2. **JSON-schema forzado (`format`)** — cada respuesta final es JSON
   válido con una forma fija (`name`, `description`, `evidence_quotes`,
   `confidence`, `notes`), parseable sin ambigüedad. Esto es lo que hace
   viable el paso de validación automática.
3. **Contexto de 262K tokens** — alcanza para incluir ejemplos few-shot
   (las traducciones ya mergeadas de Fase 3) y varias rondas de
   tool-calling sin truncar la conversación, algo que un modelo de
   contexto chico no soportaría de forma confiable a este volumen.

`evidence_quotes` es la pieza clave del diseño: le exijo al modelo que
cite TEXTUALMENTE el fragmento del manual que encontró. Verificar que esa
cita existe de verdad en el manual es una comparación de substring —
gratis, determinística, cero tokens — y es la forma más barata posible de
detectar una alucinación: si el modelo inventa una "evidencia" que no
existe en el texto real, el chequeo lo detecta sin que Sonnet tenga que
leer nada.

## El embudo de validación (por qué el costo de Sonnet queda acotado)

```
                    ┌─────────────────────┐
                    │  gemma_translate.py  │  (gratis, corre local)
                    └──────────┬───────────┘
                               │  batches/<cat>.jsonl
                               ▼
                    ┌─────────────────────┐
                    │  validate_batch.py   │  (gratis, determinístico)
                    │  - schema            │
                    │  - dice notation     │
                    │  - estructura        │
                    │  - evidence_quotes   │◄── verify_quote() contra
                    │    realmente existen │    el manual real
                    │  - confidence=low    │
                    │  - inglés residual   │
                    │  - fuga de JSON en   │
                    │    campos de prosa   │
                    └──────────┬───────────┘
                               │
              flagged ∪ muestra aleatoria 15%
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Sonnet 5 (yo)      │  ← ÚNICO paso con costo real
                    │  lee review.md       │     de tokens de este plan
                    │  aprueba/corrige     │
                    └──────────┬───────────┘
                               │  decisions.json
                               ▼
                    ┌─────────────────────┐
                    │   merge_batch.py     │  (gratis, con guardrail de
                    │                      │   diff quirúrgico + pytest)
                    └─────────────────────┘
```

Con esto, si el pipeline entrega un batch donde el 90% pasa todos los
checks automáticos, Sonnet solo necesita leer ~15-20% del batch en vez
del 100% — y ese 15-20% incluye garantizado el 100% de lo genuinamente
sospechoso (baja confianza, evidencia falsa, estructura rota), no solo
una muestra ciega. Un error sistemático como el de Grappled/Restrained
(que no dispara ningún check automático porque el texto está "bien
formado", solo semánticamente cruzado) es el caso que la muestra
aleatoria del 15% está para atrapar estadísticamente — con 300 hechizos,
un 15% son ~45 entradas revisadas, suficiente para notar un patrón
sistemático si existe.

## Cómo correrlo (ejemplo, un nivel de hechizos)

```bash
# 1. Generar (corre en background, puede tardar — ver nota de tiempos)
python3 scripts/i18n_pipeline/gemma_translate.py --category spells --level 1

# 2. Validar + armar paquete de revisión
python3 scripts/i18n_pipeline/validate_batch.py \
    scripts/i18n_pipeline/batches/spells_level1.jsonl

# 3. Sonnet (o vos) lee spells_level1.review.md, escribe decisions.json:
#    {"alarm": "approve", "animal-friendship": {"name": "Amistad animal"}, ...}

# 4. Mergear al dataset real
python3 scripts/i18n_pipeline/merge_batch.py \
    scripts/i18n_pipeline/batches/spells_level1.jsonl \
    --decisions scripts/i18n_pipeline/batches/spells_level1.decisions.json

# 5. Verificación final (igual que cada PR anterior de CLA-8)
python -m pytest tests/ -q
```

## Tiempos observados (smoke test real, este repo, 31/08/2026)

Con el modelo ya cargado en memoria, cada entrada de hechizo tarda
~90-110 segundos (varias rondas de tool-calling + respuesta final con
schema). Para los ~718 registros de spells/equipment/features que este
plan cubre ahora, eso son entre 18 y 22 horas de cómputo local
**sin costo de tokens** — pensado para dejarlo corriendo desatendido
(`--resume` permite cortar y continuar), no para esperarlo en vivo.

## Alcance de esta primera etapa

Cubre `spells` (295 restantes, niveles 1-9), `equipment` (237), `features`
(186) — las tres categorías bien verificables contra el Manual del
Jugador 2024 que tenés. **`monsters` (334) y `magic_items` (362) quedan
explícitamente fuera de este pipeline por ahora**: el manual no trae
bloques de estadísticas de monstruos completos (eso es el Bestiario/
Manual de Monstruos, que no tenés) y solo menciona objetos mágicos de
forma parcial — meterlos en este flujo significaría que `search_manual`
casi siempre vuelve vacío y el modelo termina generando con
`confidence=low` en casi el 100% de los casos, lo que en la práctica
anula el ahorro (Sonnet terminaría revisando casi todo igual). Cuando
consigas esas fuentes, el mismo pipeline se reusa sin cambios de código
— solo se necesita apuntar `grounding.py` a los textos nuevos.

## Campos que este pipeline NUNCA toca

`index`, `school`, `casting_time`, `range`, `duration`, `components`,
`category`, `rarity`, tipo de daño, tamaño, alineamiento — son los
campos "enum" que CLA-8 marca para una revisión aparte (¿algo en
`character.py`/`combat.py` hace matching programático sobre el valor
literal?). `gemma_translate.py` ni siquiera se los pasa al modelo como
campos a traducir — no existe camino de código por el que puedan
cambiar en este flujo.

## Riesgos conocidos y cómo el plan los cubre

| Riesgo | Mitigación |
|---|---|
| El modelo inventa un nombre sin verificar | System prompt lo obliga a `search_manual`/`glossary_lookup`; `evidence_quotes` se verifica por substring real |
| Evidencia citada pero falsa (alucinada) | `verify_quote()` — comparación literal contra el manual, cero costo |
| Traduce con reglas 2024 en vez de la mecánica 2014 del dataset | Instrucción explícita repetida en el system prompt (regla 3); ejemplos few-shot ya verificados anclan el estilo |
| Notación de dados alterada | `check_dice_notation` — todo NdM del inglés debe aparecer igual en el español |
| Fuga de estructura JSON en el texto (visto en el dry-run: `"...\n\nindex: alarm"`) | `check_field_bleed` + limpieza automática en `merge_batch.py` |
| Error sistemático "silencioso" (bien formado pero mal traducido) | Muestra aleatoria del 15%, no solo lo auto-flagueado |
| JSON malformado en la respuesta final | Reintento automático (hasta 3 intentos) en `gemma_translate.py` |
| Costo de Sonnet se dispara igual | El único paso con costo de tokens es leer `review.md` (15-25% del batch) — nunca la traducción completa |

## Estado

- [x] Pipeline implementado y probado end-to-end contra Ollama real (2
      hechizos de nivel 1: `alarm`, `animal-friendship`)
- [x] Confirmado tool-calling real (`search_manual`) con traza de
      `thinking` visible
- [x] Confirmado JSON-schema forzado + reintento ante parseo fallido
- [x] Corrida completa mergeada a `dnd5e_srd.json`: `spells` 319/319 (24
      nivel 0 + 295 niveles 1-9), `equipment` 235/237, `features` 186/186
      (716/718 total). 55 nombres sin traducir y 2 fugas de campo detectadas
      y corregidas en la misma pasada; ~315 entradas quedan documentadas en
      `local-review/pending_review.json` (local, no versionado) para
      verificación futura contra una fuente adicional
- [ ] `monsters`/`magic_items` — bloqueado hasta conseguir Bestiario/DMG
      en español

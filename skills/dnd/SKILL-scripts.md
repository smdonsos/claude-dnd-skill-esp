# D&D Skill — Referencia de Scripts

Sintaxis completa de todos los scripts Python auxiliares. Carga este archivo una vez en `/dm:dnd load`, y queda en contexto durante toda la sesión.

> **Nota de rutas:** los comandos de abajo usan `${CLAUDE_SKILL_DIR}` como directorio del skill. Este archivo se lee verbatim, así que ese token **no** se auto-expande acá — sustituye la ruta absoluta del skill dir (desde `SKILL.md`) antes de ejecutar cualquier comando, o va a fallar con una ruta `/scripts/…` rota.

---

## Script de Dados — `scripts/dice.py`

**OBLIGATORIO.** Toda tirada de dados en la partida — chequeos de jugador, ataques de PNJ, salvaciones, daño, generación de puntuaciones de característica, cualquier cosa — debe producirse invocando este script vía Bash. **Nunca muestrees dados mentalmente ni con llamadas `random` inline.** El script enruta las tiradas a través de un servidor local de dados físicos que puede mostrarlas en el teléfono del jugador para que las tire; tirar en tu cabeza evita eso y rompe el ritual. Si el servidor no está corriendo, el script recurre a random local — así que no hay ningún escenario donde el script se deba omitir.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+5
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py 2d6+3
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py 4d6kh3        # tirada de puntuación de característica
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20 adv       # ventaja
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+3 dis     # desventaja + modificador
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20 --silent  # devuelve solo el entero

# Siempre pasa --label para que el HUD del teléfono muestre para qué es la tirada:
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+4 --label "Chequeo de Percepción"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+6 adv --label "Ataque — Jefe Goblin vs Piper"
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py 2d8+3 --label "Daño de Hacha Grande"

# Tiradas de jugador — pasa --player <nombre-pj> para enrutar al teléfono de ese jugador:
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+4 --label "Percepción" --player piper
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+6 adv --label "Ataque" --player piper
# Tiradas de PNJ / monstruo / lado del DM — omite --player (enruta al canal del DM,
# que auto-tira del lado del servidor si el DM no tiene una pestaña abierta).
python3 ${CLAUDE_SKILL_DIR}/scripts/dice.py d20+5 --label "Ataque de goblin"
```

**Regla de enrutamiento:** si la tirada es **para un personaje jugador**, pasa `--player <nombre-pj>` (minúsculas, coincidiendo con el nombre que el jugador usó en la URL). Si la tirada es para un PNJ/monstruo/algo que resuelve el DM, omite `--player` para que no le suene el teléfono a los jugadores.

**Regla de etiqueta (importante):** cuando invoques con `--player`, el jugador no está mirando su teléfono — está escuchando tu narración. **Siempre avísale en voz alta antes de invocar**, para que agarre el teléfono. Patrón:

> *"Piper — haz un chequeo de Percepción. Tíralo."*

Después corre el comando. La llamada de Bash va a bloquear mientras el jugador agarra el teléfono, ve el prompt, y tira; el resultado te vuelve después. Sin el aviso verbal el jugador no va a saber que tiene que mirar, y la llamada va a esperar unos 3 minutos antes de expirar hacia una auto-tirada.

Marca 20 natural (GOLPE CRÍTICO) y 1 natural (PIFIA) automáticamente. Si el output contiene `[auto]`, el teléfono del objetivo no estaba conectado y el servidor tiró por su cuenta — no hace falta ninguna acción, solo narra el resultado.

Para forzar que se salte el tirador físico (ej. tiradas de PNJ de alto volumen que no quieres mostrar): flag `--auto`, o `DND_DICE_PHYSICAL=0 python3 ...`.

---

## Script de Puntuaciones de Característica — `scripts/ability-scores.py`
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py roll
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py pointbuy
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py pointbuy --check STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
python3 ${CLAUDE_SKILL_DIR}/scripts/ability-scores.py modifiers STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
```
Modo tirada: genera 3 arreglos (4d6kh3 × 6 cada uno). Modo compra por puntos: imprime la tabla de costos; `--check` valida contra el presupuesto de 27 puntos.

---

## Script de XP — `scripts/xp.py`
Otorga XP por combate y encuentros no-combate que califican. Lee los archivos de personaje del directorio de la campaña, actualiza la XP, y empuja a la barra lateral del display. Todas las tablas (umbrales de dificultad, valor de desafío→XP, multiplicadores de monstruo, avance de nivel) están codificadas en el script — el DM solo decide el nivel de dificultad o provee una lista de monstruos.

```bash
# Vista previa — no modifica archivos:
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py calc --level 3 --players 2 --difficulty hard --type combat
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py calc --level 3 --players 2 --monsters "goblin:1/4:3,hobgoblin:1:1"

# Otorgar después de un encuentro de combate — por nivel de dificultad (usar cuando no se dispone de la lista completa de monstruos):
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <nombre> --characters "Max of Thraxx,Ethros the 19th" --difficulty hard --type combat

# Otorgar después de un encuentro de combate — cálculo exacto por valor de desafío (preferido para combates estándar):
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <nombre> --characters "Max of Thraxx,Ethros the 19th" \
  --monsters "goblin:1/4:3,hobgoblin:1:1" --note "Emboscada en el callejón"

# Otorgar por un encuentro no-combate que califica:
python3 ${CLAUDE_SKILL_DIR}/scripts/xp.py award \
  --campaign <nombre> --characters "Max of Thraxx,Ethros the 19th" --difficulty medium --type noncombat \
  --note "interrogatorio a informante del gremio"
```

**Niveles de dificultad:** `easy` `medium` `hard` `deadly`
**Tipos de encuentro:** `combat` `noncombat` (ambos usan la misma tabla de umbrales de dificultad)
**Formatos de valor de desafío de monstruo:** `1/4`, `0.25`, `1/2`, `0.5`, `1/8`, `0.125`, o entero (`1`, `5`, `10`)
**Cantidad de monstruos:** omitir para 1 (ej. `"dragon:10"`); explícito para grupos (ej. `"goblin:1/4:3"`)
**Multiplicador de monstruo** (aplicado automáticamente): ×1 (1), ×1.5 (2), ×2 (3–6), ×2.5 (7–10), ×3 (11–14), ×4 (15+)

`award` actualiza el campo de XP del archivo de personaje, marca SUBIDA DE NIVEL PENDIENTE si se cruza un umbral, y empuja la XP al display vía `push_stats.py`. La etiqueta `--note` se imprime solo en terminal — no se guarda.

---

## Script de Combate — `scripts/combat.py`
```bash
# Tirar iniciativa e imprimir el tracker
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py init '<JSON>'
# JSON: [{"name":"Flerb","dex_mod":0,"hp":12,"ac":16,"type":"pc"}, ...]

# Reimprimir el tracker desde el estado guardado
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py tracker '<JSON>' <round_num>

# Resolver un solo ataque
python3 ${CLAUDE_SKILL_DIR}/scripts/combat.py attack --atk 4 --ac 15 --dmg 2d6+2
```
`init` produce una línea `STATE_JSON:` — guárdala en `state.md` bajo `## Active Combat` entre turnos.

---

## Script de Personaje — `scripts/character.py`
```bash
# Ficha completa a partir de puntuaciones crudas
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py calc --class fighter --level 1 \
    STR=15 DEX=10 CON=15 INT=9 WIS=11 CHA=14 \
    --proficient STR CON Athletics Intimidation Perception Survival

# Cálculo de PG y bonificadores al subir de nivel
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py levelup --class fighter --from 1 --hp-roll 7 --con-mod 2

# Seguimiento de XP
python3 ${CLAUDE_SKILL_DIR}/scripts/character.py xp --level 1 --gained 150
```

---

## Script de Display de Estadísticas — `display/push_stats.py`
Empuja estadísticas de personaje y combate a la barra lateral. Los jugadores se combinan por nombre; las actualizaciones parciales funcionan.

```bash
# Push completo de estadísticas (en /dm:dnd load — usar --replace-players para limpiar personajes obsoletos):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --replace-players --json '{
  "players": [{
    "name": "Flerb", "race": "Tiefling", "class": "Fighter", "level": 1, "background": "Soldier",
    "hp": {"current": 12, "max": 12, "temp": 0},
    "xp": {"current": 220, "next": 300},
    "ac": 16, "initiative": "+0", "speed": 30,
    "hit_dice": {"remaining": 1, "max": 1, "die": "d10"},
    "second_wind": true,
    "ability_scores": {
      "str": {"score": 15, "mod": "+2"}, "dex": {"score": 10, "mod": "+0"},
      "con": {"score": 15, "mod": "+2"}, "int": {"score": 9, "mod": "-1"},
      "wis": {"score": 11, "mod": "+0"}, "cha": {"score": 14, "mod": "+2"}
    },
    "sheet": {
      "attacks": [
        {"name": "Longsword", "bonus": "+4", "damage": "1d8+2", "type": "Slashing", "notes": "Versatile (1d10)"},
        {"name": "Handaxe",   "bonus": "+4", "damage": "1d6+2", "type": "Slashing", "notes": "Thrown 20/60 ft"}
      ],
      "spells": null,
      "features": [
        {"name": "Second Wind",  "text": "Bonus action: regain 1d10+level HP. Recharges on short/long rest."},
        {"name": "Action Surge", "text": "Once per rest: take an additional action on your turn."}
      ],
      "inventory": ["Longsword", "Handaxe ×2", "Chain Mail", "Shield", "Explorer'\''s Pack", "15 gp"]
    }
  }]
}'

# subclaves de sheet: attacks, spells ({slots, save_dc, attack_bonus, cantrips, prepared} o null),
# features ([{name, text}]), inventory ([strings])
# sheet es opcional — omitir si solo necesitas la barra lateral de estadísticas sin el modal de ficha completa

# Actualizaciones parciales (usar cada vez que cambien valores durante la sesión):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --hp 7 12
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --xp 220 300
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --second-wind false

# PG temporales (Symbiotic Entity, Aid, etc.):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --temp-hp 8   # fijar
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --temp-hp 0   # limpiar

# Dados de golpe (descanso corto):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --hit-dice-use          # gastar uno
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --hit-dice-restore 2    # restaurar N

# Condiciones — reemplazo completo:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --conditions "Poisoned,Frightened"
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --conditions ""          # limpiar todas

# Condiciones — granular (preferido durante la sesión):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --conditions-add "Poisoned"
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --conditions-remove "Poisoned"

# Concentración:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --concentrate "Bless"
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --concentrate ""        # limpiar

# Espacios de conjuro — reemplazo completo (en /dm:dnd load):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb \
  --spell-slots '{"1":{"used":1,"max":4},"2":{"used":0,"max":2}}'

# Espacios de conjuro — granular (preferido durante la sesión):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --slot-use 1      # gastar un espacio de nivel 1
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --slot-restore 2  # restaurar un espacio de nivel 2

# Inventario — granular (preferido a una reescritura completa de --sheet):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --inventory-add "Iron key"
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Flerb --inventory-remove "Folded paper"

# Posturas de facción (para todo el grupo — REQUERIDO en /dm:dnd load para mostrar el panel de facciones):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py \
  --factions '[{"name":"Pale Court","standing":"Allied"},{"name":"Watch","standing":"Neutral"}]'
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --factions '[]'   # limpiar todas

# Orden de turno de combate (en /dm:dnd combat start):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-order \
  '{"order":["Goblin 1","Flerb","Goblin 2"],"current":"Goblin 1","round":1}'

# Avanzar el puntero de turno:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-current "Flerb"

# Nueva ronda:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-current "Goblin 1" --turn-round 2

# Combate terminado:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-clear

# Reloj del mundo:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --world-time \
  '{"date":"19 Ashveil 1312 AR","day_name":"Moonday","time":"morning","season":"Long Hollow","weather":"calm"}'

# Limpiar el display (usar push_stats.py, NO curl — curl crudo no tiene el token de auth en modo LAN):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --clear

# Cuenta regresiva del ciclo de autorun (mostrada en el panel de input del grupo):
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-waiting true --autorun-cycle 60
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-waiting false   # ocultar después de que se resuelva el turno

# Umbral de N jugadores — dispara automáticamente cuando N jugadores (no todos) están listos:
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-threshold 2   # dispara cuando 2 están listos
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-threshold 0   # resetear a la cantidad de jugadores
```

**Cola de input de jugador — `display/check_input.py`:**
```bash
# Se llama al inicio de cada turno ANTES de procesar el mensaje del jugador.
# Drena cualquier acción encolada desde el companion del display (ej. un iPad) y la imprime.
# Output: "[Max of Thraxx]: I draw my rapier" — vacío si no hay nada encolado. Limpia el indicador del display.
python3 ${CLAUDE_SKILL_DIR}/display/check_input.py
```

Si `check_input.py` devuelve output, antepónelo al input de terminal del jugador al armar el turno:
- Solo input encolado: tratarlo como la acción completa del jugador este turno
- Input encolado + input de terminal: combinar como `[Personaje]: <encolado>\n[Personaje]: <terminal>`
- Cola vacía: proceder normalmente (usar solo el input de terminal)

---

**Cuándo empujar estadísticas:**
- `/dm:dnd load` → `--replace-players --json` (estadísticas completas) + `--spell-slots` + `--world-time` + `--factions`
- Cambio de PG → `--player NOMBRE --hp <actual> <máximo>`
- PG temporales ganados/perdidos → `--player NOMBRE --temp-hp N` (0 para limpiar)
- XP otorgada → `--player NOMBRE --xp <actual> <siguiente>`
- Segundo Aliento usado/recuperado → `--player NOMBRE --second-wind false/true`
- Dado de golpe gastado → `--player NOMBRE --hit-dice-use`; restaurado → `--hit-dice-restore N`
- Espacio de conjuro usado → `--player NOMBRE --slot-use <nivel>`; restaurado → `--slot-restore <nivel>`
- Condición ganada → `--player NOMBRE --conditions-add "Nombre"`; removida → `--conditions-remove "Nombre"`
- Concentración iniciada → `--player NOMBRE --concentrate "Conjuro"`; terminada → `--concentrate ""`
- Objeto recogido → `--player NOMBRE --inventory-add "Objeto"`; soltado/usado → `--inventory-remove "Objeto"`
- Efecto temporizado inicia → `--effect-start "NOMBRE:CONJURO:DURACIÓN[:conc]"` incluido con el send de narración
- Efecto temporizado termina → `--effect-end "NOMBRE:CONJURO"` incluido con el send de narración
- Cambio de postura de facción → `--factions '[...]'` (reemplazo completo)
- Inicio de combate → `--turn-order`; cada turno → `--turn-current`; fin → `--turn-clear`
- Subida de nivel → empujar estadísticas completas actualizadas
- Descanso largo → restaurar PG, dados de golpe, espacios de conjuro, segundo aliento; empujar `--world-time` con la hora actualizada
- Cualquier descanso o avance de tiempo → empujar `--world-time`

**Mantén el reloj honesto.** El reloj del mundo es continuidad, no decoración. Narra de forma consistente con la hora que empujaste por última vez, y avánzalo *deliberadamente* cuando una acción cueste tiempo — un intercambio breve son unos minutos, una búsqueda o una compra es más largo, un descanso o un viaje todavía más. Nunca dejes que la hora del día derive sola o se resetee silenciosamente entre escenas. Si el reloj y la ficción alguna vez no coinciden, reconcílialo con la verdad con un push `--world-time` fresco en vez de acumular el error; ponerlo *hacia atrás* a la hora correcta está bien y no deshace nada, ya que los efectos temporizados corren en sus propias duraciones de ronda/minuto/hora en `tracker.py`, independientes del reloj de pared.

---

## Script de Tracker — `scripts/tracker.py`
Rastrea condiciones, concentración, efectos temporizados, y tiradas de salvación contra la muerte. El estado persiste en `~/.claude/dnd/campaigns/<nombre>/tracker.json`.

```bash
CAMP=my-campaign

# Efectos temporizados — duración: 10r (rondas), 60m (minutos), 8h (horas), indef
# Agrega 'conc' para marcar como concentración (fija el campo de concentración automáticamente)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Max of Thraxx" "Web" 10r conc
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Ethros the 19th" "Disguise Self" 1h
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect start "Ethros the 19th" "Hunter's Mark" indef
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect end   "Max of Thraxx" "Web"   # fin narrativo (roto/disipado)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP effect tick  "Max of Thraxx"         # llamar en el turno del actor — decrementa rondas, imprime expiración

# Condiciones
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition add "Ethros the 19th" poisoned
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition remove "Ethros the 19th" poisoned
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP condition clear "Ethros the 19th"

# Concentración (limpia automáticamente la anterior si se cambia de conjuro)
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP concentrate "Max of Thraxx" "Bless"
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP concentrate "Max of Thraxx" break

# Tiradas de salvación contra la muerte
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" success
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" failure
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" stable
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP saves "Ethros the 19th" reset

# Estado / limpiar
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP status
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP status "Ethros the 19th"
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP clear           # condiciones + concentración + efectos
python3 ${CLAUDE_SKILL_DIR}/scripts/tracker.py -c $CAMP clear --all     # también limpia tiradas de salvación contra la muerte
```

**Cuándo correrlo:** condición aplicada/removida; el lanzador inicia/pierde concentración (inmediatamente, no al final del turno); un PJ cae a 0 PG; cada tirada de salvación contra la muerte; fin del encuentro → `clear`.

---

## Script de Calendario — `scripts/calendar.py`
```bash
# Configuración única (correr durante /dm:dnd new):
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP init \
    --date "15 Harvestmoon 1247" \
    --time "morning" \
    --months "Frostfall,Deepwinter,Thawmonth,Seedtime,Bloomtide,Highsun,Harvestmoon,Duskfall" \
    --month-length 30 \
    --day-names "Sunday,Moonday,Ironday,Windday,Earthday,Fireday,Starday"

# Avance de tiempo
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP advance 8 hours
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP advance 2 days
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP rest short   # +1 hora
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP rest long    # +8 horas

# Consulta / fijar manualmente
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP now
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP set "22 Harvestmoon 1247" evening
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP time night
python3 ${CLAUDE_SKILL_DIR}/scripts/calendar.py -c $CAMP events
```

**Cuándo correrlo:** después de cada descanso; después de un viaje significativo o un salto de tiempo; al actualizar manualmente la fecha en `state.md` — usa `calendar.py set` para mantenerlos sincronizados.

**Nota:** `--time`/`calendar.py time` solo acepta estos seis tokens literales en inglés (`midnight`, `early morning`, `morning`, `afternoon`, `evening`, `night`, más `midday`) — son vocabulario de CLI que el script matchea exactamente, no traducir aunque la documentación esté en español. El campo `time` de `push_stats.py --world-time` es distinto: es un string libre que se muestra tal cual en la barra lateral, y ahí sí se puede poner "mañana", "tarde", etc.

---

## Búsqueda de Campaña — `scripts/campaign_search.py`
Búsqueda por palabra clave a través de los archivos de campaña. Usa esto **antes** de cargar archivos completos al contexto cuando busques un evento pasado específico, un detalle de PNJ, o un hilo argumental.

```bash
CAMP=my-campaign

# Buscar en todos los archivos por defecto (state, log, archive, world, npcs):
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP Lasswater

# Acotar a archivos específicos:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP "merchant letter" --files log,archive

# Búsqueda AND multi-palabra clave:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP VARETH Kel

# Más líneas de contexto alrededor de cada coincidencia:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_search.py -c $CAMP Harwick -C 6
```

Claves de archivo: `state`, `log`, `archive`, `world`, `seeds`, `npcs`, `npcsfull`
Archivos buscados por defecto: state, log, archive, world, npcs

**Cuándo usarlo:** cada vez que un jugador pregunte sobre un evento pasado, un detalle de PNJ, una ubicación, o un hilo argumental que podría no estar en el contexto activo. Corre esto primero — escala a un `Read` completo solo si la búsqueda devuelve contexto insuficiente.

---

## Resumen de Sesión — `scripts/session_recap.py`

Diferencia de estado determinística entre dos snapshots de personaje. Calcula el conjunto de cambios mecánicos (PG/temporales/nivel/dados de golpe/tiradas de salvación contra la muerte/condiciones/concentración/cansancio/inspiración/espacios de conjuro) a partir de datos, así la narración nunca lo recalcula — los resúmenes son lo que un LLM tiene más probabilidad de alucinar. Lee `<campaña>/characters/*.md` y combina las condiciones/concentración en vivo de `tracker.json`. Cero llamadas al LLM.

```bash
CAMP=my-campaign

# Sacar una foto del grupo ahora — fija la línea base (escribe en <campaña>/.recap/,
# rotando last → prev). Correr esto al INICIO de la sesión (ej. /dm:dnd load) para que
# haya una línea base contra la cual comparar después.
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py snapshot --campaign $CAMP

# Comparar la línea base contra el estado actual → resumen de un párrafo, después AVANZA
# la línea base a "ahora" para que la próxima comparación encadene desde acá. Correr en
# /dm:dnd save (fin de sesión) para un resumen desde-el-inicio, o cada turno para un
# resumen desde-el-último-turno — de cualquier forma avanza, así comparaciones
# consecutivas nunca re-reportan cambios viejos.
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP
# → "Aldric: took 18 damage (30→12 HP); gained Poisoned; spent 2 level 1 slots."

# Misma comparación sin mover la línea base (ad-hoc "¿qué cambió hasta ahora?"):
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP --no-roll

# Lista de cambios estructurada en vez de prosa:
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff --campaign $CAMP --json

# Comparar dos archivos de snapshot directamente (sin buscar la campaña):
python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py diff-files before.json after.json
```

---

## Oráculo — `scripts/oracle.py`

Oráculos en solitario/improvisación guiados por dados (factor de caos Mythic, sí/no Ironsworn, Foco de Evento Aleatorio, pares de palabras de significado de escena). Mantiene el ritmo transparente y sujeto a tirada en vez de inventado. Las tiradas son random de la librería estándar y admiten semilla (`--seed N`). El factor de caos persiste en `state.md → ## Session Flags` como `chaos_factor: N`. Cero llamadas al LLM.

```bash
CAMP=my-campaign

# Factor de caos (1-9): mostrar / fijar / ajustar (persiste en state.md)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos --campaign $CAMP
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos set --campaign $CAMP --value 7
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py chaos adjust --campaign $CAMP --pc-lost

# Oráculo sí/no — probabilidad + modificador de caos → veredicto + d100
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py ask --likelihood likely --campaign $CAMP
# → "NO-BUT  (d100=82, likelihood=likely, chaos=8)"

# Foco de Evento Aleatorio (d100 → etiqueta de dirección)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py event

# Par de palabras de significado de escena (acción / sujeto)
python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py scene
```

Probabilidades: `sure-thing`, `likely`, `50/50`, `unlikely`, `no-way`. Sufijos de veredicto: `-and` (extremo, en dobles), `-but` (calificado, cerca del umbral).

---

## Extracción Determinística de Grafo — `scripts/graph_extract_deterministic.py`

Extractor de relaciones cero-LLM. Compara por patrones las oraciones del log de sesión contra la semilla del léxico de verbos incluida (`data/graph/verb_table_seed.yaml`) y emite propuestas de arista tipada en la forma exacta que consume `campaign_graph.py`. ~50% de recall (solo sujeto-verbo-objeto limpio), ~95% de precisión, sin llamada a la API de Claude. Normalmente se invoca a través de `campaign_graph.py extract --deterministic` en vez de directamente:

```bash
CAMP=my-campaign

# Proponer aristas (stdout), sin escribir:
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py extract --campaign $CAMP --deterministic

# Auto-aplicar de una vez las propuestas de alta confianza a graph.json (idempotente):
python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py extract --campaign $CAMP \
    --deterministic --apply --min-confidence high
```

---

## Comandos de Datos — `scripts/sync_srd.py`, `scripts/build_srd.py`, y `scripts/lookup.py`

El dataset viene incluido en `${CLAUDE_SKILL_DIR}/data/dnd5e_srd.json`. No requiere descarga en tiempo de ejecución.

```bash
# Chequear / reconstruir el dataset (solo hace falta cuando las fuentes originales se actualizan):
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py             # reconstruye si 5e-bits o FoundryVTT tienen commits nuevos
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py --check     # chequea los SHA originales, no reconstruye
python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py --force     # siempre reconstruye
python3 ${CLAUDE_SKILL_DIR}/scripts/build_srd.py --status   # muestra los metadatos actuales del dataset

# Búsqueda durante la partida (CLI):
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py spell "fireball"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py item "cloak of protection"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py feature "sneak attack"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py condition "poisoned"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py monster "goblin"
python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py monster "dragon" --all   # todas las coincidencias aproximadas

# Programático (usado por el endpoint /srd-lookup del companion del display):
from lookup import lookup, lookup_record, lookup_with_level, suggest
lookup("fireball", category="spell")                  # → string formateado
lookup_with_level("sneak attack", category="feature", level=3)  # → string resuelto por nivel
suggest("poisonned", category="condition")            # → [("Poisoned", "conditions"), ...]
```

**Recuperación de "quisiste decir".** Un nombre mal tipeado no es un callejón sin salida. Cuando una búsqueda falla, el CLI imprime una línea `Did you mean: …?` y el modal SRD del display ofrece chips tocables de coincidencias cercanas — ambos con `suggest()`, que hace fuzzy-match de la consulta contra nombres reales (`poisonned` → Poisoned, `fireballl` → Fireball, `gobblin` → Goblin). Las sugerencias respetan la categoría cuando se da una, y buscan en todas las categorías si no. Usa el nombre sugerido en vez de adivinar la ortografía.

**Cuándo usarlo:** combate (fichas de monstruo antes de usarlas); lanzamiento de conjuros (alcance, componentes, duración, a niveles superiores); condiciones (texto de regla antes de aplicarla); botín y equipo; generación de PNJ (ficha de monstruo como base mecánica). El modal de ficha de personaje del companion del display maneja las búsquedas automáticamente durante la partida — estas llamadas de CLI son para referencia del DM fuera de la UI.

---

## Configuración del Companion del Display (única vez)

```bash
cd ${CLAUDE_SKILL_DIR}/display
pip3 install -r requirements.txt
```

```
Terminal (correr claude directamente — no hace falta wrapper)
    ↓ llamadas a send.py por bloque de narración / tirada de dados / cambio de estadística
Flask en https://localhost:5001 (dnd-display-app.py — HTTPS, certificado autofirmado)
    ↓ Server-Sent Events
Pestaña de navegador → Chromecast → TV
```

**Iniciar el display:**
```bash
bash ${CLAUDE_SKILL_DIR}/display/start-display.sh          # localhost
bash ${CLAUDE_SKILL_DIR}/display/start-display.sh --lan    # modo LAN (teléfonos, tablets)
open https://localhost:5001                                  # abrir el navegador antes de /dm:dnd load
```

`start-display.sh` siempre mata a la fuerza cualquier instancia previa antes de iniciar — no hace falta matarla manualmente de antemano.

**Cargar una campaña:**
```
/dm:dnd load <nombre-campaña>   # el skill auto-detecta el display en ejecución, empuja las estadísticas del grupo
```

El skill de DM envía cada bloque de narración, resultado de dados, y actualización de estadística vía llamadas a `send.py` (ver Modo DM Activo en SKILL.md para la secuencia completa de sends y la referencia de flags de estadísticas).

Abre la pestaña del navegador y haz Chromecast *antes* de correr `/dm:dnd load` para que el navegador esté conectado cuando llegue la narración de apertura. El display guarda un buffer de los últimos 60 fragmentos y los reproduce a los navegadores que se reconectan.

**Detección de escena:** el servidor escanea la narración en busca de palabras clave y cambia el degradado de fondo + tipo de partícula (17 escenas: taberna, mazmorra, bosque, cripta, arcano, océano, etc.). Transición con fundido en ~2.5 s.

**Audio (del lado de Python):** `audio.py`, auto-importado por `dnd-display-app.py`. Dos interruptores: Ambiente (paisaje sonoro en loop) y Efectos (SFX de un solo disparo). Ambos apagados por defecto. Los cambios de escena hacen fundido cruzado del loop ambiente. Toda la síntesis es vía numpy — no hacen falta archivos de audio.

---

## Autoguardado de Continuidad — `scripts/autosave_checkpoint.py`, `scripts/install_autosave_hook.py`

Checkpoint de continuidad detrás de escena para sesiones largas, así una compactación de contexto nunca pierde el lugar del jugador. Dos capas; ver la regla de *Guardado automático de continuidad* en SKILL.md y el comando `/dm:dnd autosave`.

```bash
# Opcional: registrar el Stop hook (escribe ~/.claude/settings.json, idempotente)
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py --uninstall
python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py --status

# El objetivo del hook (también se puede correr a mano para forzar un snapshot o inspeccionar el estado)
python3 ${CLAUDE_SKILL_DIR}/scripts/autosave_checkpoint.py --status
python3 ${CLAUDE_SKILL_DIR}/scripts/autosave_checkpoint.py --campaign <nombre> --snapshot-only
```

`autosave_checkpoint.py` corre como un **Stop hook** de Claude Code (después de cada turno). Lee la campaña activa desde `<runtime-dir>/active-campaign.json` (escrito en `/dm:dnd load`) y el flag `autosave` del `state.md` de esa campaña. **No hace nada** cuando no hay campaña activa (ej. una sesión que no es de D&D), cuando `autosave: off`, o cuando ya está dentro de una continuación manejada por hook. Cada turno saca una foto de `state.md` al directorio runtime; cada N turnos (10 por defecto, `DND_AUTOSAVE_EVERY` para cambiarlo) emite una decisión `block` de Stop-hook que le pide al DM que vuelque la continuidad antes de ceder el control. El hook es **opcional** — el ritmo de guardado automático en el modelo funciona sin él.

**Cuándo usarlo:** ofrécele `install_autosave_hook.py` a jugadores que corren módulos importados largos y se topan con compactación a mitad de sesión. El interruptor del flag (`/dm:dnd autosave on|off`) es el control dentro de la sesión.

## Corpus Perezoso — `scripts/corpus_check.py`

Las campañas importadas (estructuradas) mantienen el texto completo del módulo como una capa de referencia de carga perezosa en vez de incluirlo inline. Estructura:

```
<campaña>/
  world.md           # núcleo de tiempo de carga (Fundamentos, Tres Verdades, facciones)
  world-nodes.md     # perezoso: banco completo de Semillas de Misión + Nodos de Aventura (lectura por acto)
  arc.md             # perezoso: árbol completo de actos/capítulos (state.md solo guarda actual+siguiente)
  source-index.md    # id-de-capítulo -> archivo fuente -> alcance en una línea
  source/<id>.md     # perezoso: un archivo por capítulo, el texto fuente del módulo
```

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/corpus_check.py --campaign <nombre>
```

Valida que cada id de capítulo en `source-index.md` tenga un `source/<id>.md` correspondiente (y viceversa) y que `arc.md` exista. Correrlo al final de `/dm:dnd import`. Una campaña sin capa `source/` (dinámica, sandbox, o una importación anterior a v2.2.0) se reporta como un no-op limpio — nada que validar, y su ruta de carga no cambia.

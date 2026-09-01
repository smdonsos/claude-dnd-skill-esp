# D&D Skill — Procedimientos de comandos

Procedimientos completos, paso a paso, para todos los comandos slash `/dm:dnd`. Cargá este archivo en `/dm:dnd load` o antes de ejecutar cualquier comando slash.

> **Nota de ruta:** los comandos de abajo usan `${CLAUDE_SKILL_DIR}` para el directorio del skill. Este archivo se lee de forma literal, así que ese token **no** se expande automáticamente acá — sustituye la ruta absoluta del skill dir (de `SKILL.md`) antes de correr cualquier comando, o va a fallar con una ruta `/scripts/…` rota.

---

## `/dm:dnd new <nombre-campaña> [tema]`
1. **Configuración de sesión — llama a `AskUserQuestion`** con **dos preguntas**:

   **P1 *"¿Modo de pantalla y de entrada?"***
   - `Sin pantalla` → continuar sin display.
   - `Pantalla (local)` → `bash ${CLAUDE_SKILL_DIR}/display/start-display.sh`, imprimir la URL, poner `_display_running = true`, luego `python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --clear`.
   - `Pantalla (LAN)` → `bash ${CLAUDE_SKILL_DIR}/display/start-display.sh --lan`, imprimir ambas URLs, poner `_display_running = true`, luego `--clear` como arriba.
   - `Pantalla + autorun (LAN)` → igual que **Pantalla (LAN)**, y además escribir `autorun: true` en `state.md → ## Session Flags`.

   Si se activa alguna pantalla: la plantilla de campaña ya trae `sfx_languages: es` en `## Session Flags`, así que los efectos de sonido usan el paquete en español por defecto. Para cambiarlo (ej. `en` o `es,en` con fallback), edita esa línea directamente — ver "Sound Effects" en README.md.

   **P2 *"¿Tiradas de dados?"*** — define cómo se manejan los d20 de los PJ (ver "Convención de tiradas" en SKILL.md):
   - `Los jugadores tiran los suyos` (default) → escribir `roll_mode: players` en `state.md → ## Session Flags`. Vas a pedir cada tirada de PJ y esperar — nunca tirar por un PJ.
   - `El DM tira todo abiertamente` → escribir `roll_mode: auto`. Tú resuelves las tiradas de PJ mostrando toda la matemática.

   Default a `roll_mode: players` si se descarta la pregunta.
2. **Selección de reglamento (agregado 2026-05-08).** Preguntá: *"¿Reglamento de D&D 5e para esta campaña? **2014** (SRD 5.1, default — mecánicas completas, estructura clásica del Manual del Jugador) o **2024** (SRD 5.2, maestría de armas + dotes de trasfondo + ASIs por trasfondo + cansancio revisado)?"* Default a `2014` si no hay respuesta o es ambigua. Escribí el valor elegido en la línea de encabezado de `state.md` como `**Ruleset:** 2014` o `**Ruleset:** 2024`.

   Si se eligió 2024: verifica que el dataset exista con `ls ${CLAUDE_SKILL_DIR}/data/dnd5e_srd_2024.json`. Si falta, corre `python3 ${CLAUDE_SKILL_DIR}/scripts/build_srd.py --ruleset 2024` (una sola vez, ~3 min). Hasta que el dataset exista, las funciones basadas en lookup usan 2014 como fallback.
3. `mkdir -p ~/.claude/dnd/campaigns/<nombre>/characters`
4. Copiá y completa las plantillas de `${CLAUDE_SKILL_DIR}/templates/` — state.md, world.md, npcs.md, session-log.md. El encabezado de state.md mantiene el campo `**Ruleset:**` fijado en el paso 2.
5. Preguntá: **tamaño del grupo** y **nivel inicial**
6. **Asistente de Tono/Género** — presenta los cuatro en un solo mensaje:
   - Tono: `grimdark / fantasía oscura / heroico / terror / político / capa y espada / cósmico`
   - Nivel de magia: `ninguno / bajo / medio / alto`
   - Tipo de ambientación: `medieval / renacentista / antigua / náutica / subterránea`
   - Nivel de peligro: `letal / crudo / estándar / heroico`
   *(Si se proporcionó `[tema]`, precarga el Tono y pregunta las otras tres. Elegí al azar cualquier campo vacío con dice.py y registra `"d6=N → [resultado]"` en world.md.)*
7. **Fundamentos del mundo** — geografía/bioma/clima, sistema de magia, panteón (2–3 deidades activas), calendario. Escribí en `## World Foundations` en world.md. Sembrá `state.md → ## World State → In-world date`.
8. **Tres Verdades** — un asentamiento, una amenaza cercana, un misterio (con pistas). Escribí en las secciones correspondientes de world.md.
9. **Arco de Escalada de la Amenaza** — completa la tabla de cinco etapas en world.md justo después de generar la amenaza. Poné la etapa actual en 1. Escribí `Threat arc stage: 1 — Now` en `state.md → ## World State`.
10. **2 Facciones** — arquetipo, todos los campos incluida la actividad actual. Escribí en `## Factions` en world.md. Escribí los estados de facción en una línea en `state.md → ## World State`.
11. **3 PNJ con red de relaciones** — entradas completas (rol, stats, actitud, motivación, secreto, tic de habla, facción, objetivo actual, horario, ejes de personalidad). Generá los tres primero, después completa Relaciones (cada PNJ necesita ≥2 vínculos con otros). Actualizá la tabla índice.
12. **3–5 Semillas de Misión** a partir de la amenaza, facciones, misterio, motivaciones de PNJ. Escribí en `## Quest Seed Bank` en world.md.
13. **Arco de Campaña Dinámico** — genera automáticamente el arco a partir de todos los datos del mundo recién creados. Usá Opus para este paso. Preguntá: *"¿Generar un arco narrativo comprometido? [s/n — recomendado]"*

   **Si sí:** A partir del tono, las etapas del arco de amenaza, las facciones, las Tres Verdades, las motivaciones de PNJ y las semillas de misión, deriva:
   - **`theme`** — una oración: ¿de qué trata en el fondo esta historia? No la amenaza — su significado.
   - **`resolution`** — la forma comprometida del desenlace: si el grupo tiene éxito, ¿cuál es la verdad emocional? Mantené los eventos específicos abiertos; comprometete con la forma.
   - **Actos 1–3**, cada uno con 2 beats. Cada beat tiene:
     - `label` — un nombre dramático
     - `what_changes` — antes/después: ¿qué es fundamentalmente distinto una vez que esto aterriza? **CRÍTICO: escribe esto como una CONSECUENCIA, no como un evento.** Una consecuencia es un estado del mundo después del beat. Un evento es una cosa específica que pasa. Las consecuencias sobreviven cuando los jugadores se adelantan a la entrega obvia del evento; los eventos se rompen y el beat queda obsoleto. Ejemplo de contraste para un beat 2b "Todo Está Perdido":
       - ❌ Con forma de evento (frágil): *"La nominación de Vedra tiene éxito y toma el tercer asiento."* Si el grupo voltea al escribano, esto no puede aterrizar — el beat queda obsoleto.
       - ✅ Con forma de consecuencia (robusto): *"El grupo sufre un costo concreto de la escalada de los Kept que no puede revertir — una tapadera al descubierto, un aliado comprometido, o una posición en la que confiaban que ya no está disponible."* Esto sobrevive múltiples caminos de entrega.
     - `world_pressure` — el movimiento específico de facción o PNJ (nombrando entidades reales de este mundo) que hace que el beat se sienta inevitable. Esto PUEDE tener forma de evento — pero si los jugadores se adelantan, se espera que revises según la regla 8 de SKILL.md (adelantarse dispara una revisión).
   - **`steering_notes`** — cómo llegar al primer beat sin forzarlo

   Disposición de los beats:
   - Acto 1: **1a Incidente Incitador** (la amenaza se vuelve personal para el grupo), **1b Complicación** (el problema es más grande o más extraño de lo que parecía al principio)
   - Acto 2: **2a Giro del Punto Medio** (lo que el grupo *creía* que estaba haciendo cambia), **2b Todo Está Perdido** (un revés genuino — algo falla, se pierde, o se derrumba)
   - Acto 3: **3a Confrontación Final** (el momento decisivo sobre el que gira la campaña), **3b Resolución** (qué es distinto del mundo y de los personajes después)

   Escribí en `state.md → ## Campaign Arc` con `type: dynamic`. Entregá al DM un resumen del arco de un párrafo.

   **Si no:** Escribí `type: sandbox` en `## Campaign Arc`. La historia queda abierta, sin seguimiento de arco.

14. Escribí state.md con contador de sesión 0, ubicación inicial.
15. **Chequeo de servidor de dados físico (solo si está instalado).** Salteá este paso a menos que el servidor de dados opcional esté configurado: prueba con `test -d ~/.dnd-dice || test "$DND_DICE_PHYSICAL" = "1"` y corta si el test falla. Si pasa, corre `curl -sf http://localhost:7777/health` (timeout 1s). Si devuelve OK, obtén la IP de LAN con `python3 -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()"` y anuncia: *"El servidor de dados está activo. Una vez que cada jugador haya creado un personaje con `/dm:dnd character new`, deberían abrir `http://<ip>:7777/?player=<nombre-pj>` en su teléfono (minúsculas, guiones en vez de espacios) y tocar **consagrar** antes de empezar. Las tiradas de PNJ/DM se resuelven automáticamente en el host."* Si no es alcanzable, saltea en silencio.
16. Confirmá la creación, ofrece `/dm:dnd character new`.

---

## `/dm:dnd load <nombre-campaña>`
0. **Elegí la campaña si no se nombró ninguna.** Si se proporcionó `<nombre-campaña>` (o el jugador claramente nombró una), usala. Si no, haz `ls` en el directorio de campañas (`~/.claude/dnd/campaigns/` o `$DND_CAMPAIGN_ROOT/campaigns/`) y **llama a `AskUserQuestion`**: *"¿Qué campaña?"* con los nombres de campañas existentes como opciones (la jugada más recientemente primero — ordenar por mtime de `state.md`). El jugador puede elegir "Otra" para escribir un nombre. Si no hay campañas, avisale y ofrece `/dm:dnd new`.
1. **Configuración de sesión — llama a `AskUserQuestion`** con **dos preguntas** (no prompts tipeados de s/n):

   **P1 *"¿Modo de pantalla y de entrada?"***
   - `Sin pantalla` → continuar sin display.
   - `Pantalla (local)` → `bash ${CLAUDE_SKILL_DIR}/display/start-display.sh`, imprimir la URL, poner `_display_running = true`.
   - `Pantalla (LAN)` → `bash ${CLAUDE_SKILL_DIR}/display/start-display.sh --lan`, imprimir ambas URLs, poner `_display_running = true`.
   - `Pantalla + autorun (LAN)` → igual que **Pantalla (LAN)**, y además escribir `autorun: true` en `state.md → ## Session Flags`; entrar a la espera de autorun después del resumen.

   **P2 *"¿Tiradas de dados?"*** — confirma cómo se manejan los d20 de los PJ esta sesión (ver "Convención de tiradas" en SKILL.md). Precargá la opción recomendada a partir del `roll_mode` existente en `state.md` si está presente, si no `players`:
   - `Los jugadores tiran los suyos` → escribir `roll_mode: players`. Pedí cada tirada de PJ y espera — nunca tires por un PJ.
   - `El DM tira todo abiertamente` → escribir `roll_mode: auto`. Resolvé las tiradas de PJ mostrando toda la matemática.

   - (Defaults si el jugador descarta la pregunta: sin pantalla, sin autorun, `roll_mode: players` — o el valor guardado existente.)
   - **Repetición de la cola de sesión (session tail):** antes de limpiar el display, chequea si existe `session_tail.json` de la campaña. La ruta del lado de la campaña es la autoritativa — `~/.claude/dnd/campaigns/<nombre>/session_tail.json`. **No leas** el legado/fallback en `${CLAUDE_SKILL_DIR}/display/session_tail.json`; ese archivo puede existir de sesiones anteriores u otras campañas y va a confundir la repetición. Si el archivo del lado de la campaña no existe, saltea la repetición (el display arranca vacío). Si existe, leelo. Después de `--clear` y el push completo de stats (paso 4 abajo), repite la cola enviando cada entrada con el flag apropiado de `send.py`. Mapeo tipo de entrada → flag:
     - clave `player` presente → `send.py --player <nombre>` con texto vía stdin
     - clave `npc` presente → `send.py --npc <nombre>` con texto vía stdin
     - clave `dice` presente → `send.py --dice` con texto vía stdin
     - clave `xp_award` presente → `send.py --xp-award '<json del sub-diccionario xp_award>'`
     - clave `inspiration_award` presente → `send.py --inspiration-award '<nombre>'`
     - ninguna de las anteriores (narración pura del DM) → `send.py` con texto vía stdin
     Esto restaura la última escena en el display antes del resumen. La cola se escribe continuamente por `dnd-display-app.py` — siempre contiene los últimos intercambios de la sesión anterior sin importar cómo terminó la sesión.
   - Limpiar la transcripción previa: `python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --clear`

     ⚠ **`--clear` borra tanto el log de texto COMO las stats** (tarjeta de jugador, tiempo del mundo, facciones, misiones). Siempre debe ir emparejado con el push completo `--replace-players ... --world-time ... --factions ... --quests ...` del paso 4 — si no, la tarjeta lateral y la pestaña de hoja de personaje se renderizan vacías. La misma regla aplica cualquier vez que hagas `--clear` a mitad de sesión (ej. restaurando el estado de escena después de una re-repetición): siempre re-envía el JSON completo de personajes + world-time + factions + quests en la misma ráfaga de bash que el clear.
   - Registrar la campaña activa para DM Help: `python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --set-campaign <nombre-campaña>`
   - Si autorun **sí** → escribir `autorun: true` en `state.md → ## Session Flags`; entrar a la espera de autorun después del párrafo de resumen.
   - Si autorun **no** → continuar sin autorun; el DM lleva los turnos manualmente.
   - **Chequeo de servidor de dados físico (solo si está instalado).** Salteá este paso a menos que el servidor de dados opcional esté configurado: prueba con `test -d ~/.dnd-dice || test "$DND_DICE_PHYSICAL" = "1"` y corta si el test falla. Si pasa, corre `curl -sf http://localhost:7777/health` (timeout 1s). Si devuelve OK, obtén la IP de LAN con `python3 -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()"` y anuncia a la mesa: *"El servidor de dados está activo. Cada jugador, abran `http://<ip>:7777/?player=<su-nombre-pj>` en su teléfono (nombre en minúsculas, guiones en vez de espacios — el mismo nombre que voy a usar al pedir tiradas) y toquen **consagrar** antes de empezar. Las tiradas de PNJ y DM se resuelven automáticamente acá."* Después lista los nombres cortos de los PJ de `characters/` para que los jugadores sepan qué escribir. Si el servidor no es alcanzable, saltea en silencio — `dice.py` cae de vuelta a aleatorio local.

2. **Retrocompatibilidad: chequeo de migración de reglamento.** Antes de leer state.md, corre:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/migrate_ruleset.py <nombre-campaña> --check
   ```

   - Código de salida `0` (`migrated`) → proceder al paso 3.
   - Código de salida `1` (`needs-migration`) → esto es una campaña legada anterior al campo de reglamento. Mostrale al DM exactamente una vez: *"Esta campaña es anterior al versionado de reglamento. ¿La marco como **2014** (recomendado para campañas legadas) o **2024**? state.md se respaldará en `state.md.backup-pre-ruleset-<timestamp>` antes de cualquier escritura. [2014/2024/omitir]"*. Con la respuesta, corre:

     ```bash
     python3 ${CLAUDE_SKILL_DIR}/scripts/migrate_ruleset.py <nombre-campaña> --ruleset 2014 --yes
     # o --ruleset 2024
     ```

     El migrador es idempotente y crea un respaldo con timestamp. Con `omitir`, no migres; `paths.campaign_ruleset()` va a devolver `2014` como default de seguridad al leer, pero el campo queda sin marcar (se le va a volver a preguntar al DM en la próxima carga).
   - Código de salida `2` (`missing`) → no se encontró state.md; no continúes con /dm:dnd load. Mostrale el error al DM.

   Migraciones futuras (ej. cuando llegue el reglamento 2026) siguen el mismo patrón: un pequeño script migrador bajo `scripts/migrate_<tema>.py` invocado acá como un par `--check` y después `--yes`.

3. **Leé el reglamento de la campaña** para esta sesión: `python3 ${CLAUDE_SKILL_DIR}/scripts/paths.py campaign-ruleset <nombre>` (o importa `campaign_ruleset` directamente). Guardá el resultado; pasa `--ruleset <valor>` a las llamadas de `lookup.py`, `build_supplemental.py`, y `combat.py mastery` para que enruten al dataset correcto. El display companion recibe el mismo valor automáticamente vía `push_stats.py --set-campaign`.

4. Leé SKILL-scripts.md (para la sintaxis de scripts de esta sesión)
5. **Marcá esta campaña como activa** (para el hook de autosave): escribe `{"name": "<nombre-campaña>"}` en `$(python3 ${CLAUDE_SKILL_DIR}/scripts/paths.py runtime-dir)/active-campaign.json`. Esto es lo que lee `autosave_checkpoint.py` para saber qué campaña checkpointear; un marcador desactualizado es inofensivo. Después lee state.md, world.md, npcs.md (solo el índice), y todos los characters/*.md
   - **state.md contiene `## DM Style Notes`** — lee e internaliza antes de narrar cualquier cosa. Son patrones de calibración específicos de esta mesa que anulan los instintos por defecto del DM.
   - **state.md contiene `## Pinned Facts`** — lee y mantén presentes durante toda la sesión. Son hechos blandos y estables que la mesa eligió no olvidar nunca (una promesa hecha, el nombre de un pariente muerto, una regla casera, una broma recurrente, un detalle que el jugador marcó como importante). A diferencia de Live State Flags, no cambian turno a turno — son canon permanente. Incorporalos cuando sea relevante y nunca contradigas uno; si un hecho fijado ahora es incorrecto, corregilo vía `/dm:dnd pin` en vez de sobreescribirlo en silencio. Si la sección dice *(none pinned yet)*, no hay nada que cargar.
   - **world.md:** Cargá completo — Fundamentos del Mundo, Tres Verdades, y facciones informan la narración y los movimientos de facción. NO leas `world-seeds.md` al cargar (artefacto de generación, no referencia en vivo).
   - **world-nodes.md (solo campañas importadas):** NO cargar al inicio de sesión. Contiene todo el Banco de Semillas de Misión y los Nodos de Aventura del módulo completo; lee solo los nodos del acto actual cuando una escena los necesite. Si el archivo no existe (dinámica/sandbox, o una importación más vieja), no hay nada que cargar de forma perezosa — `world.md` ya lleva los nodos, sin cambios respecto al comportamiento anterior.
   - **arc.md (solo campañas importadas):** NO cargar al inicio de sesión. `state.md → ## Campaign Arc` ya lleva la ventana del capítulo actual + siguiente. Leé `arc.md` solo al avanzar de capítulo o cuando un jugador pregunte sobre el arco más amplio. Si no existe, el arco vive inline en `state.md` (dinámica/sandbox) — leelo ahí como antes. **Chequeá el puntero al cargar:** si el `current_chapter` de `## Campaign Arc` muestra sus `outstanding_beats` ya vacíos, o la última sesión claramente terminó en la ubicación o situación del *siguiente* capítulo, el puntero nunca avanzó — mostralo (*"el capítulo actual parece terminado; ¿seguimos en `<next_chapter>`?"*) en vez de abrir otra escena en un capítulo que ya está resuelto. Un puntero que nunca se mueve es exactamente cómo una campaña estructurada se desvía en silencio de su propio arco y empieza a improvisar.
   - **source/<chapter-id>.md (solo campañas importadas):** el texto completo del módulo, un archivo por capítulo. Nunca se carga al inicio de sesión. Antes de correr una escena en un capítulo, lee el `source/<id>.md` de ese capítulo (el `source_ref` en el arco) — y solo ese capítulo. Es el equivalente de historia predefinida de leer la entrada completa de un solo PNJ bajo demanda.
   - **npcs.md:** Solo la fila del índice al cargar. **Antes de escribir diálogo sustancial o decisiones para cualquier PNJ nombrado, lee su entrada completa en `npcs-full.md`.** No esperes una llamada explícita a `/dm:dnd npc [nombre]` — hacelo proactivamente cuando una escena gira en torno a ese personaje. Las filas del índice llevan solo rasgos superficiales; los ejes de personalidad, relaciones, y objetivos ocultos están en la entrada completa.
   - **NO leas session-log.md al cargar** — los eventos recientes ya están en `state.md → ## Recent Events`. Leé session-log.md solo si el jugador pide explícitamente un resumen, o si se necesita Calibración del DM de las últimas 1-2 sesiones y no está ya internalizada.
6. Enviá las stats completas del grupo a la barra lateral del display. **CRÍTICO:** usa `--json` con un objeto de jugador completo — **nunca** el atajo `--player` acá. `--player` solo actualiza campos existentes; no puede poblar la tarjeta ni las pestañas de hoja. El display muestra "Full sheet not loaded" cuando falta `sheet`.

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --replace-players --json '{
     "players": [
       {
         "name": "NombrePJ",
         "race": "Raza",
         "class": "Clase (Trasfondo)",
         "level": N,
         "hp": {"current": N, "max": N, "temp": 0},
         "ac": N,
         "speed": 30,
         "hit_dice": {"max": N, "remaining": N, "die": "d8"},
         "xp": {"current": N, "next": N},
         "conditions": [],
         "concentration": null,
         "inspiration": 0,
         "spell_slots": {},
         "sheet": {
           "attacks": [{"name":"...","bonus":"+N","damage":"...","type":"...","notes":"..."}],
           "features": [{"name":"Rasgo 1","text":"Descripción de qué hace."},{"name":"Rasgo 2","text":"Descripción."}],
           "inventory": ["Objeto 1", "Objeto 2"]
         }
       }
     ]
   }'
   ```

   Para lanzadores de conjuros, agrega `"spells": {"cantrips":["..."],"level1":["..."]}` dentro de `sheet`. Omitilo para no-lanzadores.

   **Inspiración:** leela de `state.md → ## Current Situation → Party status`. Poné `"inspiration": 1` (o `true`) si el personaje la tiene, `0` si no. La Inspiración NO se resetea con un descanso largo — persiste hasta gastarse. Debe registrarse explícitamente en la línea de estado del grupo en `/dm:dnd save` (ej. `Mara: Inspiration ✓`) y cargarse en `/dm:dnd load`. Usá `push_stats.py --player <nombre> --inspiration true/false` para actualizaciones a mitad de sesión.

   `--replace-players` limpia personajes obsoletos de campañas anteriores. Armá el JSON a partir del archivo de personaje — cada campo de arriba es obligatorio para que la tarjeta y las pestañas de hoja se rendericen correctamente.

   También envía `--world-time`, `--factions`, y `--quests` en la **misma** llamada a `push_stats.py` que el JSON de jugadores para evitar condiciones de carrera donde el servidor de display recibe una actualización parcial. Combiná todo en una sola invocación:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --replace-players \
     --json '{...jugadores...}' \
     --world-time '{...}' \
     --factions '[...]' \
     --quests '[...]'
   ```

   Estructura JSON de facciones — **`standing` es obligatorio**:
   ```json
   [{"name":"Pale Court","standing":"Allied"},{"name":"The Kept","standing":"Hostile"}]
   ```
   Valores de `standing`: `Allied`, `Friendly`, `Neutral`, `Suspicious`, `Hostile`. Si se omite el campo, `dnd-display-app.py` lo pone por defecto en `"Neutral"` y registra una advertencia en stderr — pero incluilo siempre explícitamente. Mapeá la prosa de `state.md` a los valores exactos (ej. "aliado profundo" → `"Allied"`, "hostil activo" → `"Hostile"`). Usá `[]` para limpiar.

   El panel de facciones solo aparece cuando hay al menos una facción presente — no te saltees este push.

   Estructura JSON de misiones:
   ```json
   [{"name":"El Cargamento Perdido","status":"resolved"},{"name":"Keth el Coleccionista","status":"threat"}]
   ```
   Valores de `status` de misión: `active` (ámbar), `threat` (rojo), `resolved` (verde), `failed` (apagado). Usá `[]` para limpiar todas las misiones:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --quests '[...]'
   ```
   El panel de misiones solo aparece cuando hay al menos una misión presente — no te saltees este push.
7. **Traé el contexto de escena del grafo de campaña.** Corre siempre, incluso si sospechas que `graph.json` no existe — el script termina limpiamente con un aviso cuando no está inicializado.
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py scene-context \
     --campaign <nombre-campaña> \
     --place "<nombre-o-id-de-ubicación-actual>" \
     --present "<nombres-de-PNJ-probablemente-presentes-separados-por-coma>" \
     --hops 2 \
     --at-session <sesión-N-actual>
   ```
   Identificá `<ubicación-actual>` desde `state.md → ## World State → location` (o la ubicación más reciente en `## Recent Events`). Identificá `<presentes>` de los PNJ probablemente en escena según `state.md` / `session-log.md`. `<sesión-N-actual>` es `state.md → ## Session Count`.

   La salida es un subgrafo enfocado (nodos por tipo + bloque de relaciones). **Internalizá este subgrafo antes de entregar el resumen** — es la fuente autoritativa de quién-se-relaciona-con-quién en la escena actual. No releas `npcs-full.md` para relaciones que puedes responder desde el subgrafo.

   Si la salida dice `# graph not initialized` — el grafo todavía no fue sembrado para esta campaña. **La inicialización del grafo es un requisito duro, no aplazable.** La regla de compresión del archivo de continuidad (paso 6 de abajo + `/dm:dnd save`) asume que graph.json está presente y es canónico para el estado relacional; aplazar la inicialización crea desvío del archivo de estado que se acumula sesión tras sesión. Corre el flujo de inicialización antes de entregar el resumen:

   1. **Detectá legado.** Una campaña es "legada" si alguna de: `Session count > 1` en el encabezado de state.md, O `## Continuity Archive` tiene al menos una entrada `### Session N`, O session-log.md tiene > 100 líneas. Una campaña recién creada con `/dm:dnd new` falla las tres señales — NO la clasifiques como legada.

   2. **Respaldá el directorio de campaña** (siempre — tanto fresca como legada):
      ```bash
      cp -R ~/.claude/dnd/campaigns/<nombre> \
            ~/.claude/dnd/campaigns/<nombre>.backup-$(date +%Y%m%d-%H%M%S)
      ```
      Decile al DM la ruta del respaldo explícitamente para que pueda revertir si hace falta.

   3. **Corre `/dm:dnd graph init <nombre>`** — propón nodos/edges semilla a partir de `npcs.md`, `world.md`, y `state.md` (Live State Flags + Active Quests + disposiciones recientes de PNJ). Mostrale al DM un único bloque de aprobación (conteos por tipo + entradas nombradas) y pide un solo sí/no. Después de la aprobación, ejecuta en lote las llamadas `add-node` y `add-edge`. Usá coincidencia `--since N` según cuándo cada nodo/edge se volvió canon (usa `1` para lo fundacional; el número de sesión real para PNJ/edges más nuevos).

   4. **Validá** con una consulta `scene-context` en la ubicación actual para confirmar que el subgrafo es alcanzable.

   5. **(Solo legado)** Ofrecé el paso único de compresión del Archivo de Continuidad:

      > "Esta campaña es legada ({session_count} sesiones, {archive_count} entradas de archivo). Ahora que `graph.json` es la fuente canónica para membresías de facción, disposiciones de PNJ, y relaciones tipadas, puedo hacer un paso único para recortar las entradas existentes de `## Continuity Archive` de reafirmaciones relacionales que el grafo ya responde. Los cambios mecánicos, beats de trama, momentos atmosféricos/de decisión, e información revelada se mantienen íntegros. Reducción estimada: 5–30% de los bytes del archivo (varía según qué tan relacionales vs. densas en contenido sean tus entradas existentes). El respaldo ya está en `<ruta-de-respaldo>`. ¿Continuamos? [s/n]"

      - `s` → recorta cada entrada del archivo quirúrgicamente; mantén la estructura de viñetas; elimina SOLO reafirmaciones puramente relacionales (ej. "X es aliado de Y", "Z vio las caras del grupo", "W es miembro de la facción F") que tengan un edge correspondiente en el grafo recién inicializado. Preservá: PX/nivel/objetos/PG, beats de trama ("Beat 2a sellado"), momentos atmosféricos, contenido revelado, material de calibración, eventos del mundo fuera de escena. Agregá una nota de una línea al principio de `## Continuity Archive`: *"Comprimido AAAA-MM-DD (paso de inicialización del grafo). El estado relacional es canónico en graph.json — las entradas de abajo preservan cambios mecánicos, beats de trama, contenido revelado, momentos atmosféricos/de decisión, y material de calibración."*
      - `n` → deja el archivo sin tocar. La regla de compresión a futuro (según `/dm:dnd save`) sigue aplicando a las entradas NUEVAS de esta sesión en adelante.

      Para campañas frescas (no legadas): saltea la oferta por completo — todavía no hay nada que comprimir, y la regla a futuro cubre todas las entradas futuras.

   6. Volvé a correr scene-context (ahora poblado). Después continúa al paso 6 (resumen).

8. Entregá un párrafo en personaje resumiendo la situación actual — dónde está el grupo, qué está en juego, qué pasaba por última vez.
9. Entrá en modo DM activo — no hace falta el prefijo `/dm:dnd` desde este punto.

---

## `/dm:dnd import <ruta-archivo> [nombre-campaña]`

Importá una campaña pre-escrita desde un archivo fuente (PDF, MD, TXT, DOCX) y crea una campaña jugable a partir de ella.

**Tipos de archivo soportados:** `.pdf` `.md` `.txt` `.markdown` `.docx`

### Paso 1 — Extraer texto fuente
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/import_campaign.py "<ruta-archivo>" --info
```
**Fuentes PDF:** la extracción usa PyMuPDF (con conciencia de columnas) para que los módulos multi-columna se de-columnicen en orden de lectura y se segmenten correctamente en capítulos — sin eso, los libros de dos columnas colapsan en un solo capítulo. Si el script imprime un aviso de `pip3 install pymupdf` en su stderr, decile al DM que lo instale y vuelva a correr; si no, cae de vuelta a `pdftotext` pero la segmentación es menos confiable.

Imprimí la info del archivo. Si el conteo de palabras supera 4000, fragmenta la fuente:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/import_campaign.py "<ruta-archivo>" --chunks  # total de fragmentos
python3 ${CLAUDE_SKILL_DIR}/scripts/import_campaign.py "<ruta-archivo>" --chunk 0  # primer fragmento
```
Para fuentes cortas (menos de 4000 palabras), lee completo:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/import_campaign.py "<ruta-archivo>"
```

### Paso 2 — Analizar la estructura
Leé el texto extraído e identifica:
- **Título de la campaña y sistema**
- **Tipo de estructura:** `linear` (cadena de escenas A→B→C) | `hub-and-spoke` (hub central + ubicaciones radiales, orden decidido por el jugador) | `faction-web` (ciudad/complejo multi-facción, arcos superpuestos)
- **Actos y capítulos** — secciones numeradas, encabezados de capítulo, o escenas nombradas
- **Beats clave** — eventos de historia obligatorios que el DM debe entregar (revelaciones de jefes, giros de facción, encuentros obligatorios)
- **Ubicaciones** — lugares distintos y nombrados con descripciones
- **PNJ** — nombres, roles, motivaciones, relaciones, bloques de estadísticas si están presentes
- **Facciones** — grupos con agendas, relaciones con el grupo
- **Ganchos y semillas de misión** — ganchos de aventura explícitos, misiones secundarias, encuentros opcionales
- **Condiciones iniciales** — dónde empieza el grupo, qué nivel, cuál es el evento incitador

Para fuentes largas, lee todos los fragmentos antes de continuar.

### Paso 3 — Confirmar nombre de campaña
Si no se proporcionó `[nombre-campaña]`, sugiere uno a partir del título y pide confirmación.

### Paso 4 — Mostrar resumen y confirmar
Mostrá un resumen estructurado antes de escribir ningún archivo:

```
Título:      <título de la fuente>
Tipo:        estructurada / <tipo de estructura>
Actos:       N  |  Capítulos: N  |  Beats clave: N
PNJ:         N nombrados  |  Facciones: N
Ubicaciones: N distintas

Nombre de campaña: <nombre>
Directorio:        ~/.claude/dnd/campaigns/<nombre>/

¿Continuamos? [s/n]
```

### Paso 5 — Crear archivos de campaña
Con la confirmación:

1. `mkdir -p ~/.claude/dnd/campaigns/<nombre>/characters`
2. Copiá las plantillas de `${CLAUDE_SKILL_DIR}/templates/`
3. Escribí **world.md** (núcleo de carga — se mantiene chico para poder leerse completo en cada carga):
   - `## World Foundations` — ambientación, geografía, tono, nivel de magia, calendario si está presente
   - `## Three Truths` — un asentamiento, una amenaza, un misterio (tomados de la fuente)
   - `## Threat Escalation Arc` — mapea los actos de la fuente a la tabla de 5 etapas; pon la etapa 1
   - `## Factions` — todas las facciones con arquetipo, actividad actual, relación con el grupo

3a. Escribí **world-nodes.md** (referencia perezosa — NO se lee al cargar, se trae según el acto actual):
   - `## Quest Seed Bank` — todos los ganchos explícitos + 2–3 hilos secundarios implícitos
   - `## Adventure Nodes` — ubicaciones nombradas con descripciones de una línea, agrupadas por acto/capítulo

   Para un módulo chico la separación es opcional, pero para cualquier aventura publicada es el
   ahorro más grande en tiempo de carga — todo el banco de misiones/ubicaciones ya no vive en
   contexto en cada sesión. Si escribes `world-nodes.md`, no dupliques sus
   secciones en `world.md`.

4. Escribí la tabla índice de **npcs.md** (una fila por PNJ: nombre, rol, ubicación, actitud en una línea)

5. Escribí **npcs-full.md** — entrada completa para cada PNJ nombrado:
   - Rol, motivación, secreto, tic de habla, afiliación de facción
   - Relaciones con otros PNJ (mín. 2 por PNJ)
   - Resumen de bloque de estadísticas si está presente en la fuente

6. Escribí **arc.md** a partir de `${CLAUDE_SKILL_DIR}/templates/arc.md` — el árbol **completo** de actos/capítulos: el `id`, `title`, `location`, `source_ref` (su archivo en el corpus perezoso, ver paso 6b), `key_beats`, `telegraph_scene`, `branching_notes` de cada capítulo, más `outstanding_beats` y `steering_notes`. Esta es la estructura pesada; vive acá para que se lea bajo demanda, no en cada carga.

6a. Escribí **state.md** a partir de la plantilla:
   - Poblá `## Current Situation` — ubicación inicial y placeholder de grupo
   - Poblá `## World State` — fecha en el mundo si se dio, facciones, etapa 1 del arco de amenaza
   - Poblá `## Campaign Arc` solo con el **PUNTERO DE ARCO ESTRUCTURADO** (ver plantilla): `type: structured`, `source`, `structure`, `arc_file: arc.md`, `current_act`, `current_chapter`, el bloque `current_chapter_detail`, `next_chapter`, `outstanding_beats`, `steering_notes`. **Borrá todo el bloque yaml de ARCO DINÁMICO** de la plantilla — no dejes las dos formas de arco en el archivo. El árbol completo está en arc.md; state.md solo lleva la ventana del capítulo actual + siguiente.
   - Dejá `## Active Quests`, `## Session Flags` (autosave en default activado), `## DM Style Notes` con los defaults de la plantilla

6b. Escribí el **corpus perezoso** — el texto fuente completo, disponible pero fuera del camino caliente:
   - `mkdir -p ~/.claude/dnd/campaigns/<nombre>/source`
   - Para cada capítulo en arc.md, escribe `source/<chapter-id>.md` (ej. `source/1.1.md`) con el texto fuente de ese capítulo a partir de los fragmentos extraídos. Usá los mismos ids de capítulo que arc.md.
   - Escribí **source-index.md** — una tabla que mapea `chapter-id → source/<id>.md → alcance en una línea`, más título de la fuente y fecha de importación.
   - Validá la disposición: `python3 ${CLAUDE_SKILL_DIR}/scripts/corpus_check.py --campaign <nombre>` (espera "lazy-corpus layout OK"). Arreglá cualquier problema de archivo huérfano/faltante antes de terminar. Si imprime una **ADVERTENCIA de capítulo sobredimensionado**, divide ese capítulo en subcapítulos (ej. `1.1a` / `1.1b` en cortes naturales de escena) en `arc.md`, `source-index.md`, y `source/`, y vuelve a correr — un solo capítulo gigante es lo único que todavía infla una carga, así que mantén cada `source/<id>.md` cómodamente bajo el límite.

7. Escribí **session-log.md** con el registro de importación de la Sesión 0:
   ```
   ## Session 0 — Import — <fecha>
   Source: <ruta-archivo>
   Imported: <N> actos, <N> capítulos, <N> PNJ, <N> ubicaciones
   ```

### Paso 6 — Asistente de completado de vacíos
Después de escribir los archivos, identifica cualquier cosa que la fuente dejó ambigua:
- Si no se especifica el nivel inicial → pregunta
- Si no se especifica el tamaño del grupo → pregunta
- Si falta calendario/fecha en el mundo → ofrece generarla o dejarla en blanco
- Si el tono no está claro en la fuente → ofrece el Asistente de Tono/Género

### Paso 7 — Confirmar y ofrecer el siguiente paso
Imprimí el resumen de archivos escritos. Ofrecé:
```
Campaña "<nombre>" creada a partir de <título de la fuente>.
→ /dm:dnd character new      — crea tu personaje
→ /dm:dnd load <nombre>      — empieza a jugar de inmediato
```

---

## `/dm:dnd save`
Escribí los eventos de la sesión en session-log.md, actualiza state.md (ubicación, misiones activas, PG/recursos del grupo, eventos recientes), actualiza cualquier characters/*.md que haya cambiado. Reflejá cada personaje actualizado en el roster global (`~/.claude/dnd/characters/<nombre>.md`).

**Seguimiento de Inspiración:** en cada save, registra el estado de Inspiración de cada PJ en `state.md → ## Current Situation → Party status`. Usá texto explícito: `Inspiration ✓` si la tiene, omitilo o `No Inspiration` si no. La Inspiración persiste entre sesiones y NO se limpia con descansos largos. Ejemplo: `Mara: HP 24/24. Inspiration ✓. Theo: HP 24/24.`

**Actualizá `## Live State Flags` en state.md en cada save.** Esta sección es el ancla resistente a compactación — contiene hechos que las prosas de resumen aplanan. Después de cada sesión, revisa y actualiza:
- **Tapadera:** la tapadera activa de cada PJ, su estado (INTACTA / DESCUBIERTA / PARCIAL), y el motivo en una línea. Eliminá tapaderas que ya no están activas.
- **Posturas de facción:** cada facción con postura no-neutral hacia el grupo. Formato: `[Facción]: [Allied/Friendly/Neutral/Suspicious/Hostile] — [motivo en una línea]`. Eliminá facciones que volvieron a neutral.
- **Disposiciones de PNJ:** cada PNJ con postura cambiada o notable. Formato: `[Nombre]: [disposición] — [motivo en una línea]`. Eliminá PNJ que volvieron a la línea base.

Si nada cambió en una categoría esta sesión, dejala como está. Si un hecho estaba mal en el save anterior, corregilo.

**Campañas estructuradas (importadas) — mantén sincronizados la ventana del arco y arc.md.** Avanzar el puntero no es contabilidad opcional — es lo que mantiene a la campaña en sus propios rieles, y un puntero que nunca se mueve es cómo un módulo importado se convierte en silencio en uno improvisado. Antes de decidir "no avanzó ningún capítulo", chequea honestamente: **si esta sesión vació el resto de los `outstanding_beats` del capítulo actual, o el grupo claramente se movió a la ubicación o situación del siguiente capítulo, el capítulo avanzó — tratalo como tal y mueves el puntero ahora.** Cuando un capítulo avanza: marca el capítulo completado como `status: complete` en `arc.md`, pon el nuevo capítulo como `status: current`, y actualiza `state.md → ## Campaign Arc` para que su `current_chapter`, `current_chapter_detail`, `next_chapter`, y `outstanding_beats` reflejen la nueva ventana. El árbol completo se queda en `arc.md`; `state.md` solo lleva el capítulo actual + siguiente para que la carga se mantenga liviana. Solo cuando el grupo genuinamente sigue a mitad de capítulo, actualiza `outstanding_beats`/`steering_notes` inline en `state.md` — sin necesidad de tocar `arc.md`. (Las campañas dinámicas/sandbox no tienen `arc.md`; actualiza el arco inline en `state.md` como antes.)

Después actualiza `## Faction Moves` en state.md: para cada facción activa, responde *"¿qué hicieron mientras el grupo estaba ocupado?"* Una línea por facción — incluso si todavía no hay nada visible. Confirmá qué se escribió.

**Archivo de cola de sesión (session tail):** `dnd-display-app.py` escribe continuamente `~/.claude/dnd/campaigns/<nombre>/session_tail.json` — ruta específica de la campaña, escritura atómica, protegida contra vaciado (desde 2026-05-01). Al momento del save:

1. Verificá que el archivo del lado de la campaña exista y no esté vacío:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/display/verify_tail.sh <nombre-campaña>
   ```
   El script devuelve 0 si la cola está sana (lista JSON no vacía y válida), 1 si falta/está vacía/corrupta. Si devuelve 1, la cola no es segura para confiar en ella en la repetición de la próxima sesión — **escribe un reemplazo canónico directamente en la ruta de la campaña** con los 5–8 beats narrativos más importantes de esta sesión como una lista JSON de entradas `{"text": "...", "_camp": "<nombre>"}` (no hace falta llamar al display; puede que ya esté muerto). Usá el helper `${CLAUDE_SKILL_DIR}/display/write_canonical_tail.py`.
2. También escribe `~/.claude/dnd/campaigns/<nombre>/session-tail.md` (instantánea legible por humanos — acompaña al JSON, se usa como fallback durante /dm:dnd load si falla la lectura del JSON).

**Archivado del log de sesión (correr en cada save después de que el contador de sesión > 3):**
session-log.md mantiene solo las **2 entradas de sesión completas más recientes**. Las entradas más viejas se mueven a session-log-archive.md (agregar, nunca borrar). Antes de archivar cada entrada, extrae un resumen de continuidad de 3–5 viñetas y escribilo en `## Continuity Archive` en state.md. Formato:

```markdown
### Session N — [fecha] — [ubicación/evento en una línea]
- [Hecho clave que puede resurgir como referencia]
- [Revelación de PNJ, redacción exacta de algo importante, decisión con consecuencias]
- [Resultado de tirada que cambió la ficción]
- [Objeto adquirido con significado narrativo, beat de trama, momento atmosférico/de decisión]
```

**Regla de compresión a futuro del Archivo de Continuidad (desde 2026-05-07; aplica cuando `graph.json` existe para la campaña):** Cuando `graph.json` está presente, las viñetas del Archivo de Continuidad NO deben reafirmar estado relacional que el grafo ya guarda de forma canónica. Específicamente, **omite** viñetas/cláusulas que digan:
- "X es aliado de Y" / "X es hostil a Y" / "X es amistoso con Y" — ya es un edge tipado con `--since N` y ancla de fuente
- "X es miembro de la facción F" / "X trabaja para Y" / "X le reporta a Y" — ya es un edge `member_of` / `works_for` / `reports_on`
- "Z vio las caras del grupo" / "K ahora está en el perfil de los Kept" — ya es un edge `hostile_to` / `surveils` con `--since`
- Membresías de facción y disposiciones de PNJ que no cambiaron esta sesión
- Perfiles de PNJ reafirmados (cargo, edad, ubicación) que ya viven como tags de nodo + resumen

**Mantené** en las viñetas del archivo:
- Cambios mecánicos (PX otorgados, subidas de nivel, objetos ganados/gastados, espacios consumidos, deltas de PG al final de sesión)
- Beats de trama (finalizaciones de beat de arco, "Beat 2a sellado", "Beat 2b ATERRIZÓ")
- Momentos atmosféricos / de decisión sin edge en el grafo ("Mira comió el pan — primera comida en 800 años", "Mara le apretó la mano")
- Contenido revelado (el QUÉ se aprendió — "fragmento / ancla / huésped", "tres factores de aceleración") incluso cuando el hecho relacional está en el grafo
- Eventos del mundo fuera de escena / movimientos de facción
- Calibración / Notas del DM
- Cliffhangers y puntos de pausa

Tratá cada viñeta como una oración con un solo trabajo. Si el único trabajo es "reafirmar un edge del grafo", eliminala. Si lleva contenido + edge, quedate con la mitad de contenido. El grafo se consulta en el paso 5 de `/dm:dnd load`; el archivo se consulta para narrativa cronológica + estado mecánico — no deberían superponerse.

El resumen de continuidad es lo que se mantiene presente en contexto. El log verboso completo está en el archivo, legible en `/dm:dnd recap` o bajo pedido explícito. Cuando un detalle pasado resurge a mitad de escena, chequea primero `## Continuity Archive`, después `/dm:dnd graph scene-context` para contexto relacional, y después lee session-log-archive.md si hace falta más profundidad.

**Barrido de cambios de relación del grafo de campaña:** antes de terminar el save, escanea la narración de esta sesión buscando cambios de relación que no se capturaron en vivo vía `/dm:dnd graph add-edge` / `close-edge`. Buscá momentos que coincidan con estos patrones:

- Nueva alianza, traición, o rivalidad entre PNJ/facciones nombrados ("Velkyn ahora sirve a la Corte Pálida")
- Un cambio en cómo el **grupo** se posiciona hacia un PNJ o facción ("la Corte Pálida ahora ve al grupo como hostil", "Aldric cambió de parecer y confía en ellos"). Redactá esto como llamadas `set-disposition --to <pnj-o-facción> --level <allied/friendly/neutral/suspicious/hostile>`, coincidiendo con el `standing` que envías al display y las líneas de disposición de PNJ en `## Live State Flags`.
- Un PNJ que se muda a / se va de una ubicación ("Mira huyó de la Ciudadela hacia el Bajomercado")
- Una facción que toma control de (o pierde) un lugar ("La Casa Tarn perdió la mina de plata")
- Un personaje que aprende un secreto ("el grupo ahora sabe que Velkyn era el espía")
- Un hilo/misión que termina o queda bloqueado

Para cada candidato, redacta una llamada `add-edge` o `close-edge`. Después **presentale el lote al DM como una lista numerada** y pregunta: *"¿Aplico todo? [s / elegir / omitir]"*

- `s` → corre todas las llamadas propuestas vía `python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py ...`
- `elegir` → el DM nombra los números a aplicar (ej. `1, 3, 5`); saltea el resto
- `omitir` → no apliques ninguna

Siempre proporciona `--since <sesión-N-actual>` de state.md. Nunca escribas edges propuestos en silencio.

Si `graph.json` todavía no existe para esta campaña, saltea el barrido por completo (sin bloque de propuesta) — el grafo no está sembrado.

---

## `/dm:dnd end`
1. Corre `/dm:dnd save`, después:
   a. Agregá el bloque **Session Recap** a session-log.md con eventos clave e hilos abiertos.
   b. Preguntá: *"Calibración rápida — ¿qué funcionó esta sesión, y qué ajustarías la próxima vez?"* Escribí las respuestas en `### DM Calibration`. Si se saltea, dejalo en blanco.
   c. Actualizá `## World State` en state.md: chequea si los eventos avanzaron la etapa del arco de amenaza, cambiaron estados de facción, o cambiaron la fecha en el mundo. Actualizá los tres.
   d. Si la respuesta de calibración revela un patrón nuevo (o confirma/contradice uno existente), actualiza `## DM Style Notes` en state.md. Agregá viñetas nuevas; refina las existentes si el patrón se afinó. No registres cada sesión — solo actualiza cuando se observa algo genuinamente nuevo o cambiado.
   e. **Chequeo de arco** (solo arcos dinámicos — saltea para sandbox/estructurada): Si `## Campaign Arc` tiene `type: dynamic`, haz todo esto:

      i. Preguntá: *"¿Aterrizó algún beat de arco esta sesión? [id(s) de beat como '1b 2a', o 'ninguno']"*
      ii. Si aterrizaron beats: corre `/dm:dnd arc advance <beat-id>` para cada uno.
      iii. **Chequeo de adelantamiento (crítico — agregado 2026-05-01):** para cada beat pendiente restante cuyo `world_pressure` se entregó visiblemente esta sesión (el evento del mundo nombrado en el beat efectivamente apareció en la narración o en Faction Moves), evalúa si la consecuencia `what_changes` del beat TAMBIÉN aterrizó. Tres estados posibles:
        - **Aterrizó limpiamente** → marca el beat completo (paso ii).
        - **No aterrizó — la presión se absorbió sin consecuencia** → el beat está vencido y su forma actual ya no encaja. **Corre `/dm:dnd arc revise` de inmediato**; no te limites a actualizar `steering_notes`. El `what_changes` del beat tenía forma de evento (algo específico pasa) cuando debería tener forma de consecuencia (algo fundamentalmente distinto es verdad) — revisa tanto `what_changes` como `world_pressure` para que encajen en un camino que SÍ aterrice. La forma comprometida se dobla; no se rompe.
        - **La presión todavía no se entregó** → deja el beat en paz; se espera que se entregue la próxima sesión.
      iv. Actualizá `steering_notes` para el próximo beat pendiente con la *forma de consecuencia* esperada, no el evento específico.
   f. **Verificación de la cola (agregado 2026-05-01):** antes de matar el display, verifica que el `session_tail.json` del lado de la campaña esté sano:
      ```bash
      bash ${CLAUDE_SKILL_DIR}/display/verify_tail.sh <nombre-campaña>
      ```
      Salida 0 = sano. Salida 1 = falta/vacío/corrupto → escribe un reemplazo canónico en `~/.claude/dnd/campaigns/<nombre>/session_tail.json` a partir del contexto de sesión (5–8 entradas, cada una `{"text": "...", "_camp": "<nombre>"}`) ANTES de matar el display — una vez que el display está muerto, solo importa el archivo. El propio `_persist_tail` del display tiene protecciones de vaciado + escritura atómica, pero el respaldo asegura que el peor caso de estado de archivo sea imposible.
2. Detené el display (siempre — incluso si `_display_running` no estaba claro):
   ```bash
   kill $(cat ${CLAUDE_SKILL_DIR}/display/app.pid 2>/dev/null) 2>/dev/null
   rm -f ${CLAUDE_SKILL_DIR}/display/app.pid
   ```
3. **Re-verificación de la cola post-cierre:** corre `verify_tail.sh` una vez más después del kill. Si ahora reporta no-sano (el archivo se truncó por una condición de carrera en una escritura final), restaura desde la versión canónica escrita en el paso 1f.

---

## `/dm:dnd abandon`

Salí de la sesión actual **sin guardar ningún cambio de estado**. Usalo cuando ocurrió un error y quieres descartar todo desde el último `/dm:dnd save` (o desde la carga, si la sesión nunca se guardó).

1. Confirmá: *"¿Abandonar la sesión? Se van a perder todos los cambios de estado sin guardar. Escribí 'sí' para confirmar."* — no continúes hasta confirmar.
2. NO escribas en state.md, world.md, npcs.md, session-log.md, ni en ningún archivo de personaje.
3. Limpiá el flag de autorun en memoria (`autorun: false`) para que el loop de espera no vuelva a arrancar.
4. Si `_display_running = true`, detén el display:
   ```bash
   kill $(cat ${CLAUDE_SKILL_DIR}/display/app.pid 2>/dev/null) 2>/dev/null
   rm -f ${CLAUDE_SKILL_DIR}/display/app.pid
   ```
5. Confirmá: *"Sesión abandonada. No se escribió ningún archivo. Corre `/dm:dnd load <campaña>` para recargar desde el último estado guardado."*

---

## `/dm:dnd data [sync|status]`
- `sync` → `python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py` — chequea los SHA upstream (5e-bits + FoundryVTT) y reconstruye `dnd5e_srd.json` solo si alguna de las fuentes tiene commits nuevos
- `sync --force` → `python3 ${CLAUDE_SKILL_DIR}/scripts/sync_srd.py --force` — reconstruye sin importar qué
- `sync --check` → chequea el upstream sin reconstruir
- `status` → `python3 ${CLAUDE_SKILL_DIR}/scripts/build_srd.py --status` — muestra los metadatos actuales del dataset

El dataset viene incluido en `${CLAUDE_SKILL_DIR}/data/dnd5e_srd.json` (1453 registros: hechizos, equipo, objetos mágicos, condiciones, monstruos, rasgos de clase). No hace falta descarga en tiempo de ejecución. Corre `sync` solo cuando quieras traer contenido nuevo del upstream.

---

## `/dm:dnd path [<nueva-ruta> | reset]`

Ver o configurar dónde se guardan los datos de campaña y personaje. Envuelve la
variable de entorno `DND_CAMPAIGN_ROOT`.

- Sin argumentos → `python3 ${CLAUDE_SKILL_DIR}/scripts/path_config.py` y mostrar la salida.
- Nueva ruta → `python3 ${CLAUDE_SKILL_DIR}/scripts/path_config.py set <ruta>`. Confirmale al usuario, después recordale que el cambio solo tiene efecto en shells nuevas (o después de que hagan `source` de su rc en macOS/Linux).
- `reset` → `python3 ${CLAUDE_SKILL_DIR}/scripts/path_config.py reset`.

La persistencia es vía rc de shell en macOS/Linux y vía `setx` en Windows. Las campañas existentes no se migran automáticamente; `paths.find_campaign()` maneja el fallback legado + copia-al-acceder.

---

## `/dm:dnd update [--check]`

Trae los últimos cambios del skill desde `origin/main`.

- Sin argumentos → `python3 ${CLAUDE_SKILL_DIR}/scripts/update_skill.py` y mostrar la salida en streaming (el script pregunta antes de hacer pull).
- `--check` → `python3 ${CLAUDE_SKILL_DIR}/scripts/update_skill.py --check` — reporta el estado sin hacer pull.
- El script se niega a actualizar si el árbol de trabajo está sucio y usa `--ff-only` para nunca fusionar historia divergente en silencio.
- Después de un pull exitoso, recordale al usuario que reinicie Claude Code para que se recarguen el nuevo `SKILL.md` y `SKILL-commands.md`.

---

## `/dm:dnd display [start|stop|status]`
- `start` → pregunta modo LAN [s/n]; corre `bash ${CLAUDE_SKILL_DIR}/display/start-display.sh [--lan]`; imprime la(s) URL(s)
- `stop` → `kill $(cat ${CLAUDE_SKILL_DIR}/display/app.pid) 2>/dev/null && rm -f ${CLAUDE_SKILL_DIR}/display/app.pid`
- `status` → `curl -sk $(cat ${CLAUDE_SKILL_DIR}/display/.scheme 2>/dev/null || echo http)://localhost:5001/ping` — alcanzable o no alcanzable
- Sin argumento → imprime instrucciones rápidas de inicio

---

## `/dm:dnd list`
Leé `~/.claude/dnd/campaigns/*/state.md`, imprime una tabla resumen: nombre de campaña | fecha de última sesión | contador de sesiones.

---

## `/dm:dnd character new [nombre-campaña]`

**Primero lee el reglamento de la campaña** — `python3 ${CLAUDE_SKILL_DIR}/scripts/paths.py` no es un CLI; en su lugar, lee inline con:

```bash
python3 -c "import sys; sys.path.insert(0,'${CLAUDE_SKILL_DIR}/scripts'); from paths import campaign_ruleset; print(campaign_ruleset('<campaña>'))"
```

El resultado guía la ramificación en los pasos 1 (fuente de ASI), 4 (dote de origen), y 5 (momento de la subclase). El default `2014` aplica para campañas legadas anteriores al campo de reglamento.

**Primero, ofrece los dos caminos de construcción — llama a `AskUserQuestion`:** *"¿Cómo quieres construir [o: tu personaje]?"*
- `Paso a paso` → el flujo guiado de abajo (pasos 1–10). Usalo cuando el jugador quiere hacer cada elección deliberadamente, o ya sabe la construcción exacta.
- `Describilo` → el camino de prosa (paso 0 abajo). Usalo cuando el jugador prefiere decir quién es el personaje en una oración y dejar que armes una hoja legal.

Default a `Paso a paso` si se descarta la pregunta. Los dos caminos terminan en la misma hoja y corren la misma validación, cálculo, y pasos de escritura — la única diferencia es cómo se recolectan las elecciones.

0. **Camino de descripción.** Hacé una pregunta abierta: *"En una o dos oraciones, describe tu personaje — quién es, cómo pelea o resuelve problemas, de dónde viene. Voy a construir una hoja de 5e legal y de nivel apropiado a partir de eso y te la muestro antes de escribir nada."* Después:

   a. **Derivá la construcción de la prosa, del lado del modelo.** Mapeá la descripción a un chasis de 5e legal para el reglamento de esta campaña: **clase** (y, si el nivel lo justifica, subclase según el momento del reglamento — ver paso 5), **especie/raza**, **trasfondo**, prioridades de puntuación de característica (qué dos o tres puntuaciones favorece el concepto), competencias de habilidad/herramienta que otorgan la clase+trasfondo, un estilo de combate o conjuros iniciales si la clase los tiene, y un **Pilar de Personaje** de una línea (Vínculo / Defecto / Ideal / Objetivo — el mismo campo que completa el paso 2). Leé la descripción buscando lo que al jugador realmente le importa — un "guardia del templo deshonrado que habla para salir de las peleas" es un Paladín o Clérigo con trasfondo de Soldado/Acólito y prioridad CAR/CON, no una elección genérica. Nunca inventes un detalle que la prosa contradiga; donde la prosa no dice nada, elige la opción legal que más encaje con el concepto y anotalo como una elección, no como un hecho.

   b. **Validá la legalidad en 5e antes de mostrar nada.** La hoja derivada debe ser legal para el reglamento de la campaña y el nivel inicial acordado: clase/especie/trasfondo existen en 5e (SRD o una fuente que la mesa permita — busca cualquier cosa de la que no estés seguro vía `lookup.py`), las puntuaciones de característica vienen de un método legal (tirada o compra por puntos — paso 3), la fuente de ASI coincide con el reglamento (raza en 2014, trasfondo + una dote de origen en 2024 — paso 1), las competencias efectivamente las otorgan la clase+trasfondo elegidos (sin duplicados, sin elecciones fuera de lista), y cualquier hechizo/rasgo está disponible a este nivel. Si el concepto implica algo ilegal (un personaje de nivel 1 con un rasgo tope, una subclase antes de lo que el reglamento permite), elige el equivalente legal más cercano y decilo.

   c. **Presentá la hoja derivada para una sola confirmación.** Mostrá la construcción completa — especie/raza, clase (+ subclase si aplica), trasfondo, arreglo de característica con las prioridades del concepto asignadas, competencias, kit inicial, y el Pilar derivado con su oración fuente — y pregunta: *"Esto es lo que leí de tu descripción. ¿Cambiás algo, o la armo?"* Dejá que el jugador ajuste cualquier campo en prosa; re-valida después de cualquier cambio.

   d. **Converge en el flujo compartido.** Con la confirmación, corre el chequeo de unicidad de nombre (`name_registry.py check` del paso 1), después continúa en el **paso 3** (finalizar puntuaciones de característica — reusando las prioridades derivadas), **paso 4** (bonos raciales/de trasfondo + `character.py calc`), y pasos 6–10 (equipo, escritura, reflejo en roster, constructor suplementario). No re-preguntes lo que el paso a paso ya respondió con la descripción; completa solo los vacíos genuinos.

1. Preguntá: nombre, **especie** (2024) o **raza** (2014), clase, trasfondo.

   **Chequeo de unicidad de nombre:** corre `python3 ${CLAUDE_SKILL_DIR}/scripts/name_registry.py check "<nombre>"`. Código de salida 1 (duplicado) → muestra el uso previo; el jugador confirma o cambia. Registrá después del paso 9.

   **2014 (raza-como-ASI):** la especie/raza otorga los aumentos de puntuación de característica (ej. Elfo del Bosque: +2 DES, +1 SAB). Aplicá a las características en el paso 4.
   **2024 (trasfondo-como-ASI):** el **trasfondo** otorga el aumento de puntuación de característica +2/+1 O tres +1, Y una **Dote de Origen** gratis (ej. Iniciado en Magia, Suerte, Resistente). La especie otorga rasgos pero no puntuaciones de característica. Los jugadores en 2024 deben elegir el trasfondo ANTES de tirar las características — el patrón de ASI del trasfondo determina qué puntuaciones se benefician.
2. Preguntá: *"En una oración, ¿qué debería saber el DM sobre [Nombre]?"*
   - Si se responde: deriva UN pilar — **Vínculo**, **Defecto**, **Ideal**, o **Objetivo** (el que mejor encaje). Guardá tanto la oración cruda como el pilar derivado en `## Character Pillar`.
   - Si se saltea: deja `## Character Pillar` en blanco. No inventes uno. No vuelvas a preguntar.
3. Preguntá: tirada o compra por puntos
   - Tirada → `ability-scores.py roll`, presenta 3 arreglos, el jugador asigna
   - Compra por puntos → `ability-scores.py pointbuy --check <puntuaciones>` para validar
4. Aplicá los bonos raciales. Corre `character.py calc` para derivar todas las estadísticas secundarias.
5. Preguntá: Estilo de Combate (Guerrero/Paladín/Explorador), hechizos (si es lanzador)
6. Asigná el equipo inicial según clase + trasfondo
7. Escribí en `characters/<nombre>.md` usando `templates/character-sheet.md`; pon `## Campaign History → Origin campaign`
8. Agregá a la línea de grupo en `state.md`
9. Reflejá en el roster global: `cp characters/<nombre>.md ~/.claude/dnd/characters/<nombre>.md`
10. Corre el constructor suplementario para traer cualquier hechizo/rasgo no-SRD que use el personaje:
    ```bash
    python3 ${CLAUDE_SKILL_DIR}/scripts/build_supplemental.py --character ~/.claude/dnd/campaigns/<nombre>/characters/<nombrepj>.md
    ```
    Esto escanea el archivo de personaje buscando hechizos y rasgos que no están en la SRD y trae descripciones de dnd5e.wikidot.com hacia `dnd5e_supplemental.json`. Se saltea cualquier entrada ya presente. Seguro de volver a correr.

---

## `/dm:dnd character sheet [nombre]`
Leé `characters/<nombre>.md`, mostralo limpio. Si se omite el nombre y existe un solo personaje, muestra ese.

---

## `/dm:dnd character import <nombre> [from:<campaña>]`
1. Encuentra la hoja de personaje: si se especifica `from:<campaña>` → los characters/ de esa campaña; si no, chequea el roster global `~/.claude/dnd/characters/<nombre>.md`; si ninguno → busca en todas las campañas, lista coincidencias, pregunta.
2. Mostrá un resumen (nivel, PX, PG, inventario clave) y pregunta: *"¿Importar al nivel actual [X], o subir de nivel antes de empezar?"*
   - Tal cual → copia directamente; Subir de nivel primero → corre `/dm:dnd level up` en la hoja fuente
3. Copiá a `characters/<nombre>.md` de la campaña actual. Actualizá: Campaign, Last Updated, Previous campaigns, Death Saves (reset).
4. Opcionalmente pregunta sobre ajustes de equipo para la nueva ambientación.
5. Agregá a la línea de grupo en `state.md`. Actualizá el roster global.
6. Corre el constructor suplementario para cualquier entrada no-SRD:
    ```bash
    python3 ${CLAUDE_SKILL_DIR}/scripts/build_supplemental.py --character ~/.claude/dnd/campaigns/<nombre>/characters/<nombrepj>.md
    ```
7. Entregá un párrafo en personaje — ¿cómo se siente entrar a un mundo nuevo?

---

## `/dm:dnd level up [nombre]`
1. **Chequeo de PX — primero:**

   | Nivel | PX requeridos | Nivel | PX requeridos |
   |-------|-------------|-------|-------------|
   | 2 | 300 | 11 | 85,000 |
   | 3 | 900 | 12 | 100,000 |
   | 4 | 2,700 | 13 | 120,000 |
   | 5 | 6,500 | 14 | 140,000 |
   | 6 | 14,000 | 15 | 165,000 |
   | 7 | 23,000 | 16 | 195,000 |
   | 8 | 34,000 | 17 | 225,000 |
   | 9 | 48,000 | 18 | 265,000 |
   | 10 | 64,000 | 19 | 305,000 |
   |    |         | 20 | 355,000 |

   PX insuficientes → reporta el déficit y parate. Continuá solo con anulación explícita del DM.
2. Leé la hoja. Corre `character.py levelup`. Aplicá los rasgos de clase. Preguntá por tirada de PG o promedio. Actualizá la hoja + roster global. Narrá el crecimiento.

   **Momento de subclase según reglamento (agregado 2026-05-08):** lee el reglamento de la campaña vía `paths.campaign_ruleset(<campaña>)`.
   - **2014:** La selección de subclase pasa en el nivel especificado por la clase (Clérigo/Hechicero/Brujo en el 1; Druida/Mago en el 2; la mayoría del resto en el 3).
   - **2024:** La selección de subclase se unifica en el **nivel 3** para TODAS las clases. Si el jugador está llegando al nivel 3 en una campaña 2024 y todavía no eligió subclase, preguntale. Los rasgos de clase que en 2014 iban en el nivel 1 (ej. Dominio del Clérigo) pasan al nivel 3 en 2024.

   **Maestría de Armas (solo 2024):** Guerrero/Bárbaro/Paladín/Explorador ganan Maestría de Armas en el nivel 1 (el Guerrero conoce 3 propiedades de maestría; los demás conocen 2). Registrá qué propiedades conoce el personaje en la hoja bajo `## Class Features → Weapon Mastery: <lista>`. Las propiedades se eligen entre las ocho de `data/dnd5e_srd_2024.json → weapon_mastery_properties`. El personaje solo puede usar la maestría con armas que tengan la propiedad correspondiente (busca en `data/dnd5e_srd_2024.json → equipment[…].mastery`).

---

## `/dm:dnd npc [nombre]`
- Existente → lee la entrada completa de npcs-full.md (busca por nombre), interpretalo con voz/tic
- Nuevo → genera la entrada completa: rol, estadísticas apropiadas al CR, actitud, motivación, secreto, tic de habla, facción (o "independiente"), objetivo actual, horario, los cuatro ejes de personalidad, ≥2 relaciones con PNJ existentes. Actitud por defecto neutral. Agregá la entrada completa a npcs-full.md; agrega una fila resumen de una línea al índice de npcs.md.

  **Chequeo de unicidad de nombre (agregado 2026-05-07):** antes de generar, corre `python3 ${CLAUDE_SKILL_DIR}/scripts/name_registry.py check "<nombre-propuesto>"`. Si es duplicado (código de salida 1), mostrale al DM el uso previo y ofrece: (a) continuar con el duplicado (algunos escenarios quieren nombres recurrentes — una referencia a Voss puede ser deliberada); o (b) regenerar con un nombre distinto. Cualquiera sea el camino elegido, después de que el PNJ se agregue a npcs.md / npcs-full.md, llama a `name_registry.py add --name "<nombre>" --type npc --campaign <nombre> --session <actual>` para registrar la entrada.

  Cuando **/dm:dnd new** genera un lote de PNJ durante la generación de mundo, corre el chequeo en cada nombre generado dentro del mismo loop: si es duplicado, regenera ese nombre (vuelve a pedirle al LLM con el nombre previo agregado a una lista de exclusión "no-elegir"). Después de que termine la generación de mundo, llama a `name_registry.py add` en lote para cada PNJ aceptado.

## `/dm:dnd npc attitude <nombre> <cambio>`
Encuentra al PNJ en npcs.md, cambia la actitud un paso (hostile → unfriendly → neutral → friendly → allied), registra motivo y fecha.

## `/dm:dnd npc rename "Nombre Viejo" <"Nombre Nuevo" | random> [flags]`
Renombrá a un personaje en toda una campaña — `npcs.md`, `npcs-full.md`, `state.md` (todas las secciones), `session-log.md`, `graph.json` (nodo + edges preservados), y `characters/<slug>.md` si `--type pc`. Respalda la campaña primero.

Mapea a: `python3 ${CLAUDE_SKILL_DIR}/scripts/npc_rename.py --campaign <actual> --old "..." --new "..." [flags]`. Usa la campaña actualmente cargada por defecto; para uso con campaña explícita, pasa `--campaign <nombre>` directamente.

Flags:
- `--random` — elige un nombre del corpus de nombres de fantasía incluido (~4800 combinaciones únicas) que no esté ya en `~/.claude/dnd/.name_registry.json`. Mutuamente excluyente con "Nombre Nuevo" explícito.
- `--type npc | pc` (default `npc`) — `pc` también mueve el archivo de personaje y actualiza el roster global.
- `--dry-run` — muestra todas las coincidencias en todos los archivos sin escribir. Correlo siempre primero como chequeo de cordura.
- `--yes` — se salta el prompt de confirmación.
- `--include-archive` — también renombra en `session-log-archive.md`. **El default es dejar el archivo intacto** por precisión histórica y agregar una nota de auditoría de una línea al principio: *"`<viejo>` renombrado a `<nuevo>` en S<N>; las entradas históricas de abajo preservan el nombre original."*

El script siempre respalda la campaña en `<nombre>.backup-rename-<slug-viejo>-AAAAMMDD-HHMMSS/` antes de cualquier escritura. El comando para revertir se imprime al final.

Después del renombrado, se actualiza el registro de nombres: el nombre viejo se marca `retired_from` esta campaña con `replaced_by` apuntando al nuevo slug; el nombre nuevo se agrega con la sesión actual de esta campaña como `first_session`.

## `/dm:dnd registry <subcomando>`
Ver y gestionar el registro de nombres cruzado entre campañas en `~/.claude/dnd/.name_registry.json`. Usado por `/dm:dnd npc rename --random` para nunca reusar un nombre y (en un desarrollo futuro) por `/dm:dnd new` / `/dm:dnd character new` / `/dm:dnd npc <nuevo>` para marcar duplicados en el momento de la creación.

Mapea a: `python3 ${CLAUDE_SKILL_DIR}/scripts/name_registry.py <subcomando> [args]`.

- `/dm:dnd registry rebuild [--include-prose]` — escanea `npcs.md`, `npcs-full.md`, `characters/*.md`, y `graph.json` (nombres de nodo) de cada campaña; reconstruye el registro desde las fuentes canónicas. Preserva cualquier historial `retired_from` existente. Corre una vez al instalar, después ad hoc cuando quieras.

  **`--include-prose` (agregado 2026-05-07, opt-in):** también escanea session-log.md y session-log-archive.md buscando secuencias capitalizadas de 2-3 palabras (patrones de probable nombre). Se filtra contra una lista de palabras vacías (lugares, facciones, palabras de mecánica como "Theo Stealth", comienzos de oración) pero **la extracción basada en regex es inherentemente ruidosa** — típicamente 5-15x más entradas que las canónicas, con quizás 10-20% de aciertos reales. Etiquetado `source: prose` para distinguirlo; consulta con `/dm:dnd registry list --source prose` para revisar y podar manualmente. Para extracción de prosa de alta calidad, el paso futuro es con LLM (parecido a `/dm:dnd graph extract`).

- `/dm:dnd registry list [--campaign C] [--type npc|pc] [--source canonical|prose]` — imprime todas las entradas del registro; filtra por campaña-actualmente-activa, tipo, o fuente.
- `/dm:dnd registry lookup <nombre>` — búsqueda sin distinción de mayúsculas; imprime la entrada completa como JSON.
- `/dm:dnd registry check <nombre> [--json]` — chequea si un nombre propuesto choca con el registro. Código de salida 0 si es único, 1 si es duplicado. La severidad (`warn` por default, `strict` opt-in vía `<DND_CAMPAIGN_ROOT>/.name_registry_config.json`) controla si los duplicados se reportan como advertencias o rechazos duros. Usado por los procedimientos de `/dm:dnd new`, `/dm:dnd character new`, `/dm:dnd npc <nuevo>`.
- `/dm:dnd registry add --name N --type npc|pc --campaign C --session N` — registra una entrada nueva manualmente (se llama automáticamente desde `/dm:dnd npc rename` y los ganchos de unicidad al momento de creación).
- `/dm:dnd registry retire --name N --campaign C [--replaced-by NUEVO]` — marca un nombre como ya no activo en una campaña (se llama automáticamente desde `/dm:dnd npc rename`).

Por defecto, el registro captura personajes **canónicos** (los que están en `npcs.md` / `npcs-full.md` / `characters/` / nombres de nodo de graph.json). Los nombres que aparecen solo en prosa de session-log (menciones puntuales, PNJ desechables, etiquetas de chequeo de habilidad) NO se registran por defecto — es deliberado, para evitar prohibir nombres comunes por uso incidental. El flag `--include-prose` es opt-in para usuarios que quieran la vista más amplia (y más ruidosa).

**Configuración de severidad:** crea `~/.claude/dnd/.name_registry_config.json` con `{"severity": "strict"}` para que todas las detecciones de duplicado rechacen por defecto en vez de advertir-y-permitir. Poné `"none"` para desactivar los chequeos por completo (el rebuild y el rename del registro siguen funcionando).

---

## `/dm:dnd characters`
Lista todos los personajes en el roster global (`~/.claude/dnd/characters/`). Muestra: nombre, raza/clase/nivel, campaña de origen, campañas previas, última actualización.

---

## `/dm:dnd roll <notación>`
Corre `scripts/dice.py <notación>`. Mostrá la salida tal cual. Ejemplos: `d20`, `2d6+3`, `d20 adv`, `4d6kh3`.

---

## `/dm:dnd combat start`
1. Identificá a los combatientes; recolecta nombre, mod de DES, PG, CA, tipo (pc/npc) de cada uno.
2. Corre `combat.py init '<JSON>'` — tira iniciativa automáticamente para cada combatiente incluidos los PJ. Mostrá el tracker y el desglose de tirada de cada combatiente.
3. Enviá la iniciativa al display:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/display/send.py << 'DNDEND'
   ⚔️ Iniciativa — Ronda 1
   [Nombre]: d20(N) + DES = total
   Orden de turno: [Nombre] → [Nombre] → ...
   DNDEND
   ```
4. Enviá el orden de turno a la barra lateral de stats:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-order '{"order":[...],"current":"PrimerNombre","round":1}'
   ```
5. Guardá STATE_JSON en `state.md` bajo `## Active Combat`.
6. Andá turno por turno usando la secuencia por turno (en SKILL.md, Modo DM Activo).
7. Al terminar el combate: actualiza PG en las hojas de personaje, limpia `## Active Combat`, `push_stats.py --turn-clear`, narra las secuelas, envía el resumen de PX, corre `tracker.py -c <campaña> clear`.

**Los PX otorgados** van en el envío final al display:
```bash
python3 ${CLAUDE_SKILL_DIR}/display/send.py << 'DNDEND'
[narración de las secuelas del combate]

⭐ PX Otorgados
- [Enemigo] derrotado: N PX
- [Objetivo] completado: N PX
- Total: N PX ÷ [jugadores] = N PX cada uno
- [Nombre]: N / 300 PX | [Nombre]: N / 300 PX
DNDEND
```

---

## `/dm:dnd rest <short|long>`
**Corto (1 hora):**
1. Preguntá cuántos Dados de Golpe gasta el jugador. Tirá `d[dado-de-golpe] + mod CON` por dado vía `dice.py`. Actualizá PG, envía `push_stats.py --player NOMBRE --hp`.
2. Anotá los rasgos de clase que se recargan (ej. Segundo Aliento → `push_stats.py --player NOMBRE --second-wind true`).
3. Avanzá el tiempo: `calendar.py -c <campaña> rest short`
4. Limpiá condiciones de encuentro: `tracker.py -c <campaña> clear` (la concentración puede persistir — pregunta)

**Largo (8 horas):**
1. Restaurá todo el PG, la mitad de los Dados de Golpe máximos (redondeado hacia arriba), todos los espacios de conjuro, la mayoría de los rasgos de clase. Actualizá la hoja.
2. Enviá: `push_stats.py --player NOMBRE --hp <max> <max>` y `--second-wind true`.
3. Avanzá el tiempo: `calendar.py -c <campaña> rest long`
4. Limpiá todo el estado del tracker: `tracker.py -c <campaña> clear --all`
5. Actualizá la fecha en el mundo de `state.md` para que coincida con la salida del calendario.

---

## `/dm:dnd recap`
Leé session-log.md. Entregá un resumen en personaje de 3-5 oraciones de la entrada de sesión más reciente.

## `/dm:dnd pin [<hecho> | list | remove <hecho-o-número>]`

Gestioná los **Hechos Fijados** de la campaña — el canon blando y estable que la mesa nunca quiere olvidar. Los hechos fijados viven en `state.md → ## Pinned Facts` y se leen en cada `/dm:dnd load` junto con `## DM Style Notes`, y después se mantienen presentes durante toda la sesión. Son la memoria a largo plazo del DM: cosas que no encajan en Live State Flags (que sigue estado cambiante) porque no cambian — una promesa hecha, el nombre de un hermano muerto, un chiste interno, una regla casera, un detalle que el jugador dijo que importaba.

- **`/dm:dnd pin <hecho>`** — agrega `<hecho>` como una viñeta nueva bajo `## Pinned Facts` (reemplazando el placeholder *(none pinned yet)* si está presente). Confirmá qué se fijó. Mantené cada hecho a una línea; fija el hecho, no un párrafo.
- **`/dm:dnd pin`** *(sin argumentos, a mitad de escena)* — cuando el jugador dice "acordate de esto" / "no te olvides de X" / "fija eso", captura el hecho al que se refiere en una línea y fijalo como arriba, después reconocelo brevemente en la ficción y sigue.
- **`/dm:dnd pin list`** — lee e imprime las viñetas actuales de `## Pinned Facts`.
- **`/dm:dnd pin remove <hecho-o-número>`** — elimina la viñeta coincidente (por su texto o su posición en la lista). Si deja la sección vacía, restaura el placeholder *(none pinned yet)*. Confirmá la eliminación.

Los hechos fijados nunca se reescriben por completo en `/dm:dnd save` como sí pasa con Live State Flags — solo cambian cuando el jugador fija o desfija uno, o cuando uno se corrige porque quedó mal. Un registro continuo de *qué pasó* ya vive en `session-log.md`, `## Recent Events`, y `## Continuity Archive` (consultado vía `/dm:dnd recap`); Pinned Facts es el conjunto separado, deliberadamente chico, de cosas para llevar siempre, no un segundo registro de eventos.

## `/dm:dnd world`
Leé y muestra world.md.

## `/dm:dnd quests`
Leé `state.md` → muestra las secciones de Misiones Activas e Hilos Abiertos.

---

## `/dm:dnd arc [status|advance|revise|view]`

Gestioná el arco de campaña dinámico. Los subcomandos `advance`/`revise`/`new` solo están activos cuando `state.md → ## Campaign Arc` tiene `type: dynamic` — no hacen nada en campañas sandbox. Para campañas **estructuradas (importadas)**, `status` y `view` leen de `arc.md` (el avance de capítulo pasa en `/dm:dnd save`, no acá); `advance`/`revise`/`new` no hacen nada.

- **`/dm:dnd arc`** o **`/dm:dnd arc status`** — imprime el acto actual, la etiqueta del beat actual, `what_changes` del beat actual, y `steering_notes`. Referencia rápida, una sola pantalla. (Estructurada: imprime `current_act`, `current_chapter`, los `key_beats` del capítulo actual, y `outstanding_beats` de `state.md`; lee `arc.md` solo si se pide más detalle.)
- **`/dm:dnd arc advance [beat-id]`** — marca el beat nombrado como completo (el beat actual si se omite). Lo elimina de `outstanding_beats`. Avanza `current_beat` al siguiente beat pendiente. Si todos los beats de un acto están completos, avanza `current_act`. Actualizá `steering_notes` para describir cómo llegar al beat recién actual sin forzarlo.

  **Cuando el beat final (3b) se marca completo — continuación del arco:**
  `outstanding_beats` ahora está vacío. Preguntá: *"El arco está completo. ¿Continuar la campaña con un arco nuevo? [s/n]"*
  - **Sí** → corre `/dm:dnd arc new` (ver abajo).
  - **No** → pon `type: sandbox` y limpia `outstanding_beats`. La campaña continúa abierta desde el estado de resolución.

- **`/dm:dnd arc new`** — genera un arco nuevo para una campaña que completó su arco anterior. Usá Opus para este paso.

  El arco nuevo debe ser **intencionalmente distinto** — no una continuación del mismo conflicto, sino un capítulo nuevo que crece del mundo cambiado. La resolución del arco N es el statu quo del arco N+1.

  Procedimiento:
  1. Leé el campo `resolution` del arco completado — esa es ahora la línea base del mundo.
  2. Leé `## DM Notes`, `## World State`, `## Faction Moves`, y cualquier entrada de `## Continuity Archive` para entender cómo se ve el mundo post-resolución.
  3. Derivá el arco nuevo a partir de **las consecuencias** de lo que se acaba de resolver. Preguntá: *¿qué problema creó resolver el último arco? ¿Qué vacío de poder se formó? ¿Qué le costó a la victoria del grupo que ahora hay que enfrentar? ¿Qué se ignoró porque el último arco demandaba toda la atención?*
  4. Generá un arco nuevo y completo (tema, resolución, actos 1-3, 6 beats) usando el mismo formato que el arco inicial. El tema nuevo debe ser significativamente distinto del anterior — mismo mundo, lente nueva.
  5. Archivá el arco completado: mueves el bloque `acts` actual, `theme`, y `resolution` a una nueva sección `## Arc History` en state.md bajo `arc_N` (numerado), con un resumen de una línea de cómo se resolvió.
  6. Escribí el arco nuevo en `## Campaign Arc`, incrementando `arc_number`. Poné `current_act: 1`, `current_beat: "1a"`, `outstanding_beats` con los 6 ids de beat.
  7. Agregá a `revision_log`: `"<fecha>: Arco N completo. Arco N+1 nuevo generado. [premisa en una línea del arco nuevo]"`
  8. Entregá un resumen de un párrafo de la premisa del arco nuevo y en qué se diferencia del anterior.

- **`/dm:dnd arc view`** — muestra el arco completo: tema, resolución, todos los actos y beats con estado de finalización (actual / completo / pendiente). Si existe `## Arc History`, muestra un resumen de una línea de cada arco completado antes del actual.
- **`/dm:dnd arc revise`** — abre el flujo de revisión para cuando la historia tomó un giro mayor inesperado O cuando se dispara el auto-trigger del chequeo de adelantamiento de /dm:dnd end (el caso más común):
  1. Mostrá todos los beats pendientes con su `what_changes` y `world_pressure` actuales.
  2. Preguntá: *"¿Qué cambió en la historia que el arco no refleja?"* — o, cuando se auto-dispara por adelantamiento, nombra el beat adelantado directamente: *"La presión del beat 2b se entregó pero la consecuencia no aterrizó. Eligiendo un camino de revisión…"*
  3. **Aplicá una de tres plantillas de camino de aterrizaje** (según la regla 8 de SKILL.md) al beat pendiente afectado:
     - **Camino de costo** — `what_changes` se convierte en "el grupo pagó un costo concreto por moverse rápido"; `world_pressure` se convierte en el costo específico (tapadera descubierta, aliado comprometido, posición perdida). Mejor cuando el grupo se adelantó limpiamente.
     - **Camino de consecuencia secundaria** — `what_changes` se convierte en "el mundo respondió a haber sido adelantado de una forma que el grupo no anticipó"; `world_pressure` se convierte en la nueva escalada (el antagonista lee la disrupción como una señal y hace algo PEOR). Mejor cuando el antagonista es inteligente y adaptativo.
     - **Camino diferido** — mantén la forma original de `what_changes`; reescribe `world_pressure` con una presión NUEVA que apunta a la misma consecuencia, programada para las próximas 1-2 sesiones. Mejor cuando la consecuencia original todavía es narrativamente esencial y solo se atrasó el momento.
  4. Reescribí `what_changes` (con forma de consecuencia según la regla en /dm:dnd new paso 12) y `world_pressure` (forma de evento está bien) para el beat afectado. NO modifiques beats completados.
  5. Agregá a `revision_log`: `"<fecha>: <beat-id> — <camino: cost/secondary/deferred> — <qué cambió y por qué — una oración>"`
  6. Actualizá `steering_notes` para describir la entrega esperada de la próxima sesión.
  7. Confirmá qué se revisó. Mostrá antes/después de `what_changes` y `world_pressure`.

---

## `/dm:dnd graph <subcomando>` — grafo de relaciones de campaña

Grafo de relaciones tipadas, local, que complementa el markdown. Se guarda en `~/.claude/dnd/campaigns/<nombre>/graph.json`. Complementa a `npcs-full.md` / `session-log.md` — no los reemplaza. Los edges tienen timestamp (`since_session` / `until_session`), así que el estado histórico es recuperable.

**Se trae automáticamente en el paso 5 de `/dm:dnd load`** (scene-context) y **se barre en `/dm:dnd save`** (extracción de cambios de relación). El DM también usa `/dm:dnd graph scene-context` bajo demanda a mitad de sesión, especialmente antes de escenas sociales o políticas pesadas.

Para lectura de fondo sobre el diseño y el estudio de replay A/B que lo motivó, ver `docs/research/graph/`.

Todos los subcomandos invocan `python3 ${CLAUDE_SKILL_DIR}/scripts/campaign_graph.py <subcomando> --campaign <nombre> [args]`.

### `/dm:dnd graph init [nombre-campaña]`
Inicialización de primera vez. Leé el `npcs.md` / `world.md` / `state.md` existentes de la campaña. Proponé una lista de nodos (PNJ como `npc_*`, facciones como `faction_*`, ubicaciones clave como `place_*`) y una lista de edges iniciales (membresía de facción de las tablas de npcs.md, ubicación de PNJ de campos "Vive en / Basado en", relaciones de facción de world.md). Mostrale la lista propuesta al DM y **pide aprobación** antes de escribir — no extraigas en silencio. Con la aprobación, corre `add-node` y `add-edge` para cada uno. Usá `--since` coincidiendo con el contador de sesión actual de state.md.

Para campañas existentes que se inicializan por primera vez, el flujo de `/dm:dnd load` ofrece respaldar el directorio de campaña primero; respeta ese flujo en vez de correr init desde un prompt frío.

### `/dm:dnd graph add-node --type T --name N [--tags ...] [--summary ...]`
Agrega un solo nodo. El tipo es vocabulario abierto; sugeridos: `npc`, `faction`, `place`, `item`, `thread`. El id por defecto es `<type>_<slug-nombre>`.

### `/dm:dnd graph add-edge --from <id> --to <id> --type T [--since N] [--note ...]`
Agrega un edge tipado entre dos nodos existentes. El tipo de edge es vocabulario abierto; comunes: `loyal_to`, `opposes`, `allied_with`, `member_of`, `lives_in`, `controls`, `knows_about`, `friends_with`, `lover_of`, `owes`, `rules`, `related_by_blood`, `advances_thread`, `blocks_thread`. Proporcioná siempre `--since` (el número de sesión actual de state.md) para que el replay histórico funcione.

### `/dm:dnd graph set-disposition --to <pnj-o-facción> --level <L> [--since N] [--note ...]`
Tipeá cómo se posiciona el **grupo** hacia un PNJ o facción en la escala normalizada `allied | friendly | neutral | suspicious | hostile` — los mismos cinco valores que usa el panel de facciones del display, así que el grafo y la barra lateral hablan el mismo idioma. El edge va del nodo compartido `party` (auto-creado en el primer uso) al objetivo; su tipo se infiere del objetivo — `disposition` para un PNJ, `standing` para una facción — y lleva el `level`.

De un solo valor y actual: fijar una postura nueva **cierra** cualquier edge previo activo de postura party→objetivo en `--since` (su arco sigue consultable con `--at-session <N vieja>`) y agrega el nivel nuevo, así que `scene-context` solo muestra la postura *actual* del grupo. `scene-context` la renderiza como `The Party --[disposition:suspicious]--> Aldric` para que la postura se lea de un vistazo. Siempre pasa `--since <sesión-N-actual>`.

Usalo cuando la ficción cambia la postura del grupo — un PNJ se vuelve contra ellos, una facción a la que agraviaron se vuelve hostil, se gana una alianza. Es la contraparte del lado del grafo de los valores `standing` que se envían al display vía `push_stats.py --factions` y de las líneas de disposición de PNJ en `state.md → ## Live State Flags`; mantén los tres consistentes cuando cambia una postura.

### `/dm:dnd graph close-edge --id <edge-id> --at-session N`
Marca un edge como terminado en la sesión N (ej. cuando se rompe una alianza). El edge original se preserva con `until_session` fijado; sigue visible en consultas históricas pero se excluye de resultados "activo en sesión ≥ N".

### `/dm:dnd graph list [--type T] [--at-session N]`
Imprime una tabla compacta de nodos agrupados por tipo. Con `--at-session`, también reporta el conteo de edges activos en esa sesión.

### `/dm:dnd graph show --id <node-id>`
Imprime un nodo con todos sus edges entrantes y salientes.

### `/dm:dnd graph scene-context --place <id> [--present id1,id2] [--threads id1,id2] [--hops H] [--at-session N]`
**Consulta principal para uso en sesión.** Devuelve un subgrafo enfocado de la escena actual (lugar + PNJ presentes + hilos activos) acotado por número de saltos, opcionalmente filtrado a edges activos en una sesión dada. La salida está agrupada: nodos por tipo, después un bloque de relaciones. Default `--hops 2`. Usalo cuando necesites recordar quién-se-relaciona-con-quién en la escena actual sin releer `npcs-full.md` o los archivos de session-log.

### `/dm:dnd graph subgraph --seed <id> [--seed <id>] [--hops H] [--at-session N]`
Recorrido de nivel más bajo — igual que `scene-context` pero con nodos semilla arbitrarios. Usalo cuando el encuadre de la escena no encaja (ej. rastreando política de facción independiente de cualquier lugar específico).

### `/dm:dnd graph extract [nombre-campaña] [--last-session-only]`
Corre un paso de Haiku sobre el session-log de la campaña para proponer edges nuevos con anclas de fuente literales. Escribe un JSON de propuesta en `~/.claude/dnd/campaigns/<nombre>/graph-proposals-<fecha>.json` para revisión humana. NO escribe en graph.json — eso es el paso de aplicación.

### `/dm:dnd graph extract --deterministic [--last-session-only] [--write FILE]`
**Alternativa sin LLM.** Compara por patrones las oraciones del session-log contra la tabla de verbos semilla incluida (`data/graph/verb_table_seed.yaml`) y emite la misma forma de propuesta que el paso de Haiku — sin llamada a la API de Claude, sin costo, totalmente portable. Cambia recall (~50%, solo sujeto-verbo-objeto limpio) por precisión (~95%) y determinismo. Imprime las propuestas a stdout, o las escribe con `--write`.

### `/dm:dnd graph extract --deterministic --apply [--min-confidence low|medium|high] [--no-auto-nodes]`
Auto-aplicación de un solo paso: corre la extracción determinística y escribe las propuestas con confianza igual o mayor a `--min-confidence` (default `high`) directamente en graph.json — deduplicado contra edges existentes e **idempotente** (volver a correr no agrega nada nuevo). Los nodos faltantes se auto-crean como placeholders `npc_*` a menos que se ponga `--no-auto-nodes`. Usalo para un barrido de relaciones sin intervención en `/dm:dnd save`; usa el camino de revisión de abajo cuando quieras un humano en el loop.

### `/dm:dnd graph extract-apply --proposals <file> [--pick N1,N2,...] [--review]`
Aplica propuestas previamente extraídas (del paso de Haiku o del determinístico). Sin `--pick`/`--review`, aplica todas. Con `--pick`, aplica solo los índices de propuesta listados. Con `--review`, recorre las propuestas una por una con prompts s/n/q.

### Flujo de trabajo sugerido para el DM

1. **Primera sesión después de instalar:** `/dm:dnd load` va a ofrecer inicializar el grafo (con un prompt de respaldo primero). Aceptá; revisa la semilla propuesta; aprueba.
2. **Durante la sesión:** cuando una relación cambia en la narración, corre `/dm:dnd graph add-edge` (o `close-edge`) con `--since` fijado en el número de sesión actual. No lo hagas en lote — registralo en el momento del cambio narrativo para no olvidarte.
3. **Antes de una escena social/política pesada:** corre `/dm:dnd graph scene-context --place <lugar-actual> --present <pnj-clave>` para refrescar qué relaciones importan ahora mismo.
4. **En `/dm:dnd save`:** revisa el session log y agrega cualquier edge que te hayas perdido durante la partida (el flujo de save corre un barrido automático y presenta propuestas para aprobación).

---

## `/dm:dnd oracle <subcomando>` — herramientas de oráculo solo/improvisado

Oráculos guiados por dados para juego improvisado — mantienen el ritmo transparente y tirable en vez de dejar que el DM invente cada beat. Todos los subcomandos invocan `python3 ${CLAUDE_SKILL_DIR}/scripts/oracle.py <subcomando>`. Las tiradas son de random estándar y sembrables (`--seed N`) para reproducibilidad. Cero llamadas a LLM.

### `/dm:dnd oracle chaos [--campaign N]`
Muestra el **factor de caos** actual de la campaña (estilo Mythic, 1-9). 1 = los PJ tienen el control firme; 9 = el mundo se les está yendo de las manos. Se guarda en `state.md → ## Session Flags` como `chaos_factor: N` (default 5).

### `/dm:dnd oracle chaos set --campaign N --value V`
Fija el factor de caos en V (acotado 1-9) y lo persiste en `state.md`.

### `/dm:dnd oracle chaos adjust --campaign N (--pc-won | --pc-lost)`
Mueve el factor un paso en la dirección estándar Mythic: `--pc-won` (el PJ logró el objetivo de la escena) → −1; `--pc-lost` (el PJ fue reactivo o falló) → +1. Ajustá una vez por escena.

### `/dm:dnd oracle ask [--likelihood L] [--campaign N | --chaos C] [--seed S]`
Oráculo de **sí/no** con forma Ironsworn. Likelihood ∈ {`sure-thing`, `likely`, `50/50`, `unlikely`, `no-way`} (default `50/50`); el factor de caos (leído de la campaña, o `--chaos`) cambia las probabilidades. Devuelve un veredicto — `yes`/`no` opcionalmente sufijado `-and` (extremo, en dobles) o `-but` (calificado, cerca del umbral) — más el d100. Usalo cuando la ficción plantea una pregunta que la preparación no responde.

### `/dm:dnd oracle event [--seed S]`
**Foco de Evento Aleatorio** Mythic (d100). Devuelve una etiqueta de dirección en inglés — literal, tal como la imprime el script (`new NPC`, `NPC action`, `move toward thread`, `PC negative`, etc.) — interpretala en español contra los hilos, PNJ, y ubicaciones actuales de la campaña. Usalo cuando una escena necesita un giro inesperado.

### `/dm:dnd oracle scene [--seed S]`
Generador de **significado de escena** de dos palabras (verbo de acción + sustantivo sujeto, One Page Solo Engine). Usalo como chispa cuando la narración se seca o rueda un foco de evento. Interpretalo con libertad.

---

## `/dm:dnd recap` — diferencia de estado del grupo precalculada

Diferencia determinística de estado entre dos instantáneas de personaje — `python3 ${CLAUDE_SKILL_DIR}/scripts/session_recap.py`. Los resúmenes son lo #1 que un LLM alucina (PG mal, hechos perdidos); esto calcula el conjunto de cambios a partir de datos para que la narración nunca tenga que hacerlo. Lee las hojas de personaje en `~/.claude/dnd/campaigns/<nombre>/characters/*.md` y fusiona condiciones/concentración en vivo de `tracker.json`. Cero llamadas a LLM.

### `/dm:dnd recap snapshot --campaign N`
Toma una instantánea del estado actual del grupo (PG/temp/nivel/dados de golpe/tiradas de muerte/condiciones/concentración/cansancio/inspiración/espacios de conjuro) en `~/.claude/dnd/campaigns/<nombre>/.recap/`. Mueve el `last.json` anterior a `prev.json` para que la próxima diferencia tenga una línea base. **Tomá una instantánea en `/dm:dnd end`** para que la carga de la próxima sesión pueda diferenciar contra ella.

### `/dm:dnd recap diff --campaign N [--before FILE] [--after FILE]`
Diferencia la instantánea previa contra el estado actual e imprime un resumen en inglés llano de un párrafo (ej. *"Aldric: tomó 18 de daño (30→12 PG); ganó Envenenado; gastó 2 espacios de nivel 1."*). Sin `--before`, usa la instantánea guardada `prev`/`last`; sin `--after`, toma una instantánea del estado en vivo al vuelo. **Inyectá esta línea en `/dm:dnd load`** como la mitad mecánica del resumen. `--json` emite la lista de cambios estructurada.

---

## `/dm:dnd tutor on` / `/dm:dnd tutor off`
Alterná el modo tutor/aprendizaje. Escribí `tutor_mode: true/false` en `state.md` bajo `## Session Flags`. Con alcance de sesión — no persiste a la próxima `/dm:dnd load` a menos que se fije explícitamente de nuevo. (El comportamiento completo del modo tutor está en SKILL.md.)

---

## `/dm:dnd autorun on` / `/dm:dnd autorun off`

Alterná el modo autorun (taxi) — Claude lleva el loop de turnos automáticamente cuando los jugadores envían vía el display companion. No hace falta wrapper de PTY.

**Activar:**
1. Escribí `autorun: true` en `state.md → ## Session Flags`.
2. **Chequeá los permisos de Bash** — lee `~/.claude/settings.json`. Si `permissions.allow` no incluye `"Bash"` (o `"Bash(*)"` o similar), agregalo automáticamente:
   - Leé el archivo, fusiona `"Bash"` en `permissions.allow`, escribilo de vuelta.
   - Decile al DM: *"Agregué Bash a permissions.allow en ~/.claude/settings.json — autorun no va a preguntar en cada espera. Reiniciá esta sesión para que tenga efecto si no lo hace de inmediato."*
   - Si ya estaba presente, saltea en silencio.
3. Confirmale al DM: *"Autorun activado. Los jugadores envían vía el display; voy a recoger cada acción automáticamente. Mandame un mensaje en cualquier momento para tomar control de un turno."*
4. Si el usuario especificó un intervalo (ej. `/dm:dnd autorun on 45`), escribe `autorun_interval: 45` en `state.md → ## Session Flags`. El default es 60 si se omite.
5. Entrá de inmediato a la espera de autorun (ver SKILL.md para el bloque de Bash). Si ya hay algo en `.input_queue`, recogelo como la acción del turno actual.

El display muestra una cuenta regresiva de reloj de torta drenándose de lleno a vacío en el intervalo. Pulso verde = esperando activamente. Configurable vía `autorun_interval: N` en state.md (default 60 segundos).

**Desactivar:**
1. Escribí `autorun: false` (o elimina la línea) en `state.md → ## Session Flags`.
2. Confirmá: *"Autorun desactivado. Volvemos a modo manual — presiona Enter o decime cuando los jugadores estén listos para enviar."*
3. NO inicies la espera de autorun después de esta respuesta.

**Chequeo en `/dm:dnd load`:** Si `autorun: true` está presente en state.md, decile al DM que autorun está activo y empieza el loop de espera después del párrafo de resumen.

**Cuándo NO correr la espera de autorun (incluso si el flag está activo):**
- A mitad de combate, resolviendo el turno de un combatiente específico
- Esperando el resultado de una tirada de un jugador
- El DM acaba de mandar un mensaje (está llevando este turno)
- Durante `/dm:dnd save`, `/dm:dnd end`, o cualquier respuesta de comando

---

## `/dm:dnd autosave on` / `/dm:dnd autosave off`

Alterná el checkpoint de continuidad detrás de escena. Escribe `autosave: on|off` en `state.md → ## Session Flags`. **El default es activado.** Aplica a cada tipo de campaña (estructurada, dinámica, sandbox) — solo escribe siempre las mismas anclas de continuidad que un save normal escribe, solo que más seguido, y nunca cambia la narración.

**Qué hace el autosave cuando está activo:**
1. **Micro-saves en el modelo** (siempre disponibles, sin configuración): el DM vacía la continuidad en silencio en los límites de escena y en un ritmo de turnos — ver la regla de *Continuity micro-save* en SKILL.md. Esto mantiene el estado sin guardar cerca de cero para que una compactación de contexto no cueste nada.
2. **Checkpoint determinístico por Stop-hook** (opcional, opt-in): si el usuario instaló el hook, `autosave_checkpoint.py` toma una instantánea de `state.md` en cada turno y sugiere un micro-save cada N turnos. Instalalo una vez con:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py        # activar
   python3 ${CLAUDE_SKILL_DIR}/scripts/install_autosave_hook.py --uninstall
   ```
   El hook lee este mismo flag `autosave`, así que `/dm:dnd autosave off` lo silencia sin desinstalarlo.

**Activar:** escribe `autosave: on`. Confirmá: *"Autosave activado — voy a checkpointear la continuidad detrás de escena para que una compactación de contexto nunca pierda tu lugar."*

**Desactivar:** escribe `autosave: off`. Confirmá: *"Autosave desactivado — solo voy a persistir en /dm:dnd save y /dm:dnd end."*

**Por qué contador de turnos, no un porcentaje de contexto:** el modelo no puede ver su propio nivel de uso de contexto, así que no hay un disparador confiable de "guardar al 80% lleno" desde dentro del skill. El ritmo se basa en turnos en cambio, calibrado para dispararse bastante antes de la auto-compactación.

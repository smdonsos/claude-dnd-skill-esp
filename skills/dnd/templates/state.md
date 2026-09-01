# Campaña: <nombre>
**Created:** <fecha>  **Last session:** —  **Session count:** 0  **Ruleset:** 2014

## Current Situation
- **Ubicación:**
- **Fecha/hora en el mundo:**
- **Grupo:** <Nombre> — <Raza> <Clase> <Level> | HP X/X | AC X | <recursos>
- **Estado del grupo:**

## Pinned Facts
*Hechos suaves que el DM siempre mantiene presentes — canon que la mesa nunca quiere que se olvide. Leer en cada /dnd load junto con DM Style Notes y mantenerlos presentes toda la sesión. A diferencia de Live State Flags (que sigue estado cambiante y se reescribe en cada guardado), los pinned facts son estables y solo se agregan o quitan a pedido. Fija una promesa hecha, el nombre de un hermano muerto, un chiste recurrente de la mesa, una regla casera de la mesa, un detalle que el jugador dijo que le importa. Agregar/listar/quitar con `/dm:dnd pin`.*
*(todavía no hay nada fijado)*

## World State
- **Fecha en el mundo:** <Día, Mes, Año — fuente canónica; mantener sincronizado arriba>
- **Estación:** <estación actual>  **Clima:** <condiciones actuales>
- **Etapa del arco de amenaza:** 1 — Ahora
- **Estado de las facciones:**
  - <Nombre de facción>: <disposición y actividad actual en una línea>
  - <Nombre de facción>: <una línea>

## Active Quests
*(todavía ninguna)*

## Open Threads & Rumours

## Faction Moves
*Se actualiza al final de cada sesión — qué hizo cada facción activa mientras el grupo estaba ocupado.*
*(todavía ninguna)*

## Recent Events
*(Sesión 1 pendiente)*

## Active Combat
*(ninguno)*

## Live State Flags
*Hechos estructurados diseñados para sobrevivir a la compactación de contexto. Releer esta sección antes de cualquier resumen, actualización de estado, o afirmación sobre coartadas, postura de un NPC, o standing de una facción. Actualizar en cada /dnd save.*

**Cover:**
*(nada establecido)*

**Faction stances** *(listar solo facciones con standing no neutral hacia el grupo)*:
*(nada establecido)*

**NPC dispositions** *(listar solo NPCs con standing cambiado o notable)*:
*(nada establecido)*

## Campaign Arc
*(campañas sandbox: definir `type: sandbox` — sin seguimiento de arco)*
*(campañas estructuradas: pobladas por /dnd import — usar formato structured)*
*(campañas improvisadas: auto-generadas en /dnd new — usar formato dynamic)*
```yaml
# --- ARCO DINÁMICO (campañas improvisadas, auto-generado en /dnd new) ---
type: dynamic
arc_number: 1          # se incrementa cada vez que /dnd arc new genera un arco sucesor
generated: "<fecha>"
revised: null

theme: "<una frase — de qué trata esta historia en el fondo, no qué pasa sino qué significa>"
resolution: "<forma de desenlace comprometida — no eventos específicos, sino la verdad emocional/temática si el grupo tiene éxito>"

acts:
  - act: 1
    title: "Planteamiento"
    drive: "<qué quiere o necesita el grupo al principio>"
    beats:
      - id: "1a"
        label: "<Incidente incitador>"
        what_changes: "<antes vs. después — qué es fundamentalmente distinto una vez que esto sucede>"
        world_pressure: "<movimiento específico de facción/NPC que hace que este beat se sienta inevitable>"
        status: current     # current | complete | skipped
      - id: "1b"
        label: "<Complicación>"
        what_changes: "<qué descubre el grupo que hace el problema más grande o más extraño de lo que parecía al principio>"
        world_pressure: "<qué genera esta presión>"
        status: pending

  - act: 2
    title: "Confrontación"
    drive: "<qué persigue el grupo ahora — puede diferir del acto 1>"
    beats:
      - id: "2a"
        label: "<Giro del punto medio>"
        what_changes: "<lo que creían que era verdad / la meta que creían tener cambia>"
        world_pressure: "<qué fuerza esta revelación>"
        status: pending
      - id: "2b"
        label: "<Todo está perdido>"
        what_changes: "<un revés genuino — algo falla, se pierde, o colapsa>"
        world_pressure: "<qué provoca este fracaso>"
        status: pending

  - act: 3
    title: "Resolución"
    drive: "<qué entiende el grupo ahora y por qué está luchando>"
    beats:
      - id: "3a"
        label: "<Confrontación final>"
        what_changes: "<el momento decisivo sobre el que gira la campaña>"
        world_pressure: "<la forma escalada de la amenaza original>"
        status: pending
      - id: "3b"
        label: "<Resolución>"
        what_changes: "<qué es distinto del mundo y los personajes después>"
        world_pressure: "<qué hacen las facciones/NPCs con el desenlace>"
        status: pending

current_act: 1
current_beat: "1a"

outstanding_beats:
  - "1a"
  - "1b"
  - "2a"
  - "2b"
  - "3a"
  - "3b"

steering_notes: >
  <Guía activa — qué presión del mundo aplicar para llegar al beat actual sin forzarlo.
  Actualizar en cada /dnd end cuando un beat avanza o necesita conducción activa.>

revision_log: []

# --- PUNTERO DE ARCO ESTRUCTURADO (campañas importadas, poblado por /dnd import) ---
# Las campañas estructuradas mantienen inline solo esta ventana liviana. El árbol
# completo de actos/capítulos vive en arc.md para que quede fuera del camino
# crítico al cargar. Leer arc.md solo al avanzar capítulos o al responder una
# pregunta sobre el arco general.
# type: structured
# source: "<título>"
# structure: linear      # linear | hub-and-spoke | faction-web
# arc_file: arc.md
# current_act: 1
# current_chapter: "1.1"
# current_chapter_detail:
#   id: "1.1"
#   title: "<nombre del capítulo>"
#   location: "<ubicación principal>"
#   source_ref: "source/1.1.md"
#   key_beats: ["<beat>", "<beat>"]
#   telegraph_scene: "<escena de preparación>"
# next_chapter: "1.2"      # para que el DM pueda anticipar sin cargar arc.md
# outstanding_beats: ["<beat>"]
# steering_notes: >
#   <Cómo guiar a los jugadores hacia los beats pendientes sin forzar.>
```

## Arc History
*(poblado por /dnd arc new cuando un arco completado es sucedido por uno nuevo — una entrada por arco completado)*
*(dejar vacío hasta que se complete el primer arco)*

## Session Flags
*(tutor_mode, autorun, autorun_interval, tts_voice, sfx_languages, autosave — flags de sesión definidos vía comandos /dnd o por el display companion)*
*(autosave: on|off — default on. Gobierna el checkpoint de continuidad tras bambalinas (Live State Flags + graph + session tail). Alternar con /dm:dnd autosave on|off.)*
sfx_languages: es

## DM Notes (hidden from players)

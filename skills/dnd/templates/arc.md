# Campaign Arc — <nombre-de-campaña>

*Solo para campañas estructuradas (importadas). El árbol completo de actos/capítulos vive
acá para que quede fuera del camino crítico en `/dm:dnd load`. `state.md → ## Campaign Arc`
mantiene solo el puntero liviano más el capítulo actual y el siguiente. Leer este archivo
al avanzar capítulos o cuando un jugador pregunta sobre el arco general — no en cada carga.*

*Las campañas dinámicas y sandbox no usan este archivo; su arco vive inline en
`state.md → ## Campaign Arc`.*

```yaml
type: structured
source: "<título de la fuente>"
structure: linear        # linear | hub-and-spoke | faction-web
current_act: 1
current_chapter: "1.1"

acts:
  - act: 1
    title: "<título del acto>"
    chapters:
      - id: "1.1"
        title: "<nombre del capítulo>"
        location: "<ubicación principal>"
        source_ref: "source/1.1.md"   # texto del capítulo en el corpus perezoso
        key_beats: ["<beat>", "<beat>"]
        telegraph_scene: "<escena de preparación que hace que el beat se sienta ganado>"
        branching_notes: "<cómo pueden variar el capítulo las decisiones del jugador>"
        status: current               # current | complete | skipped | pending
      - id: "1.2"
        title: "<nombre del capítulo>"
        location: "<ubicación principal>"
        source_ref: "source/1.2.md"
        key_beats: ["<beat>"]
        telegraph_scene: "<escena de preparación>"
        branching_notes: "<ramificación>"
        status: pending

outstanding_beats: ["<beat>", "<beat>"]

steering_notes: >
  <Cómo guiar a los jugadores hacia los beats pendientes sin forzar — la presión
  del mundo a aplicar para el capítulo actual. Actualizar en cada /dm:dnd save
  cuando un beat avanza o necesita conducción activa.>

revision_log: []
```

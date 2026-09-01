# Dungeon Master de D&D con Claude (no oficial)
### *con Display Companion Cinemático — Edición Couch Co-op*
> **Sistema de reglas:** D&D 5e — **2014 (SRD 5.1)** por defecto; **2024 (SRD 5.2)** opt-in por campaña. Se elige al hacer `/dm:dnd new`; las campañas legacy reciben un aviso automático para migrar (con backup) en la primera carga. Ver la [sección de Ruleset](#ruleset) para las diferencias mecánicas y detalles del dataset.

<div align="center">
  <img src="skills/dnd/display/icons/logo_primary_fullcolor.png" width="280" alt="D20 Neural Core">
</div>

> Claude dirige el juego. Tú juegas. La TV muestra la historia. Tu teléfono es tu control.

Un skill de Dungeon Master de D&D 5e (sistema 2014 / SRD 5.1) no oficial para [Claude Code](https://claude.ai/code) — campañas persistentes, mecánica completa de 5e, y un display companion cinemático opcional que transmite narración con efecto de máquina de escribir, tiradas de dados, y estadísticas de personaje en vivo a cualquier pantalla — TV vía Chromecast, tablet, teléfono, o segundo monitor — mientras los jugadores envían sus acciones desde un teléfono o tablet.

Hecho para grupos que quieren una experiencia de DM real sin necesitar uno en la mesa.

![Cinematic Display Demo](screenshots/demo-v3.gif)

---

## Qué es esto

Corres `/dm:dnd load mi-campaña` en Claude Code. Claude se convierte en tu DM — tira dados, le da voz a los PNJ, lleva el registro de PG y XP, y dirige el combate. Si tienes una TV o tablet cerca, el **display companion cinemático** pone la narración en pantalla en tiempo real — efecto de máquina de escribir, fondos atmosféricos que cambian con la escena, un canvas de cielo dinámico, y una barra lateral en vivo con las estadísticas del grupo. Ábrelo en cualquier dispositivo de tu red y todos en la mesa pueden seguir la partida. Los jugadores envían sus acciones desde sus teléfonos; Claude las recoge automáticamente y corre el siguiente turno.

Hay dos formas de jugar, y sirven necesidades distintas:

**Campañas improvisadas** — Claude genera el mundo desde cero y crea automáticamente un arco narrativo comprometido de tres actos a partir del setting, las facciones, y las amenazas que acaba de construir. El arco le da a la historia una forma definida sin guionar lo que pasa — los beats se definen por consecuencia ("qué cambia") no por evento, así que Claude se mantiene flexible en cómo aterriza cada beat mientras se compromete al hecho de que debe aterrizar. El arco avanza a través de las sesiones, se puede revisar cuando los jugadores redirigen la historia, y continúa en un nuevo arco cuando los seis beats se resuelven. Esto es Claude como colaborador creativo completo: constructor de mundos, compañero de improvisación, y arquitecto de historias en uno.

**Campañas estructuradas** — Usa `/dm:dnd import` para meter una fuente pre-escrita (módulos oficiales de WotC, campañas publicadas de terceros, o un documento propio escrito por el DM en formato PDF, markdown, DOCX, o texto plano). Claude lee y segmenta la fuente, extrae el tipo de estructura (lineal, hub-and-spoke, o red de facciones), y construye todos los archivos de campaña automáticamente — actos, capítulos, beats clave de la historia, escenas de anticipo, PNJ, facciones, ubicaciones, y ganchos de misión. La campaña corre con una estructura determinística forzada: los beats requeridos deben aterrizar en cada capítulo, Claude los anticipa antes de entregarlos, y guía con presión del mundo en vez de paredes cuando los jugadores se desvían. Metele el Lost Mine of Phandelver y Claude lo va a correr capítulo por capítulo con los mismos doce estándares de DM aplicados a cada escena.

Ambos modos comparten el mismo motor de DM. Los [doce estándares de comportamiento aplicados](https://github.com/neuralinitiative/claude-dnd-skill/blob/main/SKILL.md#what-makes-a-great-dm--applied-standards) se aplican como restricciones duras en cada sesión sin importar en qué modo estés — improvisado o estructurado, el DM improvisa dentro de las situaciones, deja que las decisiones importen, hace de cada PNJ una persona, y controla el ritmo deliberadamente.

También gestiona una red profunda de datos de campaña sin sobrecargar al LLM — coherente y completa, sin quemar tokens en contexto que todavía no se necesita:

- **Instrucciones del DM** — divididas en tres archivos con tiempos de carga escalonados; las reglas centrales siempre en el system prompt, la sintaxis de scripts y los procedimientos de comandos se cargan una vez al inicio de la sesión
- **Datos de campaña** — el roster de PNJ se indexa al cargar, las entradas completas se traen solo cuando un personaje se vuelve relevante; los ganchos de misión y el texto de worldbuilding quedan en almacenamiento frío hasta que se necesitan
- **Módulos importados** — un libro publicado se mantiene como un corpus de carga perezosa, no inlineado: el árbol de actos/capítulos, el banco de misiones/ubicaciones, y el texto fuente por capítulo se cargan bajo demanda, así un módulo largo corre capítulo por capítulo sin sentarse entero en el contexto
- **Historial de sesión** — se archiva como resúmenes de continuidad, no transcripciones crudas; el historial completo de campaña está disponible como referencia sin cargar el peso de tokens por adelantado
- **Resiliencia a la compactación** — un bloque compacto de Live State Flags en `state.md` ancla las posturas de facciones, la cobertura de los jugadores, y las disposiciones de PNJ; se relee ante cualquier afirmación para mantener la continuidad del mundo fundamentada en los archivos fuente en vez de en la impresión cada vez más difusa de Claude sobre ellos
- **Autoguardado** — la continuidad (flags de estado, grafo de relaciones, cola de sesión) se checkpointea detrás de escena en los límites de escena y con una cadencia de turnos, así una compactación de contexto nunca pierde tu lugar; actívalo/desactívalo con `/dm:dnd autosave on|off`, con un Stop hook opcional como respaldo determinístico por turno

Una campaña puede correr docenas de sesiones de profundidad — con memoria coherente de eventos pasados, actitudes de PNJ, y consecuencias de cola larga — sin la sobrecarga de contexto que fuerza a otras implementaciones a resumir, olvidar, o resetear.

No es un producto oficial de Wizards of the Coast. Usa a Claude como motor de DM. Se toma las reglas en serio y la narración todavía más en serio.

---

## ¿Usas otro LLM?

Este skill está construido específicamente para Claude Code. Si quieres correr el mismo framework en otro modelo — inferencia local, OpenRouter, o cualquier endpoint compatible con OpenAI — mira [open-tabletop-gm](https://github.com/neuralinitiative/open-tabletop-gm), la versión agnóstica de modelo extraída de este repo. Sacrifica algo de profundidad de integración específica de Claude a cambio de soporte más amplio de modelos e incluye una herramienta de sondeo para comparar la calidad de narración entre modelos.

Si prefieres saltarte la instalación por completo y jugar en el navegador, [neuralinitiative.ai](https://neuralinitiative.ai) es la versión alojada — mismo ADN de diseño, inicia sesión con Google, carga saldo en tu cuenta, juega. Cambia el auto-hosting (y menor costo por sesión) por cero configuración y una GUI más refinada.

Si estás en Claude Code, estás en el lugar correcto.

---

## Funciones

- <img src="skills/dnd/display/icons/scroll.png" height="18"> **Campañas persistentes** — el estado, los PNJ, las misiones, y los personajes sobreviven entre sesiones en archivos markdown planos
- <img src="skills/dnd/display/icons/dragon.png" height="18"> **Dos modos de campaña** — improvisado (Claude genera el mundo + arco dinámico) o estructurado (importa material pre-escrito y fuerza sus beats)
- <img src="skills/dnd/display/icons/crystal_ball.png" height="18"> **Arco narrativo dinámico** — auto-generado en `/dm:dnd new` a partir de la amenaza, facciones, y setting del mundo; tres actos, seis beats definidos por consecuencia y no por evento; el arco se trackea entre sesiones, se revisa cuando los jugadores redirigen la historia, y continúa en un nuevo arco cuando se completa
- <img src="skills/dnd/display/icons/spellbook.png" height="18"> **Grafo de relaciones de campaña** — grafo de aristas tipadas junto a los archivos markdown de campaña, con anclas de fuente textuales en cada arista; la consulta `scene-context` se trae automáticamente en `/dm:dnd load` para mostrar quién-conoce-a-quién en la escena actual sin releer archivos completos de PNJ; diseñado para sostener la continuidad de sesiones largas cuando la compactación de contexto saca archivos de alcance. Investigación de fondo y el estudio A/B de replay que lo motivó: [`docs/research/graph/`](docs/research/graph/)
- <img src="skills/dnd/display/icons/pack.png" height="18"> **Importación de campaña** — `/dm:dnd import` acepta PDF, markdown, DOCX, o texto plano; extrae el tipo de estructura, actos, capítulos, beats clave, escenas de anticipo, PNJ, facciones, y ganchos de misión; construye todos los archivos de campaña automáticamente y mantiene la fuente completa como un corpus de carga perezosa así hasta un módulo largo carga capítulo por capítulo
- <img src="skills/dnd/display/icons/helmet.png" height="18"> **Personajes portables** — trae tu personaje a cualquier campaña; sube de nivel, haz crecer tu árbol de stats, y lleva tu inventario y botín — o empieza de cero cada vez
- <img src="skills/dnd/display/icons/attack.png" height="18"> **Mecánica completa de D&D 5e** — iniciativa, ataques, tiradas de salvación, espacios de conjuro, XP, subida de nivel, descansos cortos/largos
- <img src="skills/dnd/display/icons/chat.png" height="18"> **DM atmosférico** — tono de fantasía oscura, voces de PNJ distintas, tiradas ocultas, un mundo que reacciona a las decisiones
- <img src="skills/dnd/display/icons/crystal_ball.png" height="18"> **Display companion cinemático** — narración con máquina de escribir en tu TV, fondos reactivos a la escena, canvas de cielo dinámico, barra lateral en vivo del grupo; proyecta, duplica, o ábrelo en cualquier pantalla de tu red
- <img src="skills/dnd/display/icons/location.png" height="18"> **Canvas de cielo dinámico** — arco solar, luna, estrellas titilantes, y densidad de nubes renderizados en tiempo real a partir de los datos de tiempo del mundo; transiciona con la hora del día y el clima
- <img src="skills/dnd/display/icons/focus.png" height="18"> **Input de jugador desde la UI del companion** — los jugadores envían acciones desde el teléfono/tablet con un envío de un toque y una franja de estado en vivo *Tu turno → Enviado → ✓ El DM tiene tu turno → narrando*; Claude las recoge automáticamente en modo autorun
- <img src="skills/dnd/display/icons/attack.png" height="18"> **Manejo forzado de tiradas** — elige al inicio de la partida si los jugadores tiran sus propios d20 (el DM pide la tirada y espera) o el DM tira abiertamente; override por personaje desde el teléfono; el DM nunca tira en silencio por un PJ
- <img src="skills/dnd/display/icons/scroll.png" height="18"> **Controles de lectura** — un stepper de tamaño de texto por jugador (legible desde el otro lado de la sala vía Chromecast) y un slider de longitud de narración que fija el presupuesto de palabras por turno del DM
- <img src="skills/dnd/display/icons/timer.png" height="18"> **Modo autorun / taxi** — Claude conduce el ciclo de turnos sin input del DM; un reloj de cuenta regresiva circular muestra la próxima ventana de disparo automático
- <img src="skills/dnd/display/icons/shield.png" height="18"> **Soporte de mesa por LAN** — sírvete el companion en tu red local; cada dispositivo en la sala ve el mismo display
- <img src="skills/dnd/display/icons/shield.png" height="18"> **TLS / HTTPS** — generación de certificado autofirmado incluida; necesario para soporte completo de funciones del navegador sobre LAN
- <img src="skills/dnd/display/icons/location.png" height="18"> **17 tipos de escena** — detectados automáticamente a partir de palabras clave de la narración — taberna, mazmorra, océano, cripta, arcano, glaciar, y más
- <img src="skills/dnd/display/icons/spellbook.png" height="18"> **Hojas de personaje clickeables** — toca cualquier tarjeta de la barra lateral para abrir un modal de hoja de personaje completa (ataques, rasgos, inventario); funciona en teléfonos y tablets vía LAN
- <img src="skills/dnd/display/icons/spellbook.png" height="18"> **Lookup de conjuro/rasgo del SRD** — haz clic en cualquier nombre de conjuro o rasgo en una hoja de personaje para ver su descripción completa; dataset de 5e incluido con entradas suplementarias para contenido no-SRD (Xanathar's, Tasha's, rasgos de subclase); link de respaldo a wikidot para lo que no está en los datos locales
- <img src="skills/dnd/display/icons/crystal_ball.png" height="18"> **Botón de Ayuda del DM** — haz clic en el botón ◈ del display para una pista o advertencia contextual bajo demanda; generada a partir de la escena actual sin sobrecarga de tokens por turno
- <img src="skills/dnd/display/icons/potion.png" height="18"> **Modo tutor / aprendizaje** — actívalo por sesión para bloques de pista automáticos después de cada escena, punto de decisión, y tirada; ideal para jugadores nuevos en D&D
- <img src="skills/dnd/display/icons/focus.png" height="18"> **Efectos de sonido del lado del navegador** — 12 tipos de SFX sintetizados bajo demanda vía numpy y reproducidos a través de Web Audio API; funciona en cualquier dispositivo con la pestaña abierta, incluidos teléfonos vía LAN
- <img src="skills/dnd/display/icons/dragon.png" height="18"> **Couch co-op** — múltiples personajes, display compartido, orden de turnos visible para todos en la sala
- <img src="skills/dnd/display/icons/attack.png" height="18"> **Tracker de combate** — iniciativa auto-tirada, puntero de turno `▶`, barras de PG, matemática de dados en línea enviada al display
- <img src="skills/dnd/display/icons/dagger.png" height="18"> **Scripts helper** — tirada de dados, puntajes de característica, combate, derivación de stats de personaje, condiciones/tracker, calendario, sincronización de datos SRD, lookup de SRD, constructor de datos suplementarios

---

## Cómo funciona

```
Claude Code CLI  ──→  comandos /dm:dnd  ──→  archivos de campaña (~/.claude/dnd/)
                                              state.md · world.md · npcs.md
                                              session-log.md · characters/

Pipeline del display (modo autorun):
  Jugadores (teléfono/tablet)  ──→  UI del Companion  ──→  servidor Flask SSE (localhost:5001)
                                                          ↓
                                                   autorun_wait.py
                                                          ↓
                                                   Claude procesa el turno
                                                          ↓
                                              send.py / push_stats.py  ──→  display de TV
```

El servidor Flask recibe el texto de narración, las acciones de jugador, los resultados de dados, y las estadísticas de personaje vía HTTP POST. Transmite todo en tiempo real a los navegadores conectados vía Server-Sent Events. El navegador renderiza la narración con un efecto de máquina de escribir sobre un fondo con gradiente reactivo a la escena y una barra lateral de personaje en vivo. En modo autorun Claude consulta por envíos de jugador y procesa cada turno automáticamente.

---

## Requisitos previos

- CLI de [Claude Code](https://claude.ai/code) instalada
- Python 3.10+
- `pip3 install flask flask-cors numpy cryptography` (display companion; numpy necesario para efectos de sonido, cryptography para TLS en LAN)
- `pip3 install pymupdf` (importación de campaña desde PDF — extracción consciente de columnas para que los módulos multi-columna se segmenten correctamente en capítulos; recae en `pdftotext` de poppler si no está)

---

## Instalación

Instálalo como plugin de Claude Code:

```
/plugin marketplace add neuralinitiative/claude-dnd-skill
/plugin install dm@neural-initiative
```

Después invócalo como **`/dm:dnd`** (los skills de plugin llevan namespace `plugin:skill` — el plugin `dm` provee el skill `dnd`), o simplemente describe lo que quieres una vez que una campaña está cargada. Actualiza con `/plugin update dm`.

```bash
# Opcional — instala las dependencias del display companion (una sola vez).
# El juego principal funciona sin esto; potencian la pantalla en vivo + audio.
pip3 install flask flask-cors numpy cryptography
```

> **¿Actualizando desde una instalación standalone v1?** Desde v2.0.0 el skill es
> solo-plugin — el viejo standalone `~/.claude/skills/dnd` (`/dnd`) es reemplazado por
> el plugin (`/dm:dnd`). **Tus campañas y personajes quedan intactos** — viven en
> `~/.claude/dnd/` (o `$DND_CAMPAIGN_ROOT`), completamente separados del
> código del skill. Instala el plugin de arriba, después corre el helper de una sola vez para trasladar
> los emparejamientos de dispositivo / certificados TLS y retirar la instalación vieja:
> `python3 <plugin>/skills/dnd/scripts/migrate_v1_to_v2.py`. Guía completa:
> **[MIGRATING.md](MIGRATING.md)**.

---

## Versionado y actualizaciones

El skill trackea releases vía un archivo `VERSION` de nivel superior y notas por release en [`CHANGELOG.md`](CHANGELOG.md). La versión actual está en `VERSION`; los cambios significativos — comandos nuevos, mecánicas nuevas, cambios de comportamiento — reciben una entrada en el CHANGELOG.

**Para chequear actualizaciones:**

```bash
/dm:dnd update --check    # muestra versión local vs. remota + diff de commits, sin pull
/dm:dnd update            # hace pull si estás atrás (solo fast-forward; se niega con árbol sucio)
```

**Las instalaciones como plugin se actualizan a través del gestor de plugins** — corre `/plugin update dm` en su lugar. `/dm:dnd update` detecta una instalación como plugin y te redirige ahí en vez de hacer git-pull bajo el estado trackeado del gestor.

La salida de `--check` incluye las cadenas de versión de ambos lados así puedes ver de un vistazo si te quedaste atrás. Después de actualizar, reinicia Claude Code para que carguen el nuevo `SKILL.md` y los procedimientos de comandos.

El skill sigue el [versionado semántico](https://semver.org/): `MAJOR.MINOR.PATCH`. Los cambios que rompen compatibilidad y requieren migración de datos de campaña suben MAJOR; las funciones nuevas opt-in suben MINOR; las correcciones de bugs suben PATCH. Las campañas activas siguen funcionando a través de subidas de MINOR/PATCH sin acción.

---

## Inicio Rápido

**Campaña improvisada** — Claude construye el mundo y genera un arco narrativo:

```
/dm:dnd new mi-campaña          # genera semilla de mundo, facciones, PNJ, arco de historia dinámico
/dm:dnd character new           # crea un personaje
/dm:dnd load mi-campaña         # empieza una sesión
```

**Campaña estructurada** — importa un módulo pre-escrito o publicado:

```
/dm:dnd import mi-campaña ruta/al/modulo.pdf   # extrae la estructura y construye los archivos de campaña
/dm:dnd load mi-campaña                        # empieza una sesión — Claude fuerza el arco
```

Una vez cargada, escribe con naturalidad — no hace falta el prefijo `/dm:dnd`. El DM interpreta todo como acción dentro del juego.

---

## Comandos de Campaña

| Comando | Descripción |
|---------|-------------|
| `/dm:dnd new <nombre>` | Crea una campaña nueva — genera semilla de mundo, PNJ, ubicación inicial, y arco narrativo dinámico |
| `/dm:dnd import <nombre> <fuente>` | Importa una campaña pre-escrita desde PDF, markdown, DOCX, o texto plano; extrae la estructura y construye todos los archivos de campaña |
| `/dm:dnd load <nombre>` | Carga una campaña existente y entra en modo DM |
| `/dm:dnd save` | Escribe los eventos de la sesión al log, actualiza el estado y los archivos de personaje |
| `/dm:dnd end` | Guarda la sesión, agrega el recap, detiene el display companion |
| `/dm:dnd abandon` | Sale sin guardar — descarta todos los cambios sin guardar de esta sesión |
| `/dm:dnd list` | Lista todas las campañas con fecha de última sesión y conteo |
| `/dm:dnd recap` | Recap en 3-5 oraciones en personaje de la última sesión |
| `/dm:dnd world` | Muestra el lore del mundo |
| `/dm:dnd quests` | Muestra las misiones activas y los hilos abiertos |
| `/dm:dnd arc status` | Muestra el arco narrativo actual, los beats completados, y las notas de dirección |
| `/dm:dnd arc advance <beat>` | Marca un beat como completo y actualiza el seguimiento del arco (solo arcos dinámicos) |
| `/dm:dnd arc revise` | Revisa los beats pendientes cuando una decisión de jugador redirige significativamente la historia |
| `/dm:dnd arc new` | Genera un arco nuevo a partir de las consecuencias de uno completado |
| `/dm:dnd autorun on [segundos]` | Activa el modo autorun — Claude conduce el ciclo de turnos automáticamente |
| `/dm:dnd autorun off` | Vuelve al modo manual |
| `/dm:dnd tutor on` | Activa el modo tutor / aprendizaje para esta sesión |
| `/dm:dnd tutor off` | Desactiva el modo tutor / aprendizaje |
| `/dm:dnd data sync` | Reconstruye el dataset SRD incluido desde las fuentes upstream (solo necesario para contenido upstream nuevo) |
| `/dm:dnd data status` | Muestra los conteos actuales de registros del dataset y el SHA upstream |
| `/dm:dnd update` | Trae los últimos cambios del skill desde `origin/main` (se niega con árbol sucio, solo fast-forward) |
| `/dm:dnd update --check` | Muestra la versión local-vs-remota y el diff de commits sin hacer pull |
| `/dm:dnd path [<nuevo>\|reset]` | Ve o reubica el almacenamiento de campaña vía `DND_CAMPAIGN_ROOT` |
| `/dm:dnd graph init` | Inicializa el grafo de relaciones de campaña (propone nodos y aristas semilla; pide aprobación) |
| `/dm:dnd graph scene-context --place <id> [--present id1,id2]` | Subgrafo enfocado para la escena actual; consulta primaria dentro de sesión |
| `/dm:dnd graph add-edge --from <id> --to <id> --type T --since N` | Registra un cambio de relación a mitad de sesión |
| `/dm:dnd graph close-edge --id <id> --at-session N` | Marca una arista como terminada (alianza rota, PNJ se mudó, etc.) |
| `/dm:dnd graph extract [--last-session-only]` | Corre una pasada de Haiku sobre el session-log para proponer aristas nuevas (revisar-y-aplicar) |

---

## Sistema de Arco Narrativo

Ambos modos de campaña usan la misma estructura de seis beats y tres actos trackeada en `state.md`. El tipo de arco determina cómo se puebla y se fuerza.

### Fundamentos estructurales

El arco dinámico toma de varios marcos superpuestos en estructura de historia y diseño de aventuras de mesa:

- **Estructura de tres actos** — la división clásica de planteamiento, confrontación, y resolución, presente en la teoría dramática desde Aristóteles hasta la escritura de guiones moderna. Los seis beats son dos por acto, dándole a cada fase un giro complicador en vez de un arco plano a través de ella.
- **El Círculo de Historia de Dan Harmon** — un motor de historia de 8 pasos (derivado del Viaje del Héroe de Campbell) que enfatiza a un personaje cruzando hacia una situación desconocida, encontrando algo, pagando un precio por tomarlo, y volviendo cambiado. Los beats de Cambio de Punto Medio y Todo Está Perdido son reflejos directos de esto — el momento en que la historia revela su forma real, y el costo que el protagonista debe pagar antes de poder actuar sobre ella.
- **Beats como consecuencias, no eventos** — la adaptación clave para el juego de mesa. En una historia guionada, un beat es una escena ("el héroe encuentra la carta"). En un arco de mesa, un beat es una consecuencia ("el grupo se da cuenta de que la amenaza fue construida para sobrevivir a cualquier persona"). Docenas de escenas distintas podrían entregar la misma consecuencia. Esto le da al DM flexibilidad genuina mientras mantiene comprometida la forma de la historia.
- **Estructura de aventura hub-and-spoke** — usada por el tipo de arco estructurado para módulos publicados no lineales. Los jugadores abordan cada ubicación-spoke en cualquier orden; cada spoke tiene sus propios beats de capítulo; el punto de convergencia central no abre hasta que todos los spokes requeridos se resuelven. Esto coincide con cómo se construyen realmente la mayoría de las campañas publicadas bien diseñadas y le permite a Claude forzar los beats a granularidad de capítulo sin forzar un camino lineal.

### Improvisado (tipo: dynamic)

Generado automáticamente en `/dm:dnd new` a partir de la amenaza, facciones, y las Tres Verdades del mundo. Los beats se definen por `what_changes` — la consecuencia narrativa que debe aterrizar — no por un evento específico. Esto le da al DM flexibilidad en *cómo* llega cada beat mientras se compromete a *que* debe llegar.

| Acto | Beat | Qué marca |
|-----|------|---------------|
| 1 | Incidente Incitador | La amenaza se vuelve personal |
| 1 | Complicación | El problema es más grande de lo que parecía al principio |
| 2 | Cambio de Punto Medio | Lo que el grupo pensaba que estaba haciendo cambia |
| 2 | Todo Está Perdido | Un revés genuino — algo falla o colapsa |
| 3 | Confrontación Final | El momento decisivo sobre el que gira la campaña |
| 3 | Resolución | Qué es distinto del mundo y los personajes después |

Los beats del arco se trackean en `/dm:dnd end` y se marcan completos vía `/dm:dnd arc advance`. Cuando una decisión de jugador importante redirige la historia, `/dm:dnd arc revise` actualiza los beats pendientes para que encajen en la nueva dirección. Cuando los seis beats se resuelven, `/dm:dnd arc new` genera un arco nuevo a partir de las consecuencias del primero — mismo mundo, nueva pregunta de historia.

### Estructurado (tipo: structured)

Poblado por `/dm:dnd import` a partir del material fuente. Los actos contienen beats clave a nivel de capítulo, escenas de anticipo (escenas de planteamiento que naturalmente acotan las decisiones hacia cada beat), y notas de ramificación. Claude anticipa antes de entregar cualquier beat requerido, guía con presión del mundo en vez de paredes duras cuando los jugadores se desvían, y marca los beats completos a medida que se resuelve cada capítulo.

Los dos tipos de arco son mutuamente excluyentes por campaña y totalmente compatibles con todos los demás sistemas — combate, XP, actitudes de PNJ, y display se comportan idénticamente sin importar el tipo de arco.

---

## Comandos de Personaje

| Comando | Descripción |
|---------|-------------|
| `/dm:dnd character new` | Crea un personaje — point buy guiado o stats tirados |
| `/dm:dnd character sheet [nombre]` | Muestra una hoja de personaje |
| `/dm:dnd level up [nombre]` | Sube de nivel a un personaje — aplica rasgos de clase, tirada de PG |

### Creación de Personaje

El flujo de creación recorre:
1. Nombre, raza, clase, trasfondo
2. **Point buy** (valida contra el presupuesto de 27 puntos) o **tirado** (3 arreglos de 4d6kh3 para elegir)
3. Bonificaciones raciales aplicadas automáticamente
4. Stats derivados calculados vía `character.py`
5. Equipo inicial asignado por clase + trasfondo
6. Hoja escrita en `characters/<nombre>.md`

---

## Sistema de Combate

```
/dm:dnd combat start
```

1. Identifica a todos los combatientes, recoge mods de DES, PG, CA
2. Auto-tira iniciativa para **cada combatiente** incluyendo PJ — resultados enviados al display
3. Trackea PG, condiciones, orden de turnos a través de las rondas
4. Resuelve ataques de PNJ/monstruo en línea con matemática de dados completa:
   ```
   Goblin attacks: d20(14) + 4 = 18 vs AC 16 — hit! 1d6(3) + 2 = 5 piercing
   ```
5. Las tiradas de ataque/habilidad/salvación de PJ siguen el modo de tirada de la campaña (ver [Manejo de Dados y Tiradas](#manejo-de-dados-y-tiradas)) — bajo el modo por defecto `players` el DM pide cada tirada de PJ por nombre y espera; bajo `auto` las tira abiertamente. El DM siempre resuelve las tiradas de PNJ/monstruo.

### Display de Combate

Durante el combate la barra lateral muestra un orden de turnos en vivo con un puntero `▶`:

```
— COMBATE — Ronda 2
▶ Aldric
  Esqueleto
  Mira
```

El puntero avanza después de cada turno. Las barras de PG se actualizan en tiempo real cuando se recibe daño. El combate termina con `--turn-clear`.

---

## Manejo de Dados y Tiradas

Cómo se tiran los propios d20 de un jugador (ataques, chequeos, salvaciones, tiradas de muerte) se elige **al inicio de la partida** y se guarda como `roll_mode` en `state.md → ## Session Flags`. Tanto `/dm:dnd new` como `/dm:dnd load` preguntan **"¿Tiradas de dados?"** así lo confirmas cada sesión.

| Modo | Comportamiento |
|------|------|
| **`players`** (por defecto) | El DM pide cada d20 de PJ **por nombre y espera** el resultado del jugador — nunca tira por el personaje de un jugador. Si una tirada no vuelve (ej. el servidor de dados físicos por teléfono está caído) el DM pide el número en voz alta en vez de tirar automáticamente en silencio. |
| **`auto`** | El DM tira los d20 de PJ abiertamente con la matemática completa mostrada en línea (`Piper — Percepción: d20+5 = 18`), sin esperar. Bueno para juego en solitario o rápido. |

**La iniciativa siempre la tira el DM** para cada combatiente (PJ y PNJ) sin importar el modo, así como todas las tiradas de PNJ/monstruo.

**Override por jugador** — un jugador puede cambiar solo su propio personaje vía el toggle **Configuración → Tiradas** del teléfono. Eso hace POST a `/roll-pref`, y el DM respeta una directiva `[[<Personaje> roll mode: …]]` para ese personaje, sobrescribiendo el default de campaña. Precedencia: **toggle por personaje > `roll_mode` de campaña**.

> Esto reemplaza la vieja asunción de "los jugadores siempre tiran lo suyo": el DM ya no recae en un resultado auto-tirado `[auto]` para un PJ cuando el servidor de dados no está disponible. El manejo de tiradas ahora es explícito y forzado.

---

## Sistema de PNJ

```
/dm:dnd npc Osk             # interpreta un PNJ existente o genera uno nuevo
/dm:dnd npc attitude Osk friendly   # cambia la actitud en la escala de 5 pasos
```

Cada PNJ recibe: rol, stat block, comportamiento, motivación, secreto, y una peculiaridad de habla. Las actitudes cambian en una escala de 5 pasos: `hostile → unfriendly → neutral → friendly → allied`. Los cambios se registran con razón y fecha en `npcs.md`.

---

## Descansos

```
/dm:dnd rest short    # 1 hora — gasta Dados de Golpe, recarga algunos rasgos
/dm:dnd rest long     # 8 horas — PG completos, la mitad de Dados de Golpe de vuelta, todos los espacios de conjuro
```

Los descansos largos avanzan el reloj del mundo en `state.md`.

---

## Display Companion Cinemático

Un servidor web local opcional (`display/dnd-display-app.py`) que renderiza la narración del DM en cualquier pantalla — TV, tablet, teléfono, o segundo monitor. Proyéctalo, duplícalo, o ábrelo en cualquier dispositivo de tu red local.

### Configuración

```bash
pip3 install flask flask-cors numpy cryptography
```

### Arrancando el Display

El display arranca automáticamente cuando respondes **y** al prompt de `/dm:dnd load`. O arráncalo manualmente:

```bash
# Solo local (Mac/misma máquina) — HTTP, sin configuración de certificado
bash ${CLAUDE_SKILL_DIR}/display/start-display.sh

# Modo LAN — HTTP, accesible para teléfonos/tablets en tu red
bash ${CLAUDE_SKILL_DIR}/display/start-display.sh --lan

# Modo LAN con TLS — para redes públicas o no confiables
bash ${CLAUDE_SKILL_DIR}/display/start-display.sh --lan --tls
```

Después abre `http://localhost:5001` en tu navegador. HTTP es el default — sin advertencias de certificado. Para dispositivos LAN usa la URL con IP impresa al arrancar (ej. `http://192.168.1.x:5001`). Usa `--tls` solo cuando la red es pública o no confiable.

### Opciones de Visualización

Abre la URL del display en un navegador, después elige cómo mostrarlo:

| Opción | Cómo |
|--------|-----|
| **TV — Proyectar pestaña** | Chrome → menú de tres puntos → Cast → Cast tab; selecciona tu Chromecast o smart TV |
| **TV — Duplicar pantalla** | macOS: Centro de Control → Duplicar Pantalla → Apple TV / receptor AirPlay |
| **iPad / tablet** | Arranca con `--lan`, abre `http://<tu-ip>:5001` en Safari o Chrome; funciona apaisado |
| **Segundo monitor** | Abre `http://localhost:5001` en una ventana del navegador y arrástrala al segundo display |

### TLS / HTTPS (opcional)

HTTP es el default. Usa `--tls` solo cuando la red es pública o no confiable. Cuando se pasa `--tls` a `start-display.sh`:
- Se auto-genera un certificado autofirmado (validez de 10 años) si `cert.pem` todavía no está presente
- Un servidor HTTP plano arranca en `:8080` para servir `cert.pem` para descarga
- Se imprimen en la terminal instrucciones de instalación por plataforma (iOS, Android, Mac)

Para iOS: abre `http://<tu-ip>:8080/cert.pem` en Safari → toca Permitir → Configuración → General → VPN y Gestión de Dispositivos → instala el perfil → Configuración de Confianza de Certificado → activa confianza completa.

### Input de Jugador desde la UI del Companion

![Player input panel — staging an action from a phone](screenshots/screenshot-player-input.png)

Los jugadores abren el companion en el navegador de su teléfono. Cada dispositivo se vincula a un personaje del grupo, y la vista de input muestra el flujo de turno de ese jugador como una **franja de estado** simple así siempre saben dónde está su turno.

1. **Escribir y enviar** — el staging es de **un toque**. La acción se envía al DM inmediatamente (auto-lista) — sin un paso separado de Preparar / Marcar Lista. **Saltar** pasa el turno sin escribir.
2. **Enviado → recibido** — la franja pasa a *Enviado al DM*, después a un toast de **confirmación** en el momento en que el DM realmente recoge la acción de la cola (no solo cuando se prepara), después a *el DM está narrando…*, y vuelve a *tu turno*. Esto cierra el loop así un jugador siempre puede saber si su turno entró.

> Nota de estado de traducción: el texto exacto de esta franja (`_PS_TEXT` en `index.html`) todavía se muestra en inglés en tiempo de ejecución — quedó fuera del alcance cubierto en la Fase 4 (CLA-9) y está reportado como pendiente de seguimiento. El flujo conceptual de estados es el descrito arriba.

El panel muestra un reloj circular de cuenta regresiva **"Próximo Turno"** que se repite en el intervalo de autorun configurado.

**La aprobación de dispositivo confía por defecto en cualquier dispositivo de tu LAN** — conveniente para una red hogareña casual. Configura `DND_REQUIRE_APPROVAL=1` para restaurar la compuerta de aprobar/rechazar por dispositivo en redes públicas o no confiables.

### Configuración de Jugador (teléfono)

Cada dispositivo tiene una vista de **Configuración** con controles que ajustan la experiencia para ese jugador o para toda la mesa:

| Control | Qué hace |
|---------|---------------|
| **Tamaño de Texto** (`A−` / `A+`, clic en el % para resetear) | Escala la columna de lectura vía un multiplicador de tamaño de fuente (tamaño de fuente, no zoom de página) así la narración se mantiene legible desde el otro lado de la sala vía Chromecast. Persiste por navegador (`localStorage`), aplicado anti-FOUC. |
| **Narración** slider (250–2500 palabras) | Fija el objetivo de conteo de palabras al que apunta el DM cada turno. Hace POST a `/narration-pref`; la próxima acción en cola lleva una directiva `[[Narration length…]]` que el DM respeta como presupuesto duro por turno. Perilla rápida "mantén los turnos cortos" para mesas con presión de tiempo. |
| **Tiradas** toggle (se muestra cuando el dispositivo está vinculado a un PJ) | Cambia ese personaje entre *Jugadores* (tiras tus propios d20) y *Auto-tirar* (el DM los tira abiertamente), sobrescribiendo el default de campaña para ese personaje puntual. Ver [Manejo de Dados y Tiradas](#manejo-de-dados-y-tiradas). |
| **Efectos de Sonido** toggle | Activa los SFX del lado del navegador (ver [Efectos de Sonido](#efectos-de-sonido)). |

### Modo Autorun

Autorun es la forma principal de correr sesiones con la UI del companion. Una vez activado, Claude conduce el ciclo de turnos sin requerir que el DM presione Enter entre cada turno.

```
/dm:dnd autorun on          # activa — cuenta regresiva de 60s por defecto
/dm:dnd autorun on 45       # activa con cuenta regresiva de 45 segundos
/dm:dnd autorun off         # vuelve al modo manual
```

La cuenta regresiva es configurable por campaña fijando `autorun_interval: N` en `state.md → ## Session Flags`. Para interrumpir autorun desde la CLI de Claude Code, presiona **Ctrl+C** durante la espera.

**Umbral de N jugadores** — por defecto autorun se dispara cuando todos los jugadores conocidos están listos. Para grupos multi-dispositivo puedes requerir solo N jugadores:

```bash
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-threshold 2  # dispara cuando 2 están listos
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --autorun-threshold 0  # resetea al conteo de jugadores
```

### Ayuda del DM y Modo Tutor

Hay dos formas de mostrar pistas y advertencias en el display — un botón bajo demanda y un modo automático por sesión.

**Botón de Ayuda del DM (◈)** — un botón **◈ Ayuda del DM** está siempre en la esquina inferior derecha del display. Haz clic y en unos segundos se genera una pista o advertencia contextual a partir de la escena actual y se envía al display — sin comando de CLI necesario, sin sobrecarga de tokens por turno. El botón lee los últimos 8 bloques del display y el estado actual de campaña, llama a Claude en modo no interactivo, y envía el resultado como un bloque de pista vía el pipeline SSE normal. Muestra "Pensando…" mientras está en vuelo; se resetea automáticamente cuando llega el bloque. Múltiples clics simultáneos solo disparan una ejecución.

Los bloques de pista están **colapsados por defecto** — haz clic o toca el encabezado para expandir. Las advertencias usan un borde ámbar:

- **Pista del DM** (◈, colapsable) — habilidades que vale la pena intentar, opciones visibles, qué podría costar cada camino
- **Advertencia** (⚠, borde ámbar) — marca decisiones irreversibles antes de que el jugador se comprometa

![Tutor mode intro hint](screenshots/tutor-hint-intro.png)

Las pistas pueden mostrar conocimiento contextual de PNJ y situación que el DM naturalmente marcaría:

![Tutor hint with NPC context](screenshots/tutor-hint-npc.png)

Las advertencias usan un borde ámbar para distinguir decisiones de alto riesgo:

![Tutor warning block](screenshots/tutor-warning.png)

**Modo tutor (por sesión)** — para jugadores nuevos que quieren guía continua, activa bloques de pista automáticos después de cada escena, punto de decisión, y tirada — sin necesidad de botón. Agrega ~10–20% de sobrecarga de tokens por turno. Usa el botón de Ayuda del DM en su lugar para pistas bajo demanda sin el costo continuo.

```
/dm:dnd tutor on    # activa para esta sesión
/dm:dnd tutor off   # desactiva
```

El modo tutor está acotado a la sesión — no persiste al siguiente `/dm:dnd load` a menos que se active de nuevo.

Los dos son independientes — el botón ◈ siempre está disponible sin importar si el modo tutor está activo.

---

### Detección de Escenas

El servidor escanea el texto de narración en busca de palabras clave y hace un crossfade del gradiente de fondo y el tipo de partícula para que coincidan con el ambiente actual. Las escenas cambian automáticamente a medida que avanza la historia. La detección matchea tanto en inglés como en español (ver Fase 5 / CLA-10) — la tabla de abajo muestra una muestra de las palabras clave en español; cada escena también reconoce sus equivalentes en inglés.

| Escena | Palabras clave de muestra (ES) | Partículas |
|-------|-----------------|-----------|
| La Posada | taberna, posada, chimenea, cerveza, tabernero | brasas |
| La Mazmorra | mazmorra, calabozo, corredor, antorcha, reja de hierro | polvo |
| La Mina | mina, veta, pozo, túnel, mineral | polvo |
| La Caverna | cueva, caverna, estalactita, subterráneo, gruta | niebla |
| El Bosque | bosque, árbol, rama, hojas, maleza | hojas |
| El Castillo | castillo, muralla, almena, torreón, trono | polvo |
| Las Montañas | montaña, nieve, cima, ventisca, glaciar | nieve |
| El Mar | océano, mar, barco, oleaje, marinero | ondas |
| El Desierto | desierto, arena, duna, árido, espejismo | arena |
| Las Ruinas | ruinas, derrumbe, escombros, antiguo, olvidado | polvo |
| El Pantano | pantano, ciénaga, barro, fétido, estancado | niebla |
| La Cripta | cripta, tumba, sepultura, no-muerto, sarcófago | humo |
| El Fuego | fuego, llama, incendio, brasa, ceniza | brasas |
| Lo Arcano | arcano, magia, hechizo, runa, glifo | chispas |
| El Pueblo | mercado, calle, multitud, plaza, distrito | lluvia |
| La Noche | noche, medianoche, luna, estrella, constelación | estrellas |
| El Templo | templo, santuario, altar, sagrado, capilla | humo |

Las transiciones de escena hacen crossfade a lo largo de ~2.5 segundos. El servidor mantiene una ventana móvil de 20 fragmentos para la detección así las escenas no parpadean con coincidencias de una sola palabra clave.

### Canvas de Cielo Dinámico

Una capa de canvas renderizada sobre el fondo de la escena muestra un cielo en vivo que reacciona a los datos de `world_time` enviados vía `push_stats.py`:

- **Hora del día** — el sol arquea desde el amanecer (abajo-izquierda) a través del mediodía (arriba-centro) hasta el atardecer (abajo-derecha); cambia a luna creciente + estrellas titilantes de noche; el crepúsculo muestra un horizonte anaranjado
- **Clima** — calmo: 2 nubes livianas; nublado: 5 nubes oscuras pesadas, sol atenuado; lluvioso: cobertura de nubes densa, paleta apagada; tormentoso: cielo casi negro; noche despejada: campo de estrellas completo
- **Nubes** — 5 objetos de nube cada uno construido con 8 círculos superpuestos; van a la deriva lentamente y envuelven

Envía los datos de tiempo del mundo después de cargar una campaña y después de cualquier descanso o avance de tiempo:

```bash
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --world-time \
  '{"date":"7 Deepmonth 1312 CR","day_name":"Starday","time":"morning","season":"Deep Winter","weather":"overcast"}'
```

Valores válidos de `time`: `dawn`, `morning`, `midday`, `afternoon`, `evening`, `dusk`, `night`
Valores válidos de `weather`: `calm`, `clear`, `overcast`, `rainy`, `stormy`

### Efectos de Sonido

El texto de narración se escanea del lado del servidor en busca de 12 categorías de triggers de SFX. Cuando se encuentra una coincidencia, el navegador trae un archivo WAV sintetizado y lo reproduce vía Web Audio API — sin salida de audio del servidor, funciona en cualquier dispositivo con la pestaña abierta.

```
impact · sword · arrow · shout · thud · magic · coins · door · low_hum · fire · breath
```

La síntesis de SFX usa numpy — si numpy no está instalado la función se degrada en silencio. Actívalo vía el toggle de **Efectos de Sonido** arriba a la derecha del display.

| Texto de narración | SFX |
|----------------|-----|
| "...golpea el escudo..." | impact |
| "...desenvaina su espada..." | sword |
| "...dispara una flecha..." | arrow |
| "...ruge a través del muelle..." | shout |
| "...se desploma al piso..." | thud |
| "...la energía arcana crepita..." | magic |
| "...las monedas se desparraman sobre la mesa..." | coins |
| "...la puerta cruje al abrirse..." | door |
| "...el altar zumba con energía..." | low_hum |
| "...la antorcha llamea..." | fire |
| "...una exhalación aguda..." | breath |

El navegador cachea cada WAV después del primer fetch. Los SFX se disparan naturalmente junto con la animación de máquina de escribir ya que ambos se conducen por los mismos fragmentos de narración.

La detección de triggers es específica por idioma — un paquete en español (`es`) viene incluido junto al de inglés (`en`), y de hecho el skill trae paquetes para los 24 idiomas soportados por Gemini. Las campañas nuevas usan `sfx_languages: es` por defecto en `state.md → ## Session Flags` (este fork narra en español por defecto; ver `CLAUDE.md`). Sobrescribe con una lista separada por comas, ej. `sfx_languages: en` o `sfx_languages: es,en` (se chequean en orden, la primera coincidencia gana). `state.md` tiene precedencia siempre que el campo esté presente — un default a nivel de entorno vía `DND_SFX_LANGUAGES` solo aplica a campañas que omiten el campo por completo.

### Barra Lateral de Personaje en Vivo

![NPC dialogue block and character sidebar with faction panel](screenshots/screenshot-npc-dialogue.png)

Una barra lateral fija a la izquierda muestra estadísticas en vivo de todos los miembros del grupo, actualizadas automáticamente a medida que avanza la partida.

```bash
# Envía las stats completas al cargar la campaña (limpia personajes obsoletos de campañas previas)
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --replace-players --json '{
  "players": [{
    "name": "Aldric", "race": "Human", "class": "Fighter", "level": 2,
    "hp": {"current": 14, "max": 18}, "xp": {"current": 220, "next": 300},
    "ac": 17, "initiative": "+1", "speed": 30,
    "hit_dice": {"remaining": 2, "max": 2, "die": "d10"},
    "ability_scores": {
      "str": {"score": 16, "mod": "+3"}, "dex": {"score": 12, "mod": "+1"},
      "con": {"score": 15, "mod": "+2"}, "int": {"score": 10, "mod": "+0"},
      "wis": {"score": 11, "mod": "+0"}, "cha": {"score": 13, "mod": "+1"}
    }
  }]
}'

# Actualizaciones parciales durante la partida
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Aldric --hp 10 18
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Aldric --xp 270 300
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Aldric --conditions-add "Poisoned"
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --player Aldric --slot-use 2

# O agrupa los cambios de stats directamente con un envío de narración (sin llamada separada a push_stats.py):
python3 ${CLAUDE_SKILL_DIR}/display/send.py \
  --stat-hp "Aldric:10:18" \
  --stat-condition-add "Aldric:Poisoned" \
  --stat-slot-use "Aldric:1" << 'EOF'
The goblin's blade catches Aldric across the ribs...
EOF

# Orden de turnos de combate
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py \
  --turn-order '{"order":["Aldric","Skeleton","Mira"],"current":"Aldric","round":1}'

# Avanza el puntero de turno
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-current "Skeleton"

# Combate terminado
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --turn-clear

# Reloj de tiempo del mundo
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --world-time \
  '{"date":"7 Deepmonth 1312 CR","day_name":"Starday","time":"morning","season":"Deep Winter","weather":"overcast"}'
```

![Character sidebar card](screenshots/sidebar-card.png)

### Hoja de Personaje Clickeable

Haz clic o toca cualquier tarjeta de personaje en la barra lateral para abrir un modal de hoja de personaje completa — ataques, rasgos, e inventario de un vistazo. Funciona en desktop y en teléfonos/tablets conectados vía LAN.

![Character sheet modal](screenshots/character-sheet-modal.png)

Incluye el campo `sheet` al enviar las stats en `/dm:dnd load` para poblar la hoja completa:

```bash
python3 ${CLAUDE_SKILL_DIR}/display/push_stats.py --replace-players --json '{
  "players": [{
    "name": "Aldric",
    ...
    "sheet": {
      "attacks": [
        {"name": "Longsword", "bonus": "+5", "damage": "1d8+3", "type": "Slashing", "notes": "Versatile (1d10)"}
      ],
      "features": [
        {"name": "Second Wind", "text": "Bonus action: regain 1d10+level HP. Short/long rest recharge."}
      ],
      "inventory": ["Longsword", "Chain Mail", "Shield", "Explorer'\''s Pack", "15 gp"]
    }
  }]
}'
```

Si se omite `sheet`, el modal igual abre pero solo muestra las stats visibles en la barra lateral. Cierra con **Esc**, haciendo clic afuera del panel, o el botón ✕.

Hacer clic en el nombre de un conjuro o rasgo dentro de la hoja abre un modal de descripción tomado del dataset SRD incluido. Las progresiones escalables (ej. el daño de Ataque Furtivo) se colapsan automáticamente al nivel actual del personaje. Si un conjuro o rasgo no está en el dataset SRD central, se muestra en su lugar un link a la página correspondiente en D&D 5e Wiki. Para extender el dataset local con contenido no-SRD desde un archivo de personaje:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/build_supplemental.py --character ~/.claude/dnd/campaigns/<nombre>/characters/<nombrepersonaje>.md
```

Esto trae descripciones de dnd5e.wikidot.com para cualquier entrada faltante y las escribe en `data/dnd5e_supplemental.json`. Córrelo una vez después de crear o importar un personaje. Un suplemento pre-construido cubriendo Circle of Spores, rasgos de arquetipo Thief, y varios conjuros de Xanathar's viene incluido con el skill.

La barra lateral:
- Muestra tarjetas compactas de doble columna para grupos de 2+ (grilla completa de habilidades para juego en solitario)
- Las barras de PG cambian de verde → amarillo → rojo a medida que bajan los PG
- La barra de XP se llena hacia el próximo nivel
- Las condiciones activas se muestran por personaje
- Los indicadores de espacio de conjuro trackean las cargas restantes
- Aparece con fade automáticamente en el primer envío de stats
- Persiste a través de reinicios de Flask (`stats.json`)
- Se limpia automáticamente en `/dm:dnd new` (campaña nueva)

### Buffer de Repetición

El servidor buffea los últimos 60 fragmentos de texto a disco (`text_log.json`). Los navegadores que se reconectan (corte de Chromecast, refresh de pestaña) repiten el historial completo de la sesión automáticamente — no se pierde narración.

---

## Referencia de Scripts

Todos los scripts viven en `${CLAUDE_SKILL_DIR}/scripts/`.

### `dice.py` — Todas las tiradas de dados

```bash
python3 scripts/dice.py d20+5
python3 scripts/dice.py 2d6+3
python3 scripts/dice.py d20 adv          # ventaja
python3 scripts/dice.py d20+3 dis        # desventaja + modificador
python3 scripts/dice.py 4d6kh3          # se queda con los 3 mejores (tirada de puntaje de característica)
python3 scripts/dice.py d20 --silent    # solo entero (para tiradas ocultas)
```

Marca automáticamente 20 natural (`GOLPE CRÍTICO`) y 1 natural (`PIFIA`).

### `ability-scores.py` — Creación de personaje

```bash
python3 scripts/ability-scores.py roll                          # 3 arreglos para elegir
python3 scripts/ability-scores.py pointbuy                     # imprime la tabla de costos
python3 scripts/ability-scores.py pointbuy --check STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
python3 scripts/ability-scores.py modifiers STR=15 DEX=10 CON=15 INT=8 WIS=11 CHA=12
```

### `combat.py` — Iniciativa y resolución de ataques

```bash
# Tira iniciativa para todos los combatientes e imprime el tracker
python3 scripts/combat.py init '[
  {"name":"Aldric","dex_mod":1,"hp":18,"ac":17,"type":"pc"},
  {"name":"Skeleton","dex_mod":2,"hp":13,"ac":13,"type":"npc"}
]'

# Reimprime el tracker desde el estado guardado
python3 scripts/combat.py tracker '<state_json>' <numero_ronda>

# Resuelve un ataque individual
python3 scripts/combat.py attack --atk 5 --ac 13 --dmg 1d8+3
```

`init` genera una línea `STATE_JSON:` — guarda esto en `state.md` bajo `## Active Combat` para persistencia entre turnos.

### `build_supplemental.py` — Extiende el dataset SRD con contenido no-SRD

Corre esto después de crear o importar un personaje para traer descripciones de conjuros y rasgos que no están en el SRD central:

```bash
# Escanea un archivo de personaje y trae lo que falte
python3 scripts/build_supplemental.py --character ~/.claude/dnd/campaigns/<nombre>/characters/<nombrepersonaje>.md

# Escanea todos los personajes de una campaña de una vez
python3 scripts/build_supplemental.py --campaign <nombre-campaña>

# Agrega una entrada específica por nombre
python3 scripts/build_supplemental.py --add "Toll the Dead" spell
python3 scripts/build_supplemental.py --add "Halo of Spores" feature

# Ve qué hay actualmente en caché
python3 scripts/build_supplemental.py --list

# Previsualiza qué se traería sin escribir
python3 scripts/build_supplemental.py --campaign <nombre> --dry-run
```

Trae de `dnd5e.wikidot.com` con una demora de solicitud cortés. Usa solo la stdlib de Python — sin dependencias extra. Escribe en `data/dnd5e_supplemental.json`, que `lookup.py` mergea al cargar.

---

### `character.py` — Derivación de stats y subida de nivel

```bash
# Stat block completo a partir de puntajes crudos
python3 scripts/character.py calc --class fighter --level 2 \
    STR=16 DEX=12 CON=15 INT=10 WIS=11 CHA=13 \
    --proficient STR CON Athletics Intimidation Perception Survival

# Subida de nivel
python3 scripts/character.py levelup --class fighter --from 2 --hp-roll 8 --con-mod 2

# Seguimiento de XP
python3 scripts/character.py xp --level 2 --gained 150
```

---

## Estructura de Archivos

```
${CLAUDE_SKILL_DIR}/
├── SKILL.md                  # Definición del skill e instrucciones del DM
├── SKILL-scripts.md          # Referencia de sintaxis de scripts y herramientas
├── SKILL-commands.md         # Procedimientos de comandos /dm:dnd
├── README.md                 # Este archivo
├── data/
│   ├── dnd5e_srd.json        # Dataset SRD 5e incluido (1453 registros — conjuros, rasgos, equipo, monstruos)
│   └── dnd5e_supplemental.json  # Contenido no-SRD (Xanathar's, rasgos de subclase, etc.)
├── scripts/
│   ├── dice.py
│   ├── ability-scores.py
│   ├── combat.py
│   ├── character.py
│   ├── tracker.py
│   ├── calendar.py
│   ├── lookup.py             # API de consulta SRD + suplementario
│   ├── build_srd.py          # Trae datos 5e upstream y construye dnd5e_srd.json
│   ├── sync_srd.py           # Chequea SHAs upstream; reconstruye solo con commits nuevos
│   └── build_supplemental.py # Trae entradas no-SRD de wikidot para un personaje o campaña
├── display/
│   ├── dnd-display-app.py    # Servidor Flask SSE
│   ├── audio.py              # Síntesis de SFX y trigger de navegador (numpy)
│   ├── autorun_wait.py       # Espera bloqueante para modo autorun (seguro para TCC, python puro)
│   ├── check_input.py        # Consulta no bloqueante de la cola de input de jugador (chequeo a mitad de turno)
│   ├── send.py               # Envío directo de narración/dados/acciones de jugador
│   ├── push_stats.py         # Actualizaciones de stats de personaje y combate
│   ├── setup_tls.py          # Generador de certificado TLS autofirmado para modo LAN
│   ├── start-display.sh      # Arranque del display con un solo comando
│   ├── dm_help.py            # Generador de pista de DM bajo demanda (botón ◈)
│   ├── wrapper.py            # Wrapper PTY (legacy — se prefiere autorun)
│   ├── requirements.txt
│   └── templates/
│       └── index.html        # Frontend de navegador
└── templates/
    ├── character-sheet.md
    ├── state.md
    ├── world.md
    ├── npcs.md
    └── session-log.md

~/.claude/dnd/campaigns/<nombre>/
├── state.md                  # Ubicación actual, estado del grupo, misiones activas, seguimiento del arco
├── world.md                  # Lore del mundo, detalles del setting, nodos de aventura
├── npcs.md                   # Índice de PNJ con stat blocks y actitudes
├── session-log.md            # Historial de sesión y recaps (últimas 2 sesiones; las más viejas se archivan)
├── session-log-archive.md    # Archivo completo del historial de sesión
├── session_tail.json         # Cola del display de la última sesión — se repite al cargar
└── characters/
    ├── Aldric.md
    └── Mira.md
```

---

## Filosofía del DM

El skill está diseñado alrededor de un conjunto de restricciones duras, no de notas aspiracionales:

- **Improvisar por sobre guionar** — el mundo es una sandbox; las decisiones de jugador siempre encuentran un "sí, y..."
- **Las consecuencias son reales** — los PNJ recuerdan conversaciones; las facciones cambian; el fracaso es posible
- **Economía de descripción** — dos detalles sensoriales precisos ganan a un párrafo de exposición
- **Cada PNJ es una persona** — hasta los personajes menores tienen un tic verbal, una contradicción, un objetivo
- **Las tiradas ocultas se mantienen ocultas** — Percepción, Perspicacia, y Sigilo se tiran en silencio; solo se narra el desenlace (pero los resultados siempre aparecen en el display)
- **El arco se dobla, nunca se rompe** — cuando los jugadores redirigen la historia, los beats se revisan para encajar en la nueva dirección; la forma comprometida es una guía, no una jaula
- **Se calibra a este jugador específico a través de las sesiones** — las Notas de Estilo del DM acumulan patrones específicos de la mesa a partir de feedback de calibración; qué funciona para este grupo, qué divide a la mesa, en qué apoyarse; se leen en cada carga de sesión y se actualizan en cada final
- **El mundo se mueve entre sesiones** — las facciones actúan mientras el grupo está ocupado; los PNJ persiguen sus propios objetivos; las puertas que se derribaron siguen rotas; el jugador llega a un mundo con peso, no a una escena que quedó pausada esperándolo

---

## Ruleset

Cada campaña declara su ruleset en la línea de encabezado de `state.md`: `**Ruleset:** 2014` (SRD 5.1) o `**Ruleset:** 2024` (SRD 5.2). `/dm:dnd new` pregunta por el ruleset al crear; `/dm:dnd load` lee el campo en cada sesión. Las campañas legacy (anteriores al campo) usan **2014** por defecto y se les ofrece una migración de una sola vez con un backup con timestamp.

### Dataset 2014 (por defecto)

`data/dnd5e_srd.json` — construido a partir de `5e-bits/5e-database` (rama `main`, SRD 2014) y `foundryvtt/dnd5e` (rama `master`). 1,453 registros: 319 conjuros, 237 equipo, 362 objetos mágicos, 15 condiciones, 334 monstruos, 186 rasgos.

### Dataset 2024 (opt-in)

`data/dnd5e_srd_2024.json` — construido a partir de `5e-bits/5e-database` (`src/2024/en/`), `foundryvtt/dnd5e` (`packs/_source/spells24/`, `packs/_source/actors24/`, `packs/_source/classfeatures24/`). Todo el contenido de foundry es CC-BY-4.0, con procedencia `_source` y `_license` preservada en cada registro. Aproximadamente 1,420+ registros: 341 conjuros nativos 2024, 376 monstruos nativos 2024, 8 propiedades de maestría de arma, 9 especies, 24 subespecies, 17 dotes de origen/generales/de estilo de combate, 4 trasfondos, más equipo / objetos mágicos / rasgos. Construilo con `python3 scripts/build_srd.py --ruleset 2024` (una sola vez, ~3 min).

### Diferencias mecánicas aplicadas en la mesa

| Mecánica | 2014 | 2024 |
|---|---|---|
| Momento de subclase | varía por clase (1/2/3) | nivel 3 universalmente |
| Fuente de ASI | raza | trasfondo |
| Dote de origen | n/a | otorgada al nivel 1 por el trasfondo |
| Maestría de arma | n/a | 8 propiedades (Vex, Topple, Sap, Cleave, Graze, Nick, Push, Slow) |
| Agotamiento | tabla de 6 niveles con efectos variados | 1 nivel = -2 a todas las tiradas de d20 (acumulativo); muerte en el nivel 6 |
| Desventaja de sigilo en armadura pesada | sí | sí (sin cambios) |
| Alcance de palabra sanadora | 18 m | 18 m (sin cambios) |

La resolución de combate, la tirada de dados, la iniciativa, la derivación de CA/PG, las tablas de XP, el escalado de daño de trucos, y la recuperación en descansos son idénticos entre ediciones y no requieren ramificación por ruleset en el motor.

### Compatibilidad hacia atrás

Las campañas existentes siguen cargando sin cambios. La primera vez que se carga una campaña legacy bajo el nuevo camino de código, `migrate_ruleset.py` detecta el campo faltante `**Ruleset:**` y le pregunta al DM. El migrador:

- Respalda `state.md` a `state.md.backup-pre-ruleset-<timestamp>` antes de cualquier escritura
- Inyecta el ruleset elegido en la línea de encabezado
- Es idempotente — volver a correrlo en una campaña ya migrada es un no-op limpio
- Tiene un modo `--check` para detección no mutante (usado por `/dm:dnd load`)

Los archivos de personaje heredan el ruleset de su campaña en tiempo de ejecución vía `paths.campaign_ruleset()`; no se requiere migración por personaje. El display companion auto-detecta el ruleset de la campaña y lo muestra como una pequeña insignia en el cluster del reloj del mundo.

Si quieres cambiar una campaña legacy a 2024, corre el migrador manualmente:

```bash
python3 scripts/migrate_ruleset.py <nombre-campaña> --ruleset 2024 --yes
```

Nota: cambiar una campaña 2014 en curso a 2024 a mitad de arco no es recomendable — las builds de personaje (dotes de origen, ASI de trasfondo, maestría de arma para clases marciales) quedaron fijadas bajo reglas 2014. El migrador simplemente estampa el campo; reconstruir los personajes bajo 2024 es un ejercicio manual aparte.

---

## Licencia

[AGPL-3.0-or-later](LICENSE). Copyright (c) 2026 Neural Initiative LLC.

El auto-hosting y la modificación son explícitamente bienvenidos — forkea, corre, cambia como quieras. La AGPL protege específicamente contra re-alojar esto como un SaaS de código cerrado sin compartir las modificaciones de vuelta. Para la mayoría de los usuarios esta distinción nunca importa.

# Migrar de v1 (skill standalone) a v2 (plugin)

**v2.0.0 hace que el skill de D&D sea solo-plugin.** La instalación standalone
(`~/.claude/skills/dnd`, invocada como `/dnd`) es reemplazada por el plugin de
Claude Code `dm@neural-initiative`, invocado como **`/dm:dnd`**.

## TL;DR — tus campañas están a salvo

Tus datos de campaña **nunca estuvieron dentro del skill.** Viven en la raíz de
datos (`~/.claude/dnd`, o donde apunte `$DND_CAMPAIGN_ROOT`) y se leen de la
misma forma tanto por el skill standalone viejo como por el plugin nuevo.
Personajes, campañas e historial necesitan **cero migración** — ambas
versiones ya los comparten.

La migración son solo dos pasos:

```text
1. Instalá el plugin
   /plugin marketplace add neuralinitiative/claude-dnd-skill
   /plugin install dm@neural-initiative

2. Corré el helper de migración de una sola vez
   python3 <plugin>/skills/dnd/scripts/migrate_v1_to_v2.py
```

Después usá **`/dm:dnd`** de ahí en adelante.

> Las dos instalaciones coexisten sin problema entre el paso 1 y el paso 2
> (comparten la misma raíz de datos), así que no hay ninguna ventana en la que
> algo esté roto.

## Qué hace el helper

`migrate_v1_to_v2.py`:

1. **Detecta** tu instalación standalone legacy y reporta su versión.
2. **Traslada el estado en tiempo de ejecución** que las builds standalone más
   viejas escribían *dentro* del skill (`~/.claude/skills/dnd/display/`) al
   directorio runtime a prueba de actualizaciones (`<data-root>/.runtime`):
   **aprobaciones de dispositivos, el token de auth del display, y los
   certificados TLS.** Esto es lo importante — los teléfonos emparejados
   siguen emparejados y HTTPS sigue siendo confiable, así que nadie tiene que
   reaprobar cada dispositivo después del cambio.
3. **Verifica** (no mueve) los datos de tu campaña en la raíz de datos.
4. **Respalda y retira** el viejo `~/.claude/skills/dnd` (movido a
   `~/.claude/skills/dnd.v1-backup-<timestamp>`, no se borra) para que el
   `/dnd` legacy ya no tape ni duplique a `/dm:dnd`.

**No** toca los datos de campaña, y **no puede** correr `/plugin install` por
vos (es un comando de la UI de Claude Code) — por eso instalás el plugin
primero.

### Opciones

```text
python3 migrate_v1_to_v2.py            # interactivo (pregunta antes de retirar v1)
python3 migrate_v1_to_v2.py --yes      # no interactivo
python3 migrate_v1_to_v2.py --dry-run  # muestra qué pasaría, no cambia nada
python3 migrate_v1_to_v2.py --keep-standalone   # solo reubica el runtime; deja /dnd en su lugar
```

Si tu instalación standalone vive en un lugar no estándar, apuntá el helper
ahí con `DND_LEGACY_SKILL_DIR=/ruta/a/dnd`. Si es un **symlink** (un clon de
dev o un setup con GNU Stow), el helper lo detecta y lo deja tal cual — sacá
el link vos mismo cuando estés listo.

## Volver atrás

No se borra nada. Para volver a la instalación standalone, movés el
directorio de backup (`~/.claude/skills/dnd.v1-backup-<timestamp>`) de vuelta
a `~/.claude/skills/dnd`, o reinstalás desde la rama congelada
**`legacy-1.x`**. Tus datos de campaña no se ven afectados de ninguna forma.

## Reportar problemas

Los casos límite de la migración se trackean en el hilo de discusión fijado
**"v2 migration reports"** del repo. Si algo no se trasladó limpio — un
dispositivo que necesitó reaprobación, un certificado que no se detectó —
dejá una nota ahí con tu versión previa y tu SO para que podamos detectarlo
temprano.

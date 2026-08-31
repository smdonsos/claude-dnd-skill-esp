# Glosario de terminología — D&D 5e en español

Fuente primaria: **Manual del Jugador 2024 (ESP)**, edición oficial licenciada. Cada término de este glosario fue verificado por frecuencia de aparición contra el texto real del manual (no de memoria) — ver método al final del documento. El manual en sí **no** se distribuye en este repo (contenido con copyright; ver `.gitignore`); este glosario extrae solo los nombres de términos, que no son objeto de protección de copyright por sí solos.

**Alcance de esta fase (Fase 0 / CLA-5):** solo categorías cerradas y de tamaño manejable — clases, puntuaciones de característica, habilidades, condiciones, tipos de daño, escuelas de magia, tamaños, alineamientos, y vocabulario común de mecánica/UI. La lista larga (319 hechizos, 334 monstruos, 237 objetos, 362 objetos mágicos del dataset SRD) se traduce entrada por entrada en Fase 3 (CLA-8), usando este mismo glosario como base de estilo — no se pre-construye acá para evitar duplicar ese trabajo.

**Registro:** español neutro, tuteo. Sin "vosotros" ni modismos de un solo país (ver decisión de proyecto).

**Qué traduce este glosario vs. qué no:** estos son términos de **presentación** — lo que el jugador lee en pantalla o en la narración del DM. Las claves estructurales que los scripts Python parsean (`## Session Flags`, `**Ruleset:**`, `roll_mode`, etc.) **no** se tocan — quedan en inglés como esquema interno, según la política ya fijada en `CLAUDE.md`.

---

## Clases

| Inglés | Español |
|---|---|
| Barbarian | Bárbaro |
| Bard | Bardo |
| Cleric | Clérigo |
| Druid | Druida |
| Fighter | Guerrero |
| Monk | Monje |
| Paladin | Paladín |
| Ranger | Explorador |
| Rogue | Pícaro |
| Sorcerer | Hechicero |
| Warlock | Brujo |
| Wizard | Mago |

## Puntuaciones de característica

| Inglés | Español |
|---|---|
| Strength (STR) | Fuerza |
| Dexterity (DEX) | Destreza |
| Constitution (CON) | Constitución |
| Intelligence (INT) | Inteligencia |
| Wisdom (WIS) | Sabiduría |
| Charisma (CHA) | Carisma |

## Habilidades (skills)

| Inglés | Español |
|---|---|
| Acrobatics | Acrobacias |
| Animal Handling | Trato con animales |
| Arcana | Conocimiento arcano |
| Athletics | Atletismo |
| Deception | Engaño |
| History | Historia |
| Insight | Perspicacia |
| Intimidation | Intimidación |
| Investigation | Investigación |
| Medicine | Medicina |
| Nature | Naturaleza |
| Perception | Percepción |
| Performance | Interpretación |
| Persuasion | Persuasión |
| Religion | Religión |
| Sleight of Hand | Juego de manos |
| Stealth | Sigilo |
| Survival | Supervivencia |

## Condiciones

| Inglés | Español |
|---|---|
| Blinded | Cegado |
| Charmed | Hechizado |
| Deafened | Ensordecido |
| Exhaustion | Cansancio |
| Frightened | Asustado |
| Grappled | Apresado |
| Incapacitated | Incapacitado |
| Invisible | Invisible |
| Paralyzed | Paralizado |
| Petrified | Petrificado |
| Poisoned | Envenenado |
| Prone | Derribado |
| Restrained | Apresado (mismo término que Grappled en 2024 — distinguir por contexto/efecto mecánico, no por nombre) |
| Stunned | Aturdido |
| Unconscious | Inconsciente |

> **Nota de verificación:** en la SRD 2024, "Grappled" y "Restrained" comparten la traducción "Apresado" en el manual oficial — a diferencia de ediciones anteriores donde "Restrained" era "Retenido". Confirmado por búsqueda directa (0 apariciones de "Retenido", 4 de "Apresado" en contextos distintos). Al traducir `dnd5e_srd.json` en Fase 3, verificar cuál de las dos aplica por el efecto mecánico de la entrada, no asumir.

## Tipos de daño

| Inglés | Español |
|---|---|
| Acid | Ácido |
| Bludgeoning | Contundente |
| Cold | Frío |
| Fire | Fuego |
| Force | Fuerza |
| Lightning | Relámpago |
| Necrotic | Necrótico |
| Piercing | Perforante |
| Poison | Veneno |
| Psychic | Psíquico |
| Radiant | Radiante |
| Slashing | Cortante |
| Thunder | Trueno |

## Escuelas de magia

| Inglés | Español |
|---|---|
| Abjuration | Abjuración |
| Conjuration | Conjuración |
| Divination | Adivinación |
| Enchantment | Encantamiento |
| Evocation | Evocación |
| Illusion | Ilusión |
| Necromancy | Nigromancia |
| Transmutation | Transmutación |

## Tamaños

| Inglés | Español |
|---|---|
| Tiny | Diminuto |
| Small | Pequeño |
| Medium | Mediano |
| Large | Grande |
| Huge | Enorme |
| Gargantuan | Gargantuesco |

## Alineamientos

| Inglés | Español |
|---|---|
| Lawful Good | Legal bueno |
| Neutral Good | Neutral bueno |
| Chaotic Good | Caótico bueno |
| Lawful Neutral | Legal neutral |
| True Neutral / Neutral | Neutral (verdadero) |
| Chaotic Neutral | Caótico neutral |
| Lawful Evil | Legal malvado |
| Neutral Evil | Neutral malvado |
| Chaotic Evil | Caótico malvado |

## Vocabulario común de mecánica / UI

| Inglés | Español |
|---|---|
| Hit Points (HP) | Puntos de Golpe (PG) |
| Armor Class (AC) | Clase de Armadura (CA) |
| Saving Throw | Tirada de salvación |
| Proficiency / Proficiency Bonus | Competencia / Bonificador por competencia |
| Inspiration | Inspiración |
| Concentration | Concentración |
| Advantage / Disadvantage | Ventaja / Desventaja |
| Short Rest / Long Rest | Descanso corto / Descanso largo |
| Hit Dice | Dado(s) de golpe |
| Experience Points (XP) | Puntos de Experiencia (PX) |
| Spell Slot | Espacio de conjuro |
| Level | Nivel |
| Roll | Tirada / tirar |
| Attack Roll | Tirada de ataque |
| Death Save | Tirada de salvación contra la muerte |

---

## Método de verificación

Cada término se contrastó por búsqueda de frecuencia (`grep -c`) contra un volcado de texto plano del Manual del Jugador 2024 en español (`pdftotext -layout`, generado una sola vez en un directorio local no versionado). Se compararon variantes candidatas cuando había ambigüedad razonable (ej. "Cansancio" vs. "Agotamiento" para Exhaustion; "Apresado" vs. "Retenido" para Restrained; "Espacio de conjuro" vs. "Ranura de conjuro" para Spell Slot) y se adoptó la que aparece consistentemente en el texto oficial. El volcado de texto no se conserva en el repo — es un artefacto de trabajo local, regenerable con `pdftotext -layout <manual>.pdf salida.txt` a partir del PDF que cada colaborador debe conseguir por su cuenta (contenido con copyright, no distribuido acá).

## Pendiente para Fase 3

Terminología de hechizos, monstruos, objetos y objetos mágicos individuales — se resuelve entrada por entrada al traducir `dnd5e_srd.json`, verificando cada nombre contra el manual del mismo modo que se hizo acá. Este glosario da el marco de estilo (registro, términos de mecánica compartidos) pero no pre-traduce esa lista larga.

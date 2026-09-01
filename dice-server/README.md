# Servidor de dados físicos (opcional)

Un pequeño servidor web local que le da a cada jugador en la mesa una bandeja
de dados 3D en su teléfono. Cuando el DM (Claude) tira por un personaje
jugador, los dados se envían al teléfono de ese jugador, donde sacude o toca
para lanzar — y el resultado vuelve a la campaña.

Es completamente opcional: el comando [`scripts/dice.py`](../scripts/dice.py)
chequea si el servidor está corriendo al arrancar y recae en el `random` local
de Python si no lo está, así que instalar esto no cambia nada del
comportamiento por defecto del skill.

---

## Cómo se siente

1. El DM (Claude Code) está sentado en la mesa con el skill cargado.
2. Cada jugador abre `http://<ip-mac-del-dm>:7777/?player=<su-nombre-de-pj>`
   en su teléfono una vez al inicio de la sesión y toca "tap to consecrate."
3. Cuando el DM resuelve una acción — *"Haz una tirada de Percepción"* —
   Claude corre `dice.py d20+4 --player piper --label "Perception"`.
4. El teléfono de Piper vibra un d20 3D sobre una mesa iluminada con velas.
   Piper sacude el teléfono. El dado da vueltas, se asienta, y Piper ve el
   resultado.
5. El resultado vuelve a Claude, que narra el desenlace.

Las tiradas de PNJ / monstruo / ocultas del DM se mantienen fuera de los
teléfonos de los jugadores (omitiendo `--player`); se auto-tiran del lado del
servidor y solo Claude las ve.

---

## Requisitos

- Host macOS o Linux (la máquina del DM corriendo Claude Code)
- Python 3.9+ con Flask: `pip3 install flask`
- Todos los teléfonos en el mismo Wi-Fi que el host (LAN-only por diseño)
- Un navegador de teléfono razonablemente moderno — la escena de dados usa
  WebGL vía Three.js cargado desde `unpkg.com`. Probado en iOS 16+ Safari y
  Chrome.

---

## Instalación

### Lo más rápido: correrlo en primer plano

```bash
python3 dice-server/server.py
```

Vas a ver algo como:

```
🎲 dice server
   local:   http://localhost:7777
   network: http://192.168.1.42:7777/?player=<tu-nombre>   ← jugadores
            http://192.168.1.42:7777/                       ← pestaña del DM
```

Los jugadores abren la URL `?player=...` en sus teléfonos. Listo.

### Recomendado en macOS: auto-inicio con launchd

```bash
./dice-server/install-launchd.sh
```

Esto instala `~/Library/LaunchAgents/com.dnd-skill.dice-server.plist`, arranca
el servidor, y lo mantiene corriendo entre logins / crashes. Vuelve a correr el
script para actualizar o después de mover el directorio del skill. Para
quitarlo:

```bash
launchctl unload ~/Library/LaunchAgents/com.dnd-skill.dice-server.plist
rm ~/Library/LaunchAgents/com.dnd-skill.dice-server.plist
```

### Linux

El servidor es una app Flask sencilla. Córrelo bajo systemd, screen, tmux, o
en una terminal — lo que prefieras. La dirección de bind es `0.0.0.0:7777`
por defecto; cámbiala con `DND_DICE_PORT=8081`.

---

## Cómo se unen los jugadores

Cada jugador abre esta URL en su teléfono, sustituyendo su propio nombre de PJ:

```
http://<ip-mac-del-dm>:7777/?player=piper
```

Minúsculas, sin espacios (usa guiones). El nombre debe coincidir con lo que el
DM pasa vía `--player` en `dice.py`. La convención es usar el nombre corto del
PJ.

El teléfono debe mantenerse abierto y en la pestaña activa durante la partida.
La página mantiene un wake-lock de pantalla para que no se duerma a mitad de
sesión.

Si un jugador cierra la pestaña, las tiradas dirigidas a él se auto-tiran del
lado del servidor en su lugar — el juego nunca se traba esperando un teléfono
ausente.

---

## Integración con el skill

El opt-in ya está cableado en `scripts/dice.py`:

```bash
# Tirada resuelta por el DM (ataques de PNJ, salvaciones de monstruos, etc.)
python3 scripts/dice.py d20+5 --label "Goblin attack"

# Tirada de jugador — se enruta al teléfono de ese jugador
python3 scripts/dice.py d20+4 --label "Perception" --player piper

# Forzar-saltear el roller físico para esta llamada puntual
python3 scripts/dice.py d20+5 --auto

# Forzar-saltear globalmente para una sesión
DND_DICE_PHYSICAL=0 python3 scripts/dice.py d20+5
```

Si el servidor no está corriendo, el script recae silenciosamente en el
random local — exactamente el comportamiento original de `dice.py`. Así que
una campaña se puede jugar en una máquina sin el servidor instalado y nada se
rompe.

Cuando el servidor *sí* se usó pero ningún teléfono estaba en el canal
objetivo, la salida recibe una etiqueta `[auto]` para que sepas que el
resultado vino del servidor en vez de una tirada física:

```
Roll: 17 + 5 = 22 [auto]
```

---

## Cómo se ve

La escena del teléfono es un único `<canvas>` renderizado con
[Three.js](https://threejs.org/): geometría de poliedro real
(`IcosahedronGeometry` para el d20, `DodecahedronGeometry` para el d12, etc.),
material PBR de bronce iluminado por una luz clave cálida y un rim frío azul,
dados numerados con calcomanías de bronce grabadas dibujadas sobre texturas de
canvas (tipografía Cormorant Garamond), física hecha a mano (gravedad, rebote,
asentamiento hacia la cara objetivo), y audio sintetizado (traqueteo, golpe
por rebote, campanilla en un 20 natural). Aplica tone-mapping ACES con una
sutil superposición de grano de película para el ambiente de impresión
antigua.

Sin dependencias de CDN externas más allá del propio Three.js y Google Fonts
— sin `node_modules`, sin paso de build, sin compilación.

---

## Protocolo (para los curiosos)

| Endpoint | Método | Propósito |
|---|---|---|
| `GET /` | — | La página de dados. Agrega `?player=NOMBRE` para suscribir un canal. |
| `GET /events` | SSE | Stream de Server-Sent Events de tiradas para el canal de este jugador (default: `_dm`). |
| `POST /roll` | JSON | `{"spec":"1d20+5","label":"...","player":"piper","physical":true}` |
| `GET /spec/<id>` | — | Devuelve la spec de una tirada en vuelo (la página usa esto al cargar). |
| `POST /submit/<id>` | JSON | `{"total":17,"rolls":[12],"kept":[12],"modifier":5,"spec":"1d20+5"}` |
| `GET /result/<id>` | — | Consulta por el resultado de una tirada (usado por `dice.py`). |
| `GET /health` | — | `{"ok":true,"subscribers":{"piper":1}}` |

La notación soportada por el servidor coincide con `dice.py`:
`NdM[kh|kl N][+|-K]` (ej. `4d6kh3`, `2d20kh1+5`).

---

## Privacidad y seguridad

- Solo-LAN: hace bind a `0.0.0.0:7777`. No hay auth — cualquiera en el mismo
  Wi-Fi puede conectarse, ver tiradas, y disparar tiradas falsas. Esto es
  intencional para un entorno de confianza de hogar/mesa.
- No expongas el puerto a internet sin agregar auth.
- Sin telemetría, sin analytics, sin llamadas de red salientes más allá de
  Three.js + Google Fonts en el teléfono del jugador (ambos cargan por HTTPS
  directo desde CDNs).

---

## Por qué existe esto

El `dice.py` por defecto tira de forma determinística en Python. Eso está
bien, pero elimina el momento en que un dado realmente cae — el pequeño rito
que hace que D&D se sienta como un ritual en vez de un chat. Esto vuelve a
agregar ese momento sin cambiar cómo funciona el skill para quien no lo
quiera.

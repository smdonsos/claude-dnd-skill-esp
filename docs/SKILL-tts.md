# Configuración de TTS del narrador (opcional)

El display companion puede leer en voz alta los bloques de narrador y de PNJ usando Gemini Flash TTS de Google. Es opcional, está apagado por defecto, y el resto del skill funciona bien sin esto. Esta guía te deja con una configuración funcionando en ~5 minutos usando una cuenta de Google gratuita.

Si te saltás esta guía, el display sigue renderizando el texto exactamente como lo hace hoy — sin audio, sin advertencias, sin cambios de comportamiento.

## Qué obtenés

- Un botón de altavoz al final de cada bloque de narrador y de PNJ. Hacé clic para escuchar ese bloque leído en voz alta.
- Un desplegable de 9 voces (4 masculinas, 5 femeninas) al lado del botón de altavoz. Cambiá de voz a mitad de sesión.
- Un toggle opcional de **Narración automática** en los controles de audio arriba a la derecha. Cuando está activo, cada bloque nuevo de narrador/PNJ se reproduce automáticamente **solo en tu navegador** — perfecto para un dispositivo de TV o pantalla principal mientras los teléfonos de los jugadores se mantienen en silencio.
- Soporte multi-idioma — Gemini detecta automáticamente el idioma a partir del texto, así que una campaña jugada en español, japonés, hindi, o cualquiera de los [24 idiomas soportados](https://ai.google.dev/gemini-api/docs/speech-generation) simplemente funciona.

## Qué cuesta

Gemini Flash TTS cobra por carácter. Un bloque de narración típico tiene ~600 caracteres; el precio actual es de ~$0.001 por bloque. Una sesión de 3 horas con ~30 bloques de narración cuesta aproximadamente 3¢. **El nivel gratuito cubre el uso casual** — solo necesitás habilitar la facturación si te topás con errores de rate-limit o si sos una cuenta nueva de AI Studio (Google requiere facturación prepaga para cuentas nuevas desde 2026).

## Configuración — tres pasos, ~5 minutos

### 1. Conseguí una API key de Gemini en Google AI Studio

Este es el camino más fácil. Sin `gcloud`, sin Cloud Console, sin service accounts.

1. Visitá **https://aistudio.google.com/apikey** e iniciá sesión con tu cuenta de Google / Gmail. Aceptá los términos la primera vez.
2. Hacé clic en **Create API key**. Si pregunta qué proyecto usar, aceptá el default — Google va a crear uno.
3. Copiá la key. Se ve como `AIza...` y tiene aproximadamente 39 caracteres.

### 2. Guardá la key en tu configuración local

```bash
mkdir -p ~/.config/claude-dnd && chmod 700 ~/.config/claude-dnd

# Pegá la key cuando se te pida, presioná Enter, después Ctrl-D:
cat > ~/.config/claude-dnd/tts.key

chmod 600 ~/.config/claude-dnd/tts.key
```

El skill lee de esta ruta automáticamente. Si preferís usar una variable de entorno, exportá `DND_TTS_KEY` (o `GEMINI_API_KEY`) en su lugar y saltate el archivo de key — las variables de entorno tienen prioridad.

### 3. Verificá

Desde el directorio base del skill:

```bash
python3 display/tts.py --test
```

Deberías ver:

```
API key source: file:/Users/vos/.config/claude-dnd/tts.key
Model: gemini-2.5-flash-preview-tts
Voice: Enceladus
Text:  'Hello, narrator voice test. The torchlit hall awaits.'
Calling Gemini Flash TTS…
  OK — received 76800 bytes of L16 PCM (24 kHz mono).
```

Para también escucharlo (solo macOS):

```bash
python3 display/tts.py --test --speak
```

Si la verificación falla, revisá la tabla de **Solución de problemas** al final.

## Usándolo durante una sesión

Una vez que la key está configurada y el display companion está corriendo:

- Aparece un pequeño ícono de altavoz abajo a la derecha de cada bloque de narrador (`.dm-block`) y de PNJ (`.npc-block`). Hacé clic para reproducir. Hacé clic de nuevo para detener.
- Un desplegable de **Voces** al lado te deja cambiar la voz del narrador. La selección persiste por campaña en `state.md → ## Session Flags → tts_voice: <name>`.
- La fila de **Narración automática** en los controles de audio arriba a la derecha es por navegador — activala para tu TV de proyección, desactivala en los teléfonos de los jugadores. La configuración se guarda en `localStorage`.

Los bloques de input de jugador, los bloques de tirada de dados, y los bloques de tutor/ayuda intencionalmente **no** tienen botón de altavoz — son metadata, no voz narrativa. El límite de 2000 caracteres del endpoint de síntesis es el tope máximo; los bloques de narración más largos se truncan del lado del servidor.

## Catálogo de voces

Subconjunto curado de 9 voces del catálogo de 30 voces de Gemini, acotado a voces narrativas de DM.

| Grupo | Voz | Notas |
|---|---|---|
| Masculina | Charon | Grave, áspera — villanos, personajes pesados |
| Masculina | **Enceladus** *(default)* | Profunda, medida — narrador clásico |
| Masculina | Fenrir | Ruda, gruñona — personajes feroces |
| Masculina | Umbriel | Suave, reflexiva — sabios y ancianos |
| Femenina | Aoede | Clara, brillante — heroica / informativa |
| Femenina | Gacrux | Madura, cálida — taberneros, mentores |
| Femenina | Kore | Juvenil, enérgica |
| Femenina | Vindemiatrix | Nítida, formal — nobles, eruditos |
| Femenina | Zephyr | Ligera, aérea — feéricos, hadas |

Para expandir el desplegable a las 30 voces completas de Gemini, editá `_TTS_VOICES_MALE` / `_TTS_VOICES_FEMALE` en `display/templates/index.html` y agregá los nombres nuevos a `VALID_VOICES` en `display/tts.py`. El catálogo completo está documentado en la [guía de speech-generation de Google](https://ai.google.dev/gemini-api/docs/speech-generation).

## Costo visible por navegador

Cada jugador que hace clic en el botón de altavoz sobre el mismo bloque de narración produce una llamada **separada** a Gemini — no hay caché del lado del servidor por hash de contenido. Una mesa de 4 jugadores donde todos hacen clic multiplica aproximadamente por 4× el costo por bloque. Si eso se vuelve una preocupación, dos mitigaciones prácticas:

1. Usar **Narración automática solo en la TV de proyección** — los jugadores escuchan el audio desde el parlante de la TV y no hacen clic en sus propios teléfonos.
2. Poner un tope de gasto diario en tu proyecto de facturación de Google en [console.cloud.google.com/billing](https://console.cloud.google.com/billing).

## Sesiones multi-idioma

Gemini Flash TTS detecta automáticamente el idioma de entrada a partir del contenido del texto. Para reproducir una campaña en español, simplemente narrá en español — el mismo endpoint `/tts` devuelve la síntesis correctamente. El catálogo de voces se mantiene idéntico entre idiomas.

Para también activar los paquetes de triggers de SFX (sonidos de choque de espadas, destello mágico, etc.) para narración en un idioma distinto del inglés, configurá los idiomas de SFX activos ya sea vía variable de entorno:

```bash
export DND_SFX_LANGUAGES=en,es     # inglés primero, después español
```

…o por campaña vía `state.md → ## Session Flags`:

```
sfx_languages: en,zh
```

El skill actualmente trae paquetes de SFX para los 24 idiomas soportados por Gemini (`ar`, `bn`, `de`, `en`, `es`, `fr`, `hi`, `id`, `it`, `ja`, `ko`, `mr`, `nl`, `pl`, `pt`, `ro`, `ru`, `ta`, `te`, `th`, `tr`, `uk`, `vi`, `zh`). Los PRs de la comunidad para extender cualquier paquete son bienvenidos.

## Camino B — key restringida con `gcloud` (avanzado, opcional)

Si ya usás la CLI de `gcloud` y preferís acuñar una key acotada *solo* a la API de TTS — para que una filtración no pueda alcanzar Cloud Storage, BigQuery, u otros servicios de Google en el mismo proyecto — usá este camino:

```bash
PROJ=my-dnd-tts                  # cualquier id de proyecto globalmente único
BILLING=YOUR-BILLING-ID          # gcloud billing accounts list

gcloud projects create "$PROJ"
gcloud billing projects link "$PROJ" --billing-account="$BILLING"
gcloud services enable generativelanguage.googleapis.com --project="$PROJ"

mkdir -p ~/.config/claude-dnd && chmod 700 ~/.config/claude-dnd
gcloud alpha services api-keys create \
  --project="$PROJ" \
  --display-name="claude-dnd-tts" \
  --api-target=service=generativelanguage.googleapis.com \
  --format='value(response.keyString)' \
  > ~/.config/claude-dnd/tts.key
chmod 600 ~/.config/claude-dnd/tts.key
```

La restricción `--api-target` significa que una key filtrada solo puede llamar a `generativelanguage.googleapis.com` en este proyecto específico. Deshabilitala / rotala sin afectar ninguna otra superficie.

## Solución de problemas

| Síntoma | Causa probable |
|---|---|
| `python3 display/tts.py --test` dice "API key: unset" | No hay variable de entorno **ni** archivo de key — guardá tu key en `~/.config/claude-dnd/tts.key`. |
| El botón de altavoz muestra "TTS 401" | API key inválida o deshabilitada — acuñá una nueva en https://aistudio.google.com/apikey. |
| El botón de altavoz muestra "TTS 403" | La key no está autorizada para `generativelanguage.googleapis.com` (keys del Camino B), o la facturación no está configurada en una cuenta nueva de AI Studio. |
| El botón de altavoz muestra "TTS 429" | Límite de rate del nivel gratuito, o cuenta nueva de AI Studio sin facturación — habilitá la facturación en https://aistudio.google.com o configurá un saldo prepago. |
| El botón de altavoz muestra "TTS 503" | El servidor reporta que TTS no está configurado — reverificá el archivo de key y reiniciá el display. |
| El audio no se reproduce pero no hay etiqueta de error | Revisá el volumen del dispositivo; en iOS Safari, hacé clic en el altavoz una vez para conceder el gesto de AudioContext, después la narración automática va a funcionar el resto de la sesión. |
| Demora de 1-3 segundos antes de que empiece el audio | Normal — latencia de síntesis de Gemini Flash TTS. La velocidad de tipeo `Fast` combinada con narración automática da el emparejamiento más ajustado de texto y voz. |

## Cómo deshabilitarlo

Borrá el archivo de key:

```bash
rm ~/.config/claude-dnd/tts.key
```

Los botones de altavoz desaparecen del display en la próxima carga de página. Nada más cambia.

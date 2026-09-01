# Cómo contribuir a claude-dnd-skill

Gracias por tu interés en contribuir — los pull requests son bienvenidos. Algunas notas prácticas abajo.

## Licencia de las contribuciones

Al enviar un pull request, aceptas que tu contribución queda licenciada bajo la [GNU Affero General Public License v3.0 or later](LICENSE), la misma licencia que el resto del proyecto.

Conservas el copyright de tus propias contribuciones. AGPL-3.0-or-later aplica hacia adelante desde tu contribución en más; la obra combinada sigue licenciada bajo AGPL-3.0-or-later.

## Qué es más útil contribuir

- **Correcciones de bugs** en el display companion, la mecánica de dados, los scripts de flujo de sesión, o cualquier cosa en `scripts/`
- **i18n / paquetes de idioma** para los triggers de SFX — ver `display/audio.py` para el patrón existente. Ya hay 24 paquetes de idioma (incluido español); más idiomas son muy bienvenidos
- **Extensiones atmosféricas** como el servidor de dados opcional (#30) — cualquier cosa que mejore la experiencia de mesa presencial sin comprometer el modelo de estado persistente
- **Rendimiento y limpieza** en los módulos helper de Python

## Proceso

1. Para cambios sustantivos, abre un issue primero — da la oportunidad de alinear el alcance antes de escribir código
2. Correcciones de bugs chicas o mejoras de documentación pueden ir directo a un PR
3. Escribe una descripción de PR clara que explique el *por qué*, no solo el *qué*
4. No hay CI; el maintainer revisa los PRs manualmente
5. El maintainer puede aplicar hardening menor sobre PRs ya mergeados (ej. ajustar defaults, agregar SRI a assets cargados desde CDN) — esto se documenta como commits de seguimiento separados en el mismo release, nunca como ediciones a tu trabajo

## Preguntas

Abre un issue o comenta en un PR existente. El maintainer lee todo.

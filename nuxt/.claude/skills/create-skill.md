---
name: create-skill
description: Crear un nuevo skill de Claude Code (.claude/skills/<name>.md). Úsalo cuando el usuario quiera documentar un patrón reutilizable, agregar un slash command, o estandarizar cómo implementar una funcionalidad recurrente del proyecto. Aplica cuando mencione "crear skill", "nuevo skill", "agregar comando" o quiera documentar un patrón.
---

# Crear skill de Claude Code

Archivo destino: `.claude/skills/<name>.md`

## Estructura obligatoria

```markdown
---
name: <slug-kebab-case>
description: <qué hace, 1-2 oraciones con palabras clave naturales que el usuario usaría>
---

# <nombre>

<contenido>
```

## Reglas de contenido

- **Máximo 120 líneas** — si crece más, mueve detalles a un archivo hermano y enlázalo
- Lee los archivos del proyecto antes de escribir — usa snippets reales, no abstractos
- Documenta qué store, composable o plugin usar, con rutas exactas
- Incluye ejemplos mínimos funcionales; evita boilerplate innecesario
- Usa tablas para mapeos (acción → mensaje, campo → validación, etc.)

## Campos YAML opcionales

| Campo | Cuándo usarlo |
|-------|---------------|
| `user-invocable: false` | Solo para Claude, no aparece en el menú `/` |
| `disable-model-invocation: true` | Solo invocación manual, Claude no lo auto-dispara |
| `allowed-tools: Read, Grep` | Restringe herramientas (útil para skills de solo lectura) |
| `argument-hint: [nombre]` | Hint en autocompletado al escribir `/skill-name` |

## Skills vs. Commands

| `.claude/skills/` | `.claude/commands/` |
|-------------------|---------------------|
| Patrón de implementación (cómo codificar algo) | Referencia de API / documentación externa |
| Claude lo auto-dispara por contexto | Se invoca manualmente vía `/command` |
| Incluye snippets de código del proyecto | Puede ser pura documentación |

## Proceso

1. Identifica el tema; elige `name` en kebab-case
2. Lee los archivos relevantes del proyecto para extraer patrones reales
3. Escribe `description` con palabras clave que el usuario usaría naturalmente
4. Estructura el contenido: contexto → patrón principal → ejemplo mínimo → notas
5. Cuenta las líneas — si supera 120, extrae secciones a un archivo hermano
6. Si ya existe un skill relacionado, actualízalo en lugar de crear uno nuevo

## Ejemplo mínimo

```markdown
---
name: api-calls
description: Hacer llamadas a la API con el plugin $api del proyecto. Aplica cuando
el usuario necesite GET, POST o DELETE a endpoints del backend Django REST.
---

# api-calls

Usa el plugin `$api` (axios) inyectado por `plugins/api.ts`.

\`\`\`js
const { $api } = useNuxtApp()
const { data } = await $api.get('/api/resource/')
const created = await $api.post('/api/resource/', payload)
await $api.delete(`/api/resource/${id}/`)
\`\`\`

El plugin adjunta `Authorization: Token <value>` desde la cookie `auth_onigies`.
```
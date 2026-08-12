---
type: task
id: task-108
title: GeneralGroup y GeneralQuestion como catálogos del dashboard
state: closed
date: 2026-08-11
owner: ai
parent: "[[task-101]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
depends-on: ["[[task-107]]"]
---

# GeneralGroup y GeneralQuestion como catálogos del dashboard

Con el modelo en pie ([[task-107]]), la sección se da de alta como catálogo editable — que es exactamente lo que Rubén acordó en la reunión del 11 de agosto: que su equipo edite los textos «igual que hoy se editan los criterios de buenas prácticas».

**Dos esquemas de catálogo**, uno para `GeneralGroup` y otro para `GeneralQuestion`. El procedimiento para declararlos está en el skill `manage-collections`.

**Menú:** entrada nueva **«Preguntas base»**, que sustituye al ítem muerto que hoy cuelga de la sección «Gestión Catálogos» en `nuxt/app/layouts/dashboard.vue` apuntando a una colección que no existe en el API. Por [[adr-0006]] el menú se declara a mano, así que dar de alta el esquema no basta: hay que tocar las dos capas.

**Presentación:** en el Sheet del grupo, las preguntas se listan debajo de los campos directos, con el patrón de objetos relacionados que el dashboard ya usa para las colecciones hijas (skill `dashboard-collections`).

**Campos protegidos:** `name` y `addl_config` van ocultos o de solo lectura. Son justamente los dos que rompen cosas si alguien los edita — el primero desengancha la respuesta de su columna, el segundo altera comportamiento que vive en código.

## Cierre (2026-08-12, sesión orquestada)

Entregada en `943c7ac`. Los dos esquemas quedaron cada uno en su app (`indicator` y `question`); ambos con `EditSimple` propio porque el marco genérico pinta el `name_field` siempre editable y aquí `name` debe ser intocable (probado con PATCH hostil: 200 pero el valor no cambia). Micro-decisiones ratificadas: `hide_create` en ambos (los objetos los crea el seed — preguntas nuevas exigen deploy), `q_type` y `addl_config` de solo lectura, `hint` y `public_name` editables. El menú ganó soporte de `path` por ítem porque `GeneralGroup` tiene PK de slug y la ruta de FilterGroup habría tronado (el ítem viejo `question_groups` estaba muerto: apuntaba a una colección inexistente). Tras la revisión crítica se bloqueó el DELETE por API en ambos catálogos (405), congruente con «ninguna pregunta debe morir». Bug latente hallado y registrado aparte: [[task-119]].

## Criterios de aceptación

- [x] El equipo de Rubén edita título, subtítulo, instrucción y el texto de cada pregunta desde el dashboard
- [x] El menú tiene «Preguntas base» y ya no queda ningún ítem apuntando a una colección inexistente
- [x] Las preguntas de un grupo se ven y se editan desde el Sheet del grupo
- [x] `name` y `addl_config` no son editables desde el dashboard

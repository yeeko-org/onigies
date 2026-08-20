---
type: task
id: task-128
title: Generar desde el backend la capa de tipos de collection.js
state: open
date: 2026-08-20
owner: ai
related: ["[[task-126]]", "[[task-23]]"]
---

# Generar desde el backend la capa de tipos de collection.js

Hoy `nuxt/app/types/collection.js` se escribe a mano, y describe un contrato que el backend ya conoce: el payload de `/catalogs/all/` lo produce el registry de `ps_schema` a partir de los `catalog_schema.py`. El typedef es, literalmente, una copia manual de una estructura generada. Cada campo nuevo en un esquema obliga a repetirlo del lado del frontend, y nada garantiza que ambos lados sigan de acuerdo — es el boilerplate duplicado que motivó la duda de Ricardo al revisar la [[task-23]].

La propuesta es un management command de Django que emita esa capa desde el registry.

**Arquitectura de dos typedefs**, y esta partición es el punto de la tarea. No todo lo que el frontend lee de un `collection_data` viene del backend: `cats.js` enriquece el objeto en el cliente —`has.*`, `is_category`, la construcción de los filtros— y esas propiedades no existen en el payload. Meterlas en un archivo generado las borraría en la siguiente corrida.

- **Generado:** el contrato del payload de `/catalogs/all/`, tal como lo produce el registry. Se regenera con el comando y no se edita a mano.
- **Manual:** un typedef que extiende al generado con el enriquecimiento del cliente. Vive aparte, sobrevive a la regeneración y es donde se documenta lo que el backend no sabe.

Queda por resolver en la ejecución cómo se expresa la extensión en JSDoc y dónde se corta la frontera cuando una propiedad viaja del backend pero el cliente la reescribe.

Es complemento de [[task-126]], no sustituto: aquella decide **qué contratos del frontend vale la pena tipar**; esta resuelve que el contrato ya tipado deje de mantenerse a mano.

## Criterios de aceptación

- [ ] Un management command emite el typedef del payload de /catalogs/all/ desde el registry de ps_schema
- [ ] El enriquecimiento cliente de cats.js vive en un typedef manual que extiende al generado y sobrevive a la regeneración
- [ ] Agregar un campo a un catalog_schema.py se refleja en el IDE sin editar el frontend a mano

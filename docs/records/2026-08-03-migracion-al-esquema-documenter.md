---
type: record
id: 2026-08-03-migracion-al-esquema-documenter
title: Migración de la documentación de onigies al esquema documenter
date: 2026-08-03
parent: "[[task-39]]"
---

# Migración de la documentación de onigies al esquema documenter

Sesión del 3 de agosto de 2026. Se migró el `docs/` heredado al esquema de cinco tipos y se hizo el triage de pendientes. El plan global del rediseño es [[global:task-2]]; onigies no figuraba entre sus cuatro repos y se sumó como quinto.

## Decisiones de Ricardo en esta sesión

- **El instrumento del cuestionario entra a `docs/`** como `reference` (la versión reducida, que es la fuente literal del seed) y `record` (los dos originales, 2026 y 2024).
- **El bundle del design system sale a la raíz** (`design-system/`, antes `docs/onigies-design-system/`), no a `.claude/skills/`: es material de marca, no documentación de proceso, y por ahora se queda donde se vea.
- **Triage completo con jerarquía:** todos los pendientes detectados se elevaron a nodos, agrupados bajo seis tasks padre.
- **Una task por punto pendiente del cliente**, con `owner: ricardo`, en lugar de tasks paraguas — para que `pending --owner ricardo` devuelva la deuda real.

## Qué quedó dónde

- **1 decisión:** `adr-0001` (ramas main/production sin divergencia), con sus valores de enum traducidos al inglés.
- **2 referencias:** el cuestionario 2026 reducido y la definición y medición de buenas prácticas.
- **19 registros:** los dos históricos del deploy de julio, las tres piezas de la reunión con Rubén, los cuatro planes ya ejecutados (motor de flujo, mejoras y auditoría, progreso del frontend, port de ps_schema, seed del cuestionario), el instrumento en sus dos versiones, la prueba con usuarias, el prompt a Fable, las dos auditorías del dashboard y esta bitácora.
- **39 tareas:** seis padres (flujo, cuestionario, dashboard, producción, definiciones con Rubén, buenas prácticas), 32 hijas y la de esta migración, cerrada.

Los cuatro `PLAN_*` se archivaron como `record` y no como `reference` porque ya se ejecutaron: el mapa vivo del motor es el skill `flow` y el del cuestionario el skill `cp-questionnaire`. Lo que seguía abierto en ellos se elevó a tareas, que es donde el ciclo se puede cerrar.

## Rutas y enlaces reparados

Las rutas citadas desde el código y las skills apuntaban a los nombres viejos —y varias ya estaban podridas desde antes, en `api/ies/flux_rules/`, que no existe desde junio—. Se actualizaron en `api/CLAUDE.md`, los modelos de `answer`/`survey`/`example`/`indicator`, `question/seed_data/`, `load_questionnaire`, `migrate_flow_data`, `flow/notifications.py` y las skills `flow`, `cp-questionnaire`, `deploy-api` y `deployment`. Los enlaces relativos entre documentos pasaron a `[[id]]`.

El hook de pre-commit quedó instalado en `.githooks/`; cada clon nuevo necesita `git config core.hooksPath .githooks`.

## Decisiones rescatadas de los registros

En la misma sesión se detectaron cuatro decisiones enterradas en los registros que merecían nodo propio, y Ricardo aportó el porqué de dos de ellas: [[adr-0002]] (terminales absolutos en `gen` y `bp`), [[adr-0003]] (el seed manda sobre el catálogo de estados, porque la configuración es demasiado intrincada para delegarla al cliente), [[adr-0004]] (la composición sexo-genérica se captura en Generales) y [[adr-0005]] (la configuración de colecciones vive en clases de Python, porque el esquema anterior duplicaba y partía las definiciones). De esta última salió además [[adr-0006]]: el menú del dashboard se declara a mano en el frontend.

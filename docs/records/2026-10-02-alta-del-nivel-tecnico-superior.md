---
type: record
id: 2026-10-02-alta-del-nivel-tecnico-superior
date: 2026-10-02
related: ["[[adr-0024]]", "[[adr-0025]]", "[[task-191]]", "[[task-192]]", "[[task-134]]"]
---

# Alta del nivel técnico superior (TSU) en el instrumento

Sesión del 2026-10-02 (session log `7d2128b1-f51e-4681-bf6d-85c99b705a7e`), rama `sector-tsu`, en paralelo con la sesión de comentarios y válvula de admin ([[2026-10-02-comentarios-editables-y-valvula-de-admin]]), que compartió el árbol de trabajo y rebasó `cp-backend` a mitad de la sesión.

## Punto de partida

Rubén creó desde el catálogo del dashboard («Gestión Catálogos → Sectores poblacionales») el sector «Alumnado de nivel técnico superior»: tres IES lo tienen. `Sector` no está en el admin de Django; el catálogo expone todos los campos y precarga los defaults del modelo (`is_main=True`, `order=0`). Ricardo acordó con Rubén que todas las IES de 2025 lo reciben con `is_present=False` y quien lo necesite en «Sí» lo cambia en la revisión. Pidió pensar todos los campos del sector «para que esté lo más perfecto posible».

## Lo que se encontró

- No hay signal al crear un `Sector`: las filas de `PopulationQuantity` solo nacen al guardar una `Institution` (y con presencia nula) o cuando la IES contesta. El acuerdo «todas en No» necesitaba un script.
- `load_sectors` renumera `order` 1–17 en cada corrida; Ricardo decidió no usarlo para producción («sin seed») y aceptar `order=6` empatado con medio superior.
- Las 32 preguntas de alcance estándar reciben el TSU solas por `is_main`; la lista fija del 1.16 no.
- La captura de planes del cp (`PlanResponse`) tenía tres columnas fijas y la pregunta general de planes TSU quedaba huérfana. Ricardo: «Meter el TSU al cp».
- Las preguntas de alcance mostraban todos los sectores, incluidos los declarados «No» en Generales; los planes sí ocultaban el nivel «No aplica». Ricardo decidió filtrar.
- El seed del cuestionario aborta si una lista fija nombra un sector inexistente, así que meter el TSU al seed del 1.16 obligó a meterlo también a `load_sectors` (opción 1, decisión de Ricardo).

## Decisiones

En [[adr-0024]] (el nivel TSU) y [[adr-0025]] (el alcance sin sectores ausentes). Ricardo dejó para platicar con Rubén la relación sector ↔ pregunta de planes: [[task-191]]. P1 de la sesión (que un script actualizara los textos vivos del 1.12) se retiró: «sí que lo modifique Rubén o yo directo, no por script».

## Lo hecho en código

- Comando one-off idempotente `add_tsu_sector` (cinco pasos: sector, presencias 2025 en «No» incluidas las nulas, pregunta `technical_plans` con reorden, respuestas 2025 en «No aplica», TSU en la lista del 1.16). Corrido dos veces en la base local: 66 encuestas 2025; la segunda corrida no crea nada.
- Migración `answer.0008_technical_plans_in_plan_response`; `PLAN_LEVELS`, `GEN_DENOMINATORS`, `PlanResponseSerializer`, `cp_capture.js`.
- Filtro de sectores ausentes en `get_sectors` con `absent_sector_ids` en el contexto de `AxisValueViewSet` y `ObservableResponseViewSet`.
- Seeds: `load_sectors` con el TSU, `catalogs.py` con la cuarta pregunta de planes, `axis_1.py` con el TSU en el 1.16 y en los textos del 1.12.
- Comentarios «10 principales / 12 poblaciones» → 11 / 13 en modelo, seed, validación y composable; skill `cp-questionnaire` con la columna nueva y el filtro de alcance.
- Tests: `AddTsuSectorTests` (3 casos, verificados que muerden) y `test_reach_hides_sectors_declared_absent`; `answer/tests.py` ajustado a cuatro niveles. Suite: 152 pytest, 11 vitest.

## Correcciones del critic aplicadas

Comentarios del Nuxt y del mock de tests a 13 poblaciones / 11 principales; el skill `cp-questionnaire` corrige «32 de 35» preguntas de alcance estándar. `docs/reference/cuestionario-2026-reducido.md` se deja en 12 por estar `state: obsolete`. Lo que el critic levantó sobre el deploy y las 3 IES con TSU vive en [[task-192]].

## Pendiente de deploy

En la sesión de deploy, cuando ambas sesiones de hoy hayan cerrado, y lo ejecuta Claude: `migrate answer`, `add_tsu_sector` en producción (ver antes el sector tal como lo dejó Rubén: la `description` se respeta, lo demás se sobreescribe), reinicio de `apionigies`, deploy del Nuxt. Rubén o Ricardo editan en el catálogo los textos vivos de las cuatro preguntas de planes del 1.12.

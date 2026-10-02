---
type: decision
id: adr-0024
title: El nivel técnico superior entra al instrumento como nivel de alumnado pleno
state: accepted
date: 2026-10-02
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-10-02-alta-del-nivel-tecnico-superior]]"]
affects: ["api/indicator/models.py", "api/indicator/management/commands/add_tsu_sector.py", "api/indicator/management/commands/load_sectors.py", "api/question/seed_data/catalogs.py", "api/question/seed_data/axis_1.py", "api/answer/models.py", "api/answer/group_validation.py", "api/api/views/answer/serializers.py", "nuxt/app/utils/cp_capture.js"]
related: ["[[adr-0004]]", "[[adr-0012]]", "[[adr-0023]]", "[[2026-07-04-seed-del-cuestionario]]", "[[task-134]]", "[[task-111]]", "[[task-191]]", "[[task-192]]", "[[task-190]]"]
---

# El nivel técnico superior entra al instrumento como nivel de alumnado pleno

## Contexto y planteamiento del problema

Rubén creó el 2026-10-02, desde el catálogo del dashboard, el sector «Alumnado de nivel técnico superior» (Técnico Superior Universitario, TSU): tres IES del padrón lo tienen y el instrumento no lo contemplaba. El instrumento 2026 trataba tres niveles de alumnado (medio superior, licenciatura, posgrado) en tres lugares distintos: como sectores principales de la tabla de poblaciones de Generales ([[adr-0004]]), como tres preguntas de «planes de estudio» en Generales, y como tres columnas fijas de `PlanResponse` en el observable 1.12 del cuestionario principal, más la lista fija de la pregunta de alcance del 1.16. Había que decidir si el TSU es un nivel más en los tres lugares o solo un sector del catálogo, y qué pasa con las IES de 2025 que ya completaron o aprobaron sus Generales, que son terminales y no se reabren.

## Criterios de decisión

- Coherencia: un nivel de alumnado recibe el mismo trato que los otros tres, en todos los bloques.
- No romper lo ya contestado: ninguna IES con Generales completadas o aprobadas debe quedar bloqueada por una fila nueva.
- No pedirle a Rubén más capturas de las necesarias.

## Opciones consideradas

- **Sector principal pleno (`is_main=True`) en los tres bloques** — poblaciones con conteo, pregunta de planes en Generales, columna de planes en el cp.
- **Sector extra (`is_standard_extra`)** — solo presencia, sin conteo ni planes. Descartada: incoherente con los otros niveles.
- **Solo en el catálogo, fuera de Generales** — no aparece en ningún bloque salvo donde se agregue a mano. Descartada.
- **Pregunta de planes solo en Generales, sin columna en el cp** — la IES declararía planes TSU que ningún observable usa. Descartada por Ricardo: «Meter el TSU al cp».

## Resultado

El TSU es un nivel de alumnado pleno:

- **Sector** «Alumnado de nivel técnico superior», `is_main=True`, el principal número 11. POB-ESTÁNDAR pasa de 12 a 13 poblaciones y los principales de 10 a 11; la composición del 1.7 ([[adr-0004]]) incluye al TSU. `order=6`, empatado con medio superior: la lista de alcance ordena por (`order`, `id`) y el TSU, de id mayor, cae entre medio superior y licenciatura sin renumerar nada. Ricardo aceptó el empate. Sin `description`; Rubén la edita en el catálogo si quiere.
- **Pregunta general** `technical_plans` («Planes de estudio vigentes de nivel técnico superior (TSU, profesional asociado)») en el grupo `planes_estudio`, orden 2; licenciatura y posgrado pasan a 3 y 4. Con «No aplica», como las otras tres.
- **Columna** `technical_plans` en `PlanResponse` (migración `answer.0008`), en la validación por nivel (`PLAN_LEVELS`), en los denominadores que el cp toma de Generales (`GEN_DENOMINATORS`) y en la captura del Nuxt, siempre en el orden medio superior, técnico superior, licenciatura, posgrado.
- **Lista fija del 1.16** («¿En qué sectores del alumnado se implementan dichos mecanismos?»): el TSU se agrega; las 32 preguntas de alcance estándar lo reciben solas por `is_main`.
- **Precarga 2025**, acuerdo Rubén–Ricardo: todas las encuestas 2025 reciben la presencia del TSU como «No» explícito (`is_present=False`) y su pregunta de planes como «No aplica». Lo hace el comando one-off `add_tsu_sector`, idempotente, que además pasa a «No» las filas que `Institution.save` haya dejado con presencia nula. El motivo es la compuerta de completitud ([[adr-0012]]): nulo bloquea («falta indicar si está presente»), «No» y «No aplica» eximen, así que ningún grupo ya completado o aprobado se rompe. Las IES que sí tienen TSU lo cambian a «Sí» en la revisión.
- **Seeds** alineados con producción para instalaciones nuevas: `load_sectors` crea el TSU (orden 7 en limpio, 6 en producción, mismo orden visible), el seed del cuestionario lista el TSU en el 1.16 y las cuatro preguntas de planes del 1.12 terminan en «— nivel medio superior / técnico superior / licenciatura / posgrado». Los textos vivos del 1.12 en producción no los toca ningún script: los edita Rubén o Ricardo en el catálogo.

### Consecuencias

- **Bueno:** el TSU se mide igual que los demás niveles; las 60 y tantas IES sin TSU no tienen que capturar nada.
- **Malo:** poner el TSU en «Sí» exige reabrir Generales de esa IES, que hoy es terminal; el camino depende de la válvula de admin, en construcción por otra sesión ([[task-190]], [[adr-0023]]), y de que esa válvula aplique a paquetes en `gen_finished`, lo que no está verificado. Toda la prosa que decía «10 principales / 12 poblaciones» queda enmendada, no reescrita.
- Las preguntas de alcance ya contestadas no incluyen el TSU en su respuesta; nada las bloquea.
- **Malo:** si una IES con TSU ya capturó el 1.12 en el cp y después su Generales pasa de «No aplica» a un número de planes TSU, su grupo de planes del cp deja de pasar la compuerta («Falta el conteo de nivel técnico superior», `group_validation.py`) hasta que capture ese nivel: el mismo mecanismo que el «No» precargado evitó en Generales. Voltear a las 3 IES en el mismo deploy o aceptar la devolución en revisión queda abierto en [[task-192]].
- Queda abierta la relación explícita entre el sector y su pregunta de planes: [[task-191]].

### Cómo se comprueba

`AddTsuSectorTests` (`api/indicator/test_add_tsu_sector.py`): dos corridas del comando no duplican sector, presencia, pregunta, respuesta ni la lista del 1.16; lo contestado no se pisa; la presencia nula pasa a «No». `answer/tests.py` valida los cuatro niveles de planes contra Generales. En producción: `Sector` TSU con `is_main=True` y `order=6`, cuatro `GeneralQuestion` en `planes_estudio`, y una `PopulationQuantity` con `is_present=False` por encuesta 2025.

## Más información

Record de la sesión: [[2026-10-02-alta-del-nivel-tecnico-superior]]. Riesgo de `load_sectors` por llave de nombre: [[task-134]]. Fórmula del 1.7, aún pendiente: [[task-111]].

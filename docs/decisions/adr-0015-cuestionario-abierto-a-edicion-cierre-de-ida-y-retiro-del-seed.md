---
type: decision
id: adr-0015
title: El cuestionario tiene un interruptor de edición en base de datos que abre la estructura al dashboard, cierra de ida y retira el seed; los pesos default solo se heredan en el trío estándar
state: accepted
date: 2026-09-10
origin: ricardo
deliberation: dialogued
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
rationale: recorded
supersedes: null
superseded-by: null
affects:
  - api/question/models.py
  - api/indicator/models.py
  - api/api/views/content_gate.py
  - api/api/views/question/serializers.py
  - api/api/views/indicator/serializers.py
  - api/question/catalog_schema.py
  - api/question/initial_data.py
  - api/question/management/commands/load_questionnaire.py
  - api/question/admin.py
  - nuxt/app/components/dashboard/indicator/observable/ObservableEditSimple.vue
  - nuxt/app/components/dashboard/question/questionnaire_settings/QuestionnaireGate.vue
related: ["[[adr-0014]]", "[[task-131]]", "[[task-132]]", "[[task-133]]", "[[task-135]]", "[[task-139]]"]
---

# El cuestionario tiene un interruptor de edición en base de datos que abre la estructura al dashboard, cierra de ida y retira el seed; los pesos default solo se heredan en el trío estándar

## Contexto y planteamiento del problema

[[adr-0014]] fijó el 7 de septiembre que el dashboard manda sobre los textos del instrumento y que la estructura (qué preguntas existen, a qué observable cuelgan, qué tipos aplican, banderas de sectorial y orgánica) la gobierna el seed. Tres días después el contexto cambió: Rubén hace la edición final del cuestionario desde el dashboard antes de compartirlo a las IES, y hay un observable sin pregunta de transversalidad orgánica (1.12) y seis sin sectorial que él mismo debe poder completar. Ricardo lo planteó así en la sesión ([[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]):

> Ya el control total debe estar de lado de Rubén hasta que él decida que ya está terminado.

Con la restricción de que el seed no vuelva a correr después del deploy que entrega esto: «`load_questionnaire` no debería correrse más que una vez, y esta única vez, hoy, antes de que Rubén toque el contenido del cuestionario». Y con una garantía de datos que hace todo esto seguro: no hay respuestas ni ediciones previas del cuestionario principal, solo de Generales y Buenas Prácticas.

## Criterios de decisión

- Rubén completa y corrige el instrumento sin intervención técnica, y cuando lo da por terminado la estructura queda congelada.
- Nada de lo que Rubén cree desde el dashboard puede ser borrado por un proceso automático después.
- El cierre no se revierte por accidente desde la misma pantalla en la que se edita.
- Los pesos default reflejan la ponderación tentativa acordada con Rubén y no fingen un valor donde no lo hay.

## Opciones consideradas

- **Dónde vive el interruptor**: (A) variable de entorno, rápida pero cerrar exige entrar al servidor y recargar el API; (B) fila única en base de datos expuesta como catálogo, con el cierre a un clic desde el dashboard.
- **Quién reabre**: (A) el mismo interruptor en ambos sentidos; (B) cerrar desde el dashboard y reabrir solo en el admin de Django, a mano.
- **Cómo completar el 1.12 y los reach faltantes**: (A) por el seed, con una última corrida en el deploy de cierre; (B) por el dashboard, abriendo la creación de preguntas y de tipos.
- **Pesos default de planes, especial y población**: (A) 0, que el editor mostraría como «usa 0 del tipo»; (B) nulo, que dispara el aviso de captura.
- **Herencia del default**: (A) siempre que el peso propio esté vacío; (B) solo cuando el observable tiene exactamente los tres tipos para los que se calibró la ponderación.

## Resultado

1. **Interruptor en base de datos** (B): `QuestionnaireSettings`, fila única con `content_open` y `seeded_at`, catálogo «Ajustes del cuestionario» y barra con `v-switch` arriba de la vista «Cuestionario: ejes, observables y preguntas».
2. **Mientras está abierto**, el dashboard crea y borra preguntas en las cinco familias y filas puente de tipo, y edita `includes_academic`/`includes_admin` de orgánica y `has_main_sectors`/`others_sectors`/`has_general_planning` de sectorial. Crear una pregunta crea sola la fila puente de su tipo; borrar la última pregunta no borra la fila. **Cerrado**, solo textos y pesos: POST y DELETE responden 403 y las banderas estructurales se ignoran en PATCH. El catálogo de sectores no está bajo el interruptor. `number`, `order` y `component` del observable y `order` de las preguntas siguen sin editarse.
3. **Cerrar es de ida** (B): la API rechaza `content_open: True` sobre una fila cerrada; reabrir es acto manual de Ricardo en el admin. Ricardo: «una vez cerrado no debería ser editable, solo vía el admin y manualmente por mí, para no generar caos».
4. **El seed se retira**: `load_questionnaire` corre por última vez en el deploy que entrega esto ([[task-139]]) y escribe `seeded_at`; después aborta salvo `--force`. Desde entonces el dashboard es la única fuente del instrumento y la premisa de [[adr-0014]] «lo que es estructura lo gobierna el seed» termina. Con `--force` el seed sigue podando preguntas de A y planes que no estén en sus listas ([[task-133]]).
5. **Pesos**: defaults 5 (armonización e institucionalización), 2.5 (sectorial), 2.5 (orgánica), nulo en planes, especial y población (B). El default se hereda solo cuando el observable tiene exactamente ese trío (B); con cualquier otro conjunto, cada fila puente lleva peso propio y mientras falte alguno el observable avisa, sin bloquear ningún guardado. Ricardo: «El ponderador normal debería incluir los tres tipos (aunque los 3 no sean obligatorios) … Si el observable no tiene exactamente esos tres, entonces se deben establecer los ponderadores customizados».
6. **`QuestionType` lleva `icon` y `color`**, editables, para que un tipo sin colección propia (población) y cualquier tipo futuro no necesiten un mapa a mano en el frontend.
7. **Las preguntas nuevas nacen con el texto «Nueva pregunta»**, preseleccionado, porque las columnas `text` rechazan el vacío y Ricardo prefirió no tocar el esquema en el deploy de hoy ([[task-141]]).

## Enmienda a adr-0014

Esta decisión **modifica el punto 5 de [[adr-0014]]** (estructura no editable) y la premisa de su punto 4 de que el seed gobierna la estructura; refina su punto 1 (el peso efectivo ya no es incondicionalmente «propio o default») y su punto 2 (`QuestionType` gana `icon` y `color`, y sus defaults cambian). Sus puntos 3 y 6 y el resto de 1, 2 y 4 quedan intactos. **No se marca adr-0014 como reemplazada**: el modelo intermedio, la fuente de nombres y la política de textos siguen vigentes y los citan los skills `cp-questionnaire` y `dashboard-collections`.

### Consecuencias

- **Bueno:** Rubén termina el instrumento solo, y el 1.12 y los reach faltantes se resuelven desde su pantalla, no desde el seed ni desde un deploy.
- **Bueno:** el cierre es un acto explícito y reversible solo por quien administra: no hay carrera entre dos pestañas ni cierre accidental sin diálogo de confirmación.
- **Malo:** desde el retiro del seed, un observable o pregunta borrado por error no tiene de dónde restaurarse salvo un respaldo de la base; los respaldos previos al deploy y al cierre pasan a ser obligatorios.
- **Malo:** siete observables abren con «ponderación pendiente» desde el primer día (1.1, 1.12, 1.14, 1.15, 4.1 y 4.7 sin sectorial, más el 1.7 por su tipo de población), hasta que Rubén capture sus pesos; es lo esperado por el punto 5, pero se ve como aviso.
- **Malo:** `/catalogs/all/` es `AllowAny`, así que la fila de `questionnaire_settings` (`content_open`, `seeded_at`) la ve cualquier llamada anónima, como el resto de los catálogos; las escrituras siguen protegidas.
- **Malo:** con el cuestionario abierto, la API permite borrar la fila puente de un tipo `required`; solo la interfaz lo impide.
- **Malo:** `seeded_at` se escribe fuera del bloque atómico del seed: una falla después de cargar la estructura deja el candado sin poner.
- **Malo:** hoy cualquier usuario del dashboard con permiso de escritura en catálogos puede cerrar el cuestionario ([[task-143]]).

### Cómo se comprueba

Migraciones `question` 0009 y 0010 aplicadas; `QuestionType` con defaults 5 / 2.5 / 2.5 / nulo / nulo / nulo e ícono y color; `questionnaire_settings` con una fila `content_open=True`; suite de 103 en verde; la sonda `api/.claude/smoke_content_gate.py` con 13 comprobaciones (alta y baja abiertas, 403 cerradas, orden y fila puente automáticos, banderas abiertas y congeladas, cierre de ida, 405 del catálogo de ajustes).

## Más información

[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]], [[adr-0014]], [[task-135]] (reunión del 11 de septiembre, donde Rubén decide si sectorial se vuelve requerida).

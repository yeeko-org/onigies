---
type: task
id: task-139
title: Deploy del editor por bloques y última siembra del cuestionario antes de que Rubén edite
state: open
date: 2026-09-10
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-10-editor-por-bloques-cuestionario-abierto-y-retiro-del-seed]]"]
depends-on: ["[[task-131]]"]
related: ["[[adr-0015]]", "[[2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra]]"]
---

# Deploy del editor por bloques y última siembra del cuestionario antes de que Rubén edite

Sesión propia, después del commit de la rama `task-131-editor-observables-cuestionario-abierto`. Es el deploy que entrega el control del instrumento a Rubén ([[adr-0015]]): después de él, `load_questionnaire` no vuelve a correr.

Estado de partida: producción está en `e01c3e6` y `origin/main` está cuatro commits atrás de `main` (25823a7, 033e1fd, 58d58a2, f2be3d0). Faltan en el servidor las migraciones `question` 0005–0010 e `indicator` 0010, y `QuestionType` de producción sigue con los defaults viejos (60 / 0 / 40 / 0 / 0 / 0): la migración 0010 los cambia solo donde nadie los editó, y en producción nadie los ha editado. La fila de `questionnaire_settings` la crea la misma migración, con `content_open=True` y `seeded_at` nulo, así que la siembra final no necesita `--force`.

Runbook, con el skill `deploy-api` como guía de detalle:

1. Respaldo de la base de producción en `~/databases/` antes de tocar nada: desde el retiro del seed no hay de dónde restaurar una pregunta borrada.
2. Push de la rama y merge a `main` y a `production` según el skill.
3. En el servidor: `migrate` (checklist de deriva de migraciones del skill), después, exactamente `load_questionnaire --overwrite-texts --sync-institutions`, una sola vez. `--overwrite-texts` es obligatorio, no opcional: el commit 033e1fd partió `a_main_question` en `a_main_question` + `a_main_subtitle` en el seed, producción sigue con el texto combinado y el subtítulo nulo, y sin esa bandera la actualización no escribe textos; no hay segunda corrida porque `seeded_at` la bloquea. `--sync-institutions` es inocuo (GENERAL_GROUPS no cambió desde e01c3e6) y evita que el aviso «Pendiente: correr con --sync-institutions» del propio comando quede como paso imposible. Comprobar que `seeded_at` quedó escrito y que una segunda invocación aborta.
4. Comprobar `questionnaire_settings`: una fila, `content_open=True`. Comprobar `QuestionType`: defaults 5 / 2.5 / 2.5 / nulo / nulo / nulo, ícono y color poblados.
5. Netlify: build del frontend y verificación por id de build (skill `deploy-api`).
6. Humo en producción: abrir el 1.3 y el 1.12 en «Cuestionario: ejes, observables y preguntas», ver la barra del interruptor abierta, guardar un texto y revertirlo.
7. Entregar a Rubén: él agrega la pregunta de orgánica del 1.12 y los reach que falten, captura pesos, y avisa cuando termine; el cierre lo hace Ricardo desde la barra (o Rubén, ver [[task-143]]).

Respaldo también inmediatamente antes de cerrar el cuestionario.

Ejecutada el 10 de septiembre: [[2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra]]. Dos desviaciones del runbook, ambas decididas por Ricardo en la sesión: sin `migrate_initial_data` (redundante con las migraciones 0006 y 0010) y sin `--sync-institutions` (escribía `is_centralized` en encuestas existentes, [[task-148]]). Lo que sigue abierto es el paso 7 y el respaldo previo al cierre.

## Criterios de aceptación

- [x] Producción con las migraciones aplicadas y `load_questionnaire` corrido una sola vez, con `seeded_at` escrito
- [x] Frontend publicado en Netlify con el editor por bloques y la barra del interruptor
- [x] Humo del 1.3 y el 1.12 en producción sin errores de consola
- [ ] Rubén avisado de que puede editar

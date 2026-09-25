---
type: task
id: task-163
title: Deploy del retiro de StatusControl y del cuestionario principal (cp)
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-7]]", "[[task-153]]", "[[adr-0018]]", "[[2026-09-23-reunion-ruben]]", "[[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]", "[[task-175]]", "[[task-178]]", "[[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]"]
---

# Deploy del retiro de StatusControl y del cuestionario principal (cp)

Todo lo construido el 22 de septiembre está en la rama `cp-backend` sin desplegar. Antes: la revisión manual de Ricardo (23 de septiembre temprano). El runbook detallado, con la subsección one-off del release cp, está en el skill `deploy-api`.

Orden obligatorio:

1. Frontend en Netlify primero (el código limpio tolera el payload viejo; el store viejo caería sin `status_control`).
2. API: dump previo; `migrate` (answer 0005 y 0006, survey 0011, example 0009 —borra `example_evidence`, 661 filas ya duplicadas en `flow_attachment`, sin vuelta atrás salvo dump—, ies 0014 y 0015); `seed_flow` (crea `cp_not_present` y actualiza reglas e hints; sin él el «No» falla); `provision_cp_responses` en dry-run y luego `--apply` (espera 41 × surveys observables, 0 creados en la segunda corrida); nunca `resave_institutions` (escribe `is_centralized`).
3. Smoke: como IES de prueba, `/respuestas` muestra cp con el aviso de compuerta; como staff, la colección «Ejes del cuestionario».
4. Opcional: `remove_stale_contenttypes` (5 content types y 20 permisos huérfanos).
5. El día de apertura: fijar `Period.cp_open_at` del periodo 2025 en el admin, y publicar cp a las IES reales agregándolo a `PUBLISHED_SECTIONS` (`nuxt/app/utils/sections.js`) con su deploy.

Lo que no debe limpiarse: la carpeta `evidences/` (disco y S3), compartida con los adjuntos nuevos de bp.

## Riesgos y pasos añadidos tras la crítica de cierre (2026-09-23)

1. **Nadie puede capturar aunque se fije la fecha.** En la copia de producción del 22 de septiembre, 0 de 66 paquetes de generales estaban en `gen_finished` (51 `gen_draft`, 14 `gen_sent`, 1 `gen_need_changes`); leído en producción la madrugada del 25 (~01:30, solo lectura), siguen 0 de 66 en `gen_finished`: 46 `gen_draft`, 19 `gen_sent`, 1 `gen_need_changes`. Con [[adr-0018]], fijar `cp_open_at` no abre la captura a ninguna IES hasta que la revisión finalice la información base de cada una; el ritmo lo pone Rubén ([[task-165]]).
2. **El instrumento sigue editable** (`QuestionnaireSettings.content_open=True`, [[adr-0015]]). Crear un observable o un tipo de pregunta desde el dashboard no reprovisiona el árbol eager, y borrar un observable o una pregunta con respuestas las borra en cascada (`on_delete=CASCADE` en `api/answer/models.py`). Opciones para Ricardo: cerrar el instrumento antes de fijar `cp_open_at` ([[task-143]] pide dump previo), o reprovisionar tras cada edición estructural (`provision_cp_responses --apply`) y pasar a `PROTECT` cuando haya respuestas.
3. **Publicar cp en `PUBLISHED_SECTIONS` el mismo día de apertura** pierde la ventana «ver antes de responder» de [[task-153]]. Opción: publicarlo en este mismo deploy con `cp_open_at` vacío, para que las IES vean el cuestionario sin poder capturar.
4. **Ramas antes de Netlify:** falta decidir qué rama se mergea a cuál (`cp-backend` nació de `remove-statuscontrol`, que nació de `main`). La tolerancia «frontend nuevo sobre API viejo» se verificó solo para `2f5ef8c`; con el frontend de `cp-backend` sobre el API viejo, abrir un eje da 404 hasta que aterrice el API.
5. **`Period.cp_open_at` en el dashboard** solo se expone por el `PeriodSerializer` genérico; no se verificó que el formulario del periodo lo edite. Si no, el admin de Django es el camino seguro.

## Criterios de aceptación

- [x] Frontend publicado en Netlify antes que el API (build `2589a7c2…`, commit `d290636` a las 00:11 del 2026-09-25 y build detectado a las 00:12; `fd309f8f…` con el enlace de descarga, detectado a las 00:45)
- [x] Migraciones, seed_flow y provision_cp_responses --apply corridos en producción con los conteos esperados (siete migraciones; 2706 / 7920; segunda corrida en 0)
- [ ] ⚠️ Smoke de IES de prueba y de staff en verde — lo que corrió la madrugada del 25 fue un curl (`catalogs/all` y `api/` en 200, log sin trazas), no el smoke del runbook; el smoke visual en navegador lo hace Ricardo la mañana del 25 (como revisora, «Ejes del cuestionario» abre un eje; como IES de prueba, `/respuestas` muestra cp y un guardado en «Por iniciar» sale sin snackbar de error)
- [ ] ⚠️ Antes de ese smoke: ninguna IES de prueba tiene su paquete de generales en `gen_finished` (leído en producción a la 01:30 del 25), y las de prueba están exentas de la fecha pero no de esa llave ([[task-168]] punto 10), así que como IES de prueba no se puede guardar nada. Salida: como revisora, llevar a `gen_finished` el paquete de generales de una IES de prueba desde el dashboard (o por admin) antes del smoke
- [ ] ⚠️ El instrumento sigue abierto (`QuestionnaireSettings.content_open=True`, leído en producción a la 01:30 del 25) con `cp_open_at` ya fijado; nadie verificó si Rubén lo cerró tras el aviso de Ricardo. Decidir qué se le dice antes de la presentación ([[task-178]])
- [x] cp_open_at fijado y cp publicado en PUBLISHED_SECTIONS el día de apertura (2026-09-25 00:00 hora de México; cp en `PUBLISHED_SECTIONS` desde `d290636`)
- [ ] ⚠️ Avisar a Rubén cuando el deploy esté arriba (`[1:25:04]`, "hoy mismo") — de Ricardo, la mañana del 25 antes de la reunión de Rubén, junto con el documento de [[task-164]]. Líneas sugeridas para el aviso: ninguna IES captura hasta que su paquete de generales esté en `gen_finished`; no tocar la estructura del instrumento hasta cerrarlo; las erratas se corrigen en el dashboard; y quien tenga una pestaña de la plataforma abierta desde antes de las 00:14 del 25 verá errores hasta recargar (el frontend viejo no sobrevive al API nuevo sin `status_control`)

La task se cierra cuando el aviso y el smoke estén hechos.

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]]. Rubén autorizó liberar el cuestionario sin esperar la ponderación. Ricardo, `[1:20:00]`: «termino, porque hay detallitos pequeñitos que tengo que terminar aquí, y lo subo y lo prueba allá» (quién prueba, duda T13 de la limpia). Rubén, `[1:20:17]`: «Lo puedes subir, porque entiendo que estas preguntas que tenemos no son preguntas de cuestionario, son preguntas de valor, y se pueden ajustar». Ricardo, `[1:23:58]`: «en un par de horas acabo esto: los últimos detalles chiquititos, que ya son muy poquitos, para que pueda subir estas preguntas. Le pides a tu equipo que lo revise, por si ve algo, y ya lo mandas»; `[1:25:04]`: «te aviso cuando esté arriba, que va a ser hoy mismo». Rubén, `[1:23:58]`: «Buenísimo, Ricardo». La prisa de Rubén es su reunión del viernes 25 (`[12:04]`, `[35:17]`).

## Pasos de deploy del diseño cp, 2026-09-23

La sesión de diseño de la captura cp dejó sus pasos de deploy pendientes (migración `question.0011`, `seed_flow`, `provision_cp_responses --apply`, nombres y colores de estatus) en la sección «Pasos de deploy pendientes» de [[2026-09-23-diseno-de-la-captura-cp-y-decisiones-pendientes]]; se corren con este deploy. El bug del guardado «en llenado» encontrado el mismo día está en [[task-174]]: las respuestas sí se guardan, pero si se libera con el bug toda IES verá el error en su primer guardado; la decisión pendiente está en [[task-175]], entrada (a).

Las tres A que piden texto que la plataforma no guarda (1.16 A1 y A2, 2.5 A9) son lo único de la brecha que bloquea compartir las preguntas tal cual: decisión pendiente en [[task-175]], entrada (e).

## Deploy hecho, 2026-09-25

Se hizo la madrugada del 25 de septiembre (record [[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]), en dos builds: `d290636` (cp publicado a las IES reales, el bug de [[task-174]] corregido, «Eje N. Nombre» y «Nota:» de [[task-172]]) y `a8e9bcf` (enlace discreto para descargar el cuestionario en Word desde `/respuestas`). Ramas por fast-forward `cp-backend → main → production` ([[adr-0001]]); el riesgo 4 (qué rama a cuál) no fue decisión: `cp-backend` descendía del `main` local. En el servidor: dump en el servidor Yeeko, `~/unam/onigies/api/_backups/pre_cp_20260925_0614.dump`, `migrate` con las siete migraciones (survey 0011, answer 0005 y 0006, example 0009, ies 0014 y 0015, question 0011: el runbook decía seis y le faltaba `question.0011`), `makemigrations --check` limpio, `seed_flow` (1 estatus creado, 32 actualizados), `migrate_ps_schemas`, reinicio de `apionigies`, y `provision_cp_responses` en dry-run y `--apply` con 264 ejes recorridos, 2706 `ObservableResponse` y 7920 `GroupResponse` creados, segunda corrida en 0; por estatus, los 66 grupos de población en `cp_approved` ([[adr-0020]]) y los 7854 restantes en `cp_pre_start`. `remove_stale_contenttypes` (paso 4, opcional) no se corrió. `Period.cp_open_at` del periodo 2025 (el único, con las 66 encuestas) quedó en 2026-09-25 00:00 hora de México por shell, con la compuerta reportando abierta.

Decisiones de Ricardo esa noche: publicar cp y abrir la fecha el mismo día (riesgo 3: la ventana «ver antes de responder» no existió; [[task-153]]); el riesgo 2 (instrumento editable) sigue vivo: Ricardo dijo que le avisaría a Rubén «ahora mismo», y el aviso y su resultado quedan pendientes mientras se decide [[task-178]]. El riesgo 1 sigue: ninguna IES real captura hasta que su paquete de generales esté en `gen_finished` ([[task-165]] punto 5); en producción a la 01:30 del 25, 0 de 66. Verificado en producción también que `Axis.order` es 1 a 4 con los mismos nombres que en local, de lo que depende el título «Eje N. Nombre». Riesgo no anotado antes: las pestañas abiertas desde antes del primer build (00:14 del 25) fallan hasta recargar, porque el store viejo caía sin `status_control`.

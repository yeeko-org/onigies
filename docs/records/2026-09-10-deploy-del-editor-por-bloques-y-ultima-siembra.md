---
type: record
id: 2026-09-10-deploy-del-editor-por-bloques-y-ultima-siembra
date: 2026-09-10
parent: "[[task-139]]"
---

# Deploy del editor por bloques y última siembra del cuestionario

Sesión `duo` del 10 de septiembre de 2026, ejecutando el runbook de [[task-139]]. Un ejecutor Opus reunió el contexto (task, skills `deploy-api` y `deployment`, records del 4 de septiembre y del incidente del 12 de agosto, diff completo `origin/production..HEAD`, inventario de escritos de `load_questionnaire` leído del código); el coordinador ejecutó el deploy. Es el deploy que entrega el control del instrumento a Rubén ([[adr-0015]]): desde hoy `load_questionnaire` está retirado en producción.

## Estado de partida verificado

- Rama `task-131-editor-observables-cuestionario-abierto` en `0248cce`, descendiente directa de `origin/main` (`8ffe954`) y de `origin/production` (`e01c3e6`): fast-forward puro, sin merge ni rebase. Payload: 8 commits, 109 archivos.
- El servidor estaba en `bad2f71`, no en `e01c3e6`: `e01c3e6` solo agrega el lockfile de pnpm de Nuxt encima de `bad2f71`, sin cambios en `api/`. Benigno.
- Tests locales: API 103 pasados; sonda `api/.claude/smoke_content_gate.py` 13 pasados; Vitest 9 pasados. Playwright no corrió (necesita el dev server con certificado).
- Build de Netlify emulado localmente (`NODE_ENV=production NITRO_PRESET=netlify pnpm run build`): completó, 251 chunks en `dist/_nuxt`. Sin cambios en `package.json` ni en `pnpm-lock.yaml`, así que la falla del 4 de septiembre no podía repetirse.
- Sin variables de entorno ni dependencias nuevas en el rango. Deriva de migraciones limpia: 7 migraciones nuevas (`question` 0005–0010, `indicator` 0010), todas adiciones, ninguna amendada. `flow.Status` intacto.
- Producción viva antes del push: `question_type` en 60 / 40 / 0 / 0 / 0 / 0 con los nombres viejos, exactamente el guard de la migración 0010; `questionnaire_settings` inexistente; build id de Netlify `1f419592-6d95-4ce9-90fb-bb79dfe0f6fc` (4 de septiembre), idéntico en `onigies.netlify.app` y en el proxy de la UNAM.
- El borrado en cascada de [[task-133]] no podía dispararse: comparación del seed viejo contra el nuevo, observable por observable: 41/41 observables, 280/280 opciones A, 35/35 reach, 4/4 plan, 1/1 especial. El commit del cotejo (`033e1fd`) cambió textos, no estructura.

## Decisiones de Ricardo antes de tocar producción

Tres preguntas abiertas, tres respuestas verbatim:

1. `migrate_initial_data`: el skill `deploy-api` decía correrlo; la task-139 no lo mencionaba. Leído el código, era redundante (las migraciones 0006 y 0010 ya escriben orden, requerido, nombres, pesos, ícono y color) y no gratis (reescribe 15 `StatusControl` legacy vía `AppConfig.ready` de cuatro apps).
   > Creo que omitir, pero sí se resiembran las preguntas y QuestionType, cierto?

   Respuesta: sí, las preguntas por `load_questionnaire --overwrite-texts`; `QuestionType` por las migraciones 0006 y 0010; `load_questionnaire` nunca escribe en `QuestionType`. Se omitió.

2. `--sync-institutions`: la task lo llamaba «inocuo», pero al re-guardar cada institución `_preload_centralized` (`api/ies/models.py:90`) escribe `is_centralized` en la respuesta general de encuestas existentes cuando está en nulo. Código preexistente, no de la rama.
   > No deberíamos modificar is_centralized en ningún sentido, ya hay IES que han respondido.

   Se corrió sin la bandera. Abre [[task-148]].

3. Respaldo: `pg_dump` desde el servidor o snapshot de RDS.
   > Sí pg_dump

Y sobre la propuesta de corregir el pathspec del check de deriva del skill:
> De la propuesta, no puedo decidir ahora

Queda en [[task-149]].

## Secuencia ejecutada

1. **Dump** en el servidor con las credenciales del `.env`, en la carpeta `_backups` del API (fuera del repo), archivo `onigies_20260911_0141_pre_task139.dump` (694 KB, `pg_dump -Fc`, marca UTC), copiado a `~/databases/onigies_20260911_0141_pre_task139.dump`.
2. **Push** `HEAD:main` (`8ffe954..0248cce`) y `HEAD:production` (`e01c3e6..0248cce`). El clasificador de auto mode bloqueó el comando combinado con `git branch -f`; los pushes solos pasaron. Las ramas locales `main` y `production` no se realinearon.
3. **Servidor**, en secuencia continua (el cambio rompe en las dos direcciones: el frontend viejo lee columnas de peso que `indicator` 0010 borra, el nuevo lee `questionnaire_settings`): `git pull`, `migrate` (las 7 aplicadas), `makemigrations --check --dry-run` → «No changes detected».
4. **Sonda previa al seed**, con expectativa escrita de cero altas y cero bajas: observable 41, aquestion 280, aoption 2, reach 35, bquestion 40, plan 4, special 1, generalquestion 7, respuestas generales booleanas en nulo 112, puente 120 (a 41, b 41, reach 35, plan 1, especial 1, población 1), `QuestionType` 5 / 2.5 / 2.5 / nulo / nulo / nulo con ícono y color, `questionnaire_settings` una fila `content_open=True`, `seeded_at` nulo, subtítulos nulos 41. El 40 de preguntas B se verificó contra el seed antes de correr: un observable del eje 1 no trae pregunta B.
5. **`load_questionnaire --overwrite-texts`**, una sola vez: «Observables: 0 creados, 41 actualizados. Grupos generales: 5 asegurados, 7 preguntas.» El comando imprimió su aviso «Pendiente: correr con --sync-institutions», sin efecto. Segunda invocación: `CommandError: El cuestionario ya se sembró el 11/09/2026 01:45. Resembrar pisaría la estructura editada desde el dashboard; si de veras hace falta, corre con --force.`
6. **Sonda posterior**: todos los conteos idénticos; `seeded_at` = 2026-09-11 01:45:04 UTC; subtítulos nulos de 41 a 1 (uno sin subtítulo en el seed); respuestas booleanas en nulo siguen en 112.
7. **Recarga** con `kill -HUP` al master de gunicorn de `apionigies` (pid bajo supervisord); `supervisorctl status` RUNNING; `error.log` solo con los `RuntimeWarning` de siempre.
8. **Humo del API**: `/api/` 200; `/api/catalogs/all/` 200 con `questionnaire_settings` abierta, los seis `question_type` con pesos e íconos nuevos, 120 `observable_question_type`; descarga anónima de adjunto 404.
9. **Netlify**: build id nuevo `03278642-d15f-4f0d-9e96-89ede778cea7`, idéntico en `onigies.netlify.app` y en `onigies.unam.mx`.
10. **Humo del dashboard** en producción con la sesión de Ricardo (el coordinador no tecleó la contraseña: regla fija de las herramientas de Chrome; Ricardo la ofreció y se le pidió iniciar sesión él). Barra del interruptor abierta: «Cuestionario abierto a edición · Última siembra: 10 de septiembre de 2026». 1.3 abrió con el editor por bloques y los tres tipos estándar en «Sin valor propio: usa 5 / 2.5 / 2.5 del tipo»; se guardó « (humo)» al final del nombre, se confirmó por API y en el encabezado de la fila, se revirtió con el botón Guardar y se confirmó por API el nombre original. 1.12 abrió con «Ponderación pendiente» y armonización, orgánica y planes marcados como faltantes: el estado que prevé el [[adr-0015]]. Sin errores ni excepciones en consola, incluida una recarga completa.

## Hallazgos

- El check de deriva del skill `deploy-api` usa el pathspec `'*/migrations/'`, que con la diagonal final no empata ningún archivo: reporta «modelos cambiados sin migración» en un rango sano con siete migraciones. La forma correcta es `'*/migrations/*'`. [[task-149]].
- Ctrl+Enter no guarda desde el campo «Nombre del observable» del editor; solo desde los textos largos, como dice el tooltip del botón. Detalle de UX, no error; se anota en [[task-145]].
- El skill `deploy-api` quedó corregido en la misma sesión con ok de Ricardo: paso 7 del runbook sin `migrate_initial_data`, y la sección del seed marcada como retirado con la advertencia sobre `--sync-institutions`.

## Lo que queda de la task-139

El cuarto criterio, avisar a Rubén que ya puede editar, y el respaldo inmediatamente antes de cerrar el cuestionario cuando él termine. Ambos de Ricardo.

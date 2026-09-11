---
type: record
id: 2026-09-11-diagnostico-uaeh-informacion-base-vacia
date: 2026-09-11
---

# Diagnóstico: la UAEH veía «Aún no hay información base disponible para este periodo»

Reporte de la usuaria de la UAEH (institución 45) al entrar a 2025 en `/respuestas/2025`: la sección de Información base mostraba la alerta de «sin información». Sesión de diagnóstico del 2026-09-11, con Ricardo.

## Qué se verificó en producción (solo lectura)

- Survey 45 (UAEH, periodo 2025) con `GeneralPackage` 33 en `gen_draft` y sus 5 `GeneralGroupResponse` colgando del paquete. Las 65 instituciones tienen sus 5 grupos en el paquete 2025; ninguna sin Survey 2025.
- Una sola usuaria ligada a la institución, activa. Con su token, `GET /api/login/` y `GET /api/survey/45/` responden 200 y el detalle trae los 5 grupos.
- Netlify y el proxy de la UNAM sirven el mismo build id.
- En la base local tampoco hay filas de grupo huérfanas ni surveys sin paquete: la migración `survey/0006` no deja huérfanos por sí sola.

## Causa

Del lado del cliente: la usuaria probó en otro navegador con la misma cuenta y funcionó; el fallo era solo en su Chrome. La causa exacta dentro de Chrome no se persiguió (lo habitual tras un deploy de Nuxt son chunks viejos en caché).

## Lo que sí era un defecto

La pantalla no distinguía «respuesta sin grupos» de «la petición falló»: la carga en `GeneralGroupList.vue` llamaba a `getSimple` sin mensaje de error, y en producción el aviso de consola está compilado fuera, así que cualquier 401/404/500 o error de red pintaba la misma alerta sin rastro. Se corrigió pasando el mensaje «No se pudo cargar la información base», que muestra el snackbar de error como ya hacía el guardado. Entra con el siguiente deploy.

## Nota de método

El payload de login serializa el paquete general en forma breve (sin `general_group_responses`); la lista de grupos siempre viene del detalle `GET /api/survey/{id}/`. Un frontend que tomara los grupos del login vería siempre la lista vacía.

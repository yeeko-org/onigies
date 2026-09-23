---
type: task
id: task-163
title: Deploy del retiro de StatusControl y del cuestionario principal (cp)
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-7]]", "[[task-153]]", "[[adr-0018]]"]
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

## Criterios de aceptación

- [ ] Frontend publicado en Netlify antes que el API
- [ ] Migraciones, seed_flow y provision_cp_responses --apply corridos en producción con los conteos esperados
- [ ] Smoke de IES de prueba y de staff en verde
- [ ] cp_open_at fijado y cp publicado en PUBLISHED_SECTIONS el día de apertura (compromiso: 25 de septiembre o antes)

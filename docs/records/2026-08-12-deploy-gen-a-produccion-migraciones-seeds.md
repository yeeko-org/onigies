---
type: record
id: 2026-08-12-deploy-gen-a-produccion-migraciones-seeds
title: "Deploy gen a producción: migraciones, seeds, flow y respaldos"
date: 2026-08-12
---

# Deploy gen a producción: migraciones, seeds, flow y respaldos

Sesión duo (coordinador Fable + ejecutores). Tercer deploy del sistema nuevo. Alcance real: `819c2ee..e5c6a51` — **17 commits**, no solo los del día: incluye la sesión de adjuntos sobre flow ([[adr-0010]]), la Sesión A+B de captura gen y la mudanza de valores de [[task-117]]. Sin cambios en requirements ni nginx.

## Preparación

- **Análisis previo delegado**: un ejecutor reconstruyó el runbook completo desde documenter y las skills `deploy-api`/`deployment` antes de tocar nada — inventario de commits, las 3 migraciones en orden de dependencia, seeds con veredicto de idempotencia y 6 preguntas abiertas para Ricardo.
- **Sondeos read-only en la RDS**: `django_migrations` sin rastro de las 3 migraciones nuevas (la enmienda en caliente de `survey/0009` no mordía en prod, a diferencia del entorno local); el único survey con datos en las 6 columnas a borrar era el de **«Ferprueba»** (`is_test`) — la premisa de task-117 («no hay datos reales de gen que salvar») quedó confirmada empíricamente.
- **Respaldos verificados antes de empezar**: dump `onigies_pre_gen_deploy_20260812_202658.dump` (`-Fc`, 611 entradas TOC) descargado a `/home/rick/databases/` y conservado en `~/unam/onigies/api/_backups/` del servidor como punto de rollback — único camino de regreso para las columnas borradas; y los 817 adjuntos (2.8 GB, la carpeta de subidas `~/unam/onigies/api/files/` del servidor) descargados a `/home/rick/respaldos/onigies-files-2026-08-12/` con conteo exacto (storage confirmado en disco local, no S3).

## Decisiones de Ricardo

1. **`migrate_flow_data` completo**, aceptando el riesgo de resurrección de comentarios de [[task-97]]: no se ha borrado ningún comentario en producción.
2. **Ventana de desfase frontend/backend aceptada**, minimizada con secuencia continua (~6 min entre el push que dispara Netlify y el reload del API). Este deploy rompía en ambas direcciones, así que la dirección segura del runbook no aplicaba.
3. **«Es test» → «De prueba»**: su corrección manual se integró al commit que introdujo el error (`fixup` + `rebase --autosquash`, 10 commits no pusheados reescritos) en vez de generar un commit propio.

## Ejecución y resultados

Secuencia: push `main` → ff `production` (`819c2ee..e5c6a51`, vía `git push origin main:production` sin checkout, por working tree sucio) → pull en servidor → `migrate` → seeds → flow → HUP.

- Migraciones `indicator/0009` (backfill de textos de grupo), `question/0004`, `survey/0009` (borrado de 6 columnas): **OK, cero drift** (`makemigrations --check` limpio).
- `load_sectors` + `load_questionnaire --sync-institutions`: «Grupos generales: 5 asegurados, 7 preguntas», 63 instituciones re-guardadas.
- `migrate_flow_data`: **609 evidencias espejadas → 661 = 661 [ok], sin huérfanas**; 8 comentarios legacy de features espejados; 1 reconciliación `bp_draft → bp_completed` de un paquete ya enviado. Alimenta [[task-7]].
- Reload con SIGHUP solo a `apionigies`; smoke: `/api/catalogs/all/` y `/api/` en 200, evidencia real bajo `/files/` en 200, log sin tracebacks nuevos, regla `v-count-input` viva en el `entry.css` publicado por Netlify (el fix del colapso aplica). Smoke visual de la captura gen confirmado por Ricardo.
- Cierre del ciclo: re-pull del servidor tras el commit documental (lección del 2026-08-04).

---
type: task
id: task-192
title: Deploy del nivel técnico superior
state: closed
date: 2026-10-02
owner: ai
parent: "[[task-2]]"
source: ["[[2026-10-02-alta-del-nivel-tecnico-superior]]"]
related: ["[[adr-0024]]", "[[adr-0025]]", "[[task-178]]", "[[task-186]]", "[[task-190]]", "[[task-200]]", "[[2026-10-03-deploy-del-nivel-tecnico-superior-y-la-valvula-de-admin]]"]
---

# Deploy del nivel técnico superior

Lleva a producción la rama `sector-tsu` ([[adr-0024]], [[adr-0025]]): la migración `answer.0008_technical_plans_in_plan_response`, el comando one-off `add_tsu_sector`, el filtro de alcance y el Nuxt. **Lo ejecuta Claude en la sesión de deploy**, nunca se entrega como pasos a Ricardo.

**Condición:** se corre cuando también haya cerrado la sesión onigies-fa (motor `flow`, [[task-190]]), que comparte `cp-backend`. `answer.0008` depende de `answer.0007` ([[task-178]]); la fusión de ramas es [[task-186]].

## Runbook

En el servidor del API (Yeeko), venv de `apionigies`:

1. Revisar el sector tal como lo dejó Rubén, para confirmar nombre exacto y `description` (el comando busca por nombre y respeta la descripción; lo demás lo sobreescribe):
   `python manage.py shell -c "from indicator.models import Sector; print(vars(Sector.objects.get(name='Alumnado de nivel técnico superior')))"`
2. `git pull` de la rama fusionada.
3. `python manage.py migrate answer`
4. `python manage.py add_tsu_sector` — esperado: «existente, banderas aseguradas», conteos reales de 2025, la cifra «nulas puestas en False» dice cuántas IES se guardaron entre el alta de Rubén y el comando, «ReachQuestion 1.16: sector agregado».
5. `sudo supervisorctl restart apionigies`
6. Deploy del Nuxt a Netlify.

**Cuidado:** `ensure_question` fuerza el orden 1–4 de las cuatro preguntas de planes de Generales (`PLANS_ORDER`); si Rubén reordenó esas preguntas a mano en el catálogo, el comando lo pisa. Revisar el orden vivo antes de correrlo.

## Resuelto (Ricardo, 2026-10-02)

Ninguna de las 3 IES con TSU tiene Generales aprobadas, así que el caso del grupo de planes del cp no ocurre: lo cambian ellas en Generales antes de llegar al cp. Ricardo lo cuida con Rubén fuera de la plataforma; no hace falta voltearlas en el deploy.

## Deploy hecho, 2026-10-03

Record: [[2026-10-03-deploy-del-nivel-tecnico-superior-y-la-valvula-de-admin]]. Se desplegó fusionada con `cp-backend` (`a32b48e`), con `migrate` completo (las tres migraciones, no solo `answer`). El orden fue el contrario al que pedía [[task-190]]: el push a `production` publicó Netlify a las 06:27:45 UTC y la API se reinició a las 06:28:50; ~1.5 min de front nuevo contra API vieja, sin candado de Netlify. Orden vivo de planes leído antes del comando (media 1, superior 2, posgrado 3: Rubén no lo había tocado); `add_tsu_sector` salió como se esperaba: sector 18 existente con banderas aseguradas, 67 encuestas 2025, 67 presencias en False (0 nulas, 0 respondidas), `technical_plans` creada (id 8) con 2 preguntas reordenadas, 67 respuestas `no_apply`, sector agregado al 1.16. Netlify en `07764370…`.

Los dos criterios que no cumple un deploy quedan sin marcar y pasan a [[task-200]], de Ricardo: los textos de las cuatro preguntas se editan en el dashboard, y las 3 IES con TSU quedan en «No» por lo resuelto arriba.

## Criterios de aceptación

- [x] Migración y comando corridos en producción con su salida en el record de deploy (2026-10-03)
- [ ] Textos vivos de las cuatro preguntas de planes del 1.12 editados por Rubén o Ricardo con «técnico superior» — no lo cumple el deploy; reasignado a [[task-200]] el 2026-10-03
- [ ] Las 3 IES con TSU puestas en «Sí» — no se voltean en el deploy (sección «Resuelto»); el aviso a Rubén de que el TSU ya está vivo va en [[task-200]]

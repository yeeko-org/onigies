---
type: task
id: task-192
title: Deploy del nivel técnico superior
state: open
date: 2026-10-02
owner: ai
parent: "[[task-2]]"
source: ["[[2026-10-02-alta-del-nivel-tecnico-superior]]"]
related: ["[[adr-0024]]", "[[adr-0025]]", "[[task-178]]", "[[task-186]]", "[[task-190]]"]
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

## Abierto (decisión de Ricardo)

Las 3 IES con TSU hoy quedan en «No». Si una de ellas ya capturó el 1.12 en el cp y después su Generales pasa de «No aplica» a un número de planes TSU, su grupo de planes del cp deja de pasar la compuerta («Falta el conteo de nivel técnico superior») hasta que capture ese nivel. Opciones: voltear a las 3 IES a «Sí» en el mismo deploy (con sus planes), o aceptar la devolución en revisión. No se resuelve aquí.

## Criterios de aceptación

- [ ] Migración y comando corridos en producción con su salida en el record de deploy
- [ ] Textos vivos de las cuatro preguntas de planes del 1.12 editados por Rubén o Ricardo con «técnico superior»
- [ ] Las 3 IES con TSU puestas en «Sí»

---
type: task
id: task-186
title: Limpieza de ramas y fusión de cp-backend ligada al deploy
state: open
date: 2026-09-28
owner: ricardo
related: ["[[adr-0001]]", "[[task-178]]", "[[2026-09-28-panorama-onigies]]"]
---

# Limpieza de ramas y fusión de cp-backend ligada al deploy

Estado de git al 2026-09-28, verificado en la sesión del panorama. `main`, `production` y `origin/main` coinciden en `de32e72`. `cp-backend` llevaba tres commits solo de documentación (estimación de costos) y desde el commit de hoy lleva además código sin desplegar: los `PROTECT` de [[task-178]], el manejador global de `ProtectedError` y la migración `answer 0007`; fusionarla a `main` equivale a desplegar ([[adr-0001]]: `main` y `production` avanzan por fast-forward). `claude/gallant-jemison` (`111e7c1`, 2026-04-15, «Corrige bugs reportados en prueba con usuarios reales») está 1 commit por delante y 120 por detrás de `main`; `git cherry` no encuentra su parche en `main` y toca `GoodPracticeCard.vue`, `GoodPracticeEditSimple.vue`, `SurveyInitData.vue` y `RegisterForm.vue`. Hipótesis sin verificar: esos arreglos se rehicieron en el rediseño de buenas prácticas. Siete ramas locales no tienen commits propios: `edicion-cuestionario-v2`, `fix_bugs_ia`, `questionnaire-ies`, `remove-statuscontrol`, `task-131-editor-observables-cuestionario-abierto`, `task-150-word-export`, `task-42-edicion-preguntas-dashboard`. Borrar ramas es decisión de Ricardo.

Actualización del 2026-09-28 por la noche ([[2026-09-28-revisoras-sin-is-staff-en-generales]]): `main` y `production` avanzaron a `a6cd4cd`, el arreglo de frontend de las revisoras, copiado por cherry-pick sobre `de32e72` para desplegarlo sin arrastrar la migración `answer 0007`. `cp-backend` (`6a08f0c`) **no contiene el arreglo**: su árbol sigue con la UI vieja (`isStaff` = `is_staff`) hasta que se rebase sobre `main`, que es lo que lo trae; no hay nada que omitir. La otra copia del arreglo, `37f202a`, vive solo en `reviewer-role-naming` (cp-backend más ese commit). Se suman dos ramas locales sin nada propio que conservar una vez rebasada `cp-backend`: `reviewer-role-naming` y `reviewer-role-naming-prod` (ya fusionada en `main`).

Actualización del 2026-10-02: `cp-backend` ya está rebasada sobre `main` (`a6cd4cd`), sin conflictos; era local, sin upstream. Sus siete commits quedaron encima del arreglo de las revisoras, así que el árbol ya trae `is_reviewer`. La fusión a `main` sigue atada al deploy de [[task-178]].

## Criterios de aceptación

- [ ] `cp-backend` fusionada a `main` en el mismo acto que el deploy de task-178 (migrate `answer 0007`)
- [ ] Verificado si los cuatro arreglos de `claude/gallant-jemison` existen en `main` por otra vía; la rama se borra o se rescata
- [ ] Ricardo decide sobre las siete ramas locales sin commits propios
- [x] `cp-backend` rebasada sobre `main` (`a6cd4cd`) (2026-10-02)
- [ ] Borradas `reviewer-role-naming` y `reviewer-role-naming-prod`

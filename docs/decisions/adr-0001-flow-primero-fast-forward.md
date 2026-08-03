---
type: decision
id: adr-0001
title: Ramas main/production sin divergencia — commits ordenados por destino y fast-forward
state: accepted
date: 2026-07-29
origin: ai
deliberation: confirmed
rationale: recorded
related: ["[[2026-07-29-commits-tematicos-y-deploy-flow]]", "[[2026-07-29-incidente-500-migracion-faltante]]"]
affects: ["api/", "nuxt/"]
---

# Ramas main/production sin divergencia — commits ordenados por destino y fast-forward

## Contexto y planteamiento del problema

El repo mantiene dos ramas con roles distintos: `main` (integración) y `production` (lo desplegado — Netlify construye el frontend con cada push y el API en Yeeko hace `git pull origin production`). El 2026-07-29 había ~60 archivos sin commitear que mezclaban temas, y solo una parte (la lógica de flows y el rename `/media→/files`) debía llegar a producción; el seed del cuestionario, no. Hacía falta una regla para pasar commits selectivamente de `main` a `production` sin ensuciar la historia.

## Criterios de decisión

- Historia lineal y legible: mismos SHAs en ambas ramas.
- Sincronizaciones futuras baratas: sin conflictos artificiales acumulados.
- Que "¿qué hay en producción?" se responda con `git log`, sin comparar parches.

## Opciones consideradas

- **Flow-primero + fast-forward** — en `main` se committean primero los temas destinados a producción y al final los que no; `production` avanza con `git merge --ff-only` hasta el último commit que sí entra. `production` queda siempre estrictamente detrás de `main`.
- **Cherry-pick selectivo** — commits en `main` en cualquier orden; los seleccionados se cherry-pickean a `production`. Más flexible, pero las ramas divergen (mismos cambios, SHAs distintos) y cada sincronización arrastra ese ruido.

## Resultado

Se eligió **flow-primero + fast-forward**. Precondición que hay que verificar cada vez: los cambios destinados a producción deben ser autocontenidos (sin depender de hunks de los temas que se quedan solo en `main`); si hay dependencia cruzada, se parte por hunks o se cae al plan B (cherry-pick) avisando.

### Consecuencias

- **Bueno:** cero divergencia; `production` es un prefijo exacto de `main`; los deploys se razonan como "avanzar el puntero".
- **Malo:** obliga a ordenar los commits por destino antes de crearlos, lo que a veces exige clasificar diffs grandes (como en esta sesión) o partir archivos por hunks.

### Cómo se comprueba

`git log --oneline production..main` muestra solo lo excluido de producción y `git log main..production` está vacío.

## Más información

Primera aplicación: [[2026-07-29-commits-tematicos-y-deploy-flow]].

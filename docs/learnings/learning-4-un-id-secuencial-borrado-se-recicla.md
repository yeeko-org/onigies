---
type: learning
id: learning-4
title: "Un id secuencial borrado se recicla: el tooling no sostiene la regla de que un id nunca se reutiliza"
state: pending
date: 2026-08-20
created: "2026-08-20T14:00:42-06:00"
scope: global
kind: new
author:
  role: subagent
  model: claude-opus-5[1m]
mode: requested
session: 9fe62aac-0320-41e0-8135-27bf4d63c60b
target: skills/documenter/SKILL.md
---

# Un id secuencial borrado se recicla: el tooling no sostiene la regla de que un id nunca se reutiliza

## Qué pasó

Ocurrido el 20 de agosto de 2026 en el monorepo ONIGIES. Ricardo lo formuló como pregunta abierta: «¿los ID de tasks o de docs se pueden quemar? Hay que tener un tratamiento claro para ello eventualmente».

El episodio: una task recién creada como `task-127` resultó ser de alcance global y se mudó al grafo de `~/.claude`, así que su archivo se borró del proyecto. Al crear dos tasks nuevas en la misma sesión, `doc.mjs create` volvió a repartir el 127 — reparte los ids secuenciales de una sola pasada sobre el árbol, así que un hueco en la numeración le parece disponible. Hubo que rehacer la creación pasando `id` explícito para saltarlo.

La regla existe y es tajante (§7 del skill: «El id nunca se reutiliza ni cambia, aunque el archivo se renombre»), pero **la sostiene la mano, no el tooling**. Es consistente con el diseño declarado —la fuente de verdad es el repo y no un contador aparte, precisamente para no desincronizarse—, y por eso el hueco es real: sin archivo no hay rastro del id consumido.

El daño no es cosmético. En esta sesión el `task-127` viejo ya había viajado en un reporte a Ricardo con otro contenido; si nadie nota el reciclaje, dos cosas distintas quedan citadas con el mismo id en conversaciones, commits y enlaces `[[id]]` de otros nodos.

## Propuesta

Que el skill defina un tratamiento explícito para los ids quemados, hoy inexistente. Tres piezas a decidir, ninguna obvia:

1. **Cuándo se quema un id.** Al menos en dos casos: un nodo mudado a otro grafo y un nodo borrado sin curar. Conviene nombrarlos, porque hoy la §7 solo prohíbe reutilizar sin decir qué hacer con el hueco.
2. **Dónde queda el rastro.** Un archivo lápida en la carpeta con `state` propio conserva la trazabilidad y el mecanismo del reparto por barrido sin tocar nada; un registro aparte de ids consumidos contradice el diseño de «la fuente de verdad es el repo». La primera parece más barata, pero es decisión de Ricardo.
3. **Que `create` no recicle.** Con lápidas, el barrido deja de ver el hueco y el problema se resuelve solo. Sin ellas haría falta que `create` avise en vez de asignar en silencio.

## Outcome

---
type: decision
id: adr-0003
title: El seed manda sobre el catálogo de estados; el admin no es fuente de verdad
state: accepted
date: 2026-07-03
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
affects: ["api/flow/seed.py", "api/flow/admin.py"]
---

# El seed manda sobre el catálogo de estados; el admin no es fuente de verdad

## Contexto

El seed del motor escribía el color **solo al crear** (`if created`), y eso era deliberado: preservaba lo que se editara desde el admin. Al rediseñar el seed en julio de 2026 hubo que decidir si esa preservación seguía teniendo sentido, ahora que también se sembrarían íconos y prioridades.

## Opciones consideradas

- **El admin manda** — quien opera edita en caliente y el seed respeta lo editado. Cómodo, pero la configuración real deja de estar en el repositorio y deriva en silencio entre entornos.
- **El seed manda** — `seed_flow` sobreescribe siempre color, ícono y prioridad; el admin sirve para experimentar y ver cómo se ve algo, no para fijarlo.

## Resultado

El seed manda. La razón de fondo no es técnica sino de a quién se le puede delegar esta configuración: **el catálogo de estados es demasiado intrincado para dejarlo en manos del cliente**. Son decenas de estados con transiciones, reglas de hijos, flags de comentario y confirmación, propagación y textos por rol; un cambio aparentemente cosmético en el admin puede dejar el flujo inconsistente sin que nadie lo note. Al vivir en `seed.py`, versionado, la configuración solo cambia por una edición deliberada de Ricardo, revisable en un diff.

### Consecuencias

- **Bueno:** la configuración del motor es reproducible, viaja con el código y se lee en el IDE; ningún entorno deriva por una edición suelta.
- **Malo:** todo ajuste, hasta cambiar un color, exige editar código y re-sembrar; y cualquier prueba hecha en el admin se pierde en el siguiente `seed_flow`.
- Condiciona a [[task-12]] (`export_flow_seed`, la sesión S6 opcional): un comando que regenere el seed desde la base solo tiene sentido como comodidad de Ricardo para volcar un experimento a código, nunca como camino para que el admin sea la fuente.

## Cómo se comprueba

Correr `seed_flow` después de editar un status en el admin devuelve el valor del seed.

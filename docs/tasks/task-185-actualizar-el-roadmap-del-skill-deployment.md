---
type: task
id: task-185
title: "Actualizar el roadmap del skill deployment: Fase 3 contra adr-0021 y cp ya en producción"
state: open
date: 2026-09-28
owner: ricardo
related: ["[[adr-0021]]", "[[task-100]]", "[[2026-09-28-panorama-onigies]]"]
---

# Actualizar el roadmap del skill deployment: Fase 3 contra adr-0021 y cp ya en producción

Hallazgo del panorama del 2026-09-28. La Fase 3 de `.claude/skills/deployment/references/roadmap.md` dice «Migrate or archive data from the legacy Python 2 Django», pero [[adr-0021]] (2026-09-25) decidió que lo histórico del ONIGIES original se conecta por liga y no se integra. Además el roadmap no se toca desde el 2026-09-11 y no refleja que el cuestionario principal está en producción desde el 25 de septiembre. Es una edición del harness del proyecto: se describe y aterriza con el ok de Ricardo.

## Criterios de aceptación

- [ ] Ricardo confirma cómo queda la Fase 3 (liga, no migración de datos) o si adr-0021 tiene una excepción que el roadmap deba nombrar
- [ ] El roadmap refleja cp en producción y el estado real de la Fase 1 (nada iniciado con la DGTIC)
- [ ] La contradicción DEBUG/CORS entre task-4 y task-115 queda resuelta en el mismo pase, leyendo el `.env` del servidor

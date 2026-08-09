---
type: task
id: task-93
title: Decidir los pendientes de la sesión de adjuntos y campos numéricos
state: closed
date: 2026-08-06
owner: ricardo
source: ["[[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]"]
related: ["[[task-67]]", "[[task-68]]", "[[task-55]]"]
---

# Decidir los pendientes de la sesión de adjuntos y campos numéricos

Batch de decisiones que quedaron abiertas al cierre de la sesión duo del 6 de agosto — Ricardo tuvo que salir. El contexto completo de cada una está en la bitácora [[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]] y el análisis UX de la señal numérica vive resumido en [[task-67]]. Ninguna bloquea lo ya construido: son afinaciones sobre el stack de adjuntos ([[adr-0010]]) y la decisión de UX de [[task-67]].

## Criterios de aceptación

- [x] task-67: elegida la señal del campo numérico — Ricardo diseñó algo mayor que las dos opciones: componente-fila con la pregunta a la izquierda e input fijo a la derecha, sobre un alias `VCountInput` de Vuetify; la primera implementación quedó mal visualmente y el rediseño sigue en [[task-96]]
- [x] task-67 anexas: los años de BP se quedan como están, con su validación actual; la retroalimentación al rechazo mudo queda fuera; el checkbox «sigue vigente» junto al año de fin (compromiso con Rubén) se anotó en [[task-31]]
- [x] Candado de periodo en adjuntos: se cierra **junto con** [[task-55]], un solo guard para ambos
- [x] Validación de archivo: límite de 30 MB, sin filtro de tipo ni extensión (deliberado) — implementado en `flow/serializers.py` con sus tests
- [x] Borrado físico: sí se borra el archivo del storage (señal `post_delete`), con anti-resurrección en `migrate_flow_data` (la ausencia del archivo funciona como lápida); la rama homóloga de comentarios quedó en [[task-97]]
- [x] Menores con default por paridad: confirmados sin cambios

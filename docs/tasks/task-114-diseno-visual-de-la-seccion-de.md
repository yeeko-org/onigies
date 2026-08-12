---
type: task
id: task-114
title: Diseño visual de la sección de evidencia probatoria
state: open
date: 2026-08-11
owner: ai
parent: "[[task-41]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-68]]", "[[adr-0011]]"]
---

# Diseño visual de la sección de evidencia probatoria

La evidencia probatoria vive hoy dentro del cuerpo del panel sin nada que la distinga del resto de la card: un rótulo de subtítulo y el componente de adjuntos, y ya. Hay que separarla visualmente, porque no es una pregunta más — es el respaldo de todo el bloque, y desde [[adr-0011]] es una expectativa que la interfaz comunica sin imponer, así que la comunicación visual carga con más trabajo que antes.

**Esto se registra como propuestas a dialogar, no como plan.** Decisión explícita de Ricardo: se resuelven al tomar la task, con pase por el skill `ux-designer`. Ninguna se ejecuta sin ese diálogo.

Propuestas sobre la mesa, **no excluyentes entre sí**:

- Superficie con variante tonal en el color de acento, entre el ocho y el doce por ciento, con el título también en acento.
- Borde izquierdo de tres o cuatro píxeles en acento: patrón de nota al margen.
- Icono de adjunto más un divisor — la versión mínima, si lo demás resulta ruidoso.
- De Ricardo: card tonal; divisor superior; título en otro color.

## Criterios de aceptación

- [ ] Las propuestas pasaron por el skill `ux-designer` y se dialogaron con Ricardo antes de ejecutar
- [ ] La evidencia probatoria se distingue visualmente del resto del cuerpo del panel
- [ ] La solución es la misma en la captura de la IES y en la vista de revisión

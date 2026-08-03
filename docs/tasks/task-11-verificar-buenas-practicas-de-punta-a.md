---
type: task
id: task-11
title: Verificar buenas prácticas de punta a punta y re-sembrar
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-1]]"
source: ["[[2026-06-23-progreso-frontend-del-flujo]]", "[[2026-07-03-auditoria-y-mejoras-del-flujo]]"]
---

# Verificar buenas prácticas de punta a punta y re-sembrar

La verificación manual del recorrido de bp nunca se corrió con el servidor levantado, y el rediseño visual del hint (S8) quedó pendiente de tu revisión en la app. Recorrido: IES responde «Sí» → agrega → marca completada → envía a revisión (confirmación y faltantes) → `bp_sent` con `sent_at`; revisora ve status, transiciones, comentarios y sliders, y ejecuta `bp_sent → bp_finished` con los hijos en `bp_for_ruling`/`bp_rejected`. Al desplegar hay que re-correr `seed_flow`.

## Criterios de aceptación

- [ ] El recorrido completo de bp funciona en la app, en ambas superficies
- [ ] `seed_flow` corrió tras el despliegue

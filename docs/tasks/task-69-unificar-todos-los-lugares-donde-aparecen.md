---
type: task
id: task-69
title: Unificar todos los lugares donde aparecen comentarios
state: open
date: 2026-08-06
owner: ai
parent: "[[task-99]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-44]]"]
---

# Unificar todos los lugares donde aparecen comentarios

§10 de la reunión con Fernanda, `[17:20]`–`[24:33]`. Los comentarios viven en tres niveles —a nivel de **buena práctica**, a nivel de **característica/criterio** y a nivel del **envío** (paquete completo)— y no se ven ni se comportan igual entre sí. Fernanda valoró muy bien el menú nuevo de comentarios («quedó increíble» comparado con lo anterior), pero la inconsistencia entre niveles sigue confundiendo.

**Encargo de Ricardo (2026-08-06): unificar todos y cada uno de los lugares donde aparecen comentarios.** No es un arreglo puntual; es un barrido completo. Se resuelve **en diálogo con Ricardo y con el skill `ux-designer`**, no de corrido.

Lo que la reunión dejó identificado y entra en el barrido:

- **Inconsistencia visual entre tipos de comentario:** el comentario a nivel de envío no se ve igual que el de buena práctica o el de criterio. Hay que unificar el estilo.
- **Color por defecto de los puntos del timeline — ya decidido:** hoy un comentario aparece en gris cuando no está asociado a un cambio de estatus, o en naranja cuando va asociado a «requiere ajustes». Se descartó el naranja como default, porque «requiere ajustes» es un estatus específico y no aplica cuando el estatus real es «completado». **Ricardo decidió `light-blue` como color por defecto** para los comentarios sin cambio de estatus asociado; está libre en los tres flujos del seed (`api/flow/seed.py`).
- **Reporte no confirmado, a verificar durante el barrido:** Fernanda reportó que al comentar en una buena práctica específica el comentario a veces parecía guardarse y desaparecía al cerrar y reabrir, recuperándose con Ctrl+R. **Ricardo no está seguro de que el bug sea real**, así que no se abre task de bug: se comprueba mientras se unifican las superficies y, si aparece, se arregla ahí.

Superficies: `nuxt/app/components/dashboard/flow/FlowComments.vue`, `FlowTimeline.vue`, `FlowCommentIcon.vue`, y los puntos donde se montan (`nuxt/app/components/dashboard/example/good_practice/FeatureItem.vue`, `GoodPracticeEditSimple.vue`, `nuxt/app/components/dashboard/example/good_practice_package/GoodPracticePackageEditSimple.vue`). El motor está en el skill `flow`; el reparto por audiencia, en el skill `bp-validation-ux`.

## Criterios de aceptación

- [ ] Están inventariados todos los lugares donde aparece un comentario
- [ ] Los tres niveles (envío, buena práctica, criterio) usan la misma presentación
- [ ] El color por defecto del punto de timeline sin cambio de estatus es `light-blue`
- [ ] Se verificó si el comentario que «desaparecía» hasta refrescar es real, y quedó corregido o descartado con razón escrita
- [ ] El diseño se resolvió en diálogo con Ricardo, con el skill `ux-designer`

---
type: task
id: task-70
title: Editar y borrar los comentarios propios mientras el envío siga de tu lado
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Editar y borrar los comentarios propios mientras el envío siga de tu lado

§10 de la reunión con Fernanda, `[17:20]`–`[24:33]`. Fernanda pidió un botón para editar comentarios; Ricardo detectó además que hoy no se puede borrar un comentario general ya guardado (lo probó con el COLEF), y propuso que si el envío está en tu turno y son tus últimos comentarios, debería permitirse.

**La regla que enunció Ricardo en la llamada:** se puede editar o borrar un comentario **mientras el envío siga de tu lado**; una vez que la contraparte ya lo vio o empezó a atenderlo, ya no debería poder modificarse. Es la misma noción de turno que gobierna la edición de contenido en el motor (`canEditContent`, skill `flow`).

Aplica a los tres niveles de comentario. El caso que lo motivó: Fernanda metió un comentario general muy largo en la buena práctica equivocada («agenda estadística») cuando debía ir a nivel de envío, y no pudo moverlo ni borrarlo; Ricardo le pidió eliminar el duplicado para que la IES no viera dos y no fue posible desde la interfaz.

## Criterios de aceptación

- [ ] Se puede editar un comentario propio mientras el envío siga del lado de quien lo escribió
- [ ] Se puede borrar un comentario propio bajo la misma condición
- [ ] Cuando el envío ya pasó a la contraparte, el comentario queda inmutable
- [ ] La regla aplica a los tres niveles: envío, buena práctica y criterio

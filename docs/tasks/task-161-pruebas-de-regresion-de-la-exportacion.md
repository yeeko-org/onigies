---
type: task
id: task-161
title: Pruebas de regresión de la exportación a Word y de los documentos públicos
state: open
date: 2026-09-22
owner: ai
parent: "[[task-2]]"
related: ["[[task-150]]", "[[task-151]]", "[[2026-09-22-exportacion-del-cuestionario-a-word]]"]
---

# Pruebas de regresión de la exportación a Word y de los documentos públicos

Plan de pruebas acordado con Ricardo el 2026-09-22 al cerrar la sesión de [[task-150]]. Lo escribe un ejecutor **después del deploy** (el deploy va primero, en una sesión nueva justo tras el commit de la rama `task-150-word-export`). Las pruebas 1, 3 y 4 son parte del encargo; la 2 es opcional.

1. **Descarga pública.** Anónimo recibe 200 con el tipo de contenido del .docx y el nombre de adjunto; un slug desconocido da 404; un documento en borrador da 404 a anónimos y 200 a una revisora.
2. **(Opcional) Constructor.** Sobre un fixture chico, conteos estructurales del .docx (encabezados de observable, filas de `Option Table` por pregunta A, tablas de verificación) y la nota cruzada del 1.7.
3. **Plantilla.** `template.docx` conserva los estilos y numeraciones que busca el writer: `Option Table`, `List Item`, `OnigiesLetter`, la imagen `image2.png` y el `updateFields`.
4. **`PublicDocument`.** Archivo-o-generador exactamente uno (400 si no); el endpoint de gestión cerrado a anónimos e IES; el slug se desduplica; el borrado de un generado se rechaza; el cambio de slug de un generado se rechaza.

Nivel: pytest + pytest-django, junto al código (`api/documents/`, `api/question/export/`). Al terminar, revisar que `TESTING.md` siga al día.

## Criterios de aceptación

- [ ] Pruebas 1, 3 y 4 escritas y en verde
- [ ] Cada prueba muerde: revertir el comportamiento la hace fallar
- [ ] Decidido con Ricardo si se escribe la prueba 2
- [ ] TESTING.md revisado

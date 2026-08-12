---
type: task
id: task-65
title: Rediseñar el correo de recuperación de contraseña
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
related: ["[[task-38]]"]
---

# Rediseñar el correo de recuperación de contraseña

§4 de la reunión con Fernanda, `[10:06]`–`[10:50]`. Ricardo vio el correo de recuperación y le pareció feo. Fernanda aclaró que el rosa fue decisión de Rubí, que no quería que la marca ONIGIES se asociara con la UNAM.

**El rosa como color de marca es correcto y no se revalida con Rubí.** Lo que no funciona es el rosa **como fondo del header del correo**. Dos cambios concretos: cambiar ese fondo y usar la tipografía oficial de ONIGIES.

Archivos: `api/email_send/templates/email/password_recovery.html` y `api/email_send/templates/email/base_email.html`. Ojo con la restricción del medio, ya anotada al cierre de [[task-38]]: los clientes de correo no soportan variables CSS, así que la paleta y la tipografía van en línea. El procedimiento de plantillas está en el skill `send-mail`.

## Criterios de aceptación

- [ ] El header del correo ya no usa el rosa como fondo
- [ ] El correo usa la tipografía oficial de ONIGIES
- [ ] El resto de las plantillas que heredan de `base_email.html` siguen viéndose bien

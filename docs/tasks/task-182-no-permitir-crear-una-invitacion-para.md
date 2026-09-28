---
type: task
id: task-182
title: No permitir crear una invitación para un correo ya registrado
state: open
date: 2026-09-28
owner: ai
related: ["[[task-64]]"]
---

# No permitir crear una invitación para un correo ya registrado

Dato de Ricardo (2026-09-28): «no debería poder agregar una invitación de un correo ya registrado». Hoy el dashboard acepta crear una invitación cuya dirección ya pertenece a un usuario existente. Solo se abre; no se implementa en esta sesión. Contexto: el registro ya rechaza correos duplicados (`validate_email` de `api/api/views/auth/serializers.py`, «Ya existe una persona usuaria registrada con este correo»); el hueco está en `InvitationTokenCreateSerializer.validate`, que solo exige correo o institución. Contexto de la app en el skill `invitations`.

## Criterios de aceptación

- [ ] Propuesta a Ricardo: validar en el serializer de invitaciones que el correo no corresponda a un usuario ya registrado (¿también a una invitación pendiente?), con el mensaje de error que verá quien invita
- [ ] Implementado con su ok, con la validación en el backend y el mensaje visible en el formulario del dashboard

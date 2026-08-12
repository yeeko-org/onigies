---
type: task
id: task-64
title: Investigar la lentitud al crear una invitación
state: open
date: 2026-08-06
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-06-temas-reunion-fer]]"]
---

# Investigar la lentitud al crear una invitación

§3 de la reunión con Fernanda, `[03:43]`–`[10:04]`. Crear una invitación nueva desde el dashboard tarda «un montón». Sospecha de Ricardo en la llamada: el envío del correo.

Hipótesis a verificar antes de tocar nada: el envío es síncrono dentro del request. El punto de entrada está en `api/email_send/service.py`, y el contrato desde el frontend está descrito en el skill `invitations`. Primero medir dónde se va el tiempo (SMTP, render de plantilla, o la creación misma); recién entonces decidir si se mueve a segundo plano o basta con dar retroalimentación en la interfaz mientras ocurre.

## Criterios de aceptación

- [ ] Está identificado dónde se va el tiempo al crear una invitación
- [ ] La creación responde rápido o la interfaz indica claramente que está en curso

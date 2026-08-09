---
type: task
id: task-94
title: Tests de regresión del stack de adjuntos sobre flow
state: open
date: 2026-08-06
owner: ai
source: ["[[2026-08-06-sesion-duo-adjuntos-sobre-flow-y]]"]
depends-on: ["[[task-93]]"]
related: ["[[task-68]]", "[[adr-0010]]"]
---

# Tests de regresión del stack de adjuntos sobre flow

Propuesta salida de la sesión de adjuntos ([[adr-0010]]). Candidatos backend, en `api/flow/tests/` (desde 2026-08-09 es paquete; los de adjuntos irían en `test_attachments.py`, que ya cubre tamaño y borrado físico): 1) la IES dueña sube → 201, `event` null, `uploaded_by`/`target` correctos; 2) IES ajena → 403 en GET/POST/DELETE (la regresión que cierra el hueco viejo del `EvidenceViewSet`); 3) revisora → 200 en GET, 403 en POST/DELETE; 4) paquete enviado (turno de revisión) → 403 a la IES dueña — la raíz gobierna; 5) `FeatureGoodPractice` hereda los tres casos de su `GoodPractice` (`flow_delegate`); 6) DELETE de un adjunto de otro target → 404; 7) modelo ni participante ni delegado → 404; 8) `resolve_upload_path`: gen → `attachments/{acronym}/{period}_general/group_{name}/`, BP → `evidences/` plano (convivencia con lo migrado); 9) `flow_attachments` presente en los tres serializers de detalle sin crecer en queries (prefetch). Frontend (Vitest, depende de la task del arnés): render y permisos de `FlowAttachments.vue`.

## Criterios de aceptación

- [ ] Ricardo acotó la lista propuesta (regla de la casa: los tests se proponen, no se escriben solos)
- [ ] Los tests aprobados existen en `api/flow/tests/` y corren en verde
- [ ] TESTING.md refleja la cobertura nueva

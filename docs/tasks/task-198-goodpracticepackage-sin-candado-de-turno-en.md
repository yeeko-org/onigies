---
type: task
id: task-198
title: GoodPracticePackage sin candado de turno en el servidor y con survey escribible
state: open
date: 2026-10-02
owner: ai
parent: "[[task-6]]"
related: ["[[adr-0026]]", "[[task-193]]"]
---

# GoodPracticePackage sin candado de turno en el servidor y con survey escribible

[[adr-0026]] cerró pertenencia y escritura por turno en práctica y criterio, pero `GoodPracticePackageViewSet` quedó fuera: no tiene candado de contenido por turno y su serializer expone `survey` por `fields='__all__'`, la misma clase de hueco que se cerró para la FK `package` de la práctica (una IES podría apuntar su paquete a otra encuesta). Lo señaló el crítico del 2026-10-02; no se probó. Aplicar el mismo patrón: `survey` solo lectura y `user_can_edit_flow_content` para la IES en `perform_update`.

## Criterios de aceptación

- [ ] `survey` es solo lectura en los serializers del paquete
- [ ] La IES no edita el paquete fuera de su turno (403 probado)
- [ ] Test en `api/example/tests.py`

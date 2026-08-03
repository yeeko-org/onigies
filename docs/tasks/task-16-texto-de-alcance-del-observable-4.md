---
type: task
id: task-16
title: Texto de alcance del observable 4.4
state: open
date: 2026-08-03
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-07-03-dudas-del-instrumento-con-el-cliente]]"]
---

# Texto de alcance del observable 4.4

El observable 4.4 (personas de primer contacto especializadas en violencias de género) tiene copiadas literalmente las preguntas de alcance de los observables de armonización normativa: «¿A qué poblaciones se consideró este proceso de armonización?». Es un error de copiado del instrumento original y está sembrado verbatim. Hay propuesta redactada, falta que el cliente la confirme.

Al resolverse: corregir [[cuestionario-2026-reducido]], luego `api/question/seed_data/axis_4.py`, y re-correr `load_questionnaire`.

## Criterios de aceptación

- [ ] El cliente confirmó el texto
- [ ] El instrumento reducido, el seed y la base dicen lo mismo

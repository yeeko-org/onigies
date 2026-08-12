---
type: task
id: task-104
title: El logo institucional es obligatorio al guardar y no debería serlo
state: open
date: 2026-08-11
owner: ai
parent: "[[task-3]]"
source: ["[[2026-08-11-reunion-con-ruben-sobre-la-informacion-base]]"]
related: ["[[task-62]]"]
---

# El logo institucional es obligatorio al guardar y no debería serlo

Visto en vivo durante la reunión del 11 de agosto, `[31:59]`: al guardar una institución desde el dashboard se exige el logo. Ricardo dijo en la llamada que lo corrige.

En el modelo no es obligatorio — el campo `logo` de `Institution`, en `api/ies/models.py`, admite vacío y nulo. La exigencia no venía del esquema de datos.

## Diagnóstico y cura (2026-08-11)

Confirmado: es **el mismo bug** que [[task-62]] tenía anotado como «error preexistente al guardar desde el dashboard de institución». Esta task lo absorbe entero y aquélla se queda solo con la estandarización del lenguaje.

El síntoma es un 400 con `{"logo": ["The submitted data was not a file..."]}`. La causa está en el frontend: al construir el PATCH reenvía el valor del logo **tal como llegó en el GET** —la URL, o el objeto que la envuelve—, y el backend espera un archivo. No es que falte el campo: es que se manda mal justamente cuando ya existe.

La cura es doble, y cada mitad arregla una cosa distinta:

- **Frontend:** excluir `logo` del payload salvo que la usuaria haya elegido un archivo nuevo. Esto quita el 400.
- **Backend:** declarar el campo `required=False, allow_null=True` en el serializer. Esto resuelve lo que Rubén vio en la demo — que el logo se exija cuando la institución no tiene ninguno.

Sin la segunda mitad se corrige el error al guardar, pero sigue sin poderse crear una institución sin logo, que es lo que Ricardo dijo en la llamada que quería resolver.

## Criterios de aceptación

- [ ] Se guarda una institución que ya tiene logo, sin tocarlo, y no hay 400
- [ ] Se guarda una institución sin logo desde el dashboard
- [ ] El frontend no manda `logo` en el payload salvo que haya archivo nuevo
- [ ] El serializer declara el campo opcional y anulable

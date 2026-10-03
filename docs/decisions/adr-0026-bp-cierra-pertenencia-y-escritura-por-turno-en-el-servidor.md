---
type: decision
id: adr-0026
title: "Buenas prácticas cierra en el servidor la pertenencia por institución y la escritura por turno"
state: accepted
date: 2026-10-02
origin: ricardo
deliberation: dialogued
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
rationale: recorded
supersedes: null
superseded-by: null
affects:
  - api/api/views/example/__init__.py
  - api/api/views/example/serializers.py
  - api/flow/permissions.py
  - nuxt/app/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue
related: ["[[adr-0019]]", "[[adr-0023]]", "[[task-70]]", "[[task-193]]"]
---

# Buenas prácticas cierra en el servidor la pertenencia por institución y la escritura por turno

## Contexto y planteamiento del problema

Al poner bajo turno la nota privada por criterio ([[task-70]]) se revisó el viewset de criterios y apareció que ni él ni el de la buena práctica tenían clase de permiso propia ni filtro por institución: aplicaba el default global (lectura anónima, escritura para cualquier usuaria autenticada). En la base de pruebas, con dos instituciones, la IES A editó criterios de la B, una petición anónima leyó justificaciones de la B, y la IES A **borró una práctica de la B** por `DELETE`. Además la escritura de contenido de bp no estaba atada al turno del flujo en el servidor: una IES podía, por API, editar justificación o «sí lo tiene» de un criterio con el envío ya en revisión, calificarse (`final_option`, `final_value` ocultos al leer pero no al escribir), mover un criterio a otra práctica, crear criterios en prácticas ajenas y cambiar el `status` de su práctica por `PATCH` saltándose el motor. Solo la interfaz lo impedía. En cp todo esto ya lo resolvían `InstitutionScopedMixin`, `IsFlowInstitutionOwnerOrReviewer` y `ContentWriteMixin`.

## Criterios de decisión

- Que el servidor sea la frontera, no la interfaz: lo que la UI oculta, la API lo rechaza.
- Un solo patrón de permisos para los tres flujos, en vez de uno nuevo para bp.
- No romper los guardados legítimos de la IES, que reenvía campos ocultos.

## Opciones consideradas

- **Dejarlo y abrir una task** — el riesgo era real y las revisoras trabajan sobre bp a diario.
- **Mínimo** — pertenencia por institución y FK de práctica solo lectura, sin atar contenido al turno.
- **Permiso base del flujo con delegación + pertenencia + escritura por turno + campos de revisión solo para revisoras** — la elegida: Ricardo pidió «de una vez completo» y luego «de una vez» para la escritura por turno.

## Resultado

Se eligió la tercera, en el mismo diff:

- `IsFlowInstitutionOwnerOrReviewer` resuelve el dueño por `flow_delegate` (`resolve_flow_owner`), así que un satélite como el criterio hereda la institución de su práctica sin clase aparte.
- `GoodPracticeViewSet` y `FeatureGoodPracticeViewSet` llevan `InstitutionScopedMixin` (anónimo nada, IES solo lo suyo, revisión todo) y ese permiso; al crear o mover validan que el paquete o la práctica sean de la propia institución.
- `PracticeContentWriteMixin`: la IES escribe contenido solo con `user_can_edit_flow_content` sobre la práctica (al crear, sobre el paquete); la revisión no tiene candado de contenido pero solo escribe sus campos de calificación (`final_value`; `final_option`, `comments`, `reviewers`) y lo demás se le descarta; a la IES se le descartan en silencio los campos de calificación (responder 403 rompería su guardado, porque el formulario reenvía los campos ocultos vacíos).
- `status` es solo lectura en los serializers de práctica y paquete: cambia solo por `/flow/…/transitions/`.
- La revisión no borra prácticas ni criterios (403 en `DELETE` y `confirm-delete/`); el botón «Eliminar» de la IES se oculta fuera de su turno.
- Las cuentas admin (`User.is_admin`) quedan exentas de las tres reglas de revisión en bp —borrar, crear y el descarte de contenido—, espejo de la válvula de [[adr-0023]]; la nota de criterio sigue bajo turno para todas. Lo decidió Ricardo el 2026-10-02 («D1. (2)») cuando el crítico mostró que `is_reviewer` incluía a staff y superusuario y el coordinador había presentado la regla como de un solo camino.
- Se mantiene `disable_protection` en la práctica: nace con sus diez criterios y sin eso cada borrado de la IES pediría confirmación.

### Consecuencias

- **Bueno:** el servidor rechaza lo que la interfaz escondía, con el mismo patrón de pertenencia y turno que cp y gen en práctica y criterio.
- **Malo:** `GoodPracticePackageViewSet` sigue sin candado de turno y con `survey` escribible por `fields='__all__'`, y la calificación (`final_option`, `final_value`) no se bloquea por turno: una revisora puede recalificar un envío finalizado ([[task-198]], [[task-199]]).
- **Malo:** un guardado de la IES fuera de turno que antes pasaba en silencio ahora da 403; la UI ya no ofrece esos guardados, pero un cliente viejo o un script los verá fallar.
- **Malo:** el periodo cerrado sigue sin candado en el servidor para bp ([[task-193]]).

### Cómo se comprueba

`GoodPracticeFenceTests`, `CriterionFieldsTests` y `PracticeContentTurnTests` en `api/example/tests.py`: anónimo 401, otra institución 404 en lectura y borrado, IES fuera de turno 403, calificación de la IES ignorada, revisora no borra, `status` por PATCH ignorado.

## Más información

[[2026-10-02-comentarios-editables-y-valvula-de-admin]] (P16, P17, P20 y los tres ajustes finales).

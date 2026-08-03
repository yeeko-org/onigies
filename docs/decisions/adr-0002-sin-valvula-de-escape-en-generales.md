---
type: decision
id: adr-0002
title: "Sin válvula de escape en generales y buenas prácticas: los terminales son absolutos"
state: accepted
date: 2026-07-03
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-07-03-auditoria-y-mejoras-del-flujo]]", "[[2026-06-05-diseno-del-motor-de-flujo]]"]
affects: ["api/flow/seed.py"]
---

# Sin válvula de escape en generales y buenas prácticas: los terminales son absolutos

## Contexto

El diseño v2 del motor contemplaba una reapertura para generales: `gen_approved → gen_need_changes`, descrita como válvula de escape para que la revisora pudiera reabrir en vez de dejar un terminal puro. La transición se perdió al implementar el seed, y la auditoría de julio de 2026 la reportó como hallazgo (§4-3), es decir, la trató como omisión a corregir. La pregunta que llegó a Ricardo fue si restituirla, y si convenía una equivalente en buenas prácticas.

## Opciones consideradas

- **Restituir la reapertura en `gen` (y agregar una en `bp`)** — le da a la revisora una salida cuando aprueba por error, al costo de que ningún estado sea realmente final.
- **Terminales absolutos en `gen` y `bp`** — solo el cuestionario principal conserva su válvula, `cp_voluntary_readjust`.

## Resultado

Terminales absolutos. La razón es la dependencia entre grupos: **los generales alimentan el arranque del cuestionario principal**, así que reabrirlos después invalidaría lo que ya se construyó sobre ellos. En buenas prácticas el argumento es distinto y más simple: son pocas prácticas por institución y el ciclo de revisión es corto, así que una válvula no paga su complejidad.

`gen_approved`, `gen_finished`, `bp_finished`, `bp_rejected` y `bp_for_ruling` quedan sin transiciones de salida (`role=None`).

### Consecuencias

- **Bueno:** el estado aprobado significa algo firme; lo que depende de generales puede confiar en que no se mueve bajo sus pies.
- **Malo:** un error detectado después de aprobar no tiene camino por la interfaz. Qué hacer en ese caso (corrección por admin, rehacer el periodo, convivir con el error) no está definido y hoy sería intervención manual.
- Esta decisión existe sobre todo para que la ausencia de la transición no vuelva a leerse como bug: ya se reportó una vez como hallazgo y es barata de "arreglar" por descuido.

## Cómo se comprueba

En `api/flow/seed.py`, ningún status del grupo `gen` ni los terminales de `bp` aparecen como origen en `NEXT_STATUSES`.

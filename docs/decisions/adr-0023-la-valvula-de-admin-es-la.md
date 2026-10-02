---
type: decision
id: adr-0023
title: "La válvula de admin es la única salida de un terminal: adr-0002 sigue para el flujo normal"
state: accepted
date: 2026-10-02
origin: ricardo
deliberation: dialogued
rationale: recorded
source: ["[[2026-10-02-comentarios-editables-y-valvula-de-admin]]"]
affects: ["api/flow/seed.py", "api/flow/services.py", "api/flow/views.py", "api/flow/urls.py", "api/flow/permissions.py", "nuxt/app/composables/useFlowActions.js", "nuxt/app/store/auth.js"]
related: ["[[adr-0002]]", "[[adr-0019]]"]
---

# La válvula de admin es la única salida de un terminal: adr-0002 sigue para el flujo normal

## Contexto y planteamiento del problema

[[adr-0002]] dejó sin transiciones de salida a `gen_approved`, `gen_finished`, `bp_finished`, `bp_rejected` y `bp_for_ruling`, y anotó como consecuencia mala que «un error detectado después de aprobar no tiene camino por la interfaz». Ese camino hacía falta: una revisora devuelve un grupo gen sin devolver el paquete ([[task-58]]) y el grupo queda en rol IES bajo una raíz que sigue en turno revisor; una práctica marcada «recibida para dictamen» por error no vuelve; y el motor, que solo mira el rol del status propio y `next_statuses`, no deja que nadie, staff incluido, lo corrija. Hoy eso es intervención manual en la base.

Ricardo pidió el 2026-10-02 que los usuarios admin puedan llevar un hijo o nieto a cualquier status que la revisión puede establecer, desde cualquier origen, terminales incluidos, mientras la raíz esté del lado de la revisión ([[2026-10-02-comentarios-editables-y-valvula-de-admin]]).

## Criterios de decisión

- Que el flujo normal no cambie: lo que [[adr-0002]] protege (que un aprobado signifique algo firme) sigue valiendo para toda revisora.
- Que el error tenga un camino por la interfaz sin tocar la base.
- Que quien lo use sepa que está fuera del flujo y lo deje escrito.

## Opciones consideradas

- **Solo saltar el rol propio del hijo, conservando `next_statuses`** — desde `gen_need_changes` los destinos son los de la IES, así que no resuelve el caso de [[task-58]].
- **Cualquier destino que establece la revisión, desde cualquier origen no terminal** — respeta [[adr-0002]] a la letra, pero deja sin salida justo los errores sobre terminales (`bp_for_ruling`, `gen_approved`).
- **Cualquier destino que establece la revisión, desde cualquier origen, terminales incluidos, solo para admin y con confirmación explícita** — la elegida.

## Resultado

Se eligió la tercera. Es una válvula, no una transición: no se agrega a `NEXT_STATUSES`, no la ve una revisora y no aparece en el menú de transiciones. Sus límites:

- Solo usuarios con `User.is_admin` (`is_superuser or is_staff`); el frontend lo decide por un getter `is_admin` del store, nunca por `is_staff` en un componente ([[2026-09-28-revisoras-sin-is-staff-en-generales]]).
- Solo hijos y nietos, nunca la raíz, y solo mientras la raíz tenga rol reviewer; en `cp` la raíz es el eje (`AxisValue`), no la encuesta.
- Destinos: los que la revisión establece (destinos de sus transiciones en `NEXT_STATUSES`) más los status de rol `reviewer` del grupo, para deshacer y devolverle el turno; nunca un status que solo la IES establece. Salta el rol propio del hijo y `next_statuses`; conserva la regla de hijos y la propagación.
- Comentario obligatorio, que queda en el timeline. No hay columna nueva: un evento cuyo destino no está entre los siguientes legales de su origen y que trae comentario es, por definición, un cambio administrativo, y así se pinta («Cambio administrativo»), visible por igual para la IES y la revisión.
- Endpoint propio (`admin-transitions/`), para que el de transiciones normales no cambie.

[[adr-0002]] no se reemplaza: sigue gobernando el flujo normal y la seed. Este ADR es su única excepción.

### Consecuencias

- **Bueno:** el error de revisión tiene salida sin tocar la base, y queda en la bitácora con su razón.
- **Malo:** reabrir un grupo gen aprobado puede invalidar lo que el cuestionario principal ya construyó sobre él; el diálogo de confirmación lo advierte y pide confirmación explícita, pero no lo impide. Es una decisión de quien aprieta el botón.
- **Malo:** `is_staff` gana por primera vez un poder propio en el flujo; hay que mantener la distinción `is_reviewer` / `is_admin` limpia y probada ([[task-189]]).

### Cómo se comprueba

En `api/flow/seed.py` ningún terminal aparece como origen en `NEXT_STATUSES` (igual que hoy). El endpoint de transiciones normales rechaza con 400 un destino fuera del grafo para cualquier usuario; `admin-transitions/` lo acepta solo con `is_admin`, comentario y raíz en rol reviewer.

## Más información

[[2026-10-02-comentarios-editables-y-valvula-de-admin]], [[task-58]], [[task-87]], [[task-71]].

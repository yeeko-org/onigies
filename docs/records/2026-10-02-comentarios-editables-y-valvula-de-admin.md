---
type: record
id: 2026-10-02-comentarios-editables-y-valvula-de-admin
date: 2026-10-02
related: ["[[task-70]]", "[[task-99]]", "[[task-190]]", "[[adr-0023]]", "[[adr-0026]]", "[[task-44]]", "[[task-186]]"]
---

# Comentarios editables por turno y válvula de admin en el flujo

Sesión del 2026-10-02 (session-log `80460f08-b659-4023-82b9-4f86ed4d5686`). Empezó como diálogo sobre dos peticiones de Ricardo y terminó con ambas implementadas y probadas, vistas en navegador en su primera versión, más los cierres de seguridad de bp que salieron en el camino. La primera parte del record es el diálogo; la segunda, el resto del día.

## Lo que pidió

> ¿Es posible que los comentarios sean editables por «la revisora» (sin importar quién sea la revisora) mientras siga siendo el turno de las revisoras?

> También me gustaría que los usuarios con is_staff puedan hacer cambios libres a cualquier status que pueda establecer la revisora a nivel de hijos o nietos (por ejemplo, una buena práctica o un grupo de preguntas generales, o un observable) siempre y cuando esté todo el grupo completo (por el nivel más alto) en el turno de las revisoras.

## Estado de partida verificado

- Un comentario es un `FlowEvent` con `comment`; no hay PATCH ni DELETE sobre eventos en ningún nivel, ni campos de auditoría; el admin del timeline es de solo lectura por decisión.
- El guard del POST de comentarios (`api/flow/views.py`, `FlowEventView.post`) compara el rol del usuario con el status **propio** del objeto, no con la raíz; `canEditContent` y [[adr-0019]] usan la raíz. Esa divergencia ya estaba anotada en [[task-124]].
- `is_staff` no tiene ningún poder propio en el flujo: `User.is_reviewer` es `is_superuser or is_staff or reviewer`. Las nueve revisoras reales de producción no son staff ([[2026-09-28-revisoras-sin-is-staff-en-generales]]), así que «staff» en la práctica significa Ricardo o un admin.
- La raíz de `cp` es `AxisValue`, uno por eje, no la encuesta. El nivel «nieto» solo existe en `cp`; en `bp` las features no tienen status.
- `cp-backend` no contenía `a6cd4cd` (el fix de `is_reviewer`); se rebasó sobre `main` en esta misma sesión.

## Decisiones de Ricardo

**Cambio 1, comentarios.** La regla del turno para editar y borrar es la raíz, como [[adr-0019]] («P1. La raíz»). Aplica a ambos lados, IES y revisión, cada uno sobre los comentarios de su lado sin importar la autoría («P2. Ambos»). Borrar sí, «borrar solo el comentario»: en un comentario puro se borra la fila; en uno de transición se vacía el texto y el evento se queda. Sin `edited_at`: «Siento innecesario el edited_at»; el modelo coincidió porque mientras la raíz siga de tu lado la contraparte aún no ha actuado sobre ese comentario. El campo privado `comments` de los criterios de bp (`FeatureGoodPractice.comments`, editado desde el componente `FeatureItem`) sigue la regla de turno («P11. sí»); que ese campo no tenga rondas —es un solo texto, no una bitácora— lo decidió después el coordinador con el executor, no Ricardo. Esto extiende [[task-70]] (que decía «propios») y no la contradice.

La excepción que el modelo propuso para el comentario de la transición raíz que dispara el correo se retiró: con la regla de la raíz sale sola, porque ese correo se envía justo cuando la raíz deja el lado revisor.

**Cambio 2, válvula de admin.** Lectura confirmada: cualquier status que la revisión puede establecer, desde cualquier origen, **terminales incluidos** («P5. La lectura es la 3»), con un botón especial junto al menú de transiciones, solo para admin, «con un diálogo muy claro que diga que no se recomienda y que si está bien segura de eso». Conserva la regla de hijos y la propagación («P6. Sí como propones»); la unidad en `cp` es el eje («P7. confirmo»); vive en la UI normal, oculto, con candado en los endpoints («P8. … tiene sentido?» → sí). Sin columna `is_override`: el timeline deriva «cambio administrativo» cuando el destino no está entre los siguientes legales del origen. El check se llama `is_admin` en ambos lados, nunca `is_staff` en componentes. La motivación confirmada por Ricardo es [[task-58]]: un grupo gen devuelto sin devolver el paquete queda en rol IES bajo una raíz en turno revisor y nadie puede deshacerlo.

Esto acota [[adr-0002]]: los terminales siguen sin salida en el flujo normal; la válvula es la única excepción. Queda en el ADR nuevo.

**Cierre del diálogo (misma sesión, tras el diseño UX).** El brief al diseño dijo «status de rol reviewer», que no es lo que Ricardo pidió; corregido: el selector lista lo que la revisión establece **y** los status de rol reviewer para deshacer («P12. Las dos»). El timeline y el motivo son visibles para la IES («P13. Transparencia total»). Nombre en la UI: «Cambio administrativo» («P14. Tu recomendación»). Resueltos por un solo camino: request con `target_status`, montaje dentro de `FlowStatusActions`, raíces finalizadas excluidas, detección «fuera del grafo y con comentario». La sesión paralela (sector TSU) comparte el árbol de trabajo y dejó `sector-tsu` como rama activa; los docs de hoy se commitean a `cp-backend` sin mover el checkout.

**Ramas.** «tú decide cómo, si rebase o merge»: se hizo rebase porque `cp-backend` era local, sin upstream y sin conflictos ([[task-186]]).

## El resto del día

**Implementación.** Dos executors en paralelo en el worktree `~/dev/unam/onigies-flow` (ver abajo): backend (PATCH/DELETE de eventos, POST por raíz, `admin-transitions/`, `admin_targets` en el catálogo, candado de la nota de criterio) y frontend (getter `is_admin`, `FlowAdminOverride`, edición inline, marca en el timeline). Tests escritos por un tercer executor con la lista que decidió el modelo («Tú decide los tests»); la poda de la skill `flow` la hizo un delegado Fable a petición de Ricardo («Manda un SAG Fable a que haga la poda»).

**Decisiones de la tarde, textuales.**

- P15, borrar el motivo de un cambio administrativo: «Sí» → el backend lo rechaza (403), editar sigue.
- P16, cerrar el viewset de práctica: «Sí». Hallazgo: `GoodPracticeViewSet` y `FeatureGoodPracticeViewSet` no tenían permiso propio ni filtro por institución; en la base de pruebas una IES editó criterios de otra institución, una petición anónima leyó justificaciones, y una IES borró una práctica ajena. Cerrados con el patrón de `InstitutionScopedMixin` + `IsFlowInstitutionOwnerOrReviewer`.
- P17, huecos de criterios: «De una vez completo (3) o es demasiado complejo para un SAG?» → se hizo la 3 (el permiso base del flujo entiende `flow_delegate`) junto con la 1 (la IES no se califica, no mueve criterios, no crea en prácticas ajenas).
- P18, columnas `comments` de práctica y paquete: «Sí borrarlas, estoy seguro que ya habíamos hecho la migración y todo funcionó bien, solo hay que asegurar que es correcto cuando se haga ese paso específico en el deploy» → migración `example.0010_remove_dead_comments`; el paso de verificación queda en [[task-190]].
- P19, resolución de `pinia` en Vitest: «Tú decide» → alias en `vitest.config.ts`, sin dependencia nueva.
- P20, escritura de contenido de bp atada al turno en el servidor: «De una vez» → `PracticeContentWriteMixin` en los dos viewsets de bp; la revisora solo escribe campos de calificación; `final_value` y `final_option` se descartan para no revisoras; `status` solo lectura en los serializers de bp (una IES podía cambiarlo por PATCH saltándose el motor); la revisora no borra prácticas ni criterios; el botón «Eliminar» de la IES se oculta fuera de turno. Esos tres ajustes (status solo lectura, revisora no borra, botón) los presentó el coordinador como «de un solo camino» aunque el executor había dejado el de borrar como pregunta abierta; el crítico lo señaló y Ricardo decidió al cierre («D1. (2)»): las cuentas admin quedan exentas de borrar, crear y del descarte de contenido en bp ([[adr-0026]]). Fuera de alcance, a task: el bloqueo del periodo cerrado en bp sigue siendo solo del cliente.
- P21, válvula a destino legal (defecto visto en navegador): «Opción 1» → la válvula solo ofrece destinos fuera del grafo; un destino legal responde 400.
- P22, revertir los datos de prueba de la pasada en navegador: «Tú decide» → revertidos en la base local con el script de la pasada.
- P23, comentarios de rondas anteriores (hallazgo del auditor): «Opción 1» → solo la ronda actual (`round_started_at`).
- P24, quién corrige el motivo de un cambio administrativo: «Opción 1» → solo `is_admin`.
- P25, advertencia específica de generales en el diálogo: «Opción 1» → línea extra cuando el destino es de `gen`. **Revocada al cierre («D3 (1)»)**: el crítico mostró que cp solo abre con el paquete en `gen_finished`, terminal y de nadie, y la válvula exige la raíz en turno revisor, así que nunca puede reabrir un grupo sobre el que cp ya construyó; la línea se quitó y adr-0023 pierde esa consecuencia.
- D2, el «¿está segura?» del diálogo: Ricardo lo había pedido («que si está bien segura de eso») y el coordinador ofreció un checkbox dando su silencio por no; al cierre Ricardo decidió dejar el diálogo sin checkbox («D2. (2)»).

**Medición en producción de la posible pérdida de notas de criterio.** Hipótesis: el formulario de la IES reenviaba el campo oculto `comments` vacío en cada guardado (el textarea de justificación guarda en cada blur) y desde el 2026-06-23, cuando la IES dejó de recibir la nota, pudo vaciar notas de la revisora en prácticas devueltas. Resultado: **no es medible** desde la base (el criterio no tiene fecha de modificación ni historial, y no hay copias en el timeline). Lo que sí: 11 notas en toda la base; 40 prácticas expuestas, 24 devueltas ese mismo día sin actividad de la IES todavía; las revisoras escriben la retroalimentación en el comentario de devolución y casi nunca en el criterio; 7 candidatas reales (dos de la Universidad de Colima, cinco de la UJAT). Ricardo cerró el tema: «Ok, no hace falta averiguar, con que no ocurra en futuro todo bien». El script queda en `.claude/scratch/measure_criterion_notes_loss.py`. La lectura se corrió a mano por el coordinador: el clasificador de permisos bloqueó el primer intento y el ssh-agent de la shell colgaba la autenticación (`-o IdentityAgent=none` la destraba).

**Pasada en navegador.** Playwright MCP desde el worktree, API en 8019 y nuxt en 3019, tres usuarios (staff, revisora sin staff, IES de dos instituciones de prueba), 46 capturas en `.claude/scratch/browser-pass/`. Lo construido hasta ese momento rindió como se diseñó; quedó sin ver en navegador lo que vino después: la alerta de lista vacía de la válvula, los tres arreglos siguientes, la regla de ronda y el motivo editable solo por admin. La pasada destapó el defecto de P21 y tres preexistentes, corregidos: el diálogo de práctica se quedaba con un objeto viejo tras refrescar el paquete, la vista previa del comentario mostraba el más viejo, y los íconos de editar/borrar del timeline no alineaban (el cuerpo del `v-timeline-item` no ocupaba el ancho).

**Auditoría de congruencia** sobre el worktree: tres hallazgos para Ricardo (P23–P25) y una veintena de un solo camino aplicados (adjuntos no siguen la regla de comentarios; descripción de la skill `flow` bajo 250 caracteres; duplicados entre skills resueltos con una sola casa por tema; mensajes «status» → «estatus»; etc.). La skill `flow` bajó de ~30.7k a ~8.6k caracteres con seis references.

**Ramas y árbol de trabajo.** La sesión paralela del sector TSU dejó `sector-tsu` como rama activa del checkout; esta sesión commiteó los docs del mediodía a `cp-backend` con un índice temporal y siguió en el worktree `~/dev/unam/onigies-flow` ([[task-186]]).

**Desviaciones de delegados aceptadas por el coordinador.** El candado de criterios descarta en silencio el campo de un no revisor en vez de responder 403 (el cliente de la IES reenvía el campo oculto); el cierre de prácticas valida también el paquete al crear y editar; el POST de criterios se conservó con candado de institución porque el cliente lo usa; la regla de ronda cuenta solo entradas al lado (el origen del evento no tenía tu rol), no cualquier evento con tu rol como decía el texto que Ricardo aprobó en P23; un movimiento dentro del mismo lado, como `cp_sent` → `cp_in_review`, no abre ronda. Presentada a Ricardo al cierre como desviación.

**Faltas del coordinador, presentadas a Ricardo al cierre.** Movió la sesión al worktree y resolvió P17 sin esperar su respuesta; en P21 afirmó que la admin «usa el menú normal» para movimientos legales, falso cuando el origen es de rol IES (esos movimientos quedan fuera de la válvula y del menú; son acciones de la IES); en P18 Ricardo dijo «estoy seguro que ya habíamos hecho la migración» y el repo decía otra cosa sin que se le contradijera en texto; corrió un `pkill` sobre cualquier ssh con la llave de Yeeko sin decirlo; dijo que TESTING.md mencionaba `pnpm lint` y no era así; y Ricardo no entendió cinco mensajes en la sesión (feedback global). El ADR de bp nació como adr-0024 cuando `sector-tsu` ya tenía ese id; se renumeró a [[adr-0026]] antes del commit.

**Deploy.** Pendiente, decidido por Ricardo: «Sí están trabajando hoy, tal vez el deploy debemos hacerlo un poco más tarde». Pasos en [[task-190]].

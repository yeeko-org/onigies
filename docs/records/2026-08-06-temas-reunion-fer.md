---
type: record
id: 2026-08-06-temas-reunion-fer
date: 2026-08-06
source: ["[[2026-08-06-transcripcion-reunion-fer]]"]
---

# Temas de la reunión con Fernanda (asistente de Rubén) — 6 de agosto de 2026

Reorganización fiel de la transcripción [[2026-08-06-transcripcion-reunion-fer]], por temas y con los bloques de tiempo (`mm:ss`) en que se habló de cada uno. Participantes: **Ricardo** (desarrollador/responsable de la plataforma) y **Fernanda** (asistente de Rubén, revisora). Se omite únicamente el saludo inicial y comentarios protocolarios sin contenido de plataforma. Todo lo demás —cada bug, cada pendiente, cada duda— se conserva completo.

---

## 1. Documentación del propio Ricardo (idea suelta) `[01:29]`

Ricardo comenta que podría ir armando, poco a poco, un manual básico de dudas frecuentes, medio autogenerado porque para ese tipo de tareas usa IA. Queda como idea suya, sin desarrollarse más en la llamada.

---

## 2. Acceso de Fernanda y concepto de "IES test" `[01:54]`–`[03:43]`

- Se confirma que Fernanda puede entrar al dashboard con su correo (M. Flores / María Fernández de Pol) y que ve el listado de instituciones correctamente.
- Ricardo explica el porqué de las "universidades de prueba" (IES test): hay funcionalidades todavía no aprobadas internamente para mostrarse a todas las instituciones. Mientras no se desbloqueen para todos, solo las IES marcadas como test pueden ver y capturar esas partes, para que el equipo las pruebe.
- Ejemplo concreto: cuando Fernanda entró antes a una institución normal, solo veía la sección de buenas prácticas; el resto no aparecía porque aún no está aprobado por el proceso interno.

---

## 3. Cuentas de prueba, invitaciones y contraseñas `[03:43]`–`[10:04]`

- Fernanda había creado antes una IES de prueba con nombre "SEP" pero no recuerda la contraseña; decide en cambio usar otra que ya había creado, llamada "Fer" (alias "FP" / "Fer Prueba").
- **Pendiente detectado:** al editar los detalles de una IES en el dashboard falta el campo/checkbox para marcarla como "IES test" — Ricardo lo agrega desde el admin al vuelo durante la llamada y anota que hay que exponerlo también en la edición desde el dashboard.
- Recuperación de contraseña: Ricardo explica el flujo (botón "recuperar contraseña" en login, reenvío por correo).
- Gestión de usuarios de una institución (ejemplo con "SEP"): en la lista de invitaciones/usuarios el filtro por default muestra "pendientes"; Ricardo indica que el default debería ser "todas".
- **Truco de pruebas explicado por Ricardo:** al crear una invitación se puede usar el mismo correo con un `+algo` antes de la arroba (ej. `correo+sep@...`) para generar un usuario distinto en el sistema que de todas formas llega al mismo buzón — útil para simular varias cuentas sin usar correos reales distintos.
- **Bug/pendiente:** crear una nueva invitación tarda mucho ("un montón"); Ricardo sospecha que puede ser el envío de correo y anota que hay que revisar por qué es tan lento.
- **Pendiente de seguridad (idea, no decisión):** Ricardo piensa que sería importante añadir autenticación de doble factor porque la plataforma maneja información importante.
- Se confirma que se puede tener sesión como administradora en un navegador y como revisora en otro simultáneamente (usado para las pruebas de la llamada).

---

## 4. Correo de recuperación de contraseña — color y tipografía `[10:06]`–`[10:50]`

- Ricardo ve el correo de recuperación de contraseña y le parece que el color (rosa/rosita) es feo.
- Fernanda aclara que el color rosa fue decisión de **Rubí**, quien no quería que se asociara la marca ONIGIES con la UNAM; Ricardo reconoce que en efecto es el color de marca de ONIGIES.
- **Pendiente:** aun así, Ricardo considera que el correo "se ve feo" y que debería usar la tipografía oficial de ONIGIES; queda como tarea pendiente mejorar el diseño del correo.

---

## 5. Datos básicos / información general — bugs visuales `[11:21]`–`[12:15]`

- Con cuenta de prueba se puede ver todo el contenido (aunque no esté aprobado para el resto).
- **Bug de interfaz:** en la tabla de hombres y mujeres (datos básicos), el input es demasiado grande y no está centrado respecto al título de las columnas de arriba.

---

## 6. Duda metodológica de redacción — pendiente con Rubén `[12:17]`–`[13:07]`

- Ricardo señala que en una de las preguntas la palabra **"existen"** puede no ser la mejor redacción; entre ambos se sugiere que sería mejor algo como **"se atiende"** o **"es parte de"** / **"está presente"**.
- Ricardo marca esto explícitamente como un tema **metodológico que hay que consultar con Rubén** antes de decidir el cambio de texto; no se decide en la llamada.
- Se explica el mecanismo de revisión: Fernanda/Rubén pueden mandar comentarios por voz o por escrito sobre cualquier cosa que no se entienda o que convenga redactar distinto.

---

## 7. Bug de campo numérico sin indicación clara `[13:34]`–`[14:14]`

- Fernanda reporta que en un campo no la deja escribir texto; al intentar, solo acepta números.
- Ricardo confirma que el campo está definido como tipo numérico pero **no se indica visualmente que es un número** (no hay etiqueta ni los símbolos de incremento/decremento típicos de un `input type="number"`). Queda como pendiente aclarar la indicación visual de ese tipo de campo.

---

## 8. Objetivo general de esta ronda de revisión (UX de validación) `[14:14]`–`[15:21]`

Ricardo enmarca el propósito de la sesión: es una versión preliminar y lo que más le interesa validar es la UX de interfaz — cómo se navega, cómo se guarda, cómo intentar guardar distintos estados, y cómo la revisión debe señalar cuando algo no está completo (por ejemplo, adjuntos faltantes).

---

## 9. Adjuntos / evidencia probatoria faltante `[14:14]`–`[15:49]`

- Ricardo nota que **no aparecen los adjuntos** en la vista revisada.
- Fernanda responde que no recordaba que se pidieran archivos probatorios.
- **Ricardo confirma que sí se necesitan: fue un acuerdo con Rubí**, de la nueva actualización del instrumento.
- Fernanda plantea que esto probablemente dependa del año/versión del instrumento (a confirmar). Queda pendiente hacerlo más visible en la interfaz y agregar la función de adjuntar evidencia en preguntas base/iniciales.

---

## 10. Sistema de comentarios de revisión — permisos por turno y estatus `[17:20]`–`[24:33]`

Bloque extenso sobre el sistema de comentarios en buenas prácticas (BP):

- Fernanda reporta que en cierto botón/campo de comentario no la dejaba escribir.
- Se determina que el comportamiento depende del **estatus** del envío: en estatus **"requiere ajustes"** el envío ya está "del lado de la IES" (se le mandó de regreso), así que la revisora no debería poder comentar ahí — y en efecto no debería dejar comentar. Ricardo confirma que esto es correcto conceptualmente, aunque en el momento de la prueba sí la dejó comentar y considera raro ese caso puntual (ver §11 más abajo, sobre el caso real del COLEF).
- Se aclara que existen comentarios en tres niveles: a nivel de **buena práctica**, a nivel de **característica**, y a nivel del **envío** (paquete completo).
- Fernanda relata un episodio previo (con "el Colegio", posiblemente COLEF): no la dejaba comentar una por una, así que terminó metiendo todo en un solo comentario general muy largo en un envío específico, cuando en realidad el comentario general debía ir en el nivel de envío y no en la buena práctica particular ("agenda estadística"). Reconoce que ahí se equivocó ella, no la plataforma.
- **Bug reportado:** al comentar en una BP específica, a veces parecía guardarse pero al cerrar y reabrir el comentario desaparecía; había que refrescar (Ctrl+R). No quedó resuelto si era un problema de refresco de caché o de guardado real; Ricardo lo dejó pendiente de investigar. Fernanda terminó dejando un comentario duplicado (el grande, mal ubicado, y luego intentos sueltos); Ricardo le pide borrar el duplicado para que la IES no vea dos.
- **Confirmado (comportamiento esperado):** una vez que el envío ya se mandó y ya no está "de tu lado", no deberías poder seguir agregando comentarios ahí.
- **Pendiente de propagación de regla:** ese mismo bloqueo (no poder comentar si ya no es tu turno) debería aplicarse también a nivel de **buena práctica individual**, no solo a nivel de envío — actualmente no ocurre de forma consistente.
- **Pendiente — edición de comentarios desde el admin:** Ricardo propone agregar, desde el admin (edición directa de base de datos, "menos bonita" pero funcional), la posibilidad de editar/mover comentarios mal ubicados, para corregir casos como el de Fernanda. Lo plantea como algo que podría agregar al día siguiente.
- **Pendiente — botón de editar comentarios en la interfaz normal:** Fernanda pide que sea útil tener un botón de editar comentarios. Ricardo aclara que la regla debe ser: se puede editar un comentario **mientras el envío siga de tu lado** (tu turno); una vez que la IES ya vio/empezó a revisar el comentario general, ya no debería poder modificarse.
- Fernanda valora positivamente el nuevo menú de comentarios en general, dice que "quedó increíble" comparado con lo anterior.
- **Pendiente — inconsistencia visual entre tipos de comentario:** el comentario a nivel de envío no se ve igual (visualmente) que el comentario a nivel de buena práctica/característica; hay que unificar el estilo.
- **Pendiente — color por defecto de los puntos del timeline de comentarios:** actualmente un comentario aparece en gris (sin asociación a cambio de estatus) o en naranja (asociado al estatus "requiere ajustes"). Se discute si el naranja debería ser el color por defecto — se descarta, porque "requiere ajustes" es un estatus específico y no aplica cuando el estatus real es "completado". Se deja como pendiente definir un color por defecto para comentarios no asociados a cambio de estatus, distinto del naranja de "requiere ajustes".
- **Bug — borrado de comentarios propios:** actualmente no se puede borrar un comentario general ya guardado (probado con el COLEF). Ricardo propone que si está en tu turno y son tus últimos comentarios, debería permitirse editar/borrar.

---

## 11. Caso real: estatus "requiere ajustes" generados por reapertura manual (COLEF, Universidad de Colima, Sonora) `[25:49]`–`[28:32]`

- Al revisar el estatus real del COLEF surge una inconsistencia: el envío estaba en "requiere ajustes" pero eso no debería ser posible si el estatus previo era "completado" sin que se haya enviado formalmente a revisión.
- **Explicación reconstruida en la llamada:** Rubí (no Rubén) reabrió manualmente el sistema para que algunas IES pudieran editar información porque se les había acabado el tiempo (a solicitud de la propia IES). Ese reabrir manualmente dejó el estatus del envío como "requiere ajustes", aunque en realidad **no hubo una revisión formal** que generara ese estatus — fue un efecto colateral de la reapertura manual de Rubí, no un ajuste solicitado por la revisora.
- El mismo patrón se repite en varias IES que están en "requiere ajustes": todas corresponden a reaperturas manuales porque se les acabó el tiempo, no a revisiones reales.
- **Caso Universidad de Colima:** sí está funcionando "bien" dentro de esta lógica — llegó a estatus "ajustes atendidos" (que significa "en espera de que la institución atienda las correcciones") y de hecho ya incluye un comentario donde se explica que Rubí les abrió el sistema para continuar la captura a solicitud de la IES.
- **Acción tomada en vivo:** Ricardo decide, en ese momento, regresar/corregir el estatus de ese envío del COLEF a **"enviado a revisión"**.
- **Caso Sonora**, mencionado más adelante (§13): mismo patrón — se quedó con una sola buena práctica capturada en estatus "borrador" tras cerrarse el periodo.
- Este bloque queda como un **problema de flujo a resolver**: cómo evitar que una reapertura administrativa manual produzca un estatus de revisión ("requiere ajustes") que no refleja una revisión real.

> **Resolución (Ricardo, 2026-08-06, al documentar): no se hace nada.** Fue una excepción rara; en adelante bastará con cambiar la fecha de cierre del periodo en vez de reabrir a mano. No se construye mecanismo de reapertura ni se limpian en batch los estatus sucios de las demás IES. La corrección del COLEF a "enviado a revisión" fue un cambio de datos hecho en vivo sobre producción durante esta llamada, y queda asentado aquí y en ningún otro lado. La anotación de que estos casos **no** son evidencia de [[task-54]] quedó en esa task.

---

## 12. Lista de pendientes dictada por Ricardo a su asistente de IA (bloque 1) `[29:43]`–`[34:37]`

Ricardo dicta en voz alta (monólogo, notado por Fernanda) una lista de tareas para su sistema de generación automática de tareas a partir de la conversación:

- Limpiar en todos lados los restos del estatus previo ("estatus control"), **incluido en el admin**.
- El **filtro de estatus de envío de buenas prácticas** en el listado del dashboard **no funciona bien**.
- Poner la **etiqueta "IES test"** en el header de cada envío de buenas prácticas (actualmente el header solo muestra siglas y año); debe ser un icono identificador (ya existe uno, tipo frasco de laboratorio) y debe usarse también en los headers de instituciones que sean test.
- En vez de mostrar el número total de buenas prácticas (ej. "4 buenas prácticas"), debería mostrarse el **conteo por estatus**, cada uno con su icono.
- En los envíos de buenas prácticas debería mostrarse **si la IES respondió sí/no** a la pregunta de si tiene/quiere reportar buenas prácticas — actualmente esa respuesta no se ve ni en el header del envío ni en el contenido (detalle del package de buena práctica), lo cual Ricardo considera que no tiene sentido.

---

## 13. Confusión entre estatus de una BP individual y estatus del conjunto/paquete `[35:27]`–`[40:40]`

- Fernanda, viendo el listado (segunda página), nota varias IES cuyo envío sigue en estatus "borrador" aunque sí tengan buenas prácticas capturadas.
- Ricardo explica la causa: hay **dos niveles de estatus** — el de cada buena práctica individual (su propio ciclo de vida) y el del **paquete/conjunto de buenas prácticas** que se envía como unidad. Cuando una IES agrega solo **una** buena práctica, no queda clara la diferencia entre el estatus de esa única práctica y el estatus del conjunto — terminan pensando que ya "completado" equivale a enviado, y el paquete se queda en borrador.
- Con más de una buena práctica el doble nivel es más evidente; con una sola, es confuso. **Pendiente de resolver en interfaz.**
- Casos concretos detectados en el listado: al menos tres instituciones en esta situación — **UPN** (dejada en borrador sin llenar nada, caso distinto: simplemente no llenaron), **Universidad Tecnológica de Hermosillo** y otra de la plataforma ONIGIES (nombre no se termina de precisar en el audio) con estatus "completado" a nivel de BP individual pero paquete sin enviar.
- Surge la pregunta de si se puede cambiar el estatus una vez pasada la fecha límite — Ricardo reconoce que **no había contemplado** ese escenario dentro de la lógica de flujos, que ya es compleja.

---

## 14. Lista de pendientes dictada por Ricardo (bloque 2) — paginación, headers de instituciones y navegación por año `[43:57]`–`[49:43]`

Segundo monólogo dictado a la IA con tareas de interfaz:

- **Paginación:** debería haber un control muy pequeño cuando dice "página 1 de 2"; reordenar mostrando primero el número de resultados, luego "página X de Y", y luego los botones siguiente/anterior (solo si aplica), en tamaño chico y color azul — que sean claramente clicables pero sin ocupar más altura de la necesaria.
- **Header de instituciones:** mantener las siglas visibles, pero agregar el nombre completo abajo, en tamaño más chico y con tooltip (Ricardo cree que ya existe una herramienta de "title" genérico reutilizable para esto). También deberían aparecer los estatus o los años registrados con el estatus de cada uno — Ricardo anota que hay que pensarlo bien, sin resolverlo en la llamada.
- **Parecido visual sugerido:** que el header se parezca a la tarjeta (card) de cada año que aparece al entrar como IES — quizás no tan larga, pero con los iconos, sin los nombres, y el estatus de cada cosa.
- **Auto-carga de contenido:** al abrir una institución, los envíos de buenas prácticas y las buenas prácticas deberían aparecer automáticamente, sin que haya que buscarlos manualmente ("desde el get" deben salir).
- **Reorganización por año:** todo el contenido debería organizarse por año; dentro de cada año, pestañas para las distintas secciones (ejes, buenas prácticas, etc.), y al principio de cada año debería aparecer el bloque de preguntas generales. Ricardo no cierra del todo cómo debe verse, lo deja como algo por definir ("no sé cómo").
- **Deuda técnica de esquema (frontend):** en `dashboard.pu` (definición de "main items"), el `plural_name` no debería ser obligatorio — debería tomarse por default de la definición ya existente del modelo, igual que el icono y el color, que ya pueden definirse desde los esquemas.

---

## 15. Estatus tras el cierre del periodo de registro `[49:43]`–`[58:41]`

- Retomando algo que Fernanda había mencionado antes: cuando termina el periodo de registro, Ricardo cree que debería haber **estatus que la revisora pueda cambiar manualmente** — por ejemplo, si una IES dejó algo en "borrador", debería poder marcarse como "cerrado", "finalizado", "descartado" (nombre exacto sin definir). Aplica sobre todo a estatus que no son finales y que se quedaron "en la cancha de la IES" sin avanzar después del cierre del periodo.
- Ejemplo puesto por Fernanda: el caso de Sonora, que se quedó con una sola experiencia capturada — ¿puede considerarse valiosa aun así?
- Ricardo explica que el estatus "borrador" es simplemente el estado inicial por defecto al crear cualquier registro, no implica necesariamente que nadie trabajó en ello.
- **Decisión de enfoque (tentativa, de Ricardo):** tiene más sentido resolverlo de forma **manual** — que la revisora pueda decir explícitamente "esto ya no es borrador" — que automatizarlo. Queda pendiente revisar qué estatus conviene exactamente.
- **Pendiente de verificación:** confirmar si, una vez cerrado el periodo, la IES sigue pudiendo generar/editar borradores o no. Ricardo cree que no debería poder, pero no está seguro y propone corroborarlo en vivo creando una IES de prueba nueva (desde cero, sin buenas prácticas previas) para probar el límite.
- **Prueba en vivo con la cuenta "Fer"/"FP" (ya existente, con BP previas):**
  - Fernanda, al intentar editar buenas prácticas con esa cuenta, sí pudo editar todo — pero Ricardo aclara que eso es porque ella misma acababa de agregar esa BP (con el periodo aún abierto), no una prueba válida del cierre.
  - Al intentar completar el envío, aparece un mensaje de error poco descriptivo: **"Antes de completar, faltaban buenas prácticas por alcanzar un estatus válido, completado o descartado."** Ricardo reconoce que **debe ser más descriptivo** — debería explicar que para poder enviar, todas las buenas prácticas del paquete deben estar en un estatus "enviable" (completado o descartado), y que hay varias en borrador que hay que cambiar de estatus antes de poder enviar.
- **Bug de inconsistencia de bloqueo tras fecha límite:** actualmente, pasada la fecha límite de envío, el sistema bloquea algunas acciones (enviar, cambiar de estatus) pero **permite seguir agregando** contenido nuevo — comportamiento inconsistente. Ricardo considera que debería estar **completamente bloqueado y de forma clara**, incluyendo un aviso explícito de que ya no se puede editar nada tras el cierre.
- **Propuesta de recordatorio automático, previo al cierre:** enviar un recordatorio automático X días antes del cierre del periodo, **solo a las instituciones que ya empezaron a capturar algo** (no a todas). Ricardo aclara en `[57:39]` que esto **no estaba presupuestado** inicialmente pero le parece buena idea **proponérselo a Rubí** para reforzar el proceso. Queda como propuesta, no como compromiso de implementación.
- Fernanda está de acuerdo en que ayudaría mucho, y considera que aunque se implemente el ajuste manual del estatus, tener también el aviso/recordatorio automático es valioso.
- **Aviso automático de periodo ya cerrado, dentro de la interfaz:** en `[58:25]` Fernanda plantea que haga falta un aviso de que el periodo ya se cerró, para que la IES no lo descubra chocando con un botón que no responde. Ricardo responde en `[58:41]` «eso sí lo agrego». **Es a este aviso —el de la interfaz, posterior al cierre— a lo que se compromete, no al recordatorio previo del punto anterior.**

> **Corrección de atribución (2026-08-06, al documentar).** Una lectura anterior de este mismo bloque atribuía el «eso sí lo agrego» al recordatorio previo al cierre. Al releer la cruda `[55:45]`–`[58:41]` quedó claro que responde a lo que Fernanda dice en `[58:25]`, el aviso en la interfaz. Se corrigió aquí para que el compromiso quede bien asignado: el aviso de cierre es task de implementación ([[task-74]]); el recordatorio previo es propuesta a Rubí ([[task-89]]).

---

## 16. Cierre de la reunión — balance y forma de trabajo `[58:41]`–`[1:00:19]`

- Ricardo valora la reunión como muy productiva: permitió detectar muchos detalles que faltaban o cuyo comportamiento no está bien cerrado.
- **Próximos pasos anunciados por Ricardo:**
  - Ajustes inmediatos en el tema de "generales" (información base).
  - Lo demás es más tardado porque implica revisar muchas partes: adjuntar evidencia en preguntas base/iniciales, y los detalles de interfaz de números y claridad visual en general.
- Fernanda plantea que preferiría que **Rubén también revisara** antes de que ella mande sus comentarios, para no hacer trabajar doble a Ricardo (evitar mandarle comentarios de ella y luego, por separado, los de Rubén). Va a proponerle a Rubén que entre a ver la plataforma directamente, o en su defecto mandarle capturas de lo que ella le diga a Ricardo para que Rubén confirme o agregue observaciones — menciona como ejemplo que ella no sabía que lo de los archivos probatorios era un acuerdo ya tomado con Rubí.
- Ricardo dice que no tiene problema con recibir comentarios de ambos por separado, pero **prefiere la comunicación directa** (llamadas) porque los detalles se pueden perder si pasan por intermediarios. Propone un criterio de cuándo usar cada canal:
  - Un detalle puntual y pequeño (ej. una palabra a cambiar) puede resolverse con un mensaje.
  - Cuando se acumulan varias cosas (como en esta sesión), conviene hacer llamada, porque permite aclarar en el momento lo que no queda claro para todas las partes (Ricardo, IES, revisoras).
- Cierre cordial de la llamada.

---

## Preguntas abiertas para Ricardo

Ninguna de las decisiones tomadas en la reunión quedó ambigua en cuanto a *qué* se dijo, pero hay varios puntos que la propia reunión dejó explícitamente sin resolver y que requieren decisión posterior de Ricardo (no interpretados aquí):

1. **Redacción de "existen" (§6, `[12:17]`–`[13:07]`):** Ricardo mismo marcó este cambio de texto como pendiente de **consultar con Rubén** antes de decidir la redacción final ("se atiende", "es parte de", "está presente" u otra). No se debe implementar sin esa validación metodológica.
2. **Nombre exacto del/los nuevo(s) estatus post-cierre de periodo (§15):** Ricardo dejó abierto qué estatus (`cerrado`, `finalizado`, `descartado` u otro nombre) usar para los envíos que quedaron sin completar tras el cierre del periodo, y si el cambio será manual, automático, o ambos.
3. **Alcance exacto del "archivo probatorio" por año (§9):** Fernanda planteó que la obligatoriedad de adjuntar evidencia probablemente dependa del año/versión del instrumento; no se confirmó la regla exacta.
4. **Verificación pendiente, no una decisión pero sí una tarea de comprobación explícita que la reunión dejó sin cerrar (§15):** confirmar en la práctica si una IES puede seguir generando borradores después de cerrado el periodo (crear una IES de prueba nueva para probarlo).

### Respuestas de Ricardo (2026-08-06)

1. **«Existen»:** implementar ya **«Se atiende»** — [[task-88]] —, dejando anotado que igual hay que corroborarlo con Rubén.
2. **Estatus post-cierre:** queda pendiente, sin definir nombre ni mecánica; cuando se aborde, verlo con detalle con el skill `flow` — [[task-75]], y su acuerdo con el cliente en [[task-26]].
3. **Archivo probatorio:** la obligatoriedad debería ser **por cada `GeneralGroup` y también por cada `Observable`**; queda por corroborar en su momento si es a ese nivel que se sube la evidencia — [[task-68]].
4. **Borradores tras el cierre:** no era una zona gris. **La IES no debería poder en absoluto** — deja de ser verificación abierta y pasa a ser regla que debe hacer cumplir el candado de [[task-10]].

Menores resueltas al documentar: color por defecto del timeline de comentarios = `light-blue` ([[task-69]]); doble factor = propuesta a Rubí, no estaba presupuestado ([[task-90]]); el rosa del correo es marca correcta y no se revalida — lo que se cambia es el rosa como **fondo del header** más la tipografía ([[task-65]]); el icono de IES de prueba no lleva restricción de visibilidad ([[task-78]]); el rediseño del header y la organización por año sí es convertible en tarea, y la tarea es pensarlo en co-construcción con el skill `ux-designer` ([[task-84]]).

---

## Dónde aterrizó cada tema

Índice de trazabilidad levantado al documentar la reunión, para que ningún punto del acta se quede sin destino. Los temas sin tarea lo dicen explícitamente.

| § | Tema | Destino |
|---|---|---|
| 1 | Manual de dudas frecuentes | [[2026-08-06-ideas-sueltas-de-la-revision-con-fernanda]] — idea, no tarea |
| 2 | Acceso de Fernanda y concepto de IES test | Sin tarea: es la explicación de [[adr-0009]], ya construido en [[task-53]] |
| 3 | Casilla de IES test en la edición del dashboard | [[task-62]] |
| 3 | Filtro por defecto de invitaciones | [[task-63]] |
| 3 | Lentitud al crear una invitación | [[task-64]] |
| 3 | Doble factor de autenticación | [[task-90]] — propuesta a Rubí, no implementación |
| 3 | Truco del `correo+alias@` | [[2026-08-06-ideas-sueltas-de-la-revision-con-fernanda]] |
| 4 | Diseño del correo de recuperación | [[task-65]], anotado en [[task-38]] |
| 5 | Input de la tabla de hombres y mujeres | [[task-66]] |
| 6 | Redacción de «existen» | [[task-88]], anotado en [[task-50]] |
| 7 | Campo numérico sin indicación visual | [[task-67]] |
| 8 | Objetivo general de la ronda de revisión | Sin tarea: es el marco de la sesión |
| 9 | Evidencia probatoria en preguntas base | [[task-68]], con la duda cruzada anotada en [[task-7]] |
| 10 | Estilo dispar y color del timeline de comentarios | [[task-69]] |
| 10 | Editar y borrar comentarios propios | [[task-70]] |
| 10 | Editar y mover comentarios desde el admin | [[task-71]] |
| 10 | Bloqueo de comentarios cuando no es tu turno | [[task-44]], ampliada a hijos y nietos en los tres flujos |
| 10 | Comentario que parecía desaparecer hasta refrescar | Sin tarea propia: Ricardo no confirma el bug; se verifica dentro de [[task-69]] |
| 11 | «Requiere ajustes» por reapertura manual | Sin tarea, por decisión de Ricardo — ver la resolución en el propio §11 |
| 12 | Restos del «estatus control», incluido el admin | Ya cubierto: [[task-7]] (backend y admin) y [[task-9]] (frontend) |
| 12 | Filtro de estatus de envíos roto | [[task-77]] |
| 12 | Etiqueta de IES test en los headers | [[task-78]] |
| 12 | Conteo por estatus en vez del total | [[task-79]], hermana de [[task-49]] |
| 12 | Respuesta sí/no sobre reportar buenas prácticas | [[task-80]] |
| 13 | Estatus de la práctica vs. estatus del paquete | [[task-72]], hermana de [[task-58]] |
| 13 | ¿Se puede cambiar el estatus tras la fecha límite? | [[task-76]] |
| 14 | Control de paginación | [[task-81]], a agendar con [[task-22]] |
| 14 | Nombre completo con tooltip en el header de IES | [[task-82]] |
| 14 | Estatus del último año activo en el header | [[task-83]] |
| 14 | Organización por año, pestañas y parecido con la tarjeta | [[task-84]] — co-construcción con `ux-designer` |
| 14 | Auto-carga de envíos y prácticas al abrir una IES | [[task-85]] |
| 14 | `plural_name` obligatorio en los main items | [[task-86]] |
| 15 | Estatus manual post-cierre | [[task-75]], a acordar en [[task-26]] |
| 15 | Mensaje de error poco descriptivo al completar | [[task-73]] |
| 15 | Bloqueo inconsistente tras la fecha límite | [[task-10]], con alcance ampliado a `create`/`update`/`destroy` |
| 15 | Aviso en la interfaz de que el periodo cerró | [[task-74]] |
| 15 | Recordatorio automático previo al cierre | [[task-89]] — propuesta a Rubí, no implementación |
| 16 | Canal de comunicación y revisión previa de Rubén | Sin tarea: criterio de trabajo, queda asentado en el §16 |
| — | Edición masiva de estatus de prácticas y envíos | [[task-87]] — dictada por Ricardo al documentar, no en la llamada |

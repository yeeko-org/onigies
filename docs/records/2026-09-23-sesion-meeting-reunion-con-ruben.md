---
type: record
id: 2026-09-23-sesion-meeting-reunion-con-ruben
title: Sesión meeting de la reunión con Rubén del 23 de septiembre
date: 2026-09-23
source: ["[[2026-09-23-reunion-ruben]]"]
related: ["[[2026-09-23-reunion-ruben_raw]]", "[[task-171]]", "[[task-172]]", "[[task-173]]", "[[task-174]]", "[[task-175]]"]
---

# Sesión meeting de la reunión con Rubén del 23 de septiembre

Sesión `meeting` del 23 de septiembre de 2026 sobre la reunión de trabajo Ricardo–Rubén del mismo día (86 min 18 s, grabada a las 14:49). Un primer ejecutor corrió el pipeline, escribió la cruda y la limpia y devolvió 33 ideas con su destino propuesto; Ricardo respondió el triage; un segundo ejecutor, que escribe este record, aterrizó las ideas en los nodos. **Ricardo se fue antes del cierre**: lo que necesitaba su llamado quedó en tasks con owner `ricardo`, no como pregunta abierta en el chat. Los ids de contenido de la reunión son los timestamps de la limpia.

## Pipeline y records

- Cruda: [[2026-09-23-reunion-ruben_raw]], con el audio en `s3://meetings-audio-032892915740-us-west-2/meetings/unam/onigies/2026-09-23-reunion-ruben.m4a`. Limpia: [[2026-09-23-reunion-ruben]]. Ninguna de las dos se tocó en este pase: ninguna respuesta de Ricardo cambia la lectura de la limpia, y la cruda nunca se edita.
- Hablantes: A = Rubén; B y C = Ricardo (el pipeline partió su voz en dos letras).
- Los defectos del pipeline observados en esta reunión quedaron como feedback en el grafo de written.django (fb-27 a fb-32), sin commitear al cierre de este pase; los commitea el coordinador allá.

## Respuestas de Ricardo y llamados del coordinador

Ricardo respondió por escrito a las preguntas P1–P5 del triage que le hizo el coordinador. Sus respuestas, literales:

- **P1, tarjetas con sombra frente al borde suave de la sesión paralela:** «Lo que dije en la reunión es lo más actual, al final de las aclaraciones le mandas un mensaje de regreso al mismo agente con lo que sea relevante de lo que esté haciendo». Sobre el bug: «Lo del bug, creo que no era un bug y al final sí lo logré, estoy casi seguro que lo logré, manda a un SAG a verificar con playwright».
- **P2, los 80 mil con o sin IVA:** «No lo sabemos, quedó pendiente». Queda en [[task-154]]; la reference [[estado-administrativo-y-de-pagos]] no se reescribe.
- **P3, qué mandó Rubén a las IES:** «No importa, el exportador de word ya está cerrado, no se harán más cambios». [[task-150]] se cerró; la línea de Rubén sobre sus correcciones quedó en [[task-157]], que sigue abierta.
- **P4, fechas por sección:** «Eso no nos corresponde, no guardar nada, con los campos existentes tenemos, si acaso uno para "cierre de cp"». Línea en [[task-153]].
- **P5, el documento de tres horas:** «Lo enviaré hasta mañana, ya le avisé. Esa sesión no la reactivaré, llegó hasta donde debía llegar». El documento de la brecha se lo manda Ricardo a Rubén el 24 de septiembre: línea en [[task-164]].
- **Las ideas metodológicas:** «propongo agregar una nueva tarea para pensarlo bien a fondo y analizar juntos propuestas, anótalas por lo pronto». Es [[task-173]]. Que el dictamen de la revisora no se implemente hoy y quede hacia el 7 de octubre de 2026 lo registra [[task-173]] (a).
- **Lo que quedara por decidir:** «si hay otras decisiones que debo tomar, guárdalas en alguna tarea y después retomamos la conversación».

Consecuencia de P1: donde la reunión contradice lo que decidió la sesión paralela de la captura cp, manda la reunión; por eso [[task-172]] incluye las tarjetas de grupo con sombra. Consecuencia de la frase sobre el bug: un agente lo verificó con Playwright, se confirmó, y vive en [[task-174]].

Llamados del coordinador, no de Ricardo:

- La hipótesis D4 (abajo) sobre el documento que Rubén revisó en tres horas.
- El cierre de [[task-21]], porque Rubén vio el despliegue y lo aprobó (`[22:31]`).
- No escribir ADRs: se infirió de «anótalas por lo pronto»; los candidatos quedan dentro de [[task-173]] (h).
- Las tasks obvias [[task-171]] (textos que escribe o revisa Rubén) y [[task-172]] (retoques de la captura cp).
- Las discrepancias de pagos, a [[task-154]] como datos por cuadrar.
- Las decisiones pendientes que dejó el análisis de la brecha, a [[task-164]] como P1–P3, textuales.

Las decisiones pendientes de Ricardo que salieron de esta sesión quedaron en [[task-175]].

## Dudas del triage y cómo quedaron

- **D1, los 80 con o sin IVA** (`[01:36]`–`[02:03]`): sin resolver, en [[task-154]] con las frases y la aritmética.
- **D2**: Ricardo respondió «no importa» y declaró cerrado el exportador; [[task-150]] se cerró con las líneas de la reunión en su cuerpo.
- **D3, las fechas por eje** (`[35:17]`–`[37:59]`): respondida por Ricardo en P4 (arriba), en [[task-153]]; el posible campo de «cierre de cp» es la entrada (b) de [[task-175]].
- **D4, qué documento revisó Rubén en tres horas.** Rubén, `[34:31]`: «Me ayudó mucho el que me mandaste; la verdad, me fui uno por uno y acabé como en tres horas». Ricardo, `[34:35]`: «¿Y sí estaba más o menos claro, no estaba muy repetitivo?». Rubén, `[34:42]`: «Me tardé más en prepararme mentalmente para hacerlo […] lo hice en un solo salto». **Hipótesis (a), no confirmada**: es el documento de correcciones de redacción del 4 de septiembre, [[2026-09-04-correcciones-de-redaccion-del-instrumento]]. A qué task va, entrada (d) de [[task-175]].
- **El 1.6 A5**: Ricardo dijo en vivo que «sí podría tener el no aplica» (`[1:00:33]`); el record [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]] la clasificó como candidata débil que se resuelve como «No». No se resolvió: es P4 en [[task-164]].

## El bug visto en vivo

Rubén, `[17:28]`: «Cuando marcan sí o no, ¿se guarda o hay que darle guardar?». Ricardo, `[17:32]`–`[17:39]`: «Lo que no se guarda es esto: le tienes que poner aquí "guardar", y entonces le pones "en llenado". Mira este roche, este es un bug que está bueno: en guardar decía guardar "en llenado" y lo intentó guardar como si fuera de "completado"; hasta que no pongas todo esto como completado no te deja guardarlo como completado. Ahora ya me dejó». Ricardo pidió verificarlo con Playwright; la verificación lo confirmó, con otra mecánica de la que él describió, y vive en [[task-174]].

## Terminología

Ricardo, `[40:28]`–`[40:32]`: «No sé si está bien que uno diga transversalidad o transversalización; no sé cuál es la palabra correcta». Rubén, `[40:33]`: «Yo digo transversalidad, porque es más rápido y me trabo menos». Es «transversalidad», no «transversalización»; [[adr-0014]] §3 ya lo recoge en la nomenclatura.

## Cada idea y su destino

| Idea | Timestamps | Destino |
|---|---|---|
| I1 montos dichos | `[00:56]`, `[01:36]`–`[02:07]`, `[05:15]`–`[05:38]` | [[task-154]] |
| I2 conceptos que cubren los 80; renglón repetido | `[02:12]`–`[04:32]`, `[06:32]`–`[07:26]` | [[task-154]] |
| I3 ruta del pago | `[07:34]`–`[07:59]`, `[1:25:24]` | [[task-155]] |
| I4 el dashboard llevó más tiempo; medir trabajo | `[05:57]`–`[05:59]` | [[task-154]] |
| I5 el documento del presupuesto ya salió | `[1:25:25]`–`[1:26:11]` | [[task-154]] |
| I6 exportación «casi idéntico»; Word → PDF | `[11:00]`–`[11:52]`, `[1:24:28]` | [[task-150]], cerrada; `[11:34]` también en [[task-157]] |
| I7 fecha de apertura por periodo | `[12:40]` | [[task-153]] |
| I8 descripciones de los ejes | `[13:22]`–`[14:02]`, `[38:32]` | [[task-171]] |
| I9 retoques de la captura | `[15:01]`–`[16:42]`, `[22:01]`, `[25:46]`, `[27:54]` | [[task-172]] |
| I10 bug al guardar «en llenado» | `[16:42]`–`[17:39]` | [[task-174]], verificado con Playwright |
| I11 descripciones de los tipos de pregunta | `[18:33]`, `[38:32]` | [[task-171]] |
| I12 Rubén aprueba el despliegue progresivo | `[18:59]`–`[19:10]`, `[22:31]`, `[23:04]`–`[24:54]`, `[26:43]`, `[49:42]` | [[task-21]], cerrada |
| I13 rosa y morado | `[19:23]`–`[20:09]` | [[task-38]] |
| I14 enviar a revisión deshabilitado; tamaño de Cuidados | `[20:13]`–`[21:53]` | [[task-98]]; el tamaño, [[task-172]] |
| I15 sin base validada se consulta y no se responde | `[23:54]`–`[24:52]` | [[task-153]] |
| I16 notas de aclaración | `[25:15]`–`[26:43]` | [[task-150]] |
| I17 el 1.14 sin «no aplica» | `[28:06]`–`[33:28]` | [[task-165]] punto 1, criterio marcado |
| I18 análisis de «no aplica»; el 1.6 A5 | `[30:51]`, `[32:00]`, `[33:28]`, `[59:35]`–`[1:02:53]` | [[task-164]], P4 |
| I19 Rubén revisó «el que me mandaste» | `[34:31]`–`[34:42]` | este record, hipótesis D4 |
| I20 liberar hoy; la reunión del viernes | `[12:04]`, `[34:54]`–`[35:17]`, `[1:20:00]`–`[1:20:17]`, `[1:23:58]`, `[1:25:04]` | [[task-163]] y [[task-153]] |
| I21 sin fechas por eje | `[35:17]`–`[37:59]` | [[task-153]] |
| I22 la fecha límite funcionó, 60 % | `[37:59]`–`[38:30]` | [[task-165]] punto 5 |
| I23 default del trío; «todo lo que esté activo tiene que sumar 10» | `[38:32]`–`[43:31]`, `[44:09]`–`[44:32]` | [[task-15]] |
| I24 «transversalidad» | `[40:28]`–`[40:33]` | este record |
| I25 el 1.12 y la transversalidad curricular | `[44:47]`–`[48:56]` | [[task-173]] (b) y [[task-165]] punto 3 |
| I26 ponderación de la población | `[49:01]`–`[51:55]` | [[task-111]] y [[task-173]] (d) |
| I27 ¿pesa el sí/no inicial? | `[52:08]`–`[53:38]` | [[task-28]], [[task-173]] (e) y [[task-164]] |
| I28 «parcialmente» solo por la revisora, .5 | `[54:16]`–`[55:13]`, `[1:01:19]`–`[1:06:07]` | [[task-173]] (a) |
| I29 «no cumple» sin que la IES cambie | `[55:41]`–`[57:48]` | [[task-173]] (a) |
| I30 casos excepcionales | `[58:12]`–`[59:35]` | [[task-15]] y [[task-173]] (f) |
| I31 reparto interno y sectorial | `[1:06:23]`–`[1:19:55]` | [[task-28]] y [[task-173]] (c) |
| I32 exportar buenas prácticas para el comité | `[00:04]`–`[00:18]`, `[1:20:31]`–`[1:23:54]` | [[task-173]] (g), destino abierto entre [[task-32]] y una task nueva |
| I33 «recibida para dictamen» sin uso | `[1:21:32]`–`[1:23:35]` | [[task-87]] |

**Candidatos a ADR**, ninguno escrito: C1 (el «parcialmente» de la revisora) y C2 (planes de estudio como transversalidad curricular) en [[task-173]] (h); C3 (sin fechas por eje) quedó como línea de [[task-153]]; C4 («todo lo que esté activo tiene que sumar 10») como criterio de Rubén en [[task-15]].

## Nodos

- Creados: [[task-171]], [[task-172]], [[task-173]], [[task-174]] (bug verificado con Playwright), [[task-175]] (decisiones pendientes de Ricardo) y este record.
- Cerrados: [[task-21]] y [[task-150]]. Para cerrar [[task-150]] sin arrastrar a sus hijas abiertas, [[task-158]], [[task-161]] y [[task-162]] pasaron a colgar de [[task-2]], con enlace de vuelta a [[task-150]].
- Editados, cada uno con una sección «Reunión con Rubén, 2026-09-23»: [[task-15]], [[task-28]], [[task-38]], [[task-87]], [[task-98]], [[task-111]], [[task-153]], [[task-154]], [[task-155]], [[task-157]], [[task-163]], [[task-164]] (más «Decisiones pendientes de Ricardo», P1–P4) y [[task-165]] (criterio del 1.14 marcado).
- Sin tocar: la cruda, la limpia, [[estado-administrativo-y-de-pagos]], [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]] y [[task-169]].

## Cobertura

La limpia tiene 384 timestamps únicos en su cuerpo; todos están citados, directamente o dentro de un rango, en una task o en este record. Los que no generan trabajo son charla y quedan aquí:

| Timestamps | Qué era |
|---|---|
| `[00:43]` | Ricardo, «Sí», a la cotización del año pasado |
| `[02:07]` | Ricardo, «De acuerdo. Entonces pusiste…» |
| `[11:59]`–`[12:09]`, `[12:10]`, `[12:23]` | Rubén propone ver primero el cuestionario; Ricardo, «Va, va. Sí, a ver, pues ya va muy bien. Lo primero es que… un momento» |
| `[49:37]` | Rubén, «Bueno…» |
| `[1:22:09]` | Ricardo, «¿No?» |
| `[1:23:55]` | Ricardo, «Sí, va, bueno, sale pues» |
| `[1:25:01]`, `[1:25:11]`, `[1:25:12]` | Despedida: «OK», «Muchas gracias», «Larga reunión, pero productiva; ya necesitábamos discutir cosas metodológicas» |

Fuera del cuerpo de la limpia, y por eso fuera de la cuenta: `[10:17]`–`[10:49]` (la suscripción a la IA para un cuadro en Excel) y `[1:25:19]`–`[1:25:21]` (el «vamos a comer»), que la limpia retiró por ajenos al proyecto. Entre `[07:59]` y `[10:17]` la cruda no tiene párrafos.

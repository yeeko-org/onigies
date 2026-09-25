---
type: task
id: task-164
title: Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A
state: open
date: 2026-09-22
owner: ricardo
parent: "[[task-2]]"
source: ["[[2026-09-22-cierre-cuestionario-principal-captura-y-borrado]]"]
related: ["[[task-157]]", "[[task-50]]", "[[2026-09-23-reunion-ruben]]", "[[task-175]]", "[[2026-09-24-documento-para-ruben-brecha-entre-pregunta]]", "[[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]"]
---

# Análisis de la brecha entre la pregunta inicial de cada observable y sus preguntas A

Ricardo lo pidió el 22 de septiembre para una sesión Fable aparte, antes de compartir las preguntas con las IES: «no con la idea de cambiar todo, sino de observar qué puede mejorar y en qué sentido». El disparador fue la observación de que la pregunta inicial («¿La IES cuenta con…?») mide tenencia de una medida, mientras que las opciones A miden grados de armonización e institucionalización que a veces no se corresponden con lo que la inicial prometió (el análisis de «no aplica» del mismo día, sobre el texto real de la base, lo hizo visible en 1.10, 1.14, 1.15, 3.2 y 4.7, donde una IES puede responder «Sí» y marcar solo las opciones que dependen de ella).

**Urgencia que dio Ricardo:** antes de que se compartan las preguntas, hoy mismo (22-23 de septiembre).

Material: los 41 observables con `init_question`, `a_main_question`, `a_main_subtitle` y sus `AQuestion` (280), en la base local restaurada de producción; la skill `cp-questionnaire`. Entregable: un record con la tabla por observable (qué promete la inicial, qué miden las A, dónde se abren) y una lista corta de mejoras propuestas en el sentido que Rubén pueda aceptar, sin rehacer el instrumento. Sin alucinar casos: sobre el texto real.

**Ampliación del 23 de septiembre (Ricardo):** el mismo ejercicio de «no aplica» que se hizo con las preguntas iniciales se repite sobre las AQuestion: revisar si existen opciones donde una IES pueda necesitar «No aplica». Mientras tanto la captura cp asume que no hay «No aplica» en las A (radios Sí/No en `YesNoRadio`); si el análisis lo introduce, el control pasa de radio a select en ese momento.

**Entregado el 2026-09-23** en [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]]: tabla de los 41, siete bloques de mejoras por impacto y constancia de que ninguna A requiere «No aplica» (`YesNoRadio` se queda). Cierre pendiente de la lectura de Ricardo y de qué se lleva a Rubén.

## Criterios de aceptación

- [x] Record con la tabla de los 41 observables y las brechas encontradas
- [x] Lista de mejoras propuestas, ordenadas por impacto, lista para llevar a Rubén
- [x] Lista de AQuestion candidatas a «No aplica», o constancia de que no hay
- [ ] ⚠️ Ricardo le mandó a Rubén la lista de candidatas a «no aplica» en preguntas iniciales (`[32:00]`) — va dentro del documento, apartado 5
- [ ] ⚠️ Ricardo le mandó a Rubén el análisis de «no aplica» de las 280 A y el documento de la brecha (el 24 de septiembre, `[59:35]`) — el documento está listo desde la madrugada del 25: Word y PDF en `~/respaldos/onigies-ruben/ONIGIES-2026-brecha-y-no-aplica.docx` y `.pdf` (copiados ahí desde `/tmp`, que es tmpfs y se borra al reiniciar; se regeneran del record con `~/respaldos/onigies-ruben/build.py <md> <docx>` y `soffice --headless --convert-to pdf`); lo envía Ricardo la mañana del 25 junto con el aviso del deploy

## Reunión con Rubén, 2026-09-23

Fuente: [[2026-09-23-reunion-ruben]].

**Lo que Ricardo le contó y prometió mandar.** `[30:51]`–`[31:18]`: pidió a la IA «un análisis de si podría haber alguna pregunta de este tipo, de las de armonización, institucionalización, en la que pueda aplicar el no aplica». `[32:00]`: «te mando la lista de las posibles. […] esta fue la única, la 1.14». `[33:28]`: otro análisis «que ahorita está corriendo», porque «a veces puede ser que […] respondas directamente a esta que no, pero alguna de estas sí aplique […] te lo paso tal cual […] Va a ser otro documento muy breve de observaciones». `[59:35]`–`[1:00:03]`: «te mando esto, que ya está hecho […] dice que en ninguna de las […] 280 preguntas tendría sentido poner el no aplica». `[1:02:34]`–`[1:02:48]`: «Si hay casos específicos donde un no aplica aplica para preguntas de institucionalización, pues igual sí se pueden poner, pero van a ser tres o cuatro máximo, tal vez una o dos». Rubén, `[1:01:14]`–`[1:01:19]`: «¿Eso me lo podrías mandar para checarlo? Y ya con eso, junto con el análisis que vemos ahorita…»; `[1:02:53]`–`[1:02:55]`: «Si quieres, mándamelo, lo checo».

**El 1.6 A5, en vivo, contra el record.** Ricardo, `[1:00:07]`: «Solo… cargos de elección, en la 1.6. Mira, de una vez lo checamos: 1.6, es la 5. Si no tiene cuerpos colegiados…»; Rubén, `[1:00:31]`: «Difícil»; Ricardo, `[1:00:33]`: «O cargos de elección: si es una pregunta que hacemos… cuerpo colegiado máximo sí tienen. Entonces, ¿qué pasa? Esta pregunta sí podría tener el no aplica». Rubén, `[1:01:00]`: «si quieres tú puedes hacer esa consulta»; Ricardo, `[1:01:05]`–`[1:01:10]`: «Ya la hice; por eso te puedo decir este ejemplo: me lo dio en el reporte ahorita la IA». El record [[2026-09-23-brecha-entre-pregunta-inicial-y-preguntas-a]] clasifica el 1.6 A5 como candidata débil que se resuelve como «No», porque la misma A cubre los cuerpos colegiados de máximo nivel, que sí existen. Llamado de Ricardo: P4 abajo.

**Envío:** Ricardo le manda el documento de la brecha a Rubén mañana, 24 de septiembre de 2026 (triage).

**La brecha, dicha por Rubén** ([[task-173]] punto e): Ricardo, `[53:22]`–`[53:36]`, «¿qué pasa si alguien pone que sí y en todas estas pone que no?»; Rubén, `[53:38]`, «sí puede pasar. Es que la realidad siempre va a superar al cuestionario».

## Decisiones pendientes de Ricardo

Del análisis de la brecha, textuales:

- **P1.** Qué bloques de mejora llevar a Rubén: recomendación del agente 1 a 5 como propuesta, 6 (erratas) se corrige sin él, 7 se menciona como agenda de la versión siguiente.
- **P2.** Bloque 3, la que sí bloquea compartir las preguntas: las tres A que piden texto (1.16 A1 y A2, 2.5 A9): editar el texto o abrir un campo de texto en AResponse.
- **P3.** Las diez erratas del bloque 6: corregirlas en el admin local para el próximo deploy o dejárselas a Rubén, que edita ahí.

De la reunión del 23 de septiembre:

- **P4.** El 1.6 A5: ¿«No aplica», como lo leyó Ricardo en vivo (`[1:00:33]`), o candidata débil que se resuelve como «No», como la clasificó el record? Si se habilita, el control de esa A deja de ser `YesNoRadio` (ampliación del 23, arriba).

La task sigue abierta; su cierre espera el envío.

## Documento para Rubén, 2026-09-24 y 25

El documento es el record [[2026-09-24-documento-para-ruben-brecha-entre-pregunta]] (cinco apartados: qué se le pide; la brecha con los bloques 1 a 5 como propuesta, las erratas como lista informativa y el bloque 7 como agenda; las tres A que piden texto con su redacción Sí/No; el «no aplica» en las 280 A; las candidatas entre las preguntas iniciales con 1.6 A5 en sus dos lecturas). Le habla de tú, cita a Rubén, y cada tabla de propuestas lleva columna «Decisión» como el documento del 4 de septiembre. Cifras recalculadas sobre la copia local de producción del 22: 41 observables y 280 A; 0 A que necesiten «no aplica» (18 examinadas de cerca, dos más que el record de la brecha: 1.4 A6 y 4.9 A4); 1 inicial candidata, la 1.14 (copiada de [[adr-0017]] y [[task-165]], no recalculada: el clasificador de permisos negó al ejecutor leer las bitácoras donde estaba el análisis original; releyó las 41 sin hallar otra, pasada ligera); 18 erratas (las 10 del record más 8 nuevas, entre ellas un «sexo/género» que el propio Rubén estandarizó). Dos discrepancias con el record de la brecha, corregidas en el documento: «pertenecientes las poblaciones» está en 1.16 A4, no A5; el bloque 4 son tres títulos, dos preguntas principales y un subtítulo. Ricardo aceptó los agregados del ejecutor (unidad de análisis de las IES no autónomas con el 1.12; redacción «y, en su caso, en los cargos de elección» para 1.6 A5; redacción Sí/No para 2.5 A9 además de borrarla; las 8 erratas) y el encabezado 2.2 pasó de «cinco» a «seis» (su tabla trae seis filas).

Cómo quedaron las decisiones pendientes. ⚠️ **P1, P2 y P4 no las respondió Ricardo**: entraron al documento con la recomendación del coordinador cuando él preguntó «el contenido ya quedó, no?», y las notas «[Ricardo: …]» que las señalaban se quitaron; confirmarlas antes de enviar. **P1** aplicada con la recomendación (bloques 1–5 como propuesta, 6 informativo, 7 agenda). **P2** aplicada con la recomendación: editar el texto de las tres A a Sí/No ([[task-175]] e); la alternativa del campo de texto en `AResponse` no va en el documento por decisión del brief al ejecutor, no de Ricardo, así que Rubén no la ve como opción. **P3** cambió de forma: la opción «corregir en el admin local para el próximo deploy» no existe, porque desde [[adr-0015]] el seed está retirado y lo editado en local nunca llega a producción; Ricardo lo confirmó («las erratas sólo se corrigen desde el dashboard»); el documento dice «se corrigen en la plataforma» sin decir quién, y quién las corrige (Ricardo tras el deploy o Rubén) sigue abierto. **P4** aplicada con la recomendación: se mandan ambas lecturas del 1.6 A5 y Rubén decide.

Correcciones que el coordinador hizo al documento tras la crítica de cierre (madrugada del 25), en el record y en el Word: (a) en el apartado 1, «texto cargado al 22 de septiembre» en vez de «hoy cargado en la plataforma», porque todo se calculó sobre la copia local del 22 y Rubén edita en el dashboard; (b) «casi todas son de redacción; dos proponen quitar una pregunta A (4.14 A3 en 2.4 y 2.5 A9 en la opción 2 del apartado 3)» en vez de «ninguna propuesta agrega ni quita»; (c) en 5.1, «ya se declara en la Información de base» sin «y de ahí se toma», porque la herencia gen → cp de denominadores no está construida ([[task-165]] punto 4). La línea de fecha del record dice 24 de septiembre y la del Word 25. ⚠️ Releer esas tres frases antes de enviar; si se quiere, el modelo hace un diff de solo lectura de las columnas «Redacción actual» contra producción antes del envío.

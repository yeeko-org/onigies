---
type: record
id: 2026-09-04-reunion-con-ruben_raw
title: Reunión con Rubén, 4 de septiembre — transcripción cruda
date: 2026-09-04
audio: s3://meetings-audio-032892915740-us-west-2/meetings/unam/onigies/2026-09-04-reunion-con-ruben.m4a
speakers:
  A: Ricardo
  B: Rubén
  C: sin identificar
parent: "[[2026-09-04-reunion-con-ruben]]"
---

# Transcripción cruda: reunión con Rubén, 4 de septiembre

Salida cruda del pipeline de `written.django` (`manage.py transcribe`, formato `md`) sobre el audio de la reunión de trabajo del 4 de septiembre de 2026 (57 min 22 s, grabada a las 14:57 hora de la Ciudad de México) entre Ricardo (desarrollador de la plataforma ONIGIES) y Rubén (CIGU, responsable del ONIGIES). El audio vive en el bucket privado, en la URI del frontmatter. La versión limpia es [[2026-09-04-reunion-con-ruben]].

El pipeline separó tres hablantes: «Participante A» (124 bloques, nombre candidato Ricardo), «Participante B» (128 bloques, nombre candidato Rubén) y «Participante C» (18 bloques, sin nombre candidato). C es en su mayoría ruido de alineación —palabras sueltas de una o dos sílabas que el alineador no pudo asignar («Porque…», «el», «y», «una»)—, salvo el tramo `[44:25]`–`[45:00]`, donde sí interviene una tercera persona real de la CIGU que entra a avisar que vigilancia va a cambiar de turno y pregunta por la credencial de Ricardo. El mapa `speakers` del frontmatter recoge los candidatos del pipeline; queda pendiente la confirmación de Ricardo.

Avisos del pipeline, no verificados palabra por palabra contra el audio: un único `compression_warnings.json` (idx 11, ratio 0.698, el párrafo `[01:37]` sobre el registro como proveedor), dos párrafos sin hablante asignado (segundos 1508.54 y 1584.36) y varios grupos sin emparejar con hablantes mezclados A/B. La atribución tiene además cruces visibles a simple vista: hay frases partidas a la mitad entre A y B —por ejemplo `[03:36]`, donde «¿Son 80 mil pesos en total?» es de Ricardo y el resto del bloque de Rubén, y el tramo `[21:15]`–`[21:30]`—. Reasignarlas es trabajo de la limpia; aquí se conserva la salida tal cual.

Lo que sigue es la salida del pipeline sin modificar, incluidas sus notas de corrección.

---

## Notas generales

*Se recomienda al revisor humano verificar los términos técnicos propios de la plataforma ONIGIES, así como los nombres de personas mencionados de pasada (como Dana, Claudio, Norma, Fer, Isabela y Pati) para asegurar la máxima precisión.*

## Participantes

**A (Desarrollador del sistema)**

*Nombre probable: Ricardo*

*Notas: Parece ser el desarrollador o responsable técnico del sistema u observatorio.*

**B (Coordinador / Líder institucional)**

*Nombre probable: Rubén*

*Notas: Líder del proyecto u observatorio, discute presupuestos y lineamientos metodológicos.*

**C**

*No se encontraron nombres probables*

*Notas: Intervenciones cortas o de terceros (como personal de vigilancia o avisos administrativos).*

# Transcripción final

**Participante A (Desarrollador del sistema — Ricardo)**

`[00:18]` ¿Pues cómo va todo?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[00:18]` A ver. Si quieres empezamos por lo administrativo. ¿Te busco agua?

**Participante A (Desarrollador del sistema — Ricardo)**

`[00:24]` Sí, ya mandé mis documentos. No me han respondido todavía. O sea, se supone que entre dos y no sé cuántos días hábiles. El primero de septiembre me dijeron que: «Informamos que su registro quedará concluido una vez que se haya verificado su información», pero se supone, o sea, no sé cuántos días hábiles ha estado, pero ahorita te digo lo que me dijo Dana.

`[01:05]` Me dijo que iba a estar entre mañana y el jueves, pero eso me lo dijo el martes.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[01:11]` ¿Cómo te dijo que te registraras? ¿Como proveedor? ¿Fue todo lo que te dijo?

**Participante A (Desarrollador del sistema — Ricardo)**

`[01:17]` Ahora no... déjame ver si ya llegó algo, dame un segundo.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[01:21]` OK.

**Participante A (Desarrollador del sistema — Ricardo)**

`[01:37]` No me ha llegado nada. O sea, ya pasamos el tiempo que ellos mismos ponen y no me ha llegado nada. No sé, ¿quieres que le pregunte así de pronto?

**Participante C**

`[02:02]` Porque...

**Participante A (Desarrollador del sistema — Ricardo)**

`[02:02]` Me dijo que... No, o sea, tenía, justo yo tenía que estar al pendiente de que me avisaran y no, todavía no está, entonces dependemos de eso.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[02:22]` Mira, lo que me dijeron es que del presupuesto que nos queda van a asignar todo lo que nos quedaba para la partida en la que te vas a registrar, que es como proveedor. Eso no sería honorarios, sería factura y te pagarían en dos partes. Uno ya ahora empezaría a tramitar el proceso y otro en octubre, serían...

**Participante A (Desarrollador del sistema — Ricardo)**

`[02:56]` Yo tengo que hacer cuentas bien de cómo va el pedo porque, o sea, independientemente de que no se pague, pues como decirte claramente: «Mira, he trabajado esto y estoy implicado» de lo que ya...

**Participante C**

`[03:13]` Sobre todo

**Participante A (Desarrollador del sistema — Ricardo)**

`[03:14]` con el módulo de buenas prácticas, como que habíamos pensado en hacerlo muy chiquito y como que le fuimos aumentando más cositas y variaciones, o sea, lo demás ha estado bien, o sea, creo que ha estado dentro de todo.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[03:36]` ¿Son 80 mil pesos en total? No, no, no, te debo todavía más, pero lo que te van a pagar en

**Participante A (Desarrollador del sistema — Ricardo)**

`[03:46]` estos dos pagos, vale, en esos dos.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[03:48]` Sí, te van a dar primero 32 y luego 48.

**Participante A (Desarrollador del sistema — Ricardo)**

`[03:51]` ¿Pero no era un presupuesto más grande?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[03:54]` No, no, no, o sea, te van a dar esto en abono y todavía me faltan como más de 100 mil de lo que tú cotizaste, pero ahorita lo que tenemos disponible en la vaquita de la CIGU es eso y te van a dar todo; esa es la estrategia que encontramos.

**Participante A (Desarrollador del sistema — Ricardo)**

`[04:15]` Ya te entendí, me agarren

**Participante B (Coordinador / Líder institucional — Rubén)**

`[04:16]` todo lo que nos queda, que no estaba asignado al observatorio, pero me lo pasaron, ¿si me explico? Entonces te van a pagar esto y esos 80 obviamente no... hace falta mucho, creo que apenas vamos ahí como a un tercio. Hay que checar la, o sea, estos 80 mil pesos no llegan ni a un tercio de lo que es la cotización, nada más es un abono.

**Participante A (Desarrollador del sistema — Ricardo)**

`[04:39]` De todas maneras todavía falta una parte potente de las BO y falta la página pública.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[04:45]` Claro, o sea, lo que te vamos a ir dando como ya abonos, porque no nos liberaron el recurso completo como lo pedí. Es lo que te digo, siempre pasa, para todo pasa, nunca nos dan dinero para nada. Nunca me dan, o sea, no aquí en la CIGU, sino presupuesto de la UNAM. De hecho yo volví a pedir, ¿te acuerdas que te dije que volví a pedir para el año que viene, como si no me hubieran dado nada, el presupuesto completo y también uno para mantenimiento? Entonces, eso se te pagaría de agosto a octubre y en cuanto llegue

**Participante C**

`[05:21]` el

**Participante B (Coordinador / Líder institucional — Rubén)**

`[05:21]` siguiente presupuesto en enero, ahí vamos a tratar de dártelo todo, todo lo que faltaba.

**Participante A (Desarrollador del sistema — Ricardo)**

`[05:28]` va, va.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[05:34]` Y la verdad es que los resultados van a ser lucidores. Ya no hay duda de que hay que pagar eso. Incluso yo le dije a Norma que nosotras hicimos un diplomado, es otro proyecto, pero cobramos y de ahí ingresaron como 200 mil pesos. La UNAM te quita mucho, pero yo le dije que ese dinero si se podía disponer para el observatorio y me dijo que sí, pero como todo ese dinero lo tiene la Secretaría Administrativa de la UNAM, no lo tiene aquí directamente la CIGU. Sí, sí, entiendo, siempre es, hola Adri, siempre es un rollo. Pero bueno, decirte que estos ya están asegurados. Y si quieres un día en octubre, cuando te paguen el segundo pago, nos sentamos un día nada más para ver qué has hecho, qué se te ha pagado y cuánto falta.

**Participante A (Desarrollador del sistema — Ricardo)**

`[06:25]` Sí, va, me parece bien, sí.

**Participante B (Coordinador / Líder institucional — Rubén)**

> *Nota: Se mantiene 'ONIGIES' por el contexto de la reunión y la sigla mencionada.*

`[06:28]` OK, entonces ahora pasamos a ONIGIES.

**Participante A (Desarrollador del sistema — Ricardo)**

`[06:34]` Ah, OK, invítame a esos

**Participante B (Coordinador / Líder institucional — Rubén)**

`[06:37]` webinars. Sí, tuvimos reunión y les expliqué, tenían muchas dudas, no técnicas sino metodológicas de algunos ítems. Pero mira, les hice una simulación de cómo llenar la información y estaban muy felices, pues ya voy a hacer las siguientes sesiones.

**Participante A (Desarrollador del sistema — Ricardo)**

`[07:02]` Te voy a mandar un documento, me das un segundo. Te lo comparto por correo, por WhatsApp, o sea, un documento con dudas que ya había medio preparado pero no tenía bien listo y ahorita le pedí a Claudio que me ayudara para trabajar con eso.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[07:28]` Si quieres WhatsApp.

**Participante A (Desarrollador del sistema — Ricardo)**

`[07:29]` Sí, va. No sé por qué está en zip, así se descargó.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[07:50]` No lo leí. Ah, ya lo voy a descomprimir.

**Participante A (Desarrollador del sistema — Ricardo)**

`[07:57]` Descomprimir, ¿cómo? A ver, no se deja descomprimir. ¿Le puedes poner F, o sea, F? No funcionan esos, ¿es comando? Sí, era quitarle el punto. O sea, no tenemos que hacerlo ahorita, pues, pero te explico como los cambios y eso. Ahí, o sea, como en la revisión fuimos —y hablo en plural, pero bueno— encontrando como algunos detalles de cómo se relacionan; la idea es que esto pues se modifique en el dashboard.

`[09:11]` Como las preguntas, ¿te acuerdas? Por ejemplo. Texto actual: «¿A qué población se considera este proceso de organización?». Pregunta: «¿A qué población se dirige?».

**Participante B (Coordinador / Líder institucional — Rubén)**

`[09:25]` No sé, o sea, como sí se fue la que encontraste que se copió de la pregunta de armonización normativa.

**Participante A (Desarrollador del sistema — Ricardo)**

`[09:32]` Exacto. Luego, no sé, o sea, de hecho no sé si tengo el último, el último cuestionario, o sea, ya no se ha modificado.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[09:43]` Sí, te acuerdas que hasta me dio nervio y dije, ay, no sé, dije, ya, bueno, te lo voy a mandar y me dijiste, sí, de todos modos se puede.

**Participante A (Desarrollador del sistema — Ricardo)**

`[09:49]` Ah, justo. Y estas son las cosas, o sea, como, o sea, creo que lo ideal es que tú las hagas porque implica decisión y algunas cosas son pendejadas, pero prefiero que esté en tu contra.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[10:00]` No, y además hoy lo pidieron ya.

**Participante A (Desarrollador del sistema — Ricardo)**

`[10:01]` O sea, prefiero no tocarlo, no estaría.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[10:04]` Está bien porque es mi responsabilidad, pero hoy ya, yo creo que ya llegó al límite en el que ya lo, ya pidieron el cuestionario.

**Participante A (Desarrollador del sistema — Ricardo)**

`[10:12]` ¿Quieres que te... Mira, algo que puede ser muy rápido es que haga una exportación, o sea, en el dashboard. Se va a poder exportar la lista de... Ya se puede editar, pero puedo exportarlo. No sé si en algún, o sea, como tú me lo mandaste en un formato, ¿te acuerdas?, de Word.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[10:46]` Sí, te lo mandé en Word, lo

**Participante A (Desarrollador del sistema — Ricardo)**

`[10:49]` tienes ahí para verlo porque no me acuerdo, o sea, ya tiene mucho tiempo cómo está.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[11:40]` Ah, pero ya salió el PDF, no era Word, era PDF.

**Participante A (Desarrollador del sistema — Ricardo)**

`[11:46]` No importa. O sea, PDF y Word, da igual, pero así son todas las preguntas, son todas, todas, todas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[12:29]` ¿Lo que no tiene es las armonización, la tablita?

**Participante A (Desarrollador del sistema — Ricardo)**

`[12:41]` ¿Tablita de transversalización, no? De distintos...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[12:46]` O sea, esta es la pregunta de instituciones, ya los criterios de la organización están adentro con una tablita, ese creo que también lo tenías.

**Participante A (Desarrollador del sistema — Ricardo)**

`[12:54]` Ya lo tengo, sí. Yo tengo todo, o sea, tengo. Ese no es el documento final, sino es otro.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[12:59]` Esta es la lista final de preguntas, pero pues quisieron lo que más...

**Participante A (Desarrollador del sistema — Ricardo)**

`[13:24]` ¿Se lo mandas así o lo terminamos en corto? Es que yo me he atrasado, pero puedo trabajar así durísimo el fin de semana y lunes a primera hora lo checamos y se los mandamos o ya que puedan contestar. Bueno, dijimos que el 10, ¿no? ¿El 10 de septiembre o qué día era que lo íbamos a abrir? 25. Pero podemos, podemos abrir solo la parte que no es de que vean las preguntas sin que todavía puedan. Lo que habíamos platicado la otra vez.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[14:00]` Yo he manejado una retórica de vamos por partes: si no está verificada la información base, lo demás sale mal.

**Participante A (Desarrollador del sistema — Ricardo)**

`[14:08]` Sí, pero ya estamos.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[14:09]` Pero ya me dijeron, es que sí te quiero dar la información base, pero a mí las áreas a las que les pido información no me dejan que les haga por separado las peticiones o corro el riesgo de que ya no me den la información si pido un alcance y tal, entonces.

**Participante A (Desarrollador del sistema — Ricardo)**

`[14:25]` Oye, ¿por qué no lo abrimos a zonas possible? Sí, o sea, como yo la siguiente semana estoy tranquilo porque ya acabé un observatorio de conflictos ambientales, el 9 de septiembre va a tener su presentación de informe y entonces pues había estado la verdad muy enfocado en eso, pero la siguiente semana estoy tranquilo, entonces puedo dedicarme así full para tenerlo y mandarlo. ¿Cómo les ha ido con lo de las preguntas generales?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[15:09]` Bien, ya como diez terminaron.

**Participante A (Desarrollador del sistema — Ricardo)**

`[15:12]` ¿Y cómo les ha ido con la validación y los botones?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[15:16]` Es que apenas hoy fue la reunión y ya tuve reunión con mis compañeras becarias y ya van a hacer la primera verificación el lunes.

**Participante A (Desarrollador del sistema — Ricardo)**

`[15:25]` El lunes la información básica, creo que estaría bien. Es que sabes qué me sirvió mucho la reunión que tuve con Fer donde me dio retroalimentación, ¿te acuerdas? Entonces siento que estaría bueno, no sé si el martes, no sé si el mismo lunes cuando se los mostremos, pero tener una sesión de trabajo como para ver si ha funcionado, qué no, y poder hacer aclaraciones o no sé, o sea, como tú las capacitaste para hacer esta cosa de cómo validar y no hubo dudas, o sea, no sé, lo que quiero es como, es algo que va a ser de muchos años, pues que quede lo más claro posible desde el principio.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[16:21]` Sí, pues si quieres puedes terminar de montar el cuestionario y de las, pero de las y de las instituciones que son prueba, yo les puedo pedir a ellas que suban información, que contesten. ¿Cómo, cómo? ¿Pero quieres que te den retroalimentación?

**Participante A (Desarrollador del sistema — Ricardo)**

`[16:42]` De la parte de revisión.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[16:45]` De la parte de revisión, pero pues ahorita no están revisando. Sí, pero la información va por eso, pero no creo que te vaya...

**Participante A (Desarrollador del sistema — Ricardo)**

`[16:56]` Pues el Fer me dijo un montón de cosas muy buenas, entonces justo eso es como lo que...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[17:04]` Yo preferiría que terminemos.

**Participante A (Desarrollador del sistema — Ricardo)**

`[17:06]` Está bien, terminamos el cuestionario ya. Entonces tú le echas un ojo a estas... ¿Por qué le echamos un ojo? O sea, como para la estructura de lo que te acabo de enviar.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[17:26]` Ah, de lo que me acabo de

**Participante C**

`[17:27]` enviar.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[17:34]` Sí, esta está muy bien, esta que encontré yo la puedo corregir sin problema, la 4.1. Luego el 4.4 dice a cuántas instancias académicas se consideró para este proceso. Sí tiene el mismo problema, es como un copy paste que luego no se ajustó.

**Participante A (Desarrollador del sistema — Ricardo)**

`[17:56]` No hay ningún problema, yo lo

**Participante B (Coordinador / Líder institucional — Rubén)**

`[17:57]` puedo ajustar, ya vi cuál es el problema. Qué bien que lo viste.

**Participante A (Desarrollador del sistema — Ricardo)**

`[18:04]` Lo vi yo y lo vio Claudio, o sea, como que son cosas ahí sí, y...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[18:08]` Es que yo no reviso esas preguntas porque como son idénticas en estructura, no en contenido, siempre cuando reviso nada más reviso lo que es diferente. Pero por eso se fue justamente. Luego cuántas instancias académicas... Este es Políticas, Políticas institucionales y académicas de inclusión y no discriminación. Ah, ya, ya vi esta, la tengo

**Participante A (Desarrollador del sistema — Ricardo)**

`[19:04]` que revisar.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[19:06]` No sé si esto quedó en académicas porque nada más es para procesos académicos y las administrativas no tendrían relación, no me acuerdo. Luego este dice, este observable, la pregunta inicial no abre interrogación, le falta la...

**Participante A (Desarrollador del sistema — Ricardo)**

`[19:24]` Sí, sí, sí, o sea, hay cosas que son una trivialidad, ¿no?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[19:30]` Pero está bien. Tres formas distintas, sexo y género en

**Participante C**

`[19:35]` el instrumento.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[19:38]` Con diagonal, con guión, pues creo que es mejor con guión, lo vamos a estandarizar. Nueve observables tienen dos títulos distintos, uno en la lista de verificación y otro

**Participante A (Desarrollador del sistema — Ricardo)**

`[19:50]` en el cuestionario. ¿Pero esto no es el nombre corto que habíamos hecho? Sí, creo que más bien... Pero me parece curioso que no todos, o sea, a ver, ¿cuántos son? Son nueve, dice, y son 40, entonces ¿por qué solo nueve de 40? ¿Me explico? O sea, si es un nombre corto, ¿por qué es diferente? Aquí es nombre corto este y aquí, o sea, como que no coincide, entonces como que...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[20:28]` Sí me voy a tardar como un día, yo creo.

**Participante A (Desarrollador del sistema — Ricardo)**

`[20:30]` Sí, sí, sí.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[20:33]` 1.11 eliminó un fragmento que parecía una nota de trabajo.

**Participante C**

`[20:39]` El

**Participante B (Coordinador / Líder institucional — Rubén)**

`[20:39]` sufijo «Características de los observables».

**Participante A (Desarrollador del sistema — Ricardo)**

`[20:42]` Sí, eso está bien. O sea, no todo tiene que... O sea, como, o sea, literal yo la verdad es que ni siquiera. Sí, sí, todo lo que hemos observado.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[20:59]` Mujer, hombre, para persona titular, plantea sexo y género. Ah, no se estudia, o sea, más...

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:07]` Bien, lo que... o sea, lo que se puede modificar directo en el cuestionario desde el dashboard pues se genera lo...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[21:15]` que tú no has montado todavía las preguntas, ¿verdad?

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:21]` ¿Para que lo vean las instituciones?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[21:23]` Para que tú lo veas, no, para ti como parte del proceso de evaluación.

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:27]` Sí, ya están todas montadas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[21:30]` Sí, solo lo tengo que corregir más bien.

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:32]` Ahí en el dashboard, o sea, igualito, va a estar catálogos y una por

**Participante C**

`[21:39]` una.

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:41]` Van agrupados, observable, bueno, eje, observable...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[21:47]` Si ya la subiste, ¿qué te falta?

**Participante A (Desarrollador del sistema — Ricardo)**

`[21:49]` No, pero no están en el cuestionario, o sea, no, el cuestionario que contesta

**Participante B (Coordinador / Líder institucional — Rubén)**

`[21:55]` las instituciones, te falta programar las soluciones para que desaparezca como cuestionario.

**Participante A (Desarrollador del sistema — Ricardo)**

`[22:03]` Pero bueno, esto es lo único para cerrar ya el cuestionario y poderlo mostrar y yo lo que puedo hacer es como que puedo, o sea, puedo programar que no pueda responder todavía hasta el 25. Bueno, más bien si lo podemos abrir antes, pues que se abra. ¿Creo que no hay ningún impedimento para abrirlo antes del 25, o sí?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[22:30]` Pues tú ya un poco viste cómo es, o sea, sí se necesita mucho acompañamiento porque...

**Participante A (Desarrollador del sistema — Ricardo)**

`[22:38]` OK, o sea, lo pregunto porque como que creo que lo ideal... Más bien no tengo muy claro cómo le vamos a mostrar. ¿Cuál es la mejor forma de mostrarles ya todas las preguntas a las instituciones? Yo creo que la mejor forma es ya en la plataforma.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[22:59]` Así lo hemos hecho siempre, hacemos una presentación

**Participante A (Desarrollador del sistema — Ricardo)**

`[23:04]` ¿cuándo es la próxima reunión? Pero ya te la están pidiendo. ¿Pero no es mucho tiempo de aquí al 25, no?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[23:16]` Sí, ese día cumplimos con llegar ya con el cuestionario montado.

**Participante A (Desarrollador del sistema — Ricardo)**

`[23:20]` Aunque te estén presionando de aquí al 25.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[23:25]` Porque el compromiso fue mandarles el cuestionario completo.

**Participante A (Desarrollador del sistema — Ricardo)**

`[23:28]` Ah, bueno, el documento, pero eso no, o sea, eso puede ser antes de que esté en la plataforma.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[23:38]` Sí, porque incluso lo necesita porque antes de la plataforma. Claro, porque tienen que pedirle la información a las áreas, ¿quieres que, o sea...?

**Participante A (Desarrollador del sistema — Ricardo)**

`[23:46]` Mira, eso es algo que yo no voy a tardar nada porque literal es una... le digo a Claudio, haz un Word, o sea, como de estas preguntas conviértelas a un Word y ya, tú le das formato como este Word, este Word me da de nada. Entonces para que la fuente siempre sea como la fuente, lo que sea en el dashboard.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[24:16]` Fuentes, yo creo que hay que generar una especie de documento que se llame «Cuestionario final final» y ya con los errores que tenga ni modo que se quede, o sea, obviamente vamos a corregir todo lo que tú ya encontraste. Y con base en ese documento nada más me explicas cómo entrar a corregir, corrijo y tú ya con eso publicas. Pero mientras tanto tienes algunas cosas que

**Participante A (Desarrollador del sistema — Ricardo)**

`[24:49]` programar para que te enseñe dónde son las preguntas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[24:54]` No, me refiero a que tienes una parte de chamba todavía para mandar el guacho para que sea visible para los...

**Participante A (Desarrollador del sistema — Ricardo)**

`[25:11]` Pero puedo hacer mientras una exportación del Word, o sea, tú editas y en cualquier momento agrega un botón para descargar todo el cuestionario. Es que si no, ¿cómo le compartes el cuestionario a las...? O se lo compartes ya que esté editable. Tengo los cuestionarios, pero si vas a hacer cambios...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[25:44]` Claro, porque yo los haría en el Word en función de tus comentarios y en el dashboard.

**Participante A (Desarrollador del sistema — Ricardo)**

`[25:55]` Ah, es que lo que yo te decía es como que al revés, o sea que no edites, o sea que ya no edites nada en Word y entonces tú lo editas en el dashboard y agregas un botón de exportación de Excel a Word y entonces el Word

**Participante B (Coordinador / Líder institucional — Rubén)**

`[26:10]` ya no hace formato, entonces ya no

**Participante A (Desarrollador del sistema — Ricardo)**

`[26:13]` tienes que editar en dos lados y como que la fuente, la única fuente, el único lugar donde está como... Pues no, o sea, como es que lo...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[26:24]` Voy, yo no lo digo por aquí, lo digo porque otras veces exporto cosas de plataformas, media hora estar poniéndoles espacios,

**Participante A (Desarrollador del sistema — Ricardo)**

`[26:35]` le ponemos un diseño, o sea, un diseño bonito, o sea, de hecho puedo seguir el lineamiento de lo que me enseñaste, de lo que mencionaste, o sea, yo puedo, esto lo puedo programar... O sea, yo no lo voy a hacer, o sea, no voy a decirle... Bueno, sí lo voy a hacer porque voy a coordinarlo, pero es algo que me va a tomar una hora y esa hora creo que vale la pena para que ya no... Sí, porque ahí

**Participante B (Coordinador / Líder institucional — Rubén)**

`[27:03]` cualquier ajuste ya nada más es descargar, ya, dos, tres.

**Participante A (Desarrollador del sistema — Ricardo)**

`[27:08]` Incluso esa descarga podría estar en la plataforma también pública, estaría muy bien porque

**Participante B (Coordinador / Líder institucional — Rubén)**

`[27:13]` así pueden descargar el cuestionario y ya no depende de que selecciones, pase, pase, el pase, porque todo hoy me lo volvieron a pedir y además dice, o sea yo, pero a veces me dicen cosas como «no me mandaste...» una cosa es «no me llegó», pero siento que mala onda que te digan esas cosas después de tantas veces.

**Participante A (Desarrollador del sistema — Ricardo)**

`[27:37]` O sea, podría, justo como si la respuesta siempre es en la plataforma, y entonces vamos generando ahí una cosa, un pequeño espacio donde podamos subir cosillas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[27:49]` ¿Por qué?

**Participante A (Desarrollador del sistema — Ricardo)**

`[27:51]` Porque, o sea, podemos agregar un botón que diga documentos y que tú puedas ir subiendo los documentos.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[27:58]` Sí, es que por más que tratamos de generar acuerdos, de hacer todo con tiempo, ¿cuánto meses llevamos con esto? Como dos años. Y aún así, pero...

**Participante A (Desarrollador del sistema — Ricardo)**

`[28:10]` eso te puede ayudar justo como ya está ahí y entonces como que la forma que he descubierto que funciona con las organizaciones, o sea, con los usuarios, es que les dices a ver, qué necesitas, búscame, si lo que necesitas no está ahí... si está ahí, todo es el pelo en la plataforma y entonces ya la respuesta es como «ya no tengo que enviar el correo, que buscar el archivo», creo que eso puede. Ahora, creo que lo que acabo de decir, creo que sí es diferente a la generación del Word, porque por mucho que le ponga estilos, puede ser que haya dos, tres cosas que todavía le tengas que modificar,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[29:01]` ¿Te acuerdas lo que habían dicho? Tratemos como que no trabajes más de lo que ya cotizaste.

**Participante A (Desarrollador del sistema — Ricardo)**

`[29:06]` Sí, está bien. Sí, por eso, o sea, por eso digo que yo no voy a hacer que sea... pero si hay algo que modificar, pues ya lo modificas tú, pero que tenga ya. Ahora, este PDF estaba basado en un Word. ¿Me puedes pasar el Word?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[29:39]` Qué nos toca hacer en paralelo al observatorio. El observatorio es uno de seis proyectos, son todos los proyectos y los doratos no aparecen.

**Participante A (Desarrollador del sistema — Ricardo)**

`[30:04]` Es que además como que te avientan y te avientan cosas, te tengo que enseñar a Claudio para que te ayude, o sea, güey, está muy cabrón.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[30:15]` Un día vamos a ver, este es compulsivo

**Participante A (Desarrollador del sistema — Ricardo)**

`[30:20]` ¿y qué es?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[30:22]` ¿Cuál necesitas?

**Participante C**

`[30:25]` Creo que es el que quieres, mira.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[30:28]` Es el que quieres, en Word, ¿verdad?

**Participante A (Desarrollador del sistema — Ricardo)**

`[30:34]` Viste, ahí dice «maqueta» justo, pero ese no está completo, completo, solo son... Ah, ya sé, complete.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[30:47]` Es el que quieres, ¿verdad? En Word, ¿verdad?

**Participante A (Desarrollador del sistema — Ricardo)**

`[30:54]` Es que ya todo lo registro, o sea, todo hay un registro documental. Entonces mira, espero que no te ofenda,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[31:08]` tienes que hablarle con honestidad.

**Participante A (Desarrollador del sistema — Ricardo)**

`[31:10]` No, yo, más bien, estoy diciendo que yo voy a ser honesto contigo de qué he acabado y qué no. ¿Ya viste? Entonces me dices, o sea, ¿cómo? Entonces yo no tendo memoria en cosas porque todo se guarda en un lugar muy específico. Entonces cuando avanzo, o sea, si ahorita le digo, le digo como avanza, avanza... Le puedo decir, quiero trabajar este tema que no hemos trabajado, con qué está conectado, no sé qué tengo que hacer antes. «Antes de esto tienes pendiente esta cosa y esto y esto». Lo vamos resolviendo, o sea, pero como que es como si tuvieras como un asistente súper inteligente y te va... Yo pago 1.700 euros.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[31:57]` No es que tú...

**Participante A (Desarrollador del sistema — Ricardo)**

`[32:01]` Todos lo necesitamos más de lo que pensamos.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[32:04]` Sí, pero yo tengo cinco compañeros.

**Participante A (Desarrollador del sistema — Ricardo)**

`[32:06]` El de ChatGPT hay 400. 400 es algo viable. También Claudio, pero Claudio no es muy eficiente. Ya tiene una cosa que se llama códecs, que es el para...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[32:23]` ChatGPT.

**Participante A (Desarrollador del sistema — Ricardo)**

`[32:26]` Pero es que esto es otro pedo. Esto es una dinámica de trabajo donde vas dialogando y tiene toda la información y vas resolviendo como varias cosas. Más bien, voy a hacer un tallado. ¿Y qué más? A ver, déjame. Justo

**Participante B (Coordinador / Líder institucional — Rubén)**

`[32:48]` ahorita el tema sería que pudieras... Ya te mandé el cuestionario, que pudieras mandarlo a que fuera visible para las de prueba, no, en las pruebas lo vemos con base en lo que tú me des y se lo voy a pasar también a mis compañeras. Si encuentran algo hacemos correcciones, descargamos y ya y ya con base en eso ya nada más toca avisarles a las IES que ya está listo.

**Participante A (Desarrollador del sistema — Ricardo)**

`[33:16]` OK.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[33:18]` Sí, creo que la parte en la que nos quedamos, que tú ya estabas ideando era cómo le ibas a hacer para que aparezca. Yo te diría que eso es lo más indispensable. ¿Y por qué es crucial? Porque yo sé que se van a súper espantar cuando vean el tamaño. Las conozco muy bien.

**Participante A (Desarrollador del sistema — Ricardo)**

`[33:42]` Entonces no les vas a mandar el PDF,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[33:45]` pero podríamos mandar después de que verifiquemos.

**Participante A (Desarrollador del sistema — Ricardo)**

`[33:49]` Junto con la plataforma, aunque no estén abiertas para que vean.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[33:54]` No importa que tarde a la semana que viene. ¿Por qué? Porque si yo les mando un cuestionario y luego contigo hacemos uno que corrige errores, les voy a tener que decir «oigan, hicimos unos ajustes, por favor no le hagan caso al anterior» y se van a empezar a revolver versiones y no, no, no. Entonces este, luego... Entonces este, a ver, ya déjame anotarlo para consultar. El orden va a ser el siguiente: uno, le mando a Ricardo cuestionario, ya te lo mandé, sí. Dos, yo corrijo en plataforma. Sí, ahorita

**Participante A (Desarrollador del sistema — Ricardo)**

`[34:37]` te enseño dónde se corrigió.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[34:41]` Tres, exportamos, Ricardo, programa exportación. Cuatro, exportamos y es el cuestionario final.

**Participante A (Desarrollador del sistema — Ricardo)**

`[35:01]` Voy a ponerle así formato a medias, o sea, formato a medias es como algo no crudo, crudo que tengas que, pero algo como que ya diste pocas ediciones de tu parte, o sea, como la parte fina para no tardarme yo haciendo la parte fina, sino que sea algo muy automatizado, como «Claudio, ayúdame, toma este Word y ayúdame».

**Participante B (Coordinador / Líder institucional — Rubén)**

`[35:25]` Y cinco, sería que tú alistas la estrategia de listado,

**Participante A (Desarrollador del sistema — Ricardo)**

`[35:52]` despliegue de los observables y las preguntas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[36:06]` El reto acá, tú ya lo tienes como súper claro, es que las IES puedan interactuar primero con un menú bastante compacto, obvio, ya vemos, si les da curiosidad y te dicen «no sé a qué se refiere con esto», le pueden dar clic y digan, bueno, aquí me están preguntando, no sé, cuidados, y yo pienso que no, pero le abro y tengo una sala de lactancia, entonces sí, pero que de entrada puedan tener algo muy compacto y que si dicen de cuidados no, y sé que no tengo sala, no tengo nada, mejor no, desde el principio ya se van a ahorrar un montón de trabajo, entonces así que puedan interactuar desde...

**Participante A (Desarrollador del sistema — Ricardo)**

`[36:51]` OK, eso lo puedo tener, o sea, puedo meterle full el domingo. Sí, el sábado, domingo, o sea, puedo hacer este fin de semana bastante labor

**Participante B (Coordinador / Líder institucional — Rubén)**

`[37:07]` para completar eso. Sí, estaría muy bueno. ¿Y nos podríamos reunir si quieres jueves o viernes de la próxima semana, o miércoles? El martes y miércoles vamos a estar a full con lo de la clausura del diplomado.

**Participante A (Desarrollador del sistema — Ricardo)**

`[37:22]` Ah, va, entonces el jueves... que va a estar muy grande el jueves y

**Participante B (Coordinador / Líder institucional — Rubén)**

`[37:27]` el jueves ya voy a estar libre.

**Participante A (Desarrollador del sistema — Ricardo)**

`[37:29]` Y si quieres que, o sea, si van a empezar a revisar las preguntas generales, si hay alguna duda de tu equipo... no sé, ¿quieres que me juegue? Yo sé que tú no quieres que haga eso, pero yo sí quiero ir mejorando la plataforma para que sea usable y el mejor momento es cuando lo empiecen a usar, ¿no?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[37:51]` Sí, hagámoslo. Pero ¿te parece cerramos esto?

**Participante A (Desarrollador del sistema — Ricardo)**

`[37:53]` Sí.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[37:54]` Y ahí ellas ya también van a haber cogido un poco más de experiencia, apenas están empezando a revisar.

**Participante A (Desarrollador del sistema — Ricardo)**

`[38:01]` ¿Tú cuándo vas a revisar estas texturas?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[38:05]` Creo que es mejor que sea viernes.

**Participante A (Desarrollador del sistema — Ricardo)**

`[38:07]` Para que yo lo haga el jueves. ¿Tú hasta el jueves? ¿Ya viste? Es muy poquito.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[38:14]` Sí, es más por lo que tengo encima, es mucha logística en serio. ¿El otro evento? No, esto sé que no lo voy a hacer.

**Participante A (Desarrollador del sistema — Ricardo)**

`[38:27]` ¿Quieres que te diga nada más dónde

**Participante B (Coordinador / Líder institucional — Rubén)**

`[38:32]` encuentras? Sí, de hecho es posible que el jueves que nos veamos, si no alcanzo, no tenga listo eso, pero podemos ver lo que tú avanzaste y yo le daría prioridad a más tardar el viernes o el lunes para que ya esté listo el bo... el sondeo. Pero bueno, veamos esto. Y mira, dice lo que me dijiste de en dos navegadores.

**Participante A (Desarrollador del sistema — Ricardo)**

> *Nota: Se mantiene 'onigis.unam.mx' basándose en la sigla ONIGIES de la plataforma.*

`[38:58]` ¿Y por qué usas Netlify? ¿Por qué no usas onigis.unam.mx?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[39:06]` Porque sí, siempre entro a este, ya se me acostumbró, ya está guardando, nomás pongo la O y se pone.

**Participante A (Desarrollador del sistema — Ricardo)**

`[39:13]` Está bien, está bien.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[39:14]` ¿Estás aquí en gestión de catálogo, no? Preguntas base, no.

**Participante A (Desarrollador del sistema — Ricardo)**

`[39:29]` Entonces si te vas a componente, abres uno y ahí se edita el nombre del componente y ahí abajo están los observables. Perdón, creo que no subí la última parte, déjame... déjame subirla, pero bueno, aquí se lo hice. Observables... Perdón, o sea, algo me falta ahí ponerte esto, pero bueno. Sí, sí, sí, perdón, lo completo, pero bueno, ahí va a estar,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[40:13]` Aquí me va a aparecer la redacción y nada más llevo...

**Participante A (Desarrollador del sistema — Ricardo)**

`[40:15]` cambio, en eje vas a poder ver los observables, o sea, los componentes aquí y de los componentes vas a poder ver los observables y de los observables, o sea, como que va a estar todo anidado.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[40:23]` Y puedo cambiar el título y la redacción.

**Participante A (Desarrollador del sistema — Ricardo)**

`[40:27]` Todas estas cosas que están aquí habrían de estar editadas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[40:35]` Entonces ahí también lo

**Participante A (Desarrollador del sistema — Ricardo)**

`[40:36]` anoto. Eso lo subo porque ya...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[40:39]` lo tenía y no voy a ponerlo hasta mandar... ¿A cuándo ya sacas de producción?

**Participante A (Desarrollador del sistema — Ricardo)**

`[40:48]` Deploy, subir a producción, despliegue a producción. En catálogos y ahí va.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[41:08]` Sí, porque en ese yo trabajaría.

**Participante A (Desarrollador del sistema — Ricardo)**

`[41:12]` ¿Qué más nos falta? Creo que eso es todo, ¿no? Sí, la reunión de Cómputo UNAM.

**Participante C**

`[41:24]` Ni

**Participante B (Coordinador / Líder institucional — Rubén)**

`[41:24]` siquiera lo he cuestionado. ¿Y si grabas la reunión, se genera

**Participante A (Desarrollador del sistema — Ricardo)**

`[41:34]` una tarea, o sea, la tarea ya está generada, mira, dice task 102 reunión con la IBA, gestionando

**Participante B (Coordinador / Líder institucional — Rubén)**

`[41:43]` No, pero lo que te pregu... es, cuando tú grabes la reunión, Patricia, ¿cómo se llama?

**Participante A (Desarrollador del sistema — Ricardo)**

`[41:49]` Claudia.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[41:54]` Claudio sabe que tiene que agarrar esa grabación, o sea, yo le digo:

**Participante A (Desarrollador del sistema — Ricardo)**

`[42:00]` «Esta es la grabación de la última reunión» y como que por cada hora de reunión yo necesito como 20 minutos de detalle, como que tengo un diálogo de esto, o sea, como para aclarar como las cosas y luego ya se convierten esas cosas en tareas o las tareas que ya existían como se actualizan, se vinculan, no se ponen decisiones, o sea, son tareas, decisiones y documentos, entonces como que todo se va guardando.

**Participante C**

`[42:29]` Y

**Participante A (Desarrollador del sistema — Ricardo)**

`[42:33]` todo se va guardando automáticamente, entonces ya no tengo que estar, o sea, es como de, o sea, yo voy a... ahorita hago la sesión como de cierre de esta madre, como le paso el audio, le digo oye, está este audio, actualizamos las tareas, tengo un diálogo, tengo como una metodología para actualizar unas instrucciones y después yo al rato cuando empieza a trabajar esto le digo oye «¿Qué es lo siguiente que tengo que hacer?». Así literal digo, «¿Qué es lo siguiente que tengo que hacer?». Me da la lista y le digo... Me los da por grupos y le digo «OK, vamos a trabajar este grupo ahorita», entonces ya lo mandan y luego es como «¿qué otra cosa pendiente?», entonces ya no llevo el registro, o sea, mira, mis anotaciones ya no importan. Y el tema es que estos más se pierden, entonces como que es muy difícil para mí como abrir esta cosa y es muy fácil preguntarle a Claudio: «Claudio, ¿qué tengo pendiente?» y empezar a hacerlo.

**Participante C**

`[43:42]` y

**Participante B (Coordinador / Líder institucional — Rubén)**

`[43:46]` ¿El stick ya quedó lista la parte esta de la computadora virtual, hicieron

**Participante A (Desarrollador del sistema — Ricardo)**

`[43:53]` la migración? Ya, pero falta que hagan las pruebas de seguridad. Eso es lo que tenía duda, de que tenemos que mandar... Tuvimos una reunión con DGT, con DGTIC creo que no tienen general, no sé, no importa.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[44:12]` Y estuvo... ¿estuvo Pati? No, Patricia. Ah, no, pero tú me habías dicho que ella hizo la solicitud, ¿no?

**Participante A (Desarrollador del sistema — Ricardo)**

`[44:22]` ¿Había hecho una su...?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[44:23]` Ajá, es que en azul trabajaba con ella, con Pati.

**Participante C**

`[44:25]` Hola, oye, ¿todavía te vas a tardar? Porque me están hablando de vigilancia que como dejaste tu identificación, que ya van a cambiar de turno, entonces nada más quieren saber si todavía vas a estar.

**Participante A (Desarrollador del sistema — Ricardo)**

`[44:37]` Más tiempo aquí, como a las 4.

**Participante C**

`[44:43]` Va a ser más tarde porque ella ya se va, entonces yo creo que ya va a ser hasta después de las 3, ya que hicieron el cambio

**Participante B (Coordinador / Líder institucional — Rubén)**

`[44:48]` de turno, para que a las 3 baje

**Participante C**

`[44:51]` por su credencial. No, es que no se la van a dar si no

**Participante B (Coordinador / Líder institucional — Rubén)**

`[44:56]` es necesario. Entrega el gafete, pero yo le digo

**Participante C**

`[45:00]` que te vas a ir entre 3 y 3:10.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[45:04]` Gracias. Ah, sí, sí, sí. Entonces eso es lo que nos dice... Ah, OK, entonces es para ti.

**Participante A (Desarrollador del sistema — Ricardo)**

`[45:12]` Ahora, tú puedes... Mira, puedes preguntar de una vez a este muchachito.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[45:21]` Todavía me falta crear ese vínculo.

**Participante A (Desarrollador del sistema — Ricardo)**

`[45:24]` Ah, pero puedo decirle, oye,

**Participante C**

`[45:29]` Es que

**Participante B (Coordinador / Líder institucional — Rubén)**

`[45:30]` apenas acaba casi de entrar, él nos

**Participante A (Desarrollador del sistema — Ricardo)**

`[45:33]` puede ayudar a hacer la apertura del ticket. O sea, pero eso pues es importante, mientras corre en mis y yo hago un puente y así,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[45:49]` Sí, pero no... está bien, pero la

**Participante A (Desarrollador del sistema — Ricardo)**

`[45:51]` información está en mi servidor.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[45:53]` Sí, bueno, confío en ti, pero de

**Participante A (Desarrollador del sistema — Ricardo)**

`[45:55]` todos modos es lo adecuado. La van a hacer de pedo en algún momento con el tema, o sea, no pasa nada, pero no porque la información no esté segura, solo porque la pueden hacer de a tos.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[46:05]` Sí, por esta cosa de... Está bien. ¿Quién tiene los datos? De hecho, por eso usamos este correo de Outlook, porque dicen que el de Google no sé qué tiene, pero que parece como que la información se almacena en no sé qué lugar, como que es de la empresa y no de la universidad. Yo no entiendo esas cosas, pero por esa razón usamos este servidor... Paquetería horrorosa, ese servicio de...

**Participante A (Desarrollador del sistema — Ricardo)**

`[46:36]` Sí, es horrible. Gmail sí es muchísimo mejor. Outlook es horrible. En realidad Microsoft es horrible,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[46:45]` sí, en serio, borra correos, los pierde, los traspapela, los botones no son intuitivos. A veces no encuentro el valor para firmar.

**Participante A (Desarrollador del sistema — Ricardo)**

`[46:54]` Lo que está claro es que Gmail tiene 20 años funcionando. 20 años funcionando, pero es simple.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[47:01]` Y Outlook no. Outlook a veces no encuentro el menú.

**Participante C**

`[47:08]` Por

**Participante B (Coordinador / Líder institucional — Rubén)**

`[47:08]` ejemplo, Outlook, si abres un correo para ponerle no leído, lo tienes que ver, salirte, volver a entrar, ponerle no leído... Pues eso.

**Participante A (Desarrollador del sistema — Ricardo)**

`[47:23]` Y hay como otros criterios que todavía no sé si ya están definidos, no me acuerdo, como lo del 0 al 10 o del 0 al 5, cuánto va a pesar cada cosita. Ahora, lo que yo puedo hacer es que en estos observadores y componentes, la idea es que cada uno tenga su peso y aquí lo puedas editar, pero es algo que hay que decidir y no sé si lo van a preguntar ellas, las instituciones, como de cuánto pesa cada cosa y cómo se va a medir eso. Siento que es una discusión metodológica importante.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[47:51]` Que tenemos pendiente, sí es que no hemos definido. Yo soy de subirlo al 10, mi intuición me dice que

**Participante A (Desarrollador del sistema — Ricardo)**

`[48:04]` para diferenciarlo del anterior,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[48:08]` porque si lo dejas de 0 al 5, todas van a sacar puntos más bajos, eso es obvio. ¿Y qué te van a decir? «Bajé». Y lo que tenemos que responder es «no bajaste porque no es la misma metodología, no estás midiendo la misma, quizás con la metodología anterior subiría», entonces creo que es mejor tener una de 0 a 5... además si antes sacabas 3 y ahora sacas 3, se siente tan feo.

`[48:29]` Es que es 3 de 0 al 5 y 3 de 0 al 10, pero no sé, como que siento que la carga psicológica se puede matizar con eso. Una escala del 0 al 10 creo que es más común a las métricas universitarias, por lo general se evalúa en esos rangos y lo que habíamos hablado con Isabela, que a mí me pareció bien —fue una propuesta de ellas— es que quizás lo mejor para no meternos en ese rollo de tener que justificar que vale 3, que vale 2, que vale tal, todo valiera lo mismo en términos de observables.

**Participante A (Desarrollador del sistema — Ricardo)**

`[49:11]` Sí, eso, eso creo que sí es como lo que ha sucedido durante todo este año, o sea, no hay problema, pero lo que me preocupa es, hay preguntas de transversalización, otras de institucionalización, otras de planes, hay otras que... hay preguntas específicas, eso cómo, o sea, cuánto vale cada cosa y porque depende también del indicador. Pues hay unas que tienen... tenemos tres tipos de preguntas, hay unas que tienen solo una, bueno, todos tienen dos, institucionalización y tras... pero hay otras como las planes, como no sé qué,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[49:47]` Yo creo que sí tendríamos que definir el peso interno, que ahí no sé si puedes ir pensando, pero pensaba si... pues hay que hacer un análisis, le tengo que preguntar a otras personas, tener muchas visiones, pero no sé si se vuelve muy relajo que todo sea promedio al interior, que valga lo mismo la transversalidad que la institucionalización. El tema es que son...

**Participante A (Desarrollador del sistema — Ricardo)**

`[50:21]` Sí, pero es que hay más preguntas que solo transversalidad, o sea, hay otro tipo de preguntas. No, no, esas son de institucionalización. Sí, armonización, bueno, institución, armonización es una y luego estabilización es otra, pero hay otros tipos de preguntas, o sea, hay unas que dentro de esas preguntas es como cuál es la distribución de género, o tienen... o por ejemplo los planes de estudio, ¿cuántos planes de estudio conciliaron? Y entonces ahí, qué güey, o sea,

**Participante B (Coordinador / Líder institucional — Rubén)**

`[50:54]` como... creo que ahorita hasta este nivel lo que me da tranquilidad es que la idea es que si cada observable vale 10, internamente...

**Participante A (Desarrollador del sistema — Ricardo)**

`[51:11]` Sí está bien, eso no hay problema.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[51:13]` Hasta ahí creo que vamos tranquilos. Ahora, internamente pues tengo que revisar, lo

**Participante A (Desarrollador del sistema — Ricardo)**

`[51:19]` voy a poner aquí también. Eso no es parte de lo que estaba editable en observables, pero voy a poner un campito que... ¿Qué puedes hacer? Ahora, hay una calificación, o sea, como... Tú puedes tener un default para visualización y transversalización. Ese no hay ningún lugar donde se pueda editar todavía, o sea, como tengo que pensar dónde... Y, o sea, como si tú dices que pese siempre, o sea, que el default de trans... antes lo que teníamos era 3 y 2, no sé si te acuerdas.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[51:53]` Y había unos que valían 5 porque no

**Participante A (Desarrollador del sistema — Ricardo)**

`[51:56]` había transversalización, entonces lo ideal es que haya un default que sea para los 41 observables y algunos observables los puedas, sobre todo los que tienen una lógica distinta, que puedas personalizar, o sea, que no tengas que personalizar uno por uno, sino que tengas un default y si modificas ese default es el que se comporta diferente al default general.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[52:25]` Y el default no tendría problemas si por ejemplo en los criterios de institucionalización, que es armonización, hay más o menos elementos, ¿verdad?

**Participante A (Desarrollador del sistema — Ricardo)**

`[52:36]` Se ajustaría otra vez, perdón, ya viste

**Participante B (Coordinador / Líder institucional — Rubén)**

`[52:39]` que en institucionalización luego viene una batería, dice por ejemplo, cómo se institucionalizó esta política, se aprobó y tiene criterios y cada uno es uno solito, y este default no importa porque hay tablitas que tienen cinco, otras cuatro.

**Participante A (Desarrollador del sistema — Ricardo)**

`[52:53]` Ah no, pero eso siempre el default...

**Participante B (Coordinador / Líder institucional — Rubén)**

`[52:56]` les promedia estos, esos, ahí sí ya...

**Participante A (Desarrollador del sistema — Ricardo)**

`[52:58]` No me meto, o sea, yo no haría que esos valieran diferente porque sería demasiado difícil de mantener.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[53:03]` No, no, no, y además no hay criterio, lo mejor siempre es promediado, de hecho así lo hicimos metodológicamente pensando una jerarquía entre ellos, esto vale 2... No, no, todos valen lo mismo. El valor de institucionalización con armonización es el promedio de sus elementos, pero lo que no hemos definido es si institucionalización vale algo distinto que transversalidad y las otras preguntas que son

**Participante A (Desarrollador del sistema — Ricardo)**

`[53:32]` específicas. Eso no tenemos que resolverlo ahorita, pero hay que, o sea, como lo ideal es que destinemos un día para conversar eso y para, o sea, como si es algo que está bien tenerlo pues presente.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[53:50]` Me dieron el contacto de una consultora para preguntarle, o sea, es muy buena, pero no, o sea, lo que me dijo es que no había realmente como un canon, ¿no? No, todo es nada más tomar la decisión, dejarla metodológicamente sentada y argumentar un grado de razonabilidad. Hola Pati, ¿cómo estás? Entonces, en realidad es lo que siempre hago, o sea, hacer cosas con seriedad, no definir al azar el criterio, sino que sí hacerlo por una razón, esa razón escribirla y argumentar.

**Participante A (Desarrollador del sistema — Ricardo)**

`[54:34]` Sí, yo coincido. Bueno, yo puedo también decir los indicadores, y sí le

**Participante B (Coordinador / Líder institucional — Rubén)**

`[54:40]` pregunté, le dije como de «oye, pero hay un consenso a nivel regional en la CEPAL».

**Participante A (Desarrollador del sistema — Ricardo)**

`[54:45]` Ah, pero de género en específico, ella

**Participante B (Coordinador / Líder institucional — Rubén)**

`[54:48]` sabe en general y en género en particular, ella se ha dedicado a estadísticas para indicadores en organismos internacionales, trabaja en ONU Mujeres, y me dijo, hay índices de 0 al 5, hay índices de 0 al 3, no sé por qué, hay índices de 5 al 10, hay índices de 0 al 4, hay unos

**Participante A (Desarrollador del sistema — Ricardo)**

`[55:08]` que son porcentajes, hay otros que son... Sí, o sea, eso es cada quien, y lo que sí es que hay diferentes metodologías, por ejemplo, esta es la metodología de al menos, o sea, si no tienes al menos una, pues eso es como un índice de carencia, no solo existen los promedios sino también como los índices de carencia, los indicadores de carencia, si no cumples ninguno de estos cinco, entonces... o si no se cumple, cumples dos de cinco, o sea, por ejemplo, CONEVAL es así, pero yo creo que no tiene sentido hacer eso porque complicaría hacerlo lo más simple. ¿Y la última pregunta es como hay un... tuteamos o ustedeamos?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[56:02]` Así lo vi en el comentario.

**Participante C**

`[56:09]` Sí.

**Participante A (Desarrollador del sistema — Ricardo)**

`[56:12]` Yo no conozco ninguna plataforma que

**Participante B (Coordinador / Líder institucional — Rubén)**

`[56:13]` usted, pero es que está en tercera persona la IES, no sé, pero tú que trabajas en la IES piensas que...

**Participante A (Desarrollador del sistema — Ricardo)**

`[56:27]` Pero por ejemplo, cuando eliminas, ¿estás seguro de eliminar?

**Participante B (Coordinador / Líder institucional — Rubén)**

`[56:32]` Ahí sí puedes tutear, porque ahí lo que estás diciendo es... No, es una pregunta de cuestiones, no una pregunta de formulario.

**Participante A (Desarrollador del sistema — Ricardo)**

`[56:39]` No, no, las del cuestionario sí tienen que estar en tercera persona, pero yo me refiero a los mensajes de la plataforma y sobre todo la parte que tiene que ver con los estatus.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[56:49]` Están todas en...

**Participante A (Desarrollador del sistema — Ricardo)**

`[56:50]` Está bien en tú.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[56:52]` Todas están en tú y se ven re bien. Sí, ya la gente se acostumbró a usarlo así.

**Participante A (Desarrollador del sistema — Ricardo)**

`[56:58]` Es que eso es algo que notó Clau, no es algo que yo haya notado. Y me dijo, hay cosas en tu y hay cosas en usted, o más bien, o sea, me propusieron la redacción de usted y le dije «cámbialo a tú», y me dice «no, pero hay unas cosas en usted y en tu», no sé... Bueno, pues muy bien, creo que es todo.

**Participante B (Coordinador / Líder institucional — Rubén)**

`[57:18]` Muy bien, ¿qué vamos a hacer?, ¿qué tengo que hacer?

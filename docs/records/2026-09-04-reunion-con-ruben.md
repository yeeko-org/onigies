---
type: record
id: 2026-09-04-reunion-con-ruben
title: "Reunión con Rubén, 4 de septiembre — transcripción limpia"
date: 2026-09-04
source: ["[[2026-09-04-reunion-con-ruben_raw]]"]
---

# Transcripción limpia: reunión con Rubén, 4 de septiembre

Versión editada de la reunión de trabajo de 57 min 22 s entre Ricardo (desarrollador de la plataforma ONIGIES) y Rubén (CIGU, responsable del ONIGIES), grabada el 4 de septiembre de 2026 a las 14:57 hora de la Ciudad de México. Fuente: [[2026-09-04-reunion-con-ruben_raw]], donde vive la salida sin tocar del pipeline y la URI del audio en el bucket privado.

**Qué se hizo aquí y qué no.** No se resumió nada: se conserva todo lo que se dijo sobre el proyecto, en el orden en que se dijo, con sus cifras, sus fechas y el registro de cada quien. Lo que cambió es cómo se lee: las letras del pipeline son ahora los nombres, las frases que el alineador partió a la mitad entre dos bocas volvieron a la que las dijo, los fragmentos sueltos que el pipeline atribuyó a un tercer hablante inexistente se reabsorbieron en el hilo al que pertenecían, y los titubeos y las repeticiones de máquina se acortaron. **Los timestamps son los ids de párrafo**: cada uno apunta a su párrafo en la cruda y al minuto del audio; un párrafo fundido de varios lleva todos sus timestamps, el primero como cabeza.

**Lo que se quitó por ajeno al proyecto**, y solo esto: la interrupción de `[44:25]`–`[45:04]`, cuando entra alguien de la CIGU a avisar que vigilancia cambia de turno y pregunta por la credencial de Ricardo; el desahogo sobre Outlook y Gmail de `[46:05]` (cola) a `[47:08]`; y dos saludos sueltos a terceros que pasaban, incrustados en párrafos que sí se conservan («hola Adri» en `[05:34]` y «Hola Pati, ¿cómo estás?» en `[53:50]`). El forcejeo con el archivo comprimido en `[07:57]` no se cortó: se acortó a lo que dejó como hecho.

**Correcciones de término aplicadas aquí** (la cruda las conserva como salieron): «BO» → «BP» en `[04:39]`; «códecs» → «Codex» en `[32:06]`; «task-102, reunión con la IBA» → «task-102, reunión con Cómputo UNAM» en `[41:34]`, verificado contra el nodo `task-102` del grafo; «estabilización» → «institucionalización» en `[50:21]`; «visualización» → «institucionalización» en `[51:19]`; «observadores» → «observables» en `[47:23]`; «onigis.unam.mx» → «onigies.unam.mx» en `[38:58]`.

**Lo que quedó sin resolver está listado al final**, en «Dudas de lectura», con el fragmento textual y las lecturas posibles.

**Dos marcas quedaron dentro del cuerpo**, ambas fechadas el 11 de septiembre y ninguna altera lo dicho:

- En `[48:08]`, la escala del índice: el pipeline transcribió «de 0 a 5» contra el sentido de todo el párrafo, y Ricardo, de memoria, el 2026-09-11, fijó que Rubén dijo **«de 0 a 10»** y la declaró definitiva. La frase va corregida en la limpia; la cruda conserva lo que salió del pipeline. La escala quedó fijada en [[adr-0016]].
- Antes de `[43:46]`, una nota editorial que separa lo que en ese tramo **es de STIG y no de ONIGIES**: el proyecto hermano del mismo cliente. Sin ella, el tramo se lee como si la migración al servidor de la UNAM del ONIGIES ya hubiera ocurrido, y no ha ocurrido.

---

## Transcripción

**Ricardo**

`[00:18]` ¿Pues cómo va todo?

**Rubén**

`[00:18]` A ver. Si quieres empezamos por lo administrativo. ¿Te busco agua?

**Ricardo**

`[00:24]` `[01:05]` Sí, ya mandé mis documentos. No me han respondido todavía; se supone que entre dos y no sé cuántos días hábiles. El primero de septiembre me dijeron: «Informamos que su registro quedará concluido una vez que se haya verificado su información». Ahorita te digo lo que me dijo Dana: me dijo que iba a estar entre mañana y el jueves, pero eso me lo dijo el martes.

**Rubén**

`[01:11]` ¿Cómo te dijo que te registraras? ¿Como proveedor? ¿Fue todo lo que te dijo?

**Ricardo**

`[01:17]` Ahora no… déjame ver si ya llegó algo, dame un segundo.

**Rubén**

`[01:21]` OK.

**Ricardo**

`[01:37]` `[02:02]` No me ha llegado nada. Ya pasamos el tiempo que ellos mismos ponen y no me ha llegado nada. No sé, ¿quieres que le pregunte así de pronto? Me dijo que tenía que estar al pendiente de que me avisaran, y todavía no está; entonces dependemos de eso.

**Rubén**

`[02:22]` Mira, lo que me dijeron es que del presupuesto que nos queda van a asignar todo lo que nos quedaba para la partida en la que te vas a registrar, que es como proveedor. Eso no sería honorarios, sería factura, y te pagarían en dos partes: una ya ahora, empezaría a tramitar el proceso, y otra en octubre.

**Ricardo**

`[02:56]` `[03:13]` `[03:14]` Yo tengo que hacer cuentas bien de cómo va, porque independientemente de que no se pague, decirte claramente: «Mira, he trabajado esto y estoy implicado» en lo que ya… Sobre todo con el módulo de buenas prácticas, que habíamos pensado en hacerlo muy chiquito y le fuimos aumentando más cositas y variaciones. Lo demás ha estado bien, creo que ha estado dentro de todo.

`[03:36]` ¿Son 80 mil pesos en total?

**Rubén**

`[03:36]` `[03:46]` No, no, no, te debo todavía más; pero lo que te van a pagar en estos dos pagos…

**Ricardo**

`[03:46]` Vale, en esos dos.

**Rubén**

`[03:48]` Sí, te van a dar primero 32 y luego 48.

**Ricardo**

`[03:51]` ¿Pero no era un presupuesto más grande?

**Rubén**

`[03:54]` No, no, no. Te van a dar esto en abono, y todavía me faltan como más de 100 mil de lo que tú cotizaste; pero ahorita lo que tenemos disponible en la vaquita de la CIGU es eso, y te van a dar todo. Esa es la estrategia que encontramos.

**Ricardo**

`[04:15]` Ya te entendí.

**Rubén**

`[04:16]` Me agarré todo lo que nos queda, que no estaba asignado al observatorio, pero me lo pasaron, ¿si me explico? Entonces te van a pagar esto, y esos 80 obviamente no… hace falta mucho. Creo que apenas vamos ahí como a un tercio: estos 80 mil pesos no llegan ni a un tercio de lo que es la cotización, nada más es un abono.

**Ricardo**

`[04:39]` De todas maneras todavía falta una parte potente de las BP y falta la página pública.

**Rubén**

`[04:45]` `[05:21]` Claro, lo que te vamos a ir dando como abonos, porque no nos liberaron el recurso completo como lo pedí. Es lo que te digo: siempre pasa, para todo pasa, nunca nos dan dinero para nada. No aquí en la CIGU, sino presupuesto de la UNAM. De hecho yo volví a pedir —¿te acuerdas que te dije que volví a pedir para el año que viene, como si no me hubieran dado nada, el presupuesto completo y también uno para mantenimiento?—. Entonces eso se te pagaría de agosto a octubre, y en cuanto llegue el siguiente presupuesto en enero, ahí vamos a tratar de dártelo todo, todo lo que faltaba.

**Ricardo**

`[05:28]` Va, va.

**Rubén**

`[05:34]` Y la verdad es que los resultados van a ser lucidores; ya no hay duda de que hay que pagar eso. Incluso yo le dije a Norma que nosotras hicimos un diplomado —es otro proyecto, pero cobramos y de ahí ingresaron como 200 mil pesos—. La UNAM te quita mucho, pero yo le dije que ese dinero sí se podía disponer para el observatorio y me dijo que sí; solo que todo ese dinero lo tiene la Secretaría Administrativa de la UNAM, no lo tiene aquí directamente la CIGU. Siempre es un rollo. Pero bueno, decirte que estos ya están asegurados. Y si quieres, un día en octubre, cuando te paguen el segundo pago, nos sentamos nada más para ver qué has hecho, qué se te ha pagado y cuánto falta.

**Ricardo**

`[06:25]` Sí, va, me parece bien.

**Rubén**

`[06:28]` OK, entonces ahora pasamos a ONIGIES.

**Ricardo**

`[06:34]` Ah, OK, invítame a esos webinars.

**Rubén**

`[06:37]` Sí, tuvimos reunión y les expliqué; tenían muchas dudas, no técnicas sino metodológicas, de algunos ítems. Pero mira, les hice una simulación de cómo llenar la información y estaban muy felices. Ya voy a hacer las siguientes sesiones.

**Ricardo**

`[07:02]` Te voy a mandar un documento, me das un segundo. Te lo comparto por correo, por WhatsApp: un documento con dudas que ya había medio preparado pero no tenía bien listo, y ahorita le pedí a Claudio que me ayudara para trabajar con eso.

**Rubén**

`[07:28]` Si quieres WhatsApp.

**Ricardo**

`[07:29]` Sí, va. No sé por qué está en zip, así se descargó.

**Rubén**

`[07:50]` No lo leí. Ah, ya lo voy a descomprimir.

**Ricardo**

`[07:57]` `[09:11]` No se deja descomprimir… era quitarle el punto. No tenemos que hacerlo ahorita, pero te explico los cambios. En la revisión —y hablo en plural, pero bueno— fuimos encontrando algunos detalles de cómo se relacionan; la idea es que esto se modifique en el dashboard. Como las preguntas, ¿te acuerdas? Por ejemplo: texto actual, «¿A qué población se considera este proceso de organización?»; pregunta, «¿A qué población se dirige?».

**Rubén**

`[09:25]` Sí, se fue esa: es la que encontraste, que se copió de la pregunta de armonización normativa.

**Ricardo**

`[09:32]` Exacto. Luego, de hecho no sé si tengo el último cuestionario; ya no se ha modificado.

**Rubén**

`[09:43]` Sí, te acuerdas que hasta me dio nervio y dije «ay, no sé», dije «ya, bueno, te lo voy a mandar», y me dijiste «sí, de todos modos se puede».

**Ricardo**

`[09:49]` Ah, justo. Y estas son las cosas… creo que lo ideal es que tú las hagas, porque implica decisión. Algunas cosas son pendejadas, pero prefiero que esté en tu cancha.

**Rubén**

`[10:00]` No, y además hoy lo pidieron ya.

**Ricardo**

`[10:01]` Prefiero no tocarlo.

**Rubén**

`[10:04]` Está bien, porque es mi responsabilidad. Pero hoy ya creo que llegó al límite: ya pidieron el cuestionario.

**Ricardo**

`[10:12]` ¿Quieres que…? Mira, algo que puede ser muy rápido es que haga una exportación en el dashboard: se va a poder exportar la lista. Ya se puede editar, pero puedo exportarlo. Tú me lo mandaste en un formato, ¿te acuerdas?, de Word.

**Rubén**

`[10:46]` Sí, te lo mandé en Word.

**Ricardo**

`[10:49]` Lo tienes ahí para verlo, porque no me acuerdo cómo está; ya tiene mucho tiempo.

**Rubén**

`[11:40]` Ah, pero ya salió el PDF: no era Word, era PDF.

**Ricardo**

`[11:46]` No importa, PDF y Word da igual. Pero así son todas las preguntas: todas, todas, todas.

**Rubén**

`[12:29]` ¿Lo que no tiene es la armonización, la tablita?

**Ricardo**

`[12:41]` ¿Tablita de transversalización, no? De distintos…

**Rubén**

`[12:46]` Esta es la pregunta de instituciones; los criterios de la organización ya están adentro, con una tablita. Ese creo que también lo tenías.

**Ricardo**

`[12:54]` Ya lo tengo, sí. Yo tengo todo. Ese no es el documento final, sino es otro.

**Rubén**

`[12:59]` Esta es la lista final de preguntas.

**Ricardo**

`[13:24]` ¿Se lo mandas así o lo terminamos en corto? Es que yo me he atrasado, pero puedo trabajar durísimo el fin de semana y el lunes a primera hora lo checamos y se los mandamos, o ya que puedan contestar. Bueno, dijimos que el 10, ¿no? ¿El 10 de septiembre o qué día era que lo íbamos a abrir? El 25. Pero podemos abrir solo la parte de que vean las preguntas, sin que todavía puedan contestar: lo que habíamos platicado la otra vez.

**Rubén**

`[14:00]` Yo he manejado una retórica de «vamos por partes»: si no está verificada la información base, lo demás sale mal.

**Ricardo**

`[14:08]` Sí, pero ya estamos.

**Rubén**

`[14:09]` Pero ya me dijeron: «Sí te quiero dar la información base, pero a mí las áreas a las que les pido información no me dejan hacerles por separado las peticiones, o corro el riesgo de que ya no me den la información si pido un alcance y tal».

**Ricardo**

`[14:25]` Oye, ¿por qué no lo abrimos por zonas? La siguiente semana estoy tranquilo, porque ya acabé un observatorio de conflictos ambientales —el 9 de septiembre va a tener su presentación de informe, y había estado la verdad muy enfocado en eso—; entonces puedo dedicarme full para tenerlo y mandarlo. ¿Cómo les ha ido con lo de las preguntas generales?

**Rubén**

`[15:09]` Bien, ya como diez terminaron.

**Ricardo**

`[15:12]` ¿Y cómo les ha ido con la validación y los botones?

**Rubén**

`[15:16]` Es que apenas hoy fue la reunión; y ya tuve reunión con mis compañeras becarias, ya van a hacer la primera verificación el lunes.

**Ricardo**

`[15:25]` El lunes la información básica, creo que estaría bien. Es que, sabes qué, me sirvió mucho la reunión que tuve con Fer, donde me dio retroalimentación, ¿te acuerdas? Entonces siento que estaría bueno —no sé si el martes, no sé si el mismo lunes cuando se los mostremos— tener una sesión de trabajo para ver si ha funcionado, qué no, y poder hacer aclaraciones. Tú las capacitaste para esta cosa de cómo validar y no hubo dudas; lo que quiero es, como es algo que va a ser de muchos años, que quede lo más claro posible desde el principio.

**Rubén**

`[16:21]` Sí. Pues si quieres puedes terminar de montar el cuestionario, y de las instituciones que son de prueba yo les puedo pedir a ellas que suban información, que contesten. ¿Pero quieres que te den retroalimentación?

**Ricardo**

`[16:42]` De la parte de revisión.

**Rubén**

`[16:45]` De la parte de revisión, pero ahorita no están revisando. La información va por eso, pero no creo que te vaya…

**Ricardo**

`[16:56]` Pues Fer me dijo un montón de cosas muy buenas, entonces justo eso es como lo que…

**Rubén**

`[17:04]` Yo preferiría que terminemos.

**Ricardo**

`[17:06]` Está bien, terminamos el cuestionario ya. Entonces tú le echas un ojo a la estructura de lo que te acabo de enviar.

**Rubén**

`[17:26]` `[17:27]` Ah, de lo que me acabas de enviar.

`[17:34]` Sí, esta está muy bien; esta que encontraste yo la puedo corregir sin problema, la 4.1. Luego el 4.4 dice «a cuántas instancias académicas se consideró para este proceso»: sí tiene el mismo problema, es un copy-paste que luego no se ajustó.

**Ricardo**

`[17:56]` No hay ningún problema.

**Rubén**

`[17:57]` Yo lo puedo ajustar, ya vi cuál es el problema. Qué bien que lo viste.

**Ricardo**

`[18:04]` Lo vi yo y lo vio Claudio; son cosas ahí sí, y…

**Rubén**

`[18:08]` `[19:04]` `[19:06]` Es que yo no reviso esas preguntas porque, como son idénticas en estructura —no en contenido—, siempre que reviso nada más reviso lo que es diferente. Pero por eso se fue, justamente. Luego, «cuántas instancias académicas…»: este es «Políticas institucionales y académicas de inclusión y no discriminación». Ah, ya vi esta, la tengo que revisar. No sé si esto quedó en «académicas» porque nada más es para procesos académicos y las administrativas no tendrían relación, no me acuerdo. Luego este observable: la pregunta inicial no abre interrogación, le falta la…

**Ricardo**

`[19:24]` Sí, sí, sí, hay cosas que son una trivialidad, ¿no?

**Rubén**

`[19:30]` `[19:35]` `[19:38]` `[19:50]` Pero está bien. Tres formas distintas de «sexo y género» en el instrumento: con diagonal, con guion… Pues creo que es mejor con guion, lo vamos a estandarizar. Nueve observables tienen dos títulos distintos, uno en la lista de verificación y otro en el cuestionario.

**Ricardo**

`[19:50]` ¿Pero esto no es el nombre corto que habíamos hecho? Sí, creo que más bien… Pero me parece curioso que no todos. A ver, ¿cuántos son? Son nueve, dice, y son 40: entonces ¿por qué solo nueve de 40? Si es un nombre corto, ¿por qué es diferente? Aquí es nombre corto este y aquí no coincide, entonces…

**Rubén**

`[20:28]` Sí, me voy a tardar como un día, yo creo.

**Ricardo**

`[20:30]` Sí, sí, sí.

**Rubén**

`[20:33]` `[20:39]` «1.11: eliminó un fragmento que parecía una nota de trabajo, el sufijo "Características de los observables"».

**Ricardo**

`[20:42]` Sí, eso está bien. No todo tiene que… literal, yo la verdad ni siquiera. Sí, todo lo que hemos observado.

**Rubén**

`[20:59]` «Mujer, hombre» para persona titular; plantea «sexo y género». Ah, no se estudia…

**Ricardo**

`[21:07]` Bien. Lo que se puede modificar directo en el cuestionario desde el dashboard, pues se genera…

**Rubén**

`[21:15]` Tú no has montado todavía las preguntas, ¿verdad?

**Ricardo**

`[21:21]` ¿Para que lo vean las instituciones?

**Rubén**

`[21:23]` Para que tú lo veas; no, para ti, como parte del proceso de evaluación.

**Ricardo**

`[21:27]` Sí, ya están todas montadas.

**Rubén**

`[21:30]` Sí, solo lo tengo que corregir, más bien.

**Ricardo**

`[21:32]` `[21:39]` `[21:41]` Ahí en el dashboard, igualito: va a estar catálogos, y una por una. Van agrupados: eje, componente, observable…

**Rubén**

`[21:47]` Si ya la subiste, ¿qué te falta?

**Ricardo**

`[21:49]` `[21:55]` No, pero no están en el cuestionario; el cuestionario que contestan las instituciones.

**Rubén**

`[21:55]` Te falta programar el despliegue para que aparezcan como cuestionario.

**Ricardo**

`[22:03]` Pero bueno, esto es lo único para cerrar ya el cuestionario y poderlo mostrar. Y lo que yo puedo hacer es programar que no se pueda responder todavía hasta el 25. Bueno, más bien: si lo podemos abrir antes, pues que se abra. Creo que no hay ningún impedimento para abrirlo antes del 25, ¿o sí?

**Rubén**

`[22:30]` Pues tú ya un poco viste cómo es: sí se necesita mucho acompañamiento, porque…

**Ricardo**

`[22:38]` OK. Lo pregunto porque creo que lo ideal… Más bien, no tengo muy claro cómo les vamos a mostrar. ¿Cuál es la mejor forma de mostrarles ya todas las preguntas a las instituciones? Yo creo que la mejor forma es ya en la plataforma.

**Rubén**

`[22:59]` Así lo hemos hecho siempre: hacemos una presentación.

**Ricardo**

`[23:04]` ¿Cuándo es la próxima reunión? Pero ya te la están pidiendo. ¿Pero no es mucho tiempo de aquí al 25?

**Rubén**

`[23:16]` Sí, ese día cumplimos con llegar ya con el cuestionario montado.

**Ricardo**

`[23:20]` Aunque te estén presionando de aquí al 25.

**Rubén**

`[23:25]` Porque el compromiso fue mandarles el cuestionario completo.

**Ricardo**

`[23:28]` Ah, bueno, el documento. Pero eso puede ser antes de que esté en la plataforma.

**Rubén**

`[23:38]` Sí, porque incluso lo necesitan antes de la plataforma. Claro, porque tienen que pedirle la información a las áreas.

**Ricardo**

`[23:46]` Mira, eso es algo en lo que yo no voy a tardar nada, porque literal le digo a Claudio: «Haz un Word; estas preguntas conviértelas a un Word», y tú le das formato como este Word. Entonces, para que la fuente siempre sea la fuente: lo que esté en el dashboard.

**Rubén**

`[24:16]` Yo creo que hay que generar una especie de documento que se llame «Cuestionario final final», y ya con los errores que tenga, ni modo, que se quede —obviamente vamos a corregir todo lo que tú ya encontraste—. Y con base en ese documento nada más me explicas cómo entrar a corregir, corrijo, y tú ya con eso publicas. Pero mientras tanto tienes algunas cosas que programar.

**Ricardo**

`[24:49]` ¿Para que te enseñe dónde son las preguntas?

**Rubén**

`[24:54]` No, me refiero a que tienes una parte de chamba todavía para mandar el guacho, para que sea visible para los…

**Ricardo**

`[25:11]` Pero puedo hacer mientras una exportación del Word: tú editas, y en cualquier momento agrega un botón para descargar todo el cuestionario. Es que si no, ¿cómo le compartes el cuestionario a las…? O se lo compartes ya que esté editable. Tengo los cuestionarios, pero si vas a hacer cambios…

**Rubén**

`[25:44]` Claro, porque yo los haría en el Word en función de tus comentarios, y en el dashboard.

**Ricardo**

`[25:55]` `[26:10]` `[26:13]` Ah, es que lo que yo te decía es al revés: que ya no edites nada en Word, que tú lo edites en el dashboard y agregas un botón de exportación de Excel a Word; y entonces el Word ya no hace formato, entonces ya no tienes que editar en dos lados, y la fuente, la única fuente, el único lugar donde está…

**Rubén**

`[26:24]` Yo no lo digo por aquí, lo digo porque otras veces exporto cosas de plataformas y es media hora estar poniéndoles espacios.

**Ricardo**

`[26:35]` Le ponemos un diseño bonito; de hecho puedo seguir el lineamiento de lo que me enseñaste, de lo que mencionaste. Esto lo puedo programar… yo no lo voy a hacer; bueno, sí lo voy a hacer porque voy a coordinarlo, pero es algo que me va a tomar una hora, y esa hora creo que vale la pena para que ya no…

**Rubén**

`[26:35]` `[27:03]` Sí, porque ahí cualquier ajuste ya nada más es descargar, ya, dos, tres.

**Ricardo**

`[27:08]` `[27:13]` Incluso esa descarga podría estar en la plataforma también pública; estaría muy bien, porque así pueden descargar el cuestionario y ya no depende de que se los pases.

**Rubén**

`[27:13]` Porque todo hoy me lo volvieron a pedir. Y además a veces me dicen cosas como «no me mandaste…» —una cosa es «no me llegó»—, pero siento que mala onda que te digan esas cosas después de tantas veces.

**Ricardo**

`[27:37]` Podría, justo: como si la respuesta siempre es en la plataforma, entonces vamos generando ahí un pequeño espacio donde podamos subir cosillas.

**Rubén**

`[27:49]` ¿Por qué?

**Ricardo**

`[27:51]` Porque podemos agregar un botón que diga «Documentos» y que tú puedas ir subiendo los documentos.

**Rubén**

`[27:58]` Sí, es que por más que tratamos de generar acuerdos, de hacer todo con tiempo… ¿Cuántos meses llevamos con esto? Como dos años. Y aun así…

**Ricardo**

`[28:10]` Eso te puede ayudar, justo como ya está ahí. La forma que he descubierto que funciona con las organizaciones, con los usuarios, es que les dices «a ver, ¿qué necesitas?, búscame; si lo que necesitas no está ahí…»; si está ahí, todo está en la plataforma, y entonces ya la respuesta es «ya no tengo que enviar el correo, ni que buscar el archivo». Creo que eso puede. Ahora, creo que lo que acabo de decir sí es diferente a la generación del Word, porque por mucho que le ponga estilos, puede ser que haya dos, tres cosas que todavía le tengas que modificar.

**Rubén**

`[29:01]` ¿Te acuerdas lo que habíamos dicho? Tratemos de que no trabajes más de lo que ya cotizaste.

**Ricardo**

`[29:06]` Sí, está bien. Por eso digo que yo no voy a hacer que sea… pero si hay algo que modificar, pues ya lo modificas tú, pero que tenga ya. Ahora, este PDF estaba basado en un Word: ¿me puedes pasar el Word?

**Rubén**

`[29:39]` ¿Qué nos toca hacer en paralelo al observatorio? El observatorio es uno de seis proyectos; son todos los proyectos, y los doratos no aparecen.

**Ricardo**

`[30:04]` Es que además te avientan y te avientan cosas. Te tengo que enseñar a Claudio para que te ayude; güey, está muy cabrón.

**Rubén**

`[30:15]` Un día vamos a ver. Este es compulsivo.

**Ricardo**

`[30:20]` ¿Y qué es?

**Rubén**

`[30:22]` `[30:25]` `[30:28]` ¿Cuál necesitas? Creo que es el que quieres, mira. Es el que quieres, ¿verdad? En Word, ¿verdad?

**Ricardo**

`[30:34]` Viste, ahí dice «maqueta», justo; pero ese no está completo, completo, solo son… Ah, ya sé, «complete».

**Rubén**

`[30:47]` Es el que quieres, ¿verdad? En Word, ¿verdad?

**Ricardo**

`[30:54]` Es que ya todo lo registro: de todo hay un registro documental. Entonces mira, espero que no te ofenda…

**Rubén**

`[31:08]` Tienes que hablarle con honestidad.

**Ricardo**

`[31:10]` No, más bien estoy diciendo que yo voy a ser honesto contigo de qué he acabado y qué no. ¿Ya viste? Yo no tengo memoria en cosas, porque todo se guarda en un lugar muy específico. Entonces, cuando avanzo, le puedo decir «quiero trabajar este tema que no hemos trabajado, ¿con qué está conectado?, no sé qué tengo que hacer antes», y me responde «antes de esto tienes pendiente esta cosa, y esto, y esto». Lo vamos resolviendo. Es como si tuvieras un asistente súper inteligente. Yo pago 1 700 euros.

**Rubén**

`[31:57]` No, es que tú…

**Ricardo**

`[32:01]` Todos lo necesitamos más de lo que pensamos.

**Rubén**

`[32:04]` Sí, pero yo tengo cinco compañeros.

**Ricardo**

`[32:06]` El de ChatGPT hay de 400; 400 es algo viable. También Claudio, pero Claudio no es muy eficiente. Ya tiene una cosa que se llama Codex.

**Rubén**

`[32:23]` ChatGPT.

**Ricardo**

`[32:26]` Pero es que esto es otro pedo. Esto es una dinámica de trabajo donde vas dialogando, y tiene toda la información, y vas resolviendo varias cosas. Más bien, voy a hacer un tallado. ¿Y qué más? A ver, déjame.

**Rubén**

`[32:26]` `[32:48]` Justo ahorita el tema sería que pudieras… Ya te mandé el cuestionario; que pudieras mandarlo a que fuera visible para las de prueba. En las pruebas lo vemos con base en lo que tú me des, y se lo voy a pasar también a mis compañeras. Si encuentran algo hacemos correcciones, descargamos, y ya con base en eso nada más toca avisarles a las IES que ya está listo.

**Ricardo**

`[33:16]` OK.

**Rubén**

`[33:18]` Sí, creo que la parte en la que nos quedamos, que tú ya estabas ideando, era cómo le ibas a hacer para que aparezca. Yo te diría que eso es lo más indispensable. ¿Y por qué es crucial? Porque yo sé que se van a súper espantar cuando vean el tamaño. Las conozco muy bien.

**Ricardo**

`[33:42]` Entonces no les vas a mandar el PDF.

**Rubén**

`[33:45]` Podríamos mandarlo después de que verifiquemos.

**Ricardo**

`[33:49]` Junto con la plataforma, aunque no estén abiertas, para que vean.

**Rubén**

`[33:54]` No importa que tarde a la semana que viene. ¿Por qué? Porque si yo les mando un cuestionario y luego contigo hacemos uno que corrige errores, les voy a tener que decir «oigan, hicimos unos ajustes, por favor no le hagan caso al anterior», y se van a empezar a revolver versiones, y no, no, no. Entonces, a ver, déjame anotarlo para consultar. El orden va a ser el siguiente: uno, le mando a Ricardo el cuestionario —ya te lo mandé—. Dos, yo corrijo en plataforma.

**Ricardo**

`[34:37]` Sí, ahorita te enseño dónde se corrige.

**Rubén**

`[34:41]` Tres, Ricardo programa la exportación. Cuatro, exportamos, y es el cuestionario final.

**Ricardo**

`[35:01]` Voy a ponerle formato a medias. Formato a medias es algo no crudo, crudo, que tengas que…, sino algo en lo que ya des pocas ediciones de tu parte; la parte fina, para no tardarme yo haciéndola, sino que sea algo muy automatizado, como «Claudio, ayúdame, toma este Word y ayúdame».

**Rubén**

`[35:25]` `[35:52]` Y cinco, sería que tú alistas la estrategia de listado y despliegue de los observables y las preguntas.

`[36:06]` El reto acá —tú ya lo tienes súper claro— es que las IES puedan interactuar primero con un menú bastante compacto. Obvio, ya vemos: si les da curiosidad y te dicen «no sé a qué se refiere con esto», le pueden dar clic y decir «bueno, aquí me están preguntando, no sé, cuidados, y yo pienso que no, pero le abro y tengo una sala de lactancia, entonces sí». Pero que de entrada puedan tener algo muy compacto; y que si dicen «de cuidados no, y sé que no tengo sala, no tengo nada, mejor no», desde el principio ya se van a ahorrar un montón de trabajo. Entonces, que puedan interactuar desde…

**Ricardo**

`[36:51]` `[37:07]` OK, eso lo puedo tener: puedo meterle full el domingo. Sí, el sábado, domingo; puedo hacer este fin de semana bastante labor para completar eso.

**Rubén**

`[37:07]` Sí, estaría muy bueno. ¿Y nos podríamos reunir, si quieres, jueves o viernes de la próxima semana, o miércoles? El martes y miércoles vamos a estar a full con lo de la clausura del diplomado.

**Ricardo**

`[37:22]` Ah, va, entonces el jueves… que va a estar muy grande el jueves.

**Rubén**

`[37:27]` Y el jueves ya voy a estar libre.

**Ricardo**

`[37:29]` Y si quieres —si van a empezar a revisar las preguntas generales, si hay alguna duda de tu equipo—, no sé, ¿quieres que me meta? Yo sé que tú no quieres que haga eso, pero yo sí quiero ir mejorando la plataforma para que sea usable, y el mejor momento es cuando la empiecen a usar, ¿no?

**Rubén**

`[37:51]` Sí, hagámoslo. Pero ¿te parece, cerramos esto?

**Ricardo**

`[37:53]` Sí.

**Rubén**

`[37:54]` Y ahí ellas ya también van a haber cogido un poco más de experiencia; apenas están empezando a revisar.

**Ricardo**

`[38:01]` ¿Tú cuándo vas a revisar estos textos?

**Rubén**

`[38:05]` Creo que es mejor que sea viernes.

**Ricardo**

`[38:07]` Para que yo lo haga el jueves. ¿Tú hasta el jueves? ¿Ya viste? Es muy poquito.

**Rubén**

`[38:14]` Sí, es más por lo que tengo encima; es mucha logística, en serio.

**Ricardo**

`[38:14]` ¿El otro evento?

**Rubén**

`[38:14]` No, esto sé que no lo voy a hacer.

**Ricardo**

`[38:27]` `[38:32]` ¿Quieres que te diga nada más dónde encuentras?

**Rubén**

`[38:32]` Sí. De hecho es posible que el jueves que nos veamos, si no alcanzo, no tenga listo eso; pero podemos ver lo que tú avanzaste, y yo le daría prioridad a más tardar el viernes o el lunes, para que ya esté listo el sondeo. Pero bueno, veamos esto. Y mira, dice lo que me dijiste de en dos navegadores.

**Ricardo**

`[38:58]` ¿Y por qué usas Netlify? ¿Por qué no usas onigies.unam.mx?

**Rubén**

`[39:06]` Porque sí, siempre entro a este, ya me acostumbré, ya está guardado, nomás pongo la O y se pone.

**Ricardo**

`[39:13]` Está bien, está bien.

**Rubén**

`[39:14]` ¿Estás aquí en gestión de catálogos, no? Preguntas base, no.

**Ricardo**

`[39:29]` `[40:15]` Entonces, si te vas a componente, abres uno y ahí se edita el nombre del componente, y ahí abajo están los observables. Perdón, creo que no subí la última parte, déjame subirla… Observables… Perdón, algo me falta ahí, ponerte esto, pero bueno, ahí va a estar. En eje vas a poder ver los componentes, y de los componentes vas a poder ver los observables, y de los observables… va a estar todo anidado.

**Rubén**

`[40:13]` Aquí me va a aparecer la redacción, y nada más llevo…

`[40:23]` Y puedo cambiar el título y la redacción.

**Ricardo**

`[40:27]` Todas estas cosas que están aquí habrían de estar editables.

**Rubén**

`[40:35]` `[40:36]` Entonces ahí también lo anoto.

**Ricardo**

`[40:36]` `[40:39]` Eso lo subo, porque ya lo tenía y no voy a ponerlo hasta mandar…

**Rubén**

`[40:39]` ¿Y cuándo ya sacas a producción?

**Ricardo**

`[40:48]` Deploy, subir a producción, despliegue a producción. En catálogos, y ahí va.

**Rubén**

`[41:08]` Sí, porque en ese yo trabajaría.

**Ricardo**

`[41:12]` ¿Qué más nos falta? Creo que eso es todo, ¿no? Sí, la reunión de Cómputo UNAM.

**Rubén**

`[41:24]` `[41:34]` Ni siquiera lo he cuestionado. ¿Y si grabas la reunión, se genera una tarea?

**Ricardo**

`[41:34]` La tarea ya está generada, mira: dice «task-102, reunión con Cómputo UNAM», gestionando…

**Rubén**

`[41:43]` No, pero lo que te pregunto es: cuando tú grabes la reunión, Patricia… ¿cómo se llama?

**Ricardo**

`[41:49]` Claudio.

**Rubén**

`[41:54]` Claudio sabe que tiene que agarrar esa grabación. O sea, yo le digo…

**Ricardo**

`[42:00]` `[42:29]` `[42:33]` «Esta es la grabación de la última reunión». Y por cada hora de reunión yo necesito como 20 minutos de detalle: tengo un diálogo para aclarar las cosas, y luego esas cosas se convierten en tareas, o las tareas que ya existían se actualizan, se vinculan; se ponen decisiones. Son tareas, decisiones y documentos, entonces todo se va guardando. Todo se va guardando automáticamente, entonces ya no tengo que estar… Ahorita hago la sesión de cierre de esta madre: le paso el audio, le digo «oye, está este audio, actualizamos las tareas», tengo un diálogo, tengo una metodología para actualizar, unas instrucciones. Y después, cuando empiezo a trabajar, le digo «¿qué es lo siguiente que tengo que hacer?». Así literal. Me da la lista, me la da por grupos, y le digo «OK, vamos a trabajar este grupo ahorita», y luego «¿qué otra cosa pendiente?». Entonces ya no llevo el registro: mis anotaciones ya no importan. Y el tema es que estas más se pierden; entonces es muy difícil para mí abrir esta cosa, y es muy fácil preguntarle a Claudio «Claudio, ¿qué tengo pendiente?» y empezar a hacerlo.

> **Nota editorial (2026-09-11, aclaración de Ricardo).** Lo que sigue, de `[43:46]` a `[44:23]`, **no es de ONIGIES sino de STIG** —otro proyecto del mismo cliente, la CIGU, con repo propio en `~/dev/unam/stig`, completamente independiente de este—. La máquina virtual migrada, la reunión con DGTIC, la solicitud de Pati y «Azul» pertenecen a ese proyecto; Ricardo los trajo como contexto de los pasos que siguen. **Para ONIGIES la reunión con Cómputo UNAM no ha ocurrido** —es justo lo que Rubén dice en `[41:24]`, «ni siquiera lo he cuestionado»— y faltan varias cosas antes de avanzar con el servidor de la UNAM. Sí son de ONIGIES `[41:12]`–`[41:34]` y `[45:12]`–`[45:55]`: la vía del ticket por la persona recién llegada, el vínculo que a Rubén le falta crear y el hecho de que los datos viven hoy en el servidor de Ricardo. No se alteró nada de lo dicho.

**Rubén**

`[43:42]` `[43:46]` `[43:53]` ¿El stick ya quedó lista la parte esta de la computadora virtual, hicieron la migración?

**Ricardo**

`[43:53]` Ya, pero falta que hagan las pruebas de seguridad. Eso es lo que tenía duda, de que tenemos que mandar… Tuvimos una reunión con DGTIC.

**Rubén**

`[44:12]` Y estuvo… ¿estuvo Pati? No, Patricia. Ah, no, pero tú me habías dicho que ella hizo la solicitud, ¿no?

**Ricardo**

`[44:22]` ¿Había hecho una solicitud?

**Rubén**

`[44:23]` Ajá, es que en Azul trabajaba con ella, con Pati.

**Ricardo**

`[45:12]` Ahora, tú puedes… Mira, puedes preguntarle de una vez a este muchachito.

**Rubén**

`[45:21]` Todavía me falta crear ese vínculo.

**Ricardo**

`[45:24]` Ah, pero puedo decirle, oye…

**Rubén**

`[45:29]` `[45:30]` Es que apenas acaba casi de entrar.

**Ricardo**

`[45:33]` Él nos puede ayudar a hacer la apertura del ticket. Eso es importante, mientras corre en mi servidor y yo hago un puente y así.

**Rubén**

`[45:49]` Sí, pero no… está bien, pero la…

**Ricardo**

`[45:51]` La información está en mi servidor.

**Rubén**

`[45:53]` Sí, bueno, confío en ti.

**Ricardo**

`[45:55]` Pero de todos modos es lo adecuado. La van a hacer de pedo en algún momento con el tema; no pasa nada, pero no porque la información no esté segura, solo porque la pueden hacer de tos.

**Rubén**

`[46:05]` Sí, por esta cosa de… Está bien. ¿Quién tiene los datos? De hecho, por eso usamos este correo de Outlook: porque dicen que el de Google no sé qué tiene, pero que parece como que la información se almacena en no sé qué lugar, como que es de la empresa y no de la universidad. Yo no entiendo esas cosas, pero por esa razón usamos este servicio.

**Ricardo**

`[47:23]` Y hay otros criterios que todavía no sé si ya están definidos, no me acuerdo, como lo del 0 al 10 o del 0 al 5: cuánto va a pesar cada cosita. Ahora, lo que yo puedo hacer es que en estos observables y componentes cada uno tenga su peso y aquí lo puedas editar; pero es algo que hay que decidir, y no sé si lo van a preguntar ellas, las instituciones, de cuánto pesa cada cosa y cómo se va a medir eso. Siento que es una discusión metodológica importante.

**Rubén**

`[47:51]` `[48:04]` `[48:08]` `[48:29]` Que tenemos pendiente, sí; es que no hemos definido. Yo soy de subirlo al 10; mi intuición me dice que, para diferenciarlo del anterior, porque si lo dejas de 0 al 5 todas van a sacar puntos más bajos, eso es obvio. ¿Y qué te van a decir? «Bajé». Y lo que tenemos que responder es «no bajaste, porque no es la misma metodología, no estás midiendo lo mismo; quizás con la metodología anterior subirías». Entonces creo que es mejor tener una de 0 a 10 **[nota de limpia: el pipeline transcribió «de 0 a 5», que contradecía todo el párrafo; Ricardo, de memoria, el 2026-09-11: dijo «de 0 a 10», declarada definitiva]**. Además, si antes sacabas 3 y ahora sacas 3, se siente tan feo. Es que es 3 de 0 al 5 y 3 de 0 al 10, pero siento que la carga psicológica se puede matizar con eso. Una escala del 0 al 10 creo que es más común a las métricas universitarias, por lo general se evalúa en esos rangos. Y lo que habíamos hablado con Isabela, que a mí me pareció bien —fue una propuesta de ellas—, es que quizás lo mejor, para no meternos en ese rollo de tener que justificar que vale 3, que vale 2, que vale tal, es que todo valiera lo mismo en términos de observables.

**Ricardo**

`[49:11]` Sí, eso creo que sí es lo que ha sucedido durante todo este año; no hay problema. Pero lo que me preocupa es: hay preguntas de transversalización, otras de institucionalización, otras de planes; hay preguntas específicas. ¿Eso cómo, cuánto vale cada cosa? Porque depende también del indicador. Tenemos tres tipos de preguntas: hay unas que tienen solo una —bueno, todos tienen dos, institucionalización y transversalización—, pero hay otras, como las de planes.

**Rubén**

`[49:47]` Yo creo que sí tendríamos que definir el peso interno; ahí no sé si puedes ir pensando. Pero pensaba… pues hay que hacer un análisis, le tengo que preguntar a otras personas, tener muchas visiones; pero no sé si se vuelve muy relajo que todo sea promedio al interior, que valga lo mismo la transversalidad que la institucionalización. El tema es que son…

**Ricardo**

`[50:21]` Sí, pero es que hay más preguntas que solo transversalidad; hay otro tipo de preguntas. No, esas son de institucionalización: armonización es una y luego institucionalización es otra. Pero hay otros tipos de preguntas: hay unas en las que se pregunta cuál es la distribución de género, o por ejemplo los planes de estudio, ¿cuántos planes de estudio conciliaron? Y entonces ahí…

**Rubén**

`[50:54]` Creo que ahorita, hasta este nivel, lo que me da tranquilidad es que la idea es que si cada observable vale 10, internamente…

**Ricardo**

`[51:11]` Sí, está bien, eso no hay problema.

**Rubén**

`[51:13]` Hasta ahí creo que vamos tranquilos. Ahora, internamente pues tengo que revisar.

**Ricardo**

`[51:19]` Lo voy a poner aquí también. Eso no es parte de lo que estaba editable en observables, pero voy a poner un campito. Ahora, hay una calificación: tú puedes tener un default para institucionalización y transversalización. Ese no hay ningún lugar donde se pueda editar todavía, tengo que pensar dónde. Y si tú dices que pese siempre… antes lo que teníamos era 3 y 2, no sé si te acuerdas.

**Rubén**

`[51:53]` `[51:56]` Y había unos que valían 5 porque no había transversalización.

**Ricardo**

`[51:56]` Entonces lo ideal es que haya un default que sea para los 41 observables, y que algunos observables —sobre todo los que tienen una lógica distinta— los puedas personalizar; que no tengas que personalizar uno por uno, sino que tengas un default, y si modificas ese default, es el que se comporta diferente al default general.

**Rubén**

`[52:25]` `[52:36]` `[52:39]` Y el default no tendría problemas si, por ejemplo, en los criterios de institucionalización —que es armonización— hay más o menos elementos, ¿verdad? Ya viste que en institucionalización luego viene una batería: dice, por ejemplo, cómo se institucionalizó esta política, se aprobó, y tiene criterios, y cada uno es uno solito; y este default no importa, porque hay tablitas que tienen cinco, otras cuatro.

**Ricardo**

`[52:36]` Se ajustaría otra vez.

`[52:53]` Ah, no, pero eso siempre el default…

**Rubén**

`[52:56]` Les promedia; esos sí ya…

**Ricardo**

`[52:58]` No me meto. Yo no haría que esos valieran diferente, porque sería demasiado difícil de mantener.

**Rubén**

`[53:03]` `[53:32]` No, no, no; y además no hay criterio, lo mejor siempre es promediado. De hecho así lo hicimos metodológicamente, pensando una jerarquía entre ellos: «esto vale 2»… No, no, todos valen lo mismo. El valor de institucionalización con armonización es el promedio de sus elementos. Pero lo que no hemos definido es si institucionalización vale algo distinto que transversalidad y que las otras preguntas, que son específicas.

**Ricardo**

`[53:32]` Eso no tenemos que resolverlo ahorita, pero lo ideal es que destinemos un día para conversar eso; es algo que está bien tenerlo presente.

**Rubén**

`[53:50]` Me dieron el contacto de una consultora para preguntarle; es muy buena. Lo que me dijo es que no había realmente como un canon: todo es nada más tomar la decisión, dejarla metodológicamente sentada y argumentar un grado de razonabilidad. Entonces, en realidad es lo que siempre hago: hacer las cosas con seriedad, no definir al azar el criterio, sino hacerlo por una razón, esa razón escribirla y argumentar.

**Ricardo**

`[54:34]` Sí, yo coincido. Bueno, yo puedo también decir los indicadores.

**Rubén**

`[54:34]` `[54:40]` Y sí le pregunté, le dije «oye, pero ¿hay un consenso a nivel regional en la CEPAL?».

**Ricardo**

`[54:45]` Ah, pero ¿de género en específico?

**Rubén**

`[54:45]` `[54:48]` `[55:08]` Ella sabe en general, y en género en particular: se ha dedicado a estadísticas para indicadores en organismos internacionales, trabaja en ONU Mujeres. Y me dijo: hay índices de 0 al 5, hay índices de 0 al 3 —no sé por qué—, hay índices de 5 al 10, hay índices de 0 al 4, hay unos que son porcentajes, hay otros que son…

**Ricardo**

`[55:08]` Sí, eso es cada quien. Y lo que sí es que hay diferentes metodologías. Por ejemplo, esta es la metodología de «al menos»: si no tienes al menos una, eso es como un índice de carencia. No solo existen los promedios, sino también los índices de carencia, los indicadores de carencia: si no cumples ninguno de estos cinco, entonces…, o si cumples dos de cinco. Por ejemplo, CONEVAL es así. Pero yo creo que no tiene sentido hacer eso, porque complicaría hacerlo lo más simple. ¿Y la última pregunta es: tuteamos o ustedeamos?

**Rubén**

`[56:02]` `[56:09]` Así lo vi en el comentario. Sí.

**Ricardo**

`[56:12]` `[56:13]` Yo no conozco ninguna plataforma que use «usted».

**Rubén**

`[56:13]` Pero es que está en tercera persona la IES, no sé; pero tú, que trabajas en la IES, ¿piensas que…?

**Ricardo**

`[56:27]` Pero por ejemplo, cuando eliminas: «¿Estás seguro de eliminar?».

**Rubén**

`[56:32]` Ahí sí puedes tutear, porque ahí lo que estás diciendo es… No, es una pregunta de cuestiones, no una pregunta de formulario.

**Ricardo**

`[56:39]` No, las del cuestionario sí tienen que estar en tercera persona; pero yo me refiero a los mensajes de la plataforma, y sobre todo a la parte que tiene que ver con los estatus.

**Rubén**

`[56:49]` Están todas en…

**Ricardo**

`[56:50]` Está bien en «tú».

**Rubén**

`[56:52]` Todas están en «tú» y se ven re bien. Sí, ya la gente se acostumbró a usarlo así.

**Ricardo**

`[56:58]` Es que eso es algo que notó Clau, no es algo que yo haya notado. Me dijo: «Hay cosas en "tú" y hay cosas en "usted"». O más bien, me propusieron la redacción de «usted» y le dije «cámbialo a tú», y me dice «no, pero hay unas cosas en usted y en tú», no sé. Bueno, pues muy bien, creo que es todo.

**Rubén**

`[57:18]` Muy bien, ¿qué vamos a hacer? ¿Qué tengo que hacer?

---

## Dudas de lectura

Lo que no quedó resuelto al limpiar. Cada entrada lleva el timestamp, el fragmento como salió del pipeline, las lecturas posibles y qué cambia con cada una.

### Sin resolver — las decide Ricardo

**1. `[48:08]` — RESUELTA el 2026-09-11: Rubén dijo «de 0 a 10».** El pipeline transcribió «entonces creo que es mejor tener una de 0 a 5», que contradecía todo el párrafo —abre con «yo soy de subirlo al 10» y sigue con «una escala del 0 al 10 creo que es más común a las métricas universitarias»—. **Ricardo, de memoria, el 2026-09-11, fijó «de 0 a 10» y la declaró definitiva**; la limpia lleva la frase corregida y su nota, la cruda conserva lo que salió del pipeline. La escala quedó fijada en [[adr-0016]].

**2. `[19:50]` vs `[51:56]` — ¿40 o 41 observables?** Ricardo dice «son nueve, dice, y son 40» en `[19:50]`, y «un default que sea para los 41 observables» en `[51:56]`. Ambas conservadas tal cual. Qué cambia: el denominador de los nueve observables con doble título. No la resolví: es dato del instrumento, no de la transcripción.

**3. `[31:10]` — «Yo pago 1 700 euros».** Cifra conservada literal. Lecturas: (a) es la cifra correcta; (b) el pipeline oyó «euros» donde se dijo «pesos», o alteró el monto. No tengo nada en el audio que la respalde ni que la desmienta, y la regla es que las cifras se conservan.

**4. `[56:32]` — «es una pregunta de cuestiones, no una pregunta de formulario».** Fragmento incoherente tal cual. Lecturas: (a) «es una pregunta de la plataforma, no una pregunta del cuestionario» —Rubén distinguiría el mensaje de interfaz, que sí se tutea, de la pregunta del instrumento, que va en tercera persona—; (b) lo contrario. Qué cambia: cuál de las dos superficies lleva tuteo. Conservado literal; mi lectura preferida es (a), por coherencia con lo que Ricardo responde inmediatamente en `[56:39]`.

**5. `[13:24]` — «dijimos que el 10, ¿no? ¿El 10 de septiembre o qué día era que lo íbamos a abrir? El 25».** Dos fechas en la misma frase. El pipeline lo puso entero en boca de Ricardo. Lecturas: (a) Ricardo se corrige solo; (b) el «25» es una interjección de Rubén que el alineador absorbió. Qué cambia: nada operativo —el resto de la reunión confirma el 25—, pero sí quién tiene la fecha en la cabeza. Lo dejé como lo dio el pipeline.

### Fragmentos no recuperables — conservados literales

**Frases truncadas — pendientes de que Ricardo complete la idea.** Se cortaron a media idea en el audio; no se interpretan.

**T1. `[24:54]`** — «No, me refiero a que tienes una parte de chamba todavía para mandar el guacho, para que sea visible para los…». Truncada; pendiente de que Ricardo complete la idea (qué falta para hacer visible el cuestionario).

**T2. `[49:47]`** — «Yo creo que sí tendríamos que definir el peso interno […] no sé si se vuelve muy relajo que todo sea promedio al interior, que valga lo mismo la transversalidad que la institucionalización. El tema es que son…». Truncada; pendiente de que Ricardo complete la idea (la razón por la que promediar al interior podría ser un relajo).

**T3. `[50:54]`** — «Creo que ahorita, hasta este nivel, lo que me da tranquilidad es que la idea es que si cada observable vale 10, internamente…». Truncada; pendiente de que Ricardo complete la idea (qué pasa internamente si cada observable vale 10).


**6. `[24:54]`** — «tienes una parte de chamba todavía para mandar el guacho, para que sea visible para los…». «El guacho» no se resuelve por contexto.

**7. `[29:39]`** — «son todos los proyectos, y los doratos no aparecen».

**8. `[32:26]`** — «Más bien, voy a hacer un tallado».

**9. `[43:46]`** — «¿El stick ya quedó lista la parte esta de la computadora virtual…?». Mi lectura: «El stick» es basura de alineación y la pregunta arranca en «¿Ya quedó lista…?». No lo corté porque no es seguro.

**10. `[45:33]`** — «mientras corre en mis y yo hago un puente». Escribí «mientras corre en mi servidor y yo hago un puente», porque en `[45:51]` Ricardo dice justamente que la información está en su servidor. Es una interpolación mía sobre un fragmento roto.

### Resueltas por contexto, con el cómo

**11. `[04:39]` «las BO» → «las BP».** Por `[03:14]`, donde Ricardo acaba de hablar del módulo de buenas prácticas.

**12. `[41:34]` «task 102 reunión con la IBA» → «task-102, reunión con Cómputo UNAM».** Verificado **leyendo** el nodo `task-102` del grafo —«Reunión con Cómputo UNAM: procedimiento, dominio y capacidad de disco»—; no lo modifiqué.

**13. `[32:06]` «códecs» → «Codex».** Herramienta de OpenAI, en una frase sobre planes de ChatGPT.

**14. `[50:21]` «estabilización» → «institucionalización»** y **`[51:19]` «visualización» → «institucionalización»**. Ambas en enumeraciones donde el par opuesto es «transversalización», y el vocabulario del instrumento solo tiene «institucionalización».

**15. `[47:23]` «estos observadores y componentes» → «observables».**

**16. `[21:55]` «te falta programar las soluciones para que desaparezca como cuestionario» → «te falta programar el despliegue para que aparezcan como cuestionario».** La lectura literal —«desaparezca»— invertiría lo que Rubén pide en toda la reunión (`[33:18]`, «cómo le ibas a hacer para que aparezca», y `[35:25]`, «la estrategia de listado y despliegue»).

**17. `[09:49]` «prefiero que esté en tu contra» → «prefiero que esté en tu cancha».** Ricardo está diciendo que la corrección del texto le toca a Rubén porque implica decisión; «en tu contra» no tiene lectura coherente.

**18. `[14:25]` «¿por qué no lo abrimos a zonas possible?» → «¿por qué no lo abrimos por zonas?».**

**19. `[28:10]` «todo es el pelo en la plataforma» → «todo está en la plataforma».**

**20. `[37:29]` «¿quieres que me juegue?» → «¿quieres que me meta?»**, y **`[38:01]` «estas texturas» → «estos textos»**.

**21. `[40:27]` «habrían de estar editadas» → «editables»**, y **`[42:00]` «no se ponen decisiones» → «se ponen decisiones»** —la frase siguiente enumera «tareas, decisiones y documentos»—.

**22. `[26:10]` «un botón de exportación de Excel a Word».** Conservado literal. El objeto que se exporta es el cuestionario del dashboard, no una hoja de cálculo; «de Excel» es casi seguro ruido, pero como es una frase sobre el formato de salida preferí no tocarla.

---
type: task
id: task-173
title: Analizar a fondo las ideas metodológicas de la reunión del 23 de septiembre
state: open
date: 2026-09-23
owner: ricardo
parent: "[[task-5]]"
source: ["[[2026-09-23-reunion-ruben]]"]
related: ["[[task-15]]", "[[task-28]]", "[[task-111]]", "[[task-165]]", "[[task-32]]", "[[adr-0014]]", "[[adr-0015]]", "[[adr-0016]]", "[[adr-0017]]", "[[adr-0019]]"]
---

# Analizar a fondo las ideas metodológicas de la reunión del 23 de septiembre

Propuesta de Ricardo en el triage de la reunión del 23 de septiembre ([[2026-09-23-reunion-ruben]]): la parte metodológica de la reunión —casi la mitad del audio— no se resuelve con líneas sueltas en cada task, sino en un análisis conjunto. Aquí queda todo lo que se dijo, con sus timestamps, para que ese análisis no tenga que volver al audio. Nada de esto está decidido; donde Ricardo y Rubén parecieron acordar algo, va como candidato a ADR en (h).

Enlaces de contexto: los pesos ([[task-15]], [[adr-0014]], [[adr-0015]]), la agregación ([[task-28]], [[adr-0016]]), la paridad del 1.7 ([[task-111]]), la agenda con Rubén ([[task-165]]), el «No» que vale cero ([[adr-0017]]) y la revisión por eje ([[adr-0019]]).

## Reunión con Rubén, 2026-09-23

### (a) El dictamen de la revisora: «no cumple» y «parcialmente»

**De dónde sale.** Rubén, `[53:38]`: «puede pasar que sí tenga algo, pero que, por diseño metodológico, no coincida con ninguna de las variables del cuadrito […] Por ejemplo, no una política general, pero sí una implementación parcial». Ricardo, `[54:16]`–`[54:58]`: «estas se pueden responder con "parcialmente"; el tema es cuánto van a pesar» (el principio del párrafo está truncado, duda T9 de la limpia). Ricardo, `[55:05]`–`[55:09]`: «¿…le cuenta la mitad, el 30 %, el 40, el 60?». Rubén, `[55:13]`: «el "parcialmente" ayuda sobre todo para liberar tensiones: la institución sostiene una cosa y nosotras otra, pero como que poquito».

**«No cumple» sin que la IES cambie su respuesta.** Ricardo, `[55:41]`–`[55:48]`: «lo que hemos platicado era que la revisora pudiera cambiar manualmente un resultado al no». Rubén, `[55:53]`: «Sí sería importante que las revisoras pudieran aprobar o no aprobar sin que la institución tenga que modificar». Ricardo, `[56:39]`: «algo así como "finalizado", "rechazado", o "no aplica", y que eso lleve al no, que cambie al no aunque la institución haya puesto que sí». Rubén, el caso, `[56:56]`–`[57:48]`: una IES con el 99 % validado y una pregunta que no acredita y no va a cambiar; «lo que necesitamos es la opción de que nosotros digamos: "bueno, no te obligo a cambiarlo, pero no te lo valido". Es lo mismo a que te metas y le pongas que no lo tienes»; con la revisión anterior eso generaba «reuniones de trabajo muy tensas»; «Le pones "no cumple" y ya se resuelve de nuestro lado. […] puedes pensar, para la parte de revisión, cómo se resuelve eso».

**«Parcialmente», cuánto vale.** Ricardo, `[1:01:19]`–`[1:01:25]`: «no terminamos de definir lo de parcialmente». Rubén, `[1:01:28]`: «si se abre la opción de parcialmente, ¿cuánto vale?». Ricardo, `[1:01:45]`: «Un tercio». Rubén, `[1:01:48]`: «lo más justo sería que valiera el 50 %, la mitad». El riesgo, `[1:01:53]`–`[1:02:15]` (atribuido a Ricardo; la limpia marca la atribución como dudosa, duda 1): «se presta a que todo el mundo ponga parcial en todos lados y que te discutan si es parcial, lo mismo que el no aplica». Rubén, `[1:02:22]`: «Tú le puedes poner no aplica a todo, y eso hace que en vez de evaluarte 10 aspectos te evalúen 3». Ricardo, `[1:02:55]`: «lo de parcialmente, yo digo que lo descartemos» (la atribución puede ser de Rubén, duda 1 de la limpia; el desenlace no cambia: Rubén fija .5 en `[1:05:44]`); Rubén, `[1:03:00]`: «Sí, dejémoslo fuera»; Ricardo, `[1:03:02]`: «Por ahora. O dejémoslo como una opción que, solo si se pone heavy la cosa, ustedes lo puedan poner».

**Solo la revisora, solo en preguntas marcadas, .5 fijo.** Rubén, `[1:03:13]`–`[1:03:19]`: «¿si el parcialmente solo lo puede usar la revisora? […] le pongo parcialmente en la revisión». Ricardo, `[1:03:32]`: «podríamos marcar cuáles sí admiten parcialmente y cuáles no […] "¿La disposición es jurídicamente vinculante y de observancia obligatoria?": pues eso no tiene parcialmente»; `[1:04:11]`: «intentémoslo así. Sí, me gusta. Es un poquito más complicado». El ejemplo de Rubén, `[1:04:23]`–`[1:04:47]`: un reglamento de paridad solo en los sínodos de examen profesional, «los sínodos no son todos los cuerpos colegiados. Ahí sí sería parcialmente». Ricardo, `[1:04:56]`: «¿tendría sentido darle un slider?»; `[1:05:11]`: «O que todo valga 0.5, o un 0.2, 0.4, 0.6 y 0.8» (atribución del final dudosa, duda 3). Rubén, `[1:05:23]`–`[1:05:30]`: «una revisora […] le ponga .4 y otra le ponga .8 a lo mismo»; `[1:05:41]`–`[1:05:44]`: «Es mejor sin arbitrariedad: todo lo parcial, que valga lo mismo, .5, o sea, la mitad. Simple, .5». Ricardo, `[1:05:34]`: «de acuerdo»; `[1:06:07]`: «Sí, me parece bien. A ver si está preparada esta madre para eso —y que sea solo para las revisoras es una cosa más—, pero creo que sí se puede implementar».

**Lo que Ricardo decidió en el triage (23 de septiembre):** «Lo de "parcialmente" no es algo que implementaremos hoy, puede quedar para dentro de 2 semanas sin problema», es decir, hacia el 7 de octubre de 2026. Pendientes: la granularidad (por pregunta A, por grupo o por observable) y el choque de nombre con los estatus existentes `cp_partial` («Parcialmente respondido») y `cp_partial_approved` («Parcialmente aprobado»). Se cruza con [[adr-0017]] (el «No» vale cero) y [[adr-0019]] (la revisión actúa por eje).

### (b) El observable sin transversalidad orgánica y los planes de estudio

El observable no se nombra en la reunión; por lo que se describe (tiene planes de estudio y ninguna pregunta de transversalidad orgánica) es el 1.12, el mismo que [[task-165]] punto 3 anota «sin pregunta B».

Ricardo, `[44:32]`–`[44:49]`: «todas tienen transversalidad orgánica, pero no todas tienen transversalidad sectorial, como formación docente. Ah, bueno, fíjate: esta tampoco tiene transversalidad orgánica». `[45:24]`–`[45:26]`: «esta está marcada, pero no tiene ninguna pregunta. Eso está mal». Rubén, `[45:33]`–`[45:38]`: «no aplica transversalidad orgánica ahí»; `[45:46]`: la orgánica serían las escuelas y facultades, «sería como medir dos veces el mismo tema». Ricardo, `[46:11]`: «los planes de estudio serían una manera de medir la transversalidad orgánica». Rubén, `[46:17]`: «No: los planes de estudio son otra transversalidad, que es la transversalidad curricular».

La regla de obligatoriedad, Ricardo, `[46:32]`–`[46:35]`: «la regla que yo fui escribiendo dice que tiene que tener al menos una pregunta de armonización, institucionalización y al menos una de transversalidad. Si metemos planes de estudio dentro del universo de lo que es transversalidad, esta ya cumpliría. Ahorita por eso no puedo quitar transversalidad orgánica: la había puesto como obligatoria en todas, y esta es la única pregunta que no la tiene» (hoy `b_questions` tiene `required=True`). `[47:11]`: «que se pueda quitar transversalidad orgánica, porque tiene planes de estudio […] transversalidad curricular está bien, me gusta». Rubén, `[47:35]`–`[47:48]`: «resuélvelo como tú consideres mejor: abrir una nueva categoría que se llame transversalidad curricular, o darle nada más la opción de que en ese caso pueda no tener transversalidad, pero sí planes de estudio». Ricardo, `[47:48]`–`[47:51]`: «hacer una agrupación de transversalidad, porque en las visualizaciones […] todo va a tener su parte de armonización e institucionalización y, por otro lado, su parte de transversalidad»; `[48:27]`: «sí tengo que pensar cómo, pero planes de estudio sí tiene que entrar dentro del grupo o el subgrupo de transversalidad […] son dos grandes grupos, armonización e institucionalización por un lado, y transversalidad por otro».

Rubén, `[44:59]`–`[45:14]`, había propuesto abrir formación docente; Ricardo abrió otro.

### (c) Todo lo activo suma 10, y cómo se reparte dentro

**El piso de Rubén.** `[42:17]`: «La idea es que sumen 10 en cada una y que decidamos cómo se van a generar sus equilibrios cuando falte un componente». `[43:24]`: «todo lo que esté activo tiene que sumar 10». `[44:09]`: «Lo que hemos decidido, de verdad —ese sí fue un criterio para todas—, es que vale 5 la institucionalización con armonización y 5 la transversalidad, ¿verdad? Pero hay algunos que no van a tener nada de transversalidad». Ricardo, `[43:31]`: «primero hay que decidir los que tienen tres, luego los que tienen dos; hay que ver si los que tienen transversalidad orgánica de un solo tipo —solo instancias académicas— cuentan igual que los que tienen dos».

**El reparto dentro del 5.** Rubén, `[1:06:23]`–`[1:06:36]`: «¿Qué va a hacer con los elementos internos? […] ¿Cómo va a estimar ese 5?». Ricardo, `[1:06:51]`–`[1:07:24]`: «Aquí hay 6 preguntas; entonces cada una vale 0.8 […] yo no sé si debería valer 2.5 la sectorial; yo creo que la sectorial tendría que valer menos». Rubén, `[1:07:28]`–`[1:07:42]`, sobre la orgánica: «¿Le puede cambiar 100 % de las instancias entre 2.5?» (duda T11) y «si son 10 sectores, va a ser 2.5 entre 10». Ricardo, `[1:08:03]`: «la transversalidad sectorial es mucho más fácil de alcanzar y es más cualitativa […] tal vez distribuiría 6, 3, 1, o 4, 4, 2»; `[1:09:09]`: «estos los pondría como default». Rubén, `[1:08:53]`: «si le voy cambiando a cada uno, va a ser difícil sostener metodológicamente que a cada cosa le ponga algo distinto»; `[1:09:25]` y `[1:10:32]`: lo sectorial «es muy difícil que lo logren»; un protocolo de violencia de los centros de investigación de la administración pública que no incluye estudiantes; «Por eso, que valga lo mismo». Ricardo, `[1:10:18]`–`[1:10:24]`: en las normativas «es más fácil lograr la sectorización».

**Multiplicar por sectores.** Ricardo, `[1:11:27]`–`[1:13:40]`: «La otra opción es hacer una multiplicación por sector»; «multiplicar esos 5 por el porcentaje» de sectores en que aplique. Rubén, `[1:12:21]`: con pocos criterios y transversalidad total, «lo máximo que pueden sacar es un 5 y algo, un 6»; `[1:13:08]`: «Cada uno vale un punto»; `[1:14:15]`–`[1:14:52]`: ayudaría en instituciones chicas, no en la UNAM, donde la administración central puede cumplir los criterios y cada facultad no. Ricardo, `[1:14:42]`: «esta pregunta no se hace por cada instancia académica»; `[1:15:11]`–`[1:15:41]`: «yo no tocaría la orgánica […] Siento que estas dos están demasiado conectadas y deberían multiplicarse de alguna manera». Ricardo, `[1:18:52]`–`[1:19:11]`: el caso de quien contesta una sola pregunta que sí con todos los sectores, «va a tener un chingo de puntos cuando el avance es súper chiquito». Rubén, `[1:19:15]`: «si eso vale 2.5 de todos modos, aunque tenga todo, es lo máximo que puede sacar […] lo mejor es tener reglas lo más generales».

**Fórmula general y excepciones.** Rubén, `[1:16:52]`: «sería bueno que tengamos una fórmula general, y las excepciones […] sobre esa fórmula general quizás podemos hacer algunos casos para ver cómo se comportaría el índice, y si nos convence, pues ya lo dejamos». Ricardo, `[1:17:15]`–`[1:17:20]`: «¿no te han presionado sobre cómo se mide eso?»; Rubén, `[1:17:23]`–`[1:17:33]`: «nunca jamás alguien me ha preguntado "oye, ¿por qué promedias y no multiplicas?" […] lo que resulta mejor […] es tener una fórmula muy bien hecha […] cada parte del índice vale 5 puntos; en el caso de la institucionalización depende del número de elementos […] y la transversalidad puede ser sectorial, orgánica y curricular, y dependiendo del índice se elegirá uno o varios de esos elementos, que se promedian también […] démosle una pensadita […] y lo resolvemos la próxima» (los «dos componentes» del principio del párrafo, duda T12). Rubén, `[1:19:49]`: «Pero no me cierro»; Ricardo, `[1:19:50]`: «O sea, pensémoslo. Sí, y no urge»; Rubén, `[1:19:55]`: «está muy bueno tener esta conversación».

### (d) La ponderación de la población en el observable de integración paritaria

Enlace: [[task-111]], donde queda el detalle. Ricardo, `[48:56]`–`[49:01]`: «¿cuánto vale la ponderación de la distribución de la población? ¿Cómo medir eso?»; `[49:26]`: «es la de integración paritaria»; `[49:41]`–`[49:42]`: «no tenemos que definirla ahora». Rubén, `[50:12]`: entre 45 y 55 «se considere paritaria»; `[50:51]`: un índice de paridad, decidiendo «si lo construyes con base en las mujeres o en los hombres». Ricardo, `[50:36]`–`[50:43]` y `[51:30]`: ¿44 % igual que 22 % o 12 %?, ¿cuánto vale la paridad?, «tal vez haya poblaciones que sean más importantes que otras». Rubén, `[51:55]`: «Tienes razón».

### (e) Si el sí/no inicial pesa en el ponderador de institucionalización

Enlace: [[task-28]], donde queda el detalle. Rubén, `[52:29]`: si el ponderador «utiliza la batería de acá abajito […] o si también toma en cuenta la pregunta de sí o no inicial». Ricardo, `[52:52]`: «Ahorita no lo toma […] No sé si tendríamos que, solo por contestar que sí, regalarles un punto; yo creo que no, pero no lo sé». Rubén, `[53:20]`: «Como que hay que revisarlo». El caso límite (Ricardo, `[53:22]`–`[53:36]`): «¿qué pasa si alguien pone que sí y en todas estas pone que no?»; Rubén, `[53:38]`: «sí puede pasar».

### (f) Los casos excepcionales, candidatos a «parcialmente»

Ricardo, `[58:12]`–`[58:20]`: «los casos excepcionales… hago un análisis para ver cómo se podría resolver; más bien, yo te los paso. Los casos excepcionales son los que podrían tenerlo parcialmente, o los que podrían tener que…». Rubén, `[58:39]`: «Los que podrían tener parcialmente —si quieres le podemos pedir eso a la IA— y los que no tienen esta estructura, que es la más parecida en todos los observables: una batería de institucionalización, una de transversalidad sectorial y una de transversalidad orgánica». Ricardo, `[59:00]`–`[59:09]`: eso se ve en los contadores del dashboard. Rubén, `[59:14]`: «hay que revisar los casos en los que no se sigue esa estructura, para ver qué se va a hacer». Compromiso: Ricardo se los pasa. Lo de la estructura toca también [[task-15]].

### (g) Exportar las buenas prácticas para el comité científico de expertas

Rubén, `[00:04]`–`[00:18]`: «Estoy trabajando las buenas prácticas […] son 150 y luego las tengo que revisar yo, porque todas implican un nivel de criterio». Ricardo, `[00:09]`: «Eso deberías delegarlo a la IA». Rubén, `[1:20:44]`: «Las buenas prácticas no se pueden exportar, ¿verdad?»; Ricardo, `[1:20:54]`: «Ahorita todavía no». Rubén, `[1:21:01]`: «creo que va a tocar bajar una por una». Ricardo, `[1:21:05]`: «¿Pero por qué no lo hacen en el dashboard?». Rubén, `[1:21:08]`: «no son las revisoras: es el comité científico de expertas que van a revisar las mejores». Ricardo, `[1:21:15]`–`[1:21:32]`: «Hacer la exportación ahora es muy rápido y muy fácil; puedo hacer una básica y ya. ¿Pero con filtros? No sé»; `[1:23:46]`: «igual no urge, porque todavía falta que aprueben algo». Rubén, `[1:23:54]`: «Falta un ratito…» (fin ininteligible, duda T15).

**Destino abierto:** [[task-32]] (exportación a Excel de las puntuaciones, para la revisora) o una task nueva; el destinatario aquí es el comité, no la revisora.

### (h) Candidatos a ADR, pendientes de confirmación de Ricardo

No se escribieron como ADR: Ricardo no los confirmó.

- **C1.** «Parcialmente» solo lo pone la revisora, vale .5 fijo, sin slider, y solo en las preguntas marcadas como admisibles. Rubén fija el .5 en `[1:05:44]`; Ricardo, `[1:04:11]`, «intentémoslo así», y `[1:06:07]`, «me parece bien». Timestamps: `[1:01:48]`, `[1:03:13]`–`[1:06:07]`. Sujeto a lo decidido en el triage para (a): no hoy, hacia el 7 de octubre.
- **C2.** Los planes de estudio son transversalidad curricular, dentro del grupo de transversalidad; dos grandes grupos, armonización-institucionalización y transversalidad. Rubén lo delegó en `[47:35]`; Ricardo eligió en `[47:51]` y en `[48:27]` dijo «sí tengo que pensar cómo». Timestamps: `[46:17]`, `[47:11]`–`[48:56]`.

## Criterios de aceptación

- [ ] Cada punto (a)–(g) tiene decisión de Ricardo y Rubén registrada, o una task propia
- [ ] El dictamen de la revisora (a) tiene definida su granularidad y su nombre frente a `cp_partial` y `cp_partial_approved`
- [ ] Los candidatos C1 y C2 se confirmaron como ADR o se descartaron
- [ ] (f) Ricardo le pasa a Rubén los casos excepcionales (`[58:20]`)

---
type: record
id: 2026-09-28-panorama-onigies
date: 2026-09-28
parent: "[[task-2]]"
related: ["[[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]", "[[2026-09-25-estimacion-costos-onigies]]", "[[2026-09-23-reunion-ruben]]"]
---

# Panorama de ONIGIES al 28 de septiembre de 2026

Sesión que empezó como orientación y terminó ejecutando dos cambios en el API (los `PROTECT` y el manejador global de [[task-178]]): Ricardo pidió «entender el panorama de en dónde estamos con ONIGIES, qué tenemos por delante, qué pendientes urgentes faltan de cerrar», agrupado por tema y ordenado por prioridad. Un explorador de apertura leyó el árbol documental (131 tasks abiertas: 72 del asistente, 59 de Ricardo; un feedback pendiente), los records y ADRs de las últimas cuatro semanas, el roadmap del skill `deployment` y el estado de git. Este record es el panorama ampliado: las secciones 1 y 2 tal como Ricardo las leyó en la sesión, con sus respuestas aplicadas; las secciones 3 a 7 y git con más detalle del que se presentó, porque él las dejó para leer aquí. Bitácora `ef5df6ef-e536-4601-a844-cdaa3da4f2eb`.

## Dónde estamos

El cuestionario principal (cp, la captura por observable) está en producción desde el 25 de septiembre a las 00:00 hora de México, publicado y abierto a las IES reales ([[2026-09-25-deploy-del-cuestionario-principal-y-documento-para-ruben]]). Pero abrirlo no abrió nada todavía: por [[adr-0018]], una IES solo captura cp cuando su paquete de generales está en `gen_finished`, y a la 01:30 del 25 había 0 de 66 en ese estado (46 en borrador, 19 enviados, 1 con cambios). La llave real de cp es el ritmo al que la revisora apruebe generales.

Git: `main`, `production` y `origin/main` coinciden en `de32e72`. La rama `cp-backend` lleva tres commits solo de documentación (la estimación de costos y sus scripts) que no están en `main` ni tienen upstream. Hay una carpeta `.claude/scratch/` sin versionar con el triaje de memorias del proyecto, propuesta no ejecutada.

## 1. Cola del deploy de cp

Cuatro cosas quedaron abiertas la madrugada del 25 y el grafo no tenía constancia posterior. Respuestas de Ricardo el 28:

- **Instrumento editable con IES dentro** ([[task-163]] y [[task-178]]). `QuestionnaireSettings.content_open=True` sigue activo: Rubén puede editar observables y preguntas desde el dashboard mientras las IES ya ven el cuestionario. El riesgo real es el borrado: con `on_delete=CASCADE` en `api/answer/models.py`, borrar una pregunta arrastra lo que las IES hayan capturado. Las opciones de task-178 eran bloquear la visibilidad mientras `content_open`, pasar los borrados a `PROTECT`, o seguir con avisos a Rubén. **Ricardo: «Va con PROTECT».** Un executor lo aplica en esta misma sesión; la task queda abierta hasta que se despliegue.
- **Smoke visual en producción** y llevar antes una IES de prueba a `gen_finished` (task-163). **Ricardo lo está haciendo hoy**; los criterios se marcan cuando él lo confirme.
- **Documento de la brecha para Rubén** ([[task-164]], el Word y PDF de `~/respaldos/onigies-ruben/ONIGIES-2026-brecha-y-no-aplica`). Tres decisiones del documento (P1, P2 y P4) habían entrado con la recomendación del coordinador sin respuesta de Ricardo. **Ricardo: «ya se lo mandé, ya cerremos esa tarea, ya no está de nuestro lado». Cerrada.**
- **Ritmo de aprobación de generales** ([[task-165]] punto 5). Rubén dijo que ~60 % de las IES subieron su información base; eso es envío, no revisión. **Ricardo: «eso no se registra acá, eso es operativo».** El criterio queda fuera del alcance del grafo; dónde guardar esa regla es [[task-183]].

## 2. Dinero y trámite con la CIGU

Era una cadena: [[task-155]] → [[task-154]] → [[task-179]] → [[task-180]]. Estado tras las respuestas de Ricardo:

- **Registro como proveedor de la UNAM** (task-155): **ya quedó**; cerrada. Lo que sigue es lo que pide Dana por correo ([[mail-admin-cotizacion]]): cotización con el concepto «Servicio de actualización de plataforma ONIGIES» y cronograma octubre–noviembre–diciembre de 2026, con las mismas actividades que Rubén entregó a la Titular. Es [[task-181]], con la tabla de conceptos 2026 transcrita (80,000 + IVA = 92,800).
- **IVA, resuelto.** 2026 son 80,000 más IVA; lo pagado en 2025 fueron 100,000 con IVA incluido, que cuadra con el subtotal de 86,206.90 que ya usa [[estado-administrativo-y-de-pagos]]. Ricardo señaló que ya lo había aclarado antes y el grafo lo seguía tratando como duda (feedback global fb-826).
- **Cuadre de pagos** (task-154): sigue en octubre de 2026, compromiso de Rubén. Siguen por cuadrar las cifras que no coinciden: 89,727 de Rubén contra 86,206.90 de subtotal; 80 + 156 = 236 contra 233; y el renglón repetido de visualizaciones de población (17k y 18k) que Rubén redondeó a 20k.
- **Estimación de costos** (task-179, 4 de 15 criterios): **«luego, con calma, cuando vea a Rubén próximamente»**. **Documento de negociación** (task-180, 0 de 7): **«después»**. La cifra gruesa ya existe ([[2026-09-25-estimacion-costos-onigies]]): lo hecho cuesta ~165,600 MXN contra 86,206.90 cobrados; desborde neto ~75,000, de los cuales ~29,800 cobrables por exceso de lo pedido y ~62,200 no planeado que se factura prorrateado ([[adr-0022]]). Faltan datos que solo Ricardo tiene: fecha de Miró, cláusula de soporte de 18 meses, costos de terceros (Yeeko, S3, Netlify), fracciones de las sesiones mixtas; el record advierte que abril–junio «lee alto» antes de llevarlo a Rubén. La idea registrada para task-180: pedirles templates de informes hechos con Opus, o dejarles un skill como el de OCSA, como compensación de los costos.

## 3. Metodología del índice, con Rubén

- **[[task-173]]**, el análisis de las ideas metodológicas de la reunión del 23 ([[2026-09-23-reunion-ruben]]), tiene siete puntos y dos con fecha o compromiso: (a) el dictamen «parcialmente» (solo la revisora, .5 fijo) que Ricardo puso «para dentro de 2 semanas», es decir hacia el 7 de octubre de 2026; y (f) su compromiso con Rubén de pasarle los casos excepcionales del cuestionario. Los otros: planes de estudio como transversalidad curricular, «todo lo activo suma 10», paridad del 1.7, peso del sí/no inicial, exportar buenas prácticas al comité científico (que task-173 quiere colgar de la exportación a Excel de [[task-32]]).
- **[[task-28]] y [[task-29]]** (ecuación del índice y sus ~10 condiciones base): la estimación las calcula en ≈3 h de reunión con Rubén más ≈3 h de Ricardo, y son el prerrequisito de las visualizaciones, ~92k del contrato. Nada llena hoy `GroupResponse.value`; los pesos propios siguen nulos ([[task-15]], cuya cabecera todavía habla de un fallback 60/40 que adr-0014 y adr-0015 dejaron atrás: 5 / 2.5 / 2.5).
- **[[task-165]]**: faltan la unidad de análisis en IES no autónomas, el alcance obligatorio, el 1.12 y la simulación de calificaciones. **[[task-111]]**: paridad. **[[task-5]]** (raíz): taller de estados ([[task-26]]) y comentario obligatorio al marcar «atendido» ([[task-30]]). **[[task-16]] y [[task-17]]**: textos del 4.4 y del 2.1/2.2. **[[task-2]]** (raíz de cp): le faltan «pesos reales» y «la calificación existe».
- **[[task-157]]**, el barrido crítico del cuestionario, estaba bloqueado «hasta el aviso de Rubén». En la reunión del 23 Rubén dijo «ya había terminado los cambios; ya los mandé a las IES». **Ricardo: «Ya se cierra». Cerrada**: el instrumento ya está con las IES y el barrido no procede.

## 4. Decisiones de Ricardo sobre la captura cp (diálogo, sin fecha)

Se acumularon en tasks de la última semana; ninguna bloquea, todas esperan su voto. Conviene una sesión de diálogo dedicada a vaciarlas:

- [[task-169]]: nueve puntos de UI de la captura cp (menú del chip, historia sin comentarios, orden gen/bp, contraste, ancho, flaky con Playwright, `YesNoRadio`, foco de «Te toca», etiquetas de la pregunta especial) y dos cosas aplicadas sin su voto.
- [[task-175]]: campo `cp_submission_deadline`, abandonar [[task-162]], qué documento revisó Rubén en tres horas, confirmar la edición Sí/No de las tres preguntas A.
- [[task-176]]: repensar las respuestas en null.
- [[task-172]] (3 de 6): «Ver preguntas» a la derecha sin verificar, confirmar que «Nota:» se queda, quitar el paréntesis de la pregunta especial, tamaño del eje Cuidados.
- [[task-166]]: lista de 11 e2e de cp por acordar. [[task-140]]: tests de la compuerta y del editor. [[task-143]]: quién puede cerrar el cuestionario.
- Decisiones menores del editor y del Word: [[task-141]], [[task-145]], [[task-148]], [[task-158]], [[task-159]], [[task-160]].

## 5. Infraestructura y migración a la UNAM

La Fase 1 del roadmap del skill `deployment` (`.claude/skills/deployment/references/roadmap.md`) no ha empezado: «Nothing here has started»; ONIGIES no ha pedido servidor a la DGTIC ni tiene interlocutor ahí. Quien levanta tickets es Carlos Gutiérrez y el vínculo depende de Rubén ([[interlocucion-con-la-cigu]]). Las tasks son [[task-100]] (raíz), [[task-102]] y [[task-103]]. Mientras tanto producción vive en Yeeko con el puente nginx a Netlify y los archivos en el bucket S3 `onigies-v3-temporal`.

Pendientes del roadmap tal como están escritos (última actualización 2026-09-11): Fase 1, pedir la VM a la DGTIC, aprovisionarla, desplegar `api/`, regresar los archivos al disco y retirar el bucket, decidir dónde vive `nuxt/`, reapuntar `NUXT_API_URL` y `NUXT_ADMIN_URL`, reemplazar el puente nginx; Fase 2, allowlist de CORS, revisar `ALLOWED_HOSTS`, confirmar `DJANGO_DEBUG=False`; Fase 3, rehacer el sitio público, migrar o archivar los datos del Django legacy, retirar el legacy. Decisiones abiertas: el hogar de Nuxt a largo plazo y el dominio final del API.

Dos contradicciones documentales, pendientes de Ricardo:

- **DEBUG y CORS.** [[task-4]] marca como hecho «El API en producción corre sin `DEBUG` ni CORS abierto», pero [[task-115]] (0 de 4), el skill `deployment` («Production currently runs `DEBUG=True`») y el roadmap dicen lo contrario. El código lee `DJANGO_DEBUG` con default False (`api/core/settings/__init__.py`); el `.env` del servidor no se leyó. Hipótesis: el criterio de task-4 se marcó por el código, no por el servidor. Se resuelve con un `grep` en el servidor.
- **Roadmap contra [[adr-0021]].** La Fase 3 dice «Migrate or archive data from the legacy Python 2 Django»; adr-0021 decidió liga a lo histórico, no integración. El roadmap tampoco sabe que cp está en producción. Es una edición de un camino; se hace cuando Ricardo diga.

Pendientes chicos del mismo tema: borrar la carpeta de respaldos del API en el servidor Yeeko ([[task-25]], ahora también con el dump `pre_cp_20260925_0614`), retirar onigies de pm2 en el EC2 ([[task-95]]), y el pathspec de migraciones en `deploy-api` ([[task-149]], que Ricardo dejó «no puedo decidir ahora»).

## 6. Textos e instrumento que esperan a Rubén

Descripciones de los ejes Inclusión y Cuidados y revisión de las seis descripciones de `QuestionType` ([[task-171]]); la revisión humana del cuestionario ([[task-50]]); «existen» por «se atiende» ([[task-88]]); tercera persona y tú ([[task-156]]); la sesión de acompañamiento con las becarias que aún no ocurre ([[task-152]]).

## 7. Backlog

Unas 80 tasks del asistente, casi todas de agosto:

- Buenas prácticas y comentarios: [[task-6]] y [[task-98]] con sus hijas, [[task-99]]. [[task-44]] es un bug real: los comentarios por criterio siguen abiertos cuando el paquete regresa a la IES. [[task-10]], candado de periodo en el backend; [[task-11]], verificación de punta a punta de bp.
- Dashboard y deuda técnica: [[task-3]], [[task-41]], [[task-61]], [[task-101]] con sus hijas, y una veintena sueltas.
- De Ricardo sin fecha: [[task-89]] (recordatorio automático) y [[task-90]] (doble factor).
- Tres raíces con todos sus criterios marcados que siguen abiertas solo por sus hijas: [[task-1]], task-41 y task-61.
- Nuevo este día: [[task-182]], no permitir una invitación para un correo ya registrado.

El único feedback pendiente era [[fb-1]] (el campo `order` nunca se edita en formulario), `scope: local` en un proyecto con cliente, cosa que documenter §5 no permite; su propuesta ya estaba escrita en el skill `dashboard-collections`, así que se cerró como `promoted`.

## Git, dos decisiones chicas de Ricardo

- **`cp-backend` sin fusionar a `main`.** Al abrir la sesión llevaba tres commits solo de documentación; con el commit de esta sesión lleva además código sin desplegar (los `PROTECT`, el manejador global y la migración `answer 0007`), así que fusionarla a `main` equivale a desplegar ([[adr-0001]]). Va ligada al deploy de [[task-178]]; la limpieza de ramas es [[task-186]].
- **`claude/gallant-jemison`** (`111e7c1`, 2026-04-15, «Corrige bugs reportados en prueba con usuarios reales», toca `GoodPracticeCard.vue`, `GoodPracticeEditSimple.vue`, `SurveyInitData.vue` y `RegisterForm.vue`): 1 commit por delante y 120 por detrás; `git cherry` no encuentra su parche en `main`. Hipótesis: los arreglos se rehicieron en el rediseño de bp. Vale un vistazo antes de borrarla. Las otras siete ramas locales (`edicion-cuestionario-v2`, `fix_bugs_ia`, `questionnaire-ies`, `remove-statuscontrol`, `task-131-…`, `task-150-word-export`, `task-42-…`) no tienen nada propio y son borrables.

## Orden propuesto

1. Cerrar la cola del deploy (`PROTECT`, smoke), porque hay IES dentro y un riesgo irreversible abierto.
2. La cotización y el cronograma para la administración de la CIGU ([[task-181]]), que es lo que destraba el pago de 2026.
3. [[task-173]] (a) pegada al 7 de octubre; el cuadre en octubre; la estimación cuando Ricardo vea a Rubén, y la negociación después.
4. Ecuación del índice ([[task-28]], [[task-29]]), porque desbloquea el tramo más caro del contrato.
5. Lo demás sin orden impuesto.

## Fechas conocidas

- Hacia el 7 de octubre de 2026: dictamen «parcialmente» (task-173 §a).
- Octubre–diciembre de 2026: cronograma de la cotización (task-181).
- Enero de 2027: pago de lo restante (~156k) según Rubén; visualizaciones e informes «para el año que viene».
- Las fechas límite por sección para las IES las pone Rubén fuera de la plataforma y no se registran aquí. No hay fecha de cierre de cp en ningún nodo; solo el posible campo `cp_submission_deadline` ([[task-175]] b).

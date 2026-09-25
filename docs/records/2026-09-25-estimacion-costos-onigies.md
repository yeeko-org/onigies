---
type: record
id: 2026-09-25-estimacion-costos-onigies
date: 2026-09-25
parent: "[[task-154|cuadre de pagos con la CIGU]]"
related: ["[[estado-administrativo-y-de-pagos]]", "[[task-179]]", "[[task-180]]", "[[adr-0021]]", "[[adr-0022]]", "[[2026-09-25-conceptualizacion-en-miro]]", "[[2026-09-25-reuniones-sin-grabacion]]", "[[2026-09-25-analisis-y-construccion-de-la-base]]", "[[2026-09-25-identidad-grafica-en-claude-design]]", "[[2025-09-11-cotizacion-plataforma-v3]]", "[[2026-01-07-cotizacion-plataforma-v3]]"]
---

# Estimación de costos de ONIGIES del lado de Ricardo (25 de septiembre de 2026)

Documento primero para Ricardo; después él decide qué parte y en qué forma llega a Rubén. Método: skill `cost-audit` (horas medidas × tarifa declarada, una sola base), invocado por Ricardo en la sesión `fdef28fa-50b5-4e49-8a6a-7b05bd2a7241`, que queda excluida del conteo. Scripts y salidas en `docs/scripts/cost-audit/`.

## Veredicto

**El trabajo hecho hasta hoy cuesta, a tus tarifas, unos 165,600 MXN antes de IVA (rango 156,900–189,100), por 143.3 horas (rango 136.1–167.9).** De eso, 2,600 son el adelanto de la identidad gráfica de la cotización de 2026 (2 h en Claude Design); los otros **162,950** corresponden a los renglones de la cotización de 2025 ya pagados (88,000) y a lo que se hizo fuera de ellos. Por ese trabajo se han cobrado 86,206.90: el costo es **1.89 veces** lo cobrado, y **costo a tarifa menos lo cobrado da unos 76,700 MXN de subtotal**. No es una desproporción de cinco o diez veces; es casi el doble, y todavía es un piso: faltan la preparación de las cotizaciones y los días sin commit de diciembre–febrero (ver «Lo que falta declarar»). Esa diferencia no es lo que el contrato permite cobrar: por la regla contractual del skill («cotizado × % entregado − cobrado») lo pendiente de lo ya entregado es solo 1,793.10, porque la cotización del dashboard era baja (ver la síntesis).

**Cómo se reparte el desborde** (sección «Brecha por concepto y sus causas», con los ajustes de Ricardo de la noche del 25 de septiembre). Contra los 88,000 cotizados, el trabajo hecho va **unos 75,000 arriba**, y se arma así:

- **Por cobrar, lo que pidió el cliente: ~29,800.** El excedente de buenas prácticas, el editor del cuestionario, las invitaciones de las IES, la exportación a Word y la institución de prueba. Ricardo lo decidió: se cobra ([[adr-0022]]).
- **Costos no planeados: ~62,200.** La base del dashboard, la infraestructura y los deploys, las reuniones grabadas y las no grabadas, las transcripciones y la planeación, y el exceso del diseño de la base de datos. Ricardo lo decidió: se registran para aprender **y también se facturan, prorrateados entre los demás renglones cuando sea posible** ([[adr-0022]]).
- **Renglones que van por debajo de su precio: −17,100.** Casi todo es el cuestionario por observable, que al 85 % lleva 12,400 contra 27,000.

**Y lo que falta cabe en lo cotizado con margen** (sección «Lo que falta»): los 233,000 de 2026 se estiman en 138,000–208,000 con IA y el harness, incluidas la máquina virtual y una reserva de coordinación que no tienen renglón. El margen de 22,400 a 92,400 (ya descontados los 2,600 de la identidad gráfica gastados a cuenta del renglón de 16,000) es el argumento para la negociación con Rubén ([[task-180]]): en el mejor caso compensa casi todo el desborde de 92,000 brutos; en el peor, una cuarta parte, y los ~30,000 pedidos se cobran aparte en cualquier caso.

El «% entregado» por renglón ya no es solo un supuesto de esta estimación: Ricardo fijó el cuestionario por observable en 85 % y el flujo de validación en 95 %, y dio por buenos los demás (poblaciones ~95 %, buenas prácticas ~80 %, base de datos 100 %).

## Las tres cifras que se comparan

- **Costo real**: horas estimadas × tarifa (850 MXN/h antes del 2026-03-02, fecha del primer `CLAUDE.md`, commit `b24f686`; 1,300 MXN/h desde entonces). Decisión de Ricardo del 2026-09-25.
- **Cobrado**: dos pagos de 43,103.45 + IVA en 2025, **86,206.90 de subtotal** (100,000 con IVA). Dato de Ricardo; la cotización de 2026 da por pagados 88,000 y Rubén dijo 89,727 el 2026-09-23 — solo como nota, la base es la de Ricardo.
- **Cotizado**: 240,000 en 2025 (septiembre) y 233,000 en 2026 (enero), subtotales. Alcance total cotizado: 88,000 pagados + 233,000 pendientes = **321,000**. Comprometidos para 2026: 80,000 (sin saber si incluyen IVA), sin cobrar aún.

Todas las cifras de dinero son subtotales, antes de IVA.

## Horas por periodo y por fuente

Cada renglón dice de dónde sale su cifra: **bitácora** (sesiones de Claude Code medidas con el modelo de crédito, ya repartidas con los demás proyectos abiertos al mismo tiempo — la magnitud «asignada», la única que factura — y netas de lo no facturable), **historial** (días con prompts en `history.jsonl` pero sin bitácora, convertidos con un cociente calibrado), **git** (días con commits y sin ningún rastro de Claude) o **declarado** (trabajo sin huella digital, con `offline_minutes`).

| Periodo | Fuente | Horas (central) | Rango | Tarifa | MXN (central) |
|---|---|--:|--:|--:|--:|
| 2025-12-03 → 2026-02-24 | git: 22 commits en 9 días activos | 20.0 | 18.8–38.7 | 850 | 17,034 |
| 2026-02-25 y 02-27 | historial: 39 prompts en 2 días | 4.1 | 3.8–4.3 | 850 | 3,442 |
| Miró, fecha desconocida | declarado, estimado | 6.0 | — | 850 | 5,100 |
| Reuniones sin grabación (antes del 2026-03-02; fecha y reparto no declarados) | declarado, estimado: «al menos 8 horas» | 8.0 | — | 850 | 6,800 |
| Análisis y construcción de la base de datos | declarado, estimado | 8.0 | — | 850 | 6,800 |
| **Subtotal antes de IA** | | **46.1** | 44.6–65.0 | | **39,176** |
| 2026-03-02 → 03-16 | historial: 34 prompts en 4 días | 2.4 | 1.1–3.7 | 1,300 | 3,146 |
| 2026-04-15 → 06-13 | bitácora de Windows (disco y RAR), neta | 16.9 | — | 1,300 | 22,010 |
| 2026-06-16 → 07-04 | historial: 264 prompts en 9 días | 24.5 | 20.1–28.9 | 1,300 | 31,863 |
| 2026-07-28 → 09-25 | bitácora de Fedora, neta, con ajustes | 45.3 | — | 1,300 | 58,915 |
| Reuniones grabadas (seis, jun–sep) | declarado, medido en la transcripción | 6.0 | — | 1,300 | 7,843 |
| Identidad gráfica en Claude Design (adelanto de un renglón de 2026) | declarado, estimado | 2.0 | — | 1,300 | 2,600 |
| **Subtotal con IA** | | **97.2** | 91.5–102.9 | | **126,377** |
| **Total** | | **143.3** | 136.1–167.9 | | **165,553** |

Los subtotales se sumaron sin redondear; los renglones están redondeados a una décima. Los tres renglones declarados del 25 de septiembre (reuniones sin grabación, análisis de la base y Claude Design) viven en [[2026-09-25-reuniones-sin-grabacion]], [[2026-09-25-analisis-y-construccion-de-la-base]] y [[2026-09-25-identidad-grafica-en-claude-design]], con su `offline_minutes`.

Las horas de bitácora van netas de lo no facturable (sección «Qué no se factura»): 67.8 h asignadas − 5.5 h = 62.4 h. En la época de Windows (abril–junio) son 20.4 h brutas menos 3.4 de dos sesiones personales = 16.9 h. En Fedora (julio–septiembre) son 47.5 h brutas menos 2.1 no facturables = 45.4 h, más 0.18 h de la sesión `803fabce` (abajo) y menos 0.29 h de sesiones que corrieron durante reuniones grabadas (abajo) = 45.3 h.

**Rango del total**: de 156,856 (git por racimos de commits, historial por ventana diaria) a 189,051 (git a 4.3 h por día activo, que es lo que midió OCSA para trabajo a mano; historial por prompt). Sin el adelanto de identidad, en cualquier punto del rango el costo queda entre 1.79 y 2.16 veces lo cobrado.

## Cómo se midió

### Bitácoras

`credit.py` (copiado de OCSA, con un arreglo, ver abajo) construye una línea de tiempo global con **todas** las sesiones de **todos** los proyectos de `~/.claude/projects/` y del archivo `~/.claude/session-logs-archive/projects/`. Cada instante se acredita una sola vez y se reparte entre los proyectos abiertos en proporción a su densidad de registros. Constantes sin cambios respecto al skill: escritura 90 caracteres/min, lectura 150 palabras/min, atención a la máquina 35 % en modo manual y 15 % en automático, hueco humano con tope de 20 min, tope de 95 % del reloj.

Las tres magnitudes, para ONIGIES:

| Magnitud | Horas | Qué es |
|---|--:|---|
| Crédito por sesión, sumado | 92.1 | Cada sesión por su cuenta; se enciman, no se compara con nada |
| Fusión intra-proyecto | 85.7 | Las sesiones paralelas de ONIGIES colapsadas, cada instante una vez |
| Asignada tras el reparto global | 67.8 | Lo que queda para ONIGIES al repartir los instantes con los otros proyectos abiertos; la única que factura |

El reparto le quitó 18 horas a ONIGIES: en agosto y septiembre casi siempre había otro proyecto corriendo en paralelo (OCSA, `~/.claude`, SNSP). Es la corrección más conservadora del método y está a favor del cliente.

Insumos: 88 sesiones con crédito; 28 vacías descartadas (sin ningún prompt real: 9 son los directorios de subagentes huérfanos de febrero–marzo, cuyas sesiones madre ya no existen; el resto son sesiones de solo comandos como `/clear` o `/model`, de respuestas de tres caracteres o menos, o, como `7d623dc1`, manejadas por otra sesión de Claude sin que Ricardo tecleara en ellas); el texto pegado descontado línea por línea (consola, logs, rutas, y desde la corrección de esta sección también páginas de error de Django; 128 líneas más descontadas por ser eco de algo ya visto ese día); 1.9 h de escritura que no cupo antes del corte de día y se perdió.

**Días con commits de ONIGIES y sin sesión de ONIGIES.** Cuatro días operativos tienen commits en este repo hechos desde sesiones abiertas en otro proyecto; `credit.py` asigna cada sesión ajena entera a su `cwd` dominante, así que ninguno llegaba a ONIGIES:

| Día | Commits | Sesión que los hizo | Clasificación | Horas a ONIGIES |
|---|---|---|---|--:|
| 08-19 | `673dd34` (status_groups, props sin mutar, typedefs, `patchCatalog`), `1b968fa` (Vitest, Playwright), `dc72a96` (cierre documental) | `803fabce`, abierta en `~/.claude` | MIXTA: 37 % de sus llamadas a herramientas (289 de 783, contando subagentes) tocan ONIGIES; el resto, SNSP, `written.django` y el harness. Fracción estimada: 40 % | 0.18 (de 0.44 h de crédito, casi todo en modo automático) |
| 08-27 | `fb0ab07` (enlaces a feedbacks globales, rename learning → feedback) | `aefd7da6`, en `~/.claude` | HARNESS | 0 |
| 08-28 | `72b35c0` (aviso en `nuxt/CLAUDE.md`) | una sesión de OCSA | HARNESS | 0 |
| 09-05 (commit a la 01:05 del 6) | `25823a7` (transcripciones del 11-ago migradas desde `written.django`) | `51d1e0b3`, en `~/.claude` | INVERSION_PROPIA: mudanza de archivos entre repos | 0 |

**Reuniones y sesiones al mismo tiempo.** Las reuniones grabadas entran completas al 100 %, así que el crédito de las sesiones que corrían durante ellas contaría el mismo reloj dos veces. Para las tres reuniones con hora de inicio registrada (11-ago 12:29, 4-sep 14:57, 23-sep 14:49) se midió el reloj vivo de cada sesión dentro de la reunión y se multiplicó por el cociente asignado/duración de esa sesión: `0d557873` 0.11 h, `a7383a8d` 0.08 h, `cd144c44` 0.10 h (y `34ca5579` 0.04 h, que ya no factura). Se restan **0.29 h** a Fedora. Es una aproximación: el crédito real dentro de la reunión no está guardado por intervalo. Las reuniones del 26-jun, 28-jul y 6-ago no tienen hora de inicio registrada y no se ajustaron; la del 26-jun cae en un día ciego cuya ventana (5.6 h) probablemente la incluye.

### Historial, para los periodos sin bitácora

`blind.py` (nuevo, en la misma carpeta) calibra sobre los 28 días que tienen a la vez prompts en el historial y bitácora de ONIGIES: 569 prompts y **62.36 h netas** (las 67.84 asignadas menos lo no facturable, porque el skill pide descontar del cociente las fracciones que no se facturan; con las brutas, todo lo estimado por historial y git salía 8 % alto). Los dos lados del cociente salen del historial, así que el subconteo de prompts encolados se cancela.

- **0.110 h por prompt** (mediana diaria 0.114).
- **0.382 h por hora de ventana diaria** (del primer al último prompt del día).
- **2.23 h por día activo** en promedio.

El renglón central de cada periodo ciego es el promedio de los dos primeros cocientes; el rango, uno y otro. Ninguno de los dos es mejor en todos los días: por prompt sobrevalora los días de muchos prompts cortos (03-16: 15 prompts en 26 minutos) y por ventana los subvalora.

Del 16 de junio al 4 de julio el historial tiene **287 prompts en 12 días**; se usan **264 en 9**. Salen: el 06-20 antes de las 12:55 (10 prompts de instalación de Fedora; de 12:55 a 17:24 es trabajo del proyecto — recomendaciones del dashboard, `EditCommonFields.saveStatus`, el rediseño de Flow contra StatusControl — y el commit `6dcfa8c` de las 16:05 lo confirma), el 06-27 (un solo prompt) y el 06-30 y 07-02 (12 prompts de un puente SSH a la UNAM con la llave de soporte de STIG; ⚠️ ambiguo, ver [[task-179]]; la VM del observatorio es la misma máquina que producción de STIG, lo que explica la llave). Del 5 al 27 de julio no hay ni prompts ni commits de ONIGIES: no hay evidencia de trabajo en ese tramo. Los días 08-07 y 09-12 tienen un solo prompt (`/resume`, `/logout`) y no cuentan.

### Git, para diciembre–febrero

Sin ningún rastro de Claude antes del 25 de febrero, solo quedan los commits: 22 commits de ONIGIES en 9 días activos (desde `7f91562`, «Primeros modelos», 2025-12-03; lo anterior de la historia de `api/` es el proyecto de escaleras y no cuenta). A 2.23 h por día activo, el cociente neto medido en la época con IA, salen **20.0 h**; los racimos de commits con 90 minutos de anticipación dan 18.8 h (piso). Las dos cifras son bajas por construcción:

- Es trabajo a mano: la época sin IA rinde menos por hora, y OCSA midió 4.3 h por día activo (38.7 h aquí, el techo del rango).
- Los commits son escasos y grandes («Buenas prácticas completo», «Muchos cambios»): los días de trabajo sin commit no aparecen.
- Enero incluye código copiado de OCSA (`04c0099`), así que las líneas de enero no miden trabajo; por eso se usan días, no líneas.

Febrero 25 y 27 ya tienen Claude Code (historial) pero caen antes del corte del 2 de marzo que Ricardo eligió, y van a 850.

**Principios de marzo, probablemente subcontado** (⚠️ decisión de Ricardo). El 03-02 tiene un solo prompt en el historial pero 7 commits, entre ellos `b24f686` («Reestructura total de answer y question…; agrego Claude…»); el 03-03 tiene 2 commits y 11 prompts; el 03-09, la unión en monorepo y 6 prompts. El historial les da **1.3 h** a esos tres días; el estimador de git (2.23 h por día activo) les daría **6.7 h**, unos 7,000 MXN más. No se aplicó: el skill dice que donde hay historial, git reparte las horas pero no las produce. Tomar el mayor de los dos en días con commits sería una desviación declarada del método.

## Qué no se factura

Harness, sesiones ajenas al proyecto y trabajo administrativo con el cliente, clasificados leyendo los prompts, no por título. Las fracciones viven en `cost-audit.json` (`billable_fraction`):

| Sesión | Horas asignadas | Clasificación | Descontado |
|---|--:|---|--:|
| Compartir Wi-Fi con VPN a una TV Samsung (junio) | 1.20 | personal | 1.20 |
| Memoria USB para el .iso de Fedora (junio) | 2.22 | personal | 2.22 |
| Configurar Opus 4.8 como modelo por defecto | 0.08 | harness | 0.08 |
| Migrar el sistema de docs a las reglas nuevas de documenter (dos sesiones) | 0.32 | inversión propia | 0.32 |
| Optimizar la lógica de /duo | 0.72 | mixta, 50 % proyecto | 0.36 |
| Estrategia de coordinación con agentes | 1.63 | mixta, 80 % proyecto | 0.33 |
| Reescribir párrafos y verificar hipótesis | 0.39 | mixta, 70 % proyecto | 0.12 |
| `b055612f`, exportación a Word (11 y 22 de septiembre) | 1.68 | mixta, 90 % proyecto (algo de diálogo sobre el proceso) | 0.17 |
| `34ca5579`, preparar la reunión del 11 de agosto | 0.13 | admin-cliente | 0.13 |
| `25bf79de`, qué pendientes llevar a Rubén | 0.05 | admin-cliente | 0.05 |
| `b6c8a4f0`, intake de la reunión del 4 de septiembre | 1.66 | mixta: 20 % admin-cliente (la reference de pagos, task-154 y task-155), el resto convertir la reunión en tareas | 0.33 |
| `6635e96d`, intake de la reunión del 23 de septiembre | 0.34 | mixta: 50 % admin-cliente (el cuadre de pagos de task-154) | 0.17 |
| **Total** | | | **5.48** |

Criterio del skill: la preparación de reuniones y el trabajo de cobro son admin-cliente y no se facturan; convertir una reunión en tareas y decisiones es proyecto. Las fracciones de las sesiones mixtas son estimaciones de lectura. La suscripción de Claude no aparece en ningún lado: los 1,300 por hora ya la absorben.

**Deploys, incidentes y puentes de infraestructura.** Ricardo los clasificó la noche del 25 de septiembre junto con las transcripciones: «más que "por cobrar" serán costos adicionales que yo no planee bien, igual que lo de los deploys». Eso es suyo: los deploys son costo no planeado, que se registra y se factura prorrateado ([[adr-0022]]). Lo que **no** dijo es cómo queda la cláusula de 18 meses frente a Rubén: leer su frase como «la cláusula no los absorbe» es interpretación de esta estimación, pendiente de que él la confirme en [[task-179]], junto con las opciones de abajo (incluida la c, el puente nginx). El planteamiento original, para contexto: ambas cotizaciones traen, bajo «Instalación y Soporte a mediano plazo», 18 meses de «soporte técnico para resolver dudas, capacitar al personal operativo… resolver bugs» después de pedir la máquina virtual a Cómputo: se lee como soporte posterior a la instalación, no como los deploys de la construcción. Opciones: (a) los deploys e incidentes durante la construcción son trabajo del proyecto y los puentes (archivos privados en S3, 2.5 h; proxy nginx hacia Netlify, 0.5 h) son un extra por «necesario para operar»; (b) todo queda dentro de lo cotizado; (c) el puente nginx, que deja el sitio viejo junto a las rutas nuevas, se asigna al renglón «Modificación de versión 1 para compatibilidad» (3,000).

## Síntesis por renglón de la cotización

Esta tabla es la vista contractual (la regla del skill); la vista para entender y negociar es la de «Brecha por concepto y sus causas». Ricardo confirmó el avance de los renglones pagados la noche del 25 de septiembre (cp 85 %, flujo 95 %, el resto como estaba); el bloque se toma como ~100 % para la regla porque lo que falta de cp y del flujo es poco.

| Renglón | Cotizado | % entregado | h antes de IA | h con IA | Costo real | Δ (costo − cotizado) | Por cobrar |
|---|--:|--:|--:|--:|--:|--:|--:|
| Pagado en 2025: dashboard + diseño de BD + soporte de BP | 88,000 | ~100 % | 46.1 | 85.1 | 149,774 | +61,774 | 1,793 |
| Plataforma pública | 43,000 | identidad diseñada, sin implementar | — | 2.0 | 2,600 | — | — |
| Base de datos (Excel e indicadores) | 17,000 | ~0 % | — | — | — | — | — |
| Visualizaciones | 92,000 | 0 % | — | — | — | — | — |
| Automatización de informes | 81,000 | 0 % | — | — | — | — | — |
| Editor del cuestionario y exportación a Word (pedidos, tabla siguiente) | — | — | — | 10.1 | 13,179 | +13,179 | se cobran ([[adr-0022]]) |

El renglón pagado incluye aquí todo lo que no es editor ni Word: también las invitaciones, la institución de prueba y el excedente de buenas prácticas, que la tabla de la brecha separa como pedidos, y los costos no planeados.

«Por cobrar» sigue la regla del skill: cotizado × % entregado − cobrado. Con 88,000 × 100 % − 86,206.90 salen 1,793.10: por la regla estricta casi no hay nada pendiente, **porque la cotización del dashboard era baja**, no porque el trabajo esté pagado. El Δ es lo que la cotización no previó.

Las horas con IA no se repartieron entre los seis sub-renglones del dashboard (poblaciones, preguntas básicas, transversalización, complementarias, flujo de validación, buenas prácticas).

## Extras entregados fuera de la cotización

Ricardo confirmó la noche del 25 de septiembre cuáles de estos se cobran: **todo lo que le pidieron y se excedió** —el excedente de buenas prácticas, el editor del cuestionario, las invitaciones de las IES, la institución de prueba y la exportación a Word—. Lo demás que se hizo fuera de renglón es costo no planeado ([[adr-0022]]). Las horas de cada fila vienen de la tabla de la brecha.

| Extra | Horas | MXN a hoy | Categoría | Causa y evidencia |
|---|--:|--:|---|---|
| Excedente de buenas prácticas sobre sus 12,000 | 19.2 en total | 9,914 (≈15,400 al terminar, con 80 % de avance) | por cobrar | Pedido: creció por la prueba con usuarias del 16 de abril, por los acuerdos del 26 de junio y, en palabras de Ricardo del 4 de septiembre, porque «le fuimos aumentando más cositas y variaciones» |
| Herramienta para que Rubén edite el cuestionario: estandarización de `QuestionType` (`8e146f37`), revisión del cuestionario v2 (`d5ef9c1e`), reseed (`03f1e4b9`), documento integrado y prototipo del 4 de septiembre (`0d557873`) | 8.3 | 10,825 | por cobrar | Pedido por Rubí el 28 de julio, `[37:32]` «No sólo la integración, sino la visualización para que se puedan editar» ([[task-42]]) |
| Invitaciones de las IES | 5.1 (rango 4–7.5) | 5,782 | por cobrar | Pedido así por el cliente, según Ricardo; ninguna reunión grabada lo registra, porque las anteriores a junio no se grabaron. Ver el argumento abajo |
| Institución de prueba («De prueba») | 0.7 | 910 | por cobrar | Pedida en la reunión del 28 de julio, `[26:22]` ([[task-53]]) |
| Exportación del cuestionario a Word: estrategia de Pandoc (`503b55da`) y la sesión del 11 y 22 de septiembre (`b055612f`) | 1.8 | 2,354 | por cobrar | Pedido por el cliente |
| **Subtotal por cobrar** | | **29,785** (≈35,300 con buenas prácticas terminada) | | |
| Puente de archivos privados en S3 (`4328191a`, 2.49) y proxy nginx hacia Netlify (`f94b34b0`, 0.52) | 3.0 | dentro de los 10,272 de infraestructura | no planeado | Necesario para operar mientras no hay servidor UNAM |

**El argumento de las invitaciones, por si Rubén lo discute.** La cotización de 2026 promete, en «Otras mejoras», «la posibilidad de enviar un link con un token para que sean las IES las que gestionen por su cuenta sus contraseñas». Eso es recuperación de contraseña, y está hecha dentro de la base del dashboard. Lo que se construyó para las invitaciones es otra cosa: el modelo `InvitationToken`, el listado de invitaciones con su estado y su reenvío (`sent_at`), el alta de personas usuarias staff y el envío desde la cuenta institucional de correo. Es un sistema de alta de instituciones, no un link de contraseña. Las horas: 0.5 en git (26 de enero, «avanzo en tokenInvitation»), 2.5 del historial de febrero–marzo y 2.1 de sesiones de mayo, sobre todo el 20–22 («gestionar mejor invitaciones y personas usuarias staff»). Después hubo ajustes pedidos por Fernanda el 6 de agosto ([[task-63]], [[task-64]]).

## Brecha por concepto y sus causas

Esta sección responde otra pregunta que las anteriores: no cuánto falta cobrar, sino **en qué conceptos el trabajo real se separó de lo cotizado, por qué, y qué hacer para que no se repita** en los 233,000 pendientes. Parte de las mismas horas del record, sin el adelanto de identidad gráfica (141.3 h, 162,953 MXN), repartidas entre los renglones de la cotización de septiembre de 2025 con `lines.py` (misma carpeta de scripts): cada sesión según sus prompts y los archivos que tocó, cada día del historial según lo que dicen sus prompts, cada día de git según los archivos de sus commits, y lo declarado según a qué sirvió. La suma da 162,965 MXN; los 12 de diferencia con el record son redondeo del cociente de git.

**Ajustes de Ricardo de la noche del 25 de septiembre**, ya aplicados: la conceptualización en Miró va al flujo de validación, no a coordinación; el cuestionario por observable está al 85 % y el flujo al 95 %; las invitaciones y la institución de prueba salen de la base del dashboard como pedidos; entran sus 8 h de reuniones sin grabación y sus 8 h de análisis y construcción de la base de datos.

Las columnas: **Cotizado** es el monto del renglón. **Costo a tarifa** son las horas atribuidas por 850 (antes del 2 de marzo) o 1,300. **Diferencia** es costo menos cotizado: positiva quiere decir que trabajaste más de lo que el renglón pagaba. **% de avance** lo fijó Ricardo, y **Al 100 %** divide el costo entre ese avance. **Categoría** es la de [[adr-0022]]: *por cobrar* es lo pedido que se excedió; *no planeado* se registra y se factura prorrateado.

| Concepto | Cotizado | Horas | Costo a tarifa | Diferencia | Avance | Al 100 % | Categoría | Confianza de la atribución |
|---|--:|--:|--:|--:|--:|--:|---|---|
| Diseño de nueva base de datos (con las 8 h de análisis declaradas) | 8,000 | 14.3 | 12,195 | +4,195 | 100 % | 12,200 | exceso no planeado | media: días de git de diciembre y enero, más lo declarado |
| Poblaciones (la sección de información base, `gen`) | 16,000 | 11.4 | 14,830 | −1,170 | ~95 % | 15,600 | | alta: sesiones de agosto |
| Preguntas de institucionalización, transversalización y complementarias (el cuestionario por observable, `cp`: 5,000 + 14,000 + 8,000) | 27,000 | 9.5 | 12,375 | −14,625 | 85 % | 14,600 | | media |
| Flujo de validación con estatus y comentarios (con Miró) | 25,000 | 20.3 | 23,729 | −1,271 | 95 % | 25,000 | | media: la primera versión (StatusControl) quedó mezclada en los días de git |
| Buenas prácticas (subir y aprobar, 7,000; subir y mostrar, 5,000) | 12,000 | 19.2 | 21,914 | +9,914 | ~80 %: falta la parte pública | 27,400 | excedente por cobrar | media |
| Base del dashboard: acceso, registro, recuperación de contraseña, usuarios staff, catálogos, colecciones, diseño | sin renglón | 21.5 | 23,815 | +23,815 | ~100 % | 23,800 | no planeado | media |
| **Subtotal de lo pagado en 2025** | **88,000** | **96.2** | **108,858** | **+20,858** | | **118,600** | | |
| Invitaciones de las IES | — | 5.1 | 5,782 | +5,782 | 100 % | 5,800 | por cobrar | media: febrero–marzo por proporción de prompts; mayo por herramientas |
| Institución de prueba | — | 0.7 | 910 | +910 | 100 % | 900 | por cobrar | media: no se volvió a medir |
| Editor y estandarización del cuestionario para Rubén | — | 8.3 | 10,825 | +10,825 | 100 % | 10,800 | por cobrar | alta |
| Exportación del cuestionario a Word | — | 1.8 | 2,354 | +2,354 | 100 % | 2,400 | por cobrar | alta |
| Infraestructura: deploys, puentes S3 y nginx, Netlify, correo en producción | — | 7.9 | 10,272 | +10,272 | continuo | — | no planeado | media |
| Reuniones grabadas (seis, junio–septiembre) | — | 6.0 | 7,843 | +7,843 | continuo | — | no planeado | alta |
| Reuniones sin grabación (antes de marzo) | — | 8.0 | 6,800 | +6,800 | — | — | no planeado | declarado |
| Transcripciones y planeación de sesiones | — | 7.2 | 9,321 | +9,321 | continuo | — | no planeado | media |
| **Subtotal fuera de renglón** | **—** | **45.0** | **54,107** | **+54,107** | | | | |
| **Total** | **88,000** | **141.2** | **162,965** | **+74,965** | | | | |

### El desborde, en las dos categorías de Ricardo

| Componente | MXN |
|---|--:|
| **Por cobrar**: excedente de buenas prácticas 9,914, editor 10,825, invitaciones 5,782, Word 2,354, institución de prueba 910 | **+29,785** |
| Base del dashboard sin renglón | +23,815 |
| Infraestructura y deploys | +10,272 |
| Reuniones grabadas | +7,843 |
| Reuniones sin grabación | +6,800 |
| Transcripciones y planeación | +9,321 |
| Exceso del diseño de la base de datos | +4,195 |
| **Costos no planeados** | **+62,246** |
| Renglones por debajo de su precio: cuestionario −14,625, flujo −1,271, poblaciones −1,170 | −17,066 |
| **Desborde neto a hoy** | **+74,965** |

Al terminar, el cuestionario deja un margen de unos 12,400 (no 14,600), el flujo cierra en su precio y buenas prácticas sube su excedente a unos 15,400. Lo por cobrar queda en unos 35,300.

### Lo que dice la tabla

**1. Los módulos con nombre se estimaron bien.** Los cinco renglones con precio, llevados al 100 %, costarían unos 94,800 contra 88,000 cotizados: 8 % arriba. Poblaciones, flujo y el cuestionario caben en su precio (el cuestionario con holgura); la base de datos se pasa por el análisis que no dejó huella. El único renglón con nombre que se desborda de verdad es buenas prácticas: 19.2 h contra un precio que a 1,300 la hora alcanza para 9.2, y es por pedidos.

**2. La brecha está en lo que no tiene renglón.** Base del dashboard (23,800), coordinación (reuniones grabadas y no grabadas, transcripciones y planeación: 24,000) e infraestructura (10,300) suman unos 58,000: **el 36 % de todo el costo**. La cotización sí promete parte de eso en su texto —«la nueva plataforma deberá ser fácilmente editable», la instalación en una máquina virtual de Cómputo— pero ningún renglón lo tiene con precio, y las reuniones no aparecen en ninguna parte. Ese es el error de estimación principal: no faltó precio en los módulos, faltaron renglones.

**3. Lo pedido durante la construcción suma unas 23.5 h y 29,800.** El editor del cuestionario lo pidió Rubí en la reunión del 28 de julio, `[37:32]` «No sólo la integración, sino la visualización para que se puedan editar» ([[task-42]]); la institución de prueba, en la misma reunión, `[26:22]` ([[task-53]]); las invitaciones, en palabras de Ricardo, «me lo pidieron así»; la exportación a Word, después. Buenas prácticas creció por la prueba con usuarias del 16 de abril ([[2026-04-16-prueba-con-usuarias-reales]]), por los acuerdos del 26 de junio ([[2026-06-26-seguimiento-pendientes-ruben]]) y, en tus palabras del 4 de septiembre, porque «le fuimos aumentando más cositas y variaciones».

**4. El retrabajo propio es chico.** El incidente del 12 de agosto ([[2026-08-12-incidente-migrate-flow-data]]: una segunda corrida en producción de la migración de estatus aplastó 179 estatus, que se restauraron) y la reparación de `sent_at` suman 2.2 h, y caen dentro del renglón del flujo sin desbordarlo. Traer de OCSA la lógica de colecciones y `ps_schema` (enero y junio) y preparar Fedora suman 5.3 h.

### Horas por causa

Aproximado: la base del dashboard y la inversión propia se partieron en proporción a sus horas.

| Causa | Horas | MXN aprox. | Qué incluye |
|---|--:|--:|---|
| (a) La cotización no tenía renglón para eso | 37.6 | 42,100 | Base del dashboard sin los puertos de OCSA (16.4 h) y la coordinación: reuniones grabadas y sin grabar, transcripciones y planeación (21.2 h) |
| (b) Pedido por el cliente durante la construcción | 23.5 | 29,800 | Editor (8.3), invitaciones (5.1), Word (1.8), institución de prueba (0.7), lo que buenas prácticas excede su renglón (~7.6) |
| (c) Necesidad de operar o falla externa | 7.0 | 9,200 | Puentes S3 y nginx mientras no hay servidor UNAM, Netlify en monorepo, deploys, correo en producción |
| (d) Retrabajo propio | 2.2 | 2,900 | Incidente del 12 de agosto y `sent_at`; dentro del renglón del flujo, no agranda la diferencia |
| (e) Inversión propia | 5.3 | 5,800 | Puertos de OCSA (colecciones, `ps_schema`, catálogos) y preparación de Fedora |
| (f) Subestimación de un renglón con nombre | 8.0 | 6,800 | El análisis de la base de datos fuera de sesiones |

⚠️ Tu decisión, en [[task-179]]: si (e) es inversión propia, el skill dice que no se factura y el costo baja unos 5,800.

### Cómo cerrar la brecha en lo pendiente

La estimación de lo que falta, con las cifras de Ricardo, está en la sección siguiente. Las palancas:

1. **Poner precio a lo invisible.** En este proyecto, de cada 100 horas, 15 fueron coordinación y 6 infraestructura. En la próxima cotización (o en la adenda de lo pendiente) van como renglón propio o como una reserva de un 20 % sobre cada módulo; las reuniones también pueden cobrarse por hora. La plataforma pública tendrá su propia «base» (el sitio sin sesión, su despliegue en el servidor de la UNAM, [[task-100]]), que hoy tampoco tiene renglón.
2. **Cada pedido nuevo, con su estimación antes de construirlo.** Las 23.5 h pedidas no las absorbió ningún renglón. Basta una línea en la task donde nace el pedido —ya citan el minuto de la reunión— con «cambio pedido: N h, M MXN», y avisar a Rubén en el momento. Él mismo lo abrió el 4 de septiembre, `[29:01]` «Tratemos de que no trabajes más de lo que ya cotizaste».
3. **Medir mientras se construye.** Con `credit.py` y `lines.py` se puede ver cada mes cuánto lleva cada módulo contra sus horas de presupuesto, y levantar la mano al llegar a la mitad, no al final.
4. **La velocidad con IA ya está en los precios.** Los módulos construidos con IA (poblaciones, 11.4 h; el flujo reescrito) cupieron en su precio cobrando 1,300 la hora. Los datos no dicen que los renglones estén caros o baratos; dicen que alrededor de cada módulo hay trabajo que nadie cotizó. Que las visualizaciones ahora sean «súper rápidas» todavía no se puede medir (llevan 0 h); Ricardo les pone un tope de 40 h contra las 71 que pagan a 1,300.
5. **La infraestructura de la construcción es costo no planeado** (Ricardo, [[adr-0022]]). Si la cláusula de soporte de 18 meses la cubre o no frente a Rubén sigue abierto en [[task-179]]; en lo pendiente, la máquina virtual y sus trámites llevan su propio renglón.

### Lo más débil de esta atribución

- Los 20 h de git (diciembre–febrero) se reparten por los archivos de cada día; un día con commits de buenas prácticas y de la base se partió a ojo.
- Los 24.5 h del historial de junio–julio se reparten leyendo los prompts de cada día, y junio mezcla flujo y buenas prácticas casi en cada prompt.
- La frontera entre el editor y el cuestionario por observable: la estandarización de `QuestionType` y la resiembra cuentan como editor; si parte era estructura del cuestionario, `cp` sube y el editor baja.
- La coordinación incluye sesiones de planeación que podrían repartirse entre los módulos que planeaban.
- Los porcentajes de avance los fijó Ricardo de memoria, no con una revisión por funcionalidad; la columna «Al 100 %» depende de ellos.
- Las invitaciones de febrero–marzo salen del historial repartido por proporción de prompts (rango 4–7.5 h); las de mayo mezclan invitaciones con la gestión de personas usuarias staff.
- Las 8 + 8 h declaradas las dio Ricardo de memoria: las reuniones sin grabación como piso («al menos 8 horas»), el análisis de la base como cifra aproximada.

## Lo que falta: estimación con IA y el harness

Estimación del 25 de septiembre, construida en diálogo: el coordinador propuso rangos y Ricardo los corrigió con lo que ya sabe de su propia velocidad. Las cifras de Ricardo mandan sobre las del modelo. Todas a 1,300 MXN/h.

| Renglón | Cotizado | Horas | Costo | Supuesto clave |
|---|--:|--:|--:|---|
| Diseño de nueva identidad gráfica | 16,000 | 3–6 de implementación, estimación del asistente (más las 2 ya hechas) | 4–8k (más 2,600 ya hechos) | Ya existe, hecha con Claude Design, y gustó mucho ([[2026-09-25-identidad-grafica-en-claude-design]]) |
| Configuración base de vistas del sitio público | 17,000 | 10–16 | 13–21k | Páginas por IES, contenidos editables, SEO |
| Interactividad web y fichas intermedias | 7,000 | 4–6 | 5–8k | |
| Modificación de la versión 1 para compatibilidad | 3,000 | 2–3 | 3–4k | Lo histórico se conecta por liga, no se integra ([[adr-0021]]) |
| Exportaciones a Excel | 12,000 | 5 (tope de Ricardo) | 6.5k | Dos exportaciones con `xlsx_django_export`: la de cada IES con sus datos en cualquier estado y la pública solo con lo aprobado |
| Cálculo de indicadores y ponderaciones | 5,000 | 2–3 | 3–4k | Lo hace el asistente en corto con las definiciones cerradas; la decisión metodológica (≈3 h de reunión con Rubén + ≈3 h de Ricardo, [[task-28]] y [[task-29]]) va a coordinación |
| Visualizaciones (seis renglones) | 92,000 | 30–40 (tope de Ricardo: 40) | 39–52k | El índice llega cerrado antes de graficarlo |
| Automatización de informes | 81,000 | 31–49 | 40–64k | Plantillas completas del cliente o un kit como el de OCSA; los multianuales hasta que existan varios años de datos (2027 o después) |
| **Subtotal cotizado** | **233,000** | **87–128** | **113–166k** | |
| Instalación y trámites de la máquina virtual de la UNAM *(sin renglón)* | — | 6–12 | 8–16k | El trámite no ha empezado ([[task-102]]); la espera ante Cómputo no se controla |
| Coordinación, ~15 % *(sin renglón)* | — | 13–20 | 17–26k | Incluye las ≈6 h de la metodología del índice |
| **Total** | **233,000** | **106–160** | **138–208k** | |

**Por qué las visualizaciones pueden ser rápidas.** La gráfica misma, con d3, el skill de dataviz y el patrón de colecciones ya resuelto, es una sesión de unas 6 horas o menos. Lo único que podía volverla lenta era que el cálculo del índice no estuviera decidido, porque «Índices agregados» (40,000) grafica justo eso. Ricardo lo resuelve con una reunión de ≈3 horas con Rubén más ≈3 horas propias, que cubren la ecuación del índice y su agregación ([[task-28]]) y sus condiciones base ([[task-29]]). Con eso el índice llega cerrado a las visualizaciones.

**Los informes, y por qué son la palanca.** El renglón promete PDFs terminados por institución, con diseño editorial, una vista editable en el dashboard y redacciones por nivel de avance. Ricardo ve dos caminos, y la recomendación es combinarlos: (1) exigir al cliente un par de plantillas completas y automatizarlas en corto —Opus 5.5, o lo que venga después, resuelve los informes uno a uno con mucha precisión, y la exportación a Word de septiembre ya trae la base (`python-docx` sobre el documento maquetado del cliente)—; (2) el modelo del kit que Ricardo le hizo a Paola en OCSA (una carpeta con un `CLAUDE.md` que hace preguntas aclaratorias, referencias del esquema y ejemplos, con la que ella misma exploró los datos y escribió su informe): dejarles la herramienta y que ellos la ajusten. Eso cambia lo que promete el renglón, y es la moneda de cambio con Rubén para compensar el desborde ([[task-180]]). Lo que ningún camino resuelve solo: las «descripciones de cada nivel de avance» que la cotización promete no tienen todavía ningún nodo. Rubén puso los informes en 2027, y Ricardo no quiere task del módulo hasta que se la pidan; lo que se abre ahora es la negociación, no la construcción.

**La cuenta que importa para la negociación.** Lo pendiente deja un margen de **22,400 a 92,400** contra lo cotizado (25,000 a 95,000 menos los 2,600 de identidad gráfica ya gastados a cuenta de ese renglón). El desborde bruto a hoy es de **~92,000**: 29,800 pedidos más 62,200 no planeados (el neto de 75,000 ya descuenta lo que va por debajo). En el mejor escenario, el margen de lo pendiente compensa casi todo; en el peor, una cuarta parte. Por eso el argumento queda así: los extras pedidos se cobran aparte sí o sí; lo no planeado se prorratea contra el margen de visualizaciones e identidad (el del cuestionario es de 2025 y ya está descontado en el neto de 75,000); y los informes con plantillas o kit protegen ese margen.


## Lo que falta declarar (el costo real es mayor)

Ya declarados el 25 de septiembre y sumados: las reuniones sin grabación (8 h, [[2026-09-25-reuniones-sin-grabacion]]), el análisis y construcción de la base de datos (8 h, [[2026-09-25-analisis-y-construccion-de-la-base]]) y la identidad gráfica en Claude Design (2 h, [[2026-09-25-identidad-grafica-en-claude-design]]). Siguen sin declarar:

- **Preparación de las dos cotizaciones** y del informe de actividades de diciembre de 2025.
- **Días sin commit en diciembre–febrero**, que el git no ve.
- **Costos de terceros** (se suman al costo, no son horas): el servidor de Yeeko donde corre la API, el bucket S3 `onigies-v3-temporal` y Netlify. El repo no dice quién los paga ni cuánto cuestan (⚠️ en [[task-179]]).

Cada uno se declara con `offline_minutes` en un nodo del grafo y el script lo suma solo. A 850 o 1,300 la hora, cada cinco horas declaradas mueven el total entre 4,250 y 6,500.

## Migración de bitácoras de la madrugada del 25 de septiembre

Para esta estimación se migraron primero las sesiones de ONIGIES de Windows al archivo `~/.claude/session-logs-archive/projects/-home-rick-dev-unam-onigies/` (skill `migrate-session-logs`).

- **Fuentes**: el disco de Windows (`D--dev-unam-onigies`, 25 sesiones del 20 de mayo al 13 de junio; `D--dev-unam-onigies-api`, 1 sesión del 20 de mayo) y el respaldo RAR del `~/.claude` de Windows del 2026-04-25 (`D--dev-unam-onigies`, 19 sesiones del 15 y 16 de abril; `-api` y `-nuxt`, solo directorios de subagentes de febrero–marzo sin sesión madre; `--claude-worktrees-gallant-jemison`, un directorio). La Surface no tiene nada de ONIGIES.
- **Mapa de rutas**:

| Ruta en Windows | Ruta en Fedora |
|---|---|
| `D:\dev\unam\onigies` | `/home/rick/dev/unam/onigies` |
| `D:\dev\unam\onigies_api` | `/home/rick/dev/unam/onigies/api` |
| `D:\dev\unam\onigies_nuxt` | `/home/rick/dev/unam/onigies/nuxt` |
| `C:\Users\rick_\.claude` | `/home/rick/.claude` |
| `D:\dev\ibero\ocs-django-db` | `/home/rick/dev/ibero/ocsa/api` |
| `D:\dev\ibero\ocsa-nuxt` | `/home/rick/dev/ibero/ocsa/nuxt` |
| `D:\dev\open\xlsx_django_export` | `/home/rick/dev/open/xlsx_django_export` |

  Sin mapear a propósito: el virtualenv `D:\env\onigies\…`, `AppData`, `hotspot-vpn` y `C:/Temp/bugfix.patch`.
- **Sesiones**: 45 copiadas, 0 omitidas, 0 forzadas, más 14 directorios `<uuid>/`, 9 de ellos huérfanos. `history.jsonl` recibió las 273 líneas de ONIGIES de Windows. `--fix-relative-seps` apagado.
- **Memoria**: la revisión quedó diferida por decisión de Ricardo; esperan cuatro tarjetas de Windows (`email-smtp-microsoft365`, `feedback_docstrings_es`, `feedback_minimal_queryset`, `email.md`), en [[task-179]].
- **Harness**: el script de migración ahora copia los directorios de subagentes huérfanos y trae un extractor del RAR; el skill documenta el RAR como tercera fuente y la colisión de prefijos (`D:\dev\x` también reescribe `D:\dev\x_api`). Commit `efd927e` en `~/.claude`.

Lo que ninguna fuente conserva: las sesiones madre de febrero–marzo (ya podadas en abril) y las de Fedora del 16 de junio al 4 de julio (borradas por la retención antes de que se desactivara el 20 de agosto; del 5 al 27 de julio no hay rastro de trabajo en ONIGIES). Por eso esos periodos van por historial.

## Cambios a las herramientas

- `credit.py` solo leía el árbol vivo del proyecto; ahora lee también su gemelo en el archivo (deduplicando por `uuid`) y, en el reparto global, no carga dos veces un proyecto que existe en los dos árboles. Sin esto, abril–junio no entraba en la cuenta. La copia canónica en OCSA no se tocó.
- `blind.py` es nuevo: la calibración del historial que el skill describe y ningún script hacía. Calibra con horas netas y lee de `cost-audit.json` las exclusiones de días y el corte del 06-20.
- `credit.py` no reconocía como pegada una página de error de Django (el volcado de `settings` y las líneas «Request Method:», «Django Version:», rutas de Windows). Una sola sesión del 25 de mayo, `a354126c`, de seis minutos, cargaba 24,788 caracteres de esa página como si Ricardo los hubiera tecleado: 3.4 h de escritura inexistente. Corregido al preparar la sección de la brecha; el total bajó de 131.5 a 125.3 h (de 156,800 a 149,400 MXN), porque el arreglo también baja los cocientes de calibración. El `credit.json` anterior queda como `credit-2026-09-25-antes-de-la-pagina-de-debug.json`. La copia de OCSA tiene el mismo hueco.
- `lines.py` es nuevo: reparte las horas netas entre los conceptos de la cotización (sección «Brecha por concepto y sus causas»). Los mapeos de sesión y de día son lectura, no medición.
- `cost-audit.json` excluye esta sesión y guarda las fracciones facturables por sesión (`billable_fraction`), los días ciegos excluidos y el corte del 06-20.
- La auditoría de congruencia del cierre no se corrió, por instrucción de Ricardo; sí se corrió el crítico, y sus hallazgos están aplicados en este record.

## Advertencias

- Los cocientes del historial vienen de días con mucha concurrencia (agosto–septiembre); si en febrero–marzo o junio Ricardo tenía menos proyectos abiertos, esos periodos están subestimados.
- **Abril–junio lee alto.** El reparto entre proyectos solo ve lo que está en `~/.claude/projects/` y en el archivo. Proyectos de Windows que corrieron los mismos días que ONIGIES nunca se migraron: `clientes-yco-data` (20 de mayo), `yeeko-written-django` (10 de junio; el directorio de Fedora no tiene sesiones de mayo–junio) y `open-sanginiela` (11 al 13 de junio), además de los proyectos del RAR que no se extrajeron (la concurrencia del 15 y 16 de abril no se revisó). Sin ellos, ONIGIES se queda con instantes que debía compartir. El tamaño no se midió; conviene migrarlos o revisar la concurrencia antes de llevarle la cifra a Rubén.
- **Reuniones sin hora de inicio** (26-jun, 28-jul, 6-ago): pueden contar dos veces con sesiones que corrían al mismo tiempo; en las tres con hora el traslape medido fue de 0.3 h.
- La tarifa de la conceptualización en Miró (850) supone que fue antes de marzo; si fue después, sube 2,700.
- Los estimados generados por IA son referencia; lo que Ricardo declare manda sobre ellos.

---
type: record
id: 2026-08-12-sesion-orquestada-a-b-captura-correcta
title: "Sesión A+B: la captura correcta y el modelo de preguntas, en una sola noche orquestada"
date: 2026-08-12
related: ["[[2026-08-11-cierre-de-sesion-duo-reunion-auditorias-y-reorganizacion]]", "[[adr-0012]]", "[[adr-0008]]"]
---

# Sesión A+B: la captura correcta y el modelo de preguntas, en una sola noche orquestada

Sesión del 12 de agosto de 2026, corrida hasta la madrugada con Fable 5 como coordinador y ejecutores Opus. Arrancó como la «Sesión A» acordada el día anterior (la captura correcta para la ventana miércoles→jueves) y terminó absorbiendo la Sesión B completa por decisión de Ricardo. Commits: `ee549df` (docs), `943c7ac` (implementación), `eb2ecc1` (e2e). Fue además el laboratorio del futuro skill `orchestrator`.

## El arreglo previo: 31 citas de ruta

Antes de tocar tareas se repararon los errores que bloqueaban el pre-commit. Hallazgo de encuadre: el grafo ADR estaba sano — cero `[[id]]` rotos; los 31 errores eran citas `[ruta]` a archivos inexistentes (prefijo `api/` obsoleto, rutas elididas, un documento mudado). `research_guide.md` migró al repo global como `reference` (sus citas genéricas a `.claude/` solo validan allá); Ricardo confirmó después que se queda así. Cuatro nodos recibieron `validate-paths: false`; en los records es defendible (fotografías), en task-25 y task-42 desactiva la validación a futuro — señalado por la revisión crítica, se acepta.

## Las decisiones de Ricardo del día

Resueltas por AskUserQuestion y prosa, en orden aproximado:

- **`sectors`**: renombrar el M2M a `sectors_legacy` con la propiedad derivada tomando el nombre, «con miras a borrarlo muy pronto para que no haya dos fuentes de verdad» ([[task-118]]).
- **Filas omitidas**: el backend deja de borrar por omisión (upsert puro). Regla de limpieza: marcar `no_apply` o `is_present=False` anula los conteos de la fila, en front y back.
- **Alcance del tri-estado**: poblaciones + los 2 extras; autoridades no. El «No aplica» de autoridades va al final, después del Total (posición delegada al coordinador).
- **Compuerta**: guardar libre, transición bloqueada; después se extendió a `gen_adjusted` y, tras la revisión, se duplicó en el backend.
- **Pregunta previa**: nace como `GeneralQuestion` — lo que llevó a adelantar la Sesión B entera: «Hoy todo… no dejemos deudas técnicas de algo tan fundamental». El dimensionador había mostrado que 107 tenía traslape cero con la Sesión A y que 113 era la única riesgosa; se hizo de todos modos, con orden estricto: 107 backend → 113 → features → 108 en paralelo → 106 al final.
- **Rótulo**: «No binarie»; columna oculta sin flag; tercera opción en el radio de la titular con flag activo; conteo no binario obligatorio en filas presentes cuando el flag está activo (ratificado tras la revisión).
- **`unit`**: octavo campo de GeneralQuestion, con `label` cayendo a `unit` cuando está vacío. **Gobierno**: una sola booleana `is_centralized` con las opciones en `addl_config`.
- **Seed vs edición**: «textos solo al crear» (`create_defaults`), tras verificar que hoy no se borra nada (el seed no toca Feature/FeatureOption y nadie ha editado gen). Costo asumido y documentado: cambios de redacción en semilla ya no bajan a filas existentes; el flag `--force-texts` se descartó.
- **`hint`**: promovido de `addl_config` a campo editable cuando Ricardo detectó que como JSON el equipo de Rubén no podría corregirlo.
- **«Ninguna pregunta debe morir»** una vez implementado: FK `PROTECT` en las respuestas y DELETE bloqueado por API en los catálogos nuevos; en fase de pruebas se borra vía seed/ORM.
- **Planes de estudio**: ganan «No aplica» por fila (0 = tiene el nivel sin planes; No aplica = no tiene el nivel); solo los 3 planes, las instancias no. El mecanismo pasó por una reversión (abajo) y quedó en `GeneralQuestionResponse`, modelo aparte «no importa el tiempo».
- **Mudanza de valores**: esta misma noche, sesión dedicada — [[task-117]] con sus 4 resoluciones.
- Las reglas madre de validación (null bloquea, false/No aplica exime, **el 0 es 0**) y la redacción final de la pregunta previa («En sus registros de sexo y género, ¿su institución contempla la categoría no binaria?», Rubén revisará) salieron del diálogo satélite que sí funcionó, antes de que el experimento se cancelara.

## El experimento satélite y su veredicto

Se probó delegar el diálogo de decisiones a una sesión paralela (`onigies-a1`). Funcionó a medias: entregó las reglas de validación y la redacción, pero **cerró por Ricardo una pregunta que él había dejado explícitamente abierta** (el mecanismo del «No aplica» de planes: mandó «3 booleanos en Survey» como resuelto) e inventó candidatos sin sentido (`is_estimated`, `no_data`). Ricardo frenó en caliente: ALTO parcial al ejecutor backend — que ya había implementado los flags y los revirtió por completo, dejando la 0009 en sus 5 operaciones — y el diálogo regresó a la sesión principal, donde se resolvió el join-row. Veredicto de Ricardo, literal: «tener agentes paralelos que no tienen todo el contexto es una pésima idea, solo complica todo». Un segundo intento de worker session (`onigies-7a`, para la mudanza) murió por no poder invocar duo y llenarse de contexto leyendo archivos; la mudanza se relanzará en fresco sobre base commiteada. Ambos aprendizajes quedaron en el skill.

## La revisión crítica y sus frutos

Al terminar la implementación, un revisor independiente (Opus fresco, reconstruyendo las decisiones desde las transcripciones, sin narrativa del coordinador) auditó congruencia decisión por decisión. Encontró un bloqueante que todos los verdes locales escondían — **D1: los textos de grupo jamás llegarían a producción**, porque «textos solo al crear» + filas ya existentes en prod + componentes que ya borraron sus textos hardcodeados = tablas sin instrucciones el viernes; se corrigió con backfill inline dentro de `indicator/0009`, idempotente y que no pisa ediciones. También D2 (el `text-body-1` solo se había aplicado a la mitad del módulo) y las observaciones que llevaron a la compuerta backend, el bloqueo de DELETE, ocultar `sectors_legacy` del API y limpiar el copy del editor. Todo corregido y re-verificado la misma noche.

## Verificación final

Smoke de navegador contra el stack local real: **9 de 9 pasos**, cero errores de consola, incluida la compuerta con su señalamiento y el espejo backend (mismo 400 con los mismos textos por API directa). Suite e2e: de 27 a **37 specs en verde** (gen-capture, gen-non-binary, gen-validation-gate), estables con repetición; `nuxt/TESTING.md` al día con la credencial CIAD para prueba manual. pytest 74, `makemigrations --check` limpio. Pendientes menores registrados: [[task-119]], [[task-120]], [[task-121]] y la nota accesible en [[task-96]].

## El skill orchestrator

Nació en el repo global (`~/.claude/skills/orchestrator/SKILL.md`) como **capa sobre duo**, en construcción y no auto-invocable — nombre `orchestrator` decidido por Ricardo. Recoge los aprendizajes de esta sesión: el árbol de calibración de sus intervenciones (trivial/cerrada/deliberación), el batching, el veredicto sobre agentes sin contexto, los semáforos de worker sessions, el piso de modelos (Sonnet solo mecánico — «Sonnet no debería encargarse de algo que requiere tanta inteligencia»), los frenos en caliente y el revisor crítico pre-commit. Su deuda de construcción quedó anotada en el propio skill y en task-13 del grafo general.

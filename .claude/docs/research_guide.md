

# Objetivo: Construir los archivos CLAUDE.md que irán en .claude (de mi usuario global) así como en user/.claude/rules: coding-preferences.md y workflow-preferences.md, o si hiciera falta otro, también.


# Cómo ejecutarás esta tarea:

Tomarás las buenas prácticas que pongo más abajo (Resultado de una investigación al respecto) para intentar implementarlas, también tomarás mi archivo CLAUDE.md que he estado modificando personalmente para que tenga varios de mis objetivos y de la forma en que quiero trabajar, sin embargo, hay que

Quiero que intentes darme realimentación sobre mi contenido inicial de mi archivo CLAUDE.md que te pego en esta conversación y lo que estoy escribiendo en todo este mensaje. Por ejemplo, elimina lo que se repita y si algo ya lo contempla Claude code dentro de sus instrucciones, también hay que eliminarlo, también si hay algo que es innecesariamente verboso.

** Por ahora no construiremos los skills ni los agents, pero sí especificarás al final de que acabemos qué skills y agents me faltan de construir (para darle contexto a otras sesiones de Claude).

 
Explícame qué cambios hiciste y por qué hiciste o sugeriste los cambios.


## Otros detalles que quiero que estén en mis archivos generados:

* Mi objetivo al utilizar la IA generativa en el desarrollo de mis plataformas para que me auxilie en la escritura de código, para que pueda avanzar más rápido y también para que me ayude a generar soluciones, investigar y proponer (en conjunto conmigo y con mis ideas) posibles soluciones. 

* Para mí es fundamental ir leyendo el contenido propuesto, la mayoría de las veces hago modificaciones directas en el diff propuesto, o escribo nuevos cambios después de la opción "1. Yes". Si yo no entiendo el código y lo que hace, perderé gran parte de mi valor agradado y dejaré de aprender. También, en muchas ocasiones requiero que la tarea compleja se descomponga en partes más pequeñas. Para ello, es posible que se puedan usar subagentes para proponer la división y proponerme la división en distintas conversaciones, dándome una propuesta de prompt para cada parte.
* Otra de las cosas en las que quiero que me ayude es, ocasionalmente, a explorar y entender otras funciones, métodos y arquitecturas a lo que yo estoy usando, ya que muchas veces uso cosas limitadas por mi conocimiento limitado y me pierdo de buenas prácticas o de otras formas. Cuando eso ocurra (no sé cómo generar la instrucción para ello) me gustaría que me explicara la alternativa antes de implementar cualquier otra cosa.

* Quiero que si el algún momento le pido a Claude Code una tarea compleja sin una aproximación propia, me preguntes de modo abierto cuál es mi idea (sin darme opciones cerradas para no predisponerme). El objetivo acá es que no deje de pensar lo que estoy haciendo, lo que estoy pensando. Conversar acerca de lo que se hará (sí es complejo) es fundamental previo a hacer el plan o de proponer los cambios. Es importante que todo el tiempo el agente me rete a pensar para que la solución sea lo más conjunta posible.


# CLAUDE.md — Instrucciones generales para AI Code Assistants

Este archivo define el comportamiento esperado del asistente en todos los proyectos con Claude Code.

---

## Modo de comunicación y toma de decisiones

- **Piensa antes de codificar (Modo Plan):** Para tareas complejas, genera primero un paso a paso de lo que vas a modificar. Discute el enfoque conmigo antes de escribir una sola línea de código. Si el usuario proponga una idea, no la tomes como ley, critícala y cuestiona, de modo tal que siempre pueda aprender alternativas, incluso si es la solución ideal, explica por qué es mejor que otras alternativas
- **Nunca asumas decisiones relevantes sin preguntar.** Si existe más de una solución viable, preséntala como opciones con sus ventajas y desventajas, y espera confirmación antes de proceder.
- **Pregunta antes de asumir comportamiento no especificado.** Si el comportamiento esperado no está claramente definido en la solicitud, haz las preguntas necesarias para aclararlo.
- **No asumas, pregunta:** Antes de ejecutar refactorizaciones o aplicar arquitecturas nuevas o funciones complejas nuevas, evalúa si falta información o contexto. Si hay dudas sobre la mejor ruta, detente y preséntame opciones con sus pros y contras.
- **Sé explícito sobre lo que vas a cambiar y por qué.** Antes de implementar cambios importantes o de ejecutar comandos en bash, explica qué se cambiará y cuál es la razón técnica detrás de cada decisión.


---

## Planificación antes de implementar (`/plan`)

- Cuando la solicitud sea compleja, multarchivo o implique refactorización significativa, **activa el modo `/plan` por defecto**, incluso si no se solicita explícitamente.
- El plan debe incluir:
  - Lista de archivos a modificar o crear
  - Descripción breve de los cambios en cada uno
  - Preguntas o decisiones pendientes que requieran confirmación del usuario
  - Discute el enfoque conmigo antes de escribir una sola línea de código.
  - En toda la interacción con plan, siempre pregúntame antes de asumir cualquier decisión, también dame retroalimentación para saber si estoy teniendo el enfoque correcto o si existen otros enfoques.
  - Antes de empezar a escribir los planes, ayúdame a analizar si me falta alguna definición o si estoy perdiendo algo de vista, pregúntame qué agregar a partir de tus propias sugerencias y observaciones.
- **No ejecutes el plan hasta obtener confirmación**.

---

## Análisis y comprensión antes de cambiar

- **Analiza el código existente antes de proponer cambios.** Comprende la lógica actual, identifica dependencias y posibles efectos colaterales.
- **Identifica escenarios no contemplados.** Al revisar una función o lógica, señala activamente los casos borde o flujos que no están siendo manejados.
- **Evalúa si las soluciones actuales siguen las mejores prácticas.** Si identificas anti-patrones o código que podría mejorarse más allá de la solicitud, menciónalos sin implementarlos a menos que se pida.

---

## Minimizar código boilerplate y repetición

- **Identifica y extrae lógica reutilizable** en composables, mixins, clases base, serializadores comunes o utilidades compartidas.
- **Propón la unificación de componentes o módulos similares** cuando dos o más piezas de código hacen esencialmente lo mismo.
- **Usa slots, parámetros y composición** antes que duplicar componentes o lógica.
- **Pregunta si vale la pena separar** cuando el código empieza a ser demasiado largo o tiene responsabilidades mezcladas.


---

## Separación de responsabilidades

- **Los stores (Pinia, Vuex, Redux, etc.) solo deben manejar estado global y persistente.** Estado local de UI como `isLoading`, `showForm`, `showDetail`, `currentObject`, `isEditing` debe vivir en los componentes como `ref` o `useState`.
- **Los serializers, validators y lógica de negocio deben estar separados** de las vistas y controladores.
- **Señala explícitamente cuando se detecte una responsabilidad mal ubicada**, aunque no se haya solicitado revisarla.

---

## Documentación y skills

- **Actualiza `CLAUDE.md` cuando se implementen módulos nuevos o cambios estructurales importantes.** Si el usuario no lo pide, sugiérelo al final de la implementación.
- **Actualiza skills existentes cuando cambie la lógica** que documentan, no dejes documentación desactualizada.

---

## Explicación del código y diagnóstico

- **Cuando el usuario pida entender algo, explica con claridad conceptual**, no solo técnica. Adapta el nivel de detalle al contexto de la pregunta.
- **Cuando haya un error, analiza el stack trace completo** antes de proponer soluciones. Señala la causa raíz, no solo el síntoma.
- **Distingue entre múltiples posibles causas** si el error es ambiguo, y sugiere pasos de diagnóstico en orden de probabilidad.
- **Si puedes ejecutar comandos para diagnosticar, hazlo** antes de asumir la causa del problema.

* **Explicación sobre Ejecución:** Cuando te pida entender un error, una arquitectura o un concepto, prioriza la enseñanza. Explícame el "porqué" de las cosas antes de darme el bloque de código solucionado.

---


## Comportamiento general

- **Si una solicitud está incompleta o tiene ambigüedad crítica, pregunta antes de asumir.**



# El siguiente código salió de un archivo CLAUDE.md real de un proyecto de django. También ayúdame a incorporar sus instrucciones

## Code Style Rules

- **Interface messages** (user-facing strings, API responses, admin labels) must be in **Spanish**
- **Code** (functions, variables, class names, file names) must be in **English**
- **Line width limit: 80 columns** — wrap only lines that exceed this
- Build with **typing hints and docstrings** for all views, serializers,
  and complex functions.
- When asked for advice on approach: answer first, then ask for confirmation before writing any code
- When some bash commands are needed, explain why is necessary to run them, and what they do, before writing the command itself. If the command is not trivial, break it down into multiple steps and explain each one.
- Avoid boilerplate and repetition by leveraging DRF's generic views, mixins, and the `BaseViewSet` where possible. If the standard suggest that, answer before choose the best approach for the specific case.
- Never execute `makemigrations` or `migrate` commands yourself. I will to execute manually after review post session the changes.


## Creating new Views
- **APIView vs ViewSet**: Use `views.APIView` for non-model or custom
  auth endpoints (login, recovery, etc.). Use `BaseViewSet` /
  `BaseGenericViewSet` (from `api/views/common_views.py`) for standard
  model CRUD.
- **Request validation**: Always validate `request.data` through a DRF
  serializer — never access it directly via `.get()`. Use
  `serializer.is_valid(raise_exception=True)` so DRF handles the 400
  response automatically.
- **Error response format**:
  - Field errors (auto via `raise_exception=True`): serializer errors
    dict returned directly → HTTP 400
  - Single non-field message: `{'detail': '...'}` → appropriate status
- **Serializer location**: Place serializers for a given sub-package in
  `api/views/{sub-package}/serializers.py`
  (e.g., auth views → `api/views/auth/serializers.py`).
- Import the serializers and common elements at the beginning of the
  file, and then define the views.
## QuerySet optimization for nested serializers
Every time a View or its related Serializers are created or modified,
follow this checklist to prevent N+1 queries:

1. **Inspect serializer fields for relations.** Check every serializer
   referenced in `action_serializers` (list, create, retrieve, update,
   etc.). Identify fields that traverse relationships — nested
   serializers, `source="rel.field"` declarations,
   `SerializerMethodField`s that access related objects, and any
   `StringRelatedField` or `SlugRelatedField` pointing to a FK/M2M.

2. **Ensure the base `queryset` covers the common case.** Add
   `select_related()` for ForeignKey / OneToOne lookups and
   `prefetch_related()` for reverse FKs / ManyToMany lookups that are
   shared by most or all actions. This is the default defined at the
   class level (`queryset = Model.objects.select_related(...)`).

3. **Decide whether to override `get_queryset()` per action.**
   - **Override when** different actions have significantly different
     nesting depth. For example, `retrieve` may use a deeply nested
     serializer (multi-level joins) while `list` only needs shallow
     fields. Keeping the heavy prefetches on every action wastes
     database work. In that case, override `get_queryset()` and branch
     on `self.action`:
     ```python
     def get_queryset(self):
         qs = super().get_queryset()  # base queryset
         if self.action == 'retrieve':
             qs = qs.prefetch_related(
                 'deep_relation__nested_relation',
             )
         return qs
     ```
   - **Do not override when** the difference is minor — e.g., only one
     action uses a single extra shallow prefetch that the others
     ignore. In that case, just include it in the base `queryset`.
     A small unused prefetch is cheaper than the added complexity of
     a branched `get_queryset()`.

4. **Rule of thumb for the threshold.** If the extra prefetch adds a
   new join level (nested `Prefetch` objects, or chained double-
   underscore paths like `a__b__c`) and is only needed by one action,
   override `get_queryset()`. If it is a single flat
   `prefetch_related('simple_rel')`, keep it in the base `queryset`.



## INFO EXTRA, recomendaciones sacadas de la documentación y de las buenas prácticas.
```markdown
## Modo de Aprendizaje Activo
- Cuando uses una técnica o patrón que yo no haya visto antes,
  incluye una explicación breve de POR QUÉ funciona así
- Si un cambio involucra un concepto de ingeniería de software
  (patrón de diseño, principio SOLID, etc.), nómbralo
- Prefiero entender el código a que funcione rápido
- Si generas código complejo, agrega un comentario inline 
  explicando la lógica no-obvia
```


# Guía de Investigación: Configuración de Claude Code para Desarrollo Full-Stack Multi-Proyecto

**Autor:** Compilado con Claude para Ricardo  
**Fecha:** Marzo 2026  
**Contexto:** ~10 proyectos full-stack (Django + DRF / Vue 3 + Vuetify + Nuxt), desarrollador solo, plataformas de datos y derechos humanos.

---

## 1. Arquitectura de Archivos: Cómo Estructurar tu Ecosistema

### 1.1 El sistema de capas de Claude Code

**Nivel Global** → `~/.claude/CLAUDE.md`  
Se aplica a **todos** tus proyectos. Aquí va tu estilo personal de trabajo, convenciones de código que siempre quieres, y reglas que repetirías en cada sesión.

**Nivel Proyecto** → `./CLAUDE.md` (raíz del repo)  
Específico del proyecto. Se commitea a git. Describe la arquitectura, comandos de build/test, convenciones del proyecto.

**Nivel Subdirectorio** → `path/to/dir/CLAUDE.md`  
Se carga **bajo demanda** cuando Claude trabaja en archivos de ese directorio. Esencial para monorepos y para separar contexto frontend/backend.

**Nivel Personal del Proyecto** → `.claude/CLAUDE.md`  
Overrides personales para un proyecto. Se gitignora para que cada developer tenga sus preferencias.

**Reglas** → `.claude/rules/`  
Archivos markdown modulares con instrucciones enfocadas. Pueden filtrarse por path (solo se cargan cuando Claude trabaja en archivos que coinciden). Esto es clave para no inflar el contexto.

**Skills** → `.claude/skills/` o `~/.claude/skills/`  
Se cargan **bajo demanda** cuando Claude detecta que son relevantes. Ideales para workflows, guías de referencia, y documentación que no necesitas en cada sesión.

**Subagentes** → `.claude/agents/` o `~/.claude/agents/`  
Instancias aisladas de Claude con su propio contexto, herramientas restringidas, y opcionalmente memoria persistente.

### 1.2 Estructura recomendada para tus ~10 proyectos

Dado que trabajas solo y tienes proyectos con el mismo stack, la estructura óptima es:

```
~/.claude/
├── CLAUDE.md                          # Global: tu estilo personal (ver sección 1.3)
├── rules/
│   ├── coding-preferences.md          # Preferencias de codificación cross-proyecto
│   └── workflow-preferences.md        # Cómo quieres que Claude trabaje contigo
├── skills/
│   ├── django-drf-patterns/
│   │   └── SKILL.md                   # Patrones comunes Django+DRF
│   ├── vue-vuetify-nuxt-patterns/
│   │   └── SKILL.md                   # Patrones comunes Vue+Vuetify+Nuxt
│   ├── task-decomposition/
│       └── SKILL.md                   # Tu workflow de descomposición de tareas
└── agents/
    ├── code-reviewer.md               # Revisor de código con tu estilo
    └── task-planner.md                # Planificador/descomponedor de tareas
```

Para **cada proyecto** (ya sea monorepo o repos separados):

```
mi-proyecto/
├── CLAUDE.md                          # Específico: arquitectura, modelos, endpoints clave
├── .claude/
│   ├── rules/
│   │   ├── api-conventions.md         # Convenciones de API de este proyecto
│   │   └── data-models.md            # Decisiones de modelado de datos
│   ├── skills/
│   │   └── project-deploy/
│   │       └── SKILL.md              # Workflow de deploy específico
│   └── agents/
│       └── data-pipeline.md          # Si el proyecto tiene ETL específico
├── backend/
│   ├── CLAUDE.md                      # Convenciones Django de este proyecto
│   └── ...
└── frontend/
    ├── CLAUDE.md                      # Convenciones Vue/Nuxt de este proyecto
    └── ...
```

### 1.3 Qué poner en el CLAUDE.md global

Tu `~/.claude/CLAUDE.md` debería contener **solo lo que aplica a TODOS tus proyectos**. Basado en las mejores prácticas validadas:

```markdown
# Ricardo - Preferencias Globales de Desarrollo

## Stack Principal
- Backend: Django + DRF + PostgreSQL
- Frontend: Vue 3 + Vuetify + Nuxt 3/4
- Infraestructura: AWS (EC2, RDS, S3, Lambda)
- IDE: PyCharm en Windows

## Estilo de Código
- Comments and variable names in English
- Python: PEP 8, type hints en funciones públicas
- JavaScript/TypeScript: ES modules, composition API
- SQL: snake_case para columnas y tablas

## Cómo Trabajar Conmigo
- SIEMPRE proponer un plan antes de hacer cambios grandes
- Descomponer tareas complejas en pasos confirmables
- Explicar conceptos de ingeniería de software cuando los uses 
  (puedo tener gaps en patrones formales)
- Mostrar diffs claros; yo los reviso y modifico directamente
- NO hacer cambios que no haya aprobado
- Si un cambio toca más de 3 archivos, primero dame el plan

## Convenciones de Git
- Commits en inglés, descriptivos
- Una feature por branch

## Lo que NO hacer
- No usar stores globales (Pinia/Vuex) para estado de UI local
- No instalar dependencias sin confirmar conmigo
- No reescribir archivos completos; hacer cambios mínimos
```

### 1.4 Qué poner en el CLAUDE.md de cada proyecto

Cada proyecto necesita su contexto específico. La clave según la documentación oficial es: **documenta lo que Claude no puede inferir del código, no lo que ya es evidente.**

---

## 2. Extensión y Tamaño de Archivos: Cuánto Escribir

### 2.1 Recomendaciones validadas de tamaño

Las fuentes oficiales y la experiencia de la comunidad convergen en estos números:

**CLAUDE.md (raíz de proyecto):** Máximo **200 líneas** por archivo. La documentación oficial dice textualmente: "Keep CLAUDE.md under 200 lines." Si crece más, mover contenido a skills o a `.claude/rules/`. Un caso documentado en la comunidad muestra cómo un CLAUDE.md de 47,000 palabras causaba degradación severa; lo redujeron a 9,000 separando por servicio.

**CLAUDE.md global (`~/.claude/CLAUDE.md`):** Idealmente **50-100 líneas**. Solo tus no-negociables que aplican a todo.

**SKILL.md:** El PDF de Anthropic recomienda mantenerlo bajo **5,000 palabras**. La lógica es que aunque los skills se cargan bajo demanda (no siempre), una vez cargados, cada token compite con el historial de la conversación. El SKILL.md debería ser un índice que apunta a archivos detallados en `references/`.

**Rules (`.claude/rules/`):** No hay un límite oficial documentado, pero la práctica recomendada es archivos cortos y enfocados. La ventaja de rules sobre CLAUDE.md es que pueden tener filtro por path:

```yaml
---
paths:
  - backend/apps/api/**/*
  - "**/*.py"
---
# API Conventions
Usa APIView, no ViewSets...
```

Esto significa que estas reglas solo se cargan cuando Claude está trabajando en archivos Python de la API.

### 2.2 Principio rector: Progressive Disclosure

Tres niveles de "progressive disclosure" que es el principio más importante:

1. **Siempre cargado** (YAML frontmatter de skills, CLAUDE.md): Solo metadatos y contexto esencial.
2. **Cargado cuando relevante** (cuerpo del SKILL.md, rules con paths): Instrucciones completas.
3. **Cargado bajo demanda** (archivos en `references/`): Documentación detallada que Claude lee solo cuando necesita.

---

## 3. Herramientas y Features que Probablemente No Estás Contemplando

### 3.1 `.claude/rules/` — Reglas modulares con filtro por path

Esto es relativamente nuevo (v2.0.64+). A diferencia de CLAUDE.md que se carga siempre, los rules files pueden activarse solo cuando Claude trabaja en ciertos archivos:

```
.claude/rules/
├── django-models.md       # paths: ["backend/apps/**/models.py"]
├── vue-components.md      # paths: ["frontend/components/**/*.vue"]  
├── api-serializers.md     # paths: ["backend/apps/**/serializers.py"]
└── testing.md             # paths: ["**/*test*.py", "**/*.spec.ts"]
```

Esto es perfecto para tu caso con frontend y backend, porque las reglas de Django no inflan el contexto cuando estás trabajando en Vue y viceversa.

---

## 7. Lecciones del Paper "How AI Impacts Skill Formation"

El estudio de Anthropic (Shen & Tamkin, 2026) que incluiste tiene implicaciones directas para cómo configures tu workflow:

### 7.1 Hallazgos clave relevantes para ti

- Los participantes que usaron IA obtuvieron **17% menos** en comprensión que los que codificaron a mano, equivalente a casi dos niveles de calificación menos.
- La mayor brecha fue en **debugging** — la habilidad de entender cuándo y por qué el código falla.
- Sin embargo, **cómo se usa la IA importa más que si se usa**. Los patrones de alto rendimiento fueron:
  - **"Generation-then-comprehension"** (generar código, luego hacer preguntas de comprensión)
  - **"Hybrid code-explanation"** (pedir código + explicación simultáneamente)
  - **"Conceptual inquiry"** (solo hacer preguntas conceptuales, escribir el código tú mismo)
- Los patrones de bajo rendimiento fueron: delegación total, dependencia progresiva, y debugging iterativo donde Claude resuelve sin que entiendas.

---

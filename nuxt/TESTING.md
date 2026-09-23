# Testing — nuxt

## Niveles montados

- **Unitario con Vitest** (`vitest.config.ts`, tests en `tests/unit/`): lógica pura sin Nuxt ni DOM. Hoy cubre `app/utils/sections.js` — `sectionOfTab`, `visibleSections`/`isSectionVisible` para IES real y de prueba, y la regla de la IES real: no ve `cp` y un deep-link a una sección no publicada cae en la primera publicada.
- **End-to-end con Playwright**, contra el backend **mockeado** (`page.route`): la app corre de verdad, la API no. Ver el skill `playwright-e2e` para el flujo de trabajo MCP ↔ tests.

## Comandos

```bash
pnpm run test:unit           # unitarios (Vitest, solo tests/unit/)
pnpm run test:e2e            # suite completa
pnpm run test:e2e:ui         # modo interactivo
pnpm run test:e2e:debug      # paso a paso
pnpm run test:e2e:report     # abre el último reporte HTML
npx playwright test e2e/login.test.ts   # un solo spec
```

Playwright levanta el servidor solo (`pnpm run dev:test`, puerto 3019 sobre HTTPS con certificado local) y reutiliza el que ya esté corriendo.

## Flujos cubiertos

| Spec | Flujo |
|---|---|
| `login.test.ts` | login de staff a `/dashboard` y de IES a `/respuestas`, cookie de sesión, credenciales inválidas, validación de formato |
| `logout.test.ts` | el botón de salir limpia la cookie y redirige a `/login` |
| `protected-routes.test.ts` | `/dashboard` y `/respuestas` redirigen a `/login` sin sesión y se sostienen con ella |
| `register.test.ts` | alta con invitación válida, invitación ya usada, invitación inexistente, validación de contraseña |
| `forgot-password.test.ts` | solicitud de recuperación y error de servidor |
| `recover-password.test.ts` | token válido e inválido, contraseñas que no coinciden, reset exitoso con auto-login, token que expira entre validar y confirmar |
| `respuestas-tabs.test.ts` | chips del card ligados a su `?tab=`, navegación al tab correcto y deep-link que sobrevive a la recarga |
| `gen-capture.test.ts` | «Información base»: tri-estado «Está presente» que gobierna los conteos y su total, poblaciones estructurales sin conteo, el «no» explícito que limpia y viaja como respuesta, el escalar capturado que viaja en la fila de su pregunta (`value_integer`), y el «No aplica» de los planes de estudio (que las instancias no ofrecen) |
| `gen-non-binary.test.ts` | la pregunta previa de la categoría no binaria: agrega o retira la columna en las dos tablas y la tercera opción del radio de la titular, y apagarla borra los conteos ya capturados |
| `gen-validation-gate.test.ts` | la compuerta de completado: bloquea enumerando qué falta y marcando los campos, no estorba al guardar sin transicionar, y deja pasar la transición con el grupo completo |

## Fixtures y credenciales

No hay credenciales reales: todo es mock. Los datos viven en `e2e/mocks/auth.ts` y los interceptores en `e2e/mocks/handlers.ts`; `e2e/fixtures.ts` instala el catch-all en cada test y `e2e/helpers.ts` setea la cookie `auth_onigies` para arrancar ya autenticado.

Dos usuarios de referencia: `mockStaffUser` (sin institución, va a `/dashboard`) y `mockIesRespuestasUser` (institución `UP` con una encuesta 2025 completa). Ese último lleva `is_test: true` a propósito, porque los tests de `/respuestas` recorren las tres secciones y una IES real solo vería las publicadas (`app/utils/sections.js`).

Los datos de «Información base» viven aparte, en `e2e/mocks/gen.ts`: el catálogo Sector reducido a las filas que ejercitan cada bandera (`is_main`, `is_standard_extra`, `is_authority`, `is_ies_head`), los status del grupo `gen` con `role` y `content_editable`, y `makeGenSurvey()`, que arma el Survey con su `general_package` en borrador — la única combinación en la que los paneles son editables. `completeGenContent` es el contenido que ya satisface la compuerta. El andamiaje de interacción (abrir el tri-estado, el split-button de guardado, llegar a un campo numérico por su `aria-describedby`) está en `e2e/helpers.ts`.

## Propuestos para cp, no escritos

Pendientes de que Ricardo acuerde la lista. Necesitan un mock `e2e/mocks/cp.ts`, espejo de `gen.ts`: los status del grupo `cp` (incluido `cp_not_present`) con `role`, `content_editable`, `next_statuses` y `valid_child_statuses`; un `makeAxisValue()` con dos o tres observables de tipos distintos (A, B, alcance; uno especial y el 1.7 con su grupo `population`), `cp_capture` abierto o cerrado, `gen_denominators` y `a_options`; y los handlers de `/axis_value/`, `PATCH /observable_response/`, `PATCH /group_response/` (con `completion`, `observable_status` y `axis_status` en la respuesta) y `/flow/answer/…`.

Captura de la IES (`/respuestas`):

- compuerta cerrada: por fecha y por generales sin validar, el cuestionario se ve completo con su aviso, sin controles de captura ni módulo de estatus;
- respuesta inicial: «Sí» habilita los grupos; «No» lleva observable y grupos a «No cuenta con la medida» y la vuelta a «Sí» los reabre;
- guardado por grupo: el botón solo aparece con cambios, el PATCH lleva solo las filas tocadas y `completion` se muestra sin bloquear el guardado;
- oferta del siguiente paso: tras completar el último grupo, snackbar con acción para el observable; tras el último observable, para el eje; nada transiciona solo;
- tipos especiales: planes sin el nivel declarado «No aplica», la salida de planeación general del alcance, el especial con cumplen > total, y el 1.7 sin preguntas que se promueve con el «Sí».

Revisión (dashboard):

- lista de «Ejes del cuestionario» por urgencia, con el conteo de observables por estatus en el renglón y el filtro de estatus;
- detalle en modo revisión: contenido de solo lectura, adjuntos y comentarios visibles, y el aviso de compuerta sin detener a la revisora;
- devolver un grupo con comentario obligatorio, y el observable y el eje transicionados aparte;
- regla de hijos: el eje no se aprueba con observables pendientes (diálogo de bloqueo), y la revisión queda bloqueada mientras el eje siga en turno de la IES;
- «No cuenta con la medida»: terminal, sin transiciones, cuenta como hijo resuelto.

## Prueba manual contra el stack local

Los e2e son mockeados; para ejercitar la app contra Django de verdad (`:8018` + `:3018`) hay que usar la base local, hoy una restauración de producción. Qué existe en ella y qué no:

- **Staff**: `smoke-staff@test.local`, contraseña `SmokeStaff2026!` (id 87, `is_staff`). Existe en la base local de hoy; si se restaura otro dump de producción hay que crearla de nuevo.
- **IES de prueba con datos cp**: **FP** («Ferprueba», institución 76, `is_test=True`), persona usuaria `rickrebel+fp@gmail.com` (id 80), contraseña desconocida. Se entra con su token DRF: la cookie `auth_onigies` con el valor de `Token.objects.get(user_id=80).key`, o `Authorization: Token …` contra la API. Sus ejes del periodo 2025 son los AxisValue 293 a 296.
- **No existen** en la base restaurada: `rickrebel+ciad@gmail.com` / `SmokeGen2026!` (la IES CIAD sí existe, pero no es de prueba y no tiene esa persona usuaria). Para probar «Información base» con una IES con contraseña conocida hay que crearla.

Ninguna de estas credenciales existe en algún servidor.

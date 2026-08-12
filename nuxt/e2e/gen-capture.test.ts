import { test, expect } from './fixtures'
import {
  setupGenSection, genPanel, setPresence, saveGenGroup, genNumberField,
} from './helpers'
import { mockSurveyPatch } from './mocks/handlers'
import {
  makeGenSurvey, GEN_SURVEY_ID, QUESTION_ACADEMIC_INSTANCES,
  QUESTION_MEDIA_PLANS, SECTOR_UNDERGRADUATE,
} from './mocks/gen'

const BASE_TAB = '/respuestas/2025?tab=base'

const MEDIA_PLANS = 'Planes de estudio vigentes de nivel medio superior'
const ACADEMIC_INSTANCES = 'Instancias académicas reconocidas en el marco '
  + 'normativo u organigrama de la IES'

test.describe('Información base — captura', () => {
  test('el tri-estado gobierna los conteos y el total los suma',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      await page.goto(BASE_TAB)

      const women = page.getByLabel(
        'Mujeres — Alumnado de nivel licenciatura')
      const men = page.getByLabel('Hombres — Alumnado de nivel licenciatura')

      // Sin respuesta de presencia no hay dónde capturar.
      await expect(women).toBeDisabled()

      await setPresence(page, 'Alumnado de nivel licenciatura', 'Sí')
      await expect(women).toBeEnabled()
      await women.fill('120')
      await men.fill('98')

      const row = genPanel(page, 'Poblaciones')
        .getByRole('row', { name: /Alumnado de nivel licenciatura/ })
      await expect(row.getByRole('cell', { name: '218' })).toBeVisible()
    })

  test('las poblaciones estructurales solo declaran presencia',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      await page.goto(BASE_TAB)

      const row = genPanel(page, 'Poblaciones')
        .getByRole('row', { name: /Población externa/ })
      await expect(row.getByText('No requiere conteo')).toBeVisible()
      await expect(row.locator('input[inputmode="numeric"]')).toHaveCount(0)
    })

  test('el «No» limpia los conteos y viaja como respuesta sin conteos',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      const captured = await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      const women = page.getByLabel(
        'Mujeres — Alumnado de nivel licenciatura')
      await setPresence(page, 'Alumnado de nivel licenciatura', 'Sí')
      await women.fill('120')

      // Cambiar de opinión no puede dejar el conteo viejo a la vista.
      await setPresence(page, 'Alumnado de nivel licenciatura', 'No')
      await expect(women).toHaveValue('')
      await expect(women).toBeDisabled()

      await saveGenGroup(page, 'Poblaciones')
      await expect.poll(() => captured.length).toBe(1)

      // Un «no» explícito es respuesta: la fila viaja aunque no lleve
      // conteo, porque la existencia vive en ella (adr-0012).
      const rows = captured[0].population_quantities as Record<
        string, unknown>[]
      expect(rows).toContainEqual(expect.objectContaining({
        sector: SECTOR_UNDERGRADUATE,
        is_present: false,
        number_women: null,
        number_men: null,
      }))
    })

  test('«No aplica» solo lo ofrecen los planes de estudio',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      await page.goto(BASE_TAB)

      const instances = await genNumberField(page, ACADEMIC_INSTANCES)
      // Toda institución tiene estructura: no hay escape que ofrecer.
      await expect(instances.noApply).toHaveCount(0)

      const plans = await genNumberField(page, MEDIA_PLANS)
      await expect(plans.noApply).toBeVisible()
    })

  test('el valor capturado viaja en la fila de su pregunta',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      const captured = await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      const instances = await genNumberField(page, ACADEMIC_INSTANCES)
      await instances.count.fill('12')

      await saveGenGroup(page, 'Estructuras')
      await expect.poll(() => captured.length).toBe(1)

      // Desde task-117 el escalar ya no es columna del Survey: viaja en la
      // fila de su pregunta, en la columna que dicta su `q_type`.
      expect(captured[0].question_responses).toContainEqual({
        general_question: QUESTION_ACADEMIC_INSTANCES,
        no_apply: false,
        value_integer: 12,
        value_boolean: null,
      })
    })

  test('marcar «No aplica» en un plan limpia y bloquea su conteo',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      const captured = await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      const plans = await genNumberField(page, MEDIA_PLANS)
      await plans.count.fill('12')
      await plans.noApply.check()

      await expect(plans.count).toHaveValue('')
      await expect(plans.count).toBeDisabled()

      await saveGenGroup(page, 'Planes de estudio')
      await expect.poll(() => captured.length).toBe(1)

      // «No aplica» y valor viajan en la misma fila, y el valor queda en
      // nulo: un cero significaría otra cosa.
      expect(captured[0].question_responses).toContainEqual({
        general_question: QUESTION_MEDIA_PLANS,
        no_apply: true,
        value_integer: null,
        value_boolean: null,
      })
    })
})

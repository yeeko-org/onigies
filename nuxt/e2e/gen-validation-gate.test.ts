import { test, expect } from './fixtures'
import { setupGenSection, genPanel, transitionGenGroup } from './helpers'
import { mockSurveyPatch, mockFlowTransition } from './mocks/handlers'
import {
  makeGenSurvey, completeGenContent, GEN_SURVEY_ID, GEN_GROUP_RESPONSE_IDS,
} from './mocks/gen'

const BASE_TAB = '/respuestas/2025?tab=base'
const COMPLETE = 'Marcar como completado'

// Guardar nunca valida —la IES captura en varias sesiones—; la compuerta
// es solo del paso a completado, que compromete el grupo ante la revisión.
test.describe('Información base — compuerta de completado', () => {
  test('con campos vacíos enumera lo que falta y los marca en error',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      const panel = genPanel(page, 'Poblaciones')
      await transitionGenGroup(page, 'Poblaciones', COMPLETE)

      const alert = panel.locator('.v-alert')
      await expect(alert).toBeVisible()
      // El criterio es decir QUÉ falta, no solo que falta.
      await expect(alert).toContainText(
        'Falta indicar si su institución contempla la categoría no binaria.')
      await expect(alert).toContainText(
        'Alumnado de nivel licenciatura: falta indicar si está presente.')

      // Y el campo exacto queda señalado, no solo la lista.
      await expect(panel.locator('.v-input--error')).not.toHaveCount(0)
    })

  test('la compuerta no estorba al guardar sin transicionar',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      const captured = await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      await genPanel(page, 'Poblaciones')
        .getByRole('button', { name: /Guardar/ }).click()
      await page.locator('.v-overlay-container .v-list-item')
        .filter({ hasText: 'Guardar y mantener como' }).click()

      await expect.poll(() => captured.length).toBe(1)
      await expect(genPanel(page, 'Poblaciones').locator('.v-alert'))
        .toHaveCount(0)
    })

  test('con todo respondido la transición se ejecuta',
    async ({ page, context }) => {
      await setupGenSection(
        page, context, makeGenSurvey(completeGenContent))
      await mockSurveyPatch(page, GEN_SURVEY_ID)
      await mockFlowTransition(
        page, 'survey', 'generalgroupresponse',
        GEN_GROUP_RESPONSE_IDS.poblaciones,
        // `to_status` es lo que el kernel escribe sobre el registro.
        { id: 900, to_status: 'gen_completed', comment: '' })
      await page.goto(BASE_TAB)

      const transitioned = page.waitForResponse(
        (res) => res.url().includes('/transitions/') && res.status() === 201)
      await transitionGenGroup(page, 'Poblaciones', COMPLETE)
      await transitioned

      // El panel se colapsa solo cuando la transición realmente ocurrió.
      await expect(genPanel(page, 'Poblaciones').locator('.v-alert'))
        .toHaveCount(0)
      await expect(genPanel(page, 'Poblaciones')
        .getByText('Completado')).toBeVisible()
    })
})

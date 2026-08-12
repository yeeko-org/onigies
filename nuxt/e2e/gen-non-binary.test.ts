import type { Page } from '@playwright/test'
import { test, expect } from './fixtures'
import { setupGenSection, genPanel } from './helpers'
import { mockSurveyPatch } from './mocks/handlers'
import { makeGenSurvey, GEN_SURVEY_ID } from './mocks/gen'

const BASE_TAB = '/respuestas/2025?tab=base'

// La pregunta previa es capacidad de medición de la institución, no
// propiedad de una tabla: manda sobre las dos y sobre el radio de la
// persona titular.
const nonBinaryAnswer = (page: Page, value: 'Sí' | 'No') =>
  genPanel(page, 'Poblaciones')
    .getByRole('radio', { name: value, exact: true })

const nonBinaryColumns = (page: Page) =>
  page.getByRole('columnheader', { name: 'No binarie' })

test.describe('Información base — columna No binarie', () => {
  test('la columna aparece en las dos tablas solo si la IES mide '
    + 'esa población', async ({ page, context }) => {
    await setupGenSection(page, context, makeGenSurvey())
    await page.goto(BASE_TAB)

    // La pregunta previa lleva su ayuda debajo, no como placeholder.
    await expect(genPanel(page, 'Poblaciones').getByText(
      'Si responde Sí, las tablas de esta sección incluirán una columna',
    )).toBeVisible()

    await expect(nonBinaryColumns(page)).toHaveCount(0)
    // Sin la bandera, la titular solo puede ser mujer u hombre.
    await expect(genPanel(page, 'Autoridades')
      .getByRole('radio', { name: 'No binaria' })).toHaveCount(0)

    await nonBinaryAnswer(page, 'Sí').check()

    // Poblaciones y autoridades: una sola respuesta las gobierna.
    await expect(nonBinaryColumns(page)).toHaveCount(2)
    await expect(genPanel(page, 'Autoridades')
      .getByRole('radio', { name: 'No binaria' })).toBeVisible()
  })

  test('responder «No» retira la columna y borra los conteos capturados',
    async ({ page, context }) => {
      await setupGenSection(page, context, makeGenSurvey())
      const captured = await mockSurveyPatch(page, GEN_SURVEY_ID)
      await page.goto(BASE_TAB)

      await nonBinaryAnswer(page, 'Sí').check()
      const board = page.getByLabel(
        'No binarie — Máximo cuerpo colegiado de toda la IES')
      await board.fill('4')

      await nonBinaryAnswer(page, 'No').check()
      await expect(nonBinaryColumns(page)).toHaveCount(0)

      // Volver a encenderla no debe resucitar el conteo: apagar la
      // pregunta previa lo borra, no solo lo esconde.
      await nonBinaryAnswer(page, 'Sí').check()
      await expect(board).toHaveValue('')

      await nonBinaryAnswer(page, 'No').check()
      await page.getByRole('button', { name: /Guardar/ }).first().click()
      await page.locator('.v-overlay-container .v-list-item')
        .filter({ hasText: 'Guardar y mantener como' }).click()

      await expect.poll(() => captured.length).toBe(1)
      expect(captured[0].measures_non_binary).toBe(false)
      const rows = captured[0].population_quantities as Record<
        string, unknown>[]
      for (const row of rows) expect(row.number_non_binary).toBeNull()
    })
})

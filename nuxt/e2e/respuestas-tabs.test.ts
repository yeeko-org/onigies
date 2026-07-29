import { test, expect } from './fixtures'
import type { Page, BrowserContext } from '@playwright/test'
import { setAuthCookie } from './helpers'
import { mockCurrentUser, mockCatalogs, mockFlowStatuses } from
  './mocks/handlers'
import {
  mockIesRespuestasUser,
  mockRespuestasCatalogs,
  mockRespuestasFlowStatuses,
} from './mocks/auth'

// Bootstrap común: sesión IES + los tres endpoints que el middleware
// dashboard necesita (checkAuth, catálogos, catálogo de flujo).
async function setupIes(page: Page, context: BrowserContext): Promise<void> {
  await setAuthCookie(context, mockIesRespuestasUser.token)
  await mockCurrentUser(page, mockIesRespuestasUser)
  await mockCatalogs(page, mockRespuestasCatalogs)
  await mockFlowStatuses(page, mockRespuestasFlowStatuses)
}

test.describe('/respuestas — chips y tabs ligados a la URL', () => {
  test('el card muestra los chips como enlaces a su ?tab=',
    async ({ page, context }) => {
      await setupIes(page, context)
      await page.goto('/respuestas')

      // Cada chip es un enlace al tab correspondiente del año 2025.
      // (Datos base + 2 ejes + Buenas prácticas.)
      await expect(
        page.locator('a[href*="/respuestas/2025?tab=base"]')).toBeVisible()
      await expect(
        page.locator('a[href*="/respuestas/2025?tab=axis-1"]')).toBeVisible()
      await expect(
        page.locator('a[href*="/respuestas/2025?tab=axis-2"]')).toBeVisible()
      await expect(
        page.locator('a[href*="/respuestas/2025?tab=bp"]')).toBeVisible()

      // Solo esos cuatro llevan ?tab= ("Ver respuestas" no lleva query).
      await expect(
        page.locator('a[href*="/respuestas/2025?tab="]')).toHaveCount(4)
    })

  test('click en un chip navega al tab correcto',
    async ({ page, context }) => {
      await setupIes(page, context)
      await page.goto('/respuestas')

      await page.locator('a[href*="/respuestas/2025?tab=axis-1"]').click()

      await expect(page).toHaveURL(/\/respuestas\/2025\?tab=axis-1/)
      await expect(
        page.getByRole('tab', { name: /Institucional/ })
      ).toHaveAttribute('aria-selected', 'true')
    })

  test('deep-link con ?tab= se conserva (no lo borra setCurrentPeriod)',
    async ({ page, context }) => {
      await setupIes(page, context)
      await page.goto('/respuestas/2025?tab=axis-2')

      // Regresión: el watch de respuestas.vue no debe descartar el query.
      await expect(page).toHaveURL(/\/respuestas\/2025\?tab=axis-2/)
      await expect(
        page.getByRole('tab', { name: /Docencia/ })
      ).toHaveAttribute('aria-selected', 'true')

      // Y persiste tras recargar.
      await page.reload()
      await expect(page).toHaveURL(/\/respuestas\/2025\?tab=axis-2/)
      await expect(
        page.getByRole('tab', { name: /Docencia/ })
      ).toHaveAttribute('aria-selected', 'true')
    })
})

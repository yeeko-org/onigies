import { test, expect } from './fixtures'
import {
  mockRequestResetFailure,
  mockRequestResetSuccess,
} from './mocks/handlers'

test.describe('forgot-password', () => {
  test('successful request shows confirmation and disables button',
    async ({ page }) => {
      await mockRequestResetSuccess(page)

      await page.goto('/forgot-password')
      await page.getByLabel('Correo electrónico').fill('user@example.com')
      await page.getByRole('button', { name: 'Enviar correo' }).click()

      await expect(
        page.getByText('Si el correo existe, recibirás un enlace en breve.')
      ).toBeVisible()
      await expect(page.getByRole('button', { name: 'Enviar correo' }))
        .toBeDisabled()
    })

  test('invalid email format blocks submit', async ({ page }) => {
    await page.goto('/forgot-password')
    await page.getByLabel('Correo electrónico').fill('not-an-email')
    await page.getByRole('button', { name: 'Enviar correo' }).click()

    await expect(page.getByText('Escribe un correo válido')).toBeVisible()
    await expect(
      page.getByText('Si el correo existe, recibirás un enlace en breve.')
    ).toHaveCount(0)
  })

  test('server error shows alert', async ({ page }) => {
    await mockRequestResetFailure(page, 500, { detail: 'Error interno' })

    await page.goto('/forgot-password')
    await page.getByLabel('Correo electrónico').fill('user@example.com')
    await page.getByRole('button', { name: 'Enviar correo' }).click()

    await expect(page.locator('.v-alert')).toContainText('Error interno')
  })

  test('volver button navigates back to /login', async ({ page }) => {
    await page.goto('/forgot-password')
    await page.getByRole('link', { name: 'Volver' }).click()
    await expect(page).toHaveURL(/\/login/)
  })
})
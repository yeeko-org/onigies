import { test, expect } from './fixtures'
import {
  mockConfirmResetFailure,
  mockConfirmResetSuccess,
  mockCurrentUser,
  mockValidateResetToken,
  mockValidateResetTokenInvalid,
} from './mocks/handlers'
import {
  API_BASE,
  mockResetEmail,
  mockResetToken,
  mockStaffUser,
} from './mocks/auth'

async function mockPostLoginNoise(page, user) {
  await mockCurrentUser(page, user)
  await page.route(`${API_BASE}/catalogs/all/`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '{}' })
  )
}

test.describe('recover-password', () => {
  test('valid token shows form with email in subtitle',
    async ({ page }) => {
      await mockValidateResetToken(page, mockResetToken, mockResetEmail)

      await page.goto(`/recover-password?token=${mockResetToken}`)

      await expect(
        page.getByText(`Restablecer contraseña para ${mockResetEmail.email}`)
      ).toBeVisible()
      await expect(
        page.getByLabel('Nueva contraseña', { exact: true })
      ).toBeVisible()
    })

  test('invalid token shows warning and link to forgot-password',
    async ({ page }) => {
      await mockValidateResetTokenInvalid(page, 'bad-token')

      await page.goto('/recover-password?token=bad-token')

      await expect(
        page.getByText('El enlace es inválido o ha expirado.')
      ).toBeVisible()

      await page.getByRole('link', { name: 'Solicitar nuevo enlace' }).click()
      await expect(page).toHaveURL(/\/forgot-password/)
    })

  test('password mismatch blocks submit', async ({ page }) => {
    await mockValidateResetToken(page, mockResetToken, mockResetEmail)

    await page.goto(`/recover-password?token=${mockResetToken}`)

    await page.getByLabel('Nueva contraseña', { exact: true })
      .fill('pass1234')
    await page.getByLabel('Confirmar contraseña').fill('pass5678')
    await page.getByRole('button', { name: 'Guardar contraseña' }).click()

    await expect(page.getByText('Las contraseñas no coinciden')).toBeVisible()
  })

  test('successful reset logs user in and redirects', async ({ page }) => {
    await mockValidateResetToken(page, mockResetToken, mockResetEmail)
    await mockConfirmResetSuccess(page, mockResetToken, mockStaffUser)
    await mockPostLoginNoise(page, mockStaffUser)

    await page.goto(`/recover-password?token=${mockResetToken}`)

    await page.getByLabel('Nueva contraseña', { exact: true })
      .fill('new-password-123')
    await page.getByLabel('Confirmar contraseña').fill('new-password-123')
    await page.getByRole('button', { name: 'Guardar contraseña' }).click()

    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10_000 })
  })

  test('token expires between validation and confirm falls back to invalid state',
    async ({ page }) => {
      await mockValidateResetToken(page, mockResetToken, mockResetEmail)
      await mockConfirmResetFailure(page, mockResetToken, 400,
        { token: ['Token expirado'] })

      await page.goto(`/recover-password?token=${mockResetToken}`)

      await page.getByLabel('Nueva contraseña', { exact: true })
        .fill('new-password-123')
      await page.getByLabel('Confirmar contraseña').fill('new-password-123')
      await page.getByRole('button', { name: 'Guardar contraseña' }).click()

      await expect(
        page.getByText('El enlace es inválido o ha expirado.')
      ).toBeVisible()
    })
})
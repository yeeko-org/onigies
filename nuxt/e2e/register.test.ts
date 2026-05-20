import { test, expect } from './fixtures'
import {
  mockCurrentUser,
  mockInvitationAlreadyRegistered,
  mockInvitationNotFound,
  mockInvitationValid,
  mockRegisterSuccess,
} from './mocks/handlers'
import {
  API_BASE,
  mockInvitationPayload,
  mockInvitationUuid,
  mockStaffUser,
} from './mocks/auth'

async function mockPostLoginNoise(page, user) {
  await mockCurrentUser(page, user)
  await page.route(`${API_BASE}/catalogs/all/`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '{}' })
  )
}

test.describe('register', () => {
  test('valid invitation prefills email and completes registration',
    async ({ page }) => {
      await mockInvitationValid(
        page, mockInvitationUuid, mockInvitationPayload)
      await mockRegisterSuccess(
        page, mockInvitationUuid, mockStaffUser)
      await mockPostLoginNoise(page, mockStaffUser)

      await page.goto(`/register?token=${mockInvitationUuid}`)

      const emailField = page.getByLabel('Correo electrónico')
      await expect(emailField).toHaveValue(mockInvitationPayload.email)
      await expect(page.getByText('Institución Nueva')).toBeVisible()

      await page.getByLabel('Nombre(s)').fill('Juan')
      await page.getByLabel('Apellidos').fill('Pérez')
      await page.getByLabel('Contraseña', { exact: true })
        .fill('password-valid-1')
      await page.getByLabel('Confirmar contraseña')
        .fill('password-valid-1')

      await page.getByRole('button', { name: 'Crear cuenta' }).click()

      await expect(page).toHaveURL(/\/dashboard/, { timeout: 10_000 })
    })

  test('already-registered invitation shows info and login button',
    async ({ page }) => {
      await mockInvitationAlreadyRegistered(page, mockInvitationUuid)

      await page.goto(`/register?token=${mockInvitationUuid}`)

      await expect(page.getByText(/Tu cuenta ya fue creada/)).toBeVisible()

      await page.getByRole('link', { name: 'Iniciar sesión' }).click()
      await expect(page).toHaveURL(/\/login/)
    })

  test('invitation not found shows alert', async ({ page }) => {
    await mockInvitationNotFound(page, 'does-not-exist')

    await page.goto('/register?token=does-not-exist')

    await expect(page.locator('.v-alert'))
      .toContainText('Invitación no encontrada')
  })

  test('password mismatch blocks submit', async ({ page }) => {
    await mockInvitationValid(
      page, mockInvitationUuid, mockInvitationPayload)

    await page.goto(`/register?token=${mockInvitationUuid}`)

    await page.getByLabel('Nombre(s)').fill('Juan')
    await page.getByLabel('Apellidos').fill('Pérez')
    await page.getByLabel('Contraseña', { exact: true }).fill('pass1234')
    await page.getByLabel('Confirmar contraseña').fill('pass5678')
    await page.getByRole('button', { name: 'Crear cuenta' }).click()

    await expect(page.getByText('Las contraseñas no coinciden')).toBeVisible()
    await expect(page).toHaveURL(/\/register/)
  })

  test('short password blocks submit', async ({ page }) => {
    await mockInvitationValid(
      page, mockInvitationUuid, mockInvitationPayload)

    await page.goto(`/register?token=${mockInvitationUuid}`)

    await page.getByLabel('Nombre(s)').fill('Juan')
    await page.getByLabel('Apellidos').fill('Pérez')
    await page.getByLabel('Contraseña', { exact: true }).fill('short')
    await page.getByLabel('Confirmar contraseña').fill('short')
    await page.getByRole('button', { name: 'Crear cuenta' }).click()

    await expect(page.getByText('Mínimo 8 caracteres').first()).toBeVisible()
    await expect(page).toHaveURL(/\/register/)
  })
})
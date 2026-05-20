import { test, expect } from './fixtures'
import { fillLoginForm, getAuthCookieValue } from './helpers'
import {
  mockCurrentUser,
  mockLoginFailure,
  mockLoginSuccess,
} from './mocks/handlers'
import {
  API_BASE, mockIesUser, mockStaffUser,
} from './mocks/auth'

// Mockea endpoints que el middleware de dashboard/respuestas dispara
// tras el redirect, para que no caigan en el catchAll y ensucien la
// consola del test.
async function mockPostLoginNoise(page, user) {
  await mockCurrentUser(page, user)
  await page.route(`${API_BASE}/catalogs/all/`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '{}' })
  )
}

test.describe('login', () => {
  test('staff login redirects to /dashboard and sets auth cookie',
    async ({ page, context }) => {
      await mockLoginSuccess(page, mockStaffUser)
      await mockPostLoginNoise(page, mockStaffUser)

      await page.goto('/login')
      await fillLoginForm(page, mockStaffUser.email, 'any-password-123')

      await expect(page).toHaveURL(/\/dashboard/, { timeout: 10_000 })
      expect(await getAuthCookieValue(context)).toBe(mockStaffUser.token)
    })

  test('ies user login redirects to /respuestas', async ({ page }) => {
    await mockLoginSuccess(page, mockIesUser)
    await mockPostLoginNoise(page, mockIesUser)

    await page.goto('/login')
    await fillLoginForm(page, mockIesUser.email, 'any-password-123')

    await expect(page).toHaveURL(/\/respuestas/, { timeout: 10_000 })
  })

  test('invalid credentials show alert and clear password',
    async ({ page }) => {
      await mockLoginFailure(page, 400,
        { non_field_errors: ['Correo o contraseña incorrectos'] })

      await page.goto('/login')
      await fillLoginForm(page, 'wrong@example.com', 'bad-password')

      await expect(page.locator('.v-alert'))
        .toContainText('Correo o contraseña incorrectos')
      await expect(page.getByLabel('Contraseña', { exact: true }))
        .toHaveValue('')
      await expect(page).toHaveURL(/\/login/)
    })

  test('invalid email format blocks submit', async ({ page }) => {
    await page.goto('/login')
    await page.getByLabel('Correo electrónico').fill('not-an-email')
    await page.getByLabel('Contraseña', { exact: true }).fill('12345678')
    await page.getByRole('button', { name: 'Iniciar sesión' }).click()

    await expect(page.getByText('Escribe un correo válido')).toBeVisible()
    await expect(page).toHaveURL(/\/login/)
  })

  test('link to forgot-password navigates correctly', async ({ page }) => {
    await page.goto('/login')
    await page.getByRole('link', { name: 'Recuperar contraseña' }).click()
    await expect(page).toHaveURL(/\/forgot-password/)
  })
})
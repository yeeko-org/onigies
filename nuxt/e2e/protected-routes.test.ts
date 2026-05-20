import { test, expect } from './fixtures'
import { setAuthCookie } from './helpers'
import { mockCurrentUser } from './mocks/handlers'
import { API_BASE, mockStaffUser } from './mocks/auth'

test.describe('protected routes', () => {
  test('/dashboard without session redirects to /login',
    async ({ page }) => {
      await page.goto('/dashboard')
      await expect(page).toHaveURL(/\/login/, { timeout: 5_000 })
    })

  test('/dashboard with valid session stays on /dashboard',
    async ({ page, context }) => {
      await setAuthCookie(context, mockStaffUser.token)
      await mockCurrentUser(page, mockStaffUser)
      await page.route(`${API_BASE}/catalogs/all/`, (route) =>
        route.fulfill({ status: 200, contentType: 'application/json',
          body: '{}' })
      )

      await page.goto('/dashboard')

      // Dar tiempo a que el middleware corra su lógica async.
      await page.waitForTimeout(500)
      await expect(page).toHaveURL(/\/dashboard/)
    })

  test('/respuestas without session redirects to /login',
    async ({ page }) => {
      await page.goto('/respuestas')
      await expect(page).toHaveURL(/\/login/, { timeout: 5_000 })
    })

  test('/respuestas with valid session stays on /respuestas',
    async ({ page, context }) => {
      await setAuthCookie(context, mockStaffUser.token)
      await mockCurrentUser(page, mockStaffUser)
      await page.route(`${API_BASE}/catalogs/all/`, (route) =>
        route.fulfill({ status: 200, contentType: 'application/json',
          body: '{}' })
      )

      await page.goto('/respuestas')

      await page.waitForTimeout(500)
      await expect(page).toHaveURL(/\/respuestas/)
    })
})
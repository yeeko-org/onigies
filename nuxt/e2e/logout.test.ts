import { test, expect } from './fixtures'
import {
  getAuthCookieValue,
  setAuthCookie,
} from './helpers'
import {
  mockCurrentUser,
} from './mocks/handlers'
import {
  API_BASE,
  mockStaffUser,
} from './mocks/auth'

test.describe('logout', () => {
  test('logout button clears cookie and redirects to /login',
    async ({ page, context }) => {
      // Seed session: cookie + mocks necesarios para que el layout
      // dashboard renderice sin pegarle al backend real.
      await setAuthCookie(context, mockStaffUser.token)
      await mockCurrentUser(page, mockStaffUser)
      await page.route(`${API_BASE}/catalogs/all/`, (route) =>
        route.fulfill({ status: 200, contentType: 'application/json',
          body: '{}' })
      )

      await page.goto('/dashboard')
      await expect(page).toHaveURL(/\/dashboard/)

      await page.getByTestId('logout-button').click()

      await expect(page).toHaveURL(/\/login/)
      expect(await getAuthCookieValue(context)).toBeFalsy()
    })
})
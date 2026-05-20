import type { Page, BrowserContext } from '@playwright/test'
import { expect } from '@playwright/test'

const COOKIE_NAME = 'auth_onigies'

// Setea la cookie de sesión sin pasar por la UI de login. Útil para
// tests que empiezan ya autenticados (rutas protegidas, logout).
export async function setAuthCookie(
  context: BrowserContext, token: string,
): Promise<void> {
  await context.addCookies([{
    name: COOKIE_NAME,
    value: token,
    domain: 'localhost',
    path: '/',
    httpOnly: false,
    secure: true,
    sameSite: 'Lax',
  }])
}

export async function clearAuthCookie(
  context: BrowserContext,
): Promise<void> {
  const cookies = await context.cookies()
  const filtered = cookies.filter((c) => c.name !== COOKIE_NAME)
  await context.clearCookies()
  if (filtered.length > 0) await context.addCookies(filtered)
}

export async function getAuthCookieValue(
  context: BrowserContext,
): Promise<string | null> {
  const cookies = await context.cookies()
  const found = cookies.find((c) => c.name === COOKIE_NAME)
  return found?.value ?? null
}

// Llena y envía el form de login desde la UI.
export async function fillLoginForm(
  page: Page, email: string, password: string,
): Promise<void> {
  await page.getByLabel('Correo electrónico').fill(email)
  await page.getByLabel('Contraseña', { exact: true }).fill(password)
  await page.getByRole('button', { name: 'Iniciar sesión' }).click()
}

// Espera a que el navegador navegue a una ruta específica.
export async function expectUrlToBe(
  page: Page, pathname: string, timeout = 5000,
): Promise<void> {
  await expect.poll(
    () => new URL(page.url()).pathname,
    { timeout },
  ).toBe(pathname)
}
import type { Page, BrowserContext, Locator } from '@playwright/test'
import { expect } from '@playwright/test'
import {
  mockCurrentUser, mockCatalogs, mockFlowStatuses, mockSurveyDetail,
} from './mocks/handlers'
import { mockIesRespuestasUser } from './mocks/auth'
import { mockGenCatalogs, mockGenFlowStatuses, GEN_SURVEY_ID } from
  './mocks/gen'

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

// ── Sección «Información base» (grupo de flujo `gen`) ────────────────

/**
 * Deja la sección lista para capturar: sesión de la IES, los tres
 * endpoints del bootstrap (checkAuth, catálogos, catálogo de flujo) y el
 * detalle del Survey, que es de donde cuelgan el paquete y sus grupos.
 *
 * No navega: cada test decide si entra por `?tab=base` o por otro lado.
 */
export async function setupGenSection(
  page: Page, context: BrowserContext, survey: Record<string, unknown>,
): Promise<void> {
  await setAuthCookie(context, mockIesRespuestasUser.token)
  await mockCurrentUser(page, mockIesRespuestasUser)
  await mockCatalogs(page, mockGenCatalogs)
  await mockFlowStatuses(page, mockGenFlowStatuses)
  await mockSurveyDetail(page, GEN_SURVEY_ID, survey)
}

// Un panel de grupo por su título; cada uno vive en su expansion panel.
export function genPanel(page: Page, title: string): Locator {
  return page.locator('.v-expansion-panel').filter({ hasText: title })
}

/**
 * El tri-estado «Está presente» es un v-select: hay que abrirlo y elegir.
 * Se centra antes de hacer clic porque la barra superior es fija y el
 * scroll mínimo de Playwright deja el campo debajo de ella.
 */
export async function setPresence(
  page: Page, sector: string, value: 'Sí' | 'No',
): Promise<void> {
  // Se abre desde el `.v-field`, no desde el input: en un v-select el
  // input va detrás del div que pinta el valor y los clics no le llegan.
  const select = page.locator(
    `.v-field:has([aria-label="Está presente — ${sector}"])`)
  await select.evaluate((el) => el.scrollIntoView({ block: 'center' }))
  await select.click()
  await page.getByRole('option', { name: value, exact: true }).click()
}

/**
 * Guardar sin transicionar. Con transiciones disponibles el botón es un
 * split-button, así que el guardado simple vive en la primera entrada del
 * menú, no en el botón.
 */
export async function saveGenGroup(
  page: Page, title: string,
): Promise<void> {
  await genPanel(page, title).getByRole('button', { name: /Guardar/ }).click()
  await page.locator('.v-overlay-container .v-list-item')
    .filter({ hasText: 'Guardar y mantener como' }).click()
}

// Elige una transición del split-button de guardado del grupo.
export async function transitionGenGroup(
  page: Page, title: string, action: string,
): Promise<void> {
  await genPanel(page, title).getByRole('button', { name: /Guardar/ }).click()
  await page.locator('.v-overlay-container .v-list-item')
    .filter({ hasText: action }).click()
}

/**
 * Los campos numéricos de un grupo de preguntas no llevan rótulo propio
 * (el texto del instrumento va aparte), pero sí `aria-describedby` hacia
 * él: ese vínculo es el asidero estable para llegar al renglón.
 */
export async function genNumberField(
  page: Page, question: string,
): Promise<{ count: Locator, noApply: Locator }> {
  const id = await page.getByText(question, { exact: true })
    .getAttribute('id')
  const field = page.locator(`div.ga-6:has(input[aria-describedby="${id}"])`)
  return {
    count: field.locator('input[inputmode="numeric"]'),
    noApply: field.getByLabel('No aplica'),
  }
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
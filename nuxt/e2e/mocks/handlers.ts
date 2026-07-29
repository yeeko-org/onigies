import type { Page, Route } from '@playwright/test'
import { API_BASE } from './auth'

type JsonBody = Record<string, unknown> | unknown[] | string | null

// CatchAll: cualquier request al backend fake que no tenga mock
// específico responde 501 con un mensaje legible. Protege contra tests
// que olvidan mockear un endpoint — en vez de colgarse contra un
// puerto muerto, fallan con "No mock for <METHOD> <URL>".
export async function installMocks(page: Page): Promise<void> {
  const escaped = API_BASE.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const pattern = new RegExp(`^${escaped.replace(/\/api$/, '')}/.*`)
  await page.route(pattern, async (route: Route) => {
    const req = route.request()
    await route.fulfill({
      status: 501,
      contentType: 'application/json',
      body: JSON.stringify({
        detail: `No mock for ${req.method()} ${req.url()}`,
      }),
    })
  })
}

// Helper interno: filtra por método y responde JSON.
async function fulfillMethod(
  page: Page,
  url: string,
  method: string,
  status: number,
  body: JsonBody,
): Promise<void> {
  await page.route(url, async (route: Route) => {
    if (route.request().method() !== method.toUpperCase()) {
      await route.fallback()
      return
    }
    await route.fulfill({
      status,
      contentType: 'application/json',
      body: body === null ? '' : typeof body === 'string'
        ? body : JSON.stringify(body),
    })
  })
}

// ── Login ────────────────────────────────────────────────────────────

export async function mockLoginSuccess(
  page: Page, user: Record<string, unknown>,
): Promise<void> {
  await fulfillMethod(page, `${API_BASE}/login/`, 'POST', 200, user)
}

export async function mockLoginFailure(
  page: Page,
  status = 400,
  body: JsonBody = { non_field_errors: ['Credenciales inválidas'] },
): Promise<void> {
  await fulfillMethod(page, `${API_BASE}/login/`, 'POST', status, body)
}

export async function mockCurrentUser(
  page: Page, user: Record<string, unknown> | null,
): Promise<void> {
  if (user === null) {
    await fulfillMethod(page, `${API_BASE}/login/`, 'GET', 204, null)
  } else {
    await fulfillMethod(page, `${API_BASE}/login/`, 'GET', 200, user)
  }
}

// ── Catálogos / flujo (bootstrap del dashboard e IES) ────────────────

export async function mockCatalogs(
  page: Page, catalogs: JsonBody = {},
): Promise<void> {
  await fulfillMethod(page, `${API_BASE}/catalogs/all/`, 'GET', 200, catalogs)
}

export async function mockFlowStatuses(
  page: Page, statuses: unknown[] = [],
): Promise<void> {
  await fulfillMethod(page, `${API_BASE}/flow/statuses/`, 'GET', 200, statuses)
}

// ── Invitation / register ────────────────────────────────────────────

export async function mockInvitationValid(
  page: Page, uuid: string, payload: Record<string, unknown>,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/invitation/${uuid}/`, 'GET', 200, payload)
}

export async function mockInvitationNotFound(
  page: Page, uuid: string,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/invitation/${uuid}/`, 'GET', 404,
    { detail: 'No encontrada.' })
}

export async function mockInvitationAlreadyRegistered(
  page: Page, uuid: string,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/invitation/${uuid}/`, 'GET', 400,
    { detail: 'Ya registrada.' })
}

export async function mockRegisterSuccess(
  page: Page, uuid: string, user: Record<string, unknown>,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/invitation/${uuid}/register/`, 'POST', 200, user)
}

export async function mockRegisterFailure(
  page: Page, uuid: string, status = 400, body: JsonBody = {},
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/invitation/${uuid}/register/`,
    'POST', status, body)
}

// ── Password recovery ────────────────────────────────────────────────

export async function mockRequestResetSuccess(page: Page): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/`, 'POST', 200,
    { detail: 'Correo enviado.' })
}

export async function mockRequestResetFailure(
  page: Page, status = 400, body: JsonBody = {},
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/`, 'POST', status, body)
}

export async function mockValidateResetToken(
  page: Page, token: string, payload: Record<string, unknown>,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/${token}/`, 'GET', 200, payload)
}

export async function mockValidateResetTokenInvalid(
  page: Page, token: string,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/${token}/`, 'GET', 404,
    { detail: 'Token inválido o expirado.' })
}

export async function mockConfirmResetSuccess(
  page: Page, token: string, user: Record<string, unknown>,
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/${token}/confirm/`,
    'POST', 200, user)
}

export async function mockConfirmResetFailure(
  page: Page, token: string, status = 400, body: JsonBody = {},
): Promise<void> {
  await fulfillMethod(
    page, `${API_BASE}/password-recovery/${token}/confirm/`,
    'POST', status, body)
}
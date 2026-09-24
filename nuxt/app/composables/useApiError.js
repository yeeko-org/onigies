import { useDashboardStore } from '~/store/dash.js'

// Composable para extraer y notificar errores de la API DRF.
// Cubre las formas comunes de respuesta:
// - { detail: '...' } o { detail: ['...', ...] }   (errores genéricos)
// - { field: ['msg', ...], ... }                    (errores de validación)
// - ['msg', ...]                                    (ValidationError con lista)
// - string plano                                    (respuestas no JSON)
// Varios mensajes se unen uno por renglón: el snackbar respeta los saltos.

const flatten = (value) => {
  if (value === null || value === undefined) return []
  if (Array.isArray(value)) return value.flatMap(flatten)
  if (typeof value === 'object') return Object.values(value).flatMap(flatten)
  return [String(value)]
}

export function useApiError() {
  const dashStore = useDashboardStore()

  function extractMessage(err, fallback = 'Error al procesar la solicitud') {
    const data = err?.response?.data
    if (!data) return fallback
    if (typeof data === 'string') return data
    const source = (!Array.isArray(data) && data.detail !== undefined)
      ? data.detail : data
    const messages = flatten(source).filter((msg) => msg.trim())
    return messages.length ? messages.join('\n') : fallback
  }

  function notifyApiError(err, fallback) {
    const msg = extractMessage(err, fallback)
    dashStore.showError(`Error: ${msg}`)
    return msg
  }

  return { extractMessage, notifyApiError }
}

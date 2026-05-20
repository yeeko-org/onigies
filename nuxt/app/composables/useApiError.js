import { useDashboardStore } from '~/store/dash.js'

// Composable para extraer y notificar errores de la API DRF.
// Cubre tres formas comunes de respuesta:
// - { detail: '...' }                 (errores genéricos)
// - { field: ['msg', ...] }           (errores de validación)
// - string plano                      (respuestas no JSON)

export function useApiError() {
  const dashStore = useDashboardStore()

  function extractMessage(err, fallback = 'Error al procesar la solicitud') {
    const data = err?.response?.data
    if (!data) return fallback
    if (typeof data === 'string') return data
    if (data.detail) return data.detail
    const firstField = Object.keys(data)[0]
    if (firstField) {
      const val = data[firstField]
      return Array.isArray(val) ? val[0] : String(val)
    }
    return fallback
  }

  function notifyApiError(err, fallback) {
    const msg = extractMessage(err, fallback)
    dashStore.showSnackbar(`Error: ${msg}`)
    return msg
  }

  return { extractMessage, notifyApiError }
}
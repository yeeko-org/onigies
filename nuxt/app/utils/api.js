import { useApiError } from "~/composables/useApiError.js"
import { devWarn } from "~/utils/log.js"

// Contrato uniforme de las acciones CRUD de los stores: éxito -> { data },
// fallo -> { errors }. Los callers leen res.data o res.errors.
// Si se pasa error_msg, fail muestra además el snackbar (con el mensaje del
// servidor si existe, o error_msg como respaldo). Si no, el caller decide la
// presentación (p. ej. errores inline en EditCommon).
// Auto-importadas por Nuxt (carpeta utils/): se usan sin import en .vue;
// en stores/composables .js se importan explícitamente por convención.

export const ok = (response) => ({ data: response.data })

export const fail = (error, error_msg = null) => {
  devWarn(error)
  if (error_msg)
    useApiError().notifyApiError(error, error_msg)
  return { errors: error.response?.data ?? null }
}
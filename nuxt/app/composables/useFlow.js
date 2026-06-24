import { useApiError } from '~/composables/useApiError.js'

/**
 * Centraliza el plumbing del motor de flujo para un objeto concreto: arma el
 * base URL `/flow/{app}/{model}/{pk}/` y expone las dos acciones de escritura
 * (transición y comentario) con su manejo de error vía notifyApiError. El
 * historial NO se pide aquí: llega embebido en el objeto (serializer
 * `flow_events`) y cada acción devuelve el evento creado para que el padre lo
 * agregue a ese array.
 *
 * Los tres identificadores pueden ser valores, refs o getters (se resuelven con
 * `toValue`), para seguir reactivos cuando el pk cambia.
 */
export function useFlow(appLabel, modelName, pk) {
  const { $api } = useNuxtApp()
  const { notifyApiError } = useApiError()

  const sending = ref(false)

  const base = computed(() =>
    `/flow/${toValue(appLabel)}/${toValue(modelName)}/${toValue(pk)}`)

  // Devuelve el FlowEvent creado en éxito, undefined en error (ya notificado).
  async function addComment(text) {
    const comment = (text || '').trim()
    if (!comment) return
    sending.value = true
    try {
      const res = await $api.post(`${base.value}/events/`, { comment })
      return res.data
    } catch (e) {
      notifyApiError(e, 'No se pudo agregar el comentario.')
    } finally {
      sending.value = false
    }
  }

  // Devuelve el FlowEvent en éxito, undefined en error (ya notificado).
  async function transition(targetStatus, comment = '') {
    sending.value = true
    try {
      const res = await $api.post(`${base.value}/transitions/`, {
        target_status: targetStatus,
        comment: comment || '',
      })
      return res.data
    } catch (e) {
      notifyApiError(e, 'No se pudo ejecutar la acción.')
    } finally {
      sending.value = false
    }
  }

  return { sending, base, addComment, transition }
}

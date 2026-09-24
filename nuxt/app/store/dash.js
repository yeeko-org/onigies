import { defineStore } from 'pinia'

export const useDashboardStore = defineStore('dash', {
  state: () => ({
    global_snackbar: false,
    global_snackbar_message: '',
    // `{label, handler}` opcional: un botón que ofrece el siguiente paso
    // sin darlo (p. ej. marcar el observable como completado).
    global_snackbar_action: null,
    global_snackbar_color: 'success',
  }),
  actions: {
    showSnackbar(message = 'Cambios guardados', action = null) {
      this.global_snackbar_message = message
      this.global_snackbar_action = action
      this.global_snackbar_color = 'success'
      this.global_snackbar = true
    },
    // Un error nunca se pinta con el color de éxito.
    showError(message) {
      this.global_snackbar_message = message
      this.global_snackbar_action = null
      this.global_snackbar_color = 'error'
      this.global_snackbar = true
    },
  },
});

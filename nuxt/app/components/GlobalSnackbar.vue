<script setup>
/**
 * Aviso global de la aplicación (`dashStore.showSnackbar`).
 *
 * Vive en el layout, no en las páginas, y lo montan LOS DOS: `dashboard.vue`
 * (revisión) e `ies.vue` (institución). Sin él en un layout, ese lado de la
 * aplicación pierde en silencio tanto las confirmaciones de guardado como los
 * errores de `notifyApiError`, que se publican por este mismo store.
 */
import { storeToRefs } from 'pinia'
import { useDashboardStore } from '~/store/dash.js'

const { global_snackbar, global_snackbar_message, global_snackbar_action } =
  storeToRefs(useDashboardStore())

// Con acción el aviso espera más: es una oferta que hay que alcanzar a leer
// y a pulsar, no una confirmación.
const timeout = computed(() => (global_snackbar_action.value ? 12000 : 4000))

function runAction() {
  const action = global_snackbar_action.value
  global_snackbar.value = false
  action?.handler?.()
}
</script>

<template>
  <v-snackbar
    v-model="global_snackbar"
    color="success"
    location="right bottom"
    location-strategy="connected"
    :timeout="timeout"
  >
    {{ global_snackbar_message || 'Cambios guardados' }}
    <template #actions>
      <v-btn
        v-if="global_snackbar_action"
        color="white"
        variant="outlined"
        class="mr-1"
        @click="runAction"
      >
        {{ global_snackbar_action.label }}
      </v-btn>
      <v-btn
        color="accent"
        variant="text"
        @click="global_snackbar = false"
      >
        Cerrar
      </v-btn>
    </template>
  </v-snackbar>
</template>

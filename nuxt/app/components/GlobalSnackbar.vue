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

const { global_snackbar, global_snackbar_message } =
  storeToRefs(useDashboardStore())
</script>

<template>
  <v-snackbar
    v-model="global_snackbar"
    color="success"
    location="right bottom"
    location-strategy="connected"
    timeout="4000"
  >
    {{ global_snackbar_message || 'Cambios guardados' }}
    <template #actions>
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

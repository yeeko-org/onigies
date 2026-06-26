<script setup>
/**
 * Diálogo genérico de "transición bloqueada": se abre cuando las entry_rules
 * de un status destino no se cumplen. Presentacional; quien lo invoca arma el
 * título y la lista de motivos (reasons) a partir de las reglas que fallaron.
 */
defineProps({
  title: { type: String, default: 'Aún no puedes hacer este cambio' },
  reasons: { type: Array, default: () => [] },
})

const open = defineModel({ type: Boolean, default: false })
</script>

<template>
  <v-dialog v-model="open" max-width="560">
    <v-card>
      <v-card-title class="text-h6">{{ title }}</v-card-title>
      <v-card-text>
        <template v-if="reasons.length">
          <v-alert type="info" variant="tonal" class="mb-3">
            <b>Antes debes completar:</b>
            <ul class="ml-4">
              <li v-for="(r, i) in reasons" :key="i" class="mb-1">{{ r }}</li>
            </ul>
          </v-alert>
        </template>
        <div v-else class="text-body-2">
          Revisa los requisitos de este cambio antes de continuar.
        </div>
      </v-card-text>
      <v-card-actions class="mx-3 mb-2">
        <slot name="extra-actions" />
        <v-spacer />
        <v-btn variant="elevated" color="primary" @click="open = false">
          Entendido, regresar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
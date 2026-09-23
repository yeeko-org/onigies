<script setup>
/**
 * Renglón colapsado de la colección «Ejes del cuestionario»: institución,
 * periodo y eje como título; HeaderCommon pinta el chip de status del eje
 * y aquí se suma el conteo de observables por status, el más urgente
 * primero.
 */
import HeaderCommon from
  '~/components/dashboard/common/generic/HeaderCommon.vue'
import CpStatusCounts from
  '~/components/dashboard/answer/capture/CpStatusCounts.vue'

defineProps({
  main: Object,
  collection_data: Object,
  show_details: { type: Boolean, default: false },
})
</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
    :width="360"
  >
    <template #icon>
      <v-icon :color="main.axis_full?.color" class="ml-3">
        {{ main.axis_full?.icon || 'checklist' }}
      </v-icon>
    </template>
    <template #title>
      <div class="ml-2">
        <div class="text-caption text-grey-darken-1">
          {{ main.institution_acronym }} - {{ main.period }}
        </div>
        <div class="font-weight-bold">
          {{ main.axis_full?.name }}
        </div>
      </div>
    </template>
    <template #details>
      <CpStatusCounts :counts="main.observables_by_status" />
    </template>
  </HeaderCommon>
</template>

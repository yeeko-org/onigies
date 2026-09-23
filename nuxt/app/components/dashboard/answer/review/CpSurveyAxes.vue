<script setup>
/**
 * Sección «Cuestionario principal» del detalle de un survey en el
 * dashboard: los ejes (raíces del flujo `cp`) con su status y el conteo
 * de observables por status, y el acceso a cada uno. El eje se abre en un
 * diálogo con el mismo detalle de revisión que la colección «Ejes del
 * cuestionario» (CpAxisCapture en modo revisión).
 *
 * `axisValues` son las filas resumidas del detalle del survey; se
 * actualizan en sitio con lo que el diálogo reporta, para que la sección
 * no quede atrasada al cerrarlo.
 */
import { storeToRefs } from 'pinia'
import { useMainStore } from '~/store/index.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import CpAxisCapture from
  '~/components/dashboard/answer/capture/CpAxisCapture.vue'
import CpStatusCounts from
  '~/components/dashboard/answer/capture/CpStatusCounts.vue'

const props = defineProps({
  axisValues: { type: Array, default: () => [] },
  // Título del diálogo: «FP - 2025».
  context: { type: String, default: '' },
})

const { cats } = storeToRefs(useMainStore())

const axesById = computed(() => Object.fromEntries(
  (cats.value?.axis || []).map((axis) => [axis.id, axis])))

// En el orden del instrumento (Axis.order), no en el de la base.
const rows = computed(() => props.axisValues
  .map((av) => ({ av, axis: axesById.value[av.axis] || {} }))
  .sort((a, b) => (a.axis.order || 0) - (b.axis.order || 0)))

const openRow = ref(null)

function onFlowChanged(brief) {
  const row = props.axisValues.find((av) => av.id === brief.id)
  if (!row) return
  row.status = brief.status
  row.observables_by_status = brief.observables_by_status
}
</script>

<template>
  <v-card elevation="6" class="pa-3 mt-4" data-testid="cp-survey-axes">
    <v-card-title class="d-flex align-center ga-3">
      <v-icon start>checklist</v-icon>
      <span>Cuestionario principal</span>
    </v-card-title>
    <v-card-text class="py-1 text-body-2 text-grey-darken-1 font-italic">
      Los ejes del cuestionario: cada uno se envía y se revisa por
      separado.
    </v-card-text>
    <v-card-text>
      <v-alert v-if="!rows.length" type="info" variant="tonal">
        Este cuestionario aún no tiene ejes.
      </v-alert>
      <v-list v-else lines="one" density="comfortable">
        <v-list-item
          v-for="{ av, axis } in rows"
          :key="av.id"
          class="px-2"
          @click="openRow = av"
        >
          <template #prepend>
            <v-icon :color="axis.color">{{ axis.icon || 'checklist' }}</v-icon>
          </template>
          <div class="d-flex align-center flex-wrap ga-3">
            <span class="font-weight-medium cp-axis-name">
              {{ axis.name || `Eje ${av.axis}` }}
            </span>
            <FlowStatusChip :status="av.status" x-small />
            <CpStatusCounts :counts="av.observables_by_status" />
          </div>
          <template #append>
            <v-btn
              variant="text"
              append-icon="chevron_right"
              @click.stop="openRow = av"
            >
              Revisar eje
            </v-btn>
          </template>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-dialog
      :model-value="!!openRow"
      max-width="1200"
      scrollable
      @update:model-value="openRow = null"
    >
      <v-card v-if="openRow">
        <v-card-title class="d-flex align-center">
          <span class="text-subtitle-1 text-grey-darken-1">
            {{ context }}
          </span>
          <v-spacer />
          <v-btn
            icon="close"
            variant="text"
            aria-label="Cerrar"
            @click="openRow = null"
          />
        </v-card-title>
        <v-card-text class="pt-0">
          <CpAxisCapture
            :axis-value-id="openRow.id"
            review
            @flow-changed="onFlowChanged"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<style scoped>
.cp-axis-name {
  min-width: 220px;
}
</style>

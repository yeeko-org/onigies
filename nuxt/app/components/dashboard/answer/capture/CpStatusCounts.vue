<script setup>
/**
 * Conteo de objetos del flujo por status como fila de chips (ícono y
 * color del catálogo), el más urgente primero. Lo comparten la captura
 * de la IES, el renglón del eje en el dashboard y la sección del
 * cuestionario principal en el detalle del survey.
 */
import { useFlowStore } from '~/store/flow.js'
import { statusRows } from '~/utils/cp_capture.js'

const props = defineProps({
  // `{status: n}`, p. ej. `observables_by_status`.
  counts: { type: Object, default: () => ({}) },
  // Sustantivo del tooltip: «3 observables · En llenado».
  noun: { type: String, default: 'observables' },
})

const flowStore = useFlowStore()

const rows = computed(() => statusRows(props.counts, flowStore.getStatus))
</script>

<template>
  <span class="d-inline-flex align-center flex-wrap ga-1">
    <v-chip
      v-for="row in rows"
      :key="row.name"
      :color="row.st.color"
      size="small"
      variant="tonal"
    >
      <v-icon start>{{ row.st.icon }}</v-icon>
      {{ row.count }}
      <v-tooltip activator="parent" location="top">
        {{ row.count }} {{ noun }} · {{ row.st.public_name }}
      </v-tooltip>
    </v-chip>
  </span>
</template>

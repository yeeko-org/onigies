<script setup>
/**
 * Renglón colapsado de la colección «Cuestionarios de las IES»: institución y
 * periodo como título, y en los detalles el estado del envío de generales más
 * el avance de sus grupos.
 *
 * Survey no tiene campo de nombre, así que el título va por slot; y su status
 * de flujo no es propio sino el de su `general_package` (raíz del flujo gen),
 * por eso el chip se pinta aquí y no lo resuelve HeaderCommon.
 */
import HeaderCommon from
  '~/components/dashboard/common/generic/HeaderCommon.vue'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import { useFlowStore } from '~/store/flow.js'

const props = defineProps({
  main: Object,
  collection_data: Object,
  show_details: { type: Boolean, default: false },
})

const flowStore = useFlowStore()

const generalPackage = computed(() => props.main?.general_package || null)

// `groups_by_status` viene del payload de lista: {status: cuántos grupos}.
// Se muestra como una fila de chips ordenada por prioridad del status, para
// leer de un vistazo qué falta sin abrir el cuestionario.
const groupCounts = computed(() => {
  const counts = generalPackage.value?.groups_by_status || {}
  return Object.entries(counts)
    .map(([name, total]) => ({ name, total, st: flowStore.getStatus(name) }))
    .sort((a, b) => (b.st?.priority || 0) - (a.st?.priority || 0))
})
</script>

<template>
  <HeaderCommon
    :main="main"
    :show_details="show_details"
    :collection_data="collection_data"
  >
    <template #title>
      {{ main.institution_full?.acronym || main.institution_full?.name }}
      - {{ main.period }}
    </template>
    <template #details>
      <FlowStatusChip
        v-if="generalPackage"
        :status="generalPackage.status"
        size="small"
        label="Generales:"
        class="mr-2"
      />
      <v-chip
        v-for="item in groupCounts"
        :key="item.name"
        :color="item.st?.color || 'grey'"
        size="small"
        variant="tonal"
        class="mr-1"
      >
        <v-icon start>{{ item.st?.icon || 'trip_origin' }}</v-icon>
        <b class="mr-1">{{ item.total }}</b>
        {{ item.st?.public_name || item.name }}
      </v-chip>
    </template>
  </HeaderCommon>
</template>

<script setup>
/**
 * Render read-only del historial del objeto (cambios de status + comentarios),
 * en orden cronológico. Presentacional: recibe los eventos ya cargados; no
 * hace fetch. Se reusa en la tarjeta de comentarios (FlowComments) y en el
 * diálogo de transición con comentario (FlowStatusActions).
 */
import { useDates } from '~/composables/useDates.js'
import { useFlowStore } from '~/store/flow.js'
import { useMainStore } from '~/store/index.js'
import { flowRoleOf } from '~/composables/flowRules.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'

const props = defineProps({
  events: { type: Array, default: () => [] },
})

const flowStore = useFlowStore()
const mainStore = useMainStore()
const { formatDate } = useDates()

// Más antiguo arriba; resuelve color del punto y datos de la persona
// (rol + nombre) desde los catálogos; los eventos solo traen el id.
const timeline = computed(() =>
  [...props.events]
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    .map((ev) => {
      const user = mainStore.users_by_id[ev.user]
      return {
        ...ev,
        dotColor: flowStore.getStatus(ev.to_status)?.color || 'grey',
        roleLabel: mainStore.cats?.flow_roles?.[flowRoleOf(user)] || '',
        fullName: user?.full_name || user?.username || 'Revisora',
      }
    }))
</script>

<template>
  <v-timeline
    v-if="timeline.length"
    side="end"
    density="compact"
    truncate-line="both"
    class="my-2"
  >
    <v-timeline-item
      v-for="ev in timeline"
      :key="ev.id"
      :dot-color="ev.dotColor"
      size="small"
    >
      <div class="d-flex align-center flex-wrap ga-2">
        <span class="text-caption">
          <strong v-if="ev.roleLabel">{{ ev.roleLabel }}</strong>
          {{ ev.fullName }}
        </span>
        <span class="text-caption text-medium-emphasis">
          · {{ formatDate(ev.created_at) }}
        </span>
        <FlowStatusChip
          v-if="ev.to_status"
          :status="ev.to_status"
          size="x-small"
        />
      </div>
      <div v-if="ev.comment" class="text-body-2 mt-1">
        {{ ev.comment }}
      </div>
    </v-timeline-item>
  </v-timeline>

  <p v-else class="text-caption text-medium-emphasis my-2">
    Sin comentarios ni movimientos todavía.
  </p>
</template>
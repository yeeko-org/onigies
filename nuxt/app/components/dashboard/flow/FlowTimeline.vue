<script setup>
/**
 * Render del historial del objeto (cambios de status + comentarios), en
 * orden cronológico. Presentacional: recibe los eventos ya cargados; no
 * hace fetch.
 *
 * Con `canEdit` (ev → boolean) muestra lápiz y bote junto a los comentarios
 * que la persona puede tocar, y emite `edit(ev, text)` / `delete(ev)`; la
 * llamada y la mutación del registro son del padre.
 */
import { useDates } from '~/composables/useDates.js'
import { useFlowStore } from '~/store/flow.js'
import { useMainStore } from '~/store/index.js'
import { flowRoleOf } from '~/composables/flowRules.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'

const props = defineProps({
  events: { type: Array, default: () => [] },
  canEdit: { type: Function, default: null },
  // Una edición o un borrado en vuelo: congela los controles.
  busy: Boolean,
})

const emit = defineEmits(['edit', 'delete'])

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
      const isAdmin = flowStore.isAdminEvent(ev)
      return {
        ...ev,
        isAdmin,
        dotColor: isAdmin ? 'grey-darken-3'
          : (flowStore.getStatus(ev.to_status)?.color || 'grey'),
        roleLabel: mainStore.cats?.flow_roles?.[flowRoleOf(user)] || '',
        fullName: user?.full_name || user?.username || 'Revisora',
        editable: !!props.canEdit?.(ev),
      }
    }))

const statusName = (name) => flowStore.getStatus(name)?.public_name || name

// Un solo comentario en edición o en confirmación de borrado a la vez.
const editingId = ref(null)
const draft = ref('')
const confirmingId = ref(null)

function startEdit(ev) {
  confirmingId.value = null
  editingId.value = ev.id
  draft.value = ev.comment
}

function cancelEdit() {
  editingId.value = null
  draft.value = ''
}

function saveEdit(ev) {
  const text = draft.value.trim()
  if (!text || text === ev.comment) return cancelEdit()
  emit('edit', ev, text)
}

function askDelete(ev) {
  cancelEdit()
  confirmingId.value = ev.id
}

// El padre confirma el éxito cambiando `events`: el comentario editado ya
// trae el texto guardado, o el borrado desapareció o quedó vacío.
watch(() => props.events, () => {
  const byId = Object.fromEntries(props.events.map((e) => [e.id, e]))
  const editing = byId[editingId.value]
  if (editingId.value
    && (!editing || editing.comment === draft.value.trim()))
    cancelEdit()
  if (confirmingId.value && !byId[confirmingId.value]?.comment)
    confirmingId.value = null
}, { deep: true })
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
      width="100%"
      :data-testid="ev.isAdmin ? 'flow-admin-event' : undefined"
    >
      <template v-if="ev.isAdmin" #icon>
        <v-icon size="14" color="white" aria-hidden="true">
          admin_panel_settings
        </v-icon>
      </template>
      <!-- width="100%" en el ítem: el cuerpo de v-timeline-item se ajusta a
           su contenido (justify-self: flex-start), y sin ancho fijo el
           v-spacer no empuja los íconos al borde ni el textarea lo llena. -->
      <div class="d-flex align-center flex-wrap ga-2">
        <span class="text-caption">
          <strong v-if="ev.roleLabel">{{ ev.roleLabel }}</strong>
          {{ ev.fullName }}
        </span>
        <span class="text-caption text-medium-emphasis">
          · {{ formatDate(ev.created_at) }}
        </span>
        <!-- Cambio administrativo: el texto es la señal; color e ícono la
             refuerzan. Origen y destino, porque aquí el origen no se
             deduce del flujo. -->
        <template v-if="ev.isAdmin">
          <v-chip
            size="x-small"
            label
            variant="outlined"
            color="grey-darken-3"
            prepend-icon="admin_panel_settings"
          >
            Cambio administrativo
          </v-chip>
          <span class="d-inline-flex align-center ga-1">
            <span class="d-sr-only">
              de {{ statusName(ev.from_status) }} a
              {{ statusName(ev.to_status) }}
            </span>
            <FlowStatusChip
              :status="ev.from_status"
              size="x-small"
              variant="outlined"
              aria-hidden="true"
            />
            <v-icon size="14" aria-hidden="true">arrow_forward</v-icon>
            <FlowStatusChip
              :status="ev.to_status"
              size="x-small"
              aria-hidden="true"
            />
          </span>
        </template>
        <FlowStatusChip
          v-else-if="ev.to_status"
          :status="ev.to_status"
          size="x-small"
        />
        <template v-if="ev.editable && editingId !== ev.id">
          <v-spacer />
          <v-btn
            icon
            variant="text"
            size="x-small"
            density="comfortable"
            aria-label="Editar comentario"
            :disabled="busy"
            data-testid="flow-comment-edit"
            @click="startEdit(ev)"
          >
            <v-icon size="16">edit</v-icon>
            <v-tooltip activator="parent" location="top">
              Editar comentario
            </v-tooltip>
          </v-btn>
          <v-btn
            v-if="!ev.isAdmin"
            icon
            variant="text"
            size="x-small"
            density="comfortable"
            aria-label="Borrar comentario"
            :disabled="busy"
            data-testid="flow-comment-delete"
            @click="askDelete(ev)"
          >
            <v-icon size="16">delete</v-icon>
            <v-tooltip activator="parent" location="top">
              Borrar comentario
            </v-tooltip>
          </v-btn>
        </template>
      </div>

      <div v-if="editingId === ev.id" class="mt-2">
        <v-textarea
          v-model="draft"
          :label="ev.isAdmin ? 'Motivo del cambio' : 'Comentario'"
          variant="outlined"
          rows="2"
          auto-grow
          hide-details
          density="compact"
          autofocus
        />
        <div class="d-flex justify-end ga-2 mt-2">
          <v-btn
            size="small"
            variant="text"
            :disabled="busy"
            @click="cancelEdit"
          >
            Cancelar
          </v-btn>
          <v-btn
            size="small"
            color="accent"
            variant="tonal"
            :loading="busy"
            :disabled="!draft.trim() || draft.trim() === ev.comment"
            data-testid="flow-comment-save"
            @click="saveEdit(ev)"
          >
            Guardar
          </v-btn>
        </div>
      </div>
      <div v-else-if="ev.comment" class="text-body-2 mt-1">
        <strong v-if="ev.isAdmin">Motivo:</strong>
        {{ ev.comment }}
      </div>

      <!-- Confirmación ligera en línea, sin diálogo encima del diálogo. -->
      <div
        v-if="confirmingId === ev.id"
        class="d-flex align-center flex-wrap ga-2 mt-2 text-body-2"
        role="group"
        aria-label="Confirmar borrado del comentario"
      >
        <span>
          {{ ev.to_status
            ? '¿Borrar este comentario? El cambio de estatus se conserva.'
            : '¿Borrar este comentario?' }}
        </span>
        <v-btn
          size="small"
          variant="text"
          :disabled="busy"
          @click="confirmingId = null"
        >
          Cancelar
        </v-btn>
        <v-btn
          size="small"
          color="error"
          variant="tonal"
          :loading="busy"
          data-testid="flow-comment-delete-confirm"
          @click="emit('delete', ev)"
        >
          Borrar
        </v-btn>
      </div>
    </v-timeline-item>
  </v-timeline>

  <p v-else class="text-caption text-medium-emphasis my-2">
    Sin comentarios ni movimientos todavía.
  </p>
</template>
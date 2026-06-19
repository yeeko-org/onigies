<script setup>
/**
 * Timeline del objeto del flujo: cambios de status + comentarios puros,
 * con caja para agregar un comentario nuevo.
 *
 * GET  /flow/{app}/{model}/{pk}/events/  → lista de FlowEvent
 * POST /flow/{app}/{model}/{pk}/events/  → { comment } (comentario puro)
 *
 * Sirve igual a IES y revisora, a nivel paquete y práctica.
 * Emite `commented(flowEvent)` al agregar uno (por si el padre refresca).
 */
import { useApiError } from '~/composables/useApiError.js'
import { useDates } from '~/composables/useDates.js'
import { useDashboardStore } from '~/store/dash.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  pk:        { type: Number, required: true },
})

const emit = defineEmits(['commented'])

const { $api } = useNuxtApp()
const { notifyApiError } = useApiError()
const { formatDate } = useDates()
const dashStore = useDashboardStore()

const events = ref([])
const loading = ref(false)
const sending = ref(false)
const newComment = ref('')

const base = computed(
  () => `/flow/${props.appLabel}/${props.modelName}/${props.pk}`)

// Orden cronológico (más antiguo arriba); la caja de escribir queda abajo.
const timeline = computed(() =>
  [...events.value].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)))

async function loadEvents() {
  loading.value = true
  try {
    const res = await $api.get(`${base.value}/events/`)
    events.value = res.data
  } catch (e) {
    notifyApiError(e, 'No se pudo cargar el historial.')
  } finally {
    loading.value = false
  }
}

async function addComment() {
  const text = newComment.value.trim()
  if (!text) return
  sending.value = true
  try {
    const res = await $api.post(`${base.value}/events/`, { comment: text })
    events.value.push(res.data)
    newComment.value = ''
    emit('commented', res.data)
  } catch (e) {
    notifyApiError(e, 'No se pudo agregar el comentario.')
  } finally {
    sending.value = false
  }
}

// Permite al padre forzar un refresco tras una transición.
defineExpose({ loadEvents })

onMounted(loadEvents)
watch(() => props.pk, loadEvents)
</script>

<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <v-timeline
      v-else-if="timeline.length"
      side="end"
      density="compact"
      truncate-line="both"
      class="my-2"
    >
      <v-timeline-item
        v-for="ev in timeline"
        :key="ev.id"
        :dot-color="ev.to_status?.color || 'grey'"
        size="small"
      >
        <div class="d-flex align-center flex-wrap ga-2">
          <span class="text-caption text-medium-emphasis">
            {{ ev.user_name || 'Sistema' }} · {{ formatDate(ev.created_at) }}
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

    <div class="d-flex align-end ga-2 mt-2">
      <v-textarea
        v-model="newComment"
        label="Agregar comentario"
        variant="outlined"
        rows="2"
        auto-grow
        hide-details
        density="compact"
      />
      <v-btn
        color="accent"
        variant="tonal"
        :loading="sending"
        :disabled="!newComment.trim()"
        prepend-icon="send"
        @click="addComment"
      >
        Comentar
      </v-btn>
    </div>
  </div>
</template>

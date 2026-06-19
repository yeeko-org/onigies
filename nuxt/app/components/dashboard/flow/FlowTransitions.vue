<script setup>
/**
 * Muestra los botones de transición disponibles para un objeto del flujo
 * y ejecuta la transición vía POST /flow/{app}/{model}/{pk}/transitions/.
 *
 * Emite `transitioned(flowEvent)` al completarse (flowEvent incluye
 * to_status con color, icon, public_name, role).
 */
import { useApiError } from '~/composables/useApiError.js'
import { useDashboardStore } from '~/store/dash.js'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  pk:        { type: Number, required: true },
  // Status actual del objeto (StatusBrief); solo para explicar por qué no
  // hay acciones cuando la lista de transiciones llega vacía.
  status:    { type: Object, default: null },
})

const emit = defineEmits(['transitioned'])

const { $api } = useNuxtApp()
const dashStore = useDashboardStore()
const { notifyApiError } = useApiError()

const transitions = ref([])
const loading = ref(false)
const executing = ref(null)       // name del status en ejecución
const commentDialog = ref(false)
const pendingTransition = ref(null)
const comment = ref('')

const base = computed(
  () => `/flow/${props.appLabel}/${props.modelName}/${props.pk}`)

// Sin acciones: si el status tiene role, el turno es de la otra parte; sin
// role, es un estado final.
const emptyMessage = computed(() => {
  const role = props.status?.role
  if (!role) return 'Sin acciones: este estado es final.'
  if (role === 'ies') return 'En espera de la institución.'
  if (role === 'reviewer') return 'En espera de la revisión.'
  return 'Sin acciones disponibles.'
})

async function loadTransitions() {
  loading.value = true
  try {
    const res = await $api.get(`${base.value}/transitions/`)
    transitions.value = res.data
  } catch (e) {
    notifyApiError(e, 'No se pudieron cargar las acciones disponibles.')
  } finally {
    loading.value = false
  }
}

function onTransitionClick(t) {
  if (t.requires_comment) {
    pendingTransition.value = t
    comment.value = ''
    commentDialog.value = true
  } else {
    executeTransition(t, '')
  }
}

async function executeTransition(t, commentText) {
  executing.value = t.name
  commentDialog.value = false
  try {
    const res = await $api.post(`${base.value}/transitions/`, {
      target_status: t.name,
      comment: commentText || '',
    })
    dashStore.showSnackbar(
      `Estado cambiado a "${t.public_name}"`)
    emit('transitioned', res.data)
    await loadTransitions()
  } catch (e) {
    notifyApiError(e, 'No se pudo ejecutar la acción.')
  } finally {
    executing.value = null
  }
}

function confirmComment() {
  if (!pendingTransition.value) return
  executeTransition(pendingTransition.value, comment.value)
  pendingTransition.value = null
}

onMounted(loadTransitions)
watch(() => props.pk, loadTransitions)
</script>

<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <div v-else-if="transitions.length" class="d-flex flex-wrap ga-2">
      <v-btn
        v-for="t in transitions"
        :key="t.name"
        :color="t.color || 'primary'"
        variant="tonal"
        size="small"
        :loading="executing === t.name"
        :prepend-icon="t.icon || 'arrow_forward'"
        @click="onTransitionClick(t)"
      >
        {{ t.public_name }}
      </v-btn>
    </div>

    <div v-else class="text-caption text-grey-darken-1 font-italic">
      {{ emptyMessage }}
    </div>

    <v-dialog v-model="commentDialog" max-width="480" persistent>
      <v-card v-if="pendingTransition">
        <v-card-title class="text-subtitle-1">
          {{ pendingTransition.public_name }}
        </v-card-title>
        <v-card-text>
          <v-textarea
            v-model="comment"
            label="Comentario *"
            variant="outlined"
            rows="3"
            auto-grow
          />
        </v-card-text>
        <v-card-actions class="mx-3 mb-2">
          <v-btn
            variant="text"
            @click="commentDialog = false; pendingTransition = null"
          >
            Cancelar
          </v-btn>
          <v-spacer />
          <v-btn
            :color="pendingTransition.color || 'primary'"
            variant="flat"
            :disabled="!comment.trim()"
            @click="confirmComment"
          >
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

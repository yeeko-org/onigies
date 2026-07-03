<script setup>
/**
 * Tarjeta de comentarios del objeto del flujo (look tipo nota de Comments.vue):
 * muestra el acumulado y, al abrirla, despliega un diálogo con el timeline
 * completo (FlowTimeline: cambios de status + comentarios) y una caja para
 * agregar un comentario puro.
 *
 * El historial vive embebido en el registro (`flow_events`); al agregar un
 * comentario lo empuja a ese array. Sirve igual a IES y revisora, 
 * a nivel paquete y práctica.
 */
import { useFlow } from '~/composables/useFlow.js'
import { useFlowStore } from '~/store/flow.js'
import { useAuthStore } from '~/store/auth.js'
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  width:     { type: Number, default: 280 },
})

// Registro completo (con flow_events). Lo mutamos en sitio al comentar.
const record = defineModel({ type: Object, required: true })

const { sending, addComment } = useFlow(
  () => props.appLabel, () => props.modelName, () => record.value?.id)

const flowStore = useFlowStore()
const auth = useAuthStore()

// Solo comenta quien tiene el turno del registro: la IES no comenta cuando el
// objeto está del lado de la revisora y viceversa. El timeline sigue visible
// para ambos; solo se oculta la caja de captura.
const canComment = computed(
  () => flowStore.getStatus(record.value?.status)?.role === auth.flow_role)

const open = ref(false)
const newComment = ref('')

const events = computed(() => record.value?.flow_events || [])

const commentCount = computed(
  () => events.value.filter((e) => e.comment).length)

const lastComment = computed(() => {
  const withText = events.value.filter((e) => e.comment)
  return withText.length ? withText[withText.length - 1].comment : ''
})

async function onAdd() {
  const ev = await addComment(newComment.value)
  if (!ev) return
  newComment.value = ''
  if (!record.value.flow_events)
    record.value.flow_events = []
  record.value.flow_events.push(ev)
}
</script>

<template>
  <div>
    <!-- Con historial: tarjeta amarilla compacta que abre el diálogo. -->
    <v-card
      v-if="events.length"
      color="yellow-accent-4"
      variant="flat"
      :width="width"
      class="d-flex align-center border-lg"
      style="cursor: pointer;"
      @click="open = true"
    >
      <v-icon class="ml-2" color="yellow-darken-3">sticky_note_2</v-icon>
      <v-card-text class="px-2 py-1" style="overflow: hidden;">
        <span class="font-weight-medium">Comentarios</span>
        <span class="text-medium-emphasis"> ({{ commentCount }})</span>
        <div v-if="lastComment" class="text-caption text-truncate">
          {{ lastComment }}
        </div>
      </v-card-text>
      <v-icon class="mr-2" color="yellow-darken-3">open_in_full</v-icon>
    </v-card>

    <!-- Sin historial y es mi turno: botón para abrir el diálogo y comentar. -->
    <v-btn
      v-else-if="canComment"
      color="yellow-accent-4"
      variant="elevated"
      size="small"
      prepend-icon="sticky_note_2"
      @click="open = true"
    >
      Comentar
    </v-btn>

    <v-dialog v-model="open" max-width="600" scrollable>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon start color="yellow-darken-3">sticky_note_2</v-icon>
          Comentarios y movimientos
          <v-spacer />
          <v-btn icon variant="text" @click="open = false">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <FlowTimeline :events="events" />
        </v-card-text>
        <v-divider v-if="canComment" />
        <v-card-actions v-if="canComment" class="d-flex align-end ga-2 pa-3">
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
            @click="onAdd"
          >
            Comentar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
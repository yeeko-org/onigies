<script setup>
/**
 * Tarjeta de comentarios del objeto del flujo (look tipo nota de Comments.vue):
 * muestra el acumulado y, al abrirla, despliega un diálogo con el timeline
 * completo (FlowTimeline: cambios de status + comentarios) y una caja para
 * agregar un comentario puro.
 *
 * El historial vive embebido en el registro (`flow_events`); al agregar,
 * editar o borrar un comentario se muta ese array en sitio. Sirve igual a
 * IES y revisora, en la raíz y en sus descendientes.
 */
import { useFlow } from '~/composables/useFlow.js'
import { useFlowStore } from '~/store/flow.js'
import { useAuthStore } from '~/store/auth.js'
import { useDashboardStore } from '~/store/dash.js'
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  width:     { type: Number, default: 280 },
  // Apaga la captura aunque sea el turno de quien mira: el turno del
  // registro no basta cuando su contenido no se trabaja todavía (p. ej. un
  // grupo cp en consulta previa o con la compuerta de respuesta cerrada).
  readonly:  Boolean,
  // Raíz del flujo (valor o getter) cuando el registro es descendiente: el
  // turno de comentar, editar y borrar lo da ella, como en el backend.
  root:      { type: [Object, Function], default: null },
})

// Registro completo (con flow_events). Lo mutamos en sitio al comentar.
const record = defineModel({ type: Object, required: true })

const { sending, addComment, editComment, deleteComment } = useFlow(
  () => props.appLabel, () => props.modelName, () => record.value?.id)

const flowStore = useFlowStore()
const auth = useAuthStore()
const dashStore = useDashboardStore()

const rootRecord = computed(() => toValue(props.root) || record.value)

// Solo comenta quien tiene el turno de la RAÍZ: la IES no comenta
// cuando el envío está del lado de la revisora y viceversa, aunque el hijo
// esté en un status de su rol. El timeline sigue visible para ambos.
const canComment = computed(() => !props.readonly
  && flowStore.rootRole(rootRecord.value) === auth.flow_role)

// Editar y borrar: raíz en turno, comentario del propio lado y de la ronda
// en curso (flowStore.canEditComment).
const canEditComment = (ev) => !props.readonly
  && flowStore.canEditComment(ev, rootRecord.value)

const open = ref(false)
const newComment = ref('')

const events = computed(() => record.value?.flow_events || [])

const commentCount = computed(
  () => events.value.filter((e) => e.comment).length)

// El más reciente por fecha, no el último del array: la API entrega los
// eventos del más nuevo al más viejo y los agregados en sitio van al final.
const lastComment = computed(() => {
  let newest = null
  for (const ev of events.value) {
    if (!ev.comment) continue
    if (!newest || isNewer(ev, newest)) newest = ev
  }
  return newest?.comment || ''
})

function isNewer(a, b) {
  const diff = new Date(a.created_at) - new Date(b.created_at)
  return diff ? diff > 0 : (a.id || 0) > (b.id || 0)
}

function replaceEvent(ev) {
  const list = record.value.flow_events || []
  const i = list.findIndex((e) => e.id === ev.id)
  if (i >= 0) list.splice(i, 1, ev)
}

async function onEdit(ev, text) {
  const updated = await editComment(ev.id, text)
  if (!updated) return
  replaceEvent(updated)
  dashStore.showSnackbar('Comentario actualizado')
}

async function onDelete(ev) {
  const res = await deleteComment(ev.id)
  if (!res) return
  if (res.removed) {
    const list = record.value.flow_events || []
    const i = list.findIndex((e) => e.id === ev.id)
    if (i >= 0) list.splice(i, 1)
  } else {
    replaceEvent(res.event)
  }
  dashStore.showSnackbar('Comentario eliminado')
}

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
    <!-- Con comentarios: tarjeta amarilla compacta que abre el diálogo. Los
         eventos sin texto (cambios de status, incluido el automático del
         primer guardado) no cuentan: sin ellos sería «Comentarios (0)». -->
    <v-card
      v-if="commentCount"
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

    <!-- Sin comentarios y es mi turno: botón para abrir el diálogo y comentar. -->
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
          <FlowTimeline
            :events="events"
            :can-edit="canEditComment"
            :busy="sending"
            @edit="onEdit"
            @delete="onDelete"
          />
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
<script setup>
/**
 * Control unificado de estado: muestra el status actual (FlowStatusChip) y,
 * cuando es el turno del usuario (role) y hay next_statuses aplicables, lo
 * vuelve activador de un menú con las transiciones disponibles. El `hint` 
 * del status (del catálogo) va como guía persistente bajo el chip.
 *
 * Antes de ejecutar una transición evalúa las `entry_rules` del status destino
 * (compuerta de UX, registry flowRules) sobre el registro; si no se cumplen,
 * abre FlowBlockedDialog con los faltantes en vez de transicionar.
 *
 * Si la transición exige comentario (requires_comment), el diálogo muestra el
 * historial (FlowTimeline, desde flow_events del registro) para no escribirlo
 * aislado del contexto previo.
 */
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlow } from '~/composables/useFlow.js'
import { runEntryRules } from '~/composables/flowRules.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'
import FlowBlockedDialog from '~/components/dashboard/flow/FlowBlockedDialog.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
})

// Registro completo (con status y flow_events): única fuente del display, el
// hint, las acciones y la evaluación de entry_rules. Lo mutamos en sitio al
// transicionar, así el padre no necesita handlers.
const record = defineModel({ type: Object, required: true })

const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const { sending, transition } = useFlow(
  () => props.appLabel, () => props.modelName, () => record.value?.id)

const st = computed(() => flowStore.getStatus(record.value?.status))
const events = computed(() => record.value?.flow_events || [])
const transitions = computed(() => flowStore.getAvailableTransitions(
  record.value?.status, props.appLabel, props.modelName))
const hasActions = computed(() => transitions.value.length > 0)

const commentDialog = ref(false)
const pendingTransition = ref(null)
const comment = ref('')

const blockedDialog = ref(false)
const blockedTitle = ref('')
const blockedReasons = ref([])

function onSelect(t) {
  const { ok, missing } = runEntryRules(t.entry_rules, record.value)
  if (!ok) {
    blockedTitle.value = `Aún no puedes pasar a "${t.public_name}"`
    blockedReasons.value = missing
    blockedDialog.value = true
    return
  }
  if (t.requires_comment) {
    pendingTransition.value = t
    comment.value = ''
    commentDialog.value = true
  } else {
    runTransition(t, '')
  }
}

async function runTransition(t, commentText) {
  const ev = await transition(t.name, commentText)
  if (!ev) return
  closeDialog()
  // Mutamos el registro en sitio: el motor ya devolvió el evento y el nuevo
  // status, así el chip, el hint y el timeline se refrescan sin recargar.
  record.value.status = ev.to_status
  if (!record.value.flow_events)
    record.value.flow_events = []
  record.value.flow_events.push(ev)
  dashStore.showSnackbar(`Estado cambiado a "${t.public_name}"`)
}

function confirmComment() {
  if (pendingTransition.value)
    runTransition(pendingTransition.value, comment.value)
}

function closeDialog() {
  commentDialog.value = false
  pendingTransition.value = null
}
</script>

<template>
  <div v-if="st">
    <!-- Con acciones: el chip es activador del menú de transiciones. -->
    <v-menu v-if="hasActions" location="bottom start">
      <template #activator="{ props: menuProps }">
        <FlowStatusChip v-bind="menuProps" :status="record.status">
          <v-progress-circular
            v-if="sending"
            indeterminate
            size="16"
            width="2"
            class="ml-2"
          />
          <v-icon v-else end>expand_more</v-icon>
        </FlowStatusChip>
      </template>

      <v-list density="compact" min-width="260">
        <v-list-item
          v-for="t in transitions"
          :key="t.name"
          :title="t.public_name"
          :subtitle="t.description"
          @click="onSelect(t)"
        >
          <template #prepend>
            <v-icon :color="t.color || 'primary'">
              {{ t.icon || 'arrow_forward' }}
            </v-icon>
          </template>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Sin acciones: solo display, reusando el mismo chip. -->
    <FlowStatusChip v-else :status="record.status" />

    <!-- Hint persistente: la guía de siguiente paso, tomada del catálogo. -->
    <div
      v-if="st.hint"
      class="text-caption text-medium-emphasis mt-1"
      style="max-width: 320px;"
    >
      {{ st.hint }}
    </div>

    <v-dialog v-model="commentDialog" max-width="520" persistent scrollable>
      <v-card v-if="pendingTransition">
        <v-card-title class="text-subtitle-1">
          {{ pendingTransition.public_name }}
        </v-card-title>
        <v-card-text>
          <div class="text-caption text-medium-emphasis">Historial</div>
          <FlowTimeline :events="events" />
          <v-divider class="my-2" />
          <v-textarea
            v-model="comment"
            label="Comentario *"
            variant="outlined"
            rows="3"
            auto-grow
          />
        </v-card-text>
        <v-card-actions class="mx-3 mb-2">
          <v-btn variant="text" @click="closeDialog">Cancelar</v-btn>
          <v-spacer />
          <v-btn
            :color="pendingTransition.color || 'primary'"
            variant="flat"
            :loading="sending"
            :disabled="!comment.trim()"
            @click="confirmComment"
          >
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <FlowBlockedDialog
      v-model="blockedDialog"
      :title="blockedTitle"
      :reasons="blockedReasons"
    />
  </div>
</template>
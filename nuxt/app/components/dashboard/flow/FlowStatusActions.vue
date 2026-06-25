<script setup>
/**
 * Control unificado de estado: muestra el status (FlowStatusChip) y, cuando es
 * el turno del usuario y hay transiciones aplicables, vuelve el chip activador
 * de un menú (FlowTransitionMenu). El `hint` del status va como guía
 * persistente bajo el chip.
 *
 * Toda la lógica (transiciones disponibles, entry_rules, comentario,
 * ejecución y mutación en sitio) vive en el kernel useFlowActions; aquí solo se
 * aporta el activador-chip y se montan los diálogos compartidos.
 */
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowTransitionMenu from '~/components/dashboard/flow/FlowTransitionMenu.vue'
import FlowTransitionDialogs from '~/components/dashboard/flow/FlowTransitionDialogs.vue'

const props = defineProps({
  appLabel:  { type: String, required: true },
  modelName: { type: String, required: true },
  // Kernel ya construido por el padre, para compartir transiciones y diálogos
  // con otro disparador (p.ej. un botón inferior). Si se omite, se crea propio.
  actions: { type: Object, default: null },
})

// Registro completo (con status y flow_events): única fuente del display, el
// hint y las acciones. El kernel lo muta en sitio al transicionar.
const record = defineModel({ type: Object, required: true })

const flowStore = useFlowStore()
const st = computed(() => flowStore.getStatus(record.value?.status))

const actions = props.actions || useFlowActions(
  record, () => props.appLabel, () => props.modelName)
const { sending, transitions, hasActions, onSelect } = actions
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

      <FlowTransitionMenu :transitions="transitions" @select="onSelect" />
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

    <!-- Si el kernel es externo, el padre monta los diálogos (no duplicar). -->
    <FlowTransitionDialogs v-if="!props.actions" :actions="actions" />
  </div>
</template>
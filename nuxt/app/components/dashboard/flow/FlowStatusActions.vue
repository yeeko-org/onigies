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
import { useAuthStore } from '~/store/auth'
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
const authStore = useAuthStore()
const st = computed(() => flowStore.getStatus(record.value?.status))

// Presentación del hint según a quién le habla: 'mine' = es tu turno
// (hint, énfasis accent), 'theirs' = espera al otro rol (hint_wait, gris),
// 'terminal' = cerrado (hint neutro, tenue). Null = sin hint que mostrar.
const hintMode = computed(() => {
  if (!st.value) return null
  if (!st.value.role) return st.value.hint ? 'terminal' : null
  return st.value.role === authStore.flow_role ? 'mine' : 'theirs'
})
const hintText = computed(() => hintMode.value === 'theirs'
  ? (st.value.hint_wait || st.value.hint)
  : st.value?.hint)
const hintWho = computed(() => {
  if (hintMode.value === 'mine') return 'Te toca'
  return st.value?.role === 'reviewer'
    ? 'En espera de la revisión' : 'En espera de la institución'
})

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

      <FlowTransitionMenu
        :transitions="transitions"
        @select="onSelect"
      />
    </v-menu>

    <!-- Sin acciones: solo display, reusando el mismo chip. -->
    <FlowStatusChip v-else :status="record.status" />

    <!-- Hint persistente, sensible al turno: callout accent cuando te toca,
         gris apagado en espera del otro rol, texto tenue en terminales. -->
    <div
      v-if="hintMode && hintText"
      class="flow-hint mt-1"
      :class="`flow-hint--${hintMode}`"
    >
      <v-icon v-if="hintMode !== 'terminal'" size="14" class="mt-1">
        {{ hintMode === 'mine' ? 'flag' : 'schedule' }}
      </v-icon>
      <div>
        <div v-if="hintMode !== 'terminal'" class="flow-hint__who">
          {{ hintWho }}
        </div>
        {{ hintText }}
      </div>
    </div>

    <!-- Si el kernel es externo, el padre monta los diálogos (no duplicar). -->
    <FlowTransitionDialogs v-if="!props.actions" :actions="actions" />
  </div>
</template>

<style scoped>
.flow-hint {
  display: flex;
  gap: 6px;
  align-items: flex-start;
  max-width: 360px;
  font-size: 0.75rem;
  line-height: 1.4;
  border-radius: 6px;
  padding: 6px 10px;
}
.flow-hint--mine {
  background: #fdf1e0;
  color: #7a4a08;
  border-left: 3px solid #f59322;
}
.flow-hint--theirs {
  background: #f5f5f5;
  color: rgba(0, 0, 0, 0.55);
  border-left: 3px solid #e0e0e0;
}
.flow-hint--terminal {
  background: none;
  padding: 2px 0 0;
  color: rgba(0, 0, 0, 0.45);
}
.flow-hint__who {
  font-size: 0.62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin-bottom: 1px;
  opacity: 0.75;
}
</style>
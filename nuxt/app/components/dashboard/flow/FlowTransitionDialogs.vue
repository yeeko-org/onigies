<script setup>
/**
 * Diálogos del flujo: uno unificado de acción (confirmación y/o comentario
 * opcional u obligatorio, con timeline) + el bloqueo por entry_rules,
 * atados al estado de un kernel useFlowActions. Presentacional: recibe el
 * objeto del kernel y lee/escribe sus refs (siguen reactivas por ser el mismo
 * objeto estable). Lo montan FlowStatusActions y los split-buttons que usan el
 * kernel, para no duplicar el markup de los diálogos.
 */
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'
import FlowBlockedDialog from '~/components/dashboard/flow/FlowBlockedDialog.vue'
import ConfirmActionDialog from
  '~/components/dashboard/common/dialog/ConfirmActionDialog.vue'

const props = defineProps({
  actions: { type: Object, required: true },
})

const {
  sending, actionDialog, pendingTransition, comment, events,
  blockedDialog, blockedTitle, blockedReasons, confirmAction,
} = props.actions

// Rótulo de la caja de comentario: el del catálogo, con un genérico de
// respaldo cuando el status no trae prompt propio (el badge
// Obligatorio/Opcional del diálogo ya distingue ambos casos).
const commentPrompt = computed(() => {
  const t = pendingTransition.value
  if (!t || t.comment_type === 'none') return null
  return t.comment_prompt || 'Escribe tu comentario.'
})
</script>

<template>
  <div>
    <ConfirmActionDialog
      v-if="pendingTransition"
      v-model="actionDialog"
      v-model:comment="comment"
      :title="pendingTransition.confirm_title
        || `¿${pendingTransition.action_name || pendingTransition.public_name}?`"
      :confirm-label="pendingTransition.action_name || 'Confirmar'"
      :comment-prompt="commentPrompt"
      :comment-required="pendingTransition.comment_type === 'required'"
      :loading="sending"
      @confirm="confirmAction"
    >
      <!-- El aviso toma el color del status destino (el motor manda): los
           terminales rojos/cafés se ven severos, los envíos toman su morado. -->
      <v-alert
        v-if="pendingTransition.confirm_text"
        :color="pendingTransition.color || 'warning'"
        :icon="pendingTransition.icon || 'info'"
        variant="tonal"
        border="start"
        density="comfortable"
        class="mb-2"
      >
        {{ pendingTransition.confirm_text }}
      </v-alert>
      <template #comment-history>
        <!-- Historial colapsado por defecto: la acción queda arriba y el
             diálogo no crece con timelines largos. -->
        <v-expansion-panels v-if="events.length" class="mt-3">
          <v-expansion-panel>
            <v-expansion-panel-title class="text-body-2">
              <v-icon start size="18">history</v-icon>
              Historial de comentarios y cambios
              <v-chip size="x-small" class="ml-2">{{ events.length }}</v-chip>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <FlowTimeline :events="events" />
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </template>
    </ConfirmActionDialog>

    <FlowBlockedDialog
      v-model="blockedDialog"
      :title="blockedTitle"
      :reasons="blockedReasons"
    >
      <template #extra-actions>
        <slot name="blocked-actions" />
      </template>
    </FlowBlockedDialog>
  </div>
</template>
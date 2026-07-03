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
// respaldo cuando el status no trae prompt propio. El respaldo distingue
// obligatorio de opcional (p. ej. terminales role=None como bp_rejected, que
// el seed deja sin prompt por rol) para no rotular igual ambos casos.
const commentPrompt = computed(() => {
  const t = pendingTransition.value
  if (!t || t.comment_type === 'none') return null
  if (t.comment_prompt) return t.comment_prompt
  return t.comment_type === 'required'
    ? 'Comentario (obligatorio)'
    : 'Comentario (opcional)'
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
      <v-alert
        v-if="pendingTransition.confirm_text"
        type="warning"
        variant="outlined"
        density="comfortable"
        class="mb-2"
      >
        {{ pendingTransition.confirm_text }}
      </v-alert>
      <template #comment-history>
        <template v-if="events.length">
          <div class="text-caption text-medium-emphasis">
            Historial de comentarios y cambios
          </div>
          <FlowTimeline :events="events" />
          <v-divider class="my-3" />
        </template>
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
<script setup>
/**
 * Diálogos del flujo (comentario obligatorio + bloqueo por entry_rules),
 * atados al estado de un kernel useFlowActions. Presentacional: recibe el
 * objeto del kernel y lee/escribe sus refs (siguen reactivas por ser el mismo
 * objeto estable). Lo montan FlowStatusActions y los split-buttons que usan el
 * kernel, para no duplicar el markup de los diálogos.
 */
import FlowTimeline from '~/components/dashboard/flow/FlowTimeline.vue'
import FlowBlockedDialog from '~/components/dashboard/flow/FlowBlockedDialog.vue'

const props = defineProps({
  actions: { type: Object, required: true },
})

const {
  sending, commentDialog, pendingTransition, comment, events,
  blockedDialog, blockedTitle, blockedReasons,
  confirmComment, closeDialog,
} = props.actions
</script>

<template>
  <div>
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
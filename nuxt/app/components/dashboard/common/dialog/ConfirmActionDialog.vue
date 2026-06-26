<script setup>

const emits = defineEmits(['confirm'])
defineProps({
  title: {
    type: String,
    required: true,
  },
  confirmLabel: {
    type: String,
    default: 'Confirmar',
  },
  confirmIcon: {
    type: String,
    default: 'send',
  },
  cancelLabel: {
    type: String,
    default: 'Cancelar',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  maxWidth: {
    type: [String, Number],
    default: 600,
  },
  // Si se pasa, se renderiza la caja de comentario; el texto va como guía
  // sobre el campo (no como label, suele ser largo).
  commentPrompt: {
    type: String,
    default: null,
  },
  // Obliga a escribir el comentario (botón confirmar deshabilitado si vacío).
  commentRequired: {
    type: Boolean,
    default: false,
  },
});
const dialog_visible = defineModel({ type: Boolean, default: false });
const comment = defineModel('comment', { type: String, default: '' });

</script>

<template>
  <v-dialog
    v-model="dialog_visible"
    :max-width="maxWidth"
    :persistent="loading"
  >
    <v-card>
      <v-card-title>
        {{ title }}
      </v-card-title>
      <v-card-text>
        <!-- Slot por defecto: contenido contextual (alertas, texto, etc.) -->
        <slot />
        <v-card
          v-if="commentPrompt" variant="tonal" class="mt-2"
          color="primary"
        >
          <v-card-text class="py-3">
            <slot name="comment-history" />
            <div class="text-body-2 text-medium-emphasis mb-2">
              {{ commentPrompt }}
            </div>
            <v-textarea
              v-model="comment"
              :label="commentRequired ? 'Comentario *' : 'Comentario'"
              variant="outlined"
              rows="3"
              auto-grow
              hide-details
            />
          </v-card-text>
        </v-card>
      </v-card-text>
      <v-card-actions class="mx-2">
        <v-btn
          color="error"
          variant="outlined"
          :disabled="loading"
          @click="dialog_visible = false"
        >
          {{ cancelLabel }}
        </v-btn>
        <v-spacer />
        <v-btn
          color="accent"
          variant="elevated"
          :append-icon="confirmIcon"
          :loading="loading"
          :disabled="commentRequired && !comment.trim()"
          class="px-6"
          @click="emits('confirm')"
        >
          {{ confirmLabel }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

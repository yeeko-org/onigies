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
    default: null,
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
});
const dialog_visible = defineModel({ type: Boolean, default: false });

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
          class="px-6"
          @click="emits('confirm')"
        >
          {{ confirmLabel }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

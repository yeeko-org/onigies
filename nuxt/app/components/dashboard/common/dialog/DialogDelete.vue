<script setup>

const emits = defineEmits(['confirm-delete'])
const props = defineProps({
  is_saved: Boolean,
  title: {
    type: String,
    default: '¿Confirmas la eliminación de este registro?',
  },
  subtitle: {
    type: String,
    default: 'Esta acción no se puede deshacer',
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
const dialog_visible = defineModel({ type: Boolean, default: false });
const delete_text = defineModel('delete_text', {type: String, default: '' });

</script>

<template>
  <v-dialog
    v-model="dialog_visible"
    max-width="500"
    :persistent="loading"
  >
    <v-card>
      <v-card-title>
        {{ title }}
      </v-card-title>
      <v-card-subtitle>
        {{ subtitle }}
      </v-card-subtitle>
      <v-card-text>
        <!-- Slot opcional: mensaje contextual sobre el registro a eliminar -->
        <slot />
        <v-row>
          <v-col
            v-if="is_saved"
            cols="12"
          >
            <v-text-field
              v-model="delete_text"
              label="Escribe 'eliminar' para confirmar"
              outlined
              dense
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="accent"
          variant="outlined"
          :disabled="loading"
          @click="dialog_visible = false"
        >
          Cancelar
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="elevated"
          :loading="loading"
          @click="emits('confirm-delete')"
        >
          Eliminar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>
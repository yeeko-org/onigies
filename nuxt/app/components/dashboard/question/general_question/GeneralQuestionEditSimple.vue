<script setup>
/**
 * Edición del texto de una pregunta base, dentro del Sheet de su grupo.
 *
 * Igual que en el grupo, reemplaza el marco genérico porque ese pinta
 * siempre el name_field: aquí `name` es la columna del Survey donde
 * aterriza la respuesta. `q_type` y `addl_config` tampoco se editan —
 * el componente de captura se elige a partir de ellos.
 */
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";

const Q_TYPE_NAMES = {
  integer: 'Número entero',
  boolean: 'Sí / No',
}

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict.general_question)

const has_addl_config = computed(
  () => Object.keys(full_main.value.addl_config || {}).length > 0)

function saveRecord() {
  errors.value = null
  saving.value = true
  saveElement(collection_data.value, full_main.value).then((res) => {
    saving.value = false
    if (res.errors) {
      errors.value = res.errors
      return
    }
    emits('item-saved', {res: res.data, is_new: false})
    showSnackbar('Se guardó el texto de la pregunta')
  })
}

</script>

<template>
  <v-card class="mb-3 pa-3" elevation="4">
    <v-alert
      v-if="errors"
      type="error"
      class="mb-3"
      style="white-space: pre-wrap;"
    >
      {{ errors }}
    </v-alert>
    <v-card-subtitle class="px-0 pb-3 d-flex flex-wrap ga-2 align-center">
      <span>Clave interna: <b>{{ full_main.name }}</b></span>
      <span>
        Tipo de respuesta:
        <b>{{ Q_TYPE_NAMES[full_main.q_type] || full_main.q_type }}</b>
      </span>
      <v-chip v-if="has_addl_config" size="small" variant="tonal">
        Configuración técnica — no editable
      </v-chip>
    </v-card-subtitle>
    <v-textarea
      v-model="full_main.text"
      label="Pregunta"
      variant="outlined"
      rows="2"
      auto-grow
      class="mb-2"
    />
    <v-textarea
      v-model="full_main.hint"
      label="Texto de ayuda"
      hint="Texto de apoyo que aparece bajo la pregunta; puede dejarse vacío"
      persistent-hint
      variant="outlined"
      rows="2"
      auto-grow
      class="mb-4"
    />
    <div class="d-flex flex-wrap ga-3">
      <v-text-field
        v-model="full_main.label"
        label="Rótulo del campo"
        hint="Si va vacío se usa la unidad"
        persistent-hint
        variant="outlined"
        style="min-width: 220px;"
      />
      <v-text-field
        v-model="full_main.unit"
        label="Unidad"
        variant="outlined"
        style="min-width: 180px;"
      />
      <v-text-field
        v-model="full_main.order"
        label="Orden"
        type="number"
        variant="outlined"
        style="max-width: 90px;"
      />
    </div>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="accent"
        variant="elevated"
        :loading="saving"
        @click="saveRecord"
      >
        Guardar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>

</style>

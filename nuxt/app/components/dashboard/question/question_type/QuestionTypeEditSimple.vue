<script setup>
// Reemplaza el marco genérico, que pintaría `name` como editable: es la
// PK que el código consulta; lo editable es `public_name`.

import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";

const WEIGHT_HINT = 'Ponderación que usa cada observable donde aplica ' +
  'este tipo, salvo que el observable declare la suya propia'

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict.question_type)

const required_hint = computed(() => full_main.value.required
  ? 'Se pregunta en todos los observables, no por excepción'
  : 'Aplica solo a los observables donde se sembró')

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
    showSnackbar('Se guardó el tipo de pregunta')
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
    <div class="d-flex flex-wrap ga-3">
      <v-text-field
        :model-value="full_main.name"
        label="Clave interna"
        readonly
        variant="outlined"
        style="max-width: 220px;"
      />
      <v-text-field
        :model-value="full_main.model_question"
        label="Modelo de pregunta"
        readonly
        variant="outlined"
        style="min-width: 200px; max-width: 260px;"
      />
      <v-text-field
        :model-value="full_main.model_response"
        label="Modelo de respuesta"
        readonly
        variant="outlined"
        style="min-width: 200px; max-width: 260px;"
      />
      <v-checkbox
        :model-value="full_main.required"
        label="Aplica a todo observable"
        readonly
        :hint="required_hint"
        persistent-hint
        style="flex: 0 1 320px;"
      />
    </div>
    <v-text-field
      v-model="full_main.public_name"
      label="Nombre público"
      hint="Como se nombra este bloque en todo el sistema"
      persistent-hint
      variant="outlined"
      class="mb-4"
    />
    <div class="d-flex flex-wrap ga-3">
      <v-text-field
        v-model="full_main.default_weight"
        label="Ponderación por defecto"
        type="number"
        :hint="WEIGHT_HINT"
        persistent-hint
        variant="outlined"
        style="min-width: 320px;"
      />
      <v-text-field
        v-model="full_main.order"
        label="Orden del bloque"
        type="number"
        variant="outlined"
        style="max-width: 120px;"
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

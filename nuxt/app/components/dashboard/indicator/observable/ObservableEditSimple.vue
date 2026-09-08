<script setup>
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";
import { useQuestionTypes } from "~/composables/useQuestionTypes.js";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { types_by_model } = useQuestionTypes()
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict.observable)

// Minúscula inicial porque va dentro del rótulo.
const a_block_name = computed(() => {
  const name = types_by_model.value.AQuestion?.public_name
  return name ? name.charAt(0).toLowerCase() + name.slice(1) : 'este bloque'
})

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
    showSnackbar('Se guardaron los textos del observable')
  })
}

</script>

<template>
  <v-card class="mb-3 pa-3" elevation="8">
    <v-alert
      v-if="errors"
      type="error"
      class="mb-3"
      style="white-space: pre-wrap;"
    >
      {{ errors }}
    </v-alert>
    <v-card-subtitle class="px-0 pb-3">
      Observable <b>{{ full_main.number }}</b>
      — orden {{ full_main.order }} en el cuestionario
    </v-card-subtitle>
    <v-text-field
      v-model="full_main.name"
      label="Nombre del observable"
      variant="outlined"
      class="mb-2"
    />
    <v-textarea
      v-model="full_main.description"
      label="Descripción"
      variant="outlined"
      rows="1"
      auto-grow
      class="mb-2"
    />
    <v-textarea
      v-model="full_main.init_question"
      label="Pregunta inicial (sí / no)"
      hint="La que abre el observable y decide si se captura lo demás"
      persistent-hint
      variant="outlined"
      rows="2"
      auto-grow
      class="mb-4"
    />
    <v-textarea
      v-model="full_main.a_main_question"
      :label="`Enunciado de ${a_block_name}`"
      hint="Encabeza el checklist de preguntas que va abajo"
      persistent-hint
      variant="outlined"
      rows="2"
      auto-grow
      class="mb-4"
    />
    <v-textarea
      v-model="full_main.a_main_subtitle"
      :label="`Subtítulo de ${a_block_name}`"
      variant="outlined"
      rows="1"
      auto-grow
      class="mb-4"
    />
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

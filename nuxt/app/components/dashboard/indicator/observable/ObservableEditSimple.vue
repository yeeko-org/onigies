<script setup>
/**
 * Edición de los textos de un observable del cuestionario.
 *
 * Reemplaza el marco genérico (EditCommon) porque ese pinta siempre el
 * «Orden», y aquí el orden es el recorrido global 1..41 que asigna
 * load_questionnaire. Tampoco aparecen las ponderaciones: son
 * metodología, no redacción. El número y el componente ubican la fila
 * en el instrumento y viajan como referencia, no como campo.
 *
 * Las preguntas de este observable no se editan aquí: las lista el
 * Sheet genérico debajo, una colección hija por familia.
 */
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict.observable)

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
      label="Enunciado de institucionalización"
      hint="Encabeza el checklist de opciones que va abajo"
      persistent-hint
      variant="outlined"
      rows="2"
      auto-grow
      class="mb-4"
    />
    <v-textarea
      v-model="full_main.a_main_subtitle"
      label="Subtítulo de institucionalización"
      variant="outlined"
      rows="1"
      auto-grow
      class="mb-4"
    />
    <v-textarea
      v-model="full_main.reach_instances_question"
      label="Pregunta de instancias (alcance)"
      variant="outlined"
      rows="2"
      auto-grow
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

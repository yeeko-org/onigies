<script setup>
/**
 * Editor de texto compartido por las cinco familias de preguntas por
 * observable. No se carga por convención: lo envuelve un
 * `{Model}EditSimple.vue` por cada tipo, que es lo que la convención de
 * nombre sí resuelve.
 *
 * Reemplaza el marco genérico (EditCommon) porque ninguno de estos
 * modelos tiene `name_field`: el marco pintaría un «Nombre/Título»
 * vacío y un «Orden» que la API no acepta —en A, B y planes el orden
 * es, con el observable, la clave natural del seed—.
 */
import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";

const props = defineProps({
  collection_snake: {
    type: String,
    required: true,
  },
  // Etiqueta del textarea: cada tipo de pregunta se lee distinto.
  text_label: {
    type: String,
    default: 'Texto de la pregunta',
  },
  // Datos estructurales que se muestran para ubicar la fila, nunca
  // para editarla.
  chips: {
    type: Array,
    default: () => [],
  },
})

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict[props.collection_snake])

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
    <v-card-subtitle
      v-if="chips.length"
      class="px-0 pb-3 d-flex flex-wrap ga-2 align-center"
    >
      <v-chip
        v-for="chip in chips"
        :key="chip"
        size="small"
        variant="tonal"
      >
        {{ chip }}
      </v-chip>
    </v-card-subtitle>
    <v-textarea
      v-model="full_main.text"
      :label="text_label"
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

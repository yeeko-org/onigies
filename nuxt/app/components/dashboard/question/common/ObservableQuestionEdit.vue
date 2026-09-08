<script setup>
// Compartido por las cinco familias: lo envuelve un `{Model}EditSimple`
// porque la convención de nombre no resuelve un componente común.
// Reemplaza a EditCommon, que sin `name_field` pintaría un título vacío
// y un «Orden» que la API rechaza (es clave natural del seed).

import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";
import { useQuestionTypes } from "~/composables/useQuestionTypes.js";

const props = defineProps({
  collection_snake: {
    type: String,
    required: true,
  },
  chips: {
    type: Array,
    default: () => [],
  },
})

const full_main = defineModel({type: Object, required: true})

const emits = defineEmits(['item-saved'])

const { schemas } = storeToRefs(useMainStore())
const { types_by_model } = useQuestionTypes()
const { showSnackbar } = useDashboardStore()

const saving = ref(false)
const errors = ref(null)

const collection_data = computed(
  () => schemas.value.collections_dict[props.collection_snake])

const text_label = computed(() =>
  types_by_model.value[collection_data.value?.model_name]?.public_name
  || 'Texto de la pregunta')

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

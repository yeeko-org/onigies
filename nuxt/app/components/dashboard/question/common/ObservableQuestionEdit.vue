<script setup>
// Compartido por las cinco familias: lo envuelve un `{Model}EditSimple`
// porque la convención de nombre no resuelve un componente común.
// Reemplaza a EditCommon, que sin `name_field` pintaría un título vacío
// y un «Orden» que la API rechaza (es clave natural del seed).

import { storeToRefs } from "pinia";
// Importado a mano: como raíz dinámica, la cadena "v-card" no resuelve
// contra el registro global que arma vite-plugin-vuetify.
import { VCard } from "vuetify/components";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";
import { useQuestionTypes } from "~/composables/useQuestionTypes.js";

const SAVE_TOOLTIP = 'Ctrl / Cmd + Enter dentro del texto guarda esta pregunta'
const DEFAULT_MESSAGE = 'Se guardó el texto de la pregunta'

const props = defineProps({
  collection_snake: {
    type: String,
    required: true,
  },
  // Dentro de un bloque la cabecera ya dice el tipo; en la colección
  // suelta el nombre público es lo único que sitúa la pregunta.
  text_label: {
    type: String,
    default: null,
  },
  // Numeración tipográfica de lista, no un campo. Las familias de una
  // sola pregunta por observable no la reciben.
  position: {
    type: [Number, String],
    default: null,
  },
  success_message: {
    type: String,
    default: DEFAULT_MESSAGE,
  },
  // Renglón dentro de un bloque del editor de observable: sin tarjeta
  // propia y con acciones discretas, para que la jerarquía de botones
  // se lea por tamaño y variante.
  in_block: Boolean,
  // Las familias de una sola pregunta con controles anchos ponen las
  // acciones bajo el grupo, no a su derecha.
  actions_below: Boolean,
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

const final_text_label = computed(() => props.text_label
  || types_by_model.value[collection_data.value?.model_name]?.public_name
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
    showSnackbar(props.success_message)
  })
}

</script>

<template>
  <component
    :is="in_block ? 'div' : VCard"
    :class="in_block ? 'py-2' : 'mb-3 pa-3'"
    :variant="in_block ? undefined : 'outlined'"
  >
    <v-alert
      v-if="errors"
      type="error"
      class="mb-3"
      style="white-space: pre-wrap;"
    >
      {{ errors }}
    </v-alert>
    <div class="d-flex ga-3">
      <div
        v-if="position"
        class="text-h6 text-medium-emphasis mt-2"
      >
        {{ position }}.
      </div>
      <div class="flex-grow-1">
        <slot name="before" />
        <v-textarea
          v-model="full_main.text"
          :label="final_text_label"
          variant="outlined"
          density="comfortable"
          rows="2"
          auto-grow
          class="reading-width"
          @keydown.ctrl.enter.prevent="saveRecord"
          @keydown.meta.enter.prevent="saveRecord"
        />
        <slot name="after" />
      </div>
      <div
        v-if="!actions_below"
        class="d-flex flex-column align-center ga-1 pt-1"
      >
        <v-btn
          color="accent"
          :variant="in_block ? 'tonal' : 'elevated'"
          :size="in_block ? 'small' : undefined"
          :loading="saving"
          @click="saveRecord"
        >
          Guardar
          <v-tooltip activator="parent" location="top">
            {{ SAVE_TOOLTIP }}
          </v-tooltip>
        </v-btn>
        <slot name="actions" />
      </div>
    </div>
    <div
      v-if="actions_below"
      class="d-flex align-center"
    >
      <slot name="actions" />
      <v-spacer></v-spacer>
      <v-btn
        color="accent"
        :variant="in_block ? 'tonal' : 'elevated'"
        :size="in_block ? 'small' : undefined"
        :loading="saving"
        @click="saveRecord"
      >
        Guardar
        <v-tooltip activator="parent" location="top">
          {{ SAVE_TOOLTIP }}
        </v-tooltip>
      </v-btn>
    </div>
  </component>
</template>

<style scoped>
/* Tope de ancho de lectura para el cotejo de textos; el panel del
   dashboard es mucho más ancho. */
.reading-width {
  max-width: 90ch;
}
</style>

<script setup>
/**
 * Edición de textos de un grupo de la sección «Información de base».
 *
 * Reemplaza el marco genérico (EditCommon) en vez de aportarle campos:
 * ese marco pinta siempre el name_field, y aquí `name` es la PK y la
 * clave que engancha cada respuesta con su columna del Survey. Se
 * muestra, no se edita; tampoco hay borrar, los grupos los siembra
 * load_questionnaire.
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
  () => schemas.value.collections_dict.general_group)

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
    showSnackbar('Se guardaron los textos del grupo')
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
      Clave interna: <b>{{ full_main.name }}</b>
      — orden {{ full_main.order }}
    </v-card-subtitle>
    <v-text-field
      v-model="full_main.public_name"
      label="Nombre público"
      variant="outlined"
      class="mb-2"
    />
    <v-text-field
      v-model="full_main.title"
      label="Título del bloque"
      variant="outlined"
      class="mb-2"
    />
    <v-text-field
      v-model="full_main.subtitle"
      label="Subtítulo"
      variant="outlined"
      class="mb-2"
    />
    <v-textarea
      v-model="full_main.instruction"
      label="Instrucción para la IES"
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

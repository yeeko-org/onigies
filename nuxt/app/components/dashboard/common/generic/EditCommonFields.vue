<script setup>

import Comments from "~/components/dashboard/common/utils/Comments.vue";

const props = defineProps({
  final_collection_data: Object,
})
const full_main = defineModel({type: Object, required: true})

const rules = ref({
  required: value => !!value || "Campo requerido",
  defined: value => value !== undefined || "Debes seleccionar una opción",
})

function openLink(type) {
  if (type === 'icon')
    window.open('https://fonts.google.com/icons', '_blank')
    // window.open('https://material.io/resources/icons/?style=baseline', '_blank')
  else if (type === 'color')
    window.open('https://vuetifyjs.com/en/styles/colors/#material-colors', '_blank')
}

const emits = defineEmits(['update-status', 'update-comments'])

</script>

<template>
  <v-card-text
    class="d-flex flex-wrap"
  >
    <v-col cols="12" class="d-flex pa-0">
      <v-text-field
        v-if="final_collection_data.has.order"
        v-model="full_main.order"
        label="Orden"
        type="number"
        variant="outlined"
        class="mr-2"
        style="max-width: 70px;"
      >
      </v-text-field>
      <v-text-field
        v-if="final_collection_data.name_field"
        v-model="full_main[final_collection_data.name_field]"
        label="Nombre/Título"
        class="mr-2"
        variant="outlined"
        style="width: 300px;"
        :rules="[rules.required]"
      />
      <v-spacer></v-spacer>
      <Comments
        v-if="final_collection_data.has.comments"
        :main="full_main"
        :final_collection_data="final_collection_data"
        @update-comments="emits('update-comments', $event)"
      />
    </v-col>
    <v-col
      v-if="final_collection_data.has.icon || final_collection_data.has.color"
      cols="12"
      class="d-flex pa-0"
    >
      <v-text-field
        v-if="final_collection_data.has.icon"
        v-model="full_main.icon"
        label="Ícono (material icons)"
        variant="outlined"
        style="max-width: 260px;"
        :rules="[rules.required]"
      >
        <template v-slot:append>
          <v-icon
            @click="openLink('icon')"
          >open_in_new</v-icon>
        </template>
      </v-text-field>
      <v-text-field
        v-if="final_collection_data.has.color"
        v-model="full_main.color"
        label="Color"
        variant="outlined"
        class="ml-6"
        style="max-width: 220px;"
        :rules="[rules.required]"
      >
        <template v-slot:append>
          <v-icon
            @click="openLink('color')"
          >open_in_new</v-icon>
        </template>
      </v-text-field>
    </v-col>
    <slot name="edit">
      EDICIÓN 2 (REVISAR PORQUE NO ES NORMAL)
    </slot>
    <v-col
      v-if="final_collection_data.has.description
        && final_collection_data.name_field !== 'description'"
      cols="12"
      class="d-flex pa-0"
    >
      <v-textarea
        v-model="full_main.description"
        label="Descripción"
        rows="1"
        auto-grow
        class="mr-2"
        variant="outlined"
      ></v-textarea>
    </v-col>
    <v-col
      cols="12"
      class="d-flex pa-0"
    >
      <v-textarea
        v-if="final_collection_data.has.help_text"
        v-model="full_main.help_text"
        label="Texto visible de ayuda"
        variant="outlined"
        rows="2"
        auto-grow
        hint="Aparecerá una 'alerta' cuando se seleccione esta categoría"
        persistent-hint
        _hide-details
      >
      </v-textarea>
    </v-col>
  </v-card-text>
</template>

<style scoped>

</style>
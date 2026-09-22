<script setup>

const props = defineProps({
  is_massive_edit: Boolean,
  is_edit: Boolean,
})

import {useDashboardStore} from "~/store/dash.js";

const full_main = defineModel({type: Object, required: true})
const { showSnackbar } = useDashboardStore()

const slug_hint = 'Se genera del título si lo dejas vacío. ' +
  'Cambiarlo rompe los enlaces ya compartidos.'
const generated_slug_hint = 'Fijo: el sitio público enlaza a este ' +
  'documento por su identificador.'

const new_file = ref(null)

// Según la versión, v-file-input entrega un File o un arreglo de uno.
watch(new_file, (val) => {
  const file = Array.isArray(val) ? val[0] : val
  if (file)
    full_main.value.file = file
})

function copyUrl() {
  navigator.clipboard.writeText(full_main.value.download_url)
  showSnackbar('Enlace copiado')
}
</script>

<template>
  <v-col cols="12" class="pa-0">
    <v-text-field
      v-model="full_main.slug"
      label="Identificador en la URL"
      variant="outlined"
      :readonly="!!full_main.generator"
      :hint="full_main.generator ? generated_slug_hint : slug_hint"
      persistent-hint
      class="mb-3"
      style="max-width: 420px;"
    />
    <v-text-field
      v-if="full_main.generator"
      model-value="Se genera desde la base al descargarlo"
      label="Contenido"
      variant="outlined"
      readonly
    />
    <template v-else>
      <v-file-input
        v-model="new_file"
        :label="full_main.file_name
          ? `Reemplazar archivo (actual: ${full_main.file_name})`
          : 'Archivo'"
        variant="outlined"
        prepend-icon=""
        prepend-inner-icon="attach_file"
      />
    </template>
    <v-switch
      v-model="full_main.is_published"
      label="Publicado: cualquiera puede descargarlo, sin iniciar sesión"
      color="accent"
    />
    <v-text-field
      v-if="full_main.is_published && full_main.download_url"
      :model-value="full_main.download_url"
      label="Enlace público de descarga"
      variant="outlined"
      readonly
    >
      <template #append-inner>
        <v-icon class="mr-2" @click="copyUrl">content_copy</v-icon>
        <a :href="full_main.download_url" target="_blank">
          <v-icon>open_in_new</v-icon>
        </a>
      </template>
    </v-text-field>
  </v-col>
</template>

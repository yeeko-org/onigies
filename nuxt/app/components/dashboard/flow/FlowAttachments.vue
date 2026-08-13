<script setup>
/**
 * Adjuntos de un objeto del flujo (`flow.Attachment`), genérico para
 * cualquier target: lista, sube y borra contra
 * `/flow/{app}/{model}/{id}/attachments/`.
 *
 * El adjunto se ancla AL OBJETO, no al evento del timeline, así que el
 * historial no cambia al subir o borrar un archivo.
 *
 * `v-model` es el array `flow_attachments` que ya viaja embebido en el
 * serializer de detalle del target: no se pide por separado, y las
 * mutaciones se hacen en sitio (mismo criterio que FlowComments con
 * `flow_events`). `editable` decide quién escribe — la IES en su turno;
 * la revisión siempre lee.
 */
import { useApiError } from '~/composables/useApiError.js'
import { useDashboardStore } from '~/store/dash.js'

const props = defineProps({
  appLabel: { type: String, required: true },
  modelName: { type: String, required: true },
  id: { type: [Number, String], required: true },
  // Solo el turno de la IES habilita subir y borrar.
  editable: { type: Boolean, default: false },
  label: { type: String, default: 'Agregar archivo' },
})

const attachments = defineModel({ type: Array, default: () => [] })

const { $api } = useNuxtApp()
const { notifyApiError } = useApiError()
const dashStore = useDashboardStore()

const saving = ref(false)
const confirmTarget = ref(null)
const inputRef = ref(null)

const base = computed(
  () => `/flow/${props.appLabel}/${props.modelName}/${props.id}/attachments/`)

function pickFile() {
  inputRef.value?.click()
}

async function onFileChosen(event) {
  const file = (event.target.files || [])[0]
  // Se limpia el input para poder volver a elegir el mismo archivo.
  event.target.value = ''
  if (!file) return
  saving.value = true
  try {
    const formData = new FormData()
    formData.append('file', file, file.name)
    const res = await $api.post(base.value, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    attachments.value = [res.data, ...attachments.value]
    dashStore.showSnackbar('Archivo adjunto')
  } catch (e) {
    notifyApiError(e, 'No se pudo subir el archivo.')
  } finally {
    saving.value = false
  }
}

async function openFile(item) {
  // La pestaña se abre ANTES del await para que el navegador la ligue al
  // clic y no la bloquee como popup.
  const win = window.open('', '_blank')
  if (win) win.opener = null
  try {
    const res = await $api.get(`${base.value}${item.id}/download/`, {
      params: { redirect: false },
    })
    if (win) win.location = res.data.url
    else window.location.href = res.data.url
  } catch (e) {
    win?.close()
    notifyApiError(e, 'No se pudo abrir el archivo.')
  }
}

async function removeFile() {
  const item = confirmTarget.value
  if (!item) return
  saving.value = true
  try {
    await $api.delete(`${base.value}${item.id}/`)
    attachments.value = attachments.value.filter((a) => a.id !== item.id)
    dashStore.showSnackbar('Archivo eliminado')
    confirmTarget.value = null
  } catch (e) {
    notifyApiError(e, 'No se pudo eliminar el archivo.')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="d-flex flex-wrap align-center ga-1">
    <v-chip
      v-for="item in attachments"
      :key="item.id"
      class="my-1"
      color="accent"
      variant="tonal"
      prepend-icon="description"
      link
      @click="openFile(item)"
    >
      {{ item.name }}
      <template v-if="editable" #append>
        <v-icon
          size="small"
          color="error"
          class="ml-2"
          @click.stop.prevent="confirmTarget = item"
        >
          delete
        </v-icon>
      </template>
    </v-chip>

    <span
      v-if="!attachments.length && !editable"
      class="text-caption text-grey-darken-1"
    >
      Sin archivos adjuntos
    </span>

    <template v-if="editable">
      <input
        ref="inputRef"
        type="file"
        style="display: none"
        @change="onFileChosen"
      >
      <v-btn
        variant="outlined"
        color="accent"
        size="small"
        class="ml-2"
        append-icon="attach_file"
        :loading="saving"
        @click="pickFile"
      >
        {{ label }}
      </v-btn>
    </template>

    <v-dialog :model-value="!!confirmTarget" max-width="380" persistent>
      <v-card>
        <v-card-title class="text-h6">
          ¿Eliminar el archivo?
        </v-card-title>
        <v-card-text>
          Una vez eliminado no lo podrás recuperar:
          <b>{{ confirmTarget?.name }}</b>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="confirmTarget = null">
            No eliminar
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            :loading="saving"
            @click="removeFile"
          >
            Sí eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

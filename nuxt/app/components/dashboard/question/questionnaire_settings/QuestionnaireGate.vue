<script setup>
// Cromo de la vista del cuestionario, no un {Model}{Suffix}: se importa a
// mano porque la convención de auto-carga no lo resuelve.

import { storeToRefs } from "pinia";
import { useMainStore } from "~/store/index.js";
import { useDashboardStore } from "~/store/dash.js";
import { saveElement } from "~/composables/save_elements.js";
import ConfirmActionDialog from
  "~/components/dashboard/common/dialog/ConfirmActionDialog.vue";
import { docxUrl } from "~/utils/public_documents.js";

const OPEN_LABEL = 'Cuestionario abierto a edición'
const CLOSED_LABEL = 'Cuestionario cerrado a edición'
const OPEN_CAPTION = 'Se pueden agregar y eliminar preguntas y tipos.'
const CLOSED_CAPTION = 'Solo se corrigen textos y ponderaciones.'
const CONFIRM_TITLE = '¿Cerrar el cuestionario a edición?'
const CONFIRM_BODY = 'Una vez cerrado solo se pueden corregir textos y '
  + 'ponderaciones: no se agregan ni se eliminan preguntas ni tipos. '
  + 'Reabrirlo ya no se hace desde el dashboard, lo hace el equipo técnico '
  + 'desde el admin de Django.'
const CLOSE_ERROR = 'No se pudo cerrar el cuestionario.'

const { cats, schemas } = storeToRefs(useMainStore())
const { showSnackbar } = useDashboardStore()
const config = useRuntimeConfig()

const dialog = ref(false)
const saving = ref(false)

const settings = computed(() => cats.value?.questionnaire_settings?.[0])

const docx_url = docxUrl(config.public.apiUrl)

const is_open = computed(() => settings.value?.content_open ?? true)

// Dice cuándo pasó `load_questionnaire` por encima por última vez: es el
// dato que se consulta antes de tocar el instrumento.
const seeded_label = computed(() => {
  if (!settings.value?.seeded_at)
    return null
  const formatter = new Intl.DateTimeFormat('es-MX', {dateStyle: 'long'})
  return formatter.format(new Date(settings.value.seeded_at))
})

async function closeQuestionnaire() {
  saving.value = true
  const collection = schemas.value.collections_dict.questionnaire_settings
  const res = await saveElement(
    collection, {...settings.value, content_open: false}, CLOSE_ERROR)
  saving.value = false
  if (res.errors)
    return
  dialog.value = false
  showSnackbar(CLOSED_LABEL)
}

</script>

<template>
  <v-card
    v-if="settings"
    variant="outlined"
    class="pa-3 mb-3 text-body-2"
  >
    <div class="d-flex flex-wrap align-center ga-3">
      <v-icon :color="is_open ? 'accent' : 'grey-darken-1'">
        {{ is_open ? 'lock_open' : 'lock' }}
      </v-icon>
      <!-- Cerrar es de ida: con el cuestionario cerrado la barra queda
           como texto, sin control que insinúe que se puede reabrir. -->
      <v-switch
        v-if="is_open"
        :model-value="true"
        :label="OPEN_LABEL"
        color="accent"
        density="compact"
        hide-details
        class="flex-grow-0"
        @update:model-value="dialog = true"
      />
      <div v-else class="font-weight-bold">
        {{ CLOSED_LABEL }}
      </div>
      <v-spacer></v-spacer>
      <div v-if="seeded_label" class="text-caption text-medium-emphasis">
        Última siembra: {{ seeded_label }}
      </div>
      <v-btn
        color="accent"
        variant="tonal"
        prepend-icon="download"
        :href="docx_url"
      >
        Descargar Word
      </v-btn>
    </div>
    <div class="text-caption text-medium-emphasis">
      {{ is_open ? OPEN_CAPTION : CLOSED_CAPTION }}
    </div>

    <ConfirmActionDialog
      v-model="dialog"
      :title="CONFIRM_TITLE"
      confirm-label="Cerrar"
      confirm-icon="lock"
      :loading="saving"
      @confirm="closeQuestionnaire"
    >
      {{ CONFIRM_BODY }}
    </ConfirmActionDialog>
  </v-card>
</template>

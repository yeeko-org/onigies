<script setup>
import FeatureList from "~/components/dashboard/example/good_practice/FeatureList.vue";
import StatusDetail from "~/components/dashboard/status/StatusDetail.vue";
import StatusToggle from "~/components/dashboard/status/StatusToggle.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import {
  isPracticeComplete, getMissingFields
} from "~/composables/good_practice_validation.js"
import Evidences from "~/components/dashboard/common/utils/Evidences.vue";
import { useRules } from "~/composables/useRules.js"
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const { rules } = useRules()

const props = defineProps({
  isStaff: { type: Boolean, default: true },
  sentAt: String,
  editionAvailable: {
    type: Boolean,
    default: true
  }
})

const full_main = defineModel({type: Object, required: true})

const emit = defineEmits(['close', 'saved', 'deleted'])

const confirmDelete = ref(false)
const loading = ref(false)
const showBlockedAlert = ref(false)
const blockedItems = ref([])
const formRef = ref(null)

const isEditing = computed(() => !!full_main.value?.id)

const canToggleStatus = computed(() => {
  if (props.isStaff) return false
  if (props.sentAt) return false
  const code = full_main.value?.status_sending
  return !code || code === 'draft' || code === 'ready_to_send'
})

function canMarkReady() {
  return isPracticeComplete(full_main.value)
}

function missingForReady() {
  return getMissingFields(full_main.value)
}

function onStatusChange(newCode) {
  full_main.value.status_sending = newCode
  showBlockedAlert.value = false
}

function onStatusBlocked(items) {
  blockedItems.value = items
  showBlockedAlert.value = true
}

const showReadyPrompt = ref(false)
const pendingPractice = ref(null)

const savePractice = async () => {
  if (!props.isStaff) {
    const { valid } = await formRef.value.validate()
    if (!valid) return
  }
  loading.value = true
  try {
    const res = await mainStore.saveSimple(
      ['good_practice', full_main.value])
    if (res?.errors) {
      dashStore.showSnackbar(
        res.errors.detail || 'No se pudo guardar la buena práctica', 'error')
      return
    }
    if (isPracticeComplete(res) && res.status_sending === 'draft') {
      pendingPractice.value = res
      showReadyPrompt.value = true
      return
    }
    dashStore.showSnackbar('Se guardó la buena práctica')
    emit('saved', res)
  } catch (e) {
    console.error('Error al guardar:', e)
  } finally {
    loading.value = false
  }
}

function keepAsDraft() {
  const res = pendingPractice.value
  showReadyPrompt.value = false
  pendingPractice.value = null
  dashStore.showSnackbar('Se guardó la buena práctica')
  emit('saved', res)
}

async function markAsReady() {
  const base = pendingPractice.value
  loading.value = true
  try {
    const res = await mainStore.patchSimple([
      'good_practice', base.id, {status_sending: 'ready_to_send' }])
    if (res?.errors) {
      dashStore.showSnackbar(
        res.errors.detail || 'No se pudo cambiar el status', 'error')
      showReadyPrompt.value = false
      emit('saved', base)
      return
    }
    showReadyPrompt.value = false
    pendingPractice.value = null
    dashStore.showSnackbar(
      'Buena práctica marcada como "Lista para enviar"'
    )
    emit('saved', res)
  } finally {
    loading.value = false
  }
}

const remove = async () => {
  try {
    await mainStore.deleteSimple(['good_practice', full_main.value.id])
    emit('deleted')
  } catch (e) {
    console.error('Error al eliminar:', e)
  }
}

</script>

<template>
  <v-card>
    <slot name="header">
    </slot>
    <v-card-text
      class="pa-4"
    >
      <v-form ref="formRef" validate-on="input">
        <div class="d-flex align-center">
          <v-text-field
            v-model="full_main.name"
            :rules="[rules.required]"
            label="Nombre de la buena práctica *"
            :variant="isStaff ? 'solo' : 'outlined'"
            class="mr-6"
            :readonly="isStaff"
          />
          <StatusToggle
            v-if="canToggleStatus"
            :main="full_main"
            collection="sending"
            from-code="draft"
            to-code="ready_to_send"
            :can-transition="canMarkReady"
            :missing-items="missingForReady"
            @change="onStatusChange"
            @blocked="onStatusBlocked"
          />
          <StatusDetail
            v-else-if="full_main.status_sending
              && full_main.status_sending !== 'draft'
              && full_main.status_sending !== 'ready_to_send'"
            v-model="full_main"
            collection="sending"
          />
        </div>
        <v-alert
          v-if="showBlockedAlert"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-3 mt-2"
          closable
        >
          <div class="text-subtitle-1 mb-1">
            Para poder marcar esta buena práctica como
            <b>"Lista para enviar"</b>, aún falta agregar:
          </div>
          <ul class="ml-4 mb-2 text-body-2">
            <li v-for="item in blockedItems" :key="item">
              {{ item }}
            </li>
          </ul>
<!--          <div class="d-flex justify-center">-->
<!--            <v-btn-->
<!--              variant="outlined"-->
<!--              color="accent"-->
<!--              size="small"-->
<!--              @click="showBlockedAlert = false"-->
<!--            >-->
<!--              Entendido-->
<!--            </v-btn>-->
<!--          </div>-->
        </v-alert>
        <div class="d-flex align-center">

          <SelectGroup
            v-model="full_main"
            filter_group_name="axes"
            main_collection_name="good_practice"
            forced_level="subtype"
            :required="true"
            :width="380"
          />
          <div v-if="!isStaff" class="ml-4">
            <div class="text-subtitle-1">
              Periodo de vigencia
            </div>
            <div class="d-flex">
              <v-text-field
                type="number"
                label="Año de inicio"
                variant="outlined"
                v-model="full_main.start_year"
                :readonly="isStaff"
                class="mr-4"
                width="160"
                density="compact"
              />
              <v-text-field
                type="number"
                label="Año de fin"
                variant="outlined"
                v-model="full_main.end_year"
                :readonly="isStaff"
                width="160"
                density="compact"
              />
            </div>
          </div>
          <div v-else class="mb-4 ml-4 text-subtitle-1">
            <b>Vigencia:</b> Del {{ full_main.start_year || '----'}}
            al {{ full_main.end_year || '----'}}
          </div>
        </div>

        <v-textarea
          v-model="full_main.description"
          label="Descripción"
          :variant="isStaff ? 'solo' : 'outlined'"
          rows="3"
          :readonly="isStaff"
          :counter="5000"
        />

        <v-textarea
          v-model="full_main.results"
          label="Resultados obtenidos"
          :variant="isStaff ? 'solo' : 'outlined'"
          rows="3"
          :readonly="isStaff"
          :counter="5000"
        />
      </v-form>
      Evidencias:
      <Evidences
        :full_main="full_main"
        main_collection_name="good_practice"
      />
      <v-divider class="mt-4"></v-divider>
      <FeatureList
        v-if="isEditing"
        :good-practice-id="full_main.id"
        v-model:feature-values="full_main.feature_values"
        :is-staff="isStaff"
        class="mt-4 mb-4"
      />
    </v-card-text>


    <v-card-actions class="mb-3 mx-3">
      <v-btn
        v-if="isEditing && !isStaff"
        color="error"
        variant="text"
        @click="confirmDelete = true"
      >
        <v-icon start>delete</v-icon>
        Eliminar
      </v-btn>
      <v-spacer />
      <v-btn
        v-if="!isStaff"
        variant="text"
        @click="emit('close')"
      >
        Cerrar
      </v-btn>
      <v-btn
        v-if="editionAvailable"
        color="accent"
        variant="flat"
        :loading="loading"
        prepend-icon="save"
        @click="savePractice"
      >
        Guardar
      </v-btn>
    </v-card-actions>

    <!-- Diálogo de confirmación de eliminación -->
    <v-dialog v-model="confirmDelete" max-width="400">
      <v-card>
        <v-card-title>¿Eliminar buena práctica?</v-card-title>
        <v-card-text>
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="confirmDelete = false">Cancelar</v-btn>
          <v-btn color="error" @click="remove">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Prompt tras guardar: ¿marcar como Lista para enviar? -->
    <v-dialog v-model="showReadyPrompt" max-width="520" persistent>
      <v-card>
        <v-card-title class="text-h6">
          Buena práctica completa
        </v-card-title>
        <v-card-text>
          Esta buena práctica ya cumple con los elementos
          mínimos necesarios para enviarse a revisión.
          ¿Quieres marcarla como
          <b>"Lista para enviar"</b>
          o dejarla en borrador para seguirla editando?
        </v-card-text>
        <v-card-actions class="mx-3 mb-2">
          <v-btn
            variant="outlined"
            @click="keepAsDraft"
          >
            Dejar en borrador
          </v-btn>
          <v-spacer />
          <v-btn
            color="success"
            variant="elevated"
            :loading="loading"
            prepend-icon="done_outline"
            @click="markAsReady"
          >
            Lista para enviar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>
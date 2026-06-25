<script setup>
import FeatureList from "~/components/dashboard/example/good_practice/FeatureList.vue";
import GoodPracticeChecklist from "~/components/dashboard/example/good_practice/GoodPracticeChecklist.vue";
import GoodPracticeIntro from "~/components/dashboard/example/good_practice/GoodPracticeIntro.vue";
import FlowStatusChip from "~/components/dashboard/flow/FlowStatusChip.vue";
import FlowTransitionMenu from "~/components/dashboard/flow/FlowTransitionMenu.vue";
import FlowTransitionDialogs from "~/components/dashboard/flow/FlowTransitionDialogs.vue";
import FlowComments from "~/components/dashboard/flow/FlowComments.vue";
import { useFlowActions } from "~/composables/useFlowActions.js"
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import Evidences from "~/components/dashboard/common/utils/Evidences.vue";
import { useRules } from "~/composables/useRules.js"
import { yearRules } from "~/composables/good_practice_validation.js"
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const { rules } = useRules()

const props = defineProps({
  isStaff: { type: Boolean, default: true },
  editable: {
    type: Boolean,
    default: true
  }
})

const full_main = defineModel({type: Object, required: true})

const emit = defineEmits(['close', 'saved', 'deleted'])

const confirmDelete = ref(false)
const loading = ref(false)
const formRef = ref(null)
const showErrorSummary = ref(false)

const isEditing = computed(() => !!full_main.value?.id)

const flowActions = useFlowActions(full_main, 'example', 'goodpractice')
const { transitions, currentStatus } = flowActions

// Lleva el foco visual al primer campo en rojo tras un guardado inválido.
const scrollToFirstError = () => {
  const el = formRef.value?.$el?.querySelector('.v-input--error')
  el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

// Persiste el contenido. Devuelve true si guardó, SIN cerrar el diálogo, para
// que el split-button pueda guardar y luego transicionar sin cerrar antes.
const persist = async () => {
  if (!props.isStaff) {
    const { valid } = await formRef.value.validate()
    if (!valid) {
      showErrorSummary.value = true
      await nextTick()
      scrollToFirstError()
      return false
    }
    showErrorSummary.value = false
  }
  loading.value = true
  const msg_error = 'No se pudo guardar la buena práctica'
  try {
    const res = await mainStore.saveSimple(
      ['good_practice', full_main.value], msg_error)
    if (res.errors) return false
    dashStore.showSnackbar('Se guardó la buena práctica')
    emit('saved', res.data)
    return true
  } catch (e) {
    devWarn('Error al guardar:', e)
    return false
  } finally {
    loading.value = false
  }
}

const savePractice = async () => {
  if (await persist()) emit('close')
}

// Guarda contenido y, si guardó, dispara la transición elegida en el caret.
// Cierra solo si la transición se ejecutó (onSelect devuelve el evento; null
// si abrió el diálogo de bloqueo o de comentario).
const saveAndTransition = async (t) => {
  if (!(await persist())) return
  const ev = await flowActions.onSelect(t)
  if (ev) emit('close')
}

const remove = async () => {
  try {
    const res = await mainStore.deleteSimple(
      ['good_practice', full_main.value.id])
    if (res.errors) {
      dashStore.showSnackbar('No se pudo eliminar la buena práctica')
      return
    }
    emit('deleted')
  } catch (e) {
    devWarn('Error al eliminar:', e)
  }
}

</script>

<template>
  <v-card>
    <slot name="header">
    </slot>
    <div
      v-if="isEditing"
      class="d-flex align-start justify-space-between px-4 pt-3"
    >
      <FlowStatusChip :status="full_main.status" />
      <FlowComments
        v-model="full_main"
        app-label="example"
        model-name="goodpractice"
      />
    </div>
    <v-card-text
      class="pa-4"
    >
      <div class="d-flex justify-end mb-2">
        <GoodPracticeIntro>
          <template #activator="{ props: activatorProps }">
            <v-btn
              v-bind="activatorProps"
              size="small"
              variant="text"
              color="primary"
              prepend-icon="help_outline"
            >
              ¿Qué es una buena práctica?
            </v-btn>
          </template>
        </GoodPracticeIntro>
      </div>
      <v-form ref="formRef" validate-on="input">
        <v-text-field
          v-model="full_main.name"
          :rules="[rules.required]"
          label="Nombre de la buena práctica *"
          :variant="isStaff ? 'solo' : 'outlined'"
          :readonly="isStaff"
        />
        <div class="d-flex align-center">

          <SelectGroup
            v-model="full_main"
            filter_group_name="axes"
            main_collection_name="good_practice"
            forced_level="type"
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
                :rules="yearRules(full_main, 'start')"
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
                :rules="yearRules(full_main, 'end')"
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
        :editable="editable"
        class="mt-4 mb-4"
      />
      <GoodPracticeChecklist
        v-if="!isStaff && editable"
        :practice="full_main"
        class="mt-4"
      />
    </v-card-text>

    <v-expand-transition>
      <v-alert
        v-if="showErrorSummary && !isStaff"
        type="error"
        variant="tonal"
        density="compact"
        class="mx-4 mb-2"
      >
        Hay campos con errores: revisa los marcados en rojo.
      </v-alert>
    </v-expand-transition>

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
      <!-- Sin transiciones (status terminal o no es turno): el botón guarda y
           cierra directo, sin desplegar opciones. -->
      <v-btn
        v-if="editable && !transitions.length"
        color="accent"
        variant="flat"
        density="comfortable"
        :loading="loading"
        prepend-icon="save"
        @click="savePractice"
      >
        Guardar
      </v-btn>
      <!-- Con transiciones: el botón despliega un menú hacia abajo encabezado
           por "Guardar y mantener como {status}" (guarda sin transicionar),
           seguido de cada transición (guarda y luego transiciona). -->
      <v-menu
        v-else-if="editable"
        location="bottom end"
      >
        <template #activator="{ props: menuProps }">
          <v-btn
            v-bind="menuProps"
            color="accent"
            variant="flat"
            density="comfortable"
            :loading="loading"
            prepend-icon="save"
            append-icon="expand_more"
          >
            Guardar
          </v-btn>
        </template>
        <FlowTransitionMenu
          :transitions="transitions"
          @select="saveAndTransition"
        >
          <template #lead>
            <v-list-item
              :title="`Guardar y mantener como ${currentStatus?.public_name}`"
              @click="savePractice"
            >
              <template #prepend>
                <v-icon color="accent">save</v-icon>
              </template>
            </v-list-item>
            <v-divider />
          </template>
        </FlowTransitionMenu>
      </v-menu>
    </v-card-actions>

    <FlowTransitionDialogs :actions="flowActions" />

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
  </v-card>
</template>
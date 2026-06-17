<script setup>
import FeatureList from "~/components/dashboard/example/good_practice/FeatureList.vue";
import GoodPracticeIntro from "~/components/dashboard/example/good_practice/GoodPracticeIntro.vue";
import FlowStatusChip from "~/components/dashboard/flow/FlowStatusChip.vue";
import FlowTransitions from "~/components/dashboard/flow/FlowTransitions.vue";
import FlowComments from "~/components/dashboard/flow/FlowComments.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import Evidences from "~/components/dashboard/common/utils/Evidences.vue";
import { useRules } from "~/composables/useRules.js"
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const { rules } = useRules()

const props = defineProps({
  isStaff: { type: Boolean, default: true },
  editionAvailable: {
    type: Boolean,
    default: true
  }
})

const full_main = defineModel({type: Object, required: true})

const emit = defineEmits(['close', 'saved', 'deleted'])

const confirmDelete = ref(false)
const loading = ref(false)
const formRef = ref(null)

const isEditing = computed(() => !!full_main.value?.id)

// El motor entrega el nuevo status en flowEvent.to_status; sincronizamos el
// objeto local para que el chip y las transiciones disponibles se refresquen.
function onTransitioned(flowEvent) {
  full_main.value.status = flowEvent.to_status
}

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
    dashStore.showSnackbar('Se guardó la buena práctica')
    emit('saved', res)
  } catch (e) {
    console.error('Error al guardar:', e)
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
        <div class="d-flex align-center">
          <v-text-field
            v-model="full_main.name"
            :rules="[rules.required]"
            label="Nombre de la buena práctica *"
            :variant="isStaff ? 'solo' : 'outlined'"
            class="mr-6"
            :readonly="isStaff"
          />
          <FlowStatusChip
            :status="full_main.status"
            class="mr-3 flex-shrink-0"
          />
          <FlowTransitions
            v-if="isEditing"
            app-label="example"
            model-name="goodpractice"
            :pk="full_main.id"
            @transitioned="onTransitioned"
          />
        </div>
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
      <template v-if="isEditing">
        <v-divider class="mt-2" />
        <div class="text-subtitle-2 mt-3 mb-1">Comentarios</div>
        <FlowComments
          app-label="example"
          model-name="goodpractice"
          :pk="full_main.id"
        />
      </template>
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
  </v-card>
</template>
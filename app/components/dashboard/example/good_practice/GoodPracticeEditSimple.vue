<script setup>
import FeatureList from "~/components/dashboard/example/good_practice/FeatureList.vue";
import StatusDetail from "~/components/dashboard/status/StatusDetail.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

import { useMainStore } from '~/stores/index.js'
import Evidences from "~/components/dashboard/utils/Evidences.vue";
const mainStore = useMainStore()

const props = defineProps({
  full_main: { type: Object, default: null },
  isStaff: { type: Boolean, default: true },
  sentAt: String,
  editionAvailable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'saved', 'deleted'])

const tab = ref('info')
const confirmDelete = ref(false)
const loading = ref(false)

const form = ref({
  id: null,
  package: null,
  axis: null,
  component: null,
  name: '',
  description: '',
  results: '',
  status_register: null,

})

const isEditing = computed(() => !!props.full_main?.id)

const canSave = computed(() => {
  if (props.isStaff) return true
  return form.value.name && form.value.axis && form.value.component
})


const populateForm = () => {
  if (props.full_main) {
    form.value = {
      id: props.full_main.id,
      package: props.full_main.package,
      axis: props.full_main.axis?.id || props.full_main.axis,
      component: props.full_main.component?.id || props.full_main.component,
      name: props.full_main.name,
      description: props.full_main.description,
      results: props.full_main.results,
      status_register: props.full_main.status_register,
      start_year: props.full_main.start_year,
      end_year: props.full_main.end_year
    }
  }
}

const savePractice = async () => {
  if (!canSave.value) return
  loading.value = true
  try {
    const res = await mainStore.saveSimple(['good_practice', form.value])
    emit('saved', res)
  } catch (e) {
    console.error('Error al guardar:', e)
  }
  loading.value = true
}

const remove = async () => {
  try {
    await mainStore.deleteSimple(['good_practice', form.value.id])
    emit('deleted')
  } catch (e) {
    console.error('Error al eliminar:', e)
  }
}

watch(() => props.full_main, populateForm, { immediate: true })

</script>

<template>
  <v-card>
    <slot name="header">
    </slot>
    <v-card-text
      class="pa-4"
    >
      <v-form>
        <div class="d-flex">
          <v-text-field
            v-model="form.name"
            label="Nombre de la buena práctica *"
            :variant="isStaff ? 'solo' : 'outlined'"
            class="mr-6"
            :readonly="isStaff"
          />
          <StatusDetail
            v-if="full_main.status_register !== 'draft'"
            :final_filters="form"
            collection="register"
          />
        </div>
        <div class="d-flex align-center">

          <SelectGroup
            :main_object="form"
            filter_group_name="axes"
            forced_level="subtype"
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
                v-model="form.start_year"
                :readonly="isStaff"
                class="mr-4"
                width="160"
                density="compact"
              />
              <v-text-field
                type="number"
                label="Año de fin"
                variant="outlined"
                v-model="form.end_year"
                :readonly="isStaff"
                width="160"
                density="compact"
              />
            </div>
          </div>
          <div v-else class="mb-4 ml-4 text-subtitle-1">
            <b>Vigencia:</b> Del {{ form.start_year || '----'}}
            al {{ form.end_year || '----'}}
          </div>
        </div>

        <v-textarea
          v-model="form.description"
          label="Descripción"
          :variant="isStaff ? 'solo' : 'outlined'"
          rows="3"
          :readonly="isStaff"
          :counter="5000"
        />

        <v-textarea
          v-model="form.results"
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
        :good-practice-id="form.id"
        :feature-values="full_main?.feature_values || []"
        :is-staff="isStaff"
        class="mt-4 mb-4"
      />

<!--          <Evidences-->
<!--            v-if="isEditing"-->
<!--            model="good_practice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
<!--          <Comments-->
<!--            v-if="isEditing"-->
<!--            model="good_practice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
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
        @click="full_main.in_edition = false"
      >
        Cerrar
      </v-btn>
      <v-btn
        v-if="editionAvailable"
        color="accent"
        variant="flat"
        :loading="loading"
        :disabled="!canSave"
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
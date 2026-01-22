<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useGoodPractice } from '~/composables/useGoodPractice.js'
import FeatureList from "~/components/dashboard/example/goodpractice/FeatureList.vue";
import StatusDetail from "~/components/dashboard/status/StatusDetail.vue";
import SelectGroup from "~/components/dashboard/common/select/SelectGroup.vue";

import { useMainStore } from '~/stores/index.js'
import Evidences from "~/components/dashboard/utils/Evidences.vue";
const mainStore = useMainStore()

const props = defineProps({
  practice: { type: Object, default: null },
  packageId: { type: Number, required: true },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'saved', 'deleted'])

const { loading, deleteGoodPractice } =
  useGoodPractice()

const tab = ref('info')
const confirmDelete = ref(false)

const form = ref({
  id: null,
  package: props.packageId,
  axis: null,
  component: null,
  name: '',
  description: '',
  results: '',
  status_register: null
})

const isEditing = computed(() => !!props.practice?.id)

const canSave = computed(() => {
  return form.value.name && form.value.axis && form.value.component
})


const populateForm = () => {
  if (props.practice) {
    form.value = {
      id: props.practice.id,
      package: props.practice.package,
      axis: props.practice.axis?.id || props.practice.axis,
      component: props.practice.component?.id || props.practice.component,
      name: props.practice.name,
      description: props.practice.description,
      results: props.practice.results,
      status_register: props.practice.status_register
    }
  }
}

const save = async () => {
  if (!canSave.value) return
  try {
    const res = await mainStore.saveSimple(['good_practice', form.value])

    emit('saved', res)
  } catch (e) {
    console.error('Error al guardar:', e)
  }
}

const remove = async () => {
  try {
    await deleteGoodPractice(form.value.id)
    emit('deleted')
  } catch (e) {
    console.error('Error al eliminar:', e)
  }
}

watch(() => props.practice, populateForm, { immediate: true })

</script>

<template>
  <v-card
    tile
    variant="text"
  >

    <v-card-text
      class="pa-4"
    >
      <v-form :disabled="isStaff">
        <div class="d-flex">

          <v-text-field
            v-model="form.name"
            label="Nombre de la buena práctica *"
            variant="outlined"
            class="mr-6"
            :readonly="isStaff"
          />
          <StatusDetail
            :final_filters="form"
            collection="register"
          />
        </div>
        <div class="d-flex">

          <SelectGroup
            :main_object="form"
            filter_group_name="axes"
            forced_level="subtype"
            :width="360"
          />
        </div>

        <v-textarea
          v-model="form.description"
          label="Descripción"
          variant="outlined"
          rows="3"
          :readonly="isStaff"
        />

        <v-textarea
          v-model="form.results"
          label="Resultados obtenidos"
          variant="outlined"
          rows="3"
          :readonly="isStaff"
        />
      </v-form>
      Archivos adjuntos:
      <Evidences
        :full_main="practice"
        main_collection_name="good_practice"
      />

      <FeatureList
        v-if="isEditing"
        :good-practice-id="form.id"
        :feature-values="practice?.feature_values || []"
        :is-staff="isStaff"
        class="mt-4"
      />

<!--          <Evidences-->
<!--            v-if="isEditing"-->
<!--            model="goodpractice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
<!--          <Comments-->
<!--            v-if="isEditing"-->
<!--            model="goodpractice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
    </v-card-text>


    <v-card-actions>
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
        variant="text"
        @click="practice.in_edition = false"
      >
        Cerrar
      </v-btn>
      <v-btn
        v-if="!isStaff"
        color="accent"
        variant="flat"
        :loading="loading"
        :disabled="!canSave"
        prepend-icon="save"
        @click="save"
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
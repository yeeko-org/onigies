<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useGoodPractice } from '~/composables/useGoodPractice.js'
import FeatureList from "~/components/dashboard/example/goodpractice/FeatureList.vue";

const props = defineProps({
  practice: { type: Object, default: null },
  packageId: { type: Number, required: true },
  isStaff: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'saved', 'deleted'])

const { loading, saveGoodPractice, deleteGoodPractice, fetchFeatures } =
  useGoodPractice()

const features = ref([])
const tab = ref('info')
const confirmDelete = ref(false)

const form = ref({
  id: null,
  package: props.packageId,
  axis: null,
  component: null,
  name: '',
  description: '',
  results: ''
})

const isEditing = computed(() => !!props.practice?.id)
const title = computed(() => {
  if (props.isStaff) return 'Evaluar Buena Práctica'
  return isEditing.value ? 'Editar Buena Práctica' : 'Nueva Buena Práctica'
})

const canSave = computed(() => {
  return form.value.name && form.value.axis && form.value.component
})

const loadFeatures = async () => {
  features.value = await fetchFeatures()
}

const populateForm = () => {
  if (props.practice) {
    form.value = {
      id: props.practice.id,
      package: props.practice.package,
      axis: props.practice.axis?.id || props.practice.axis,
      component: props.practice.component?.id || props.practice.component,
      name: props.practice.name,
      description: props.practice.description,
      results: props.practice.results
    }
  }
}

const save = async () => {
  if (!canSave.value) return
  try {
    await saveGoodPractice(form.value)
    emit('saved')
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
onMounted(loadFeatures)
</script>

<template>
  <v-card>
    <v-toolbar color="primary" density="compact">
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>

    <v-tabs v-model="tab" bg-color="grey-lighten-4">
      <v-tab value="info">
        <v-icon start>mdi-information</v-icon>
        Información
      </v-tab>
      <v-tab value="features" :disabled="!isEditing">
        <v-icon start>mdi-format-list-checks</v-icon>
        Características
      </v-tab>
      <v-tab value="evidence" :disabled="!isEditing">
        <v-icon start>mdi-file-document</v-icon>
        Evidencias
      </v-tab>
      <v-tab value="comments" :disabled="!isEditing">
        <v-icon start>mdi-comment-multiple</v-icon>
        Comentarios
      </v-tab>
    </v-tabs>

    <v-card-text class="pa-4" style="max-height: 60vh; overflow-y: auto;">
      <v-tabs-window v-model="tab">
        <!-- TAB: Información -->
        <v-tabs-window-item value="info">
          <v-form :disabled="isStaff">
<!--            <SelectGroup-->
<!--              v-model:axis="form.axis"-->
<!--              v-model:component="form.component"-->
<!--            />-->

            <v-text-field
              v-model="form.name"
              label="Nombre de la buena práctica *"
              variant="outlined"
              density="compact"
              class="mt-4"
              :readonly="isStaff"
            />

            <v-textarea
              v-model="form.description"
              label="Descripción"
              variant="outlined"
              density="compact"
              rows="3"
              :readonly="isStaff"
            />

            <v-textarea
              v-model="form.results"
              label="Resultados obtenidos"
              variant="outlined"
              density="compact"
              rows="3"
              :readonly="isStaff"
            />
          </v-form>

<!--          <StatusDetail-->
<!--            v-if="isEditing"-->
<!--            model="goodpractice"-->
<!--            field="status_validation"-->
<!--            :item-id="form.id"-->
<!--            class="mt-4"-->
<!--          />-->
        </v-tabs-window-item>

        <!-- TAB: Características -->
        <v-tabs-window-item value="features">
          <FeatureList
            v-if="isEditing"
            :good-practice-id="form.id"
            :features="features"
            :feature-values="practice?.feature_values || []"
            :is-staff="isStaff"
          />
        </v-tabs-window-item>

        <!-- TAB: Evidencias -->
        <v-tabs-window-item value="evidence">
<!--          <Evidences-->
<!--            v-if="isEditing"-->
<!--            model="goodpractice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
        </v-tabs-window-item>

        <!-- TAB: Comentarios -->
        <v-tabs-window-item value="comments">
<!--          <Comments-->
<!--            v-if="isEditing"-->
<!--            model="goodpractice"-->
<!--            :parent-id="form.id"-->
<!--          />-->
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>

    <v-divider />

    <v-card-actions>
      <v-btn
        v-if="isEditing && !isStaff"
        color="error"
        variant="text"
        @click="confirmDelete = true"
      >
        <v-icon start>mdi-delete</v-icon>
        Eliminar
      </v-btn>
      <v-spacer />
      <v-btn variant="text" @click="emit('close')">
        Cerrar
      </v-btn>
      <v-btn
        v-if="!isStaff"
        color="primary"
        variant="flat"
        :loading="loading"
        :disabled="!canSave"
        @click="save"
      >
        <v-icon start>mdi-content-save</v-icon>
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
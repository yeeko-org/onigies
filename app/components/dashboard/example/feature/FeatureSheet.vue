<script setup>
import { ref, computed } from 'vue'
import { useMainStore } from "~/stores/index.js";

const mainStore = useMainStore()
const { saveSimple, deleteSimple } = mainStore

const props = defineProps({
  full_main: {
    type: Object,
    required: true,
  },
  show_details: {
    type: Boolean,
    default: false,
  },
  collection_data: Object,
})

const editingId = ref(null)
const option_form = ref({ name: '', value: null })
const deleteDialog = ref(false)
const toDelete = ref(null)
const want_edit = ref(false)

const options = computed(() =>
  props.full_main.feature_options || []
)

const resetForm = () => {
  option_form.value = { name: '', value: null }
  editingId.value = null
  want_edit.value = false
}

const editOption = (option) => {
  want_edit.value = true
  option_form.value = { ...option }
  editingId.value = option.id
}

const saveOption = async () => {
  const params = {
    ...option_form.value,
    feature: props.full_main.id
  }

  const response = await saveSimple(['catalogs/feature_option', params])

  if (!response.errors) {
    if (editingId.value) {
      const idx = options.value.findIndex(
        o => o.id === editingId.value)
      if (idx !== -1) options.value[idx] = response
    }
    else {
      if (!props.full_main.feature_options)
        props.full_main.feature_options = []
      props.full_main.feature_options.push(response)
    }
    resetForm()
  }
}

const confirmDelete = (option) => {
  toDelete.value = option
  deleteDialog.value = true
}

const executeDelete = async () => {
  const res = await deleteSimple([
    'catalogs/feature_option',
    toDelete.value.id
  ])

  if (res.success) {
    want_edit.value = false
    const idx = options.value.findIndex(
      o => o.id === toDelete.value.id
    )
    if (idx !== -1) options.value.splice(idx, 1)
  }

  deleteDialog.value = false
  toDelete.value = null
}
</script>

<template>
  <v-card class="mb-4">
    <v-card-title class="d-flex align-center">
      Opciones de calificación:
      <v-spacer />
      <v-btn
        color="accent"
        size="small"
        variant="outlined"
        @click="want_edit = !want_edit"
      >
        {{ want_edit ? 'Ocultar formulario' : 'Agregar opción' }}
      </v-btn>
    </v-card-title>
    <v-card-text>
      <v-list v-if="options.length" density="compact">
        <v-list-item
          v-for="option in options"
          :key="option.id"
        >
          <v-list-item-title>
            <b class="mr-2">
              {{ option.value }}
            </b>
            {{ option.name }}
          </v-list-item-title>

          <template v-slot:append>
            <v-btn
              icon="edit"
              size="small"
              variant="text"
              @click="editOption(option)"
            />
            <v-btn
              icon="delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(option)"
            />
          </template>
        </v-list-item>
      </v-list>

      <div v-else class="text-caption mb-4">
        No hay opciones registradas
      </div>

      <v-divider class="my-4" />

      <v-row dense v-if="want_edit">
        <v-col cols="12" md="3">
          <v-text-field
            v-model="option_form.value"
            label="Valor"
            type="number"
            density="compact"
            hide-details
          />
        </v-col>
        <v-col cols="12" md="7">
          <v-text-field
            v-model="option_form.name"
            label="Nombre"
            density="compact"
            hide-details
          />
        </v-col>
        <v-col cols="12" md="2" class="d-flex align-center">
          <v-btn
            color="accent"
            @click="saveOption"
            :disabled="!option_form.name || option_form.value === null"
            block
            size="small"
          >
            {{ editingId ? 'Actualizar' : 'Agregar' }}
          </v-btn>
        </v-col>
      </v-row>

      <v-btn
        v-if="editingId"
        @click="resetForm"
        size="small"
        variant="text"
        class="mt-2"
      >
        Cancelar edición
      </v-btn>

    </v-card-text>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          Confirmar eliminación
        </v-card-title>
        <v-card-text>
          ¿Está seguro de eliminar esta opción?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog = false">
            Cancelar
          </v-btn>
          <v-btn color="error" @click="executeDelete">
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<style scoped>

</style>
<script setup>
import {useMainStore} from "~/stores/index.js";
const mainStore = useMainStore()
// const { saveSimple, deleteSimple } = mainStore

const props = defineProps({
  packageId: { type: Number, required: true },
  isStaff: { type: Boolean, default: false }
})

const createForm = ref(null)
const emit = defineEmits(['close', 'created'])
const loading = ref(false)


const form = ref({
  id: null,
  package: props.packageId,
  name: '',
  status_register: 'draft'
})

const create = async () => {
  loading.value = true
  const { valid } = await createForm.value.validate()
  if (!valid) return
  try {
    const res = await mainStore.saveSimple(['good_practice', form.value])
    console.log("res", res)
    emit('created', res)
  } catch (e) {
    console.error('Error al guardar:', e)
  }
  loading.value = false
}

</script>

<template>
  <v-card>
    <v-toolbar color="primary" density="compact">
      <v-toolbar-title>Crear Buena Práctica</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="emit('close')">
        <v-icon>close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text>
      <v-form ref="createForm">
        <v-text-field
          v-model="form.name"
          label="Nombre de la buena práctica *"
          variant="outlined"
          class="mt-4"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn variant="text" @click="emit('close')">
        Cerrar
      </v-btn>
      <v-btn
        color="primary"
        variant="flat"
        :loading="loading"
        @click="create"
      >
        <v-icon start>save</v-icon>
        Crear
      </v-btn>
    </v-card-actions>

  </v-card>
</template>
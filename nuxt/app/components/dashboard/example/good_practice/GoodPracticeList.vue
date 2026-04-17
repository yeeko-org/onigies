<script setup>
import {ref, computed, onMounted, watch} from 'vue'
import { useAuthStore } from '~/store/auth.js'
import { useIesStore } from "~/store/ies.js";
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { getMissingFields } from "~/composables/good_practice_validation.js"
import GoodPracticeCard from "~/components/dashboard/example/good_practice/GoodPracticeCard.vue";
import NewGoodPractice from "~/components/dashboard/example/good_practice/NewGoodPractice.vue";
import GoodPracticeEditSimple from "~/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue";

const props = defineProps({
  packageId: { type: Number, required: false },
  period: { type: Number, required: false }
})

const authStore = useAuthStore()
const { getSimple, saveSimple, saveAction, status_dict } = useMainStore()
const mainStore = useMainStore()
const iesStore = useIesStore()
const dashStore = useDashboardStore()

const isStaff = computed(() => authStore.is_staff)
const goodPracticePackage = ref({
  has_good_practices: null,
})
const goodPractices = ref([])
const create_dialog = ref(false)
const current_loading = ref(false)
const editingPractice = ref(null)
const loadingId = ref(null)

const limit_reached = computed(() => {
  return goodPractices.value.length >= 5
})

const editionAvailable = computed(()=> {
  if (isStaff.value)
    return false
  else {
    return statusSending.value.role === 'ies'
  }
})

const canAddMore = computed(() => {
  if (isStaff.value)
    return false
  if (!editionAvailable.value)
    return false
  return goodPracticePackage.value.has_good_practices && !limit_reached.value
})

const responseOptions = [
  {
    value: true,
    label: 'Sí tengo buenas prácticas',
    color: 'success',
    icon: 'check_circle',
  },
  {
    value: false,
    label: 'No / No deseo responder',
    color: 'grey-darken-1',
    icon: 'cancel',
  },
]

const selectedResponse = computed(() =>
  responseOptions.find(
    o => o.value === goodPracticePackage.value.has_good_practices
  ) || {}
)

const package_id = computed(() => {
  if (props.packageId)
    return props.packageId
  // if (!iesStore.ies_data)
  //   return null
  return iesStore.all_packages.find(p=>p.period === props.period)?.id

})

const loadPractices = async () => {
  current_loading.value = true
  const result = await getSimple(
    ['good_practice_package', package_id.value]
  )
  // console.log("Result good practices:", result)
  if (result && result.good_practices){
    goodPracticePackage.value = result
    setPractices(result.good_practices)
  }
  current_loading.value = false
}

function setPractices(newPractices) {
  goodPractices.value = newPractices
}

onMounted(loadPractices)

async function openEdit(practiceId) {
  loadingId.value = practiceId
  try {
    const full_practice = await getSimple(['good_practice', practiceId])
    if (full_practice) editingPractice.value = full_practice
  } finally {
    loadingId.value = null
  }
}

function onSaved(updated) {
  const idx = goodPractices.value.findIndex(p => p.id === updated.id)
  if (idx !== -1) goodPractices.value[idx] = updated
  editingPractice.value = null
}

function onDeleted() {
  if (!editingPractice.value) return
  const id = editingPractice.value.id
  goodPractices.value = goodPractices.value.filter(p => p.id !== id)
  editingPractice.value = null
}

const openNewForm = () => {
  create_dialog.value = true
}

const onCreated = async (new_practice) => {
  goodPractices.value.push(new_practice)
  create_dialog.value = false
  await openEdit(new_practice.id)
}

function editPackage() {
  current_loading.value = true
  saveSimple(['good_practice_package', goodPracticePackage.value]).then(res=>{
    goodPracticePackage.value = res
    current_loading.value = false
  }).catch(e=>{
    console.error("Error updating package:", e)
    current_loading.value = false
  })
}

const send_dialog = ref(false)
const not_ready_dialog = ref(false)

const canSendPackage = computed(() => {
  if (!goodPractices.value.length) return false
  return goodPractices.value.every(p => p.status_sending === 'ready_to_send')
})

const notReadyDetails = computed(() => {
  return goodPractices.value
    .filter(p => p.status_sending !== 'ready_to_send')
    .map(p => ({
      id: p.id,
      name: p.name || 'Sin nombre',
      missing: getMissingFields(p)
    }))
})

function wantSend() {
  if (canSendPackage.value)
    send_dialog.value = true
  else
    not_ready_dialog.value = true
}

function sendPackage(){
  saveAction(['good_practice_package', package_id.value, 'send']).then(res=>{
    if (res?.errors) {
      dashStore.showSnackbar(
        res.errors.detail || 'No se pudo enviar el paquete', 'error')
      return
    }
    goodPracticePackage.value = res
    setPractices(res.good_practices)
    send_dialog.value = false
  }).catch(e=>{
    console.error("Error sending package:", e)
  })
}

const statusSending = computed(()=> {
  if (!mainStore.status_dict.sending)
    return {}
  return mainStore.status_dict.sending[goodPracticePackage.value.status_sending] || {}
})

</script>

<template>
  <v-card elevation="6" class="pa-3">
    <v-card-title class="d-flex align-center flex-wrap ga-2">
      <v-icon start>lightbulb</v-icon>
      <span>
        Buenas prácticas
        <template v-if="goodPractices.length && false">
          ({{ goodPractices.length }})
        </template>
      </span>
      <v-spacer />
      <v-chip
        variant="text"
        color="grey-darken-1"
      >
        <span
          v-if="limit_reached"
        >
          Has alcanzado el límite de buenas prácticas.
        </span>
        <span v-else-if="editionAvailable">
          (Puedes agregar hasta 5 buenas prácticas)
        </span>
      </v-chip>
      <v-btn
        v-if="canAddMore"
        color="accent"
        variant="elevated"
        @click="openNewForm()"
        prepend-icon="add"
      >
        Agregar
      </v-btn>
<!--        <StatusDetail-->
<!--          v-if="!isStaff"-->
<!--          model="goodpracticepackage"-->
<!--          field="status_sending"-->
<!--          :item-id="goodPracticePackage.id"-->
<!--        />-->
    </v-card-title>
    <v-alert
      v-if="!isStaff && statusSending.role !== 'ies'"
      type="success"
    >
      Las buenas prácticas han sido enviadas y están en revisión.
      Espera los resultados.
    </v-alert>

    <v-card-text class="text-subtitle-1 mt-3 mb-1 d-flex">
      <div class="text-indigo">
        ¿Durante los últimos tres años, su institución ha implementado
        alguna política, programa o acción en materia de igualdad de género,
        no discriminación, cuidados corresponsables y/o
        una vida libre de violencias que, por su trascendencia o innovación,
        considere que constituya una práctica exitosa
        que pudiera ser compartida a nivel nacional?
      </div>
      <v-spacer></v-spacer>
      <div
        v-if="!editionAvailable"
        class="ml-3 d-flex align-center"
        style="width: 680px;"
      >
        <v-chip
          :color="selectedResponse.color"
          :prepend-icon="selectedResponse.icon"
          variant="tonal"
          size="large"
        >
          {{ selectedResponse.label }}
        </v-chip>
        <span class="text-caption text-medium-emphasis ml-3">
          Respuesta registrada
        </span>
      </div>
      <v-radio-group
        v-else
        v-model="goodPracticePackage.has_good_practices"
        style="width: 680px;"
        class="ml-3"
        @update:modelValue="editPackage"
      >
        <v-radio
          v-for="(opt, i) in responseOptions"
          :key="opt.value"
          :class="{ 'mr-3': i === 0 }"
          :label="opt.label"
          :value="opt.value"
        />
      </v-radio-group>
    </v-card-text>

    <v-divider />
    <v-card-text v-if="goodPracticePackage.has_good_practices">
      <v-progress-linear
        v-if="current_loading"
        indeterminate
        color="primary"
      />
      <v-alert
        v-else-if="!goodPractices.length"
        type="info"
        variant="tonal"
      >
        No hay buenas prácticas registradas.
      </v-alert>

      <v-row v-else>
        <v-col
          v-for="practice in goodPractices"
          :key="practice.id"
          cols="12"
        >

          <GoodPracticeCard
            :practice="practice"
            :is-staff="isStaff"
            :sent-at="goodPracticePackage.sent_at"
            :edition-available="editionAvailable"
            :loading="loadingId === practice.id"
            @open="openEdit"
          />

        </v-col>
      </v-row>

    </v-card-text>
    <v-card-actions
      v-if="goodPracticePackage.has_good_practices && editionAvailable"
      class="mb-3 mx-3"
    >
      <v-btn
        v-if="canAddMore"
        color="accent"
        variant="outlined"
        @click="openNewForm()"
        prepend-icon="add"
      >
        Agregar
      </v-btn>

      <v-spacer></v-spacer>
      <v-btn
        color="accent"
        variant="tonal"
        append-icon="send"
        @click="wantSend"
        class="px-6"
      >
        Enviar a revisión
      </v-btn>
    </v-card-actions>
    <v-dialog
      v-model="create_dialog"
      max-width="600"
      persistent
      scrollable
    >
      <NewGoodPractice
        :package-id="package_id"
        :is-staff="true"
        @close="create_dialog = false"
        @created="onCreated"
      />
    </v-dialog>
    <v-dialog
      :model-value="!!editingPractice"
      @update:model-value="editingPractice = null"
      scrollable
    >
      <GoodPracticeEditSimple
        v-if="editingPractice"
        v-model="editingPractice"
        :sent-at="goodPracticePackage.sent_at"
        :is-staff="isStaff"
        :edition-available="editionAvailable"
        class="mt-3"
        @saved="onSaved"
        @deleted="onDeleted"
        @close="editingPractice = null"
      >
        <template #header>
          <v-toolbar
            color="secondary"
            density="compact"
          >
            <v-toolbar-title>
              Editar Buena Práctica
            </v-toolbar-title>
            <v-spacer />
            <v-btn
              icon
              @click="editingPractice = null"
            >
              <v-icon>close</v-icon>
            </v-btn>
          </v-toolbar>
        </template>
      </GoodPracticeEditSimple>
    </v-dialog>
    <v-dialog
      v-model="not_ready_dialog"
      max-width="640"
    >
      <v-card>
        <v-card-title class="headline">
          Aún no puedes enviar las buenas prácticas
        </v-card-title>
        <v-card-text>
          <v-alert
            type="info"
            variant="tonal"
            class="mb-3"
          >
            Todas tus buenas prácticas deben estar en el estado
            <b>"Lista para enviar"</b> antes de enviar el paquete
            a revisión.
          </v-alert>
          <div
            v-if="!goodPractices.length"
            class="text-body-2"
          >
            Aún no has agregado ninguna buena práctica.
          </div>
          <div v-else>
            <div class="text-body-2 mb-2">
              Estas prácticas aún no están listas:
            </div>
            <ul class="ml-4">
              <li
                v-for="p in notReadyDetails"
                :key="p.id"
                class="mb-1"
              >
                <b>{{ p.name }}</b>
                <template v-if="p.missing.length">
                  — falta: {{ p.missing.join(', ') }}
                </template>
                <template v-else>
                  — falta marcarla como "Lista para enviar"
                </template>
              </li>
            </ul>
          </div>
        </v-card-text>
        <v-card-actions class="mx-3 mb-2">
          <v-spacer />
          <v-btn
            variant="elevated"
            color="primary"
            @click="not_ready_dialog = false"
          >
            Entendido, regresar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="send_dialog"
      max-width="600"
    >
      <v-card>
        <v-card-title class="headline text-no-wrap no-wrap">
          ¿De verdad quieres enviar a revisión las buenas prácticas?
        </v-card-title>
        <v-card-text cxlass="text-grey-darken-2">
          <v-alert
            type="warning"
            border="start"
            variant="outlined"
          >
            Una vez enviadas, no podrás realizar modificaciones o agregar nuevas.
          </v-alert>
        </v-card-text>
        <v-card-actions class="mx-2">
          <v-btn
            color="error"
            variant="outlined"
            @click="send_dialog = false"
          >
            Cancelar envio
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="accent"
            variant="elevated"
            @click="sendPackage"
            append-icon="send"
            class="px-6"
          >
            Sí enviar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>

</template>

<style scoped>
.no-wrap{
  word-break: normal !important;
}
</style>
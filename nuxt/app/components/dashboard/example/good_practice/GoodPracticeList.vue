<script setup>
import {ref, computed, onMounted, watch} from 'vue'
import { useAuthStore } from '~/store/auth.js'
import { useIesStore } from "~/store/ies.js";
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlow } from '~/composables/useFlow.js'
import GoodPracticeCard from "~/components/dashboard/example/good_practice/GoodPracticeCard.vue";
import NewGoodPractice from "~/components/dashboard/example/good_practice/NewGoodPractice.vue";
import GoodPracticeEditSimple from "~/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue";
import GoodPracticeIntro from "~/components/dashboard/example/good_practice/GoodPracticeIntro.vue";
import FlowBlockedDialog from "~/components/dashboard/flow/FlowBlockedDialog.vue";
import ConfirmActionDialog from "~/components/dashboard/common/dialog/ConfirmActionDialog.vue";
import FlowStatusChip from "~/components/dashboard/flow/FlowStatusChip.vue";
import FlowComments from "~/components/dashboard/flow/FlowComments.vue";
import { useFlowStore } from '~/store/flow.js'

const props = defineProps({
  packageId: { type: Number, required: false },
  period: { type: Number, required: false }
})

const authStore = useAuthStore()
const { getSimple, saveSimple, saveAction } = useMainStore()
const iesStore = useIesStore()
const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const { transition: packageTransition } = useFlow(
  () => 'example', () => 'goodpracticepackage', () => package_id.value)

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

// Status del paquete resuelto en el catálogo (objeto, no el nombre).
const packageStatus = computed(
  () => flowStore.getStatus(goodPracticePackage.value.status))

const editionAvailable = computed(()=> {
  if (isStaff.value)
    return false
  // Descartado (has_good_practices=false) deja el paquete en bp_discarded
  // (role ies): la IES ya cerró, no debe editar prácticas, solo reabrir.
  if (goodPracticePackage.value.has_good_practices === false)
    return false
  // El motor marca role='ies' cuando es turno de la institución.
  return packageStatus.value?.role === 'ies'
})

const periodOpen = computed(() =>
  !goodPracticePackage.value.survey_full?.period_full?.good_practices_published
)

// La IES puede cambiar su respuesta (Sí/No) mientras sea su turno y el
// periodo siga abierto: bp_draft (respondió "Sí") o bp_discarded ("No"),
// ambos con role 'ies'.
const canEditResponse = computed(() => {
  if (isStaff.value)
    return false
  if (!periodOpen.value)
    return false
  return packageStatus.value?.role === 'ies'
})

const responseModel = computed({
  get: () => goodPracticePackage.value.has_good_practices,
  set: (newValue) => {
    if (newValue === true) {
      goodPracticePackage.value.has_good_practices = true
      editPackage()
    } else if (newValue === false) {
      discard_dialog.value = true
    }
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
  if (result.data && result.data.good_practices){
    goodPracticePackage.value = result.data
    setPractices(result.data.good_practices)
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
    if (full_practice.data) editingPractice.value = full_practice.data
  } finally {
    loadingId.value = null
  }
}

// El diálogo de la IES trabaja sobre una copia (getSimple) para aislar la
// edición de contenido hasta "Guardar". Pero un cambio de status sí se persiste
// en el acto (motor de flujo); lo reflejamos en la tarjeta sin esperar a
// Guardar, sincronizando solo status y flow_events (no el contenido en edición).
watch(() => editingPractice.value?.status, (newStatus) => {
  if (!editingPractice.value || !newStatus) return
  const idx = goodPractices.value.findIndex(
    p => p.id === editingPractice.value.id)
  if (idx === -1) return
  goodPractices.value[idx].status = newStatus
  goodPractices.value[idx].flow_events = editingPractice.value.flow_events
})

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
  const msg_error = 'No se pudo guardar el paquete.'
  saveSimple(['good_practice_package', goodPracticePackage.value], msg_error)
    .then(res=>{
      if (!res.errors)
        goodPracticePackage.value = res.data
      current_loading.value = false
    }).catch(e=>{
      devWarn("Error updating package:", e)
      current_loading.value = false
    })
}

const send_dialog = ref(false)
const blocked_dialog = ref(false)
const discard_dialog = ref(false)

// "Lista" = la IES ya marcó la práctica como completada → su status salió del
// turno de la IES (role !== 'ies'). La regla dura (todas en bp_completed) la
// valida el motor vía valid_child_statuses; esto es solo para la UX.
function practiceReady(p) {
  const st = flowStore.getStatus(p.status)
  return !!st && st.role !== 'ies'
}

const canSendPackage = computed(() => {
  if (!goodPractices.value.length) return false
  return goodPractices.value.every(practiceReady)
})

// Motivos por los que aún no se puede enviar: prácticas que no están marcadas
// como completadas. El detalle de qué falta en cada práctica vive en su
// edición (FlowStatusActions + entry_rules), no aquí.
const notReadyReasons = computed(() => {
  if (!goodPractices.value.length)
    return ['Aún no has agregado ninguna buena práctica.']
  return goodPractices.value
    .filter(p => !practiceReady(p))
    .map(p => `${p.name || 'Sin nombre'}: márcala como completada.`)
})

function wantSend() {
  if (canSendPackage.value)
    send_dialog.value = true
  else
    blocked_dialog.value = true
}

async function sendPackage() {
  const ev = await packageTransition('bp_sent', '')
  if (!ev) return
  send_dialog.value = false
  // Recargamos el paquete: trae status, sent_at, prácticas y flow_events
  // actualizados (incluido el evento de envío), que alimentan los comentarios.
  await loadPractices()
  dashStore.showSnackbar('Buenas prácticas enviadas a revisión')
}

function discardPackage() {
  const msg_error = 'No se pudo descartar el paquete'
  saveAction(['good_practice_package', package_id.value, 'discard'], msg_error)
    .then(res => {
      if (res.errors) return
      goodPracticePackage.value = res.data
      discard_dialog.value = false
    }).catch(e => {
      devWarn("Error discarding package:", e)
    })
}

function reopenPackage() {
  const msg_error = 'No se pudo reabrir el paquete'
  saveAction(['good_practice_package', package_id.value, 'reopen'], msg_error)
    .then(res => {
      if (res.errors) return
      goodPracticePackage.value = res.data
      setPractices(res.data.good_practices || [])
    }).catch(e => {
      devWarn("Error reopening package:", e)
    })
}

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
      <GoodPracticeIntro>
        <template #activator="{ props: activatorProps }">
          <v-btn
            v-bind="activatorProps"
            variant="elevated"
            color="primary"
            prepend-icon="help_outline"
          >
            ¿Qué es una buena práctica?
          </v-btn>
        </template>
      </GoodPracticeIntro>
    </v-card-title>
    <v-alert
      v-if="!isStaff && packageStatus?.role === 'reviewer'"
      type="success"
    >
      Las buenas prácticas han sido enviadas y están en revisión.
      Espera los resultados.
    </v-alert>

    <v-card-text class="py-1 text-body-2 text-grey-darken-1 font-italic">
      Experiencias institucionales exitosas que han logrado
      transformaciones significativas para la igualdad de género.
    </v-card-text>

    <v-card-text class="text-subtitle-1 mt-3 mb-1 d-flex">
      <div class="text-indigo">
        ¿Durante los últimos cinco años, su institución ha implementado
        alguna política, programa o acción en materia de igualdad de género,
        no discriminación, cuidados corresponsables y/o
        una vida libre de violencias que, por su trascendencia o innovación,
        considere que constituya una práctica exitosa
        que pudiera ser compartida a nivel nacional?
      </div>
      <v-spacer></v-spacer>
      <div
        v-if="goodPracticePackage.has_good_practices != null"
        class="ml-3 d-flex flex-column align-center"
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
<!--        <span class="text-caption text-medium-emphasis text-info">-->
<!--          Respuesta registrada-->
<!--        </span>-->
        <v-btn
          v-if="canEditResponse"
          color="accent"
          variant="outlined"
          prepend-icon="undo"
          class="mt-3"
          size="small"
          @click="reopenPackage"
        >
          Cambiar respuesta
        </v-btn>
      </div>
      <v-radio-group
        v-else-if="canEditResponse"
        v-model="responseModel"
        style="width: 680px;"
        class="ml-3"
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

    <v-divider></v-divider>

    <v-card-title class="d-flex my-3 align-center">
      <span class="mr-6">
        {{ goodPractices.length
          ? `${goodPractices.length} buenas prácticas`
          : 'No hay buenas prácticas registradas'
        }}
      </span>
      <v-spacer></v-spacer>
      <v-btn
          v-if="canAddMore"
          color="accent"
          variant="elevated"
          @click="openNewForm()"
          prepend-icon="add"
      >
        Agregar
      </v-btn>
      <v-chip
        v-if="goodPracticePackage.has_good_practices"
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
      <v-spacer></v-spacer>
      <FlowStatusChip
        :status="goodPracticePackage.status"
        label="Status de envío:"
        class="mr-3"
      />
      <FlowComments
        v-if="goodPracticePackage.id"
        v-model="goodPracticePackage"
        app-label="example"
        model-name="goodpracticepackage"
      />
    </v-card-title>
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
        :is-staff="isStaff"
        :edition-available="editionAvailable"
        class="mt-3"
        @saved="onSaved"
        @deleted="onDeleted"
        @close="editingPractice = null"
      >
        <template #header>
          <v-toolbar
            color="primary"
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
    <FlowBlockedDialog
      v-model="blocked_dialog"
      title="Aún no puedes enviar las buenas prácticas"
      :reasons="notReadyReasons"
    />
    <ConfirmActionDialog
      v-model="send_dialog"
      title="¿De verdad quieres enviar a revisión las buenas prácticas?"
      confirm-label="Sí enviar"
      confirm-icon="send"
      cancel-label="Cancelar envío"
      @confirm="sendPackage"
    >
      <v-alert
        type="warning"
        border="start"
        variant="outlined"
      >
        Una vez enviadas, no podrás realizar modificaciones o agregar nuevas.
      </v-alert>
    </ConfirmActionDialog>
    <ConfirmActionDialog
      v-model="discard_dialog"
      title="¿Confirmas que no quieres reportar Buenas Prácticas?"
      confirm-label="Sí, confirmo"
      @confirm="discardPackage"
    >
      <v-alert
        type="info"
        border="start"
        variant="outlined"
      >
        Vas a cerrar tu participación en este módulo.
        Mientras el periodo siga abierto, podrás reabrir y cambiar
        tu respuesta.
      </v-alert>
    </ConfirmActionDialog>
  </v-card>

</template>
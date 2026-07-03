<script setup>
import {ref, computed, onMounted, watch} from 'vue'
import { useAuthStore } from '~/store/auth.js'
import { useIesStore } from "~/store/ies.js";
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import GoodPracticeCard from "~/components/dashboard/example/good_practice/GoodPracticeCard.vue";
import NewGoodPractice from "~/components/dashboard/example/good_practice/NewGoodPractice.vue";
import GoodPracticeResponseQuestion from "~/components/dashboard/example/good_practice/GoodPracticeResponseQuestion.vue";
import GoodPracticeEditDialog from "~/components/dashboard/example/good_practice/GoodPracticeEditDialog.vue";
import GoodPracticeIntro from "~/components/dashboard/example/good_practice/GoodPracticeIntro.vue";
import FlowTransitionDialogs from "~/components/dashboard/flow/FlowTransitionDialogs.vue";
import FlowTransitionMenu from "~/components/dashboard/flow/FlowTransitionMenu.vue";
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
const flowStore = useFlowStore()
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

// Kernel de flujo del paquete: gate de hijos + confirmación + transición.
// onTransitioned recarga para traer sent_at y los flow_events frescos.
const sendActions = useFlowActions(
  goodPracticePackage, 'example', 'goodpracticepackage',
  { onTransitioned: () => loadPractices() })
// Transiciones de envío = las disponibles que ceden el turno a la revisora
// (role 'reviewer': bp_sent / bp_resent). Motor-driven, sin nombres de status;
// excluye el descarte (role 'ies'), que va por su endpoint y su UI Sí/No.
const sendTransitions = computed(() =>
  flowStore.getAvailableTransitions(
    goodPracticePackage.value.status, 'example', 'goodpracticepackage')
    .filter(t => t.role === 'reviewer'))

const limit_reached = computed(() => {
  return goodPractices.value.length >= 5
})

// Status del paquete resuelto en el catálogo (objeto, no el nombre).
const packageStatus = computed(
  () => flowStore.getStatus(goodPracticePackage.value.status))

// Textos del diálogo de descarte desde el catálogo (bp_discarded);
// el descarte va por la acción custom `discard`, no por el kernel de
// flow, así que el diálogo se arma aquí con los mismos textos.
const discardStatus = computed(() => flowStore.getStatus('bp_discarded'))

// Editabilidad de contenido de cualquier nodo del paquete : el motor
// (flowStore) combina el turno de la RAÍZ —el paquete— con el
// content_editable del status propio. Además, con el periodo cerrado la IES
// no edita nada: el backend no lo bloquea en /good_practice/, así que el
// candado de periodo vive aquí.
const canEdit = (obj) =>
  !isStaff.value && periodOpen.value
    && flowStore.canEditContent(obj, goodPracticePackage.value)

const packageEditable = computed(() => canEdit(goodPracticePackage.value))
const editingEditable = computed(() => canEdit(editingPractice.value))

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

// Mapea la intención emitida por GoodPracticeResponseQuestion: "Sí" guarda
// el paquete; "No" abre la confirmación de descarte (la acción de flow
// la ejecuta discardPackage tras confirmar).
function onRespond(value) {
  if (value === true) {
    goodPracticePackage.value.has_good_practices = true
    editPackage()
  } else if (value === false) {
    discard_dialog.value = true
  }
}

const canAddMore = computed(() => {
  if (isStaff.value)
    return false
  if (!packageEditable.value)
    return false
  return goodPracticePackage.value.has_good_practices && !limit_reached.value
})

const hasResponse = computed(
  () => goodPracticePackage.value.has_good_practices != null)

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

const discard_dialog = ref(false)

// Envío del paquete: el menú entrega la transición elegida y delegamos en el
// kernel (gate de hijos por valid_child_statuses + confirmación + transición).
// Sincronizamos el array embebido con el vivo: el gate de hijos lee
// record.good_practices, que se desincroniza tras altas/bajas sin recargar.
function onSendSelect(t) {
  goodPracticePackage.value.good_practices = goodPractices.value
  sendActions.onSelect(t)
}

function discardPackage() {
  const msg_error = 'No se pudo descartar el paquete'
  saveAction(['good_practice_package', package_id.value, 'discard'], msg_error)
    .then(res => {
      if (res.errors) return
      goodPracticePackage.value = res.data
      discard_dialog.value = false
      dashStore.showSnackbar('Registramos tu respuesta.')
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
      dashStore.showSnackbar('Puedes cambiar tu respuesta.')
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

    <GoodPracticeResponseQuestion
      :has-good-practices="goodPracticePackage.has_good_practices"
      :can-edit-response="canEditResponse"
      @respond="onRespond"
      @reopen="reopenPackage"
    />

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
        <span v-else-if="packageEditable">
          (Puedes agregar hasta 5 buenas prácticas)
        </span>
      </v-chip>
      <v-spacer></v-spacer>
      <template v-if="hasResponse">
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
      </template>
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
            :editable="canEdit(practice)"
            :loading="loadingId === practice.id"
            @open="openEdit"
          />
        </v-col>
      </v-row>

    </v-card-text>
    <v-card-actions
      v-if="goodPracticePackage.has_good_practices && packageEditable
        && sendTransitions.length"
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
      <!-- CTA de envío motor-driven: el menú lista las transiciones que ceden
           el turno a la revisora (FlowTransitionMenu usa su action_name). -->
      <v-menu location="top end">
        <template #activator="{ props: menuProps }">
          <v-btn
            v-bind="menuProps"
            color="accent"
            variant="tonal"
            prepend-icon="send"
            append-icon="expand_more"
            class="px-6"
          >
            Enviar a revisión
          </v-btn>
        </template>
        <FlowTransitionMenu
          :transitions="sendTransitions"
          @select="onSendSelect"
        />
      </v-menu>
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
    <GoodPracticeEditDialog
      v-model="editingPractice"
      :is-staff="isStaff"
      :editable="editingEditable"
      @saved="onSaved"
      @deleted="onDeleted"
      @transitioned="loadPractices"
    />
    <FlowTransitionDialogs :actions="sendActions" />
    <ConfirmActionDialog
      v-model="discard_dialog"
      :title="discardStatus?.confirm_title
        || '¿Confirmas que no deseas reportar buenas prácticas?'"
      confirm-label="Sí, confirmo"
      @confirm="discardPackage"
    >
      <v-alert
        type="info"
        border="start"
        variant="outlined"
      >
        {{ discardStatus?.confirm_text
          || 'Tu participación quedará cerrada. Mientras el periodo siga '
          + 'abierto, podrás reabrirla y cambiar tu respuesta.' }}
      </v-alert>
    </ConfirmActionDialog>
  </v-card>

</template>
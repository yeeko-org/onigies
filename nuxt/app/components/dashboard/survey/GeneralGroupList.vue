<script setup>
/**
 * Sección «Información base» (grupo de flujo `gen`): los cinco grupos de
 * preguntas como paneles expandibles sobre un solo Survey, con el envío del
 * GeneralPackage en el encabezado.
 *
 * Sirve a las dos audiencias con el mismo árbol: la IES captura desde
 * /respuestas y la revisión lo monta en el dashboard (SurveyEditSimple) en
 * solo lectura, con sus propias transiciones. Espeja el reparto de Buenas
 * Prácticas: aquí vive el estado del envío y la decisión de quién puede
 * editar; cada panel resuelve su contenido y su transición. La persistencia
 * es de esta sección, no del panel, porque los cinco grupos escriben sobre el
 * mismo recurso.
 */
import { useAuthStore } from '~/store/auth.js'
import { useMainStore } from '~/store/index.js'
import { useDashboardStore } from '~/store/dash.js'
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'
import { useDates } from '~/composables/useDates.js'
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import FlowTransitionMenu from
  '~/components/dashboard/flow/FlowTransitionMenu.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import GeneralGroupPanel from
  '~/components/dashboard/survey/GeneralGroupPanel.vue'

const props = defineProps({
  // Id del Survey (se pide al backend) u objeto Survey ya completo. El
  // dashboard entrega el objeto —su EditSimple solo recibe v-model— y
  // /respuestas entrega el id.
  survey: { type: [Number, Object], required: false },
})

// Resumen del envío tal como lo consume el renglón colapsado del dashboard.
// El kernel de flujo muta `status` en sitio sobre el paquete y sobre cada
// grupo, y `groups` guarda esos mismos objetos: por eso este computed se
// recalcula solo y el watch avisa hacia arriba sin plomería por panel.
const emit = defineEmits(['flow-changed'])

const authStore = useAuthStore()
const mainStore = useMainStore()
const dashStore = useDashboardStore()
const flowStore = useFlowStore()
const { formatDate, formatLongDate } = useDates()

const isStaff = computed(() => authStore.is_staff)

const surveyData = ref(null)
const generalPackage = ref({})
// Array propio (no computed) para que cada panel reciba un modelo escribible.
// El orden lo manda el servidor (GeneralGroup.order): aquí no se reordena.
const groups = ref([])
const panels = ref([])
const loading = ref(false)
const saving = ref(false)

const { ensureRows, buildPayload } = useGeneralSurvey(surveyData)

const packageStatus = computed(
  () => flowStore.getStatus(generalPackage.value.status))

// Espejo cliente de `GeneralPackageBriefSerializer` (lo que trae la lista).
const packageBrief = computed(() => {
  const pkg = generalPackage.value
  if (!pkg.id) return null
  const counts = {}
  for (const group of groups.value)
    counts[group.status] = (counts[group.status] || 0) + 1
  return {
    id: pkg.id,
    status: pkg.status,
    sent_at: pkg.sent_at,
    groups_by_status: counts,
  }
})

watch(packageBrief, (brief) => {
  if (brief) emit('flow-changed', brief)
})

// Cierre autoritativo del backend, espejo del candado de buenas prácticas; el
// front no recalcula con el reloj del cliente.
const periodOpen = computed(
  () => !surveyData.value?.period_full?.is_gen_submission_closed)

const submissionDeadline = computed(
  () => surveyData.value?.period_full?.gen_submission_deadline || null)

// Editabilidad de contenido por grupo: el motor combina el turno de la RAÍZ
// (el envío) con el content_editable del status propio del grupo. Con el
// periodo cerrado la IES no edita nada.
const canEdit = (group) => !isStaff.value && periodOpen.value
  && flowStore.canEditContent(group, generalPackage.value)

// Kernel de flujo del envío: la compuerta de hijos (valid_child_statuses)
// bloquea el envío hasta que los cinco grupos estén completados.
// Tras enviar, ningún grupo sigue siendo editable: los paneles se recalculan.
const sendActions = useFlowActions(
  generalPackage, 'survey', 'generalpackage',
  { onTransitioned: () => resetPanels() })

// Transiciones de envío = las que ceden el turno a la revisión
// (gen_sent / gen_resent), sin nombrar status en el código.
const sendTransitions = computed(() => flowStore.getAvailableTransitions(
  generalPackage.value.status, 'survey', 'generalpackage')
  .filter((t) => t.role === 'reviewer'))

// Al cargar quedan abiertos los grupos que la IES puede editar en su turno
// (borrador, regresados con ajustes) y cerrados los completados o terminales.
// La revisión los ve todos abiertos: solo lee.
function resetPanels() {
  panels.value = isStaff.value
    ? groups.value.map((g) => g.id)
    : groups.value.filter((g) => canEdit(g)).map((g) => g.id)
}

/**
 * El detalle del Survey ya anida el `general_package` completo, con sus
 * grupos, sus status y sus flow_events: traer contenido y flujo juntos evita
 * que se desincronicen. El endpoint /general_package/ existe, pero aquí no
 * hace falta.
 *
 * El paquete se guarda en su propia ref porque el PATCH del Survey NO lo
 * devuelve: la respuesta de guardado reemplaza el contenido, no el flujo.
 */
function applySurvey(data) {
  surveyData.value = data
  ensureRows()
  generalPackage.value = data.general_package || {}
  groups.value = generalPackage.value.general_group_responses || []
  resetPanels()
}

async function loadAll(source) {
  if (!source) return
  // Objeto completo (dashboard): se usa tal cual, sin petición extra.
  if (typeof source === 'object') return applySurvey(source)
  loading.value = true
  try {
    const res = await mainStore.getSimple(['survey', source])
    if (res.data) applySurvey(res.data)
  } finally {
    loading.value = false
  }
}

watch(() => props.survey, loadAll, { immediate: true })

/**
 * Persiste el Survey completo. Se manda con PATCH: la sincronización de
 * `population_quantities` es total sobre las claves presentes, y solo PATCH
 * garantiza que lo ausente no se toque.
 */
async function persist() {
  if (!surveyData.value) return false
  saving.value = true
  const msg_error = 'No se pudo guardar la información base'
  try {
    const res = await mainStore.patchSimple(
      ['survey', surveyData.value.id, buildPayload()], msg_error)
    if (res.errors) return false
    // El PATCH devuelve solo el contenido: se conserva lo que ya se tenía
    // (period_full, general_package) para no perder candado ni flujo.
    surveyData.value = { ...surveyData.value, ...res.data }
    ensureRows()
    dashStore.showSnackbar('Cambios guardados')
    return true
  } catch (e) {
    devWarn('Error al guardar la información base:', e)
    return false
  } finally {
    saving.value = false
  }
}

function collapseGroup(groupId) {
  panels.value = panels.value.filter((id) => id !== groupId)
}

// El menú entrega la transición elegida; el kernel corre la compuerta de
// hijos, pide confirmación y ejecuta.
function onSendSelect(transition) {
  sendActions.onSelect(transition)
}
</script>

<template>
  <v-card elevation="6" class="pa-3">
    <v-card-title class="d-flex align-center flex-wrap ga-3">
      <v-icon start>fact_check</v-icon>
      <span>Información base</span>
      <v-spacer />
      <template v-if="generalPackage.id">
        <!-- La revisión dictamina el envío desde aquí; la IES lo envía con el
             botón de abajo y aquí solo lee su estado. -->
        <FlowStatusActions
          v-if="isStaff"
          v-model="generalPackage"
          app-label="survey"
          model-name="generalpackage"
          :actions="sendActions"
        />
        <FlowStatusChip
          v-else
          :status="generalPackage.status"
          label="Status de envío:"
        />
        <FlowComments
          v-model="generalPackage"
          app-label="survey"
          model-name="generalpackage"
        />
      </template>
    </v-card-title>

    <v-card-text class="py-1 text-body-2 text-grey-darken-1 font-italic">
      Datos institucionales que dan contexto al resto del cuestionario:
      estructura, poblaciones, autoridades, planes de estudio y forma de
      gobierno.
    </v-card-text>

    <!-- Institución y periodo ya están en el renglón colapsado del Survey;
         aquí solo falta cuándo llegó el envío. -->
    <v-card-text
      v-if="isStaff && generalPackage.sent_at"
      class="py-1 text-body-2 text-grey-darken-1"
    >
      <v-icon size="small" start>send</v-icon>
      Enviado el {{ formatDate(generalPackage.sent_at) }}
    </v-card-text>

    <v-alert
      v-if="!isStaff && packageStatus?.role === 'reviewer'"
      type="success"
      variant="tonal"
      class="mx-3 my-2"
    >
      Su información base fue enviada y está en revisión.
      Le avisaremos si se requieren ajustes.
    </v-alert>

    <v-card-text>
      <v-progress-linear v-if="loading" indeterminate color="primary" />
      <v-alert
        v-else-if="!surveyData || !groups.length"
        type="info"
        variant="tonal"
      >
        Aún no hay información base disponible para este periodo.
      </v-alert>
      <v-expansion-panels
        v-else
        v-model="panels"
        multiple
        variant="accordion"
      >
        <GeneralGroupPanel
          v-for="(group, index) in groups"
          :key="group.id"
          v-model:group="groups[index]"
          v-model:survey="surveyData"
          :is-staff="isStaff"
          :editable="canEdit(group)"
          :saving="saving"
          :persist="persist"
          @collapse="collapseGroup(group.id)"
        />
      </v-expansion-panels>
    </v-card-text>

    <!-- Recordatorio de la fecha límite mientras es el turno de la IES y el
         periodo sigue abierto (solo si hay fecha configurada). -->
    <v-alert
      v-if="!isStaff && periodOpen && submissionDeadline
        && packageStatus?.role === 'ies'"
      type="info"
      variant="tonal"
      density="comfortable"
      class="mt-2 mx-3"
    >
      Tiene hasta el {{ formatLongDate(submissionDeadline) }} para enviar
      su respuesta.
    </v-alert>

    <!-- Periodo cerrado con la IES aún en turno: perdió la ventana de envío.
         El candado real vive en el backend; esto solo lo comunica. -->
    <v-alert
      v-if="!isStaff && !periodOpen && packageStatus?.role === 'ies'"
      type="warning"
      variant="tonal"
      class="my-3 mx-3"
    >
      El periodo de envío ya cerró.
    </v-alert>

    <v-card-actions
      v-if="!isStaff && periodOpen && sendTransitions.length"
      class="mb-3 mx-3"
    >
      <v-spacer />
      <v-menu location="top end">
        <template #activator="{ props: menuProps }">
          <v-btn
            v-bind="menuProps"
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

    <!-- Un solo juego de diálogos por kernel, para las dos audiencias: el
         botón de envío de la IES no monta ninguno, y FlowStatusActions solo
         los monta cuando crea su propio kernel (aquí se le pasa el de
         arriba). Sin esto la revisora elige una transición y no pasa nada. -->
    <FlowTransitionDialogs :actions="sendActions" />
  </v-card>
</template>

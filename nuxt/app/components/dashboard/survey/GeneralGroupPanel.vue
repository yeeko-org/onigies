<script setup>
/**
 * Un grupo de la sección «Información base» como panel expandible.
 *
 * Componente de doble audiencia (`isStaff` / `editable`, igual que
 * GoodPracticeEditSimple): la IES captura desde /respuestas y la revisión lo
 * reutiliza tal cual en solo lectura, sin bifurcar la presentación de las
 * preguntas.
 *
 * El contenido de los cinco grupos vive en un solo recurso (el Survey), así
 * que la persistencia NO es del panel: el padre le pasa `persist`, que guarda
 * el Survey completo. El panel solo decide cuándo llamarlo y qué transición
 * disparar después.
 */
import FlowStatusChip from '~/components/dashboard/flow/FlowStatusChip.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import FlowTransitionMenu from '~/components/dashboard/flow/FlowTransitionMenu.vue'
import FlowTransitionDialogs from '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowStatusActions from '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowAttachments from '~/components/dashboard/flow/FlowAttachments.vue'
import GeneralNumberFields from '~/components/dashboard/survey/GeneralNumberFields.vue'
import GeneralPopulations from '~/components/dashboard/survey/GeneralPopulations.vue'
import GeneralAuthorities from '~/components/dashboard/survey/GeneralAuthorities.vue'
import GeneralGovernment from '~/components/dashboard/survey/GeneralGovernment.vue'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'
import { useGeneralValidation } from '~/composables/useGeneralValidation.js'

// Qué hijo pinta cada grupo. Mapa constante a nivel de módulo: no es
// reactivo y los grupos sin entrada propia son preguntas numéricas.
const GROUP_COMPONENTS = {
  poblaciones: GeneralPopulations,
  autoridades: GeneralAuthorities,
  forma_gobierno: GeneralGovernment,
}

// Grupos cuyo hijo coloca él mismo la instrucción, porque no encabeza al
// grupo entero sino a un bloque interno: en `autoridades` describe la
// tabla, que va después del radio de la persona titular.
const OWN_INSTRUCTION_GROUPS = ['autoridades']

// Transiciones que comprometen el contenido del grupo ante la revisión y
// por eso pasan por la compuerta de campos vacíos (task-106). Guardar
// nunca valida: la captura ocurre en varias sesiones.
const VALIDATED_TRANSITIONS = ['gen_completed', 'gen_adjusted']

// Cuántos faltantes se enumeran antes de resumir el resto: la lista debe
// decir qué falta sin volverse un muro de texto.
const MAX_LISTED_ISSUES = 8

const props = defineProps({
  isStaff: { type: Boolean, default: false },
  editable: { type: Boolean, default: false },
  saving: { type: Boolean, default: false },
  // Guarda el Survey completo y resuelve a true si persistió.
  persist: { type: Function, required: true },
})

const survey = defineModel('survey', { type: Object, required: true })
const group = defineModel('group', { type: Object, required: true })

const emit = defineEmits(['collapse'])

const { populationSectors, mainSectors, iesHead, authorityBodies,
  isPresent, rowFor, hasCount } = useGeneralSurvey(survey)

// Tolera las dos formas posibles del anidado del catálogo: la convención del
// repo es `{campo}_full`, pero el contrato solo promete «los datos del
// catálogo GeneralGroup».
const catalog = computed(() => {
  const raw = group.value.general_group_full || group.value.general_group
  return raw && typeof raw === 'object' ? raw : {}
})
const groupName = computed(() => catalog.value.name || '')

const title = computed(() => catalog.value.title
  || catalog.value.public_name || catalog.value.name)
const questions = computed(() => catalog.value.questions || [])

const groupComponent = computed(
  () => GROUP_COMPONENTS[groupName.value] || GeneralNumberFields)

const placesOwnInstruction = computed(
  () => OWN_INSTRUCTION_GROUPS.includes(groupName.value))

const { issues } = useGeneralValidation(survey, catalog)

// Los errores se pintan solo después de un intento de completar: mientras
// la IES captura, un formulario en rojo desde el primer render estorba.
const showErrors = ref(false)
const invalid = computed(() => new Set(
  showErrors.value ? issues.value.map((i) => i.key) : []))
const listedIssues = computed(() => issues.value.slice(0, MAX_LISTED_ISSUES))
const hiddenIssues = computed(
  () => Math.max(issues.value.length - MAX_LISTED_ISSUES, 0))

const flowActions = useFlowActions(group, 'survey', 'generalgroupresponse')
const { transitions, currentStatus } = flowActions

// El serializer siempre manda `flow_attachments`; se garantiza el array
// para que el v-model de FlowAttachments tenga dónde escribir aunque el
// grupo llegue de una respuesta parcial.
watchEffect(() => {
  if (group.value && !Array.isArray(group.value.flow_attachments))
    group.value.flow_attachments = []
})

// Fracción capturada: cuántas de las respuestas que este grupo espera ya
// tienen dato. Nunca es un porcentaje de avance del flujo. Poblaciones lleva
// su propia redacción: su cabeza cuenta las presentes (incluidas las extra,
// que no se cuentan) y la fracción solo las contables.
const fraction = (filled, expected) =>
  `${filled}/${expected} capturado${expected === 1 ? '' : 's'}`

// Renglón-resumen del panel colapsado: cuántos renglones tiene el grupo y
// cuántos están capturados.
const summary = computed(() => {
  const data = survey.value
  if (groupName.value === 'poblaciones') {
    // Las presentes se cuentan todas, pero solo las principales esperan
    // conteo: las 2 extra son estructurales y nunca se cuentan.
    const present = populationSectors.value.filter((s) => isPresent(s.id))
    if (!present.length) return '0 presentes'
    const expected = mainSectors.value.filter((s) => isPresent(s.id))
    const filled = expected.filter((s) => hasCount(rowFor(s.id))).length
    return `${present.length} presentes · `
      + `${filled}/${expected.length} con conteo`
  }
  if (groupName.value === 'autoridades') {
    const bodies = authorityBodies.value
    const expected = bodies.length + (iesHead.value ? 1 : 0)
    // «No aplica» es una respuesta, no un pendiente: el renglón marcado
    // cuenta como resuelto aunque nunca lleve conteo.
    const resolved = (sector) => {
      const row = rowFor(sector.id)
      return row?.no_apply === true || hasCount(row)
    }
    let filled = bodies.filter(resolved).length
    if (iesHead.value && hasCount(rowFor(iesHead.value.id))) filled += 1
    return `${expected} autoridades · ${fraction(filled, expected)}`
  }
  // El resto de los grupos responde sobre columnas del Survey, una por
  // pregunta del catálogo: `name` es justamente esa columna.
  if (!questions.value.length) return ''
  const answered = questions.value.filter(
    (q) => data[q.name] != null && data[q.name] !== '').length
  return fraction(answered, questions.value.length)
})

const keepStatusLabel = computed(
  () => `Guardar y mantener como ${currentStatus.value?.public_name}`)

const saveGroup = async () => {
  await props.persist()
}

// Guarda primero y transiciona después (patrón de GoodPracticeEditSimple):
// si el guardado falla no se mueve el estado, y el panel se colapsa solo
// cuando la transición realmente ocurrió y ya no es editable.
const saveAndTransition = async (transition) => {
  if (VALIDATED_TRANSITIONS.includes(transition.name) && issues.value.length) {
    showErrors.value = true
    return
  }
  showErrors.value = false
  if (!(await props.persist())) return
  const event = await flowActions.onSelect(transition)
  if (event) emit('collapse')
}
</script>

<template>
  <v-expansion-panel :value="group.id">
    <v-expansion-panel-title color="grey-lighten-3">
      <div class="d-flex align-center ga-3 w-100 pr-2">
        <span class="text-subtitle-1 font-weight-medium">{{ title }}</span>
        <FlowStatusChip :status="group.status" x-small />
        <v-spacer />
        <span class="text-caption text-grey-darken-1">{{ summary }}</span>
      </div>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <div class="d-flex align-center justify-end ga-2 mb-3">
        <FlowStatusActions
          v-if="isStaff"
          v-model="group"
          app-label="survey"
          model-name="generalgroupresponse"
          :actions="flowActions"
        />
        <FlowComments
          v-if="group.id"
          v-model="group"
          app-label="survey"
          model-name="generalgroupresponse"
          :width="220"
        />
      </div>

      <!-- Encabezado del grupo: se pinta aquí una sola vez y sale del
           catálogo; ningún hijo lleva textos introductorios propios. -->
      <p v-if="catalog.subtitle" class="text-body-1 mb-1">
        {{ catalog.subtitle }}
      </p>
      <p
        v-if="catalog.instruction && !placesOwnInstruction"
        class="text-body-1 text-grey-darken-1 mb-4"
      >
        {{ catalog.instruction }}
      </p>

      <component
        :is="groupComponent"
        v-model="survey"
        :catalog="catalog"
        :editable="editable"
        :invalid="invalid"
      />

      <!-- Evidencia probatoria del grupo. Se ancla al GeneralGroupResponse
           y se guarda al instante (no entra en el PATCH del Survey). -->
      <div class="mt-6">
        <p class="text-subtitle-2 mb-1">
          Evidencia probatoria
        </p>
        <FlowAttachments
          v-model="group.flow_attachments"
          app-label="survey"
          model-name="generalgroupresponse"
          :id="group.id"
          :editable="editable"
        />
      </div>

      <!-- Compuerta de completado: dice qué falta, campo por campo, y se
           vacía sola conforme la IES responde. -->
      <v-alert
        v-if="editable && showErrors && issues.length"
        type="error"
        variant="tonal"
        density="compact"
        class="mt-4"
      >
        <div class="text-body-2 mb-1">
          Para marcar este grupo como completado falta responder:
        </div>
        <ul class="pl-4 text-body-2">
          <li v-for="issue in listedIssues" :key="issue.key">
            {{ issue.label }}
          </li>
          <li v-if="hiddenIssues">
            … y {{ hiddenIssues }} respuesta{{ hiddenIssues === 1 ? '' : 's' }}
            más.
          </li>
        </ul>
      </v-alert>

      <v-card-actions v-if="editable" class="px-0 mt-4">
        <v-spacer />
        <!-- Sin transiciones disponibles: el botón solo guarda. -->
        <v-btn
          v-if="!transitions.length"
          variant="flat"
          prepend-icon="save"
          :loading="saving"
          @click="saveGroup"
        >
          Guardar
        </v-btn>
        <!-- Con transiciones: split-button encabezado por el guardado simple
             y seguido de cada acción que guarda y luego transiciona. -->
        <v-menu v-else location="bottom end">
          <template #activator="{ props: menuProps }">
            <v-btn
              v-bind="menuProps"
              variant="flat"
              prepend-icon="save"
              append-icon="expand_more"
              :loading="saving"
            >
              Guardar
            </v-btn>
          </template>
          <FlowTransitionMenu
            :transitions="transitions"
            @select="saveAndTransition"
          >
            <template #lead>
              <v-list-item
                :title="keepStatusLabel"
                @click="saveGroup"
              >
                <template #prepend>
                  <v-icon color="accent">save</v-icon>
                </template>
              </v-list-item>
              <v-divider />
            </template>
          </FlowTransitionMenu>
        </v-menu>
      </v-card-actions>

      <!-- Un solo juego de diálogos por kernel, para las dos audiencias: el
           split-button de la IES no monta ninguno, y FlowStatusActions solo
           los monta cuando crea su propio kernel (aquí se le pasa el de
           arriba). Sin esto la revisora elige una transición y no pasa
           nada. -->
      <FlowTransitionDialogs :actions="flowActions" />
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

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
import FlowTransitionMenu from
  '~/components/dashboard/flow/FlowTransitionMenu.vue'
import FlowTransitionDialogs from
  '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowStatusActions from
  '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowAttachments from
  '~/components/dashboard/flow/FlowAttachments.vue'
import GeneralNumberFields from
  '~/components/dashboard/survey/GeneralNumberFields.vue'
import GeneralPopulations from
  '~/components/dashboard/survey/GeneralPopulations.vue'
import GeneralAuthorities from
  '~/components/dashboard/survey/GeneralAuthorities.vue'
import GeneralGovernment from
  '~/components/dashboard/survey/GeneralGovernment.vue'
import { useFlowActions } from '~/composables/useFlowActions.js'
import { useGeneralSurvey } from '~/composables/useGeneralSurvey.js'

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
  isSelected, rowFor, hasCount } = useGeneralSurvey(survey)

// Tolera las dos formas posibles del anidado del catálogo: la convención del
// repo es `{campo}_full`, pero el contrato solo promete «los datos del
// catálogo GeneralGroup».
const catalog = computed(() => {
  const raw = group.value.general_group_full || group.value.general_group
  return raw && typeof raw === 'object' ? raw : {}
})
const groupName = computed(() => catalog.value.name || '')
const title = computed(() => catalog.value.public_name || catalog.value.name)
const fields = computed(() => catalog.value.fields || [])

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
// su propia redacción: su cabeza cuenta las marcadas (incluidas las extra,
// que no se cuentan) y la fracción solo las contables.
const fraction = (filled, expected) =>
  `${filled}/${expected} capturado${expected === 1 ? '' : 's'}`

// Renglón-resumen del panel colapsado: cuántos renglones tiene el grupo y
// cuántos están capturados.
const summary = computed(() => {
  const data = survey.value
  if (groupName.value === 'poblaciones') {
    // Las marcadas se cuentan todas, pero solo las principales esperan
    // conteo: las 2 extra son estructurales y nunca se cuentan.
    const marked = populationSectors.value.filter((s) => isSelected(s.id))
    if (!marked.length) return '0 marcadas'
    const expected = mainSectors.value.filter((s) => isSelected(s.id))
    const filled = expected.filter((s) => hasCount(rowFor(s.id))).length
    return `${marked.length} marcadas · `
      + `${filled}/${expected.length} con conteo`
  }
  if (groupName.value === 'autoridades') {
    const bodies = authorityBodies.value
    const expected = bodies.length + (iesHead.value ? 1 : 0)
    let filled = bodies.filter((s) => hasCount(rowFor(s.id))).length
    if (iesHead.value && hasCount(rowFor(iesHead.value.id))) filled += 1
    return `${expected} autoridades · ${fraction(filled, expected)}`
  }
  if (groupName.value === 'forma_gobierno')
    return fraction(data.is_centralized == null ? 0 : 1, 1)
  if (!fields.value.length) return ''
  const answered = fields.value.filter(
    (f) => data[f.name] != null && data[f.name] !== '').length
  return fraction(answered, fields.value.length)
})

const saveGroup = async () => {
  await props.persist()
}

// Guarda primero y transiciona después (patrón de GoodPracticeEditSimple):
// si el guardado falla no se mueve el estado, y el panel se colapsa solo
// cuando la transición realmente ocurrió y ya no es editable.
const saveAndTransition = async (transition) => {
  if (!(await props.persist())) return
  const event = await flowActions.onSelect(transition)
  if (event) emit('collapse')
}
</script>

<template>
  <v-expansion-panel :value="group.id">
    <v-expansion-panel-title>
      <div class="d-flex align-center ga-3 w-100 pr-2">
        <span class="text-subtitle-1 font-weight-medium">{{ title }}</span>
        <FlowStatusChip :status="group.status" x-small />
        <v-spacer />
        <span class="text-caption text-grey-darken-1">{{ summary }}</span>
        <div @click.stop>
          <FlowComments
            v-if="group.id"
            v-model="group"
            app-label="survey"
            model-name="generalgroupresponse"
            :width="220"
          />
        </div>
      </div>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <GeneralPopulations
        v-if="groupName === 'poblaciones'"
        v-model="survey"
        :editable="editable"
      />
      <GeneralAuthorities
        v-else-if="groupName === 'autoridades'"
        v-model="survey"
        :editable="editable"
      />
      <GeneralGovernment
        v-else-if="groupName === 'forma_gobierno'"
        v-model="survey"
        :fields="fields"
        :editable="editable"
      />
      <GeneralNumberFields
        v-else
        v-model="survey"
        :fields="fields"
        :editable="editable"
      />

      <!-- Evidencia probatoria del grupo. Se ancla al GeneralGroupResponse
           y se guarda al instante (no entra en el PATCH del Survey). -->
      <div class="mt-6">
        <p class="text-subtitle-2 mb-1">
          Evidencia probatoria (opcional)
        </p>
        <FlowAttachments
          v-model="group.flow_attachments"
          app-label="survey"
          model-name="generalgroupresponse"
          :id="group.id"
          :editable="editable"
        />
      </div>

      <!-- La revisión no edita contenido: corre sus transiciones directo
           desde el control de estado, sin guardado previo que encadenar. -->
      <v-card-actions v-if="isStaff" class="px-0 mt-4">
        <FlowStatusActions
          v-model="group"
          app-label="survey"
          model-name="generalgroupresponse"
          :actions="flowActions"
        />
      </v-card-actions>
      <v-card-actions v-else-if="editable" class="px-0 mt-4">
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
                :title="`Guardar y mantener como ${currentStatus?.public_name}`"
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
           arriba). Sin esto la revisora elige una transición y no pasa nada. -->
      <FlowTransitionDialogs :actions="flowActions" />
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

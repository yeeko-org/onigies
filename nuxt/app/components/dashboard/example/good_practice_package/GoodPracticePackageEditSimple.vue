<script setup>
/**
 * Centro de control de revisión de un Envío de Buenas Prácticas
 * (dashboard / revisora). 
 *
 * Espejea la lógica de GoodPracticeList.vue (la vista IES): cabecera con los
 * datos del envío + status + comentarios, un resumen de progreso y una rejilla
 * de GoodPracticeCard. Al abrir una tarjeta se despliega GoodPracticeEditSimple
 * en un diálogo para calificar (FeatureList) y cambiar el status de esa
 * práctica.
 *
 * NO incluye has_good_practices ni enviar/descartar: eso es del
 * mundo de la IES (ver GoodPracticeList.vue en /respuestas).
 */
import { useFlowStore } from '~/store/flow.js'
import { useFlowActions } from '~/composables/useFlowActions.js'
import FlowStatusActions from '~/components/dashboard/flow/FlowStatusActions.vue'
import FlowTransitionMenu from '~/components/dashboard/flow/FlowTransitionMenu.vue'
import FlowTransitionDialogs from '~/components/dashboard/flow/FlowTransitionDialogs.vue'
import FlowComments from '~/components/dashboard/flow/FlowComments.vue'
import GoodPracticeCard from '~/components/dashboard/example/good_practice/GoodPracticeCard.vue'
import GoodPracticeEditSimple from '~/components/dashboard/example/good_practice/GoodPracticeEditSimple.vue'
import { useDates } from '~/composables/useDates.js'

const pkg = defineModel({ type: Object, required: true })

const flowStore = useFlowStore()
const { formatDate } = useDates()

// Un solo kernel para el menú-chip de arriba y el botón "Enviar evaluación"
// de abajo: comparten transiciones y un único juego de diálogos.
const flowActions = useFlowActions(pkg, 'example', 'goodpracticepackage')
// Desestructurado para el CTA inferior: en el template los refs anidados
// (flowActions.transitions) no se desenvuelven; como variables tope, sí.
const { transitions: sendTransitions, onSelect: onSendSelect } = flowActions

const institution = computed(
  () => pkg.value.survey_full?.institution_full || {})

const period = computed(
  () => pkg.value.survey_full?.period_full?.year
    || pkg.value.survey_full?.period)

const practices = computed(() => pkg.value.good_practices || [])

// Turno de la revisora: el motor marca role='reviewer' en bp_sent / bp_resent.
const canReview = computed(
  () => flowStore.getStatus(pkg.value.status)?.role === 'reviewer')

// Progreso de dictamen: prácticas en status terminal (role null) ya resueltas
// (bp_for_ruling / bp_rejected). El motor bloquea bp_finished hasta que todas
// lo estén; el resumen es solo orientación.
const ruledCount = computed(() => practices.value.filter(p => {
  const st = flowStore.getStatus(p.status)
  return !!st && st.role === null
}).length)

const editingPractice = ref(null)

function openPractice(practiceId) {
  editingPractice.value =
    practices.value.find(p => p.id === practiceId) || null
}

function onSaved(updated) {
  if (editingPractice.value)
    Object.assign(editingPractice.value, updated)
}
</script>

<template>
  <v-card variant="flat">
    <!-- Cabecera: datos del envío + status + comentarios ───────────────── -->
    <v-card-title class="d-flex align-start flex-wrap ga-2">
      <div class="d-flex align-center flex-wrap ga-2 flex-grow-1">
        <v-card
          v-if="pkg.survey_full"
          class="px-3 py-1"
          color="blue"
          variant="tonal"
        >
          {{ institution.name }}
          <span v-if="institution.acronym" class="text-caption ml-1">
            ({{ institution.acronym }})
          </span>
        </v-card>
        <v-card class="px-3 py-1" color="indigo" variant="tonal">
          {{ period }}
        </v-card>
        <v-card
          v-if="pkg.sent_at"
          class="px-3 py-1"
          color="green"
          variant="tonal"
        >
          Enviado el {{ formatDate(pkg.sent_at) }}
        </v-card>
      </div>
      <FlowComments
        v-if="pkg.id"
        v-model="pkg"
        app-label="example"
        model-name="goodpracticepackage"
      />
    </v-card-title>

    <!-- Estado + transiciones del envío (turno de la revisora) ─────────── -->
    <v-card-text v-if="pkg.id" class="d-flex align-center flex-wrap ga-6 py-3">
      <FlowStatusActions
        v-model="pkg"
        app-label="example"
        model-name="goodpracticepackage"
        :actions="flowActions"
      />
      <v-chip
        v-if="practices.length"
        variant="tonal"
        :color="ruledCount === practices.length ? 'success' : 'warning'"
        prepend-icon="gavel"
      >
        {{ ruledCount }}/{{ practices.length }} prácticas dictaminadas
      </v-chip>
    </v-card-text>

    <v-divider />

    <!--  Buenas Prácticas del envío  ─────────────────────────────────── -->
    <v-card-text>
      <div class="text-subtitle-1 mb-3">
        {{ practices.length
          ? `${practices.length} buenas prácticas`
          : 'Este envío no tiene buenas prácticas registradas' }}
      </div>
      <v-row v-if="practices.length">
        <v-col
          v-for="practice in practices"
          :key="practice.id"
          cols="12"
        >
          <GoodPracticeCard
            :practice="practice"
            :is-staff="true"
            :sent-at="pkg.sent_at"
            :editable="canReview"
            @open="openPractice"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <!-- CTA de la revisora: envía la evaluación eligiendo el siguiente status.
         Comparte kernel con el menú-chip de arriba. -->
    <v-card-actions
      v-if="sendTransitions.length"
      class="px-4 pb-4"
    >
      <v-spacer />
      <v-menu location="bottom end">
        <template #activator="{ props: menuProps }">
          <v-btn
            v-bind="menuProps"
            color="accent"
            variant="flat"
            prepend-icon="send"
            append-icon="expand_more"
          >
            Enviar evaluación
          </v-btn>
        </template>
        <FlowTransitionMenu
          :transitions="sendTransitions"
          @select="onSendSelect"
        />
      </v-menu>
    </v-card-actions>

    <FlowTransitionDialogs :actions="flowActions" />

    <!-- Diálogo de calificación / status de una práctica ───────────────── -->
    <v-dialog
      :model-value="!!editingPractice"
      @update:model-value="editingPractice = null"
      scrollable
    >
      <GoodPracticeEditSimple
        v-if="editingPractice"
        v-model="editingPractice"
        :is-staff="true"
        :editable="canReview"
        class="mt-3"
        @saved="onSaved"
        @close="editingPractice = null"
      >
        <template #header>
          <v-toolbar color="primary">
            <v-toolbar-title>
              {{ canReview ? 'Calificar buena práctica' : 'Buena práctica' }}
            </v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="editingPractice = null">
              <v-icon>close</v-icon>
            </v-btn>
          </v-toolbar>
        </template>
      </GoodPracticeEditSimple>
    </v-dialog>
  </v-card>
</template>